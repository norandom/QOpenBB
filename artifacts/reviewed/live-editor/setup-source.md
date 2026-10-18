# Implement Set Up from the retained ordinary capture

Task 2.73 source handoff, 2026-10-18. The seven aggregation operators and category/series inversion are source-resolved. Implement selection, aggregation, then optional inversion from the retained untransformed capture; disabling either transformation recomputes from that capture. Do not try to reverse an aggregate or recover an alternate category from the currently selected snapshot. This audit changes no production code, phase status or acceptance evidence and runs no tests.

Scope follows the integration design (`../../.kiro/specs/openbb-self-service/chart-live-editor-integration-design.md`, local source reference), contracts (`../../.kiro/specs/openbb-self-service/chart-live-editor-contracts.md`, local source reference), task 2.73 and original range contract (`../../.kiro/specs/openbb-self-service/chart-grid-range-contract.md`, local source reference). Production handoff caps remain 400 physical lines/file, 300 logical units/file and 50/function. The documentation-only handoff is exempt. Core product/tech/structure steering files remain absent.

## Source identity and finite operator contract

All bundle line references below refer to AG Grid Enterprise main.cjs.js (`../task-2.1/frontend/terminalpro/node_modules/ag-grid-enterprise/dist/package/main.cjs.js`, local source reference), version 34.1.1, SHA256 `ff634fef7612738444a1618604ea88c0625328f271382f2fb3aaf9a26926d30c`. This is read-only installed reference source, not a dependency to reintroduce.

`CategoriesDataPanel` lines 46241-46331 fixes the menu order to `sum`, `first`, `last`, `min`, `max`, `count`, `avg`. Aggregate on selects `sum` every time; off assigns undefined. The picker calls `setAggFunc`. Aggregate is displayed only when a selected dimension differs from `AG-GRID-DEFAULT-CATEGORY`. Selecting that default category silently clears aggregation before the range update (46170-46179). Do not derive the chart menu from the differently sorted general aggregation-service menu.

For ordinary finite numeric/null/missing observations, the exact reducers are at 24122-24239:

| Operator | Input contract and result |
| --- | --- |
| sum | Add numeric values in encounter order, including negatives and zero; ignore null/missing; return null when no numeric value exists. |
| first / last | Return the first/last observation itself, including a null or missing endpoint; do not skip it. Empty input returns null. |
| min / max | Numeric minimum/maximum, including negatives; ignore null/missing; return null when none exists. |
| count | Count observations, including null/missing; ordinary `[null, -4, 0]` produces 3, not 2. Library nested-aggregate objects can contribute their own `.value`, but those are outside ordinary finite capture. |
| avg | Sum numeric values divided by their numeric count; null/missing do not enter numerator or denominator. All missing returns null. Library weighted nested aggregates and bigint behavior are outside this finite numeric adapter. |

Independent expected examples, derived from the source rather than claimed runtime observations: `[null, -4, 0, 10, null]` produces sum 6, first null, last null, min -4, max 10, count 5 and avg 2. For `[null, null]`, all results are null except count 2. Represent a missing first/last result by an absent numeric key; never introduce own undefined into `SnapshotRow.values`.

`ChartDatasource.getData` aggregates before the controller can invert (41919-41939, 42061-42120). Ordinary aggregation groups by selected dimension and applies each reducer independently to each numeric column; it does not add revenue to operating income. Groups retain first-encounter order and the first encountered dimension value. The implementation uses JavaScript object property keys, so numeric/string keys that coerce identically collide; null and the literal string `"null"` can also collide. Duplicate ordinary labels collapse under aggregation only. Do not accidentally substitute category-wrapper IDs as group keys. Use safe own-key storage when matching coercion; inherited object keys in this upstream implementation are not a financial behavior to reproduce as unsafe code.

## Matrix inversion, identities and financial meaning

