# Selected open-source dashboard baseline

Latest owner decision: Apache ECharts is the selected replacement chart engine, behind the existing OpenBB controls and saved-state contract. Perspective remains a candidate analytical engine and existing Plotly widgets remain in scope. The earlier native-explorer recommendation below is historical. Follow the [current discovery plan](../.kiro/specs/openbb-self-service/parity-plan.md); library selection does not establish functional or visual parity.

Current constraint, 2026-10-16: the owner requires a library substitution preserving OpenBB's UX, design, themes, features, controls and feature flags. The reduced-capability recommendation below is historical and no longer an acceptable delivery baseline. Perspective remains a candidate implementation dependency; equivalent behavior must be demonstrated before acceptance. In particular, unavailable legacy states and hidden Enterprise actions do not satisfy parity. See [requirements 4.8-4.9](../.kiro/specs/openbb-self-service/requirements.md) and [Workspace experience](../.kiro/steering/workspace-experience.md).

The owner selected **"Use Perspective baseline" on 2026-10-16**. Keep the Full Workspace dashboard shell and use Perspective as the primary analytical viewer for supported FMP/FRED datasets. Retain Community-compatible residual tables and complementary Plotly widgets; remove all AG Enterprise and Highcharts dependencies and initialization paths.

This is an approved integration direction, not completed implementation. Source assessment used Workspace revision `be00e95019a55d57af146919ee46b7e1a4859226`. No renderer changes, installation or runtime acceptance were performed by this assessment. The [design](../.kiro/specs/openbb-self-service/design.md) and [tasks 2.6-2.12](../.kiro/specs/openbb-self-service/tasks.md) define the amendment; independent review precedes renderer feature work.

## Why Perspective

Perspective supplies configurable grouping, pivots, aggregations and table-to-chart exploration. It preserves more analytical capability than the previously considered flat Community-grid/ready-Plotly route without recreating every Enterprise feature. Full Workspace continues to own accounts, dashboard composition, endpoint parameters, persistence and chat.

| Component | Selected role | Boundary |
| --- | --- | --- |
| Perspective, Apache-2.0 | Primary explorer for accepted profile/income and FRED datasets | Typed schema adapter, native exploration, versioned configuration and selected-view export |
| AG Grid Community, MIT | Residual supported flat tables | Ordinary sorting/filtering/formatting; no Enterprise calls or controls |
| Plotly.js, MIT | Complementary presentation widgets | Supported endpoint-bound charts, themes, zoom and image export |
| AG Charts Community, MIT | Only inventoried supported standalone widgets | Does not make AG Grid integrated charts free |
| AG Enterprise and Highcharts | Remove packages, imports, registrations and initialization keys | Unsupported imports receive explicit unavailable states |
| ECharts / TanStack Table | Not selected | No additional renderer or wholesale grid migration |

