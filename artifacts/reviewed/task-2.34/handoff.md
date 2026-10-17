# Consume the frozen source-safe chart contracts

Task 2.34 declares pure adapter contracts and compiler checks. It activates no renderer, editor, capture, feature flag or React session. Runtime helper tests start in 2.35 and 2.36. The application Vitest configuration deliberately has no runtime test files yet; no empty-suite pass is claimed.

## Task brief and evidence

Requirements 1.1, 4.8, 4.9, 10.4, 10.5 and 10.6 require source identity, preservation of the original experience and reproducible checks. The approved application design sections "Frozen session and state contracts", "Frozen financial display boundary" and "File Structure Plan" constrain this slice. Existing legacy/snapshot/option-state types remain authoritative. No category, raw grid invocation, appearance inheritance or editor event is inferred.

The new declarations and strict compiler contracts reject a missing category, mutable capture identity/range IDs, the `column` editor token as a saved family, arbitrary option paths, missing generated-column inputs, formatted numeric tooltip observations and an assertion that all source callbacks return strings. Before declarations existed, the compiler failed with TS2307 and dependent unused expectation errors; `red.log` retains that output. The initial shell invocation had a CRLF `--noEmit` argument failure; `stage.sh` was normalized to LF before the compiler RED capture.

The final compiler checks and scoped Biome check pass. Existing compatibility Vitest discovers nine files and passes 260 tests with one worker. This verifies regression safety for accepted pure compatibility modules; it does not verify application behavior. `identity.json` records actual HEAD, original pin, dirty/untracked path manifests, original source hashes and current/staged source/config hashes. The parent owns the full complexity gate, inventory, breadth, independent review and commit.

## A1 range and session callables

All declarations live in `vendor/workspace/terminalpro/src/components/General/Table/Chart/application/types.ts`. A1 owns only `chartRange.ts`, `sessionState.ts` and their task-approved tests. Keep production files at 400 physical lines, 300 logical syntax units and 50 units per function. Do not edit these shared declarations or configurations during fan-out.

- `ResolveChartRange(ResolveChartRangeInput) -> RangeResolutionResult`: caller supplies optional `storedRange`, `ignoreCellRange`, optional `configuredColumnIds`, `definitionColumnIds` and `generatedColumnIds`. IDs and visibility/order are already resolved. Prefer eligible stored ranges with more than one column unless ignored, then configured columns matched against definitions, then generated IDs. Configured empty matches produce diagnostics and fall back. Final IDs intersect generated IDs in selected order. Retain stored bounds and original JSON without mutation. Successful results carry both range and nonfatal diagnostics; no category or AG data extraction is included.
- `ValidateSessionStamp(stamp: unknown, currentStamp: unknown) -> SessionResult<SessionStamp>`: validate addresses/counters before matching widget, stateKey, generation and current render revision. Address uses `JSON.stringify([widgetId, stateKey])`; do not change the original persistence key algorithm. Invalid inputs and stale work must not write storage.
- `AdvanceSessionStamp(stamp: unknown, change: "data" | "render" | "generation") -> SessionResult<SessionStamp>`: data advances data/render revisions, render advances render only, generation advances generation and resets revisions. Overflow invalidates the session rather than wrapping tokens. Initial generation is 1. Address changes/grid replacement/teardown require the owning session to invalidate earlier tokens; this pure contract does not establish React lifecycle behavior.
- `SelectSessionBaseline(SessionBaselineInput) -> SessionResult<OptionBaseline>`: input supplies captured/current stamps and the existing `OptionBaselineInput`. Check that its address matches the session and delegate to accepted `selectOptionBaseline`; retain populated-to-empty semantics.
- `ApplyColumnEdit(ColumnEditInput) -> SessionResult<ChartStorageOutput>`: input supplies `command`, `currentStamp`, latest `storage`, optional `currentModel`, `resolvedOptions`, `totalSeries` and `isPivotMode`. The command contains captured stamp, a column family and accepted `ColumnEditorEvent`. Validate stamps, then use accepted event mapping and integrated reducer against supplied current state. The accepted four events remain title text/enabled, legend position and stroke width.
- `ApplyRangeTransition(RangeTransitionInput) -> SessionResult<ChartStorageOutput>`: input supplies captured/current stamps, latest storage, destination `chartType` and resolved `range`. Write only `storage[stateKey][chartType].cellRange`, retaining other state. This callable is independent of options reduction; destination-model family composition belongs to the appropriate reducer call, not a fabricated ECharts patch.

