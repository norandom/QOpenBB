# B2 inactive Box Plot renderer

Implement one inactive, pure Box Plot mapper using one ECharts custom Cartesian series per selected numeric field. Keep the accepted [B1 numerical boundary](box-plot-design.md) unchanged. B1 implementation is accepted at Workspace `85ca9ea247cc0c97add941b5007661b75941e734` (root record `c8ed1ac`); B2 implementation waits for this design's independent review. This document freezes B2 only; application activation remains [B3](box-plot-milestone.md).

## Evidence and scope

Read-only inspection on 2026-10-21 covered the actual current ECharts adapters, snapshot validator, appearance/display types, compatibility test configuration and retained original bundles. No implementation, tests, build, browser, installation or provider request ran for this design. Durable source identity and statistical rules are in [B1 Source contract](box-plot-design.md#source-contract). Local research inputs are `artifacts/chart-box/original-contract.md`, `artifacts/chart-box/integration-map.md` and `artifacts/chart-box/mapper-proposal.md`; these ignored files are not public evidence dependencies. This maintained design supersedes the preliminary proposal where less precise.

Native ECharts boxplot has a single styled BoxPath for outline, median, whiskers and caps, with cap width equal to box width. It cannot express the original independent whisker styles and cap ratio. Use the installed ECharts 6 public `CustomSeriesOption`, `CustomSeriesRenderItem`, `api.coord`, `api.size`, graphic groups, rects and lines. No native boxplot underneath, renderer fork, transform, second host, state owner or dependency.

## Frozen public interface

Paths in this document are relative to `vendor/workspace/terminalpro/`; production filenames below have prefix `src/components/General/Table/Chart/echarts/`. `boxPlotTypes.ts` exports the following contract, importing actual existing types from `application/appearanceModel`, `application/types`, `compatibility/snapshotTypes`, `compatibility/boxSummary` and `echarts/cartesianTypes`.

```ts
export interface BoxStroke {
  readonly stroke: string;
  readonly strokeWidth: number;
  readonly strokeOpacity: number;
  readonly lineDash: readonly number[];
  readonly lineDashOffset: number;
}
export interface ResolvedBoxFieldStyle extends BoxStroke {
  readonly fill: string;
  readonly fillOpacity: number;
  readonly whisker: BoxStroke;
  readonly cap: { readonly lengthRatio: number };
}
export interface BoxPlotMappingInput {
  readonly snapshot: ChartSnapshot;
  readonly style: {
    readonly common: Pick<ResolvedCartesianStyle,
      "textColor" | "fontFamily" | "fontSize" | "precision">;
    readonly application: Omit<ResolvedApplicationAppearance, "axes" | "series">;
    readonly direction: "vertical" | "horizontal";
    readonly axes: {
      readonly category: ResolvedApplicationAxis;
      readonly number: {
        readonly appearance: ResolvedApplicationAxis;
        readonly min?: number;
        readonly max?: number;
      };
    };
    readonly band: {
      readonly paddingInner: number;
      readonly paddingOuter: number;
      readonly groupPaddingInner: number;
    };
    readonly fields: Readonly<Record<string, ResolvedBoxFieldStyle>>;
  };
  readonly context: {
    readonly display: ChartDisplayPolicy;
    readonly viewport: { readonly width: number; readonly height: number };
    readonly legendSelection?: Readonly<Record<string, boolean>>;
  };
}
export interface BoxPlotGroup {
  readonly slot: number;
  readonly category: string | number;
  readonly rowIds: readonly string[];
}
export interface BoxPlotDatum {
  readonly groupSlot: number;
  readonly count: number;
  readonly summary: BoxSummary | null;
  readonly sourceRowIds: readonly string[];
}
export interface BoxPlotField {
  readonly descriptor: SnapshotColumn;
  readonly paletteIndex: number;
  readonly enabled: boolean;
  readonly data: readonly BoxPlotDatum[];
}
export interface BoxPlotProjection {
  readonly groups: readonly BoxPlotGroup[];
  readonly fields: readonly BoxPlotField[];
}
export interface BoxPlotDomain {
  readonly value: readonly [] | readonly [number, number];
  readonly empty: boolean;
}
export type BoxPlotTranslationResult =
  | Exclude<CartesianTranslationResult, { status: "supported" }>
  | (Extract<CartesianTranslationResult, { status: "supported" }> & {
      readonly projection: BoxPlotProjection;
      readonly domain: BoxPlotDomain;
    });
export type TranslateBoxPlot =
  (input: BoxPlotMappingInput) => BoxPlotTranslationResult;
```

`boxPlot.ts` exports `translateBoxPlot: TranslateBoxPlot`. The signature is typed for callers but runtime admission remains defensive. Successful results contain fresh options, copied projection metadata and no reference to mutable caller arrays/records. Function callbacks are retained as capabilities, never serialized. Options are not persisted. There is no aggFunc, raw grid object, options baseline, theme resolver, setup switch or category-coercion policy in this input.

Selected numeric descriptors are resolved from `snapshot.selectedColumnIds` in that order, filtering the associated category descriptor. Every numeric field receives exactly one style entry by descriptor ID, including hidden fields. The caller resolves palette and per-field overrides before admission; paletteIndex remains selected-field order and never shifts on legend hide. Extra style or legend IDs are invalid, rather than silently binding a label to the wrong financial measure. Duplicate labels are allowed.

## Admission and statistical projection

`boxPlotAdmission.ts` validates and copies snapshot data using the existing defensive `validateSnapshot(snapshot, "xy-coordinates")` structural validator. This policy currently only permits empty numeric selections; it does not coerce categories or impose XY assignments. B2 uses that observed structural behavior, with a focused regression proving empty Box admission; no cast makes Box an XY family. A Box-specific capture policy belongs to B3, before capture loses default/missing/Date identities. Do not modify `snapshotTypes.ts` merely to name the inactive mapper.

Validate plain data property descriptors before reads, dense arrays, finite numeric leaves, unique field IDs, valid callbacks and positive finite viewport dimensions. Catch synchronous inspection and callback exceptions at the translation boundary and return `invalid` diagnostics without partial options. Copy style arrays and nested records; do not freeze/mutate caller objects. Validate opacity and ratios in [0,1], nonnegative widths/dash entries, finite dash offset, nonempty color strings, precision integer 0..20 and finite explicit bounds with min <= max when both exist. Require paddingInner < 1 and paddingOuter <= .5; reject nonrepresentable derived spans. Malformed shape is `invalid`; valid but incompatible axis type/position is `unsupported`. No arbitrary resource cap or new diagnostic framework.

Category must be type category; number must be type number. Vertical accepts category bottom/top and number left/right; horizontal accepts category left/right and number bottom/top. Existing axis appearance fields, typography, grid styles and callbacks retain their meanings. Box does not support category number/time axes through coercion. Original Grid excludes axis-type selection for Box. Date categories arrive as already normalized numeric identities displayed through the caller's category callback, not as a time axis.

`boxPlotProjection.ts` groups copied rows with `Map<string | number, ...>` in first-occurrence order. Numeric 1 and string "1" stay distinct even when formatted alike. Keep empty-string categories. Rows are already selected and setup-aggregated exactly once upstream; never aggregate, rescale USD or infer dates here. For each group and each selected numeric field call `calculateBoxSummary` once with that field's ordered observations, absent values represented by null. Preserve B1 count and nullable summary. Prefix helper diagnostic paths with the group/field context and fail the whole translation if any summary is invalid. Do not calculate statistics inside renderItem or tooltip callbacks.

Retain all groups and fields, including all-null groups and hidden fields. Group rowIds include every source row; datum sourceRowIds identify rows contributing finite observations. No geometry is emitted for a null summary, and no outlier series exists. Empty rows or no numeric fields return supported empty options with stable chrome/axes and no invented observations.

## Geometry contract

Original geometry sources are retained Charts enterprise C16035-16115 (BoxPlotGroup), C16431-16515 (node positioning), and community `dist/package/main.cjs.js` C12378-12411 (BandScale), C40877-40976 (AbstractBarSeries). Enterprise bundle identity is in the original-contract report. Community source is the retained sibling package, SHA-256 `237912c75d2c7e8219fced7bb79e5ed8fca0f620d6f4d259cdfa58748445fcd1`. These formulas govern the local geometry test oracle, not a claim of matched application pixels.

Use the actual category coordinate span from `params.coordSys` after ECharts axis layout, not viewport width. Reproduce the original outer category band with `paddingInner=.3`, `paddingOuter=.15` unless the caller resolves an explicit original axis override. Original AbstractBarSeries supplies these defaults; Box theme supplies groupPaddingInner=.2. Input contains resolved values so defaults are neither guessed in the geometry function nor overwritten on rehydration.

Use one internal numeric-slot category axis so labels, ticks, pointer identity and box centers share the original band mapping for every admitted padding override. For N>1 let c=outer+(1-inner)/2 and set explicit internal axis min=-c, max=N-1+c, scale=true. Then api.coord(slot) is original band center because the span denominator is N-inner+2*outer. Set both public axisLabel.customValues and axisTick.customValues to ordered integer slots, mapping their formatters back to semantic categories. For N=1 use internal [-.5,.5], slot=0 at midpoint, and calculate original bandwidth L*(1-2*outer) separately. For N=0 use internal [-.5,.5], empty customValues and no category pointer label or financial geometry. AxisLine.onZero=false on both axes prevents ECharts shifting the perpendicular axis into the plot. Horizontal category yAxis is inverse=true. This is an internal coordinate adapter; semantic input remains category type and no editor axis type changes. Separate ECharts6 source/API proof has reported passing both orientations for the N=3 inner=.3/outer=0 counterexample and N=1 outer=.4; controller must record and review that spike before B2 dispatch. Original source formulas remain the geometry oracle below.

For N category bands over positive span L, use rawStep=L/max(1,N-inner+2*outer), inset=(L-rawStep*(N-inner))/2 and bandwidth=rawStep*(1-inner). For N=1 original BandScale instead forces inner=0 and rawStep=L*(1-2*outer). Category band scale is unrounded by default. Translate inset and slot to the axis origin, preserving input order; horizontal categories run top to bottom. Keep empty categories in N.

For M enabled fields inside category bandwidth B, original groupScale has outer padding 0 and inner padding g; when M=1 it forces inner=0. For M>1 rawStep=B/max(1,M-g), step=floor(rawStep) when g!=0, otherwise rawStep; inset=(B-step*(M-g))/2; grouped width=step*(1-g). With rounding enabled round inset and width. If resulting bandwidth<1, original uses rawBandwidth=rawStep*(1-g). Original node geometry then rounds grouped width and group offset, so a tiny box can have zero width. Preserve that outcome rather than enforcing a minimum visible box. M=0 emits no geometry and never divides by zero. Hiding a field recomputes M and its visible group index while retaining palette/series identity.

`boxPlotGeometry.ts` is the sole geometry owner. For each datum convert all five statistics with api.coord and round their value coordinates before positioning. Category start is round(category band start) + round(group offset); bandwidth is round(grouped width). Account for screen-axis reversal as original BoxPlotGroup does before taking the ordered screen low/high endpoints. For vertical orientation map the value dimension to y and band dimension to x; horizontal swaps those dimensions.

Return these children in original paint order:

- Filled Q1-Q3 rect with fillOpacity; separate transparent-fill outline with main stroke/opacity/dash/offset.
- Median filled strip in the main stroke color/opacity. Its value start is max(round(medianPixel-mainWidth/2), boxStart+mainWidth), end is min(round(medianPixel+mainWidth/2), boxEnd-mainWidth); clip to the box inset by mainWidth across the band. Show only when start<end. Original singleton and sufficiently thin boxes therefore have no visible median strip; do not replace this with an always-visible line.
- Two whisker lines with effective width=min(resolved whiskerWidth,bandwidth). Center uses floor(bandStart+bandwidth/2); endpoint offsets use round(screenMin+width/2) and round(screenMax-width/2), joined to Q1/Q3 according to screen orientation.
- Two caps using whisker styles, from floor(bandStart+bandwidth*(1-ratio)/2) to ceil(bandStart+bandwidth*(1+ratio)/2). Ratio zero can retain a one-pixel span after floor/ceil; do not assume no cap.

Singleton/constant summaries remain valid; coincident outline/caps/whiskers follow these same formulas. Main and whisker opacity must be independent child paint alpha, without multiplying a group opacity. Use only public clipping APIs against the Cartesian plot rectangle. Corner radius remains zero: no reachable original Grid corner-radius control is evidenced for this slice. Do not silently add shadow or marker behavior to Box; a later source finding of reachable controls revises this contract before acceptance.

Before returning supported options, synchronously preflight all summaries, effective semantic domains and coordinate-normalization arithmetic: finite positive spans for nonconstant domains, finite `(value-low)/(high-low)` for every statistic, finite viewport/band/group arithmetic and child style/geometry arithmetic against the admitted viewport envelope. A domain may be finite while subtraction/division overflows, including values clipped beyond a narrow explicit range; return invalid atomically for such inputs. Do not invoke ECharts or pretend the final grid exists at this stage. renderItem later validates actual coordSys/api coordinates and each child shape; unexpected nonfinite values throw a descriptive renderer error, never return undefined to silently drop a valid datum. A later exception cannot retroactively change the translation result. Existing lifecycle.ts apply/render/refreshLegend and EChartsHost error handling own engine-time failures; B2 adds no host edits or listener. Actual-engine tests must verify thrown renderer errors propagate through those existing synchronous boundaries. Any later asynchronous engine error outside them remains an integration blocker for B3 rather than a claim of mapper atomicity.

## Axes, chrome, legend and tooltips

`boxPlotDomain.ts` derives observed min/max from enabled non-null summaries' absolute endpoints, without forcing zero. Follow retained community `normalisedExtentWithMetadata`, C28727-28748, consumed by NumberAxis C30297-30301: with observations, replace each endpoint only when its explicit bound exists; if resulting low>high return semantic value=[] and empty=true. Without observations (including all-hidden), return the two explicit bounds only when both exist and min<=max, otherwise []. Equal endpoints remain [v,v], empty=false; no 5% or minimum-one financial expansion. A one-sided lower bound beyond observed max or upper bound below observed min therefore empties the domain. Two explicit ordered bounds can establish a nonempty domain even when all observations lie outside them; clipping emits no visible box in that case. Opposite-sign extremes whose positive span overflows are invalid even when B1's summaries are finite.

Semantic domain is distinct from finite ECharts transport. For a positive semantic span transport uses those endpoints (subject to safe nice rounding below). A constant observed v with a one-sided bound different from v therefore uses the resulting nonconstant range normally, rather than midpoint transport. For [v,v], use transport [0,1] and place every statistic at value-coordinate .5; retained ContinuousScale.convert C12205-12213 maps every value to the range midpoint for an equal domain. Preserve raw five-value dimensions and metadata; only the coord argument is transported. Set public ECharts6 axisTick.customValues and axisLabel.customValues to [.5], format that coordinate as v via numericAxis, and translate every crosshair numeric callback coordinate back to v. Raw tooltips never format .5; shared-axis tooltip selection uses category slot and admitted summary metadata, not native value-coordinate payloads. The retained createTicks C18490-18493 emits one v tick for an equal input domain. This is a B2 transport choice, not proof of original final ticks: LinearScale.niceDomain C30262-30285 can round a noninteger equal input outward when tickCount>1 (tickStep C18557-18560 returns 1 for equal input). Resolve the original effective nice/tick path before B3 activation; do not claim midpoint/single-tick parity for all original constant configurations. For semantic [], use transport [0,1], no series geometry, empty label/tick customValues and no numeric grid lines or crosshair label. Retain projection/groups/field identities but emit no financial values or shared-tooltip rows for that empty domain. Never display transport endpoints as observations or ticks. With no observations but both distinct bounds supplied, show the admitted bounded axis normally, without geometry. These transport rules require the focused actual-engine assertion below; they do not claim application visual parity.

Reuse `niceNumberExtent` from cartesianAxes only after finite positive-span admission, with fallback to admitted raw endpoints if its result is not finite/increasing. Preserve explicit bounds when rounding; no automatic interval may move them. Equal/empty semantic domains bypass this helper. Encode all five raw statistics on the value axis and slot on the category axis: vertical encode x=slot/y=[min,q1,median,q3,max], horizontal reverses them. Fixed explicit transport axis bounds prevent ECharts from deriving another domain from raw dimensions. Use `filterMode: "none"` if a later host supplies dataZoom, so a median outside the view cannot remove an intersecting whisker. No navigator is created by B2.

`boxPlotAxes.ts` adapts actual ResolvedApplicationAxis to the internal slot/value ECharts axes above, using `fontStyle`, `measureText`, `alternatingGrid`, and existing qopenbbGrid registration for alternating lines. Slots are unique integer keys; formatter maps slot to original category using display.category. Duplicate formatted labels do not merge. Preserve axis lines/ticks/grid/title, label rotation/autoRotate/padding and numericAxis/crosshair callbacks. Both internal axes have scale=true and explicit transport bounds. Use slot-valued data on every field's ECharts items, including a null-summary item's missing five statistics, to retain axis-trigger group identity; renderItem emits nothing for those null summaries. Shared tooltip resolves an integer slot from metadata/axisValue and lists only enabled non-null summaries at that slot; if no field has a value, return no financial tooltip. Do not depend on ECharts nearest-point behavior for a group omitted from series data. Verify public axis-pointer slot identity in the grouped actual-engine check.

`boxPlotLayout.ts` composes captions/background/padding/legend using existing `measureText`, `fontStyle` and `markerSymbol`. Existing applicationLayout/applicationAxes require CartesianFamily and full ResolvedApplicationAppearance, including unrelated series state; do not call them by casting Box to line/bar. Small family adapters are preferable to changing shared interfaces during B2. No unrelated renderer is copied wholesale. Reuse established caption/legend spacing formulas and style vocabulary; exact original runtime defaults remain B4 comparison evidence.

Every custom series has id and name equal to stable field ID. Legend data names use IDs and formatter uses display.legend(descriptor.label). Legend selection is native ECharts selection, with the existing host's event-to-remap contract supplying context.legendSelection. The pure mapper does not subscribe to events or maintain selection. Real-engine tests apply the native action and remap with its emitted selection, asserting one series/legend item per field, updated widths/domain, stable order and export.

`boxPlotTooltip.ts` prepares escaped tooltip text from the admitted category, field label and Min/Q1/Median/Q3/Max using display.tooltipNumber on raw statistics. The actual application tooltip type contains enabled and mode, not delay/range. Follow existing Cartesian mode semantics: shared uses an axis trigger and lists enabled fields' five statistics for the same slot; single uses item trigger and only the hit field; compact uses item trigger and omits category heading. This changes no statistical calculation. Validate modes against the existing editor vocabulary and diagnose an unsupported mode rather than silently ignore it. Keep counts/source IDs as metadata, not unsolicited tooltip UI. Preflight callback outputs during admission/projection; callback failure produces no partial option. Tests distinguish raw USD from display abbreviations. B3 must verify these modes against reachable original Box settings before activation.

Original constructor defaults are fillOpacity=1, strokeOpacity=1, strokeWidth=1, lineDash=[0], lineDashOffset=0 and cap.lengthRatio=.5; Box theme overrides strokeWidth=2 and resolves themed fill/stroke. Whisker missing leaves inherit the final main stroke/width/opacity/dash/offset, after theme/generated/saved layering. B2 requires those inherited leaves explicitly resolved. Whisker controls remain independent once supplied (width 0..10, opacity 0..1, dash/offset 0..30 in the original editor), and cap ratio is 0..1 with .05 slider steps. Mapper accepts valid finite values beyond UI slider maxima where the original property permits them; do not turn editor slider limits into invented saved-data rejection. B3 owns exact option paths, inheritance resolution and control reachability; no flag/default/editor delta is authorized here.

## Exclusive implementation ownership and review gate

One B2 implementer owns only new production files `boxPlotTypes.ts`, `boxPlotAdmission.ts`, `boxPlotProjection.ts`, `boxPlotDomain.ts`, `boxPlotGeometry.ts`, `boxPlotSeries.ts`, `boxPlotAxes.ts`, `boxPlotLayout.ts`, `boxPlotTooltip.ts`, `boxPlot.ts`, plus new `tests/unit/chart-compatibility/boxPlot.test.ts` and `boxPlot.render.test.ts`. Split validation or geometry further only after controller agrees exact new ownership. `boxPlotSeries.ts` creates public custom-series data/renderItem closures over the single admitted projection; composer owns failure handling. No application, host, caller, gallery, editor, capture, setup, B1 helper or shared renderer changes. The implementer is not alone in the checkout and must preserve others' edits.

Controller owns inventory additions in `.kiro/complexity-budgets.json`, explicit current workspace/data_api change manifests, breadth mapping and reviewed evidence. Foundation enforcement already exists; do not create another checker. Every new production file must pass 400 physical lines, 300 logical syntax units and 50 units/function as a whole. Tests/docs are exempt. Add inventory ownership before accepting executable feature work and audit all new shared imports at the join. No commit/build/publication in B2 worker scope.

Focused contract tests cover meaningful missing-mapper RED then GREEN, frozen-input immutability, invalid/throwing boundary atomicity, typed duplicate labels/categories, ordered multiple fields, missing observations, finite raw USD, aggregation already performed, empty/no-field/all-hidden recovery, singleton/repeated/signed values, source-backed equal/empty/bounded domains and arithmetic representability failures. Verify B1 is called once per field/group, with no renderer-time statistics. Use a few grouped actual ECharts SVG SSR checks following histogram.render/pie.render: (1) fixed-size two-field geometry in both directions, with an all-null gap, original padding, median/caps and independent inherited/overridden paint; (2) native legend hide/remap plus resize, verifying field identity, widths, domain and export; (3) constant/empty/clipped data, proving midpoint/single raw-value tick, no transport labels/false geometry, and renderer error propagation. Fold cap ratio 0/.5/1 and category alignment/pointer identity into the first check, including the three-category outer=0 and singleton outer=.4 counterexamples. Do not create a Cartesian test matrix or new browser harness. Formula tests alone do not establish engine geometry.

Run from the existing WSL-resolved terminalpro checkout with pinned Node on PATH; these are planned commands using inspected existing configs, not results:

```sh
node node_modules/vitest/vitest.mjs run --config tests/unit/chart-compatibility/vitest.config.mjs tests/unit/chart-compatibility/boxSummary.test.ts tests/unit/chart-compatibility/boxPlot.test.ts tests/unit/chart-compatibility/boxPlot.render.test.ts
node node_modules/typescript/bin/tsc --project tests/unit/chart-compatibility/tsconfig.json
```

The compatibility config uses jsdom/maxWorkers=1 and includes the new files. The strict no-emit config follows application imports and has inherited diagnostics, including typography.ts TS2578; a global clean exit is not an assumed B2 prerequisite. Controller runs the exact TypeScript command above on the untouched accepted Workspace baseline `85ca9ea247cc0c97add941b5007661b75941e734` and candidate with identical installed compiler/config. Capture both complete diagnostic streams and actual exit codes, normalize only checkout-root paths, and compare diagnostic multisets by path/code/message/location. Acceptance requires no diagnostics in B2-owned files and no added/changed dependency diagnostics; inherited baseline failures are reported as inherited, never a clean pass. Review accepted one exact presentation-only difference at TableSettings.tsx(185,38), TS2769: the two union members appear in reversed order, with identical overloads and undefined-argument rejection. Preserve the raw differing logs; this is not a general message-normalization allowance. Do not refactor shared production or add suppressions to clean baseline diagnostics. Controller may additionally use the B1 root-local scoped-config precedent `artifacts/chart-box/b1-tsconfig.json` to isolate investigation, but the frozen acceptance gate is this same-command baseline comparison. Controller runs the existing root complexity gate with actual manifests, following [complexity instructions](../../../docs/complexity.md):

```sh
pipeline/.venv/bin/python -m tools.quality.complexity --check --changes workspace=artifacts/chart-box/workspace-changes.json --changes data_api=artifacts/chart-box/data-api-changes.json --output artifacts/chart-box/b2-complexity.json
```

Record exact revision, command, exit code and local evidence path. Independent Astra review must examine source geometry, financial units, defensive boundaries and real-engine evidence before acceptance. B2 proves an inactive mapper, not integrated parity. B3 still freezes missing/default/Date capture policy before aggregation, saved style inheritance, editor transaction semantics, navigator/miniature behavior and host routing. B4 owns matched original/application screenshots, real-FMP provenance, interaction/export and owner visual decisions. Any unrepresentable original styling or geometry difference returns to the controller for explicit review rather than silent capability reduction.
