# H2 inactive histogram mapper

Implement a pure histogram projection using the accepted H1 bins and the existing ECharts 6.0.0 custom-series renderer. Keep it disconnected from production routing. This supplement resolves H2's type and renderer seams in [the histogram design](histogram-design.md); H1's interface and numerical decisions remain unchanged. Independent review of this supplement and acceptance of H1 precede H2 implementation.

## Reviewed interface changes

Retain `HistogramMappingInput` from the main design, with two additions:

```ts
// Add to style.series, alongside its existing Pick fields:
readonly fill?: string;
readonly stroke?: string;

// Add to context:
readonly legendSelection?: Readonly<Record<string, boolean>>;

export type TranslateHistogram =
  (input: HistogramMappingInput) => CartesianTranslationResult;
```

`fill` and `stroke` are resolved saved-series overrides; omission selects the first fill/stroke in `style.application.palette`. Existing `ResolvedApplicationSeries` contains widths/opacities but no colors, so its `Pick` alone would lose saved overrides. H3 resolves option-layer precedence before calling the mapper. Neither palette nor explicit colors may be replaced by a second color authority.

Legend selection is keyed by the selected X field ID. Use that ID as the ECharts series `name`; encode a collision-safe series `id` from `["histogram", fieldId]`. The legend formatter displays **Frequency**, matching the original proxy's `yName` and histogram legend implementation. The range row in the tooltip uses the selected field's display label, falling back to its ID when absent. Do not use the field label as the legend label. Retain the legend entry when hidden; hide geometry without changing H1 counts, bins or source metadata.

All other input fields retain their original types. Import `ResolvedXyAxis` as numeric-axis appearance plus optional min/max. It does not grant reuse of XY assignment, scale-domain or minimum-visible-item logic. `context.display.numericAxis` formats numeric ticks and native histogram tooltip values; `seriesLabel` formats frequency labels. The Workspace custom `tooltipNumber` formatter is inactive here. Category/fiscal formatting does not alter bin values.

## Admission and immutable projection

Validate through the existing snapshot boundary and use its returned validated copy. The existing `"xy-coordinates"` policy is currently the only policy that permits empty numeric selections; H2 may reuse that structural validation policy without changing the shared validator. H3 owns any later naming/generalization.

Choose the first selected numeric descriptor in `selectedColumnIds` order, not descriptor-array order. Additional numeric fields contribute neither geometry nor extents. Map snapshot rows to selected values or null, call H1 once and preserve its diagnostic paths and repair decision. Empty selection is supported empty geometry; H1 input options still require validation. No category aggregation, provider normalization, saved-state reads or mutation belongs in H2.

Validate known style/context fields, including inactive supplied values, before drawing. Require finite nonnegative sizes, widths and dash lengths, valid opacity ranges, nonempty palettes, finite viewport dimensions, integer precision 0-20, callable display callbacks and boolean legend selections. Empty viewport dimensions may produce an empty layout but never NaN geometry. Validate optional colors as strings and apply independent fill/stroke opacity without multiplying either into text opacity. Catch unsafe input access and rendering projections as diagnostics; do not use `any` or cast a fabricated XY input to reuse a helper.

Reuse `xyApplicationDiagnostics` for the exact shared application shape and `xyAxisCheck` for axis appearance. Add histogram-specific checks for series and context. Numeric X positions are bottom/top; numeric Y positions are left/right. Other well-formed axis types return unsupported; malformed positions/bounds return invalid. Two explicit bounds require min < max. For an affected source domain `[domainLow, domainHigh]`, only `min > domainHigh` or `max < domainLow` excludes the entire domain and yields supported empty geometry and an empty affected axis, preserving the established XY repair behavior. A minimum below `domainLow` or maximum above `domainHigh` extends the axis normally and retains geometry; equality at a domain endpoint does not trigger exclusion.

## Renderer contract

Use one `CustomSeriesOption` with `type: "custom"`, `coordinateSystem: "cartesian2d"`, `clip: true`, `animation: false`, dimensions `["lower", "upper", "frequency"]` and encode `{x: [0, 1], y: 2}`. Never use category bar width or a statistical histogram transform. Empty intervals remain outside the series data.

Each occupied datum contains `value: [lower, upper, frequency]` and transient metadata with selected descriptor, interval index, observation indices and the corresponding snapshot row IDs. This metadata is not persisted. Draw groups in ascending lower-bound order, then upper-bound order, retaining interval identity and observation membership; the original `createNodeData` sorts drawn nodes by X. H1's returned group ordering remains unchanged.

The `renderItem` callback converts `[lower, 0]` and `[upper, frequency]` through `api.coord`, derives the finite rectangle from those pixel endpoints, and returns no geometry for a zero-height or empty/clipped datum. Adjacent bins meet at their numeric boundary; no category gap is introduced. Return a native rect with independent fill, stroke, lineWidth, lineDash and shadow style. Preserve sharp corners for this slice's original reachable controls.

Center enabled labels inside the full bin rectangle, using frequency through `display.seriesLabel` and the resolved label font/color. The original labels are centered, not above bars. Attach text to the rect with `textContent`/`textConfig`, or return an equivalent group with a noninteractive text child. Keep labels independent of fill opacity. Series clipping must apply to rectangles and labels; do not shift labels to the center of the remaining clipped portion. Tooltip hit-testing must address the occupied datum.

Use `clip: true` for the native plot clip. `graphic.clipRectByRect` is available but must not be used to create a new stroked edge at a viewport boundary. Optional early rejection of wholly outside rectangles is safe. Retain the full rect shape and let the plot clip preserve the original edges and label anchor.

