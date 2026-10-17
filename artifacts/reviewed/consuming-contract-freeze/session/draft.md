# Freeze the session handoff; retain explicit editor and rendering gates

Draft inputs for controller synthesis, 2026-10-17. Read-side session inputs, original storage destinations, five admitted column commands and the host freshness requirement are concrete review inputs. The write scheduler is blocked on an explicit adaptation of the existing widget updater; its current API cannot establish the completion/rebase guarantees below. Complete editor implementation and application activation also remain blocked. This artifact changes no specification approval, production source or task status.

The inspected candidate is Workspace `ea02ec15956dee8d2c8a06825387a570757db12d`; original owned source is `38dffc33389aca0e4a87e0e88d42f7067aa220df`. The input/output hashes are in [safe-hash-allowlist.json](safe-hash-allowlist.json). [editor-field-ledger.json](editor-field-ledger.json) has 295 total rows: 202 runtime capture rows, 88 inventory capture rows and five supported-command rows. Repeated cases and paired slider/number controls are intentional; these are 290 finite capture rows, not 295 independent observations or a complete inventory. No browser, suite, build, install, provider call or secret-file read was performed. Core steering `product.md`, `tech.md` and `structure.md` are absent; available complexity, documentation, delegation, testing and CI guidance was read.

## Ownership and dependency direction

Existing legacy/snapshot types and reducers -> capture/appearance/display adapters -> React session -> original entry and editor. The host remains the sole ECharts owner. The session coordinates ephemeral stamps, pending work and the existing widget updater; it does not own another storage copy, persisted envelope, engine instance or theme store. Original widget and grid owners continue saving and restoring their existing state.

Review these named interface proposals before freezing their consuming implementation. The write methods and completion status remain conditional on the updater/scheduler prerequisite below. Do not create empty type/hook modules merely to advance a phase. `buildRender` below is the explicit composition seam inside the chart application boundary, not a second renderer or a new state owner. Its implementation must call accepted snapshot validation, the controller-frozen appearance contract, trusted display-policy projection and the existing Cartesian mapper. Unresolved appearance or tooltip behavior returns diagnostics; it cannot be hidden behind this seam.

## Concrete proposed session contract

The following names reuse actual accepted types from `application/types.ts`, `compatibility/{legacyTypes,optionStateTypes,snapshotTypes}.ts` and `echarts/{lifecycle,EChartsHost}.tsx`. `WidgetT` and `NewWidgetT` come from the existing `components/types.d.ts`. `ThemeSelection` and `SeriesIdentity` are imported from the controller-frozen appearance contract; this lane neither duplicates nor broadens their definitions. The actual financial policy returns `string | number | Date`, including falsy formatter fallback; do not restore the older design's narrower string-return signatures.

