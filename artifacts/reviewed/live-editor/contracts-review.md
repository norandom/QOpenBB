# Live editor contract review

Review date: 2026-10-18. Scope: task 2.69 draft contracts only, before consumer dispatch, including focused re-review of the initial three findings. Root revision `a190a9e3ba94ebabd71923d68079d076b50e783e`; Workspace revision `bc202e457087794e984b1bd4d44518a868560811`. Original Workspace source reference: `38dffc33389aca0e4a87e0e88d42f7067aa220df`.

## Review Verdict

- VERDICT: APPROVED
- TASK: 2.69 shared contract review only
- MECHANICAL_RESULTS:
  - Tests: N/A for this declaration/draft review. No runtime acceptance claimed.
  - TBD/TODO grep: CLEAN in the corrected contract drafts; `rg` returned 1 with no matches.
  - Secrets grep: CLEAN for the targeted credential assignment patterns; this was a spot check, not a security certification.
  - Static checks: SPOT_CHECKED imported panel names, actual panel props, finite event fields, new type-only dependencies, existing snapshot and reducer contracts. All three draft TypeScript files exactly match relocated production bytes. Physical lines: appearanceModel 87; axisStructureTypes 37; editorBindings/types 143. The controller reports latest four-file lint and combined complexity pass, with compilation reaching only known `ds/plugins/typography.ts:1 TS2578`; this reviewer did not rerun those commands or certify full compilation.
  - Boundary: WITHIN. Reviewer wrote only this report. Contract copies were placed in production by the controller during review; no consumers were dispatched.
  - Boundary audit: CLEAN for corrected shared contracts; all three initial findings resolved below.
  - RED phase: N/A, declarations and source-contract review only.

## Corrections accepted

1. **Paired axis writes:** the manifest now defines both position branches and original first-defined read order; AxisBinding carries logical axis identity, actual type and direction. This matches the inspected source methods cited in initial finding 1.
2. **Structural state:** new `axisStructureTypes.ts` separates runtime concrete axes/internal categoryAxisType from the original serializable override patch. Required `AppearanceInput.axisRuntime` exposes current structure to the resolver. The manifest freezes capture of old style, literal crosshair transfer, type/time-format changes and paired reapplication. Source comparison included bundle 52177-52286, 52355-52411 and 47629-47651. Position/time-format events produce runtime changes and an empty appearance patch. Original structural nonpersistence is explicit; no saved field is invented.
3. **Consecutive events:** `ApplicationEditorCommand` now carries an intent stripped of firstStyle/font/binding/manual-angle context. Rehydration takes latest selection and bindings inside the functional Widget update. The manifest requires replay-safe accepted runtime ordering. Synchronous stamp validation checks originating address/generation/data identity and uses the current full stamp; delayed work retains unchanged exact revision validation. These contracts resolve the stated lost-update mechanism, subject to implementation tests.

The initial verdict was REJECTED. The original findings below are retained as review history, not outstanding remediation.

Canonical consistency was checked: the live integration design's Session and persistence section and task 2.77 now explicitly preserve the original structural-axis restore limitation alongside Auto Rotate. Neither claims direct structural-value round-trip parity.

Controller-attributed verification: lint of the four production declaration files exited 0; `tools.quality.complexity` with `artifacts/live-editor/checks/{workspace,data_api}-changes.json` exited 0; the existing chart-application `tsconfig` compiler run exited 1 with only known `typography.ts:1 TS2578`, without new diagnostics. These results were supplied by the controller and are not runtime evidence.

## Initial findings, resolved

1. **Important: axis theme edits must write both original positions.** `contracts/field-manifest.md:5` defines `P` as the current position and says edits write `F.axes.A.P`. The original bundle's `setCartesianAxisThemeOverrides` at lines 52334-52354 passes `[bottom, top]` for xAxis and `[left, right]` for yAxis. `assignChartAxisThemeOverride` at 52448 writes every supplied position. `retrieveChartAxisThemeOverride` at 52428 checks that same ordered pair. A single-position patch leaves stale styling after a position switch and does not reproduce the saved leaves. Freeze the paired write and source read order for all axis typography/title/line/grid/tick edits. Keep logical category/number identity separate from the current concrete option type, including category axes switched to number or time.

