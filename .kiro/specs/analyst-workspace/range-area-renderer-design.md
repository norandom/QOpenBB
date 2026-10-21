# Inactive Range Area renderer

R3 inactive implementation is independently accepted, 2026-10-21. It adds an unreachable Range Area core beside accepted R1/R2. Each selected measure remains its own within-category minimum/maximum envelope. Box Plot remains the active delivery milestone. This bounded design uses the prototype-first amendment rather than changing the unapproved whole-spec phase.

Freeze: Workspace `1732847552a762c38e1cb1408d1efebccdeb0e6a`, root `cebf7ea`. Original Grid 34.1.1 and Charts 12.1.1 source hashes/citations are recorded in `artifacts/chart-range/source-contract.md`; additional findings are in `artifacts/chart-range/r3-source-notes.md`. Source discovery was read-only; no production edit, test, build, browser, installation or provider request ran. Core steering product/tech/structure files are absent. The kiro-spec-design light-discovery, boundary/synthesis/review guidance and documentation policy informed this draft. There are no approved numeric whole-spec requirements to claim covered; the owning bounded criteria are [the Range plan](range-chart-plan.md).

## Boundary commitments

R3 owns band paths, two boundary strokes, endpoint markers/labels, explicit category/value coordinate transport, escaped tooltips and defensive admission for these inputs. It supports ordinary normalized category snapshots only, with flat/transformed/grouped observations. It never aggregates again or changes raw units. It imports the accepted R2 projection read-only because its financial grouping is identical; geometry and paint stay separate.

Out of boundary: capture/editor/state/registries, effective defaults, automatic nicing/tick selection, category number/time/grouped-category axes, titles/grid/legend/layout, navigator, hover highlighting, lifecycle and all application activation. Valid unsupported semantics return diagnostics; no existing active control is hidden or disabled. Range Area allows category-axis type and tick controls in the original, unlike Range Bar; these require a later application contract before activation.

Allowed read-only dependencies: `projectRangeBar` from `echarts/rangeBarProjection.ts`; `RangeBarProjection`, `RangeBarProjectionResult`, `RangeBarAxisPaint`, `ResolvedRangeBarScale` and `RangeBarFieldStyle` types; `copyRangeData`, `rangeDisplayText` from `rangeBarAdmission.ts`; `escapeHtml`/`fontStyle` from `cartesianDisplay.ts`; marker helpers from `cartesianMarkers.ts`; existing snapshot/display/application types; installed ECharts 6. No Box imports, R2 mapper/admission/axes invocation, native statistical transform or new dependency. Projection diagnostics retain their existing codes; R3-owned errors use `invalid-range-area` / `unsupported-range-area`.

Revalidation triggers: changed R1/R2 projection semantics, admission utility behavior or shared marker geometry; activation or wider axis eligibility; altered interpolation/financial meaning. Controller serializes any shared change. No extraction solely to rename Bar types is necessary.

## Interfaces

Paths are relative to `vendor/workspace/terminalpro/src/components/General/Table/Chart/`.

```ts
export type RangeAreaProjection = RangeBarProjection;
export type RangeAreaProjectionResult = RangeBarProjectionResult;
export type RangeAreaInterpolation =
  | { readonly type: "linear" }
  | { readonly type: "smooth"; readonly tension: number }
  | { readonly type: "step"; readonly position: "start" | "middle" | "end" };
export interface RangeAreaFieldStyle extends RangeBarFieldStyle {
  readonly marker: {
    readonly enabled: boolean;
    readonly shape: "square" | "circle" | "cross" | "diamond" | "plus" | "triangle" | "heart";
    readonly size: number;
    readonly strokeWidth: number;
    readonly fill: string;
    readonly fillOpacity: number;
    readonly stroke: string;
    readonly strokeOpacity: number;
  };
  readonly shadow: {
    readonly enabled: boolean; readonly color: string; readonly blur: number;
    readonly xOffset: number; readonly yOffset: number;
  };
  readonly interpolation: RangeAreaInterpolation;
  readonly connectMissingData: boolean;
}
export interface RangeAreaMappingInput {
  readonly snapshot: ChartSnapshot;
  readonly style: {
    readonly categoryAxis: RangeBarAxisPaint;
    readonly numberAxis: RangeBarAxisPaint;
    readonly valueScale: ResolvedRangeBarScale | null;
    readonly band: { readonly paddingInner: number; readonly paddingOuter: number };
    readonly fields: Readonly<Record<string, RangeAreaFieldStyle>>;
    readonly tooltip: { readonly enabled: boolean; readonly mode: "single" | "shared" | "compact" };
  };
  readonly context: RangeBarMappingInput["context"];
}
export type RangeAreaTranslationResult =
  | { readonly status: "supported"; readonly options: EChartsOption;
      readonly projection: RangeAreaProjection }
  | Exclude<RangeAreaProjectionResult, { status: "resolved" }>;
export function translateRangeArea(input: RangeAreaMappingInput): RangeAreaTranslationResult;
```

