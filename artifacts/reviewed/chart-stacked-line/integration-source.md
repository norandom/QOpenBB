# Stacked Line integration source assessment

Stacked Line and 100% Stacked Line should extend the existing ordinary Cartesian session. Admission alone would currently turn them into bars or apply bar appearance. Freeze the original cumulative geometry and normalization contract before choosing reusable projection code.

Source-only assessment, 2026-10-26. QOpenBB revision `37cc2fb8bad40ae9842d5a01f9b5799f3aecbdda`; owned Workspace revision `0b2190354d2dc5f4175ffb989cf652ac36237c77`. Working-tree source was inspected; neither application behavior nor tests were run. Paths below are relative to `vendor/workspace/terminalpro/src/components/General/Table/Chart/` unless qualified. The prior `artifacts/reviewed/chart-funnel/next-family-inventory.md` inventory establishes visible original tokens, not successful activation.

## Admission and session owners

| Owner | Existing contract and required assessment/change |
| --- | --- |
| `editor/chartTypeGalleryCatalog.ts`, `editor/ChartTypeThumbnail.tsx` | Already expose `stackedLine` and `normalizedLine`. No new group or surrogate ordinary-Line entry is needed. |
| `echarts/cartesianTypes.ts` | `CartesianFamily` and `isCartesianFamily` omit both tokens; `isNormalizedFamily` admits normalized bars/columns/area only. Introduce a shared line-family predicate so all consumers agree; keep orientation separate. |
| `application/comboSessionTypes.ts` | `ApplicationChartFamily` incorporates CartesianFamily, so the public session union follows its admission. This does not authorize adding these variants to combination-series assignments. |
| `AgChartView.tsx`, `caller/useCallerDock.ts` | Both consume `isCartesianFamily` for host/dock eligibility. Verify admission reaches ordinary Table/File inputs and editor selection; avoid a second session owner. |
| `application/applicationSessionSelection.ts` | Owns baseline matching, stable range IDs, ordinary Set Up aggregation and category/series switch. `sessionBaseline` rejects a family mismatch; preserve exact saved model token through transitions. |
| `application/applicationSessionProjection.ts` | Owns translator invocation, raw-observation policy, viewport, navigator/miniature, and legend reprojection. It enables legend projection for normalized/area families; stacked cumulative lines may also require reprojection when visibility changes, depending on frozen original semantics. |
| `application/applicationSessionDispatch.ts`, `application/applicationSessionTransactions.ts`, `application/comboSessionAssignments.ts` | Retain existing stamped edit/family transactions and stale-command rejection. Review transition admission rather than inventing direct storage writes. |

## Reusable projection boundaries

`echarts/cartesian.ts` already resolves selected numerical columns, source-mode admission, compatible units/scales, display callbacks and application axes. `cartesianAdmission.ts` rejects undeclared units in declared-unit mode, mismatched known units even in raw mode, and unsupported non-flat captures without their ordinary Set Up witness. Reuse these invariants; normalized percentages do not justify combining incompatible currencies or scales.

`cartesianSeries.ts` preserves stable column IDs for series and legend keys, accepts separate raw and drawn snapshots, and resolves original marker/label/line appearance. However, its `family === "line"` branches decide line geometry, marker paint, label placement and line options. Every other admitted family falls through to `type: "bar"`. Extending only the union is therefore unsafe. Its application label formatter reads the raw snapshot, which is useful only after deciding whether original stacked labels display individual observations or cumulative endpoints.

`cartesianNormalization.ts` is an existing bar policy: for each row it scales enabled observations by `max(positive mass, absolute negative mass)` and multiplies by 100; hidden values and zero-total rows become null. Bar series use ECharts `stackStrategy: "samesign"`. These are reusable mechanics only if original Line evidence supports that exact policy. They are not an established Stacked Line contract.

The parallel original-source assessment reports signed algebraic cumulative Line endpoints and a normalized denominator equal to the maximum absolute cumulative endpoint per category. On that contract, bar normalization and same-sign stacking are incompatible and must not be reused as the Line policy. Its exact source citations belong to that companion assessment; runtime equivalence remains untested.

`cartesianArea.ts`, `cartesianAreaSpans.ts` and `cartesianAreaSeries.ts` offer a closer alternative for cumulative geometry. Area projection separates raw labels, cumulative markers, strokes and fills; handles missing substitutions, preceding-row normalization windows, legend selection and finite extents; area rendering already calls shared line appearance. Its normalization is cumulative/order-sensitive and differs materially from normalized bars. Reuse or extract the mathematically matching projection after comparison; do not instantiate filled area helpers merely to hide their fills. A shared cumulative projection should retain clear line/area responsibilities and avoid changing accepted area results.

`cartesianAxes.ts` treats ordinary line/area categorical positions as ordinal coordinates and has ordinary-Line numerical-axis behavior. `cartesianLayout.ts` has line-only legend geometry and marker sizing. `cartesianBarColors.ts` excludes ordinary line/areas from bar-fill decoration. All must recognize the new line families consistently. `cartesianStyle.ts` gates marker/style validation and line appearance on ordinary line. Navigator overview must retain full-series context while main cumulative geometry reflects legend membership if the source contract requires it. `cartesianTooltip.ts` receives the raw snapshot; keep transformed coordinates separate from financial observations and explicitly choose percentage versus raw tooltip formatting.

