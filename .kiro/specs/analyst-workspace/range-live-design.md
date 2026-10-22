# R4g live Range activation contract

Activate Range Bar and Range Area through the existing session, editor and renderer in one joined slice. Session/editor and navigation/pointer work run in two disjoint lanes; the controller freezes shared exports, joins both lanes and immediately proceeds to application and real-FMP acceptance. Neither lane is a separately accepted inactive milestone. No feature flag, disabled control or reduced Range surface satisfies this contract.

Implementation contract, 2026-10-22. Baseline Workspace `9f5a9c2d22d99fcd72d7721705c6e2fe0a6dfd43`. Evidence: local source maps `artifacts/chart-range/r4g-session-map.md`, `r4g-interaction-map.md`, `r4d-hit-contract.md`, and [accepted composition](range-application-design.md). This artifact records planned work, not executed acceptance. Paths below are relative to `vendor/workspace/terminalpro/src/components/General/Table/Chart/` unless stated otherwise.

## Frozen shared composition additions

The controller extends `echarts/rangeApplicationTypes.ts` before fan-out:

```ts
interface RangeApplicationInput {
  // Existing fields remain unchanged.
  readonly valueVisibleRange?: Window;
  readonly valueFullExtent?: Extent;
  readonly valueDataExtent?: Extent;
  readonly plotBottomInset?: number;
}
```

`valueVisibleRange` defaults to `[0, 1]`. `valueFullExtent` is an accepted full-domain decision, not observed extrema or an already cropped extent. When present, the value-axis owner invokes the existing numerical planner in window mode without replacing bounds or nicing again. The controller adds `fullExtent?: Extent` to `RangeValueAxisInput`; old calls preserve current behavior. `valueDataExtent`, when supplied without retained `valueFullExtent`, replaces only the observed value-domain operand before normal full planning. It never mutates the financial projection, tooltip values or captured observations. An empty extent is meaningful and must not fall back to the full data extent.

`plotBottomInset` defaults to zero and must be finite/nonnegative. Composition reserves it before the bounded measured-axis layout loop. It is additional to existing padding/caption/legend reservations and leaves the accepted final grid untouched afterward. Tiny remaining space produces the existing finite empty plot. B owns the reserved navigator geometry within that bottom area; it cannot subtract it a second time. Category window composition honors `categoryFullExtent` for ordinal as well as continuous categories.

The controller narrows `resolveRangeAppearance` to a named structural appearance operand containing only the fields it actually reads. Lane A can resolve editor appearance without inventing a viewport; composition continues to use the same resolver and precedence.

## Frozen live and pointer exports

Controller owns new `echarts/rangeLiveTypes.ts` and `echarts/chartPointerTypes.ts`. Existing `ChartRenderRequest` gains optional `projectPointer`; old families remain source-compatible. B implements the following exports:

```ts
type RangeComposed = Extract<RangeApplicationResult, { status: "supported" }>;
interface RangeLiveSettings {
  readonly navigatorEnabled: boolean;
  readonly miniChartEnabled: boolean;
}
interface RangeLiveSupported {
  readonly status: "supported";
  readonly composed: RangeComposed;
  readonly options: EChartsOption;
  readonly projectLegendSelection: NonNullable<
    ChartRenderRequest["projectLegendSelection"]>;
  readonly projectNavigationWindow: NonNullable<
    ChartRenderRequest["projectNavigationWindow"]>;
  readonly projectPointer: (applied: EChartsOption) => ChartPointerPlan | undefined;
}
type RangeLiveResult = RangeLiveSupported | Exclude<
  RangeApplicationResult, { status: "supported" }>;
// echarts/rangeLiveProjection.ts
function projectRangeLiveApplication(
  input: RangeApplicationInput, settings: RangeLiveSettings,
): RangeLiveResult;

interface ChartPointerPoint { readonly x: number; readonly y: number }
interface ChartPointerMatch { readonly key: string }
interface ChartPointerPick {
  readonly distance: number;
  readonly matches: readonly ChartPointerMatch[];
}
interface ChartPointerPresentation {
  readonly html: string;
  readonly anchor: ChartPointerPoint;
  readonly categoryPointer?: {
    readonly axis: "x" | "y";
    readonly coordinate: number;
    readonly label: string;
  };
}
interface ChartPointerPlan {
  readonly viewport: { readonly width: number; readonly height: number };
  readonly plot: RangeComposed["plot"];
  readonly pagination: boolean;
  readonly pick: (point: ChartPointerPoint, intent: "hover" | "click") =>
    ChartPointerPick | undefined;
  readonly present: (match: ChartPointerMatch) => ChartPointerPresentation | undefined;
}
interface ChartPointerBinding {
  setPlan(plan: ChartPointerPlan | undefined): void;
  clear(): void;
  consumeDoubleClick(point: ChartPointerPoint): boolean;
  dispose(): void;
}
// echarts/rangePointerBinding.ts; no chart instance leaves lifecycle.
function createRangePointerBinding(
  container: HTMLElement, onError: (error: unknown) => void,
): ChartPointerBinding;
```

