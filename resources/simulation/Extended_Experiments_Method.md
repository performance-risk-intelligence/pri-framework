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