```typescript
interface SessionSelection {
  readonly range: ResolvedRange;
  readonly categoryColumnId: string;
  readonly columns: readonly SnapshotColumn[];
}
type SessionSelectionResult =
  | { readonly status: "ready"; readonly value: SessionSelection }
  | { readonly status: "waiting" }
  | { readonly status: "invalid" | "unresolved";
      readonly diagnostics: readonly SnapshotDiagnostic[] };
interface SessionRenderInputs {
  readonly mode: "light" | "dark";
  readonly selectedTheme: ThemeSelection;
  readonly generated: RuntimeOptions;
  readonly chartBarFillEnabled: boolean;
  readonly formatting: FinancialFormattingInput;
}
interface SessionRenderInput {
  readonly stamp: SessionStamp;
  readonly baseline: OptionBaseline;
  readonly snapshot: ChartSnapshot;
  readonly display: ChartDisplayPolicy;
  readonly inputs: SessionRenderInputs;
}
type BuildSessionRender = (
  input: SessionRenderInput,
) => SessionResult<ChartRenderRequest>;
interface ChartSessionInput {
  readonly widget: WidgetT;
  readonly widgetFromJSON: WidgetT | null;
  readonly getWidget: () => WidgetT;
  readonly updateWidget: (update: NewWidgetT, forceStoreUpdate?: boolean) => void;
  readonly api: GridApi<Record<string, unknown>> | null;
  readonly gridDataRevision: number | null;
  readonly selection: SessionSelectionResult;
  readonly renderInputs: SessionRenderInputs;
  readonly buildRender: BuildSessionRender;
  readonly flushColumnState: () => void;
  readonly handleChartViewToggle: (previousEnabled: boolean) => void;
  readonly getHost: () => FreshEChartsHostHandle | null;
}
interface ChartSessionView {
  readonly baseline: OptionBaseline;
  readonly range: ResolvedRange;
  readonly snapshot: ChartSnapshot;
  readonly render: ChartRenderRequest;
  readonly settingsOpen: boolean;
}
interface SettingsCommand {
  readonly stamp: SessionStamp;
  readonly open: boolean;
}
interface ViewCommand {
  readonly stamp: SessionStamp;
  readonly enabled: boolean;
}
interface RangeCommand {
  readonly stamp: SessionStamp;
  readonly chartType: string;
  readonly range: ResolvedRange;
}
interface ExportCommand {
  readonly stamp: SessionStamp;
  readonly options?: ChartImageOptions;
}
interface ChartSessionActions {
  readonly column: (command: ColumnEditCommand) => void;
  readonly range: (command: RangeCommand) => void;
  readonly settings: (command: SettingsCommand) => void;
  readonly view: (command: ViewCommand) => void;
  readonly retry: (stamp: SessionStamp) => void;
  readonly exportImage: (command: ExportCommand) => SessionResult<string>;
}
interface ChartSession {
  readonly currentStamp: SessionStamp;
  readonly view: SessionResult<ChartSessionView>;
  readonly pending: boolean;
  readonly lastCommand: SessionResult<SessionStamp> | null;
  readonly actions: ChartSessionActions;
}
type UseApplicationChartSession = (input: ChartSessionInput) => ChartSession;
```

`selection` is an already resolved category/range/descriptor result, not raw provider rows. It is deliberately unstamped: the hook owns address/generation/revisions and stamps capture after receiving selection. The hook obtains the address through existing `getStateKey(widget, api.isPivotMode())` and rechecks it from the latest widget inside every storage transaction. Initial family fallback remains partition model -> root model -> widget configuration, with original default rules. The input API is the actual displayed grid; replacing it changes the generation. A null API/data revision or waiting selection yields waiting, without a storage write.

`renderInputs` explicitly supplies mode, shared `ThemeSelection`, generated original data-only options, root `chartBarFillEnabled` and the actual `FinancialFormattingInput` (period, decimalDigits including zero, global precision, category/Index definition and trusted helpers). The hook derives `ChartDisplayPolicy` with accepted `createChartDisplayPolicy`. It compares immutable mode/theme/generated data with descriptor-safe data equality preserving own undefined, compares the bar-fill boolean, and compares formatting scalar values plus bound Index formatter/helper identities. Every semantic change advances render revision even when observations do not change. Callback identity alone is not the invalidation signal. `buildRender` receives those inputs and policy explicitly and may not obtain theme/formatting/bar-fill state through a hidden store closure. It uses the single `resolveApplicationAppearance` resolved/invalid/unresolved result and existing extended `ResolvedCartesianStyle` through the existing mapper; no partial host options or second mapper. The controller owns the exact shared import location. A loop-produced palette is not a selected-mode identity. `buildRender` must return the supplied stamp and `revision === stamp.renderRevision`, with no store/GridApi access or persistence effects.

The session/options integration owner supplies `chartBarFillEnabled` from the actual root widget storage, default false as in `themes.tsx:248-250`, and refreshes the immutable render inputs when that source changes. A bar-fill change advances render revision without changing financial observations/dataRevision or persisting derived theme/style. `themes.tsx:234-236,289-294` adds `createItemStyler(..., shouldFillBars)` to custom and stock themes; projecting theme data alone intentionally omits this executable closure and would otherwise lose its dynamic root-state dependency. The explicit boolean is therefore required in the `AppearanceInput` call. It does not authorize executing saved callbacks, treating enabled fills as ordinary palette allocation or claiming their unproved effect complete. Enabled distinct-category fills retain their named source/effect/capture gate.