`ChartController.getChartUpdateParams` and `invertCategorySeriesParams` (45010-45059) provide the complete operation. Given selected category C, ordered fields F and ordered rows R after aggregation:

1. Output category key is `AG-GRID-DEFAULT-CATEGORY`.
2. Each source row R[i] becomes a numerical series with original key `${C.id}:${i}` and label `R[i][C.id] == null ? "" : String(R[i][C.id])`.
3. Each selected original field F[j] becomes one output row; category label is F[j].displayName and value at series i is R[i][F[j].colId].

The numeric matrix is transposed, with no scaling, summing, sorting or missing-value fill at this step. Duplicate category labels remain distinct series. Original export keys are positional within the current view; they are not immutable source-row identities across filter/sort changes. Keep stable source row/column identities in adapter provenance and recompute original positional keys on view changes. Never identify a series by display label. Inversion is ignored for grouped-grid charts and unsupported families; the ordinary groupedColumn/stackedColumn/line input remains a flat captured grid even when the resulting observations are aggregated.

Keep `originalModel` and `selectedRange` in original grid coordinates. Synthetic output descriptor IDs/category IDs describe render data only and must not replace the stored grid range. Keep an immutable ordinary capture so switch off restores source order and identities, including duplicates; aggregate off restores the individual observations rather than splitting a sum.

Unit/scale metadata must come from real column/provider declarations. Header text and fixture labels are not a metadata parser. Ordinary undefined unit/scale stays undefined under the explicit raw-observations policy; do not insert USD, dimensionless, scale 1 or million scaling. Sum/min/max/first/last/avg retain each source column's declared unit/scale when available. Count derives an observation count, not currency: its descriptor and display formatter must not retain a currency or percent formatter, and its numerical scale is not the source financial scale.

After inversion, one output series can contain values from several original columns. It cannot inherit one original column's unit/scale unless those declarations agree across the contributing columns. Preserve per-value origin for display, and never claim mixed known units are comparable by assigning a synthetic homogeneous unit. Unknown raw observations remain unknown. Known contradictory units must remain distinguishable and must not pass as one declared-unit axis merely because inversion succeeded. This seam requires controller agreement with the renderer/display adapter; it is not resolved by changing `sourceMode` to flat.

## Range/model writes and persistence

`DragDataPanel` (46137-46232) sets the chosen category, adds/removes selected series and sets selected order for additions/reorder. `ChartDataModel.updateColumnState` and `reorderColState` (42655-42691) preserve ID-based selection and sort by order; `setValueCellRange` (42725-42752) exports selected numeric columns in that order. `getCellRangeParams` (45326-45340) concatenates actual range columns. For ordinary single-category charts, changing the category selects exactly one category. Removing a numeric pill removes it from the selected range, not from the source column registry.

`updateForPanelChange` (44998-45005) updates ranges and data, then calls `setChartRange` and emits `chartRangeSelectionChanged`. `setChartRange` can also emit `chartOptionsChanged`; do not assume the range event is the only event. Switch (45101-45105) writes root `switchCategorySeries` then raises the model/options event. Aggregate (45110-45117) writes root `aggFunc`, recomputes data and raises the model/options event. `getChartModel` (45061-45079) exports both flags alongside original cellRange. `raiseChartOptionsChangedEvent` (45363-45372) carries chartOptions but not those root flags; the consumer must obtain the current model, not extract aggregate/switch from the options payload.

The original application range contract (`../../.kiro/specs/openbb-self-service/chart-grid-range-contract.md`, local source reference) identifies addressed persistence: options events retrieve/save the full model; range events save `storage[stateKey][chartType].cellRange` while integrated chart view is enabled. Preserve the existing Widget functional updater and unknown model/storage branches. Reordering/removal is thus a range transition, while aggregate/switch are root model transitions. Detached recreation has a documented asymmetry and is outside this ordinary integrated handoff. Source ownership does not prove backend readback or reopen.

## Existing runtime evidence, without recapturing closed facts

