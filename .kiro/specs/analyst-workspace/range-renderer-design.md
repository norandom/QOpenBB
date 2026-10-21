# Range Bar renderer core

R2 independently accepted, 2026-10-21. R2 implements an inactive Range Bar mapper against an explicit resolved value scale. It consumes the accepted [R1 min/max helper](range-chart-plan.md), preserves category/measure identity and emits grouped interval geometry with endpoint labels and tooltips. Range Area follows as a separate mapper. Box retains shared application integration ownership and remains the delivery milestone.

R1 prerequisite: Workspace `0bc5109671c3ca1af43b863a0da3616ab78ae968`, independently accepted. Current source observed at design freeze: Workspace `bca180284cefb7848b052dd4b8a4160fe0c0d5e8`, root `a37255cf3d0d5f2d94b16c9d6b38066ab3fb65b6`. Source citations G/C/M use the retained bundle identities in `artifacts/chart-range/source-contract.md`; additional bounded geometry findings are in `artifacts/chart-range/r2-source-notes.md`. This design establishes no automatic-axis or appearance parity. No production, tests, browser, builds or provider requests ran during authoring.

## Frozen boundary

R2 returns a renderable ECharts option for a caller-supplied plot rectangle, axes and value scale. It owns projection, interval drawing, endpoint labels, numeric/category tick transport and tooltip formatting. The caller owns capture, setup aggregation, effective defaults, original automatic nicing/tick selection, outer layout, axis titles/grid, chart captions/background/legend, navigator and lifecycle. Those are composition responsibilities, not unavailable controls in an active application: R2 is unreachable from application registries.

New `echarts/rangeBarTypes.ts` defines the following contract. Production paths in this document are relative to `vendor/workspace/terminalpro/src/components/General/Table/Chart/`.

```ts
import type { EChartsOption } from "echarts";
import type { ResolvedApplicationAxis, ResolvedApplicationSeries } from "../application/appearanceModel";
import type { ChartDisplayPolicy } from "../application/types";
import type { ChartSnapshot, SnapshotColumn, SnapshotDiagnostic } from "../compatibility/snapshotTypes";
import type { RangeSummary } from "../compatibility/rangeSummary";

export interface ResolvedRangeBarScale {
  readonly min: number;
  readonly max: number;
  readonly ticks: readonly number[];
}
export type RangeBarAxisPaint = Pick<ResolvedApplicationAxis,
  "fields" | "labels" | "ticks" | "lineEnabled">;
export interface RangeBarFieldStyle {
  readonly fill: string; readonly fillOpacity: number;
  readonly stroke: string; readonly strokeWidth: number;
  readonly strokeOpacity: number; readonly lineDash: readonly number[];
  readonly lineDashOffset: number;
  readonly label: ResolvedApplicationSeries["labels"] & {
    readonly placement: "inside" | "outside";
    readonly spacing: number; readonly padding: number;
  };
}
export interface RangeBarMappingInput {
  readonly snapshot: ChartSnapshot;
  readonly style: {
    readonly direction: "vertical" | "horizontal";
    readonly categoryAxis: RangeBarAxisPaint;
    readonly numberAxis: RangeBarAxisPaint;
    readonly valueScale: ResolvedRangeBarScale | null;
    readonly band: { readonly paddingInner: number; readonly paddingOuter: number;
      readonly groupPaddingInner: number };
    readonly fields: Readonly<Record<string, RangeBarFieldStyle>>;
    readonly tooltip: { readonly enabled: boolean;
      readonly mode: "single" | "shared" | "compact" };
  };
  readonly context: {
    readonly display: ChartDisplayPolicy;
    readonly viewport: { readonly width: number; readonly height: number };
    readonly plot: { readonly left: number; readonly top: number;
      readonly width: number; readonly height: number };
    readonly legendSelection?: Readonly<Record<string, boolean>>;
  };
}
export interface RangeBarDatum {
  readonly groupSlot: number; readonly count: number;
  readonly summary: RangeSummary | null; readonly sourceRowIds: readonly string[];
}
export interface RangeBarProjection {
  readonly groups: readonly { readonly slot: number; readonly category: string | number;
    readonly rowIds: readonly string[] }[];
  readonly fields: readonly { readonly descriptor: SnapshotColumn;
    readonly paletteIndex: number; readonly enabled: boolean;
    readonly data: readonly RangeBarDatum[] }[];
  readonly dataExtent: readonly [] | readonly [number, number];
}
export type RangeBarProjectionResult =
  | { readonly status: "resolved"; readonly projection: RangeBarProjection }
  | { readonly status: "invalid" | "unsupported";
      readonly diagnostics: readonly SnapshotDiagnostic[] };
export function projectRangeBar(snapshot: ChartSnapshot,
  legendSelection?: Readonly<Record<string, boolean>>): RangeBarProjectionResult;
export type RangeBarTranslationResult =
  | { readonly status: "supported"; readonly options: EChartsOption;
      readonly projection: RangeBarProjection }
  | Exclude<RangeBarProjectionResult, { status: "resolved" }>;
export function translateRangeBar(input: RangeBarMappingInput): RangeBarTranslationResult;
```

