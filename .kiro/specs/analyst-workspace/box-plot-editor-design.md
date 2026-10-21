# B3d Box Plot editor and session activation

Independently source-accepted, 2026-10-21. Activate ordinary Table/File `boxPlot` through the existing application session, gallery, editor and ECharts host. B3a/b/c are accepted at Workspace `b34984e46ee3fd942a5d80999dde77de1988896a`; root inspection base is `c1262c3`. This slice delivers the working production join. B4 retains real-data, identified-image and original/replacement visual acceptance; B5 retains publication.

## Boundary commitments

One integration owner implements the entire coupled join below. Reuse accepted Box capture/setup, `translateBoxPlot`, `boxPlotNavigationWindow`, Widget transactions, editor primitives and host lifecycle. Preserve the original control reachability recorded in [B3](box-plot-integration-design.md), with axes/navigation governed by [B3c](box-plot-axis-navigation-design.md). No feature flags, second editor, catalog redesign or foundation work is needed.

**Out of boundary:** Range, standalone/AI callers, provider expansion, builds, browser runs, image publication and blanket whole-spec approval. Controller owns inventory, breadth, status, checkboxes, evidence and commits; preserve unrelated catalog/Perspective edits.

**Allowed dependencies:** caller data/theme -> application capture/selection/appearance -> accepted Box mapper -> existing host. Editor emits typed intents to the existing session owner; reducers receive latest Widget storage. Mapper/navigation never read storage or aggregate again.

**Revalidation triggers:** new production paths beyond the table, mapper signature changes, a reachable saved configuration rejected by admission, category/statistical changes, or lost original controls require controller review. Numeric-category legacy autoscale and remaining layout/miniature appearance differences remain explicit B4 owner decisions.

This English addendum applies local `kiro-spec-design` light integration and synthesis under the prototype-first amendment; it does not advance unapproved whole-spec metadata. Core product/tech/structure steering is absent. Existing milestone acceptance clauses 1-3 and 5-6 own this join; clause 4 and final clause 5 acceptance remain B4. No new requirement IDs are invented. Reuse of Histogram selection/transactions and Pie's specialized editor state is the smallest current extension; no new dependency or harness is proposed.

## Frozen session and persistence contract

Use model family `boxPlot`, option family `box-plot`, ready discriminant `kind: "boxPlot"`, and editor mode `kind: "boxPlot"`. Add `BoxPlotEditIntent` to `ApplicationChartCommand["intent"]`:

```ts
type BoxPlotEditIntent =
  | { panel: "boxPlot"; edit: { kind: "direction"; value: "vertical" | "horizontal" } }
  | { panel: "boxPlot"; edit: { kind: "whisker";
      field: "stroke" | "strokeWidth" | "strokeOpacity" | "lineDash" | "lineDashOffset";
      value: string | number | readonly number[] } }
  | { panel: "boxPlot"; edit: { kind: "cap"; value: number } };
```

Transaction validation narrows value by field, rejects nonfinite/malformed input, and preserves valid arrays and values outside slider maxima. Foreign-family specialized intents return stale before generic reducers. Box rejects unsupported generic intents (labels, markers, shadow, connectMissingData, geometry/combo/XY/Pie/Histogram) rather than accidentally writing another family's options.

`selectBoxPlotSession(storage, context)` follows `selectHistogramSession`: obtain `sessionBaseline`, latest range/setup, call `projectOrdinarySetup` with `box-observations`, resolve appearance, build current concrete axis bindings and editor selection. Return baseline/range/setup/projection/Box style/selection/editor together. Do not recapture or reaggregate within mapper, legend or navigator callbacks.

`projectBoxPlotSession` waits for capture and viewport, then translates immutable snapshot/style/context. Supply existing navigator/mini flags and current theme in `context.navigation`. Expose `projectLegendSelection` by retranslating the same immutable mapping with selected field IDs, and `projectNavigationWindow` by closing over that mapping and calling the accepted B3c helper. Host owns live range; Widget storage contains no new zoom window. Ready output includes current editor, model, snapshot, setup props and Box projection. Mapper unsupported -> unresolved diagnostics; invalid -> invalid diagnostics; callback failures throw to existing host cleanup/export invalidation. Forward the navigation callback from ready to the existing host in `AgChartView`.

