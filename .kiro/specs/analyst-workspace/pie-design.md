# Pie and donut assignment design

Use one small, inactive assignment resolver to preserve the original integrated chart's field ordering and ring layout metadata. Rendering, value normalization and editor integration remain separate reviewed tasks in [the milestone](pie-milestone.md).

## Original evidence

The original owned Workspace baseline is `38dffc33389aca0e4a87e0e88d42f7067aa220df`. Its constants map `doughnut` to `donut`; the original Table selection menu exposes Pie and Doughnut.

The retained `artifacts/task-2.1/frontend/terminalpro/node_modules/ag-grid-enterprise/dist/package/main.esm.mjs`, `PieChartProxy.getSeries/getFields` and `calculateOffsets` around lines 46418–46518, supplies the following contract:

- Pie selects only the first field from the already selected field list. It supplies no radius-offset or field-title override.
- Donut/doughnut retains every selected field. One field uses outer offset 0 and inner offset -40. With multiple fields, successive pairs are (0,-20), (-40,-60), (-80,-100), continuing in that order.
- Offsets are pixel adjustments to a common available radius, not percentages. P1 preserves the offsets; P2 owns conversion to actual engine radii and small-container behavior.
- Donut's field title, when its display name exists, sets `showInLegend` only when more than one field is selected. This changes title participation, not slice visibility.
- The renderer family for both donut spellings is `donut`. Keep the requested saved spelling separately.

## Frozen P1 interface

Create only `compatibility/pieAssignments.ts` and its focused test file.

```ts
export type PieChartType = "pie" | "donut" | "doughnut";
export interface PieValueColumn {
  readonly colId: string;
  readonly selected: boolean;
}
export interface PieAssignmentInput {
  readonly chartType: PieChartType;
  readonly valueColumns: readonly PieValueColumn[];
}
export interface PieRingAssignment {
  readonly outerRadiusOffset: number;
  readonly innerRadiusOffset: number;
  readonly titleInLegend: boolean;
}
export interface PieSeriesAssignment {
  readonly colId: string;
  readonly ring?: PieRingAssignment;
}
export interface PieAssignmentDiagnostic {
  readonly code: "invalid-input";
  readonly message: string;
}
export type PieAssignmentResult =
  | {
      readonly status: "resolved";
      readonly chartType: PieChartType;
      readonly seriesType: "pie" | "donut";
      readonly assignments: readonly PieSeriesAssignment[];
      readonly diagnostics: readonly PieAssignmentDiagnostic[];
    }
  | {
      readonly status: "invalid";
      readonly diagnostics: readonly PieAssignmentDiagnostic[];
    };
export function resolvePieAssignments(input: unknown): PieAssignmentResult;
```

## P1 rules and acceptance

Validate the complete ordered column list before assigning anything. Entries must have string IDs and boolean `selected`; duplicate IDs, sparse arrays, non-record entries, unsupported types and failed reads are invalid. Follow the accepted XY resolver's defensive boundary for accessors/proxies. Empty strings remain valid IDs, consistent with that existing contract; do not invent stricter ID rules here.

Filter selected entries while preserving order. Zero selected fields is resolved with an empty assignment list. Pie emits one assignment without `ring`. Donut emits all selected assignments and computes the offset sequence above. `titleInLegend` is true only for multiple selected fields; the later mapper adds a title only when a display name exists. Return fresh output and do not modify caller inputs or retain mutable input objects.

Focused tests cover each spelling, empty/all-unselected inputs, ordering and deselection, one/two/three rings, first-field pie with extra selections, immutable inputs, malformed/duplicate/sparse data and thrown reads. Compare expected offsets to the original proxy, not an ECharts default. Use the existing one-worker `tests/unit/chart-compatibility/vitest.config.mjs`; run scoped strict TypeScript and the parent-owned explicit complexity manifest. All new production code stays within 400/300/50.

## Later rendering boundary

P1 performs no aggregation, numeric-value sanitation, angle calculation, legend mutation or persisted-state change. P2 must freeze those rules against the original engine before using this helper. No library, feature flag, alternate state owner or extra UI is introduced.

The planned real-data fixture is fiscal-2025 quarterly AAPL revenue and gross profit derived from the existing FMP income-statement capture. Separate rings show separate quarterly distributions. Provenance, derived row selection and totals must be checked before application acceptance; planned fixture use is not a completed test.

## P0 review

Independent Astra review approved this inactive P1 boundary on 2026-10-20 against the retained original proxy. P1 code, P2 numerical semantics, UI integration and publication remain unaccepted. Core product/tech/structure steering files are absent; the available delivery, delegation, complexity and experience policies govern this bounded slice.
