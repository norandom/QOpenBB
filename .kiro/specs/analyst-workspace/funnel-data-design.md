# F1: freeze Funnel data interfaces and prepare finite geometry inputs

Implement one bounded types-and-adapter task before renderer work. The adapter consumes the existing `SetupProjection`, chooses the first selected numeric descriptor and preserves every projected row. It does not capture, aggregate, format, persist or render data. This design follows the approved rules in [the contract](funnel-contract.md), read 2026-10-26. Independent interface review approved the bounded F1 task on 2026-10-26. Implementation acceptance remains separate.

## Exclusive implementation ownership

Paths below are relative to `vendor/workspace/terminalpro/`:

- New `src/components/General/Table/Chart/compatibility/funnelContracts.ts`: public readonly types and family guard/native-type map.
- New `src/components/General/Table/Chart/echarts/funnelData.ts`: pure admission and normalization over `SetupProjection`.
- New `tests/unit/chart-compatibility/funnelData.test.ts`: independent behavioral assertions, using existing real ordinary setup projection in fixtures.

Parent owns `.kiro/complexity-budgets.json`, fork changed-file manifests and eventual shared routing. Worker must preserve other edits and must not modify shared snapshot/setup/session/renderer code. No new capture owner or global observation policy in F1. Unused modules are intentional until F3 wires them.

## Frozen public interface

`funnelContracts.ts` imports `SnapshotColumn`, `SnapshotDiagnostic` from `./snapshotTypes` and `SetupValueOrigin` from `../application/setupTypes` as types only:

```ts
export type FunnelFamily = "funnel" | "coneFunnel" | "pyramid";
export type NativeFunnelType = "funnel" | "cone-funnel" | "pyramid";
export function isFunnelFamily(value: unknown): value is FunnelFamily;
export function nativeFunnelType(family: FunnelFamily): NativeFunnelType;

export interface FunnelStageIdentity {
  readonly index: number;
  readonly rowId: string;
  readonly category: string | number;
  readonly label: string;
}
export type FunnelStage = FunnelStageIdentity & (
  | { readonly kind: "missing"; readonly reason: "absent" | "null";
      readonly origin?: SetupValueOrigin }
  | { readonly kind: "value"; readonly value: number;
      readonly magnitude: number; readonly origin: SetupValueOrigin }
);
export interface FunnelData {
  readonly family: FunnelFamily;
  readonly field: SnapshotColumn;
  readonly observationKind: "raw-observations" | "count";
  readonly stages: readonly FunnelStage[];
}
export interface FunnelMagnitudeData extends FunnelData {
  readonly family: "funnel" | "coneFunnel";
  readonly maxAbs: number;
  // Null slots retain missing stage positions; zero is a real observation.
  readonly magnitudeRatios: readonly (number | null)[];
}
export interface PyramidData extends FunnelData {
  readonly family: "pyramid";
  readonly maxValue: number;
  readonly scaledTotal: number;
  readonly axialRanges: readonly (
    { readonly start: number; readonly end: number } | null
  )[];
}
export type FunnelDataResult =
  | { readonly status: "ready";
      readonly value: FunnelMagnitudeData | PyramidData }
  | { readonly status: "empty";
      readonly reason: "no-series" | "no-rows" | "no-values";
      readonly stages: readonly FunnelStageIdentity[];
      readonly field?: SnapshotColumn }
  | { readonly status: "invalid";
      readonly diagnostics: readonly SnapshotDiagnostic[] };
```

`funnelData.ts` imports the actual `SetupProjection` from `../application/setupTypes` and exports only:

```ts
export function buildFunnelData(
  projection: SetupProjection,
  family: FunnelFamily,
): FunnelDataResult;
```

The native map is a pure finite lookup. Diagnostics use exact snapshot-relative paths such as `["rows", i, "values", field.id]` and stable codes `funnel-value`, `funnel-origin`, `funnel-orientation`, `funnel-source-column`, `pyramid-negative`, `pyramid-total`. Invalid output carries no drawable geometry. Existing session will later keep source data/controls and surface these diagnostics; F1 adds no UI.

## Admission and identity rules

