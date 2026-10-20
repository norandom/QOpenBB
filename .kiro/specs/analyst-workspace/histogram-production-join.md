# H3 histogram production join

Connect the accepted H1/H2 histogram implementation to ordinary Table/File charts through the existing session, editor and host. H3 starts only after H2 acceptance and independent review of this join. [The milestone](histogram-milestone.md) owns completion; [the mapper supplement](histogram-mapper-design.md) owns numerical rendering. This document records source inspection and planned checks, not implementation evidence.

## One owner and one integration task

Keep `useApplicationChartSession` and Widget transactions as the state owner. Add histogram selection/projection/edit modules; extend existing family discriminants and routing. Never call ordinary Cartesian projection with a fake family, create a second widget state owner, or persist ECharts options. Histogram remains available through the existing gallery and ordinary entry point.

H3 is one cohesive implementer task because capture policy, setup transitions, editor projection and host navigation share contracts. H4 may prepare only its separately owned new browser files. H3 owns the component/host tests below; H2 modules remain read-only after acceptance. Controller owns inventory, source lock, breadth, evidence, commits and publication.

## Frozen capture and setup contract

Add explicit snapshot policy `"histogram-observations"` alongside `"xy-coordinates"` in `compatibility/snapshotTypes.ts`. Both allow empty numeric selection at structural validation; only histogram capture normalizes its source values. Propagate the policy through `GridCaptureInput`, retained capture, setup transitions, initial capture, category recapture, added-series recapture and post-refresh validation. No missed empty-selection checkpoint may leave the first re-added field unusable.

`application/histogramCapture.ts` owns normalization: retain finite numbers, convert valid native Dates to timestamp numbers, unwrap recognized native Number values, and map null/undefined, ordinary numeric strings, invalid dates and nonfinite numbers to null. Do not invoke an arbitrary object's `valueOf`, parse strings or change ordinary/XY/combo capture. Apply normalization before the finite-JSON snapshot validator and before category aggregation. Structural failures and unsafe property access remain visible errors.

Extend setup's axis policy with `"histogram-observations"`: allow empty selections, retain numeric column order and unused fields, reject category/series inversion, and skip the ordinary all-columns-same-unit check because only the first selected numeric field is plotted. Preserve the existing category aggregation and source-row provenance. First selected numeric descriptor supplies X; aggregate count changes X to observation counts, while histogram Y still counts the resulting rows. None category retains unique row identities and hides aggregation controls.

Force histogram's effective `switchCategorySeries=false` without erasing an inactive saved setting used by another family. No selected numeric field produces the supported empty chart and existing empty-state message. Removing the last field, refresh, category change and re-adding the first field must all remain recoverable.

## Saved options and editor

`histogramAppearance.ts` composes the same ordered layers as XY: defaults, theme common, theme histogram, composed common, composed histogram. Resolve each numeric-axis leaf in layer order; do not merge all layers before resolving shared-versus-positional precedence. Reuse `resolveXyAxisPositions` and `xyPositionPatch` for their numeric position semantics only. X remains bottom/top, Y left/right. Histogram uses concrete number axes while existing editor IDs remain category/number.

Resolve saved series options from `histogram.series.*`, including binCount, bins, fill/stroke, widths/opacities/dash, labels, tooltip and shadow. Add histogram generated options and theme-family handling explicitly; `effectiveAppearanceLayers.ts` currently falls back to bar and must not be used for this projection. Use `resolveCommonAppearance` with a narrow histogram type extension and histogram-local defaults; do not broaden the ordinary family validator.

Add `kind:"histogram"` to the ready/editor mode unions and a stamped `panel:"histogram"` bin-count intent. Reuse common editor bindings for existing controls; the histogram transaction validates family/stamp, resolves current selection, writes only its option patch through `reduceSessionOptions`, and preserves unrelated/inactive saved options. Reject XY/combo-only events. Keep legend, shadow, labels, numeric axis positions, stroke width/dash/opacity, fill opacity, tooltip, titles, background and padding reachable. Hide marker, connection and inversion controls exactly where the original does.

The single new control reuses `ChartNumberInput` with exact visible label **Bin count** and accessible numeric input name **Bin count value**. Retained Grid source 19088 establishes the label; `initBins` at 14131-14138 sets the displayed value to `(bins ?? calculatedBins).length` and maximum to `Math.max(value,20)`. The control minimum is zero. Preserve this display precedence even when binCount overrides bins for calculation. Do not display the saved count directly or add an extra calculated-count label, help text, badge or replacement control. Numeric saved fractional counts remain valid under H1; the typed input must not impose integer-only validation.

Changing the control writes `histogram.series.binCount`; it never writes calculatedBins or deletes explicit bins. On a new stamped projection, the displayed value comes from the explicit bins or the actual H1 result. The equal-integer repair remains recorded in evidence and preserves the saved requested count.

## Retained geometry and navigation