## Controls, themes and persistence

The editor requires no new bespoke panel if original line controls apply. The affected owners are:

- `compatibility/editorBindings/eligibility.ts`: line-only shadow exclusion, marker admission and Connect Missing Data eligibility.
- `compatibility/editorBindings/selectApplicationEditorState.ts`: line-only Line Width label and omission of Fill Opacity.
- `compatibility/editorBindings/rehydrateApplicationEditorEvent.ts`: ordinary-Line-specific event reconstruction.
- `compatibility/editorBindings/mapApplicationEditorEvent.ts`: supported-family admission and saved-option family namespace. Its current final mapping routes unrecognized Cartesian variants into `bar`; proposed variants need the source-confirmed `line` namespace.
- `application/axisStructure.ts`: crosshair/axis structural edits choose `line` namespace only for ordinary line; preserve those leaves across axis type changes.
- `application/effectiveAppearanceDefaults.ts`, `effectiveAppearanceLayers.ts`, `effectiveAppearanceSeries.ts`, `effectiveAppearance.ts`: line-only default stroke width, enabled markers, label colors, theme/generated/saved `line` precedence, stroke fallback and marker stroke width. A new family predicate should carry these together.

Use existing `appearanceComposition`, option baseline and integrated-state owners to preserve unknown saved leaves, raw observation values, range/state-address partitions and exact chartType. Do not serialize derived cumulative points, percentage arrays, viewport or legend runtime state into the financial data. Confirm the original saved namespace and variant model fields before implementation; this assessment establishes the current native routing problem, not original persistence semantics.

## Evidence patterns and bounded delivery

Existing tests under `vendor/workspace/terminalpro/tests/` provide directly reusable patterns:

| Test source | Useful evidence pattern |
| --- | --- |
| `unit/chart-compatibility/cartesian.normalized.test.ts` and `fixtures/normalized-bars.json` | Numerical fixture comparisons, legend membership, ECharts SSR model inspection, signed extents. Use independent Line fixtures, not bar expectations copied as authority. |
| `unit/chart-compatibility/cartesian.area-values.test.ts`, `cartesian.area-contract.test.ts`, `cartesian.area.test.ts` | Cumulative/missing/normalization contracts and geometry distinctions. |
| `unit/chart-application/editorArea.test.tsx` | Actual controls through rehydration, event mapping, integrated state and appearance resolution; checks preserved unrelated options and original family namespaces. |
| `unit/chart-application/editorSavedLeaves.test.ts`, `editorHorizontalAxes.test.tsx`, `sessionState.test.ts` | Saved leaves, structural axis edits, stamped lifecycle and transition regressions. |
| `e2e/live-chart/area-charts.spec.ts`, `normalized-bars.spec.ts` | Ordinary native route, editor and runtime evidence patterns. `e2e/chart-compatibility/cartesian.spec.ts` is a fixture harness and cannot substitute for Table/File acceptance. |

Proposed bounded sequence, requiring contract approval and independent review before implementation:

1. Controller freezes token/predicate, raw-versus-derived values, sign/zero/missing/overflow/order/legend semantics, saved namespace and transition behavior using original-source findings. Inventory maintained paths and the existing complexity checker command; no new checker foundation is needed because steering records it accepted.
2. Geometry worker owns a new cohesive cumulative-line projection plus narrowly scoped `echarts/cartesian*` changes and independent numerical/geometry fixtures. Completion includes ordinary line, accepted area and normalized bar regressions and explicit raw-data immutability.
3. After the shared predicate/interface is frozen, editor worker owns `application/effectiveAppearance*`, `axisStructure.ts` and `compatibility/editorBindings/*`, plus control/theme/persistence tests. Do not overlap the geometry lane's shared predicate ownership; controller serializes that edit.
4. Controller joins session/host admission, family transition, navigator/legend and Table/File browser evidence. Reviewer independently challenges financial semantics and source equivalence before acceptance. Update `.kiro/breadth.toml`, complexity inventory and status only against actual evidence.

Every production task must pass 400 physical lines/file, 300 logical syntax units/file and 50 units/function, with whole-file scope and final shared-module audit. A read-only physical scan found no files above 400 in the inspected `application`, `editor`, `compatibility`, `echarts`, and `caller` subtrees; no syntax-unit checker was run. Existing large functions such as `cartesian.ts`'s `buildOptions` must be measured before modification; physical file compliance does not establish function compliance. Root host/generated scopes were not fully inventoried, so any expanded touch scope requires a fresh measured inventory and cohesive extraction or reviewed exception where needed.

Runtime unknowns remain original-equivalent mixed-sign stacks, crossing/missing topology, zero normalization, continuous/time categories, legend reflow, label/tooltip meaning, native save/reopen, light/dark/theme transitions and actual Table/File activation. A source match or passing fixture harness alone cannot close these unknowns. Anthropic acceptance remains a prerequisite for any Excel work; Excel and standalone/AI/theme-preview callers are outside this bounded assessment.
