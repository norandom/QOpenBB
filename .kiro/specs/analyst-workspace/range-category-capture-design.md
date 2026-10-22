# R4e Range capture provenance contract

Implement one capture-to-snapshot slice: retain the first selected raw category's Date identity and the selected Grid column's chart metadata, resolve the source category kind during capture, and prove that statistical setup aggregation preserves those facts. Do not change row schemas or activate Range rendering. This is sufficient input provenance for the later Range session; it does not supply numeric/calendar ticks, layout, navigation, or pointer interaction.

Source-reviewed bounded implementation contract, 2026-10-22, Workspace baseline `c348a497451df7d876ee127a0a0463f66807c95d`. This continues the approved autonomous Range integration under the prototype-first delivery policy.

## Frozen data contract

Add an optional `rangeCategory` member to `ResolvedSnapshotInput` with this JSON-only shape:

```ts
interface RangeCategoryProvenance {
  readonly categoryColumnId: string;
  readonly columnChartDataType: string | null;
  readonly firstCategoryIsDate: boolean;
  readonly kind: "category" | "number" | "time";
}
```

`categoryColumnId` binds facts to the selected captured column. `columnChartDataType` is the actual selected public Grid column's `getColDef().chartDataType`; absent/null metadata becomes null and an empty string remains an empty string. Do not substitute `SnapshotColumn.role`, financial units, `cellDataType`, guessed values, or caller formatter metadata. Reject a non-null non-string metadata value with an explicit diagnostic. For the synthetic default category there is no source column: use null metadata and false Date evidence.

`firstCategoryIsDate` records only the raw category of the first selected displayed row, before `captureBoxCategory` converts native Dates to epoch numbers. With no selected rows it is false. A later Date does not change it. Invalid/custom Date values continue to fail existing capture admission. Capture the evidence in the existing cell read; do not invoke a valueGetter again or reread the first row through a second path.

`kind` is the result for the model supplied to this capture. Keep the facts as well as the result because a later category-axis editor event changes the model override without changing the data revision. Expose the same pure resolver for the later selection boundary, accepting these facts plus an explicitly supplied current model override. The later caller must use its current model; it must not reuse a stale captured `kind` after an axis edit.

## Resolver decision order

The retained Grid source constructs metadata using `model.categoryAxisType ?? model.getChartDataType(colId)` (G7581-7592; selected column definition lookup at G17784). Its category-axis resolver uses grouping first, then truthy metadata, then first-row Date inference (G8148-8174). Range chooses axes from pre-normalization data (G9765).

For the admitted flat capture in this slice:

1. Compute `effective = currentModel.categoryAxisType ?? columnChartDataType`. Model null/undefined falls back to column metadata. An empty string suppresses the column fallback, as the source nullish operator does.
2. If `effective` is truthy, return `time` for exactly `"time"`, `number` for exactly `"number"`, and `category` for other admitted strings. Explicit `"category"` suppresses Date inference.
3. Otherwise return `time` only if `firstCategoryIsDate` is true; return `category` otherwise. Raw numeric categories do not imply a number axis. Date-looking strings do not imply a time axis.
4. Reject a present non-null non-string model override with an explicit diagnostic. This is bounded input admission rather than an implicit coercion of malformed state.

Grouped/pivot/tree/pinned/remote Grid inputs retain the current capture rejection. Do not produce `grouped-category` in this flat-capture contract. Statistical aggregation later sets snapshot `sourceMode` to `grouped`; that derived marker must not be mistaken for a grouped Grid row model and must not rerun inference from aggregated rows.

## Integration and validation

Only `snapshotPolicy === "statistical-observations"` produces the new field. `observationSnapshotPolicy` already selects that policy for Range Bar/Area. Existing Box capture remains `box-observations` and must retain its observable behavior. Ordinary, histogram, pie and XY captures remain unchanged.

`captureDisplayedChart` must call the resolver as part of its real ready-result path and attach the field before final `validateSnapshot`. A standalone unconsumed helper does not complete this slice. Read actual column metadata once, match the selected column by ID, and report an unresolved diagnostic if a nonsynthetic selected column cannot be found. Existing broad Grid throw containment remains the outer error boundary.

