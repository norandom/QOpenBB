# X2 inactive numeric-coordinate mapper

Implement `translateXy` as a pure projection of a validated snapshot, X1 assignments and effective appearance. It must remain disconnected from production routing. The output establishes numerical and drawing contracts for the later session adapter; it creates no persistence, editor or transaction owner. [X1](xy-assignment-design.md) owns pairing and [source research](xy-chart-research.md) owns original-behavior evidence.

## Input and output

Define the following in `echarts/xyTypes.ts`, importing existing types rather than copying their definitions:

```ts
interface ResolvedXyStyle {
  readonly common: Pick<
    ResolvedCartesianStyle, "textColor" | "fontFamily" | "fontSize" | "precision"
  >;
  readonly application: Omit<ResolvedApplicationAppearance, "axes" | "series">;
  readonly axes: {
    readonly x: ResolvedXyAxis;
    readonly y: ResolvedXyAxis;
  };
  readonly series: ResolvedApplicationSeries;
  readonly maxSize: number;
  readonly overrides: Readonly<Record<string, CartesianSeriesStyle>>;
}
interface ResolvedXyAxis {
  readonly appearance: ResolvedApplicationAxis;
  readonly min?: number;
  readonly max?: number;
}
interface XyMappingInput {
  readonly snapshot: ChartSnapshot;
  readonly chartType: XyChartType;
  readonly assignments: readonly XySeriesAssignment[];
  readonly style: ResolvedXyStyle;
  readonly context: {
    readonly observations: { readonly kind: "raw-observations" };
    readonly display: ChartDisplayPolicy;
    readonly viewport: { readonly width: number; readonly height: number };
    readonly legendSelection?: Readonly<Record<string, boolean>>;
    readonly labels: "category" | "y";
  };
}
type TranslateXy = (input: XyMappingInput) => CartesianTranslationResult;
```

`series.markers.size` is scatter diameter or bubble minimum diameter; `maxSize` is the bubble maximum diameter. Shapes use `series.markers.shape`. `overrides` and native legend selection are keyed by Y column ID, which X1 assigns at most once. ECharts series IDs use a deterministic encoding of family and the full assignment tuple, while legend names use Y IDs and a formatter displays `Y label vs X label`. Do not identify a series by its display label.

The interface removes duplicate common palette, background, legend and caption fields. `application.palette` alone supplies palette fills/strokes; `application.background`, `application.title`, `application.subtitle` and `application.legend` alone supply their corresponding appearance. `common` supplies only global text defaults and precision; explicit caption/axis/label fonts take precedence over global text defaults. Series palette index is its assignment index before legend filtering.

For Y override `o` and that palette index, point fill resolves as `o.markerFill ?? o.fill ?? o.color ?? paletteFill`; stroke resolves as `o.markerStroke ?? o.stroke ?? o.color ?? paletteStroke`; stroke width resolves as `o.markerStrokeWidth ?? o.strokeWidth ?? series.markers.strokeWidth`. `series.markers.strokeWidth` is the effective XY outline authority. The inherited `series.strokeWidth` is inactive in this projection; the later appearance adapter must resolve saved top-level XY `strokeWidth` into `markers.strokeWidth`. Fill/stroke opacity and dash come from `series.fillOpacity`, `series.strokeOpacity` and `series.lineDash`. Inherited `series.connectMissingData` and per-Y `lineWidth` are inactive, retained inputs and never draw connecting lines or override marker width.

Validate supplied known fields even when inactive: wrong types, nonfinite numbers, negative dimensions/widths, invalid opacity ranges and malformed nested structures are invalid. A well-formed but unsupported shape or axis scale returns unsupported. Unknown extra fields are ignored without mutation. Inactive numeric `lineWidth` must be finite and nonnegative, `connectMissingData` must be boolean, and `series.strokeWidth` must be finite and nonnegative. A short palette cycles independently within its nonempty fills/strokes arrays; empty arrays are invalid.

`context.labels` is explicit because the snapshot always has a category identity, including generated categories. The later adapter must distinguish a genuinely selected Labels column from the original generated-category sentinel. `category` formats `row.category`; `y` formats the raw Y value. The mapper must not infer this choice from a label's spelling.

