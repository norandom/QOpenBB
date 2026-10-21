# B3c Box Plot axes and navigation

B3c independently accepted, 2026-10-21. Implement the existing inactive Box mapper's rounded numeric scales and working horizontal navigator in one bounded slice. Reuse the host's viewport and measured two-pass axis-footprint pattern. Do not port AG Charts' scene layout or add a second layout/state owner. The numerical tick arithmetic is source-derived; final font metrics, tick density and label spacing remain an explicit original/replacement visual comparison at B4. B3d activates this adapter and the existing controls after independent B3c review.

Inspected 2026-10-21 at Workspace `1732847552a762c38e1cb1408d1efebccdeb0e6a`, root `cebf7ea`. This addendum supersedes the unresolved tick-layout reservation and unconditional miniature-inheritance statement in [B3 integration](box-plot-integration-design.md). [B1](box-plot-design.md), [B2](box-plot-renderer-design.md) and [B3b](box-plot-setup-design.md) retain statistical, style, capture and aggregate ownership. No activation or milestone acceptance is claimed.

## Boundary commitments

B3c owns numeric scale planning, measured usable axis spans, Box-specific full-data overview composition, screen-x navigation and the existing lifecycle's safe callback join. It keeps selected observations, quartiles, categories, palette identity, saved options and reachable actions intact. The pure mapper remains inactive until B3d; its result must already be usable through the real ECharts host.

**Out of boundary:** application capture/editor/session routing, new controls, Range Area, provider requests, image builds, browser acceptance and publication. Do not introduce a custom chart editor, second ECharts instance or retired AG runtime dependency. Existing approved libraries and public ECharts custom series/dataZoom APIs are sufficient.

**Allowed dependencies:** compatibility projection and display policy flow into pure Box adapters, then the existing lifecycle. Box modules may use `cartesianLayout.measureText`, existing navigator chrome/overview composition, and existing appearance types. Lifecycle calls a generic optional request callback; it does not import application/session code. Other families retain their current projections.

**Revalidation triggers:** a change to capture/grouping, explicit bound admission, mini-chart source selection, main/overview orientation, native zoom filtering, or the callback signature returns to the integration owner. Font/spacing differences go to matched visual review; changes to observations, summaries, category membership, controls or persistence require correction rather than visual waiver.

The local `kiro-spec-design` integration workflow was applied under the prototype-first bounded-delivery amendment. Core product/tech/structure steering remains absent; applicable complexity, testing, delegation, documentation, delivery and workspace-experience steering was read. This English addendum does not advance whole-spec approval metadata or invent requirement IDs; it traces to B3/B4 in the [approved milestone contract](box-plot-milestone.md).

## Original scale and layout findings