Consumers needing raw extrema call the existing `projectRangeBar` directly; no duplicate public projection implementation. Its selected order, numeric/string identities, first-encounter groups, all-null slots, contributor IDs, hidden-field palette identity and enabled-only raw dataExtent apply unchanged. No peer grouping/offset exists for Range Area: fields overlay the same category centres.

Admission copies data before callbacks and rejects accessors/cycles/sparse arrays/nonfinite or malformed inputs without partial options. Retain R2's finite paint/font/axis/context/domain validation contract, implemented independently only for the Area-specific input shape. Dense fields must exactly cover selected measure IDs. Marker size/width, shadow blur, label spacing/padding and stroke widths are finite nonnegative; shadow offsets/dash offset are finite signed numbers; opacities and smooth tension are in [0,1]. Unknown shape/interpolation/axis semantics are unsupported. Category x-axis is top/bottom, number y-axis left/right; auto rotation must already be resolved. Band paddings retain R2 limits. No direction or groupPaddingInner input is accepted.

## Coordinates, paths and text

The explicit valueScale contract is identical to R2, including independent raw dataExtent, empty observations with supplied ticks, finite observations with null effective scale, and equal semantic bounds transported to [0,1] with raw endpoints at .5. Never let ECharts choose financial ticks, include zero or expand singleton financial values. Use the same custom tick arrays and raw formatter lookup; null scale suppresses geometry/numeric ticks/endpoints/tooltips while retaining the projection. No arithmetic on raw endpoint differences is needed for summaries. Detect nonfinite projected pixels/control points before options and in renderItem against actual engine coordinates; later engine failures throw to the future lifecycle owner.

Category centres use slot i, with R2's BandScale-compatible category-domain arithmetic: for N>1, c=outer+(1-inner)/2 and domain [-c,N-1+c]; for N<=1 use [-.5,.5]. There is no bar-start rounding. Public custom Cartesian geometry uses actual ECharts coordSys dimensions and clips to that plot. Preserve unsorted first-encounter order; do not sort categorical labels lexically or by their numeric-looking text.

C19493-19618 partitions each field into runs: null summary breaks both boundaries when connectMissingData=false; true omits the null point and bridges the surviving neighbours while retaining its category gap/slot. Both finite endpoints are required. One-point runs have endpoint markers/labels but no invented band or boundary segment. Equal endpoints produce a zero-area band with coincident original strokes/markers, never a fabricated thickness or zero-based stem. Each run's fill follows the high boundary forward and low boundary backward and closes; boundary strokes contain only the high and low paths, with no vertical end-cap stroke. Fill and stroke have independent opacity; shadow applies to fill only (C19664-19712). Markers use the supplied resolved marker paint, not a guessed inheritance rule. Both endpoints exist even when equal.

Interpolate in pixel space independently on each boundary, following M38703-38819 and M39404-39426. Linear joins adjacent points. Step changes at x0+(x1-x0)*p with p=0/.5/1 for start/middle/end. Smooth uses the source gradient rule: zero at extrema or interior neighbour proportions within .05 of either end; otherwise (nextY-prevY)/(nextX-prevX), with terminal neighbour equal to the terminal itself. Double the first/last gradient when the adjacent gradient is zero. Cubic controls start at dx*tension/3 along x and dx*gradient*tension/3 along y; apply the source overshoot clamp when the opposite endpoint gradient is zero. Reverse the low cubic's control order when closing the fill. Do not substitute ECharts smooth, stacked area or interpolate raw financial values. A small pure path helper and public custom path elements are sufficient; preserve continuous run strokes/dash phase and fill shadow rather than independently shadowing every adjacent trapezoid.

