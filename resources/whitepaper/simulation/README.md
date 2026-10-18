# PRI synthetic study

Companion to PRI White Paper version 1.0, October 18, 2026.

All observations are generated. This executes a reference analysis; it does not time an application or validate a predictor. See Section 12 of the paper for the generating process, estimand, policy, limitations and interpretation.

## Reproduce

Use Python 3.10 or later, standard library only. From this directory:

```sh
python3 pri_synthetic_study.py --out results
```

To export all 90,000 generated observations as well:

```sh
python3 pri_synthetic_study.py --out reproduction --raw
```

The raw export is optional and generated locally. No private data, credentials or network calls are used.

## Files

- `pri_synthetic_study.py`: generator, summary, paired bootstrap, illustrative rule and invariant checks.
- `results/summary.json`: parameters, runtime version, analysis method and calculated scenario results.
- `results/batch_summary.csv`: 180 generated batch summaries, including nine scenarios.
- `results/checks.json`: outcome reconciliation and selected expected-disposition checks.
- `results/sha256.json`: integrity checks for the result files and source script.

Matching the recorded Python runtime is recommended for exact-byte reproduction. Neutral and baseline share the random stream and are identical by construction. This is not a false-positive-rate experiment. The bootstrap interval describes mean batch p95 change, not pooled p95. A data hold takes precedence over regression interpretation. Eligible for review never means production approval.

## Next work

The operational benchmark service, real adapters, identity-backed approvals, expiry and replay protection remain proposed implementation. Preserve new measured evidence under a distinct study ID. Do not relabel generated values as measured service performance.

Licensing and permitted reuse follow the applicable repository terms; this README does not grant new rights.
