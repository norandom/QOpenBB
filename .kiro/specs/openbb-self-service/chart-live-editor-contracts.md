# Bind every accepted panel field to its original write

Task 2.69 defines finite contracts beneath `vendor/workspace/terminalpro/src/components/General/Table/Chart/`. These declarations do not establish live rendering or persistence acceptance. See [integration design](chart-live-editor-integration-design.md).

`F` is `bar` for groupedColumn/stackedColumn and `line` for line. `A` is the actual original axis option type (category/number/time/grouped-category). `P` below means BOTH original positions for the resolved direction: x writes bottom then top; y writes left then right. It does not mean just the current position. `AxisBinding` carries actual direction and type, resolved from current concrete axes. Ordinary initial horizontal/vertical bindings are category/x and number/y. Theme style writes use both `F.axes.A.P` branches. Source override reads return the first defined value in bottom/top or left/right order, including wildcard object reads; they do not merge both positions. Effective inherited unpositioned styles remain available through original theme composition. Accepted panels expose neither footnote nor axis range; neither is added here.

| Panel fields | Original leaf beneath F unless stated | Renderer effect |
| --- | --- | --- |
| title/subtitle enabled,text,font,weight,color,size,spacing | title/subtitle.enabled,text,fontFamily,(fontWeight + fontStyle),color,fontSize,spacing | visible retained text, typography and spacing |
| horizontal/vertical title same fields | axes.A.P.title with same leaf conversion | category/number axis name and typography |
| legend enabled,font,weight,color,position,size,spacing | legend.enabled; item.label.fontFamily,(fontWeight + fontStyle),color; legend.position; item.label.fontSize; legend.spacing | visibility, text, placement and chart gap |
| legend markerSize,markerStroke,itemSpacing,horizontalSpacing,verticalSpacing | legend.item.marker.size,strokeWidth,padding; legend.item.paddingX,paddingY | marker geometry and inter-item layout |
| padding top,right,bottom,left | padding.<side> | four plot margins |
| background visible,fill | background.visible,fill | visibility/transparent fill |
| tooltips enabled,mode | tooltip.enabled,mode | pointer behavior and content grouping |
| series strokeWidth,lineDash,strokeOpacity,fillOpacity | series.strokeWidth,lineDash=[value],strokeOpacity,fillOpacity | stroke width/dashes/alpha and fill alpha |
| shadow enabled,color,blur,xOffset,yOffset | series.shadow.<field> | series shadow geometry |
| labels enabled,font,weight,size,color | series.label.enabled,fontFamily,(fontWeight + fontStyle),fontSize,color | raw-value labels with original formatter |
| markers enabled,shape,size,strokeWidth | series.marker.<field> | retained symbols and outline |
| connectMissingData | series.connectMissingData | missing-value connection |
| axis color,thickness | axes.A.P.line.stroke; line.enabled=(value != 0),line.width=value | line color, visibility, width |
| grid enabled,color,thickness,lineDash | axes.A.P.gridLine.enabled,style,width,style | split lines, styles as described below |
| ticks enabled,color,width,length | axes.A.P.tick.enabled,stroke,width,size | ticks and length |
| axis labels font,weight,size,color,padding,autoRotate,rotation | axes.A.P.label.fontFamily,(fontWeight + fontStyle),fontSize,color,spacing,autoRotate,rotation | typography, gap and rotation |
| axis type,timeFormat,position | runtime concrete axes[index].type,label.format,position; categoryAxisType is runtime model state only | axis interpretation, date labels, placement; original save/reopen limitation below |

Axis structural writes are not ordinary theme patches. `ApplicationAxisStructureEvent` carries type/timeFormat/position separately from `ApplicationEditorEvent`; the stamped command accepts both and dispatches by panel. `transitionApplicationAxisStructure(input: AxisStructureInput): ValidationResult<AxisStructureTransition>` in `application/axisStructureTypes.ts` freezes the pure transaction. It returns runtime concrete axes plus only the original theme-override patch. The appearance resolver consumes that runtime through `AppearanceInput.axisRuntime`. No serialized axes or categoryAxisType field is added.

The structural transaction is ordered as follows:

1. Resolve the selected concrete axis using source direction selection (52398 onward). Preserve all unrelated concrete options and unknown fields. Reject missing axes or invalid identity/type/position. For this ordinary three-family journey the category axis occupies index zero, as required by the original category type operation; do not silently apply that operation to another index.
2. Position and timeFormat edits update only the selected concrete axis position or label.format. Return an empty appearance patch; neither operation is converted into a new saved leaf.
3. A category type edit equal to the current type is a no-op. Otherwise capture the first defined old applied override object for the old actual type in its direction's position order. Transfer original retained crosshair overrides using the source literal expressions `crosshair`, `crosshair.top`, `crosshair.bottom` for x, or `crosshair`, `crosshair.left`, `crosshair.right` for y, from the old type to all original Cartesian types (number, category, time, grouped-category). Do not reinterpret the source suffix ordering as a different nested path.
4. Change concrete axes[0].type and runtime categoryAxisType to the requested eligible category/number/time value. When crossing into time, update label.format to `%d %B %Y`; when leaving time, write runtime undefined. Preserve other label siblings. Then reapply the captured old override object under the new actual type at both positions for the resolved direction. Undefined original values retain original merge behavior; no delete/null/reset operation is introduced.
5. Return the resulting runtime axes and exact theme override patch from steps 3 and 4. The existing integrated reducer receives latest original baseline.options plus that patch and the existing serialized ChartModel unchanged except for source-established model fields owned by other commands. Runtime axes are never passed to it as chartOptions.

