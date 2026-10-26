# F3 ordinary-Table integration design

Wire all three Funnel variants into the existing ordinary application session in one parent-owned join. Retain editable ready state when financial data cannot be drawn. Do not activate a gallery route before capture, setup, theme, transaction, empty recovery and editor routing are joined.

This is source-only design, inspected 2026-10-26 against root `d8383ab`, which pins the accepted Workspace baseline `a3e1a86`, and current files. No build, tests, browser, network or production changes were run. F1/F2 interfaces remain as implemented. Core steering files product.md, tech.md and structure.md are absent; complexity, testing, delegation, documentation and CI steering were read. Requirements remain approved; this proposal does not reopen them or claim implementation acceptance.

## Contracts to freeze

Paths in this section start at `vendor/workspace/terminalpro/src/components/General/Table/Chart/`.

Add `application/funnelSessionTypes.ts` with these data-only application contracts, importing the actual F1/F2 types:

```ts
interface FunnelSessionSelection {
  readonly baseline: OptionBaseline;
  readonly range: ResolvedRange;
  readonly setup: SetupSelection; // Complete selection for controls/storage.
  readonly projection: SetupProjection;
  readonly data: FunnelDataResult;
  readonly style: ResolvedFunnelStyle;
  readonly editor: FunnelEditorState;
}
type FunnelNotice = Readonly<{
  kind: "empty" | "invalid-data" | "missing-stages";
  message: string;
  diagnostics?: readonly SnapshotDiagnostic[];
}>;
type FunnelSessionReady = Omit<ApplicationSessionReady, "editor"> & {
  readonly kind: "funnel";
  readonly family: FunnelFamily;
  readonly editor: FunnelEditorState;
  readonly notice?: FunnelNotice;
};
```

`kind: "funnel"` identifies the application branch; `family` retains `funnel | coneFunnel | pyramid`. Do not conflate `coneFunnel` model type with saved `cone-funnel` option scope. The F2 mapper already supplies the native envelope.

New parent-owned functions:

```ts
// application/funnelSessionSelection.ts
function selectFunnelSession(
  storage: ChartStorageOutput,
  context: ApplicationSessionContext<FunnelFamily>,
): FunnelSessionSelection;
// application/funnelSessionProjection.ts
function projectFunnelSession(
  storage: ChartStorageOutput,
  inputs: ApplicationSessionInputs<FunnelFamily>,
  state: ApplicationSessionState,
): SessionResult<FunnelSessionReady>;
// application/funnelEditorTransaction.ts
function applyFunnelSessionTransaction(
  storage: ChartStorageOutput,
  context: ApplicationSessionContext<FunnelFamily>,
  command: ApplicationChartCommand,
): SessionResult<ApplicationSessionCommit>;
// caller/funnelThemePaint.ts
function projectFunnelThemePaint(
  mode: "light" | "dark",
  names: readonly string[],
  themes: Readonly<Record<string, unknown>>,
  family: FunnelFamily,
): ValidationResult<FunnelThemePaint>;
```

Use `sessionBaseline`, `sessionRange`, `sessionSetup`, retained ordinary capture, `resolveFunnelAppearance`, `projectFunnelEditorState`, `buildFunnelData` and `translateFunnel` directly. No second capture or lifecycle owner. Theme helper validates unknown raw selected input rather than trusting an AG Charts cast. Invalid paint must be explicit; do not stringify an object or substitute a guessed color.

### Safe caller paint failure boundary

`projectFunnelThemePaint` returns the existing `ValidationResult<FunnelThemePaint>` from compatibility/legacyTypes: `{ valid: true, value }` or `{ valid: false, error: string }`. It never throws for JSON-reachable palette/theme values. Validate shape and nonempty CSS-color arrays before deriving colors, and catch failures from its common-theme projection. Return a specific advanced-palette message for image/gradient/pattern objects and a distinct invalid-palette message for malformed colors/arrays. Do not include raw payloads or image URLs in diagnostics.

