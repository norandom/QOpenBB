# Pie and donut application integration design

Connect accepted P2 through the existing Table/File caller, Widget transaction owner, chart host and dock. Use one integration owner for shared modules; a small optional label-control lane can work independently after the interface below is frozen. P2 is accepted. Independent Astra review approved this integration design on 2026-10-21; P3 source implementation is independently accepted; P4 browser and image acceptance remain open.

Local research in ignored artifacts/chart-pie/p3-seams.md and p3-controls.md records source locations, sizes and original controls. The [renderer design](pie-renderer-design.md) owns P2. Do not duplicate its six mapper modules or edit them during P3 without returning the changed contract to review.

## Integration contract

Keep `pie`, `donut` and saved `doughnut` as distinct caller/model spellings. Normalize `doughnut` to `donut` only for renderer/option-family lookup and gallery selection comparison. Continue to persist through `reduceSessionOptions`/the existing integrated reducer inside the latest functional Widget transaction. No new flag, storage branch, editor instance, chart hook or lifecycle owner is needed.

Add `isPieChartFamily` and the pie selection/projection types in `application/pieSessionTypes.ts`. Add one `kind: "pie"` member to `ApplicationChartReady`, using `Omit<ApplicationSessionReady, "editor">` plus the axis-free editor projection. The shared session may retain its existing inactive axis fields for family return; pie selection, appearance and rendering must not manufacture axes or consume them as a polar contract. Caller/session synchronization skips axis preference interpretation for pie so inactive Cartesian settings cannot change or invalidate pie geometry. Keep the existing axis preference path for every axis family.

`selectPieSession` resolves the current baseline/range/setup, then uses the existing setup projection with an explicit `pie-observations` policy. That policy permits empty numeric selection and independent units across rings. It permits transpose only after the session establishes that the requested family is donut/doughnut. Pie hides and rejects Switch Category/Series; donut exposes it in the supported ordinary ungrouped Enterprise journey. Inactive saved switch settings remain retained where original family switching retains them; a pie projection never applies transpose.

Aggregation and transpose run once in `projectOrdinarySetup`. Feed its projected snapshot into P1 assignments and P2 with `context.aggFunc` omitted, avoiding double aggregation. Keep the existing setup value-origin record and count-unit transformation. Build assignments from projected selected numeric IDs in order, so pie still takes the first field and donut retains every field, including fields produced by transpose. Each projection begins from the retained flat capture, never a previous aggregate. Donut transpose with no selected numeric fields returns zero assignments and retains setup recovery; guard the existing inverted setup path before reading the first effective column. Removing the last selected field while transposed must not invent empty per-category rings. Duplicate categories remain separate unless aggregation is enabled.

Add `normalizePieObservation` to a small `application/pieCapture.ts`; use it only for `pie-observations` in `gridCapture`. Finite numbers, zero and negatives survive unchanged; absent/null, nonfinite values and ordinary numeric strings become null for P2 omission. Preserve the original documented object-backed numeric extraction where applicable, with failed/nonfinite conversions becoming missing. Do not reuse histogram's Date-to-timestamp coercion for pie. Tests must distinguish primitive strings, valid original numeric wrappers and dates. Category validation and unsupported grouped/pivot/remote capture stay under the existing capture boundary.

`projectPieSession` builds the accepted `PieMappingInput`, calls `translatePie`, and exposes the existing `projectLegendSelection` callback. The callback closes over immutable current mapping input, supplies native slice-key selection and reruns the mapper; failures throw through the host's existing error/export invalidation channel. Use the current session/generation/family `legendScope`; do not store slice selection in Widget options. No navigator, mini chart, axes or dataZoom is added. Keep the ready host and dock when all fields are removed so the existing setup controls can recover the chart. An assigned empty/all-invalid ring retains P2's outline; the application no-data message must not turn that into filled geometry or disable chart mode.

## Appearance and editor reuse without artificial axes

Extract common caption/legend/padding/background/tooltip/palette resolution from `effectiveAppearance.ts` into `effectiveAppearanceChrome.ts`. Its input is source layers, selected palette and explicit inherited legend-stroke width; its result is `Omit<ResolvedApplicationAppearance, "axes" | "series">`. The existing `resolveCommonAppearance` calls this helper and continues to resolve its own axes/series. Preserve old outputs with focused common-appearance regressions. This is a shared-function extraction, not a second appearance owner.

`pieAppearance.ts` composes defaults, selected-theme common/family values and `composeAppearanceOptions` output in the existing precedence order. Resolve `donut` options for saved `doughnut`. Use the existing `font`, `caption`, `bool`, `number`, `child` and color primitives. `appearanceDefaults` needs only the fields it reads; narrow its input type to theme, family and seriesIds rather than supplying unused axisRuntime. Read the two pie label branches independently. Preserve engine-only saved rotation, ratios, callout colors/minAngle and sector positionOffset; leave unsupported paint-spacing parity under P4's existing limitation. P1 offset precedence remains fixed by the original Grid proxy. No radius/hole/rotation sliders are introduced.