C19620-19659 labels use raw min/max, horizontal alignment centre, effective spacing=spacing+padding: outside high is above/bottom-baseline and low below/top-baseline; inside reverses these. Labels do not depend on marker.enabled, and no label appears at a synthetic clipping intersection. Original integrated extrema cannot reverse. Original standalone reversed-endpoint behavior is out of boundary.

Tooltips use category heading plus field label and formatted raw `min - max` (C19799-19840). Single targets one field/slot; shared lists enabled non-null fields at that slot in selected order; compact removes the heading. Metadata always identifies raw field ID and group slot; interpolated points never become financial observations. Hidden fields, null scale and disabled features do not invoke endpoint callbacks. Precompute required category/pointer/tick/label/tooltip text atomically; runtime callbacks only look up admitted escaped text. Reuse R2 callback timing policy; do not invoke unused legend callbacks.

Render continuous run fill and boundary paths with public `CustomSVGPathOption.shape.pathData` and `silent:true`; outline uses lineCap/lineJoin round. Markers and labels are also silent. Separate custom data records cover every field/slot, including null slots, and retain raw `{fieldId, groupSlot}` datum metadata. Enabled non-null records own transparent non-silent rect hit shapes; null/hidden records remain in axis data but renderItem returns no hit or visible glyph. Their x cells extend halfway to adjacent category centres, clipped to plot edges; first/last cells extend to the respective plot edge. Their y extent is the raw endpoint pixel interval clipped to the plot, with a one-pixel minimum invisible target for an on-plot equal interval, centred then clipped. Wholly off-plot intervals and null slots have no hit shape. Transparent targets never add visible financial thickness. Overlapping field targets use selected order, with the last selected enabled field on top, matching visual layering. Within each field, lower-slot hit shapes render above higher-slot shapes, so exact category-cell boundaries deterministically select the lower slot. Selected-field layering takes precedence over within-field slot ordering.

Shared tooltips use the public x-axis pointer with snap:true and full per-slot data records, including null records, so native snapping retains missing category positions. Use the engine-selected integer slot and look up only actual non-null summaries there. Native engine tie behavior remains engine-owned; the pure mapper adds no pointer-coordinate ingress or lifecycle listener. Retain integer slot identity on the x-axis and admit only integer slots in formatter data; never round arbitrary formatter input into a financial observation. A null slot with connected interpolated fill still yields no field row; all-null slots yield an empty tooltip. Single/compact hits use the per-item field/slot metadata. No run-level item is allowed to attribute its whole band's hits to the first observation. Source-equivalent nearest-marker/highlight behavior remains an application integration question; these deterministic core hit semantics establish correct identities, not pointer parity.

## File structure and worker boundary

One implementer owns only new `echarts/rangeAreaTypes.ts` (contracts), `rangeAreaAdmission.ts` (Area boundary), `rangeAreaAxes.ts` (transport/paint), `rangeAreaPaths.ts` (run partition and source interpolation), `rangeAreaSeries.ts` (public custom paths, markers and labels), `rangeAreaTooltip.ts` (precomputed text/identities) and `rangeArea.ts` (composition), plus new `tests/unit/chart-compatibility/rangeArea.fixtures.ts`, `rangeArea.test.ts`, `rangeArea.render.test.ts`. Split a cohesive helper further only after controller freezes its path. The worker is not alone; preserve others' edits. No existing production file, registry, dependency, Box path or shared helper may change.

Controller owns inventory/manifests/breadth/status/evidence and selective commits. Each whole production file must pass 400 physical lines, 300 logical syntax units and 50 units/function through the existing combined checker with explicit current fork manifests. Existing inventory foundation is already accepted; add the seven actual maintained files before acceptance. Do not use arbitrary wrappers or statement compression to pass caps.

## Verification and acceptance

