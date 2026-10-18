import json,math
from pathlib import Path
from company_impact import company_value
P=Path(__file__).parent;r=json.loads((P/'results/results.json').read_text());v=company_value(r);fixtures=[]
assert v['first_year']['active_workflow_years']==5*9/12+5*6/12
assert v['first_year']['costs']['setup']==240*91
assert v['first_year']['costs']['maintenance']==116*91
assert v['first_year']['costs']['routine_review']==81.25*91
assert v['steady_state']['costs']['routine_review']==130*91
for period in ['first_year','steady_state']:
 q=v[period];assert math.isclose(sum(q['benefits'].values())-sum(q['costs'].values()),q['net_value']);assert q['demonstrated_cash_saving_usd']==0
for changes in [{},{'transfer_fraction':0},{'first_year_active_fraction':0},{'contribution_usd':0},{'license_usd_year':5000},{'workflows':1}]:
 q=company_value(r,changes);fixtures.append(dict(r=r,c=q['assumptions'],expected=q))
 if changes.get('transfer_fraction')==0:assert q['first_year']['gross_benefit']==0 and q['first_year']['net_value']<0
 if changes.get('first_year_active_fraction')==0:assert q['first_year']['gross_benefit']==0 and q['first_year']['costs']['setup']>0
 if 'license_usd_year' in changes:assert math.isclose(v['first_year']['net_value']-q['first_year']['net_value'],5000)
for case in ['unrepresentative_preflight','lower_demand']:
 rr=json.loads((P/'results/sensitivity'/case/'results.json').read_text());q=company_value(rr);fixtures.append(dict(r=rr,c=q['assumptions'],expected=q))
 for period in ['first_year','steady_state']:
  assert q[period]['net_value']<0
  assert all(q[period]['benefits'][k]==0 for k in ['retained_contribution','support_capacity','manual_recovery_capacity','incident_response_capacity'])
for bad in [{'workflows':1.5},{'transfer_fraction':1.1},{'support_fraction':.6,'manual_fraction':.6},{'events_per_workflow_year':53},{'platform_usd_month':float('nan')}]:
 try:company_value(r,bad)
 except ValueError:pass
 else:raise AssertionError('Invalid company input accepted')
(P/'work/qa').mkdir(parents=True,exist_ok=True);(P/'work/qa/company_parity.json').write_text(json.dumps(fixtures));result=dict(rollout_exposure='passed',shared_cost_accounting='passed',zero_exposure='passed',license_cost_sensitivity='passed',failure_boundaries='passed',invalid_inputs='passed',parity_fixtures=len(fixtures));(P/'results/company_checks.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
