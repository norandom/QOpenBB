# Capture ordinary displayed grid values for charts

## Overview

This amendment makes the A2 capture boundary in the approved [application design](chart-application-integration-design.md) implementable for an ordinary, flat, client-side grid with a caller-resolved category. It consumes the accepted contracts from tasks 2.34-2.37. It does not reconnect the chart button or accept the original application journey.

The original runtime proves that chart observations follow unformatted GridApi values, including an explicitly synthetic value getter. Reading node.data or parsing rendered cell text would change results. The selected displayed rows and ordered series must survive capture unchanged. Original source: 38dffc33389aca0e4a87e0e88d42f7067aa220df. Candidate: 945e438a9a65c3eeef7073dbce64a03b02f0ff6f. The accompanying [grid findings](chart-grid-runtime-next.md) own exact cases, assertions and limitations.

## Boundary commitments

**Owns:** synchronous extraction of an already resolved ordinary range from a live GridApi, stable row identities, unformatted category/numeric values, immutable snapshot construction and path diagnostics. The existing snapshot validator remains the sole validator of the resulting snapshot structure.

**Out of boundary:** category/series inference, generated numeric-only categories, custom getter installation, grouping, pivot, transpose, pinned rows, server-side/remote coverage, aggregation, table controls, theme resolution, React lifetime, mapper changes and persisted state writes. These remain required product behaviors with separate contracts. This internal boundary must not become a user-visible feature gate or justify a reduced menu.

**Allowed dependencies:** the existing ag-grid-community GridApi types/public methods, accepted application types/session stamp validation, and compatibility snapshot types/validator. No enterprise registration, reference-only chart proxy, DOM scraping, original private processedOptions, new package, service or storage owner enters production.

**Revalidation triggers:** changed grid value/identity behavior, altered range precedence, new category or row models, shared snapshot types, and descriptor unit/scale rules. Activation must separately prove that the caller resolves all required inputs and handles current generations correctly.

## Contract

Keep the frozen `CaptureDisplayedChart` and `GridCaptureInput` in application/types.ts unchanged:

```ts
type CaptureDisplayedChart =
  (input: GridCaptureInput) => SessionResult<ResolvedSnapshotInput>;
```

Input already supplies api, stamp, range, categoryColumnId, columns and originalModel. No callback is inferred, persisted or executed from stored JSON. Existing public GridApi value getters are trusted grid behavior, not newly installed by capture.

### Preconditions and ownership

1. The caller applies current range precedence using the accepted A1 resolver, supplies current visible selected column IDs and descriptors, and has finished applying pending grid filter/sort/column changes. Capture consumes that resolved range unchanged; it never repeats visibility filtering. Initial visible-column intersection belongs to A1/caller, and its hidden-series case is verified at that seam.
2. There is one explicitly resolved category descriptor and one or more numeric descriptors selected in the range. Preserve their resolved selected order; do not force category-first ordering. Category values are strings or finite numbers for this boundary. Descriptors carry explicit financial unit/scale when known; capture never invents units or rescales observations.
3. The grid is a live, ready client-side flat model. Group, pivot, transpose, pinned and remote data cannot be silently flattened into this path. Caller-owned transformation metadata remains outside the frozen input and must be checked before dispatch.
4. Bounds are both absent for all displayed rows or both valid finite nonnegative integers with start <= end within the displayed count. Partial, reversed and out-of-range bounds have no accepted clipping rule and return unresolved diagnostics. This is a conservative internal contract proposal, not an observed original clipping rule. Malformed nonnumeric bounds are invalid. An empty displayed grid with no bounds produces an empty validated snapshot; acceptance of the resulting empty chart remains downstream.
5. Each included node has a nonempty stable string ID and an ordinary row. Missing or duplicate IDs reject; never substitute the category label or current displayed index. Duplicate category labels remain separate observations.
6. The caller validates its current session stamp before and after capture. The frozen input has no currentStamp, so the adapter cannot independently identify an otherwise well-formed stale generation. It validates stamp shape and returns the supplied stamp; asynchronous commit/revision arbitration belongs to the future application session owner.

### Extraction and result

Read displayed rows in GridApi displayed order over the inclusive resolved bounds. For every selected category and numeric column, read `api.getCellValue({ rowNode, colKey, useFormatter: false })`. Preserve finite zero, negative and fractional values and explicit numeric null. Do not parse formatted text, multiply normalizedPercent, coerce missing values into zero, or use raw node.data as a fallback. An undefined numeric value has no established missing-value conversion here and returns a path diagnostic; an unhandled category/value kind remains unresolved rather than silently converted.

