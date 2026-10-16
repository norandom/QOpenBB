# ECharts integration proposal

Retain OpenBB's chart controls and saved models, translate them to ECharts at the existing chart container, and make the editor emit narrow updates to the original model. This proposal defines the chart integration boundary for requirements 4.8-4.9. It is not the approved replacement design, does not cover every table capability, and does not authorize production integration yet.

The [findings](echarts-findings.md) establish a narrow translation probe. The [editor contract](echarts-editor-contract.md) identifies source-level panels and original conditions. Remaining browser inventory and integrated evidence must resolve the acceptance gaps before finalizing the amendment to [design.md](design.md).

## Boundary commitments

Own chart lifecycle, translation of original chart data/settings/themes, original editor interaction, chart-state updates and PNG generation. Keep original widget IDs, tab placement, table/chart toggle, action locations, feature predicates and state keys.

Out of boundary: provider fetching, dashboard authentication, Compose topology, Anthropic protocol, Excel add-in, PostgreSQL and Jupyter. Existing table selection, grouping, pivot, remote data, formulas and XLSX restoration remain required parallel compatibility work under the parity amendment; this chart proposal does not remove them from acceptance.

Allowed dependencies: existing OpenBB table/action/state helpers and design-system controls; the selected ECharts package through its public API; browser ResizeObserver. Perspective remains a candidate analytical engine behind the original data contract, not a second widget interface. Existing Plotly widgets retain their own path.

Revalidate when saved-model fields, original flag predicates, data transformations, chart families, theme semantics or renderer/package identity change. Do not treat an untranslated legacy option as safely ignored merely because its JSON survives.

## Responsibilities and file plan

Proposed paths are in the owned Workspace fork under `terminalpro/src/components/General/Table/`, unless noted. These files are not claimed to exist.

| Component | Proposed path or existing seam | Responsibility |
| --- | --- | --- |
| Legacy chart state | `Chart/compatibility/legacyState.ts` | Read original integrated/detached/legacy partitions; apply field-scoped patches while retaining unrelated values. |
| Chart snapshot contract | `Chart/compatibility/snapshot.ts` | Capture ordered columns/rows, selected range, model and data revision from original transformations. Do not refetch providers or treat one remote page as the full dataset. |
| ECharts option mapping | `Chart/echarts/options.ts`, `families/cartesian.ts`, subsequent inventoried family modules | Translate model, data and resolved theme into library options; explicit family coverage, no silent downgrade. |
| Theme mapping | `Chart/echarts/theme.ts` | Preserve active mode, palettes, typography, axis/tooltip/legend formatting and custom overrides. |
| Renderer host | `Chart/echarts/EChartsHost.tsx`, `lifecycle.ts` | Initialize in sized original container, update options/data, resize, dispose and generate image bytes. |
| Original container/toggle | Existing `Chart/AgChartView.tsx` | Keep original control semantics; mount the renderer host inside the original resize wrapper. |
| Table callers and removed-path guards | Existing `AgGridTable.tsx`, `communityBoundary.ts` and audited callers | Restore original call sites and chart-view state read; remove replacement-era rejection guards only as the equivalent behavior is implemented and verified. Guard removal alone is not acceptance. |
| Lifecycle/action join | Existing `hooks/useTableContext.tsx`, `Chart/hooks/useChartOptions.tsx`; cohesive chart-specific extraction if required | Route existing update/action flows to the new host without creating a counterfeit GridApi. |
| Compatible docked editor | `Chart/editor/ChartSettingsPanel.tsx`, `fields.ts`, `families/` | Use existing design-system primitives, original panel placement and recorded fields/conditions; emit original-model patches. No new toolbar or alternate editor flow. |
| Detached chart join | Restore existing `AgChartFromTable.tsx` and `hooks/useCreateChart.ts` behavior | Preserve same-tab placement, selected-data scope, legacy forms and forecast-specific conditions. |
| Verification | `terminalpro/tests/unit/chart-compatibility/`, `terminalpro/tests/e2e/chart-compatibility/` | Original-state fixtures, semantic mapping, integrated interactions/themes, lifecycle and export regressions. These are planned paths, not completed tests. |

Dependency direction: original data/state contracts -> state/snapshot helpers -> ECharts mappings -> host -> original UI join. Editor controls depend on the legacy-model patch contract, not the renderer instance. The host never owns dashboard persistence or provider state. The controller owns shared locks, package imports, capability/breadth mapping and inventory joins.