`applyBoxPlotEditorTransaction` validates synchronous stamps, family and latest range/setup, reselects from the supplied latest storage, rehydrates common events against that selection, then uses `reduceSessionOptions`. Common series edits write `box-plot.series`; whisker edits write `box-plot.series.whisker`; caps write `box-plot.series.cap.lengthRatio`; direction writes `box-plot.series.direction` and uses the existing chart-model update path so category/number axes rebuild coherently. Caption/axis edits use concrete current family bindings, including after direction change. Do not persist ECharts options or overwrite inactive family branches. Family return, external storage edits and save/reopen retain existing baseline composition/transaction behavior.

## Appearance, options and controls

Resolve defaults -> theme common/family -> composed generated/saved common/family using `composeAppearanceOptions`, preserving intentional generated-common replacement. Extend caller theme enumeration and generated series options with `box-plot`. Use B2's exact defaults: Box main stroke width 2, selected-field palette identity stable through legend hiding, final main stroke leaves inherited by unspecified whisker leaves only after all layers. Explicit whisker leaves override inheritance independently. Direction and numeric bounds remain raw admitted values; category/number positions are resolved for actual direction. Do not borrow Histogram's two-number-axis bindings.

Keep titles/subtitle/axis captions, legend, padding/background, tooltips, main stroke width/dash/opacity/fill opacity, axes/labels/grid and source-series setup panels. Retain original Direction selector in Setup with existing choice primitives. Whisker group exposes color, width, opacity, dash and dash offset; cap group exposes length ratio, using original labels/ranges recorded in B3. Existing numeric primitives expand bounds to display valid saved values. Exclude only source-ineligible axis type/configurable tick controls, Cartesian labels/markers/shadow/connectMissingData and Switch Category / Series. Eligibility must not accidentally suppress axis labels, line/grid or caption controls.

Admission must inspect effective raw options before projecting them into a narrower style. Ordinary default miniature uses B3c's full-data, direction/configured-visibility inheritance; never force vertical or mirror transient legend hiding. Read-only source search of `terminalpro/src` finds no `miniChart` option producer; the original `hooks/useChartOptions.tsx` only toggles `chartMiniChartEnabled`, and current caller/generated/editor paths do not construct custom miniature series. Explicit `navigator.miniChart.series` is therefore an extension/saved-import input outside this ordinary Table/File baseline, not a missing ordinary control. Preserve its saved data unchanged. B3c has no explicit-custom-series input: detect it and return an explicit unresolved compatibility diagnostic rather than silently rendering the default miniature. Likewise detect explicit custom numeric tick arrays/steps not represented by the accepted style. This is outside-baseline admission, not accepted feature parity: a concrete reachable ordinary Table/File producer or saved fixture requiring either behavior blocks B3d acceptance until supported; an unavailable diagnostic cannot close that gap. No menu/toggle is disabled, hidden or relabeled complete. Tests must distinguish absent/default options from these explicit options and prove storage is retained.

B4 must exercise numeric category identities coinciding with financial extrema in the original. B3c intentionally retains horizontal category rows; original accidental category autoscale, if observed, requires the owner's explicit deviation decision. Do not describe it as already accepted. B4 also checks default horizontal miniature, singleton fractional ticks and long-label spacing in matched themes.

## File structure plan

Paths are relative to `vendor/workspace/terminalpro/src/components/General/Table/Chart/` unless stated. This table replaces B3d's reservation with an executable single-owner boundary.

