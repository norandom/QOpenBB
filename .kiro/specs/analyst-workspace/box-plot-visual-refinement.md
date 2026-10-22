# Box visual refinement

Correct observed Box defaults within the approved B4 parity scope. Candidate run 5 passes both application scenarios; original run 1 passes its capture scenario. These results establish usable controls and comparison inputs, not visual acceptance. Financial observations, five-number summaries, saved option paths, visible controls and dashboard flow remain the governing contracts.

## Evidence and requirements

Original source `38dffc3`, image `f48eb1c9`; candidate application source `ba98f00`, image `05c1c6fc`. Both vertical canvases are 619 by 284 at DPR 1. Horizontal original is 619 by 592; candidate is 619 by 593. Retained FMP provenance and comparisons are in [verification](../../../artifacts/reviewed/chart-box/verification.md).

1. Restore original default colour mixing, native legend outlines and category/group spacing; preserve explicit saved overrides and independent fill/stroke opacity.
2. Derive category label wrapping, rotation, collision thinning and reserved space from one plan consumed by layout and rendering. Feed the resulting numeric plot span to the existing original-derived tick arithmetic; do not hardcode financial intervals or the observed 200B limit.
3. Restore the original 18px default miniature with separate main-axis label space, full raw extent and independently generated raw numeric miniature labels. Retain navigation, legend, visibility, resize and export contracts.
4. Verify changes through source-backed tests, actual ECharts rendering and a freshly identified candidate with the retained FMP journey. Compare original/replacement captures in qView. B4/B5 remain open until remaining appearance and feature checks pass.

## Frozen source contracts

Retained enterprise Box theme around line 16797 blends palette fill toward chart background at ratio .7, with fillOpacity 1. Reuse `mixAppearanceColor` for missing fill only; explicit fill wins. Original series legend data around line 16504 carries fill/stroke and their respective opacities, stroke width and dash. Resolve independent alpha into native legend colours without applying a second global opacity. Preserve the effective original legend width rule: `min(2, series strokeWidth)` unless the legend marker explicitly overrides it (community source around 36387-36412). Inherit the series dash in the native legend marker.

Category defaults are inner padding .3, outer padding .15 and category-axis group padding .2. Resolve group padding from the effective category axis, retaining layered explicit overrides; it is not a series option. Original geometry formulas already exist and consume those values.

Retained community category labels default to on-space wrapping (around line 26757), wrap against actual band width (19791-19837), retain original text when wrapping fails, and use collision-driven power-of-two category thinning (18340-18373, 19287-19539). Preserve effective label minSpacing when explicitly supplied. Otherwise the original collision gap is zero for rotated labels and 10px for unrotated labels (16398-16403); the separate label spacing is an axis margin, not collision minSpacing. AxisLabel initializes it to 5px, but the effective Cartesian ChartTheme overrides it to 11px (around line 26324); retain the resolved theme spacing. At this viewport original visible category slots are 0,2,4,6,8,10; this is verification evidence, not a fixed selection rule.

Original category wrapping and total axis reservation use a 30% scene cross-dimension budget (community source 19934, 48928-48943 and 49141): width for a vertical category axis, height for a horizontal category axis. Preserve raw text when wrapping fails, but cap its reservation to that budget. Numeric endpoint overflow removal must respect disabled collision avoidance (20062).

Layout currently reserves the footprint at rotation zero and rendering separately selects 25 degrees. One shared label plan must determine both. Preserve explicit rotation and disabled collision avoidance. Use bounded layout convergence without modifying shared Cartesian layout or numeric arithmetic.

The shared resolved axis currently drops enabled, avoidCollisions, minSpacing and wrapping. Add a Box-only resolved axis type whose labels extend the existing labels with optional typed `enabled`, `avoidCollisions`, `minSpacing` and `wrapping`. Wrapping values are `never`, `always`, `hyphenate`, and `on-space` (original 28366). Use this type for both Box category and number appearances. The Box resolver supplies enabled/avoidCollisions true, category wrapping on-space and numeric wrapping never; minSpacing stays absent unless explicitly supplied by effective layers. Preserve generic and positional layer precedence. Box admission validates present fields. Existing typed fixtures may omit these fields and receive the same source defaults; no saved schema change or shared axis modification is needed.

Original miniature spans y537-555, main numeric text is at y518 and raw miniature labels at y560 in the observed horizontal view. Anchor miniature from chart chrome and its own label space, then separately reserve the main-axis footprint above it. A height-only change cannot resolve the overlap. Use existing `boxRawTicks`/`boxTickDensity` on full miniature extent and `String(value)` for its default numeric labels. Preserve existing explicit overrides and visibility policy; do not change other chart families.

Layout returns the final main grid plus optional `BoxNavigatorGeometry {left, right, bottom, height, labelSpace}`. The miniature bottom derives from unexpanded chrome; main bottom separately includes the main-axis footprint, navigator height, gap and miniature label space. Calculate category/numeric spans from this final grid, without subtracting a second reservation. Pass this geometry to the Box navigator. Shared decoration may be reused, but restore the planned main/overview grid, slider and mask consistently without a second placement algorithm. Apply raw miniature tick customValues after shared overview cloning, which replaces axis labels and drops customValues.

