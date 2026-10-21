# B3b Box capture and setup contract

Connect the accepted category helper to an inactive Box snapshot policy and setup projection. Preserve raw aggregate keys before statistical grouping and implement the seven original finite-observation aggregates inside the Box adapter. Do not activate the gallery/session family or change visible controls. B3c axes/navigation and B3d application activation remain separate.

This accepted contract follows the [B3 ownership reservations](box-plot-integration-design.md#exclusive-ownership-and-bounded-task-split). B3a is accepted at Workspace `bca180284cefb7848b052dd4b8a4160fe0c0d5e8`. Inspection on 2026-10-21 used that revision and root `a37255c`. Reuse the current steering and [milestone](box-plot-milestone.md); B3b acceptance is recorded below.

## Source evidence and numerical decision

Original source identity remains [B1 Source contract](box-plot-design.md#source-contract): retained Grid34.1.1 SHA-256 `1a195685c473488defe1ce535e3115c26a42b2be94ad6ccc7fefa351eac7094f`. Relevant physical lines are G6298-6440 (built-in aggregates), G6456-6471 (`_aggregateValues`), G9975-10002 (numeric extraction), G10024-10096 (raw-key grouping and result unwrapping), and G9798-9820 (later statistical grouping). No runtime dependency on the retired renderer is introduced.

The read-only oracle `artifacts/chart-box/b3b-plan-aggregate-oracle.mjs` extracted those exact built-in aggregate functions and datasource methods from the hash-checked bundle. It supplied only `_last`, `_addGridCommonParams`, built-in lookup and module-presence stubs, then exercised the original datasource's `.value` unwrapping. Pinned WSL Node24.22.0 exited0; `b3b-plan-aggregate-oracle.json` records 63 numerical comparisons, 28 grouped cases and 12 inherited-key failures. Undefined and signed zero have explicit report markers rather than lossy JSON numbers. These are source-method results, not browser or feature acceptance.

For `[null,3,-4,3,0,null]`, original results are sum2, avg0.5, min-4, max3, count6, firstnull and lastnull. All-null `[null,null]` returns null except count2. For absent/null endpoints `[undefined,2,null,undefined]`, count4 and numerical reducers2; first/last return undefined, represented by an absent output value key. Empty input emits no aggregate row; do not manufacture a count0 observation.

The current shared `aggregateSetupRows` differs in three observed cases: sum[-0] becomes +0 instead of original -0; min[+0,-0] becomes -0 instead of original +0; max[-0,+0] becomes +0 instead of original -0. **B3b therefore supersedes the integration draft's proposed numerical-reducer reuse.** Keep the existing reducer and all accepted families unchanged; put the small Box-specific reducer in the already reserved `application/boxPlotSetupProjection.ts`.

Freeze these operations over ordered finite numbers, null and absent values:

| Operator | Exact original operation |
| --- | --- |
| sum | Start result=null; first numeric value becomes result; subsequent numeric values use result+=value in row order. No seed0 or reassociation. |
| avg | Start sum0/count0; add each numeric value in row order; return count>0 ? sum/count : null. |
| min / max | Start result=null; replace only for a numeric value when result is null or strict result>value / result<value. Equal values retain the first signed zero. |
| count | Count every row, including null and absent value entries. No nested count wrappers in this flat scope. |
| first / last | Use the exact first/last row's value; retain null; an absent endpoint remains an absent key. |

Reject the entire projection with diagnostics if any derived number is nonfinite, including finite-input sum/avg overflow. Do not turn Infinity into null or calculate a replacement average. `Number.MAX_VALUE` repeated twice is a recorded original overflow counterexample. This is the existing finite snapshot boundary, not equivalence for original nonfinite outputs.

## Capture and metadata interface

Add only `"box-observations"` to `SnapshotPolicy` and `readonly boxPlotAggregationKey?: string` to `SnapshotRow`. For this policy every row must own a string key, including empty string. `validateSnapshot` validates and detaches it under the existing descriptor-safe JSON copy; a missing/wrong-type key produces `invalid-snapshot` at `["rows", index, "boxPlotAggregationKey"]`. Empty numeric selection is admitted, like the existing observation policies. Other snapshot policies retain their existing interpretation. The key is transient raw-category provenance, never a saved option or model field.

In `gridCapture.ts`, only the Box policy calls accepted `captureBoxCategory` before category rejection. For a real category read the unformatted public grid value once. For default category read no category cell and supply `index - start + 1` as its third argument. Save both returned category and aggregationKey. Prefix helper diagnostic paths with the displayed row path; failures remain unresolved capture results, not silent omitted rows. Preserve the existing ordinary-row, range, stable-ID and grid-model checks.

Box numeric capture accepts finite primitive numbers unchanged and null unchanged. A raw undefined is represented by omitting that descriptor's value key, preserving the existing snapshot distinction between absent and null. This is source-backed by the additional absent-endpoint oracle. Numeric strings, booleans, bigint, nonfinite numbers and value objects return unresolved at `["rows", displayedIndex, "values", columnId]`; do not coerce, invoke hooks, borrow Histogram/Pie normalizers or replace them with null. Original extraction invokes wrapper conversion hooks and can admit other shapes; those remain explicit unverified activation inputs. If a reachable supported Table/File input requires wrappers, B3d/B4 cannot close until that capture contract is resolved. B3b adds no feature flag or hidden capability restriction.

`observationSnapshotPolicy("boxPlot")` returns `"box-observations"`. Its string admission does not add Box to ApplicationChartFamily or any runtime renderer guard. `applicationSessionCapture.ts` resolves the policy once and passes that same policy through capture and retention, including empty selection. No family casts or Box branch in the session/gallery are necessary in this slice. Category/family recapture later must produce fresh raw keys; they cannot be reconstructed from normalized categories.

## Setup adapter interface and behavior

New `application/boxPlotSetupProjection.ts` exports only this typed adapter, using existing `SnapshotRow`, `SetupAggregation`, `SetupObservationGroup` and `SetupResult` types:

```ts
export function aggregateBoxSetupRows(
  rows: readonly SnapshotRow[],
  seriesIds: readonly string[],
  operator?: SetupAggregation,
): SetupResult<readonly SetupObservationGroup[]>;
```

The sole production caller is `projectOrdinarySetup` after whole-snapshot validation and selected-series admission. Do not duplicate the snapshot validator or expose new aggregation options. The adapter owns Box grouping, numerical reduction and derived finiteness checks. It returns a ready detached group list or invalid diagnostics; no partial list on failure. Use code `box-setup-aggregation` with row/key or value paths. Preserve caller input and arrays.

Without an operator return one copied row/group per input row, with sourceRowIds `[row.id]`, values restricted to selected fields, and the raw key intact. With an operator, group by **boxPlotAggregationKey**, using a Map and first-occurrence order. Keep each bucket's first normalized category and raw key; reduce each selected field exactly once over the bucket's ordered rows. Output row IDs use the existing deterministic form `setup:aggregate:${JSON.stringify(sourceRowIds)}`. Each group's sourceRowIds retain all bucket rows, including null/absent entries. Never call the shared reducer and never group aggregated output again in setup.

The original ordinary-object accumulator throws for inherited Object.prototype keys, including `__proto__`, `constructor` and `toString`; the oracle observed all12 own prototype names failing. When operator exists, fail with an explicit original-incompatible aggregate diagnostic at the offending raw-key path. Detect keys safely using `Object.hasOwn(Object.prototype,key)`; do not index a writable ordinary object with them. When operator is absent these categories stay valid. Capturing a string key remains valid independently of whether a later Aggregate request can process it.

Extend `projectOrdinarySetup`'s existing axisPolicy union to include `"box-observations"`. Use that exact policy for retention, final validation and empty-selection allowance; route its groups to this adapter. Reject `switchCategorySeries=true` before projection. Only Box bypasses `selectedColumns`' current default-category+aggFunc rejection: a saved aggFunc can remain active while original Aggregate controls are hidden. Other policy behavior and selection validation stay unchanged. No UI or model transition changes are made here.

For default category, metadata keys1/2/... keep separate per-row aggregate buckets although each statistical category is1. Thus default count over three selected rows creates three observations of1, rather than one observation of3. For ordinary categories, typed1/string1 share a raw aggregate bucket but remain statistically distinct without Aggregate. Null/undefined/empty may form separate raw buckets which later share statistical empty category; first representative controls the final category. Date/epoch can form separate raw buckets then merge statistically, and Date-string collisions retain the first epoch. These cases are in the retained grouped oracle and must be asserted through projection, not just key-helper tests.

The oracle's default sum example `[1,null,3]` yields three projected values `[1,null,3]` under statistical category1, retaining the two finite observations for B1. Its mixed missing-category sum example yields three observations `[5,5,3]` under statistical empty category. These concrete outputs disprove premature normalized-category aggregation; tests can pass these values to accepted B1 without adding a production statistics dependency.

Use existing ordinary output/provenance construction after group reduction. No-aggregate sourceMode is flat; with aggFunc it is grouped, including the default category case. Selected field order, column labels, units/scales, originalModel, selectedRange, stateAddress and dataRevision are retained. Count columns become unit `observation-count`, scale1, observationKind=count; provenance identifies original source field/unit/scale and every source row. All other operators retain source units/scales and observationKind=raw-observations. axisUnits remains deferred for Box. Final rows retain their raw key for defensive policy validation. B2 later computes summaries from these projected observations; setup itself computes no quartiles.

## Exclusive implementation and acceptance

One integration worker owns exactly these production edits relative to the Chart directory:

- Modify `application/{gridCapture.ts,histogramCapture.ts,applicationSessionCapture.ts,setupProjection.ts}` and `compatibility/{snapshotTypes.ts,snapshot.ts}`.
- Create `application/boxPlotSetupProjection.ts` and `tests/unit/chart-application/boxPlotSetup.test.ts` (test path relative to terminalpro).

No changes to accepted B3a, shared `setupAggregation.ts`, state/editor/caller routing, B2 renderer, Range files or browser harness. The worker is not alone; preserve catalog/Perspective/Range/controller edits. Controller owns inventory entries, explicit fork manifests, breadth/status, evidence and commits. Range's inactive mapper work may proceed independently; shared ownership changes return to controller before editing.

Current six-file baseline was measured with existing project-syntax-units-v1/TypeScript6.0.3 and pinned Node24.22.0, exit0, in `b3b-plan-baseline.json`: gridCapture205physical/96logical/max23; histogramCapture24/17/11; applicationSessionCapture80/29/14; setupProjection264/97/22; snapshotTypes50/38/no callable; snapshot110/122/29. No existing over-cap exception is needed. Every modified/new maintained production file must pass whole-file400physical/300logical and50 per callable. Keep the Box responsibility in its adapter; extract cohesive capture or validation helpers within owned files if needed. Further new paths require controller review; no compressed statements or implicit exceptions. Tests/docs are exempt. Reuse the existing checker/inventory foundation.

The focused test file must establish meaningful RED then GREEN for: policy admission with required raw keys and empty selection; real GridApi capture of missing/default/Date categories and unformatted number/null/absent values; default ordinal numbering from a nonzero selected-range start; all seven source aggregate results including all-null/count/first/last, signed-zero ties, order-sensitive cancellation and overflow rejection; raw-key bucket order/first representative for missing/typed/Date/default cases; source provenance/count units; no double aggregation or input mutation; prototype aggregate diagnostics and nonaggregate recovery; wrapper/throwing input rejection without hook execution; and unchanged representative ordinary/Pie/Histogram capture/setup results. Use `Object.is` for signed zero. Prefer grouped cases to a duplicated test matrix.

Planned command from the existing WSL terminalpro checkout, pinned Node on PATH:

```sh
node node_modules/vitest/vitest.mjs run --config tests/unit/chart-application/vitest.config.mjs tests/unit/chart-application/boxPlotCapture.test.ts tests/unit/chart-application/boxPlotSetup.test.ts
node node_modules/typescript/bin/tsc --project tests/unit/chart-application/session.tsconfig.json
```

The config is jsdom/maxWorkers1. The controller compares complete strict TypeScript diagnostics against accepted B3a baseline with the same installed compiler/config; require no new/changed diagnostics or suppressions, rather than claim inherited diagnostics are clean. Also run affected existing capture/setup regression files selected from actual imports once at the join. Controller runs the existing combined complexity gate with actual workspace/data_api manifests and records exact revision, command, exit and report. Independent review examines original numerical behavior, failure boundaries and shared-family regressions before acceptance. No image build is needed for this inactive slice.

## B3b acceptance

B3b inactive capture/setup is independently accepted at Workspace `7912870325e9ee12dadddf8a8fbe1a5fbf1a7ee6`. Fresh focused checks passed 88 tests; Biome passed eight files and combined complexity passed. Strict typing retains 2,713 inherited diagnostics, exit 2; raw comparison remains false with exactly two reviewed printed-order differences. Selected shared checks passed 112 tests and failed four Pie assertions reproduced at accepted B3a `bca1802`. B3c axes/navigation, B3d activation, B4 real-FMP/image/browser acceptance and B5 publication remain open. The published alpha is unchanged.

Independent approval: `artifacts/chart-box/b3b-review.md`. Commands and limitations: [verification](../../../artifacts/reviewed/chart-box/verification.md).
