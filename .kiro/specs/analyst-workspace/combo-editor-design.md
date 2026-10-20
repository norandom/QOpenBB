# C3 combination-chart editor and session contract

C3 extends the existing application session and editor for combination charts. It preserves Set Up column assignments separately from Customize geometry styling. C4 owns production admission, mapper routing, navigator integration and real-data acceptance. Completing C3 does not make the feature releasable.

The owning contracts are [the milestone](chart-port-milestone.md) and [the C2 mapper design](combo-mapper-design.md). This bounded proposal was checked against the retained original AG Grid Enterprise 34.1.1 bundle and Workspace sources on 2026-10-20. Source inspection establishes the contracts below; it does not establish runtime acceptance.

## Confirmed source semantics

All bundle line references refer to `artifacts/task-2.1/frontend/terminalpro/node_modules/ag-grid-enterprise/dist/ag-grid-enterprise.js`.

| Source | Required behavior |
| --- | --- |
| ChartController 7833-7852 | Editing a series type or secondary flag converts the chart to Custom Combo, retains the other assignments and reruns primary-only coercion. |
| SeriesDataPanel 12163-12238 | Set Up displays selected columns. Type choices are line, area, stackedArea, groupedColumn, stackedColumn. Secondary Axis is disabled for stackedArea and both column types. |
| SeriesPanel 13930-14166 | Customize selects active geometry types in area/bar/line order, then exposes the selected type's controls. It does not select a column. |
| ChartOptionsService 18596-18602, 18829-18840 | Series edits write a type-wide series theme override. |
| Axis position selector 12580-12605 | Combo X position can be top/bottom; Y can be left/right. Only heatmap is excluded here. |
| ChartOptionsService 18764-18800, 18817-18828 | Theme numeric-axis edits apply across left/right orientations; concrete setters target one selected axis. xAxis/yAxis selection considers the first two concrete axes by direction. |
| getChartModel 7634-7651; getChartThemeOverrides 8640-8642 | Saved chart options contain theme overrides. Concrete position edits and the older custom-assignment cache are not serialized. |
| CartesianChartProxy 8119-8127; ComboChartProxy 9017-9084 | Data-driven proxy rebuilding recreates axes from defaults: bottom X, left primary if present, and one right axis per selected secondary series. |
| supportsInvertedCategorySeries 19816-19818 | Combo charts do not support the Switch Category / Series interaction. |

Preserve reachable axis-position controls. Position edits affect the current concrete axis until a source-equivalent rebuild; reopen restores default positions. Do not add persistence for concrete positions through `qopenbbAxisSettings` or another extension. All-secondary input has no left primary axis; its first right numeric axis is the yAxis editor target. Other secondary axes retain separate identity even when the first numeric axis changes side.

Original gallery `setChartType` at 7662-7671 also resets `switchCategorySeries`, `categoryAxisType` and `seriesGroupType`. The milestone explicitly requires preserving `seriesGroupType`, so retain that inactive saved field as the authorized compatibility exception and do not use it to stack combo geometry. Do not expose the unsupported inversion control for combos.

## Custom assignment cache and model ownership

`ComboChartModel.savedCustomSeriesChartTypes` is transient. Gallery selection calls `updateSeriesChartTypes` directly, bypassing `initComboCharts`. This distinction matters: passing retained nonempty assignments through C1 initialization on every builtin gallery selection would immediately turn that builtin back into Custom Combo.

Use an optional custom-assignment cache on the existing `ApplicationSessionLocal` owner. It is not a new persistence owner or a new Widget storage field. Initialize it from supplied custom assignments when applicable. A custom assignment edit updates it. Selecting a builtin computes its selected-column split without overwriting the live custom cache. Returning to Custom Combo uses the cache and C1's missing-column/default rules. Selection and projection preserve unselected custom assignments.

`getChartModel` serializes current `seriesChartTypes` for a combo chart and omits them for noncombo charts; it never serializes the older cached custom assignment list. On reopen, hydrate only the saved current assignments. Do not promise recovery of an older custom configuration after saving a builtin or noncombo chart.

There is a source-derived initialization nuance: builtin models also serialize current assignments, and the original constructor's nonempty supplied assignments select Custom Combo. Preserve C1's supplied-assignment semantics. Add a regression for this restore path and distinguish preserved drawn assignments from the restored chart-type identity; do not silently invent an alternate initialization rule.