The public projection step lets a future scale resolver consume the same summaries; translation calls that pure step itself and retains no mutable projection cache. Neither step updates saved state. No native statistical transform, Box summary call, feature flag or application import of R2 is allowed.

## Admission and projection

Use the existing `validateSnapshot(snapshot, "xy-coordinates")` structural/finite boundary. Accept normalized `flat`, `transformed` and `grouped` sources; pivot and remote-page modes return unsupported in this core. The ordinary setup aggregate projection uses sourceMode=grouped while retaining ordinary SnapshotRow categories, so admitting grouped does not introduce a hierarchical axis or another aggregation step. Group copied rows by the existing string/number category identity in first-encounter Map order. Numeric 1 and string "1" remain distinct even if displayed alike; retain blank and all-null categories. Date/default/missing-category normalization and pre-statistics aggregation already belong upstream. Do not aggregate or rescale again.

Numeric fields follow selectedColumnIds order, independent of descriptor order/labels. For every category/field call R1 once with ordered observations, mapping absent numeric values to null. Retain count, nullable summary, every group's source row IDs and each datum's contributing row IDs. Null summary emits no interval or endpoint labels, while other fields and the category slot survive. Hidden fields retain summaries/palette identity but occupy no visible group slot. `dataExtent` is the raw finite min/max over enabled non-null summaries; it is empty when none exist. No numeric fields is supported empty output. Prefix R1 diagnostics with group slot/field ID and fail atomically.

Validate and defensively copy boundary data before producing callbacks; reject sparse arrays, accessors, cycles, nonfinite numbers and malformed identities without partial options. Reuse SnapshotDiagnostic and established admission patterns, with `invalid-range-bar` for malformed data/paint/scale/geometry and `unsupported-range-bar` for valid but unsupported axis/source/mode semantics. Do not import Box modules or create another validation framework. Every selected field has exactly one style entry; legend map keys are known field IDs and values are booleans.

Colors/font names are nonempty strings; widths, spacing, padding and font sizes are finite nonnegative; opacities and band paddings are in [0,1], category paddingInner<1 and paddingOuter<=.5. Font weight/style retain the existing resolved vocabulary. Viewport and plot dimensions are finite positive; plot offsets are nonnegative and the rectangle fits the viewport. Axis types must be category/number with positions compatible with direction. Number/time/grouped category axes are unsupported rather than coerced. Explicit label rotations are finite; unresolved automatic label rotation is unsupported in this core, because caller layout must resolve it before activation.

## One explicit scale for coordinates and ticks

