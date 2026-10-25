# HM3 executable join boundary

Implement HM3a dispatch extraction, review and commit it, then HM3b atomic Heatmap integration. The owner authorized continuation on 2026-10-25. This compact boundary follows the [prototype-first workflow](../../steering/delivery-workflow.md), not a new whole-feature specification. Accepted HM2 source is Workspace `8b4426b9ca7f0b04ccfdfa05c495a415f7741ddf`. Application acceptance remains the subsequent identified-image journey.

All Chart paths below are relative to `vendor/workspace/terminalpro/src/components/General/Table/Chart/`. One integration implementer owns the coupled production edits serially. The controller owns inventory, breadth, evidence, acceptance and selective commits; a fresh reviewer independently reviews each task. The implementer is not alone and must preserve unrelated edits. Separate public-grid/all-missing research is read-only and has no production ownership.

## Decisions and frozen boundaries

- Reuse ordinary `ChartSnapshot`, existing capture/recapture, range, setup aggregation and Widget transactions. No third capture kind, parallel reducer, persistent matrix, feature flag or replacement host.
- The observed native Setup has no category/series switch. Heatmap never applies transpose; hide that control, reject its command and ignore an inactive saved switch flag without deleting unrelated preferences.
- Empty numeric selection must keep chart view, Setup and add-series recovery available, including fresh reopen. Add a narrow `heatmap-observations` snapshot policy that permits zero selected numbers while retaining all ordinary finite/null/absent validation. It remains an ordinary snapshot. Admit it in ordinary capture and setup; do not alias Radar/Pie policy or manufacture a fake numeric column.
- Preserve every existing family's compatible-unit/scale check, but do not transfer the ordinary positional single-axis prohibition to newly activated Heatmap. Compatibility interpretation of the owner's existing no-capability-cuts direction: native Heatmap accepts selected numeric fields on one raw shared color scale; HM3 must not add an unsupported mixed-unit restriction. The dedicated policy uses the existing deferred axis-unit result, retains descriptor units/scales and provenance, and performs no conversion, normalization or zero-centering. Count retains its derived observation-count unit. Test that mixed descriptor units retain their original values in Heatmap while an ordinary single-axis projection of the same input still rejects. Shared colors do not establish economic comparability; application financial acceptance uses explicitly identified units.
- Reuse accepted `HeatmapMappingInput`, `ResolvedHeatmapStyle`, `HeatmapEditorState`, `HeatmapEditIntent`, `HeatmapThemePaint`, HM1 data adapter and HM2 functions verbatim. Frozen `heatmapTypes.ts` hash remains `729ba59722dfae0bc315219aef8ce3f2c81edbc9ade32c572e0f185261f94bb1`. HM2 files are outside writable scope.
- Existing `hierarchyHover` host field carries Heatmap's structurally identical gradient plan. Do not rename or edit the host/lifecycle for naming consistency. Host revision, viewport, resize, disposal and PNG export remain authoritative.

## HM3a: behavior-preserving dispatch extraction

Exclusive production paths: existing `application/applicationSessionDispatch.ts`; new `application/applicationSessionTransactions.ts`. Move existing `transaction` and `comboTransaction`, and only their required imports, to the new file. Export the first under this exact signature:

```ts
export function applyOrdinarySessionTransaction(
  storage: ChartStorageOutput,
  context: ApplicationSessionContext<ApplicationChartFamily>,
  command: ApplicationChartCommand,
  recapture?: SessionResult<ChartSnapshot>,
): SessionResult<ApplicationChartCommit>;
```

Keep `comboTransaction` private. Replace only the existing final ordinary delegation call in `joinedTransaction`. Leave hierarchy routing, `executeApplicationChartCommand`, latest Widget range reads, assignment/data/stamp admission, exception handling, revision increments and Widget/local/capture commit in `applicationSessionDispatch.ts`. Preserve branch order and all rejection behavior. No Heatmap union or live-route activation in HM3a; no generic dispatch registry.

