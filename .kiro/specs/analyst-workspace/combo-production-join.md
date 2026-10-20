# Combination chart production join

C3c controls and C4b routing form one cohesive implementation task. The accepted C1/C2/C3a/C3b helpers and C4a navigator are dependencies. This source-reviewed Astra contract connects the existing editor/session owner; it introduces no parallel persistence owner or feature flag.

## Session boundary

Add an `ApplicationChartReady` discriminated union: ordinary `ApplicationSessionReady` plus `kind: "cartesian"`, or the same ready fields plus `kind: "combo"` and `combo: { assignments, geometry, activeGeometries }`. Types use the accepted combo assignment/geometry exports.

Add `projectComboSession(storage, inputs: ApplicationSessionInputs<ComboChartType>, state)` returning the combo ready variant through the existing `SessionResult`. Broaden the existing `useApplicationChartSession` input to `ApplicationSessionInputs<ApplicationChartFamily>` and its projection result to this union. Preserve existing host, resize, freshness and ordinary editing callbacks.

Add `onComboAssignment(colId, edit)`, `onComboGeometry(geometry)` and `onChartType(chartType)` on that existing hook. Assignment and family callbacks call accepted C3a transactions; Customize calls accepted C3b with the currently rendered geometry. Geometry selection validates active geometry and changes only existing `local.comboGeometry` plus render revision. All persistent edits use the existing functional Widget transaction.

## Projection and lifecycle

The combo projector calls `selectComboSession`, then `translateCombo` with the projected snapshot, resolved assignments/style, display policy and viewport. Preserve neutral count formatting.

Generate full overview options without legend filtering. Every combo exposes `projectLegendSelection`, remapping the main view with selection and passing the unchanged full overview to the accepted navigator. Preserve axis identity/palette order and same-scope range retention. Include chart identity in `legendScope`: family changes reset stale legend membership; appearance/data refresh retain interactions.

Scope ownership remains tied to widget/state address and grid API. The current family-dependent re-registration must not discard the live custom cache. Validate incoming family against committed baseline; distinguish accepted family transitions from external model replacement rather than removing equality checks. Advance/invalidate revisions appropriately. Saved builtin normalization to Custom Combo must not cause repeated initialization or writes during render.

Data/range rebuilds clear concrete combo overrides; appearance edits retain them. Preserve semantic category type across data rebuilding and keep concrete positions transient. Existing setup transactions choose ordinary or combo selection/projection policy while retaining recapture, range and stamp checks.

## Existing editor composition

Use a discriminated editor mode: ordinary, or combo with assignments, selected geometry, active geometries and assignment/geometry callbacks. Keep the dock and existing panel styling. Set Up adds selected-column type/secondary-axis controls; the original combo inversion restriction remains. Customize adds area/bar/line geometry selection inside Series, then reuses existing controls.

Route live gallery choices through `session.onChartType`; the previous direct caller mutation cannot retain the live custom cache. Preserve docking, keyboard ordering, expansion and ordinary chart behavior.

## Exclusive ownership

- New `application/comboSessionProjection.ts` and `application/applicationChartSessionTypes.ts`; a cohesive transaction-dispatch extraction if needed.
- Existing `useApplicationChartSession.ts`, `useApplicationSessionScope.ts`, session runtime/setup and family-neutral capture typings.
- `caller/useCallerSessionInputs.ts`, `AgChartView.tsx`; cohesive dock/live-chart presentation extraction where required.
- Existing editor composition, new combo assignment/geometry controls, and extraction of the existing Series panel.
- Focused application-session/component tests and a maintained browser regression.

Do not silently modify accepted C3b appearance/editor helpers or C4a navigator; report a concrete contract defect before widening ownership. Every touched production file must pass 400 physical lines, 300 logical units and 50 units/function. The existing caller/hook are near the physical cap, so extract cohesive presentation/dispatch responsibilities as needed.

## Acceptance

Independently test actual builtin/custom transitions and live-cache retention, assignment/geometry edits, mixed-unit setup, refresh, full-overview versus hidden-main behavior, stale-command rejection and ordinary-chart regressions. Verify controls in the existing editor composition, not a substitute test UI.

This task removes the remaining source admission barrier. It does not by itself establish real application or image acceptance. The milestone still requires actual FMP data, save/reopen, export, console/network diagnostics and independent end-to-end review before image publication.