Build main options once per accepted data/options projection. Retain their resolved interval data and mapper input in the projection closure. Legend, zoom, pan, reset and mask updates consume that retained geometry; they do not invoke H1 or rerun category aggregation. A real data refresh or bin-setting edit creates a new projection and may recalculate bins.

The H2 worker and join author agreed this narrow existing-series-module export, subject to H2 review:

```ts
export function createHistogramRenderer(
  input: HistogramMappingInput,
  data: readonly HistogramDatum[],
  labelsEnabled = input.style.series.labels.enabled,
): NonNullable<CustomSeriesOption["renderItem"]>;
```

`HistogramDatum` is exported by H2 types. Construct overview options using the retained data and `createHistogramRenderer(input,data,false)`; do not call the full mapper again. The generic overview clone's `label.show=false` cannot suppress text captured inside a custom renderItem callback, so this explicit seam is required. Main and overview retain identical boundaries/frequencies and distinct axis/series identities; overview remains silent and has no tooltips. No H2 ownership transfer is needed if this export is accepted with H2. If it is absent or changes, stop the join seam for controller review rather than editing an active H2 file.

`histogramNavigator.ts` may reuse `cartesianNavigator` for the existing slider, mask and overview layout, replacing the cloned overview custom renderer as above. Use numeric X domain including empty boundary bins. Main slider and histogram inside navigation target only main X axis index 0; overview always uses full data. Set `filterMode:"none"` so endpoint filtering cannot remove a partially intersecting interval or change frequency. Native plot clipping crops geometry.

Use a distinct inside ID, `openbb-histogram-inside`, alongside the existing `openbb-navigator` slider. Extend `retainNavigatorExtent` to synchronize this ID; retain normal session/family reset behavior. Do not call `xyNavigator`, `xyNavigationWindow`, their minValueSpan calculation or a four-observation guard. No minimum bin/observation count limits a histogram window.

`histogramNavigationWindow.ts` reads retained intervals and the current numeric window. A bin intersects inclusively when `upper >= windowLow && lower <= windowHigh`, matching retained Charts 45010-45028. Automatic Y domain is zero through the maximum frequency of intersecting occupied bins, respecting supplied Y min/max. No intersection yields empty geometry/axis behavior without NaN/Infinity; moving/resetting the window restores it. Preserve the H2 direction-specific excluded-bound rule; an outward bound extends normally.

Extend lifecycle's existing datazoom handler with a histogram branch that reads retained options directly. It must not route histogram zoom through `legendOptions(pending)`, because that callback may reproject the mapper. Histogram legend callbacks similarly apply visibility to retained full geometry. Retain full overview data on legend toggles, autoscale visible main data, and preserve the single Frequency legend identity. Extend double-click reset eligibility to histogram and keep wheel zoom/pan behavior. Guard reentrant events with the existing `applying` owner and keep export invalidation/error handling unchanged.

## Exact ownership and measured baseline

All paths below are relative to `vendor/workspace/terminalpro/src/components/General/Table/Chart/`. Shared files were inspected on 2026-10-20 at Workspace `42170015627a7a09c1245b2dbf76e602b247d235` (H1 source); H2 was active separately. Read-only measurements used pinned Node 24.22.0 and `tools/quality/syntax_units.ts` on explicit file paths. P/L/F means physical lines, file logical units and maximum callable units; `-` means no callable. This inventory is not the final complexity gate.

| Shared writable file | P/L/F | Bounded change |
| --- | --- | --- |
| `AgChartView.tsx` | 292/93/11 | Histogram admission, empty state and editor mode |
| `caller/generatedOptions.ts` | 42/8/3 | Generated histogram option branch |
| `caller/themeInputs.ts` | 168/42/9 | Histogram theme normalization |
| `caller/useCallerDock.ts` | 62/24/7 | Existing family transaction admission |
| `application/comboSessionTypes.ts` | 25/26/1 | Extend ApplicationChartFamily |
| `application/applicationChartSessionTypes.ts` | 33/23/- | Histogram ready/intent discriminants |
| `application/applicationSessionCapture.ts` | 80/29/14 | Histogram policy across capture/recovery |
| `application/applicationSessionSetup.ts` | 214/84/40 | Histogram selection and all recapture checkpoints |
| `application/applicationSessionSelection.ts` | 155/73/17 | Suppress effective histogram inversion |
| `application/applicationSessionDispatch.ts` | 150/56/27 | Stamped histogram editor dispatch |
| `application/useApplicationChartSession.ts` | 231/77/10 | Projection/edit hook and lifecycle closure |
| `application/gridCapture.ts` | 202/93/22 | Delegate histogram value normalization |
| `application/types.ts` | 182/112/- | Capture policy type |
| `application/setupProjection.ts` | 263/95/22 | Histogram setup policy |
| `application/setupTransitions.ts` | 178/82/26 | Propagate structural policy |
| `application/effectiveAppearance.ts` | 238/73/20 | Narrow common-appearance family type extension |
| `compatibility/snapshot.ts` | 110/122/29 | Allow empty histogram selection only |
| `compatibility/snapshotTypes.ts` | 49/37/- | Named structural policy union |
| `compatibility/editorBindings/types.ts` | 143/143/- | Histogram family in editor contracts |
| `compatibility/editorBindings/selectApplicationEditorState.ts` | 143/33/10 | Admit explicit histogram selection |
| `compatibility/editorBindings/mapApplicationEditorEvent.ts` | 138/78/29 | Preserve histogram option branch |
| `editor/combo/comboEditorMode.ts` | 17/13/- | Histogram mode contract |
| `editor/ApplicationSeriesEditor.tsx` | 59/19/2 | Insert original bin control |
| `editor/setup/ChartSetupPanel.tsx` | 250/96/10 | Hide histogram inversion without redesign |
| `echarts/lifecycle.ts` | 248/181/28 | Retained histogram window and reset dispatch |
| `echarts/cartesianNavigator.ts` | 135/45/15 | Retain histogram inside range |