- [x] Capture current typing signatures; perform the extraction without behavior changes.
- [x] Run affected existing application transaction/session, Combo assignment and hierarchy owner tests once; exact-file lint, baseline-relative typing and inventory-backed whole-file caps pass.
- [x] Fresh independent review confirms source parity, then controller selectively commits HM3a. Existing dispatch baseline is 362 physical lines; extraction must create real headroom, not compressed formatting.

## HM3b: atomic Heatmap join

Add one cohesive `application/heatmapSession.ts`, housing session selection, projection and appearance transaction. Target below 300 physical lines; if measured caps require separation, split appearance transactions into `heatmapSessionTransaction.ts` after controller boundary acknowledgement. Do not create three ceremonial forwarding files. The following contracts are frozen for implementation/review; declarations live beside implementation or in existing shared union owners, not in accepted HM2 types:

```ts
interface HeatmapSessionSelection {
  readonly baseline: OptionBaseline;
  readonly range: ResolvedRange;
  readonly setup: SetupSelection;
  readonly projection: SetupProjection;
  readonly style: ResolvedHeatmapStyle;
  readonly editor: HeatmapEditorState;
}
type HeatmapSessionReady = Omit<ApplicationSessionReady, "editor"> & {
  readonly kind: "heatmap";
  readonly editor: HeatmapEditorState;
  readonly hierarchyHover?: GradientHoverPlan;
};
function selectHeatmapSession(storage: ChartStorageOutput,
  context: ApplicationSessionContext<"heatmap">): HeatmapSessionSelection;
function projectHeatmapSession(storage: ChartStorageOutput,
  inputs: ApplicationSessionInputs<"heatmap">,
  state: ApplicationSessionState): SessionResult<HeatmapSessionReady>;
function applyHeatmapSessionTransaction(storage: ChartStorageOutput,
  context: ApplicationSessionContext<"heatmap">,
  command: ApplicationChartCommand): SessionResult<ApplicationSessionCommit>;
```

Selection uses `sessionBaseline`, `sessionRange`, `sessionSetup`, `projectOrdinarySetup(..., "heatmap-observations")`, accepted appearance and editor projection. Projection uses the current viewport, Count-aware display policy, accepted translator and hover projection; returns real empty data with the accepted renderer's no-data message and usable Setup. Do not add the generic overlay on top of that message. Preserve row/column provenance and detached projection inputs. Appearance transactions admit only `HeatmapEditIntent`, validate synchronous stamp/family and current range/setup, map against the latest stored baseline and reduce only returned `eventOptions`. Appearance changes advance render only; Setup advances data once through the existing owner. Two immediate appearance intents from one data frame must compose; changed data/address/generation/family must reject.

Add optional `heatmapThemePaint: HeatmapThemePaint` to session inputs and retained appearance identity. Caller supplies it from the original selected theme palette and resolved background via accepted `heatmapThemePaint`; do not feed a synthesized default palette that misclassifies a stock theme as custom. Selection requires valid caller-supplied paint for Heatmap. Generated/theme parameter layers preserve native label/gradient defaults and existing explicit saved precedence; do not serialize resolved defaults.

### Exact shared writable manifest

| Responsibility | Existing files |
| --- | --- |
| Family/ready/intent/theme unions and dispatch | `application/comboSessionTypes.ts`, `application/applicationChartSessionTypes.ts`, `application/applicationSessionTypes.ts`, `application/applicationChartProjection.ts`, `application/applicationSessionTransactions.ts` |
| Runtime, Setup selection, no-switch and side effects | `application/applicationSessionRuntime.ts`, `application/applicationSetupSelection.ts`, `application/applicationSessionSelection.ts`, `application/applicationSessionSetup.ts`, `application/useApplicationChartSession.ts` |
| Narrow empty-selection policy | `compatibility/snapshotTypes.ts`, `compatibility/snapshot.ts`, `application/histogramCapture.ts`, `application/setupProjection.ts` |
| Caller theme, original defaults and axis isolation | `caller/useCallerSessionInputs.ts`, `caller/themeInputs.ts`, `caller/generatedOptions.ts`, `caller/chartInputs.ts` |
| Gallery/live route and correlated UI | `caller/useCallerDock.ts`, `AgChartView.tsx`, `caller/LiveChartEditor.tsx`, `editor/ApplicationChartEditor.tsx`, `editor/combo/comboEditorMode.ts`, `editor/setup/ChartSetupPanel.tsx` |

