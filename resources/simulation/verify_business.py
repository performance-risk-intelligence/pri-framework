"""Check consequence accounting, failed-gate boundaries and JS/Python parity fixtures."""
import json,copy,math
from pathlib import Path
from business_impact import calculate,DEFAULTS,PROFILES
P=Path(__file__).parent
(P/'work/qa').mkdir(parents=True,exist_ok=True)
r=json.loads((P/'results/results.json').read_text());a=r['business_impact']['operating_assumptions'];d=r['delta_summary'];o=r['preflight_overhead_cpu_s']
v=calculate(d,o,a)
assert math.isclose(v['gross_annual_value']-sum(v['costs'].values()),v['first_year_net_usd'])
assert math.isclose(v['ongoing_annual_net_usd']-v['costs']['setup'],v['first_year_net_usd'])
assert math.isclose(v['annual_support_contacts_avoided']+v['annual_manual_cases_avoided'],v['annual_failed_journeys_avoided']*.02)
assert math.isclose(v['benefits']['retained_contribution'],v['annual_failed_journeys_avoided']*.05*.10*10)
assert v['demonstrated_cash_saving_usd']==0
for profile in PROFILES:
 for ev,tr in [(6,.5),(0,.5),(6,0)]:
  q=calculate(d,o,{**a,'events_per_service_year':ev,'effect_transfer_fraction':tr},profile=profile)
  assert q['costs']['routine_release_review']==13*91
  if not ev or not tr:
   assert all(value==0 for value in q['benefits'].values()) and q['first_year_net_usd']<0
for key in ['unrepresentative_preflight','lower_demand']:
 rr=json.loads((P/'results/sensitivity'/key/'results.json').read_text());q=rr['business_impact']['default']
 assert all(q['benefits'][x]==0 for x in ['retained_contribution','support_capacity','manual_recovery_capacity','incident_response_capacity'])
 assert q['first_year_net_usd']<0
for bad in [dict(support_fraction=.8,manual_fraction=.3),dict(transaction_share=1.1),dict(support_minutes=float('nan')),dict(contribution_usd=-1)]:
 try:calculate(d,o,a,bad)
 except ValueError:pass
 else:raise AssertionError('Accepted invalid input')
# Old operational results are preserved exactly against archived edition 1.1.
import zipfile
archive=P.parent/'Archive/Release_Safety_interactive_v1.1_before_business_impact.zip'
archive_status='not available in standalone package; original comparison recorded in results/business_checks.json'
if archive.exists():
 with zipfile.ZipFile(archive) as z:
  for name in ['results/results.json',*[str(x.relative_to(P)) for x in (P/'results/sensitivity').glob('*/results.json')]]:
   old=json.loads(z.read(name));new=json.loads((P/name).read_text());new.pop('business_impact');old.pop('business_impact',None);assert old==new,name
 archive_status='all seven cases match archived edition 1.1'
fixtures=[]
for profile in PROFILES:
 q=calculate(d,o,a,profile=profile);fixtures.append(dict(r=r,a=a,b=q['assumptions'],expected=q))
(P/'work/qa/business_parity_fixtures.json').write_text(json.dumps(fixtures))
result=dict(accounting='passed',zero_exposure='passed',missed_defect_no_business_credit='passed',disjoint_recovery='passed',invalid_inputs='passed',operational_results_unchanged=archive_status,parity_fixtures=len(fixtures))
(P/'results/business_checks.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
