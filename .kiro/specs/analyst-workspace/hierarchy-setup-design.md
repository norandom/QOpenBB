# H1c inactive hierarchy setup and prepared-node plan

Freeze this boundary before implementing hierarchy setup or dispatching renderer/control consumers. H1c adds pure, independently callable preparation and transition functions; H3 alone activates them in the application. This proposal targets accepted Workspace `61d1475205bd6bd18799309e674cb6d96494ff15`. It is not implementation or verification evidence. No tests, builds, browser, install or commit ran during planning.

The [canonical contract](hierarchy-contract.md), [H0 observed review](../../../artifacts/reviewed/chart-hierarchy/observed-contract-review.md) and [source research](../../../artifacts/reviewed/chart-hierarchy/research-contract.md) own the evidence. This bounded plan applies the local kiro-spec-design boundary/type-safety and light-discovery guidance under the already authorized milestone; it does not change whole-spec approvals. Spec language is English. Complexity, delegation, testing, documentation, CI and root AGENTS guidance were read. The default product.md, tech.md and structure.md steering files are absent; no replacement policy is invented.

## Ownership and completion boundary

One implementer owns only these new Chart-relative production modules:

| File | Responsibility |
| --- | --- |
| `application/hierarchySetupTypes.ts` | Exact prepared projection, edit and transition declarations below |
| `application/hierarchySetupSelection.ts` | Read model/range selections and validate available descriptor roles/order |
| `application/hierarchySetupAggregation.ts` | Full-path grouping, numeric reduction and row provenance |
| `application/hierarchySetupProjection.ts` | Validate retained capture and selection; construct immutable tree and finite subtree weights |
| `application/hierarchySetupTransitions.ts` | Pure setup edits and detached model/range result |

Do not modify H1a types, ordinary setup, Box aggregation, live session types/routing, controls, renderer, dependencies or saved schema. Existing `HierarchySetupSelection`, `HierarchyAssignments`, `HierarchySnapshot`, `HierarchyCategoryPath`, `HierarchySnapshotRow`, `SetupAggregation`, `SetupResult`, `SnapshotColumn`, `ChartModel` and `ResolvedRange` remain their authoritative imported types. The implementer is not alone; preserve others' work. Stop for reviewed ownership changes if these modules cannot contain the task cohesively.

Tests belong in new `tests/unit/chart-application/hierarchySetupProjection.test.ts` and `hierarchySetupTransitions.test.ts`; use the existing chart-application test configuration and small fixture style. Controller owns inventory, breadth, fork manifests, canonical contract freeze and commits. No separate arithmetic framework, generic tree service, copied browser harness or feature flag belongs here.

## Exact proposed consumer contract

All fields below are readonly, including nested arrays/maps. Returned values are detached and deeply frozen. The retained source is the validated H1b capture, not a synthetic transformed snapshot. There is no ordinary `categoryColumnId`, switch flag or sourceMode rewrite.

```ts
export interface HierarchyPreparedDatum {
  readonly sourceRowIds: readonly string[];
  readonly representativeRowId: string;
  readonly categoryPath: HierarchyCategoryPath;
  readonly values: Readonly<Record<string, number | null>>;
}
export interface HierarchyPreparedNode {
  readonly id: string;
  readonly path: HierarchyCategoryPath;
  readonly label: string | null;
  readonly children: readonly HierarchyPreparedNode[];
  readonly datum?: HierarchyPreparedDatum;
  readonly ownWeight: number;
  readonly subtreeWeight: number;
}
export interface HierarchySetupProjection {
  readonly source: HierarchySnapshot;
  readonly selection: HierarchySetupSelection;
  readonly assignments: HierarchyAssignments;
  readonly numericColumns: readonly SnapshotColumn[];
  readonly observationKind: "raw-observations" | "count";
  readonly root: HierarchyPreparedNode;
}
export type HierarchySetupEdit =
  | { readonly kind: "category-add" | "category-remove";
      readonly id: string }
  | { readonly kind: "category-order"; readonly ids: readonly string[] }
  | { readonly kind: "series-add" | "series-remove"; readonly id: string }
  | { readonly kind: "series-order"; readonly ids: readonly string[] }
  | { readonly kind: "aggregate"; readonly value: boolean }
  | { readonly kind: "aggregation-method"; readonly value: SetupAggregation };
export interface HierarchySetupTransitionInput {
  readonly capture: HierarchySnapshot;
  readonly selection: HierarchySetupSelection;
  readonly availableColumns: readonly SnapshotColumn[];
  readonly range: ResolvedRange;
  readonly model: ChartModel;
}
export interface HierarchySetupTransition {
  readonly selection: HierarchySetupSelection;
  readonly range: ResolvedRange;
  readonly model: ChartModel;
  readonly change: "range" | "model";
  readonly recapture?: {
    readonly categoryColumnIds: readonly string[];
    readonly columnIds: readonly string[];
  };
}
export function selectHierarchySetup(
  model: ChartModel,
  range: ResolvedRange,
  availableColumns: readonly SnapshotColumn[],
): SetupResult<HierarchySetupSelection>;
export function projectHierarchySetup(
  capture: HierarchySnapshot,
  selection: HierarchySetupSelection,
): SetupResult<HierarchySetupProjection>;
export function transitionHierarchySetup(
  input: HierarchySetupTransitionInput,
  edit: HierarchySetupEdit,
): SetupResult<HierarchySetupTransition>;
```