valueScale is the caller-resolved final semantic display domain, independent of raw dataExtent. A supplied scale requires finite min<=max and a dense strictly increasing finite tick array inside [min,max]. For distinct bounds require finite positive span. An empty tick array is permitted when the resolver intentionally supplies no numeric ticks. The mapper must not insert zero, expand an equal semantic endpoint, call niceNumberExtent or let ECharts choose financial ticks. Supplied scale bounds may clip observations; do not replace summaries or dataExtent with clipped values. Reject nonfinite coordinate normalization before returning options, including overflow for otherwise finite extremes.

valueScale=null means the caller resolved no effective numeric domain. It is valid with empty observations or with finite observations excluded by a one-sided bound. Preserve all raw summaries/dataExtent but suppress financial geometry, numeric labels/ticks/pointer labels, endpoint labels and tooltip content. Emit an internal [0,1] transport solely for finite empty axes; never pass its values to financial display callbacks. Conversely, empty observations may have a nonnull scale from explicit bounds: render the supplied numeric ticks/labels and retain no data geometry. Do not infer scale presence from observations or hidden-field selection.

For distinct semantic bounds map min/max directly to the value axis with scale=true, onZero=false and supplied ticks through both axisLabel.customValues and axisTick.customValues. If final semantic min=max=c, keep that equal domain in input and preserve the raw projection, but use internal transport [0,1]; map every finite raw endpoint to .5, as original unclamped ContinuousScale.convert does for an equal final domain (M12182-12216). A supplied singleton tick [c] maps to internal [.5], displayed as raw c. Equal bounds permit only [] or [c] as ticks. Raw summary, endpoint labels and tooltip values remain unchanged even when a bound places unequal source endpoints onto the same midpoint. Do not let transport values enter financial metadata or display callbacks. A singleton observation v may have a distinct caller-resolved display domain or an equal final domain [v,v]; R2 supports both without choosing which applies.

Disable native splitLine/minor ticks in this core so no second tick source appears. Numeric labels receive raw supplied ticks; numeric pointer labels stay disabled until the shared crosshair composition is reviewed. The caller will compose axis titles/grid at the shared join; it must use this same scale/tick contract. Box B3c owns the forthcoming source-backed axis work. The controller assesses reuse after that contract freezes; R2 must not duplicate its resolver or modify Box files.

Category labels, ticks and pointer identities use integer slots on an internal value axis. For N>1, c=outer+(1-inner)/2, min=-c, max=N-1+c; explicit custom tick/label values are [0..N-1]. For N<=1 use [-.5,.5]. N=0 has no category labels/pointer. The underlying semantic type remains category; horizontal category yAxis is inverse=true. axisLine.onZero=false prevents perpendicular-axis repositioning. Axis label/line/tick paint uses the supplied subset; no axis title or grid input is silently discarded.

## Geometry and tooltip contract

Use public ECharts custom Cartesian series and the actual post-layout coordSys plot dimensions. Each selected field has stable id/name=descriptor.id and data [slot,minCoordinate,maxCoordinate], retaining null endpoint rows and metadata {fieldId,groupSlot}. Coordinates equal the raw endpoints for distinct semantic domains, use .5 for equal-domain transport, and cannot produce geometry for a null effective domain. Raw endpoints remain in projection/metadata, never replaced by transport values. Do not use a hidden base stack or derive interval height by changing financial observations. Custom geometry clips to the real plot; endpoint labels use the same clip, with no fabricated label at a clipping boundary.

Reproduce retained BandScale/AbstractBarSeries category and peer-band arithmetic (M12378-12411, M40946-40971), then RangeBarSeries placement (C20398-20465). Category width is L*(1-2*outer) for N=1, otherwise L/(N-inner+2*outer)*(1-inner). Visible peer count, not all selected fields, determines subgroup widths/offsets. A null datum still reserves its field's subgroup slot. Preserve the original rounded group step/inset/width when padding is nonzero, including the original rawBandwidth fallback below one pixel; do not copy Box's unconditional final width rounding.