`validateSnapshot` already descriptor-copies the complete JSON object and therefore preserves extra fields. Add semantic validation for the optional field after this safe copy: own required fields, exact primitive types, associated category ID, admitted kind and agreement between `kind`, the stored facts and `originalModel.categoryAxisType`. Do not read arbitrary incoming getters in a new pre-copy helper. Old snapshots without the optional field remain valid. Malformed presence must fail; absence must not silently authorize future Range activation, whose session will require capture provenance.

`projectOrdinarySetup` already spreads `...source` into the validated derived snapshot, and statistical setup rejects category/series transpose. Preserve that mechanism. No `SnapshotRow`, `boxPlotAggregationKey`, aggregation algorithm, Range projection schema or row-by-row provenance extension is needed. Test the existing path to establish retention; do not add redundant aggregation wiring.

Keep raw facts frozen across setup count/first/last/sum/etc. They describe the capture that selected the axis, not the representative row selected by an aggregate. Changing the category ID still requires the existing recapture transition.

## Ownership and execution

One implementer owns this coupled slice sequentially. Allowed production files are `application/gridCapture.ts`, `compatibility/snapshotTypes.ts`, `compatibility/snapshot.ts`, and one cohesive new provenance module under `compatibility/` if extraction is needed. The new module may own the shared type, source resolver and semantic validation while keeping application capture responsible for public Grid reads. Avoid a compatibility-to-application import. The controller owns inventory, breadth, maintained documentation and selective commits. Preserve all unrelated working-tree changes.

Tests belong in focused new chart-application provenance tests and chart-compatibility snapshot tests, with a focused setup-retention regression. Existing fixture helpers may be extended only where necessary to expose actual column IDs/definitions for the Range policy. Do not change live family gates, `ApplicationChartFamily`, chart session dispatch, caller editor routing, renderer hosts, feature flags, Range cores or release configuration.

Every modified maintained production file must pass 400 physical lines, 300 logical syntax units and 50 logical units per callable. Use the existing scoped checker and explicit Workspace revision manifest, register the cohesive new module in the inventory, and retain evidence. This artifact itself is documentation and outside those production caps. One heavy verification process at a time; no image build or publication is warranted by this bounded capture slice.

## Focused acceptance cases

- Native first Date with no metadata becomes time while its normalized row category is an epoch number; a finite numeric first category remains category. Date-looking strings and later-only Dates remain category.
- Column `time` and `number` metadata select their kinds; explicit column `category` suppresses Date inference. Model time/number/category overrides column metadata; null falls back; empty-string model suppresses fallback and allows only first-Date inference.
- First-row evidence follows the inclusive selected displayed bounds after filtering/sorting, not original row order. A valueGetter is invoked once per captured category cell. Empty and synthetic-default captures produce false Date evidence.
- Non-string metadata/override, missing selected actual column, stale category association, wrong Date-flag type, missing required provenance fields and inconsistent stored kind fail explicitly. Getter-bearing/cyclic/malformed JSON still fails before semantic reads.
- Validated snapshots detach provenance from input mutation. Legacy snapshots without provenance and existing Box capture remain accepted as before.
- Capture through `projectOrdinarySetup(..., "statistical-observations")` retains the facts and resolved kind for raw and representative/count aggregations, including Date versus epoch inputs that normalize identically. Aggregation output must not supply new inference evidence.
- A pure resolver call using the retained facts and a newer model axis override produces the newer kind without changing stored capture facts. This establishes the future editor seam without claiming it is wired into an active Range session.

Run the focused provenance/snapshot/setup/Box regressions, the established chart-application strict typing check and scoped formatting/complexity checks. Keep a parent baseline comparison for any pre-existing typing failure. No passing result from these checks establishes full Range application acceptance.

The proposal is disproved if capture cannot retain the source's first raw category evidence through current validation and setup without row-schema changes, if the actual selected column metadata differs from the assumed public Grid seam, or if a source-supported model value is rejected without a recorded bounded admission decision. Resolve such a failure in this contract before expanding implementation scope.

## Task acceptance

- [x] R4e: implement and independently review capture provenance, retained setup metadata, focused regressions, type/size gates and reconciled evidence.