Source evidence: original bundle getChartModel45061-45080 exports chartProxy.getChartThemeOverrides only; getChartThemeOverrides41231 returns theme.overrides. Concrete axes and categoryAxisType are absent from that serialized model. setCategoryAxisType45342 changes internal ChartDataModel only. Workspace original useChartOptions.tsx onChartOptionsChanged reads getChartModels and merges the event theme overrides into original stored options. Thus structural axis choices can affect the current chart but their direct concrete values do not round-trip through original storage. Save/reopen reinitializes them from original data/model/theme inputs, with only transferred override effects retained. This source-proven limitation must be named in acceptance, alongside auto-rotation; repairing it would require an expressly reviewed persistence behavior change.

Grid color writes a one-item style array retaining the previous first entry's dash; dash writes a one-item array with `[value]` and previous stroke. Preserve untouched option branches under the original reducer's array merge behavior. Typography weight keys normal/bold/italic/boldItalic map to their original paired weight/style values; predefined retains the exact pair from the effective source. These bounded contexts accompany imported panel events. Do not persist the contexts or effective defaults.

## Immediate edits and freshness

UI callbacks dispatch `ApplicationEditorIntent`, not a hydrated `ApplicationEditorEvent`: no firstStyle, predefined font pair, axis binding or manual angle from a render closure is authoritative. Inside each functional Widget update, select latest original storage/model, resolve latest effective appearance and eligibility, resolve direction/type, then call `rehydrateApplicationEditorEvent` and the finite mapper. Consequently a grid color edit immediately followed by a dash edit uses the newly accepted color. Structural transitions use the same latest-state boundary. Runtime axes/manual-angle retention belong to the existing session lifecycle and are updated in accepted command order with replay-safe transaction handling; they are not another persistence owner. Updater replay must not repeat external mutations or advance runtime state twice.

`validateSynchronousEditorStamp(viewStamp,currentStamp)` checks address, generation and dataRevision, validates all stamp fields, then returns the current accepted full stamp. It intentionally permits renderRevision to advance between two immediate edits from the same control view. The command's family, selected IDs and original predicates must still match the latest selection; data/view identity changes reject it. Address/grid/family/selection changes invalidate the appropriate view/data identity. Asynchronous render, capture and export completions continue to use unchanged `validateSessionStamp`, including exact renderRevision equality. Never weaken that existing validator globally.

Auto Rotate writes its flag and runtime `rotation: undefined` when enabled; disabling restores retained manual rotation. Original lodash merge can retain a previously saved numeric angle, and reopen gives that angle precedence over autoRotate. Preserve this limitation and distinguish current interaction from reopened initialization. No deletion, null sentinel or new merge semantics.

## Production menus and eligibility

Full font source: original ag-grid enterprise bundle FontPanel lines 47233-47405. Keep its exact spellings, including `Aria Black` and doubled spaces: Arial, Aria Black, Book Antiqua, Charcoal, Comic Sans MS, Courier, Courier New, Gadget, Geneva, Helvetica, Impact, Lucida Console, Lucida Grande, Lucida Sans Unicode, Monaco, Palatino Linotype, Palatino, Times New Roman, Times, Verdana, with source generic-family suffixes. Source sorts families, matches current values case-insensitively and appends unknown current choices. Size choices are 8,10,12,14,16,18,20,22,24,26,28,30,32,34,36 plus current size, numerically sorted. Weight menus preserve the conditional predefined choice. Production metadata must be derived from these full menus for each typography state, not copied from stories.

Axis type/time choices and original predicates are recorded in chart-axis-fields-design.md. Time defaults to `%d %B %Y` on entering time; leaving writes undefined under original semantics. Fields types/timeFormats/positions are absent when ineligible; tickLength and autoRotate follow original axis predicates. Shadow, labels, markers, connectMissingData and series numeric controls follow family/data predicates. Set Up remains a separate range/model command contract and does not enter the appearance patch union. All three-family fields must have a renderer assertion and saved-leaf assertion before lane acceptance.

## Exact implementation exports

`resolveApplicationAppearance(input: AppearanceInput): AppearanceResult`

`selectApplicationEditorState(input: EditorSelectionInput): EditorSelectionResult`

`mapApplicationEditorEvent(event: ApplicationEditorEvent, family: CartesianFamily): ValidationResult<RuntimeOptions>`

The mapper validates runtime shape/value constraints despite static types. Session validates latest original namespace and eligibility before reduction, and never supplies generated/resolved appearance as reducer resolvedOptions. Every relocated type file must pass 400 physical / 300 logical / 50 per-function caps and strict affected type checking. These declarations have not yet been compiled in the production tree.

