# C2 combination-chart mapper contract

C2 adds an inactive, pure ECharts mapper for the assignments resolved by C1. It does not admit combination charts in the gallery, change application session routing, write saved state, or establish feature acceptance. C3 resolves editor and saved appearance state into this contract; C4 joins the mapper to the application and navigator. The owning acceptance criteria remain in [the chart milestone](chart-port-milestone.md).

This contract is based on the retained original AG Grid Enterprise 34.1.1 bundle at `artifacts/task-2.1/frontend/terminalpro/node_modules/ag-grid-enterprise/dist/ag-grid-enterprise.js`: `ComboChartModel` at 18073-18165 and `ComboChartProxy` at 9017-9084. It also reflects the current Workspace `cartesian*.ts` helpers and application appearance model inspected on 2026-10-20. It is a bounded implementation contract, not evidence that the mapper or application has passed verification.

## Public boundary

Add `echarts/comboTypes.ts` and export `translateCombo` from `echarts/combo.ts`. Paths in this design are relative to `vendor/workspace/terminalpro/src/components/General/Table/Chart/` unless otherwise stated.

```ts
import type { ComboSeriesAssignment } from "../compatibility/comboAssignments";
import type {
  ApplicationResolvedStyle,
  ResolvedApplicationAppearance,
  ResolvedApplicationAxis,
  ResolvedApplicationSeries,
} from "../application/appearanceModel";
import type { ChartSnapshot } from "../compatibility/snapshotTypes";
import type {
  CartesianMappingContext,
  CartesianSeriesStyle,
  CartesianTranslationResult,
} from "./cartesianTypes";

export type ComboGeometry = "area" | "bar" | "line";

export interface ComboGeometryStyle {
  readonly series: ResolvedApplicationSeries;
  readonly overrides: Readonly<Record<string, CartesianSeriesStyle>>;
}

export interface ResolvedComboStyle {
  readonly common: Omit<
    ApplicationResolvedStyle,
    "application" | "series" | "line"
  >;
  readonly application: Omit<
    ResolvedApplicationAppearance,
    "series" | "axes"
  >;
  readonly axes: {
    readonly category: ResolvedApplicationAxis;
    readonly primary?: ResolvedApplicationAxis;
    readonly secondary: Readonly<Record<string, ResolvedApplicationAxis>>;
  };
  readonly geometry: Partial<
    Readonly<Record<ComboGeometry, ComboGeometryStyle>>
  >;
}

export interface ComboMappingInput {
  readonly snapshot: ChartSnapshot;
  readonly assignments: readonly Readonly<ComboSeriesAssignment>[];
  readonly style: ResolvedComboStyle;
  readonly context: CartesianMappingContext;
}

export type TranslateCombo = (
  input: ComboMappingInput,
) => CartesianTranslationResult;
```

Use the actual C1 `ComboSeriesAssignment` export. C2 receives the `seriesChartTypes` from a resolved C1 result; it neither repeats builtin splitting nor silently repairs unresolved assignments. An omitted `secondaryAxis` means primary for drawing without rewriting the supplied object.

The result uses the existing supported/unsupported/invalid union. Unsupported and invalid results contain diagnostics and no partial ECharts options. The public boundary catches malformed structures or throwing property access without exposing an exception. Use diagnostic paths into `snapshot`, `assignments`, `style` or `context`; distinguish missing required data from a supported source that cannot be represented.

Select numeric columns in `snapshot.selectedColumnIds` order. Require exactly one valid assignment for every selected numeric column and unique stable selected IDs. Reject duplicate assignment IDs, unknown assignment types and secondary assignments for groupedColumn, stackedColumn or stackedArea. Retained assignments for unselected columns are permitted but do not generate series, axes or legends. No selected numeric series yields an explicit unsupported diagnostic. C1 owns warning/default behavior before this boundary.

## Resolved appearance responsibilities

`common` contains the existing shared Cartesian display fields. `application` contains shared layout, captions, tooltip and palette settings. Their overlapping presentation values must be produced coherently by C3; C2 uses the existing application helpers' established precedence rather than introducing another saved-option merger.

`geometry` contains independent effective area, bar and line settings. Both area types use `area`; both column types use `bar`. Require every active geometry's entry and validate it. An inactive entry may remain present and must not be altered. Missing active styling must not fall back to another geometry. The `overrides` map provides resolved palette/color/outline values by column ID, not a new per-column Customize persistence model. Type-wide editor changes remain type-wide.

The existing `resolveApplicationAppearance` is a single-family resolver: it merges a family's option layers and requires exactly two concrete axes. C3 must compose the combo inputs deliberately. Calling it once and copying its series settings to every geometry would erase independently saved appearance.