For the supported ordinary snapshot, `buildRender` constructs ordered `SeriesIdentity` values by traversing `snapshot.selectedColumnIds`, resolving each numeric `SnapshotColumn`, and assigning `id = column.id`, `sourceKey = column.id`, `label = column.label`. This is an explicit binding rule, not a store lookup or label match: `gridCapture.ts:123-153` reads each numeric selected ID through public GridApi `colKey: id` and stores its raw value under `values[id]`; `snapshotTypes.ts:14-23,27-33` makes those stable descriptor IDs the observation keys; `cartesian.ts:91-101,197-199` selects descriptors in the same order and consumes `row.values[column.id]`. Appearance's sourceKey thus denotes that admitted numeric binding. This evidence does not establish that every arbitrary AG `field`/`colId` or transformed yKey is interchangeable. A consuming path with a different source-key mapping must supply an explicit reviewed immutable binding map at the input boundary or remain unresolved; no hidden store/metadata inference is admitted here. Duplicate labels retain separate IDs and changing selected order/bindings triggers data/render invalidation.

`view` represents the current committed requested render; `pending` describes rendering, and remains true until its host receipt is accepted. It must not lock text entry while waiting for a host render. The void write methods and `lastCommand` are provisional: the current `updateWidget` has no admission/completion receipt, so these types do not yet define a safe write scheduler. `Widget.hooks.tsx:255-280` schedules React state; returning from it cannot prove commit, rejection, unchanged outcome or backend persistence. The controller must freeze the completion port before implementing these methods. Command receipts are ephemeral and cannot become a saved command log, optimistic widget copy or success toast used as acceptance.

## Latest-storage transaction and invalidation

The prior one-pending-write-until-next-view rule is withdrawn. It could discard successive title keystrokes or remain locked forever after a rejected/unchanged command, because neither outcome necessarily produces a widget commit. Safe scheduling is an explicit blocked interface, with the following required semantics rather than a claim that the current updater supplies them:

1. Every event receives an ephemeral sequence/ticket and a captured displayed stamp. Admission validates its address, generation and input shape and acknowledges admitted or rejected immediately. It does not equate admission with application. Admit continuous edits from the same valid editor interaction while earlier edits/rendering are pending; never silently drop them or disable an original control to avoid scheduling.
2. Preserve admitted event order and complete every ticket exactly once with applied, unchanged, invalid, unresolved, stale or cancelled. Rejection and unchanged completion release their ticket directly; they cannot await a nonexistent widget/render commit. Applied completion is acknowledged by the existing widget owner only after actual acceptance into its current state. Backend saving and host application remain separate acknowledgements.
3. An admitted burst must be evaluated against each current `previous` widget in sequence. Each reduction derives stateKey, pivot mode, selected baseline, current original model and storage from that `previous`, preserving intervening unrelated widget changes. A same-interaction title edit may be rebased across earlier admitted title edits; an event from an unadmitted obsolete view/address/generation may not be silently restamped. The exact interaction token, completion-port types and same-field coalescing policy are not frozen here. Any coalescing must explicitly complete superseded tickets and preserve the latest full entered value. Range/family/data or external same-field changes require an explicit stale/rebase decision, not an arbitrary last-write rule.
4. For `column`, the accepted reduction remains `applyColumnEdit` with latest validated storage, selected `baseline.options` as `resolvedOptions`, latest original currentModel, current series count and pivot mode. Stamping the scheduler's re-evaluated command must follow its reviewed rebase policy; bypassing `validateSessionStamp` would violate the accepted pure contract. Preserve initialize/synchronize semantics, unknown/inactive-family options and other partitions. Never persist composed appearance, resolved style, functions or ECharts options.
5. The replayable reduction is pure: stale/invalid/unresolved/unchanged returns the identical previous widget; engines, grid, downloads, persistence and receipt callbacks do not run inside it. Publish revision/render invalidation only for accepted semantic changes after owner completion. A generation change cancels pending tickets exactly once; late work cannot revive them. No optimistic widget mirror is introduced.
6. Address change, grid replacement, chart exit and unmount invalidate generation and reset data/render counters. Data/range/filter/sort/selection/order refresh advances data and render. Theme, family, options, formatting or retry advances render; family/range changes also advance data whenever bindings/observations change. Settings open/close alone writes the existing root flag and changes panel layout; it does not change financial data. Resize reuses the same render revision. Counter overflow starts a fresh host/session lifetime.

## Existing widget updater prerequisite

Observed source `components/Widget.hooks.tsx:255-280` is not a replay-safe functional transaction port. At line 260 its React updater assigns `newWidget = newWidget(currentWidget)`, changing the captured request from function to object. A replay/rebase can therefore reuse the prior object instead of reevaluating the function against its new previous widget. The same updater changes `needsUpdateRef`, queues `storeUpdateWidget` and calls `contextOverride.updateWidget` while computing React state. A pure callback supplied by the session cannot repair these enclosing replay and side-effect hazards.

