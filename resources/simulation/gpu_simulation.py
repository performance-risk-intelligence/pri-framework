#!/usr/bin/env python3
"""Finite, seeded GPU batch scheduler; no GPU, model inference or cloud calls."""
import heapq,random,math,json,statistics
from pathlib import Path
from simulation import uncertainty,authorize,promote
P=Path(__file__).parent
CONFIG=dict(seed=20261018,replications=8,jobs=1000000,gpus=32,current_batch_size=4,candidate_batch_size=8,job_weight_sigma=.25,batch_fixed_s=.2,batch_work_s=2.,batch_exponent=.8,deadline_s=16*3600,startup_s=120,shutdown_s=60,preflight_jobs=1000,maximum_batch=8)
ECON=dict(instance_usd_hour=1.006,runs_year=250,benefit_transfer=.5,validations_year=52,setup_hours=80,maintenance_hours_year=48,review_hours_per_validation=.25,engineering_usd_hour=91,incremental_platform_usd_year=1200,license_usd_year=0)
SOURCES=[dict(title='NVIDIA Triton dynamic batching',url='https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/user_guide/batcher.html',supports='Batch aggregation and workload-specific profiling; no numerical speedup borrowed.'),dict(title='NVIDIA Triton tuning and measurement',url='https://github.com/triton-inference-server/server/blob/main/docs/user_guide/optimization.md',supports='Measure configurations; bigger batches are not a universal improvement.'),dict(title='AWS March 31, 2026 regional GPU case study',url='https://aws.amazon.com/jp/blogs/news/case-study-dentsusoken-unveil/',supports='Published March 2026 g5.xlarge US East N. Virginia on-demand reference $1.006/instance-hour; historical reference, not current quote.'),dict(title='AWS EC2 on-demand billing',url='https://aws.amazon.com/ec2/pricing/on-demand/',supports='Linux per-second billing with 60-second minimum. Idle allocated instances remain chargeable. Excludes storage/network, support, taxes, negotiated discounts.'),dict(title='AWS accelerated instance specifications',url='https://docs.aws.amazon.com/ec2/latest/instancetypes/ac.html',supports='g5.xlarge has one A10G GPU; price is per whole instance, not just GPU.'),dict(title='BLS labor proxy method',url='https://www.bls.gov/news.release/archives/ocwage_04022025.pdf',supports='Engineering wage reference; benefit loading in Business_Impact_Method.md.')]

def weights(n,seed,sigma):
 rng=random.Random(seed);prefix=[0.]
 for _ in range(n):prefix.append(prefix[-1]+rng.lognormvariate(-.5*sigma*sigma,sigma))
 return prefix

def batch_run(prefix,cfg,batch_size,gpus=None):
 n=len(prefix)-1;g=cfg['gpus'] if gpus is None else gpus
 heap=[(cfg['startup_s'],i) for i in range(g)];heapq.heapify(heap);busy=[0.]*g;done=[];late=0;gpu_seconds=0.;checksum=0
 for lo in range(0,n,batch_size):
  hi=min(n,lo+batch_size);size=hi-lo;t,worker=heapq.heappop(heap)
  duration=cfg['batch_fixed_s']+cfg['batch_work_s']*(size**cfg['batch_exponent'])*(prefix[hi]-prefix[lo])/size
  end=t+duration;busy[worker]+=duration;gpu_seconds+=duration;heapq.heappush(heap,(end,worker));done.append((end,size))
  if end>cfg['deadline_s']:late+=size
  # Job-ID sum is a conservation checksum, not a model-accuracy test.
  checksum+=(lo+hi-1)*size//2
 def percentile(p):
  count=0;threshold=math.ceil(n*p)
  for t,size in sorted(done):
   count+=size
   if count>=threshold:return t
  return 0
 billed=sum(max(60,math.ceil(cfg['startup_s']+work+cfg['shutdown_s'])) for work in busy)
 hist=[]
 for hour in range(1,math.ceil(max(t for t,_ in done)/3600)+1):hist.append(dict(hour=hour,completed=sum(size for t,size in done if t<=hour*3600)))
 return dict(jobs=n,completed=n,late_jobs=late,retries=0,batches=len(done),batch_size=batch_size,gpus=g,gpu_busy_s=gpu_seconds,billed_instance_s=billed,elapsed_processing_s=max(t for t,_ in heap)-cfg['startup_s'],p95_completion_s=percentile(.95),conservation_checksum=checksum,hourly_completions=hist)

