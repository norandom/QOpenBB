# H1b inactive hierarchy validation and capture plan

Implement an independently callable hierarchy validator and displayed-row capture, sharing the ordinary grid safety checks. Keep the live session unchanged. This bounded task passed independent design review before implementation, based on Workspace `9d007b2f40b65ec5f1e2e760787a9fc2d9e4e3d5` and the frozen [H1a contract](hierarchy-contract.md). H1a declarations are accepted at Workspace 2e900d9965902a88adba3338732de2efb054248d; use their exact exports from compatibility/hierarchyContracts.ts and application/hierarchyTypes.ts. No implementation, tests, compilation or build ran while writing this plan.

## Scope and ownership

One implementer owns these Chart-relative production paths exclusively:

- New `compatibility/hierarchySnapshot.ts`: hierarchy envelope/selection/row validation and detached readonly return.
- New `compatibility/snapshotJson.ts`: the existing neutral safe JSON-copy primitive extracted from snapshot.ts, with no behavior change.
- Modified `compatibility/snapshot.ts`: import neutral copy helper only; retain ValidateSnapshot/ChartSnapshot/SnapshotPolicy and all ordinary validation rules.
- New `application/gridCaptureGuards.ts`: shared public API admission, model restrictions, inclusive bounds and displayed-node guards.
- Modified `application/gridCapture.ts`: replace extracted checks with helpers while preserving its public signature, status/diagnostic paths, normalizers, statistical range provenance and flat output.
- New `application/hierarchyCapture.ts`: captureDisplayedHierarchy plus hierarchy category/numeric reading; no application import or routing to it.

`application/histogramCapture.ts` needs **no edit**: it owns family-to-flat-policy routing and a histogram normalizer, neither of which hierarchy uses. Do not add a hierarchy-observations policy. All other production files are read-only, including H1a declarations, applicationSessionCapture, runtime/state/context/commit/result owners, setup, renderer and controls. If neutral helper extraction requires another production file, stop and obtain a reviewed scope revision rather than growing an implicit helper set.

Test ownership: new `tests/unit/chart-compatibility/hierarchySnapshot.test.ts`; new `tests/unit/chart-application/hierarchyCapture.test.ts`; existing gridCapture.test.ts only if a missing flat guard assertion must be added. Reuse the local vi.fn GridApi pattern from gridCapture.test.ts and real-grid regression in gridCapture.grid.test.ts; no copied browser harness or provider fixture. Tests are outside production caps but remain behavior-focused.

The controller owns maintained inventory/breadth registration and explicit fork-change scope before acceptance. The implementer is not alone: preserve other lanes' changes; no commits or reverts outside these paths.

## Exported APIs

No new dependency or public declaration owner is needed.

```ts
// compatibility/hierarchySnapshot.ts
export function validateHierarchySnapshot(
  input: unknown,
): HierarchySnapshotValidationResult;

// application/hierarchyCapture.ts
export function captureDisplayedHierarchy(
  input: HierarchyGridCaptureInput,
): SessionResult<HierarchySnapshot>;

// compatibility/snapshotJson.ts
export function copySnapshotJson(
  value: unknown,
  path?: DiagnosticPath,
): SnapshotJson;
// Helper throws only a registered validation error; inspect that error through:
export function snapshotJsonDiagnostic(
  error: unknown,
): SnapshotDiagnostic | undefined;
```

The JSON helper retains the current own-enumerable-data-property copy, plain/null prototype admission, finite JSON numbers, dense arrays, symbol/getter/cycle rejection and diagnostic paths. It must not invoke getters, toJSON or arbitrary coercion. Its error registry remains module-private; snapshot.ts keeps its own non-JSON validation failures and maps helper failures through snapshotJsonDiagnostic. Hierarchy uses the same helper rather than copying vulnerable JSON traversal. Preserve ordinary invalid-snapshot diagnostics. New hierarchy semantic diagnostics use `invalid-hierarchy-snapshot` and precise source-root paths.

Proposed neutral grid exports use existing GridApi/IRowNode and SessionResult types:

```ts
type CaptureGridApi = GridCaptureInput["api"];
type CaptureRow = IRowNode<Record<string, unknown>>;
export function inspectCaptureApi(api: unknown): CaptureGuardResult<CaptureGridApi>;
export function checkCaptureGridModel(
  api: CaptureGridApi,
  statisticalCategoryId?: string,
): CaptureGuardResult<{ readonly columnChartDataType: string | null }>;
export function captureRangeBounds(
  range: ResolvedRange,
  displayedCount: number,
): CaptureGuardResult<readonly [number, number]>;
export function validateDisplayedCaptureRow(
  node: CaptureRow | undefined,
  index: number,
  seenIds: Set<string>,
): CaptureGuardResult<CaptureRow>;
```