The result reuses `supported/options`, `invalid/diagnostics`, and `unsupported/diagnostics`. Empty assignments or no plottable rows produce supported empty geometry without fabricated points. The later session adapter owns the original empty-chart message. Invalid input produces no partial options. Valid but unimplemented modes, such as logarithmic axes, produce unsupported diagnostics rather than silently changing scale.

## Admission and observations

Validate snapshot input through the existing snapshot boundary and validate all supplied resolved style fields at the mapper boundary. Assignments must reference selected numeric descriptors, use distinct identities within each group, have unique Y identities, and include size only for bubble. Preserve their supplied order; do not rerun pairing or silently repair assignments. X1's ordinary incomplete-group result is valid.

Only finite numeric X and Y values produce plotted points. Missing or null coordinates omit that point while preserving other rows and series. Retain row ID, snapshot row index, category, X/Y/size descriptor identities and raw values in transient datum metadata. The index addresses the supplied snapshot, which may already be aggregated; it is not an original grid/provider row index. Duplicate category labels and duplicate coordinates must remain separate observations. Data values and metadata never multiply descriptor scales or apply display rounding.

Compute each bubble size domain from every finite size value in that series' snapshot rows, including a row whose X or Y is missing. This matches the original independent data-column domain processing. Null or absent size does not enter the domain and uses the minimum marker diameter for otherwise plottable coordinates. Zero and negative sizes enter the domain unchanged. For minimum diameter `a`, maximum diameter `b`, domain `[lo,hi]`, and finite size `v`:

```text
lo == hi: diameter = (a + b) / 2
otherwise: diameter = a + (v - lo) / (hi - lo) * (b - a)
missing size: diameter = a
```

Use a numerically safe equivalent where subtraction or interpolation would overflow; reject derived nonfinite geometry if safety cannot be established. Do not use absolute values, square roots or a zero-based size domain. Do not reorder reversed user size endpoints merely because the control calls them minimum and maximum. Zero resulting marker size is invisible, consistent with the original.

X2 does not accept a custom bubble-domain override: the original internal `marker.domain` serves cross-filtering, outside the ordinary caller scope. Its extrapolation semantics remain documented for a later cross-filtering implementation.

Legend visibility changes drawn series and visible coordinate extents, but must not change a series' bubble size domain. Rows remain in original order. No interpolation, stacking, area geometry, category aggregation or synthetic values belong in this mapper.

## Drawing and helper reuse

Use ECharts scatter geometry for both families, with explicit numeric bottom X and left Y axes. Derive each axis from the assigned coordinate columns, never from size columns or row indexes. Preserve shared font/grid/tick configuration through `axis.appearance`. Each `min`/`max` is optional; present values must be finite numbers. Explicit endpoints take precedence over computed extents and automatic nice rounding on that side. An absent side remains automatic. Two supplied endpoints require `min < max`; equal or reversed bounds are invalid, never swapped. For a single explicit bound beyond all observations, preserve that bound and leave the other endpoint automatic; do not clamp data or synthesize an observation. Renderer tests must verify a finite nondegenerate automatic opposite endpoint, or fail admission with a diagnostic until a safe expansion rule is established. The later adapter owns normalization of legacy bounds; the mapper accepts only this explicit contract.

Do not reuse `cartesianAxes.numberExtent`, whose all-selected-column and zero-seeded domain would change XY observations. Axis range expansion and tick placement require focused original-versus-mapper evidence before claiming visual parity.

Reuse `cartesianMarkers.markerSymbol` and `markerDimensions`: they already retain the original cross, plus, triangle and heart paths and nominal dimensions. Validate supported shapes before calling the helper. Circle, square, cross, diamond, plus, triangle and heart must work in both families. Do not substitute an ECharts built-in triangle. Size callbacks use precomputed diameter plus shape dimensions; disabling markers hides geometry without deleting raw metadata.

Reuse `cartesianDisplay.fontStyle` and `escapeHtml`, and `cartesianLayout.measureText`. Existing `applicationLayout` assumes category/value axes and a Cartesian family; `cartesianGrid` requires full `application.axes.category/number`. Neither is callable with the XY input. Do not pass a fake family or map X to a category axis merely to satisfy those signatures.

