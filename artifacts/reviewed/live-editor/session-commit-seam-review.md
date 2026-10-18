# Keep chart runtime and saved edits in the same replayed transaction

- DECISION: APPROVED for the bounded adapter design below only.
- TASK: 2.74; independent architecture review, 2026-10-18.
- SOURCE: Workspace `e8874aae0c8030bc20db57f62daaaddf952a0260`; parent `5300bebd9dbb6ee6cea28dc6b1e5f0859491e4af`.
- IMPLEMENTATION ACCEPTANCE: Not reviewed or granted. No production files changed by this review.

Carry the session's immutable transient value beside `widget` in the existing Widget owner's reducer. A session transaction computes both values from that reducer's latest input. Publish the committed pair through a dedicated context. This closes the demonstrated acceptance gap without another store, persistence envelope, event bus or chart-specific dependency in the Widget owner.

## Finding and rejected alternative

`src/components/widgetSync/updates.ts::reduceWidget` already calculates Widget updates purely and collects effects. `useWidgetUpdates.ts` delivers those effects after commit, deduplicating operation IDs with `wasDelivered`. Its existing deferred-delivery branch uses `state.widget` to preserve urgent fields. `tests/unit/widget-sync/owner.test.tsx` explicitly exercises urgent/deferred rebasing and override delivery.

A receipt attached to those once-delivered effects cannot own transient chart acceptance. An earlier deferred operation D can change eligibility; urgent chart operation A first commits accepted against the old Widget, then replays rejected after D. The receipt for A has already been delivered. A later restoration can make final storage indistinguishable from an accepted operation. Current-stamp validation does not detect every namespace or eligibility change. Dispatching A synchronously does not prevent React from replaying it after earlier deferred work.

A serialized session queue also fails: command B can already have captured transient axes produced by A before A rebases. Emitting a corrected receipt for A would not repair B's captured input. Ref mutation inside the reducer, speculative journals, Widget-identity caches, and receipt deduplication variants do not supply the missing atomic input.

## Frozen responsibilities

1. The existing owner holds at most one active opaque scoped transient value. It is reducer metadata, never a property of `WidgetT`, saved storage, an effect Widget snapshot, or an override payload. The session defines its concrete runtime type and all chart semantics.
2. A pure scoped transaction receives the latest Widget and the preceding value for its matching scope, and returns the next Widget and next value together. Both are replayed from the same preceding reducer state. Later commands receive that preceding value through the reducer, never through a captured ref or earlier receipt. Rejection preserves both values; no runtime advancement occurs.
3. A dedicated transaction context exposes the committed scoped value and transaction dispatch from the same `useWidgetSync` instance. Its fourth tuple item may carry this adapter; preserve the original first three items and ordinary `updateWidget` API. Consumers select their scope before using its value. No callback copies the authoritative runtime into another state owner.
4. Ordinary Widget updates, internal replacements, saves and effect acknowledgements retain the scoped metadata unless an explicit lifecycle action changes it. Existing dirty, force-persist, override, notification and once-per-operation persistence behavior remains intact. A scoped-only lifecycle update must not dirty or persist the Widget, trigger an override, or emit unrelated notifications.
5. The session continues latest-state baseline, eligibility, axis and intent rehydration inside its pure transaction. Persist only original reducer output and preserve unknown/inactive branches. Original numeric-rotation and structural-axis reopen limitations remain unchanged.

## Scope lifetime and disposal

Use an opaque scope identity for one address/grid/family/session generation. Only explicit registration installs its initial transient value through the same reducer; commands require an exact active-scope match and cannot implicitly initialize a missing or retired scope. Keep the existing data/render stamp checks as additional guards. A new lifecycle generation installs a new identity; old closures retain their old identity and are rejected. Capture the identity in each submitted action; do not read a mutable current-token ref inside the reducer.

