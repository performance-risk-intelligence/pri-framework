#!/usr/bin/env python3
import json
from pathlib import Path
from simulation import DEFAULT,experiment
root=Path(__file__).parent/'results';rows=[]
cases=[('Fast incident rollback',dict(rollback_delay_s=0)),('Fast rollback and retry budget',dict(rollback_delay_s=0,retry_budget_fraction=.1)),('Lower demand',dict(base_rps=20,peak_rps=35)),('Slow incident rollback',dict(rollback_delay_s=600)),('Unrepresentative preflight',dict(preflight_bad_multiplier=1)),('Missing preflight records',dict(preflight_coverage=.7))]
for name,changes in cases:
 r=experiment(dict(DEFAULT,replications=4,**changes),root/'sensitivity'/name.lower().replace(' ','_'),verbose=False)
 rows.append(dict(case=name,config_changes=changes,replications=4,failed_journeys_avoided=r['delta_summary']['failed'],production_cpu_s_avoided=r['delta_summary']['cpu_s'],net_cpu_s_including_preflight=r['net_cpu_s_per_incident_including_preflight'],faulty_gate_states=[p['faulty_assessment']['disposition'] for p in r['preflights']],bad_release_promoted=any(p['bad_release_promoted'] for p in r['preflights'])))
(root/'sensitivity.json').write_text(json.dumps(rows,indent=2)+'\n');print(json.dumps(rows,indent=2))