In `useCallerSessionInputs`, perform this validation after all hooks and after successful resolveCallerChart, before the generic projectCallerTheme/projectHierarchyThemePalette calls and before constructing live inputs. On valid:false return `{ valid: false, error: paint.error, chartType: result.value.chartType }`; do not access paint.value or call the family renderer. On valid:true pass only paint.value as `funnelThemePaint`, retaining the defined session appearance fingerprint/clone behavior. Protect the hook's synchronous Funnel theme/input-projection construction with a narrow try/catch that returns the same diagnostic envelope, so malformed theme projection cannot escape React rendering. This does not catch or suppress host failures or change other families' behavior.

Extend AgChartView's invalid caller branch to forward the retained optional chartType to `PendingCallerChart` (using a property guard for older resolveCallerChart failures without it). This preserves selected gallery identity. PendingCallerChart already renders UnsupportedRenderer in the plot and Set Up/Customize slots, with the existing ChartEditorDock/gallery. UnsupportedRenderer already has role=status and says saved configuration is preserved. No new theme state, fallback palette or fake resolved editor style is created. Unsupported appearance differs deliberately from valid appearance with rejected financial data: Pyramid negative/zero-total keeps its ready editor under the preceding contract.

Recovery routes are outside the failed live chart: ChartViewButton remains available to return to source Table; PendingCallerChart/useCallerDock retains the gallery; application Settings -> General exposes Light mode/Dark mode (`components/Settings/GeneralTab.tsx`) and the command palette exposes Toggle theme (`components/LayoutAuth/Search/constants.tsx`). An administrator's existing `/admin/theme-settings` -> Charts route owns palette updates/reset (`useChartSettings.handleSave` persists chartTheme=null for an explicit reset). The chart dock itself has no theme selector; do not invent one or claim otherwise. F3 changes no theme store or permission boundary. Reselecting an existing supported theme mode or receiving a corrected plain-color theme from the existing owner reruns the hook and restores normal live projection from preserved widget storage. If both configured modes are unsupported, choosing a different mode alone cannot repair them; retain the explicit diagnostic and the existing administrator correction path, without silently resetting either theme.

Focused caller/UI evidence must seed an advanced palette into one mode and a supported stock/plain palette into the other, render the actual caller without an uncaught exception, assert the explicit diagnostic and unchanged theme/widget payload, keep table/gallery/global Settings reachable, then change mode through the existing control and assert chart/editor restoration with the original range/options. Add malformed palette failure and recovery coverage without relying on TypeScript casts as runtime validation. F4 repeats the visible supported-mode recovery journey. Shared advanced-palette editor behavior itself remains in the separately tracked theme task.
### Setup and first-field semantics

Add `"funnel-observations"` to the existing SnapshotPolicy union and admitted-policy lists in `compatibility/snapshot.ts` and `application/setupProjection.ts`; return it from `observationSnapshotPolicy` for all three variants. It permits zero selected numeric fields and rejects switch-category-series. It does not normalize or coerce source values and does not introduce Waterfall's single-axis units constraint. Existing capture/recapture owners remain authoritative. In `application/gridCapture.ts:145-166`, add funnel-observations to the existing raw-undefined skip branch used by box/statistical policies: absent cell reads remain absent keys, explicit null remains null, and genuine zero remains zero. Do not use the polar/histogram coercers or add a new capture implementation. Recapture uses this same policy path.

Project the complete selected numeric list through ordinary setup, then let F1 choose the first descriptor in selected-ID order. Retain the original full range and full capture. This matches F1's approved contract and the observed native ability to append Reserve while Value remains selected. Do not turn Add a series into a single-select or delete later selections. The setup model and reorder/remove/add controls keep all selected fields; rendered field promotion follows list order. Do not use the Waterfall transient slice here: with the dedicated policy no numerical-axis incompatibility is introduced across unused selected fields.

Aggregate remains `transitionOrdinarySetup`/`aggregateSetupRows` responsibility. Preserve default-category restrictions, existing operators, duplicate-row behavior with Aggregate off, Count provenance and integer count display (`countDisplayPolicy`). No reaggregation inside F1 or F3. Negative Pyramid values and zero total are drawing admission failures after setup, not reasons to reject a valid setup edit; otherwise the user cannot select a correcting field.