Neutral guards use this local result shape, avoiding fabricated session stamps:

```ts
export type CaptureGuardResult<T> =
  | { readonly status: "ready"; readonly value: T }
  | { readonly status: "invalid" | "unresolved";
      readonly diagnostics: readonly SnapshotDiagnostic[] };
```

SessionResult remains exclusively the public capture API result. Their caller returns unsuccessful guard results unchanged. Ordinary guard diagnostics keep code grid-capture and existing paths/messages; sanitizing external GridApi throws stays at each public capture boundary. `checkCaptureGridModel` returns null chart metadata when no statisticalCategoryId is supplied; statistical category presence/type validation remains source-compatible. Export CaptureGridApi/CaptureRow only if required by signatures, otherwise keep aliases local.

## Hierarchy validation contract

Copy first, then validate the detached JSON tree. Require kind hierarchy, sourceMode flat, nonempty stateAddress, finite dataRevision, own originalModel/selectedRange JSON, descriptor uniqueness/role/label/unit/positive-scale validity, unique selectedColumnIds referencing known descriptors, and categoryColumnIds matching **all selected category descriptors in selected-column order**. No fake default category descriptor or categoryColumnId/rangeCategory field is allowed. Unselected numeric descriptors may remain to support retained captures; unselected category descriptors are rejected so the captured category order stays unambiguous. Zero categories and zero numeric selections are valid.

Rows require unique nonempty stable IDs; dense rawCategoryValues/categoryPath vectors with lengths equal to categoryColumnIds; raw string/finite number/boolean/null; canonical path exactly `raw == null ? null : String(raw)`, retaining empty string separately. Raw undefined is invalid in a validated snapshot because it is not JSON; capture normalizes undefined category cells to null before validation. Numeric values have only declared numeric descriptor keys, with finite numbers/null; absent keys remain missing, own undefined is invalid. Preserve signed numeric observations without clamping or aggregation. Preserve selected order, provenance JSON and raw rows; do not construct tree nodes, group duplicate paths, infer size/color, calculate weights, or format labels here. A no-category row keeps raw/path [] and its stable ID; duplicate empty paths are valid and remain separate rows.

The validator returns a detached deeply frozen HierarchySnapshot on success. It diagnoses hostile input rather than throwing. Do not mutate/freeze caller-owned inputs. Preserve raw numeric 1 versus string 1 while requiring both canonical components "1". Boolean scalar admission is source-backed, not claimed mixed-scalar File browser coverage.

## Capture sequence and unchanged guards

Validate input/stamp/range/descriptors before reading cells, matching ordinary boundary ordering where practical. Build and validate an empty hierarchy template; use hierarchy-specific selected category IDs and descriptor roles, never scalar categoryColumnId. Require the same public API methods currently required in gridCapture. Return waiting when destroyed or rowData is not an array. Check client-side row model only, pivot/tree disabled, configured/API pinned rows absent and every grid column's active/declarative grouping/pivot flags and indexes absent. Preserve statistical metadata behavior for the ordinary caller. Guard all grid reads with the existing sanitized external-failure boundary.

Check displayed count is a safe nonnegative integer and resolve inclusive bounds, including both null endpoints meaning full range. Empty full range is [0,-1]. Visit `getDisplayedRowAtIndex` in the displayed filtered/sorted order; reject missing nodes, groups, footers, pinned nodes and duplicate/empty row IDs. Do not read rowData for cell values or include filtered-out rows. Read every category via getCellValue with useFormatter false in categoryColumnIds order. Admit only raw safe scalars, normalize undefined/null to raw null, preserve typed finite/boolean/string cells and derive canonical string/null components. Reject objects and nonfinite category values without coercion.

Read selected numeric descriptors via getCellValue with useFormatter false. Finite numbers and null remain unchanged; undefined remains an absent values key so missingness is retained. Reject nonfinite/nonnumber numeric values with an unresolved source-row/column diagnostic; do not reuse histogram/box/polar coercion. No geometry exists in H1b: negative, zero and missing source size remain raw, and no-size remains zero selected numeric fields. Freeze/validate final capture and return input stamp. Catch unregistered external throws as sanitized grid-api-failure with no arbitrary thrown message/property access.

## Bounded RED/GREEN evidence

Before implementation, retain expected RED failure for new exports/behavior, then implement and retain focused GREEN output. Two new suites with table-driven cases are sufficient:

