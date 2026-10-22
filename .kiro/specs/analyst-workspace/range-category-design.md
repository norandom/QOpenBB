# R4d: Range category geometry through both cores

Implement actual number/time category geometry in both inactive Range mappers, then join their tests. This acceptance boundary covers supplied domains/ticks, drawing and identity-safe callbacks; application inference, calendar planning and source-exact pointer interaction remain explicit later joins. No activation switch, disabled controls or isolated replacement mapper is introduced.

2026-10-22; workspace baseline `491d6ca`. Use the retained source findings recorded below and local coordinate, curve and hit research under artifacts/chart-range/. The [accepted numeric foundation](range-value-axis-design.md) remains the only Range value-axis planner. All paths below are relative to `vendor/workspace/terminalpro/`.

## Shared foundation: freeze before fan-out

Controller-owned files: `src/components/General/Table/Chart/echarts/rangeCategoryTypes.ts`, `rangeCategoryCoordinates.ts`, `rangeCategoryAdmission.ts`, and the optional style member in `rangeBarTypes.ts`; Area inherits it. Tests: `tests/unit/chart-compatibility/rangeCategoryCoordinates.test.ts`. Leave projection, statistics and Box code unchanged. The foundation worker is not alone; preserve all other edits.

```ts
type RangeCategoryKind = "category" | "number" | "time";
type RangeCategoryExtent = readonly [] | readonly [number, number];
type RangeCategoryTick = { readonly coordinate: number; readonly label: string };
interface RangeCategoryInput {
  readonly kind: RangeCategoryKind;
  readonly fullExtent: RangeCategoryExtent;
  readonly visibleRange?: readonly [number, number]; // normalized; defaults [0,1]
  readonly ticks: readonly RangeCategoryTick[]; // already selected and formatted
}
interface RangeCategoryStyle {
  readonly categoryAxis: { readonly fields: { readonly type: string } };
  readonly band: { readonly paddingInner: number; readonly paddingOuter: number };
  readonly categoryCoordinates?: RangeCategoryInput;
}
interface RangeCategoryData {
  readonly coordinates: readonly (number | null)[]; // dense groupSlot identity
  readonly observedExtent: RangeCategoryExtent;
  readonly paddedExtent: RangeCategoryExtent;
  readonly minInterval: number | null;
}
interface RangeCategoryPlan extends RangeCategoryData {
  readonly kind: RangeCategoryKind;
  readonly fullExtent: RangeCategoryExtent;
  readonly visibleExtent: RangeCategoryExtent;
  readonly visibleFraction: number;
  readonly ticks: readonly RangeCategoryTick[];
}
rangeCategoryData(projection: RangeBarProjection, kind: RangeCategoryKind,
  family: "bar" | "area"): RangeCategoryData;
resolveRangeCategory(style: RangeCategoryStyle, projection: RangeBarProjection,
  categoryLabels: readonly string[], family: "bar" | "area"): RangeCategoryPlan;
rangeCategoryTransport(plan: RangeCategoryPlan): readonly [number, number] | null;
rangeCategoryEngineCoordinate(plan: RangeCategoryPlan, coordinate: number): number;
rangeCategoryExactSlot(plan: RangeCategoryPlan, engineCoordinate: number): number | null;
rangeCategoryCell(plan: RangeCategoryPlan, groupSlot: number): readonly [number, number] | null;
rangeContinuousBandwidth(plan: RangeCategoryPlan, plotSpan: number, minWidth?: number): number;
```

Add `categoryCoordinates?: RangeCategoryInput` to Bar style. `resolveRangeCategory` is the sole ordinal compatibility boundary: absent input is allowed only for literal `category`, creates slots/ticks from projection and prepared category labels, and exactly preserves the existing count/band-padding domain, including zero/one group transport. Explicit number/time requires matching axis type. Axis paint remains separate from geometry.

