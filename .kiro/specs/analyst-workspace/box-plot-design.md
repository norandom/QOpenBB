# Box plot numerical design

Preserve the original finite-observation five-number summary in a small inactive helper. Rendering and application integration are later tasks in the [milestone](box-plot-milestone.md); they must not silently replace these numerical rules with an ECharts transform.

## Source contract

Original Workspace is `38dffc33389aca0e4a87e0e88d42f7067aa220df`. Retained Grid 34.1.1, `artifacts/task-2.1/frontend/terminalpro/node_modules/ag-grid-enterprise/dist/ag-grid-enterprise.js`, defines `BoxPlotChartProxy` at lines 9664-9710 and `StatisticalChartProxy` at 9764-9820. Bundle SHA-256: `1a195685c473488defe1ce535e3115c26a42b2be94ad6ccc7fefa351eac7094f`. The original Charts 12.1.1 series consumes five summary values rather than calculating quartiles. Local source research is retained in `artifacts/chart-box/original-contract.md`.

For each selected numeric field and category independently, the original sorts retained numeric observations ascending. Minimum and maximum are the first and last values. For each quartile probability q = 0.25, 0.5, 0.75, calculate position = (n - 1) × q, lower = floor(position), fraction = position - lower. If a next observation exists, return `values[lower] + fraction * (values[lower + 1] - values[lower])`; otherwise return `values[lower]`. Preserve expression order. A singleton has five equal statistics; no observations produce five nulls in the original proxy.

Whiskers are absolute minimum and maximum. There is no IQR fence or separate outlier series. Negative, zero and repeated finite observations retain their normal positions. Every selected field has its own summary; values from different units or measures must never be pooled.

The original raw proxy drops nonnumbers and NaN but admits infinities. QOpenBB's existing snapshot contract supplies finite numbers or null. B1 explicitly operates on that normalized domain, not arbitrary original raw values. It rejects nonfinite inputs and nonfinite derived quartiles; it does not fabricate fallback values or claim parity for original nonfinite results. The original expression can overflow even for finite extreme inputs, so derived finiteness is checked before returning a summary.

## Frozen B1 boundary

Create only `compatibility/boxSummary.ts` and `tests/unit/chart-compatibility/boxSummary.test.ts`. Paths are relative to `vendor/workspace/terminalpro/`, except the production prefix `src/components/General/Table/Chart/`.

```ts
import type { SnapshotDiagnostic } from "./snapshotTypes";

export interface BoxSummary {
  readonly min: number;
  readonly q1: number;
  readonly median: number;
  readonly q3: number;
  readonly max: number;
}
export type BoxSummaryResult =
  | { readonly status: "resolved"; readonly count: number;
      readonly summary: BoxSummary | null }
  | { readonly status: "invalid"; readonly diagnostics: readonly SnapshotDiagnostic[] };
export function calculateBoxSummary(values: unknown): BoxSummaryResult;
```

Accept a dense array containing only finite numbers or null. Validate the whole array before producing output. Null means an omitted observation already normalized by capture; exclude it from count and statistics. Empty/all-null input resolves to count 0 and summary null. Retain repeated numeric values as distinct observations. Return a fresh summary without sorting or mutating the caller's array. Invalid shapes, sparse arrays, undefined, strings, booleans, nonfinite values and thrown property reads return a diagnostic with no partial result. Use the established defensive boundary style; do not add resource caps, statistical options or a new error framework.

This helper does not group categories, aggregate, select fields, normalize currency, build options, mutate selection or persist anything. B2 owns grouping/projection after its input is reviewed. Tests must not make an unimplemented grouping contract appear accepted.

## B1 verification and completion

Use the existing one-worker compatibility Vitest configuration with the focused test file. In WSL, set the pinned Node directory on PATH, change to `vendor/workspace/terminalpro`, then run:

```sh
node node_modules/vitest/vitest.mjs run \
  --config tests/unit/chart-compatibility/vitest.config.mjs \
  tests/unit/chart-compatibility/boxSummary.test.ts
```

Capture a missing-module RED before implementation and a passing GREEN afterward. Cover hand-calculated odd/even samples, interpolation with two values, singleton, empty/all-null, repeated values, signed/zero values, missing values, unsorted input and immutability. An extreme observation must remain the whisker endpoint, not become an outlier. Verify malformed input/throwing reads fail atomically and arithmetic overflow produces an explicit invalid result. Assert original arithmetic for a decimal interpolation example rather than replacing it with a statistically equivalent expression with different floating-point behavior.

Run scoped strict TypeScript against the helper/test. The controller adds the helper to the maintained inventory and runs the existing combined checker with explicit fork changes. The whole production file must pass 400 physical lines, 300 logical units and 50 units per function. Independent source/numerical review and fresh evidence precede task completion and selective commit. No feature flags are introduced: the owner's no-flag-delta requirement takes precedence over generic skill templates.

## Later mapper and application contract

The original groups rows in category insertion order and keeps every selected numeric field independent. A default category groups all rows; missing categories become an empty label and Date categories use their epoch identity. Existing configured aggregation happens before statistics and can collapse a distribution to a singleton. B2/B3 must reconcile these facts with the current capture/setup contract without adding another category or saved-state owner.

Trace and preserve original reachable tooltips, stroke/fill opacity, dash settings, whisker stroke/width/opacity/dash/offset, cap length ratio, axes, titles, legend and saved direction. Current integration research is `artifacts/chart-box/integration-map.md`. Freeze mapper inputs and exact file ownership before implementation, including any cohesive extraction needed by caps. Source evidence alone does not establish controls or original appearance in the application.

The proposed FMP sample reuses the retained 40-quarter AAPL income-statement capture, with raw USD revenue and a separately labelled second measure. Repeated fiscal-year categories can show quarterly distributions; incomplete fiscal years must be labelled as partial. Retain source dates, units and capture hash. Do not scale data merely for convenient chart fitting; display formatting may abbreviate billions. Fixture preparation and original runtime comparison remain B4 prerequisites, not B1 acceptance.

## B0 review

Independent Astra review approved the original numerical contract and frozen B1 boundary on 2026-10-21. The reviewer checked the retained bundle hash and actual arithmetic/filter/grouping source. Later mapper/application contracts remain unfrozen. The design governs raw USD fixture planning and `compatibility/boxSummary.ts`; preliminary research suggestions do not override it. No runtime or implementation acceptance is implied.
