# Histogram numerical and application design

Implement Histogram as a count of the first selected numeric field after the existing category aggregation. Keep one application session and the current editor/persistence owner. Independent H0 review accepted the H1 binning boundary; H2/H3 retain their later mapper/join review gates; [the milestone](histogram-milestone.md) owns acceptance and tasks.

## Boundary and evidence

The slice owns ordinary Table/File histogram binning, ECharts interval geometry and its existing controls. It depends on the accepted snapshot, option layering, category aggregation, session stamps, host lifecycle and export contracts. It adds no library, renderer framework, alternative state owner or feature flag. Standalone/AI callers and other distribution families remain out of scope.

Original reference is Workspace `38dffc`, `terminalpro/src/components/General/Table/Chart/`. Retained AG Charts and Grid bundles under `artifacts/task-2.1/frontend/terminalpro/node_modules/` establish the numerical contracts below. Local preparation notes are `artifacts/chart-histogram/research.md`; that ignored file is supporting research, not durable acceptance evidence. The prior accepted source is Workspace `17a35f3468452c5ae92cbf9f57de4d7bd92cde12`.

Source facts verified on 2026-10-20:

| Contract | Retained source |
| --- | --- |
| Histogram proxy supplies first X field, no Y key, Frequency and `areaPlot=false` | Grid bundle 8291-8315 |
| Default target 10; tick multipliers 1, 2, 5, 10 | Charts bundle 20329-20425, 44858-44883 |
| Explicit-count formula, adaptive rounding and final membership fallback | Charts bundle 44885-44980 |
| Empty groups are not synthesized; calculated endpoints determine X domain | Charts bundle 16368-16435, 45000-45008 |
| Count schema accepts zero and fractions: `positiveNumber=numberMin(0)` | Charts bundle 862-863, 32883 |
| Category preaggregation and hidden inversion | Grid bundle 9965-9966, 10024-10089, 11764-11767 |
| Histogram navigator range intersects intervals; visible-item count is infinite | Charts bundle 45010-45028, 23410-23411 |
| Bin-count slider and numeric axis positions | Grid bundle 11390-11406, 12580-12605, 14131-14138 |

Use local `kiro-impl` and `kiro-spec-design` boundary/review guidance, subject to prototype-first delivery. Documentation follows COBESY's conclusion-first, falsifiable claims. Core steering `product.md`, `tech.md` and `structure.md` were absent at draft time; no policy is inferred from them. Available complexity, testing, delegation, documentation, CI and delivery steering govern this slice.

## Frozen H1 interface

Create `compatibility/histogramTypes.ts` and `compatibility/histogramBins.ts` beneath the Chart directory:

```ts
export type HistogramInterval = readonly [number, number];
export interface HistogramBinInput {
  readonly values: readonly (number | null)[];
  readonly binCount?: number;
  readonly bins?: readonly HistogramInterval[];
}
export interface HistogramGroup {
  readonly intervalIndex: number;
  readonly frequency: number;
  readonly observationIndices: readonly number[];
}
export type HistogramBinResult =
  | {
      readonly status: "resolved";
      readonly bins: readonly HistogramInterval[];
      readonly groups: readonly HistogramGroup[];
      readonly skippedIndices: readonly number[];
      readonly repair: "none" | "equal-integer-count";
    }
  | {
      readonly status: "invalid";
      readonly diagnostics: readonly SnapshotDiagnostic[];
    };
export function calculateHistogramBins(input: unknown): HistogramBinResult;
```

Import `SnapshotDiagnostic` from the existing snapshot types. The function accepts only dense arrays of finite numbers or null; null means an omitted/missing/invalid observation already normalized by the capture boundary. Wrong shapes, nonfinite numeric values, strings, sparse arrays, throwing properties and malformed option values return diagnostics with no partial result. Read defensively and never mutate input. Preserve original value-array indices in metadata, including duplicates. Numeric wrappers and dates belong to capture normalization, not this JSON-compatible interface.

Absent or undefined `binCount` means use explicit `bins` if present, otherwise defaults. A supplied count must be finite and nonnegative; zero uses one segment. Do not round a positive fractional count: the original loop produces `ceil(count)` intervals, with its final-upper extension only when the loop index equals `count-1`. Count takes precedence over a well-formed explicit bin array. Validate known supplied options even when inactive.

