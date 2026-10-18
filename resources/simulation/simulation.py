#!/usr/bin/env python3
"""Discrete-event PRI release-safety experiment. All operational data is modeled.
No cloud calls, user records, employer data, sleeping or network services.
"""
import argparse,csv,hashlib,heapq,json,math,random,statistics,time
from collections import deque
from pathlib import Path
VERSION='1.0.0'
DEFAULT=dict(seed=20261018,replications=12,duration_s=1800,base_rps=40,peak_rps=70,peak_start_s=480,peak_end_s=1080,workers=8,mean_cpu_s=.085,cpu_sigma=.35,bad_multiplier=2.0,release_s=600,fix_s=1200,attempt_timeout_s=.8,journey_deadline_s=2.0,retry_delay_s=.12,max_retries=1,alarm_failure_fraction=.02,alarm_p95_ratio=1.20,alarm_windows=2,rollback_delay_s=300,preflight_s=60,preflight_rps=70,min_coverage=.99,latency_limit_pct=10,failure_limit_pp=1)

def quantile(v,p):
 if not v:return None
 a=sorted(v);i=(len(a)-1)*p;lo=int(i);hi=math.ceil(i);return a[lo]+(a[hi]-a[lo])*(i-lo)
def avg(v):return statistics.mean(v) if v else 0

def workload(cfg,seed,duration=None,constant_rps=None):
 rng=random.Random(seed);d=cfg['duration_s'] if duration is None else duration;out=[];t=0
 # Thinning produces a nonhomogeneous Poisson arrival process; marks are shared across arms.
 high=max(cfg['base_rps'],cfg['peak_rps']) if constant_rps is None else constant_rps
 while True:
  t+=rng.expovariate(high)
  if t>=d:break
  rate=constant_rps if constant_rps is not None else (cfg['peak_rps'] if cfg['peak_start_s']<=t<cfg['peak_end_s'] else cfg['base_rps'])
  if rng.random()>rate/high:continue
  cpu=rng.lognormvariate(math.log(cfg['mean_cpu_s'])-.5*cfg['cpu_sigma']**2,cfg['cpu_sigma'])
  out.append((t,cpu))
 return out