Before session write activation, adapt this existing widget owner to retain the immutable functional request on every evaluation, distinguish accepted change from unchanged/rejected/cancelled outcomes, and deliver owner completion plus persistence/context effects once per accepted operation outside replayable state calculation. The actual completion/admission API is a design prerequisite, not an API already available from `updateWidget`; do not await inferred commits, mutate a receipt ref inside the updater or add a second widget/store owner to simulate it. Controller synthesis must settle this port and the scheduler interaction/rebase types together; until then `ChartSessionInput.updateWidget`, write-action return types and `lastCommand` remain blocked proposals.

The integration owner exclusively owns the future adaptation in `components/Widget.hooks.tsx` and any cohesive extracted widget-update responsibility, with controller ownership of shared API types. Its measured whole-file baseline is 307 physical lines on this inspection, leaving 93 physical lines before the 400 cap; logical/function metrics were not run. Plan extraction if required and inventory all maintained changes; no implicit exception. The session worker must not independently patch the owner or persistence/context delivery.

Required focused evidence before freeze/acceptance: invoke the same functional request repeatedly against distinct previous widgets and verify rebasing preserves intervening fields; rapid title input before any render completion retains the final complete text and ordered ticket completion; unchanged, invalid, unresolved and stale operations complete without waiting for a commit; generation teardown cancels all admitted tickets once; one accepted operation causes one persistence/context delivery despite replay, while rejected/unchanged/cancelled work causes none; injected effect failures do not replay state mutation or lose completion. Separately verify explicit save/reopen behavior. These are proposed tests, not checks run by this artifact lane.

Generation resets render revision to zero. Therefore key the existing host by address plus generation, or otherwise dispose/remount its owner at that boundary. Passing zero to a reused host whose pending revision is greater would be rejected as stale. Do not make host revisions a second independently incremented counter.

Malformed external input is invalid; structurally valid but unproved original effects are unresolved; late work is stale; unavailable grid/host/application commit is waiting. Preserve diagnostics and saved data. Last-good pixels may remain visible during retry only with explicit stale state; export cannot treat them as current. Return-to-table and retry remain reachable through existing application failure handling. None of these engineering outcomes authorizes an unavailable shipped replacement screen.

## Five admitted column events and original state destinations

| Event | Accepted value | Exact option patch | Family boundary |
| --- | --- | --- | --- |
| `title-text` | string, including empty | `bar.title.text` | groupedColumn and stackedColumn |
| `title-enabled` | boolean | `bar.title.enabled` | both column families; retain text while disabled |
| `legend-position` | top/bottom/left/right | `bar.legend.position` | both column families |
| `stroke-width` | finite number >= 0 | `bar.series.strokeWidth` | both column families; UI slider 0..10 does not narrow validator |
| `tooltip-mode` | single/shared/compact | `bar.tooltip.mode` | groupedColumn only; exact valid stacked event is unresolved |

Multiple is the UI label for `shared`; it is not a stored enum. Malformed stacked events remain invalid. `mapColumnEditorEvent` and `applyColumnEdit` already implement these exact distinctions. No arbitrary option path, line event, family switch, Aggregate or transpose command is admitted by this union.

| Action | Storage/effect ordering |
| --- | --- |
| Option command | Existing integrated reducer writes root `chartType`, `totalSeries`, `isPivotMode` plus `storage[stateKey].chartModel` and strips root `theme` from stored options. Root widget `chartOptions` is not replaced by derived render options. |
| Range command | Existing `applyRangeTransition` writes only `storage[stateKey][chartType].cellRange`, retaining original range metadata/bounds and ordered IDs. Original callback additionally writes root `chartType`; the consuming session must compose that root write in the same latest-widget transaction. This does not masquerade as an option patch or invent a model update. |
| Settings action | Integrated settings toggle writes root `chartSettingsOpen`; docked close explicitly writes false. Original hook inspected DOM menu visibility before opening/closing. Proposed controlled panel uses actual controlled open state as that visibility source, with the same root destination. Original delayed listener attachment is source behavior, not a need to retain anonymous DOM listeners. |
| View toggle | Set `previousChartEnabledRef` to the prior value, flush pending column-state save, then functional root `chartView.enabled` update, then invoke existing toggle handler with the prior enabled value. Original source resets its previous-enabled ref after 1 second on exit. Retain the restore protection; test its timing rather than assuming timer duration proves correct restoration. |