`ChartPointerPlan.plot` should use the existing neutral plot-rectangle type when the controller writes the type, avoiding a runtime or semantic dependency on Range in shared renderer code. The match key is opaque to the binding. B preserves field slot, group slot, endpoint and raw identity in its immutable match data; `present` must not parse a lossy display label or query engine targets to recover them.

B owns an `EChartsOption` intersection carrying immutable `openbbRange` metadata with family, exact composition and source input. Every initial/legend/navigation result carries fresh metadata. `projectPointer` reads metadata from the **final returned options**, after all callbacks; it never reads metadata from native `getOption` or closes over a mutable last composition. Native options supply only current legend and zoom state. Callback composition failures throw into the existing lifecycle error boundary; initial unsupported/invalid results retain their diagnostics.

Lane A's new `application/rangeSessionProjection.ts::projectRangeSession` follows the existing session projection input and result conventions, dispatches the real factory above and returns ready `kind: "range"` only on a supported live result. Its ready state exposes `projection: live.composed` and forwards all four renderer operands. It owns setup/editor/stamp metadata and legend scope. It does not call a second layout or duplicate B's composition call. Controller freezes the Range branch of the ready union and family edit intent before dispatch.

The binding owns only transient selection, page, drag detection, listeners and tooltip DOM. `setPlan` clears old selection before replacement. `clear` makes stale picks impossible. `consumeDoubleClick` returns true only when the current valid source node-event rule consumes the double-click; otherwise lifecycle retains its established reset behavior. The controller wires this explicit return value into reset handling. Hover remains inactive when actual container size differs from plan viewport, until a fresh composed plan arrives. Failures clear pointer state and invalidate the existing error/export path.

## Exclusive files and execution

Use two fresh-context implementers, `gpt-6.1-sol` with high reasoning, and one fresh independent reviewer after a slot is available. Each handoff includes this contract, both maps and 400 physical lines/file, 300 logical units/file, 50 units/function. Workers are not alone in the checkout; preserve other edits. No installs, builds, shared fixture mutation, staging or commits in worker lanes.

| Owner | Exclusive writable production paths |
| --- | --- |
| A: live session/editor | New `application/rangeSessionTypes.ts`, `rangeSessionSelection.ts`, `rangeSessionProjection.ts`, `rangeEditorState.ts`, `rangeEditorTransaction.ts`, `rangeAxisTransaction.ts`; new `editor/range/*`; existing `compatibility/editorBindings/{types,selectApplicationEditorState,mapApplicationEditorEvent,eligibility}.ts`, `editor/combo/comboEditorMode.ts`, `editor/setup/ChartSetupPanel.tsx`, `editor/ApplicationSeriesEditor.tsx` |
| B: navigation/pointer | New `echarts/rangeLiveProjection.ts`, `rangeNavigator.ts`, `rangeNavigationWindow.ts`, `rangeNavigatorOverview.ts`, `rangeNavigationPolicy.ts`, `rangePointerCandidates.ts`, `rangePointerPick.ts`, `rangePointerTooltip.ts`, `rangePointerBinding.ts`, `rangeSpatialAdapter.ts` and cohesive responsibility splits; existing `echarts/rangeBarGeometry.ts`, `rangeAreaHit.ts`, `rangeAreaSeries.ts`, `rangeBarTooltip.ts`, `rangeAreaTooltip.ts`, `cartesianNavigator.ts` |
| Controller: shared preparation and join | New `echarts/rangeLiveTypes.ts`, `chartPointerTypes.ts`; existing `echarts/{rangeApplicationTypes,rangeApplication,rangeAxisLayout,rangeValueAxis,lifecycle}.ts`, `EChartsHost.tsx`; `application/rangeAppearance.ts`, `comboSessionTypes.ts`, `applicationChartSessionTypes.ts`, `applicationSetupSelection.ts`, `applicationSessionDispatch.ts`, `useApplicationChartSession.ts`, `applicationSessionRuntime.ts`; caller input/generated-option owners, `AgChartView.tsx`, `caller/useCallerDock.ts`; shared extraction helpers; inventory, manifests, specs, breadth and delivery records |

