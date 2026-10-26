# Original stacked Line source assessment

2026-10-26. Preserve `stackedLine` and `normalizedLine` as distinct model types. The locked original renderer stacks signed values algebraically in selected series order. Its 100% variant scales cumulative values by the largest absolute cumulative excursion within each category. It does not calculate a conventional share of gross absolute contributions. These are verified source findings; this assessment did not activate either variant in a browser.

## Source identity

- Original Workspace: `vendor/workspace` Git revision `38dffc33389aca0e4a87e0e88d42f7067aa220df`. Paths below prefixed `terminalpro/` refer to that revision, inspected with `git show`/`git grep`, not the modified checkout (currently `0b2190354d2dc5f4175ffb989cf652ac36237c77`). Its `terminalpro/package.json` pins AG Grid Enterprise 34.1.1 and AG Charts Community/Enterprise 12.1.1.
- Locked dependency source was read from WSL Debian, `/home/mc/.bun/install/cache/ag-grid-enterprise@34.1.1@@@1/dist/package/main.esm.mjs` (below, **Grid**), SHA-256 `76831274e5f22060913871da1e756d5269e71b87ea9a601ecac05baca4504286`.
- `/home/mc/.bun/install/cache/ag-charts-community@12.1.1@@@1/dist/package/main.esm.mjs` (below, **Charts**), SHA-256 `e9b1b8be8d27ffc1f2c66e715b863b36d5f3aecef0c79e18cc0101a440956df4`. Both hashes were freshly computed with `sha256sum`.
- Retained original DOM inventory: `artifacts/reviewed/ui-parity-family-navigation-plan/plan.md`, exact inventory table. It establishes Line, Stacked Line and 100% Stacked Line thumbnails, not successful activation. `artifacts/reviewed/chart-funnel/next-family-inventory.md` correctly leaves behavior unverified.

## Transformation contract verified in source

| Concern | Source result | Exact source |
| --- | --- | --- |
| Admission | `lineGroup` contains `line`, `stackedLine`, `normalizedLine`; all allow range and pivot and do not require enterprise chart modules. | Grid:52235-52238, 52285 |
| Series | First selected category supplies `xKey`; selected value fields become ordered line series. Both variants set `stacked: true`; only normalized Line sets `normalizedTo: 100`. | Grid:46156-46194; controller selected field/category construction at 45672-45694 |
| Signed stack | Cumulative sums follow ordered series, without separate positive/negative stacks. Stacking groups rows by x keys. | Charts:44120-44200; 29172-29178; 29390-29447 |
| Normalization | For each category group, inspect the cumulative start/end/marker groups. Set D to `max(abs(minimum negative cumulative), maximum positive cumulative)`; scale each cumulative value as `100 * cumulative / D`, clamped to [-100,100]. This is a category denominator, not a total across dates. | Charts:29229-29285; 44150-44185 |
| Zero | If D=0, normalization returns null for numeric cumulative values. A raw zero with D>0 remains a valid raw value and lies at its cumulative position. The actual all-zero painted path/tooltip must be characterized in runtime. | Charts:29230-29261, 44285-44341 |
| Missing/invalid | Raw invalid y becomes undefined. Stacked common invalid value is null, or zero when `connectMissingData` is enabled; hidden stacked series force zero. Accumulation skips nonfinite inputs. Missing raw points are omitted, and line spans break unless `connectMissingData` is true (default false). Do not convert all missing observations into visible zero points. | Charts:44030; 44120-44149; 29390-29446; 44285-44341 |
| Displayed values | Node coordinates use cumulative y; datum `yValue`, label input and default tooltip y use the raw series value. Normalized y-axis tick labels append `%`; raw tooltip data does not become a percentage through this calculation. Workspace formatting overrides may alter displayed strings. | Charts:44265-44341, 44477-44522; Grid:46156-46171 |
| Visibility | Hidden stacked series contribute forced zero to processing. Recomputed stack and normalized denominator therefore depend on visible series. Actual legend interactions need runtime confirmation. | Charts:44120-44138 |
| Cross-filter caveat | Normalization is disabled when crossFiltering is active, even for normalizedLine. | Grid:46191-46194 |

For finite selected values in order `[60,-80,20]`, the source arithmetic gives cumulative `[60,-20,0]`, D=60 and normalized positions `[100,-33.333...,0]`. For `[60,-20,60]`, cumulative `[60,40,100]`, D=100 and positions `[60,40,100]`. These are arithmetic deductions from the algorithm, not executed renderer observations. Reordering signed series can change D and percentage positions even when the final sum is unchanged. Financial captions must describe cumulative contribution and denominator explicitly; calling these individual shares would be misleading.

## Selection, storage and controls

Grid:45672-45722 builds ordered selected fields and dimensions; switching category/series transposes the data, creating a series for each former category and categories from former field labels. Grid:45723-45765 saves `modelType`, `chartId`, exact `chartType`, `chartThemeName`, `chartOptions`, `chartPalette`, `cellRange`, `switchCategorySeries`, `suppressChartRanges`, `aggFunc`, `unlinkChart`, `seriesChartTypes` and `seriesGroupType`. Changing type resets transpose/category-axis/group-type internally; Workspace subsequently reapplies retained range and switch state in `terminalpro/src/components/General/Table/Chart/hooks/useChartOptions.tsx:438-490`. Save/reopen equivalence remains a browser obligation.

Workspace stores the returned chart model and merged chart options under its range/pivot storage key, with top-level chartType/totalSeries/isPivotMode (`useChartOptions.tsx:438-490`). `terminalpro/src/components/General/Table/Chart/AgChartView.tsx:34` restores transpose from chartData or chartModel. The independent AgChartFromTable route has its own storage shape (`terminalpro/src/components/General/Table/AgChartFromTable.tsx:298-326`); it must not be assumed accepted by a Table-only check.

Both types map to the line format family (Grid:41357 and Workspace `terminalpro/src/lib/constants.ts:1270-1271`). The native line series format panel offers tooltips, line width, dash, opacity, markers and labels (Grid:49613-49620). Shared data/category selection, axis, legend, title and navigator controls require characterization in the actual Workspace host; the presence of dependency controls alone does not prove host availability or persistence. Workspace defaults preserve line options including connectMissingData (`useChartOptions.tsx:41-61`). No separate normalization-denominator user control was found in the bounded proxy inspection.

## Next bounded characterization

Use the original isolated runtime to compare both tokens on ordered positive, mixed-sign, all-negative, zero-only and missing rows. Inspect plotted positions and raw tooltip/label values, reorder/toggle series, change selected categories and transpose, then save/reopen. Record the actual model and exact control availability alongside screenshots. Verify ordinary Line transitions retain the appropriate range/options without silently retaining stacking or converting tokens to `line`. Until that evidence exists, gallery visibility and these source contracts do not establish runtime parity.

This task changed only this assessment. No production code or browser checks ran. Production complexity caps (400 physical lines/file, 300 logical units/file, 50/function) remain mandatory for future implementation; documentation is exempt.