New H3 production files are `application/histogramSessionTypes.ts`, `histogramSessionSelection.ts`, `histogramSessionProjection.ts`, `histogramAppearance.ts`, `histogramEditorTransaction.ts`, `histogramCapture.ts`; `editor/histogram/HistogramBinControls.tsx`; `echarts/histogramNavigator.ts`, `histogramNavigationWindow.ts`. Application filenames after the first inherit `application/`. Split only these responsibilities; any additional helper or shared path requires an updated controller-approved handoff.

Read-only reuse includes `application/comboSessionAssignments.ts` (383/136/19): its generic non-combo family transaction already carries the extended family union and should not grow. The gallery already contains Histogram; `chartTypeGalleryCatalog.ts` needs no activation edit. `EChartsHost.tsx`, `ApplicationChartEditor.tsx`, `ApplicationCustomizeEditor.tsx`, `ApplicationAxisEditor.tsx`, metadata/rehydration helpers and `xyAxisPositions.ts` already expose usable contracts; do not edit them speculatively. If actual type checking disproves a reuse assumption, identify the exact failing contract before extending ownership.

Every modified production file must pass 400 physical lines, 300 logical units and 50/function. `applyApplicationSetupTransaction` starts at 40/function; extract a cohesive histogram selection/policy helper before exceeding 50. No implicit exception or compressed statements. Controller updates maintained inventory and explicit changed-fork manifests before acceptance; run the existing combined checker, not a hand-count substitute.

## Component gate and later application acceptance

H3 owns new `tests/unit/chart-application/histogramProductionJoin.test.ts`, `histogramSessionOwner.test.tsx`, `histogramEditorControls.test.tsx` and `tests/unit/chart-compatibility/histogramNavigator.test.ts`. H2's existing histogram tests and H4's new browser files remain separately owned. Reuse established fixtures/configurations; controller owns any necessary shared fixture edit.

Focused tests must establish:

- The 40-quarter FMP-shaped selection chooses revenue when explicitly selected first, even though fiscalYear is numeric; unused columns cannot affect bins, unit checks or extents. None category yields 40 observations. Separate duplicate-category sum/avg/count cases verify aggregation before binning and retained provenance.
- Null, missing, finite signed values, invalid/native dates, numeric wrappers and numeric strings normalize only under histogram capture. Snapshot structural failures still fail. Mixed unused units, empty selections, refresh, category recapture and first-field re-addition recover.
- Bin count has the exact visible/accessibility names, writes binCount, displays explicit-versus-calculated length with original precedence, retains fractions and explicit bins, and adds no extra UI. Common controls and top/right axis edits change their resolved effect, survive family changes and preserve stale-command rejection.
- Saved histogram format outranks theme as specified; positional/common axis precedence, fill/stroke, widths/opacity/dash, labels/shadow and inactive settings persist. Family transitions preserve previous XY/combo configurations.
- Numeric windows intersect full intervals, including a partially visible bin and boundary-touching bin. Counts/boundaries are unchanged during zoom/pan/reset/legend actions; instrument H1/aggregation call counts to prove no recalculation. Mini-chart labels are absent while main labels remain enabled; overview values stay complete.
- Host resize, refresh, legend reset and export use the current revision; no extra listeners, stale exports, event loops or console errors. Empty windows and excluded bounds recover; outward bounds extend.

Use selected files with the existing application and compatibility Vitest configurations at one worker, scoped TypeScript, affected setup/capture/transaction/host regressions and the combined complexity gate. One shared integration run follows the source join. No build/provider request belongs to this drafting task.

Independent source review precedes the H4 image-only browser gate. H4 still owes actual controls/theme, real FMP values and fiscal provenance, refresh, save/reopen, decoded export, navigator/mini-chart interactions and previous-family regressions. Automatic tick/outer-extent appearance remains the H2-recorded comparison obligation; do not mark visual parity complete from component tests. Reconcile owning checklists/breadth with actual evidence, and publish only after the completed milestone's review.
