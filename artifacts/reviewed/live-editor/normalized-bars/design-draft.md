# Restore ordinary 100% stacked columns and bars

## Overview

Restore the existing `normalizedColumn` and `normalizedBar` gallery choices in ordinary Table/File widgets, using the accepted editor and ECharts renderer. Financial engineers keep the original flow, themes, controls and saved chart types. This is a scoped amendment to the existing application design and UI-10, not complete renderer or release acceptance.

### Goals and non-goals

Make both orientations render the original normalized geometry, raw labels/tooltips, percentage axes, legend interactions, navigation, overview, export and saved-state journey. Preserve all five accepted families. Normalized lines/areas, combinations, schema aliases, advanced callers, providers, database work and release images remain outside this slice.

## Boundary Commitments

### This Spec Owns

Normalization of drawn coordinates after existing Set Up projection; admission of these two exact families; percentage-axis presentation; native legend-driven reprojection; integration into existing appearance, axis and caller owners. Existing snapshots and Widget storage remain authoritative for raw observations and saved configuration.

### Out of Boundary

No new data transformation service, persistence schema, selection store, editor, flags, dependency or package upgrade. No removal or disabling of gallery entries or quick actions. Cross-filtering/standalone callers remain outside ordinary caller acceptance.

### Allowed Dependencies

Reuse `ChartSnapshot`, Cartesian mapping context, resolved application appearance, setup projection, original option/range reducers, ECharts native stacking/legend/dataZoom and the accepted host lifecycle. Use existing pinned Node/Vitest/Playwright and complexity inventory. Core product/tech/structure steering files remain absent; existing project policies apply.

### Revalidation Triggers

Changing denominator membership, legend lifetime or formatter precedence requires geometry, labels/tooltips, overview and export checks together. Changes to host request/revision handling require lifecycle cleanup/error tests. Changes to family transitions require range/axis restoration and fresh backend reopen. Other-family admission requires another bounded contract.

## Architecture

Raw grid observations -> existing Set Up projection -> immutable raw snapshot -> normalized drawn coordinates -> native ECharts signed stacks. Raw snapshot callbacks continue to supply labels/tooltips. Editor intents return through the existing Widget transaction owner. No normalized values or legend selections are written into saved observations.

The installed ECharts stack remains the renderer. A small pure `cartesianNormalization.ts` helper handles the original denominator rule; native signed stacking handles geometry. A generic normalization library would not remove the original-specific denominator, raw-value and enabled-series contracts, so no new dependency is proposed.

### Numerical contract

For each displayed category and selected stack, let P be the sum of positive enabled values and N the sum of negative enabled values. Let D = max(P, abs(N)). With D > 0, drawn segment = 100 * raw / D. Accumulate each sign separately in selected series order. This is not sum-of-absolute-values normalization and does not independently stretch each sign to 100%.

| Raw selected values | Drawn segments | Consequence |
| --- | --- | --- |
| 7, 3, -2 | 70, 30, -20 | Positive endpoint 100; negative endpoint -20 |
| -4, -6, 5 | -40, -60, 50 | Negative endpoint -100; positive endpoint 50 |
| 7, 3, -2 with second series hidden | 100, hidden, -200/7 | Enabled membership changes the denominator |
| 0, 0, missing | no finite normalized nodes | D=0 must not create NaN/Infinity or fabricate 100% |
| all missing | no finite normalized nodes | Preserve missing observations in the raw snapshot |

A zero remains raw zero when a finite row can render it; missing is not converted into a financial zero. Labels/tooltips retain raw values and current financial formatters. Aggregation and category/series switching occur before normalization through existing owners. Main numeric domains derive from the normalized endpoints plus zero; do not force all mixed-sign data to [-100,100]. Default numeric-axis labels follow the original rounded percent format; category formatting is unchanged. Preserve original crosshair formatting once the source/runtime contract is frozen.

### Native legend and renderer lifetime

