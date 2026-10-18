# PRI integration architecture

October 18, 2026 · Local review interface 1.7. The diagram describes the current simulation and a proposed production integration. It does not claim deployment, a connected CI/CD service, real GPU inference or verified savings.

Dashed links represent proposed connections: a real CI/CD build would trigger the representative harness and supply the candidate digest; an engineer would correct a held change and rerun the pipeline. Solid links represent execution or data relationships implemented inside the model. They are logical relationships, not evidence of a deployed network of services.

The harness produces comparable baseline/candidate/revalidation fixtures. Evidence artifacts retain metrics, configuration, seeds and decisions in local JSON and CSV. Production ingestion, durable storage, retention controls and authentication are proposed infrastructure. The policy gate checks coverage/environment and the CPU performance limits; the separate GPU gate checks modeled resource/deadline results and assumed memory fit.

A regression or evidence-quality hold prevents modeled promotion. Eligibility is followed by a fictional human approval, artifact digest, scope and expiry checks. There is no organizational identity provider or production authorization integration. The corrected artifact is supplied by an engineer in the modeled scenario; PRI does not autonomously repair software.

Paired runtime experiments compare an existing monitored process with the gate-driven PRI path using matched inputs. Outcome accounting records failures, retries, latency and resource consumption. GPU allocated instance time is distinct from busy time. Production telemetry, customer outcome joins and billing data must be implemented and calibrated before claiming realized value.

Business assumptions enter the economic calculator separately: exposure, applicability/transfer, eligible irreversible transaction losses, contribution, labor valuation and implementation/operating costs. The calculator avoids overlap, includes costs, and reports gross benefit, net first-year/ongoing value, sensitivity and break-even. Capacity value is not payroll reduction; fixed allocated GPU capacity receives no bill-reduction credit. Financial outputs do not change the gate, workload or experiment evidence.

The incident-history component is deliberately isolated. It illustrates deduplication and contextual review, but is not consumed by the executed gate or financial model. No automatic learning or predictive effectiveness is established by that panel.

The SVG is a code-native asset at assets/pri-system-architecture.svg. It is embedded locally without network requests. Every component has a written status, a keyboard-selectable detail panel and an alternative component list. The diagram's solid/dashed connections are also explained in text. Existing scenarios and financial calculations are unchanged.

## Release walkthrough 1.8

The interactive map now includes play/pause, previous/next, restart and a step slider. The standard hold/correction path has 15 explanatory steps. It follows the selected CPU fixture, including an evidence-quality hold when coverage is insufficient. An unrepresentative fixture uses a shorter admitted-candidate path and does not invent a HOLD or prevention benefit.

Packets trace existing graph links and represent logical evidence/workflow relationships, not user requests, live pipeline activity, or simulator time. The hold-to-CI/CD correction link remains proposed; human review remains fictional. Incident history is never included in the animated executed path. The financial ending identifies annual conditional values from the current selected-CPU calculator, not the saving from one release; other portfolio/GPU scopes remain separate.

Pause freezes the current step and packet. Manual navigation pauses playback, leaving control with the reader. Changing the selected CPU case resets the walkthrough; leaving the Technical Details tab or hiding the page pauses it. Reduced-motion mode retains step highlights/captions without moving packets. No animation starts automatically. All model evidence and financial calculators remain unchanged.
