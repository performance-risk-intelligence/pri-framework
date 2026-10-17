# A release review from signal to prevention

Synthetic worked example · v0.4.0 · October 17, 2026

## Read this example correctly

Every identifier, measurement, incident, role, decision, and verification result below is invented for instruction. This is not a customer case, operational deployment, validated prediction, or evidence of achieved benefits. The example uses explicit rules, not predictive scoring. Its thresholds are illustrative and must not be copied into production without justification.

## 1. Define the journey and comparable evidence

**Journey J-01:** a synthetic request is submitted to a cloud-backed service and ends when a usable response is visible. Failed or timed-out attempts do not count as successful completions. The test workload contains only generated inputs.

**Evidence B-01 and C-01:** compare baseline build B with candidate build C using the same generated workload, fixed test environment, resource allocation, concurrency, warmed-cache rule, and timing boundaries. Each build has five runs of 1,000 attempts. Run identifiers, software/dependency versions, and exclusions would accompany a real report.

- Baseline B: 5,000 attempts; 4,950 completions; 50 failures; 1.0% failure rate. Successful-attempt p95 latency is 800 ms; per-run p95 values range from 780 to 820 ms.
- Candidate C: 5,000 attempts; 4,850 completions; 150 failures; 3.0% failure rate. Successful-attempt p95 latency is 1,040 ms; per-run p95 values range from 1,010 to 1,070 ms.
- Comparison: aggregate p95 is 30% higher; failure rate is 2 percentage points higher. These are synthetic descriptive summaries, not confidence intervals or statistical proof of causation. Failures remain visible alongside latency so unsuccessful attempts cannot improve the apparent timing result.

**Illustrative review criteria:** investigate p95 more than 10% above baseline or failure rate more than 1 percentage point above baseline. Threshold rationale and organizational approval would be required in practice. No resource or energy result is inferred from these latency values.

## 2. Connect the signal to change and incident context

**Change CH-01:** the candidate includes a dependency timeout/retry change. **Incident I-01:** an invented earlier release had retry amplification under load. These records suggest a testable hypothesis; they do not establish that the dependency change caused the candidate regression.

Proposed investigation: isolate the change, compare retry counts and trace segments, repeat controlled measurements, and check whether environmental differences explain the signal. Unknown causes remain marked unknown.

## 3. Create a risk disposition

**Risk R-01:** if timeout/retry behavior amplifies work during the defined journey, users may wait longer or fail to receive a usable result. Evidence references: B-01, C-01, CH-01, and I-01. Owner: the fictional service engineering lead. Severity and likelihood require the adopting organization's rubric; this example does not assign a validated probability.

**Proposed controls:** a comparable-workload regression test; a completion/failure check alongside latency; an investigation of retry behavior; and review of the candidate's threshold breaches. The control record links the signal, hypothesis, owner, required evidence, and review status.

## 4. Record the decision and exception status

**Decision D-01:** hold this candidate within the illustrative review; investigate and validate mitigation. Decision role: the fictional release owner, with performance and service engineering reviewers. Open items: cause, mitigation evidence, and post-release monitoring arrangements. There is no production authorization.

**Exception status:** none granted. If an organization considered an exception, its record would need an authorized approver, rationale, evidence, residual risk, compensating controls, review/expiry conditions, and follow-up owner. An exception would not make missing measurements complete or erase a breach.

## 5. Link mitigation to durable prevention

**Action A-01:** investigate the changed retry behavior and prepare a candidate fix if the hypothesis is supported. **Control CT-01:** add the load scenario to repeatable regression checks, retain latency and unsuccessful-outcome checks, and link the test to I-01 and R-01. The fictional engineering lead owns implementation and evidence collection before the next review.

**Invented follow-up C-02:** a revised candidate has 4,960 completions and 40 failures out of 5,000 attempts, with successful-attempt p95 of 830 ms. That is 0.8% failures and 3.75% higher p95 than the baseline. Other checks and an authorized decision would still be required. The example does not establish that a real control was implemented or that a real incident was prevented.

## 6. Verify control behavior and watch for recurrence

A proposed control check would rerun the original synthetic failing candidate to confirm the check flags it, then rerun the revised candidate under the same conditions. Preserve execution logs and investigate unstable results. Record control coverage and false alerts rather than assuming the check is effective because it exists.

For any real deployment, agree a recurrence definition, observation period, exposure denominator, monitoring owner, and review date before drawing outcome conclusions. Changes in workload, architecture, dependencies, or user mix must be recorded. Passing a pre-release check alone is not evidence of sustained reliability improvement.

## The connected record

J-01 defines the journey; B-01 and C-01 describe comparable evidence; CH-01 and I-01 supply context; R-01 records the risk; D-01 records the decision; A-01 and CT-01 connect the response to prevention; follow-up measurements and recurrence review test whether the response remains useful.

The proposed contribution is this traceable handoff across measurement, change context, decision authority, and incident learning. Existing engineering tools may already support parts or all of the chain; PRI does not claim exclusive ownership of those practices or automatic superiority.

Use the [journey worksheet](journey-baseline.md), [risk register](risk-register.md), and [readiness checklist](release-readiness.md) to structure a discussion. See the [review and adaptation guide](review-guide.md) for responsible use.
