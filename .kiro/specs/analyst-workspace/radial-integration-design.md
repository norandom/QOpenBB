# Radial application integration design

RC3 should connect both Radial model names through one application family branch after RC1 renderer and controls reviews. This independently reviewed plan is based on read-only inspection at root baseline `26f1c8c` on 2026-10-24; active worker files were inspected as provisional interfaces. Implementation begins only after RC1 source acceptance. No application acceptance is claimed by the plan.

## Ownership and prerequisites

One designated integration worker owns all shared source edits below, the new `application/radialSessionProjection.ts` and focused integration tests. The controller owns scope manifests, `.kiro/complexity-budgets.json`, `.kiro/breadth.toml`, joins and commits. Paths below are relative to `vendor/workspace/terminalpro/src/components/General/Table/Chart/`, unless qualified. Renderer and controls workers retain their existing exclusive files; freeze their accepted revisions before joining. Do not edit their files opportunistically.

Consume the frozen exports `RadialChartType`, `RadialEditorState`, `RadialEditIntent`, `RadialAcceptedEditIntent`, `RadialGroupType`, `prepareRadialSelection`, `mapRadialEditorIntent`, `RadialControls`, and `translateRadial`. Existing controls use `kind: "radial"`, panels `radialGroupType`, `radialPolarAxis`, `radialPolarLabels`, family names `radialColumn`/`radialBar`, and option keys `radial-column`/`radial-bar`. The observed selection defaults absent/undefined root grouping to `grouped`, unlike Nightingale's default. Preserve that distinction.

## Minimal shared changes

| Owner file | Bounded change |
| --- | --- |
| `application/radialSessionProjection.ts` (new) | Export `isRadialChartFamily`, `selectRadialSession`, `projectRadialSession`, `applyRadialSessionTransaction`, `radialGroupKey`. Follow Nightingale session composition, but consume Radial contracts and named policy. Translate cloned mapping; preserve viewport, count display, native legend selection callback/scope, setup choices and local legend override. Validate stamps/family/root group presence and value/range/setup before mapping accepted intents. Apply root mutations to cloned model and option mutations through `reduceSessionOptions`; grouping is render-only and retains captured rows. |
| `application/comboSessionTypes.ts` | Extend `ApplicationChartFamily` with `RadialChartType`; do not admit Radial into combo geometry. |
| `application/applicationChartSessionTypes.ts` | Add ready discriminant `kind: "radial"` with `RadialEditorState`; extend command intent union with `RadialEditIntent`. |
| `application/useApplicationChartSession.ts` | Route both Radial families to `projectRadialSession`; extend `onIntent` union. Retain current host/export/resize and transient legend lifecycle. |
| `application/applicationSessionDispatch.ts` | Route Radial editor commands to its transaction; reject all three Radial-specific panels on foreign families before other family transactions. This centralized guard avoids edits to each neighboring transaction, including `histogramEditorTransaction.ts`. |
| `application/applicationSetupSelection.ts` | Route both names to `selectRadialSession`, wrapped in the existing ready setup result. |
| `application/applicationSessionSetup.ts` | Add Radial to root group stale check using `radialGroupKey`; preserve ordinary aggregation/range/transpose transitions and captured policy. |
| `application/applicationSessionRuntime.ts` | Exclude both Radial families from Cartesian axis restore/read in initialization and both synchronization preference branches. Preserve existing `sessionAssignmentKey`, which already includes `Object.hasOwn` plus root value. |
| `application/histogramCapture.ts` | Required additional shared owner absent from the original 19-file table: return `radial-observations` from `observationSnapshotPolicy` for both names. No capture owner duplication. |
| `application/gridCapture.ts` | Admit `radial-observations` into existing `normalizePolarObservation` branch. |
| `compatibility/snapshotTypes.ts`, `compatibility/snapshot.ts` | Add named policy and its existing polar numeric-admission/empty-capture validation branch. |
| `application/setupProjection.ts` | Add Radial policy to accepted policies, category/series inversion eligibility and post-aggregation finite-value sanitation. Keep aggregation before inversion and raw missing observations. |
| `caller/chartInputs.ts` | Exclude inactive Cartesian axis settings for both names, as for accepted polar families. |
| `caller/generatedOptions.ts` | Add both hyphenated option keys with existing `polarSeries` filtering; no marker/connectMissingData/callout leakage. |
| `caller/themeInputs.ts` | Add both option keys to common/family override composition; admit opposite-direction Radial axes `angle-number`/`radius-category` to parameter axis projection. Keep Radial outside the Nightingale background-stroke special case: retain standard light/dark palette strokes when no palette is supplied and supplied stroke arrays when present. |
| `editor/ApplicationCustomizeEditor.tsx` | Extend state/intent unions; route `kind: "radial"` to `RadialControls` with existing `polarAxis` props. Keep titles, legend and style ownership. |
| `editor/ApplicationSeriesEditor.tsx` | Extend existing Radar/Nightingale Series branch to Radial, preserving tooltip/style/labels and Radar-only markers. Avoid falling through to the Pie branch that expects shadow state. |
| `editor/combo/comboEditorMode.ts` | Add Radial setup mode with `RadialGroupType`, choices and callback; preserve all existing mode variants. |
| `editor/setup/ChartSetupPanel.tsx` | Reuse the existing Group Type JSX for Nightingale or Radial; keep existing choices and value validation, category/series controls, aggregation and inversion. |
| `AgChartView.tsx` | Admit Radial to live routing, empty-series keep-open and no-data branches. Extend the existing group-type editor mode expression for both kinds, choosing the correct panel without duplicate JSX. In `createRangeChart`, conditionally spread `seriesGroupType` only when `Object.hasOwn(chartModel, "seriesGroupType")`; unconditional assignment currently materializes an absent model property. Preserve own undefined if supplied explicitly. |