1. The first numeric descriptor in `projection.snapshot.selectedColumnIds` order is the chosen field; descriptor storage order does not choose it. Category IDs are skipped. No selected numeric descriptor returns `empty/no-series`; do not fall back to an unselected field. Multiple selected numeric descriptors remain untouched and the adapter uses only the first. Later selected-field removal naturally promotes the next selected numeric field without rewriting saved range.
2. `SnapshotRow.id` is the stage identity and index is its projected position. Label is `String(row.category)`; preserve the original category too. Duplicate labels remain distinct without aggregation. Output arrays include one position per input row, including missing stages. Never sort by value, filter missing slots or key by label.
3. Input precondition is an unswitched ordinary projection. The actual `OrdinarySetupProjection` uses `kind` (not mode): reject `projection.setupProjection?.kind === "ordinary-switch"` with `funnel-orientation` at `["setupProjection", "kind"]`. This rejects a supported generic setup shape that is outside Funnel scope, not corrupt source data. No new capture flag is needed. Aggregation belongs exclusively to `projectOrdinarySetup`/`aggregateSetupRows`. Adapter receives its output without reaggregation. For a numeric stage, require `projection.valueOrigins[row.id][field.id]` and valid nonempty sourceRowIds; missing/invalid origin uses `funnel-origin`. A sourceColumnId different from field.id uses `funnel-source-column`, explaining that this provenance shape is unsupported for unswitched Funnel input. Do not claim this mismatch detects every switched projection when the explicit discriminator is absent, especially all-missing data. Copy the origin and its sourceRowIds, preserving source/count meaning. Aggregated rows carry the aggregate owner's identity and provenance; do not invent original row IDs. `projection.observationKind` controls later formatter choice; geometry consumes the resulting numbers identically. Existing Count includes missing group rows: preserve the aggregate owner's count, the selected descriptor's `observation-count` unit/scale 1, and the origin's original source unit/scale independently. Never replace source-unit provenance with the derived field unit.
4. Absent own field is missing/absent. Explicit null is missing/null. Neither receives a numeric value, magnitude or normalized coordinate. Missing origin is permitted for missing stages. An own undefined, nonnumber, NaN or infinity is `invalid/funnel-value`, even when passed by a caller violating the nominal validated-snapshot type. Defensive checks apply to the chosen field; F1 does not replace validation of the complete snapshot.
5. Empty rows return `empty/no-rows`. All missing values return `empty/no-values` with retained identities and selected field. Zero observations count as usable. All-zero Funnel/Cone returns ready with maxAbs=0 and every present ratio=0. All-zero Pyramid is invalid with an accessible positive-total diagnostic for the later session. Negative Pyramid values invalidate the whole projection, including if positives would yield a positive sum.
6. Funnel/Cone retain signed `value`, set `magnitude = Math.abs(value)` and ratio `maxAbs === 0 ? 0 : magnitude/maxAbs`. Preserve signed raw values for labels/tooltips; do not infer sign from magnitude. Ratios must be finite in [0,1]. Null slots prevent later neighbor connections across a missing endpoint; renderer must test original adjacency.
7. Deep-copy the descriptor, including nested JSON in `SnapshotColumn.metadata` (a shallow spread is insufficient), identities, stage values and origin arrays into output. A structured clone of this plain-data descriptor is appropriate. No callbacks/functions, display formatter or mutable input references are required. Do not freeze/mutate the supplied projection. Runtime freeze of output is unnecessary if readonly typing and detached structures are maintained. Apply the same descriptor copy to empty-result field metadata.

## Stable Pyramid normalization

Never form the unscaled sum. For finite nonnegative usable values, find `maxValue` by a loop, then compute each scaled value `value/maxValue`. A zero maximum fails positive-total admission. Sum the scaled values with compensated summation; each is in [0,1], so the retained array cannot overflow merely because raw observations approach Number.MAX_VALUE. Compute cumulative compensated scaled sums and divide by `scaledTotal` to obtain axial boundaries. Missing stages get null, do not contribute and do not move the boundary. Genuine zero gets equal start/end. Clamp boundaries monotonically into [0,1] against rounding; force the last positive stage's end and later zero stages to exactly 1. Do not fabricate a positive extent for an underflowed or subpixel value.

Require finite positive `scaledTotal`, finite boundaries, nondecreasing ranges and start/end in [0,1]. `maxValue` and `scaledTotal` describe normalization without an overflowing raw total. The ratio for a tiny observation can round to zero in binary64; raw `value` must remain intact for tooltip/display. This is finite-precision loss in geometry, not missing data or permission to round source values. No equal-area/square-root transformation belongs here.

