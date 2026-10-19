# FINOS Perspective: done and open

Perspective is the analytical table and explorer foundation for grouping, pivoting, aggregation and interactive exploration. ECharts handles the existing editable table-chart journey; Perspective's dashboard adapter is still open.

Checked items describe shipped source foundations and isolated checks. They do not mean the explorer is already available as a dashboard widget. Remaining integration belongs to analyst-workspace and does not block the accepted alpha.

## Done

- [x] Include Perspective 5.6 packages for client, server, viewer, charts and datagrid.
- [x] Implement a React host and runtime initialization.
- [x] Implement lifecycle and resource-lease handling.
- [x] Add isolated host, lifecycle, lease and theme-race tests and a browser fixture.

## Open

- [ ] Register and connect the Perspective explorer as a production dashboard widget.
- [ ] Connect provider data through a financial schema preserving names, IDs, units, dates and missing values.
- [ ] Accept grouping, pivoting, filtering, sorting and financially valid aggregations in the real widget.
- [ ] Connect parameter changes and refresh without stale data or resource leaks.
- [ ] Save and restore viewer configuration through existing Workspace widget state.
- [ ] Match the shared theme and surrounding widget controls.
- [ ] Connect shared instrument/time context and exports.
- [ ] Accept the complete explorer journey in the assembled application.

Perspective does not automatically restore every former enterprise-table feature. Formulas, statistics, specialized/remote tables, selection and export obligations still need explicit implementation ownership and acceptance. Local unfinished financial-adapter work is not counted as done here.

## Implementation references

The owned Workspace fork contains `terminalpro/src/components/Widgets/perspective/` and its `terminalpro/tests/perspective/` browser fixture, plus `terminalpro/tests/unit/perspective*.test.*` checks. The [source lock](../sources.lock.json) identifies the selected fork revision. See the [UI worklist](../.kiro/specs/openbb-self-service/ui-parity-worklist.md) for outstanding advanced-table obligations.

[Renderer roles](../README.md#renderer-roles) · [ECharts](echarts-status.md) · [Plotly](plotly-status.md) · [Roadmap](roadmap.md)