`canSwitchCategorySeries` returns false for Funnel families, retaining dormant saved state unless an existing family transition deliberately resets it. Direction uses `funnelDirection` and only native `series.direction`; it must not alter selected columns, source order, capture, or category/series switch.

### Recoverable invalid and empty data

`selectFunnelSession` resolves setup and appearance independently of F1 admission, retaining `data` even when its status is empty/invalid. `projectFunnelSession` returns outer `status: "ready"` for those expected data states with current stamp, editor, model, snapshot and setupProps. Reserve outer invalid for broken session/appearance contracts or renderer failure; do not copy Heatmap's throw-on-failure pattern for Pyramid admission.

For non-drawable data, send fresh blank chart options through the same host at the new revision, clearing old series/graphics/tooltips. Factor the existing common option construction in `echarts/funnel.ts` into exported `funnelChromeOptions(style: ResolvedFunnelStyle): EChartsOption` (background/title/subtitle, animation false, empty series/graphic, disabled tooltip). `translateFunnel` extends that object with real geometry/tooltip. The session uses the same chrome builder for empty/invalid data. This is one common option builder, not dummy financial data or a second renderer. F1 remains unchanged.

In AgChartView render a DOM notice for ready.kind=funnel, with `role="status"`, `aria-live="polite"`, `aria-atomic="true"`. Empty/invalid messages occupy the plot, not the dock; missing-stage notices use a compact caption that does not obscure valid geometry. Keep the host mounted, existing theme controls, gallery, Setup, Customize and table-mode button available. Exclude Funnel from the existing zero-series auto-disable effect.

Messages:

- No series: "No series selected. Add a series in Set Up."
- No rows: "No rows available to chart."
- No values: "The selected series has no numeric observations."
- Pyramid negative: "Pyramid requires nonnegative observations. Choose another series or update the source data."
- Pyramid zero total: "Pyramid requires a positive total; all observations are zero."
- Partial missing: "Some stages have missing values. Missing stages have no value shape or tooltip."

Preserve stable F1 diagnostics and their paths in `notice.diagnostics`; do not announce missing as zero. All-zero Funnel/Cone remains drawable ready data with genuine zero hit targets, not no-values. Invalid Pyramid has no fabricated geometry. Remove the notice after field/data correction without remounting the session; new revision must clear stale invalid options. Missing-stage labels still follow the accepted renderer's stage-label option; gaps must never be bridged.

### Transactions and persistence

Validate synchronous stamp, family, current full range and setup against local baseline before mapping a Funnel edit. Use `mapFunnelEditorIntent(selected.style, intent)` and the existing `reduceSessionOptions`; preserve unrelated family options. Reject forged ineligible Drop-Off/Shadow intents and reject Funnel-only intents on another family before generic editor fallback. Selection must remain usable during invalid Pyramid data, so valid appearance edits still commit.

Add Funnel paint to ApplicationSessionInputs, ApplicationSessionState.appearance, sessionAppearanceKey and both initial/synchronize clone sites. Theme changes advance render revision through the existing owner; data/range changes retain existing data-revision/recapture rules. Add Funnel to non-axis families in runtime axis preference handling and to no-legend model-update handling. No new stamp or option storage schema.

Retain ordinary gallery family transition through `applyComboFamilyTransaction`/`commitFamilyTransition`, full range, existing native baseline migration and generation rules. Test Funnel -> Cone -> Pyramid -> Cartesian -> Funnel and table/chart return; stale pre-transition callbacks must not mutate the new family. Ordinary family transition functions need no new implementation if their expanded family type and observed contract tests pass.

## Theme reachability and prerequisite

The exact stock light Cone token fixture now exists in `theme/light-cone-reference.json`: `#5090dc,#629be0,#74a7e4,#85b2e8,#97bdeb,#a8c8ef,#b9d3f2,#cbdef5`. Both fills and strokes use that array. Dark is `#5090dc,#4882c6,#4073b0,#38659a,#305684,#28486e,#203a58,#182b42`. Preserve source hash/derivation provenance in focused fixture assertions; do not recalculate these using RGB interpolation.

