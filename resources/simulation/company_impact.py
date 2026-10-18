"""Budgeted company scenario over distinct workflows; conditional, not an adoption forecast."""
from business_impact import calculate
DEFAULT_COMPANY=dict(workflows=10,first_year_active_fraction=.625,events_per_workflow_year=2,transfer_fraction=.5,transaction_share=.20,unrecovered_fraction=.10,contribution_usd=20.,support_fraction=.01,support_minutes=6.,manual_fraction=.01,manual_minutes=3.,operations_usd_hour=29.30,engineering_usd_hour=91.,shared_setup_hours=80.,integration_hours_per_workflow=16.,shared_maintenance_hours_year=96.,maintenance_hours_per_workflow_year=2.,routine_review_hours=.25,platform_usd_month=600.,security_usd_year=3000.,license_usd_year=0.)

def company_value(r,c=None):
 import math
 c={**DEFAULT_COMPANY,**(c or {})}
 if any(not isinstance(x,(int,float)) or not math.isfinite(x) or x<0 for x in c.values()):raise ValueError('Company inputs must be finite and nonnegative')
 if c['workflows']<1 or c['workflows']%1 or c['events_per_workflow_year']>52:raise ValueError('Use whole workflows and no more than 52 qualifying episodes/year')
 if c['first_year_active_fraction']>1 or c['transfer_fraction']>1:raise ValueError('Exposure fractions must be 0–1')
 a={**r['business_impact']['operating_assumptions'],'events_per_service_year':c['events_per_workflow_year'],'effect_transfer_fraction':c['transfer_fraction'],'loaded_labor_usd_hour':c['engineering_usd_hour']}
 b={k:c[k] for k in ['transaction_share','unrecovered_fraction','contribution_usd','support_fraction','support_minutes','manual_fraction','manual_minutes','operations_usd_hour','routine_review_hours']}
 q=calculate(r['delta_summary'],r['preflight_overhead_cpu_s'],a,b)
 def year(fraction,setup):
  active=c['workflows']*fraction
  benefits={k:v*active for k,v in q['benefits'].items()}
  # Only test CPU and routine review follow active exposure; full-year shared budgets and maintenance are conservative.
  costs=dict(testing=q['costs']['release_testing']*active,routine_review=c['routine_review_hours']*52*active*c['engineering_usd_hour'],maintenance=(c['shared_maintenance_hours_year']+c['maintenance_hours_per_workflow_year']*c['workflows'])*c['engineering_usd_hour'],platform=c['platform_usd_month']*12,security=c['security_usd_year'],license=c['license_usd_year'],setup=(c['shared_setup_hours']+c['integration_hours_per_workflow']*c['workflows'])*c['engineering_usd_hour'] if setup else 0)
  gross=sum(benefits.values());total_cost=sum(costs.values())
  return dict(active_workflow_years=active,credited_incident_equivalents=active*c['events_per_workflow_year']*c['transfer_fraction'],avoided_failed_journeys=q['annual_failed_journeys_avoided']*active,retained_transactions=q['annual_lost_transactions_prevented']*active,support_contacts=q['annual_support_contacts_avoided']*active,manual_recovery_cases=q['annual_manual_cases_avoided']*active,support_hours=q['annual_support_hours']*active,manual_recovery_hours=q['annual_manual_recovery_hours']*active,incident_response_hours=q['annual_incident_response_hours']*active,benefits=benefits,costs=costs,gross_benefit=gross,total_cost=total_cost,net_value=gross-total_cost,benefit_cost_ratio=gross/total_cost if total_cost else None,demonstrated_cash_saving_usd=0)
 return dict(classification='Illustrative company budget and conditional consequence projection, not measured company savings',assumptions=c,first_year=year(c['first_year_active_fraction'],True),steady_state=year(1,False))