Add pie/donut to active caller theme expansion and generated defaults. Both label channels receive the effective ordinary Table default enabled state. Reuse `createChartDisplayPolicy` with its family input widened to the actual supported application family; do not cast pie to a Cartesian type. P2 receives that policy's zero-decimal label/fiscal callbacks and retains its raw-locale pie tooltip behavior. Tooltip toggle/mode edits target `F.tooltip`, never `F.series.tooltip`. Narrowly amend `echarts/pieData.ts` so compact mode omits the fiscal/category heading while single and shared modes retain it; all modes keep the hovered item field/value. The original donut has no category key for shared cross-ring collection, so preserve item triggering and do not add shared-axis behavior. Keep formatting eager and immutable. Add mapper mode regressions and an editor-to-projection test.

Keep the existing `ApplicationEditorState` for axis families. Define `PieEditorState` as its common title/legend/padding/background/tooltips/series/shadow props plus `kind: "pie"` and the two label-control projections; it has no axes, markers or generic `series.label`. Widen only the chart-level editor prop union and narrow before existing axis-family rendering. Generalize `ChartTitlesPanel` to accept the explicit available caption IDs and values; pie supplies title/subtitle only. The existing `CaptionFields` receives only a present caption. Existing callers retain their four captions and current UI.

The existing Customize/Series composition renders common panels in the same dock, then the pie label groups for pie mode; axis groups are omitted as whole groups. Reuse `ChartSeriesStylePanel` with only Stroke Width, Stroke Opacity and Fill Opacity. Do not show Line Dash, Markers, Connect Missing Data, axis titles or generic Labels for pie. Use original visible names and bounds from the control inventory. Retain custom fonts, sizes and weight/style pairs through existing typography metadata and `fontLeaf`; selecting Predefined rehydrates the latest pair at commit time.

`pieEditorTransaction.ts` performs stamp/family/range/setup freshness checks, reselects the latest pie appearance and produces one patch through the shared reducer. Common intents reuse `mapApplicationEditorEvent` after its pie family admission and original-panel whitelist; rehydrate common title/legend font context directly from the selected axis-free appearance. New pie label intents use existing validation and `fontLeaf` helpers. Reject forged axis, marker, generic-label and line-dash edits for pie even if no corresponding control is rendered. Add minimal early rejection of pieLabel/pieCallout/pieSector intents in the existing XY and histogram transactions, and reject them at dispatch before combo/Cartesian handlers; verify forged cross-family edits leave storage unchanged. Do not teach the old axis-oriented rehydration/selection functions to accept fabricated bindings.

## Frozen leaf-control interface

The integration owner defines these types in `application/pieSessionTypes.ts` before optional UI fan-out. They carry edit requests and resolved panel values only; no saved path, stamp, reducer or mapper instance crosses the leaf boundary.

```ts
type PieLabelKind = "calloutLabel" | "sectorLabel";
type PieEditIntent =
  | { panel: "pieLabel"; label: PieLabelKind; edit: ChartLabelsEdit }
  | { panel: "pieCallout"; edit: {
      field: "length" | "strokeWidth" | "offset"; value: number } }
  | { panel: "pieSector"; edit: { field: "positionRatio"; value: number } };
type LabelPanelValue = Omit<ChartLabelsPanelProps, "onEdit">;
type NumericControl = Omit<ChartNumberInputProps, "onChange">;
interface PieLabelControlsProps {
  readonly callout: LabelPanelValue;
  readonly sector: LabelPanelValue;
  readonly calloutControls: Readonly<Record<
    "length" | "strokeWidth" | "offset", NumericControl>>;
  readonly sectorPosition: NumericControl;
  readonly onIntent: (intent: PieEditIntent) => void;
}
```

`PieLabelControls.tsx` composes two independently named `ChartLabelsPanel`s and existing `ChartNumberInput`s. Add an optional presentation `label` prop to `ChartLabelsPanel`, defaulting to `Labels` for existing callers; pie supplies `Callout Labels` and `Sector Labels`. The nested Callout group has no additional toggle. Numeric controls enforce both current bounds, with maxima expanded to retained saved values as the original does; use `ChartNumberInput`, not the looser `LegendNumberInput` text validation. The UI emits the typed intents above; its owner must not patch options or resolve font pairs.

## Writable scope and cap-safe split

Paths below are relative to `vendor/workspace/terminalpro/src/components/General/Table/Chart/`. The integration owner owns every listed path except the optional leaf lane. Any additional production path requires controller review of ownership and whole-file size before editing; the P2 files except the reviewed pieData tooltip amendment, host/lifecycle and unrelated chart families remain read-only unless a demonstrated join defect requires a separately reviewed amendment.