Classify the raw selected palette before normalized defaults obscure whether it is custom: any up/down/neutral is user-full; otherwise supplied fills/strokes is user-indexed; otherwise inbuilt. Common projectCallerTheme owns default fill/stroke arrays, baseTheme override and text/background colors. Funnel uses its first fill/stroke; Pyramid uses complete arrays; custom string Cone uses first two circular fills for both arrays, including strokes-only classification and a repeated one-color palette. Saved series fills/strokes retain higher precedence in F2 appearance. Label/drop-off defaults follow frozen F2 paint contract. Test caller input/result mutation isolation.

Advanced fill reachability cannot be dismissed using TypeScript alone:

- `src/lib/state/tableChartThemes.ts:73` declares fills/strokes as string[], and `components/ThemeSettings/chartThemeState.ts` UI serializes string arrays.
- But `backend-api/backend/api/schemas.py:1985` uses `chartTheme: dict | None`, with extra allow; `/admin/theme-settings` stores it and `/pro/theme-settings` returns it.
- `src/api/auth.api.ts:getEntityThemeSettings` supplies only a TypeScript generic. Store updateThemeSettings uses `set(settings)` without a palette schema. `useAgThemes` checks only presence of baseTheme/palette/params and `getCustomChartTheme` passes palette through.
- Consequently persisted API palettes can reach the ordinary caller with gradient/pattern/image objects. ChartTheme.backgroundImage is separate dormant metadata and does not close this path.

Retained Community SAFE_RANGE2_OPERATION at 26020 explicitly checks gradient/pattern from `$palette: "fill"` but image from `$value: "$1"`. Parent relayed separate theme-lane source findings: the image branch remains an object because that binding is absent in this evaluation path, whereas gradient/pattern choose the stock fallback pair. Native Funnel/Pyramid also support advanced fills. Existing shared effectiveAppearance rejects nonstring palettes even though projectCallerTheme passes raw objects. Thus this is a reachable shared-theme capability gap, not a TS-only impossibility or an accepted string conversion. The owner settled scope on 2026-10-26: track advanced palettes separately and finish Funnel. F3 supports stock themes and plain CSS-color palettes. Image, gradient and pattern palettes are deferred to the [shared-theme task](advanced-palettes.md); retain their original stored payload and explicit unsupported diagnostic, with no coercion to blue, CSS strings or generic fills. This boundary does not claim complete advanced-paint acceptance. The ordinary supported-theme path activates all three families without a feature flag. No commercial evaluator/runtime import or silent fallback is permitted.

## Ownership and order

With the owner-settled stock/plain-color boundary, at most one inactive preparation task: own only new `caller/funnelThemePaint.ts` and `tests/unit/chart-compatibility/funnelThemePaint.test.ts`, with source-derived fixture additions under ignored theme artifacts. Assert explicit rejection of advanced fills without changing the original payload; ordinary routing stays inactive during this task. Independent financial/integration review must inspect provenance and custom-palette classification. This lane does not edit shared themeInputs, themes, F1/F2 contracts or runtime routing.

Then one parent-owned atomic integration task owns new application/funnelSessionTypes.ts, funnelSessionSelection.ts, funnelSessionProjection.ts and funnelEditorTransaction.ts; the shared files listed below; the small common-chrome extraction in echarts/funnel.ts; focused integration tests; root complexity inventory/breadth mappings. No parallel shared-file editor lane. Prepare internals, then change admission, dispatch and UI routing as one joined source candidate. All three variants become active together. No disabled feature switch.