The retained Workspace `hooks/useChartOptions.tsx` lines 436-490 writes the `getChartModels()` snapshot plus theme overrides into the computed partition. It provides no additional cache persistence. Continue using that computed-partition contract, `selectOptionBaseline`, `reduceIntegratedState` and functional Widget transactions.

## Transaction boundary

Introduce an application chart-family union containing the existing Cartesian families and C1's `ComboChartType`. Do not broaden `isCartesianFamily` or modify the C2 mapping interface. Keep a discriminated combo selection alongside the existing single-family selection rather than pretending a mixed style is `ApplicationResolvedStyle`.

Assignment intents contain only the stable column ID and requested type or secondary flag. Rehydrate current assignments inside the latest Widget transaction using existing stamp, address, generation, data and range checks. Reject a no-longer-selected target. C1 owns fallback diagnostics and primary-only coercion.

An accepted assignment edit atomically updates the computed chart model's assignments, model/root chart type and local baseline to `customCombo`. The existing `sessionBaseline` family equality check must handle that deliberate transition without allowing stale edits from unrelated family changes. Preserve unknown model fields, inactive option branches and unaffected column assignments.

Do not serialize resolved styles, palette positions, numeric-axis indexes, geometry-selector state or concrete secondary-axis IDs. Ordinary setup range/category/aggregation changes continue through the existing transition and capture machinery. Unsupported category-series inversion stays unavailable.

For C3a, derive selected numeric IDs from the latest validated range and capture without invoking `projectOrdinarySetup` or appearance selection. Its existing single-axis unit check rejects mixed declared units before combo axis assignment is known. C3b/C4 must retain setup aggregation and provenance while deferring combo unit comparability to C2's per-axis admission. Do not weaken the ordinary single-axis check or strip financial metadata to bypass it.

### Frozen inactive C3a API

Parameterize the existing `ApplicationSessionInputs` and `ApplicationSessionContext` with `F extends ApplicationChartFamily = CartesianFamily`. `ComboSessionContext` is an alias of the existing context specialized to `ComboChartType`, not another state owner. Keep default Cartesian types for the existing appearance, editor, projector and React hook consumers.

```ts
initializeComboSession(
  context: ComboSessionContext,
): SessionResult<ApplicationSessionLocal>;

selectComboSessionAssignments(
  storage: ChartStorageOutput,
  context: ComboSessionContext,
): SessionResult<ComboSessionAssignmentSelection>;

applyComboAssignmentTransaction(
  storage: ChartStorageOutput,
  context: ComboSessionContext,
  command: ComboAssignmentCommand,
): SessionResult<ApplicationSessionCommit>;

applyComboFamilyTransaction(
  storage: ChartStorageOutput,
  context: ApplicationSessionContext<ApplicationChartFamily>,
  stamp: SessionStamp,
  chartType: ApplicationChartFamily,
): SessionResult<ApplicationSessionCommit>;
```

`ComboSessionAssignmentSelection` contains `baseline: OptionBaseline`, `range: ResolvedRange`, resolved `chartType: ComboChartType`, readonly `seriesChartTypes: ComboSeriesAssignment[]` and readonly C1 `diagnostics`. `ComboAssignmentCommand` contains the current stamp, `family: ComboChartType` and an intent with `panel: "comboAssignment"`, `colId`, and either `{ kind: "type", value: ComboSeriesChartType }` or `{ kind: "secondaryAxis", value: boolean }`.

Initialization hydrates the same local owner after baseline/range initialization and does not require captured observations. Transactions return the existing storage/local/capture/change commit shape; the caller advances revisions as in existing transactions. A builtin-to-custom commit returns its coherent new baseline directly rather than testing it against the old input family.

Make only family-neutral baseline/range/setup helpers and initial-session hydration generic in C3a. Leave `selectApplicationSession`, `editorSelection`, `projectApplicationSession`, hook routing and gallery admission unchanged. The exported pure transactions are the reviewable C3a result, not a claim of live UI integration.

`changeCallerChartType` has no access to local cache and must not implement cached transitions. C3b/C4 routes gallery choices through the explicit family transaction on the existing owner. Its join must also address `useApplicationSessionScope` currently re-registering on `inputs.family`, which would otherwise discard the live cache.

## Appearance and editor projection