References `C`, `E` and `G` below are physical lines in the retained Charts community12.1.1, Charts enterprise12.1.1 and Grid34.1.1 bundles identified and hashed in [B1 source contract](box-plot-design.md#source-contract) and [B2](box-plot-renderer-design.md). Community SHA256 is `237912c75d2c7e8219fced7bb79e5ed8fca0f620d6f4d259cdfa58748445fcd1`. No downloaded/current release is substituted for these sources.

| Decision | Source and consequence |
| --- | --- |
| Initial tick density | C18683-18702, C19263-19287: continuous default count5 and minimum spacing50px. Resolve `defaultMinSpacing=max(50,span/6)`; default maximum spacing is span; derive min/max counts from actual range and visible fraction. Zero span produces no ticks. |
| Collision retries | C19327-19400, C19466-19540: measure formatted labels, try smaller counts down to minimum, skip repeated raw tick arrays, optionally autorotate. Labels disabled or `avoidCollisions=false` bypass collision retries. Each changed count can change nice domain. |
| Overlap test | C16398-16403, C16488-16506, C19858-19872: source text metrics plus label padding; default collision spacing10px, or0 when rotated; compare positioned boxes. It is not merely a fixed maximum tick count. |
| Numeric nicing | C30242-30285: choose 1/2/5/10 step by count distance and min/max-count preference; at most four rounding iterations, always round original domain endpoints against the newly chosen step. Count1 has its separate `niceTicksDomain` path. Explicit bounds enter nicing and are not clamped back afterward. |
| Zoomed ticks | C17858-17935: first calculate the unzoomed nice domain; a non-full visible fraction requests `TicksOnly`. Zoom must not repeatedly nice the cropped range and drift the full domain. |
| Horizontal edge labels | C19399-19415: with more than two ticks, a last label beyond the right edge can be hidden. At full range the first is hidden too; while zoomed only the overflowing last is hidden. This affects labels, not raw tick values or data. |

The retained-scale probe `artifacts/chart-box/b3c-axis-source-probe.mjs` executed24 cases with WSL Debian/mc Node24.22.0, exit0, output `b3c-axis-source-probe.json`. It directly calls retained `estimateTickCount`, `LinearScale.niceDomain` and `ticks`; it does not run layout or prove pixel equivalence. At spans100 and300 the same singleton5.5 can respectively retain `[5.5,5.5]` and expand to `[5,6]`. The already accepted constant-domain evidence remains applicable.

The host supplies container dimensions, not the original post-layout span. `boxPlotGeometry` receives actual ECharts `coordSys` only during drawing, after native axes have been laid out; it cannot set the same pass's axis ticks. Existing Histogram estimates usable spans with two measured footprint passes. Adopt that same bounded approach for Box. Do not call the estimate an exact original post-layout measurement.

## Scale and layout contract

Add `boxPlotValueAxis.ts`, `boxPlotTicks.ts` and `boxPlotAxisLayout.ts`. The first owns the public plan and finite transport; the second owns source-compatible linear arithmetic; the third owns layout measurement and collision selection. Keep these responsibilities together under one implementer rather than parallelizing coupled axis work.

```ts
export interface BoxTickDensity {
  readonly tickCount: number;
  readonly minTickCount: number;
  readonly maxTickCount: number;
}
export interface BoxValueAxisPlan {
  readonly semanticExtent: readonly [] | readonly [number, number];
  readonly fullExtent: readonly [] | readonly [number, number];
  readonly visibleExtent: readonly [] | readonly [number, number];
  readonly rawTicks: readonly number[];
  readonly fullTransport: BoxValueScale;
  readonly transport: BoxValueScale;
  readonly density: BoxTickDensity;
  readonly span: number;
}
export interface BoxAxisWindow {
  readonly start: number; // Percent, inclusive, 0..100.
  readonly end: number;   // Percent, inclusive, start..100.
}
export function planBoxValueAxis(
  domain: BoxPlotDomain, span: number,
  density: BoxTickDensity,
  visibleRange?: readonly [number, number],
): BoxValueAxisPlan;
```

`BoxValueScale` remains the geometry transport type from `boxPlotDomain.ts`. Move its nicing responsibility into the plan. Semantic extent is the unchanged B2 domain after bound substitution. Full extent is source-compatible nice domain. Visible extent is the clipped full extent, not a second statistical domain. `rawTicks` remain financial values; `transport.ticks` are coordinate values. For a final equal full extent use transport `[0,1]`, constant raw value and midpoint tick0.5. Empty domain uses inert finite transport and no invented financial ticks. Nonfinite intermediate arithmetic is unsupported through the existing diagnostic result; no silent arbitrary expansion.

`fullTransport` maps the full extent; `transport` maps the visible extent. At a full window they agree. Main numeric x uses `fullTransport` because native dataZoom applies its crop; main numeric y uses `transport` because vertical autoscale has no native y zoom. Both transports use the same raw value identity and explicit constant mapping, and each axis's geometry uses the transport selected for that axis. This distinction prevents an orientation-dependent interpretation of one scale field.

`planBoxValueAxis` returns a plan or throws on invalid/nonfinite input or arithmetic. It does not return the mapper's diagnostic union. The public `translateBoxPlot` catch converts planner failures into its existing invalid/unsupported translation result. A navigation callback that receives a failed translation must throw its diagnostic message; lifecycle then releases the failed instance, invalidates export and delivers the error through `onError`. Do not return old/partial options from that callback.

`boxPlotAxisLayout.ts` takes admitted input, projection and already reserved main-grid chrome. It measures category text, provisional numeric tick text, titles, labels, ticks and caption/legend footprints using existing font resolution. Reserve navigator height18 or miniature height40, spacing10 and miniature label footprint before choosing numeric span. Compute provisional ticks, remeasure their footprint, then compute the final span and count once more. There are exactly two footprint passes, followed by a bounded decreasing-count collision search; no host feedback loop.

Use the source density formulas and linear arithmetic at that measured span. Evaluate formatted numeric labels through `display.numericAxis`, with resolved rotation and font; decrease count until measured labels fit or minimum count is reached. Skip duplicate raw tick sequences. Numeric auto-rotation follows its resolved option; default generated numeric autoRotate is false. Preserve retained valid interval/spacing inputs if admitted by the appearance layer; do not add configurable tick controls that the original Box panel excludes. Explicit custom tick arrays/steps outside the current admitted Box style require an explicit compatibility diagnostic at B3d, not silently ignoring saved options.

The mapper returns the chosen plan alongside `projection` and unchanged `domain`. Geometry, axis labels/crosshair, clipping and grid ticks use this one plan. Supply numeric min/max and custom tick/label values to ECharts, disabling its independent nicing. Measure category rotation against usable category span, not full container dimensions. Geometry continues to use real `coordSys` for pixel placement and clipping. This keeps finance values consistent even when ECharts' final font/layout pixels differ from the estimate.

This is an intentional practical visual boundary: possible differences are one more/fewer tick, slightly different rounded displayed endpoints, endpoint label suppression, rotation threshold and plot whitespace. A changed displayed range does not change quartiles or tooltip raw values. B4 must show these differences in matched light/dark views, including singleton5.5 and horizontal long labels; owner acceptance is required for any remaining visible deviation. No invisible collision-loop port is an implementation prerequisite.

## Navigator and miniature source contract

The navigator changes **screen x**, including horizontal Box. Enterprise E15525-15530 updates `{x:{min,max}}`; E15918-15928 reads x zoom back into the slider. It does not switch to category-axis navigation when Box direction changes. `minRange=1e-3` at E15469 means the slider's minimum0.1-percent span. E15859-15889 reserves navigator height plus spacing, and aligns its width to the main series rectangle. Retain the existing slider/mask chrome and flags.

Vertical Box therefore selects category bands; horizontal Box crops numeric values while preserving every category row. Do not filter observations or recompute quartiles after zoom. Keep any box intersecting the selected viewport and clip its geometry; do not drop a box merely because one endpoint lies outside it.

Original Workspace `themes.tsx` at `38dffc3`, lines202-208, enables zoom, pointer anchoring, minVisibleItems4 and autoScaling. Community C13119-13180 computes visible numeric extrema using visible series, converts them into the full nice domain, applies5% padding at each eligible end, caps the padded fraction at1 and shifts it inside `[0,1]`. Explicit numeric min/max anchor the corresponding full-domain side. The full window resets to full extent; equal/empty visible extrema must not invent a new range. This is a visible window on the original full plan, not fresh min/max nicing. Horizontal category-axis autoscaling must not reinterpret numeric quartiles as category indexes; preserve the full category axis.

That horizontal policy is financial intent, not unconditional exact source parity: E16414 ignores direction when returning financial extrema; C38103 filters them through category ranges, then C13134 converts them through screen-y's category scale. Ordinary string categories do not match those numbers, but numeric category identities coinciding with raw financial extrema may accidentally autoscale the original category axis. Add that coincidence as a B4 original/replacement fixture. If observed, preserving the full category axis is an explicit source-bug deviation requiring owner review; do not claim it was already accepted.

Box does not override `Series.getVisibleItems`, which returns Infinity at C21571-21573 through AbstractBarSeries. The common minVisibleItems4 setting therefore does not justify imposing a four-category/observation floor on Box. Keep the source slider minimum0.1%; do not borrow XY's minimum-four-point window calculation.

Miniature inheritance has a material exception to the earlier B3 assumption. Enterprise E21942-21973 defines ignored Box properties including direction and visible, but E22102-22115 omits `box-plot` from `validMiniChartSeriesTypes`. E22213-22244 consequently does not automatically synthesize the usual mini series array for default Box. Community C25260 instead falls back to `newOpts.series`. C25195 only filters `showInMiniChart=false`; C25524-25540 applies direction and visible from those options. **The ordinary default Box miniature follows main direction and configured series visibility.** Do not force vertical miniature solely from the ignored-property schema.

Community C25337-25372 gives mini axes their own ranges, disables nice/grid/ticks and all but screen-x labels, and retains effective non-omitted axis options. Enterprise E15380-15414 lays out those axes against the miniature's rectangle. Build miniature geometry afresh from the full projection with a separate no-nice value plan, overview band span and inherited styles; never clone a main `renderItem` closure. Legend runtime selection is not a saved `series.visible` edit: rebuild the default overview from full selected fields, independent of transient main legend hiding. Preserve an explicit configured visibility value when B3d admits it.

Explicit `navigator.miniChart.series` takes the separate template/override path and may omit direction/visibility. This slice does not claim that arbitrary explicit custom mini series is identical to the ordinary Table/File default. Preserve such saved data and require B3d admission to identify it; ordinary menu toggles use the default fallback above. No control is hidden or disabled. A failing admitted saved fixture returns to this contract before activation.

Two no-render `ChartOptions` experiments were inconclusive: the first lacked global window/document; a second with inert globals lacked complete factory/module initialization. They establish no theme-resolution acceptance and were abandoned. The fallback decision above is source analysis; B4 original/replacement default horizontal miniature comparison remains the runtime disproof check.

## Frozen adapter and lifecycle seam

Extend `BoxPlotMappingInput.context` with optional `navigation` containing `{enabled:boolean; mini:boolean; theme:ApplicationThemeInput; window?:BoxAxisWindow}`. Omission means the accepted inactive no-navigator path. Add `valueAxis:BoxValueAxisPlan` to its supported result. B3d supplies existing flags/theme and no persisted window; the engine remains the sole live-range owner.

`boxPlotNavigator.ts` composes chrome and a separately translated overview. Its helper receives admitted input, projection, full main plan and main options; it must not recursively call the public mapper with navigation enabled. Reuse `cartesianNavigator` with `miniHeight:40`; replace its overview series input with the freshly built Box series and override dataZoom to target only main `xAxisIndex:[0]`, `filterMode:'none'`. The overview never follows the native window or transient legend selection. Register an inside zoom id `openbb-box-inside`, matching existing pointer zoom/pan/reset behavior, and synchronize it with `openbb-navigator`; controls and both feature flags retain their current application meanings.

`boxPlotNavigationWindow.ts` exports:

```ts
export function boxPlotNavigationWindow(
  input: BoxPlotMappingInput,
  projected: EChartsOption,
  current: EChartsOption,
): EChartsOption;
```

It reads/clamps the current main window, reads the already projected legend selection, and rebuilds options from immutable input with the appropriate visible axis plan. It never aggregates again or reads storage. Vertical selection uses intersecting category bands and enabled field summaries for autoscale; horizontal selection crops the full numeric x plan while leaving category transport unchanged. Invalid nonfinite callback inputs throw to the host failure channel. Retained input/source arrays remain unchanged. The returned options carry synchronized slider/inside percentages and the full overview.

Apply each range exactly once. Main x-axis min/max always retain the full unzoomed transport domain, in either orientation; native screen-x dataZoom applies the retained percentages. For horizontal Box, `visibleExtent` selects raw custom numeric ticks and labels, but must not replace main x min/max with cropped bounds while retaining the same native percentages. Geometry keeps the full x transport and uses ECharts' zoomed coordinates. For vertical Box, category x likewise retains its full domain; numeric y uses the computed autoscale visible extent directly as transport bounds, with no y-axis dataZoom. Overview axes always use full overview extents. Tests must assert coordinates for a partial numeric x window, not merely the start/end options, to catch double application.

Vertical native x zoom must expand category band step and box width together with category centers. Derive the zoomed step from actual category-coordinate distance or scale the full-domain step by the inverse visible fraction; do not retain the current `plot.width / categoryCount` width after centers have zoomed. Group spacing, box width and whisker caps consume that zoomed band geometry. Horizontal category-row widths remain unchanged, and overview bands always use the full-domain width. Include one actual ECharts SVG assertion that a partial vertical window expands box width by the expected category-scale factor while overview width remains unchanged.

Add this optional callback to the existing `ChartRenderRequest`:

```ts
readonly projectNavigationWindow?: (
  projected: EChartsOption,
  current: EChartsOption,
) => EChartsOption;
```

The application later closes it over immutable Box input. `EChartsHost.tsx` manually forwards request properties: forward `projectNavigationWindow` through its prop destructuring, latest-request ref and every mount/update request construction. A host regression proves a supplied callback reaches the actual lifecycle request; adding the lifecycle interface alone is insufficient. In lifecycle render, obtain legend-projected options, retain native window when the same scope is active, then apply the callback before `setOption`. On datazoom use that same ordered path; do not apply the current XY/Histogram y-axis-only patch to Box. Legend changes preserve the selected percentage on the same scope. A family/scope transition clears it. Native datazoom state remains authoritative; never store percentages in Widget preferences.

Resize retains the existing two-step host flow: ResizeObserver first calls `lifecycle.resize()` with the last accepted immutable request, then `notifySize` calls the session's existing `onResize` with current container dimensions. The session stores that viewport, increments its render stamp and supplies a new projection/request whose callback closes over the updated viewport. The first resize pass may use previous footprint estimates; the subsequent accepted request must recompute density, geometry and overview at the new size while retaining native percentages. Do not claim the old callback already contains fresh dimensions, and do not introduce a second viewport owner or callback argument. Test both the host notification/new-request sequence and range retention after the second request.

Guard the callback with existing `applying` and generation checks to prevent recursive events and stale listeners. Any callback, zoom dispatch or setOption failure releases the instance, invalidates export and reaches `onError` through `interactionFailure`. This also closes the existing unguarded `refreshNavigatorMask` path. Double-click reset includes Box and follows the same failure handling. Reuse latest snapshot/viewport reprojection; do not add a post-layout session transaction or polling loop.

## File structure plan and handoff

All Workspace paths below are relative to `terminalpro/src/components/General/Table/Chart/`. One implementer owns this whole table; the parallel Range lane edits none of these paths. The controller owns manifests, breadth, evidence, commits and milestone checkboxes.

| Path | Responsibility |
| --- | --- |
| New `echarts/boxPlotTicks.ts` | Retained-source numeric tick step/range/nice arithmetic, bounded helpers. |
| New `echarts/boxPlotValueAxis.ts` | Semantic/full/visible plan and finite transport. |
| New `echarts/boxPlotAxisLayout.ts` | Two-pass footprints, density and measured collision selection. |
| New `echarts/boxPlotNavigator.ts` | Default miniature recomposition and native navigation options. |
| New `echarts/boxPlotNavigationWindow.ts` | Range extraction, visible categories/extrema and reprojection. |
| Modify `echarts/{boxPlotTypes.ts,boxPlotAdmission.ts,boxPlotDomain.ts,boxPlotAxes.ts,boxPlotGeometry.ts,boxPlotSeries.ts,boxPlotLayout.ts,boxPlot.ts}` | Admit new inputs and consume one plan consistently; keep B1/B2 semantics. |
| Modify `echarts/{lifecycle.ts,cartesianNavigator.ts}` | Optional callback join, errors/reset and Box inside-range synchronization. |
| Modify `echarts/EChartsHost.tsx` | Forward the optional callback through existing manual mount/update request construction and latest-prop refs; preserve existing resize notification flow. |
| New `echarts/lifecycleNavigation.ts`, only if needed for caps | Cohesive navigation binding/reprojection/error routing extraction, no independent state owner. |
| New `tests/unit/chart-compatibility/{boxPlotValueAxis.test.ts,boxPlotNavigator.test.ts,boxPlotIntegration.render.test.ts}` | Numerical source comparisons and actual ECharts options/geometry/zoom checks. |
| Modify `tests/unit/chart-compatibility/{lifecycle.test.ts,host.test.tsx}` | Controller-selected existing harnesses for callback forwarding/order, resize notification/new request, retained window and failed-interaction export invalidation. |

The added three axis responsibilities and `boxPlotLayout.ts`/`cartesianNavigator.ts` extend B3's reservation list explicitly. Do not add other production paths without controller agreement. Caps remain400 physical lines/file,300 logical units/file and50/function across whole modified files. Reuse the existing inventory/checker; controller registers every new path and current fork manifest. No cap exceptions, generated-code disguises, unrelated family refactors or new test harness.

## Verification and completion

Execute the existing compatibility Vitest configuration with the three new files and affected Box/lifecycle suites. Use the retained24-case oracle for numeric arithmetic across spans, constants, signed ranges and nonaligned bounds, adding only meaningful cases for collision-driven count reduction and zoom ticks. Test raw numbers independently of formatter text. Compare source scale outputs, not just a duplicate implementation's outputs.

Real ECharts rendering checks must cover vertical/horizontal Box, singleton integer/fractional scales, explicit bounds, one/all series hidden, all-missing groups, finite clipping, independent mini geometry at40px and numeric screen-x cropping without dropped category rows. Assert raw five-number summaries and SVG geometry/axis ticks, not only option existence. Navigator tests cover partial-window vertical autoscale, full reset, main-only zoom target, independent full overview, same-scope resize/update/legend retention, family reset and callback failure/export invalidation. Synthetic tests prove these contracts; they do not close live-data or appearance acceptance.

Run scoped Biome, existing combined complexity and the same strict TypeScript baseline/candidate comparison. The established compatibility config currently has3427 inherited diagnostics recorded in `artifacts/chart-range/r2-typing-candidate.log`; report exact additions and exits rather than calling that project typing clean. Independent review validates actual code and meaningful engine evidence. No identical broad rechecks solely for reporting.

B3c completion requires the whole adapter and safe lifecycle join, not another arithmetic-only scaffold. B3d then joins editor/session/gallery using these frozen interfaces. B4 retains real FMP financial values, controls, theme, refresh, save/reopen/export and matched original/replacement appearance. In particular review default horizontal miniature inheritance, rounded numeric endpoints, long-label density and navigator autoscale before accepting the milestone. Publish only completed reviewed outputs, update breadth/checklists at acceptance, and leave the previously published alpha unchanged until the completed-feature release gate.

**Remaining actual gaps:** this design has no rendered original default Box miniature evidence; two-pass final whitespace/tick-density equivalence needs owner visual review; explicit custom miniature series needs a concrete saved fixture if reachable in this Table/File caller. These are explicit B3d/B4 checks, not reasons to defer implementing the default integrated adapter. No production code, installs, builds, browser, provider requests or commits ran in this design task.

## B3c acceptance

B3c inactive Box axes/navigation and the existing-host adapter join are independently accepted at Workspace `b34984e46ee3fd942a5d80999dde77de1988896a`. Eighty tests across seven files, scoped Biome on 23 reviewed files and combined complexity pass. Canonical strict baseline/candidate each retain 3,427 identical inherited diagnostics, compiler exit 2, with no additions/removals. B3d activation, B4 real-FMP/application/visual acceptance and B5 publication remain open; the published alpha is unchanged.

Independent review: `artifacts/chart-box/b3c-review.md`; exact 23-path reviewed hash manifest: `b3c-revision-owned-hashes.json`. The slice changes 21 files; boxPlotLayout and boxPlotSeries were reviewed unchanged. Five new Box helpers and the host/lifecycle join remain inactive. Review repaired zoom tick density at span 149 and explicit-bound empty autoscale envelopes. The original numeric-category autoscale quirk, two-pass font/layout differences and default horizontal miniature runtime comparison retain explicit owner decisions at B4; custom miniature admission remains a B3d check. See [verification](../../../artifacts/reviewed/chart-box/verification.md).