| Shared file | Current physical lines | Exact join responsibility |
| --- | ---: | --- |
| application/comboSessionTypes.ts | 52 | ApplicationChartFamily includes existing FunnelFamily |
| application/applicationChartSessionTypes.ts | 85 | FunnelSessionReady and FunnelEditIntent unions |
| application/applicationSessionTypes.ts | 145 | Funnel theme paint input/appearance snapshot |
| application/applicationChartProjection.ts | 151 | Ordinary Funnel projection dispatch before generic fallback |
| application/applicationSetupSelection.ts | 101 | Funnel selection usable with invalid/empty F1 result |
| application/applicationSessionSelection.ts | 173 | Switch prohibition only |
| application/applicationSessionSetup.ts | 209 | Preserve existing aggregate/recapture; ensure no axis/legend state is introduced for Funnel |
| application/applicationSessionRuntime.ts | 331 | Paint fingerprint/clone; non-axis/no-legend admission |
| application/applicationSessionTransactions.ts | 254 | Funnel transaction dispatch and wrong-family intent rejection |
| application/useApplicationChartSession.ts | 261 | onIntent union, ReadyFor narrowing if needed, no-legend update exemption |
| application/histogramCapture.ts | 39 | Return new Funnel observation policy |
| application/histogramEditorTransaction.ts | 129 before join | Reject the new Funnel-only intents at the existing Histogram boundary; required by the expanded command union |
| application/gridCapture.ts | 275 | Include Funnel policy in existing absent-value skip branch; preserve null/zero |
| application/setupProjection.ts | 299 | Admit dedicated policy, empty selection, unswitched ordinary aggregation |
| compatibility/snapshotTypes.ts / snapshot.ts | 77 / 169 | Policy type and no-series snapshot admission |
| caller/useCallerSessionInputs.ts | 119 | Selected native theme -> pure Funnel paint |
| caller/useCallerDock.ts | 75 | Route gallery through existing live transaction |
| caller/LiveChartEditor.tsx | 103 | kind=funnel branch with same dock/themeResetKey/onSetup/onIntent |
| editor/ApplicationChartEditor.tsx | 88 | Dedicated Funnel Customize composition and common Setup |
| editor/combo/comboEditorMode.ts | 64 | Funnel setup mode carrying direction and intent callback |
| editor/setup/ChartSetupPanel.tsx | 305 | Direction in Setup; hide switch, retain multi-selection/Aggregate |
| editor/funnel/FunnelCustomizeEditor.tsx | 85 | Move existing Direction fieldset to Setup; no duplicate direction control |
| AgChartView.tsx | 318 | Live admission, zero-series exemption, accessible ready-data notice |
| echarts/funnel.ts | 111 | Shared chrome builder for valid and non-drawable data |

`caller/chartInputs.ts` is 285 and currently applies generic resolveChartRange to Funnel, which already preserves the complete ordinary range. `caller/themeInputs.ts` is 269 and already owns normalized common colors. `caller/generatedOptions.ts` supplies common generated options. Read these at join; do not modify solely to add redundant family branches. `EChartsHost.tsx` (157) and `echarts/lifecycle.ts` (394) remain reused unchanged; normal resize, disposal, expected-revision PNG export and registration stay there. `radialLayout.ts` (398) is unrelated and untouched.

All new/modified maintained files require <=400 physical lines, <=300 logical units/file and <=50/function. Counts above are read-only physical inventory, not a cap pass. Add inventory entries before accepting production changes and use the exercised combined checker from docs/complexity.md with actual changed-file manifests for both forks. If runtime or AgChartView growth exceeds a cap, extract one cohesive existing presentation/family-policy responsibility in this atomic task, retaining current owners; no compression or silent exception. Existing checker foundation is accepted and should be reused.

## Focused F3 source acceptance

Extend existing chart-compatibility test locations with `funnelSession.test.ts`, `funnelThemePaint.test.ts` and a focused Funnel editor integration test. Use actual ordinary snapshot/setup, baseline, reducer, dispatcher and renderer, not independently mocked replacements. Run scoped typechecking and affected tests plus the combined complexity gate after final fixes; independent review inspects real changed source and evidence.

Required effects:

1. Actual ordinary Grid API capture with an absent middle value, explicit null and genuine zero preserves all rows and absence/null distinction through setup/F1/rendering; no connector bridges missing endpoints. Cover recapture through the same policy, not only a handcrafted snapshot. Multi-selection order, promotion after removal, aggregate on/off and Count preserve range/row identity/provenance; direction changes options only. No-series is ready+notice and allows Add a series.
2. Pyramid negative and all-zero states keep editor/setup live, clear previous polygons/tooltips, accept appearance edits and recover after changing first selected field/source. Partial missing keeps gap/identity and accessible notice; all-zero Funnel/Cone remains genuine zero.
3. Actual dispatch -> native-scoped saved options -> reselect -> translate changes numeric labels independently of stage labels, Drop-Off only for Funnel, Shadow only for Funnel/Pyramid, and common style/title/tooltip controls. Reject stale/family-ineligible edits without storage mutation.
4. Theme mode/base/custom changes advance appearance revision while capture identity remains; stock light/dark and custom first-two Cone values match independent fixtures, saved plain-color palettes win, malformed inputs remain explicit, and advanced image/gradient/pattern inputs retain their payload and unsupported diagnostic under the separately tracked shared-theme boundary.
5. Family/table-chart transitions and saved-state restoration keep full selected range and native scoped options. Normal PNG registration points to the current stamp/revision, with existing stale-export refusal intact.

These are proposed tests, not completed checks. F3 source acceptance does not establish visual parity, browser persistence or release readiness.

## F4 candidate acceptance boundary

After F3 acceptance, build one identified packaged Workspace candidate through existing Dagger image ownership. Use one owned headless browser worker, disposable accounts/state, the ordinary Table upload route used by the original harness and exact retained AAPL income-statement input underlying Stage/Level USD native screenshots. Its recorded provider endpoint is `https://financialmodelingprep.com/stable/income-statement`, parameters symbol=AAPL, period=quarter, limit=40, retrieved 2026-10-20; the selected record is FY2026 Q2 dated 2026-03-28 in unscaled USD. Use `fmp/levels.csv` and `fmp/provenance.json`, asserting Revenue 111184000000, Gross profit 54781000000, Operating income 35885000000, Pretax income 35833000000 and Net income 29578000000. These overlap financially and are not additive components or conversion counts. Record data-image identity, Workspace revision and digest; this retained-source route is not a new live FMP endpoint check. If fresh endpoint evidence is required, run it separately with configured credentials and record the exact application endpoint/result; missing credentials leave that check unverified. Reuse the existing Funnel native acceptance harness/fixtures and normal widget creation/save/download actions; no new capture owner or direct option injection as acceptance.

Check all three variants from the gallery, source financial values and signed tooltips, first-field switch by removing/reordering real selected chips, Aggregate toggle, both directions, independent numeric/stage labels, applicable Drop-Off/Shadow, titles/padding/background/stroke/font/tooltips, global light/dark and custom chart theme selection. Candidate controls must remain reachable through the normal UI flow. Explicitly verify Pyramid invalid -> correction and no-series -> add-series, missing gaps, resize, refresh, table/chart mode, family round trip and separately authenticated save/reopen. Verify persisted visible effects, not only chartOptions equality.

Download actual PNG through the normal application action and compare representative original/replacement images in qView, including Cone light palette. Inspect tooltip identity and zero hit targets; the native run's nonfinite missing polygons and disappearing labels are not acceptance expectations. Capture strict candidate console/network diagnostics with no blanket original-error suppression. A successful HTTP response/unit count is insufficient. Schedule logins under existing limiter, retain raw evidence ignored, and publish only the concise reviewed evidence set. Image/browser evidence belongs to F4; source work here cannot preclaim it.

## F4 evidence reconciliation (2026-10-26)

The earlier browser agenda is closed through reviewed source/actual-engine contracts and seven representative packaged cases, not a claim that every combination ran. [Closing verification](../../../artifacts/reviewed/chart-funnel/verification.md) records the accepted runtime, owner appearance decision, executed cases and limitations. Detailed aggregation and missing/zero contracts remain source/engine evidence; malformed-theme recovery, changed-source recalculation and every appearance/persistence combination are not claimed as browser-tested. Advanced palettes remain owner-deferred. F5 publication remains a separate gate.
