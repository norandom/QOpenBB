# Implementation plan

Current production UI priorities are collected in the [UI parity worklist](ui-parity-worklist.md). It distinguishes actual application deliverables from the historical source-helper and reference-test tasks below; it does not alter their recorded approval or acceptance.

## Unreleased local image inspection

The owner requested a local image check while resuming UI work on 2026-10-19. This bounded development check packages the accepted UI revision; it does not satisfy the renderer-complete 2.12 or deployment 4.1 gates.

- [ ] 2.91 Build and inspect the current unreleased local images
  - Controller owns exact source pins, filtered stages, Dagger export/load records and one concise reviewed record. Use the existing pinned image_cli commands with fresh stage directories and clean exact-commit owned source checkouts; preserve unrelated working changes and exclude private files.
  - Serialize Workspace and data-api builds through the single heavy-work queue. Record source revisions, archive hashes, engine identity and loaded image IDs. Do not publish or label these images release-ready.
  - Run the existing Workspace packaging smoke and data-image offline checks with disposable state and missing/synthetic provider keys. Reuse tests/delivery/workspace_runtime.py with an explicit image-only mode mutually exclusive with source overlay; retain private descriptors and ownership cleanup. Keep source-overlay mode unchanged. Image-only mode mounts only disposable /data and records that fact without asserting full release verification.
  - Reuse isolated Playwright fixtures to open the frontend from the exact loaded image, log in with the disposable account, and verify visible application shell and diagnostics. No Vite server or source mount may establish this packaged-image result. Own only necessary test-helper changes and a focused built-page check; do not introduce another harness.
  - Done when independent review accepts actual build/runtime identities, packaging/offline results and the inspected built page. Sync one concise record and necessary screenshot before commit. Production changes require a separately bounded owning-task repair and the existing 400/300/50 caps; tests and evidence are cap-exempt.
  - This checkpoint does not accept all chart families, catalog identity 3.8, controlling Compose 4.1, live providers, Anthropic, Excel, publication or deployment.
  - _Boundary: Unreleased local image packaging and built-page accessibility_
  - _Depends: 2.90, 2.5, 3.6_
  - _Requirements: 1.1, 1.2, 3.2, 9.1, 10.5, 10.6_

## Gallery refinement before local image inspection

- [ ] 2.92 Preserve gallery navigation and refine miniature drawings
  - Owner approved this refinement on 2026-10-19. Follow the existing [gallery design](chart-gallery-design.md), including its transient scroll amendment. Controller owns caller/dock/gallery navigation; Sol owns thumbnail drawings and focused tests; independent Sol reviews the final diff. No shared writable paths between lanes.
  - Done when supported-family changes, tab navigation and theme updates preserve gallery scroll; hidden mounts cannot overwrite it; area/scatter miniatures are compared in qView; existing order, controls and selection remain. Reuse the existing browser helpers and focused unit suite. Whole modified production files must pass 400 physical/300 logical/50 per-function caps.
  - _Boundary: Gallery appearance and transient navigation only; no new storage, flags or renderer admission_
  - _Requirements: 4.7, 4.9, 10.1, 10.2, 10.5, 10.6_

## Ordinary area charts: autonomous UI-10 continuation

Owner requested autonomous UI/UX progression after reviewing the [area design](chart-area-design.md). This authorizes design/task progression and implementation within the original parity constraints; independent reviews, complexity caps and owner decisions on uncertain visible deviations remain. No repeated phase confirmation is required for this bounded track.

Execution: 2.86 contract -> 2.87 numerical / 2.88 editor in parallel -> 2.89 renderer after 2.87 (may overlap 2.88) -> 2.90 application join. Sol implements bounded units; Astra reviews financial contracts and integration. At most four active agents, one heavy browser/build run, selective per-task commits. Each task is a 1-3 hour unit; unresolved native geometry requires a concrete adapter design repair, never an approximation or hidden feature reduction.

Paths follow the area design: production paths relative to Workspace `terminalpro/src/components/General/Table/Chart/`, tests relative to Workspace `terminalpro/`. All modified production files must pass existing whole-file 400 physical / 300 logical / 50 per-function checks with explicit change manifests. Controller owns inventory, breadth, source pins and artifact publication. No lane reverts another lane's edits; production interfaces freeze before dependent work. No flags or new dependencies.

- [x] 2.86 Freeze original area contracts and native geometry compatibility
  - Own `echarts/cartesianTypes.ts` type-only extensions, new `echarts/cartesianAreaTypes.ts`, fixture `tests/unit/chart-compatibility/fixtures/area-charts.json`, and focused contract/native discriminator tests in `tests/unit/chart-compatibility/cartesian.area-contract.test.ts`. Runtime admission and transitive normalization predicates remain unchanged.
  - Reuse installed original source/runtime and native ECharts fixtures. Freeze signed ordered accumulation, normalization extent, original processed labels/raw tooltips, null/gap/zero/single-series behavior, category/percent axis and crosshair, original control/default predicates, legend lifetime and miniature construction. Separate source inference from observed effects and preserve original single-date caller conversion.
  - Use one bounded synthetic original journey only for unresolved visible contracts; verify native fill/stroke boundaries for signed crossings and missing stacks. A failed native discriminator requires reviewed adapter design correction before dependent production work, not bar-style substitution. Capture executable paths/package identities and actual results without new harness/install.
  - Done when independent Astra review accepts immutable typed projection inputs/output and fixture, native strategy is demonstrated for the discriminators, scoped consumer checks and whole-file caps pass, and downstream tasks have runnable focused commands. Tests/docs are cap-exempt; production contract files are not.
  - _Boundary: Frozen area numerical/editor contract and existing runtime prerequisite_
  - _Depends: 1.4, 2.85_
  - _Requirements: 4.8, 4.9, 10.1, 10.2, 10.4, 10.5, 10.6_

- [x] 2.87 (P) Project original area boundaries without changing raw observations
  - Own new `echarts/cartesianArea.ts`, cohesive `echarts/cartesianAreaSpans.ts`, and `tests/unit/chart-compatibility/cartesian.area-values.test.ts`; read frozen interfaces/fixture only. Implement independent, ordered stacked and normalized area projection, enabled membership, raw-versus-drawn separation and gap metadata. Do not change native renderer, editor or caller admission.
  - Preserve source-backed zero/missing/hidden semantics and finite large-value behavior. Expected signed endpoints and denominator must be independently calculated from the frozen fixture, including reordered series and cross-category sign changes.
  - Done when RED/GREEN focused numerical checks cover these effects, raw snapshot remains unchanged, scoped static checks and 400/300/50 caps pass, controller registers the helper, and independent financial review accepts the projection.
  - _Boundary: Pure area numerical projection_
  - _Depends: 2.86_
  - _Requirements: 4.8, 4.9, 10.3, 10.4, 10.5, 10.6_

- [x] 2.88 (P) Bind original area settings to the existing editor
  - Own `application/effectiveAppearance.ts`, `application/effectiveAppearanceDefaults.ts`, `application/effectiveAppearanceSeries.ts`, `compatibility/editorBindings/eligibility.ts`, `compatibility/editorBindings/mapApplicationEditorEvent.ts`, `compatibility/editorBindings/selectApplicationEditorState.ts`, `compatibility/editorBindings/rehydrateApplicationEditorEvent.ts`. Own `tests/unit/chart-application/editorArea.test.tsx`; no shared renderer/contract edits.
  - Read/write the original area namespace and preserve inactive branches; apply frozen marker, labels, fill/stroke, dash, opacity, shadow and connect-missing predicates/defaults. Keep existing editor widgets, labels, layout and flags. Area is neither a bar namespace nor automatically every line control.
  - Done when actual editor actions yield correct saved leaves and resolved values for all three area types, existing seven-family regressions remain valid, RED/GREEN checks and scoped static checks pass, whole modified files satisfy 400/300/50, and independent review accepts the lane. Live geometry joins later.
  - _Boundary: Area appearance and original editor bindings_
  - _Depends: 2.86_
  - _Requirements: 4.7, 4.8, 4.9, 10.3, 10.4, 10.5, 10.6_

- [x] 2.89 (P) Render area fills, boundaries and independent overview
  - Own new `echarts/cartesianAreaSeries.ts` for native area series assembly, plus `echarts/cartesian.ts`, `echarts/cartesianSeries.ts`, `echarts/cartesianAxes.ts`, `echarts/cartesianDisplay.ts`, `echarts/cartesianTooltip.ts`, `echarts/cartesianStyle.ts`, `echarts/cartesianNavigator.ts`, `echarts/cartesianLayout.ts`, `echarts/cartesianBarColors.ts`, and `tests/unit/chart-compatibility/cartesian.area.test.ts`. Read accepted pure projection and frozen appearance contract. Cohesive extractions must be assigned before edits.
  - Use isolated baseline/delta fill spans, separate internal strokes and stable row-indexed public marker/label series from the reviewed native refinement. Exclude internal tooltip parameters and preserve hidden geometry in miniature cloning. Reproject all area families on legend changes. Use the proven native strategy for ordered signed fills/strokes, null gaps and normalized coordinates, preserving original processed labels/raw tooltips, area markers, axis spacing/domain and percent formatting. Keep all seven accepted families unchanged; no bar-normalization fallback for areas.
  - Project overview from independent full inputs where the original contract requires it, preserving physical-X navigation and full extent. Native legend membership changes main geometry without corrupting the overview.
  - Done when native geometry, renderer options and affected regression checks pass with RED evidence, scoped static checks and 400/300/50 caps pass, and independent review accepts the renderer. No application activation in this lane.
  - _Boundary: ECharts area mapping and overview_
  - _Depends: 2.86, 2.87_
  - _Requirements: 4.8, 4.9, 10.3, 10.4, 10.5, 10.6_

- [x] 2.90 Join all three area families into the existing Workspace journey
  - Controller owns `echarts/cartesianTypes.ts` final admission predicates, `application/applicationSessionProjection.ts`, `application/axisStructure.ts`, and necessary `AgChartView.tsx` / `caller/chartInputs.ts` changes. Activate only after both renderer and editor lanes are frozen/reviewed; reuse native callback/scope and existing persistence owners.
  - Own `tests/unit/chart-application/callerArea.test.ts`, necessary `applicationSession.test.tsx` cases, and `tests/e2e/live-chart/area-charts.spec.ts`. Reuse existing helpers; preserve exact family/range/unknown branches and original single-date entry conditions.
  - Run one joined actual Workspace journey through three area types: signed observations, raw tooltip, marker/fill/stroke control effects, legend plus theme/data updates, category navigator/full overview, light/dark view, current PNG and fresh-session reopen. Reuse already accepted save-failure/restart evidence unless changed owners create a concrete risk.
  - Done when focused tests and isolated browser/CDP journey pass, representative views/export are inspected, uncertain visible deviations receive an owner decision, independent Astra integration review passes, and the combined scope passes 400/300/50. Sync concise review and necessary synthetic screenshots before selective commit/push; update breadth and UI-10 only for demonstrated scope. Release-image and other families remain pending.
  - _Boundary: Explicit ordinary Table/File area integration_
  - _Depends: 2.88, 2.89_
  - _Requirements: 4.7, 4.8, 4.9, 10.1, 10.2, 10.3, 10.4, 10.5, 10.6_

Commands reuse the installed pinned Node, chart-compatibility/chart-application Vitest configs, scoped Biome, existing isolated Playwright config and `python -m tools.quality.complexity --check` with explicit fork manifests. Task 2.86 records exact executable paths. No planned command is passing evidence.


## Ordinary 100% stacked columns and bars: UI-10 next slice

Owner approved the [normalized-bar design](chart-normalized-bars-design.md), including a working horizontal overview. Owner approved tasks 2.82-2.85 for implementation. They cover exactly `normalizedColumn` and `normalizedBar`; broader UI-10 and release acceptance remain pending.

Execution: controller prerequisite 2.82 -> parallel Sol lanes 2.83 / 2.84 -> controller application join 2.85. Each task is a 1-3 hour unit with independent review and a selective commit. Astra reviews the contract and final integration. Keep at most four active agents, one heavy browser/build check, and one worker per focused unit-test process. No worker may revert another lane's changes. Shared files freeze before fan-out; stop affected lanes if the contract changes. Root inventory, breadth, source pins and publication belong exclusively to the controller.

Production paths below are relative to `vendor/workspace/terminalpro/src/components/General/Table/Chart/`; test paths are relative to `vendor/workspace/terminalpro/`. All tasks require whole modified production files to pass 400 physical lines / 300 logical units / 50 per function using the existing tasks 1.3/1.4 checker and explicit fork manifests. Register the new helper; agree cohesive extraction paths before editing, with no implicit size exception. Tests, synthetic fixtures and documentation are cap-exempt. Focused verification accompanies each implementation; no new harness or separate evidence-only lane.

- [x] 2.82 Freeze normalized geometry, legend contracts and the reference runtime
  - Controller owns `echarts/cartesianTypes.ts`, request interfaces only in `echarts/lifecycle.ts`, `application/applicationSessionTypes.ts`, and new `tests/unit/chart-compatibility/fixtures/normalized-bars.json`. Freeze family predicates without activating callers, immutable projection inputs/output, stable series-ID/native legend-key mapping, callback/scope/error fields and the independent overview seam for both lanes and the join.
  - Reuse the installed original runtime, retained sources and isolated synthetic probe to settle remaining percent-axis/crosshair precedence, zero/missing fallback domain, legend reset/save lifetime and both miniature outcomes. Record source revision/package hashes, exact executable paths and scoped verification commands; restore only the existing owned fixture if necessary. No new installation, capture framework or Dagger build.
  - Freeze independent signed expectations for max(positive sum, absolute negative sum), enabled-series membership, raw tooltip/label formatting and full-series miniature normalization. The approved working horizontal overview is explicit; contradictions or further necessary visible deviations stop the dependent work for a concrete owner decision.
  - Done when the fixture and typed contracts pass independent Astra review, existing scoped consumers pass their applicable checks, whole-file caps pass, and both lanes have exact read-only contracts and runnable commands. Record known baseline compiler limitations without claiming a full application compiler pass. Subsequent lifecycle implementation ownership transfers exclusively to 2.84.
  - _Boundary: Shared normalized contract and existing reference/toolchain setup_
  - _Depends: 1.4, 2.81_
  - _Requirements: 4.8, 4.9, 10.1, 10.2, 10.4, 10.5, 10.6_

- [x] 2.83 (P) Render normalized signed columns and bars with an independent overview
  - Sol renderer owns new `echarts/cartesianNormalization.ts`, plus `echarts/cartesian.ts`, `echarts/cartesianSeries.ts`, `echarts/cartesianAxes.ts`, `echarts/cartesianDisplay.ts`, `echarts/cartesianNavigator.ts`. Read the frozen types/fixture; do not edit lifecycle, host or application owners.
  - Normalize drawn coordinates after existing setup projection, preserving raw observations and signed accumulation. Derive finite domains from endpoints plus zero; apply the frozen default percent-axis precedence while retaining raw financial labels/tooltips and category formatting. Handle missing, zero and all-hidden values without fabricated financial zeros or nonfinite geometry.
  - Reproject main geometry from enabled membership. Independently compute the full selected-series overview with all series enabled. Keep physical-X navigation: category crop for columns and numeric crop retaining rows for bars; viewport clipping never changes the denominator. Preserve all five accepted families.
  - Own new `tests/unit/chart-compatibility/cartesian.normalized.test.ts` and necessary changes only to existing `cartesian.application.test.ts`; verify unequal signed native endpoints, membership changes, null/zero/all-hidden cases, raw labels/tooltips, percent axes and independent overview using the frozen fixture and existing one-worker config.
  - Done when these focused checks and affected scoped lint/type checks pass, the pure helper is registered in the existing inventory by the controller, whole modified files pass 400/300/50 caps, and independent review accepts the renderer. This is not caller or application acceptance.
  - _Boundary: ECharts Cartesian arithmetic, presentation and overview projection_
  - _Depends: 2.82_
  - _Requirements: 4.8, 4.9, 10.3, 10.4, 10.5, 10.6_

- [x] 2.84 (P) Keep native legend interactions current across chart revisions
  - Sol lifecycle owns implementation in `echarts/lifecycle.ts` and `echarts/EChartsHost.tsx` after interface freeze. Own only `tests/unit/chart-compatibility/lifecycle.test.ts` and `host.test.tsx` for focused verification; do not edit renderer arithmetic or application session types.
  - Pass request fields atomically and subscribe once to native legend changes using the latest accepted callback. ECharts remains the only transient selection owner: retain matching stable IDs and native zoom, enable new IDs, reset on scope change/disposal, and apply reprojected options without event recursion. Do not persist selections or add a parallel React store.
  - Route failures through the existing error channel and invalidate current export; remove listeners, release partially initialized instances and reject late callbacks after disposal. Export must reflect current native geometry under the existing revision gate.
  - Done when focused tests establish latest-request behavior, pruning/new IDs, all-hidden handling, scope reset, zoom retention, theme/data/resize updates, initialization cleanup, failure/export freshness and nonrecursive events. Scoped lint/type checks and whole-file 400/300/50 caps pass, with independent review before joining.
  - _Boundary: Native ECharts host interaction and lifecycle_
  - _Depends: 2.82_
  - _Requirements: 4.8, 4.9, 10.3, 10.4, 10.5, 10.6_

- [x] 2.85 Join both normalized families to the existing Workspace journey
  - Controller owns this explicit integration task after both lanes freeze and pass review: `AgChartView.tsx`, `application/effectiveAppearance.ts`, `application/axisStructure.ts`, `application/applicationSessionProjection.ts`, `application/useApplicationChartSession.ts`, `compatibility/editorBindings/mapApplicationEditorEvent.ts`, `compatibility/editorBindings/selectApplicationEditorState.ts`; `caller/chartInputs.ts` only if shared predicate propagation is insufficient. Compose the frozen callback over immutable current inputs, assign stable scope and pass all request fields atomically. No new storage owner or family registry.
  - Admit exactly both normalized families through current guards, preserving distinct family ranges, saved types, unknown/inactive branches, physical-axis controls, existing themes/actions and all five accepted families. Do not hide or disable any control or flag. Arithmetic/overview and native state ownership remain in the reviewed lanes.
  - Own existing `tests/unit/chart-application/editorBindings.test.ts`, `editorSavedLeaves.test.ts`, new `callerNormalizedBars.test.ts`, and only necessary changes to `applicationSession.test.tsx` / `applicationSessionTransactions.test.ts`. Own new `tests/e2e/live-chart/normalized-bars.spec.ts`, reusing existing import/editor/action/persistence/diagnostics helpers. Shared helper changes require a demonstrated need and remain controller-only.
  - Run one joined actual Workspace journey covering both orientations with signed observations, raw tooltip, legend hide/restore followed by ordinary revision updates, distinct ranges and physical-axis edit, navigator/full independent overview, light/dark appearance, current exported image and fresh backend reopen preserving unknown branches. Reuse accepted aggregation/save-failure/restart evidence unless a changed owner creates a concrete regression risk; do not expand into another matrix.
  - Done when focused units and the single isolated journey pass strict diagnostics, representative views/export are inspected, uncertain visible differences have an owner decision, independent Astra integration review passes and the combined 2.82-2.85 whole-file 400/300/50 audit passes. If integration cannot remain a bounded 1-3 hour unit, report the concrete remaining boundary instead of silently expanding it.
  - Update breadth/UI-10 only for proven behavior; sync one concise reviewed record and necessary synthetic screenshots before selective commit/push. Disclose source overlays and preserve unrelated edits. Release images and remaining UI-10 are not accepted by this task.
  - _Boundary: Explicit ordinary Table/File normalized application integration_
  - _Depends: 2.83, 2.84_
  - _Requirements: 4.7, 4.8, 4.9, 10.1, 10.2, 10.3, 10.4, 10.5, 10.6_

Planned commands reuse the pinned installed toolchain. From Workspace `terminalpro`, run `node node_modules/vitest/vitest.mjs run --config tests/unit/chart-compatibility/vitest.config.mjs <owned-test-paths>` or the existing chart-application config. From QOpenBB, select `normalized-bars.spec.ts` with the existing Playwright CLI/config and owned runtime/evidence environment. Use `python -m tools.quality.complexity --check --changes workspace=<current-manifest> --changes data_api=<current-manifest> --output <ignored-report>`. Task 2.82 verifies executable paths and exact scoped type/lint commands. These are planned checks, not completed evidence.


## Ordinary horizontal bars: UI-10 first slice

Owner approved the [horizontal-bar design](chart-horizontal-bars-design.md). The four tasks below restore `groupedBar` and `stackedBar` in ordinary Table/File widgets. Other gallery choices stay visible under their original predicates; their implementation and complete UI-10 acceptance remain pending. Owner approved tasks 2.78-2.81; implementation proceeds under the established autonomous workflow.

Execution: controller contract freeze -> two disjoint Sol lanes (2.79 and 2.80) -> controller application join. Astra reviews the prerequisite and the final integration; each implementation retains independent task review and a per-task commit. At most four active agents and one heavy build/browser check. Accepted foundation tasks 1.3/1.4 supply the inventory/checker; do not create another harness. Each task is a bounded 1-3 hour work unit; if a concrete contract cannot be settled or a lane exceeds its boundary, report the exact blocker rather than silently expanding scope.

Production ownership uses the exact paths in the approved design. All paths below beginning `tests/` are relative to `vendor/workspace/terminalpro/`. Shared configurations, source pins, breadth, inventory and artifact publication remain controller-owned. No worker may edit another lane's files or revert unrelated changes. Before fan-out, the controller records any needed cohesive extraction paths in its handoff; no broad wildcard ownership or unreviewed size exception.

- [x] 2.78 Freeze original horizontal-bar expectations and the shared family contract
  - Controller owns this explicit contract/setup integration task: reuse the installed original reference and existing isolated browser infrastructure, verify tool/package/source identities and disposable state, and bind the exact verification commands before dependent work. If runtime recovery is necessary, restore only the owned existing fixture; no alternate application or new capture framework.
  - Establish grouped/stacked top-to-bottom category order, unequal signed-stack endpoints, zero/missing observations, navigator target/extent and full miniature behavior. Inspect retained source first; perform only the bounded original observation needed to settle unresolved effects. Independently review the resulting fixture and reference expectations before renderer work. Original failures or necessary visible deviations require owner decision; never hide the action.
  - Own new `tests/unit/chart-compatibility/fixtures/horizontal-bars.json` with synthetic inputs, independent expected results and exact original provenance; the other lanes read it without modifying it. Record the finite axis/title/direction and family-transition contract beside the design. Extend the existing family union/predicate in `echarts/cartesianTypes.ts` and existing axis/session type declarations only where necessary, without enabling production callers. Preserve exact saved types, semantic IDs, original range transitions and runtime-only structural axes.
  - Done when original expectations are attributable and independently reviewed, the typed groupedBar/stackedBar contract is consumable by both lanes, current consumers still compile under their existing scoped gate, and each lane has exact non-overlapping files/tests and runnable commands. A guessed navigator target or category order prevents completion.
  - Update the existing complexity inventory/changed-file scope for any production type changes. Whole modified production files pass 400 physical / 300 logical / 50 per-function caps; synthetic fixtures and documentation are cap-exempt. No full application compiler claim follows from the known existing DS diagnostic.
  - _Boundary: Shared horizontal-bar contract and existing reference/toolchain setup_
  - _Depends: 1.4, 2.77_
  - _Requirements: 4.8, 4.9, 10.1, 10.2, 10.4, 10.5, 10.6_

- [x] 2.79 (P) Render grouped and stacked horizontal bars with original actions
  - Sol renderer lane owns only the design's `echarts/` mapping/layout/color/navigator files, excluding controller-owned `cartesianTypes.ts`. Reuse the existing snapshot, display policy and native ECharts host. Extend orientation and signed stacking without transposing source observations or rewriting saved types.
  - Implement the source-established category order, grouping/stacking, labels, tooltips, palette and financial formatting. Navigator/miniature follows the independently frozen original contract, including the main extent and unchanged overview; do not infer its target from bar direction. Preserve all accepted column/line projections and existing action predicates.
  - Own new `tests/unit/chart-compatibility/cartesian.horizontal.test.ts` and any required changes to existing `cartesian.application.test.ts`, `cartesian.geometry.test.ts`, `cartesian.grid.test.ts`. Read the shared horizontal fixture; do not change it or the controls/session tests. Use the existing compatibility Vitest config and one worker.
  - Done when independent expected observations and endpoints distinguish grouped from stacked bars, missing/zero/negative values remain correct, applicable actions project correctly, and affected existing column/line checks pass. No caller activation or standalone preview counts as application acceptance.
  - Whole modified production files pass 400 physical / 300 logical / 50 per-function caps and affected scoped type/lint checks; reuse the current inventory and explicit fork scope. Focused tests accompany the production change, not a separate evidence-only workstream.
  - _Boundary: Existing ECharts Cartesian projection and action geometry_
  - _Depends: 2.78_
  - _Requirements: 4.8, 4.9, 10.3, 10.4, 10.5, 10.6_

