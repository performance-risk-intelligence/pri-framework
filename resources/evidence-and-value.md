# PRI: evidence and value measurement

Public edition v0.2.0 · prepared October 17, 2026

## What this document supports

PRI proposes measurement standards, release-risk review, preventive controls, and compute/cost investigation. Its intended benefits require evaluation; no PRI customer results or validated predictive accuracy are asserted.

## Evaluate value within one workflow

1. Agree on the journey, successful completion, failed and incomplete outcomes, and representative workloads. Count unsuccessful interactions separately so latency results do not hide their frequency.
2. Record release/environment identifiers, repeat runs, measurement variation, missing data, sample sizes, and observation periods. Compare like workloads; segment where user populations differ.
3. Establish pre-intervention measures and define decision criteria before evaluating a pilot. Use an appropriate comparison when feasible and record alternative explanations such as architecture, demand, provider, pricing, or staffing changes.
4. Evaluate adoption and outcome separately. A completed risk register or checklist demonstrates process adoption, not automatically improved reliability.
5. Track completed preventive actions, control effectiveness, incident recurrence, completion/timeliness, retries, and compute per completed action where relevant.
6. Include assessment, implementation, testing, infrastructure, and maintenance costs in any net-value calculation. Avoid counting the same benefit as both avoided incident cost and saved labor without reconciling overlap.

## Distinguish the evidence types

- **Measured:** directly observed under documented boundaries. A billing change can be measured without establishing why it occurred.
- **Estimated:** calculated from measured inputs and explicit assumptions, with uncertainty stated.
- **Modeled:** a scenario or proxy dependent on model assumptions; not a direct measurement of electricity or emissions.
- **Potential:** a plausible benefit mechanism that has not yet been established through PRI implementation.

Lower cloud spend does not directly establish lower electricity use. Energy estimates require workload attribution, hardware/utilization assumptions, facility overhead, and provider-specific data where available. Higher demand may offset efficiency improvements.

## Potential U.S. economic value

The proposed pathway is local implementation → evaluated outcomes → authorized generalization and training → adoption in other organizations. Potential benefits include fewer disrupted digital interactions, less repeated engineering remediation, and reduced unnecessary resource use. Each link requires evidence.

No national dollar savings, job-creation totals, or PRI electricity-reduction projections are provided. Broader projections would need credible adoption assumptions, validated per-workflow effects, implementation costs, uncertainty ranges, and treatment of overlap and differences across organizations. Industry-wide loss or electricity totals are context, not PRI’s addressable savings.

## Primary-source context

Lawrence Berkeley National Laboratory, *United States Data Center Energy Usage Report: 2025 Update*, published June 2026, Executive Summary, printed page 5 (PDF page 7), projects data centers could account for 9.5–15.3% of U.S. electricity use in 2030 across its overall uncertainty range. This forecast describes infrastructure demand; it does not quantify software-regression waste or potential PRI effects.

[Report hosted by the U.S. Department of Energy](https://www.energy.gov/documents/united-states-data-center-energy-usage-report-2025-update)

External sources do not validate, endorse, or establish PRI outcomes. The public hub does not assert regulatory certification or compliance.