Explicit boundaries must be dense finite `[lower, upper]` pairs with `lower < upper`. Preserve order, gaps and overlaps, including an empty array; do not sort or fill them. Reject degenerate/reversed/nonfinite pairs rather than producing misleading geometry. For bounded resource use, reject more than 10,000 generated or supplied intervals before allocation, with a visible diagnostic; this defensive limit is a deliberate difference for extreme saved configurations, not original parity.

With no finite observations, return empty bins/groups and skipped null indices, matching the original empty-domain path. Otherwise:

- Default intervals use the original target-10 tick-step selection, including tie order, near-integer tolerance and decimal tick generation. Prepend the interval immediately before the first tick, then one interval beginning at every tick. Do not substitute ECharts automatic histograms or a different statistical bin-width rule.
- Explicit count starts from `floor(min)`, calculates width `(max-floor(min))/segments`, aligns the start downward at the width's decimal order, and rounds endpoints at the original adaptive precision. On the original integer final iteration, extend the upper endpoint to at least the maximum. Preserve the algorithm for negative and fractional observations.
- Assign each observation to the first matching interval `[lower, upper)`. At the final interval, retain the historical fallback `value <= finalUpper`, even if `value < finalLower`. Thus an observation in a gap or below all supplied bins can enter the final group. This compatibility anomaly is intentional and must have a regression test; do not label such membership conventional interval semantics.
- Return occupied groups only, ordered by interval index; each frequency equals its observation-index count. Retain all calculated bins separately for the X domain. Values above the final upper edge or otherwise unmatched join `skippedIndices`.

For equal integer observations with explicit count, the original formula produces zero width and NaN start. Repair only that condition by using the finite default equal-domain intervals `[v-1,v]` and `[v,v+1]`, retaining the requested count in saved options and returning `repair="equal-integer-count"`. The occupied group is the second interval. Tests and the delivery record must identify this exception; the bin control reports the actual calculated count. Do not silently broaden this fallback to equal fractional domains, which have a valid original count formula.

If finite inputs still yield nonfinite, collapsed or unrepresentable derived endpoints, return a diagnostic; do not clamp money values, fabricate counts or widen arbitrary domains. This includes extreme equal values for which `v+1` is not representable. Derived groups and boundaries must always remain finite, counts nonnegative integers, and each input index occur at most once in a group or skipped list.

## Mapper and application contract

H2 defines `translateHistogram(input): CartesianTranslationResult` in `echarts/histogram.ts`, using the existing supported/invalid/unsupported result union. Freeze its input in `echarts/histogramTypes.ts`:

```ts
export interface HistogramMappingInput {
  readonly snapshot: ChartSnapshot;
  readonly binning: Pick<HistogramBinInput, "binCount" | "bins">;
  readonly style: {
    readonly common: Pick<ResolvedCartesianStyle,
      "textColor" | "fontFamily" | "fontSize" | "precision">;
    readonly application: Omit<ResolvedApplicationAppearance, "axes" | "series">;
    readonly axes: {
      readonly x: ResolvedXyAxis;
      readonly y: ResolvedXyAxis;
    };
    readonly series: Pick<ResolvedApplicationSeries,
      "strokeWidth" | "strokeOpacity" | "fillOpacity" | "lineDash" | "shadow" | "labels">;
  };
  readonly context: {
    readonly viewport: { readonly width: number; readonly height: number };
    readonly display: ChartDisplayPolicy;
  };
}
```

Import these existing types rather than copying them. `ResolvedXyAxis` is reusable numeric-axis appearance plus optional bounds, not an instruction to reuse XY observation windows. H2 selects the first number-role descriptor in `snapshot.selectedColumnIds` order, maps each snapshot row to that field's finite value or null, then calls H1 exactly once. Empty numeric selection yields supported empty geometry. Snapshot indices refer to the already aggregated rows, not necessarily provider row indices.

H3 uses the same H1 calculation to derive the bin-control's calculated count; both projections consume the same stamped snapshot and effective options. Never persist calculated bins over user-supplied settings, and do not create an independent mutable bin cache. Preserve `histogram.series.*` and original common numeric-axis branches through the established layer order. A stale edit remains rejected by the existing session transaction.

Draw rectangles at their actual numeric lower/upper coordinates from Y=0 to frequency; ordinary category bars cannot represent uneven explicit widths. Keep one deterministic histogram series identity based on the selected field ID, with the original display name and palette authority. Empty intervals affect the domain without adding tooltip targets or artificial observations. Preserve clipping, labels, shadows, opacity, stroke/dash and theme behavior. Renderer tests must inspect actual geometry, not just option objects.

