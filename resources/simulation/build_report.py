#!/usr/bin/env python3
from pathlib import Path
import json,statistics,hashlib,zipfile
P=Path(__file__).parent;R=json.loads((P/'results/results.json').read_text());S=json.loads((P/'results/sensitivity.json').read_text())
means={a:{k:statistics.mean(r[a][k] for r in R['replications']) for k in ['offered','completed','failed','failure_pct','p95_ms','all_outcome_p95_ms','cpu_s','cpu_s_per_completion','retries']} for a in ['control','pri']}
cases={}
for row in S:
 key=row['case'].lower().replace(' ','_');rr=json.loads((P/'results/sensitivity'/key/'results.json').read_text());mm={arm:{k:statistics.mean(x[arm][k] for x in rr['replications']) for k in means[arm]} for arm in ['control','pri']};cases[key]=dict(results=rr,means=mm)
from company_impact import company_value
C=company_value(R)
(P/'results/company_impact.json').write_text(json.dumps(C,indent=2)+'\n')
moderate=json.loads((P/'results/extended/moderate/results.json').read_text())
portfolio=json.loads((P/'results/extended/portfolio.json').read_text())
gpu=json.loads((P/'results/extended/gpu.json').read_text())
for key,rr in [('moderate',moderate),*[(('portfolio_'+g['id']),g['result']) for g in portfolio['groups']]]:
 mm={arm:{k:statistics.mean(x[arm][k] for x in rr['replications']) for k in means[arm]} for arm in ['control','pri']}
 cases[key]=dict(results=rr,means=mm)
