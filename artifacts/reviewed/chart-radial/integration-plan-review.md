## Review Verdict

- VERDICT: APPROVED
- TASK: RC3 serialized integration plan review only.
- PLAN: `rc3-plan.md`, SHA-256 `76b51fec065fc3086a7c9d2857b22f917cb49d92ac9e017dc3f8cd3c010caf01`.
- SOURCE: Workspace HEAD `fa7f464bf7ca95248b755971c08ffcd5730236ae`, inspected 2026-10-24. Active RC1 files are provisional and were not accepted by this review.
- MECHANICAL_RESULTS:
  - Tests: NOT RUN; prohibited for this read-only plan review.
  - Builds/browser: NOT RUN.
  - Plan diff: no tracked diff returned; the ignored artifact was read directly.
  - Static checks: SPOT_CHECKED against actual source owners and existing test fixtures; no lint/type/complexity execution claimed.
  - Boundary: WITHIN the proposed 20 existing production files, one new projection, five existing test files, and controller-owned inventory/evidence manifests.
  - Boundary audit: CLEAN at planning level; no shared renderer/control ownership introduced.
  - RED phase: N/A for a plan. Behavioral implementation still requires relevant RED evidence and independent review.

The amended plan is approved after correction of the palette defect documented below. It does not authorize starting integration before RC1N/RC1P independent acceptance and the joined renderer check, and it does not establish RC3 or packaged application acceptance. RC2 remains an accepted inactive dependency under the milestone record.

## Reviewed ownership

All production paths below are relative to `vendor/workspace/terminalpro/src/components/General/Table/Chart/`. A single serialized integration owner may edit these 20 existing files:

1. `application/comboSessionTypes.ts`
2. `application/applicationChartSessionTypes.ts`
3. `application/useApplicationChartSession.ts`
4. `application/applicationSessionDispatch.ts`
5. `application/applicationSetupSelection.ts`
6. `application/applicationSessionSetup.ts`
7. `application/applicationSessionRuntime.ts`
8. `application/histogramCapture.ts`
9. `application/gridCapture.ts`
10. `compatibility/snapshotTypes.ts`
11. `compatibility/snapshot.ts`
12. `application/setupProjection.ts`
13. `caller/chartInputs.ts`
14. `caller/generatedOptions.ts`
15. `caller/themeInputs.ts`
16. `editor/ApplicationCustomizeEditor.tsx`
17. `editor/ApplicationSeriesEditor.tsx`
18. `editor/combo/comboEditorMode.ts`
19. `editor/setup/ChartSetupPanel.tsx`
20. `AgChartView.tsx`

The sole new production owner is `application/radialSessionProjection.ts`. Extend only the five named existing tests under `tests/unit/chart-application/`: `nightingaleSessionOwner.test.tsx`, `nightingaleEditorControls.test.tsx`, `callerRoute.test.tsx`, `callerInputs.test.ts`, and `radarCapture.test.ts`. The controller retains scope manifests, `.kiro/complexity-budgets.json`, and `.kiro/breadth.toml`. Renderer, accepted controls, public contracts, host lifecycle, other family transactions and gallery/button owners remain outside this write scope. Any further extraction needs a reviewed ownership amendment.

## Findings