Construct the existing snapshot using stamp.address.stateAddress, stamp.dataRevision, sourceMode flat, selected range/columns, supplied category/descriptors and ordinary row IDs/values. Deep-copy originalModel, original range provenance and metadata through the existing validation boundary; no input object is mutated. Preserve selectedRange provenance independently of the resolved selectedColumnIds, as established by A1. Call validateSnapshot and return its diagnostics when it rejects. Return ready only with the validated snapshot and original stamp.

A destroyed API, or a client-side grid whose rowData is not yet an array, returns waiting without writes; an empty rowData array is ready input, not evidence of loading. Invalid supplied shape returns invalid. A valid configuration outside the captured contract returns unresolved with the relevant path. No failure writes storage, selects a different family, changes a flag or replaces a visible chart. Unexpected API failures retain a bounded diagnostic without embedding arbitrary grid/account objects. The future application owner decides existing error/retry behavior.

## Architecture and file structure

Dependency direction is grid caller -> application/gridCapture -> accepted snapshot validator. The adapter receives domain identity and metadata from the caller; it does not determine widget addresses, infer category roles, mutate AG models or render ECharts.

| Path relative to vendor/workspace/terminalpro | Responsibility |
| --- | --- |
| src/components/General/Table/Chart/application/gridCapture.ts | New bounded extraction and result adapter |
| tests/unit/chart-application/gridCapture.test.ts | Deterministic contract cases, immutable input and error diagnostics |
| tests/unit/chart-application/gridCapture.grid.test.ts | Actual Community GridApi integration against the admitted synthetic fixture |
| tests/unit/chart-application/gridCapture.fixtures.json | Reviewed finite rows, range and expected original arrays; no accounts/runtime state |

The existing application types/configuration, reducers, mapper, host and UI are read-only. If the real GridApi integration needs an environment/configuration extension, the controller owns that small shared edit before worker dispatch; it must not silently replace locked dependencies or acceptance commands.

## Verification and complexity

| Criteria | Required evidence |
| --- | --- |
| 4.8, 4.9 | Actual GridApi values match the reviewed original flat fixture, including sorted/filtered bounds, duplicate labels, series order, hidden-series resolution, negative/fraction/zero/null, and formatter versus getter behavior |
| 4.2, 4.7 | Input state/provenance immutability and no persistence side effects; full dashboard save/reopen remains outside this task |
| 10.4, 10.5, 10.6 | Isolated bounded checks, actual test paths in breadth, independent review, truthful current source/stage identity and unresolved-case diagnostics |
| 1.1 | Original and candidate source pins and exact approved fixture hashes |

Tests must exercise actual Community GridApi behavior as well as hostile/malformed inputs; fake objects alone cannot prove grid integration. Synthetic getter injection is explicitly labelled in tests. Verify grid-not-ready/destroyed, empty rows, invalid bounds, missing/duplicate node IDs, undefined/nonfinite values, detectable non-client-side/group/pivot/pinned modes and no input mutation. Transpose and other caller transformations are explicit caller preconditions because the frozen input cannot detect them; tests must not claim the adapter does so. Do not claim unresolved original cases have equivalent product behavior merely because rejection tests pass.

Run both existing strict compiler configurations, all chart-application and chart-compatibility units, scoped Biome, exact source/stage identities and the maintained complexity checker with current fork manifests. Preserve an ordinary failing regression before implementation, with no temporary feature flag. No full application/browser/build claim follows these helper tests.

Every maintained production file must pass 400 physical lines, 300 logical units and 50 per function. The existing checker/inventory foundation is reused; the controller registers gridCapture.ts before acceptance and audits whole changed files. Test sources and deterministic evidence are explicit exclusions. No new size exception is proposed.

## Sequencing and remaining joins

After this amendment passes independent design review and human approval, generate bounded implementation tasks: freeze the finite fixture/test environment; implement the capture adapter; independently verify the actual-grid and combined suites. One worker owns the adapter and its tests; there is no benefit to concurrent writers on this small boundary. Appearance and editor contract work may continue in disjoint research paths, with one heavy check/browser at a time.

A2 completion supports later application composition but does not activate it. B2 must still resolve all required effective leaves and precedence. The editor ledger still requires coverage beyond the exercised actions. Numeric-only generated categories, multiple-category selection rules, transpose/aggregation output, formatter invocation and full save/restart all retain named integration gates. No original functionality is removed from the release obligation.

The design is disproved if the adapter's exact rows/values differ from the captured original under the stated preconditions, if current GridApi cannot provide the required unformatted values, or if the caller cannot supply trustworthy category/identity/metadata without changing original semantics. In that case amend the contract rather than relaxing expected financial values.
