# ECharts compatibility findings

Apache ECharts is the owner-selected replacement chart engine. Preserve OpenBB's existing interface and saved-state contract around it. The source assessment identifies a bounded rendering seam, but the original AG-supplied chart editor remains a separate compatibility problem. Library selection does not establish parity.

## Source boundary

Assessment uses owned Workspace `38dffc33389aca0e4a87e0e88d42f7067aa220df` as the original and `48e3f59cc48e0ae7aa6f6ce92069fc5b10ee3e86` as the removal checkpoint. Paths below are relative to `vendor/workspace/terminalpro/src/components/`. Independent source analysis was performed by `/root/echarts_contract`, GPT-6 Astra. These findings are source evidence, not integrated browser results.

| Boundary | Proposed responsibility |
| --- | --- |
| `General/Table/Chart/AgChartView.tsx::ChartViewElement` | Retain the chart container and resize wrapper around an ECharts host. |
| `General/Table/hooks/useTableContext.tsx::useUpdateChartView` | Translate chart creation, data/theme updates and disposal into bounded renderer operations. Preserve `createRangeChartParamsCbRef` for specialized callers. |
| `ChartViewButton` | Restore original pending-column-state flush, toggle, grouped-child series eligibility and exit behavior. |
| `General/Table/Chart/utils.tsx::getChartData` and `hooks/useCreateChartData.tsx` | Preserve existing transformations before translating data to ECharts series. Raw-row mapping alone does not cover this contract. |