| Responsibility | Existing files allowed to change | New files |
| --- | --- | --- |
| Pie session and dispatch | `application/comboSessionTypes.ts`, `application/applicationChartSessionTypes.ts`, `application/useApplicationChartSession.ts`, `application/applicationSessionDispatch.ts`, `application/applicationSessionSelection.ts`, `application/applicationSessionRuntime.ts`, `application/xyEditorTransaction.ts`, `application/histogramEditorTransaction.ts` | `application/pieSessionTypes.ts`, `application/pieSessionSelection.ts`, `application/pieSessionProjection.ts`, `application/pieEditorTransaction.ts`, `application/pieEditorState.ts` |
| Capture/setup | `application/histogramCapture.ts`, `application/gridCapture.ts`, `application/setupProjection.ts`, `application/applicationSessionSetup.ts` | `application/pieCapture.ts`, `application/applicationSetupSelection.ts` |
| Family transition extraction | `application/comboSessionAssignments.ts` | `application/familyTransition.ts` |
| Appearance/display | `application/effectiveAppearance.ts`, `application/effectiveAppearanceDefaults.ts`, `application/types.ts`, `caller/themeInputs.ts`, `caller/generatedOptions.ts`, `caller/useCallerSessionInputs.ts` | `application/effectiveAppearanceChrome.ts`, `application/pieAppearance.ts` |
| Tooltip mode compatibility | `echarts/pieData.ts` | None; only eager mode-specific tooltip text composition |
| Common edit mapping | `compatibility/editorBindings/types.ts`, `compatibility/editorBindings/mapApplicationEditorEvent.ts` | None; reuse validation/valueMapping/typography helpers read-only |
| Caller/gallery/quick actions | `AgChartView.tsx`, `caller/chartInputs.ts`, `caller/useCallerDock.ts`, `editor/ChartTypeGallery.tsx`, `hooks/useChartOptions.tsx` | None |
| Dock/editor composition | `editor/ApplicationChartEditor.tsx`, `editor/ApplicationCustomizeEditor.tsx`, `editor/ApplicationSeriesEditor.tsx`, `editor/combo/comboEditorMode.ts`, `editor/setup/ChartSetupPanel.tsx`, `editor/titles/ChartTitlesPanel.tsx`, `editor/titles/CaptionFields.tsx` | None |
| Optional independent label lane | `editor/labels/ChartLabelsPanel.tsx` | `editor/pie/PieLabelControls.tsx` |

Perform these extractions before growing the shared seams:

- `comboSessionAssignments.ts` is 383 physical lines. Move its existing `rebuiltLocal`/commit implementation and ordered numeric-column helper into `familyTransition.ts`; preserve the public transaction entry points. Both combo assignment and gallery transitions use that single commit path. Do not duplicate family reducers or introduce circular imports.
- `applyApplicationSetupTransaction` is already 40 logical units. Move family-specific selection into `applicationSetupSelection.ts` and use a dedicated switch-eligibility predicate. Replace the existing test of `observationSnapshotPolicy` as a proxy for switch permission; donut is an observation policy that does allow switching.
- Extract common appearance as above before adding pie resolution. Keep `pieEditorState` responsible for panel projection/metadata and `pieEditorTransaction` for freshness and patching; do not grow the session projection into an editor resolver.

All modified/new production files must pass 400 physical lines, 300 logical units and 50/function, including shared modules as whole files. The existing checker/inventory foundation is already accepted; parent adds the new maintained paths and explicit fork change manifests. Tests/docs are exempt. Do not solve a cap breach through compressed code, fake state, an implicit exception or moving maintained logic into tests.

## Execution and acceptance

Use one integration owner through the final join. After reviewed types exist, an optional second implementer may own only `ChartLabelsPanel.tsx`, `PieLabelControls.tsx` and `tests/unit/chart-application/pieLabelControls.test.tsx`. The main owner owns all other code and tests, including wiring that leaf into the dock. These lanes have no overlapping writable path. Join only after the leaf renders both independently enabled fonts and emits every typed numeric edit, with keyboard/accessibility and retained-value checks. If the controller chooses one worker, use the same interface and boundaries sequentially. No partial activation/release is accepted between these steps.

Add focused `pieProductionJoin.test.ts`, `pieSessionOwner.test.tsx` and `pieEditorControls.test.tsx` beside current chart-application tests. Cover ordinary Table and File admission for all spellings; first-field pie/ordered donut rings; custom typography; exact saved paths; latest-state/stale-event protection; category/field ordering; aggregate on/off without double reduction; donut transpose and pie rejection; mixed-unit independent rings; invalid observations and empty recovery. Verify hidden controls are absent and forged edits rejected. Use the existing caller-route tests for real navbar/gallery selection and saved-alias highlighting, and existing family-transition/appearance tests for unchanged ordinary/combo/XY/histogram behavior.

At the join, verify native legend selection reaches P2's immutable reprojection callback, separate rings retain independent duplicate-category entries, resize/refresh preserve the current host and export revision, and entering/leaving pie restores applicable navigation controls without changing retained flags. Run scoped strict TypeScript, affected one-worker suites and the full explicit-scope complexity gate. Reuse existing test configurations; root gallery/editor tests need their existing config rather than assuming the chart-application glob includes them. The controller serializes heavy checks, reconciles inventory/breadth/docs checkboxes for P3 source acceptance only, obtains independent review and records exact revision/evidence.

P4 remains the identified-image gate for both themes, matched original/candidate controls and label fitting, thick-stroke appearance, real captured FMP values, refresh, save/reopen and export. P3's source tests do not establish those results and do not trigger an image publication by themselves.
