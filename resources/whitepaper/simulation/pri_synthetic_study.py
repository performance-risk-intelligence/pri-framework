#!/usr/bin/env python3
"""PRI WP 1.0 synthetic evidence study. Generated values, NOT runtime benchmarks.
Python 3.10+ standard library only. Run: python3 pri_synthetic_study.py --out results
Optional --raw exports all generated observations. No network or credentials.
"""
import argparse,csv,hashlib,json,math,platform,random,statistics
from pathlib import Path
SEED=20261017
BATCHES=20
N=500
BOOT=2000
SCENARIOS={
 'baseline':dict(scale=1.0,fail=.01,retry=.03,coverage=1.0,env='E1'),
 'neutral':dict(scale=1.0,fail=.01,retry=.03,coverage=1.0,env='E1'),
 'latency_shift':dict(scale=1.30,fail=.01,retry=.03,coverage=1.0,env='E1'),
 'failure_increase':dict(scale=1.0,fail=.04,retry=.03,coverage=1.0,env='E1'),
 'retry_amplification':dict(scale=1.0,fail=.02,retry=.30,coverage=1.0,env='E1'),
 'revised_candidate':dict(scale=1.02,fail=.008,retry=.03,coverage=1.0,env='E1'),
 'telemetry_gap':dict(scale=1.0,fail=.01,retry=.03,coverage=.70,env='E1'),
 'environment_mismatch':dict(scale=1.20,fail=.01,retry=.03,coverage=1.0,env='E2'),
 'near_boundary':dict(scale=1.107,fail=.01,retry=.03,coverage=1.0,env='E1')}
def q(xs,p):
 s=sorted(xs); k=(len(s)-1)*p;lo=int(k);hi=math.ceil(k);return s[lo]+(s[hi]-s[lo])*(k-lo)
def generate(name,cfg):
 # Reset stream in each scenario: shared exogenous draws yield paired synthetic comparisons.
 rng=random.Random(SEED); rows=[]
 for b in range(BATCHES):
  batch_factor=math.exp(rng.gauss(0,.035))
  for i in range(N):
   base=math.exp(rng.gauss(math.log(450),.30))*batch_factor
   uf,ur,uc=rng.random(),rng.random(),rng.random()
   retries=int(ur<cfg['retry'])
   ok=uf>=cfg['fail'];observed=uc<cfg['coverage']
   # Timeout spends CPU too; elapsed and CPU are separate synthetic quantities.
   elapsed=base*cfg['scale']+retries*250 if ok else 2000.0
   cpu=base*.25*cfg['scale']+retries*90+(0 if ok else 40)
   rows.append(dict(scenario=name,batch=b+1,attempt=i+1,success=ok,observed=observed,latency_ms=elapsed,cpu_ms=cpu,retries=retries,environment=cfg['env']))
 return rows
def batch_stats(rows):
 result=[]
 for b in range(1,BATCHES+1):
  rs=[x for x in rows if x['batch']==b]; obs=[x for x in rs if x['observed']];succ=[x for x in obs if x['success']]
  result.append(dict(batch=b,expected=len(rs),observed=len(obs),success=len(succ),failure=len(obs)-len(succ),p95_ms=q([x['latency_ms'] for x in succ],.95)))
 return result
def compare(a,b):
 # Paired bootstrap of BATCH p95 summaries, not a pooled-p95 confidence interval.
 rng=random.Random(SEED+17);ratios=[];diff=[]
 for _ in range(BOOT):
  idx=[rng.randrange(BATCHES) for _ in range(BATCHES)]
  x=[a[i] for i in idx];y=[b[i] for i in idx]
  ratios.append((statistics.mean(t['p95_ms'] for t in y)/statistics.mean(t['p95_ms'] for t in x)-1)*100)
  diff.append((sum(t['failure'] for t in y)/sum(t['observed'] for t in y)-sum(t['failure'] for t in x)/sum(t['observed'] for t in x))*100)
 return [q(ratios,.025),q(ratios,.975)],[q(diff,.025),q(diff,.975)]
