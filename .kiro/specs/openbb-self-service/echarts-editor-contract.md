# Original chart editor contract

ECharts is the selected rendering engine; compatibility remains to be demonstrated. The original docked editor needs an OpenBB-owned compatibility implementation. Reuse existing controls and preserve the original settings and effects. This source inventory defines the next browser-capture scope; it is not a completed field-by-field runtime inventory.

## Evidence

Independent source inventory: `/root/echarts_editor_inventory`, GPT-6 Astra. Owned Workspace reference: `38dffc33389aca0e4a87e0e88d42f7067aa220df`. Public editor declarations were inspected in installed AG Grid Community 34.1.1, matching the original pin, at `dist/types/src/interfaces/iChartOptions.d.ts`. Community declarations describe interfaces; they do not supply the Enterprise editor implementation.

Paths below are relative to `terminalpro/src/` in the owned Workspace fork. No browser, build or installation was part of this source inventory.

## Panels and chart groups

| Surface | Public tokens |
| --- | --- |
| Panels | `settings`, `data`, `format` |
| Data groups | `categories`, `series`, `seriesChartType`, `chartSpecific` |
| Format groups | `chart`, `titles`, `legend`, `axis`, `horizontalAxis`, `verticalAxis`, `series` |
| Column group | `column`, `stackedColumn`, `normalizedColumn` |
| Bar group | `bar`, `stackedBar`, `normalizedBar` |
| Pie group | `pie`, `donut`, `doughnut` |
| Line group | `line`, `stackedLine`, `normalizedLine` |
| Area group | `area`, `stackedArea`, `normalizedArea` |
| Scatter group | `scatter`, `bubble` |
| Combination group | `columnLineCombo`, `areaColumnCombo`, `customCombo` |
| Polar group | `radarLine`, `radarArea`, `nightingale`, `radialColumn`, `radialBar` |
| Statistical group | `boxPlot`, `histogram`, `rangeBar`, `rangeArea` |
| Hierarchical group | `treemap`, `sunburst` |
| Specialized group | `heatmap`, `waterfall` |
| Funnel group | `funnel`, `coneFunnel`, `pyramid` |

Group keys append `Group` to the group name, with `combinationGroup`, `statisticalGroup`, `hierarchicalGroup` and `specializedGroup` as declared. These editor-group tokens are not automatically identical to saved chart-model types such as `groupedColumn`; the adapter must map the actual namespaces explicitly.

The public declarations describe all panels/groups as included when their lists are omitted, groups as initially closed, and the tool panel as initially hidden when no default panel is supplied. No owned `chartToolPanelsDef`, `chartGroupsDef`, `formatPanel` or `dataPanel` override was found. These defaults do not prove the rendered field list, ordering or family-specific conditions.

## Preserve intentional suppression

- `components/General/Table/AgGrid.tsx::setGlobalGridOptions` and `AgChartFromTable.tsx` both return an empty list from `getChartToolbarItems`. Do not add an ECharts toolbox or expose every AG toolbar enum.
- `index.css` hides the AG save icon. Existing external widget-menu exports remain separate and must work.
- `Chart/AgChartView.tsx::createRangeChart` sets `suppressChartRanges: true`, defaults to `groupedColumn`, and forwards aggregation, series types/grouping and category/series switching.
- `Chart/hooks/useChartOptions.tsx::useChartToolPanelAction` owns the external Chart settings action and persists `chartSettingsOpen`. The detached chart's settings action is hidden in forecast mode by the original `hide: isForecast` predicate.
- The docked close control is a right-chevron, black in light mode and white in dark mode. The integrated hook clears persisted `chartSettingsOpen` on close; detached chart actions do not update that field in the inspected source. Capture and preserve each path's behavior separately.
- Navigator and mini-chart default to false and are mutually exclusive. Distinct colors default to false, apply to bar-mapped chart views and are disabled with more than one series.

Original visibility and enabled-state conditions must be preserved in both directions. An existing suppression is part of parity; a new suppression to avoid implementing behavior is not.

## Theme ownership

`Chart/themes.tsx` selects the active light/dark theme, including OpenBB/custom variants and backgrounds `#FFFFFF` / `#151518`. Defaults include a top legend, maximum legend height 50, spacing 20, square markers of size 11, legend font size 11 and title font size 12. Zoom uses pointer anchors, a four-item minimum and auto-scaling. Lines default to no markers and connected missing data. Waterfall/funnel labels default off. Numeric axis and pie formatting have distinct rules.

Keep three palette sources distinct: AG's base palette, the 15-color `defaultFills` used for distinct categories, and the ten-fill/stroke defaults in the global light/dark chart-theme editor.

`ThemeSettings/ChartSettings.tsx::ChartThemeState` includes palettes, typography, foreground/background/accent/border colors, padding, chrome/input colors, axis/grid/crosshair-label colors and background image. Preserve edit, preview, save and reset in both modes. Background-image defaults are disabled, empty URL, 50 by 50, right/bottom offsets 10, opacity 1; positions are `nw`, `ne`, `sw`, `se`, `center`.

`index.css` additionally specifies tooltip title weight 550, radius 3px and dark content background `#1f1e23` with white text. Matching only chart background is insufficient.

## Reuse and remaining capture

Reuse OpenBB's `ds/atoms/Input`, `Select`, `FontFamilyInput`, `SpacingInput`, `Switch`, `Checkbox`, and `ds/molecules/ColorPicker`, `Tabs`, with existing accordion/slider primitives where appropriate. ColorPicker already uses react-colorful; Select/Tabs wrap Radix. Reuse reduces control infrastructure but does not establish AG-panel appearance or interaction equivalence.

Use small family-specific field modules and narrow legacy-model patches. Keep ECharts private DOM and commercial editor implementation out of the adapter. Before final design approval, capture actual fields, labels, defaults, visibility, keyboard behavior and resulting payload changes across the three panels and chart families. Include combination secondary axes, pivot/transpose, linked/detached/forecast paths and light/dark state. The [capability matrix](../../../docs/renderer-capability-matrix.md) remains the acceptance inventory; these source enums cannot close its runtime gaps.
