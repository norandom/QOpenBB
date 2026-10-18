# Restore ordinary horizontal bars

## Overview

The next UI-10 slice makes the existing Grouped Bar and Stacked Bar choices work in ordinary Table/File widgets. It reuses the accepted editor, grid snapshot, ECharts host and Widget persistence owner. The visible change is restored horizontal charts with the original controls, not a new editor or theme.

This is a scoped amendment to the approved [application integration design](chart-live-editor-integration-design.md). Tasks 2.78-2.81 are implemented and independently accepted for ordinary callers; see the [application review](../../../artifacts/reviewed/live-editor/horizontal-bars/application-acceptance/review.md). Normalized charts, areas, stacked lines, combinations and aliases used by other entry points remain explicit UI-10/UI-13 obligations. No existing gallery entry, button or flag is removed or hidden to represent this scope.

## Boundary commitments

**Owns:** `groupedBar` and `stackedBar` admission, horizontal numerical projection, family-aware initial axes and transitions, physical axis/title controls, existing quick actions, export and saved-state integration for ordinary callers.

**Out of boundary:** `bar`/`column` schema aliases and other entry points; normalization denominators; area or combination series; advanced tables; providers, database adapters, dependencies, image builds and release acceptance. Previously accepted column/line behavior must remain intact.

**Allowed dependencies:** existing `ChartSnapshot`, `OptionBaseline`, `ApplicationAxisRuntime`, `AxisBinding`, session stamps, option/range reducers, effective appearance, native ECharts APIs and owned Playwright fixtures. There is no new state store, persistence envelope, library or compatibility service.

**Revalidation triggers:** family orientation changes require axis bindings, titles, labels, tooltip coordinates, stacking and quick actions to be checked together. Changes to range or session identity require the existing replay/freshness checks. Other-family admission requires its own concrete numerical/control contract; a bar-style fallback is not acceptance.

## Architecture and contracts

Flow remains: original saved model and displayed grid -> existing session/capture -> resolved appearance and typed bindings -> ECharts mapping -> existing host. Editor intents return through the latest-state Widget transaction and original reducers. ECharts output never becomes saved `chartOptions`.

### Family and numerical meaning

Extend the existing admitted family union with exactly `groupedBar` and `stackedBar`. A small shared family-orientation predicate may live beside that union; do not scatter additional string lists or introduce a general chart registry. Persist exact chart types, with the existing `bar` option partition and per-family range keys.

Grouped bars display independent horizontal magnitudes. Stacked bars preserve selected series order and the original positive/negative stacking behavior. Keep raw observations, zeros, negative values, missing values, stable descriptor IDs and financial formatters. Displayed labels and tooltips continue to report the corresponding raw observation; no percentages or cumulative values replace it. Confirm original category ordering and stack behavior from the retained source before fixing the reference expectations.

Use the existing axis and observation-coordinate mapping rather than swapping source columns or transposing the dataset. Set Up's Switch Category / Series remains an explicit, independent transformation. Aggregation and range selection retain their current owners and financial semantics.

### Axis lifecycle and physical controls

Horizontal bars initialize category on the vertical axis and number on the horizontal axis. Entering the family from an accepted column/line chart must establish those axes as well; changing only the initial caller or saved chart type is insufficient. Family transitions retain original per-family ranges and inactive option branches through the existing session transition.

Runtime structural edits remain authoritative for their current family session under the original reset/transition behavior. Do not invent persisted axes: the original `getChartModel` omits concrete structural axes, and reopen continues to reconstruct them from original inputs. Preserve the disclosed structural-axis and numeric-rotation/Auto Rotate limitations.

The editor's Horizontal Axis section and horizontal title refer to the axis whose binding direction is `x`; Vertical Axis and vertical title refer to `y`. For bars this means number/horizontal and category/vertical. Both selection and intent rehydration resolve that mapping from the latest concrete axes. Style writes still use the actual option type and both original positions for the direction: bottom/top for x, left/right for y. Semantic category/number identity must not be replaced with a physical-heading name in storage.

