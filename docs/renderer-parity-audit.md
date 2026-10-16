# Renderer parity gaps

The current renderer changes do not meet the owner's functional and visual parity requirement. Restore equivalent behavior before accepting the replacement. Perspective's isolated rendering tests do not demonstrate that it replaces the existing OpenBB feature surface.

This preliminary source audit compares owned Workspace `38dffc33389aca0e4a87e0e88d42f7067aa220df`, before renderer isolation, with `48e3f59cc48e0ae7aa6f6ce92069fc5b10ee3e86` and the current working tree on 2026-10-16. A Sol source auditor inspected the removal boundaries; a separate Luna auditor checked specification conflicts. No browser or runtime parity verification ran for this audit.

## Source-confirmed gaps

Paths below are relative to `vendor/workspace/terminalpro/src/components`. Deleted files and original behavior refer to the baseline revision.

| Capability | Source boundary | Gap requiring equivalent behavior |
| --- | --- | --- |
| Table/chart switching | `General/Table/Chart/AgChartView.tsx` | `ChartViewButton` returns null; chart view is unavailable. Preserve switching, transformations, saved range/type and table restoration. |
| Chart options | `General/Table/Chart/hooks/useChartOptions.tsx` | Hooks return empty actions/options. Restore settings, distinct bar colors, navigator and mini-chart, including their defaults and mutual exclusion. |
| Cell and row selection | `General/Table/AgGrid.tsx` | Cell selection and original header/double-click gestures were removed or simplified. Preserve selected ranges and downstream actions. |
| Column menu | `General/Table/AgGrid.tsx` | Menu returns an empty list. Restore default items, Hide Column, conditional Minimize Column and Reset Columns with group state. |
| Context menu and AI context | `General/Table/AgGridUtils.tsx` | Restore autosizing, expand/collapse, copy, copy with headers, charts, exports and selected-cell Copilot context with original tier and Copilot conditions. |
| Range-to-chart creation | `General/Table/AgGridUtils.tsx`, deleted `hooks/useCreateChart.ts` | Restore grouped/stacked columns and bars, line, scatter, bubble, pie, doughnut, stacked area, histogram and column-line combination, including series/cell limits and chart-to-widget flow. |
| XLSX export | `General/Table/hooks/useTableContext.tsx`, `hooks/communityActions.ts` | Current actions expose CSV only. Restore XLSX behavior and original caller conditions. |
| Advanced table analysis | `General/Table/SubMenus/TableSettings.tsx`, `hooks/useTableContext.tsx`, deleted `SubMenus/FormulasToolPanel.tsx` | Restore advanced/stats/formulas toggles, columns, grouping, pivot, aggregation, statistics and formulas with original restrictions. |
| Specialized widget types | `Widgets/index.ts` | Registry routes AgChartFromTable, AgGridSQL, AgGridSSRM, AgGridSSRMAdvanced, CountryIndicators, EconomicIndicators, AnalystEstimates and ChartHighcharts to unavailable views. |
| Standalone and AI chart types | `Widgets/AgChart.tsx`, `Widgets/communityCharts.ts`, `AI/Artifact.tsx` | Eight-type allowlist rejects other configurations. Original paths include treemap, sunburst, heatmap, waterfall and radar/radial/nightingale families. Complete accepted schema enumeration remains pending. |
| Highcharts authoring/import | `DataConnectors/WidgetsBuilder/consts.ts`, `JSONConfiguration.tsx`, `Widgets/communityWidgetSchema.ts` | Builder choice and schema autocomplete were removed. Rendering alone will not restore the authoring flow. |
| Chart themes | `General/Table/Chart/themes.tsx`, `ThemeSettings/ChartSettings.tsx` | Restore zoom/navigator theme behavior and company background-image editing/rendering. Dormant saved metadata is insufficient. |
| Sparklines and saved table state | `General/Table/communityBoundary.ts` and state hooks | Sparkline columns are hidden; grouping, hierarchy, advanced filters, formulas and chart state may make saved widgets unavailable. Restore rendering and save/reopen behavior. |

The Community options boundary additionally removes clipboard processors, Excel styles/export parameters, status/sidebar configuration, aggregate functions, chart callbacks, hierarchy options and grouping panel settings. Its recursive saved-state check can make an otherwise supported widget entirely unavailable. These are functional changes, not dependency-only edits.

## Next design gate

The follow-up [capability matrix](renderer-capability-matrix.md) enumerates the owned chart schema and control contracts. The [verification contract](../.kiro/specs/openbb-self-service/parity-verification.md) defines paired reference/candidate evidence. Both remain source/planning work; runtime parity is unverified.

1. Complete a source-derived capability matrix: original control/action, visibility and flag conditions, saved-state contract, replacement implementation and executable check. Include conditional paths; do not infer coverage from visible default screens.
2. Assess how replacement libraries can serve the existing controls and chart appearance. Native Perspective UI is not the approved user interface. Do not promise that one library can satisfy every existing contract until demonstrated.
3. Split remediation into bounded implementation tasks with explicit ownership and the existing 400 physical lines/file, 300 logical units/file and 50/function caps. Preserve historical acceptance records while replacing obsolete completion criteria.
4. Require independent functional review and integrated light/dark comparison. Source absence of commercial packages, a visible button or an isolated chart canvas cannot establish parity.

Renderer implementation remains paused pending this design reconciliation. No runtime changes or automatic restoration of commercial dependencies were made by this audit. Full chart-schema enumeration, exhaustive theme-property comparison and original flag reachability remain open audit work.

See [requirements 4.8-4.9](../.kiro/specs/openbb-self-service/requirements.md), [Workspace experience policy](../.kiro/steering/workspace-experience.md) and the [historical replacement assessment](chart-replacement-assessment.md).