Use ECharts public lifecycle APIs rather than emulating the entire AG Grid API. Its documented [sizing/lifecycle](https://echarts.apache.org/handbook/en/concepts/chart-size/) and [data-update](https://echarts.apache.org/handbook/en/how-to/data/dynamic-data/) seams support this proposed boundary; equivalent application behavior still needs testing.

## Preserve saved state

The adapter must retain original payloads and unknown fields. Persisting only an ECharts option object would lose application state.

- `useCreateChart` creates `ag_chart_from_table` widgets with `{...chartData, chartModel, chartView: {enabled: true}}` and existing dashboard/inner-tab placement.
- `useChartOptions::onChartOptionsChanged` merges the model and chart options under `storage[stateKey].chartModel`, stores chart type/pivot/series metadata and removes the merged options' `theme` field.
- `getStateKey` partitions state by period, transpose, selected group, reversed order, sheet name, selected ratio and pivot. Cell ranges may be stored per chart type or in the model.
- `AgChartFromTable` also accepts legacy top-level chart model/options/ranges and `transposedT` / `transposed_CellRange` forms.
- Aggregate function, combination-series types, series grouping and category/series switching remain part of the original contract, even when absent from the first fixture.

## Editor and action ownership

OpenBB owns the widget shell, chart toggle, settings action, navigator/mini-chart actions, distinct-color action, transpose action and global theme editor. AG supplies the docked chart-settings panel and its internal controls, chart-model events, range editing and chart toolbar.

The original `useChartToolPanelAction` calls `openChartToolPanel` / `closeChartToolPanel` and inspects AG DOM classes. `AgChartFromTable` also tracks the docked panel and close button. Restoring the outer settings button therefore does not restore its editor. A new settings form would require comparison against the original controls and outcomes; it is not automatically an acceptable replacement.

## Bounded runtime probe

An isolated ECharts 6.0.0 fixture exercises a hand-authored subset of the original detached-chart storage shape. It renders Q1/Q2 revenue 100/120 and EPS 1.2/1.4 as grouped columns, changes a title programmatically through the original-shaped options, refreshes Q2 revenue to 125, reloads an identical serialized widget payload and exports a populated PNG. Unknown nested fields are retained using a synthetic sentinel. The fixture preserves aggregate metadata but does not execute aggregation.

The initial runner passed with no page errors, CDP runtime exceptions or CDP network loading failures. Local evidence and exact commands are in `artifacts/parity/echarts-probe/report.md`; the runner is `run.mjs`, with screenshots, JSON observations, a pinned pnpm lock and export image beside it. ECharts bundle SHA256 is `77c1f65da9da7c5960e103e1884470645eff868e2a5d2ceca1ec732118aac8ae`. This is artifact-only discovery, not a maintained application regression.

No original mapper/component, settings editor, table selection or dashboard runtime is executed. The edit is programmatic and persistence uses localStorage, not the backend. Arbitrary settings remain preserved but are not all interpreted; theme fidelity, navigator, combination/stacked charts, transposition and open Highcharts inputs remain unverified. The experiment supports a narrow option-translation seam, not completion of the original table-to-chart journey.

Independent Astra review reran the fixture with exit 0 and approved this bounded synthetic claim. The reviewer inspected the exported image and confirmed that only the intended title and revenue fields changed in the complete saved payload. Numeric assertions inspect ECharts options; they are not pixel-value comparisons. CDP checks cover runtime exceptions and loading failures, not every console message or HTTP error status. Resize/dispose behavior is not tested. Review evidence is retained separately in `artifacts/parity/echarts-probe/review.md` and `review-evidence/`.

## Full application integration spike

A disposable archive of candidate `48e3f59cc48e0ae7aa6f6ce92069fc5b10ee3e86` restores the original `ChartViewButton` from reference `38dffc33389aca0e4a87e0e88d42f7067aa220df` and mounts ECharts in the original chart wrapper. Actual Workspace widget/table contexts supply the data and chart-view state. The spike uses the original backend image with a temporary frontend overlay and isolated account; it is not a release image.

Three compatibility changes were necessary:

1. Replace the internals of `ChartViewElement`, preserving the original button and resize wrapper.
2. Restore `AgGridTable`'s original chart-view state read, navbar visibility predicate and chart-container call site.
3. Remove the replacement-era `communityBoundary` rejection of enabled chart view. Other legacy-state guards remain; their behavior is not accepted parity.

The first two app attempts failed at the missing caller and then the rejection guard. After those scoped repairs, the actual app journey passed: real table -> original toggle -> visible grouped columns -> viewport resize -> toggle back -> real table. Instrumentation recorded width changing from 844 to 694 and chart disposal on return. The values are synthetic revenue 100/120 and EPS 1.2/1.4. Table checks use body-wide text presence; chart numbers are asserted in options and corroborated by a populated screenshot.

This probe reads flat rows directly rather than restoring original aggregation/selection/transpose transformations. Its hardcoded dark styling, chart options and diagnostics are disposable instrumentation. No editor, theme fidelity, data refresh, detached-chart creation, save/reopen, export or broad model compatibility is established. Dashboard routes are overlaid because the SQLite readback issue remains unresolved. The known upstream HTML-as-JavaScript error remains recorded; no clean-console claim is made.

Artifacts are in `artifacts/parity/echarts-integrated/`, including the source patches, build commands/results, manifests and journey. The temporary static directory retains unreferenced files from successive builds; this is not pristine release-build evidence. Private disposable account state must remain unpublished. See the [integration proposal](echarts-integration-proposal.md) and [original editor contract](echarts-editor-contract.md) for the remaining design work.

Independent Astra review reran the Full-app journey with exit 0, checked the populated canvas and verified the original navbar predicate and unchanged button. Its source audit found four tracked modifications (the three compatibility files plus the temporary script-loading entry point) and one added ECharts asset. The served minified ECharts bundle hashes to `baa8dfe7e1d9336b98e8986ba7e20ea15e7cdbea1ef42a59d59478632fa45a1d`; this differs from the earlier standalone unminified bundle. Only the positive external-widget visibility branch ran, so full flag-condition parity remains unverified. Review evidence is in `artifacts/parity/echarts-integrated-review/review.md`. Owned browsers and the disposable container were removed after review; production files and dependencies remain unchanged.

## Next evidence gates

1. The isolated grouped-column mapping, refresh, serialization/reload and image export probe has passed. Extend fixtures to the remaining saved-state forms before treating the codec as complete.
2. Use the integrated spike to inform a typed production host. Freeze the complete state codec and selection contracts, then restore the container and outer actions in an approved integration task.
3. Inventory and reproduce the original editor's controls and outcomes without hidden reductions.
4. Compare integrated light/dark appearance, selection, detached chart creation, actual backend save/reopen and export. Resolve the independent SQLite readback issue before claiming persistence.
5. Extend verification across the [capability matrix](../../../docs/renderer-capability-matrix.md), including combination, pivot, transpose, navigator and open Highcharts inputs.

Production implementation remains gated by the revised design and tasks. Apply 400 physical lines/file, 300 logical units/file and 50/function to maintained code. The existing candidate's missing controls remain recorded failures until integrated checks prove their restoration.