## Focused evidence and tests

Follow `tests/unit/chart-compatibility/heatmapData.test.ts`: build a `ChartSnapshot`, pass it through actual `projectOrdinarySetup`, then assert pure adapter output and unchanged input. Follow `waterfallTotals.test.ts` with node environment for this pure suite. Do not assert helper call counts or mirror the implementation loop.

Required independent assertions:

- Selected-ID ordering chooses first numeric field even if descriptors are reversed; no-series does not select an unselected reserve field; removal promotes the remaining selected field.
- Duplicate stages and missing middle stage keep row identity/order; null and absent remain distinct; no invented zero. Assert complete aligned normalized arrays, allowing later renderer to refuse bridging gaps.
- Existing Sum and Count produce expected aggregate values and source-row origins; Count includes missing group rows. Assert the output field uses `observation-count`/scale 1 while origins retain their original source unit/scale. The adapter does not sum again. No aggregation preserves the original five positions.
- Actual `ordinary-switch` projection returns `funnel-orientation`; a numeric stage with differing sourceColumnId returns `funnel-source-column` as unsupported provenance shape. Neither case is described as source corruption.
- Nested metadata mutation isolation: mutate an output descriptor's nested metadata through an explicit test-only mutable cast and assert input unchanged; separately mutate input metadata after adaptation and assert output unchanged. Assert origin sourceRowIds are detached too, including the empty-result descriptor case.
- Signed Funnel/Cone input [-8,0,4] yields maxAbs=8 and ratios [1,0,0.5], values remain [-8,0,4]. All-zero yields finite zeros. MAX_VALUE and negative MAX_VALUE produce ratios 1 without overflowing.
- Pyramid [1,1] yields [0,0.5],[0.5,1], proving axial fractions rather than equal-area geometry. [MAX_VALUE,MAX_VALUE] yields the same finite ranges without a raw sum. Include subnormal-only positive values, zeros interleaved with missing stages, and widely separated magnitudes; assert bounded monotonic ranges and retained raw values.
- Pyramid negative values, zero-total values and malformed own undefined/NaN/infinities return diagnostics with exact field paths and no geometry. Empty/no-series/no-values recover by a second pure call with restored observations.
- Financial fixture exact AAPL FY2026 Q2 values [111184000000,54781000000,35885000000,35833000000,29578000000], matching retained [reviewed financial reconciliation](../../../artifacts/reviewed/chart-funnel/assessment-review.md). Hardcode observed financial amounts in the test with source/date/hash rationale; do not import ignored artifacts into maintained test entrypoints. The test confirms unchanged signed reported levels, not issuer/provider freshness.

From `vendor/workspace/terminalpro`, with the installed project toolchain, run:

```sh
bunx vitest run --config tests/unit/chart-compatibility/vitest.config.mjs tests/unit/chart-compatibility/funnelData.test.ts --maxWorkers=1
```

This is a proposed focused command using an inspected existing config (includes that directory, maxWorkers=1); F1 has no test file yet, so it has not run and cannot be marked passing. Run the existing strict chart typecheck/toolchain entrypoint used by the parent for the production imports after implementation; do not claim full application typecheck success from isolated adapter tests.

## Caps and closing handoff

New production files have no baseline and must each stay within 400 physical lines, 300 logical units/file and 50/function. Imports target unchanged `snapshotTypes.ts`, `setupTypes.ts` and `heatmapData.ts` patterns; F1 modifies none of those. Shared lifecycle remains at 394 physical lines and is explicitly outside F1. Parent updates inventory and prepares current Workspace/data_api changed-file manifests before the combined cap gate. From repository root in WSL/Linux with pinned Node on PATH:

```sh
pipeline/.venv/bin/python -m tools.quality.complexity --check \
  --changes workspace=artifacts/chart-funnel/f1/workspace-changes.json \
  --changes data_api=artifacts/chart-funnel/f1/data_api-changes.json \
  --output artifacts/chart-funnel/f1/complexity.json
```

Manifest paths are proposed outputs, not existing evidence. Parent must generate correct current fork scope including new production files; never copy historical manifest SHAs blindly. Acceptance requires focused tests, actual full-file cap output, independent review of admission/provenance/numerical cases and fresh verification after fixes. F1 does not claim rendering, integration, persistence, export or completion of the Funnel milestone.