def simulate(cfg,trace,arm='control',constant_multiplier=None,keep_jobs=False):
 """An attempt captures its version at admission. Running timed-out work continues;
 queued timed-out work is cancelled. One retry, same journey, new work item.
 Late completions cannot turn a failed journey into success or count twice.
 """
 d=cfg['duration_s'];heap=[];seq=0;queue=deque();busy=0;cpu=0.;retries=0;started=0;cancelled=0;maxq=0;rollback=None;streak=0;alarm=None
 jobs=[dict(arrival=t,cpu=c,done=False,success=False,latency=None,attempts=0) for t,c in trace]
 attempts=[];minutes=[dict(minute=i,offered=0,completed=0,failed=0,retries=0,cpu_s=0.,latencies=[]) for i in range(math.ceil(d/60))]
 def push(t,kind,payload):
  nonlocal seq
  seq+=1;heapq.heappush(heap,(t,seq,kind,payload))
 def bucket(t):return min(int(t//60),len(minutes)-1)
 def version(t):
  if constant_multiplier is not None:return constant_multiplier,'fixed' if constant_multiplier==1 else 'faulty'
  if t>=cfg['fix_s'] and (arm!='pri' or cfg.get('pri_fix_allowed',False)):return 1.,'corrected'
  if t<cfg['release_s'] or (arm=='pri' and not cfg.get('pri_bad_allowed',False)) or (rollback is not None and t>=rollback):return 1.,'baseline'
  return cfg['bad_multiplier'],'faulty'
 def resolve(jid,t,ok):
  j=jobs[jid]
  if j['done']:return
  j['done']=True;j['success']=ok;j['latency']=t-j['arrival'];b=minutes[bucket(j['arrival'])]
  b['completed' if ok else 'failed']+=1
  if ok:b['latencies'].append(j['latency'])
 def attempt(jid,t):
  nonlocal retries,maxq
  j=jobs[jid]
  if j['done'] or t>=j['arrival']+cfg['journey_deadline_s']:return
  mult,ver=version(t);aid=len(attempts);attempts.append(dict(jid=jid,deadline=min(t+cfg['attempt_timeout_s'],j['arrival']+cfg['journey_deadline_s']),active=True,started=False,cpu=j['cpu']*mult,version=ver))
  j['attempts']+=1
  if j['attempts']>1:retries+=1;minutes[bucket(j['arrival'])]['retries']+=1
  queue.append(aid);maxq=max(maxq,len(queue));push(attempts[aid]['deadline'],'timeout',aid)
 def dispatch(t):
  nonlocal busy,cpu,started,cancelled
  while busy<cfg['workers'] and queue:
   aid=queue.popleft();a=attempts[aid];j=jobs[a['jid']]
   if not a['active'] or j['done'] or t>=a['deadline']:
    a['active']=False;cancelled+=1;continue
   a['started']=True;busy+=1;started+=1;cpu+=a['cpu']
   # Charge modeled executed work across wall-clock buckets, including late work and drain.
   end=t+a['cpu'];cur=t
   while cur<end:
    nxt=min(end,(math.floor(cur/60)+1)*60)
    minutes[bucket(cur)]['cpu_s']+=nxt-cur;cur=nxt
   push(end,'finish',aid)
 for jid,(t,_) in enumerate(trace):
  minutes[bucket(t)]['offered']+=1;push(t,'arrival',jid);push(t+cfg['journey_deadline_s'],'deadline',jid)
 if constant_multiplier is None and (arm=='control' or cfg.get('pri_bad_allowed',False)):
  for t in range(60,int(d)+1,60):push(t,'monitor',None)
 reference_latency=None;last=0;retry_tokens=0.;retry_cap=cfg['peak_rps']*cfg.get('retry_budget_fraction',0)*10
 while heap:
  t,_,kind,x=heapq.heappop(heap);last=t
  if kind=='arrival':
   if 'retry_budget_fraction' in cfg:retry_tokens=min(retry_cap,retry_tokens+cfg['retry_budget_fraction'])
   attempt(x,t)
  elif kind=='retry':attempt(x,t)
  elif kind=='deadline':resolve(x,t,False)
  elif kind=='timeout':
   a=attempts[x];j=jobs[a['jid']]
   if a['active']:
    a['active']=False
    if not j['done']:
     if j['attempts']<=cfg['max_retries'] and t+cfg['retry_delay_s']<j['arrival']+cfg['journey_deadline_s'] and ('retry_budget_fraction' not in cfg or retry_tokens>=1):
      if 'retry_budget_fraction' in cfg:retry_tokens-=1
      push(t+cfg['retry_delay_s'],'retry',a['jid'])
     else:resolve(a['jid'],t,False)
  elif kind=='finish':
   a=attempts[x];busy-=1
   if a['active'] and t<=a['deadline']:resolve(a['jid'],t,True)
   a['active']=False
  elif kind=='monitor':
   # Evaluate the last fully observed arrival cohort, allowing full journey deadline.
   bidx=int(t//60)-2
   if bidx>=0:
    b=minutes[bidx];p95=quantile(b['latencies'],.95)
    if reference_latency is None and b['offered']>=100 and p95 is not None:reference_latency=p95
    severe=b['offered']>=100 and (b['failed']/b['offered']>cfg['alarm_failure_fraction'] or (p95 is not None and reference_latency and p95>reference_latency*cfg['alarm_p95_ratio']))
    streak=streak+1 if severe else 0
    if t>=cfg['release_s'] and alarm is None and streak>=cfg['alarm_windows']:
     alarm=t;rollback=t+cfg['rollback_delay_s']
  dispatch(t)
 assert all(j['done'] for j in jobs)
 assert busy==0 and not queue
 succ=[j['latency'] for j in jobs if j['success']];n=len(jobs);ok=len(succ)
 assert abs(cpu-sum(m['cpu_s'] for m in minutes))<1e-5
 assert cpu<=cfg['workers']*last+1e-5
 timeline=[]
 for b in minutes:
  p=b.pop('latencies');b['p95_ms']=1000*quantile(p,.95) if p else None;b['failure_pct']=100*b['failed']/b['offered'] if b['offered'] else 0;timeline.append(b)
 result=dict(offered=n,completed=ok,failed=n-ok,failure_pct=100*(n-ok)/n if n else 0,p50_ms=1000*quantile(succ,.5) if succ else None,p95_ms=1000*quantile(succ,.95) if succ else None,all_outcome_p95_ms=1000*quantile([j['latency'] for j in jobs],.95) if jobs else None,cpu_s_per_completion=cpu/ok if ok else None,total_journey_s=sum(j['latency'] for j in jobs),success_latency_s=sum(succ),cpu_s=cpu,retries=retries,attempts=len(attempts),started_attempts=started,cancelled_queued_attempts=cancelled,max_queue=maxq,alarm_s=alarm,rollback_s=rollback,drain_end_s=last,timeline=timeline)
 if keep_jobs:result['jobs']=jobs
 return result

def digest(label):return hashlib.sha256(label.encode()).hexdigest()
def gate(base,candidate,cfg,coverage=1.,env_match=True):
 if coverage<cfg['min_coverage'] or not env_match:return dict(disposition='HOLD_EVIDENCE',reason='Coverage or environment mismatch')
 latency=(candidate['p95_ms']/base['p95_ms']-1)*100 if base['p95_ms'] and candidate['p95_ms'] else None
 failure=candidate['failure_pct']-base['failure_pct']
 # This demonstrator uses a per-run practical threshold. Repeated-seed uncertainty is reported separately.
 if latency is None:return dict(disposition='INVESTIGATE',reason='No successful-latency estimate')
 disposition='HOLD_REGRESSION' if latency>cfg['latency_limit_pct'] or failure>cfg['failure_limit_pp'] else 'ELIGIBLE_FOR_REVIEW'
 return dict(disposition=disposition,latency_delta_pct=latency,failure_delta_pp=failure,reason='Observed preflight metrics compared with specified materiality limits')
def authorize(assessment,artifact,now=0,expires=300):
 if assessment['disposition']!='ELIGIBLE_FOR_REVIEW':raise ValueError('Cannot approve held assessment')
 return dict(artifact_digest=digest(artifact),policy_version='demo-policy-1',issued_s=now,expires_s=expires,reviewer='fictional-demo-release-owner',scope='simulation-only')
def promote(approval,artifact,now):return approval['artifact_digest']==digest(artifact) and approval['issued_s']<=now<approval['expires_s'] and approval['scope']=='simulation-only'

def uncertainty(values,seed=87):
 rng=random.Random(seed);n=len(values);samples=[avg([values[rng.randrange(n)] for _ in range(n)]) for _ in range(2000)]
 return dict(mean=avg(values),min=min(values),max=max(values),mean_ci95=[quantile(samples,.025),quantile(samples,.975)])

def economics(deltas,overhead,cfg):
 # All coefficients below are editable planning assumptions, not observed savings or market forecasts.
 a=dict(events_per_service_year=6,releases_per_service_year=52,effect_transfer_fraction=.5,execution_value_per_vcpu_hour=.05,response_person_hours_control=4,response_person_hours_pri=1,loaded_labor_usd_hour=100,setup_hours_per_service=24,annual_maintenance_hours_per_service=12,annual_noncompute_usd_per_service=120)
 cpu_gross=deltas['cpu_s']['mean'];over=overhead['mean'];events=a['events_per_service_year'];tr=a['effect_transfer_fraction'];releases=a['releases_per_service_year']
 annual_cpu=cpu_gross*events*tr-over*releases
 response_credit_eligible=deltas['failed']['mean']>0
 labor_avoided=(a['response_person_hours_control']-a['response_person_hours_pri'])*events*tr*response_credit_eligible
 ongoing=labor_avoided*a['loaded_labor_usd_hour']+annual_cpu/3600*a['execution_value_per_vcpu_hour']-a['annual_maintenance_hours_per_service']*a['loaded_labor_usd_hour']-a['annual_noncompute_usd_per_service']
 first=ongoing-a['setup_hours_per_service']*a['loaded_labor_usd_hour']
 margin=(a['response_person_hours_control']-a['response_person_hours_pri'])*tr*a['loaded_labor_usd_hour']*response_credit_eligible+cpu_gross*tr/3600*a['execution_value_per_vcpu_hour']
 fixed=a['annual_maintenance_hours_per_service']*a['loaded_labor_usd_hour']+a['annual_noncompute_usd_per_service']+over*releases/3600*a['execution_value_per_vcpu_hour']
 scales=[]
 for label,n in [('One service',1),('Organization portfolio',25),('Cross-industry scenario',1000),('Nationwide adoption scenario',10000)]:
  scales.append(dict(label=label,distinct_services=n,annual_failed_journeys_avoided=deltas['failed']['mean']*events*tr*n,annual_retry_attempts_avoided=deltas['retries']['mean']*events*tr*n,annual_journey_hours_recovered=deltas['total_journey_s']['mean']/3600*events*tr*n,annual_net_cpu_hours=annual_cpu/3600*n,annual_response_hours_avoided=labor_avoided*n,first_year_net_usd=first*n,ongoing_annual_net_usd=ongoing*n,fixed_fleet_cash_compute_savings_usd=0))
 return dict(assumptions=a,response_credit_eligible=response_credit_eligible,one_service=dict(annual_net_cpu_hours=annual_cpu/3600,first_year_net_usd=first,ongoing_annual_net_usd=ongoing,ongoing_break_even_events=fixed/margin if margin>0 else None,first_year_break_even_events=(fixed+a['setup_hours_per_service']*a['loaded_labor_usd_hour'])/margin if margin>0 else None),scales=scales,interpretation='Conditional arithmetic for distinct comparable services. Not a forecast, national estimate, measured invoice saving or GDP impact. Response hours are assumptions. Fixed provisioned fleet has zero demonstrated bill reduction.')

def experiment(cfg,out,verbose=True):
 out.mkdir(parents=True,exist_ok=True);replicas=[];preflights=[];overheads=[];diffs={k:[] for k in ['failed','retries','cpu_s','total_journey_s','completed','p95_ms','all_outcome_p95_ms']};representative=None
 for i in range(cfg['replications']):
  seed=cfg['seed']+i
  pcfg=dict(cfg,duration_s=cfg['preflight_s']);pt=workload(pcfg,seed+100000,duration=cfg['preflight_s'],constant_rps=cfg['preflight_rps'])
  baseline=simulate(pcfg,pt,constant_multiplier=1)
  faulty=simulate(pcfg,pt,constant_multiplier=cfg.get('preflight_bad_multiplier',cfg['bad_multiplier']))
  fixed=simulate(pcfg,pt,constant_multiplier=1)
  held=gate(baseline,faulty,cfg,coverage=cfg.get('preflight_coverage',1.));cleared=gate(baseline,fixed,cfg)
  badapproval=authorize(held,'faulty-v1',now=cfg['release_s'],expires=cfg['release_s']+300) if held['disposition']=='ELIGIBLE_FOR_REVIEW' else None
  approval=authorize(cleared,'corrected-v2',now=cfg['fix_s'],expires=cfg['fix_s']+300) if cleared['disposition']=='ELIGIBLE_FOR_REVIEW' else None
  bad_allowed=bool(badapproval and promote(badapproval,'faulty-v1',cfg['release_s']))
  fix_allowed=bool(approval and promote(approval,'corrected-v2',cfg['fix_s']))
  active=dict(cfg,pri_bad_allowed=bad_allowed,pri_fix_allowed=fix_allowed)
  trace=workload(cfg,seed);control=simulate(active,trace,'control');pri=simulate(active,trace,'pri')
  for k in diffs:diffs[k].append(pri[k]-control[k] if k=='completed' else control[k]-pri[k])
  overhead=sum(x['cpu_s'] for x in [baseline,faulty,fixed])+2.;overheads.append(overhead)
  preflights.append(dict(seed=seed,baseline={k:baseline[k] for k in ['offered','failed','p95_ms','cpu_s']},faulty={k:faulty[k] for k in ['offered','failed','p95_ms','cpu_s']},corrected={k:fixed[k] for k in ['offered','failed','p95_ms','cpu_s']},faulty_assessment=held,corrected_assessment=cleared,modeled_analysis_cpu_s=2.,approval=approval,bad_release_promoted=bad_allowed,corrected_release_promoted=fix_allowed))
  replicas.append(dict(seed=seed,control={k:v for k,v in control.items() if k!='timeline'},pri={k:v for k,v in pri.items() if k!='timeline'},preflight_cpu_s=overhead))
  if representative is None:representative=dict(control=control,pri=pri,preflight=preflights[-1])
 deltas={k:uncertainty(v) for k,v in diffs.items()};overhead=uncertainty(overheads)
 net=uncertainty([diffs['cpu_s'][i]-overheads[i] for i in range(cfg['replications'])])
 result=dict(study='PRI queue and release safety discrete-event simulation',version=VERSION,classification='Modeled experiment, not a running-service benchmark or customer outcome',config=cfg,replications=replicas,preflights=preflights,delta_summary=deltas,preflight_overhead_cpu_s=overhead,net_cpu_s_per_incident_including_preflight=net,economics=economics(deltas,overhead,cfg),representative=representative)
 from business_impact import attach
 attach(result)
 (out/'results.json').write_text(json.dumps(result,indent=2)+'\n')
 with (out/'replications.csv').open('w',newline='') as f:
  fields=['seed','arm','offered','completed','failed','failure_pct','p95_ms','all_outcome_p95_ms','cpu_s','cpu_s_per_completion','retries','alarm_s','rollback_s'];w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
  for r in replicas:
   for arm in ['control','pri']:w.writerow(dict(seed=r['seed'],arm=arm,**{k:r[arm][k] for k in fields[2:]}))
 if verbose:print(json.dumps(dict(deltas=deltas,overhead_cpu_s=overhead,net_cpu_s=net,one_service_economics=result['economics']['one_service']),indent=2))
 return result

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',default='results');ap.add_argument('--replications',type=int,default=12);args=ap.parse_args();cfg=dict(DEFAULT,replications=args.replications);experiment(cfg,Path(args.out))
if __name__=='__main__':main()