Keep the original section order, eligibility, position choices, typography, color tokens and control components. `ApplicationCustomizeEditor` renders direction x first and y second while retaining semantic axis IDs; relabeling category-first sections alone would reverse the original order for bars. Category-specific controls follow the category axis even when it is vertical. No extra axis selector or toolbar is introduced.

### Quick actions and saved state

Retain original action predicates, navigator/miniature behavior, export freshness and table return. Confirm the horizontal-bar navigator contract against original source; do not infer its orientation from the bar orientation. Existing `cartesianNavigator.ts` currently controls xAxisIndex 0 and projects its miniature through fixed x/y fields, so horizontal-family admission requires checking that contract explicitly.

Save/reopen preserves exact chart type, original option leaves, selected range/series and unknown/inactive branches. Existing save-failure recovery and latest-state transactions remain unchanged. A failed mapping or missing applicable action blocks this slice's acceptance; it is not a reason to hide the control or substitute a column chart.

## File structure plan and bounded parallel work

Production paths below are relative to `vendor/workspace/terminalpro/src/components/General/Table/Chart/`; test paths are relative to `vendor/workspace/terminalpro/`. The controller freezes shared types and axis lifecycle behavior before the two Sol lanes start. Astra independently reviews the contract and final join. New interfaces remain typed; this work adds no `any` or unchecked casts.

| Owner | Files | Responsibility |
| --- | --- | --- |
| Controller, first | `echarts/cartesianTypes.ts`, `application/axisStructureTypes.ts`, `application/applicationSessionTypes.ts` only if their existing types need extension | Exact family union, orientation and transition contract; no runtime activation yet |
| Sol renderer lane | `echarts/cartesian.ts`, `echarts/cartesianSeries.ts`, `echarts/cartesianAxes.ts`, `echarts/cartesianLayout.ts`, `echarts/cartesianBarColors.ts`, `echarts/cartesianNavigator.ts`, `echarts/cartesianNavigatorMask.ts` | Horizontal mapping, signed stacking, labels, tooltip/legend and source-equivalent actions; retain columns/line |
| Sol controls lane | `editor/ApplicationAxisEditor.tsx`, `editor/ApplicationCustomizeEditor.tsx`, `compatibility/editorBindings/selectApplicationEditorState.ts`, `rehydrateApplicationEditorEvent.ts`, `mapApplicationEditorEvent.ts`, `metadata.ts`, `eligibility.ts` in that same bindings directory | Direction-ordered physical headings/title selection and latest-intent mapping, existing eligibility and original saved leaves |
| Controller, after both lanes | `caller/chartInputs.ts`, `application/applicationSessionRuntime.ts`, `application/useApplicationSessionScope.ts`, `application/applicationSessionSelection.ts`, `AgChartView.tsx` | Initial and transition axes, caller admission and real application join |
| Each lane | Existing `tests/unit/chart-compatibility/` or `tests/unit/chart-application/` owning its behavior | Focused expected-value and binding regressions, without duplicating the application harness |
| Controller | Existing `tests/e2e/live-chart/` fixtures plus a behavior-named horizontal-bar journey; root inventory, breadth and spec records | One meaningful joined browser check, source/evidence identity and per-task delivery |

No lane edits another lane's files. Shared contract changes stop affected work until refrozen. Exact executable task numbers and command handoffs are generated after design approval. Each modified maintained production file must pass 400 physical lines, 300 logical units and 50 units/function, measured as a whole. Extract by responsibility before a cap is exceeded; no new exception is proposed. Reuse the existing inventory/checker and explicit fork-scope manifests; tests/docs remain exempt.

## Verification and acceptance

