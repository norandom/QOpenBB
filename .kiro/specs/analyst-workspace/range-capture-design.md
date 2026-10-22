# R4a Range capture and setup

Prepare Range Bar and Range Area to consume the accepted statistical capture and setup path without activating either family. Add a neutral `statistical-observations` policy and reuse the existing Box category and aggregate implementations. Both original families use the same upstream grouping methods; only their final statistics differ.

Independently reviewed and approved for bounded implementation, 2026-10-22. Inspection used root `29d3df94f221952a11f9f815f9aa59e111406e30` and Workspace `da5979cb020af7737f9a76544ae527d8f2a30831`. This bounded contract follows [prototype-first delivery](../../steering/delivery-workflow.md), the [Range plan](range-chart-plan.md) and accepted [Box setup contract](box-plot-setup-design.md). It leaves whole-spec approval metadata unchanged. The source-backed contract is approved; implementation and verification remain separate acceptance steps.

## Boundary Commitments

### This Slice Owns

- Admit a neutral statistical snapshot policy for the two Range model names, preserving raw category identity before setup aggregation.
- Route that policy through the existing category capture, descriptor-safe snapshot validation and statistical setup reducer.
- Establish focused capture-to-setup-to-Range-projection regressions, including the accepted Box path's continued behavior.

### Out of Boundary

Application family unions, registries, caller routing, session selection/projection, saved option reducers, editors, appearance, layout, scales, axes, navigator, miniature, lifecycle, export and activation remain outside R4a. Existing R1/R2/R3 and Box helpers remain unchanged. There is no new UI, renderer option, dependency, coercion behavior or statistics implementation. Hierarchical grid grouping, pivot, remote pages and standalone/AI callers retain their existing boundaries.

### Allowed Dependencies

Production reuses `captureBoxCategory` from `application/boxPlotCapture.ts`, `aggregateBoxSetupRows` from `application/boxPlotSetupProjection.ts`, existing snapshot/setup types and ordinary setup provenance construction. Their historical names do not introduce Box quartiles into Range: neither helper calculates a statistical summary. Tests may call accepted `projectRangeBar`; Range Area already consumes that same projection. No production capture/setup dependency on either renderer is added.

### Revalidation Triggers

Changes to raw-key capture, finite/absent observations, aggregate arithmetic/order, snapshot key admission or setup provenance require Box and both Range projections to be rechecked. A different original Range upstream grouping or aggregate path disproves reuse and stops implementation. Wider raw value admission or application activation requires a subsequent reviewed contract.

## Source Evidence and Reuse Decision

All G citations identify one-based lines in retained `artifacts/task-2.1/frontend/terminalpro/node_modules/ag-grid-enterprise/dist/ag-grid-enterprise.js`, Grid 34.1.1. SHA-256 was rechecked as `1a195685c473488defe1ce535e3115c26a42b2be94ad6ccc7fefa351eac7094f`, matching the [Range source record](../../../artifacts/chart-range/source-contract.md). These are retained dependency sources, not a runtime dependency on the retired renderer.

| Source | Observed contract | R4a consequence |
| --- | --- | --- |
| G9112-9123 | Factory sends both Range model names to `RangeChartProxy`; Box uses `BoxPlotChartProxy`. | One Range capture/setup policy covers both. |
| G9664 onward; G9723-9749 | Both proxy classes extend the same `StatisticalChartProxy`. Range creates one selected-field series, then supplies only a min/max callback. | Reuse upstream grouping; keep accepted Range extrema separate from Box summaries. |
| G9770-9820 | Shared statistics groups categories in first-encounter Map order; default category is 1, null/undefined become empty string, Dates use epoch identity. | Existing `captureBoxCategory` is source-equivalent within its accepted primitive/native-Date boundary. |
| G9846-9864; G9964-9966 | Datasource extracts rows, then aggregates before proxy statistics; default raw categories are selected-row ordinals. | Keep raw aggregation identity separately from normalized statistical category. |
| G9975-10002; G10024-10096 | Family-independent extraction and raw object-property-key aggregation precede statistical grouping. Aggregate output keeps the first raw category representative. | Reuse accepted `aggregateBoxSetupRows`, including absent/null distinctions and first representative. |
| G6298-6440; G6456-6471 | Shared built-in reducers and aggregate dispatch supply the same seven finite-observation operations. | Existing Box reducer already matches this source boundary; generic `aggregateSetupRows` has documented signed-zero differences and is not substituted. |
| G11676-11682; G11764-11767; G19689-19703 | Default category hides Aggregate controls without deleting a retained aggFunc; neither Range family has `canInvert`. | Admit saved default-category aggregates; reject category/series transpose. UI reachability remains a later join. |