D=dict(results=R,sensitivity=S,means=means,cases=cases,company=C,extended=dict(moderate=moderate,portfolio=portfolio,gpu=gpu))
(P/'results/dashboard_data.json').write_text(json.dumps(D,indent=2)+'\n')
f=lambda x:f'{x:,.1f}'
d=R['delta_summary'];e=R['economics'];a=e['assumptions'];nr=R['net_cpu_s_per_incident_including_preflight']
report=f'''# PRI release safety simulation

Version 1.4 • October 18, 2026 • Generated operational scenario executed by a discrete-event engine

## Executive finding

In a deliberately adverse 30-minute fictional service episode, PRI's representative preflight test holds a faulty release, retains the baseline, and admits the corrected artifact after a simulated owner review. Across 12 paired random replications, this avoids an average of **{f(d['failed']['mean'])} failed journeys** and **{f(d['retries']['mean'])} retry attempts**. Production work uses **{f(d['cpu_s']['mean'])} fewer modeled CPU seconds**, while completing more work. All figures describe the model; they are not observations from an application, customer, employer or national infrastructure.

Including three preflight runs and an explicit two-CPU-second analysis allowance, total work is **{f(-nr['mean'])} CPU seconds higher** in this episode. The business consequence overlay projects **${R['business_impact']['default']['first_year_net_usd']:,.2f} first-year net economic value** and **${R['business_impact']['default']['ongoing_annual_net_usd']:,.2f} ongoing annual value** under the reference assumptions. This includes retained contribution, support/recovery capacity and all-release review costs. Rates and durations are scenario assumptions; BLS supports the labor-cost proxy only.

## Realistic operating mechanism

The fictional journey is submission to a usable digital-service result. An eight-worker, first-come-first-served system processes requests. Arrivals follow a piecewise Poisson process: 40 requests per second normally and 70 during Minutes 8–18. Each request has lognormally distributed CPU work with a mean of 85 milliseconds and log standard deviation 0.35. A faulty release at Minute 10 duplicates an expensive transformation, doubling its work. These coefficients are design assumptions, not benchmark measurements.

Each attempt times out after 0.8 seconds, at most one retry follows after 0.12 seconds, and the journey deadline is two seconds. Running work continues after timeout and is charged. Expired queued work is cancelled before execution. A late completion cannot count as a successful journey, and no journey can complete twice. There is one shared CPU queue; network calls, database contention, autoscaling, cache dynamics and output correctness are outside this model.

The existing-process comparator has monitoring and rollback. It evaluates completed one-minute arrival cohorts with a one-minute observation lag, alerts after two bad windows, then has an assumed five-minute operational rollback delay. A bad window exceeds a 2 percent failure rate or a 20 percent successful-p95 increase over its initial reference. Thus it represents a particular process without a representative loaded preflight, not every organization operating without PRI.

The corrected artifact restores the original per-request work; it does not magically outperform the baseline. Its availability at Minute 20 is identical in both arms. The model assumes an engineer removes the duplicate transformation. PRI identifies and governs the failure; it does not autonomously repair arbitrary software. Remediation effort common to both arms cancels in the incremental comparison.

## PRI implemented in the experiment

A baseline and faulty candidate each receive a separate 60-second, 70-request-per-second preflight under the same generated inputs. A practical rule checks at least 99 percent evidence coverage, matching environment, no more than 10 percent p95 degradation and no more than a one-percentage-point failure increase. A breach holds the candidate. The production simulator actually consumes the resulting authorization decision; it does not grant the PRI arm unconditional protection.

The engineer's corrected candidate repeats the preflight. The demo owner may authorize only an eligible assessment. Artifact digest and expiry checks bind that authorization to the corrected candidate. Changed and expired approvals fail verification. These are simulated identities and in-process controls, not an identity-backed production authorization service. The normal and corrected implementations intentionally have identical service work; their equality is not a false-positive study.

The executable rule uses per-run thresholds. Twelve independent seeded replications evaluate this defined case; a paired bootstrap of replication-level differences provides intervals for the mean under this generating process. The rule is not a trained predictor, and this experiment does not establish detection accuracy, calibration or controlled false-positive rates. Equivalent existing preflight controls could prevent this defect too. This is a demonstration of PRI's integration and evidence workflow, not proof of exclusive capability or superiority over mature SRE practice.

## Results per 30-minute episode

| Metric | Existing process | PRI production | Difference |
| --- | ---: | ---: | ---: |
'''
rows=[('Offered journeys','offered',''),('Completed journeys','completed','more completed'),('Failed journeys','failed','avoided failures'),('Failure percentage','failure_pct','percentage points'),('Retry attempts','retries','avoided retries'),('Production CPU seconds','cpu_s','less production work'),('CPU seconds per completion','cpu_s_per_completion','efficiency per usable result'),('Successful-only p95 milliseconds','p95_ms','survivor-sensitive'),('All-outcome p95 milliseconds','all_outcome_p95_ms','time to completion or final failure')]
for label,k,note in rows:report+=f"| {label} | {means['control'][k]:,.3f} | {means['pri'][k]:,.3f} | {note} |\n"
report+=f'''
Values are means of the per-replication statistics, not pooled quantiles. Offered work is identical within each pair. Production CPU includes work spent on failures and late attempts. Three preflights consume {f(R['preflight_overhead_cpu_s']['mean'])} CPU seconds including the two-second analysis allowance. The net episode change includes that overhead; retaining fixed capacity demonstrates no reduction in the cloud invoice.

The 95 percent bootstrap interval for mean avoided failures is {f(d['failed']['mean_ci95'][0])} to {f(d['failed']['mean_ci95'][1])}. For net CPU saving after preflight it is {f(nr['mean_ci95'][0])} to {f(nr['mean_ci95'][1])} seconds; both endpoints are negative. These intervals describe random variability within the specified simulation. They exclude uncertainty about real demand, defect types, behavior, test representativeness and adoption.

**Why successful-only p95 appears slightly worse with PRI.** Many requests disappear into failures in the overloaded comparator. Its successful requests therefore form a different, more favorable subset. PRI completes the peak-load requests too. Failure rate and all-outcome time expose this survivor effect; successful latency alone would mislead. All-outcome time is time to a usable result or final failure, not successful-latency quality. Failed users' later retries outside the modeled journey are not estimated.

## Sensitivity and limits

| Changed assumption | Mean failed journeys avoided | Net CPU seconds saved after testing | Lesson |
| --- | ---: | ---: | --- |
'''
lessons={'Fast incident rollback':'Rollback can leave retry-driven congestion until demand drops.','Fast rollback and retry budget':'A stronger existing process reduces PRI incremental benefit.','Lower demand':'No failed journeys are prevented; the benefit is bounded resource/latency improvement.','Slow incident rollback':'Longer exposure can increase the value of prevention.','Unrepresentative preflight':'The hidden defect is missed; both arms suffer the same production outcome.','Missing preflight records':'The evidence hold retains baseline; it is not a prediction of a defect.'}
for row in S:report+=f"| {row['case']} | {row['failed_journeys_avoided']['mean']:,.1f} | {row['net_cpu_s_including_preflight']['mean']:,.1f} | {lessons[row['case']]} |\n"
report+='''
Sensitivity cases use four replications each. These selected tests are mechanisms and boundaries, not a representative defect distribution. Shared configuration errors, biased fixtures, correlated failures and emergency bypasses could change the result. The model contains no direct benefit for national security, clinical efficacy, vehicle safety or individual eligibility decisions.

'''
b=R['business_impact']['default']
report+='\n'+(P/'Business_Impact_Method.md').read_text()+'\n'
report+='\n### Consequence projections for the primary executed case\n\n| Assumption scenario | Gross annual value | First-year net | Ongoing net |\n| --- | ---: | ---: | ---: |\n'
for key,q in R['business_impact']['scenarios'].items():
 report+=f"| {R['business_impact']['profiles'][key]['label']} | ${q['gross_annual_value']:,.2f} | ${q['first_year_net_usd']:,.2f} | ${q['ongoing_annual_net_usd']:,.2f} |\n"
