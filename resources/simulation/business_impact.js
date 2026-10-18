function businessValue(r,a,b){
 const events=a.events_per_service_year*a.effect_transfer_fraction;
 const failures=Math.max(0,r.delta_summary.failed.mean)*events;
 const lost=failures*b.transaction_share*b.unrecovered_fraction,contacts=failures*b.support_fraction,manual=failures*b.manual_fraction;
 const supportHours=contacts*b.support_minutes/60,manualHours=manual*b.manual_minutes/60;
 const responseHours=(a.response_person_hours_control-a.response_person_hours_pri)*events*(r.delta_summary.failed.mean>0);
 const benefits={retained_contribution:lost*b.contribution_usd,support_capacity:supportHours*b.operations_usd_hour,manual_recovery_capacity:manualHours*b.operations_usd_hour,incident_response_capacity:responseHours*a.loaded_labor_usd_hour,production_compute:r.delta_summary.cpu_s.mean*events/3600*a.execution_value_per_vcpu_hour};
 const costs={release_testing:r.preflight_overhead_cpu_s.mean*a.releases_per_service_year/3600*a.execution_value_per_vcpu_hour,routine_release_review:b.routine_review_hours*a.releases_per_service_year*a.loaded_labor_usd_hour,maintenance:a.annual_maintenance_hours_per_service*a.loaded_labor_usd_hour,noncompute:a.annual_noncompute_usd_per_service,setup:a.setup_hours_per_service*a.loaded_labor_usd_hour};
 const gross=Object.values(benefits).reduce((x,y)=>x+y,0),ongoing=gross-Object.entries(costs).filter(([k])=>k!=='setup').reduce((x,[,y])=>x+y,0);
 return {assumptions:b,annual_failed_journeys_avoided:failures,annual_lost_transactions_prevented:lost,annual_support_contacts_avoided:contacts,annual_manual_cases_avoided:manual,annual_support_hours:supportHours,annual_manual_recovery_hours:manualHours,annual_incident_response_hours:responseHours,benefits,costs,gross_annual_value:gross,first_year_net_usd:ongoing-costs.setup,ongoing_annual_net_usd:ongoing,demonstrated_cash_saving_usd:0};
}