The aggregation module exports only its internal preparation boundary to projection: `aggregateHierarchySetupRows(source: HierarchySnapshot, selection: HierarchySetupSelection): SetupResult<readonly HierarchyPreparedDatum[]>`. Consumers use projection, never call the reducer or rederive weights. Validation failures use `SetupResult` with diagnostic code `hierarchy-setup` and a precise selection/source/model path; do not use the misleading ordinary-setup diagnostic helper. Public calls sanitize unexpected failures without reading thrown-object properties.

`datum.values` contains selected numeric observations after the explicit operator, preserving absent keys versus null. With aggregation off it is the last complete-path row's values. These are signed financial observations, never geometric weights. `source` retains every original row, raw category scalar, numeric missingness, labels, units, scale, selected range and original model. `sourceRowIds` lists every row contributing to that canonical bucket in displayed order, including overwritten duplicates; representativeRowId is the final row for off/last and first row otherwise. First/last numeric endpoints apply independently per field, including missing endpoints. Provenance lists candidate input rows, not an assertion that every row supplied a numeric value. Raw per-row values are recoverable through sourceRowIds; do not copy or erase them.

`numericColumns` preserves source descriptor order as selected, with independent size/color units and scale. When Count actually executes, both selected descriptors use unit `observation-count`, scale 1; originals remain in `source`. `observationKind=count` only when categories exist and aggFunc=count. No category means aggregation bypass, so Count saved in a model cannot relabel raw amounts as counts. No currency compatibility check is needed between independent size and color. Never sum color into size, add color to parent totals, or infer an unselected financial field.

## Selection and aggregation semantics

`selectHierarchySetup` validates a treemap/sunburst model, flat compatible metadata, unique descriptor IDs, and unique known range column IDs. It takes selected order from `range.columnIds`, partitions by descriptor role into categoryIds and seriesIds, and preserves order within each. Zero categories and zero numeric fields are valid. More than two numeric fields, unknown IDs, invalid operator or incompatible family returns invalid. Read root `model.aggFunc`; absent means off. `model.switchCategorySeries` is not a hierarchy edit or projection behavior; preserve unrelated persisted fields without applying inversion.

Projection requires selection.categoryIds to equal source.categoryColumnIds exactly, including order. A different category set/order requires recapture, because H1b retains only selected category vectors. Numeric selections must be unique selected captured numeric descriptors, at most two; extra captured numeric descriptors/values may remain retained. Derive sizeId=seriesIds[0], colorId=seriesIds[1], omitting absent keys. Removing the first numeric field promotes the remaining one to size; zero numeric fields is deliberate count weighting, never fallback selection.

Group by the full canonical path, using a Map and JSON-array identity. Owner-approved correction, 2026-10-25: keep missing categories distinct from literal names during explicit aggregation. The original object-key aggregator merges null with the string "null"; this safe canonical-path contract deliberately corrects that collision. Null remains distinct from the string "null", empty string remains distinct from null, numeric 1 and string "1" share canonical "1", and boolean true shares canonical "true" with its string. Preserve raw scalar types in source. No concatenated delimiters, prototype-key hazards or raw-type identity grouping.

With categories and aggregation off, keep the last row's values for each full path while preserving the first encounter's bucket position. Explicit last has the same endpoint values but recorded operator/count provenance. With an operator, reduce both selected numeric fields before constructing any parent nodes:

| Operator | Result for each complete-path bucket |
| --- | --- |
| off | Last complete row's field, including absent/null |
| first / last | First/last field endpoint, including absent/null |
| min / max | Extrema of finite observations; no numeric observations gives null |
| sum | Ordered sum starting at the first finite observation; no numeric observations gives null |
| avg | Ordered accumulation starting at positive zero, divided by numeric observation count; no numeric observations gives null |
| count | Original bucket row count, including missing/null values |

With no categories, bypass aggregation for every operator. Every source row remains an independent unlabeled leaf at path []; its datum sourceRowIds contains only its ID. Do not collapse empty paths, invent a category or convert raw values to counts. Reproject from retained source for every edit; never aggregate an earlier prepared tree or count an earlier Count result.