Derive coordinates from projected groups: ordinal uses slot; number/time admits finite number category unchanged, string becomes null. Never parse strings, infer dates, reorder projection or accept coordinate overrides. Existing `Map<string|number,...>` projection coalesces equal numeric categories, so no duplicate bucket schema is needed. All-invalid keys produce empty observed/padded extents; identities remain present.

`rangeCategoryData` returns minInterval=null and paddedExtent=observedExtent in category mode (band padding belongs to resolveRangeCategory). In number/time mode it computes the smallest positive absolute consecutive encounter-order difference; invalid coordinates reset adjacency, equal differences do not replace the sentinel. When no positive interval exists, set `minInterval` to `null`. Bar padded extent expands observed endpoints by half a finite interval; Area retains observed extent. This is the later caller's domain input. Supplied full extent is already resolved after padding, explicit endpoint replacement and optional numeric/calendar nicing; never pad it again. No new tick algorithm or Box dependency.

Admission accepts only dense finite plain data, matching kind, ascending extents, strictly ordered ticks inside visible extent and finite derived arithmetic. Window requires `0 <= start < end <= 1`; zero-width navigation is explicitly unsupported until its interaction policy exists. Derive visible extent from full extent and window; empty has no ticks. Equal raw extent stays equal; transport is [0,1], the matching coordinate maps to .5, and observations outside that singleton extent are not drawn. Empty transport is null and suppresses glyphs/targets, with finite empty axes. Preserve raw values in labels/metadata.

`rangeCategoryExactSlot` decodes engine coordinates through the plan and returns only an exact admitted identity, never nearest. Tick labels use the supplied tick table and need not identify observations. `rangeCategoryCell` uses sorted admitted distinct coordinates, midpoint boundaries and clipped visible edges, returning null outside the visible domain and nonnegative raw intervals; it is target geometry, not a source hover algorithm. Keep the index internal if useful, without a caller-supplied bucket contract.

For continuous bandwidth use `R = plotSpan / visibleFraction`, full effective span D and interval I (null means Infinity): `N = D/I + 1`; if minWidth != 0 cap N by floor(R); result `R/max(1,N)`. Default minWidth=1; empty domain returns R. Check every derived result. Do not substitute visible D, count-based widths, an invented singleton interval or nonzero continuous peer padding.

For an explicit ordinal crop, apply the same expanded pixel span to the existing count/padding bandwidth formula. A full window has fraction 1 and preserves the accepted ordinal placement. Item metadata on a partially clipped Bar remains valid when the actual rectangle overlaps the plot, even if its center is outside; axis-only lookup still requires an exact coordinate inside the visible domain.

## Parallel consumers after foundation review

The two consumer workers may prepare their exclusively owned tests against the frozen interface while the foundation is implemented. Production edits wait for independent foundation acceptance; heavy checks remain serialized.

Each lane owns its existing family files plus its named new helper/tests. Pass one resolved plan explicitly from mapper orchestration into every axis, geometry, series and tooltip consumer; do not change RangeBarText or independently reconstruct defaults. Use shared rangeCategoryData eligibility before formatting text so rejected continuous keys produce blank text entries without invoking their display callbacks, then resolve the plan from prepared category labels. Existing ordinal calls and regressions must remain valid.

| Lane | Exclusive paths under `src/components/General/Table/Chart/echarts/` | Required behavior |
| --- | --- | --- |
| Bar | `rangeBar.ts`, `rangeBarAdmission.ts`, `rangeBarAxes.ts`, `rangeBarGeometry.ts`, `rangeBarSeries.ts`, `rangeBarTooltip.ts`; optional cohesive `rangeBarBands.ts` | Replace category-only admission, slot coordinates and category-axis ticks. Series encode `[coordinate,min,max,groupSlot]`; retain explicit metadata. Exclude invalid coordinates without deriving identity from dataIndex. Both directions use shared transport/preflight. Continuous peer padding is zero; source centering subtracts half effective peer width before group offset. Preserve accepted ordinal rounding/placement. |
| Area | `rangeArea.ts`, `rangeAreaAdmission.ts`, `rangeAreaAxes.ts`, `rangeAreaSeries.ts`, `rangeAreaPaths.ts`, `rangeAreaTooltip.ts`; new `rangeAreaHit.ts` | Replace slot geometry/ticks and reversed-index identity assumptions. Keep first-encounter path order. Filter invalid-coordinate observations before null-summary partition: invalid x is skipped; valid-x missing values obey connectMissingData. Targets encode coordinate plus explicit slot and use shared spatial cells. Preflight validates paths, glyphs and nonnegative clipped hit rectangles. |