Resolve active area, bar and line appearance independently from the existing baseline/generated/theme layers, using full selected-series order for palette allocation. Populate the frozen C2 `ResolvedComboStyle`. Extract reusable layer resolution from `effectiveAppearance.ts` if necessary; do not copy its merge precedence into a competing implementation.

Keep shared title, legend, padding, background and tooltip behavior separate from selected geometry's series styling. Series, marker, label, shadow and connection edits target the existing geometry option branch. Customize's geometry selector is transient; retain the selected type while active, otherwise choose the first active type in area/bar/line order.

Reuse existing editor panels and event rehydration with a geometry-specific view. Never map an entire combo to the default bar branch in `mapApplicationEditorEvent`. Preserve inactive options when a geometry disappears and becomes active again.

Build transient concrete axes from resolved assignments and bind the existing two axis editor groups to the first-two-axis semantics above. The current axis runtime assumes category/number identities; a combo adapter can provide those editor bindings while retaining its full concrete axis list separately within the existing session. Resolve every numeric axis's inherited theme appearance, but apply concrete rotation/type/position state only to its actual target.

## Bounded sequential slices

Paths below are relative to the Workspace `terminalpro/src/components/General/Table/Chart/` directory. Tests belong under `terminalpro/tests/unit/chart-compatibility/`, with component tests in the existing editor test infrastructure.

| Slice | Owned files and changes | Completion boundary |
| --- | --- | --- |
| C3a: assignment transaction | New `application/comboSessionAssignments.ts`, `comboSessionTypes.ts`; bounded family-neutral edits to `applicationSessionTypes.ts`, `applicationSessionSelection.ts`, `applicationSessionRuntime.ts`, `applicationSessionRange.ts` | Inactive pure atomic type/axis assignment and family transactions, transient cache and saved-model semantics with regressions |
| C3b: appearance/editor projection | New `application/comboAppearance.ts`, `comboSessionSelection.ts`, `comboEditorSelection.ts`, `comboEditorTransaction.ts`; declared extraction from `effectiveAppearance.ts`; bounded selection/runtime dispatch edits | Independent geometry styles, current editor views, full concrete axes and source-equivalent event targets |
| C3c: editor composition | New `editor/setup/ChartComboAssignmentsPanel.tsx`, `editor/series/ChartComboSeriesSelector.tsx`; extract existing private Series component into `editor/ApplicationSeriesEditor.tsx`; bounded edits to `ChartSetupPanel.tsx`, `ApplicationCustomizeEditor.tsx`, `ApplicationChartEditor.tsx` | Source-equivalent Set Up and Customize controls using existing styling, docking and accessibility behavior |

Run these slices sequentially with independent review and per-task commits. Before dispatch, the controller freezes shared type additions and the exact extraction paths, including any required editor-binding or runtime files. C3a does not edit `applicationSessionSetup.ts`, `useApplicationChartSession.ts` or `caller/chartInputs.ts`; their live transaction routing belongs to the later join. No worker edits an undeclared shared file or C2-owned code. The controller owns inventory updates and final integration.

Each modified production file must satisfy 400 physical lines/file, 300 logical units/file and 50 logical units/function. Extract cohesive transaction or presentation responsibilities when necessary; do not compress existing code or introduce forwarding modules solely to pass counts. Pass the exercised complexity and focused verification commands from the current checkout in each worker handoff.

Keep the production `AgChartView` support gate, combo rendering branch, navigator changes and release pipeline untouched until C4. C3 components and transactions can be verified without making combo choices appear fully implemented.

## Acceptance evidence

Require regressions for builtin/custom/live-cache transitions, serialized-current versus transient-cached assignments, restore initialization, unselect/reselect, reorder and missing columns. Test assignment edits against latest storage and stale command rejection, including the builtin-to-custom baseline transition.

Appearance tests must prove type-wide writes affect every matching geometry without overwriting another geometry or unknown/inactive options. Axis tests must prove all-secondary targeting, inherited numeric styles, concrete position edits, default-position restoration and source-equivalent rebuild reset. Test that combo inversion is unavailable while aggregation remains functional.

Component checks cover selected-column type controls, disabled secondary flags, active geometry selector order, correct controls for each geometry, keyboard labels and retained docking/collapse behavior. Preserve existing ordinary-chart regressions when extracting shared panels.

C4 remains responsible for the actual application's mapper routing, navigator overview and independent scales, refresh behavior, save/reopen, export and real FMP evidence. Source inspection and unit checks must not be reported as those completed acceptance tests.