def gate(coverage,env,lat,fail):
 if coverage<.99 or env!='E1':return 'HOLD_DATA'
 if lat[0]>10 or fail[0]>1:return 'HOLD_REGRESSION'
 if lat[1]<=10 and fail[1]<=1:return 'ELIGIBLE_FOR_REVIEW'
 return 'INVESTIGATE'
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',default='results');ap.add_argument('--raw',action='store_true');args=ap.parse_args();out=Path(args.out);out.mkdir(parents=True,exist_ok=True)
 data={k:generate(k,v) for k,v in SCENARIOS.items()}; batches={k:batch_stats(v) for k,v in data.items()};summary=[]
 for name,rows in data.items():
  obs=[r for r in rows if r['observed']];succ=[r for r in obs if r['success']];lat,fail=compare(batches['baseline'],batches[name]);cfg=SCENARIOS[name]
  r=dict(scenario=name,expected=len(rows),observed=len(obs),coverage_pct=100*len(obs)/len(rows),completions=len(succ),failures=len(obs)-len(succ),failure_pct=100*(len(obs)-len(succ))/len(obs),p50_ms=q([x['latency_ms'] for x in succ],.5),p95_ms=q([x['latency_ms'] for x in succ],.95),mean_batch_p95_ms=statistics.mean(x['p95_ms'] for x in batches[name]),latency_delta_ci_pct=lat,failure_delta_ci_pp=fail,cpu_ms_per_completion=sum(x['cpu_ms'] for x in obs)/len(succ),attempts_with_retry_pct=100*sum(x['retries'] for x in obs)/len(obs),within_1000ms_per_observed_pct=100*sum(x['success'] and x['latency_ms']<=1000 for x in obs)/len(obs),decision=gate(len(obs)/len(rows),cfg['env'],lat,fail))
  summary.append(r)
 with (out/'batch_summary.csv').open('w',newline='') as f:
  fields=['scenario','batch','expected','observed','success','failure','p95_ms'];w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
  for name,rs in batches.items():
   for r in rs:w.writerow(dict(scenario=name,**r))
 if args.raw:
  with (out/'generated_observations.csv').open('w',newline='') as f:
   w=csv.DictWriter(f,fieldnames=list(data['baseline'][0]));w.writeheader();w.writerows(x for rs in data.values() for x in rs)
 result=dict(study='PRI WP 1.0 synthetic simulation, not observed service tests',seed=SEED,batches=BATCHES,attempts_per_batch=N,bootstrap_resamples=BOOT,bootstrap_estimand='ratio of mean batch successful-attempt p95 and observed failure-rate difference',python=platform.python_version(),policy=dict(min_coverage=.99,max_latency_delta_pct=10,max_failure_delta_pp=1),scenarios=SCENARIOS,results=summary)
 (out/'summary.json').write_text(json.dumps(result,indent=2)+'\n')
 # Invariants check the illustrative implementation, not scientific validity.
 assert all(r['completions']+r['failures']==r['observed'] for r in summary)
 states={r['scenario']:r['decision'] for r in summary}
 for name in ['latency_shift','failure_increase','retry_amplification']:assert states[name]=='HOLD_REGRESSION',states
 for name in ['telemetry_gap','environment_mismatch']:assert states[name]=='HOLD_DATA',states
 assert states['revised_candidate']=='ELIGIBLE_FOR_REVIEW',states
 (out/'checks.json').write_text(json.dumps(dict(invariants='passed',decisions=states),indent=2)+'\n')
 hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(out.glob('*')) if p.is_file() and p.name!='sha256.json'}
 hashes['../pri_synthetic_study.py']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest();(out/'sha256.json').write_text(json.dumps(hashes,indent=2)+'\n')
 print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