- [x] 2.80 (P) Bind the existing axis and title controls to physical direction
  - Sol controls lane owns the design's `ApplicationAxisEditor`, `ApplicationCustomizeEditor` and named editor-binding files. Keep Horizontal before Vertical while resolving the semantic axis from current direction: bars show number horizontally and category vertically. Preserve original category-only controls, eligibility, position choices, typography and themes.
  - Both displayed values and latest-state intent rehydration use the current concrete bindings. Writes preserve actual option type and both original positions for that direction; retain unknown/inactive branches and the disclosed structural-axis/Auto Rotate limitations. Do not add saved axes, controls, flags or an alternate editor.
  - Own new `tests/unit/chart-application/editorHorizontalAxes.test.tsx` plus existing `editorBindings.test.ts` and `editorSavedLeaves.test.ts`. Reuse existing application config, component helpers and shared source fixture read-only; do not change mapper or caller/session test files.
  - Done when physical title/axis edits change the correct semantic option leaves, section order stays Horizontal/Vertical, stale render bindings cannot misroute an edit, and accepted column/line controls retain behavior. No inert control or hidden gallery choice is permitted.
  - Whole modified production files pass 400 physical / 300 logical / 50 per-function caps and affected scoped type/lint checks. Any cohesive extraction path is agreed with the controller before editing; tests/docs are cap-exempt.
  - _Boundary: Existing controlled editor composition and option bindings_
  - _Depends: 2.78_
  - _Requirements: 4.7, 4.8, 4.9, 10.3, 10.4, 10.5, 10.6_

- [x] 2.81 Join horizontal bars to the real Workspace journey
  - Controller owns the design's caller initialization, existing session runtime/scope/selection and `AgChartView` admission files after both lanes freeze and pass independent review. Initialize and transition category/y and number/x correctly, preserve original per-family ranges/options and the existing sole Widget persistence owner, and keep other-family buttons/flags intact.
  - Own new `tests/unit/chart-application/callerHorizontalBars.test.ts` and focused changes to `applicationSession.test.tsx` / `applicationSessionTransactions.test.ts` only when the changed lifecycle requires them. Own new `tests/e2e/live-chart/horizontal-bars.spec.ts`; reuse existing login/import/editor/persistence/diagnostics/action helpers. Modify shared browser helpers only for a demonstrated reusable need, not a second harness.
  - Exercise column -> groupedBar -> stackedBar -> column with unequal signed observations and distinct retained ranges. Verify actual drawn orientation, labels/tooltips, physical title/axis edits, applicable navigator/miniature effects, table return, current export and backend fresh-session reopen of a bar family including unknown settings. Inspect representative integrated light/dark views and retain original restore limitations. Reuse accepted aggregation, save-failure and restart evidence unless a changed owner creates a specific regression risk.
  - Done when the affected real-route browser check passes with one headless worker and unchanged strict diagnostics, the exported image matches the latest saved view, independent Astra review approves the integrated scope, and uncertain visible differences have an owner decision. A source-overlaid runtime is disclosed; this does not accept a release image or the rest of UI-10.
  - Run the existing combined complexity gate over all production files touched by 2.78-2.81 with explicit fork manifests: 400 physical / 300 logical / 50 per-function. Preserve unrelated working-tree changes. Update breadth/UI-10 only for proven horizontal-bar behavior. Sync one concise reviewed delivery record and necessary screenshots before the task commit/push; raw diagnostics remain local.
  - _Boundary: Explicit ordinary Table/File application integration_
  - _Depends: 2.79, 2.80_
  - _Requirements: 4.7, 4.8, 4.9, 10.1, 10.2, 10.3, 10.4, 10.5, 10.6_

Verification commands reuse the installed pinned toolchain: from Workspace `terminalpro`, `node node_modules/vitest/vitest.mjs run --config tests/unit/chart-compatibility/vitest.config.mjs <owned-test-paths>` or the existing chart-application config. From QOpenBB, the existing Playwright CLI/config selects `horizontal-bars.spec.ts` with the owned runtime/evidence environment. The existing `python -m tools.quality.complexity --check --changes workspace=<current-manifest> --changes data_api=<current-manifest> --output <ignored-report>` remains the size gate. Task 2.78 verifies exact executable paths and records scoped type/lint invocations; examples here are planned commands, not completed evidence. No dependency installation or Dagger build is part of this slice.


## Current production task: widget editing

The owner's latest production-UI "go" authorizes the bounded existing-owner repair below. The [concrete design](widget-edit-design.md) passed independent Astra review after removing the speculative completion/cancellation API. This does not authorize full renderer activation or complete the wider UI-01/UI-06 work packages.

- [x] 2.46 Repair replayed widget edits at the existing production owner
  - Accepted at Workspace `708d6bb`: [independent review](../../../artifacts/reviewed/task-2.46/review/review.md), 12 focused regressions, scoped types/lint and whole-file caps. Full application type checking remains unverified.
  - Preserve `useWidgetSync`'s existing API, object-replacement semantics, persistence predicate, override behavior, shared subscriptions and explicit save. Replace captured-function mutation and updater-side effects with pure ordered reduction and committed delivery in that same owner.
  - Own `Widget.hooks.tsx`, cohesive `components/widgetSync` extraction modules, and focused hook tests. No context/schema, dependency, chart-guard, feature-flag or release changes.
  - Done when the actual production hook preserves intervening fields during replay and rapid edits, delivers committed effects once in order, and saves the latest committed state. Cover legacy force-save, override, group/refresh and StrictMode behavior with focused tests and independent review.
  - Register maintained modules and enforce whole-file 400 physical / 300 logical / 50 per-function caps. Reuse installed tooling, scoped type/lint checks and existing test infrastructure. Include focused evidence in the per-task commit.
  - _Boundary: Existing widget state owner and its effects_
  - _Depends: 1.4, 2.45_
  - _Requirements: 4.7, 4.8, 4.9, 10.4, 10.5, 10.6_

- [x] 2.47 (P) Implement the original chart-type gallery as a controlled UI component
  - Follow the [gallery design](chart-gallery-design.md). Own the production gallery/catalog/thumbnail modules and focused tests/story. Keep application flags, guards, storage and rendering integration unchanged.
  - Done when the observed ordered gallery renders in the original compact style, all supplied choices work by pointer/keyboard, and exact model types reach the caller without hidden filtering or fallback. Show an explicitly scoped component preview for owner visual comparison.
  - Whole production files pass 400 physical / 300 logical / 50 per-function caps, scoped type/lint and meaningful component checks with independent review. Reuse existing tooling and original screenshots; no new reference capture infrastructure.
  - Implemented at Workspace `b244082`; independent component review passed. Owner accepted the shown [gallery preview](../../../artifacts/reviewed/task-2.47/implementer/gallery-light-dark.png) on 2026-10-17 (reply: "ok"). Dashboard integration and Storybook runtime are not accepted.
  - _Boundary: Controlled chart-type selection UI; no session or storage ownership_
  - _Depends: 2.45_
  - _Requirements: 4.8, 4.9, 10.1, 10.4, 10.5, 10.6_


- [x] 2.48 Connect the accepted gallery to the original dock navigation
  - Accepted at Workspace `a83f711`: [review](../../../artifacts/reviewed/task-2.48/review/review.md), four focused tests and isolated dark/light browser navigation passed. Scoped TypeScript retains the reproduced unchanged DS diagnostic; full application integration is pending.
  - Implement the [dock design](chart-editor-dock-design.md): controlled Chart / Set Up / Customize tabs, collapse/reopen, theme rebuild behavior and retained active-panel state/scroll.
  - Own `Chart/editor/ChartEditorDock.tsx`, cohesive dock styles/helpers, focused tests and development-only story. Require supplied Set Up/Customize content; introduce no fake production panels, storage owner, flags or renderer activation.
  - Done when real production component composition preserves the measured navigation behavior, exact gallery callbacks and accessible focus in dark/light previews. Preview fixture panels must be identified as fixtures; application integration remains pending.
  - Whole production files pass 400 physical / 300 logical / 50 per-function caps and scoped type/lint checks. Reuse existing isolated tooling and screenshots; independently review before acceptance and commit.
  - _Boundary: Dock component and gallery composition; full panel controls and session wiring remain separate_
  - _Depends: 2.47_
  - _Requirements: 4.8, 4.9, 10.1, 10.4, 10.5, 10.6_

- [x] 2.49 (P) Implement the real Set Up controls
  - Follow the frozen [controls design](chart-editor-controls-design.md). Own `Chart/editor/setup/`, focused setup tests and story; preserve stable category/series IDs, exact controlled callbacks and the original chips/switches layout.
  - Done when category choice, aggregation retention, series removal/reorder and category/series switching work by pointer and keyboard in the real panel. No data calculations, storage writes, flags or renderer activation.
  - Whole production files pass 400 physical / 300 logical / 50-function caps. Run focused unit/browser, scoped types/lint and independent review; retain known unchanged DS type-check limitations honestly.
  - _Boundary: Controlled Set Up panel; chart-session transformations remain separate_
  - _Depends: 2.48_
  - _Requirements: 4.8, 4.9, 10.1, 10.4, 10.5, 10.6_

- [x] 2.50 (P) Implement all four caption sections in Titles
  - Follow the frozen [controls design](chart-editor-controls-design.md). Own `Chart/editor/titles/`, focused title tests and story; all four captions retain independent text, typography, alpha color and spacing.
  - Done when every observed control emits a typed edit, disabled values survive, unknown choices remain visible and invalid numeric/color drafts do not corrupt state. Compose the real subsection into the dock preview, clearly identifying remaining Customize groups and storage wiring.
  - Whole production files pass 400 physical / 300 logical / 50-function caps. Run focused unit/browser, scoped types/lint and independent review; no new reference harness, flags or dependency installation.
  - _Boundary: Controlled Titles subsection; persisted style mapping and other Customize groups remain separate_
  - _Depends: 2.48_
  - _Requirements: 4.8, 4.9, 10.1, 10.4, 10.5, 10.6_

- [x] 2.51 (P) Restore the Legend controls in the original dock style
  - Follow chart-legend-padding-design.md. Implement every observed Legend field, exact typed callbacks, retained disabled/unknown values and alpha color behavior. Preserve original labels, order and size/color row; introduce no Shape choice or family filtering.
  - Done when the real panel works by pointer/keyboard, decimals and expanded slider bounds retain caller values, and focused checks and independent review pass. Combined dock composition belongs to 2.53.
  - Register maintained scope and enforce whole-file 400 physical / 300 logical / 50-function caps. Keep existing DS compiler limitations explicit; no storage, renderer activation, flags or new dependencies.
  - _Boundary: Controlled Legend panel; controller owns combined story and metadata_
  - _Depends: 2.50_
  - _Requirements: 4.8, 4.9, 10.1, 10.4, 10.5, 10.6_

- [x] 2.52 (P) Restore independent chart padding controls
  - Follow chart-legend-padding-design.md. Implement the original Padding subsection, four sides in original order, exact controlled edits and linked numeric/range inputs without an invented toggle.
  - Done when side edits remain independent and decimal/invalid/current-value cases pass with independent review. Chart Style grouping in the combined dock belongs to 2.53; other Chart Style controls remain pending.
  - Register maintained scope and enforce whole-file 400 physical / 300 logical / 50-function caps. Run focused unit/browser, scoped type/lint and independent review. No geometry, storage, flags or dependency changes.
  - _Boundary: Controlled Padding subsection; controller owns Chart Style preview grouping_
  - _Depends: 2.50_
  - _Requirements: 4.8, 4.9, 10.1, 10.4, 10.5, 10.6_

- [x] 2.53 Compose Legend and Padding in the accepted chart editor preview
  - Place real Padding under the original Chart Style group and real Legend after Titles, retaining Set Up, gallery and dock navigation. Keep incomplete sections identified in preview prose outside the controls.
  - Done when controlled edits survive close/reopen and tab changes, isolated light/dark browser checks pass with independent review, and reviewed artifacts, breadth and source pins are synchronized and pushed.
  - Development stories are excluded from production caps; verify registered production modules still satisfy 400/300/50. Do not change renderer activation, storage or shared control behavior.
  - _Boundary: Controller-owned combined development story and delivery metadata_
  - _Depends: 2.51, 2.52_
  - _Requirements: 4.8, 4.9, 10.1, 10.4, 10.5, 10.6_

- [x] 2.54 (P) Restore the chart Background controls
  - Follow chart-background-tooltip-design.md. Implement the original Background toggle and Color control with exact edits, alpha support, invalid draft handling and disabled value retention.
  - Done when real pointer/keyboard interactions and no-mount-edit cases pass focused checks and independent review, preserving the accepted styling. No new opacity control or renderer/storage changes.
  - Register maintained files and enforce whole-file 400 physical / 300 logical / 50-function caps; reuse existing tools and keep known compiler limitations explicit.
  - _Boundary: Controlled Background subsection; composition belongs to 2.56_
  - _Depends: 2.53_
  - _Requirements: 4.8, 4.9, 10.1, 10.4, 10.5, 10.6_

- [x] 2.55 (P) Restore the original Tooltips toggle and mode selection
  - Follow chart-background-tooltip-design.md. Preserve exact Single/Multiple/Compact values, caller choice order, unknown modes and retained hidden settings without introducing extra tooltip options.
  - Done when the real subsection works by pointer/keyboard, controlled edits remain exact, disabled values survive and focused checks plus independent review pass.
  - Register maintained files and enforce whole-file 400/300/50 caps; no renderer/storage/feature-flag or dependency changes.
  - _Boundary: Controlled Tooltips subsection; Series grouping belongs to 2.56_
  - _Depends: 2.53_
  - _Requirements: 4.8, 4.9, 10.1, 10.4, 10.5, 10.6_

- [x] 2.56 Compose Background and Tooltips in the accepted dock preview
  - Place Background after Padding under Chart Style and Tooltips under Series, preserving accepted sections and original layout. Keep incomplete Series/axis and live-binding scope clear outside the controls.
  - Done when retained color/mode edits survive dock close/reopen and tab changes in both themes, scoped browser checks and independent review pass, and reviewed artifacts, inventory, breadth and source pins are committed and pushed.
  - Development story is excluded from production caps; register and audit the maintained panel modules at 400/300/50. No application activation or storage behavior changes.
  - _Boundary: Controller-owned combined development story and delivery metadata_
  - _Depends: 2.54, 2.55_
  - _Requirements: 4.8, 4.9, 10.1, 10.4, 10.5, 10.6_

- [x] 2.57 Restore the original Series numeric styling controls
  - Follow chart-series-shadow-design.md. Preserve caller labels/order, exact scalar edits and native numeric bounds/steps with correctable invalid drafts and no mount edits.
  - Done when focused tests and both-theme pointer/keyboard checks pass independent review, including external updates and family-specific caller descriptors.
  - Register maintained files and enforce whole-file 400 physical / 300 logical / 50-function caps; no renderer, storage, dependency or flag changes.
  - _Boundary: Controlled Series style panel and reusable chart numeric input_
  - _Depends: 2.56_
  - _Requirements: 4.8, 4.9, 10.1, 10.4, 10.5, 10.6_

- [x] 2.58 Restore the Series Shadow subsection
  - Preserve original toggle, Color, Blur and offsets using accepted numeric/color inputs; keep hidden values, alpha and negative offsets without new fields.
  - Done when focused tests and both-theme pointer/keyboard checks pass independent review. Preparation may overlap 2.57, but production waits for its acceptance.
  - Register maintained files and enforce whole-file 400/300/50 caps; caller retains family eligibility and storage ownership.
  - _Boundary: Controlled Shadow subsection_
  - _Depends: 2.57_
  - _Requirements: 4.8, 4.9, 10.1, 10.4, 10.5, 10.6_

- [x] 2.59 Compose Series styling and Shadow in the accepted dock preview
  - Compose numeric rows after Tooltips and Shadow afterward; restore original numeric font, thin tracks and spinner-free fields. Disclose missing Labels/family-specific controls and axes outside product controls.
  - Done when edited values survive dock and tab transitions in both themes, independent review passes, and reviewed artifacts, inventory, breadth and source pins are synced, committed and pushed.
  - Development story is excluded from production caps; audit maintained production modules at 400/300/50. No application activation or storage changes.
  - _Boundary: Controller-owned combined development story and delivery metadata_
  - _Depends: 2.57, 2.58_
  - _Requirements: 4.8, 4.9, 10.1, 10.4, 10.5, 10.6_

- [x] 2.60 (P) Restore ordinary Series Labels typography controls
  - Follow chart-labels-markers-design.md: preserve Labels toggle, Font, Weight and horizontal Size/Color row with exact controlled edits, alpha and retained unknown choices.
  - Done when focused tests and independent review pass, preserving hidden values and keyboard/color-picker behavior without adding ordinary placement or text fields.
  - Register maintained files and enforce 400 physical / 300 logical / 50-function caps. Reuse accepted controls; no dependencies, flags, rendering or storage changes.
  - _Boundary: Controlled ordinary Labels subsection_
  - _Depends: 2.59_
  - _Requirements: 4.8, 4.9, 10.1, 10.4, 10.5, 10.6_

- [x] 2.61 (P) Restore the original Series Markers group
  - Preserve enabled, Shape, Size and Stroke Width with caller choice order, unknown shape, fractional values, correctable invalid drafts and disabled retention.
  - Done when focused tests and independent review pass, retaining original numeric limits and presentation. No invented Color field or scatter/bubble toggle.
  - Register maintained files and enforce 400/300/50 caps; caller owns eligibility and option mapping.
  - _Boundary: Controlled Markers subsection_
  - _Depends: 2.59_
  - _Requirements: 4.8, 4.9, 10.1, 10.4, 10.5, 10.6_

- [x] 2.62 Compose Labels and Markers in the original bar/line editor flows
  - Join the real panels in the accepted dock with original bar/line order and conditions. Keep remaining family-specific controls and live-binding limits explicit outside the UI controls.
  - Done when one joined light/dark browser check and independent review pass for exact edits and dock/tab retention, then compact evidence, inventory, breadth and source pins are synced, committed and pushed.
  - Development story is excluded from production caps; enforce 400/300/50 on maintained components. No application activation or persistence changes.
  - _Boundary: Controller-owned combined preview and delivery metadata_
  - _Depends: 2.60, 2.61_
  - _Requirements: 4.8, 4.9, 10.1, 10.4, 10.5, 10.6_

- [x] 2.63 (P) Restore axis Grid Lines controls
  - Follow chart-axis-details-design.md: preserve Grid Lines toggle, Color, Thickness and Line Dash, controlled exact edits, alpha, decimal correction and disabled retention.
  - Done when focused tests and independent review pass using existing controls, with no mapper, flags or storage changes. Register production scope and enforce 400 physical / 300 logical / 50-function caps.
  - _Boundary: Controlled Grid Lines subsection_
  - _Depends: 2.62_
  - _Requirements: 4.8, 4.9, 10.1, 10.4, 10.5, 10.6_

- [x] 2.64 (P) Restore axis Ticks controls
  - Preserve Ticks toggle, Color, Width and caller-conditional Length, exact edits, expanded maxima and retained hidden values. No invented Axis Line switch.
  - Done when focused tests and independent review pass for toggles, alpha, decimals and Length hiding without mutation. Register production scope and enforce 400/300/50 caps.
  - _Boundary: Controlled Ticks subsection_
  - _Depends: 2.62_
  - _Requirements: 4.8, 4.9, 10.1, 10.4, 10.5, 10.6_

- [x] 2.65 Compose axis details in the original editor dock
  - Join Grid Lines then Ticks under Horizontal/Vertical Axis with independent retained state. Keep pending base fields, Labels and live integration explicit outside controls.
  - Done when one focused light/dark browser/CDP check and independent review pass, compact evidence is synced, inventory/breadth/source pins updated and per-task commits pushed.
  - Story is excluded from production caps; enforce 400/300/50 on maintained controls and confirm reused shared modules remain unchanged.
  - _Boundary: Controller-owned preview composition and delivery metadata_
  - _Depends: 2.63, 2.64_
  - _Requirements: 4.8, 4.9, 10.1, 10.4, 10.5, 10.6_

- [x] 2.66 (P) Restore the main Cartesian axis fields
  - Follow chart-axis-fields-design.md: original conditional Axis Type, Time Format, Position, Color and Thickness with exact controlled edits and retained hidden values.
  - Done when focused tests and independent review pass for caller choice order, unknown values, alpha, zero/fractional thickness and invalid correction. No mapper, dependencies, flags or storage changes.
  - Register scope and enforce 400 physical / 300 logical / 50-function caps.
  - _Boundary: Controlled axis main fields_
  - _Depends: 2.65_
  - _Requirements: 4.8, 4.9, 10.1, 10.4, 10.5, 10.6_

- [x] 2.67 (P) Restore axis Labels and rotation controls
  - Preserve typography, horizontal Size/Color, Padding, Auto Rotate and conditional dial/numeric rotation. No Labels enable toggle. Retain manual rotation across auto transitions.
  - Done when focused tests and independent review pass for normalized signed angles, pointer cleanup, keyboard edits, conditional retention and correctable drafts.
  - Register maintained components/styles and enforce 400/300/50 caps; caller owns effective original option mapping.
  - _Boundary: Controlled axis Labels and its rotation input_
  - _Depends: 2.65_
  - _Requirements: 4.8, 4.9, 10.1, 10.4, 10.5, 10.6_

- [x] 2.68 Compose the remaining ordinary Cartesian axis controls
  - Join main fields before Grid Lines/Ticks and Labels after them, preserving independent axes and original conditional time-format behavior in bar/line fixtures.
  - Done when one focused light/dark browser/CDP check and independent review pass for exact fields, auto/manual rotation, pointer/keyboard and dock/tab retention. Publish compact evidence, update inventory/breadth/pins and push per-task commits.
  - Story excluded from production caps; maintained code passes400/300/50. Keep family eligibility, full font menus, live chart binding and persistence explicitly pending.
  - _Boundary: Controller-owned joined editor preview and delivery metadata_
  - _Depends: 2.66, 2.67_
  - _Requirements: 4.8, 4.9, 10.1, 10.4, 10.5, 10.6_

## Live editor integration through the existing application

Reviewed task graph for owner-authorized autonomous integration, 2026-10-18. See [live integration design](chart-live-editor-integration-design.md). This plan ends at a functioning ordinary Workspace journey with save/reopen, not at helper acceptance.

Every production task below passes whole-file 400 physical/300 logical/50 per-function caps, inventory coverage, affected strict type checks/lint and focused behavior tests. Reuse the accepted complexity foundation and explicit fork change manifest. Controller freezes exact existing executable commands before dispatch; no package installation or copied preview runner is part of this plan. Each task requires independent review and fresh relevant verification before acceptance. Workers are not alone and must preserve other lanes' changes.

### Wave 0: freeze contracts and checks

- [x] 2.69 Controller: record exact root/fork revisions and dirty-path ownership, actual panel prop/event inventory and caller paths. Freeze `application/appearanceModel.ts`, `compatibility/editorBindings/types.ts`, required mapper type extensions and session editor-command contracts. Include every applicable accepted control field and exact saved namespace. Define production theme/semantic-column input sources and latest-storage Widget updater call. Map required renderer effects to the field manifest. Update root complexity inventory and planned breadth paths. Ownership: shared contracts, root manifests and canonical design/task metadata only. Completion: Astra independently reviews persistence, financial semantics and lane boundaries; frozen types compile; commands use installed pinned tools. Non-code planning is cap-exempt; type files are capped.
  - _Boundary:_ Shared contracts and canonical metadata
  - _Depends:_ 2.68
  - _Requirements:_ 4.2, 4.7, 4.8, 4.9, 10.1, 10.3, 10.4, 10.5, 10.6

### Wave 1: independent render and editor lanes

- [x] 2.70 (P) Appearance implementer: own new `application/effectiveAppearance.ts` and cohesive appearance resolver helpers only. Consume accepted composition/colors and frozen contracts; resolve all applicable captions, layout, axes, legend, series, tooltip and palette fields for three families. Preserve original saved baseline; do not normalize it in place. Test stock/custom theme precedence, explicit false/zero, missing overrides, disabled retained values and stable IDs. Completion: full field manifest has an effective result; unresolved application inputs are concrete defects rather than silent fallbacks; caps pass.
  - _Boundary:_ Effective appearance resolver and pure helpers
  - _Depends:_ 2.69
  - _Requirements:_ 4.2, 4.7, 4.8, 4.9, 10.1, 10.3, 10.4, 10.5, 10.6
- [x] 2.71 (P) Editor implementer, parallel to 2.70: own new `compatibility/editorBindings/**`, `editor/ApplicationChartEditor.tsx` and cohesive production composition files. Bind existing panels to frozen selectors/events, including full font choices and original family/data eligibility. Emit exact validated bar/line/axis patches; preserve unrelated fields and retained disabled values. No session/store writes. Test each event leaf, ordinary panel value hydration, independent axes and original applicability. Completion: production composition imports the accepted controls without preview state; caps pass.
  - _Boundary:_ Editor bindings and production panel composition
  - _Depends:_ 2.69
  - _Requirements:_ 4.2, 4.7, 4.8, 4.9, 10.1, 10.3, 10.4, 10.5, 10.6

