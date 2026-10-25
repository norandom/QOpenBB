# Heatmap data contract

The original Heatmap uses a wide table: one selected category labels rows and selected numeric fields label columns. Reuse the existing ordinary snapshot and setup projection. Do not introduce a third capture kind or hierarchy paths for this chart.

## Observed basis

Original synthetic probe `artifacts/chart-heatmap/probe/run-2` completed one case with one worker and no retries on the qualified original image `f48eb1c9b32e1f84d5199dafc943bc1fc10f3b1745ab29860975d002dc5c8a3f`, frontend `38dffc33389aca0e4a87e0e88d42f7067aa220df`. Original diagnostics, including the known onboarding error, are retained. A completed characterization is not clean candidate acceptance.

The initial selection is category Region plus Value/Reserve. Numeric field names form x-axis columns. Each source row is a distinct y-axis occurrence, including repeated West and East labels. Negative -10 and zero 0 have visible labels and native tooltips. The final East row has a missing Value but its Reserve 105 remains visible. Selecting Desk replaces Region; it does not add a second category axis.

With native Aggregate enabled, the saved operator is sum: West Value=40 and Reserve=308; East Value=0 and Reserve=207. This agrees with the existing ordinary aggregation owner. Other operator outcomes and color-domain edge behavior are not established by this probe. Existing generic aggregation semantics remain independently tested; do not relabel them observed Heatmap behavior.

## HM1: inactive matrix adapter

This bounded task freezes data translation only. Native appearance, legend, axis and session contracts remain separate review gates. HM1 must not enable the Heatmap route or claim a rendered replacement.

Exclusive Workspace production file: `terminalpro/src/components/General/Table/Chart/echarts/heatmapData.ts`.

Exclusive test file: `terminalpro/tests/unit/chart-compatibility/heatmapData.test.ts`.

The controller owns the maintained-path inventory and source-pin updates. No shared snapshot, validator, aggregation, session, editor, gallery, host or router file belongs to this task.

Export `buildHeatmapData(projection: SetupProjection): HeatmapData` and its readonly output types from the single production file:

- `HeatmapAxisItem`: `id: string`, `label: string`.
- `HeatmapCell`: `x: number`, `y: number`, `rowId: string`, `columnId: string`, `value: number`.
- `HeatmapData`: ordered `x` and `y` axis items, ordered `cells`, and `extent: readonly [number, number] | null`.

The input is an already validated ordinary `SetupProjection`; reuse its snapshot and provenance without another persistent state representation. The adapter is a pure, transient renderer input. It must not mutate or aggregate the input, rewrite saved data, or duplicate provenance. Consumers can resolve source provenance through the existing row/column IDs in `projection.valueOrigins`.

### Mapping rules

1. Build x from selected numeric descriptor IDs in selection order; labels come from descriptors. The selected category column is not a value column.
2. Build y from every projected row in row order. Use row IDs for identity and `String(row.category)` for display. Repeated labels never collapse rows.
3. Emit cells in row-major order using numeric x/y indices. Zero and negative finite values are observations and must survive unchanged.
4. Omit absent and null numeric observations only. Keep all axis items and companion observations. Never impute zero or remove an entire row because one cell is missing.
5. Extent is the minimum and maximum emitted finite value. An empty matrix has null extent; a constant matrix retains equal endpoints. This does not decide color interpolation or expand a constant domain.
6. Treat a present undefined or nonfinite numeric value as a violated validated-input precondition and throw; never silently omit malformed observations. Do not broaden snapshot admission rules here.

### Completion evidence

Write the focused test before implementation and retain a meaningful RED result. Exercise outputs from the actual `projectOrdinarySetup`, including aggregate off/on, selection reorder and duplicate labels. Cover negative/zero/null/absent, an all-missing series with valid companions, empty and constant extents, source immutability, and malformed numeric preconditions. Confirm emitted IDs still resolve to existing source provenance, including the existing Count projection. Do not test color or fabricate a second aggregation implementation.

Run the focused unit check, relevant formatting/lint/static checks, and the existing inventory-backed complexity gate with explicit changed-file scope. Caps are 400 physical lines/file, 300 logical units/file and 50/function. Independent review must verify actual RED/GREEN evidence and that the module remains unreachable from live application routing. Per-task selective commit follows acceptance.

## Later integration constraint

Ordinary capture accepts null but rejects raw undefined numeric observations. Before active wiring, inspect the public grid value for missing CSV cells and define a bounded admission change only if required. Do not weaken other families' validation. Native control observation, real-FMP application acceptance and publication remain open in the [milestone](heatmap-milestone.md).