`ApplyColumnEdit` refines the illustrative design's command-only callable with explicit current-state inputs. The pure adapter cannot safely derive latest storage from an implicit React closure. It retains the design's command and result shapes, imports existing reducer types, and creates no storage owner. The controller reviewed this refinement before independent review.

Canonical capture remains `CaptureDisplayedChart(GridCaptureInput) -> SessionResult<ResolvedSnapshotInput>`. It is a declaration only. The input contains real public `GridApi<Record<string, unknown>>`, stamp, resolved range/category/descriptors and original model. No second capture-result type is introduced.

## B1 formatting callable

`CreateChartDisplayPolicy(FinancialFormattingInput) -> ChartDisplayPolicy` consumes explicit chart family, optional current period, widget `decimalDigits`, global precision, resolved category `cellDataType`, optional original Index definition and injected existing helpers. B1 owns only `financialFormatting.ts` and its task-approved unit tests. Keep the same production complexity caps and shared-file boundary.

The helper inputs are `formatNumber(number, decimals?)`, `formatNumberMagnitude(number|string, decimals?)`, `getFiscalPeriodString(string|Date, getParsedPeriod, chartType?)` and `isValidDate(string|Date)` using the source dayjs validity semantics. Injection avoids importing the original helper modules' large application/store graph into a pure adapter. Production must reuse these existing helper behaviors; test fixtures must execute actual extracted source helper bytes with provenance rather than invented substitute formatting rules. Numeric passthrough stays outside the source fiscal helper's narrower declared signature.

Category, axis, crosshair, legend and series callbacks accept and may return `string | number | Date`. This is a source-faithful refinement of the design's illustrative string returns: in-range numeric ticks and non-date category/legend values can remain raw. Tooltip numbers accept only numbers and return strings. Callback functions remain separate from data-only `RuntimeOptions`.

The Index definition preserves optional function/string `valueFormatter` inputs and unknown extra column fields. The original source invokes it without a callable guard whenever the definition exists, passing `{ value, colDef }`; only truthy results replace the original category. B1 must preserve that failure/truthiness behavior, without inventing fallback behavior. This declaration does not authorize AG callback-selection inference.

Date objects take the fiscal helper's early ISO UTC branch, even for quarterly/annual periods. Recognized midnight datetime strings return date-only text before period conversion. Date-only and recognized non-midnight strings can produce calendar quarters/years; Column family names use a newline for quarters. Numbers retain integrated scale. No detached normalizedPercent transformation or inferred unit prefix/suffix is admitted.

## Reproduce checks

From PowerShell:

```powershell
wsl -d Debian -u mc -- bash /mnt/d/Source/QOpenBB/artifacts/task-2.34/check.sh
wsl -d Debian -u mc -- /mnt/d/Source/QOpenBB/pipeline/.venv/bin/python /mnt/d/Source/QOpenBB/artifacts/task-2.34/identity.py
```

The script archives Workspace HEAD into `/home/mc/qopenbb-work/task234`, overlays current chart source, compatibility/application test inputs and the referenced financial helper files, and uses pinned Node 24.22.0 with the accepted dependency tree. Exact commands executed in staged `terminalpro`:

```sh
node node_modules/typescript/bin/tsc --project tests/unit/chart-application/tsconfig.json --noEmit
node node_modules/typescript/bin/tsc --project tests/unit/chart-compatibility/tsconfig.json --noEmit
node node_modules/vitest/vitest.mjs run --config tests/unit/chart-compatibility/vitest.config.mjs
node node_modules/@biomejs/biome/bin/biome check src/components/General/Table/Chart/application/types.ts tests/unit/chart-application
```

For 2.35/2.36, also run `node node_modules/vitest/vitest.mjs run --config tests/unit/chart-application/vitest.config.mjs` after actual runtime tests exist. No installs, application builds or browser checks were performed. Missing generic `product.md`, `tech.md` and `structure.md` steering files were observed; the applicable specialized complexity/testing/CI/delegation/documentation/workspace steering was read.