Add `{ kind: "heatmap" }` to existing editor mode solely to suppress the switch in the shared Setup panel. Add a correlated Heatmap arm to `ApplicationChartEditor`, composing that Setup panel with accepted `HeatmapCustomizeEditor`; bypass ordinary Customize/Pie/legend fallback. No separate Setup component. Gallery selection enters the existing family transaction and clears stale capture. Explicitly reject Heatmap-only panels before other families' transaction fallback; shared common panels still route according to current family.

Runtime and caller skip ordinary category/number axis restoration for Heatmap; its two categorical axes resolve from original Heatmap leaves. Preserve gradient visibility across series-count changes: omit ordinary local legend toggling in Setup and notification paths. The inspected shared `reduceIntegratedState` only merges options and writes counts/model; it does not synthesize a legend, so `applicationSessionEdit.ts` and the reducer need no speculative edits. Do not rebuild ordinary axes to represent Heatmap.

Existing `applicationSessionCapture.ts` and `applicationSessionRecapture.ts` should work through the new policy and need no mechanical edits. Existing `familyTransition.ts` already invalidates capture on family change. `histogramEditorTransaction.ts` may receive only a narrow specialized-panel exclusion if union typing requires it; record that concrete compiler seam before extending ownership. No other family-semantic or host/lifecycle changes are authorized.

### Evidence-dependent admission boundary

The local admission assessment (`artifacts/chart-heatmap/hm3-admission.md`) establishes that ordinary capture accepts finite/null and rejects raw undefined; sparse File objects can occur, but actual blank CSV/public-grid behavior remains unproven. The separate research must report actual missing File-grid values and all-missing native appearance for HM4 application acceptance. If raw undefined is proven, controller reviews a narrow amendment for `application/gridCapture.ts`: Heatmap-only omission/null handling chosen from source aggregation semantics, preserving absence where first/last/count distinguish it. Never broaden shared snapshot admission or HM1's validated-input contract. No permissive coercion or nonfinite normalization is authorized. HM3 can integrate the established finite/null boundary while these explicit HM4 checks remain open; do not claim integrated blank-File acceptance first.

All-missing native evidence may confirm accepted transparent-border geometry or require a bounded HM2 corrective amendment. Do not silently override the renderer inside session integration. No-series admission is already decided above and must not be conflated with all-missing selected series.

- [x] Implement the new policy and inactive session helper with focused behavioral RED/GREEN; verify empty selection/re-add/reopen, raw mixed-unit Heatmap values, unchanged ordinary unit rejection and Count units.
- [x] Wire all unions, selectors, runtime/caller/theme, transactions and UI in one serial join. No partially activated commit or hidden flag.
- [x] Add `tests/unit/chart-application/heatmapSession.test.ts` and `heatmapSessionOwner.test.tsx` using current fixtures. Cover category recapture/stale rejection, aggregate off/on, order/removal/re-add, no-switch UI/rejection, inactive-option preservation, consecutive appearance edits, both categorical axis leaves, tooltip-off, paired gradient reversal, palette/theme refresh, gallery entry/exit including hierarchy capture-kind boundaries, and no-series reopen recovery.
- [x] Run new suites plus existing `applicationSessionTransactions.test.ts`, `applicationSession.test.tsx`, `callerInputs.test.ts`, `callerRoute.test.tsx`, `setupProjection.test.ts`, `setupTransitions.test.ts`, `chart-compatibility/comboSessionAssignments.test.ts`, `lifecycle.test.ts` and `hierarchySessionOwner.test.tsx`. Run accepted Heatmap data/controls/renderer suites once at the join. Add grid suites only if the admission boundary changes, and Histogram owner regression only if its command exclusion changes.
- [x] Fresh independent review checks actual source/evidence, then controller commits HM3b with inventory/breadth status updated. HM3 closes source integration only; identified-image Table/File, retained-FMP financial comparison, light/dark controls, refresh, fresh reopen and export remain application acceptance.