## Tree identity, finite arithmetic and geometry

Pinned G42254-42333 uses a Map per category level; fixed categoryKeys.length means every ordinary flat row has the same depth. Repeated leaf labels under different parents are distinct. Retain child order by first path encounter. Do not sort preparation; later Treemap sorts effective weights while Sunburst preserves input order under its own renderer contract.

Use these exact proposed deterministic IDs (replacement identity encoding, not an upstream ID claim): root `JSON.stringify(["hierarchy-root"])`; each category node `JSON.stringify(["hierarchy-path", selection.categoryIds, prefix])`, where prefix is its complete string/null path; each no-category leaf `JSON.stringify(["hierarchy-row", sourceRowId])`. Full arrays preserve category order and avoid escaped delimiter, null/string, prototype-like and parent/leaf prefix collisions. IDs are stable across amount changes and duplicate representative changes. Reordering categories intentionally changes category-node IDs. The root is synthetic, path [], label null, no datum, ownWeight 0.

A prefix such as ["West"] and a leaf such as ["West","West"] are separate nodes. Do not trim null/empty components or interpret them as early path termination. H1b's fixed-length vectors prohibit a node simultaneously being a terminal flat leaf and a parent; reject malformed input instead of inventing internal own-value merging, synthetic self children or variable-depth tree semantics. Pinned source supports internal own values for its distinct auto-group route, which remains outside the accepted flat capture. Every nonroot internal node has no datum and ownWeight 0. Every leaf has datum and children [].

When size is selected, leaf ownWeight is max(finite numeric size, 0); absent/null size gives 0 and no area. Preserve the original datum as missing or signed, not a measured zero. Without size, leaf ownWeight is 1 regardless of unselected amounts. Internal subtreeWeight is the sum of child subtreeWeight; leaf subtreeWeight equals ownWeight. Keep zero-weight leaves in preparation for provenance; renderer must exclude zero area, including the blank all-zero case. Parent totals are derived geometry only and are not exposed as observed financial tooltip amounts. Color stays a signed/missing datum; color domain and fallback remain H2 rendering responsibilities.

No setupArithmetic.ts exists at the accepted revision. `setupAggregation.ts` has a private reducer with unchecked additions and scalar-category grouping, so cannot safely supply this contract. `boxPlotSetupProjection.ts` has a private source-faithful reducer plus finite-result rejection, but Box-specific keys/diagnostics prevent direct reuse. Reuse their exported `SetupAggregation` and result conventions; keep the small hierarchy reducer local without altering either family. Reuse H1b validateHierarchySnapshot and its safe JSON copy boundary for detached source/model/range data; never run arbitrary coercion hooks.

Preserve the pinned original finite-input operation order, including first-number Sum and strict min/max ties (signed zero). Detect nonfinite sum/average accumulation or derived subtree totals and return invalid with the bucket/source-column or node path. Do not clamp to MAX_VALUE, drop a failing child, normalize all weights, turn overflow into missing or silently use a different summation algorithm. This proposed finite-failure policy follows the existing Box safe boundary; it is not an original browser observation. Reject overflow even when a different summation order could recover a finite result. All missing Sum/Avg remains null, and absent first/last keys stay absent. No NaN/Infinity can reach prepared output.

## Pure edits and exact writes

Validate current selection, captured category vectors and model family before applying an edit. availableColumns supplies the full current descriptor inventory; it does not fabricate captured observations. Adds require an unselected ID with the correct role; removals require a selected ID; orders require an exact duplicate-free permutation. Category count is unbounded, numeric count is 0..2. Reject switch-category-series and malformed runtime edit objects. Aggregate on sets sum; off removes aggFunc; method requires an enabled operator. Aggregate edits require at least one category. Removing the final category preserves a preexisting root aggFunc but it becomes inactive through no-category bypass; readding categories reactivates it. This is source-derived, not browser-observed: G46824-46899 multi-select removal updates column state without clearing aggregation; the clear at G46846 belongs only to the single-select default-category branch. G46994-47000 merely hides aggregate controls without selected dimensions, and G42701-42706 bypasses reduction.

Category/series add/remove/order produces change=range, updates `range.columnIds` and `model.cellRange.columns` to `[...categoryIds,...seriesIds]`, preserves originalRange members and explicit row bounds, and leaves unrelated model/options fields intact. Aggregation edits produce change=model and change only root `model.aggFunc`; off deletes the own property rather than storing null/false. No setup field is written beneath chartOptions. Return a detached complete model so H3 can replace `storage[stateKey].chartModel` rather than merge a deleted flag back in. H3's existing applyRangeTransition owns `storage[stateKey][family].cellRange`.