report+='\n### Reference scenario annual benefit and cost breakdown\n\n| Item | Value |\n| --- | ---: |\n'
for key,value in b['benefits'].items():report+=f"| {key.replace('_',' ')} | ${value:,.2f} |\n"
for key,value in b['costs'].items():report+=f"| {key.replace('_',' ')} | −${value:,.2f} |\n"
report+=f"\nFirst-year net: **${b['first_year_net_usd']:,.2f}**. Ongoing annual net: **${b['ongoing_annual_net_usd']:,.2f}**. These are conditional economic values, not verified cash savings.\n"
report+='\n### Illustrative multiplication of the reference scenario\n\n| Distinct non-overlapping systems | First-year net | Ongoing annual net |\n| ---: | ---: | ---: |\n'
for count in [1,25,1000,10000]:report+=f"| {count:,} | ${b['first_year_net_usd']*count:,.0f} | ${b['ongoing_annual_net_usd']*count:,.0f} |\n"
report+="\nThese counts do not estimate adoption or national savings. Costs are replicated per system without economies of scale, and no overlapping transactions may be counted.\n"
report+=f'''
## Reproduction and verification

Run Python 3.10 or later, standard library only, from this folder:

    python3 simulation.py --out results
    python3 verify.py
    python3 sensitivity.py
    python3 verify_business.py
    python3 verify_company.py
    python3 extended_scenarios.py
    python3 gpu_simulation.py
    python3 verify_extended.py
    python3 build_report.py

The reference run uses 12 seeds beginning at 20261018; each seed supplies identical arrivals and per-request work marks to both arms. Preflight uses a separate shared seed stream. The report retains results, per-replication CSV, minute-level representative traces, gate findings and the assumption dictionary. Float arithmetic can differ across runtimes; compare numerical tolerances and semantic outcomes rather than asserting byte identity across all systems.

Verification covers outcome conservation, deadlines, bounded attempts, CPU accounting, evidence holds, refused approval of a held candidate, digest/expiry binding, repeatability with the same seeds, and an unrepresentative preflight that actually admits the harmful release. The dashboard replays saved results; changing annual assumptions recalculates arithmetic rather than rerunning the event engine. The downloadable source is the route to a new workload experiment.

## Relationship to PRI and the public paper

This is a new dated artifact accompanying White Paper Version 1.2. It extends the earlier generated-summary study with explicit arrivals, resource contention, timeout/retry feedback, a monitored rollback comparator and decisions consumed by a simulated release workflow. It preserves the four pillars and incremental roadmap. It does not retrospectively establish readiness, customer adoption or deployment at filing. No private evidence, customer identity, LOI, financial forecast or employer measurement is used. Publication remains separate from local preparation.

## Interactive edition 1.4

The updated dashboard reuses the public website stylesheet and adds executed-scenario selection, linked fictional incident/control context, proposed follow-up controls, a session-only mock review log and a JSON evidence export. Selections and mock reviews never change operational results. The gross monthly-equivalent opportunity is derived from the same annual assumptions and is shown separately from net value. Blank economic inputs produce unavailable results rather than zero. The event engine and primary experiment remain Version 1.0.0. An animated six-step CI/CD integration story and completion/compute charts explain the selected case. The incident-memory illustration filters eight fictional reports by journey, environment, confirmed mechanism and a 365-day window, then deduplicates incident IDs to obtain two relevant incidents. Those teaching records are exported separately and never tune the gate or the economic results.

## Technical sources

The overloaded queue and retry mechanism is informed by [Google SRE Addressing Cascading Failures](https://sre.google/sre-book/addressing-cascading-failures/) and [Handling Overload](https://sre.google/sre-book/handling-overload/). These discuss retry amplification, overload and mitigation; their experience does not validate the coefficients here. [AWS Retry with backoff](https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/retry-backoff.html) informs retry-policy scoping. These are conceptual sources, not PRI endorsements or measured savings inputs. Labor-cost proxies use the dated BLS sources in the business method. Consequence rates, durations, recurrence and costs remain explicit assumptions.
'''
report+='\n'+(P/'Company_Deployment_Method.md').read_text()+'\n'
report+='\n| Company item | Year 1 | Full deployment annually |\n| --- | ---: | ---: |\n'
for group in ['benefits','costs']:
 for k in C['first_year'][group]:
  sign=1 if group=='benefits' else -1
  report+=f"| {k.replace('_',' ')} | ${C['first_year'][group][k]*sign:,.2f} | ${C['steady_state'][group][k]*sign:,.2f} |\n"
