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
