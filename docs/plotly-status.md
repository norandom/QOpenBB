# Plotly: done and open

Plotly renders existing endpoint-driven chart widgets. It consumes chart data/layout/configuration or existing chart callbacks. It is retained alongside ECharts and Perspective; it is not the replacement editor for table-derived charts.

Checked items describe existing source functionality. They do not certify every provider endpoint or every Plotly chart type. Follow-up integration belongs to market-data-integrations and analyst-workspace; it does not block the accepted alpha.

## Done

- [x] Retain the existing chart widget and Plotly renderer.
- [x] Retain endpoint-data and chart-callback handling.
- [x] Retain lazy loading and the existing light/dark template hooks.
- [x] Retain existing chart resizing and export-data plumbing.

## Open

- [ ] Map the supported endpoint/chart catalog to provider coverage and record which widgets have live-data acceptance.
- [ ] Expand reusable parameterized widgets with readable instrument and series names.
- [ ] Apply consistent units, periods, provenance and missing-data presentation across providers.
- [ ] Align chart presentation with the shared analyst theme while preserving useful existing controls.
- [ ] Connect shared instrument/time selections across dashboard widgets.
- [ ] Verify parameter changes, refresh, saved state, export and failure handling for the selected widget catalog.

A Plotly-capable endpoint is not automatically a discoverable, parameterized dashboard widget. Provider adapters and widget metadata must supply that integration.

## Implementation references

The owned Workspace fork retains `terminalpro/src/components/Widgets/Chart.tsx`, `terminalpro/src/components/Charting/PlotlyChart.tsx` and its chart callbacks. The [source lock](../sources.lock.json) identifies the selected revision. The [provider map](provider-coverage.md) separates published provider coverage from installed and verified functionality.

[Renderer roles](../README.md#renderer-roles) · [ECharts](echarts-status.md) · [Perspective](perspective-status.md) · [Roadmap](roadmap.md)