1. FYI: The additional `histogramCapture.ts` owner is necessary. Its `observationSnapshotPolicy` currently recognizes Radar/Nightingale but not either Radial model name. The named policy must reach grid normalization, snapshot empty admission and setup validation/sanitation together. The plan includes these seams and preserves aggregate-before-invert behavior.
2. FYI: Root presence is a real source seam. `AgChartView.tsx:createRangeChart` currently assigns `seriesGroupType` unconditionally. Conditional own-property spreading repairs absence while retaining explicit undefined. `applicationSessionRuntime.ts:sessionAssignmentKey` already captures presence and value; the planned editor and setup group keys must use the same distinction. The source selection correctly defaults absent/undefined Radial grouping to `grouped`. Appearance/setup commits must not materialize that default. Treat the planned `Object.hasOwn` regression as required coverage of this change; it fits the explicitly owned caller test file even if the preferred fixture needs adjustment.
3. Important, RESOLVED on re-review: The original proposed extension of Nightingale background-stroke substitution to both Radial names is incorrect. `.kiro/specs/analyst-workspace/radial-contract.md:45` explicitly prohibits inheriting Nightingale background strokes; `artifacts/chart-radial/original-contract.md:62` pins the original palette-fills-and-strokes rule. `caller/themeInputs.ts` currently supplies standard light/dark strokes for non-Nightingale families without an explicit palette. Preserve that Radial behavior: absent palette uses standard strokes, supplied stroke arrays survive, and the existing partial-palette fallback remains. Theme names must not change provenance. Add caller coverage for both families/modes, custom palette under a built-in name, absent palette under a custom name, and a stroke-width-only edit exposing palette strokes. Explicit user stroke/default-width handling remains in accepted RC2. Opposite-axis parameter projection remains a valid planned change. The controller amended the table, palette invariant and caller test requirements; I reread all three and verified that the reviewed plan now expressly excludes Radial from Nightingale background substitution, retains standard/supplied strokes, and requires the discriminating stroke-width-only check.
4. FYI: The central foreign-panel rejection is an appropriate bounded seam. Preserve outer stamp/family/assignment validation, reject all three Radial-only panels before neighboring family transactions, and retain local range/setup/root comparisons. Do not broaden accepted panel unions through casts without those runtime checks. The existing session-owner tests contain direct transaction, queued external change, grouping-without-recapture and lifecycle cases suitable for extension.
5. FYI: `ApplicationSeriesEditor.tsx` otherwise routes an axis-less Radial editor into Pie controls; the explicit shared polar branch in the plan prevents that. The inherited `ApplicationChartEditor` composition derives its props from the owned customize editor and does not require another owner. Keep Radar markers conditional and reuse the existing Set Up Group Type region.
6. Suggestion: The plan calls `26f1c8c` a root baseline although the milestone identifies it as the Workspace geometry revision. Record repository-qualified source identities in the implementation handoff. The stale draft header in `radialContracts.ts` is not evidence that its accepted declarations may be changed during RC3; use the frozen contract identity and keep any header maintenance separately owned.

## Completion conditions

Independent implementation review must inspect exact revisions and meaningful focused test results, including foreign controls, captured absent/undefined/grouped roots, both axis directions, palette provenance, raw missing observations, count formatting, empty refresh/recovery, native legend selection and stale queued callbacks. Retain existing Nightingale expectations and the original gallery, flags, toggle predicates and buttons. No new harness, feature or flag is approved.

Check every modified production file as a whole against 400 physical lines, 300 logical units and 50 units per callable using the existing inventory-backed combined gate. This review does not establish available logical-size headroom. Scoped lint/type diagnostics and exact manifests must accompany focused application/compatibility verification; planned checks must remain planned in breadth records. RC4 still owns identified-image browser geometry, real financial values, export, appearance comparisons and final fresh-session persistence.

- REMEDIATION: The blocking palette issue is resolved in the reviewed plan hash above. No further blocking plan remediation; preserve the stated prerequisites and completion conditions.
- SUMMARY: The amended RC3 plan covers the actual application seams and preserves the frozen Radial palette contract; renderer acceptance, integration verification and packaged application acceptance remain separately gated.

## RC3 root-presence scope amendment

- VERDICT: APPROVED
- SCOPE: Add `compatibility/optionState.ts` to the same serialized integration worker's production ownership, and extend existing `vendor/workspace/terminalpro/tests/unit/chart-compatibility/optionState.test.ts`. The amended boundary is 21 existing production files plus the new projection and six existing test files. No accepted renderer/control ownership changes.

Source inspection confirms that `model()` currently passes every ordinary model-root property to `copy(item, path, false, ancestors)`, which rejects undefined. Thus a model with an own undefined `seriesGroupType` cannot currently satisfy the already approved three-state capture/staleness contract. The bounded change is to assign undefined only when `key === "seriesGroupType" && item === undefined`; all other values continue through the existing strict copy call.

This exception belongs after `fields()` validation inside the model-root loop. Retain own enumerable data-property requirements, plain-object checks, accessor rejection without getter invocation, cycle detection, chartType validation, existing chartOptions semantics and strict recursive copying. In particular, do not set the general copy runtime flag to true and do not admit nested undefined group fields. The field remains preserved data at this compatibility boundary; accepted family selection still validates actual group values.

Required focused evidence: root and partition initialization, populated partition synchronization and retained previous baseline preserve own undefined and distinguish it from absence and grouped. Keep rejection of unrelated root undefined and chartType undefined; add a nested `seriesGroupType: undefined` negative case and a root group accessor case with zero getter calls. Retain existing nonenumerable/symbol/plain-object/cycle checks. Extend the already owned RC3 session test to prove that external absent/undefined/grouped transitions reject stale editor/setup commands.

Mechanical result: read-only inspection and PowerShell physical count found 200 lines in the pre-change production file. No tests or type/logical-size checks ran in this amendment review. Include the whole changed file in the existing 400/300/50 inventory gate and run the focused compatibility regression with the integration evidence. Approval concerns the exact scope and exception only; it does not accept unfinished code or waive RC1/RC3 verification prerequisites.
