# PRI release safety simulation

Version 1.4 • October 18, 2026 • Generated operational scenario executed by a discrete-event engine

## Executive finding

In a deliberately adverse 30-minute fictional service episode, PRI's representative preflight test holds a faulty release, retains the baseline, and admits the corrected artifact after a simulated owner review. Across 12 paired random replications, this avoids an average of **33,558.4 failed journeys** and **33,601.6 retry attempts**. Production work uses **990.7 fewer modeled CPU seconds**, while completing more work. All figures describe the model; they are not observations from an application, customer, employer or national infrastructure.

Including three preflight runs and an explicit two-CPU-second analysis allowance, total work is **218.6 CPU seconds higher** in this episode. The business consequence overlay projects **$5,697.61 first-year net economic value** and **$7,881.61 ongoing annual value** under the reference assumptions. This includes retained contribution, support/recovery capacity and all-release review costs. Rates and durations are scenario assumptions; BLS supports the labor-cost proxy only.

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
| Offered journeys | 89,988.667 | 89,988.667 |  |
| Completed journeys | 56,430.250 | 89,988.667 | more completed |
| Failed journeys | 33,558.417 | 0.000 | avoided failures |
| Failure percentage | 37.292 | 0.000 | percentage points |
| Retry attempts | 33,601.583 | 0.000 | avoided retries |
| Production CPU seconds | 8,645.322 | 7,654.660 | less production work |
| CPU seconds per completion | 0.153 | 0.085 | efficiency per usable result |
| Successful-only p95 milliseconds | 148.036 | 152.510 | survivor-sensitive |
| All-outcome p95 milliseconds | 1,720.000 | 152.510 | time to completion or final failure |

Values are means of the per-replication statistics, not pooled quantiles. Offered work is identical within each pair. Production CPU includes work spent on failures and late attempts. Three preflights consume 1,209.3 CPU seconds including the two-second analysis allowance. The net episode change includes that overhead; retaining fixed capacity demonstrates no reduction in the cloud invoice.

The 95 percent bootstrap interval for mean avoided failures is 33,447.8 to 33,669.8. For net CPU saving after preflight it is -224.7 to -212.6 seconds; both endpoints are negative. These intervals describe random variability within the specified simulation. They exclude uncertainty about real demand, defect types, behavior, test representativeness and adoption.

**Why successful-only p95 appears slightly worse with PRI.** Many requests disappear into failures in the overloaded comparator. Its successful requests therefore form a different, more favorable subset. PRI completes the peak-load requests too. Failure rate and all-outcome time expose this survivor effect; successful latency alone would mislead. All-outcome time is time to a usable result or final failure, not successful-latency quality. Failed users' later retries outside the modeled journey are not estimated.

## Sensitivity and limits

| Changed assumption | Mean failed journeys avoided | Net CPU seconds saved after testing | Lesson |
| --- | ---: | ---: | --- |
| Fast incident rollback | 33,152.5 | -222.6 | Rollback can leave retry-driven congestion until demand drops. |
| Fast rollback and retry budget | 11,378.5 | -857.6 | A stronger existing process reduces PRI incremental benefit. |
| Lower demand | 0.0 | 207.1 | No failed journeys are prevented; the benefit is bounded resource/latency improvement. |
| Slow incident rollback | 38,261.8 | 329.8 | Longer exposure can increase the value of prevention. |
| Unrepresentative preflight | 0.0 | -1,077.5 | The hidden defect is missed; both arms suffer the same production outcome. |
| Missing preflight records | 33,539.5 | -222.2 | The evidence hold retains baseline; it is not a prediction of a defect. |

Sensitivity cases use four replications each. These selected tests are mechanisms and boundaries, not a representative defect distribution. Shared configuration errors, biased fixtures, correlated failures and emergency bypasses could change the result. The model contains no direct benefit for national security, clinical efficacy, vehicle safety or individual eligibility decisions.


## Business impact: sources, assumptions and calculation

This extension prices possible consequences of failures already generated by the event engine. It does not change the technical results or simulate customer purchasing behavior. The reference is a fictional mixed transaction workflow, not a named company, an average U.S. company or a commercial PRI offer. All amounts are USD. Prepared October 18, 2026.

### What public sources establish

