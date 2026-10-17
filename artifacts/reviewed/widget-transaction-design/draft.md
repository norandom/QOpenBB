# Add a chart write port to the existing widget owner

The smallest candidate is an additive chart-only write port in `useWidgetSync`, with completion metadata in that hook's existing React state owner. It requires a narrow repair of the captured functional-request mutation and an explicit external-fence join. It does not require converting every widget mutation into a new transaction framework. This is design research for review, not an approved implementation or a declaration that the scheduler is ready.

Current Workspace is `ea02ec15956dee8d2c8a06825387a570757db12d`. Source inputs and this draft are hash-bound in [safe-hash-allowlist.json](safe-hash-allowlist.json). No frozen `session/**` artifact was changed. No production edit, test, browser, build, install or network operation ran.

## What the actual owner does

`Widget.hooks.tsx:92-96` owns the provider widget in `useState`. `Widget.context.tsx:172-199` exposes that widget and its existing updater. Both `getWidget` and the subscription's `providerWidgetRef` use `useCreateRef`, whose assignment occurs in a passive effect (`useRefHooks.tsx:29-36`); neither is a transactional latest-state accessor for an event racing a pending React update.

| Existing setter path in Widget.hooks.tsx | Behavior that a compatible envelope adapter must preserve | Separate concern |
| --- | --- | --- |
| Preview replacement, 107-112 | Replace with supplied preview context widget after first render | Root replacement invalidates chart interaction; no new persistence |
| Initial external staleTime, 153-157 | Add fifteen-minute default only when undefined | Preserve initialization/defaulting, rather than making it a chart command |
| Group subscription, 189-225 | Update linked groups, parameter groups, secondary tickers and ignored parameters | `updateWidgetGroupValues` mutates its argument; `triggerCustomEvent(updateQueryParams)` currently runs inside the state updater |
| Subscription innerTab, 228-230 | Apply inner tab change | No chart option command or automatic save invented |
| Public/custom-event updater, 255-280 | Existing NewWidgetT replacement or function; force-store flag, persistence gate, override callback | Line 260 mutates captured request from function to object; replay can skip latest-previous evaluation; store/context effects also run inside React calculation |
| Refresh event, 295-303 | Set refreshQuery timestamp; trigger runParams for Omni/SSRM | Date.now and the queued custom event currently occur inside the updater |

This is an inventory of six setter paths, not authorization to fix all their behavior. The group helper's mutation is source-proven (`lib/utils/app.ts:636-690`), but its unrelated semantics need not be redesigned merely to add chart writes. The compatibility adapter cannot discard another path's update or reset chart completion metadata by accidentally treating a widget replacement as the whole owner envelope.

Existing persistence is also narrower than a commit receipt. `needsUpdateRef` tracks unsaved provider changes; `saveToStoreCb` copies the provider widget to AppStore on saveWidgets, beforeunload and subscribed cleanup. Ordinary chart-option edits are not selected by `shouldPersistWidgetUpdate`; its current triggers include identity fields, parameter groups and group/ticker changes. AppStore `updateWidget` updates in-memory owned/shared dashboard state (`lib/state/app.ts:1941-2010`); it is not an acknowledged backend write. `dispatchSaveState()` dispatches a synchronous CustomEvent and its async function resolves with dispatchEvent's boolean (`lib/utils/utils.ts:184-191`). Awaiting it does not await a pending React chart edit or backend persistence.

## Compare the two bounded choices

| Choice | Scope and benefit | Limitation / review decision |
| --- | --- | --- |
| A: additive chart port, same owner envelope | Replace the owner value with `{widget, chartCompletionJournal, ...chartMetadata}`; retain six setter call sites behind one widget-only compatibility setter. New chart reduction and effect delivery are separate, explicit paths. Existing API remains. | Mechanically adapting the owner shape still needs six-path compatibility tests. The captured NewWidgetT mutation must be fixed narrowly for interacting legacy functional writes. Unrelated legacy callback side effects receive no new purity/exactly-once guarantee. Preferred candidate for the next refinement. |
| B: whole-owner action reducer/outbox | Convert subscriptions, refresh, preview, public updater and save paths to named pure actions with common postcommit effects. It can settle more existing replay issues. | Much broader behavioral surface, helpers and save coordination; no evidence authorizes it as required chart work. Keep as an alternative only if A's compatibility tests expose an unavoidable seam. |