The histogram tooltip uses original numeric-axis range formatting followed by Frequency, bypassing Workspace's custom multi-series tooltip. Raw X values are not multiplied by descriptor scale. Retain the original abbreviation threshold beyond positive/negative 1,000,000 with two decimals, and zero-decimal numeric series labels. Frequency has no USD suffix. Units/provenance remain associated with the input field and test evidence; any improved currency labeling is a separate decision.

Numeric X/Y positions remain top/bottom and left/right. Respect persisted finite bounds and empty out-of-domain geometry, without reversed extents or invented observations. Unsupported scale modes and invalid options produce visible existing diagnostics. Both themes, title/legend/layout and every reachable histogram control require effect assertions.

## Capture, editor and lifecycle join

Before binning, retain category preaggregation using the existing setup owner. With the generated None category, row identities remain unique and aggregation controls stay hidden. With a selected category, aggregation changes X observations, while histogram still counts resulting rows. Preserve selections, including unused numeric fields, across refresh and family transitions.

The current `gridCapture.ts` rejects nonnumeric values. H3 must add an explicit histogram capture policy: finite primitive numbers survive, valid native Dates become timestamps, recognized numeric wrappers become their finite primitive value, and null/undefined/ordinary numeric strings/nonfinite values become null. Do not coerce numeric strings. Normalize before the snapshot boundary; keep ordinary/combo/XY capture behavior unchanged. Reject malformed snapshot structure as today. Preserve the existing aggregation stage and test invalid/missing values on both aggregated and unaggregated paths.

Reuse existing control components and transaction bindings. The bin slider writes `binCount`, has minimum zero and maximum at least 20, and displays explicit/calculated bin-array length using original precedence. Do not impose integer-only validation on saved counts. Labels, range tooltips and styling retain their existing toggles; category/series inversion remains hidden because the original excludes histogram. Retain inactive options across family changes.

Navigator and mini-chart use the full numeric bin domain, not row indices, and remain mutually exclusive through existing quick actions. Build the overview from full groups. Windowing changes visibility and interval-intersection Y autoscale; it never recalculates bins or counts from only visible rows. Preserve wheel zoom, pan and reset. Do not apply the XY minimum-four-observations guard. Empty windows, sparse groups and equal data remain finite and recoverable.

Refresh uses the current stamped source rows and preserves valid saved options. Save/reopen restores field order, category/aggregation, bin configuration, appearance and navigator mode. Export uses the current visible chart through the existing host and must preserve interval geometry. First-field removal and re-addition, including an empty selection across refresh, require browser/component regressions.

## File structure and exclusive ownership

All Chart paths are relative to `vendor/workspace/terminalpro/src/components/General/Table/Chart/`.

| Task | Owned production paths | Responsibility |
| --- | --- | --- |
| H1 | New `compatibility/histogramTypes.ts`, `compatibility/histogramBins.ts` | Pure interval calculation and assignment |
| H2 | New `echarts/histogram.ts`, `histogramTypes.ts`, `histogramAxes.ts`, `histogramSeries.ts`, `histogramLayout.ts`, `histogramTooltip.ts` | Inactive numeric projection and geometry |
| H3 | New `application/histogramAppearance.ts`, `histogramSessionProjection.ts`, `histogramEditorTransaction.ts`, `histogramCapture.ts`; new `editor/histogram/HistogramBinControls.tsx`; new `echarts/histogramNavigator.ts` | Histogram-specific effective options, session adaptation, control and range behavior |
| H3 shared join | `caller/generatedOptions.ts`, `caller/chartInputs.ts`, `caller/themeInputs.ts`, `application/effectiveAppearanceLayers.ts`, `application/gridCapture.ts`, `application/types.ts`, `application/setupProjection.ts`, `application/setupTransitions.ts`, `application/setupTypes.ts` | Ordinary caller generation, capture and setup policy |
| H3 shared join | `application/applicationSessionProjection.ts`, `application/applicationSessionDispatch.ts`, `application/applicationSessionSetup.ts`, `application/applicationSessionSelection.ts`, `application/applicationChartSessionTypes.ts`, `application/applicationSessionTypes.ts` | Existing owner routing and family transitions |
| H3 shared join | `compatibility/editorBindings/eligibility.ts`, `selectApplicationEditorState.ts`, `rehydrateApplicationEditorEvent.ts`, `mapApplicationEditorEvent.ts`, `metadata.ts`, `types.ts`; `editor/ApplicationChartEditor.tsx`, `ApplicationCustomizeEditor.tsx`, `ApplicationSeriesEditor.tsx`, `ApplicationAxisEditor.tsx`, `ChartEditorDock.tsx`, `chartTypeGalleryCatalog.ts` | Existing controls, option paths and gallery admission |
| H3 shared join | `AgChartView.tsx`, `echarts/EChartsHost.tsx`, `echarts/lifecycle.ts`, `echarts/cartesianNavigator.ts` | Existing host dispatch, interactions and export |