Release a worker slot for independent review after each task. Shared contract changes are controller-only and pause both consumers until reconciled.

### Wave 2: render projection and Set Up

Controller addition to 2.69/2.73: freeze an explicit application raw-observation semantic policy because ordinary WidgetColumnDef lacks unit/scale. 2.73 owns its application descriptor adapter and independent no-conversion/no-invented-unit tests; 2.72 consumes its frozen mapper contract. Preserve existing strict declared-unit mapper behavior for current callers. Freeze any shared mapper contract changes before parallel dispatch, with production writes remaining in 2.72.

- [x] 2.72 (P) Renderer implementer: after 2.70, own mapper `echarts/cartesian*` implementation/validation files and their tests, excluding controller-owned contracts. Extract caption/layout, axis, series and tooltip projections cohesively before exceeding caps. Project every applicable manifest field to public ECharts APIs; use existing financial display callbacks. Resolve concrete tooltip/marker/geometry gaps from source and finite evidence. Completion: numerical observations unchanged, nulls retained, all applicable fields have observable option/render effects; caps pass. No UI acceptance claimed yet.
  - _Boundary:_ ECharts projection and validation
  - _Depends:_ 2.70
  - _Requirements:_ 4.2, 4.7, 4.8, 4.9, 10.1, 10.3, 10.4, 10.5, 10.6
- [x] 2.73 (P) Setup implementer, parallel to 2.72: own new pure setup/transform modules under `application/` and focused tests. Reuse range/capture reducers and source semantics for category/series choice, order, aggregate and switch orientation. Freeze any newly required transform contract through controller before coding it. Preserve IDs, original model/range, units, missing values and sourceMode. Test duplicate categories, negative/null data, sum examples, reordered columns and transpose round trip using independent expected results. Completion: every reachable ordinary Set Up action has a real transformation and saved-state transition; caps pass.
  - _Boundary:_ Setup transforms and semantic descriptors
  - _Depends:_ 2.69
  - _Requirements:_ 4.2, 4.7, 4.8, 4.9, 10.1, 10.3, 10.4, 10.5, 10.6

### Wave 3: session and ordinary callers

- [x] 2.74 Session implementer: after 2.71/2.72/2.73, own `application/useApplicationChartSession.ts` and cohesive React/session transaction modules, plus a narrowly reviewed general edit application adapter if needed. Compose capture, selected baseline, appearance, editor and host using existing Widget latest-state updates. Retain original resolvedOptions and unknown/inactive partitions. Handle consecutive edits, delayed stale work, refresh, theme, address changes and disposal. The existing Widget owner changes only through the independently reviewed atomic transient adapter in the live-editor contracts; preserve its persistence/effect semantics and verify urgent/deferred replay and disposal. Completion: tests prove two immediate edits survive without duplicate replay persistence, stale callbacks cannot write, failure recovery retains edits, defaults are never persisted; caps pass.
  - _Boundary:_ Application chart session and edit transactions
  - _Depends:_ 2.71, 2.72, 2.73
  - _Requirements:_ 4.2, 4.7, 4.8, 4.9, 10.1, 10.3, 10.4, 10.5, 10.6
- [x] 2.75 Caller implementer: after 2.74, own exact existing `AgChartView`, `useChartOptions`, `useTableContext`, AgGridTable/File chart activation and community boundary paths frozen in 2.69. Restore createChartData, toggle, live host and actual dock; restore table state and original no-series/flag predicates. Pass valid saved chart models through boundary while retaining invalid/unknown saved data safely. Cohesively extract oversized callers before acceptance. Completion: actual Full Workspace table route reaches production session without test-only injection; existing Plotly routing preserved; scoped caller/component checks and caps pass.
  - _Boundary:_ Existing table chart callers and community boundary
  - _Depends:_ 2.74
  - _Requirements:_ 4.2, 4.7, 4.8, 4.9, 10.1, 10.3, 10.4, 10.5, 10.6
- [x] 2.76 Actions implementer: after 2.75, own narrowly named existing chart action adapters and corresponding session/host action interfaces, serialized with 2.74/2.75. Connect original quick actions, navigator/mini-chart extent, dock open/close and current-revision PNG export. Completion: each existing applicable action changes the expected chart/table effect; stale/disposed render cannot export; caps pass. Do not add a toolbar or capability flag.
  - _Boundary:_ Existing chart actions and export
  - _Depends:_ 2.75
  - _Requirements:_ 4.2, 4.7, 4.8, 4.9, 10.1, 10.3, 10.4, 10.5, 10.6

### Wave 4: one application acceptance join

- [x] 2.77 Controller and independent Astra reviewer: run the existing application browser infrastructure against the actual Full route with disposable backend state, headless owned browser and one worker. Extend maintained e2e tests by behavior, not task number. Cover groupedColumn/stackedColumn/line from the ordinary table, every applicable editor section, theme, filtered/sorted data, Set Up, table return, current export, backend save/reopen/restart and failure/retry. Inspect console/network diagnostics and actual displayed values. Use representative light/dark screenshots sufficient to assess the integrated widget. Failure fixes return to the owning task and receive focused review; rerun only affected checks and the necessary join.
  - _Boundary:_ Actual application acceptance and evidence
  - _Depends:_ 2.76
  - _Requirements:_ 4.2, 4.7, 4.8, 4.9, 10.1, 10.3, 10.4, 10.5, 10.6
  - Completion: original saved leaves and displayed settings survive a new application session/backend restart, except the explicitly disclosed original numeric-rotation/Auto Rotate and structural-axis restore limitations, which must be recorded separately and must not be claimed as round-trip parity; earlier edits and unknown branches remain; failure preserves unsaved work; no stub route or inert applicable control remains. Required production caps and final shared-module inventory audit pass. One concise review record identifies source identity, commands/results, reviewer decision, limitations and screenshots. Update UI-02 through UI-09 and breadth only to the extent proven. Preserve UI-10 through UI-16 as pending release obligations. Test/evidence-only edits are cap-exempt; any repair production files must pass caps.

The implementation continues through 2.77 under the user's live-integration authorization once this concrete contract/task graph passes independent review. Do not stop after L1 or request a new generic permission to perform the already authorized join. A concrete unresolved compatibility difference is escalated with its observed consequence, rather than accepted through a hidden feature reduction.


Design approved by the owner on 2026-10-16 ("go"). The owner approved these implementation tasks on 2026-10-16 ("approve"). Unchecked tasks remain unimplemented or unverified. Each executable leaf targets one 1-3 hour engineering work unit; investigate unexpected scope before splitting a task, rather than silently expanding it. External access, entitlement decisions and build waits are not promised completion times.

