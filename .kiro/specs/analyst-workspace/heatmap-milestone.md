# Heatmap parity

Heatmap is the next UI-12 delivery slice after the published Treemap/Sunburst milestone. The owner authorized this batch on 2026-10-25. Original behavior and the replacement's data contract are being established; Heatmap is not yet accepted in the replacement.

## Scope

Preserve the existing Table/File chart gallery, editor, themes, controls and saved state. Use the existing ECharts host and application session. No new toolbar, hidden feature flag, disabled control or second state owner is permitted. Keep the current published alpha available throughout development.

The first application acceptance target is the ordinary Table/File journey. Selected-range charts and other callers retain their existing obligations; this milestone must not claim those callers accepted without exercising them. Shared guard changes must preserve grouped, pivot, tree, pinned and remote-row restrictions.

## Current findings and open contract

Pinned original frontend: `38dffc33389aca0e4a87e0e88d42f7067aa220df`. Candidate starting source: `33a81d387b62e962ecced465b78bf2d303530468`.

Original wrapper source supplies numeric labels, theme styling and a tooltip using the chart's x, y and color keys. AG Charts owns the actual matrix construction and native controls. Two displayed category axes do not establish whether the editor accepts two category fields or expands numeric series into the second axis. Observe this before choosing a snapshot shape.

The replacement exposes Heatmap in its gallery but has no live Heatmap session or renderer. Current capture narrowing treats any non-hierarchy capture as ordinary. A third capture kind therefore requires explicit guards and reviewed routing; it must not pass through a single-category projection accidentally.

Freeze these decisions after a compact original probe:

- Category/value field assignments, axis orientation, order and switch-category/series behavior.
- Duplicate-cell reduction with aggregation off and with supported aggregation choices.
- Missing categories and values, valid zero and negative values, equal color domains and empty data.
- Native labels, axes, tooltip, color scale, legend and reachable cell/layout controls, including saved option keys.
- Refresh, family transitions and persistence through the existing session and storage owners.

## Bounded sequence

- [x] Inspect pinned original wrapper and current integration seams.
- [ ] HM0. Observe original behavior and independently review the data/control contract and exact task boundaries.
- [ ] HM1. Add reviewed data contracts, validation, capture and setup with focused financial regressions and maintained-path inventory.
- [ ] HM2. Implement the renderer and controls in disjoint lanes against frozen interfaces; independently review each lane.
- [ ] HM3. Join shared session, guards, caller and editor routes atomically; verify affected families and saved-state transitions.
- [ ] HM4. Verify an identified packaged image against real FMP values and the original appearance, controls, light/dark themes, refresh, save/reopen and export. Show uncertain differences in qView.
- [ ] HM5. Publish selected FMP examples, reconcile README/docs/breadth, and build one accepted milestone through CI. Verify the release and public image pulls.

Every executable production task must name its exclusive files and public inputs/outputs before dispatch. Caps remain 400 physical lines per file, 300 logical units per file and 50 per function, enforced by the existing inventory/checker. The shared dispatch owner is already 362 physical lines at the starting source; plan a cohesive extraction if needed instead of squeezing additional branches into it. Research, documentation and tests are excluded from production caps.

## Verification and financial fixture

Reuse the existing isolated Playwright/CDP helpers with one worker and no retries. A small synthetic discriminator must establish actual original semantics before implementing the replacement. Preserve original diagnostics as observations; they do not waive candidate errors. New-account onboarding remains the [separate baseline follow-up](../openbb-self-service/first-login-diagnostics.md).

Proposed real fixture: AAPL FY2025 quarterly cost of revenue and gross profit, both reported USD, from retained FMP `/stable/income-statement` observations retrieved on 2026-10-20. The same eight observations already reconcile to 416,161,000,000 USD in the [hierarchy milestone](hierarchy-milestone.md). Reshape only after the original field mapping is known. Do not mix percentages and USD on one color scale or convert missing observations to zero. This is retained provider evidence, not a fresh API request.

Real-FMP Heatmap sample: pending an identified application run. A screenshot alone will not establish the cell values, color mapping or behavior.

## Work allocation

Original behavior research and current integration research run independently. After HM0, data/capture work owns new data modules; renderer work owns new ECharts translation modules. Controls may run alongside the renderer only after appearance and command interfaces are frozen. The controller owns shared unions, routing, inventory, integration and selective commits. Independent review checks the joined financial semantics and public behavior. One heavy build or suite runs at a time.

Local source research is retained in `artifacts/chart-heatmap/original-research.md` and `integration-research.md`. These findings are source evidence, not completed browser checks. The [independent assessment-plan review](../../../artifacts/reviewed/chart-heatmap/plan-review.md) approves this research boundary only. HM0 remains open until the original probe resolves the mapping and control questions above.