def assess(base,candidate,cfg,coverage=1.,environment=True,memory_fit=True):
 if coverage<.99 or not environment or not memory_fit:return dict(disposition='HOLD_EVIDENCE',reason='Incomplete workload, environment mismatch or unsupported memory fit')
 saved=1-candidate['gpu_busy_s']/base['gpu_busy_s']
 if candidate['jobs']!=base['jobs'] or candidate['conservation_checksum']!=base['conservation_checksum']:return dict(disposition='HOLD_EVIDENCE',reason='Synthetic job conservation mismatch')
 if saved<.1 or candidate['late_jobs']>base['late_jobs']:return dict(disposition='HOLD_REGRESSION',reason='Insufficient modeled cost improvement or more deadline misses',gpu_work_reduction_fraction=saved)
 return dict(disposition='ELIGIBLE_FOR_REVIEW',reason='Cost and deadline eligibility within synthetic fixture; real model accuracy and memory require validation',gpu_work_reduction_fraction=saved)

def economics(result,overrides=None,mode='stop_after_job'):
 a={**ECON,**(overrides or {})}
 if any(not math.isfinite(v) or v<0 for v in a.values()) or a['benefit_transfer']>1 or a['runs_year']>365:raise ValueError('Invalid GPU annual assumptions')
 if mode not in ['stop_after_job','fixed_fleet']:raise ValueError('Unknown billing mode')
 reps=result['replications'];avg=lambda k:statistics.mean(x[k] for x in reps)
 gross=avg('billed_instance_s_saved')/3600*a['instance_usd_hour']*a['runs_year']*a['benefit_transfer'] if mode=='stop_after_job' else 0
 test=avg('preflight_billed_instance_s')/3600*a['instance_usd_hour']*a['validations_year']
 costs=dict(test_execution=test,routine_review=a['review_hours_per_validation']*a['validations_year']*a['engineering_usd_hour'],maintenance=a['maintenance_hours_year']*a['engineering_usd_hour'],incremental_platform=a['incremental_platform_usd_year'],license=a['license_usd_year'],setup=a['setup_hours']*a['engineering_usd_hour'])
 ongoing=gross-sum(v for k,v in costs.items() if k!='setup')
 return dict(billing_mode=mode,assumptions=a,gross_annual_compute_reduction_usd=gross,costs=costs,first_year_net_usd=ongoing-costs['setup'],ongoing_annual_net_usd=ongoing,annual_gpu_busy_hours_released=avg('gpu_busy_s_saved')/3600*a['runs_year']*a['benefit_transfer'],annual_test_billed_instance_hours=avg('preflight_billed_instance_s')/3600*a['validations_year'],demonstrated_cash_saving_usd=0)

def experiment(cfg=None):
 c={**CONFIG,**(cfg or {})};reps=[]
 for i in range(c['replications']):
  prefix=weights(c['jobs'],c['seed']+i,c['job_weight_sigma']);pp=weights(c['preflight_jobs'],c['seed']+100000+i,c['job_weight_sigma'])
  b=batch_run(pp,c,c['current_batch_size'],1);candidate=batch_run(pp,c,c['candidate_batch_size'],1);repeat=batch_run(pp,c,c['candidate_batch_size'],1)
  assessment=assess(b,candidate,c,coverage=c.get('preflight_coverage',1.),environment=c.get('environment_match',True),memory_fit=c['candidate_batch_size']<=c['maximum_batch']);approval=authorize(assessment,f"gpu-batch{c['candidate_batch_size']}-v1",now=0,expires=300) if assessment['disposition']=='ELIGIBLE_FOR_REVIEW' else None
  admitted=bool(approval and promote(approval,f"gpu-batch{c['candidate_batch_size']}-v1",0));control=batch_run(prefix,c,c['current_batch_size']);pri=batch_run(prefix,c,c['candidate_batch_size'] if admitted else c['current_batch_size'])
  reps.append(dict(seed=c['seed']+i,control=control,pri=pri,assessment=assessment,approval=approval,candidate_admitted=admitted,gpu_busy_s_saved=control['gpu_busy_s']-pri['gpu_busy_s'],billed_instance_s_saved=control['billed_instance_s']-pri['billed_instance_s'],preflight_billed_instance_s=b['billed_instance_s']+candidate['billed_instance_s']+repeat['billed_instance_s'],preflight_gpu_busy_s=b['gpu_busy_s']+candidate['gpu_busy_s']+repeat['gpu_busy_s']))
 r=dict(classification='Synthetic AI-style bulk batch cost experiment; no real GPU throughput, accuracy or invoice measurement',config=c,sources=SOURCES,replications=reps,summary={key:uncertainty([x[key] for x in reps]) for key in ['gpu_busy_s_saved','billed_instance_s_saved','preflight_billed_instance_s']})
 r['economics']={mode:economics(r,mode=mode) for mode in ['stop_after_job','fixed_fleet']}
 r['transfer_sensitivity']=[economics(r,dict(benefit_transfer=f)) for f in [.25,.5,1.]]
 return r
if __name__=='__main__':
 r=experiment();p=P/'results/extended/gpu.json';p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r['economics'],indent=2))
