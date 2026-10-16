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

The source paths have different write semantics. Integrated `onChartOptionsChanged` clones the resolved `chartOptionsRef.current` baseline, deep-merges event options (defaulting to an empty object), removes their top-level `theme`, and merges the current model under `storage[getStateKey()].chartModel`. Persisted options alone are not an equivalent merge baseline. The detached `AgChartFromTable` callback retains its existing top-level model while changing its chart type, replaces `storage.chartOptions` with event options, and updates series/type metadata; it does not perform the same theme removal. Use separate typed write operations for these paths. A common persistence writer must not erase that distinction. The integrated options hook also replaces `chartOptions.common` with generated common settings before merging, so editor field scopes must be traced from actual events rather than assuming every `common.*` patch survives.

A chart request contains an immutable snapshot of ordered category/series values and identities, the original model, resolved active theme, and data revision. Snapshot construction reuses original sort/filter/group/transpose transformations. Each operation uses one consistent revision; stale results must not overwrite newer state. Preserve the original export/selection completion behavior, to be verified by dedicated capture. A frozen export snapshot may remain valid after the displayed data refreshes.

Host operations are mount, update, resize, export image and dispose. Only the host retains the ECharts instance. Settings events go through the original action/state owner, which derives a new request; renderer events are translated into the same original state changes where the baseline requires them. One state owner prevents the editor and saved configuration from diverging.

## Editor behavior

Preserve the original settings/data/format panels, each path's open/close behavior and right-chevron close control. The integrated hook persists `chartSettingsOpen`; detached behavior needs separate capture rather than assuming uniform persistence. Use the [editor contract](echarts-editor-contract.md) for original suppression, flags and themes. Keep the existing external export actions; do not enable an ECharts toolbox.

A field registry records original field path, type, default, visibility predicate, patch operation, renderer mapping and test case. Split family-specific controls into small modules. The registry must come from source and browser observations, not an invented reduced set. Public AG group tokens are insufficient to define every field.

Each edit also records its target state address and revision. Integrated addresses include the original state key and pivot mode; detached addresses identify the original range key. A delayed event must not write to a newly selected period/sheet partition. Resolve the original target or surface the stale transaction internally; do not silently apply it elsewhere. Family changes resolve the destination family's saved range before updating the model.

Use a discriminated command union with value types per captured field: booleans for enablement, strings for text/colors, numbers for font sizes, the original position enum for legend placement, and a separate chart-type command. The initial grouped-column/stacked-column/line mapping does not define the total accepted model language. Retain unknown JSON separately. Field targeting, including whether a color affects one series or the whole family, must come from observed editor output.

Legacy event merging and new leaf edits are different operations. Integrated event compatibility must retain lodash merge behavior, including array index merging. A field edit clones state and changes only its registered target. Explicit deletion is separate: `undefined` is not deletion under merge and `null` is not a universal inheritance marker. Reset semantics need their own captured event contract.

ECharts shoulders rendering, zoom/navigation primitives and image generation. Existing OpenBB/Radix/react-colorful components shoulder input behavior. The application still owns the compatibility of those controls with original settings. No inspected library provides the whole AG editor as an ECharts drop-in.

## Concrete first-family mapping

Independent source research by `/root/chart_mapping_design`, GPT-6 Astra, inspected the original Workspace reference and installed ECharts 6.0.0 declarations. The following destinations exist in that package; the table is a design mapping, not evidence of visual or behavioral equivalence.

| Resolved original value | ECharts destination | Required compatibility check |
| --- | --- | --- |
| Title enable/text/color/font size | `title.show`, `text`, `textStyle.color`, `textStyle.fontSize` | Actual writable legacy scope; original title spacing, alignment and wrapping. |
| Legend enable | `legend.show` | Preserve initial and persisted state. |
| Legend position | Position coordinates, `orient` and plot allocation | Compute the layout; do not assign the original position string to an unrelated field. |
| Legend typography/markers | `legend.textStyle`, rectangular icon, item width/height | Preserve formatting and measured geometry. |
| Bar fill/stroke/width | Series `itemStyle.color`, `borderColor`, `borderWidth` | Match captured target cardinality; retain stable series identities. |
| Line stroke/width | Series `lineStyle.color`, `width` | Marker colors are separate; a bar fill does not automatically become a line stroke. |
| Connected missing line data; markers off | `connectNulls: true`, `showSymbol: false` | Preserve null observations without coercing them to zero. |
| Grouped columns | Category X/value Y, bar series without stack | Preserve original ordered data, ranges and series IDs. |
| Stacked columns | Shared stack identifier | Verify negative/missing values and `stackStrategy` against the original. |
| Line | Line series without stale bar/stack properties | Resolve original destination-family range first. |

Use original column/series identity rather than display labels for stable IDs. Duplicate labels or column reordering must not transfer settings between series. Preserve original aggregation and unit choices; the adapter must not introduce new financial restrictions.