1. Validator suite: one valid multilevel fixture with raw null/empty/boolean/number/string and deliberately equal canonical 1 labels; zero-category/zero-numeric rows; invalid metadata/order/vector length/canonical mismatch/duplicate IDs/value descriptor; hostile getter/cycle/nonfinite cases proving no hooks invoked; detached freeze/provenance preservation. This is semantic boundary evidence, not snapshots of implementation details.
2. Capture suite: selected categories Region,Desk and reversed order with two numeric fields, null/undefined category normalization and absent numeric preservation; displayed subset/order and explicit inclusive/full-null bounds; duplicate/missing row ID rejection; table-driven guard matrix for remote row model, pivotMode, treeData, both pinned mechanisms, active/declarative/index grouping and pivot across unselected columns, group/footer/pinned displayed node, destroyed/waiting and thrown-grid sanitization. Confirm full row/path/raw output and input stamp, not merely ready status.

Run existing gridCapture.test.ts and gridCapture.grid.test.ts after extraction, plus rangeCategoryCapture.test.ts, radarCapture.test.ts and boxPlotCapture.test.ts to disprove statistical/polar coercion drift. Existing pie/histogram snapshot normalization tests selected by changed dependency coverage remain a controller check; no need to blanket-run unrelated session/renderer suites because live routing is untouched. A failure justifies follow-up scope, not assertion deletion.

## Static and size verification plan

Capture baseline diagnostics before changes, then compare post-change diagnostics using the same existing installed toolchain. From terminalpro, the scoped strict commands are:

```sh
node ../../../verification/node_modules/typescript/bin/tsc --project tests/unit/chart-compatibility/tsconfig.json --pretty false
node ../../../verification/node_modules/typescript/bin/tsc --project tests/unit/chart-application/tsconfig.json --pretty false
node node_modules/vitest/vitest.mjs run --config tests/unit/chart-compatibility/vitest.config.mjs tests/unit/chart-compatibility/hierarchySnapshot.test.ts tests/unit/chart-compatibility/snapshot.test.ts --maxWorkers=1
node node_modules/vitest/vitest.mjs run --config tests/unit/chart-application/vitest.config.mjs tests/unit/chart-application/hierarchyCapture.test.ts tests/unit/chart-application/gridCapture.test.ts tests/unit/chart-application/gridCapture.grid.test.ts tests/unit/chart-application/rangeCategoryCapture.test.ts tests/unit/chart-application/radarCapture.test.ts tests/unit/chart-application/boxPlotCapture.test.ts --maxWorkers=1
```

These are planned commands, not execution evidence. Use the existing locked WSL/Node toolchain and owner heavy-check queue; do not install dependencies or substitute a temporary compiler. The scoped configs include imported session/UI dependencies and may inherit diagnostics: retain exact baseline and identify any additions; do not report a clean compile if inherited errors remain. If the installed tool layout differs, controller resolves it using existing verification instructions before dispatch, without editing package scripts/configs in this task.

Run the maintained combined complexity gate described in docs/complexity.md with controller-supplied explicit current Workspace/data-api changed manifests and inventory. Every new/modified production file must pass **400 physical lines/file, 300 logical units/file, 50/function** as a whole. Initial targets: hierarchySnapshot <=250 physical, snapshotJson <=110, hierarchyCapture <=250, gridCaptureGuards <=220, gridCapture lower than its 368-line baseline, snapshot no larger than its 231-line baseline. Targets are planning margins, not exceptions. Split validator into category/selection/row functions and capture into input/read-category/read-values/read-rows boundaries; each callable remains <=50 logical units. Neutral extraction must reduce duplicated responsibilities rather than create forwarding stubs.

Independent reviewer first approves this exact task/API/manifest before implementation. After implementation a fresh reviewer inspects source, RED/GREEN logs, baseline/static deltas, guard preservation and size evidence, then controller obtains fresh verification before acceptance. H1b cannot claim gallery/live support, financial hierarchy preparation, controls, export or H4 browser acceptance.

H3 later activates RetainedApplicationCapture atomically across applicationSessionCapture return/state/context/results, own-kind/family mismatch guards and every flat selector narrowing. Existing forced casts in applicationSessionCapture and runtime must be removed/narrowed at that join. No H1b call site uses the inactive union or converts hierarchy into a fake ordinary snapshot.


## Review clarification: hostile reflection failures

The extracted safe JSON copier must preserve the existing generic root invalid-snapshot fallback for arbitrary failures from Proxy/reflection traps. Never inspect properties of an unregistered thrown value. Recognized internal copy errors may retain their established diagnostics; all other thrown values produce the generic root diagnostic. Include one focused regression where a reflection trap throws an object whose properties themselves throw, proving the fallback remains safe and sanitized.