The original entry's disabled predicate is whether any current column definition, including one level of children, has `chartDataType === "series"`; it disables entry only when chart is not already enabled. Preserve original button/Tooltip/Icon classes and mobile tooltip behavior. Do not substitute mapper support or numeric-unit validation for this predicate.

Original table exit clears chart-generated cell selection in `setPendingUpdate`, updates table options/rows/column definitions as applicable, restores saved column/filter/group state, and destroys the chart. Saved widths suppress opportunistic auto-fit when returning from chart; `previousChartEnabledRef` is shared across apply-column-state instances. The source strips scroll/selection/focus when saving table state and clears selection on update; it does not establish exact prior cell-selection restoration. That desired interaction remains a capture question, not a proven preserved selection claim. SSRM/custom/transposed paths have separate source branches and cannot be silently routed through the ordinary flat snapshot.

Original quick actions remain root writes: bar fill requires bar-mapped enabled chart and is disabled when `totalSeries > 1`; navigator and mini-chart are enabled-chart actions, default false, and enabling either writes the other false. Their enabled rendering effects remain gates. Detached forecast settings `hide: isForecast` is a separate predicate; the integrated session does not rewrite it. Original suppressed toolbar/save icons remain suppressed. Export menu conditions, filename, MIME/download initiation and detached behavior must be joined with their existing external owner; this PNG return interface does not define a replacement menu.

## Editor props and conditional field handoff

```typescript
interface ColumnEditorProps {
  readonly stamp: SessionStamp;
  readonly chartType: "groupedColumn" | "stackedColumn";
  readonly title: { readonly enabled: boolean; readonly text: string };
  readonly legendPosition: "top" | "bottom" | "left" | "right";
  readonly strokeWidth: number;
  readonly tooltipMode: "single" | "shared" | "compact";
  readonly onChange: (command: ColumnEditCommand) => void;
}
interface DockedChartEditorProps {
  readonly open: boolean;
  readonly stamp: SessionStamp;
  readonly onClose: (command: SettingsCommand) => void;
  readonly column: ColumnEditorProps;
}
```

These are the exact supported field-subcomponent inputs, not the complete docked editor's public props. Values must come from the same resolved effective view used to render, with disabled text/details retained; baseline options alone omit defaults. `DockedChartEditorProps` is the minimal admitted column handoff and cannot be used to ship a five-control panel. Complete props still need controller-frozen Chart family selection, Set Up category/series/reorder/transform intents, and all remaining typed field groups. Do not add a generic `onPatch(path,value)` escape hatch or capability-based visibility predicate.

Chart, Set Up and Customize labels, original group order, geometry, focus restoration, scroll and conditional fields remain full obligations. Component-local expanded group, active tab, scroll and focus references are transient UI state, not widget storage. Root `chartSettingsOpen` restores panel openness on chart recreation. Finite captures do not prove active-tab/scroll/focus retention through close, theme switch or family switch: capture those transitions before deciding retention/reset rules. Theme changes re-resolve effective values/render options without writing them into the original model or recreating the panel merely to reset it.

## Fresh export through the existing host

Current `EChartsHost.tsx:10-18` exposes only `exportImage(options): string` and `onError`; searches found no onReady/onRendered/onApplied callback. `lifecycle.ts:18-26,47-66,75-81,99-106` already returns applied/deferred/stale/disposed from mount/update/resize and tracks applied revision internally. `EChartsHost.tsx:39-43,57-58,66-68` discards those return values. A newly sized container can therefore have accepted newer deferred work before the ResizeObserver applies it; a data URL alone cannot certify which revision it exports. This is a candidate integration decision derived from current source, not an original AG observation.

Prefer this minimal additive receipt on the existing owner, preserving the old export method for existing callers:

```typescript
interface ChartRenderReceipt { readonly revision: number }
interface FreshChartImageRequest extends ChartImageOptions {
  readonly expectedRevision: number;
}
interface FreshChartImage {
  readonly revision: number;
  readonly dataUrl: string;
}
interface FreshEChartsHostHandle extends EChartsHostHandle {
  exportFreshImage(request: FreshChartImageRequest): FreshChartImage;
}
interface FreshEChartsHostProps extends EChartsHostProps {
  readonly onRenderApplied?: (receipt: ChartRenderReceipt) => void;
}
```