| Paths | Responsibility |
| --- | --- |
| New `application/boxPlotSessionTypes.ts` | Family guard, typed intents, Box editor/ready projection types. |
| New `application/boxPlotSessionSelection.ts` | Existing setup/baseline join and concrete axis/editor metadata. |
| New `application/boxPlotAppearance.ts` | Family layering, Box defaults/inheritance and explicit-option admission. |
| New `application/boxPlotEditorState.ts` | Common panel eligibility and Box whisker/cap/direction values. |
| New `application/boxPlotSessionProjection.ts` | Mapper, legend/navigation callbacks and setup-ready output. |
| New `application/boxPlotEditorTransaction.ts` | Latest-state validation and original saved paths. |
| New `editor/box/BoxPlotControls.tsx` | Existing primitives for whisker/caps; direction passed to Setup. |
| Modify `AgChartView.tsx`, `caller/{useCallerDock.ts,themeInputs.ts,generatedOptions.ts}` | Real caller activation, gallery routing, family theme/generated options, ready/empty/host/editor wiring. |
| Modify `application/{comboSessionTypes.ts,applicationChartSessionTypes.ts,useApplicationChartSession.ts,applicationSessionDispatch.ts,applicationSetupSelection.ts,applicationSessionSelection.ts,applicationSessionSetup.ts,applicationSessionRuntime.ts,familyTransition.ts,comboSessionAssignments.ts}` | Family union/routing, freshness, setup policy, family transitions and Box dispatch. Preserve other family behavior. |
| Modify `application/effectiveAppearance.ts` | Narrowly widen `resolveCommonAppearance` family union for Box; reuse existing resolver without casts or copied implementation. |
| Modify `compatibility/editorBindings/{types.ts,selectApplicationEditorState.ts,mapApplicationEditorEvent.ts}` | Common Box editor eligibility and `box-plot` event path. |
| Modify `editor/{ApplicationCustomizeEditor.tsx,ApplicationSeriesEditor.tsx,ApplicationChartEditor.tsx,combo/comboEditorMode.ts,setup/ChartSetupPanel.tsx}` | Specialized mode in existing dock, Direction placement and original panel composition. |
| New Workspace `tests/unit/chart-application/{boxPlotProductionJoin.test.ts,boxPlotSessionOwner.test.tsx,boxPlotEditorControls.test.tsx}` | Real production projection, latest Widget transactions and rendered controls. |
| Modify Workspace `tests/unit/chart-application/callerRoute.test.tsx`, `tests/unit/chartTypeGallery.test.tsx` | Actual Table/File entry and existing gallery activation. |

If projection routing exceeds caps, the already reserved `application/applicationSessionProjectionDispatch.ts` may receive only cohesive family projection dispatch, after controller approval of measured need. No other extraction or new scaffolding is authorized. Every whole modified/new production file must pass 400 physical lines, 300 logical units and 50 per function using the existing inventory/checker. Controller registers new paths and explicit fork scope; no exceptions or generated-code disguise.

## Executable verification and handoff

Use existing `tests/unit/chart-application/vitest.config.mjs` with the three new application suites and existing caller route test, plus gallery command `node node_modules/vitest/vitest.mjs run --config tests/unit/chart-editor/vitest.config.mjs tests/unit/chartTypeGallery.test.tsx`. No browser/build/install/provider work belongs to B3d. Run focused changed Box/editor/session tests first; selected prior-family join regressions run once. Existing four Pie assertion failures reproduced at B3a are inherited, not new passes or permission to overlook additions.

Production-join assertions must inspect actual Box geometry/summary/raw tooltip values and direction-dependent axis bindings from real session output, not only `kind` or option presence. Cover capture -> setup aggregate once -> mapper; category/field order/removal to zero/recovery; same selected-field colors through legend; flags on/off with navigator/mini options; fresh resize request callbacks; failures reaching existing diagnostics/export invalidation. Reuse B3c engine tests instead of copying its geometry harness.

Session-owner assertions must edit each original saved path through latest Widget storage, reject stale and foreign commands without mutation, preserve inactive options on family return, retain valid dash arrays and out-of-slider saved values, and prove reinitialization from serialized saved state. Include overlapping external title/style edits to disprove stale baseline overwrite. UI assertions use actual rendered Setup/Customize panels: Direction, every whisker/cap control, main/common panels and source-ineligible exclusions. Verify effects and saved values, including inherited versus explicit whisker styles, light/dark theme changes and generated-common replacement. Explicit unsupported options must produce diagnostics without mutating saved data.