Dispose with a scope-qualified lifecycle action: clear only if the active identity matches. Late cleanup from an old session cannot erase a newer session. Cleanup and initialization must themselves be replay-safe, including StrictMode setup/cleanup/setup: mint a fresh token for each setup and never explicitly re-register a released identity. React replay of the original registration action remains a pure history calculation. Do not let an old queued command recreate a disposed scope. Host disposal and existing generation advancement remain session responsibilities. Transient values contain data only, with no host/subscription resources requiring Widget-owner cleanup. Reset and rendering logic must not present a value from a mismatched scope alongside a newly selected Widget.

Carry data-identity guards in the atomic scoped metadata, using a new token or explicit guarded refresh when that identity changes; an external stamp ref alone is insufficient. Preserve intended axis/manual-angle retention across ordinary data refresh. One active slot is sufficient for the present single-chart owner. A multi-slot Map is not required by this repair; if adopted, its additional concurrent-consumer requirement and bounded cleanup need explicit review.

## Bounded writable ownership

Paths below are relative to `vendor/workspace/terminalpro/`.

| Path | Allowed change |
| --- | --- |
| `src/components/widgetSync/updates.ts` | Integrate scoped transient state/actions with the existing pure reducer; preserve persistence calculation. |
| `src/components/widgetSync/useWidgetUpdates.ts` | Expose dispatch and committed scoped state from that reducer; preserve effect delivery and save semantics. |
| New `src/components/widgetSync/transactions.ts` | Cohesive generic scope/value/action types and pure helpers if needed for size or clarity. |
| New `src/components/WidgetTransaction.context.tsx` | Dedicated typed adapter context; no second state/store. |
| `src/components/Widget.hooks.tsx` | Return the adapter as a fourth tuple member from the same owner. |
| `src/components/Widget.context.tsx` | Supply the dedicated provider beside the existing Widget context. |
| `src/components/General/Table/Chart/application/` session modules | Own runtime data, pure transaction semantics and lifecycle scope. |
| `tests/unit/widget-sync/` and existing chart-session test suite | Focused regressions and boundary verification. |

Do not modify oversized `components/types.d.ts`, global event unions/utilities, accepted renderer/editor/Setup modules, or persistence schemas for this repair. The controller owns canonical contract/task-boundary and inventory edits. Every touched maintained production file must pass 400 physical lines, 300 logical units and 50 units per function; extract cohesively if needed. Tests and this review document are exempt.

## Required implementation evidence

- RED then GREEN: latest-state rejection after valid predispatch input preserves runtime and Widget, including invalidation followed by restoration before commit.
- Two immediate commands consume preceding accepted runtime and saved fields; the second remains valid when only render revision advanced.
- Real React urgent/deferred rebase changes A from accepted to rejected and from rejected to accepted. A subsequent B uses the rebased runtime chain. Assert final rendered/selected runtime and Widget together, not callback counts alone.
- Reducer replay/StrictMode performs no external mutation, duplicates no persistence or override effects, and neither leaks transient metadata into saved/override snapshots nor normalizes defaults into storage.
- Address/grid/generation replacement, disposal, late stale dispatch, old cleanup after new initialization, and StrictMode lifecycle replay preserve scope isolation. No closed scope is resurrected by an ordinary transaction.
- Existing owner tests retain force persistence, ordinary replacement, explicit save, unmount save, shared notifications, overrides and urgent/deferred delivery behavior. Session failure/recovery tests retain edits and the original saved-leaf contracts.
- Run affected strict type/static checks and the existing scoped complexity checker with explicit fork scope. Record commands, revision and exits. Production implementation review remains independent; this design decision is not runtime evidence.

Disproof condition: any committed chart uses transient axes/manual rotation from an operation rejected in the current replayed Widget history, or any transient value reaches a persistence/override payload. Either blocks task 2.74 acceptance.

## Review mechanics

Read actual owner code, existing urgent/deferred tests, task 2.74, integration design, field/transaction manifest, and delegation/complexity/testing/documentation steering. Inspected parent diff and source revisions. Core product/tech/structure files were absent. No production edit, build or runtime test was performed by this architecture review. Planned regression obligations above are not passing test claims.
