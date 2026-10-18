#!/usr/bin/env python3
"""Meaningful conservation, gating, reproducibility and failure-boundary checks."""
import json,tempfile
from pathlib import Path
from simulation import DEFAULT,workload,simulate,gate,authorize,promote,experiment

def run():
 c=dict(DEFAULT,duration_s=120,release_s=30,fix_s=90,peak_start_s=20,peak_end_s=80,base_rps=20,peak_rps=70,rollback_delay_s=10)
 trace=workload(c,42);x=simulate(c,trace,'control',keep_jobs=True)
 assert x['offered']==x['completed']+x['failed']
 assert x['attempts']<=x['offered']*(c['max_retries']+1)
 assert all(j['latency']<=c['journey_deadline_s']+1e-9 for j in x['jobs'])
 assert x['cpu_s']<=c['workers']*x['drain_end_s']
 # Running work which times out is still charged; reporting all outcomes prevents survivor bias.
 stress=dict(c,base_rps=150,peak_rps=150);st=workload(stress,42);z=simulate(stress,st,constant_multiplier=2)
 assert z['failed']>0 and z['cpu_s']>0 and z['all_outcome_p95_ms']>=z['p95_ms']
 # A missing or mismatched evidence set cannot grant release eligibility.
 b=simulate(c,trace,constant_multiplier=1);bad=simulate(c,trace,constant_multiplier=2)
 assert gate(b,b,c,coverage=.7)['disposition']=='HOLD_EVIDENCE'
 assert gate(b,b,c,env_match=False)['disposition']=='HOLD_EVIDENCE'
 held=gate(b,bad,c);assert held['disposition']=='HOLD_REGRESSION'
 try:authorize(held,'bad')
 except ValueError:pass
 else:raise AssertionError('Held assessment was authorized')
 good=gate(b,b,c);a=authorize(good,'fixed',now=20,expires=30)
 assert promote(a,'fixed',20) and not promote(a,'changed',20) and not promote(a,'fixed',30) and not promote(a,'fixed',19)
 # Primary treatment is driven by actual assessment and approval, not an unconditional privileged arm.
 with tempfile.TemporaryDirectory() as td:
  ec=dict(c,replications=2,preflight_s=20,preflight_rps=70)
  r=experiment(ec,Path(td)/'first',verbose=False);rr=experiment(ec,Path(td)/'repeat',verbose=False)
  assert r==rr,'Seeded experiment did not reproduce'
  assert not any(p['bad_release_promoted'] for p in r['preflights'])
  miss=experiment(dict(ec,preflight_bad_multiplier=1),Path(td)/'miss',verbose=False)
  assert all(p['bad_release_promoted'] for p in miss['preflights'])
  assert miss['delta_summary']['failed']['mean']==0,'Unrepresentative preflight incorrectly prevented the modeled failure'
  assert not miss['economics']['response_credit_eligible'],'A missed defect received avoided-response credit'
 return {'conservation':'passed','time_budgets':'passed','timeout_work_charged':'passed','coverage_and_environment_holds':'passed','artifact_and_expiry_binding':'passed','held_assessment_not_approved':'passed','identical_seed_reproduction':'passed','unrepresentative_test_can_miss':'passed'}
if __name__=='__main__':
 result=run();(Path(__file__).parent/'results/checks.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