Tooltips have one range row (`field label: formatted lower - formatted upper`) followed by `Frequency: formatted count`. Escape labels and callback results with `escapeHtml`. Use item tooltips even if a saved common tooltip mode says shared/compact: histogram has the original native range/Frequency content, not the Workspace multi-series callback. Honor tooltip enabled and keep saved inactive mode unchanged. Do not attach USD to frequency or scale the input amounts.

## Extents, layout and honest H2 limits

Automatic X input extent comes from the first calculated lower endpoint and last calculated upper endpoint, including empty bins, as the original `getSeriesDomain` does. Y starts at zero and includes the largest occupied frequency. Do not derive X from all selected columns, zero-seed X, or drop empty boundary intervals. Explicit supplied min/max override the corresponding automatic side.

For H2's isolated mapper, choose finite nondegenerate automatic axes enclosing these domain endpoints and preserve both explicitly supplied endpoints exactly. Automatic tick spacing/outer nice rounding is not yet established as pixel-identical to the original. H2 tests must distinguish raw domain/interval geometry from nice axis bounds; original-versus-replacement tick/extent comparison remains an explicit H3/H4 acceptance obligation. Do not claim full visual parity from isolated geometry tests.

Unordered explicit intervals remain ordered inputs to H1 membership. When their first/last endpoints form a valid X extent, preserve that domain and clip outlying geometry; do not replace it with all-bin min/max. A reversed/collapsed first/last domain cannot establish this mapper's valid numeric axis and returns an explicit diagnostic. This rendering limitation does not change H1 acceptance and must remain visible in H2 evidence and the later original-source comparison.

Use the shared font/padding/title/legend/background values to build a histogram-local layout. Empty bins produce no legend hit targets; the single series legend remains keyed to the field. Native legend selection must not change the source bin calculation. H3 owns navigation, mini-chart and interval-window autoscaling; H2 must not invoke `xyNavigationWindow` or `cartesianNavigator`.

## Exact helper reuse and gaps

| Existing export | Decision |
| --- | --- |
| `cartesianDisplay.fontStyle`, `escapeHtml` | Reuse for native fonts and safe tooltip text |
| `cartesianLayout.measureText` | Reuse for caption/legend layout; it accepts the resolved font shape |
| `cartesianGrid.alternatingGrid` | Reuse; importing this module already registers `qopenbbGrid` |
| `xyApplicationDiagnostics`, `xyAxisCheck` | Reuse matching shared shapes; validate histogram series separately |
| `xyLayout`, `xyAxes`, `xySeries`, `xyEmptyAxes` | Do not call: they require XY assignments and derive observation/legend domains |
| `applicationLayout`, `applicationAxes`, `applicationSeries` | Do not call with fake family/category values; their contracts assume Cartesian families |
| `cartesianAxes.niceNumberExtent` | Private export and coupled to its file; no H2 shared-file edit or import workaround |
| `color.parse`, `color.modifyAlpha` from ECharts | Available for independent fill/stroke opacity when needed |

For alternating grid lines, emit the same `qopenbbGrid.axes` entries as XY, with xAxis/yAxis, width and original style arrays, and disable the corresponding native splitLine. Use native splitLine for uniform dash arrays. Numeric-axis assembly must retain titles, tick lengths/colors/widths, line visibility, labels, rotation, positions and grid styles.

Source inspection confirms ECharts 6.0.0 `index.js` registers `CustomChart`; `CustomSeriesOption` exposes renderItem, encode, coordinateSystem and clip. Its default clip is false, so explicit true is mandatory. `coord/cartesian/prepareCustom.js` exposes actual plot coordinates and `api.coord`; `CustomView.js` applies the plot clip. No new renderer registration or dependency is needed. Public `coordSys` TypeScript types expose only `type`, so any optional rectangle inspection needs a structural type guard rather than an unchecked geometry cast.

Original source anchors are retained Charts bundle 45032-45120 (rectangles and centered labels), 45205-45269 (range/Frequency tooltip), 45303-45325 (legend label), and 45000-45008 (domain). These findings are source inspection only; H2 must establish actual-engine behavior.

## Ownership and acceptance

H2 owns only new `echarts/histogram.ts`, `histogramTypes.ts`, `histogramAdmission.ts`, `histogramStyleValidation.ts`, `histogramAxes.ts`, `histogramSeries.ts`, `histogramLayout.ts`, `histogramTooltip.ts` and focused `tests/unit/chart-compatibility/histogram.test.ts`, `histogram.render.test.ts`, `histogram.fixtures.ts`. Add only the cohesive modules needed. `histogramNavigator.ts` remains H3-owned. H1 files and all shared production helpers are read-only. Controller owns scope inventory and commits.

Use the existing compatibility Vitest configuration at one worker and scoped TypeScript checking. Actual ECharts SVG SSR tests must inspect rectangle endpoint positions and widths/heights, centered labels, clipping, independent opacity, saved color overrides, top/right axes, explicit bounds, hidden/restored legend, escaped tooltip rows, and empty-selection recovery. For each axis, verify positive extension cases (`min < domainLow`, `max > domainHigh`) retain geometry and the supplied endpoint, and negative exclusion cases (`min > domainHigh`, `max < domainLow`) produce empty geometry and an empty affected axis. Check endpoint equality and removal of an excluding bound restores geometry. Include unequal/gapped bins, empty outer intervals, repeated/signed values and the H1 repair case. Assert the rendered SVG contains no NaN/Infinity, but do not mistake that assertion for coordinate correctness.

Run no image build or provider request for H2. Independent review must compare H1 membership and real-engine geometry against independent expected values, inspect the inactive routing boundary, and verify whole-file caps of 400 physical lines, 300 logical units and 50 per function through the existing explicit-fork-scope checker. H2 acceptance does not close the deferred axis/visual comparison, H3 integration or H4 real-FMP application gate.
