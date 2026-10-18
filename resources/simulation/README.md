# PRI interactive simulation · public edition 1.8

A reproducible, generated-data decision simulator with Executive Summary, How PRI Works, Business Impact and Technical Details tabs. Includes the animated system architecture, moderate regression, mixed company portfolio and separate AI/GPU batch experiment.

Public page: https://performance-risk-intelligence.github.io/pri-framework/resources/simulation/

All operational evidence is synthetic. Business values are conditional arithmetic, not measured customer savings, a validated predictor or a real GPU benchmark. Financial examples are scenario budgets, not PRI company finances or private business-plan projections. No cloud resources are provisioned by running this package.

Open index.html for the offline interface. Read Report.md and the separate methods files for assumptions, sources, failure boundaries and cost accounting. CPU/GPU evidence and calculation engines are unchanged from the reviewed model version 1.4; interface edition is 1.8.

## Reproduce

Python 3.10 or later, standard library only. From this directory:

```
python3 simulation.py --out results
python3 verify.py
python3 sensitivity.py
python3 verify_business.py
python3 verify_company.py
python3 extended_scenarios.py
python3 gpu_simulation.py
python3 verify_extended.py
python3 build_report.py
```

The page replays saved generated outcomes. Financial controls update conditional arithmetic without rewriting the experiment. GitHub Pages serves static content; it does not execute Python. The downloadable ZIP contains the sources, results, methods and offline page. sha256.json records file integrity.

No private petition/RFE records, letters, employer data, household information, credentials, local QA exports or screenshots are included. Fictional teaching history is not a gate or financial-model input. Real production integrations, identity, telemetry and validation remain separate work.
