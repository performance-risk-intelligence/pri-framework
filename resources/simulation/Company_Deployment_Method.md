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