The accepted Box setup contract records the exact numerical comparison and raw-key oracle, including undefined values, signed-zero ties and inherited-key failures. R4a adopts those established semantics because the original source methods are shared, not because the charts look similar. No new oracle or copied numerical reducer is needed. New maintained tests embed independent expected constants and run without ignored discovery artifacts.

## Interfaces and Data Contract

Extend the existing `SnapshotPolicy` union with exactly `"statistical-observations"`. Preserve `"box-observations"` and all its current behavior; this slice does not migrate accepted Box callers. The family selector remains its existing string-based function:

```ts
export function observationSnapshotPolicy(
  family: string,
): SnapshotPolicy | undefined;
```

It returns `"statistical-observations"` for `"rangeBar"` and `"rangeArea"`, `"box-observations"` for `"boxPlot"`, and its existing results otherwise. This selector change does not add Range to `ApplicationChartFamily` or make it reachable. Contract tests call this existing lower-level selector with those strings, then pass its returned policy directly to capture/setup; no family cast or session activation is permitted. `applicationSessionCapture.ts` already resolves the selector once and passes the policy unchanged to capture and retention; it needs no production edit.

Keep `SnapshotRow.boxPlotAggregationKey?: string` as the one transient raw-key field. Update its comment to describe shared statistical provenance while retaining its historical spelling. Introducing a second Range key or renaming the existing field would add migration and duplicate-state risk without changing the contract. Both statistical policies require every row to own a string key, including empty string; descriptor-safe validation detaches the key and rejects missing/wrong-type/accessor metadata at the existing row/key path. Both admit empty numeric selection. Never save this field in ChartModel, Widget preferences or options.

For either statistical policy, `gridCapture.ts` uses the accepted `captureBoxCategory(raw, defaultCategory, defaultRowNumber)` unchanged. For default category it reads no category cell and supplies `index - start + 1`; statistical category is 1 while raw keys are `"1"`, `"2"`, etc. For real categories it reads the unformatted public cell once. Null and undefined both normalize statistically to empty string but retain different raw keys; numbers and strings keep distinct statistical identities; native finite Dates use epoch plus their intrinsic Date-string aggregate key. Preserve existing unsupported Date/object and coercion-hook boundaries and path-prefix diagnostics.

Numeric capture retains finite primitive numbers, null, and absent keys for raw undefined. Other inputs remain unresolved; do not borrow Histogram/Pie normalization, invoke provider hooks, turn absent into null, or silently omit invalid rows. Nonfinite aggregate output fails atomically. Original extraction also handles wrappers and custom conversion hooks; those remain unresolved future activation inputs, exactly as disclosed by the accepted Box boundary. R4a makes no equivalence claim outside the finite primitive/null/absent domain.

Extend `projectOrdinarySetup`'s existing third-argument union with the neutral policy. Apply the same statistical branch to both policies: retain/validate raw keys, admit zero selected fields, permit a retained aggFunc with default category, reject `switchCategorySeries`, and call `aggregateBoxSetupRows` once. Keep the existing helper diagnostic codes and paths, including historical Box names, rather than create a parallel error adapter.

Without an operator preserve ordered observations. With an operator reduce once by raw key in first-encounter order, retain the first normalized category, source row IDs and selected field order, then let accepted `projectRangeBar` group statistical categories and calculate extrema. Keep count units (`observation-count`, scale 1), `observationKind`, raw units/scales, valueOrigins, originalModel, selectedRange, address and revision behavior unchanged. Both statistical policies retain deferred axis-unit resolution; this inactive slice does not establish final axis compatibility. Prototype keys remain admitted without aggregation and fail with the existing explicit original-incompatible diagnostic when aggregation is requested.

## File Structure Plan and Exclusive Ownership

One bounded implementer owns only these edits, relative to `vendor/workspace/terminalpro/`:

| Path | Responsibility |
| --- | --- |
| `src/components/General/Table/Chart/compatibility/snapshotTypes.ts` | Add neutral policy; clarify existing transient key comment. |
| `src/components/General/Table/Chart/compatibility/snapshot.ts` | Apply existing key/empty-selection validation to either statistical policy. |
| `src/components/General/Table/Chart/application/gridCapture.ts` | Select accepted raw category and absent-value behavior for either policy. |
| `src/components/General/Table/Chart/application/histogramCapture.ts` | Map both Range names to the neutral policy; preserve other mappings. |
| `src/components/General/Table/Chart/application/setupProjection.ts` | Admit neutral setup policy and reuse the existing statistical branch. |
| New `tests/unit/chart-application/rangeSetup.test.ts` | Exercise neutral policy through real-grid capture, setup and accepted Range projection. |