## Parallel ownership and join

All production paths below are under `terminalpro/src/components/General/Table/Chart/` in the Workspace fork. Shared interfaces are the existing resolved appearance style and a Box-only category plan passed from layout to axes. No saved schema change is required.

- Paint lane owns `application/boxPlotAppearance.ts`, `echarts/boxPlotSeries.ts`, the native legend style in `echarts/boxPlotLayout.ts`, and focused tests in `boxPlotProductionJoin.test.ts` and `boxPlot.render.test.ts`. It owns the category/group default correction consumed by layout. No geometry/axis/navigation edits.
- Layout lane owns `echarts/boxPlotAxisLayout.ts`, `boxPlotAxes.ts`, `boxPlotNavigator.ts`, `boxPlot.ts`, and any cohesive new Box-only category-plan helper. It owns focused tests in `boxPlotValueAxis.test.ts`, `boxPlotNavigator.test.ts`, `boxPlotIntegration.render.test.ts` and a new category-plan test if needed. It must not edit paint-lane files or shared Cartesian modules. Register new production files before acceptance.
- Controller first owns `echarts/boxPlotTypes.ts` and `boxPlotAdmission.ts` for the typed label-policy extension, optional-field admission and navigator geometry interface. These interfaces freeze before paint/layout fan-out. Controller also owns browser scenarios, source pins, complexity inventory, evidence, documentation, integration checks, commits and candidate builds. Workers freeze before the controller's shared verification. One heavy suite/build runs at a time.

## Completion checks

- [x] Independently review this bounded contract before production edits. Astra approved the amended Box-only type/admission, source defaults and final navigator geometry boundary; runtime appearance remains unaccepted.
- [x] Paint lane: prove original light/dark defaults, explicit override precedence, proper axis option source, independent native legend paint and measured widths with actual engine output.
- [x] Layout lane: prove shared wrapped/rotated label geometry, collision thinning and explicit overrides, numeric-domain response to available span, singleton/empty recovery, and miniature/main-axis separation in actual rendering.
- [x] Run the relevant existing Box application, mapper/navigation and integration checks once at the join; add prior-family checks only for changed shared behavior.
- [x] Enforce whole-file caps of 400 physical lines, 300 logical units and 50 units per function with the maintained inventory. Tests/docs are exempt. Split cohesive responsibilities rather than compress code.
- [x] Independent code review, scoped formatting and inherited-type diagnostic comparison before source acceptance. No new inherited-diagnostic suppression.
- [ ] Build the accepted source using Dagger, run the retained-FMP browser journey against that identified image and compare the six matching reference views; keep original source and replacement identities separate.
- [x] Sync reviewed samples, README/docs checkboxes and breadth before per-task commits/pushes. Dispatch publication only after the completed feature gate.

Review constraints: resolve leaf options with existing generic/positional layer precedence and runtime axis options. Category wrapping/thinning changes display labels only; preserve raw group slots, category domain, navigation membership and summaries. Band width uses the same source defaults and current navigation window as box geometry. Raw miniature formatting also applies to singleton constant transport.

## Fresh-image repair: category collision and final plot bounds

Candidate `1458dbd`, built in CI `39732295616`, passed the synthetic browser scenario but stopped in the retained-FMP wheel-zoom check. Its default vertical capture still ends at 150B and shows three unrotated fiscal labels; the original ends at 200B and retains alternating rotated labels. B4 remains open.

The original checks rotated label boxes in two dimensions. The replacement checks projected one-dimensional intervals, which rejects the final long label in the actual 11-group sample. The earlier 12-group test removes that label when thinning and misses the defect. Original caller-generated category options also specify `minSpacing: 5`; preserve this at the Box caller layer, with explicit generated, positioned, saved-family and runtime values retaining their precedence.

Wheel zoom did change the selected range to about 90.9%. ECharts then shrank the main plot around labels despite `containLabel: false`, reducing the actual width below the planner's width. The miniature already disables this second layout pass. Establish the main-grid discrepancy with actual engine bounds before setting Box main `outerBoundsMode: none`.

- [x] Independently review the bounded repair before production edits. Astra confirmed the two-dimensional collision contract, caller precedence and ECharts outer-bound behavior on 2026-10-22.
- [x] Collision lane: own `boxPlotCategoryPlan.ts` and its existing unit test; implement the original two-dimensional collision contract and test the exact 11-group boundary case. Preserve raw slots, wrapping and navigation membership.
- [x] Bounds lane: own `boxPlotAxisLayout.ts` and `boxPlotIntegration.render.test.ts`; prove the actual/planned grid discrepancy at 619 by 593 with a modest wheel-sized zoom, then enforce one layout owner and verify plotted width and edge behavior.
- [x] Controller: own the Box appearance caller-default merge and `boxPlotProductionJoin.test.ts`; preserve explicit zero and positional/runtime overrides. Shared caller generation, numerical ticks and statistical summaries remain unchanged.
- [ ] Retain the 400/300/50 production caps, independent review and focused integration/typing checks. Reuse the browser scenario unchanged against a new identified image; source acceptance alone cannot close B4.