ECharts remains the sole owner of transient legend selection. The initial projection and legend updates use the same pure numerical helper. Freeze an optional typed renderer request callback `projectLegendSelection(selected: Readonly<Record<string, boolean>>): EChartsOption`, built by the application projection from immutable current inputs. Its paired `legendScope: string` identifies the existing state address, session generation and family; it does not change on ordinary render revisions. It reconstructs main/overview options without rereading mutable Widget state or serializing functions into ECharts options.

`lifecycle.ts` subscribes to native `legendselectchanged` once for this capability and reads the latest accepted request. On a selection change, it reprojects, retains the native selected map and navigator extent, and applies options without emitting another selection event. Theme/size/data revisions use the latest callback; stale callbacks cannot overwrite newer requests. Retain only currently present stable series IDs; new IDs start enabled. Reset transient selection when the host is disposed or legendScope changes; no new saved field is added.

Forward interaction failures through the existing host `onError` channel using a typed optional error callback on the render request; the failed renderer must not remain exportable as if current. Disposal removes listeners, releases partial initialization and prevents late callbacks from reviving the instance. Export uses the current native geometry, including the active legend choice, under the existing revision gate. Do not create a second React/session selection owner.

### Navigation and overview

Navigator stays on physical X: category X for normalizedColumn, numeric X for normalizedBar. Numeric cropping retains category rows and never recomputes normalization from the clipped viewport.

Original miniature source omits main-series visibility and therefore computes its own full selected-series normalization. The replacement overview must retain that independence: hiding a main legend series changes main geometry but not the full overview denominator or series set. Do not simply duplicate already legend-normalized main geometry. Use the same raw helper with all selected series enabled for the overview, then the existing miniature layout/mask.

The proposed normalizedBar overview extends the owner-approved working horizontal overview to this family, with the same theme, controls and area. Original miniature source drops bar direction; actual normalized-family rendering is not yet observed. Approval of this design explicitly includes a working horizontal normalizedBar overview rather than reproducing an empty/failed strip. Any further visible deviation requires an owner decision. NormalizedColumn retains vertical overview orientation.

## File Structure Plan

All production paths below are relative to `vendor/workspace/terminalpro/src/components/General/Table/Chart/`. Tests are relative to `terminalpro/`. Freeze shared contracts before parallel work; no lane edits another lane's files.

| Owner | Concrete paths | Responsibility |
| --- | --- | --- |
| Controller prerequisite | `echarts/cartesianTypes.ts`, request interfaces in `echarts/lifecycle.ts`, `application/applicationSessionTypes.ts`; `tests/unit/chart-compatibility/fixtures/normalized-bars.json` | Family/normalization predicates, legend callback/error contract and independent original fixture; no caller activation |
| Sol numerical renderer | New `echarts/cartesianNormalization.ts`; `echarts/cartesian.ts`, `echarts/cartesianSeries.ts`, `echarts/cartesianAxes.ts`, `echarts/cartesianDisplay.ts`, `echarts/cartesianNavigator.ts` | Raw-to-drawn projection, signed stacks, axis presentation and independent full overview |
| Sol native lifecycle | `echarts/lifecycle.ts` implementation after interface freeze, `echarts/EChartsHost.tsx` | Latest-request legend reprojection, selection/zoom retention, cleanup, error/export freshness |
| Controller application join | `AgChartView.tsx`, `application/effectiveAppearance.ts`, `application/axisStructure.ts`, `application/applicationSessionProjection.ts`, `application/useApplicationChartSession.ts`; `compatibility/editorBindings/mapApplicationEditorEvent.ts`, `compatibility/editorBindings/selectApplicationEditorState.ts`; `caller/chartInputs.ts` only if predicate propagation is insufficient | Admit exactly the two families through every existing guard, compose callback and independent overview, pass host request, preserve ranges/options/orientation |
| Controller verification/delivery | Existing unit and `tests/e2e/live-chart/` infrastructure; root inventory, breadth, spec/source pins | One joined normalized dashboard journey and selective per-task delivery |