An optional cohesive split remains in its owner's directory/prefix and must be reported before creation. Existing files not listed are read-only until the controller records an exclusive transfer. A owns new `tests/unit/chart-application/rangeSession*.test.*` and `rangeEditor*.test.*`; B owns new `tests/unit/chart-compatibility/rangeLive*.test.*`, `rangeNavigation*.test.*`, `rangePointer*.test.*` and `rangeSpatial*.test.*`. Controller owns changes to existing regression tests and joined/browser tests. No test stub survives joined acceptance.

The controller creates shared type declarations and implements value/full-domain/inset seams first. A and B then implement against those exports concurrently. Parent shared runtime/caller/lifecycle edits may proceed only in the table's exclusive paths. Once A/B freeze, an independent reviewer challenges the combined consumer, and the controller repairs findings in their owning lane. Open the live gates only in this joined implementation; do not introduce a temporary feature flag. Commit only reviewed frozen scopes.

## A: retained state and controls

Use current baseline/range/setup selection and `projectOrdinarySetup(..., "statistical-observations")`. Require captured category provenance and use current `baseline.model.categoryAxisType`. Save category edits into that native semantic field; runtime-only axes cannot override composition. Preserve dashed `range-bar`/`range-area` saved namespaces, unknown siblings, interval arrays and advanced policies. Rehydrate latest state and reject stale stamps before mutations. Position/type/time-format edits require a Range structural adapter and must survive fresh-owner reopen.

Retain all existing setup, theme, titles, legend, padding/background, physical/semantic axis, labels, tooltips and navigation controls. Add Bar direction and inside/outside label placement/padding; add Area interpolation with supported tension/step position. Area retains markers, missing-data and shadow. Bar retains its original hidden category-type/tick selectors; that existing eligibility must not become a blanket Box restriction. Preserve native-Date provenance when evaluating numerical-selector eligibility. Statistical grouped capture is not Grid hierarchy. No category/series switching for Range.

Parent completes descriptor admission and generated Range series; initial-axis identity and synchronization preserve saved semantic preference while replacing stale inferred facts. Force recapture across snapshot-policy changes, including Box-to-Range provenance needs; Bar-to-Area can reuse valid Range statistical capture. Refresh, changed selected category and bounds must reach the same session source and invalidate stale editor commands.

## B: navigation and source picking

The navigator slider targets physical x: category for vertical Bar/Area, value for horizontal Bar. Wheel and pan retain independent physical windows as specified in the source correction below. Use `openbb-navigator` and `openbb-range-inside`, preserving slider, miniature, wheel, pan and reset. Main axes already contain a cropped domain, so native zoom must target a silent full-domain carrier axis on the main grid; it cannot crop the main financial axis again. Prove the carrier against installed ECharts. Singleton transport is `[0,1]` while raw value identity stays constant.

Read full composition once for each new source/scope. Retain its accepted category full extent across navigation and legend replans; re-evaluate enabled-field full value extent on legend changes while preserving the normalized window. A crop uses retained full-domain plans. B resolves source Zoom-dependent y autoscaling explicitly from retained source/settings; navigator visibility alone does not enable autoscaling. Dependent autoscale produces a normalized window against the retained full scale, without nicing it again; projection identities stay intact. Record exact default/enabled/bounds/padding/minimum-item rules in the policy module's tests before accepting that branch; do not substitute Box statistics.

