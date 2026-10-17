# Preserve widget edits through React replay

Repair the existing production widget owner before chart controls consume it. The owner requested production UI work and said "go" after redirecting effort away from reference infrastructure. This bounded repair preserves the current API and persistence policy; full chart activation remains outside its scope.

## Existing defect and repair

`terminalpro/src/components/Widget.hooks.tsx` overwrites the captured functional update with its first result inside a React state updater. Replaying the updater against newer state can therefore discard intervening fields. It also schedules store/context effects inside that replayable calculation. Group notifications and refresh events have the same effect-placement problem.

Replace this hook's state owner with one reducer-backed owner. Keep the original update function unchanged, evaluate it against the supplied current widget each time, and collect internal effect records alongside the resulting state. The reducer performs no external effects and mutates no captured inputs. Allocate operation IDs, refresh timestamps and immutable predicate inputs before dispatch. Keep object updates as replacements, not patch merges.

Deliver effect records after commit, in operation order, at most once across StrictMode effect replay. Acknowledge and prune delivered records. Use a layout commit step to expose the latest committed widget/dirty state before save listeners or cleanup can observe it. Save and cleanup must not read an abandoned render or a stale passive-effect snapshot. Preserve the existing persistence predicate, force-save behavior, context override, shared subscriptions and explicit save behavior.

React can commit an urgent operation before an earlier deferred operation. Acknowledge exact delivered records rather than a maximum submission ID. When replay combines the deferred edit with already delivered urgent work, persistence must retain the final committed widget, including both edits. Ordinary batched updates retain their ordered callback behavior. Verify this with the actual hook's transition/urgent regression.

Use one owner, not a second widget store or chart scheduler. Pure group transformations may return notification data for post-commit delivery. Internal replacement updates, group updates and refresh updates go through the same owner. Caller functional updates remain subject to React's purity requirement; this repair does not attempt to make arbitrary impure caller code safe.

No public completion, cancellation or transaction API is introduced. Define chart completion/rebase semantics when implementing its real consumer. This task does not finish the entire UI-01 work package.

## Ownership and limits

Paths are relative to `vendor/workspace/terminalpro`:

- `src/components/Widget.hooks.tsx`: compose the existing hook and retain its exports and return tuple.
- `src/components/widgetSync/updates.ts`: pure operations, state reduction and existing persistence predicate, re-exported from the original hook.
- `src/components/widgetSync/useWidgetUpdates.ts`: committed owner/effect delivery and latest-state save behavior.
- `src/components/widgetSync/useWidgetSubscriptions.ts`: extract existing subscriptions and event handling where needed for cohesive size limits.
- `tests/unit/components/Widget.hooks.test.tsx` and focused widget-sync tests/configuration as needed for actual hook verification.

Do not change `Widget.context.tsx`, the large shared type declaration, storage schema, chart controls, feature flags or release eligibility. All modified maintained files must pass the existing 400 physical lines/file, 300 logical units/file and 50/function checker. Controller registers new paths and preserves unrelated inventory edits. Test files/configuration are explicit test-only exclusions.

## Acceptance

Start with the real defect: evaluate the same submitted functional update against A and B, where B contains an intervening field. Both evaluations must retain the corresponding current fields, and calculation alone must deliver no external effect.

Focused checks must also cover two batched functional edits, committed effect ordering and single delivery under StrictMode, unchanged force-save compatibility, context override, group/refresh notifications, latest-state explicit save and cleanup. Verify that no public API or persistence predicate changed. Test actual production hook composition as well as pure reduction; disconnected helper tests cannot accept this task.

Use the existing pinned WSL dependencies and Vitest infrastructure, without installation or new browser infrastructure. Run the relevant hook tests, type checking, scoped non-mutating lint and the complexity gate with current fork manifests. Record command exits and a concise independent source review. A failure requires a targeted correction, not a separate research project.

No screenshot is needed for this internal behavior repair. The next visible deliverable remains the original docked chart controls and their application integration from the [UI worklist](ui-parity-worklist.md). Ask the owner about uncertain visual similarity using matched screenshots.