Preparing arbitrary legacy functions outside React replay is not the default recommendation. A prepared object can become obsolete while another owner update commits. Automatically retrying preparation can repeat an impure legacy callback; never claiming exactly-once callback execution is essential. For chart requests, use only audited pure reductions against the actual owner previous widget. Do not introduce an optimistic widget ref or a second store to make outside-React preparation appear atomic.

## Candidate chart-only interfaces

The names below are proposed types in a cohesive new chart-write module, not additions to the oversized existing `components/types.d.ts`. The reducer is an owned pure callback composed from the existing chart reducers; this is not a public arbitrary transaction API. `WidgetT`, `ColumnEditorEvent` and `SnapshotDiagnostic` are imported existing types. No persisted schema changes.

```typescript
interface ChartWriteFence {
  readonly stateAddress: string;
  readonly generation: number;
  readonly dataRevision: number;
  readonly environmentRevision: number;
}
interface ChartInteraction {
  readonly id: number;
  readonly field: ColumnEditorEvent["kind"];
  readonly fence: ChartWriteFence;
  readonly displayedRenderRevision: number;
}
type ChartWriteDecision =
  | { readonly status: "changed"; readonly widget: WidgetT }
  | { readonly status: "unchanged" }
  | { readonly status: "invalid" | "unresolved" | "stale";
      readonly diagnostics: readonly SnapshotDiagnostic[] };
interface ChartWriteRequest {
  readonly interaction: ChartInteraction;
  readonly sequence: number;
  readonly reduce: (previous: WidgetT) => ChartWriteDecision;
}
type ChartWriteAdmission =
  | { readonly status: "admitted"; readonly ticket: number }
  | { readonly status: "invalid" | "stale";
      readonly diagnostics: readonly SnapshotDiagnostic[] };
type ChartWriteCompletion =
  | { readonly ticket: number; readonly status: "applied" | "unchanged";
      readonly ownerRevision: number }
  | { readonly ticket: number;
      readonly status: "invalid" | "unresolved" | "stale" | "cancelled";
      readonly diagnostics: readonly SnapshotDiagnostic[] };
interface ChartWritePort {
  publishFence(fence: ChartWriteFence): void;
  beginInteraction(
    field: ColumnEditorEvent["kind"],
    displayedRenderRevision: number,
  ): ChartInteraction | null;
  submit(request: ChartWriteRequest): ChartWriteAdmission;
  endInteraction(interaction: ChartInteraction): void;
  cancel(): void;
  subscribe(listener: (completion: ChartWriteCompletion) => void): () => void;
}
```

Admission assigns a mounted-owner ticket outside replayable React calculation and dispatches an immutable chart action. It acknowledges accepted scheduling, not widget application. Malformed or already obsolete interactions reject immediately without waiting for a render. Subscribers receive completions after the committed owner processes admitted requests; no callback runs in the reducer. The chart-specific listener/ticket registry contains only callback and identity metadata, never another widget copy.

Each admitted pure reduction runs against the owner envelope's current `previous.widget`. It validates the fence, interaction and sequence before calling the session's existing reducer composition. Do not mutate the request, captured command or previous widget. Throwing reductions become invalid completions without a widget change. A changed decision updates `widget`, dirty revision and owner revision; unchanged/rejected decisions retain the widget and owner revision but append a completion record. The envelope therefore commits completion metadata even when the widget does not change. Completion never waits for a nonexistent widget-value commit.

The journal retains every completion in a batched render; a single `lastCompletion` slot would lose earlier title/slider events. A postcommit effect drains records and acknowledges their IDs. Acknowledge housekeeping removes only records at or below the delivered ID, preserving records appended by later actions. Effect cleanup/replay cannot deliver an ID again within the mounted owner: claim the ID in a delivered-ID ref before invoking listeners. Catch listener exceptions independently so one subscriber cannot strand later completions. An interrupted React calculation produces neither committed journal entries nor effects. Remount creates a fresh identity/registry; no claim spans a destroyed runtime.