| Requirement | Observable evidence |
| --- | --- |
| 4.8, 4.9 | Original Grouped Bar/Stacked Bar choices render horizontally; grouped versus signed-stacked results, category order, themes, labels, tooltip and applicable quick actions match source-backed expectations |
| 4.7, 4.8 | Family switches preserve ranges and unknown options; physical axis/title edits affect and save the correct original branch; reopen restores the selected bar family and observations |
| 10.1, 10.2, 10.3 | One isolated headless actual-Workspace journey uses existing Playwright/CDP fixtures; exercise both bar families, representative axis/title edits, navigation if originally applicable, export and fresh backend reopen |
| 10.4, 10.5, 10.6 | Bounded lanes and one heavy check; explicit size scope, per-task independent review, capability-to-evidence mapping; pending families and failed checks remain unverified |

Use unequal values including negative, zero and missing observations for independent mapper expectations. Exercise switching between a column and horizontal bars to catch stale axes and range loss. Reuse accepted save-failure/restart and aggregation checks unless a changed owner creates a specific regression risk. Do not repeat a full three-family option matrix.

Inspect representative integrated light/dark images and current export. Use retained original evidence; capture a new original observation only for a concrete unresolved contract such as horizontal navigator behavior. Ask the owner to judge uncertain visual differences with matched views. Publish one concise delivery record and only necessary screenshots.

Disproof conditions: wrong axis/title receives an edit; category order or signed values change; switch/reopen returns columns; raw values are silently normalized; inactive settings disappear; an applicable original action is inert; another family/button is hidden. Any such finding prevents acceptance.

## Research basis and remaining decisions

Source inspected at Workspace `aa2e0bfe4253edf6bf6ef2f18822d4304f07fdd8`. The capability matrix and retained family-navigation source plan establish original bar gallery choices and family-specific range restoration. Current mapper, caller and editor source establish the gaps above. The accepted live-editor contracts establish direction-aware option paths and structural-axis persistence limits.

Design synthesis: horizontal bars are an orientation/stacking extension of the existing Cartesian pipeline, not a second renderer. Native ECharts remains the chosen engine; no dependency selection or version change is needed. Normalization and combinations are deliberately separate because they need additional numerical and per-series contracts, not merely more admitted strings. Core product/tech/structure steering remains absent; existing project policies apply.

Original AG Charts `DIRECTION_SWAP_AXES` in the locally retained `ag-charts-community/dist/package/main.cjs.js` (lines 25909-25932 in the inspected install) specifies number/bottom and category/left for horizontal series. Original Workspace `themes.tsx` and `hooks/useTableContext.tsx:378-400` apply navigator/miniature flags without excluding horizontal bars. Current navigator controls xAxisIndex 0; changing it to y merely because bars are horizontal would invent a contract.

Task generation may include a controller-owned contract prerequisite. That first leaf must record and independently review original top-to-bottom category order, signed-stack endpoints, navigator target/effect and miniature behavior before dependent renderer implementation starts. Reuse the retained original runtime/source and one synthetic unequal signed-value fixture; record exact source/package identity. If source alone cannot settle an observable difference, make one bounded original observation before dependent implementation. If the original action itself fails or a necessary visible deviation is found, disclose its observed consequence and obtain an owner decision before acceptance rather than copying failure or hiding it as parity. This prerequisite does not authorize a generic capture workstream; renderer tasks cannot proceed on guessed expectations.

## Horizontal application join scope clarification

The task 2.81 browser run exposed existing three-family guards in `application/effectiveAppearance.ts` and `application/axisStructure.ts`, plus the narrow formatting input type in `application/types.ts`. These three existing application-owner files are added to the controller join scope, limited to consuming the accepted horizontal family contract. Independent Astra integration review confirmed this is necessary for the approved appearance and structural controls, without adding another state owner or feature. The combined size gate includes all three; caller tests exercise real appearance and axis transitions, and the browser changes the vertical axis position. The failed run is retained locally at `artifacts/live-editor/runtime/horizontal-join-2`.