Official sources: [Perspective repository/license](https://github.com/perspective-dev/perspective), [AG Grid comparison](https://www.ag-grid.com/javascript-data-grid/community-vs-enterprise/), [AG Charts comparison](https://www.ag-grid.com/charts/javascript/community-vs-enterprise/), [Community Charts license](https://github.com/ag-grid/ag-charts/blob/latest/packages/ag-charts-community/LICENSE.txt) and [Plotly licensing](https://plotly.com/javascript/is-plotly-free/). Verify exact selected artifacts during implementation; current documentation is capability evidence.

The old FINOS URL redirects to the current project using `@perspective-dev/*`. Research found [stable 5.6.0, released October 14, 2026](https://github.com/perspective-dev/perspective/releases/tag/v5.6.0). This is not an unconditional pin: choose an exact compatible set that passes Safe Chain's package-age policy at installation. Verify React/Vite, worker and WASM assets through protected frozen installation and browser checks.

The [React binding](https://perspective-dev.github.io/react/index.html) wraps the custom-element viewer and exposes configuration/selection callbacks. QOpenBB still owns table/worker cleanup, same-origin WASM initialization, schema validation and persistence. No additional server/database is required. PostgreSQL, Jupyter, Perspective's own workspace shell and embedded AI remain outside scope.

## Preserve the financial workflow

| Contract | Acceptance behavior |
| --- | --- |
| Ready widgets | Discover profile/income and FRED explorers with useful defaults and supported parameters; no manual widget authoring |
| Financial meaning | Preserve nulls, dates, periods, currency, units, frequency and provenance; do not default to summing EPS, ratios, prices or incompatible series |
| Exploration | Group, pivot, filter and switch supported chart/table views; identify derived aggregates separately from provider observations |
| Saved state | Add/arrange/resize/remove, save, restart, reopen layout/parameters and validated viewer settings; saved configuration does not persist its dataset |
| Refresh | Replace fetched rows while retaining compatible settings; reject stale responses, visibly mark failed-refresh data and preserve settings on schema mismatch |
| Anthropic context | Export configured view or explicitly selected rows with filters/groups/aggregations, financial metadata and data revision; reject oversized/unavailable context |
| Exports | Verify configured-view CSV and supported chart-image output against visible data/labels |

Perspective has [Candlestick and OHLC plugins](https://github.com/perspective-dev/perspective/blob/v5.6.0/packages/viewer-charts/src/ts/plugin/charts.ts); Plotly also supports [candlesticks](https://plotly.com/javascript/candlestick-charts/). Neither supplies an OHLC dataset: the accepted provider scope remains FMP profile/income and FRED. New OHLC endpoints/widgets are deferred.

Use [table replacement/update](https://perspective-dev.github.io/browser/classes/dist_wasm_perspective-js.d.ts.Table.html) deliberately: complete endpoint responses replace rows; incremental updates require stable row keys. Persist versioned config in existing widget state and capture current data through the [viewer API](https://perspective-dev.github.io/viewer/classes/dist_wasm_perspective-viewer.d.ts.PerspectiveViewerElement.html) and [view serialization](https://perspective-dev.github.io/browser/classes/dist_wasm_perspective-js.d.ts.View.html). The existing Workspace agent protocol remains authoritative; Anthropic credentials stay server-side.

## Legacy boundary and source evidence

Installing Perspective alone does not remove commercial code. `terminalpro/src/components/General/Table/Chart/utils.tsx` registers Enterprise modules; `AgGrid.tsx` enables integrated charts and cell selection globally. Table context calls range-chart, chart-model and Enterprise export APIs. Audit lazy widgets, theme previews and type imports as well as entry points. A missing watermark is not removal evidence.

`hooks/useCreateChart.ts` stores `rowData`, `columnDefs` and `chartModel` in `ag_chart_from_table`; `AgChartFromTable.tsx` consumes that snapshot. This does not establish source-refresh compatibility. Preserve unsupported imports behind clear unavailable states rather than silently translating AG chart models into Perspective settings.

Legacy AG integrated-chart Customize panels, pivot/group states, tree/master-detail/SSRM widgets, Enterprise clipboard/range/XLSX actions and arbitrary Highcharts Stock/Maps/Gantt payloads are unsupported. Grouping and pivots remain available through Perspective. Dashboard composition remains available; compatibility with every imported commercial-renderer dashboard is not promised.

`Widgets/Chart.tsx` and `Charting/PlotlyChart.tsx` provide the existing endpoint-bound Plotly/theme seam. `hooks/useCopilotFilteredData.tsx` identifies a selected-widget registration seam; the Perspective adapter must provide equivalent financial context without Enterprise ranges.

The inspected sibling checkout was `d664ba94529a7a10151307ef65784a35809660b1`. Its `perspective/package.json` pins `@finos/*` 3.3.3; `src/app/history/adapters/perspective-runtime.ts` demonstrates owned initialization, replacement, save/restore and cleanup. Its validator restricts fields to its own history model, while shadow-DOM styles and patched d3fc OHLC code are version-specific. Reuse these lessons, not its Angular implementation, restricted schemas or old patches without revalidation.

## Delivery and disproof

The task amendment separates Community isolation, commercial removal, browser runtime, typed ready explorers, persisted refresh state, Workspace context export and the final image join. Data implementation can continue independently; installed-route catalog generation feeds renderer bindings, and final catalog verification waits for those bindings. Controller owns shared locks/catalogs and serializes the central builder.

Tasks 2.1-2.5 can establish a provisional local packaging image, but it cannot be published while commercial inputs remain. Task 2.12 supplies new image and absence evidence before dashboard integration. Full restart/reopen, live-provider fidelity and Anthropic grounding remain separate gates. Excel stays blocked until Anthropic acceptance.

Known oversized candidates include `AgGrid.tsx` (840 physical lines), `hooks/useTableContext.tsx` (796) and `ThemeSettings/ChartSettings.tsx` (1,185). Whole modified maintained files require cohesive extraction or narrowly reviewed measured exceptions. Preserve 400 physical lines/file, 300 logical units/file and 50/function using the foundation checker before feature acceptance.

Reject acceptance if ready-widget discovery, financial meaning, refresh, saved exploration or selected-widget chat context cannot work without removed modules. A clean build alone proves none of those user outcomes. Planned tests remain unverified until actual paths, commands, revisions and artifacts are recorded in breadth.