This proposed envelope is the current provider's state value with ephemeral completion metadata, not a second widget owner. The existing widget-only compatibility setter applies `WidgetT | ((previous:WidgetT)=>WidgetT)` to `envelope.widget` and preserves chart metadata. All six existing call sites can continue using that setter; they are not converted into chart actions. If a replacement changes the widget/address or another write affects the protected chart field, it invalidates the active chart interaction through the reviewed guard rule. The exact field-conflict classifier is a remaining join, not an assumption that any same-object identity means no change.

## Continuous title and slider edits

The first focus/pointer interaction requires the exact current displayed render revision and publishes a new interaction identity for one of the five admitted fields. Consecutive full title values or slider values receive increasing sequences under that interaction. Admit them while prior owner/render work is pending; do not disable input, wait for host rendering, or silently drop an intermediate admitted ticket. Do not coalesce in this candidate: preserve order and emit one completion per ticket. Input-local draft text/slider position may track the active gesture for immediate control feedback; it is not an optimistic widget/model copy.

During that interaction, the owner may rebase a later sequence across earlier accepted writes from the same interaction and across changes to unrelated widget fields. The reduction reads the latest selected baseline/storage each time. Own prior option writes advance render revision but do not alone invalidate the interaction. Rebase uses a fresh command stamp only after checking interaction/fence/field ownership; `applyColumnEdit` itself retains full stamp validation. A later unrelated control edit is not accepted merely because its old stamp happens to share a widget address.

On blur/pointer end, end the interaction after admitting its last sequence. Already admitted requests remain ordered; no new sequences may join. Address, generation, data selection/order, theme/mode/custom-theme/generated options, formatting or bar-fill change cancels the old interaction. An unadmitted old displayed event is stale. An external change to the same protected field makes remaining requests stale unless an explicit reviewed conflict rule says otherwise. No arbitrary last-write-wins, automatic restamping across an external fence, or unreported queued-value loss is permitted.

`environmentRevision` is a session-owned ephemeral fence for immutable mode/theme/generated/formatting/root-bar-fill inputs; it excludes only the current interaction's own option writes. `dataRevision` covers selection/range/order/bindings. These are guard inputs, not an additional persisted state model. The session remains the sole owner of its address and revisions.

## Fence publication and cancellation are not yet fully frozen

`publishFence` must define an ordering barrier with chart submissions inside the same owner. Any unprocessed old-fence request after that barrier completes stale/cancelled, never applied. An operation already accepted before a later barrier is an earlier ordered write; its old render/export still becomes stale under the session's existing revision rules. This linearization rule must be explicit in the reviewed refinement rather than describing all temporal overlap as cancellation.

Current source supplies no such port or common external theme/data barrier. The consuming integration must identify each actual source notification and publish its committed immutable fence before admitting a subsequent editor event. Publishing only on callback identity, palette iteration or a delayed unrelated passive effect is insufficient. In particular, current `useCreateRef` timing cannot prove this ordering. The exact registration point and same-field conflict classifier remain unresolved. The interface above is a concrete candidate, not a freeze of an unimplemented race solution. No action may read a hidden theme/store closure inside the replayable reducer.

Teardown synchronously closes admission and reports cancellation once for registered outstanding tickets; reducer/effect cleanup cannot revive them. A ticket already completed is not cancelled again. Pending journal records require identity checks against this owner. Owner effect errors are completion-delivery failures, not permission to rerun a state mutation. Widget state remains accepted if a later external effect fails.

## Postcommit effects and explicit save

For new chart writes, derive dirty/persistence/context intent as data during reduction, then perform external effects only after owner commit. Ordinary chart options preserve today's explicit-save policy; no new immediate dashboard save is added. A context override receives a committed widget through its existing callback only when that path historically receives updates. When multiple chart writes batch, publish the final committed widget once per committed delivery batch and retain each ticket's owner revision in its completion. Do not replay obsolete intermediate whole-widget snapshots into AppStore or an overriding context. The exact batching compatibility with preview/context overrides must be reviewed and tested.

An effect delivery ID is claimed before invocation, giving at-most-once invocation per mounted owner. If store/context delivery throws, record failure and leave dirty state for an explicit retry/save; do not automatically retry under the same claim or promise exactly-once delivery. AppStore invocation is not network acknowledgement, and a failed backend save remains a backend failure under existing dashboard error handling.