Set recapture whenever ordered categories differ from capture, or any next numeric ID is not in capture.selectedColumnIds with a numeric descriptor. Its categoryColumnIds is exactly the next category order. Its columnIds contains those categories followed by next selected numeric IDs, then previously captured selected numeric IDs not already included, in previous order. This retains numeric observations for later reselect while forbidding extra category vectors. A pure numeric removal/reorder needs no recapture. Returning a transition does not authorize projection before requested recapture completes.

H3 serially integrates hierarchy own-kind/family narrowing, selection reads, retained capture storage and setup commands. It must validate synchronous editor stamp first; compare current resolved selection/range against the command's baseline; validate recapture address, generation/data revision and ordered category IDs plus required numeric IDs; then project and commit atomically. Waiting, stale, invalid or mismatched capture must write nothing. Refresh/data-generation changes invalidate old commands. H1c neither constructs stamps nor writes storage. Existing applicationSessionSetup/sessionState/sessionRange owners remain authoritative; remove forced flat casts only at H3's complete union join.

## Lean RED tests and review gates

Implement these behavior groups in the two new suites; expected RED comes from missing exports/behavior before production edits. Retain concise GREEN evidence after implementation. No browser/build/provider call is needed for inactive H1c.

1. Full-path synthetic groups: observed West/Alpha off Size/Color 6/20, Sum 8/10, Avg 4/5, Count 2/2; Gamma missing Color Count 1; first/last/min/max endpoints, all-missing and negative signed observations. Assert repeated leaf names under different parents and first-path insertion order. Reproject Sum -> Count -> off from the same unchanged source.
2. Category identities: canonical 1 collisions while raw number/string remain retained, boolean strings, null versus "null", empty, delimiter-bearing/prototype-like labels, repeated prefix labels, and stable IDs after value/representative changes. Reject malformed vector depth. These mixed-scalar cases are source-derived tests, not original File observations.
3. No categories with all seven operators and off: each row survives with unique row ID, path [], label null, raw missingness, no Count descriptor relabel. Selected missing/zero/negative size has zero weight; no numeric selection gives weight 1 each; numeric reorder changes assignment; all-zero root total is zero. Assert missing color stays missing and cannot affect weight.
4. Finite boundaries: Sum/Avg and subtree overflow produce invalid without partial output, absent first/last versus null, signed-zero extrema ties, detached/frozen source and output. Wrong-family/invalid selection/unknown operator fails safely. An unsafe thrown object must not escape public failure handling.
5. FMP fixture: use retained [FY2025 hierarchy CSV](../../../artifacts/chart-hierarchy/fmp/fy2025-hierarchy.csv) values and provenance, eight leaves only, no color. Assert each quarter's component total: Q1 124300000000, Q2 95359000000, Q3 94036000000, Q4 102466000000; root 416161000000 USD. Revenue is an independent expected reconciliation value, never another leaf. Numeric scale remains reported USD; parent geometry never mutates leaf observations. This is numerical fixture validation, not live-FMP application evidence.
6. Transitions: empty/multicategory selection, add/remove/order and numeric cap, exact model/cellRange writes with preserved unknown options and bounds, aggregation deletion, final-category removal/bypass, retained numeric recapture requirements, invalid order/role/switch edits and immutable inputs. Test exported pure transition output, not live session or invented stamp handling.

Planned from terminalpro using the existing installed locked toolchain:

```sh
node node_modules/vitest/vitest.mjs run --config tests/unit/chart-application/vitest.config.mjs tests/unit/chart-application/hierarchySetupProjection.test.ts tests/unit/chart-application/hierarchySetupTransitions.test.ts --maxWorkers=1
node ../../../verification/node_modules/typescript/bin/tsc --project tests/unit/chart-application/tsconfig.json --pretty false
```

Capture static baseline first; report inherited diagnostics separately rather than claim a clean build. Run scoped existing formatter/lint and the inventory-backed combined checker using the exercised command in [complexity documentation](../../../docs/complexity.md) and controller-supplied explicit fork scope. Every new production file must pass 400 physical lines/file, 300 logical units/file and 50/function. Target each module below 250 physical lines, separating selection, bucket reduction, node construction and transitions by responsibility. Checker/inventory foundation already exists; controller must register every new maintained module and actual test/evidence paths before acceptance. These are planned checks, not completed tests.

An independent reviewer must approve this contract before implementation and then inspect implementation, RED/GREEN evidence, static deltas and complexity output. Controller obtains fresh verification before acceptance. H2 renderer and controls may fan out only after this exact projection and their separate appearance contract are frozen, with disjoint paths; neither may change these setup declarations concurrently. H3 remains a serial join and H4 owns visible controls, geometry comparison, export, refresh and fresh-session reopen. Anthropic-before-Excel remains unchanged; neither lane is part of this task.