`ChartSessionInput.getHost` uses this proposed additive handle, subject to controller contract review. Ownership remains `echarts/lifecycle.ts` and `echarts/EChartsHost.tsx`; no session-owned engine/status store. The lifecycle's fresh export atomically requires mounted, sized, not disposed, and expected revision equal to both pending and applied revisions, then calls its existing PNG exporter. The host emits the applied receipt only after a successful mount/update/resize, using the actual request applied, including deferred-to-sized transitions. Equal stale updates do not emit false new receipts. No callback is emitted after cleanup or for failed/deferred work. The receipt means public setOption application, not final animation pixels. For export readiness, freeze animation completion/disabled-animation behavior at the mapper/host join and verify actual file pixels; do not infer settled output from the receipt alone.

The session accepts receipts only for its current keyed host and current render stamp. `exportImage` checks the command stamp, current commit/pending state and matching receipt, calls fresh export, then rechecks the stamp before returning a data URL. A failed update, hidden/zero-size host, old-generation callback, pending theme/data update or stale requested revision produces waiting/stale/diagnostics without a download. The external action retains filename/download behavior. Add focused lifecycle/host checks for old revision after deferred resize, mount failure, update failure/retry, generation remount, disposal and zero-size export; then an actual application export comparison after theme/data edits. These checks are planned, not run here.

## Exact remaining joins and review criteria

1. `AppearanceInput`/`AppearanceResult` and extended `ResolvedCartesianStyle`: controller appearance lane must supply exact resolved controls and render fields. `BuildSessionRender` must consume that contract with `ChartDisplayPolicy`; current mapper signature lacks display invocation. Tooltip hovered-series identity/null/tie/order/keyboard and settled export pixels remain named gates.
2. `FamilyChangeCommand`: do not freeze a chartType-only write. Requires destination original model plus original per-family range resolution, and observed family reset/restoration rules. Chart thumbnails remain original and complete in the final UI.
3. `SetupCommand` for category/series selection/order, Aggregate and Switch Category / Series: root `aggFunc` and `switchCategorySeries` evidence is distinct from option patches. Need reviewed transformed snapshot types retaining observation IDs, units, missing values and original restoration order before admitting these commands. Finite Sum/transpose evidence does not define general transforms.
4. Full docked props/field modules: ledger controls marked unknown need exact patches/effects, predicates, domain and light/dark/keyboard geometry evidence. Known finite edits may support bounded field work after review; they do not unlock activation. `ColumnEditorEvent` expansion is serialized by controller.
5. Host additive receipt/fresh export: controller must choose exact names and join animation behavior before task generation; current source does not already provide freshness acknowledgement. Table exit/range/root transaction and external export ownership must join together, not by separately removing guards.
6. `WidgetTransactionPort` and session admission/completion/rebase types: exact API remains blocked pending the existing widget-owner adaptation above. Current void `updateWidget` cannot supply the required acknowledgements; read-side session types and five pure command mappings do not establish a safe continuous editor write path.

Requirements 4.2/4.7 require real save/reopen/refresh state and financial data retention, beyond outgoing payloads. 4.8/4.9 require original controls/predicates/effects, integrated light/dark comparisons, table return and fresh export. 10.4 requires isolated bounded runs; 10.5 requires actual test/evidence paths in breadth; 10.6 keeps missing/skipped/failing gates unverified. No breadth/spec status was changed by this lane.

Future production ownership: controller freezes shared types and serializes edits to `application/types.ts`; one session lane owns `application/useApplicationChartSession.ts` and session composition; one integration owner owns `AgChartView.tsx`, `hooks/useChartOptions.tsx`, table context/update-state callers and guards; host owner exclusively changes lifecycle/host; editor lane owns `editor/**` after field interfaces are frozen. Apply 400 physical lines/file, 300 logical units/file, 50/function to whole modified files and register scope in the existing complexity inventory/checker. Split by cohesive responsibility, with no empty forwarding modules or implicit upstream exception. Preserve independent review, fresh verification and final shared-module audit. This draft itself is evidence-only and outside production caps.