Bar tests: `rangeBarCategoryCoordinates.test.ts` and `rangeBarCategoryCoordinates.render.test.ts`. Area tests: corresponding `rangeAreaCategoryCoordinates` files. Do not edit shared fixtures during fan-out. Shared types/helpers stay controller-owned; stop and request a contract correction if needed.

Area smooth arithmetic follows the source gradient/sign/flatness and cubic operation order from the curve note. Preserve finite results for nonmonotone distinct keys; reject nonfinite derived geometry explicitly instead of sorting, dropping observations or inventing interpolation. Numeric duplicates have already been grouped; assert that fact through projection rather than building impossible duplicate identities. Existing flat normalized `sourceMode: grouped` snapshots retain ordinal behavior; actual hierarchical capture and `grouped-category` labels/domain ordering remain a later explicit contract, not a silent alias.

## Interaction boundary and join checks

Item tooltip identity comes from metadata; axis callbacks accept only shared exact-coordinate lookup. Raw coordinates are never array indices. Shared rows join the same admitted raw category and skip disabled/null fields. Preserve ordinal callback behavior. New spatial cells provide finite item targets but do not establish source-exact nearest hover.

The later application pointer bridge must supply actual pixel position and family-built candidates: Bar peer-rectangle midpoint; Area high then low endpoints, even with markers disabled. Within-series source comparison is major then minor pixel distance with later exact ties; cross-series comparison uses returned distance, not coordinate-only nearest. Hidden/null candidates, marker-size distance adjustment and zero-distance pagination need that join. Do not implement an unused guessed picker in this slice or claim ECharts snap/target rectangles establish parity.

Acceptance requires actual SVG/custom-series geometry for numeric [0,100,1], irregular epoch values with explicitly supplied calendar ticks, both Bar directions, hidden peers, invalid numeric strings between valid keys, singleton/empty, supplied bounds and partial windows. Assert independent expected positions, source bandwidth and identity labels; inspect Area path order and target dimensions. Include malformed/extreme input and immutability checks. Date text on equally spaced ranks fails this gate.

Run focused new tests and unchanged Range unit/render plus R4c value-axis tests with the existing one-worker Vitest config; run scoped Biome, strict typing comparison, and the established complexity checker with an explicit changed-file manifest. Every changed production file must satisfy 400 physical lines, 300 logical units and 50 per callable. Existing checker/inventory foundation is mandatory; controller updates `.kiro/complexity-budgets.json`, breadth, concise reviewed evidence and affected README/docs checkboxes at join. One heavy gate at a time; no browser/provider/image milestone is claimed.

The controller joins both lanes, obtains fresh independent review and records actual commands/revisions/results. This slice is complete only when both existing cores consume the shared plan and tests demonstrate nonordinal geometry. Full Range acceptance remains open for caller Date provenance, numeric/calendar selection, hierarchical labels, final layout/navigation, source pointer bridge and real-FMP application checks.


## Task acceptance

- [x] R4d.1: independently accept shared types, coordinate resolution and admission.
- [x] R4d.2: implement and review Bar coordinate consumers.
- [x] R4d.3: implement and review Area coordinate consumers.
- [x] R4d.4: join actual render checks, type/size gates and evidence; update README/docs and breadth.
