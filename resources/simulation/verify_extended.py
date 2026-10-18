"""Verify new experiments' real boundaries, GPU work/billing and portfolio accounting."""
import json,math,tempfile
from pathlib import Path
from gpu_simulation import CONFIG,batch_run,weights,assess,experiment as gpu_experiment,economics
from extended_scenarios import summarize_portfolio
def equivalent(a,b):
 if isinstance(a,dict):return a.keys()==b.keys() and all(equivalent(a[k],b[k]) for k in a)
 if isinstance(a,list):return len(a)==len(b) and all(equivalent(x,y) for x,y in zip(a,b))
 if isinstance(a,(int,float)) and not isinstance(a,bool):return math.isclose(a,b,rel_tol=1e-12,abs_tol=1e-7)
 return a==b

P=Path(__file__).parent;root=P/'results/extended'
m=json.loads((root/'moderate/results.json').read_text());p=json.loads((root/'portfolio.json').read_text());g=json.loads((root/'gpu.json').read_text())
assert m['config']['bad_multiplier']==1.2 and len(m['replications'])==8
assert all(not x['bad_release_promoted'] for x in m['preflights'])
assert m['delta_summary']['failed']['mean']==0
assert all(m['business_impact']['default']['benefits'][k]==0 for k in ['retained_contribution','support_capacity','manual_recovery_capacity','incident_response_capacity'])
assert equivalent(summarize_portfolio(p['groups']),{k:p[k] for k in ['first_year','steady_state']})
assert sum(x['count'] for x in p['groups'])==10
assert len({x['result']['config']['seed'] for x in p['groups']})==5
for period in ['first_year','steady_state']:
 q=p[period];assert math.isclose(sum(q['benefits'].values())-sum(q['costs'].values()),q['net_value'])
 assert math.isclose(sum(x['annual_failed_journeys_avoided'] for x in q['groups']),q['avoided_failed_journeys'])
assert p['first_year']['active_workflow_years']==6.25
assert p['first_year']['costs']['setup']==21840
miss=next(x for x in p['groups'] if x['id']=='miss_e')['result'];assert miss['delta_summary']['failed']['mean']==0
for r in g['replications']:
 assert r['candidate_admitted']
 for arm in ['control','pri']:
  a=r[arm];assert a['completed']==a['jobs']==g['config']['jobs']
  assert a['conservation_checksum']==a['jobs']*(a['jobs']-1)//2
  assert a['billed_instance_s']>=a['gpu_busy_s']+a['gpus']*(g['config']['startup_s']+g['config']['shutdown_s'])
  assert a['batches']==math.ceil(a['jobs']/a['batch_size']) and a['retries']==0
  assert a['hourly_completions'][-1]['completed']==a['jobs']
 assert r['billed_instance_s_saved']>0
for mode in ['stop_after_job','fixed_fleet']:
 q=g['economics'][mode];assert equivalent(economics(g,mode=mode),q)
 assert math.isclose(q['gross_annual_compute_reduction_usd']-sum(q['costs'].values()),q['first_year_net_usd'])
assert g['economics']['fixed_fleet']['gross_annual_compute_reduction_usd']==0
assert economics(g,dict(benefit_transfer=0))['gross_annual_compute_reduction_usd']==0
# Partial batches, startup/deadline accounting, equal-size no-gain, and explicit billing minimum.
c={**CONFIG,'jobs':101,'gpus':3,'startup_s':0,'shutdown_s':0,'deadline_s':.01};prefix=weights(101,71,.25)
a=batch_run(prefix,c,4);b=batch_run(prefix,c,8)
assert a['late_jobs']==101 and b['late_jobs']==101
assert a['billed_instance_s']>=180
assert assess(a,a,c)['disposition']=='HOLD_REGRESSION'
assert assess(a,b,c,coverage=.5)['disposition']=='HOLD_EVIDENCE'
assert assess(a,b,c,environment=False)['disposition']=='HOLD_EVIDENCE'
assert assess(a,b,c,memory_fit=False)['disposition']=='HOLD_EVIDENCE'
small={**CONFIG,'jobs':1001,'gpus':4,'preflight_jobs':101,'replications':2}
s=gpu_experiment(small);assert s==gpu_experiment(small)
held=gpu_experiment({**small,'maximum_batch':4})
assert not any(x['candidate_admitted'] for x in held['replications'])
assert all(x['billed_instance_s_saved']==0 for x in held['replications'])
# Exact raw main result regeneration from saved data is separated from financial variations.
result=dict(moderate_gate_and_zero_business_credit='passed',mixed_group_accounting='passed',distinct_seed_streams='passed',shared_costs_not_duplicated='passed',gpu_job_conservation='passed',gpu_partial_batches='passed',gpu_minimum_billing='passed',startup_deadline_included='passed',fixed_fleet_no_bill_reduction='passed',held_gpu_candidate_no_saving='passed',gpu_seed_reproducibility='passed',all_saved_economics_reproduce='passed')
(P/'results/extended_checks.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
