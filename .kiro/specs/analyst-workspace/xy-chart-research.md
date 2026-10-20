# Next chart slice: scatter and bubble

Restore scatter and bubble together in the ordinary Table/File journey. They share the original field-pairing contract and editor controls, making them a bounded successor to the [accepted combination milestone](chart-port-milestone.md). Standalone and AI callers remain separate work.

This is source research dated 2026-10-20, not implementation or runtime acceptance. No provider request, build, installation or browser verification was performed for this research. The next action is to characterize the open edge cases below and freeze the mapper/editor contract before implementation.

## Current gap and reuse

The gallery already lists both types, but `application/comboSessionTypes.ts::ApplicationChartFamily` admits only Cartesian and combination families. The setup panel lacks Paired Mode and X/Y/size annotations. Current caller defaults generate bar/line branches; numeric X coordinates, point tooltips and scatter/bubble appearance need explicit mapping.

Paths below are relative to `vendor/workspace/terminalpro/src/components/General/Table/Chart/`. Reuse `compatibility/snapshotTypes.ts`, which retains selected numeric columns and category labels, together with option-state hydration, application capture/stamps and the existing widget transaction owner. Reuse the ECharts host, layout/theme/grid helpers and File refresh lifecycle. Numeric coordinates must replace categorical row-index assumptions. Existing navigator cloning is a candidate for reuse, subject to numeric-X and bubble-size checks.

## Original behavior to preserve

Owned source reference: Workspace `38dffc33389aca0e4a87e0e88d42f7067aa220df`. Retained library reference: AG Grid Enterprise 34.1.1, `artifacts/task-2.1/frontend/terminalpro/node_modules/ag-grid-enterprise/dist/ag-grid-enterprise.js`. Line references below identify that retained bundle.

| Contract | Source |
| --- | --- |
| Numeric bottom X and left Y axes for both families. | `ScatterChartProxy.getAxes`, 8382-8395 |
| Paired Mode defaults true; saved overrides are `chartOptions.scatter.paired` and `chartOptions.bubble.paired`. | `ChartProxy.setPaired/isPaired`, 8647-8657 |
| Paired scatter consumes successive `(X,Y)` pairs. Unpaired scatter shares the first numeric column as X across all following Y columns. | `getSeriesDefinitions`, 8498-8539 |
| Paired bubble consumes successive `(X,Y,size)` triples. Unpaired bubble shares the first X, followed by `(Y,size)` pairs. Incomplete trailing groups are omitted; fewer than two numeric fields yields no series. | Same |
| Series title is `Y display name vs X display name`. A selected category supplies point labels; otherwise Y supplies labels. Bubble size name comes from its selected size column. | `getSeries`, 8396-8430 |
| Setup uses Labels and XY Values headings, a Paired Mode toggle, and selected-column annotations `(X)`, `(Y)`, `(size)` derived from order and pairing. | 11842-11858, 12278-12331 |
| Scatter Customize exposes tooltips, shape, size, stroke width and labels. Bubble exposes tooltips, shape, min size, max size, stroke width and labels. | `SeriesPanel`, 13958-13970; size setters 14139-14144 |

The retained `ag-charts-enterprise/dist/umd/ag-charts-enterprise.js` uses a linear bubble size scale (44186-44213), maps its range to `[size,maxSize]` (44351), and supplies defaults 7 and 30 (44720-44721). Do not substitute area-proportional sizing without evidence.

Owned `Chart/utils.tsx::createDefaultSeries` formats scatter tooltips with X/Y and bubble tooltips with X/Y/size through `getLgToSm`. Baseline `Chart/hooks/useChartOptions.tsx` enables scatter default axis titles when the selected range has at most five columns, unless an orientation already supplies custom title text.

## Characterization still required

- Confirm missing, zero, negative and equal bubble-size behavior, including scale-domain and fallback rules.
- Establish exact marker-shape equivalence and effective defaults in both themes.
- Trace aggregation and Switch Category / Series reachability for XY charts; do not remove controls by inference.
- Establish numeric-X navigator, mini-chart, zoom and reset behavior.
- Confirm how insufficient numeric selections appear in the original editor and chart, without replacing them with invented points.

These questions prevent treating the source inventory as an implementation-ready contract. The proposed reuse fails if it changes original field assignment, stored options, reachable controls or numerical observations.

## Real FMP acceptance

Reuse the captured AAPL annual income statements in ignored `artifacts/chart-combo/fmp/`; no new provider request is needed. Proposed X is revenue in original USD amounts, Y is net income in original USD amounts, and bubble size is EPS in USD/share. Fiscal period labels retain the original fiscal-year/date association. Marker size represents EPS, not market capitalization or a third USD total.

Retain raw observations without rescaling. Axis and tooltip magnitude formatting is presentation only. Reuse the provenance/hash and CSV-consumption checks from `terminalpro/tests/e2e/live-chart/combo-fmp.spec.ts`, but replace its categorical hover-coordinate assumptions. The captured five observations support one scatter pair and one bubble triple; synthetic fixtures must cover multiple groups, unpaired mode, incomplete groups, duplicate labels and missing/negative/equal values.

Acceptance requires plotted coordinates and sizes, displayed values and units, applicable controls, both themes, refresh, save/reopen and export in the application. Engine-only evidence does not establish this journey.

## Bounded next task order

1. Freeze XY assignment/options and edge-case behavior. Own new `compatibility/xyAssignments.ts`, its focused tests and the bounded design record; keep it inactive. The controller owns shared interface edits.
2. Implement an inactive mapper in new `echarts/xy*.ts` and focused mapper/render tests: numeric coordinates, size mapping, axes, labels and tooltips.
3. Implement session/editor behavior in new `application/xy*.ts`, `editor/xy/*` and focused transaction/control tests. Keep the existing session as sole state owner. This lane may overlap task 2 only after interfaces are frozen and writable paths are disjoint.
4. Join production routing, caller defaults, setup/customize controls and navigator behavior under controller ownership. Preserve unknown/inactive options and stale-command protection.
5. Independently review and verify the captured-FMP application journey plus prior-family regressions. Update breadth, inventory and evidence; commit bounded accepted work and dispatch one completed-milestone image release.

Every production handoff requires whole-file caps of 400 physical lines, 300 logical units and 50 units per function, using the existing [complexity gate](../../../docs/complexity.md) with actual explicit fork scope. Extend the existing inventory; foundation enforcement already exists. Tests and this research document are outside production caps. Follow [delegation policy](../../steering/delegation.md): exclusive ownership, independent review, serialized heavy verification and selective commits. Unrelated Perspective work is outside this slice.