The miniature has its own full-window composition and plot pixels; never clone main custom callbacks carrying cropped geometry. Resolve `showInMiniChart`, per-series tooltip enablement and pagination through the accepted theme/generated/saved precedence in B's policy helper. These policies are distinct from main legend visibility. Pagination defaults false. Reserve navigator height before main layout using `plotBottomInset`, then decorate without moving the main grid.

Generate Bar midpoints from the actual rounded, grouped, minimum-stroke rectangles before clipping. Generate Area high then low endpoint candidates in encounter order, preserving marker size even when markers are disabled. Use the exact current mapping after legend, window, resize and reverse changes. Retain tolerance-1 visibility, category-like major-axis choice (otherwise x), major/minor ranking, later per-field exact ties, literal marker-adjusted scalar distance, reverse-series comparison and zero-distance matches described in the source contract. Native snap/target order never chooses the winner.

Keep Bar exact-shape mode/fallback separate. Prefer the existing MIT Community pure spatial helper through an isolated version-pinned adapter after proving renderer-free instantiation. If it is not publicly callable, retain the source algorithm under its applicable license with exact tree insertion/traversal tests and provenance; do not substitute reversed rectangle order or claim parity from a convenient tie rule. Area exact range returns no shape match. Any inaccessible/unsupported retained source policy is a reported blocker for its claim, not silently nearest behavior.

Shared rows use typed exact raw category equality, selected-field identity, and first valid matching observations in other enabled tooltip-enabled fields in chart order. Compact/single/disabled modes remain effective. Deliberate Bar gap repair: a valid picked observation formats its own raw matching values even when the original compact-node/raw-index guard could suppress it. Do not reproduce lost rows or borrow another node's style. Add a post-gap regression and disclose this narrow source difference. A retained-runtime comparison remains required before claiming the original UI exhibits the inferred bug; do not describe unexecuted source analysis as a runtime result.

Blank-plot pointermove reaches the pure picker; title, legend and miniature do not. Paging is click-to-next with identity retention/wrap, never wheel paging. Drag release must not page. Disable native automatic Range tooltips while the explicit pointer plan is active. Leave, stale revision, scope change, navigation, resize, zero-size defer, failure and disposal clear prior plans. DOM coordinates are CSS-local and must remain correct under browser scaling.

## Joined acceptance and delivery

Run focused lane checks with the existing one-worker configurations. Join once and run actual session-to-composition-to-renderer tests, existing Range/Box/ordinary regressions at modified boundaries, strict scoped typing plus canonical baseline comparison where inherited diagnostics require it, scoped no-fix formatting and the existing inventory-backed complexity checker using explicit current fork manifests. No clean-typecheck claim may replace a baseline-delta result. The controller serializes heavy checks/builds and records commands, revisions, exits and artifacts.

Acceptance must show actual glyph and final candidate changes for 25%-75% ordinal/irregular-number/native-Date navigation; both Bar directions/reversals; no double crop; full miniature; slider/wheel/pan/reset; legend peer reflow; resize invalidation; zero-distance click paging; exact shared rows; disabled markers; and post-gap valid tooltips. Session tests cover semantic category override, recapture/refresh, direction/physical axes, generated/saved precedence, empty selection, every retained panel and fresh-owner persistence. Lifecycle tests cover stale and failed updates, disposal and export validity.

Then run the actual application in the identified candidate with real FMP data. Verify per-field extrema, units, periods/dates and transformations against the captured provider response; record endpoint/parameters/retrieval time without credentials. Exercise editor controls, theme, refresh, navigation, save/reopen and export for both Range families, plus relevant ordinary/Box regressions. Inspect a small set of real chart screenshots and publish sanitized selected samples with hashes. Missing entitlement or a failed control remains open, never a synthetic pass.

Reconcile tasks, breadth, inventory and README/docs checkboxes to the reviewed evidence in the completion commit. R4g source acceptance requires live joined consumers; full Range milestone acceptance additionally requires the identified-image/FMP/browser record. Build/publish once that meaningful milestone passes independent review, following the existing cadence; no foundation-only image is requested by this contract.