The focused initial captures (`../reviewed/parity/editor-runtime-next/focused/setup-Aggregate-on.json`, local source reference) show Sum on writing `aggFunc: "sum"`, duplicate Q1 rows becoming 220/45, and off restoring 100/20 and 120/25. The initial switch capture (`../reviewed/parity/editor-runtime-next/focused/setup-Switch-Category-Series-on.json`, local source reference) proves root flag, four `period:0..3` bindings and duplicate Q1 labels, but its whitelist omits the numeric leaves.

That omission was already closed by the later numerical capture (`../reviewed/parity/editor-contract-close/setup-Switch-Category-Series-on.json`, local source reference) and report (`../reviewed/parity/editor-contract-close/report.md`, local source reference), observed 2026-10-17 against original Workspace `38dffc33389aca0e4a87e0e88d42f7067aa220df` and image `sha256:f48eb1c9b32e1f84d5199dafc943bc1fc10f3b1745ab29860975d002dc5c8a3f`. Output rows are Revenue `[100,120,140,160]` and Operating Income `[20,25,30,40]`; default-category wrappers have IDs 0/1. Switch off restores the four original rows. Later Sum geometry is settled and independently checked. Do not reopen these numerical capture gaps.

The remaining evidence limitations relevant to this adapter are finite: non-Sum operators and negative/null cases are source-established, not runtime-exercised by these captures; general category changes/series reorder/removal and persisted reopen were not demonstrated here. Implement and assert their source-defined results in the consuming task, and cover real application save/reopen in the scheduled join. A new original-runtime observation is needed only if a concrete discrepancy remains; no generic capture project is necessary.

An alternate category is an actual capture-input gap: `ChartSnapshot` stores one chosen `row.category` plus numeric values. Even if its descriptors list another category, the alternate row values are absent. On category change, recapture the selected displayed rows with that category from the current grid and unchanged ordered range semantics, or retain a separately typed complete grid capture at the existing boundary. Do not copy the current category, infer labels from row IDs, or parse formatted cell text. This is production recapture, not a request to repeat the already closed reference transpose experiment.

## Minimal mapper seam for controller freeze

Current `translateCartesian` rejects every non-flat source before mapping. Task 2.73 must emit `grouped` for aggregation and `transformed` for inversion (including aggregate then inversion), rather than falsely marking transformed observations flat. Controller approved this bounded shared contract direction during the audit. Exact finite optional addition to `CartesianMappingContext`:

```ts
type SetupAggregation = "sum" | "first" | "last" | "min" | "max" | "count" | "avg";
type OrdinarySetupProjection =
  | { readonly kind: "ordinary-aggregate"; readonly aggFunc: SetupAggregation }
  | { readonly kind: "ordinary-switch"; readonly aggFunc?: SetupAggregation };
// CartesianMappingContext.setupProjection?: OrdinarySetupProjection
```

Only the pure adapter over a validated complete ordinary flat capture emits this context. The mapper validates the finite operator and exact kind/sourceMode pairing. With no context the strict flat-only behavior remains; pivot, remote-page, unknown transformations and contradictory pairings remain rejected. Carry the same stateAddress/dataRevision from the source. This is transient provenance, never a new saved envelope, renderer output in storage, or arbitrary transformation framework. The witness is not proof of arithmetic: adapter validation and independent expected-result assertions establish that. Pure selection/reorder without an arithmetic/orientation transform remains flat. Controller freezes this shared seam before 2.72/2.73 consumers change it.

Source review verdict: **APPROVED for the bounded shared contract addition only**. Exact pairing is `ordinary-aggregate` with `grouped`, and `ordinary-switch` with `transformed`; a witness on `flat` is contradictory and rejected. Missing witness admits only flat. Controller owns the declaration edit; 2.73 owns producer/source validation and numerical tests; 2.72 owns finite witness/mode validation without weakening default callers. This verdict is not implementation acceptance and does not settle the separate per-value financial display seam identified above.