`axes.category` is the concrete X axis, with bottom as its default and top also allowed. `axes.primary` is required only when a selected primary series exists. Each selected secondary series requires its own `axes.secondary[colId]`, with number type; right is the default and left is also allowed. These keys are transient drawing bindings; they do not add persistent secondary-axis editor IDs. C3 retains the original xAxis/yAxis editor semantics, first-two-concrete-axis targeting and theme numeric-axis inheritance.

Validate finite positive viewport dimensions and the existing observation/display context. Reuse existing style validation through immutable, geometry-specific Cartesian style views where practical. Do not mutate these views into the supplied appearance object.

## Shared coordinates and axes

All combo geometry shares one X coordinate system. Existing standalone line/area application helpers choose an ordinal value X axis, while bars choose a category X axis. Do not merge separately translated standalone options.

For categorical X, use a single category axis with one stable row-index category per snapshot row. Convert index coordinates consistently for line, bar and every area fragment. Preserve duplicate category labels as separate observations. Display labels and tooltips still read the original category values. For number/time X, use one shared continuous conversion through the existing category-coordinate rules, validate observations, and apply it to every geometry. Do not silently replace malformed continuous categories with indexes.

Generate a primary numeric axis, defaulting to left, only when at least one primary series exists. This conditional behavior follows `ComboChartProxy`: an all-secondary custom combo has the X axis and distinct secondary numeric axes, with no empty left axis. Allocate numeric axis indexes deterministically: primary first if present, followed by secondary series in selected-column order. Keep this mapping stable when legend visibility changes.

Every public series and every private area fragment receives the correct `yAxisIndex`. Multiple secondary series remain separate axes even when their units match. Apply each resolved axis style to its own axis. Compute offsets on both numeric-axis sides and required plot margins from visible label/title measurements using the existing layout helpers; do not place multiple right axes at the same unaccounted position. If necessary, extract a cohesive axis-style helper rather than copying the full standalone axes implementation.

Reuse `unitDiagnostics` separately for each numeric axis. Under declared-units policy, every drawn column needs explicit units and scale. Under raw-observations policy, absent metadata is allowed, but malformed metadata and conflicting known units/scales on the same axis remain rejected. USD revenue and USD/share EPS can occupy different axes. Two incompatible primary series cannot share one scale. Never convert, normalize or rescale stored observations to make an axis compatible.

Compute each axis domain from all visible geometry assigned to it. Include raw line/grouped-column values, signed stacked-column extrema and projected area extrema. An area-only domain must not clip a larger line or column on the same axis. Preserve zero and null distinctions, reject nonfinite derived geometry, and apply finite outward domain rounding. Hidden geometry does not contribute to the visible domain; hiding it must not remove or renumber its axis.

## Mixed geometry and helper reuse

Build series in stable selected-column order, preserving the public column ID as the ECharts series ID and name. Legend labels may repeat; IDs must not. Use the global selected-series palette position, never a subgroup-local position.

Grouped columns remain independent bar groups. Stacked columns share a dedicated column stack using the existing signed-stack behavior. Area and column stacks have different identities. `seriesGroupType` is not a combo-wide grouping instruction.

Use `projectArea` for the subset of stackedArea columns together and for independent area columns. Do not include lines, columns or independent areas in stackedArea accumulation. Preserve the helper's missing-value, negative-value and legend-selection semantics. Reuse `cartesianAreaSeries` for its fill/stroke/marker decomposition rather than implementing a second area engine.

Extend the area-series helper with an optional internal rendering context carrying global palette indexes and the complete reserved public-ID namespace. Existing callers retain their current defaults. All generated area IDs must be unique against every selected public ID and every other generated ID, including IDs outside the area subgroup. Use the matching global palette position for fills, outlines and markers. Attach axis indexes to all returned fragments before combining them.

Geometry-specific Cartesian views supply the relevant `ResolvedApplicationSeries`, per-ID overrides and axis appearance to existing series helpers. Never send a bar appearance object to line/area markers as a convenience. If a helper needs extension for shared categorical coordinates, add one explicit rendering-context input with unchanged standalone defaults.

Use original snapshot observations for financial tooltips. Projected cumulative endpoints are geometry, not replacement financial values. Preserve existing area label semantics separately from raw tooltip values. Internal fill/stroke series do not appear as independent legend entries or tooltip observations.

## Legend, navigator and lifecycle boundary

C2 accepts `context.legendSelection` and produces correct main geometry without changing observations. Area projection must be recomputed when hiding a contributing stack member. Public legends retain the selected series IDs. Axis identity, palette position and private/public ID namespaces remain deterministic across repeated mapping.

