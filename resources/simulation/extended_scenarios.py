#!/usr/bin/env python3
"""Executed moderate case and independently configured mixed-workflow portfolio."""
import json
from pathlib import Path
from simulation import DEFAULT,experiment
from business_impact import calculate
from company_impact import DEFAULT_COMPANY
P=Path(__file__).parent
GROUPS=[
 dict(id='commercial_a',name='Commercial intake A · distinct customer population',count=2,active_fraction=.75,events=2,changes=dict(bad_multiplier=1.5),business=dict(transaction_share=.5,unrecovered_fraction=.1,contribution_usd=20)),
 dict(id='portal_b',name='Customer portal B · moderate regression',count=3,active_fraction=.75,events=3,changes=dict(bad_multiplier=1.2),business=dict(transaction_share=0,support_fraction=.005,manual_fraction=.005)),
 dict(id='backoffice_c',name='Back-office C · lower demand',count=2,active_fraction=.5,events=2,changes=dict(base_rps=20,peak_rps=35,bad_multiplier=1.35),business=dict(transaction_share=0,support_fraction=.005,manual_fraction=.02,manual_minutes=4)),
 dict(id='commercial_d',name='Commercial intake D · stronger existing controls',count=2,active_fraction=.5,events=1,changes=dict(rollback_delay_s=0,retry_budget_fraction=.1),business=dict(transaction_share=.25,unrecovered_fraction=.05,contribution_usd=15)),
 dict(id='miss_e',name='Submission E · unrepresentative preflight',count=1,active_fraction=.5,events=2,changes=dict(preflight_bad_multiplier=1),business=dict(transaction_share=0))]

def summarize_portfolio(groups):
 c=DEFAULT_COMPANY;out={}
 for period in ['first_year','steady_state']:
  values=[]
  for g in groups:
   r=g['result'];a={**r['business_impact']['operating_assumptions'],'events_per_service_year':g['events'],'effect_transfer_fraction':.5};q=calculate(r['delta_summary'],r['preflight_overhead_cpu_s'],a,g['business']);active=g['count']*(g['active_fraction'] if period=='first_year' else 1)
   values.append(dict(id=g['id'],name=g['name'],count=g['count'],active_workflow_years=active,annual_failed_journeys_avoided=q['annual_failed_journeys_avoided']*active,annual_support_hours=q['annual_support_hours']*active,annual_manual_recovery_hours=q['annual_manual_recovery_hours']*active,annual_incident_response_hours=q['annual_incident_response_hours']*active,benefits={k:v*active for k,v in q['benefits'].items()},testing_cost=q['costs']['release_testing']*active))
  active=sum(g['active_workflow_years'] for g in values);n=sum(g['count'] for g in values);benefits={k:sum(g['benefits'][k] for g in values) for k in values[0]['benefits']}
  costs=dict(testing=sum(g['testing_cost'] for g in values),routine_review=active*52*c['routine_review_hours']*c['engineering_usd_hour'],maintenance=(c['shared_maintenance_hours_year']+n*c['maintenance_hours_per_workflow_year'])*c['engineering_usd_hour'],platform=c['platform_usd_month']*12,security=c['security_usd_year'],license=c['license_usd_year'],setup=(c['shared_setup_hours']+n*c['integration_hours_per_workflow'])*c['engineering_usd_hour'] if period=='first_year' else 0)
  gross=sum(benefits.values());total=sum(costs.values());out[period]=dict(groups=values,active_workflow_years=active,avoided_failed_journeys=sum(g['annual_failed_journeys_avoided'] for g in values),benefits=benefits,costs=costs,gross_benefit=gross,total_cost=total,net_value=gross-total)
 return out

def run():
 root=P/'results/extended';root.mkdir(parents=True,exist_ok=True)
 moderate=experiment(dict(DEFAULT,replications=8,bad_multiplier=1.2),root/'moderate',False)
 groups=[]
 for group_index,spec in enumerate(GROUPS):
  print('Executing portfolio group '+spec['id'],flush=True)
  r=experiment(dict(DEFAULT,seed=DEFAULT['seed']+(group_index+1)*10000,replications=8,**spec['changes']),root/spec['id'],False)
  groups.append({**spec,'result':r})
 portfolio=dict(classification='Independent synthetic workflow groups; financial aggregation is conditional and does not model cross-workflow dependencies',groups=groups,assumptions=dict(company_budget=DEFAULT_COMPANY,transfer_fraction=.5,source='Business_Impact_Method.md and Company_Deployment_Method.md; group rates are assumptions'),**summarize_portfolio(groups))
 (root/'portfolio.json').write_text(json.dumps(portfolio,indent=2)+'\n')
 print(json.dumps(dict(moderate_avoided_failures=moderate['delta_summary']['failed']['mean'],portfolio_first_year=portfolio['first_year']['net_value'],portfolio_steady_state=portfolio['steady_state']['net_value']),indent=2))
if __name__=='__main__':run()