The separately approved chart-foundation design has [six foundation tasks](#approved-design-slice-chart-state-and-lifecycle-foundation), approved by the owner on 2026-10-16. Its explicit dependency branch overrides the historical numeric sequence only within that scope. [Independent task review](chart-foundation-task-review.md) passed.

## Execution contract

Renderer amendment, 2026-10-16: the owner selected "Use Perspective baseline". Tasks 2.6-2.12 add the selected viewer and remove commercial dependencies without renumbering prior tasks. Independent controller task-graph sanity review passed after splitting Community isolation from commercial removal; independent amendment review still precedes renderer feature work. No new renderer task is implemented or accepted by this plan.

Superseding owner constraint, 2026-10-16: preserve existing UX, design, themes, functional capabilities and feature-flag behavior. Follow [Workspace experience](../../steering/workspace-experience.md). Instructions below to hide or disable existing actions, or accept unavailable legacy features, are superseded. Completed task checkboxes record historical acceptance only. Renderer and release acceptance now require a capability inventory against the original owned OpenBB source, explicit identification of gaps introduced by tasks 2.6-2.7, and equivalent working replacements with verification evidence. The modified Community baseline cannot redefine the required capabilities. Reconcile affected requirements, design, tasks and breadth coverage before further renderer implementation.

- Follow the approved [design](design.md), [complexity](../../steering/complexity.md), [testing](../../steering/testing.md), [CI](../../steering/ci.md), [documentation](../../steering/documentation.md) and [delegation](../../steering/delegation.md) policies.
- Every leaf follows implementation -> independent review -> fresh verification -> acceptance. Controller owns shared contract updates, integration joins, commits and the single heavy-check queue. At most two workers plus one reviewer run alongside the controller; up to three independent lightweight checks may overlap. No parallel installation or shared-state mutation.
- Use GPT-6.1 Sol for bounded implementation/routine review, GPT-6 Astra for difficult integration/financial review, and GPT-6 Luna for mechanical inventories. Supply fresh-context workers with the leaf, allowed paths from the design, implemented verification command and complexity scope.
- Numeric order is the default sequence. The explicitly declared lanes below may progress in parallel using their listed dependencies and within-lane order; this is the project's requested fan-out override. A (P) marker identifies a lane entry, not permission to run dependent leaves concurrently. Other groups remain sequential.
- Foundation code is bootstrapped with measured caps and receives executable retrospective verification in 1.4. No feature acceptance precedes that gate. Whole modified upstream files must fit caps or have a measured reviewed exception; generated output is excluded, generator logic is not.
- The current Anthropic-before-Excel gate is the owner's earlier sequencing preference, not a technical dependency: Anthropic powers Workspace chat; Excel uses the application backend and data API directly. No Excel implementation, source changes, generator execution, function snapshots or image builds before 5.5 passes with current identities. Planning and generic eligibility validation are allowed earlier.
- Dagger builds/exports images only. Portable repository commands own generation, checks, image push and promotion. Deployment uses real Compose; Gitea infrastructure/migration is deferred.
- The user's explicit operator documentation and deployment requirements override the generic task rule excluding documentation/deployment. These appear as scoped verification/integration work with exercised procedures, not detached writing tasks.
- Actual Office acceptance, owner-run private-server evidence and required component entitlements are external inputs. The owner deploys locally with Compose; agent SSH access is not required. Missing evidence keeps the affected task unverified; do not fabricate acceptance or silently remove the gate.

## Exclusive lanes and joins

| Wave | Eligible work | Exclusive writable scope | Join and shared ownership |
| --- | --- | --- | --- |
| Foundation | Accepted 1.1-1.8 remain prerequisites | Existing checker, inventory and verification foundations | Reuse accepted checks; no new foundation implementation is implied |
| A: Workspace | Source-safe 2.34-2.37 and ordinary capture 2.38-2.40 are independently accepted; remaining appearance/editor/application joins retain their named gates | Controller owns shared test setup/inventory; one Sol worker owns actual-grid fixture, capture adapter and its tests per bounded leaf | No parallel writers within A2; disjoint appearance/editor research may continue, with separate runtime implementation gates |
| A: Data | 3.1-3.7 keep their recorded status and within-lane prerequisites | Owned provider/data API paths and tests | No independent writes to shared locks, catalog bindings or source snapshots |
| A: blocked renderer/catalog join | Remaining grid/category paths, B2, mapper, C/D and real-app joins require their named frozen contracts and separately reviewed/approved task graphs | Ownership in the application integration design; no dispatch from this table | Historical 2.8-2.11/2.9 bindings are not executable replacement plans; neither 2.37 nor 2.40 unblocks this row |
| A: image and dashboard joins | 3.8 waits for the reviewed current renderer/catalog source join; 2.12 then waits for 3.8 and complete renderer source acceptance; 4.1-4.5 wait for 2.12/3.8 and their explicit prerequisites | Controller serializes catalog/source/image records and real-app verification | No renderer-complete, dashboard-baseline or release acceptance while original capability gaps remain; an identified unreleased milestone is separate |
| B: Agent | 5.1-5.5 retain their explicit prerequisites and within-lane order | Agent service and agent-specific tests; controller owns builder/origin integration | No Excel implementation before current-identity 5.5 acceptance |
| B: Delivery | 7.1-7.6 in order after 4.5 | Portable delivery commands/wrappers/tests and backup/restore | Shared schemas/build joins remain controller-owned |
| C: Excel | 6.1-6.6 in order after 5.5 | Owned add-in/generator and Excel-specific tests/assets | May overlap eligible delivery; controller owns builder/Compose join |
| Final join | 8.1-8.6 after Excel and Delivery prerequisites | Controller-owned candidate and acceptance records | Complete source/image identities, Office/server/recovery evidence and full capability set remain required |

Chart/application production paths above are relative to `vendor/workspace/terminalpro/src/components/General/Table/`; other lanes retain their concrete ownership paths from the approved design. At most controller plus two bounded Sol implementers and one independent reviewer; difficult state/financial joins receive Astra review. One heavy check at a time. Freeze interfaces before dispatch, stop affected lanes on drift, preserve unrelated dirty inventory/catalog/renderer work, and selectively stage only independently accepted changes. No existing menu, action or feature flag may be removed, hidden, disabled, made inert or given a reduced default.

Scopes refer to the concrete paths in the design's File Structure Plan. Shared source/tool locks, schemas, breadth entries, central image builder and release manifests stay controller-owned. Workers return proposed updates; the controller merges them at joins. Test fixtures belong to their provider/agent/Excel lane; shared verification infrastructure is frozen before fan-out.

## Tasks

- [x] 1. Establish source, quality and execution foundations

- [x] 1.1 Acquire owned sources and record the candidate baseline
  - Acquire exact owned-fork revisions, select the latest API release candidate and record upstream provenance, required package inventory and component license/asset constraints.
  - Distinguish release candidates from validated releases. Record missing/commercial chart assets and remove any assumption that an upstream embedded key establishes entitlement.
  - Done when source hashes and notices are reproducible, adaptation scope is recorded, and essential unresolved asset rights are explicit release blockers.
  - Complexity: acquisition records, notices and inventory-only changes are excluded documentation/data; any maintained executable change returns to a capped production task.
  - _Boundary: Release control_
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 11.1_

- [x] 1.2 Establish locked development and verification toolchains
  - Pin stable Python, Node, Bun, Dagger engine/SDK, Docker/Compose, test parsers and base image inputs; create the portable command and test-project scaffolds without application behavior.
  - Apply the owner's implementation steering: prefer pinned pnpm with Safe Chain for maintained JavaScript rewrites and uv/uvx with Safe Chain for Python. Verify protected noninteractive installs; document compatibility exceptions for preserved upstream locks.
  - Verify tools in WSL and define the clean Linux runner prerequisites. Keep runner-specific setup outside core build and verification logic.
  - Done when lock-based setup succeeds and minimal tool smoke checks report exact versions; foundation scope remains provisionally measured until the executable quality gate is complete.
  - Complexity: measure this bootstrap scope against 400 physical/300 logical/50 per-function caps; executable cross-language enforcement in 1.4 must pass before any feature work is accepted.
  - _Boundary: Release control_
  - _Depends: 1.1_
  - _Requirements: 3.1, 9.1, 9.7, 10.4_

- [x] 1.3 Implement physical and Python complexity measurements
  - Create the maintained-scope inventory and physical/Python counters using the documented syntax-unit convention; handle nested callables, docstrings, comments and newline variants.
  - Test exact cap boundaries and reject missing changed-file/base/head inputs; record fork and generated/vendor exclusions.
  - Done when deliberately oversized examples fail and the checker measures its own maintained Python scope reproducibly.
  - Complexity: measure this bootstrap scope against 400 physical/300 logical/50 per-function caps; executable cross-language enforcement in 1.4 must pass before any feature work is accepted.
  - _Boundary: Complexity and breadth_
  - _Depends: 1.2_
  - _Requirements: 10.5, 10.6_

- [x] 1.4 Complete TypeScript measurements and the cross-repository quality gate
  - After 1.2 passes, standalone parser implementation may overlap 1.3 using the controller-reviewed interface: JSON file-path array on stdin (absolute or relative to cwd), JSON measurement array on stdout preserving input paths, with each record containing path, logical and functions (name, line, column, logical; positions are 1-based). Empty input arrays return empty arrays. Parser failures use stderr and exit 2. Early writes are limited to tools/quality/syntax_units.ts and tests/quality/test_syntax_units.mjs; Python integration, inventory and breadth updates wait for 1.3 acceptance.
  - Implement the pinned TypeScript/JavaScript parser counter, expression-bodied callable handling and combined scope reports.
  - Verify whole modified upstream files and documented exceptions; do not infer changed scope from absent container Git metadata.
  - Done when both language counters pass convention fixtures, fail missing scopes, and retroactively certify foundation code from 1.2 and 1.3. Publish the actual verified command for subsequent worker briefs.
  - Complexity: the task's entire modified maintained production scope passes 400 physical lines/file, 300 logical units/file and 50/function using the implemented checker; record generated exclusions and reviewed exceptions.
  - _Boundary: Complexity and breadth_
  - _Depends: 1.3_
  - _Requirements: 10.5, 10.6, 9.7_

- [x] 1.5 Implement typed evidence and release identity validation
  - Define source, candidate/release, backup and acceptance record validation and a portable check entry point with stable exit codes.
  - Distinguish passed, failed, skipped and unverified; reject stale revision/image/schema identities and record fixture versus live/manual evidence.
  - Done when malformed and mismatched evidence fails and a missing Anthropic acceptance record cannot make Excel eligible; link implemented checks into the breadth map.
  - Complexity: the task's entire modified maintained production scope passes 400 physical lines/file, 300 logical units/file and 50/function using the implemented checker; record generated exclusions and reviewed exceptions.
  - _Boundary: Portable CI commands_
  - _Depends: 1.4_
  - _Requirements: 1.1, 8.1, 9.2, 9.3, 10.5, 10.6, 12.4_

- [x] 1.6 Freeze runtime, source and initial financial contract inputs
  - Build-preflight correction accepted: narrow source-namespace rules retain 32 Workspace and seven data API production paths while excluding adjacent private files. Task 1.8 must also preserve these paths through Docker context handling.
  - Freeze service names, ports, public path rules, bind-only state, credential injection names, source ownership and proposed profile/income/GDP route inventory from the approved design.
  - Retain empty public credential values and exclude local configuration, private state and evidence from build contexts. Preserve the existing private environment file.
  - Done when config validation and source-filter tests pass, worker boundaries are frozen, and initial routes remain labeled provisional until installed-schema validation in 3.7.
  - Complexity: the task's entire modified maintained production scope passes 400 physical lines/file, 300 logical units/file and 50/function using the implemented checker; record generated exclusions and reviewed exceptions.
  - _Boundary: Release control_
  - _Depends: 1.5_
  - _Requirements: 2.1, 3.4, 3.6, 3.7, 3.8, 5.3, 5.9, 11.1, 11.6, 11.7_

- [x] 1.7 Establish isolated API and browser verification infrastructure
  - Create fixture-only provider responses, pytest markers, bounded xdist execution and a pinned headless Playwright environment with disposable accounts and output roots.
  - Provide owned-browser CDP diagnostics, sensitive-header redaction, credential-entry trace suppression and hidden Windows helpers where needed.
  - Done when isolation/failure smoke checks run without user-browser attachment, show worker bounds, and preserve sanitized reproducible results; missing live credentials remain unverified.
  - Complexity: the task's entire modified maintained production scope passes 400 physical lines/file, 300 logical units/file and 50/function using the implemented checker; record generated exclusions and reviewed exceptions.
  - _Boundary: Verification_
  - _Depends: 1.6_
  - _Requirements: 10.1, 10.2, 10.3, 10.4, 10.6_

- [x] 1.8 Implement Dagger source filtering and image export foundations
  - Implement locked owned-source acquisition, explicit context filtering, build selection and exported image provenance without adding test, generation, publication or deployment logic to Dagger.
  - Add portable image archive loading separately from Dagger and verify a small build/export/load round trip on WSL and the clean Linux runner.
  - Done when source/layer checks exclude a disposable secret sentinel, exact image identity survives export/load, and no publish credential reaches Dagger.
  - Complexity: the task's entire modified maintained production scope passes 400 physical lines/file, 300 logical units/file and 50/function using the implemented checker; record generated exclusions and reviewed exceptions.
  - _Boundary: Dagger image builder_
  - _Depends: 1.7_
  - _Requirements: 1.1, 1.5, 3.2, 9.1, 9.6, 9.7, 11.7_

- [ ] 2. Adapt the Full Workspace baseline

- [x] 2.1 (P) Make the Full frontend build reproducible
  - Use the owned monorepo and pinned Bun frozen-lock install instead of the missing frontend npm lock and unavailable split-repository assembly.
  - Preserve the Full selection and record any narrowly required lock adaptation; keep TradingView disabled unless separately supplied and entitled.
  - Commercial packages still present are unresolved packaging inputs, not accepted dashboard capabilities. No publication before removal and new image evidence in 2.6-2.12.
  - Done when the frontend builds cleanly from recorded inputs without lock rewriting or hidden hosted source fetches.
  - Complexity: the task's entire modified maintained production scope passes 400 physical lines/file, 300 logical units/file and 50/function using the implemented checker; record generated exclusions and reviewed exceptions.
  - _Boundary: Workspace packaging_
  - _Depends: 1.8_
  - _Requirements: 1.1, 1.4, 1.5, 3.2_

- [x] 2.2 Stabilize application startup and private bootstrap state
  - Pin backend build dependencies, retain upstream migration/admin initialization and suppress password printing during bootstrap.
  - Include valid runtime health dependencies and protect persisted credential configuration; extract cohesive helpers before changing oversized maintained scripts if necessary.
  - Done when first startup and repeated startup use the same saved account/state and sanitized logs contain no bootstrap password.
  - Complexity: the task's entire modified maintained production scope passes 400 physical lines/file, 300 logical units/file and 50/function using the implemented checker; record generated exclusions and reviewed exceptions.
  - _Boundary: Workspace packaging_
  - _Depends: 2.1_
  - _Requirements: 1.4, 2.2, 2.3, 4.1, 9.6_

- [x] 2.3 Correct application authentication request boundaries
  - Replace substring backend detection with normalized origin and complete-path matching while retaining existing application session handling.
  - Regress application routes, data routes containing the API segment, lookalike prefixes, other origins and connector-supplied headers.
  - Done when application credentials attach only to the intended backend and external connector/agent requests keep their own headers.
  - Complexity: the task's entire modified maintained production scope passes 400 physical lines/file, 300 logical units/file and 50/function using the implemented checker; record generated exclusions and reviewed exceptions.
  - _Boundary: Workspace request boundary_
  - _Depends: 2.2_
  - _Requirements: 4.3, 5.3, 5.9, 6.5_

- [x] 2.4 Implement single-origin routing and runtime frontend settings
  - Render absolute public connector bases, configured public scheme and application URLs; add data/agent routing with correct prefix handling and stream behavior.
  - Keep optional Excel upstream absent until enabled and unavailable agent DNS/processes from blocking dashboard startup; disable hosted Copilot/enhancement calls.
  - Done when route contract tests distinguish APIs from SPA fallback, public scheme is correct, and disabled optional upstreams do not prevent origin startup.
  - Complexity: the task's entire modified maintained production scope passes 400 physical lines/file, 300 logical units/file and 50/function using the implemented checker; record generated exclusions and reviewed exceptions.
  - _Boundary: Workspace packaging_
  - _Depends: 2.3_
  - _Requirements: 2.3, 2.4, 3.4, 3.5, 3.7, 3.8, 4.4, 12.5_

- [x] 2.5 Build and identify the adapted Full image
  - Add the adapted Full build to the existing Dagger image builder and export its exact source-labeled image.
  - Run packaging health and fresh account smoke checks independently through portable verification; record unavailable upstream capabilities.
  - Done when the clean image loads and starts with expected Full configuration and its source/dependency identities are available for the integration join.
  - This is a provisional local packaging checkpoint, not a publishable image while commercial dependencies remain. Task 2.12 rebuilds the renderer-complete image used by 4.1.
  - Complexity: the task's entire modified maintained production scope passes 400 physical lines/file, 300 logical units/file and 50/function using the implemented checker; record generated exclusions and reviewed exceptions.
  - _Boundary: Dagger image builder and Workspace packaging integration_
  - _Depends: 2.4_
  - _Requirements: 1.1, 1.4, 1.5, 3.2, 9.1_

- [x] 2.6 Isolate Community tables and unsupported legacy states
  - Inventory residual grid callers and use Community-supported flat-table options/actions, retaining ordinary sorting, filters and financial formatting.
  - Hide unsupported range charts, legacy grouping/pivots, SSRM/tree/master-detail and Enterprise clipboard/XLSX actions. Preserve imported unsupported state behind an explicit unavailable view; Perspective supplies its own grouping/pivot experience later.
  - Identify oversized modified files before edits and extract cohesive responsibilities or obtain narrowly reviewed measured exceptions; do not hide a broad frontend rewrite in this task.
  - Done when focused tests exercise residual tables and unsupported imports without Enterprise API calls, and the accepted 1.4 checker passes every modified maintained file.
  - Complexity: whole modified maintained files pass 400 physical lines/file, 300 logical units/file and 50/function; record exclusions and reviewed exceptions.
  - _Boundary: Community rendering boundary_
  - _Depends: 1.4, 2.5_
  - _Requirements: 1.3, 1.4, 4.4, 4.6, 5.4, 10.5, 10.6_

- [x] 2.7 Remove commercial renderer and dependency paths
  - Remove AG Enterprise/Highcharts imports, keys, registrations, wrappers, theme-preview paths and package/lock entries, including lazy and type-only paths. Retain inventoried supported standalone Community charts and complementary Plotly widgets.
  - Controller serializes frozen-lock/notices changes. Do not suppress license warnings or rely on tree-shaking as removal evidence.
  - Done when source/dependency/module-graph checks and a clean frontend build contain no removed commercial modules or initialization keys, with unsupported renderer tests passing; image absence is rechecked in 2.12.
  - Complexity: whole modified maintained files pass 400 physical lines/file, 300 logical units/file and 50/function; record exclusions and reviewed exceptions.
  - _Boundary: Community rendering boundary_
  - _Depends: 2.6_
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 3.2, 4.4, 9.6, 10.6_

- [x] 2.8 Establish the owned Perspective browser runtime
  - Select an exact compatible current-namespace release/plugins eligible under Safe Chain's package-age policy; verify React/Vite and protected frozen installation through the controller-owned dependency join.
  - Package same-origin WASM/worker assets and an owned React host with bounded worker allocation, explicit viewer/table cleanup, resize and light/dark handling. Add no server, database, Perspective AI or dashboard shell.
  - Done when isolated fixture browser checks mount, resize, hide/show, change theme and repeatedly unmount/remount without leaked owned resources or console/network failures.
  - Complexity: whole modified maintained files pass 400 physical lines/file, 300 logical units/file and 50/function; record exclusions and reviewed exceptions.
  - _Boundary: Perspective runtime_
  - _Depends: 2.7_
  - _Requirements: 1.1, 1.2, 3.2, 4.6, 5.5, 10.1, 10.3_

- [ ] 2.9 Integrate ready financial explorers with the accepted catalog
  - Preserve OpenBB's existing widget framing, controls and styling; keep renderer differences local and verify light/dark visual consistency under [the owner constraint](../../steering/workspace-experience.md). No dashboard redesign or unrelated frontend rewrite.
  - Map profile/income and FRED rows to explicit types, null/date semantics and provenance. Apply field-specific aggregation rules without default sums of ratios, EPS or incompatible currencies/units/frequencies.
  - Bind ready widget IDs, installed operations, parameters, schema versions and useful viewer defaults through the controller-owned renderer/catalog join; keep provider code renderer-independent and add no OHLC endpoint.
  - Done when fixtures prove observations and permitted aggregates, unsupported combinations fail visibly, and generated app/widget references resolve to Perspective without manual widget authoring.
  - Complexity: whole modified maintained files pass 400 physical lines/file, 300 logical units/file and 50/function; generated snapshots are excluded, adapters/generators are not.
  - _Boundary: Perspective data and widget with consumer-contract integration_
  - _Depends: 2.8, 3.7_
  - _Requirements: 4.3, 4.5, 4.6, 5.4, 5.6, 5.7, 11.3_

- [ ] 2.10 Preserve explorer configuration through refresh and reopen
  - Persist validated versioned viewer configuration, source parameters and schema identity in existing widget storage; restore columns, groups/splits, filters, aggregations, plugin settings and theme policy without treating cached rows as authoritative data.
  - Replace complete fetched data while retaining compatible settings; reject stale responses, mark last-success data on refresh failure and recover from incompatible schemas without overwriting saved configuration.
  - Done when fixture tests change parameters/configuration, remount and refresh changed observations, including out-of-order, failure/retry and incompatible-schema cases. Full application restart acceptance remains in 4.5.
  - Complexity: whole modified maintained files pass 400 physical lines/file, 300 logical units/file and 50/function; record exclusions and reviewed exceptions.
  - _Boundary: Perspective state and context_
  - _Depends: 2.9_
  - _Requirements: 2.2, 4.2, 4.7, 5.2, 5.4, 5.7, 5.8_

- [ ] 2.11 Expose configured explorer data through Workspace context
  - Capture the configured view and explicit selection scope with parameters, schema, filters, groups/splits, aggregations, units/periods and data revision; distinguish derived totals from observations.
  - Register the payload at the existing selected-widget seam. Bound exports and handle refresh/reconfiguration/removal races without truncation or full-table substitution; model credentials and inference remain in the later agent service.
  - Done when fixtures match configured/selected exports to displayed financial data and reject stale, unavailable and oversized context. Check configured-view CSV and supported chart-image output; live Anthropic grounding remains in 5.5.
  - Complexity: whole modified maintained files pass 400 physical lines/file, 300 logical units/file and 50/function; record exclusions and reviewed exceptions.
  - _Boundary: Perspective state and context with Workspace integration_
  - _Depends: 2.10_
  - _Requirements: 5.4, 10.3, 12.1, 12.3, 12.5_

- [ ] 2.12 Build and identify the renderer-complete Full image
  - BLOCKED: historical 2.11 completion cannot authorize this build. Require the separately reviewed/approved current renderer/catalog source-join graph, its complete source acceptance and 3.8 identity verification first. Source-safe 2.34-2.37 or bounded A2 2.40 acceptance does not satisfy renderer-complete eligibility. Any smaller identified unreleased image milestone needs its own reviewed bounded task and cannot complete 2.12.
  - Rebuild through the existing Dagger definition in the single heavy-build queue. Controller joins final Workspace locks, renderer bindings and verified data/catalog hashes into the candidate identity.
  - Run isolated fixture renderer smoke checks and inspect production chunks, installed dependencies and image contents for removed commercial packages/keys; retain notices and preserve every original capability; unresolved renderer parity blocks this renderer-complete gate.
  - Done when independent review accepts fixture evidence and the new image identity, and actual test paths/artifacts reach breadth. This permits the real dashboard join, not complete release promotion or a substitute for 4.3-4.5 acceptance.
  - Complexity: modified maintained builder/helpers pass 400 physical lines/file, 300 logical units/file and 50/function; tests/evidence and generated outputs are recorded exclusions.
  - _Boundary: Dagger image builder and renderer integration_
  - _Depends: 3.8_
  - _Requirements: 1.1, 1.2, 1.4, 3.2, 4.4, 9.1, 9.6, 10.5, 10.6_

- [ ] 3. Adapt the data API and generate supported widgets

- [x] 3.1 (P) Restore a provenance-preserving FMP extension skeleton
  - Acquire the recorded FMP source and license, restore its provider package in the owned data fork, and restrict initial supported registration to profile and income datasets.
  - Adapt package constraints to the selected core candidate without advertising runtime compatibility; establish the locked provider-test environment with the selected shared equity/economy router packages so subsequent route-level tests have their prerequisites. Isolate unchanged imports from maintained changes.
  - Done when installed provider discovery succeeds against the candidate core and provenance/notice records identify the exact imported artifact.
  - Complexity: the task's entire modified maintained production scope passes 400 physical lines/file, 300 logical units/file and 50/function using the implemented checker; record generated exclusions and reviewed exceptions.
  - _Boundary: Maintained FMP_
  - _Depends: 1.8_
  - _Requirements: 1.2, 1.4, 11.1, 11.2_

- [x] 3.2 Adapt and verify the FMP profile fetcher
  - Implement the selected API's profile model/fetcher interface using the stable provider endpoint and server-side credential settings.
  - Use deterministic fixtures to check identity, financial values, available currency metadata and missing-value behavior.
  - Done when the installed shared equity profile route returns the expected typed fixture response with equivalent requested parameters.
  - Complexity: the task's entire modified maintained production scope passes 400 physical lines/file, 300 logical units/file and 50/function using the implemented checker; record generated exclusions and reviewed exceptions.
  - _Boundary: Maintained FMP_
  - _Depends: 3.1_
  - _Requirements: 5.1, 5.4, 11.2_

- [x] 3.3 Adapt and verify the FMP income-statement fetcher
  - Implement the annual income statement interface while preserving period, reporting date, currency and financial values supplied by the provider.
  - Verify supported symbol/period/limit behavior, response shape and null handling through the shared income route.
  - Done when route-level fixtures match the source statement without unit conversion, silently filled zeros or altered periods.
  - Complexity: the task's entire modified maintained production scope passes 400 physical lines/file, 300 logical units/file and 50/function using the implemented checker; record generated exclusions and reviewed exceptions.
  - _Boundary: Maintained FMP_
  - _Depends: 3.2_
  - _Requirements: 5.1, 5.4, 11.2_

- [x] 3.4 Preserve provider failures without leaking credentials
  - Adapt the shared response helper so authentication, entitlement, throttling, invalid parameters and missing data remain distinguishable.
  - Redact credential-bearing URLs/error text and prohibit fallback to a different provider or fabricated results.
  - Done when each failure fixture produces the expected observable category and sentinel secrets are absent from responses and logs.
  - Complexity: the task's entire modified maintained production scope passes 400 physical lines/file, 300 logical units/file and 50/function using the implemented checker; record generated exclusions and reviewed exceptions.
  - _Boundary: Maintained FMP_
  - _Depends: 3.3_
  - _Requirements: 5.2, 5.3, 9.6_

- [x] 3.5 Initialize the data runtime with FRED and shared routers
  - Install the selected owned equity/economy/FRED packages and maintained FMP extension into the locked runtime; initialize provider settings from runtime-only credentials.
  - Implement no-quota health/readiness and the design's owner-managed origin trust choice without mistaking a Workspace session for data API auth.
  - Done when profile/income/GDP routes exist, FRED values/dates/frequency/units and failure fixtures pass, and no custom database or persistent data volume is needed.
  - Complexity: the task's entire modified maintained production scope passes 400 physical lines/file, 300 logical units/file and 50/function using the implemented checker; record generated exclusions and reviewed exceptions.
  - _Boundary: Data API runtime_
  - _Depends: 3.4_
  - _Requirements: 5.5, 5.6, 5.8, 5.9, 11.1_

- [x] 3.6 Build and load the identified data runtime image
  - Add the locked owned data runtime to the Dagger builder using recorded local provider packages rather than accidentally resolving replacements from a registry.
  - Export/load the initial image and verify source labels, supported routes and server credential initialization; generation consumes this exact loaded image in the next task.
  - Done when a clean identified image is available to the portable generation command without requiring generated contract snapshots as a build input.
  - Complexity: the task's entire modified maintained production scope passes 400 physical lines/file, 300 logical units/file and 50/function using the implemented checker; record generated exclusions and reviewed exceptions.
  - _Boundary: Dagger image builder and data API integration_
  - _Depends: 2.5, 3.5_
  - _Requirements: 1.1, 1.5, 3.2, 9.1, 11.1_

- [x] 3.7 Freeze installed routes and regenerate the supported catalog
  - Join the schema served by the loaded image from 3.6 to the provisional dataset inventory; pin operation IDs, parameters and responses only after provider registration succeeds.
  - Implement portable canonical schema/widget/app generation using upstream generators, a mixed-source starter dashboard and the bundled FRED app where compatible.
  - Done when repeated generation has identical hashes, all references resolve, supported mappings are explicit and contract changes stop affected lanes for revalidation.
  - Complexity: the task's entire modified maintained production scope passes 400 physical lines/file, 300 logical units/file and 50/function using the implemented checker; record generated exclusions and reviewed exceptions.
  - _Boundary: Consumer contracts and data API integration_
  - _Depends: 3.6_
  - _Requirements: 4.3, 4.5, 5.4, 11.1, 11.3_

- [ ] 3.8 Verify the served image and current catalog identity
  - BLOCKED pending a separately reviewed/approved current renderer/catalog source-join task graph and its acceptance; historical 2.9 Perspective bindings are superseded. Acceptance of 2.37 or 2.40 alone does not satisfy this prerequisite. This existing integration gate must be split into bounded leaves in that followup plan if needed; it is not dispatched from this amendment.
  - Compare the identified candidate data/Workspace served schema/catalog with installed generated snapshots and the accepted current renderer binding; ensure generated assets reference the actual preserved OpenBB behavior. Controller alone writes shared snapshots/source locks.
  - Inspect image layers/metadata for provider credentials. If generation changes embedded assets, rebuild the affected candidate through Dagger only and rerun portable reference checks against that exact loaded image; no prior image evidence is reused.
  - Done when independently reviewed loaded-image identities, served metadata and canonical contract hashes agree. This verifies catalog identity, not renderer parity, live-provider acceptance or publication readiness.
  - Complexity: maintained helpers pass 400 physical/300 logical/50 per-function using actual manifests; tests/evidence/generated output are documented exclusions.
  - _Boundary: Controller consumer contracts and data API integration_
  - _Depends: 3.7_
  - _Requirements: 1.1, 4.3, 4.5, 4.8, 4.9, 5.3, 5.9, 9.6, 11.1, 11.3_

- [ ] 4. Join and accept the dashboard baseline

- [ ] 4.1 Implement the controlling Compose definition and preflight
  - BLOCKED until current renderer-complete image acceptance in 2.12 and catalog identity in 3.8, including their separately reviewed replacement source-join prerequisites. Source-safe helper acceptance cannot satisfy either prerequisite or unlock dashboard/delivery acceptance.
  - Create image-only runtime control with one HTTP publication, project-relative application binds, separate provider/agent credentials and an optional Excel profile.
  - Distinguish identified local candidates from production digests; validate configuration names without values and reject placeholder selected images, wrong mounts and unsafe state roots.
  - For the dashboard checkpoint, explicitly start only Workspace and data-api from the unchanged Compose definition. Preflight validates selected images; an inactive parser-only agent reference must never be pulled, started or published, and Workspace has no startup dependency on agent.
  - Done when tests pass with no agent image available and inactive Excel needs no image. Full baseline startup and release acceptance require the real agent image.
  - Complexity: the task's entire modified maintained production scope passes 400 physical lines/file, 300 logical units/file and 50/function using the implemented checker; record generated exclusions and reviewed exceptions.
  - _Boundary: Runtime control_
  - _Depends: 2.12, 3.8_
  - _Requirements: 2.1, 2.3, 2.4, 3.1, 3.4, 3.6, 3.7, 3.8, 11.6_

- [ ] 4.2 Exercise real Compose lifecycle in isolated run directories
  - Implement the direct host Compose harness using unique project names, validated daemon-host roots, archive loading, explicit selected services and owned cleanup; prove the dashboard checkpoint never pulls or starts the inactive agent.
  - Verify actual mounts, fixed port publication, restart behavior, actionable port collisions and rejection of unsupported remote-daemon path assumptions.
  - Done when WSL and clean Linux fixture runs produce equivalent inspected topology and cleanup affects only their own services/data.
  - Complexity: the task's entire modified maintained production scope passes 400 physical lines/file, 300 logical units/file and 50/function using the implemented checker; record generated exclusions and reviewed exceptions.
  - _Boundary: Verification and runtime integration_
  - _Depends: 4.1_
  - _Requirements: 2.1, 2.2, 2.3, 3.1, 3.6, 10.4_

- [ ] 4.3 Verify original dashboard controls and their effects in the real frontend
  - BLOCKED until 4.2 and the separately reviewed current renderer/application join and complete original capability/flag mapping are accepted. Split the actual matrix into bounded verification leaves in the followup task graph before dispatch; source-safe 2.37 or bounded A2 2.40 is insufficient.
  - Preserve real Playwright account/login/connector registration, absolute same-origin discovery, FMP/FRED add/arrange/resize/remove and observable widget values. Exercise original controls, menus, conditional actions and flag defaults with actual financial results, chart/table transitions, settings and exports under 4.8/4.9.
  - Compare original/candidate integrated light/dark shell, themes, typography, controls, focus and interactions; assert resulting observations and exact state changes. Native Perspective explorer behavior and unavailable legacy controls cannot substitute for the original UX.
  - Done when independently reviewed real-app regressions verify displayed outcomes and failure/recovery with isolated headless one-worker Playwright/CDP diagnostics. Missing controls or capability differences block acceptance and remain visible in the matrix.
  - Complexity: tests/evidence are exclusions; maintained runner/helpers pass whole-file 400 physical/300 logical/50 per-function with actual scope manifests.
  - _Boundary: Verification and Workspace integration_
  - _Depends: 4.2_
  - _Requirements: 4.1, 4.3, 4.5, 4.6, 4.8, 4.9, 10.1, 10.2, 10.3_

- [ ] 4.4 Verify mixed-provider financial fidelity and failure states
  - Compare equivalent Workspace/API parameters and fixture values with units, currency, period and available frequency metadata; include visible failed refresh behavior.
  - Compare configured-view aggregates and exports with independent fixture calculations; prove missing values and incompatible units are not silently coerced, and failed refresh preserves visibly stale last-success data until recovery.
  - Run separately marked entitled live FMP profile/income and FRED GDP checks with narrowly injected local keys.
  - Done when both sources refresh and comparison evidence is recorded; missing entitlement, skipped live checks or substituted data cannot pass baseline acceptance.
  - Complexity: the task's entire modified maintained production scope passes 400 physical lines/file, 300 logical units/file and 50/function using the implemented checker; record generated exclusions and reviewed exceptions.
  - _Boundary: Verification and data API integration_
  - _Depends: 4.3_
  - _Requirements: 5.1, 5.2, 5.4, 5.6, 5.7, 5.8, 10.3, 11.2_

- [ ] 4.5 Accept actual dashboard persistence and the validated API baseline
  - BLOCKED until 4.4, accepted SQLite 4.9, current real-app renderer joins and full original capability checks pass. A separately reviewed followup graph sizes the restart/failure matrix before dispatch; helper acceptance or a smaller unreleased chart milestone cannot certify this baseline.
  - Explicitly save layout/widget parameters and original chart model, selected range, active/inactive-family options, theme and settings-open state through the existing action. Inspect successful response, close/reopen dashboard, restart the disposable environment, sign in again and assert stored state and refreshed observations under the same source/image set.
  - Preserve table column order/widths/selection ownership across chart return, refresh and family changes. Include failed-save recovery without false saved state or lost edits; outgoing POST/engine recreation alone is insufficient.
  - Join current clean-build, catalog, financial, integrated light/dark/control and persistence evidence. Done when independent review accepts the complete current baseline record and breadth distinguishes verified, failing and untested capabilities. Known original chart gaps block renderer/release acceptance; no unavailable-state exception is introduced.
  - Complexity: tests/evidence are excluded; any maintained runner/helper passes 400 physical/300 logical/50 per-function with actual scope manifests.
  - _Boundary: Verification and Workspace integration_
  - _Depends: 4.4, 4.9_
  - _Requirements: 2.2, 4.2, 4.4, 4.7, 4.8, 4.9, 8.1, 10.5, 10.6, 11.1_

- [ ] 5. Implement and accept Anthropic

- [ ] 5.1 Establish the typed agent service and discovery contract
  - Pin compatible SDK/client artifacts, initialize the service's runtime configuration and local health checks, and expose only implemented custom-agent capabilities.
  - Generate the stable agent identity and external query URL from public configuration; do not load provider or application signing keys.
  - Done when request/discovery fixtures validate against the pinned frontend protocol and health checks spend no model quota.
  - Complexity: the task's entire modified maintained production scope passes 400 physical lines/file, 300 logical units/file and 50/function using the implemented checker; record generated exclusions and reviewed exceptions.
  - _Boundary: Anthropic agent_
  - _Depends: 4.5_
  - _Requirements: 12.1, 12.3_

- [ ] 5.2 Implement selected-widget continuation without retrieval loops
  - Handle the initial selected-widget descriptors by requesting browser-side data and completing that stream, then process the subsequent tool-result request.
  - Validate message roles, result identities, available metadata and bounded context; reject unavailable/oversized data explicitly without silently truncating observations.
  - Done when continuation/error fixtures prove exactly the required retrieval cycle and no arbitrary server-side widget URL fetching occurs.
  - Complexity: the task's entire modified maintained production scope passes 400 physical lines/file, 300 logical units/file and 50/function using the implemented checker; record generated exclusions and reviewed exceptions.
  - _Boundary: Anthropic agent_
  - _Depends: 5.1_
  - _Requirements: 12.1, 12.2_

- [ ] 5.3 Stream Anthropic output with explicit model and failure behavior
  - Translate the validated conversation into Anthropic requests and frontend-compatible text/status events using the exact configured model.
  - Implement cancellation, request limits, auth/model errors and partial-stream handling without automatic model substitution or secret/payload logging.
  - Done when simulated stream/error cases pass and an authorized minimal inference validates the chosen model; model listing alone is insufficient.
  - Complexity: the task's entire modified maintained production scope passes 400 physical lines/file, 300 logical units/file and 50/function using the implemented checker; record generated exclusions and reviewed exceptions.
  - _Boundary: Anthropic agent_
  - _Depends: 5.2_
  - _Requirements: 12.1, 12.2, 12.3_

- [ ] 5.4 Build and register the agent without coupling dashboard health
  - Add the real agent image to Dagger's build-only catalog and connect it through the established origin route and existing custom-agent configuration; join the full required service set and reject any parser-only inactive reference.
  - Keep hosted Copilot enhancements disabled; verify stream buffering/timeouts and dashboard operation while the agent is stopped.
  - Done when discovery and a real streamed response work through the configured origin and the data/dashboard journey survives agent unavailability.
  - Complexity: the task's entire modified maintained production scope passes 400 physical lines/file, 300 logical units/file and 50/function using the implemented checker; record generated exclusions and reviewed exceptions.
  - _Boundary: Anthropic agent and Workspace integration_
  - _Depends: 5.3_
  - _Requirements: 2.1, 12.1, 12.3, 12.5_

- [ ] 5.5 Accept grounded Workspace AI and unlock Excel work
  - Preserve a Playwright journey selecting a known financial observation and assert that the live answer uses its value, period and unit; include cancellation and visible failures.
  - Tie the independent acceptance record to exact Workspace, data and agent identities plus model and contract hashes.
  - Done when the reviewed current record passes the eligibility validator; otherwise every Excel source, generator, snapshot and image task remains blocked.
  - Complexity: tests and evidence are excluded; any maintained runner or helper changed here passes the 400 physical/300 logical/50 per-function caps.
  - _Boundary: Verification and Anthropic integration_
  - _Depends: 5.4_
  - _Requirements: 8.1, 10.3, 10.5, 10.6, 12.1, 12.2, 12.4, 12.5_

- [ ] 6. Adapt Excel after Anthropic acceptance

- [ ] 6.1 Prepare the add-in and split oversized generator responsibilities
  - Only after agent acceptance, install the locked add-in dependencies and record exact package/asset provenance and unresolved rights.
  - Extract schema-input and compatibility responsibilities from oversized maintained generators without changing the existing supported function behavior.
  - Done when baseline generator fixtures still pass, required source files fit their measured budgets or reviewed exceptions, and unsupported dependencies remain explicit.
  - Complexity: the task's entire modified maintained production scope passes 400 physical lines/file, 300 logical units/file and 50/function using the implemented checker; record generated exclusions and reviewed exceptions.
  - _Boundary: Excel adaptation_
  - _Depends: 5.5_
  - _Requirements: 1.2, 1.3, 1.4, 6.5, 11.4_

- [ ] 6.2 Regenerate Excel functions from accepted local contracts
  - Replace private/PAT-based schema fetches with accepted local OpenAPI/widgets and generate supported functions deterministically.
  - Compare namespace, names, argument order/defaults, request paths and spill shapes against prior contracts; retain compatibility wrappers where necessary.
  - Done when contract fixtures pass, repeated output is stable and the machine-readable compatibility report lists workbook impacts.
  - Complexity: the task's entire modified maintained production scope passes 400 physical lines/file, 300 logical units/file and 50/function using the implemented checker; record generated exclusions and reviewed exceptions.
  - _Boundary: Excel adaptation_
  - _Depends: 6.1_
  - _Requirements: 6.4, 6.5, 11.3, 11.4_

- [ ] 6.3 Adapt Excel application login and data requests
  - Keep self-hosted application login/session semantics and use the same public data base without assuming its authentication accepts the app bearer.
  - Handle expiry, failed data requests and response envelopes while keeping provider and Cloudflare service secrets out of client assets.
  - Done when controlled login/data/expiry fixtures exercise the expected paths, headers and displayed failures.
  - Complexity: the task's entire modified maintained production scope passes 400 physical lines/file, 300 logical units/file and 50/function using the implemented checker; record generated exclusions and reviewed exceptions.
  - _Boundary: Excel adaptation_
  - _Depends: 6.2_
  - _Requirements: 6.2, 6.3, 6.5, 5.3, 5.9_

- [ ] 6.4 Make manifest and add-in URLs deployment-configurable
  - Render runtime public-origin configuration and the trusted HTTPS manifest consistently without rebuilding application images for WSL versus Linux.
  - Preserve the supported function namespace and SharedRuntime contract; distinguish development access from actual Office HTTPS acceptance.
  - Done when two public URL settings produce coherent manifest/assets from the same image inputs and contract checks reject mismatched origins.
  - Complexity: the task's entire modified maintained production scope passes 400 physical lines/file, 300 logical units/file and 50/function using the implemented checker; record generated exclusions and reviewed exceptions.
  - _Boundary: Excel adaptation_
  - _Depends: 6.3_
  - _Requirements: 3.3, 3.7, 6.1, 6.5_

- [ ] 6.5 Build Excel assets and integrate the optional runtime profile
  - Add the static add-in image to the Dagger build-only catalog and connect the already defined optional origin route/profile.
  - Verify enabling or disabling the add-in does not change accepted Workspace, data or agent behavior and does not require origin TLS management.
  - Done when the selected image loads correctly through the profile and shared regressions still pass.
  - Complexity: the task's entire modified maintained production scope passes 400 physical lines/file, 300 logical units/file and 50/function using the implemented checker; record generated exclusions and reviewed exceptions.
  - _Boundary: Excel adaptation and runtime integration_
  - _Depends: 6.4_
  - _Requirements: 2.4, 6.1, 9.1, 11.5_

- [ ] 6.6 Prepare reproducible Office acceptance inputs
  - Establish a validation workbook/procedure for the supported FMP function with explicit expected values/shape, refresh and reopen checks.
  - Record manifest/function/schema hashes and compatibility expectations; automate all generator/client checks that do not require a real Office host.
  - Done when the input bundle is reproducible and ready for actual Windows Excel testing against a published candidate; browser checks are not labeled Office acceptance.
  - Complexity: tests and evidence are excluded; any maintained runner or helper changed here passes the 400 physical/300 logical/50 per-function caps.
  - _Boundary: Verification and Excel integration_
  - _Depends: 6.5_
  - _Requirements: 6.3, 6.4, 6.5, 11.4, 11.5_

- [ ] 7. Build portable delivery and recovery commands

- [ ] 7.1 (P) Implement portable image publication and candidate identities
  - Load and push exact exported images using configurable registry/source inputs and ephemeral credentials, without rebuilding or giving registry credentials to Dagger.
  - Write unpromoted candidate manifests only for complete selected image sets and verify pushed digest identity.
  - Done when registry integration fixtures prove partial pushes cannot create a complete candidate and publication runs without GitHub-specific inputs.
  - Complexity: the task's entire modified maintained production scope passes 400 physical lines/file, 300 logical units/file and 50/function using the implemented checker; record generated exclusions and reviewed exceptions.
  - _Boundary: Portable CI commands_
  - _Depends: 4.5_
  - _Requirements: 1.1, 9.2, 9.6, 9.7_

- [ ] 7.2 Implement release promotion with matching evidence gates
  - Validate full candidate completeness and required live, fixture, Office, Linux and recovery records against exact digests/contracts.
  - Keep internal dashboard/agent checkpoints distinct from complete baseline releases; require prior agent eligibility before accepting Excel work records.
  - Done when absent, stale, skipped and failing records block promotion, while matching complete fixtures produce immutable release settings.
  - Complexity: the task's entire modified maintained production scope passes 400 physical lines/file, 300 logical units/file and 50/function using the implemented checker; record generated exclusions and reviewed exceptions.
  - _Boundary: Portable CI commands_
  - _Depends: 7.1_
  - _Requirements: 8.1, 9.2, 9.3, 9.5, 10.6, 12.4_

- [ ] 7.3 Add thin GitHub runners for the portable commands
  - Create pinned verification/release wrappers limited to checkout, setup, permission/secret plumbing, command invocation and artifact retention.
  - Separate untrusted fixture checks from authorized live/publication runs and enforce Excel eligibility before invoking its build/generation tasks.
  - Done when wrapper validation and a clean runner exercise build-only Dagger plus portable verification without duplicated pipeline logic.
  - Complexity: the task's entire modified maintained production scope passes 400 physical lines/file, 300 logical units/file and 50/function using the implemented checker; record generated exclusions and reviewed exceptions.
  - _Boundary: Portable CI commands_
  - _Depends: 7.2_
  - _Requirements: 9.1, 9.2, 9.3, 9.6, 9.7_

- [ ] 7.4 Prove the CI command boundary is portable to another runner
  - Invoke the same build/check/publication interfaces in clean Linux with no GitHub-specific environment or API.
  - Vary explicit registry/source/run inputs and verify documented exit/report contracts; retain platform-specific artifact/secret setup only in wrappers.
  - Done when portability checks pass and actual Gitea deployment remains explicitly untested and out of this baseline.
  - Complexity: tests and evidence are excluded; any maintained runner or helper changed here passes the 400 physical/300 logical/50 per-function caps.
  - _Boundary: Verification and portable CI integration_
  - _Depends: 7.3_
  - _Requirements: 9.1, 9.7, 10.6_

- [ ] 7.5 Implement consistent stopped-state backups
  - Capture the stopped Workspace bind tree and a backup manifest tying checksums, ownership, state format and source/image identities together.
  - Handle private runtime configuration separately from public release artifacts and prevent accidental overwrite of the only usable snapshot.
  - Done when backup tests reject running/inconsistent state and secret files never enter public reports.
  - Complexity: the task's entire modified maintained production scope passes 400 physical lines/file, 300 logical units/file and 50/function using the implemented checker; record generated exclusions and reviewed exceptions.
  - _Boundary: Runtime control_
  - _Depends: 7.4_
  - _Requirements: 8.2, 8.3, 8.4, 9.5_

- [ ] 7.6 Implement clean restore and incompatible rollback protection
  - Restore verified snapshots into new owned directories using the matching image set; check path boundaries, checksums and file ownership.
  - Reject older images against incompatible migrated state and preserve the original deployment on failure.
  - Done when restore fixtures recover known state, fail corrupted/incompatible inputs safely and record the required previous snapshot for rollback.
  - Complexity: the task's entire modified maintained production scope passes 400 physical lines/file, 300 logical units/file and 50/function using the implemented checker; record generated exclusions and reviewed exceptions.
  - _Boundary: Runtime control_
  - _Depends: 7.5_
  - _Requirements: 8.2, 8.3, 8.4, 9.5_

- [ ] 8. Accept the complete candidate and promote the release

- [ ] 8.1 Publish the complete unpromoted baseline candidate
  - Join exact fork revisions, locked builds, supported component rights, contract snapshots and all selected image digests into one complete candidate.
  - Resolve essential component availability/license decisions before acceptance; do not reuse upstream enterprise keys as entitlement evidence.
  - Done when the candidate can be pulled without source builds and its manifest contains no placeholder image, unresolved essential asset or secret.
  - Complexity: execution and evidence-only work has no production-code scope; needed fixes reopen their owning capped task and invalidate affected acceptance.
  - _Boundary: Release control integration_
  - _Depends: 6.6, 7.4, 7.6_
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 9.2, 9.6, 11.1_

- [ ] 8.2 Accept pull-only WSL and private Linux operation
  - Use the exact candidate image set in clean WSL and private Linux deployment directories; run the same topology with environment-specific public URL.
  - Verify public HTTPS through the owner's existing Access tunnel, plain HTTP origin publication, bind state, application login and marked provider/agent checks.
  - Done when no application compilation occurs on the target and evidence records actual host, image and route identities. The owner runs Compose locally on the private host and can supply acceptance evidence; missing host evidence remains unverified without requiring agent SSH access.
  - Complexity: execution and evidence-only work has no production-code scope; needed fixes reopen their owning capped task and invalidate affected acceptance.
  - _Boundary: Runtime control integration_
  - _Depends: 8.1_
  - _Requirements: 2.1, 2.3, 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8, 9.4_

- [ ] 8.3 Accept the candidate in Windows Excel
  - Load the candidate manifest in the supported Windows Excel host and exercise trusted assets, Access/session behavior and self-hosted application login.
  - Calculate the supported FMP function, compare the equivalent API result, refresh and reopen the validation workbook without signature changes.
  - Done when Office version, manifest/schema/image hashes and observed workbook results are recorded; unsupported host/access behavior blocks acceptance rather than being replaced by browser evidence.
  - Complexity: execution and evidence-only work has no production-code scope; needed fixes reopen their owning capped task and invalidate affected acceptance.
  - _Boundary: Verification and Excel integration_
  - _Depends: 8.2_
  - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5, 11.5_

- [ ] 8.4 Accept recovery against the complete candidate
  - Create a stopped snapshot with a known saved dashboard, restore into another clean directory and start the matching pulled image set.
  - Verify account sign-in, widget layout/parameters and live refresh after restore, plus a rejected incompatible rollback.
  - Done when recovery succeeds without altering the only original deployment and prior image/state requirements are recorded.
  - Complexity: execution and evidence-only work has no production-code scope; needed fixes reopen their owning capped task and invalidate affected acceptance.
  - _Boundary: Runtime control integration_
  - _Depends: 8.3_
  - _Requirements: 2.2, 4.2, 4.7, 8.2, 8.3, 8.4, 9.5_

- [ ] 8.5 Close cross-component verification and operator guidance
  - Run the final shared-module complexity audit, relevant secret/layer/log/browser checks and all required regressions against candidate identities.
  - Reconcile every breadth entry with actual checks and sanitized evidence; update financial-engineer development/deployment/recovery/compatibility guidance using the commands just exercised.
  - Done when all required criteria have current passing evidence, capability limitations are explicit, and README/docs navigation leads to accurate procedures.
  - Complexity: all maintained production scopes pass the 400 physical/300 logical/50 per-function audit; tests, generated artifacts and documentation exclusions are explicit.
  - _Boundary: Verification and documentation integration_
  - _Depends: 8.4_
  - _Requirements: 1.3, 1.4, 3.4, 8.1, 9.6, 10.1, 10.2, 10.3, 10.4, 10.5, 10.6, 11.6, 11.7, 12.3_

- [ ] 8.6 Promote and install the accepted immutable release
  - Run the portable promotion gate on the complete accepted candidate and preserve previous release/backup identifiers.
  - Install by pulling promoted digests and starting without builds; confirm the promoted set matches the accepted candidate and optional Excel leaves the other services usable.
  - Done when the release manifest, installation result and recovery references agree; no check is passed by skipping or relabeling missing evidence.
  - Complexity: execution and evidence-only work has no production-code scope; needed fixes reopen their owning capped task and invalidate affected acceptance.
  - _Boundary: Release control and runtime integration_
  - _Depends: 8.5_
  - _Requirements: 2.4, 8.1, 9.2, 9.3, 9.4, 9.5, 11.5_

- Task 2.4 process note: original RED was an artificial unconditional failure, so test-first compliance is not established. Independent review accepted current behavior after three explicitly retrospective baseline failures and fresh nginx/lint/size checks; artifacts/task-2.4/evidence.json preserves the chronology.
- Task 2.5 packaging note: pinned Dagger requires serial SDK initialization and checksum-preserving HTTP ADD translation. Exact source exceptions retain the frontend build helper and Data component. Independent review reproduced 68 tests and fresh image runtime acceptance; artifacts/task-2.5 holds the identities and evidence. The image remains provisional until renderer replacement.
- Task 2.6 review note: independent review caught pagination settings and saved Set/Multi filter compatibility regressions. Both were repaired with retained failing tests and fresh independent checks. Original implementation RED was captured only in the worker tool transcript; remediation RED logs are retained under artifacts/task-2.6. Whole-project typechecking remains blocked by the unchanged upstream configuration; lint, actual build and focused tests passed.

Task 2.7 accepted after independent Astra review: 70 independently rerun task tests and 10 audit controls passed; the protected clean install, production build, 6,488-module graph and 258 JavaScript chunks contain no removed commercial modules or initialization. Workspace `0341b12524cb822262be631fa820e2ca851a348a`. Exact 55-path snapshot and review evidence: `artifacts/task-2.7/joined-freeze.json`, `review-verification.json`, `committed-complexity.json`. Seven no-growth type-import exceptions are documented in [the narrow review](task-2.7-exception-review.md). Full typechecking remains blocked by upstream configuration; real browser and final-image checks remain later gates.

Task 2.8 accepted after independent Astra review and one repair round. Workspace `48e3f59cc48e0ae7aa6f6ce92069fc5b10ee3e86` adds the owned Perspective 5.6.0 runtime with same-origin worker/WASM assets. Independent 10 unit tests, strict selected TypeScript, Biome and four production browser cases passed; development cases also passed. A reproduced stale-theme rejection race was repaired and retained as a regression. Full-project TypeScript and integrated dashboard visual/financial acceptance remain outside this gate. Evidence: `artifacts/task-2.8/review-round2-verification.json`, `runtime-freeze.json`, `browser-evidence.json` and `committed-complexity.json`. Initial feature RED is retained; the earlier initialization-cleanup regression was GREEN-first, not retrospectively described as TDD.

## Approved design slice: chart state and lifecycle foundation

The owner approved the [first production boundary](echarts-integration-proposal.md#first-production-boundary-for-separate-review) on 2026-10-16. Tasks 2.13-2.18 below were approved by the owner on 2026-10-16 for that boundary only. They neither reactivate superseded tasks 2.9-2.12 nor approve the rest of the renderer design. They support 4.8-4.9 without closing either requirement. Existing task groups retain their own coverage and approval states.

This is an explicit dependency exception to the historical numeric renderer sequence: 2.13 starts from accepted 1.2, 1.4, 1.7 and 2.8, not from pending 2.9-2.12 or later release tasks. Thereafter the dependencies below govern this slice. All leaves target one bounded 1-3 hour engineering work unit; unexpected scope returns to the controller rather than expanding ownership silently.

### Ownership and parallel execution

Workspace paths below are relative to `terminalpro/`; root paths are relative to QOpenBB. New paths are planned, not completed assets. State and host workers are not alone: preserve other work and never revert the untracked financial lane or pending catalog/inventory changes.

| Task/lane | Exclusive writable scope | Prerequisite / model |
| --- | --- | --- |
| 2.13 setup | Workspace package/lock, new `tests/unit/chart-compatibility/vitest.config.mjs`, focused `tsconfig.json`, `tests/e2e/chart-compatibility/` Vite/Playwright fixture setup; root complexity inventory and dependency documentation | Accepted 1.2, 1.4, 1.7, 2.8; controller serializes setup |
| 2.14 contracts | `src/components/General/Table/Chart/compatibility/legacyTypes.ts`; host interface declarations in `Chart/echarts/lifecycle.ts`; contract fixtures/type checks under `tests/unit/chart-compatibility/` | 2.13; controller/Sol, then freeze shared contracts |
| 2.15 state lane | `Chart/compatibility/integratedState.ts`, `detachedState.ts`; corresponding unit fixtures/tests | 2.14; Sol |
| 2.16-2.17 host lane | `Chart/echarts/lifecycle.ts`, `EChartsHost.tsx`; host unit tests and `tests/e2e/chart-compatibility/` fixture/spec files | 2.14, then 2.16; Sol |
| 2.18 join | Controller-owned test scripts/config registration if necessary; inventory, breadth, scoped evidence/docs and source identity records | 2.15 and 2.17; controller with independent Astra review |

Full paths for the new `Chart/` modules resolve under `src/components/General/Table/`. Controller owns package/lock, shared configuration, scope inventory, commits and any root command join throughout. Foundation config ownership transfers to the host lane only after 2.14 freezes interfaces; no concurrent writes to shared files. At most controller + two workers + one reviewer; one heavy install/build/browser at a time. State unit work may overlap host work. Astra reviews state semantics and lifecycle evidence. Each code leaf requires implementation, independent review and fresh verification before its checkbox closes.

Application call sites, `communityBoundary` guards, widget registry/catalog bindings, editor UI, chart-family translation, provider/backend code and release promotion are excluded. The foundation connects through maintained module and browser tests, not a partially enabled product path. Further application integration requires its own approved design/tasks. Anthropic-before-Excel and Dagger-build-only rules remain unchanged.

### Foundation verification contract

Reuse the existing narrow Perspective test patterns without changing their files. Adapted chart commands below are planned until implemented and exercised from the owned Workspace `terminalpro/` directory:

```sh
node node_modules/vitest/vitest.mjs run --config tests/unit/chart-compatibility/vitest.config.mjs
node node_modules/typescript/bin/tsc --project tests/unit/chart-compatibility/tsconfig.json --noEmit
node node_modules/vite/bin/vite.js build --config tests/e2e/chart-compatibility/vite.config.ts
node <QOPENBB_ROOT>/verification/node_modules/@playwright/test/cli.js test --config tests/e2e/chart-compatibility/playwright.config.ts
```

The Playwright config owns a loopback-only preview server for the freshly built fixture, rejects more than one worker, uses a fresh browser context and never reuses an operator server. Set the documented project-local browser cache explicitly. Vite fixture configuration uses `envDir: false`; tests do not load `.env`, real credentials or provider data. Capture CDP runtime/console/network diagnostics, screenshot/output identities, exits and cleanup. A build or module-presence check is not a rendered-data assertion.

Use the existing [complexity gate](../../../docs/complexity.md) from QOpenBB with explicit current fork base/head or changed-file manifests for both forks. Do not reuse historical scope SHAs or an empty manifest to bypass this lane's changes. Setup must establish and freeze the exact executable scoped command before accepting 2.14 onward. Preserve unrelated unfinished work through isolated snapshots or accurately scoped manifests; do not claim a clean checkout when it is dirty.

Whole-project TypeScript remains separately blocked by upstream TS6305 composite-output and TS5103 configuration issues. These tasks require strict checks of the complete new module/test/fixture dependency closure and cannot relabel that as whole-application typecheck success. Test helpers/fixtures and docs have explicit policy exclusions; maintained build/production logic cannot hide there.

- [x] 2.13 Prepare protected chart dependencies and isolated verification
  - Pin ECharts 6.0.0 in the owned application with the existing validated Bun lock exception; verify Safe Chain interception, the 48-hour age policy and protected frozen restoration. Retain notices and dependency provenance; do not migrate the application lock or inject a global script.
  - Record planned module ownership in the foundation table. Register each maintained module in the executable complexity inventory when introduced, before accepting its leaf; the checker rejects mapped files that do not exist. Preserve unrelated pending entries and the explicit test exclusions. Establish focused Vitest/strict-TypeScript configuration and isolated production-build browser fixture tooling from exercised patterns, without importing broad app configuration or local secrets.
  - Done when protected restore and a real-library fixture smoke render pass, exact commands/tool/source identities are retained, and the scoped complexity command is ready for worker handoffs. This setup proves tooling, not the new host or renderer parity.
  - Complexity: all modified maintained production/build/configuration files pass 400 physical lines/file, 300 logical units/file and 50/function where applicable; package locks, tests and fixture exclusions are recorded rather than measured as production.
  - _Boundary: Controller-owned dependency, verification and inventory setup_
  - _Depends: 1.2, 1.4, 1.7, 2.8_
  - _Requirements: 1.1, 1.2, 4.8, 4.9, 10.1, 10.3, 10.4, 10.5_

- [x] 2.14 Freeze path-specific state inputs and the renderer host contract
  - Define distinct integrated/detached input types, retained JSON values and explicit validation results without `any`. Integrated inputs include resolved state key, current model, resolved option baseline, event options defaulting to an empty object, chart type, resolved total series and pivot. Detached inputs include original storage, event type/options and resolved total series.
  - Freeze the typed complete-option/revision host interface and lifecycle ownership. Callers remain responsible for original state-key/range/count preparation and revision/address checks; reducers neither infer API-derived counts nor silently redirect stale edits.
  - Build source-referenced contract fixtures covering different resolved/persisted options and retained unknown fields. Done when focused strict checking and contract validation pass and both implementation lanes receive immutable interfaces, fixture inputs and commands; do not infer saved paths from the editor's empty write capture.
  - Complexity: new maintained types/validation files pass 400/300/50; source fixture/test data exclusions are explicit. No application-hook extraction or wiring is part of this task.
  - _Boundary: Shared compatibility contracts_
  - _Depends: 2.13_
  - _Requirements: 4.8, 4.9, 10.1, 10.3_

- [x] 2.15 (P) Preserve integrated and detached chart-state updates
  - Implement pure, separate reducers from the frozen inputs. Integrated changes clone the resolved options baseline, retain original deep-merge/array behavior, remove only top-level option theme, overlay the current model and update original root metadata. Detached changes preserve the prior model except chart type and replace root options without integrated theme stripping.
  - Verify input immutability, untouched partition equality, nested unknown values, resolved-versus-persisted baseline differences, array merging, absent event options and both paths' type/count/pivot semantics against source-derived expectations.
  - Done when meaningful failing regression cases pass, focused strict/unit checks and independent state review pass, and no new storage format, model range resolver or UI restriction is introduced.
  - Complexity: each maintained reducer/dependency passes 400 physical lines/file, 300 logical units/file and 50/function with current scope evidence; tests/fixtures are explicitly excluded.
  - _Boundary: State reducer lane_
  - _Depends: 2.14_
  - _Requirements: 4.8, 4.9, 10.1, 10.3_

- [x] 2.16 (P) Implement bounded ECharts instance ownership
  - Implement public-API mount/update/resize/image-export/dispose operations from the frozen complete-option contract. Keep the instance private, defer initialization for an unsized container, and prevent callbacks from mutating a disposed or replaced instance.
  - Test update ordering, cleanup on failure, repeated disposal, replacement/remount, hidden-to-sized recovery and image-export error handling. Do not claim mocked lifecycle tests establish real rendering.
  - Done when lifecycle units and focused strict checking pass with independent review; no provider data, application persistence, chart-family translation or new product controls enter this module.
  - Complexity: all maintained lifecycle code passes 400/300/50 with current scope evidence; no compressed spike code is promoted unchanged.
  - _Boundary: Renderer lifecycle lane_
  - _Depends: 2.14_
  - _Requirements: 4.8, 4.9, 10.1, 10.3_

- [x] 2.17 Bind the typed host and prove its real browser lifecycle
  - Connect React mounting, option/revision updates and resize observation to the accepted lifecycle module. Keep library types within the renderer boundary and export image data without defining original menu/filename semantics.
  - Extend the maintained isolated fixture to exercise populated charts with known options, option/data updates, size changes, zero-size recovery, unmount/remount, failure cleanup and PNG contents. Assert numeric options and visible output, not just constructor calls or canvas existence.
  - Done when the freshly built production fixture passes one-worker Playwright/CDP checks, the actual host is the tested import, resources are cleaned up and an independent reviewer reproduces the bounded result. Keep zoom/selection continuity, original styling and application save/reopen explicitly unverified.
  - Complexity: host and any modified maintained build code pass 400/300/50; test fixture exclusions are recorded. This task can overlap the state lane after 2.16, but owns the sole heavy browser queue while running.
  - _Boundary: Renderer host and browser verification lane_
  - _Depends: 2.16_
  - _Requirements: 4.8, 4.9, 10.1, 10.3, 10.4_

- [x] 2.18 Join and accept only the chart foundation evidence
  - Run the complete focused strict/unit/build/browser gates against joined source and dependency identities, plus relevant existing isolated-runtime regressions affected by dependency/test configuration changes. Register portable invocation paths without moving verification into Dagger.
  - Audit imports and diffs to confirm no application wiring, guard/flag edits, catalog changes or unrelated financial-lane work entered the slice. Selectively commit only reviewed scope. Update breadth with actual test IDs and sanitized evidence; retain overall renderer parity as unverified.
  - Done when independent fresh verification, dependency checks, exact identities and final shared-module scope audit pass; document remaining editor/state-mapping/theme/table/persistence obligations without promoting a release image.
  - Complexity: all joined maintained paths pass the existing 400/300/50 gate with accurate manifests; documentation/evidence-only edits are exempt and needed code fixes return to their owning leaf.
  - _Boundary: Controller integration of foundation tests, inventory and evidence_
  - _Depends: 2.15, 2.17_
  - _Requirements: 1.1, 1.4, 4.8, 4.9, 9.6, 10.1, 10.3, 10.4, 10.5, 10.6_

Task 2.13 accepted after independent Astra review and fresh unit, strict TypeScript, production fixture build/browser and scoped complexity checks. Workspace `e56852deff2679c71e32436554f86ba096b55677` pins ECharts 6.0.0 through protected Bun restoration. Evidence: `artifacts/task-2.13/review/review.md` and `complexity.json`. Existing oversized-file exception targets are byte-identical to the prior source; only their source identity advances. No application wiring or renderer parity is accepted.

Task 2.14 accepted at Workspace `bfba80d7f7875fffa60d6d37645a422a3097ea63` after independent Astra source comparison, 11 unit tests, strict TypeScript, scoped lint and fresh complexity verification. Runtime option values remain separate from serialized unknown JSON, with repeated-edit input/output closure and no new storage envelope. Frozen contracts now permit the state and lifecycle lanes to start. Evidence: `artifacts/task-2.14/review/`.

Task 2.15 accepted at Workspace `5d6674e5629fbceda11047bcefcfac237ccd4e62`. Independent source comparison and 26 tests (16 reducer cases plus 10 contract cases), strict TypeScript, lint and complexity checks passed. Integrated and detached reducers preserve the original distinct writes, including unknown fields and runtime undefined values. Evidence: `artifacts/task-2.15/review/review.md`. These modules are not wired into application controls.

Task 2.16 accepted at Workspace `5937af2c73c3f1943fb9a16c13236b46ee623b9c`. Independent review reproduced 13 lifecycle unit cases, strict TypeScript and lint; the combined complexity gate passed. Evidence: `artifacts/task-2.16/review/review.md`. Mocked library calls establish lifecycle ownership and failure handling; real rendering remains task 2.17.

Task 2.17 accepted at Workspace `042ba87e3208a51857da4ae2d1c3109a680716d9`. Independent Astra verification passed all 46 focused tests, strict TypeScript, production build, two real-browser cases, lint and source identity checks. The reviewer inspected the 640 by 400 PNG with visible USD observations; browser tests also check numeric options, pixels, changed output, recovery and disposal. CDP diagnostics are empty. Evidence: `artifacts/task-2.17/review/verdict.md`. Original styling, interactions and application persistence remain outside this acceptance.

Task 2.18 accepted after independent Astra joined review and scoped integration GO for tasks 2.13-2.18 only. Fresh verification reproduced 46 tests, strict TypeScript, all 24 changed branch-file identities and caps for all five production modules. Matching-source chart browser evidence (two cases) and existing Perspective regression (10 unit/four browser cases) passed. See [foundation verification](chart-foundation-verification.md) and `artifacts/task-2.18/review/verdict.md`. Full renderer and release acceptance remain open.

## Approved design slice: resolved snapshots and Cartesian mappings

The owner approved the [snapshot design](chart-snapshot-design.md). The owner approved tasks 2.19-2.23 for implementation ("yes, that fits the spec"). They extend the accepted foundation without activating application charts. Requirements 4.8-4.9 remain product-level obligations; passing this slice is not full renderer acceptance. Each leaf targets a 1-3 hour engineering unit; unexpected scope returns to the controller before implementation expands.

### Ownership and execution

Paths below are relative to `vendor/workspace/terminalpro/`; `Chart/` abbreviates `src/components/General/Table/Chart/`. Root metadata belongs exclusively to the controller. Every worker receives the approved design, leaf, frozen contracts, current source identities, test commands and 400 physical/300 logical units per file/50 units per function caps. Workers are not alone in the codebase and must preserve other lanes' edits.

| Wave | Task and model | Exclusive writable paths | Join |
| --- | --- | --- | --- |
| Contract | 2.19, controller with independent Astra review | `Chart/compatibility/snapshotTypes.ts`, `Chart/echarts/cartesianTypes.ts`; `tests/unit/chart-compatibility/snapshotContracts.types.ts`, `snapshot.fixtures.ts` | Freeze shared types and fixture expectations before workers start |
| Parallel A | 2.20, Sol implementer | `Chart/compatibility/snapshot.ts`, `tests/unit/chart-compatibility/snapshot.test.ts` | Reviewed validated snapshots |
| Parallel B | 2.21, Sol implementer | `Chart/echarts/cartesian.ts`, `tests/unit/chart-compatibility/cartesian.test.ts` | Reviewed financial mapping against frozen valid inputs |
| Browser join | 2.22, Sol implementer, Astra reviewer | `tests/e2e/chart-compatibility/cartesian.html`, `cartesian.tsx`, `cartesian.spec.ts`, existing `vite.config.ts` and `playwright.config.ts` in that directory | Compose actual validator, mapper and accepted host |
| Acceptance | 2.23, controller, independent Astra review | Root inventory/source identity/breadth records; spec verification report and docs navigation | Fresh joined evidence; no app or release activation |

At most controller + two workers + one reviewer. Each leaf follows implement -> independent review -> fresh verification -> acceptance. Serialize installs, shared configuration, commits and the single heavy build/browser queue. Task 2.21 may consume frozen valid fixtures without importing unfinished task 2.20 code; the actual validator join is mandatory in 2.22. Changes to frozen contracts pause both lanes for review. Controller registers maintained paths before feature acceptance and records test exclusions; no leaf may edit shared inventory independently.

Reuse the accepted Node/dependency environment and existing Vitest, strict TypeScript, Vite and Playwright entry points recorded in [foundation verification](chart-foundation-verification.md). From the frontend root use `node node_modules/vitest/vitest.mjs run --config tests/unit/chart-compatibility/vitest.config.mjs`, `node node_modules/typescript/bin/tsc --project tests/unit/chart-compatibility/tsconfig.json --noEmit`, and `node node_modules/vite/bin/vite.js build --config tests/e2e/chart-compatibility/vite.config.ts`. Use the root verification Playwright CLI with the existing chart config, one worker, isolated evidence paths and pinned browser cache. Controller verifies paths/tool identities before dispatch. Use the existing combined checker command from [complexity checks](../../../docs/complexity.md) with truthful fork scope, never an empty manifest masking new files. No dependency additions or package/lock changes are authorized.

- [x] 2.19 Freeze snapshot and render contracts
  - Define deeply readonly snapshot inputs/results, source modes, category ownership, ordered identities, numeric/null/missing cells, JSON provenance, unit/scale metadata and resolved style/translation results from the approved design. Include field-path diagnostics, finite-number rules and explicit unsupported outcomes.
  - Add compile-time contract checks and shared synthetic fixtures with one category descriptor, distinct IDs despite duplicate labels, homogeneous financial units and malformed-input cases. Specify known valid fixtures independently of the future validator. Do not add runtime defaults or decode legacy editor options.
  - Confirm existing strict/unit discovery includes the new paths and register the two newly created type modules in controller-owned scope inventory. Controller adds each runtime module when its owning leaf creates it, before that leaf's acceptance; do not register missing files. Done when strict checks, existing foundation units and independent contract review pass and exact signatures/fixtures are frozen for both lanes.
  - Complexity: both maintained type files pass 400/300/50 with explicit fork scope; test fixtures are excluded. No changes to accepted reducers, host, application flags or guards.
  - _Boundary: Shared snapshot and Cartesian type contracts_
  - _Depends: 2.18_
  - _Requirements: 4.8, 4.9, 10.5, 10.6_

- [x] 2.20 (P) Preserve resolved observations in validated snapshots
  - Implement validation and deep copy without grid, React, ECharts, provider or store imports. Preserve ordering, numeric precision, zeros, missing/null distinctions, original model fields, state address and range provenance.
  - Verify category cardinality/association, unique row/column/selection IDs, numeric-series presence, unknown IDs, invalid provenance, nonfinite values, input mutation isolation, repeated categories and descending dates. Valid nonflat snapshots retain their source mode; renderer support is decided separately.
  - Done when focused snapshot tests, strict checks and independent review pass against frozen contracts, with no financial conversion, sorting, aggregation or persistence added.
  - Complexity: all maintained scope passes 400/300/50 using current measured manifests; tests/fixtures remain recorded exclusions.
  - _Boundary: Snapshot validation lane_
  - _Depends: 2.19_
  - _Requirements: 4.8, 4.9_

- [x] 2.21 (P) Map the three resolved Cartesian families
  - Translate exact groupedColumn, stackedColumn and line inputs through the frozen style contract. Keep series identity and style keyed to column IDs, selection order, repeated category positions and label/tooltip display. Replace complete options so family switches cannot retain bar/stack properties.
  - Validate styles and reject unsupported families/source modes or unknown/incompatible unit/scale semantics with structured results. Test missing/null gaps, negative stacks, display-only precision, numeric fidelity, reordered series styles, title/legend/palette projection and no fallback. No original model options are silently claimed as supported.
  - Done when focused mapping tests, strict checking and independent financial review pass against explicit numerical expectations. No legacy editor decoder, new product controls or production rejection guard is introduced.
  - Complexity: maintained mapper passes 400/300/50; if responsibilities cannot fit, return to controller for reviewed cohesive decomposition, not compressed code or unapproved files.
  - _Boundary: Cartesian mapping lane_
  - _Depends: 2.19_
  - _Requirements: 4.8, 4.9_

- [x] 2.22 Verify snapshot-to-host rendering in an isolated browser
  - Compose actual snapshot validation and mapping with the accepted EChartsHost. The fixture owns monotonic render revisions independently of dataRevision; invalid/unsupported inputs expose diagnostics without submitting partial renders.
  - Exercise homogeneous Revenue/Costs data across all three families, repeated labels, negative stacks, settings-only updates at unchanged dataRevision, stacked-to-line replacement, resize, PNG export, rejection and recovery. Assert exact numeric options and visible labels/output; inspect images as supplementary evidence.
  - Done when the freshly built fixture passes one-worker headless Playwright with sanitized CDP diagnostics and owned cleanup, and independent review reproduces the join. Existing fixture tests remain runnable. No original application UX or persistence acceptance is claimed.
  - Complexity: test/fixture paths are documented exclusions; any maintained configuration receives applicable whole-file checks. Production fixes return to their owning leaf and review.
  - _Boundary: Explicit snapshot/mapper/host integration fixture_
  - _Depends: 2.20, 2.21_
  - _Requirements: 4.8, 4.9, 10.1, 10.2, 10.3, 10.4_

- [x] 2.23 Accept only the joined snapshot and mapping evidence
  - Run fresh focused units, strict TypeScript, fixture build and browser regressions against exact joined source/dependency identities. Audit imports/diffs and all four maintained modules; confirm no app activation, feature/flag edits, editor parsing, SQLite, provider or Excel changes entered the branch.
  - Update actual breadth test paths/results, maintained inventory, source identities and a scoped verification report linked from chart documentation. Preserve unrelated work and overall renderer parity as unverified; select only accepted changes for commits.
  - Done when independent final review passes with reproducible commands, exit codes and sanitized evidence, the shared-module audit passes, and remaining original UI, mixed-unit/multi-axis, grid capture and persistence obligations are explicit. No release image is promoted.
  - Complexity: every joined maintained module passes 400/300/50 with exact source scope; documentation/evidence-only changes are exempt. No new exceptions are authorized.
  - _Boundary: Controller integration of scope, breadth and acceptance evidence_
  - _Depends: 2.22_
  - _Requirements: 1.1, 1.4, 4.8, 4.9, 9.6, 10.1, 10.2, 10.3, 10.4, 10.5, 10.6_

Task 2.19 accepted at Workspace 8c12a9127cd913e5f6ebb8a9dfe3fd82ba56138f after independent Astra review. Fresh strict TypeScript, 46 foundation tests, repository-configured lint and the seven-module cap audit passed. Contracts are frozen for tasks 2.20 and 2.21. Evidence: artifacts/task-2.19/review/review.md. Runtime snapshot/mapping behavior remains pending.

Task 2.20 accepted at Workspace 616a0a70241fd15a10e0dc91dcec93cf701847ac after independent Sol review. Fresh 26 snapshot tests, strict TypeScript, actual repository lint and complexity evidence pass (110 physical, 122 logical, largest function 29). Evidence: artifacts/task-2.20/review/review.md. Mapper and browser integration remain separate gates.

Task 2.21 accepted at Workspace 59118937434b9f5a9bebd4e80bcb54f7ca2d552e after independent Astra review. Fresh 52 mapping tests, strict TypeScript and actual repository lint pass. Mapper metrics: 273 physical, 90 logical, largest function 15. Evidence: artifacts/task-2.21/review/verdict.md. Browser composition remains task 2.22; original renderer parity is unverified.

Task 2.22 accepted at Workspace 06fdb859bf426eb44dce13c54b21c494fcc244fd after independent Astra verification: 124 tests, strict TypeScript, build, scoped lint and three browser cases passed; CDP diagnostics are empty. Fresh PNGs show negative stacking, repeated categories and line gaps. Evidence: artifacts/task-2.22/review/review.md. Fixture animation is disabled to make image verification deterministic; original application parity remains unverified.

Task 2.23 accepted after independent Astra joined review and scoped GO for tasks 2.19-2.23 only. Fresh verification passed 124 tests, strict TypeScript, fixture build, all nine production module caps, twenty source/dependency identity checks, metadata and documentation links. Matching-source independent task 2.22 browser evidence supplies three passing cases with empty CDP diagnostics. See [snapshot verification](chart-snapshot-verification.md) and artifacts/task-2.23/review/verdict.md. Full renderer and release acceptance remain open.

## Original option-state slice (tasks 2.24-2.27)

Owner approved the option-state design and autonomous implementation on 2026-10-16. This scope supplements the existing task graph; other requirement coverage remains with existing tasks. Independent task review precedes execution. No renderer activation, theme projection or release acceptance is included.

- [x] 2.24 Freeze option-state contracts and captured editor fixtures
  - Implement the design's shared baseline, initialization/synchronization and column-event types, using existing mutable nested compatibility types and readonly outer fields. Preserve exact kind/value fields and null/undefined distinctions.
  - Freeze minimal independent synthetic expectations from seven original outgoing payloads with source/digest provenance; include supplied model/range and unrelated options needed for reducer composition. No private state is copied.
  - Verify existing unit/strict discovery, register the type module in controller-owned inventory and pass strict checks, existing units and independent contract review before releasing parallel lanes. Any compile-only test belongs to this task's explicitly owned optionStateContracts.types.ts.
  - Done when contracts and fixtures compile, captured values match original evidence and independent review approves the frozen boundary. Production caps 400/300/50 apply to the type module; fixtures/tests are excluded.
  - _Boundary: Shared optionStateTypes.ts, editorPayload.fixtures.ts and optionStateContracts.types.ts; controller inventory_
  - _Depends: 2.23_
  - _Requirements: 4.8, 4.9, 10.5_

- [x] 2.25 (P) Preserve original baseline selection and partition transitions
  - Implement initialization and synchronization with explicit prior state, validated fallback inputs, independent nested copies and captured address. Preserve empty-partition retention, nonempty partition clearing, original initial type ownership and no synchronization root fallback.
  - Test the design's complete fallback/transition matrix, null/undefined restrictions, malformed unused fallbacks, unknown fields, arrays and special property names, accessors, cycles, throwing inspection and mutation isolation. Errors do not throw or change prior state.
  - Done when focused tests, strict checks, scoped lint and independent review pass without store, React, GridApi or renderer imports. Whole maintained module passes 400/300/50 with registered scope before acceptance.
  - _Boundary: optionState.ts and optionState.test.ts only_
  - _Depends: 2.24_
  - _Requirements: 4.8, 4.9_

- [x] 2.26 (P) Map column editor events and verify original reducer composition
  - Implement typed title-text/title-enabled, legend-position and stroke-width patches for grouped/stacked columns. Preserve separate text/enabled meaning and exact bar paths; reject invalid input and unsupported families without partial patches.
  - Test all contract value domains, captured title/bottom/width-four cases, independent outputs and malformed events. Record source corroboration for contract value domains without claiming each was browser-captured.
  - Compose with unchanged integrated reducer using complete supplied baseline and patch; compose with detached reducer using a cloned complete event-options object merged with the patch. Verify unrelated options, root-only theme stripping, null/undefined/array behavior, supplied destination range, state-key collisions and bar retention through grouped/stacked/line storage changes.
  - This lane uses frozen fixtures rather than importing the pending baseline implementation; joined baseline-to-editor composition belongs to 2.27.
  - Done when focused tests, strict checks, scoped lint and independent review pass. Whole maintained module passes 400/300/50 before acceptance; no production UI/guard/reducer changes.
  - _Boundary: editorEvents.ts and editorEvents.test.ts only_
  - _Depends: 2.24_
  - _Requirements: 4.8, 4.9_

- [x] 2.27 Verify and accept the joined option-state boundary
  - Add explicit integration cases to editorEvents.test.ts after both lanes freeze: actual baseline selection -> actual event mapper -> accepted reducers. Verify successive edits, partition transition, supplied family change and detached replacement with independent expected values.
  - Run fresh complete chart units, strict TypeScript, scoped lint, full registered chart-module complexity audit and exact source/dependency identity checks. No new browser acceptance claim: renderer code is unchanged, original runtime parity remains unverified.
  - Update actual test paths/evidence, inventory, source pin and scoped verification report; selectively commit accepted changes while preserving unrelated work. Done when independent final review verifies the joined contract and honest remaining gaps, with reproducible commands and exit codes.
  - Production caps 400/300/50 apply to all three new modules and the shared registered audit; docs/tests excluded. Controller serializes shared inventory, builds/check queue and commits. No release promotion.
  - _Boundary: Explicit integration tests after lane freeze; controller inventory, breadth, source and evidence records_
  - _Depends: 2.25, 2.26_
  - _Requirements: 1.1, 4.8, 4.9, 10.4, 10.5, 10.6_

### Lane ownership and execution prerequisites

Frontend paths are under vendor/workspace/terminalpro/src/components/General/Table/Chart/compatibility or tests/unit/chart-compatibility as specified in the design. Existing WSL pinned Node and restored dependencies are prerequisites already accepted by earlier tasks; no install or lock change is needed. Controller may copy the required source/tests to a fresh isolated stage with the restored node_modules link for reliable Linux checks. One heavy check at a time, one Vitest worker; lightweight independent lane checks must use separate outputs. Shared contracts/fixtures freeze at 2.24. Sol implementers own 2.25 and 2.26 separately, followed by fresh independent reviewers. Astra reviews shared contracts and the final join. A lane cannot change shared interfaces or its peer's files; escalate to controller. Controller owns registration and selective fork/root commits at each acceptance. Task approval follows the owner's explicit autonomous implementation request, without waiving any review gate.

Task 2.24 accepted after independent Astra review: shared contracts and captured projections verified, 124 units, strict TypeScript, scoped lint and registered complexity checks passed. Evidence: artifacts/task-2.24/review/review.md. Contracts and fixtures are frozen for tasks 2.25 and 2.26.

Task 2.25 accepted after independent Astra review: 39 focused tests, strict TypeScript, repository lint and eight adversarial cases passed. Caps: 200 physical, 96 logical, largest function 14. Evidence: artifacts/task-2.25/review/review.md. Actual reducer integration remains task 2.27.

Task 2.26 accepted after independent Sol review: 53 focused editor/composition tests, strict TypeScript, actual repository lint and registered caps passed. Evidence: artifacts/task-2.26/review/review.md. Joined baseline integration and broader renderer parity remain separate gates.

Task 2.27 accepted at Workspace 5c2df9864bed000170ffccde146273b468e0552e after independent Astra final review: scoped GO for 2.24-2.27, completion VERIFIED, fresh 221 units, strict TypeScript, scoped lint, twelve-module caps and 42 source/dependency identities passed. Evidence: artifacts/task-2.27/review/review.md and [option-state verification](chart-option-state-verification.md). Full renderer, browser parity and persistence remain unverified.

## Explicit Cartesian appearance slice (tasks 2.28-2.33)

The owner approved [explicit appearance](chart-appearance-design.md). These tasks supplement existing requirement coverage; they do not activate application controls or complete renderer parity. The owner approved tasks 2.28-2.33 on 2026-10-17. Each leaf is a bounded 1-3 hour work unit with independent review before acceptance.

### Execution and ownership

Freeze the shared contracts and fixtures in 2.28, then run 2.29 and 2.30 concurrently with separate Sol workers. Join serially in 2.31, verify actual browser outcomes in 2.32, and accept joined evidence in 2.33. Astra reviews contracts, numerical continuity and final acceptance; a fresh independent Sol reviewer can review fixture scaffolding. At most controller, two workers and one reviewer. Do not modify a peer's files; shared contract changes stop both lanes for controller review.

Paths below are relative to `vendor/workspace/terminalpro/`. Production files live under `src/components/General/Table/Chart/echarts/`; unit paths under `tests/unit/chart-compatibility/`; browser paths under `tests/e2e/chart-compatibility/`. Controller alone owns root inventory, breadth, source pins, documentation and selective commits. Preserve unrelated working-tree changes. No package/lock changes, new dependencies, application flags, provider calls, AG runtime imports or renderer activation.

Reuse the accepted pinned WSL Node, restored dependencies and isolated staging pattern from tasks 2.24-2.27. Before dispatch, controller checks actual tool/dependency identities and existing unit, strict, fixture build and browser entry points; missing runtime setup must be repaired before dependent work. From the frontend root: `node node_modules/vitest/vitest.mjs run --config tests/unit/chart-compatibility/vitest.config.mjs`, `node node_modules/typescript/bin/tsc --project tests/unit/chart-compatibility/tsconfig.json --noEmit`, and `node node_modules/vite/bin/vite.js build --config tests/e2e/chart-compatibility/vite.config.ts`. Browser verification uses root verification Playwright with the existing chart config and pinned cache. Actual repository Biome configuration and the [combined complexity checker](../../../docs/complexity.md) remain authoritative.

One heavy suite/build at a time; one browser and Vitest worker. Parallel lightweight checks require separate stages and output directories. Browser/CDP sessions are owned, hidden and headless with sanitized evidence and finally cleanup. All maintained new/modified production files pass 400 physical lines, 300 logical units and 50/function as whole files; tests and documentation are recorded exclusions. No new exceptions. Register newly created production files before acceptance, using truthful fork manifests. Foundation checker/inventory tasks are already accepted; this slice extends their scope.

- [x] 2.28 Freeze explicit appearance contracts and financial fixtures
  - Add the approved optional title, typography, line and per-series fields and the exact style-validation/projection result types. Preserve existing signatures and valid legacy inputs; freeze helper exports before either lane starts.
  - Add homogeneous-unit, same-scale four-observation fixtures with an interior null, independent expected appearance values and provenance distinguishing original UI observations from synthetic fallback rules. Include palette reorder and nonempty/empty retained titles.
  - Add compile-time positive/negative cases; verify existing discovery includes the new fixtures and existing 221 units remain green. Done when strict checks, scoped lint, whole-file caps and independent Astra contract review pass and fixtures/signatures are frozen.
  - _Boundary: cartesianTypes.ts; appearance.fixtures.ts; snapshotContracts.types.ts; controller inventory_
  - _Depends: 2.27_
  - _Requirements: 4.8, 4.9, 10.5, 10.6_

- [x] 2.29 (P) Validate and project explicit appearance
  - Extract existing style validation into the approved cohesive style module and implement typed caption/series projection. Do not edit or wire the numerical mapper in this lane.
  - Cover omitted/undefined/null optional inputs, complete typography with finite nonnegative sizes, title visibility requiring retained text, malformed inactive settings and unsupported active enabled marker shapes. Exercise every fill/stroke/marker precedence branch, zero/fractional dimensions and ID-bound overrides after reorder.
  - Add focused helper tests to the owned Cartesian test file while retaining existing mapper assertions. Verify legacy projection shapes, unchanged inputs and inactive-family omission. Done when focused tests, strict checks, actual lint and independent review pass; register the new style module and pass 400/300/50 before acceptance.
  - _Boundary: cartesianStyle.ts and cartesian.test.ts only_
  - _Depends: 2.28_
  - _Requirements: 4.8, 4.9_

- [x] 2.30 (P) Build the isolated appearance journey fixture
  - Build fixture-only controls and diagnostics around the existing real mapper and accepted host using frozen style inputs. Maintain monotonic render revisions independently of the unchanged data revision; rejected input preserves the last good render.
  - Scaffold observable outcomes for line connection, marker toggle, retained title, distinct caption typography/colors, family roundtrip, resize, export and invalid/unsupported recovery. Capture real options and rendered output without importing unfinished style helpers or copying mapper logic.
  - Register the added HTML entry in the existing Vite/Playwright configuration without changing previous fixtures or worker bounds. Done when fixture build and applicable type/lint checks pass and independent review confirms the controls and lifecycle seam. New appearance behavior remains explicitly unverified until mapper integration; do not weaken assertions or claim the old mapper implements it.
  - Applicable maintained configuration passes whole-file caps; browser fixtures/tests are documented exclusions. Shared build execution is controller-serialized.
  - _Boundary: appearance.html, appearance.tsx and existing browser Vite/Playwright configuration only_
  - _Depends: 2.28_
  - _Requirements: 4.8, 4.9, 10.1, 10.2, 10.4_

- [x] 2.31 Integrate appearance without changing observations
  - After both lanes freeze, delegate mapper style validation/projection to the reviewed module. Keep family/source-mode, unit/scale, stable-ID, exact values, ordering, escaping, display precision and stacking semantics intact.
  - Extend mapper integration assertions for all three families, legacy exact option shape, explicit marker colors/widths, title retention, caption fonts and palette selection after reorder. Invalid/unsupported style produces no partial options. Verify null arrays are identical in both connect states and input objects remain unchanged.
  - Done when all existing 221 units plus new helper/integration cases, strict checks, actual lint and independent Astra numerical review pass. Both modified mapper and style module remain within whole-file 400/300/50; no forwarding-only split or compressed code.
  - _Boundary: Explicit integration of cartesian.ts with cartesianStyle.ts; cartesian.test.ts after lane freeze_
  - _Depends: 2.29, 2.30_
  - _Requirements: 4.8, 4.9, 10.5, 10.6_

- [x] 2.32 Verify visible appearance and recovery in the real browser
  - Add the actual Playwright journey against the freshly built real mapper/host fixture. Assert connected versus broken null gaps, circle counts/positions with no null marker, title hide/re-enable retaining text, distinct colors/typography, columns-to-line replacement, resize and exported pixels alongside exact option/data assertions.
  - Verify appearance-only revisions at unchanged data revision, invalid/unsupported inputs retaining the last good chart and valid correction recovering. Do not substitute DOM labels, a toast or option equality alone for rendered outcome checks.
  - Run existing smoke, lifecycle and Cartesian browser cases as regressions in the same owned one-worker environment. Record commands, source/dependency identities, exit codes, screenshots/export checks and sanitized CDP errors. Done when independent review reproduces the journey and confirms visible outcomes and cleanup. Failures are diagnosed before rerun.
  - Tests/fixtures are excluded from production caps; any production fix returns to its owning task and review. Original screenshots support selected semantics only, not full light/dark pixel parity or application acceptance.
  - _Boundary: appearance.spec.ts and fixture corrections in appearance.tsx after scaffold freeze_
  - _Depends: 2.31_
  - _Requirements: 4.8, 4.9, 10.1, 10.2, 10.3, 10.4_

- [x] 2.33 Accept the joined appearance boundary
  - Verify exact joined source/dependency identities, fresh units, strict checks, scoped lint and all registered chart-module caps. Reuse independently reproduced browser evidence only when identities match; rerun affected checks after any source change.
  - Audit scope for unintended application, reducer, snapshot, host, flag, dependency, provider or persistence changes. Update actual breadth paths/evidence, inventory, source pins and a scoped verification report, preserving overall renderer parity as unverified.
  - Done when independent Astra final review passes with reproducible evidence and explicit remaining theme/default, formatting, original-control and application integration gaps. Selectively commit accepted changes; no release image promotion. Whole maintained scope passes 400/300/50; documentation/evidence paths are exempt.
  - _Boundary: Controller integration of scope, identity, breadth and acceptance records_
  - _Depends: 2.32_
  - _Requirements: 1.1, 4.8, 4.9, 10.4, 10.5, 10.6_

Task 2.28 accepted after independent Astra review: strict TypeScript, 221 units, actual lint on all three owned files, exact stage/source identities and twelve-module caps passed. Evidence: artifacts/task-2.28/review/review.md. Shared appearance contracts and fixtures are frozen for tasks 2.29 and 2.30; runtime appearance remains unverified.

Task 2.30 accepted after independent Sol review: strict TypeScript, four-entry fixture build, actual lint and four source/stage identities passed. Evidence: artifacts/task-2.30/review/review.md. Scaffold only; actual appearance rendering remains task 2.32. Verification stages now use persistent Linux home storage after transient WSL paths disappeared.

Task 2.29 accepted after independent Astra review: 250 units, strict TypeScript, actual lint, exact hashes and thirteen-module caps passed. Evidence: artifacts/task-2.29/review/review.md. Helper projection is accepted; mapper wiring and rendered appearance remain tasks 2.31-2.32.

Task 2.31 accepted after independent Astra numerical review: 260 units, strict TypeScript, actual lint, all thirteen module identities/caps and owned stage hashes passed. Evidence: artifacts/task-2.31/review/review.md. Mapper appearance is integrated; actual rendered outcome acceptance remains task 2.32.

Task 2.32 accepted after independent Astra browser review: fresh build, all four browser cases, 260 units, strict TypeScript and actual lint passed; exact source/dependency identities, empty CDP diagnostics and owned cleanup verified. Evidence: artifacts/task-2.32/review/review.md. Pixel evidence covers gaps, circles, retained titles, typography, family restoration, export and rejected-render recovery. Full application parity remains open.

Task 2.33 accepted after independent Astra final review: scoped GO and VERIFIED completion for tasks 2.28-2.33. Fresh 260 units, strict TypeScript, actual lint, thirteen-module caps, 47 identities and combined 67-file quality checks passed; matching-source independent browser evidence covers four cases with empty CDP diagnostics. Workspace b96d36d16ba87db2dd595d5796507d473dd0c0c6. See [appearance verification](chart-appearance-verification.md) and artifacts/task-2.33/review/review.md. Overall renderer and release remain unverified.

## Approved design slice: source-safe chart application contracts

The owner approved the [application integration design](chart-application-integration-design.md) on 2026-10-17. Tasks 2.34-2.37 passed independent task-graph review and received owner implementation approval on 2026-10-17. This branch starts after accepted 1.4/2.33 regardless of numeric position; it does not wait for blocked renderer or dashboard joins. Full application task coverage remains incomplete at the explicit gates below. [Independent review](../../../artifacts/reviewed/chart-integration-task-review/review.md).

- [x] 2.34 Freeze source-safe application contracts and executable test scope
  - Controller task, 1-3 hours. Reconcile exact current bytes with the approved design and original source pin `38dffc33389aca0e4a87e0e88d42f7067aa220df`; record actual HEAD plus explicit changed-file manifests and hashes, separating unrelated dirty changes from this slice.
  - Define the design's address/stamp/result, resolved range, column command and display-policy types in `Chart/application/types.ts`, importing accepted legacy/snapshot/option-state types. Keep canonical `CaptureDisplayedChart -> SessionResult<ResolvedSnapshotInput>` only; do not implement capture. Freeze explicit A1 range/session callable inputs/outputs against the source contracts and existing reducer, including ownership of range writes separately from option patches. Freeze B1 callback inputs against the formatting source contract. No guessed category, GridApi invocation, appearance, React session or editor API is admitted.
  - Add compile-time contracts in `tests/unit/chart-application/contracts.types.ts`, a strict `tsconfig.json` and one-worker `vitest.config.mjs` in that directory, reusing the accepted chart compatibility setup. Include both new application tests and existing compatibility tests in the explicit joined commands below. Do not edit the existing shared compatibility configurations during worker fan-out.
  - Controller adds only new owned maintained paths to `.kiro/complexity-budgets.json` and keeps new breadth checks planned/unverified. Reuse accepted 1.3/1.4 checker foundations. Preserve existing concurrent inventory/breadth edits and review their diff separately.
  - Done when independent review verifies source-supported callable contracts and exclusive ownership; strict compile and scoped lint pass, and the explicit current manifest gate measures whole modified maintained files at 400 physical lines/file, 300 logical units/file and 50/function. Record commands, exits, source hashes and config hashes before A1/B1 dispatch; tests/evidence are documented exclusions.
  - _Boundary: Controller shared contract freeze, new application test configuration and scope registration_
  - _Depends: 1.4, 2.33_
  - _Requirements: 1.1, 4.8, 4.9, 10.4, 10.5, 10.6_

- [x] 2.35 (P) Preserve source range precedence and addressed chart session updates
  - A1 task, 1-3 hours; exclusive writes `Chart/application/chartRange.ts`, `sessionState.ts`, `tests/unit/chart-application/chartRange.test.ts` and `sessionState.test.ts`. Consume 2.34's frozen types/configuration; shared types, existing reducers, contexts, grid callers and mapper are read-only.
  - Resolve eligible stored range, configured columns and generated visible columns in original precedence, honoring ignoreCellRange, the stored more-than-one-column condition, configured empty fallback diagnostics, generated-column intersection and selected-ID order. Preserve ordinary stored row bounds and original JSON without mutation. Do not infer category, raw grid values, aggregation or detached transformations.
  - Validate address/stamps and use accepted option baseline/editor/reducer semantics against the latest supplied storage. Reject stale widget/key/generation/render revision without writes; keep ephemeral counters out of storage. Preserve inactive-family/unknown state, populated-to-empty baseline behavior and root-theme stripping. Keep range transition writes separate from options reduction. Counter overflow invalidates the session; no old token is reused.
  - Done when focused regressions assert exact outputs and input immutability for these transitions, including two widget IDs sharing a stateKey, delayed edits, partition changes, destination-model inputs and separately persisted cellRange. No React activation or chart guard removal occurs; D must later consume these modules before application acceptance.
  - Run focused units, strict compile and scoped lint using the commands below; independent review and fresh verification must pass. Whole owned production files pass 400 physical/300 logical/50 per-function with the actual current manifest; record measured counts and identities. Request controller contract review if work exceeds this boundary.
  - _Boundary: A1 pure source range and session state adapters_
  - _Depends: 2.34_
  - _Requirements: 4.2, 4.7, 4.8, 4.9, 10.5, 10.6_

- [x] 2.36 (P) Preserve owned financial display callbacks without changing observations
  - B1 task, 1-3 hours; exclusive writes `Chart/application/financialFormatting.ts` and `tests/unit/chart-application/financialFormatting.test.ts`. Consume frozen 2.34 contracts and existing numeric/fiscal helpers. Existing source helpers, mapper, RuntimeOptions, shared configuration and A1 paths remain read-only.
  - Derive typed category, axis, crosshair, legend, series-label and tooltip-number display policies from explicit current period, widget/global precision, column definitions and the source Index formatter contract. Retain zero precision and callback regeneration; never persist functions or replace the data-only RuntimeOptions type.
  - Assert strict +/-1,000,000 boundaries and outside values, magnitude precisions 2/0, series precision 0, current tooltip precision, zero/negative/fractional values and existing nonfinite helper behavior. Preserve date-only/recognized datetime/Date-object, midnight/non-midnight, quarter/year and column-versus-line/legend differences. Expected strings follow the pinned source helpers, not new locale rules.
  - Keep integrated values unchanged; do not apply detached normalizedPercent rescaling or infer currency/prefix/suffix propagation. Test callbacks directly with explicit inputs. AG callback selection, invocation, multiple-tooltip ordering/layout/null behavior and mapper call-site replacement remain blocked joins.
  - Done when source-based expected-string regressions, input immutability, strict compile, scoped lint, independent financial review and fresh verification pass. Whole owned production file passes 400 physical/300 logical/50 per-function with actual manifest evidence; no invocation or application parity claim is made.
  - _Boundary: B1 pure financial display policies_
  - _Depends: 2.34_
  - _Requirements: 4.8, 4.9, 10.5, 10.6_

- [x] 2.37 Verify and accept the joined source-safe application boundary
  - Explicit controller integration task, 1-3 hours. Freeze A1/B1 worker edits, inspect their combined diff and independently reproduce all new units plus existing chart compatibility units, strict checks, scoped lint and whole-file complexity against exact joined bytes. No browser/build/runtime activation is part of this gate.
  - Audit accepted reducer/mapper/snapshot/host behavior and original feature flags for unintended changes; prove A1/B1 share the frozen contracts without creating a second storage owner. Maintain source hashes and the explicit changed-file manifests, retaining unrelated dirty work outside accepted ownership.
  - Done when independent Astra review accepts only the source-safe contracts/helpers, with actual test IDs, commands/exits, size evidence and reviewed sanitized artifacts; controller updates breadth/inventory/source records selectively. Mark actual helper checks verified while application, capture, effective appearance, editor, export and save/restart remain unverified.
  - Whole modified maintained production scope, including shared types/configuration and controller helpers if any, passes 400 physical/300 logical/50 per-function; tests and evidence are documented exclusions. No release image promotion and no implicit permission for A2/B2/C/D follows acceptance.
  - _Boundary: Controller integration of A1/B1 contracts, identity and evidence_
  - _Depends: 2.35, 2.36_
  - _Requirements: 1.1, 4.8, 4.9, 10.4, 10.5, 10.6_

### Check commands and setup contract for 2.34-2.37

Run in an isolated WSL/Linux source stage with pinned Node 24.22.0 and the accepted locked dependency tree, following the exercised `artifacts/task-2.33/check.sh` staging pattern. Controller snapshots exact dirty source bytes into the stage and hashes them; never archive HEAD alone and silently omit dirty inputs. Serialize any dependency restoration; no new install is assumed. Resolve `$QBB_STAGE` and `$QBB_ROOT` explicitly before execution and record their real paths. The first task creates the new config files; these are planned checks until exercised, not currently passing commands.

From `$QBB_STAGE/terminalpro`:

```sh
node node_modules/typescript/bin/tsc --project tests/unit/chart-application/tsconfig.json --noEmit
node node_modules/typescript/bin/tsc --project tests/unit/chart-compatibility/tsconfig.json --noEmit
node node_modules/vitest/vitest.mjs run --config tests/unit/chart-application/vitest.config.mjs
node node_modules/vitest/vitest.mjs run --config tests/unit/chart-compatibility/vitest.config.mjs
node node_modules/@biomejs/biome/bin/biome check src/components/General/Table/Chart/application tests/unit/chart-application
```

For A1 or B1 focus, append the actual owned test paths to the new Vitest command. Its include pattern must discover the new tests and maxWorkers must be 1; strict config includes new application source/tests and imported accepted contracts. No write/fix lint option. No empty/skipped-suite acceptance. Before joins, inspect test counts and exact discovered test paths rather than treating exit 0 alone as evidence.

From `$QBB_ROOT`, using controller-produced current manifests for both forks:

```sh
pipeline/.venv/bin/python -m tools.quality.complexity --check --changes workspace=artifacts/chart-application-implementation/workspace-changes.json --changes data_api=artifacts/chart-application-implementation/data-api-changes.json --output artifacts/chart-application-implementation/complexity.json
```

The controller creates these manifests before checking: exact inventory-approved repository/base, actual snapshot identity and complete changed-file entries; unchanged data API receives an explicit empty manifest only if the actual scope warrants it. Dirty inventory/catalog/renderer files may be measured by the repository gate but their unrelated work is not accepted by this slice. A cap failure outside the slice is reported to its owner, not repaired or excluded silently. Preserve source/stage hashes, commands, exits and exclusions with evidence. Review and publish only completed sanitized evidence under `artifacts/reviewed/` before selective commit/push.

## Approved design slice: ordinary displayed-grid capture

The owner approved [the bounded capture design](chart-grid-capture-design.md) after independent runtime/design review. The owner approved tasks 2.38-2.40 for implementation after independent task-graph review. Tasks 2.34-2.37 and the complexity/checker foundations are already accepted. This branch depends on those tasks, not on unfinished earlier numerical renderer entries. A2 completion alone does not unblock mapper/editor/application activation, renderer-complete images or delivery.

The three leaves are sequential because the real-grid setup, adapter and integrated tests share a fixture and configuration. No (P) marker applies. A Sol worker handles each bounded implementation leaf; fresh independent review follows each leaf, with Astra for financial capture and the final join. Controller owns shared test configuration, inventory, source pins, evidence publication and commits. Disjoint appearance/editor research may overlap, with one heavy suite/browser/build at a time; it grants no implementation permission for those lanes.

All paths below are relative to vendor/workspace/terminalpro unless explicitly rooted. Frozen application/types.ts, accepted session/range/snapshot behavior, mapper, host, UI and flags remain read-only. No new package, enterprise module, renderer activation or saved-state owner is introduced.

- [x] 2.38 Freeze the ordinary-grid fixture and exercise the real Community API
  - Foundation task, 1-3 hours. Own tests/unit/chart-application/gridCapture.fixtures.json and gridCapture.grid.test.ts; controller alone owns the narrowly scoped application tsconfig.json extension for resolveJsonModule. Reuse the existing jsdom/maxWorkers:1 configuration and existing actual Community grid test pattern; do not import root vitest.setup.ts or tests/mocks/ag-grid, which would replace the real API.
  - Translate only the admitted finite synthetic rows, expected financial arrays, selected IDs and range into the self-contained fixture. Record original reference source/image and per-input hashes separately from current candidate identity. Keep normalized-percent and getter experiments explicitly labelled; arbitrary getter configuration, mixed-unit mapping and category inference are not accepted by these fixtures.
  - Use the locked Community modules and typed real GridApi, with only necessary DOM environment shims. AllCommunityModule provides getCellValue and client-row-model/filter/sort/column APIs. Wait for observable model completion, assert actual IDs/order and unformatted values, then destroy the grid and remove the owned host. No GridApi mock or enterprise registration may satisfy this setup gate.
  - Done when executable fixture/setup checks pass for real flat rows, sorting/filtering, stable duplicate-label identities and raw-versus-unformatted getter/formatter values using the current locked environment. Tests must run without the not-yet-created capture adapter; there is no skipped or empty-suite acceptance. Freeze fixture/configuration hashes for 2.39 after independent review and fresh verification.
  - Complexity: tests/fixture and test-only configuration are documented exclusions. Reuse accepted inventory/checker tasks 1.3/1.4; any unexpected maintained production setup change returns to controller review and must meet 400 physical/300 logical/50 per function. No implicit dependency upgrade or broad compiler relaxation.
  - _Boundary: Actual Community grid verification environment and finite reference fixture_
  - _Depends: 1.4, 2.37_
  - _Requirements: 1.1, 4.8, 4.9, 10.4, 10.5, 10.6_

- [x] 2.39 Capture resolved ordinary observations without changing their meaning
  - Core task, 1-3 hours. Own src/components/General/Table/Chart/application/gridCapture.ts, tests/unit/chart-application/gridCapture.test.ts and the adapter integration additions to gridCapture.grid.test.ts. Consume the accepted fixture/configuration and frozen CaptureDisplayedChart contract; request controller review rather than editing shared types or existing helpers.
  - Consume caller-resolved category/descriptors and ordered range unchanged. Read displayed indices within inclusive valid bounds and use unformatted public grid values. Preserve node IDs, duplicate category labels, numeric zero/negative/fraction/null, supplied units/scale and resolved series order. Never infer category roles, re-filter visibility, parse displayed percentage text, rescale observations or fall back to raw node.data. Test A1 visible-range resolution followed by A2 capture as an explicit seam.
  - Construct the existing flat snapshot from supplied address/data revision, model and original range provenance through the accepted snapshot validator. Preserve input and metadata immutability and return the original captured stamp. Caller pre/post current-stamp validation remains external; do not claim this input can detect a newer generation or caller-owned transpose metadata.
  - Cover destroyed/unready API versus ready-empty rows, malformed input, partial/reversed/out-of-count bounds, missing/duplicate IDs, undefined/nonfinite/unhandled values and bounded API failures. Detectable non-client-side/group/pivot/pinned cases receive diagnostics without importing enterprise modules. Bounds and unsupported-value policies are the approved conservative internal contract, not claims about unobserved original clipping or product behavior.
  - Write meaningful failing regressions before implementation without a feature flag. Done when focused unit and actual-grid integration tests match independent original fixture expectations, waiting/invalid/unresolved behavior and no-write/no-mutation guarantees, with both strict compilers and scoped lint passing. Numeric-only synthetic category, general multiple-category rules, transformed/aggregated/remote paths and UI invocation remain unverified.
  - Complexity: controller registers gridCapture.ts before its acceptance. Its whole maintained file passes 400 physical lines, 300 logical units and 50 per function using the implemented checker and actual current fork manifests. Tests/evidence are explicit exclusions; no new size exception or additional production helper ownership is assumed. Independent Astra review and fresh verification are required.
  - _Boundary: Pure ordinary GridApi-to-snapshot capture adapter_
  - _Depends: 2.38_
  - _Requirements: 1.1, 4.2, 4.7, 4.8, 4.9, 10.4, 10.5, 10.6_

- [x] 2.40 Independently verify the joined ordinary capture boundary
  - Explicit controller integration task, 1-3 hours. Freeze worker edits and reproduce all chart-application and chart-compatibility units, both strict compilers, scoped lint, exact source/config/test identities and whole maintained complexity using current manifests for both forks. Compare the accepted fixture values to actual GridApi and capture outputs; no browser/build/application activation is part of this gate.
  - Audit the actual diff for unchanged frozen types, accepted range/session/reducer/snapshot/mapper/host behavior, UI and flags. Confirm the adapter owns no persisted storage or lifecycle and the A1/A2 visibility/ordering seam preserves exact financial observations. Keep unrelated dirty catalog/renderer work outside acceptance and selective staging.
  - Done when a fresh independent Astra review accepts tasks 2.38-2.40 only, with real-grid tests discovered and no skips, exact commands/exits/hashes, actual breadth test paths and inventory/source pins aligned. Publish only completed reviewed evidence with source/published hashes before explicit commit/push; do not reuse original-runtime research as candidate application proof.
  - Complexity: entire modified maintained scope passes 400 physical/300 logical/50 per function with unchanged-byte exception validation where applicable; tests/evidence/test-only configuration remain declared exclusions. Retain the actual maintained file count and test count rather than assuming the historical baseline counts are current.
  - No full application, effective appearance, editor, export, save/restart, renderer, image or release acceptance follows this helper gate. Blocked followups below remain binding; no hidden menu, flag or unavailable fallback is authorized.
  - _Boundary: Controller A2 verification, scope inventory and evidence join_
  - _Depends: 2.39_
  - _Requirements: 1.1, 4.2, 4.7, 4.8, 4.9, 10.4, 10.5, 10.6_

### Verification setup and commands for 2.38-2.40

Use a fresh isolated WSL/Linux stage, not a stale task237 archive. Existing pinned Node is 24.22.0, and the accepted dependency tree is /home/mc/qopenbb-work/appearance-deps/terminalpro/node_modules. Read-only prerequisite inspection found AG Grid Community/React 34.1.1, Vitest 4.1.11, jsdom 30.0.1 and application TypeScript 5.9.2; quality tooling separately uses TypeScript 6.0.3. No installation or upgrade is assumed. If the accepted tree is unavailable, restore only through the existing locked protected workflow and record actual identities before acceptance.

The application config already discovers gridCapture.grid.test.ts, uses jsdom and maxWorkers:1, and has no global setupFiles. The controller-owned resolveJsonModule setting is application-only; compatibility compiler settings remain unchanged. Reuse the environment pattern from tests/unit/communityRealGrid.test.tsx, not its broad any types or mocks. Keep any DOM shims local to the owned grid test, clean up global mutations, and never replace the public methods being verified. Unexpected setup scope returns to controller review.

Snapshot exact current fork bytes into the stage, including uncommitted owned inputs, and retain a source/stage hash manifest. Run from its terminalpro directory:

```sh
node node_modules/typescript/bin/tsc --project tests/unit/chart-application/tsconfig.json --noEmit
node node_modules/typescript/bin/tsc --project tests/unit/chart-compatibility/tsconfig.json --noEmit
node node_modules/vitest/vitest.mjs run --config tests/unit/chart-application/vitest.config.mjs
node node_modules/vitest/vitest.mjs run --config tests/unit/chart-compatibility/vitest.config.mjs
node node_modules/@biomejs/biome/bin/biome check src/components/General/Table/Chart/application tests/unit/chart-application
```

For focused setup/adapter verification, append the actual owned test paths to the application Vitest command; inspect discovered tests and skip counts. Before 2.39 there is no import of the absent adapter. The existing 36 application and 260 compatibility tests are a historical baseline, not proof that future tests passed.

The controller creates current workspace/data_api manifests with correct repository/base/head and complete changed-file entries, preserving unrelated dirty inputs measured by the full gate. From the root with pinned Node on PATH:

```sh
pipeline/.venv/bin/python -m tools.quality.complexity --check --changes workspace=artifacts/grid-capture-implementation/workspace-changes.json --changes data_api=artifacts/grid-capture-implementation/data-api-changes.json --output artifacts/grid-capture-implementation/complexity.json
```

These future manifest paths are task outputs, not existing evidence. Update inventory/source pins together and validate existing exception targets are unchanged before rebinding their revision. No new production-only environment or service is required. Core product.md/tech.md/structure.md remain absent as recorded in the parent specification; the specialized steering and approved requirements/design govern this plan.

### Blocked application followups

These are explicit return-to-design/task gates, not numbered implementation tasks or fulfilled design coverage:

| Component/join | Required frozen input before a bounded task can be approved |
| --- | --- |
| A2 gridCapture | Explicit-category flat capture is independently accepted through tasks 2.38-2.40; see chart-grid-capture-verification.md. The canonical typed signature is unchanged. Numeric-only synthetic categories, general multiple-category resolution, arbitrary getter configuration, hidden-after-entry and remote/transformed cases retain separate missing evidence. |
| B2 effectiveAppearance | Typed AppearanceInput/Result, finite admitted stock/custom leaves and explicit per-leaf precedence. Six stock defaults/two custom grouped-column observations do not establish arbitrary inheritance. |
| Mapper | Reviewed A2/B1/B2 outputs; actual formatter invocation, category binding, tooltip mode/null/order/layout and explicit effective-leaf projections. Unknown/mixed-unit semantics remain a separate reviewed parity join. |
| C docked editor | Flattened visible/conditional per-field ledger, value domains, exact namespaces/events/effects, props/events and bounded family/group ownership. Four column patches do not complete the editor. |
| D application composition | Exact ChartSessionInput/ChartSession/editor contracts; independently accepted A1/A2/B1/B2 and mapper; measured useUpdateColumnState.ts disposition. Exclusive paths from the design; actual A1/B1 consumption required. |
| Real-app milestone | Reviewed C/D and SQLite; actual financial rows/arrays, original docked journey, theme/export/table restoration and explicit save/reopen/restart, error recovery and cleanup. Unreleased milestone remains distinct from complete renderer parity. |
| Remaining release scope | Other families, detached/AI charts, entity theme preview, aggregated/pivot/transpose/remote and advanced table paths retain capability-matrix obligations and separately scoped joins. No product/menu/flag reduction. |

The completed runtime retry proves one finite initial projection and zero nested edits/saves; exit 1 and cleanup 0 remain recorded. It supplies no missing event, range or formatter seam. The controller must return affected boundaries to design/contract freeze and obtain bounded reviewed tasks before dispatch; no missing signature is invented here. Anthropic 5.5 acceptance still precedes every Excel implementation step.

## Approved design slice: appearance composition and tooltip source contracts

The owner approved [the appearance/editor amendment](chart-appearance-editor-integration-design.md) and tasks 2.41-2.45 for implementation. They preserve the original UX obligation and do not activate B2, the mapper, C/D, transformed snapshots or new product restrictions. Existing completed tasks and the parent plan's coverage of all 69 requirements remain unchanged. Candidate baseline is Workspace `76edf85a46298f7bc5212ff9944e4b66e9baa4af`; actual owned bytes are frozen in the task evidence.

- [x] 2.41 Freeze appearance contracts, reference fixtures and executable verification scope
  - Accepted: independent APPROVED/VERIFIED review in `artifacts/reviewed/task-2.41/review/verdict.md`; both strict compilers, 88 application/260 compatibility tests, scoped lint and 174-file complexity audit pass. Historical failed attempt remains disclosed. Contracts and fixtures are frozen; runtime helpers remain pending.
  - Define the approved composition and color token/result types without runtime stubs. Freeze their exact signatures and fixture hashes for workers; retain the existing option baseline, validation, session and reducer types as dependencies.
  - Derive small data-only expected fixtures from the reviewed saved-input and normalized-color evidence. Record original source/image provenance and distinguish observed winners from proposed invalid-input policy. Keep saved options deliberately different from model.chartOptions so operand mistakes fail tests.
  - Verify existing application/compatibility configs discover new appearance tests and compile-only type fixtures without global mocks; no config change is expected. Snapshot a fresh isolated WSL stage, record Node/dependency/source identities and exercise both existing suites/strict checks before work fans out. Do not import absent implementations or add placeholder production functions.
  - Register the new contracts file in the maintained inventory and confirm existing event/session ownership. Freeze a planned path list for the two implementation files; the checker rejects absent mapped files, so the controller adds each inventory entry only when its worker introduces that file, before its acceptance check. Retain unrelated inventory edits and document test/fixture exclusions. Prepare explicit current workspace/data_api change manifests; preserve exact exception target bytes.
  - Done: independent review accepts the frozen types, finite fixtures, test discovery, passing baseline commands and complete staged identities. New type file and modified maintained configurations pass 400 physical/300 logical units per file and 50/function where applicable; test/fixture files are explicitly excluded. No new exception or dependency upgrade.
  - _Boundary: Controller-owned contract, fixture and scope foundation; exclusive paths in ownership table_
  - _Depends: 1.3, 1.4, 2.40_
  - _Requirements: 1.1, 1.4, 4.8, 4.9, 10.4, 10.5, 10.6_

- [x] 2.42 (P) Preserve original saved-option composition without mutating state
  - Accepted: independent APPROVED/VERIFIED review in `artifacts/reviewed/task-2.42/review/review.md`; 126 application/260 compatibility tests, both strict compilers, scoped lint and 175-file complexity audit pass. Concurrent tooltip changes are excluded from this task-local stage and require the joined gate.
  - Use the approved saved operand baseline.options and generated operand. Return a detached combined value with generated common replacing saved common, then source-equivalent lodash merge semantics; do not reread baseline.model.chartOptions or storage.
  - Preserve family and unknown branches, own undefined/null/array behavior and input identity/contents. Keep callbacks outside data-only options. Contain accessors, cycles, nonplain values and throwing proxies through the public validation boundary without invoking getters or functions.
  - Write meaningful failing regressions before implementation for saved-common replacement, conflicting bar/line families, mismatched baseline/model options and mutation. Expected fixtures and pinned original-source composition serve as the oracle, not the new helper's output.
  - Done: focused composition tests, strict checking and lint pass after RED evidence; independent review verifies exact source winners and unchanged input state. The complete maintained file passes 400 physical/300 logical/50 per function. No changes to baseline selection, reducers, theme generation, renderer or application hooks.
  - _Boundary: Pure saved-option composition and its owned test file_
  - _Depends: 2.41_
  - _Requirements: 1.1, 1.4, 4.2, 4.7, 4.8, 4.9, 10.5, 10.6_

- [x] 2.43 (P) Reproduce derived grid and subtitle colors from explicit tokens
  - Accepted: independent APPROVED review in `artifacts/reviewed/task-2.45/review/report.md`; 42 color cases included in the 176-test application suite. Exact normalized arithmetic, explicit aliases and descriptor-safe diagnostics pass; production size is 118 physical/53 logical/16 maximum function units.
  - Accept explicit supported base and foreground/background/text/chart-background tokens. Use the approved normalized-channel operation order, literal ratios and lowercase six-digit output. Do not assume aliases are identical or resolve arbitrary saved theme graphs.
  - Separate descriptor-safe invalid structure from structurally valid unsupported strings; preserve diagnostic paths. Reject missing/non-string/unknown own fields and contain hostile access; unsupported bases/color strings are unresolved without claiming CSS validity.
  - Begin with failing independent expected-color cases, including the #000000/#9b0000 rounding edge yielding #8b0000, dark/light ratios, independent subtitle aliases, upper/lower hex input and black/white bounds. Retain the exhaustive source experiment as historical evidence rather than introducing AG into maintained runtime/tests.
  - Done: focused tests, strict checking, lint and independent review pass; inputs are unchanged and diagnostic cases produce no guessed color. The complete maintained file passes 400 physical/300 logical/50 per function. No general CSS parser, theme selector, stored-state change or renderer dependency is added.
  - _Boundary: Pure derived-color routine and its owned test file_
  - _Depends: 2.41_
  - _Requirements: 1.1, 1.4, 4.8, 4.9, 10.5, 10.6_

- [x] 2.44 (P) Integrate grouped-column tooltip edits with the existing addressed session
  - Accepted: independent APPROVED/VERIFIED review in `artifacts/reviewed/task-2.44/review-repair/report.md`; 96 application/274 compatibility tests, both strict compilers and scoped lint pass. The existing real-grid test now drains pending AG callbacks before jsdom teardown; the prior failed check and its root-cause evidence remain published. No production animation or UI change.
  - Extend the existing event union and mapper with tooltip-mode values single/shared/compact and exactly the bar.tooltip.mode patch. Preserve Multiple -> shared semantics; reject arbitrary paths and malformed values. The mapper retains its current ValidationResult signature.
  - After session stamp validation, distinguish an exact structurally valid stackedColumn tooltip event as unresolved, before mapping or writes. Mapper-level stacked tooltip rejection remains validation failure. Malformed events remain invalid; proxy/accessor handling is exception-contained. The four existing events retain both original column-family behaviors.
  - Exercise the real existing session and reducer with latest storage and baseline.options, never composed rendering options. Preserve unknown and inactive-family state, current model, prior edits and stale-address/generation/data/render revision behavior; no new save trigger.
  - Begin with failing exact-patch and session regressions. Done: actual grouped tooltip edits produce the expected original model fields, invalid/unresolved/stale inputs leave storage untouched, and all existing event/session tests pass under independent review. Both touched responsibility boundaries are an explicit event-to-session integration task.
  - Every modified maintained file is checked whole against 400 physical/300 logical/50 per function. No option reducer, baseline owner, mapper, UI or family visibility changes; no new callback/store.
  - _Boundary: Typed editor event to existing session integration; exclusive files in ownership table_
  - _Depends: 2.41_
  - _Requirements: 4.2, 4.7, 4.8, 4.9, 10.4, 10.5, 10.6_

- [x] 2.45 Independently verify and join the source contracts without activating the application
  - Accepted source gate: independent VERIFIED/scoped GO in `artifacts/reviewed/task-2.45/review/report.md`; 176 application/274 compatibility tests, both strict compilers, 25-file lint, 71 exact staged identities and the 176-file maintained audit pass. See `chart-appearance-source-verification.md`. Source pins and reviewed artifacts are reconciled for selective delivery; application and release gates stay open.
  - Freeze all worker writes and snapshot the actual combined source/config/fixture bytes to a fresh stage. Independently rerun both unit suites, both strict compilers and scoped lint with zero hidden skips; preserve failed attempts and exact command exits.
  - Verify the typed composition/color handoffs and event/session integration together against accepted fixtures. Confirm composition/color outputs remain render-only, stored baseline fields survive tooltip edits and no application guard, menu, flag, dependency or UI path changed.
  - Run the complete maintained inventory gate with explicit fork change manifests and exact source identities. All new/modified production files pass 400 physical/300 logical/50 per function; existing exception target bytes remain unchanged. Tests and synthetic fixtures remain declared exclusions.
  - Done: fresh independent review reports scoped GO and verification for 2.41-2.44 only, with actual test paths and source/artifact identities. Record the continuing B2/mapper/editor/transformation/application/persistence gates in breadth; no reference-only or unit result becomes renderer acceptance.
  - Synchronize only frozen reviewed safe artifacts before selective commit/push, preserving unrelated working changes. Reconcile source pins/inventory without absorbing catalog/Perspective work. Corrective production edits return to the owning task and independent review rather than expanding this join's scope.
  - _Boundary: Controller-owned source-contract verification and evidence join; no additional production behavior_
  - _Depends: 2.42, 2.43, 2.44_
  - _Requirements: 1.1, 1.4, 4.2, 4.7, 4.8, 4.9, 10.1, 10.2, 10.3, 10.4, 10.5, 10.6_

### Ownership and scheduling for 2.41-2.45

Production paths below are relative to terminalpro/src/components/General/Table/Chart; test paths are relative to terminalpro/tests/unit. Each task is a bounded 1-3 hour work unit, including its focused review, not a delivery-time promise.

| Owner | Exclusive writable paths |
| --- | --- |
| Controller 2.41 | application/appearanceContracts.ts; chart-application/appearanceContracts.types.ts; chart-application/appearanceFixtures.json; root .kiro/complexity-budgets.json and .kiro/breadth.toml; isolated stage/manifest outputs. Existing compiler/Vitest configs are read-only unless a concrete prerequisite is returned for review. |
| Sol 2.42 | application/appearanceComposition.ts; chart-application/appearanceComposition.test.ts |
| Sol 2.43 | application/appearanceColors.ts; chart-application/appearanceColors.test.ts |
| Sol 2.44 | compatibility/optionStateTypes.ts, compatibility/editorEvents.ts, application/sessionState.ts, application/types.ts only if required by approved command typing; chart-compatibility/editorEvents.test.ts, chart-application/sessionState.test.ts |
| Controller 2.45 | Root inventory/breadth/source pins, joined manifests and verification artifacts; no renderer/application edits |

Appearance contracts/fixtures freeze before fan-out; workers may read but not edit them. Schedule two implementation lanes: composition then colors on lane A, tooltip event/session on lane B. 2.43 is logically independent after 2.41; its lane sequencing is a resource limit, not a hidden semantic dependency. Reserve a slot for fresh independent review, using Astra for composition/state/financial boundaries and Sol for bounded routine checks. At most controller + two workers + reviewer. One heavy check at a time; installations/shared mutations/commits remain serialized. The project delegation amendment governs these explicit dependencies rather than generic list-order serialization.

### Verification setup and commands for 2.41-2.45

Use a new isolated WSL stage containing current owned source bytes, not a previous task archive. Reuse pinned Node 24.22.0 and the accepted dependency tree at /home/mc/qopenbb-work/appearance-deps/terminalpro/node_modules. Record actual versions and identities in 2.41. Existing application/compatibility configs already include their own *.ts/*.tsx unit trees and application sources, with jsdom, maxWorkers:1 and no global setup. Compile-only fixtures end in .types.ts. No new install, browser, image or config is assumed. If the accepted runtime is missing, restore through the existing locked protected workflow before proceeding; never silently upgrade.

From the stage's terminalpro directory, with pinned Node on PATH:

```sh
node node_modules/typescript/bin/tsc --project tests/unit/chart-application/tsconfig.json --noEmit
node node_modules/typescript/bin/tsc --project tests/unit/chart-compatibility/tsconfig.json --noEmit
node node_modules/vitest/vitest.mjs run --config tests/unit/chart-application/vitest.config.mjs
node node_modules/vitest/vitest.mjs run --config tests/unit/chart-compatibility/vitest.config.mjs
node node_modules/@biomejs/biome/bin/biome check src/components/General/Table/Chart/application src/components/General/Table/Chart/compatibility/editorEvents.ts src/components/General/Table/Chart/compatibility/optionStateTypes.ts tests/unit/chart-application tests/unit/chart-compatibility/editorEvents.test.ts
```

Focused workers append their actual owned test paths to the matching Vitest command. Tests are not considered accepted based on discovery alone. Historical totals of 88 application/260 compatibility tests are baseline evidence, not this wave's results. The joined check runs both complete configurations, not only new files.

Controller-generated manifest paths below are future task outputs. Run the existing full gate from the root with pinned Node on PATH:

```sh
pipeline/.venv/bin/python -m tools.quality.complexity --check --changes workspace=artifacts/appearance-editor-implementation/workspace-changes.json --changes data_api=artifacts/appearance-editor-implementation/data-api-changes.json --output artifacts/appearance-editor-implementation/complexity.json
```

Both manifests contain explicit repository/base/head and complete changed-file scope. Preserve unrelated dirty inventory entries and exact exception targets rather than overwriting or rebinding them without evidence. Source pins change only at the reviewed commit join. No new blanket exception is proposed.

### Continuing gates

The three source contracts feed the already designed B2 and original event/session boundary; they are not disconnected replacement systems. Complete effectiveAppearance, original-to-ECharts field projections, public tooltip rendering, original docked controls, transformed snapshots and D activation remain under the blocked application followups above. This task batch cannot remove guards or accept a reduced product menu. No Excel implementation precedes Anthropic acceptance; Dagger remains image-build-only.

## Approved design slice: SQLite query compatibility

The owner approved the [SQLite repair design](sqlite-repair-design.md) and its narrow size exception on 2026-10-17, then approved tasks 4.6-4.9. Independent Sol task-graph sanity review passed (`artifacts/completion-path/sqlite-task-review.md`): the merged plan has 89 unique task IDs and maps all 69 active acceptance criteria. Autonomous implementation within this boundary is authorized. These tasks supplement the parent plan without accepting renderer activation or changing the full parity requirement.

Dependency override: this independent backend branch starts after accepted foundations 1.2, 1.4, 1.7 and provisional Workspace 2.5; it does not wait for tasks 4.1-4.5 despite its numeric position. Task 4.5 additionally requires accepted 4.9. Actual environment/browser restart acceptance remains in 4.2/4.5; SQLite engine recreation cannot substitute. No cycle is introduced. Anthropic and delivery still depend on 4.5, and Excel still waits for 5.5.

Sol owns the backend lane; Astra independently reviews query semantics and acceptance. Keep its four tasks sequential because they share fixtures and source identity. Independent renderer research may proceed alongside it in disjoint files. The controller owns shared inventory, evidence, pins and commits. One heavy suite/install at a time, at most four agents, two xdist workers maximum, no owner data or credential reads.

- [x] 4.6 Establish an isolated locked SQLite verification runtime
  - Restore the frozen existing backend Python 3.13 environment through the protected toolchain, or identify a reusable backend image with exact matching dependency identity. Do not resolve a new lock. Record the actual runtime and exercised focused command; missing packages cannot count as a skip/pass.
  - Build the sibling SQLite test bootstrap and shared fixture builders specified by the design. Before settings imports, isolate dotenv-source construction, use an empty temporary working directory and minimal synthetic child environment, retain the absolute backend import path and deny outbound network. Verify denied reads with a sentinel env/account file; do not inspect operator configuration.
  - Create actual dependency-closed model tables in per-test file databases with foreign keys and original compressed/UUID types. Freeze fixture APIs for owners, creators, recipients, entities and shares before the next task. No concat UDF, fake tables or mocked database execution.
  - Done when a fresh process proves bootstrap isolation and an actual stored fixture roundtrip using the identified backend runtime, with reproducible commands and cleanup. Tests and artifact-only environment setup are excluded from production caps; no maintained production runtime changes are authorized here.
  - _Boundary: SQLite test runtime, conftest.py and fixtures.py in the design's sibling test directory_
  - _Depends: 1.2, 1.4, 1.7, 2.5_
  - _Requirements: 1.1, 10.5, 10.6_

- [x] 4.7 Repair populated dashboard and app reads without changing access semantics
  - Add regressions for all six populated reads across full, partial-null, null, empty, whitespace and asymmetric empty names. Assert exact displayed attribution, IDs, content and relevant sharing flags.
  - Seed distinct owner, creator, recipient and unrelated users across entities/permission maps, active/inactive shares and exclusion sets. Assert exact visible membership and the existing noex owner-permissions behavior. Capture raw entity query cardinality and fail on Cartesian-product warnings so result dictionaries cannot hide duplicate rows.
  - Retain failing reference evidence before applying exactly the six dialect-aware string expression replacements and missing creator join. Capture actual selects for SQLite execution and MySQL compilation; compilation is not live MySQL acceptance. If newer SQLite supports concat, preserve observed baseline results rather than manufacture six failures; the missing-join regression must expose the real defect.
  - Done when the corrected queries pass populated fixture cases and independent review confirms the seven-site diff, unchanged API/authorization contracts and exact baseline-versus-patch evidence.
  - Measure the whole modified CRUD file. The owner-approved exception permits at most 1600 physical lines and 582 logical units, with expiry 2026-11-17; function cap 50 remains enforced. Record exact post-patch counts/hash for controller registration and review. Do not alter the checker or widen the exception. Tests are excluded; any unplanned production file still requires 400/300/50.
  - _Boundary: Existing CRUD seven-site repair and dashboard/app read regressions; frozen fixture APIs from 4.6_
  - _Depends: 4.6_
  - _Requirements: 1.1, 1.4, 4.2, 4.7, 10.5, 10.6_

- [x] 4.8 Prove actual dashboard storage survives engine recreation
  - Exercise actual bulk insert/update with typed dashboard input and nested layout, widget parameters and chart state. Read through repaired queries, dispose all sessions/engine and reopen the same file with a new engine. Compare exact stored payload, dates and identities through the real compressed storage types.
  - Exercise the real on-prem share helper, replacing only queue transport. Check string UUID arguments and preserve commit-before-enqueue behavior; distinguish swallowed job timeout from propagated failures. Do not claim rollback of an already committed dashboard.
  - Verify foreign-dashboard modification/deletion and duplicate-ID failures using actual existing error behavior, explicit failed-session rollback and another owner's unchanged content. Use disposable file databases rather than outer transactions that bulk commits could escape.
  - Done when persistence and failure/isolation cases pass together with all 4.7 regressions on the same source/runtime, with independent review. This proves the storage layer only; browser/environment restart remains unverified.
  - Tests are excluded from production caps. Any required production correction returns to 4.7 scope and review, preserving its exact exception and 50-unit function cap; do not expand behavior here.
  - _Boundary: Dashboard persistence regression file using frozen shared fixtures and actual CRUD_
  - _Depends: 4.7_
  - _Requirements: 2.2, 4.2, 4.7, 10.3, 10.5, 10.6_

- [x] 4.9 Independently accept and register the SQLite repair boundary
  - Review exact source/runtime identities, rerun the focused backend suite and confirm all six reads, cardinality, storage and failure cases. Preserve source hashes, commands, exits and meaningful baseline failures. Match evidence to the final source; do not reuse stale stage results.
  - Register maintained CRUD scope and the two independently measured physical/logical exceptions with exact final fork revision, before/after hashes, reviewed seven-site diff and expiry. Preserve unrelated inventory/catalog edits and verify unchanged files before rebinding existing exceptions. Do not create a function exception.
  - Run the implemented combined checker from docs/complexity.md using actual fork changed-file manifests, not historical heads. Done when the measured file stays within its approved ceiling, all other maintained production scope meets 400/300/50, and independent Astra review returns scoped GO with reproducible runtime evidence.
  - Update breadth with actual tests and query/storage-layer status, publish the scoped verification record and accepted source pin, and selectively commit the repair. Link the exercised focused command into the existing verification documentation; do not invent a new runner or expand Dagger's build-only responsibility. Preserve dashboard/renderer/release status as unverified until their real image/browser gates pass.
  - _Boundary: Controller-owned cross-repository acceptance, inventory, breadth, source identity and verification record_
  - _Depends: 4.8_
  - _Requirements: 1.1, 1.4, 2.2, 4.2, 4.7, 10.3, 10.5, 10.6_

Task 4.6 accepted after independent Astra re-review: two real-model bootstrap/storage tests, Ruff and formatting pass; cleanup passes after success and expected nonzero exit. The initial retained pytest database defect was repaired with an owned temporary root and its three confirmed leftovers removed. Evidence: artifacts/task-4.6/review/review-round2.md. Workspace 693954f43aac8af888cfe6e7bfed6d9dcb72d2f5. Frozen runtime: Python 3.13.15 under /home/mc/qopenbb-work/sqlite-runtime/venv; launcher backend-api/backend/tests_sqlite/run.py. Query repair and application acceptance remain unverified.

Task 4.7 accepted after independent Astra review: 53 tests pass with zero skips versus 10 failing/43 passing baseline cases. Exact seven-site diff, identical test/runtime manifests and preserved sharing/name semantics verified. CRUD measures 1599 physical/582 logical/max function 36; the measured exception is registered with expiry 2026-11-17. Workspace 4579cea149db29a592b28e4a2312c4348f4038dc. See [SQLite verification](sqlite-repair-verification.md) and artifacts/task-4.7/review/verdict.md. Whole-file formatting fails equally before/after; scoped lint passes. Bulk persistence and application acceptance remain open.

Task 4.8 accepted after independent Astra review: 60 tests pass with zero skips, plus scoped Ruff and formatting. Actual typed bulk insert/update survives file SQLite engine recreation; queue transport observes already committed content, and ownership/duplicate failures preserve another owner's state. Production CRUD and frozen infrastructure are unchanged. Evidence: artifacts/task-4.8/review/review.md and independent-full.json. Application and environment restart acceptance remain open.

Task 4.9 accepted after independent Astra final review: scoped GO for tasks 4.6-4.9 at Workspace f23cb786a946a6a996deedbe87be9c7ca86b221e. Fresh 60 tests pass with zero skips; scoped lint and test formatting pass. The explicit maintained-scope audit measures 168 files with nine exact exceptions and no errors or violations, including CRUD at 1599 physical/582 logical/max function 36. Actual test paths, source identity and exception expiry are registered. Evidence: artifacts/task-4.9/review/review.md and [SQLite verification](sqlite-repair-verification.md). Browser restart, renderer parity and deployment remain unverified.

Task 2.34 accepted after independent Astra review at Workspace 4b31dfc3991e5edecb2437f94d85526bd0f9c660. Both strict compiler configurations, 260 compatibility tests, scoped lint and 55 staged source identities pass. The maintained scope checks 169 files with zero errors/violations; application types measure 181 physical/111 logical. Explicit CPython cache exclusion corrects a generated-bytecode inventory error without exempting maintained sources. Frozen contracts are ready for tasks 2.35/2.36; no application runtime or renderer parity is accepted. Evidence: artifacts/task-2.34/review/verdict.md.

Task 2.35 accepted after independent Astra review: 18 tests, both strict compilers, scoped lint and 48 staged identities pass. Range and session modules measure 47/19/13 and 166/96/16 (physical/logical/largest function); the maintained 172-file audit has no errors or violations. Evidence: artifacts/task-2.35/review/verdict.md. Application activation remains unverified.

Task 2.36 accepted after independent Astra financial review: 18 tests, both strict compilers, scoped lint, original-source fixture verification and 52 staged identities pass. The module measures 52 physical/25 logical/5 maximum function units. RED evidence is a missing-module replay after setup failures, as disclosed in the handoff. Evidence: artifacts/task-2.36/review/verdict.md. Joined acceptance remains task 2.37.

Task 2.37 independently accepted with scoped GO at Workspace 945e438a9a65c3eeef7073dbce64a03b02f0ff6f: 296 joined tests, both strict compilers, scoped lint, 62 exact staged identities and the 172-file maintained audit pass. Source-safe tasks 2.34-2.37 are VERIFIED; application and deployment remain unverified. See chart-application-source-verification.md and artifacts/reviewed/task-2.37/review/verdict.md.

## Horizontal application join scope clarification

The task 2.81 browser run exposed existing three-family guards in `application/effectiveAppearance.ts` and `application/axisStructure.ts`, plus the narrow formatting input type in `application/types.ts`. These three existing application-owner files are added to the controller join scope, limited to consuming the accepted horizontal family contract. Independent Astra integration review confirmed this is necessary for the approved appearance and structural controls, without adding another state owner or feature. The combined size gate includes all three; caller tests exercise real appearance and axis transitions, and the browser changes the vertical axis position. The failed run is retained locally at `artifacts/live-editor/runtime/horizontal-join-2`.