The shared family type/predicates replace repeated admission lists within these touched owners; no general chart registry is introduced. Existing axis/session/formatting consumers already use CartesianFamily. No unrelated historical column-command API is expanded. New pure helper receives immutable typed data and returns drawn values; no `any` or unsafe raw-option decoding is introduced.

Production caps are 400 physical lines/file, 300 logical units/file and 50/function. The existing inventory/checker from tasks 1.3/1.4 enforces them on whole modified files; register the new helper and use explicit fork manifests. Extract a cohesive responsibility before exceeding caps. Each generated implementation task must fit a bounded 1-3 hour unit; no new size exception is proposed. Tests and generated fixtures are excluded from production caps.

## Verification and acceptance

A controller prerequisite freezes the remaining original runtime details before dispatch: actual default percent-axis precedence/crosshair, zero/missing fallback domain, legend reset/save behaviour and both miniature outcomes. Reuse retained original source and one bounded synthetic original observation only for these unresolved effects; no new capture harness. Record exact package hashes/source revision. If observation contradicts the numerical source contract or exposes another necessary visible deviation, stop that dependency and obtain the concrete decision before implementing it.

| Criteria | Focused evidence |
| --- | --- |
| 4.8, 4.9 | Independent unequal signed fixtures and native ECharts endpoints for both orientations, denominator membership, zero/missing and raw labels/tooltips; percentage axis and original controls/actions |
| 4.7, 4.8 | Column/bar/normalized transitions retain distinct ranges, exact chart types, options and unknown branches; fresh backend reopen restores the normalized view without storing derived values |
| 10.1, 10.2, 10.3 | One isolated actual Workspace journey checks drawn bars, legend hide/restore, raw tooltip, physical axis edit, navigator, full overview, themes, current export and reopen with strict CDP diagnostics |
| 10.4, 10.5, 10.6 | Bounded Sol lanes, independent Astra financial/integration review, combined size audit, scoped breadth mapping and per-task artifact sync/commits |

Add behaviour-named `cartesian.normalized.test.ts` beside existing mapper tests and focused legend cases to existing lifecycle/host tests. Reuse editor saved-leaf and caller tests for the new families. One new `tests/e2e/live-chart/normalized-bars.spec.ts` reuses existing fixtures/helpers. Verify renderer subscription cleanup, hidden-all series, legend toggling followed by theme/data/resize, current export, and independent overview. Reuse accepted save-failure/restart/aggregation evidence unless a changed owner creates a concrete regression risk. Publish a concise review and only necessary synthetic screenshots.

Disproof conditions: wrong denominator, sign loss, missing converted to financial zero, raw tooltip replaced by percentages, legend hides geometry without recalculation, overview shrinks with main legend selection, stale export, lost saved branches or an existing action hidden. Any prevents acceptance. Release-image and remaining UI-10 acceptance are not implied by these checks.

## Research basis and decisions

Current Workspace: c0d002ebbc72477f6c0445c48c049e77ee2fb8b5. Original Workspace: 38dffc33389aca0e4a87e0e88d42f7067aa220df. Local retained AG Grid Enterprise 34.1.1 BarChartProxy (main.cjs.js 45429-45490) sets normalizedTo=100 and rounded percentage axis labels. AG Charts Community 12.1.1 normaliseFnBuilder/normaliseFindExtent (29040-29089), accumulation (29201-29221), BarSeries processData (41379-41445), raw labels (41623-41637) and tooltips (41869-41880) establish the arithmetic and raw-data distinction. Enterprise 12.1.1 miniature construction (21943-21961) omits visible/direction; navigator (15525-15529) targets physical X. Source observations are not browser acceptance.

Synthesis: normalization and legend membership are one rendering concern with different lifecycle owners. Keep arithmetic pure and native transient state in the existing host; preserve raw application data and original persistence. Percentage-axis geometry cannot reuse financial-magnitude formatting wholesale. Existing APIs supply all dependencies; neither a new library nor a second chart state store is justified.
