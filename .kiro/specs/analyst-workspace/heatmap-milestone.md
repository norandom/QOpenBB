# Heatmap parity

Heatmap is the next UI-12 delivery slice after the published Treemap/Sunburst milestone. The owner authorized this batch on 2026-10-25. Original behavior and the replacement's data contract are being established; Heatmap is not yet accepted in the replacement.

## Scope

Preserve the existing Table/File chart gallery, editor, themes, controls and saved state. Use the existing ECharts host and application session. No new toolbar, hidden feature flag, disabled control or second state owner is permitted. Keep the current published alpha available throughout development.

The first application acceptance target is the ordinary Table/File journey. Selected-range charts and other callers retain their existing obligations; this milestone must not claim those callers accepted without exercising them. Shared guard changes must preserve grouped, pivot, tree, pinned and remote-row restrictions.

## Current findings and open contract

Pinned original frontend: `38dffc33389aca0e4a87e0e88d42f7067aa220df`. Candidate starting source: `33a81d387b62e962ecced465b78bf2d303530468`.

Two bounded original probes establish a wide matrix: one selected category labels row occurrences and numeric field names label columns. Duplicate labels remain separate with aggregation off. Negative and zero observations remain visible; a missing cell leaves its valid companion visible. Native Sum matches the existing ordinary aggregation owner. The [reviewed data contract](heatmap-data-contract.md) therefore reuses ordinary snapshots and setup projection; no third capture kind is planned.

Native Series, gradient Legend, Chart Style and both axis controls were inventoried, including a visible line-width change. These observations do not yet establish complete control parity, color-domain edge semantics, empty selections or candidate behavior. The first capture followed section inspection and is not an untouched appearance baseline.

Freeze these decisions after a compact original probe:

- Category/value field assignments, axis orientation, order and switch-category/series behavior.
- Duplicate-cell reduction with aggregation off and with supported aggregation choices.
- Missing categories and values, valid zero and negative values, equal color domains and empty data.
- Native labels, axes, tooltip, color scale, legend and reachable cell/layout controls, including saved option keys.
- Refresh, family transitions and persistence through the existing session and storage owners.

## Bounded sequence

- [x] Inspect pinned original wrapper and current integration seams.
- [ ] HM0. Observe original behavior and independently review the data/control contract and exact task boundaries.
  - [x] Freeze the bounded matrix data contract from original observations with independent review. Full HM0 remains open.
- [x] HM1. Implement the inactive matrix adapter against existing ordinary setup projection, with focused regressions and maintained-path inventory.
- [x] HM2a. Freeze inactive [renderer/editor declarations](heatmap-renderer-design.md); independently reviewed at Workspace `216e8a296391e64f8e069602332caa09aafa9943`.
- [x] HM2. Implement the renderer and controls in disjoint lanes against frozen interfaces; independently review each lane.
- [ ] HM3. Join shared session, guards, caller and editor routes atomically; verify affected families and saved-state transitions.
- [ ] HM4. Verify an identified packaged image against real FMP values and the original appearance, controls, light/dark themes, refresh, save/reopen and export. Show uncertain differences in qView.
- [ ] HM5. Publish selected FMP examples, reconcile README/docs/breadth, and build one accepted milestone through CI. Verify the release and public image pulls.

Every executable production task must name its exclusive files and public inputs/outputs before dispatch. Caps remain 400 physical lines per file, 300 logical units per file and 50 per function, enforced by the existing inventory/checker. The shared dispatch owner is already 362 physical lines at the starting source; plan a cohesive extraction if needed instead of squeezing additional branches into it. Research, documentation and tests are excluded from production caps.

## Verification and financial fixture

Reuse the existing isolated Playwright/CDP helpers with one worker and no retries. A small synthetic discriminator must establish actual original semantics before implementing the replacement. Preserve original diagnostics as observations; they do not waive candidate errors. New-account onboarding remains the [separate baseline follow-up](../openbb-self-service/first-login-diagnostics.md).

Proposed real fixture: AAPL FY2025 quarterly cost of revenue and gross profit, both reported USD, from retained FMP `/stable/income-statement` observations retrieved on 2026-10-20. The same eight observations already reconcile to 416,161,000,000 USD in the [hierarchy milestone](hierarchy-milestone.md). The prepared fixture uses fiscal-quarter rows and two numeric columns; all eight values independently match the retained raw records. Do not mix percentages and USD on one color scale or convert missing observations to zero. This is retained provider evidence, not a fresh API request.

Real-FMP Heatmap sample: pending an identified application run. A screenshot alone will not establish the cell values, color mapping or behavior.

## Work allocation

Original behavior research and current integration research run independently. After HM0, data/capture work owns new data modules; renderer work owns new ECharts translation modules. Controls may run alongside the renderer only after appearance and command interfaces are frozen. The controller owns shared unions, routing, inventory, integration and selective commits. Independent review checks the joined financial semantics and public behavior. One heavy build or suite runs at a time.

Local source research is retained in `artifacts/chart-heatmap/original-research.md` and `integration-research.md`. These findings are source evidence, not completed browser checks. The [independent assessment-plan review](../../../artifacts/reviewed/chart-heatmap/plan-review.md) approves this research boundary only. HM0 remains open until the original probe resolves the mapping and control questions above.

## Accepted inactive foundation

HM1 is independently accepted at Workspace `0d343b00a5d168ced61a41dfbb931e4f6d4c59f9`. Eight focused tests pass; scoped typing adds no diagnostics to the inherited baseline. The 54-line adapter passes the inventory-backed caps. [Review](../../../artifacts/reviewed/chart-heatmap/data-adapter-review.md). This module is not connected to application routes and does not render Heatmap. Native color/empty-state semantics, renderer/control implementation and packaged acceptance remain open.

## Accepted inactive renderer and controls

HM2b controls (`8fb06e58582c0baea15089fdbf4e03fa70dc0a87`) and HM2c renderer (`8b4426b9ca7f0b04ccfdfa05c495a415f7741ddf`) are independently accepted. Controls pass 21 resolver/intent tests and three editor interaction tests; the renderer passes 12 focused checks plus the eight existing data-adapter checks, including actual ECharts SVG. Both pass lint, baseline-relative typing with no added or owned diagnostics, and inventory-backed size caps. The inherited application type errors remain.

The owner approved effective tooltip suppression and reversal of legend colors and labels together. Review corrected multiline label overflow, axis-label space and a weak hover assertion. See [controls review](../../../artifacts/reviewed/chart-heatmap/controls-review.md) and [renderer review](../../../artifacts/reviewed/chart-heatmap/renderer-review.md). These modules are inactive: application routing, real-FMP rendering, visual approval, refresh, persistence and export remain open. No new image was built for this foundation work.