The narrow captured-request repair is `const request = newWidget` followed by evaluating that same function against each actual previous widget; never assign the resulting widget back into the captured parameter. This corrects latest-previous behavior, but does not make arbitrary legacy callbacks pure or move their existing effects after commit. No exactly-once promise applies to unaudited legacy functions. Review targeted interacting legacy/chart writes before accepting the additive path. If those tests require broader side-effect movement, stop and propose that concrete change rather than silently adopting choice B.

Explicit save after chart editing needs a real owner barrier for all tickets already admitted when save begins, then an AppStore copy of the final committed widget, then existing dashboard save. The current boolean-only saveWidgets event cannot provide that barrier. A proposed `flushChartWrites(): Promise<ChartWriteFlushResult>` could expose that narrow barrier, but its exact type and join with `dispatchSaveState`, keyboard save, dashboard save and contextOverride are deliberately not frozen here. It is not sufficient to await `dispatchSaveState()` as currently implemented. An explicit save must fail or report cancelled/invalid pending edits; it must not claim them saved.

For beforeunload and real unmount there is no reliable asynchronous React/network drain. Preserve best-effort flush of the last committed dirty widget; cancel unaccepted tickets and record this limitation. Do not promise pending keystrokes or backend delivery during browser termination. The application acceptance path must use the explicit completed save barrier before reopen/restart.

## Required evidence and exact remaining decisions

| Contract check, not run here | Failure it must disprove |
| --- | --- |
| Pure chart reduction replay/rebase against two different previous widgets | Captured request becomes an object; unrelated updates disappear; stale field overwrites |
| Rapid title and slider burst with React batching and delayed host | Dropped final value, caret/gesture interruption, overwritten completions, host-dependent admission |
| Invalid/unresolved/unchanged and throwing reductions | Admission hangs waiting for a widget change; repeated effects; unexpected mutation |
| Old address/data/theme/generated/format/bar-fill fence, teardown and late event | Hidden closure permits a stale write; cancelled ticket applies; old receipt revives owner |
| Six-path compatibility matrix | Preview/default/group/innerTab/legacy/refresh setters reset envelope or lose chart state; existing intentional events change |
| Legacy functional write interleaved with chart actions under replay | Narrow mutation repair still overwrites accepted changes or repeats unaudited effects |
| Postcommit delivery replay, batched operations and injected failure | Duplicate callback invocation, old full-widget store overwrite, failed effects marked delivered successfully |
| Save immediately after the final edit, then actual backend reopen/restart | Boolean event masquerades as a save barrier; final text/value absent from saved readback |

Minimal implementable candidate: the same-owner envelope, chart-only pure action/journal/completion path, compatibility setter, narrow immutable-request repair and scoped postcommit chart effects. Remaining freeze decisions: exact external fence publisher/order, same-field conflict detection and interaction token lifecycle, override batching semantics, and the explicit save barrier entry points. Without those joins, neither safe application write activation nor requirements 4.2/4.7/4.8/4.9 acceptance is established. This draft makes the remaining seams concrete; it does not close them by assertion.

## Exclusive ownership and size planning

Controller owns shared type/API decisions and the join with the session. The future widget integration worker exclusively owns `components/Widget.hooks.tsx`, `Widget.context.tsx` and cohesive new widget-chart-write modules. Session workers consume the port without patching those owners. The legacy app store, group helpers, save API and unrelated widgets remain read-only unless a separately reviewed concrete prerequisite requires changes. Any save-orchestrator adaptation is controller-owned shared work.

Whole-file physical baselines are 307 for Widget.hooks.tsx, 201 for Widget.context.tsx and 886 for components/types.d.ts; logical/function counts were not run. Do not modify the 886-line declaration file without a cohesive extraction or reviewed exception. Define the additive port in a small owned module and extend the existing provider context locally by an intersection/import, preserving existing consumers. Extract pure chart-envelope transitions and completion delivery from the 307-line hook rather than growing one oversized coordinator. New modules must own real responsibilities; do not create empty forwarding layers.

Every new/modified maintained file requires the existing inventory/checker gates: 400 physical lines/file, 300 logical units/file and 50/function. Whole modified files count. Preserve the existing checker foundation, bounded independent review and final shared-module audit. Documents/reference artifacts are excluded from production caps. Planned tests above are not executable/passing evidence; 10.4-10.6 require isolated actual checks and breadth/evidence status before acceptance.