report+=f"\nCompany net economic value: Year 1 **${C['first_year']['net_value']:,.2f}**; full-deployment annual **${C['steady_state']['net_value']:,.2f}**.\n"
report+='\n'+(P/'Extended_Experiments_Method.md').read_text()+'\n'
report+='\n## Extended experiment financial results\n\n| Experiment | Year 1 net | Ongoing annual net |\n| --- | ---: | ---: |\n'
for label,q in [('Moderate CPU',moderate['business_impact']['default']),('AI/GPU stop after job',gpu['economics']['stop_after_job']),('AI/GPU fixed fleet',gpu['economics']['fixed_fleet'])]:
 report+=f"| {label} | ${q['first_year_net_usd']:,.2f} | ${q['ongoing_annual_net_usd']:,.2f} |\n"
report+=f"| Mixed portfolio | ${portfolio['first_year']['net_value']:,.2f} | ${portfolio['steady_state']['net_value']:,.2f} |\n"
for title,q in [('Mixed portfolio first year',portfolio['first_year']),('Mixed portfolio full year',portfolio['steady_state'])]:
 report+=f'\n### {title}\n\n| Item | Value |\n| --- | ---: |\n'
 for k,v in q['benefits'].items():report+=f"| {k.replace('_',' ')} | ${v:,.2f} |\n"
 for k,v in q['costs'].items():report+=f"| {k.replace('_',' ')} | −${v:,.2f} |\n"