Every changed maintained production file, including shared owners, must pass 400 physical lines, 300 logical units and 50/function. Use the existing explicit changed-file inventory gate in [complexity checks](../../../docs/complexity.md), exact-file lint and fresh baseline-relative scoped/canonical typing with zero owned additions. Run explicit Vitest paths with `--maxWorkers=1`; one heavy suite/build at a time. Current lifecycle is 394 lines and outside scope. No heavy checks, production edits or commits were performed to prepare this plan.

## HM3b function-budget amendment

The accepted extraction leaves `applyOrdinarySessionTransaction` at 50 logical units. Within the same `applicationSessionTransactions.ts`, keep family/Setup handling in the exported function and move appearance dispatch into private `applyOrdinaryAppearanceTransaction`. Its command excludes the already handled family, Setup and hierarchy-only panels. Forward the narrowed local intent without casting the whole command. The helper routes Heatmap first, then explicitly rejects Heatmap-only intents for other families before preserving the existing appearance branch order. No new file or registry is needed. Root dispatch and its stamp/capture/commit orchestration remain unchanged. The exact reviewed helper signature and discriminants are retained in `artifacts/chart-heatmap/hm3-dispatch-amendment.md`; existing HM3b checks and caps apply.

Original reference preparation now records retained-FMP light/dark cells, all-missing selected-domain axes without numeric paint/gradient, and successful zero-series recovery. These are original observations, not candidate acceptance. See retained local evidence `artifacts/chart-heatmap/reference-final/prepared-reference.md`. Explicit blank CSV fields become null; the original parser filters one-field truncated rows. Do not generalize that finding to all sparse public-grid inputs.

## HM3a acceptance

Workspace `6262a976abec8f3a0ef508b9a59005ba807df375` contains only the two-file dispatch extraction. All 36 existing affected tests, exact-file lint, complete function/import parity and inventory-backed caps pass. The reviewer accepted unchanged scoped diagnostic sites with zero owned errors, while retaining the failed raw message comparison caused by upstream type-display ordering. This is not clean canonical typing. [Independent review](../../../artifacts/reviewed/chart-heatmap/dispatch-review.md). Subsequent HM3b source acceptance is recorded below.

## Reopen range boundary amendment

HM3b testing showed that the ordinary `resolveChartRange` intentionally discards stored selections with at most one column. Heatmap must preserve its explicit category-only selection after removing all numeric series and reopening. Add `application/applicationSessionRange.ts` to the writable boundary and share this admission through a small pure `application/heatmapRange.ts` adapter used by it and the already-owned `caller/chartInputs.ts`. Reuse the ordinary resolver for other cases; honor ignoreCellRange, generated/descriptor availability, selection order and row bounds. Never silently admit unknown columns or broaden ordinary-family range behavior. Cover a category-only range, the existing (None) ordinal category with zero series, and a sole visible numeric field without an explicit category. A legitimate one-series selection must not expand to every generated field. Do not add a numeric placeholder or persistent range owner. This amendment follows the observed failing reopen case and remains subject to the same independent HM3b review and size checks.

The planned narrow `histogramEditorTransaction.ts` exclusion is now justified by TS2322 after widening the shared command union. Exclude only Heatmap-specific panels before Histogram forwards ordinary intents; preserve its current behavior.

## HM3b source acceptance

Workspace `09947a2d7bea7c93b71ad4dc74afcc1ae64f5033` integrates Heatmap through the existing chart session and editor. The [independent review](../../../artifacts/reviewed/chart-heatmap/integration-review.md) accepts 208 distinct planned checks, strengthened actual fresh-capture recovery, lint and whole-file caps. Scoped typing has no added production sites; inherited/reached diagnostics and the failed raw message comparison remain explicitly qualified in the review. This is source acceptance only. The packaged FMP journey, visual comparison, browser persistence and export remain HM4.