2. **Important: structural axis transitions are deferred and conflate internal model state with persisted fields.** `contracts/field-manifest.md:27` explicitly leaves the exact model/options transaction for a later freeze, although task 2.69 requires it before consumers. `ApplicationAxisStructureEvent` usefully separates structural events, but the actual result contract is missing. Original type changes first retain applicable prior axis overrides, change concrete `axes[0].type`, update internal `categoryAxisType`, set the label format when entering/leaving time, then reapply the previous effective axis overrides (bundle 47629-47651, 52355-52397). Position/time-format changes update the selected concrete axis. Crucially, `getChartModel` at 45061 exports neither concrete axes nor `categoryAxisType`; `chartOptions` comes from `getChartThemeOverrides` at 41231, which returns only `theme.overrides`. The original `hooks/useChartOptions.tsx` callback saves this returned model and merged override options. Freeze typed runtime structural state separately from the original serializable model/option update, with original reopen behavior stated explicitly. Do not fabricate persisted `categoryAxisType`, concrete `axes`, or `F.axes.category.type` fields. Any original persistence limitation is a source-backed limitation to disclose, not permission to change the envelope.

3. **Important: latest storage alone does not make contextual event patches safe for consecutive edits.** The grid event at `contracts/compatibility/editorBindings/types.ts:49` carries a `firstStyle` supplied by the displayed control view. A dash edit followed immediately by a color edit can send the old dash in the second patch and erase the first edit, even when the reducer uses latest Widget storage. The same freeze must govern binding identity and other retained contexts. Specify that the session rehydrates dependent patch context from the latest selected model/baseline and effective settings inside the functional `updateWidget(prev => ...)` transaction before mapping. The Widget owner evaluates functions against current reducer state (`components/widgetSync/updates.ts:reduceWidget`); use that owner, with no side effects inside replayable updaters. Validate the originating view's address/generation/data identity, then use the current accepted synchronous render stamp; delayed completions retain exact revision checks. Do not reuse `applyColumnEdit` unchanged: it rejects unequal render revisions and covers only the old column event subset. Freeze a concrete transaction input/result or an equivalently precise handoff before declaring 2.69 complete. Future focused tests must include dash-then-color without a React commit, two independent scalar edits, and obsolete data/address rejection.

## Contracts that can be retained

The explicit raw-observation policy is sound for this boundary: it permits missing metadata without inferring units, retains unchanged magnitudes and nulls, checks all known unit identities/scales for contradictions, and leaves omitted-context/declared-unit callers strict. The declaration does not prove the future implementation performs those checks.

The appearance shape covers the accepted panel fields, preserves disabled marker geometry and paired typography values, and keeps financial callbacks outside `RuntimeOptions`. The finite panel event union imports real panel types and does not introduce an arbitrary property-path API. The source-backed Auto Rotate merge/reopen limitation is correctly disclosed.

Production files still require the applicable 400 physical lines/file, 300 logical units/file and 50 units/function gate, actual strict affected compilation evidence, and the controller-owned inventory/breadth updates. Those are task 2.69 completion checks, not evidence supplied by this draft review.

## Corrected draft identity

SHA-256, relative to `contracts/`:

| File | SHA-256 |
| --- | --- |
| application/appearanceModel.ts | `4f4a594345ecd1c63795f2e02ad4a42dc77159e4f4a89a19dab12a8726c17e3c` |
| application/axisStructureTypes.ts | `86c914cd09af3a4870b63f665bd5d04bf442b1e1e2c462d493632b7a9aa66046` |
| compatibility/editorBindings/types.ts | `9fc97f0cf5ed9c00a0d1997247c7b04e410a0fcc450a90ca03c16157cc5b12b5` |
| field-manifest.md | `ca2bf8cc2a10eca0f50d362c6fddbe543ff61deb3741fa74ffa1168f32b08d7e` |
| cartesianTypes.patch.md | `978cbb9f311b5902ce6b426b30e0e0f4a5b64ae88af603b7df281a1c09489294` |

- REMEDIATION: None within this bounded contract re-review.
- SUMMARY: Corrected axis and event-transaction contracts resolve all three findings; compilation, implementation and runtime acceptance remain separate gates. This verdict does not mark task 2.69 complete.