for mode,q in gpu['economics'].items():
 report+=f'\n### AI/GPU {mode} annual breakdown\n\n| Item | Value |\n| --- | ---: |\n'
 report+=f"| Gross compute reduction | ${q['gross_annual_compute_reduction_usd']:,.2f} |\n"
 for k,v in q['costs'].items():report+=f"| {k.replace('_',' ')} | −${v:,.2f} |\n"
report+='\n### Moderate CPU annual breakdown\n\n| Item | Value |\n| --- | ---: |\n'
q=moderate['business_impact']['default']
for k,v in q['benefits'].items():report+=f"| {k.replace('_',' ')} | ${v:,.2f} |\n"
for k,v in q['costs'].items():report+=f"| {k.replace('_',' ')} | −${v:,.2f} |\n"
report+='\nFull GPU annual assumptions are retained in results/extended/gpu.json. All experiment totals are alternatives, not additive savings.\n'
report+='\n'+(P/'Executive_Redesign_Notes.md').read_text()+'\n'
(P/'Report.md').write_text(report)
(P/'results/summary_for_dashboard.json').write_text(json.dumps(dict(means=means,deltas=d,economics=e,sensitivity=S),indent=2)+'\n')
html=(P/'dashboard.template.html').read_text().replace('__EXECUTIVE_STYLE__',(P/'executive.css').read_text()).replace('__EXECUTIVE_SCRIPT__',(P/'executive.js').read_text()).replace('__ARCHITECTURE_WALK_SCRIPT__',(P/'architecture_walkthrough.js').read_text()).replace('__ARCHITECTURE_SVG__',(P/'assets/pri-system-architecture.svg').read_text()).replace('__EXTENDED_SCRIPT__',(P/'extended_ui.js').read_text()).replace('__COMPANY_SCRIPT__',(P/'company_impact.js').read_text()).replace('__BUSINESS_SCRIPT__',(P/'business_impact.js').read_text()).replace('__STORY_SCRIPT__',(P/'story.js').read_text()).replace('__SIMULATION_DATA__',json.dumps(D,separators=(',',':')).replace('</','<\\/'))
(P/'index.html').write_text(html)
# Versioned simulated governance records are rebuilt from the current run.
governance={'classification':'Simulated records with fictional identities, not organizational acceptance','risk':{'id':'PERF-DUPLICATED-WORK','owner':'fictional-service-owner','description':'Duplicated transformation creates queue and retry amplification'},'faulty_dispositions':[p['faulty_assessment']['disposition'] for p in R['preflights']],'corrected_dispositions':[p['corrected_assessment']['disposition'] for p in R['preflights']],'approval':R['preflights'][0]['approval'],'controls':{'evidence_quality':'coverage and environment checks','release_gate':'per-run practical thresholds','promotion':'artifact and expiry checks','recurrence':'adverse fixture retained and rerun across seeds'},'correction':'Engineer removes duplicate work; identical correction availability in both arms','automatic_code_repair':False,'production_identity_integration':False,'real_world_control_effectiveness':'not established','exceptions':[]}
(P/'results/governance.json').write_text(json.dumps(governance,indent=2)+'\n')
# Hash only reproducible experiment/source artifacts, not the manifest itself.
files=[p for p in P.rglob('*') if p.is_file() and '__pycache__' not in p.parts and 'work' not in p.relative_to(P).parts and p.name not in ['sha256.json','release-safety-simulation.zip','sensitivity_stdout.txt']]
(P/'sha256.json').write_text(json.dumps({str(p.relative_to(P)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(files)},indent=2)+'\n')
with zipfile.ZipFile(P/'release-safety-simulation.zip','w',zipfile.ZIP_DEFLATED) as z:
 for p in files+[P/'sha256.json']:z.write(p,p.relative_to(P))
print('Built report, dashboard and reproducible simulation package.')