Run scoped Biome, the existing combined explicit-scope complexity gate and canonical strict TypeScript baseline/candidate comparison. The controller captured the B3d application baseline using `tests/unit/chart-application/session.tsconfig.json`: 2,713 inherited diagnostics, compiler exit 2, in `artifacts/chart-box/b3d-typing-baseline.log` and `.exit`. Use that identical command/config for candidate comparison, with no added diagnostics or owned suppressions. B3c compatibility typing is a different scope (3,427); do not compare across configurations. Record exact revisions, commands/exits and independent review decision in one local B3d record. Controller reconciles breadth and maintained milestone checkboxes only for established evidence. B4/B5 stay open; no source-only check establishes financial/application/visual acceptance or triggers publication.

**Acceptance:** B3d production join and source checks are accepted. B4 browser/FMP/visual acceptance and B5 publication remain open. See [verification](../../../artifacts/reviewed/chart-box/verification.md).

## Implementation review amendment

The initial contract was independently approved at SHA-256 `67fb754c83519409d34a43d3939c7f9a889c446816f2d29471515fa03c60e97b`. Source review and compiler checking identified two necessary shared integration changes: add Box's foreign-intent guard to `application/histogramEditorTransaction.ts`, and narrow the new ready variant in the existing `tests/unit/chart-application/comboProductionJoin.test.tsx` assertions without weakening them.

Preserve configured `series.visible` and `series.showInMiniChart` from saved options as well as transient legend selection. The original ordinary caller has no explicit producer for these leaves, but its saved family options pass them to the renderer. Extend only `echarts/boxPlotTypes.ts`, `boxPlotProjection.ts`, `boxPlotNavigator.ts` and `boxPlotNavigationWindow.ts` to carry optional configured field visibility. Default behavior must remain unchanged; the overview follows configured visibility and excludes transient legend state. Freeze original precedence with the independent reviewer before implementing it. Add focused regressions to existing `tests/unit/chart-compatibility/boxPlot.test.ts` and `boxPlotNavigator.test.ts`. This amendment preserves the existing contract rather than adding another unresolved admission. Whole-file caps and independent final review apply to these additional paths.



Original-source precedence confirmed by independent review: main visibility is transient legend selection, then configured visibility, then true; the legend can re-enable an initially hidden field. The overview includes only fields whose configured visible and showInMiniChart values are not false. Apply the same configured fallback during navigation reprojection and initialize legend selection consistently.

The same bounded extension also owns `echarts/boxPlotLayout.ts` for initial legend selection from actual enabled fields and `echarts/boxPlotAdmission.ts` for optional boolean validation. Within already owned applicationSessionRuntime.ts, invalidate capture when a family transition changes Box observation policy so returning from another family requests fresh raw observation capture. Verify both capture invalidation and recovery through the actual session owner.

Host integration review also requires a narrow echarts/lifecycle.ts change: initial selection and new-ID defaults must respect request.options.legend.selected, while retained native selection takes precedence. Existing tests/unit/chart-compatibility/lifecycle.test.ts verifies that the host does not re-enable configured-hidden fields on initial rendering and preserves native re-enabling. Existing other-family defaults remain unchanged. This is part of the same configured-visibility join.

A change in configured field visibility changes the Box legend scope, so external saved-option changes take effect. Ordinary re-renders with unchanged configuration preserve native legend selection. Verify this through the real session owner.

## Source acceptance

B3d editor/session activation is independently source-accepted at Workspace `ba98f00b91693f3a9c3ae7ba3dea8b42806dceb4`. Focused application, gallery and mapper/host checks pass 94 tests; 51 selected prior-family checks pass. Scoped Biome and whole-file complexity pass. Typing retains inherited diagnostics; see the reviewed comparison below. B4 identified-image/FMP/visual acceptance and B5 publication remain open.
