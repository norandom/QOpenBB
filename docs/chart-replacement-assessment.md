# Open-source dashboard baseline

Use the Full Workspace dashboard shell with AG Grid Community tables and its existing Plotly chart renderer. This is the smallest identified route to ready FMP/FRED widgets without commercial chart dependencies. It preserves dashboard composition; it does not reproduce every Enterprise table or chart-editing feature.

Status: assessed on 2026-10-16 against Workspace revision `be00e95019a55d57af146919ee46b7e1a4859226`. No replacement has been implemented or runtime-verified. The owner requested this assessment; the proposed capability changes need a decision before renderer or lock changes.

## Compare the choices

| Component | Recommendation | Consequence |
| --- | --- | --- |
| AG Grid Community, MIT | Retain for flat financial tables | Preserve ordinary sorting, filtering, formatting and virtualization; remove Enterprise controls |
| Plotly.js, MIT | Reuse for ready FMP/FRED charts | Preserve endpoint-bound charts, themes, zoom and image export; no new arbitrary chart builder |
| AG Charts Community, MIT | Retain only where required supported widgets use it | Basic standalone charts are possible; AG Grid integrated charts are still commercial |
| Apache ECharts, Apache-2.0 | Defer | Capable renderer, but adds adapters and another dependency without shortening this baseline |
| TanStack Table, MIT | Defer | Replaces grid APIs and UI responsibilities already handled by AG Grid |
| Highcharts and AG Enterprise packages | Remove from the proposed baseline | Unsupported imported configurations must produce an explicit unavailable state |

Official sources: [AG Grid comparison](https://www.ag-grid.com/javascript-data-grid/community-vs-enterprise/), [AG Charts comparison](https://www.ag-grid.com/charts/javascript/community-vs-enterprise/), [AG Charts license](https://github.com/ag-grid/ag-charts/blob/latest/packages/ag-charts-community/LICENSE.txt), [Plotly licensing](https://plotly.com/javascript/is-plotly-free/), [ECharts features](https://echarts.apache.org/en/feature.html), [ECharts license](https://github.com/apache/echarts/blob/master/LICENSE), [TanStack architecture](https://tanstack.com/table/v8/docs/introduction) and [license](https://github.com/TanStack/table/blob/main/LICENSE). Current product documentation may differ from the pinned versions; verify exact retained artifacts during implementation.

## Preserve the financial workflow

The proposed baseline supports ready profile/income tables and FRED series widgets from the accepted API catalog. Ready Plotly charts bind their endpoint, query parameters and refresh behavior to those datasets. Users can add, arrange, resize, remove, save, reopen and refresh dashboard widgets.

Ordinary table filters, sorting and financial formatting remain in scope. CSV and image downloads are explicit acceptance targets. Selected-widget data, financial units, periods and provider metadata remain available to the later Anthropic integration.

Plotly supports [candlesticks](https://plotly.com/javascript/candlestick-charts/), [range controls](https://plotly.com/javascript/range-slider/) and [editing/export options](https://plotly.com/javascript/configuration-options/). Candlestick widgets are deferred: the current accepted provider scope is FMP profile/income and FRED, so OHLC data needs its own endpoint and financial-contract acceptance. Renderer support alone is insufficient.

Initially unavailable:

- Integrated range-chart generation and its Customize panels.
- Pivot, grouping, tree, master-detail and server-side row-model connectors.
- Enterprise advanced/set/multi filters, sidebars, status bars and context-menu actions.
- Enterprise cell-range clipboard/selection and XLSX export.
- Arbitrary Highcharts Stock, Maps and Gantt configurations.

Unsupported controls must be hidden, and imported unsupported widgets must explain their unavailable capability. Existing dashboard composition remains available. The baseline does not promise compatibility with every dashboard exported by the commercial renderer.

## Why this needs implementation work

The acquired frontend registers Enterprise modules in `terminalpro/src/components/General/Table/Chart/utils.tsx` and enables integrated charts/cell selection in `AgGrid.tsx`. Table context actions call `createRangeChart`, chart-model and Enterprise export APIs. Removing a license-key assignment alone would leave these dependencies and calls intact.

`hooks/useCreateChart.ts` saves an `ag_chart_from_table` widget containing `rowData`, `columnDefs` and `chartModel`. `AgChartFromTable.tsx` reads that saved data. This establishes a snapshot path, not proof that generated charts refresh from their original widget. Replacement tests must distinguish refreshable endpoint bindings from saved snapshots.

`Widgets/Chart.tsx` already queries an endpoint with saved parameters and uses Plotly image download. `terminalpro/src/components/Charting/PlotlyChart.tsx` supplies theme handling. Reusing this path avoids a second renderer. Highcharts-specific `userOptions` cannot be passed to Plotly unchanged.

Cell-range context actions use Enterprise APIs. Selected-widget and filtered-visible-data handling have separable paths, including `hooks/useCopilotFilteredData.tsx`; preserve those contracts for Anthropic without promising cell-range parity.

## Amend implementation before changing renderers

1. Freeze supported ready widgets, chart/table types, settings, exports and unsupported-import behavior.
2. Isolate the Community grid configuration and actions, preserving financial formatting and saved column/filter state.
3. Remove commercial registration, dependencies and renderer paths; inspect the resulting module graph, bundle and notices.
4. Supply endpoint-bound ready Plotly widgets for the accepted FMP/FRED datasets.
5. Verify displayed financial values, layout/parameter persistence across restart, refresh changes, failure recovery and selected-widget data. Revalidate the later Anthropic journey against this contract.

Tasks 2.1-2.5 currently cover packaging, startup, authentication and routing. The grid/renderer work needs an explicit design/task amendment and dashboard acceptance updates. Foundation work can continue independently.

Several upstream files exceed the production size cap, including `AgGrid.tsx` (840 physical lines), `useTableContext.tsx` (796) and `ChartSettings.tsx` (1,185). Cohesive extraction or a narrowly reviewed measured exception is required before changes. Preserve the 400 physical lines/file, 300 logical units/file and 50/function limits.

Reject this proposal if it cannot preserve ready-widget discovery, accurate financial data, refresh, dashboard persistence or selected-widget chat context without the removed modules. A successful static build alone does not establish those behaviors.