This contract is disproved by an inactive compose consumer, stale pointer pixels after a window change, a runtime-only category edit, hidden original controls, financial axes cropped twice, a miniature using main pixels, or declared source parity for an unverified fallback/tooltip behavior.

## Navigation source correction

Retain independent physical x and y windows. The navigator slider changes physical x; Zoom wheel scaling follows its configured axes after the horizontal-series flip. Treating every horizontal Range Bar interaction as physical x would change the original flow.

Read-only source review, 2026-10-22. Bundle identities and citation prefixes are recorded in local `artifacts/chart-range/source-contract.md`. This is source-derived behavior, not an executed original-runtime result. The controller requested this correction to the frozen live contract; no controls are removed or disabled to avoid the branch.

| Interaction | Retained source behavior |
| --- | --- |
| Navigator slider | Physical x; vertical Bar/Area category, horizontal Bar value. C15919-15925. |
| Wheel scaling | Zoom `axes` defaults to `x`. C25040 records `series.shouldFlipXY`; C25090-25099 swaps the requested axes for horizontal Bar. Default horizontal wheel therefore requests physical y/category. |
| Plot pan | C25063-25075 translates the existing physical-axis windows through the panner. It does not reuse wheel's axes filter. A full window cannot translate beyond its bounds. |
| Reset | Reset both physical windows to `[0,1]`, except when the current valid pointer node consumes the double-click. C24754-24760. |
| Dependent y autoscale | Runs only when Zoom is enabled and autoScaling is enabled, with default enabled when `axes === "x"`, padding 0.05. It operates on physical y, including horizontal Bar. M12983-13023, C25357-25377. |

The autoscale priority matters: a full physical-x window explicitly yields full y. Otherwise a finite calculated y window replaces the prior y window; an unavailable calculation leaves the prior y window unchanged. `applyChanges` recomputes autoscale before applying changes. Consequently default autoscaling can cancel a horizontal category-wheel request when physical x is full. With `autoScaling.enabled:false`, that category-wheel request remains. This surprising interaction must be checked against the retained runtime before claiming observed parity; do not silently replace it with a more intuitive rule.

Horizontal Range Bar inherits category-axis `xCoordinateRange` (M40928-40935). Its `getSeriesRange` ignores direction and returns financial high/low extrema selected by those category bands against the requested x fraction (C20370-20372; M38103-38130). ZoomManager then converts those financial values through the physical-y category scale (M13119-13178). Preserve this sequence. String ordinal categories normally give no finite conversion; numeric ordinal categories can match endpoint numbers exactly, so a blanket ordinal exclusion is incorrect. Continuous categories use their accepted full category scale. Padding applies in normalized scale space; explicit physical-y minimum or maximum pins the respective ratio to 0 or 1. The Range classes inherit `getVisibleItems = Infinity` (M21571-21573), so the configured default `minVisibleItems:2` does not impose a Range item-count cutoff.

The smallest integration seam is two silent full-domain carrier axes and independent native x/y zoom transport. Keep `openbb-navigator` as the physical-x slider. Preserve `openbb-range-inside` for the primary wheel/inside route and use a separately identified companion transport when the second axis needs state or panning. Range retention copies each native window by its identity; it must not overwrite every inside window with the slider window. A hidden state carrier may retain dependent-y autoscale without adding visible controls. Metadata on every returned option holds that exact composition; native options supply only current legend and window state. No mutable last-composition closure is needed.

The composition operands remain unchanged: `visibleRange` plus retained `categoryFullExtent` controls category; `valueVisibleRange` plus retained `valueFullExtent` controls value. For horizontal Bar map physical x to value and physical y to category. For vertical Bar/Area map x to category and y to value. Apply dependent autoscale to physical y, retaining its previous window on an unavailable result. Main axes must never be native-zoom targets. Miniature remains full domain.

Disproof checks are independent slider/wheel changes on horizontal Bar with autoscaling disabled, two-axis pan after both windows are cropped, default autoscale priority, finite numeric-ordinal conversion, no-result prior-y retention, reset of both windows, unchanged full miniature and final pointer geometry after each change. Installed-ECharts and retained-runtime checks remain required; source review alone does not accept the implementation.
