# X1 numeric-field assignment contract

Add an inactive pure resolver in `vendor/workspace/terminalpro/src/components/General/Table/Chart/compatibility/xyAssignments.ts`. It resolves column identities only; geometry, display names, labels, saved-state transactions and activation belong to later tasks.

The original `ScatterChartProxy.getSeriesDefinitions` at lines 8498-8539 of retained AG Grid Enterprise 34.1.1 establishes the grouping rules. `ChartProxy.isPaired` at lines 8647-8657 establishes the default. See [source research](xy-chart-research.md).

## Interface

```ts
export type XyChartType = "scatter" | "bubble";
export interface XyValueColumn {
  readonly colId: string;
  readonly selected: boolean;
}
export interface XyAssignmentInput {
  readonly chartType: XyChartType;
  readonly valueColumns: readonly XyValueColumn[];
  readonly paired?: boolean;
}
export interface XySeriesAssignment {
  readonly xColId: string;
  readonly yColId: string;
  readonly sizeColId?: string;
}
export interface XyAssignmentDiagnostic {
  readonly code: "invalid-input";
  readonly message: string;
}
export type XyAssignmentResult =
  | {
      readonly status: "resolved";
      readonly chartType: XyChartType;
      readonly paired: boolean;
      readonly assignments: readonly XySeriesAssignment[];
      readonly diagnostics: readonly XyAssignmentDiagnostic[];
    }
  | {
      readonly status: "invalid";
      readonly diagnostics: readonly XyAssignmentDiagnostic[];
    };
export function resolveXyAssignments(input: unknown): XyAssignmentResult;
```

## Rules

Filter selected columns in supplied order. Paired scatter consumes consecutive `(X,Y)` pairs; unpaired scatter shares the first selected X with each subsequent Y. Paired bubble consumes consecutive `(X,Y,size)` triples; unpaired bubble shares the first selected X with consecutive `(Y,size)` pairs. Omit incomplete trailing groups. Empty selections, one selected column and bubble with only two selected columns resolve successfully to an empty assignment list.

An omitted or undefined `paired` means true; a supplied non-boolean value is invalid. Validate the chart type, array structure, string column identities and boolean selection values. Column identities must be unique across the supplied value columns; duplicate IDs are invalid because downstream identity mapping cannot distinguish them. Do not reject a string solely because it is empty: upstream column identity strings are not display labels.

Read inputs defensively. Malformed objects, sparse arrays, throwing getters or proxies yield an invalid result with a diagnostic and no partial assignments. Unknown extra properties are ignored without changing them. Never mutate the supplied object, its columns or their order. Returned assignment objects are new values and contain only the selected numeric identities; no inferred units, values or labels.

Incomplete groups are ordinary source behavior, not an invalid-input diagnostic. This resolver does not decide how the application presents an empty chart.

## Completion

Use the existing compatibility Vitest configuration with one worker. Cover both families and modes, omitted pairing, complete and incomplete groups, interspersed unselected columns, order changes, empty selections, invalid inputs, duplicate IDs, immutable frozen input and throwing properties. Run strict scoped TypeScript checking against the actual module and focused test.

Whole-file limits are 400 physical lines, 300 logical units and 50 per function. Update the maintained scope inventory before acceptance. Independent review must compare grouping against the retained original and inspect fresh test/cap results. Passing X1 establishes no rendered-chart or release acceptance.