## State and event contracts

The legacy widget payload remains authoritative. Preserve unknown JSON fields, but distinguish retention from support. Reading a payload produces the exact state partition, original model, selected columns/range and current revision. A settings event changes only the observed original fields; a renderer option object is derived and never replaces widget storage.

The codec must cover integrated `storage[stateKey].chartModel`, per-type cell ranges, detached top-level `chartModel`/`chartOptions`, and the original transpose fields. Preserve the original theme-field handling. Do not migrate those forms into a new envelope without a separately reviewed migration contract.

A chart request contains an immutable snapshot of ordered category/series values and identities, the original model, resolved active theme, and data revision. Snapshot construction reuses original sort/filter/group/transpose transformations. Each operation uses one consistent revision; stale results must not overwrite newer state. Preserve the original export/selection completion behavior, verified during capture. A frozen export snapshot may remain valid after the displayed data refreshes.

Host operations are mount, update, resize, export image and dispose. Only the host retains the ECharts instance. Settings events go through the original action/state owner, which derives a new request; renderer events are translated into the same original state changes where the baseline requires them. One state owner prevents the editor and saved configuration from diverging.

## Editor behavior

Preserve the original settings/data/format panels, each path's open/close behavior and right-chevron close control. The integrated hook persists `chartSettingsOpen`; detached behavior needs separate capture rather than assuming uniform persistence. Use the [editor contract](echarts-editor-contract.md) for original suppression, flags and themes. Keep the existing external export actions; do not enable an ECharts toolbox.

A field registry records original field path, type, default, visibility predicate, patch operation, renderer mapping and test case. Split family-specific controls into small modules. The registry must come from source and browser observations, not an invented reduced set. Public AG group tokens are insufficient to define every field.

ECharts shoulders rendering, zoom/navigation primitives and image generation. Existing OpenBB/Radix/react-colorful components shoulder input behavior. The application still owns the compatibility of those controls with original settings. No inspected library provides the whole AG editor as an ECharts drop-in.

## Failure and release rules

Preserve the original payload on mapping or schema failure and retain diagnostic evidence without credentials or financial provider payloads in ordinary logs. A diagnostic failure in a development fixture is a failed capability, not an accepted unavailable-state replacement. No hidden feature flags, disabled controls or changed financial operations may close a gap.

PNG output needs original filename, dimensions and visible contents checked through the original export action. JSON roundtrip alone does not prove backend persistence. The independent SQLite query repair and actual save/restart/reopen test remain prerequisites to a persistence claim.

The open Highcharts input contract remains separate from enumerated AG chart models. Successful grouped-column translation cannot accept arbitrary chart, stock, map or Gantt options. Record each original capability and its outcome before renderer or release acceptance.

## Verification and bounded execution

The first integration slice is the original table/chart toggle, container and a flat grouped-column request. It establishes only that seam. Subsequent slices cover state variants, original editor fields, data/selection semantics, chart families, theme/export behavior and real persistence, with a negative regression retained for every known missing control.

Use at most two implementers and one reviewer alongside the controller. Freeze the state/request/patch interfaces before independent work: one lane owns pure state/mapping modules; another owns host/editor modules; the controller serializes existing-hook joins and dependency changes. Use Sol for bounded code, Astra for architecture/financial review and Luna only for mechanical inventory. One heavy build/browser runs at a time.

Every maintained production task must pass the existing scope inventory and 400 physical lines/file, 300 logical units/file and 50/function checker. Extract cohesive responsibilities from oversized hooks or obtain a measured narrow exception. Do not promote compressed disposable spike code into production. Documentation and ignored discovery artifacts do not establish production size compliance.

For 4.8, compare original controls, conditions, state changes and rendered outcomes in the real dashboard. For 4.9, require the full capability matrix, light/dark visual evidence, actual test paths and matching source/image identities. A green integration slice does not close either requirement by itself.

## Decisions still needed for the final design

- Complete the field-level editor browser inventory and confirm feasible mappings for its controls.
- Resolve selection, grouped/pivot/remote data and financial aggregation compatibility without reducing original operations.
- Demonstrate more than one chart family and address legacy/open Highcharts configuration coverage.
- Reconcile superseded native-explorer clauses in the main design and generate reviewed, bounded implementation tasks.

The requirements are clear; these are engineering evidence gaps. They do not require the owner to choose a new UI or relax parity merely to continue investigation.
