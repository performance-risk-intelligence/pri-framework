"""Conditional business consequences of executed outcomes; no business rates are measured."""
import math
SOURCES=[
 dict(id='bls-wages',url='https://www.bls.gov/news.release/archives/ocwage_04022025.pdf',title='BLS May 2024 occupational wages (released April 2, 2025)',facts='Median hourly wages: customer service representatives $20.59; software developers $63.98. Historical national reference, not an Irvine quote.'),
 dict(id='bls-benefits',url='https://www.bls.gov/news.release/archives/ecec_06132025.pdf',title='BLS March 2025 employer compensation (released June 13, 2025)',facts='Private industry total compensation $45.38/hour versus wages $31.89/hour. Cross-occupation loading proxy 45.38/31.89, not occupation-specific overhead.'),
 dict(id='sre-response',url='https://sre.google/workbook/incident-response/',title='Google SRE Workbook: Incident Response',facts='Separates coordination, communication and operational response. Supports task separation, not the assumed hours or PRI savings.'),
 dict(id='finops-units',url='https://www.finops.org/framework/capabilities/unit-economics/',title='FinOps Foundation: Unit Economics',facts='Supports relating cost to business units. Does not validate this scenario, loss rates or projected savings.')]
DEFAULTS=dict(transaction_share=.05,unrecovered_fraction=.10,contribution_usd=10.,support_fraction=.01,support_minutes=6.,manual_fraction=.01,manual_minutes=3.,operations_usd_hour=29.30,routine_review_hours=.25)
PROFILES={
 'no_business':dict(label='No business consequences priced',transaction_share=0,support_fraction=0,manual_fraction=0),
 'low':dict(label='Low consequence',transaction_share=.02,unrecovered_fraction=.05,contribution_usd=5,support_fraction=.005,support_minutes=4,manual_fraction=.005,manual_minutes=2),
 'base':dict(label='Reference transaction scenario'),
 'high':dict(label='Higher consequence',transaction_share=.10,unrecovered_fraction=.20,contribution_usd=15,support_fraction=.02,support_minutes=8,manual_fraction=.02,manual_minutes=5),
 'public':dict(label='Noncommercial workflow',transaction_share=0)}

def calculate(deltas,overhead,a,overrides=None,profile='base'):
 b={**DEFAULTS,**{k:v for k,v in PROFILES[profile].items() if k!='label'},**(overrides or {})}
 for k,v in b.items():
  if not isinstance(v,(int,float)) or not math.isfinite(v) or v<0:raise ValueError('Invalid business assumption: '+k)
 for k in ['transaction_share','unrecovered_fraction','support_fraction','manual_fraction']:
  if b[k]>1:raise ValueError('Fraction above one: '+k)
 if b['support_fraction']+b['manual_fraction']>1:raise ValueError('Support and manual recovery populations must be disjoint')
 events=a['events_per_service_year']*a['effect_transfer_fraction'];failed=max(0,deltas['failed']['mean'])*events
 lost=failed*b['transaction_share']*b['unrecovered_fraction'];contacts=failed*b['support_fraction'];manual=failed*b['manual_fraction']
 support_hours=contacts*b['support_minutes']/60;manual_hours=manual*b['manual_minutes']/60
 response_hours=(a['response_person_hours_control']-a['response_person_hours_pri'])*events*(deltas['failed']['mean']>0)
 items=dict(retained_contribution=lost*b['contribution_usd'],support_capacity=support_hours*b['operations_usd_hour'],manual_recovery_capacity=manual_hours*b['operations_usd_hour'],incident_response_capacity=response_hours*a['loaded_labor_usd_hour'],production_compute=deltas['cpu_s']['mean']*events/3600*a['execution_value_per_vcpu_hour'])
 costs=dict(release_testing=overhead['mean']*a['releases_per_service_year']/3600*a['execution_value_per_vcpu_hour'],routine_release_review=b['routine_review_hours']*a['releases_per_service_year']*a['loaded_labor_usd_hour'],maintenance=a['annual_maintenance_hours_per_service']*a['loaded_labor_usd_hour'],noncompute=a['annual_noncompute_usd_per_service'],setup=a['setup_hours_per_service']*a['loaded_labor_usd_hour'])
 gross=sum(items.values());ongoing=gross-sum(v for k,v in costs.items() if k!='setup');first=ongoing-costs['setup']
 return dict(profile=profile,assumptions=b,annual_failed_journeys_avoided=failed,annual_lost_transactions_prevented=lost,annual_support_contacts_avoided=contacts,annual_manual_cases_avoided=manual,annual_support_hours=support_hours,annual_manual_recovery_hours=manual_hours,annual_incident_response_hours=response_hours,benefits=items,costs=costs,gross_annual_value=gross,first_year_net_usd=first,ongoing_annual_net_usd=ongoing,demonstrated_cash_saving_usd=0)

def attach(result):
 a={**result['economics']['assumptions'],'loaded_labor_usd_hour':91.}
 # Preserve the original resource-only calculation verbatim for audit; use its original assumptions there.
 result['business_impact']=dict(version='1.0',classification='Conditional consequence overlay, not observed business outcomes',sources=SOURCES,profiles=PROFILES,operating_assumptions=a,default=calculate(result['delta_summary'],result['preflight_overhead_cpu_s'],a),scenarios={k:calculate(result['delta_summary'],result['preflight_overhead_cpu_s'],a,profile=k) for k in PROFILES})