[BLS May 2024 occupational wage tables, released April 2, 2025](https://www.bls.gov/news.release/archives/ocwage_04022025.pdf) report median hourly wages of $20.59 for customer service representatives and $63.98 for software developers. [BLS March 2025 employer compensation, released June 13, 2025](https://www.bls.gov/news.release/archives/ecec_06132025.pdf) reports private-industry total compensation of $45.38 and wages of $31.89 per hour. Multiplying the occupational wage references by 45.38 / 31.89 gives approximately $29.30 for support/recovery and $91 for engineering. These are rounded historical national planning proxies, not current Irvine quotations, occupation-specific benefit estimates or fully allocated company costs. BLS does not endorse this combination or PRI.

[Google SRE incident response](https://sre.google/workbook/incident-response/) supports distinguishing incident coordination, communication and mitigation. It supplies none of the assumed recovery hours. [FinOps unit economics](https://www.finops.org/framework/capabilities/unit-economics/) supports connecting technical units with business value; it does not establish transaction-loss rates or savings here.

No source establishes a universal conversion from a failed API journey to a lost transaction, a support contact, or minutes of recovery. Those depend on the actual journey and must be validated. Generic enterprise downtime prices and cart-abandonment percentages are deliberately not imported as per-failure prices. The following values are plausible planning scenarios to challenge, not empirical PRI statistics.

### Reference consequence assumptions

| Input | Reference value | Status and interpretation |
| --- | ---: | --- |
| Qualifying adverse release episodes/year | 6 | Existing annual scenario assumption, not observed incident frequency |
| Transfer of modeled episode benefit | 50% | Existing discount assumption, not measured effectiveness |
| Failed journeys eligible for a commercial transaction | 5% | Assumption; avoids treating every digital action as an order |
| Eligible transactions still lost after later recovery | 10% | Assumption; 90% of this eligible population receives no lost-contribution credit |
| Contribution per irrecoverable transaction | $10 | Assumption after variable fulfillment costs, not gross revenue; excludes staff tasks counted separately |
| Failed journeys creating one support contact | 1% | Assumption; one contact per affected case; no automatic retry counted as a ticket |
| Support handling time | 6 minutes | Assumption, including case handling/wrap-up; not claimed as an industry benchmark |
| Separate manual recovery population | 1% | Assumption; disjoint from support population |
| Manual recovery time | 3 minutes | Assumption for reconciliation/reprocessing; not the original request latency |
| Support and recovery hourly cost | $29.30 | Rounded BLS-derived compensation proxy described above |
| Incremental engineering response | 4 hours without gate versus 1 with gate | Assumed person-hours per credited incident, excluding shared code correction and routine release reviews |
| Engineering hourly cost | $91 | Rounded BLS-derived proxy; replaces the earlier illustrative $100 in this new overlay |
| Routine release review | 15 minutes × 52 releases | Additional assumed PRI work charged every release, including clean releases |
| Setup / annual maintenance | 24 / 12 engineering hours | Existing planning assumptions, not time measurements |
| Noncompute overhead | $120/year | Existing demo allocation; not a production hosting or commercial license quote |
| Test work | All three preflights × 52 releases | Executed modeled CPU work; $0.05/active-vCPU-hour remains an illustrative valuation, not provider pricing |

Annual avoided failures = simulated mean difference × 6 × 50%, approximately 100,675 journeys for the primary case. This is annualized arithmetic, not a year-long execution. It already includes the modeled automatic retry policy; do not multiply by retry counts again.

Retained contribution = annual avoided failures × transaction-eligible share × irrecoverable share × contribution per transaction. Reference: approximately 503 otherwise-lost transactions per year, not 100,675 lost sales.

Support capacity = annual avoided failures × support fraction × handling minutes / 60 × support hourly cost. Separate recovery capacity uses the disjoint recovery fraction and recovery minutes. Incident-response capacity = (4 − 1) person-hours × credited qualifying episodes × engineering hourly cost, only if the selected executed case prevents failures.

Ongoing net value = retained contribution + support capacity + recovery capacity + engineering response capacity + production compute-work value − all-release test work − all-release routine review − maintenance − noncompute overhead. First-year net value also deducts setup. Dollar-valued staff capacity is not automatically reduced payroll. Demonstrated cash savings remain $0.

### Sensitivity definitions

| Scenario | Transaction-eligible share | Irrecoverable share | Contribution | Support fraction / minutes | Separate recovery fraction / minutes |
| --- | ---: | ---: | ---: | --- | --- |
| No business consequences priced | 0% | Not credited | $0 credited | 0% | 0% |
| Low consequence | 2% | 5% | $5 | 0.5% / 4 | 0.5% / 2 |
| Reference transaction | 5% | 10% | $10 | 1% / 6 | 1% / 3 |
| Higher consequence | 10% | 20% | $15 | 2% / 8 | 2% / 5 |
| Noncommercial workflow | 0% | No lost contribution | $0 credited | 1% / 6 | 1% / 3 |

These are alternatives, not measured confidence bounds, expected company savings or rates selected to hit a target. A missed defect receives no avoided-failure business benefit. The low-demand case also receives none when it prevents no failures. Setup, review and operating costs still apply. Zero recurrence or transfer removes incident-related credits while retaining release costs.

### Avoiding double counting and overstatement

Support and manual-recovery populations are disjoint. Engineering incident coordination is separate from both. One transaction can incur lost contribution and a separate handling cost only if the contribution calculation excludes that labor. Common correction work cancels. No additive blanket outage cost, revenue per request, customer lifetime value, service credit, regulatory penalty, employee waiting productivity, energy or emissions benefit is assumed. Aggregate journey-time improvements are not wall-clock outage reductions and are not monetized. The 4 versus 1 engineering hours are an assumption, not measured time to recovery.

A fixed-size compute fleet has no demonstrated invoice saving. Retained contribution is conditional economic value, while support/recovery/engineering time is released capacity. Real cash effects need actual staffing, paid overtime, invoice and recovered-transaction records. The overlay is a total of the included categories, not a claim to capture every business effect.

No PRI commercial license price, customer-specific cloud integration, security review, data retention, additional instrumentation or release-delay opportunity cost has been quoted. These may materially reduce net value and must be added before a buying decision. The $120 allocation is suitable only as a demo assumption. Scaling repeats costs per non-overlapping system; it assumes neither observed adoption nor economies of scale. A nationwide count is an illustration, not a national savings estimate.

### Evidence to replace assumptions in a pilot

Define a business transaction separately from HTTP calls. Join journey identifiers to later completion/recovery records within an agreed recovery window; deduplicate shared outages and downstream services. Estimate irreversible losses from comparable baseline/control cohorts and use contribution after variable costs. Link actual support tickets and reprocessing task times to the affected cases. Obtain role-specific compensation or contractor costs, incident logs, review/setup/maintenance time and incremental infrastructure invoices. Retain the no-business and missed-defect cases. Update recurrence and transfer from representative exposure and measured control performance before using the projection as a customer forecast.


### Consequence projections for the primary executed case

| Assumption scenario | Gross annual value | First-year net | Ongoing net |
| --- | ---: | ---: | ---: |
| No business consequences priced | $819.04 | $-3,760.83 | $-1,576.83 |
| Low consequence | $2,797.31 | $-1,782.56 | $401.44 |
| Reference transaction scenario | $10,277.48 | $5,697.61 | $7,881.61 |
| Higher consequence | $43,804.02 | $39,224.14 | $41,408.14 |
| Noncommercial workflow | $5,243.72 | $663.85 | $2,847.85 |

### Reference scenario annual benefit and cost breakdown

| Item | Value |
| --- | ---: |
| retained contribution | $5,033.76 |
| support capacity | $2,949.78 |
| manual recovery capacity | $1,474.89 |
| incident response capacity | $819.00 |
| production compute | $0.04 |
| release testing | −$0.87 |
| routine release review | −$1,183.00 |
| maintenance | −$1,092.00 |
| noncompute | −$120.00 |
| setup | −$2,184.00 |

First-year net: **$5,697.61**. Ongoing annual net: **$7,881.61**. These are conditional economic values, not verified cash savings.

### Illustrative multiplication of the reference scenario

| Distinct non-overlapping systems | First-year net | Ongoing annual net |
| ---: | ---: | ---: |
| 1 | $5,698 | $7,882 |
| 25 | $142,440 | $197,040 |
| 1,000 | $5,697,608 | $7,881,608 |
| 10,000 | $56,976,076 | $78,816,076 |

These counts do not estimate adoption or national savings. Costs are replicated per system without economies of scale, and no overlapping transactions may be counted.

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

## Company-wide PRI deployment scenario

Prepared October 18, 2026. This is an illustrative transaction-oriented company budget applied to the existing synthetic technical outcomes. It is not an observed company, an average business, a customer quote or a forecast supported by adoption data. The original single-system scenario remains separate. Both retain the original monitored rollback comparator.

Ten independent business workflows serve distinct transaction populations. For example, separate regional or business-line transaction streams may qualify; the order, payment and database microservices behind the same purchase cannot each claim that purchase. Five workflows activate at the start of Month 4, and five at the start of Month 7. Exposure is 5 × 9/12 + 5 × 6/12 = 6.25 active workflow-years in Year 1, then ten in a full deployment year. The model assumes integration completes on schedule and does not claim to execute those deployments.

Each active workflow has two qualifying adverse episodes per year, with 50% transferable benefit. Year 1 therefore credits 6.25 episode equivalents; a full operating year credits ten. The modeled primary episode avoids about 33,558 failed journeys. These recurrence and transfer assumptions are not measured incident probabilities, and the severe stress case is not a representative distribution of all releases.

The company scenario assumes 20% of failed journeys are eligible commercial transactions, 10% of those are permanently lost after later recovery, and contribution is $20 per lost transaction. Thus only 2% of prevented failed journeys receive a commercial contribution credit. This is a more transaction-oriented workload than the single-system reference (5% eligible share, $10 contribution). The change is explicit; the increase is not attributed to company size alone. Contribution is after variable fulfillment costs and excludes separately counted support and recovery labor.

Support affects 1% of failed journeys at six minutes per case. A separate 1% need three minutes of manual recovery. These populations are disjoint. Engineering response costs four person-hours without prevention versus one with the gate, excluding common code correction. All durations and behavioral shares are assumptions; only the rounded $29.30 support and $91 engineering compensation proxies are anchored to the dated BLS method described in Business_Impact_Method.md.

### Deployment budget and cost boundaries

| Cost | Assumption | Year 1 treatment |
| --- | --- | --- |
| Shared configuration, access controls, documentation and training | 80 engineering hours | Full initial cost |
| Workflow instrumentation, representative fixtures and CI/CD integration | 16 engineering hours per workflow | All ten workflows charged initially |
| Shared operational maintenance | 96 engineering hours/year | Full year charged during rollout |
| Workflow maintenance | 2 engineering hours per workflow/year | All ten charged for full year, conservatively |
| Human release review | 15 minutes × 52 releases per active workflow-year | Follows active exposure |
| Test execution | Existing modeled three preflights per release | 52 releases per active workflow-year; illustrative compute valuation |
| Shared platform, telemetry, storage and backup | $600/month | Full 12-month allocation during rollout |
| Security and assurance | $3,000/year | Full allocation; limited review allowance, not certification or regulatory approval |
| Commercial PRI or vendor license | $0 default | Unpriced, editable; not a promise that deployment is free |

These are planning allowances for deploying an available implementation into a company's environment. They do not finance building the entire PRI product. $600/month is a shared budget, not a vendor quote or a sizing benchmark. Actual ingestion, retention, networking, identity, security and high-availability requirements may exceed it. The security allowance is not a full audit, penetration-test or compliance certification budget. Existing application costs common to both arms cancel; incremental platform costs are charged. The company budget replaces the single-system overhead and setup/maintenance figures, avoiding duplicate costs. No volume discount is assumed for human release review.

Shared integration plus workflow integration totals 240 engineering hours. Maintenance totals 116 engineering hours annually. Routine first-year release reviews total 81.25 person-hours, rising to 130 at full deployment. These hours support feasibility checks and should be replaced by actual implementation estimates. The result uses constant dollars without inflation, taxes, financing or a discount rate; it is a one-year incremental economic comparison, not a business valuation.

### Interpretation and validation

The displayed total combines conditional retained contribution, released support/recovery/response capacity and a negligible compute-work valuation. It is not all cash savings. No headcount reductions, extra sales beyond prevented losses, blanket downtime cost, customer lifetime value, service credits, user waiting productivity, energy or emissions are monetized. Cash savings demonstrated by this simulation remain zero.

First-year and steady-state values differ because rollout exposure rises from 6.25 to ten workflow-years and setup is a one-time cost. A full operating year has no repeat initial setup but still pays review, maintenance, platform, assurance and testing costs. Changing the selected technical case recomputes both periods. Missing-defect cases keep deployment costs but receive no prevented-failure transaction, support, recovery or response credit. The separate incident-history teaching animation does not feed this model.

Validate transaction identity, unique eligible commercial opportunities, later recovery, contribution margin, ticket linkage and handling duration, incident frequency, test representativeness, rollout timing and actual quotes before relying on this scenario. A company with fewer eligible transactions or strong existing preflight controls may realize much less value or a loss. Two hundred thousand prevented API journeys are not two hundred thousand prevented lost orders. This is an inspectable starting business case, not evidence of effectiveness or national economic benefit.

### Applying the earlier external review

The earlier v1.1 review correctly identified that $2,821 was a first-year net cost, not savings, and that the economic model omitted business consequences. The current overlays add contribution, support, recovery, routine review and shared deployment costs. Its old 2.8-cent threshold cannot be carried into this company case because the cost basis, labor coefficient, recurrence and commercial assumptions changed. The company view recalculates the required contribution and recurrence from its own inputs. Calendar payback is not calculated from annual averages; actual rollout timing, monthly incident exposure and cash realization must first be established.

Edition 1.4 now adds separately executed moderate, mixed-portfolio and bulk AI/GPU experiments, with their own assumptions and results in Extended_Experiments_Method.md. They do not change this earlier uniform-company comparison or establish real hardware performance. The GPU model distinguishes instance termination from fixed-fleet capacity and adds no financial credit to this uniform-company case.


| Company item | Year 1 | Full deployment annually |
| --- | ---: | ---: |
| retained contribution | $83,896.04 | $134,233.67 |
| support capacity | $6,145.39 | $9,832.62 |
| manual recovery capacity | $3,072.69 | $4,916.31 |
| incident response capacity | $1,706.25 | $2,730.00 |
| production compute | $0.09 | $0.14 |
| testing | $-5.46 | $-8.73 |
| routine review | $-7,393.75 | $-11,830.00 |
| maintenance | $-10,556.00 | $-10,556.00 |
| platform | $-7,200.00 | $-7,200.00 |
| security | $-3,000.00 | $-3,000.00 |
| license | $-0.00 | $-0.00 |
| setup | $-21,840.00 | $0.00 |

Company net economic value: Year 1 **$44,825.25**; full-deployment annual **$119,117.99**.

# Moderate regression, mixed portfolio and AI/GPU experiments

October 18, 2026 · Interactive edition 1.4. All three are new executed synthetic experiments. None is a customer result, real GPU benchmark, typical-incident distribution, observed business loss, or verified saving.

## Sources and their limits

[Google SRE: Canarying Releases](https://sre.google/workbook/canarying-releases/) supports representative load, attributable comparison and staged rollout checks. It does not establish that a 20% regression or any incident frequency used here is typical. [NVIDIA Triton batching](https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/user_guide/batcher.html) explains batch aggregation and recommends profiling throughput and latency. [Triton optimization guidance](https://github.com/triton-inference-server/server/blob/main/docs/user_guide/optimization.md) supports comparing measured configurations. Neither supplies this experiment's runtime formula or promises that a larger batch is better on real hardware.

An [AWS case study published March 31, 2026](https://aws.amazon.com/jp/blogs/news/case-study-dentsusoken-unveil/) gives a **March 2026** on-demand reference of **$1.006 per g5.xlarge instance-hour in US East (N. Virginia)**. This is a dated published reference, not a live October quote. [AWS instance specifications](https://docs.aws.amazon.com/ec2/latest/instancetypes/ac.html) identify a single A10G per g5.xlarge. We price the entire instance, not a standalone GPU-second. [EC2 on-demand billing](https://aws.amazon.com/ec2/pricing/on-demand/) supports per-second Linux billing with a 60-second minimum. Recheck region, operating system, purchase option and actual charges before purchasing. No AWS resources are provisioned by this code.

The dated BLS wage and compensation sources, calculation and limitations are in Business_Impact_Method.md. These supply the $91 engineering and $29.30 operations planning proxies. All workload sizes, service-time coefficients, incident counts, loss probabilities, contribution, review effort and deployment budgets are scenario assumptions. The model does not borrow a published speedup as its result.

## 1. Moderate CPU regression

The original discrete-event engine now also runs a **20% increase in per-request work** rather than a doubling, using eight paired seeds and the same arrival, queue, timeout, retry and rollback rules. This is a defined moderate work regression, not an assertion that its tail-latency effect is small or statistically typical. Nonlinear queueing can amplify small work increases.

Baseline and candidate receive identical marks. The existing-process arm still monitors and rolls back; PRI consumes the actual gate disposition. The preflight's 10% p95 / one-percentage-point failure rule is unchanged. Missing evidence cannot authorize a candidate. Results include failures, successful p95, all-outcome p95, CPU and all test overhead.

The moderate case uses the existing single-system annual assumptions: six qualifying episodes, 50% benefit transfer, 52 releases, 24 setup hours, 12 maintenance hours, 15 minutes routine review per release and $120 noncompute overhead. No conversion-loss benefit is inferred from latency alone. If no failed journeys are prevented, transaction, support, recovery and incident-response credits remain zero. A negative financial result is retained. No waiting-time productivity or electricity benefit is assigned.

## 2. Mixed company portfolio

Ten distinct workflows are divided into five separately executed groups, eight paired replications per group. Every group has its own configuration and seed range; control and PRI within a group share workload marks. Groups represent **non-overlapping customer/business populations**, not sequential steps of the same purchase. Their results are aggregated once; this is not a simulation of cross-service dependencies or correlated multi-service outages.

| Group | Count | Requests/s normal / peak | Extra work | Existing control / evidence | Episodes per workflow-year | Live from | Transaction-eligible / irrecoverable / contribution |
| --- | ---: | --- | ---: | --- | ---: | --- | --- |
| Commercial intake A | 2 | 40 / 70 | 50% | Ordinary monitored rollback | 2 | Month 4 | 50% / 10% / $20 |
| Customer portal B | 3 | 40 / 70 | 20% | Ordinary monitored rollback | 3 | Month 4 | 0%; no commercial credit |
| Back-office C | 2 | 20 / 35 | 35% | Ordinary monitored rollback | 2 | Month 7 | 0%; no commercial credit |
| Commercial intake D | 2 | 40 / 70 | 100% | Immediate rollback plus 10% retry-token budget | 1 | Month 7 | 25% / 5% / $15 |
| Submission E | 1 | 40 / 70 | 100% | Unrepresentative preflight misses the defect | 2 | Month 7 | 0%; no commercial credit |

All groups use 50% transfer, 52 releases per active workflow-year and the BLS-derived labor proxies. A and D use 1% support and 1% separate manual recovery. B uses 0.5% each. C uses 0.5% support and 2% separate recovery at four minutes per case. E uses 1% each but receives no avoided-failure credit when the fixture misses. Support takes six minutes; manual recovery otherwise takes three. All rates are assumptions, not empirical industry rates. Contribution excludes the separately counted staff work.

Five workflows live for nine months and five for six months: 6.25 active workflow-years initially, ten in a full operating year. Shared budgets match the earlier company scenario: 80 shared setup hours plus 16 per workflow; 96 shared maintenance hours/year plus two per workflow; 15 minutes human review per active release; $600/month platform allowance; $3,000/year assurance allowance; no quoted PRI license price (default $0). Full maintenance, platform and assurance budgets are charged in Year 1. They are budget allocations, not production sizing, certification or complete PRI product-development costs. Additional vendor fees must be included once quoted.

Testing follows each group's own executed preflight workload. No per-service $120 overhead or setup is added on top of the shared budget. The earlier uniform company case is retained for comparison but is no longer the mixed-portfolio result. Lower demand, modest regressions, stronger existing controls and missed defects can all reduce incremental value.

## 3. AI/GPU batch-efficiency scenario

This is a separate **bulk, stateless AI-style inference workload**, not an interactive token-streaming LLM or a real TensorRT benchmark. An engineer proposes batch-size tuning; PRI supplies evidence and a review gate, not automatic discovery or automatic code repair. Equivalent existing performance-tuning practice could deliver the same gain.

One million jobs are ready at time zero. Thirty-two one-GPU workers process the finite queue, without autoscaling, preemption, automatic retries or dropped jobs. Current batch size is four; proposed size is eight. Job work weights are lognormal with mean one and log sigma 0.25. A batch of size b takes **0.2 + 2.0 × b^0.8 × mean job weight** seconds. These coefficients create a plausible sublinear batching mechanism for exploration; they were not measured on an A10G and are not derived from NVIDIA benchmarks. Real models can perform worse at a larger batch. Memory fit at size eight is an explicit assumption, not measured VRAM use.

The scheduler repeatedly assigns the next FCFS batch to the earliest available worker, charges all executed busy time, and counts completion time for every job. Startup is included in job completion times. A 16-hour deadline is reported separately from eventual completion; late jobs still consume resources. No job is retried, so there is no invented retry saving. The synthetic checksum verifies job-count/ID conservation; it does **not** establish real model accuracy or output equivalence.

Preflight runs 1,000 jobs on one simulated GPU for current, candidate and revalidation configurations. Cost eligibility requires at least 99% coverage, matching environment, assumed memory fit, matching synthetic conservation, at least 10% less GPU work and no more deadline misses. The artifact-bound approval actually determines which batch size the PRI arm uses. Failed or missing evidence retains the current batch size. Real model accuracy, numerical tolerances, batch memory, host overhead and output-quality evaluation remain necessary before production authorization.

Every GPU instance adds 120 seconds startup and 60 seconds shutdown. Each instance is billed for rounded-up allocated seconds with a 60-second minimum. On this saturated finite queue, per-worker busy time plus startup/shutdown equals its allocated lifetime; there is no uncharged modeled waiting between jobs. One instance may stop when its final assigned batch completes. Compute-hours and per-job cost are not equated to electricity use.

Annual assumptions: 250 batches, 50% transfer of the modeled lifetime difference, 52 validations with all three test runs charged, 80 setup hours, 48 maintenance hours/year, 15 minutes review per validation, $1,200 incremental platform overhead and no quoted license fee. Production job inputs recur under the same generating process; real demand, model sizes and scheduling would require new runs. The 50% discount is not a measured efficacy rate. No retained revenue, support deflection, user productivity or AI-quality value is added.

**Stop-after-job mode** values earlier instance termination at the dated AWS rate. **Fixed-fleet mode** grants zero compute bill reduction; faster jobs release capacity but the allocated fleet remains chargeable. Preflight resources are conservatively charged separately in both modes, rather than assuming they use otherwise-free idle fleet time. Existing application/network/storage costs common to both arms cancel, but incremental telemetry is budgeted; material egress, storage, orchestration, model loading, assurance, support or procurement costs require separate estimates. Discounts, Spot pricing, taxes, financing and energy are excluded.

The three new scenarios are alternative experiments. Do not sum the GPU, uniform-company and mixed-company results without establishing distinct workloads and a common shared-cost budget. Neither the synthetic job checksum nor the gate demonstrates real inference correctness, hardware performance, customer savings or national impact.

## Reproduction

Run `python3 extended_scenarios.py` and `python3 gpu_simulation.py`, then `python3 verify_extended.py` and `python3 build_report.py`. Both execute logical event time, not wall-clock model workloads. Python standard library only. Seeded raw summaries, preflight decisions, paired results, configurations, annual assumptions and sources are included under results/extended/. The dashboard replays these artifacts; changing billing/annual assumptions does not rerun a GPU benchmark.


## Extended experiment financial results

| Experiment | Year 1 net | Ongoing annual net |
| --- | ---: | ---: |
| Moderate CPU | $-4,579.80 | $-2,395.80 |
| AI/GPU stop after job | $-6,373.40 | $906.60 |
| AI/GPU fixed fleet | $-14,100.78 | $-6,820.78 |
| Mixed portfolio | $3,632.99 | $39,962.87 |

### Mixed portfolio first year

| Item | Value |
| --- | ---: |
| retained contribution | $50,633.91 |
| support capacity | $1,632.04 |
| manual recovery capacity | $816.02 |
| incident response capacity | $546.00 |
| production compute | $0.06 |
| testing | −$5.29 |
| routine review | −$7,393.75 |
| maintenance | −$10,556.00 |
| platform | −$7,200.00 |
| security | −$3,000.00 |
| license | −$0.00 |
| setup | −$21,840.00 |

### Mixed portfolio full year

| Item | Value |
| --- | ---: |
| retained contribution | $68,291.44 |
| support capacity | $2,297.87 |
| manual recovery capacity | $1,148.94 |
| incident response capacity | $819.00 |
| production compute | $0.08 |
| testing | −$8.46 |
| routine review | −$11,830.00 |
| maintenance | −$10,556.00 |
| platform | −$7,200.00 |
| security | −$3,000.00 |
| license | −$0.00 |
| setup | −$0.00 |

### AI/GPU stop_after_job annual breakdown

| Item | Value |
| --- | ---: |
| Gross compute reduction | $7,727.39 |
| test execution | −$69.78 |
| routine review | −$1,183.00 |
| maintenance | −$4,368.00 |
| incremental platform | −$1,200.00 |
| license | −$0.00 |
| setup | −$7,280.00 |

### AI/GPU fixed_fleet annual breakdown

| Item | Value |
| --- | ---: |
| Gross compute reduction | $0.00 |
| test execution | −$69.78 |
| routine review | −$1,183.00 |
| maintenance | −$4,368.00 |
| incremental platform | −$1,200.00 |
| license | −$0.00 |
| setup | −$7,280.00 |

### Moderate CPU annual breakdown

| Item | Value |
| --- | ---: |
| retained contribution | $0.00 |
| support capacity | $0.00 |
| manual recovery capacity | $0.00 |
| incident response capacity | $0.00 |
| production compute | $0.02 |
| release testing | −$0.83 |
| routine release review | −$1,183.00 |
| maintenance | −$1,092.00 |
| noncompute | −$120.00 |
| setup | −$2,184.00 |

Full GPU annual assumptions are retained in results/extended/gpu.json. All experiment totals are alternatives, not additive savings.

# Executive review interface 1.5

October 18, 2026. Local review only. No publication or pull request is part of this redesign.

The interface reorganizes the complete v1.4 simulator into three keyboard-accessible tabs: Executive Summary, How PRI Works, and Business Impact. The original PRI stylesheet and its ivory, charcoal, sage and terracotta tokens remain the visual foundation. Every v1.4 case, engine output and economic calculator is preserved. The new executive.js and executive.css are presentation layers; no experiment or economic engine changed.

The executive comparison uses paired completion/failure bars with the same offered-journey denominator. Counts are replication means, completion rate is the ratio of mean completed to mean offered, and the representative preflight charts identify their seed. A conditional financial card identifies its selected CPU case and deployment count separately from event outcomes.

Engineering views expose baseline/candidate p95 against the actual ten-percent threshold, failure-rate differences against the one-percentage-point rule, artifact review status, and recorded scheduled release/monitoring/rollback milestones. Actual preflight wall-clock placement and human-review duration are not available; the interface does not invent them. Incident history remains separately labeled fictional context that feeds neither the gate nor the finances. Latency, completion and retry panels retain their different outcome definitions and scales.

The business view reads four existing scopes: selected CPU system, mixed portfolio, GPU batch and uniform company. A period selector distinguishes first year from ongoing operation. The waterfall separately groups retained contribution, support/recovery capacity, engineering response capacity, compute valuation, setup and ongoing costs. These groups sum to the existing selected model result. GPU fixed-fleet mode still has zero bill reduction. Negative results are retained.

The tornado chart applies a selected relative change to one named economic component at a time, holding all others fixed. It is an arithmetic sensitivity of the financial case, not a new experiment or a distribution of annual results. Credited-benefit sensitivity scales all gross benefit components; it does not claim a new measured incident frequency. Contribution/loss sensitivity scales contribution only, support/recovery effort scales those capacity benefits, engineering-price sensitivity scales engineering response benefits and engineering setup/review/maintenance costs, setup scales setup costs, and ongoing allowance scales ongoing costs. These variations overlap conceptually and must not be combined or summed. Sensitivity range is not a confidence interval.

Break-even holds other benefits and costs fixed. For CPU/company scopes it solves for average contribution per prevented failed journey; this is not contribution per lost sale. The eligible and irrecoverable fractions are already reflected in the current average. For a GPU batch it solves for instance-hour price using credited reduced allocation. With no credited unit exposure, the chart reports unavailable instead of dividing by zero or assigning an invented value.

The redesigned evidence JSON adds executiveReview with current scope, period, financial presentation and explicit provenance classifications. Existing experiment, assumption and forecast data remain separate. Assumption edits update the charts and existing calculators but never rewrite saved experiments. A standalone waterfall SVG and a printable executive review are available. No PDF is generated automatically.

All original experiments and detailed financial controls remain in an expandable drawer. Direct links to old scenario sections open the correct tab and drawer. The interface handles keyboard tab selection, labeled SVG alternatives, reduced motion and mobile layouts. Wider charts use keyboard-accessible local scrolling to preserve label readability. No remote script or backend is required.

## Technical reference tab 1.6

The fourth tab contains the selected saved CPU configuration, separate GPU scheduler configuration, gate and measurement semantics, reproduction commands, source links and existing evidence export. Methods and sources deep links now open this tab. Arrow keys and Home/End cover all four tabs; narrow screens use a two-by-two tab layout. No model input or calculation changed.

## Architecture diagram 1.7

Technical Details now includes the system architecture, selectable component descriptions, selected gate disposition and a standalone SVG download. Proposed CI/CD connections are dashed; implemented model relationships are solid. Fictional history is isolated, and financial assumptions enter only the conditional economic model. All calculation engines and saved experiment outcomes remain unchanged. See Architecture_Integration_Notes.md.

## Animated architecture walkthrough 1.8

A play/pause release story now follows the selected CPU case with manual step navigation and restart. It shows the hold, correction, revalidation, simulated review and conditional annual business case, or the admitted-candidate boundary when a fixture misses. Motion is illustrative, not simulation time. Reduced-motion mode disables packets. All saved model outputs and calculations are unchanged. See Architecture_Integration_Notes.md.