The resulting proposed shared scope is the original 19 files plus `application/histogramCapture.ts`, and one new projection file. Do not add a generic family registry or separate lifecycle. If the exact edits exceed caps, first share the existing Nightingale/Radial group-type mode expression and polar Series JSX. Further extraction requires an ownership amendment and review, not hidden scope growth.

## Root capture and palette invariants

Distinguish three structures in captured params and persisted models: absent `seriesGroupType`, own `undefined`, and own `grouped`. JSON value equality alone collapses the first two. Keep presence/value tuples in `radialGroupKey`, external synchronization and setup/editor stale rejection. An unrelated appearance or setup edit must not persist the effective `grouped` default as a new root key. An explicit Group Type edit may write it. Preserve root neighbors and unsupported stored option keys, including `normalizedTo`; the renderer consumes resolved grouping independently of those saved options.

Palette authority stays in `projectCallerTheme`. Radial uses standard light/dark palette strokes when no palette was supplied; explicit custom stroke arrays survive. Do not apply the Nightingale background-stroke substitution. A theme named `openbb-dark` can carry an explicit custom palette, and a differently named theme can lack one. Test provenance rather than names. A partial supplied palette currently falls back to standard strokes; retain the existing caller contract unless source evidence explicitly changes it.

## Focused tests to extend

Tests live under `vendor/workspace/terminalpro/tests/unit/chart-application/`. These are proposed assertions, not executed evidence.

- `nightingaleSessionOwner.test.tsx`: reuse its real session-owner fixture and parameterize suitable lifecycle cases for both Radial names. Existing meaningful cases cover grouping without recapture/raw missing values, direct transactions preserving root neighbors and rejecting external presence/value changes, aggregate-before-invert/count formatting, native legend/resize/quick actions, family transition preservation, ready empty refresh/recovery, stale captured callbacks and queued external root edits. Keep all Nightingale expectations; Radial defaults must assert `grouped`. Extend the direct root test to absent versus own undefined versus explicit grouped in editor and setup transactions.
- `nightingaleEditorControls.test.tsx`: extend actual editor rendering to Radial controls and both orientations. Reuse the test named `routes Set Up Group Type separately from ordinary setup and keeps transpose reachable`; assert Radial root panel, polar padding controls/first-axis display, no Cartesian axes/Pie shadow/Radar markers, and preserved generic title/legend/series regions.
- `callerRoute.test.tsx`: extend the existing Nightingale family journey near line 964 to both title-case gallery labels and correct engine keys. Assert real Table/File route, editor visibility, selected columns, persistence on remount, and unchanged toggle predicates, original buttons and chart flags. The stubbed host proves routing, not rendered geometry.
- `callerInputs.test.ts`: parameterize existing Nightingale palette provenance/inactive-axis test near line 355 for both Radial names, light/dark modes, explicit palette under a built-in-looking name, and no palette under a custom name. Assert both axis-direction parameter keys, family override precedence and generated marker/connect/callout filtering. A strokeWidth-only edit must reveal the applicable palette stroke; an explicit user stroke without width retains the accepted RC2 width-1 fallback.
- `radarCapture.test.ts`: extend named-policy wrapper/empty capture assertions for both names. Preserve wrapper precedence, duplicate labels with stable row IDs, null/malformed/overflow admission, no-series empty capture and the existing Radar/Nightingale cases.
- Add focused `createRangeChart` assertions to the existing `callerRoute.test.tsx` test boundary if feasible: `Object.hasOwn(chartParams, "seriesGroupType")` false for absent; true for own undefined and grouped. Inspecting values alone cannot catch the current loss of presence semantics.

Use existing files/fixtures rather than creating a new integration harness. Renderer numerical geometry remains RC1's responsibility; RC3 tests prove the application passes projected observations, grouping, palettes and legend selections into that accepted renderer.

## Completion gate and unknowns

Require independent integration review followed by fresh focused application/compatibility tests, scoped lint/type diagnostics against the frozen baseline, and combined complexity inventory/manifests. Every changed production file is checked whole against 400 physical lines, 300 logical units and 50 units/callable. `AgChartView.tsx` was read at 357 physical lines, leaving 43; no parser metrics were measured in this planning task. Update actual maintained paths and breadth test/evidence links; planned checks stay planned. A later isolated packaged browser gate owns native geometry, export, financial values and fresh-session persistence.

No tests, builds, browsers, installs, production changes or acceptance checks ran here. No nested AGENTS.md was found below `vendor/workspace`. Default steering `product.md`, `tech.md`, `structure.md` is absent at the configured paths; testing, complexity, documentation and delegation policies were read. `radialContracts.ts` still contains a draft RC0 header in the inspected working tree; controller must establish accepted contract identity. `translateRadial` and renderer behavior are pending active worker acceptance. This proposal is disproved if the frozen renderer needs a different observation policy, if capture/runtime rewrites root presence elsewhere, or if the whole-file complexity gate requires a further cohesive extraction.