For ordinal categories, original category convert is band start. Derive it from api.coord(slot) minus half category width, round that start, then add the peer offset. Round the two value coordinates separately. The value-direction rectangle starts at their minimum, has extent max(strokeWidth,abs(pixelHigh-pixelLow)), and uses the source peer width. Swap dimensions for horizontal bars. Equal endpoints therefore receive only the original stroke-width visual thickness; summary, ticks, labels and tooltip remain the single raw value. Width zero produces no visible interval. Draw fill and outline separately to preserve independent fillOpacity/strokeOpacity and dash/offset. Do not draw zero-based stems or connect categories.

Endpoint labels use display.seriesLabel on raw min/max and the original inside/outside positions/alignment (C20518-20583), with effective spacing=label.spacing+label.padding. They inherit supplied resolved typography and paint. Translation preflights finite geometry against the supplied plot rectangle and resolved coordinate transport. renderItem must still validate actual engine coordSys/api.coord output before returning shapes; an invalid actual engine coordinate throws to the future lifecycle owner. Admission cannot promise atomic detection of an unknown later engine failure. renderItem must not recalculate statistics or perform financial transformations.

Tooltip content follows the original range form (C20666-20715): optional category heading, field display name and formatted raw min - max, escaped through the existing escapeHtml helper. Min/Max are endpoint identities; counts/source IDs are metadata rather than added UI. Use supplied existing application modes: single hits one field, shared lists enabled non-null fields in selected order at the same slot, compact omits the category heading. Disabled tooltips emit no visible content. Precompute category/slot-pointer text for existing categories and supplied numeric tick text whenever a semantic scale exists, including explicit bounds with no observations. Evaluate seriesLabel only for enabled labels on enabled non-null data with a semantic scale; evaluate tooltipNumber only for enabled tooltips on enabled non-null data with a semantic scale. Disabled labels/tooltips, hidden fields and null effective scales do not invoke their endpoint callbacks. Do not evaluate the unused legend callback. Throwing/invalid results from callbacks actually needed by this output fail admission atomically. Runtime formatters look up admitted text rather than call financial callbacks again. Never show null as zero or mix measures/units. Native hit testing and shared-mode behavior still require later application acceptance.

## Ownership, checks and acceptance

One implementer owns only new production files `echarts/rangeBarTypes.ts`, `rangeBarAdmission.ts`, `rangeBarProjection.ts`, `rangeBarAxes.ts`, `rangeBarGeometry.ts`, `rangeBarSeries.ts`, `rangeBarTooltip.ts`, `rangeBar.ts` (all eight under echarts), and new `tests/unit/chart-compatibility/rangeBar.test.ts`, `rangeBar.render.test.ts`, `rangeBar.fixtures.ts` under `vendor/workspace/terminalpro/`. Projection exports projectRangeBar; composer exports translateRangeBar. Admission validates/copies, axes transports the explicit scale/paint, geometry owns source band/rectangle/label math, series binds stable identities, tooltip owns escaped precomputed text. No other writes. The worker is not alone and must preserve others' edits.

Controller owns inventory additions, current fork manifests, breadth/status reconciliation, independent review and selective commits. Every whole production file must pass 400 physical lines, 300 logical syntax units and 50 units per callable under the existing checker. Tests/docs are excluded. Freeze any additional file split before changing ownership; do not compress or add arbitrary forwarding helpers to pass caps.

Focused unit checks cover independent fields with duplicate category labels/identities, selected-order changes, all-null and absent values, empty/hidden fields, immutable raw USD extrema, explicit scale/tick validation, singletons, disabled callback policy and callback failures. Include a normalized grouped setup snapshot and prove its already-aggregated observations are consumed once, with no new setup aggregate. Include both directions of domain/data independence: no observations plus explicit bounds/ticks, and finite observations plus null effective domain. Test equal semantic [5,5]/tick [5] separately from an expanded singleton scale, including raw endpoints [2,8] both transported to midpoint without replacing them with 5. Raw labels and summaries must never contain .5 or transport [0,1]. Use hand-derived summaries and geometry expectations, not the mapper as its own oracle. R1 tests need not be duplicated.