Implement self-contained bounded assembly in `xyLayout.ts`/`xyAxes.ts`: background from `application.background`, layout measurements from captions/legend/padding plus `measureText`, and grid mapping directly from `axes.x.appearance` to `xAxis` and `axes.y.appearance` to `yAxis`. Uniform grid styles use native `splitLine`; alternating dash styles emit the existing registered `qopenbbGrid` option with entries `{axis: "xAxis" | "yAxis", width, styles}` and disable native split lines on that axis. Importing `cartesianGrid` registers that geometry-neutral renderer; do not call its category-based assembler. No edits to shared production helpers are included in X2.

Triangle anchoring is part of the marker contract. Original `Marker.anchor` returns `{x:0.5,y:0.5}` for triangle (Charts 24487-24495), while its unit vertices have vertical bounds `[0,0.87]` (24412-24417). Therefore its visual bounding-box center is `-0.065 * diameter` above the datum. Apply `symbolOffset: [0, -diameter * 0.065]` together with `[diameter, diameter * 0.87]`, matching the existing Cartesian marker correction. Bubble offsets must use each point's computed diameter, not the series minimum. A renderer test must compare apex/base position against the numeric datum center for at least two bubble diameters and scatter; option-path existence alone is insufficient.

Use `tooltip.trigger = "item"` and datum metadata for point lookup, not category-axis indexes or label matching. Tooltip rows use descriptor display names and raw X/Y/size values with `display.tooltipNumber`; omit missing size from numeric rows. Preserve the caller's descending-value order and escape formatted content. Labels use `display.seriesLabel`. Label and tooltip formatting must not alter coordinates or diameters. Units remain descriptor metadata; do not invent units for absent metadata or describe EPS as a currency total.

Both themes inherit circle/7-pixel scatter defaults and circle/7-to-30-pixel bubble defaults, fill opacity 0.8, stroke width 1 and disabled labels. These are resolved upstream into the explicit style; the mapper never reads saved option paths or theme names. Use supplied fills/strokes, background, typography and effective overrides.

## Ownership and next adapter

X2 owns new `echarts/xy*.ts` files and focused XY mapper tests only. Suggested responsibilities are admission/types, observation and size projection, series/labels/tooltips, axes/layout, and public assembly. Split by these responsibilities as needed. Every production file must pass 400 physical lines, 300 logical units and 50 units per function. Extend the existing maintained-file inventory; do not create another checker.

X3 resolves effective XY appearance and pairing from the existing option-state baseline and caller-generated options. It uses the existing widget session, transaction owner and stamps, then passes the frozen input above. Aggregation of selected X/Y/size columns occurs upstream before X1 assignment and snapshot mapping. X3 does not introduce a second store, serialize resolved style, or let rendering mutate saved options.

Navigator, mini-chart, wheel/pan/double-click reset and production routing remain X4 integration duties. This boundary does not authorize removing their controls. The numeric-X navigator must consume the same raw observations and size-domain rules; ordinary categorical overview cloning is not accepted by inference.

## Evidence required

Focused tests must cover both grouping modes through X1 output, both families, multiple series, trailing groups, duplicate labels/coordinates, null X/Y, missing/null/zero/negative/equal sizes, independent size domains, size values on unplottable rows, extreme finite arithmetic, both palettes, all marker shapes, labels/tooltips, empty geometry, legend identity, immutable inputs and malformed inputs. Axis cases include automatic, minimum-only, maximum-only, two-sided bounds, bounds excluding every observation, and invalid equal/reversed/nonfinite endpoints independently on X and Y. Appearance cases must prove each override precedence, unequal palette lengths, inactive line settings, and invalid-versus-unsupported classification. Verify type checking and production caps with an explicit fork manifest. Tests that assert only generated option structure do not establish the renderer's point coordinates, symbol dimensions or item-tooltip association; include a bounded render test before accepting X2 geometry.

Remaining visual uncertainties are exact numeric-axis padding/nice ticks, label collision/placement, marker path raster equivalence, and original large-data aggregation above the 10,000-item default. Preserve these as later acceptance checks, not unsupported claims of completed application fidelity. Null-size fallback and equal-domain midpoint are established source contracts; their application rendering remains to be tested.