AG's independent legend horizontal/vertical padding, marker padding, spacing and maximum height do not map one-to-one to ECharts `itemGap`. This requires measured layout work. Pointer-anchored zoom, navigator/mini-chart behavior, background images and tooltip formatting also require explicit mappings and tests; a plausible chart does not prove those contracts.

Keep base defaults, OpenBB overrides, selected custom theme, generated chart options and persisted family overrides distinct. The global theme editor filters undefined/null/empty parameters and resets a mode with `chartTheme: null`; that is different from deleting widget fields. Global theme edit/preview/save/reset needs its own event contract.

Derive a complete ECharts option for each request. A first implementation may use `setOption` with `notMerge: true` to prevent stale stack/family/style fields, but must preserve required interaction state through public events before acceptance. `replaceMerge: ["series"]` alone does not guarantee removal of stale nested options. Test grouped -> stacked -> grouped -> line, title disable/re-enable, palette/theme reset and background-image removal.

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

## First production boundary for separate review

The owner approved this bounded foundation design on 2026-10-16. The state reducers and renderer lifecycle can be implemented before the remaining editor fields are mapped, after task review and approval. This is a bounded foundation within the larger amendment, not permission to expose a partial replacement or narrow requirements 4.8-4.9. Full renderer integration and release gates remain closed.

**Own:** two path-specific legacy state reducers and an ECharts host, with maintained tests and inventory entries. **Exclude:** application call-site changes, guard removal, widget registry/catalog changes, new editor UI, chart-family translation, provider/backend changes, global theme migration and release-image promotion. Test fixtures may supply known options to the host; they do not become a production allowlist.

| Module | Frozen input/output boundary | Completion evidence required |
| --- | --- | --- |
| `Chart/compatibility/legacyTypes.ts` | JSON value/object types, addressed integrated or detached event inputs, explicit validation result; no `any` or new storage envelope | Type checks distinguish the two paths and retain unknown JSON values. |
| `Chart/compatibility/integratedState.ts` | Original storage, original resolved state key, current chart model, resolved `chartOptionsRef.current` baseline, event options (default `{}`), chart type, resolved total series and pivot mode; returns updated storage without mutating input | Reference-equivalent deep merge into the resolved baseline, including arrays; top-level option-theme removal only, original model overlay and root metadata updates; untouched partitions equal. |
| `Chart/compatibility/detachedState.ts` | Original storage, event chart type/options and resolved total series; returns updated storage without mutating input | Existing top-level model retained except chart type, event options replace root options without integrated theme stripping, original root metadata updated. |
| `Chart/echarts/lifecycle.ts`, `EChartsHost.tsx` | Sized DOM host plus complete typed ECharts options and request revision; update/resize/export/dispose operations | Real ECharts mount/update/resize/hidden-container/remount/disposal tests; stale work cannot update a disposed instance. No application persistence or data fetching. |

State-key construction stays with the existing original helper; the reducers receive its resolved address and do not reimplement it. The caller resolves any family-range update and obtains total series from the original chart/grid context before invoking a reducer. A JSON-only reducer must not infer that count from option-array length. The future state owner checks event revision/address before invoking a reducer. These pure functions do not decide asynchronous edit cancellation, fetch new state or silently redirect a write.

The lifecycle receives an already-resolved `EChartsOption`, keeps the library instance private and uses public APIs only. Export returns image data without inventing filename/menu behavior. Accept only the tested lifecycle contract; zoom/selection continuity and original export integration remain later obligations. No ECharts type leaks into provider, dashboard-storage or agent contracts.

Pin ECharts 6.0.0 through the existing protected toolchain and the owned application's validated lock strategy. The disposable global script injection is not the production loading mechanism. Controller owns package/lock and scope-inventory edits; other lanes do not install concurrently or modify those shared files. Reuse the existing package manager exception where a migration would rewrite the frozen baseline.

After shared types are fixed, Sol state-reducer and lifecycle lanes may proceed independently; Astra reviews persistence and lifecycle joins. Planned tests live under `terminalpro/tests/unit/chart-compatibility/` and `terminalpro/tests/e2e/chart-compatibility/`. Require the existing 400/300/50 checker on all new/modified maintained code, exact dependency/source identities and independent fresh verification. No maintained tests are claimed to exist yet.

This foundation supports original-state preservation under 4.8 and supplies executable evidence toward 4.9. It does not fulfill either criterion alone. Its review does not approve the unresolved editor, full chart mappings, table capabilities or the superseded renderer clauses in the main design.

Independent Astra review passed this bounded foundation design after correcting the integrated merge-baseline and resolved-series inputs, followed by owner approval. Source callbacks were checked at the pinned original revision. Review evidence is in `artifacts/parity/chart-editor-capture-review/review.md`. Task approval remains separate; this is not whole-renderer design acceptance.