Actual ECharts 6 SVG engine tests must inspect rendered rectangles and text, not only options: two fields/three categories with a null gap in both directions; nondefault category/group padding including fractional peer width; singleton stroke thickness under distinct and equal semantic domains; bounds cutting a range; a wholly offscale range; escaped min/max tooltip values; explicit nonuniform ticks that remain identical to supplied values; hidden-field regrouping then restoration. For [5,5]/[5], verify midpoint geometry and a single raw tick label 5 in both directions. Also verify empty observations with explicit bounds show requested ticks without rectangles, and finite raw observations with null effective domain retain projection but show no data/ticks/tooltips. Assert no NaN/Infinity, correct raw-unit labels and no null geometry. Reuse installed ECharts/Vitest and the accepted headless SVG pattern; no new browser harness or lifecycle suite.

From `vendor/workspace/terminalpro`, run the existing one-worker compatibility Vitest configuration:

```sh
node node_modules/vitest/vitest.mjs run \
  --config tests/unit/chart-compatibility/vitest.config.mjs \
  tests/unit/chart-compatibility/rangeBar.test.ts \
  tests/unit/chart-compatibility/rangeBar.render.test.ts
```

Run scoped Biome on R2 paths and strict no-emit checks. Controller prepares ignored `artifacts/chart-range/r2-tsconfig.json` for R2 files, following the accepted R1 scoped config, then runs `node vendor/workspace/terminalpro/node_modules/typescript/bin/tsc --project artifacts/chart-range/r2-tsconfig.json` from the root. If shared type imports expose inherited dependencies, the fallback acceptance command is `node node_modules/typescript/bin/tsc --project tests/unit/chart-compatibility/tsconfig.json` from `vendor/workspace/terminalpro`, run identically on the untouched baseline and candidate with pinned Node/compiler/config. The controller retains baseline output/exit in `artifacts/chart-range/r2-typing-baseline.log` and `.exit` before lane edits. Compare complete diagnostic multisets by path/code/message/location, normalizing only checkout-root paths; require no added/changed diagnostics and no R2-owned errors. Report inherited failures honestly, rather than calling that baseline route clean. Do not compare a scoped candidate against a canonical baseline, add suppressions or clean up shared modules. Run the existing root `pipeline/.venv/bin/python -m tools.quality.complexity --check` with explicit current workspace/data_api manifests and output `artifacts/chart-range/r2-complexity.json`, following [complexity instructions](../../../docs/complexity.md). Record actual commands/revisions/exits; planned tests are not evidence.

Independent source/financial review and fresh affected checks precede acceptance. R2 completion means an accepted inactive Range Bar core only. Activation additionally requires the real source-backed scale resolver, effective option/control/style composition, original/replacement runtime comparison, real-FMP extrema/unit/date checks, title/legend/navigation/theme/refresh/save/reopen/export journeys and controller-owned shared integration. The retained raw-USD quarterly fixture in R1 remains suitable without changes or provider calls; samples remain pending. No Range Area or family-completion checkbox is closed by R2.

## R2 acceptance

R2 inactive Range Bar is independently accepted at Workspace `1732847552a762c38e1cb1408d1efebccdeb0e6a`. Seventeen focused tests pass (nine unit and eight actual ECharts SVG); Biome passes 11 files and combined complexity has zero errors/violations. Scoped strict typing retains only inherited typography.ts TS2578; canonical strict baseline/candidate each retain 3,427 identical diagnostics, compiler exit 2. Range Area, application integration, real-FMP image/browser acceptance and publication remain open. Box Plot remains the active delivery milestone; the published alpha is unchanged.

Independent review: `artifacts/chart-range/r2-review.md`. The final remediation changed tests only; all eight production files retained their frozen hashes. Retained FMP extrema were verified against raw observations only, without application acceptance. See [verification](../../../artifacts/reviewed/chart-range/verification.md).