No new production helper, general policy framework or Box refactor is required. The worker is not alone; preserve all other edits. Any additional writable path returns to the controller before editing. `applicationSessionCapture.ts`, the two accepted Box helpers, `setupAggregation.ts`, all renderer/application-activation files and existing tests are read-only dependencies. The controller owns inventory/current fork manifests, breadth/status/evidence, shared integration and selective commits. Concurrent appearance discovery may read these contracts but cannot edit the same files.

## Verification and Acceptance

Require meaningful RED for the missing neutral policy behavior and GREEN after implementation. Group the following into focused cases rather than repeat the accepted Box aggregate suite:

- Both Range names resolve the neutral policy; Box and representative ordinary/Pie/Histogram mappings remain unchanged. Snapshot admission requires an own raw key, preserves empty selection and rejects getter metadata without invoking it.
- Real GridApi capture from a nonzero selected-range start produces default statistical category 1 and ordinal raw keys 1/2/3. Default category reads no category cell. Finite/null/absent values remain distinct; raw wrapper rejection invokes no conversion hook.
- Independent capture/setup/Range projection expectations distinguish the two grouping stages: raw categories numeric 1/string `"1"` with values 2/7 stay separate without Aggregate and produce one sum observation 9 with Aggregate; null/string `"null"` and undefined/string `"undefined"` preserve first-representative buckets before statistical grouping. Include Date/epoch and same-Date-string/different-epoch cases under a fixed process timezone.
- Default-category retained count over three rows produces three observations of 1, hence Range endpoints [1,1], rather than one endpoint 3. Default sum over [1,null,3] preserves finite extrema [1,3]. Two independent selected fields retain their own endpoints and selected ordering; no low/high pairing or quartile dependency appears.
- Through the neutral branch, [null,3,-4,3,0,null] gives independent reducer expectations sum 2, avg 0.5, min -4, max 3, count 6, first/last null. Retain one discriminating signed-zero tie with `Object.is`, absent first/last keys, one finite-input overflow failure and prototype-key aggregate failure followed by nonaggregate recovery. Existing Box tests retain their wider numerical matrix.
- Assert input immutability, source-row provenance/count units, sourceMode, retained model/range/address/revision and zero-field recovery. Accepted Box setup/capture tests plus representative existing capture/setup tests must still pass; do not alter expected Box behavior to make the join pass.

Planned focused command, from the installed WSL `vendor/workspace/terminalpro` checkout with the pinned Node toolchain:

```sh
node node_modules/vitest/vitest.mjs run --config tests/unit/chart-application/vitest.config.mjs tests/unit/chart-application/rangeSetup.test.ts tests/unit/chart-application/boxPlotCapture.test.ts tests/unit/chart-application/boxPlotSetup.test.ts tests/unit/chart-application/gridCapture.test.ts tests/unit/chart-application/setupProjection.test.ts
node node_modules/typescript/bin/tsc --project tests/unit/chart-application/session.tsconfig.json
```

The existing Vitest config uses one worker. Run scoped Biome on the six owned paths. The controller captures the same strict TypeScript command/config/compiler on the untouched accepted baseline and candidate; require no new/changed diagnostics or owned errors and retain inherited failures honestly. Do not add suppressions. The final fresh check selection follows actual import impact; a wider suite is warranted only for an identified shared regression.

The checker/inventory foundation already exists. Every modified maintained production file must pass whole-file 400 physical lines, 300 logical syntax units and 50 units per function under the existing combined complexity checker, with explicit current Workspace and data_api change manifests supplied by the controller. Tests/docs are excluded. No new production inventory path is expected; reconcile existing ownership entries if necessary. Do not compress statements, introduce forwarding wrappers or grant an implicit size exception. No image build/browser/provider check belongs to this inactive slice. Record revision, exact command, exit and artifacts; independent review and fresh checks precede acceptance.

R4a is disproved by changed Box outputs, normalized-category preaggregation, lost absent/default/Date identity, double aggregation, measure pairing, mutation, invented observations, hook execution, silent unsupported inputs or application activation. Any finding reopens this contract before acceptance. Appearance, full axis eligibility, real-FMP application/visual samples, controls/save/reopen/export and publication remain open in the Range plan; this draft closes none of them.