Use installed one-worker Vitest compatibility config for the two new test files, scoped Biome and strict no-emit type checks. Follow accepted R2 scoped typing and complete identical baseline/candidate diagnostic comparison if inherited errors are exposed; do not claim a clean typecheck from the baseline route. Controller supplies current complexity manifests and scope. No build/browser/provider work belongs to this inactive task; independent source/financial review and fresh affected checks precede R3 acceptance.

Unit tests cover independent fields, ordering/identity, empty/all-null/hidden fields, null/explicit/equal domains and raw callback values, immutable projection reuse, disabled callback policy, malformed/throwing admission, escaped single/shared/compact tooltips, run breaks/bridges and one-point/equal-endpoint runs. Do not repeat R1 tests or all 17 accepted R2 checks. Hand-derive linear, all three step and smooth-control expectations, including flat extrema, endpoint-gradient doubling and overshoot clamps; do not use the path helper as its own oracle.

Actual ECharts SVG tests inspect rendered paths/text/marker bounds: a two-field envelope with a middle null category under both gap modes; singletons and equal endpoints; explicit nonuniform ticks and equal-domain midpoint with raw labels; empty-data explicit axes and null-scale suppression; clipped bands; independent fill/outline paint and fill-only shadow; markers disabled with labels enabled, then all seven shapes; linear/step/smooth path commands; hidden-field restoration without peer displacement. Require no NaN/Infinity and no financial transport text. Exercise public engine element containment/event dispatch against transparent hit targets at multiple slots, including marker-disabled, singleton, overlap and exact-boundary ties, and assert raw datum identities and resulting tooltip rows. Confirm paths are silent and connected null slots invent no hit/row. Native application pointer journeys remain a later integration gate.

Portable maintained tests embed this bounded unchanged FMP-derived fixture in `rangeArea.fixtures.ts`, with source/provenance hashes from `artifacts/chart-range/source-contract.md`, endpoint `stable/income-statement`, AAPL/quarter/limit40, retrieval `2026-10-20T14:06:05.149732+00:00`, and raw reported USD. FY2016 partial Q4 (2016-09-24): revenue 46852000000, netIncome 9014000000. FY2017 Q1-Q4 (2016-12-31, 2017-04-01, 2017-07-01, 2017-09-30): revenue [78351000000,52896000000,45408000000,52579000000], netIncome [17891000000,11029000000,8717000000,10714000000]. Expected FY2017 endpoints are revenue [45408000000,78351000000] and netIncome [8717000000,17891000000]; partial FY2016 has equal endpoints. Assert projection against these independent constants and render the observations with actual ECharts SVG. Tests must run from a clean checkout without ignored root artifacts. Separately, controller can compare the embedded observations to retained `artifacts/chart-box/fmp/raw.json`, `quarter.csv`, `provenance.json` locally without modifying them or making provider calls. This is observed quarterly dispersion within each year, not annual totals, OHLC or confidence bounds. The bounded fixture establishes numerical/core rendering only; application real-FMP screenshots, controls, effective styles/axes, theme, navigation, refresh, save/reopen/export and publication remain open. Sample pending.

R3 is disproved by field pairing, reaggregation/rescaling, connecting gaps when disabled, spline substitution, invented singleton width, lost reachable series paint or application activation. These findings stop acceptance. This draft makes no visual or chart-family completion claim.

## R3 acceptance

R3 inactive Range Area is independently accepted at Workspace `c6d4329960a5176775a47aba2bfefcac36d0cd8e`. Sixteen focused tests pass (10 unit and six actual ECharts SVG); Biome passes 10 files and combined complexity reports zero errors/violations. Scoped typing retains only inherited typography.ts TS2578, exit 2. Final canonical baseline/candidate each retain 3,427 identical inherited diagnostics, exit 2, with no added/removed diagnostics. Application integration, real-FMP image/browser acceptance, visual comparison and publication remain open. Box Plot remains the active delivery milestone; the published alpha is unchanged.

Independent remediation review: `artifacts/chart-range/r3-revision-review.md`. Stronger actual-SVG checks found stale singleton endpoint labels after empty data; the custom group now replaces its complete children with `$mergeChildren:false`. Seven new production files and three test files remain inactive. The five-row FMP fixture matches retained raw observations only. See [verification](../../../artifacts/reviewed/chart-range/verification.md).