In table rows listing sibling filenames, each filename inherits the immediately preceding directory. This is an allowlist for the controller's H3 inspection, not a requirement to modify every file. Record the exact subset before dispatch. Additional shared files, new helper splits or contract changes require an updated reviewed handoff; do not improvise ownership overlap. No H3 worker may edit H1/H2 files without transferring ownership and re-reviewing the affected boundary.

Dependency direction is snapshot/types -> pure binning -> mapper -> session/caller/editor -> host. Reuse existing geometry-neutral formatting/layout helpers only where their types and semantics fit. Do not cast numeric X to a category axis or import application state into H1. Extract cohesive responsibilities if a shared file would exceed the caps; this design grants no exception.

## Verification and disproof conditions

From the Workspace `terminalpro` directory, use the established commands with pinned Node 24.22.0 and actual selected files:

```sh
node node_modules/vitest/vitest.mjs run --config tests/unit/chart-compatibility/vitest.config.mjs tests/unit/chart-compatibility/histogramBins.test.ts
node node_modules/vitest/vitest.mjs run --config tests/unit/chart-application/vitest.config.mjs tests/unit/chart-application/histogramProductionJoin.test.ts
node node_modules/@playwright/test/cli.js test --config tests/e2e/live-chart/playwright.config.ts tests/e2e/live-chart/histogram-fmp.spec.ts
```

These are planned invocations, not executed results. Use the repository's existing toolchain resolution if Playwright is installed outside that checkout; inspect the pinned runtime before dispatch rather than inventing a runner. Browser configuration requires `WORKSPACE_EVIDENCE_ROOT`, owned loopback `WORKSPACE_FRONTEND_ORIGIN` and `PLAYWRIGHT_BROWSERS_PATH`, one worker and no retries. Run in the isolated background with hidden helper consoles and the existing login-rate budget.

H1 tests must independently characterize default tick ties, final-boundary inclusion, fractional counts, zero count, negative floor alignment, equal-integer repair, equal fractional inputs, empty/overlapping/gapped explicit bins, precedence and resource/overflow diagnostics. Assert full boundaries and index membership, not just total counts.

H2 tests compare actual engine rectangle positions/widths/heights and visible range/Frequency tooltip output with independent expected bins, including unequal intervals, bounds, labels and styling. H3 tests cover category aggregation, first-field ordering, capture normalization, effective option precedence, controls, stale edits and empty-selection recovery.

H4 uses the actual FMP capture in `artifacts/chart-histogram/fmp/{raw.json,quarter.csv,provenance.json}`: `stable/income-statement`, `symbol=AAPL`, `period=quarter`, `limit=40`, retrieved `2026-10-20T14:06:05.149732+00:00`, raw SHA256 `390dc8cbfc8302720a203bd9782d5e3b1f7363a4f762bdfcef079dbbe4c72f6b`. Provenance records 40 USD revenue observations from 2016-09-24 through 2026-06-27, sorted ascending for CSV with no scaling. Select revenue explicitly; fiscalYear is also numeric in the CSV. Use None category with aggregation disabled to verify 40 observations before separate aggregation checks.

Check raw USD values against boundaries and dimensionless counts after the actual selected transformation. Retain fiscal dates/periods so annual and quarterly observations cannot be confused. Application acceptance remains unverified despite successful capture; loading these rows through File exercises real provider values but does not itself verify the data API route. Record that distinction. Synthetic cases supplement edge coverage.

The design is disproved if a valid original bin case changes boundaries or membership without a named exception, a saved reachable control loses its effect, refresh/reopen changes the observation set unexpectedly, or an observed screen/export value disagrees with the captured provider rows. Original mini-chart appearance and wheel/pan/reset need runtime comparison; source availability alone does not certify them. Independently review before H1 implementation and again at source and candidate-image joins.