## Production caller inputs

Observed source mapping on 2026-10-18. This is a read-only source inventory, not browser acceptance evidence. Paths below are relative to `vendor/workspace/terminalpro/src/`.

| Input or owner | Exact source and contract |
| --- | --- |
| Production theme adapter | `components/General/Table/Chart/themes.tsx`: `useAgThemes(theme)` returns `themePalette`, `agTheme`, `chartThemes`, `customChartThemes`. `getOpenBBChartTheme`, `getCustomChartTheme`, and `OpenBBChartThemes` own stock/custom conversion. |
| Theme aliases and selection | Stock aliases are `openbb-dark` / `openbb-light`; custom aliases are `custom-dark` / `custom-light`. Selected alias is `custom-${theme}` when that entry exists, otherwise `openbb-${theme}`. Stock base names are `ag-default-dark` / `ag-default`. |
| Custom state and palette | `lib/state/tableChartThemes.ts`: `useShallowTableChartThemesStore`, with `dark.chartTheme` / `light.chartTheme`. Valid custom conversion currently requires `baseTheme`, `palette`, and `params`. The selected object is `customChartThemes[chartThemes[0]]`. Do not assume returned `themePalette` belongs to the selected mode: its loop assigns each valid custom palette in iteration order. |
| Bar fill | `themes.tsx`: `createItemStyler(palette, shouldFillBars)` uses `palette.fills` or local `defaultFills`; `useAgThemes` reads `widget.storage.chartBarFillEnabled`. |
| Initial override generator | `Chart/hooks/useChartOptions.tsx`: retained `getDefaultChartOptions(chartOptions, chartType)` converts generic options into per-series AG overrides. It currently references unresolved `getSeriesType` and `AgChartThemeOverrides`; invoking this dormant helper needs imports/type repair. The default hook currently returns `{}`. |
| Proper old helper source | `Chart/utils.tsx`: `getSeriesType` uses `CHART_TYPE_TO_SERIES_TYPE` from `lib/constants`, falling back to `line`. The same file owns `createDefaultSeries`, fiscal-period formatting, and `createChartArtifactAxes`. `components/AI/artifacts/ChartArtifact.tsx` is a surviving production caller of `createDefaultSeries` and the selected theme object. |
| Ordinary table rows and definitions | `AgGridTable.tsx`: `useGetTableData` gets `getJsonColDefs(widget)`, queries data, calls `processAgGridTableData(queryData, widgetMemo, decimalDigitsToUse)`, and returns processed `rowData` / `columnDefs`. Use those processed values rather than raw response data. |
| Definition precedence and semantics | `lib/utils/widget.ts`: `getJsonColDefs` prefers `storage.columnDefs`, then external widget `data.table.columnsDefs`, otherwise registry definitions. `components/Widgets/dataProcessors.ts`: `processAgGridTableData` calls `getTableData`, then `getColumnDefs` and quarterly grouping. `General/Table/ColumnDefinitions.tsx` retains `field`, `chartDataType`, `cellDataType`, and header semantics; explicit definition types precede inference. `ColumnValues.ts`: `inferChartDataType` treats date/index/string as category and number as series. Grouped definitions need leaf traversal. |
| Chart data contract | `General/Table/hooks/types.d.ts`: `ChartDataT` includes processed rows, definitions, selected `columns`, widget ID, transpose, period, chart type/model, and actual transpose state. `Chart/AgChartView.tsx`: `createRangeChart` defaults to `groupedColumn`, preserves selected columns, transpose/category switching, aggregation and series configuration. Its current rendered view is unavailable and button returns null. |
| Widget persistence owner | `components/Widget.context.tsx` delegates to `Widget.hooks.tsx::useWidgetSync`, which delegates `updateWidget` to `widgetSync/useWidgetUpdates.ts::submit`; its `saveWidgets` subscription calls the owner's save. Keep changes on `updateWidget(prev => ({ ...prev, storage: { ...prev.storage, ...change } }))`. Existing concrete references: `AgGridTable.tsx` selected-group update and `AgGridFile.tsx::setCurrentSheet`. |

L4 existing caller ownership: `General/Table/Chart/AgChartView.tsx`, `Chart/hooks/useChartOptions.tsx`, `hooks/useTableContext.tsx`, `AgGridTable.tsx`, `AgGridFile.tsx`, and `communityBoundary.ts`. `useGridSync` in `useTableContext` already receives processed rows/definitions and increments `dataRevision`; `AgGridFile` currently hardcodes `chartView = false`.

L5 existing action adapter ownership: the named `useChartCloseButtonListener`, `useChartToolPanelAction`, `useChartBarFillQuickAction`, and `useChartQuickActions` exports in `Chart/hooks/useChartOptions.tsx` are current no-op adapters. Connect these through the session/host contracts after L4; this inventory does not establish which extractions the frozen L0 contracts will require.

Disproof condition for caller readiness: a production ordinary table reaches the editor with raw rather than processed data, loses explicit category/number semantics, chooses another mode's palette, bypasses the widget owner, or calls the dormant default helper before resolving its dependencies.
