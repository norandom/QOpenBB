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

## Numeric and editor characterization

The following source characterization was completed on 2026-10-20. Charts references identify `artifacts/task-2.1/frontend/terminalpro/node_modules/ag-charts-enterprise/dist/umd/ag-charts-enterprise.js`; Grid references identify the retained Grid bundle above. An isolated Node evaluation of the extracted original `ContinuousScale` verified the scale results below. This is not browser or application acceptance.

- Bubble size domains are per-series processed minima/maxima, with an internal `marker.domain` override (Charts 44186-44213). Zero and negative finite numbers participate unchanged. Independent column processing means size values on rows with invalid coordinates still contribute to the size domain (16334-16365, 16586-16645).
- Diameter is linear over `[size,maxSize]`, normally `[7,30]`. Domains `[0,10]`, `[-10,10]` and `[-10,-2]` map their endpoints/midpoint to `[7,18.5,30]`. Equal domains, including `[0,0]`, give diameter 18.5 (14045-14104, 44351, 44403).
- Missing, null and invalid processed sizes use the minimum marker size for valid-coordinate points (44403). Missing sizes do not contribute to the domain. Invalid coordinates become NaN and are hidden (23753-23755). No fabricated coordinates or size observations are needed.
- The scale defaults to no clamping (14045-14104). With explicit domain `[1,3]`, values `[-1,0,1,2,3,4]` map to `[-16,-4.5,7,18.5,30,41.5]`. Nonpositive resulting diameters are hidden (23755). The ordinary mapper need not expose the cross-filtering domain override.
- Both themes retain circle shape, size 7, fill opacity 0.8, stroke width 1 and disabled labels; bubble maxSize is 30 (38950-38965, 44717-44738, 46183-46203). Application `themes.tsx` does not override XY geometry. Grid shape choices are square, circle, cross, diamond, plus, triangle and heart (14188-14193). Existing `echarts/cartesianMarkers.ts` retains their original paths and nominal dimensions; reuse it.
- Triangle has default centered marker anchor (Charts 24487-24495), but its unit vertices occupy vertical bounds `[0,0.87]` (24412-24417). Preserve its bounding-box center offset of `-0.065 * diameter`, as existing `cartesianSeries.ts` does. Bubble must calculate the offset per point; a renderer test remains required.
- Insufficient selections produce no assignments: bubble with two selected fields is empty in both modes (Grid 8498-8539). The original hides the plot and displays "No data available to be charted." below two scatter fields, below three bubble fields, or for no data rows (10518-10544, 19151).
- Setup headings are Labels and X Y Values. Incomplete selected groups retain X/Y/size annotations (12301-12330). Aggregate is reachable with a real Labels category, defaults to sum, and offers sum/first/last/min/max/count/avg; all selected numeric columns aggregate before pairing (11641-11680, 10024-10089). Switch Category / Series is unavailable for XY by explicit source guards (19656-19661, 19816-19819, 11764-11767, 7675-7678).
- Navigator and mini-chart are exposed for XY. Their application flags default false and are mutually exclusive; either enables the navigator. Original mini-chart axes retain numeric X (Charts 68934-69065, 75544-75565), and navigator position is a normalized X range (69173-69177). Preserve later Y autoscale, minimum-visible-items, wheel/pan and double-click/reset duties; current lifecycle behavior does not yet prove those interactions.

See [X2 mapper contract](xy-mapper-design.md) for the inactive implementation boundary.

## Application characterization still required

- Render missing, zero, negative and equal sizes against the established source contract.
- Verify exact marker-shape geometry, rasterization and effective appearance in both application themes.
- Exercise category aggregation through the existing transaction owner.
- Establish application numeric-X navigator, mini-chart, zoom and reset parity.
- Verify empty-state presentation, point tooltip association and numeric-axis padding/ticks without replacing missing observations with invented points.

These questions prevent treating the source inventory as an implementation-ready contract. The proposed reuse fails if it changes original field assignment, stored options, reachable controls or numerical observations.

## Real FMP acceptance

Reuse the captured AAPL annual income statements in ignored `artifacts/chart-combo/fmp/`; no new provider request is needed. Proposed X is revenue in original USD amounts, Y is net income in original USD amounts, and bubble size is EPS in USD/share. Fiscal period labels retain the original fiscal-year/date association. Marker size represents EPS, not market capitalization or a third USD total.

Retain raw observations without rescaling. Axis and tooltip magnitude formatting is presentation only. Reuse the provenance/hash and CSV-consumption checks from `terminalpro/tests/e2e/live-chart/combo-fmp.spec.ts`, but replace its categorical hover-coordinate assumptions. The captured five observations support one scatter pair and one bubble triple; synthetic fixtures must cover multiple groups, unpaired mode, incomplete groups, duplicate labels and missing/negative/equal values.

Acceptance requires plotted coordinates and sizes, displayed values and units, applicable controls, both themes, refresh, save/reopen and export in the application. Engine-only evidence does not establish this journey.

## Bounded next task order

Integration inspection identified three constraints for X3: `setupProjection.ts` needs an explicit XY policy so USD coordinates and USD/share bubble sizes are not rejected by the ordinary single-axis unit check; `effectiveAppearanceLayers.ts` currently maps unfamiliar families to bar and must not be used as an XY resolver; original XY appearance writes top-level `series.shape/size/maxSize/strokeWidth`, while existing Cartesian marker controls write `series.marker.*`. Preserve these different saved paths through the existing option reducer.

Use the existing capture, setup aggregation, widget transaction owner and stamps. Pairing is a stamped family-specific option change; it needs no second store or persisted assignment list. The Labels selector determines whether X2 receives category or Y point labels. Axis appearance must resolve numeric X/Y explicitly. Caller defaults, navigator and wheel/reset integration remain X4 obligations before activation.

The X2 renderer check found that ECharts can reverse an extent when a lone explicit minimum exceeds all observations or a lone maximum falls below them. Original Charts `normalisedExtentWithMetadata` (30524-30543) instead produces an empty domain; `NumberAxis` (32086-32089), `LinearScale.niceDomain` (32052-32053) and marker visibility (23753-23755) preserve empty geometry. X2's inactive safety diagnostic is not final parity for this setting. Before X4 acceptance, reproduce that empty-domain behavior without reversing bounds or inventing observations.

1. Freeze XY assignment/options and edge-case behavior. Own new `compatibility/xyAssignments.ts`, its focused tests and the bounded design record; keep it inactive. The controller owns shared interface edits.
2. Implement an inactive mapper in new `echarts/xy*.ts` and focused mapper/render tests: numeric coordinates, size mapping, axes, labels and tooltips.
3. Implement session/editor behavior in new `application/xy*.ts`, `editor/xy/*` and focused transaction/control tests. Keep the existing session as sole state owner. This lane may overlap task 2 only after interfaces are frozen and writable paths are disjoint.
4. Join production routing, caller defaults, setup/customize controls and navigator behavior under controller ownership. Preserve unknown/inactive options and stale-command protection.
5. Independently review and verify the captured-FMP application journey plus prior-family regressions. Update breadth, inventory and evidence; commit bounded accepted work and dispatch one completed-milestone image release.

Every production handoff requires whole-file caps of 400 physical lines, 300 logical units and 50 units per function, using the existing [complexity gate](../../../docs/complexity.md) with actual explicit fork scope. Extend the existing inventory; foundation enforcement already exists. Tests and this research document are outside production caps. Follow [delegation policy](../../steering/delegation.md): exclusive ownership, independent review, serialized heavy verification and selective commits. Unrelated Perspective work is outside this slice.