C2 does not call or modify application session routing, the gallery, saved-state reducers, the renderer lifecycle, or navigator integration. A caller can request a full overview by omitting legend selection and a filtered main view by supplying it. The mapper itself owns no live selection state.

C4 must adapt `cartesianNavigator` before combo activation. It currently assumes singular axes and assigns every miniature series to `yAxisIndex: 1`. Combo integration must clone every numeric axis, remap each miniature series and fragment, separate miniature stack identities, and preserve independent financial scales. The overview retains all original series regardless of main legend selection.

C4 also registers combo legend reprojection, retains the existing navigator range across refresh, and validates save/reopen and export against the actual application. Unit mapper tests do not establish those lifecycle claims or real FMP acceptance.

## Sequential implementation slices

C2 should be split into C2a and C2b. Both retain independent review and per-task commits, and neither activates the feature. This split separates financial admission/axis planning from geometry assembly; it is not permission to leave inert scaffolding accepted as a completed feature.

| Slice | Exclusive writable scope | Reviewable output |
| --- | --- | --- |
| C2a | New `echarts/comboTypes.ts`, `comboAdmission.ts`, `comboAxes.ts`; focused `combo.admission.test.ts` and `combo.axes.test.ts` under the Workspace chart-compatibility unit tests | Frozen input contract, selected assignment/axis plan, source/context/unit admission, shared coordinate/axis styling and domains |
| C2b | New `echarts/combo.ts`, `comboSeries.ts`; bounded `cartesianAreaSeries.ts` rendering-context extension and, if required, a cohesive shared helper extraction; focused `combo.geometry.test.ts`, `combo.render.test.ts` | Complete inactive mapper with existing area helper reuse, independent styling, deterministic IDs/palettes and real ECharts rendering evidence |

C2b depends on reviewed C2a. Freeze the internal plan interface at the C2a review: selected columns and assignments, global palette positions, per-column numeric-axis indexes and axis groups. The controller serializes any required changes to shared axis/series helpers and declares their ownership before dispatch. Do not modify an undeclared shared file to make the mapper compile.

Production additions and every modified production file must pass 400 physical lines/file, 300 logical units/file and 50 logical units/function. Tests and this design are outside production caps. The controller adds maintained paths to the existing complexity inventory and passes the exercised commands from [complexity checks](../../../docs/complexity.md) to workers before dispatch. Cohesive extraction is required if a touched helper exceeds a cap; compressed code and arbitrary forwarding files do not satisfy the design.

## Required evidence

Focused regressions must independently establish:

- Selected numeric projection, absent/duplicate/malformed assignments, primary-only secondary rejection and immutable inputs.
- Primary plus multiple distinct secondary axes, all-secondary input, stable indexes under legend hiding and left/right-axis layout accommodation.
- USD primary with USD/share secondary succeeds; incompatible primary metadata, malformed scales and declared-unit gaps fail without partial options.
- Shared categorical alignment for mixed columns/lines/areas, duplicate labels and continuous category validation.
- Grouped columns beside signed stacked columns, area/column stack separation, independent versus stacked areas, negative/null/zero observations and overflow diagnostics.
- Union axis extrema, including a large line beside a smaller area stack, plus independent secondary extents.
- Independent geometry appearance, global palette order, internal-ID collision avoidance and numeric-axis assignment on every area fragment.
- Raw tooltip values after area stacking and hidden-stack reprojection, without mutation of the full overview source.

C2b also runs an isolated headless ECharts render check for mixed category alignment and independent numeric scales; option shapes alone cannot establish correct rendering. Retain existing area regression coverage when changing its helper. Use focused unit/static checks and the established portable gate with explicit fork scope. The controller supplies exact commands discovered in the current checkout and serializes heavy runs. Record revision, command, exit code and evidence location; planned tests remain planned until executed.

C2 acceptance requires the complete mapper, independent review and fresh verification. C3/C4 application behavior and the completed milestone's real-FMP acceptance remain separate gates. No C2 completion dispatches the alpha image pipeline.

## Original axis editing clarification

The original axis editor permits top/bottom category positions and left/right numeric positions (getAxisPositionSelectParams 12580-12605). Concrete position writes target one axes[index] (18777-18800); axis identity and financial grouping remain independent of its side. These are accepted mapper inputs, not reasons to disable controls. Original save/reopen retains theme overrides but not concrete position edits (getChartModel 7634-7651, getChartThemeOverrides 8640-8642), so restored defaults are source behavior. Combo category/series inversion is unavailable in the original supportsInvertedCategorySeries 19816-19818; C3 must preserve that original eligibility.
