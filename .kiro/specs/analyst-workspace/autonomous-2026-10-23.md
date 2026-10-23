# Work plan to 17:00 Berlin, 23 October 2026

Primary outcome: complete and independently verify Waterfall in the existing Table/File chart journey, then publish it if the application gates pass. Preserve the accepted Range alpha throughout. Start time: approximately 10:35 CEST; stop time: 17:00 CEST (15:00 UTC).

This is a time budget, not permission to mark unfinished work accepted. The [Waterfall milestone](waterfall-milestone.md) owns behavior, financial meaning and completion criteria. No broader UI redesign, provider expansion, AI, Excel or unrelated refactoring belongs to this window.

| Berlin time | Work and concrete output |
| --- | --- |
| 10:35-11:00 | Finish original-runtime observations and independent contract review. Freeze numerical, appearance and renderer interfaces; record original quirks without silently changing them. |
| 11:00-12:30 | Implement cumulative movements and Waterfall appearance/control adapters in disjoint lanes. Preserve existing capture, saved selection, theme paths and controls. Run affected regressions and complexity checks; review and commit completed tasks. |
| 12:30-14:00 | Join actual renderer, session, first-value-field admission, navigation, tooltip and editor behavior. Include hidden-navigator/default-zoom coverage learned from Range. Pass the focused integration checks and independent review; build an identified candidate. |
| 14:00-15:15 | Verify the real-FMP income-statement bridge, original/replacement appearance, positive/negative styling, direction, navigation, refresh, save/fresh reopen and PNG export in the packaged application. Repair concrete failures; publish selected samples only after verification. |
| 15:15-16:15 | If accepted, run one milestone image-publication pipeline and verify the tagged release and public pulls. If the application gate is not satisfied, finish the smallest useful reviewed task and retain the previous release. |
| 16:15-17:00 | Stop starting feature changes. Finish bounded verification/review, reconcile README/docs checkboxes and breadth, sync selected artifacts, commit/push completed scopes, and write a precise handoff. Stop local agent work by 17:00; identify any still-running hosted CI job without claiming success. |

## Execution rules

- Controller owns interfaces, shared edits, commits, release gates and the clock. Use at most two Sol implementation lanes plus one Astra reviewer, with fresh task contexts and exclusive file ownership. Reassign slots as dependencies finish.
- Reuse existing browser/financial fixtures and test runners. One heavy build/suite at a time; one isolated browser worker. Keep the 400 physical / 300 logical / 50 per-function caps, per-task reviews and commits.
- Ask only about material visual deviations or decisions that change existing behavior. Ordinary implementation choices and fixes proceed autonomously within the approved milestone.
- Start no new milestone merely to fill time. If Waterfall is published early, prepare the next Heatmap contract and financial fixture read-only; do not open a second unfinished implementation lane near the cutoff.
- Recheck actual time after each task and before a build or release dispatch. Do not begin a long hosted publication after 15:30 unless its continuation beyond 17:00 is explicitly agreed; do not cancel a healthy already-running release just to fit the report.

## Runtime prerequisite and fallback

The owner-started original runtime is available on port 55251 and the accepted Range candidate on 55557. Earlier automatic approval review rejected tool-driven runtime startup. Do not bypass that rejection. A new packaged candidate may therefore need the owner to run the updated, ignored `run_this.sh` once and return its JSON.

Prepare the build, script and exact verification commands before requesting that step. While waiting, continue independent source checks, financial assertions, review and documentation. If startup or an essential visual decision is unavailable by the application window, retain an honest source-reviewed/built checkpoint; do not substitute unit tests for packaged acceptance or publish an unaccepted feature.

## Required handoff at 17:00

Record completed tasks, source/root commits, image/release identities, actual passing and failing checks, any pending owner action and the single next task. Preserve unrelated working changes. The current public alpha remains usable even if Waterfall is not ready. No automatic PC or WSL shutdown is requested.

## Evening verification extension

At 18:42 Berlin, after supplying the running candidate, the owner explicitly chose "Continue verification tonight." This extends the verification window beyond the original cutoff. Continue the packaged Waterfall journey and repairs required to satisfy it; retain independent review, per-task commits and the accepted-milestone publication gate. The afternoon checkpoint is recorded in artifacts/chart-waterfall/handoff.md. The candidate startup blocker is resolved.

## Final closure after the evening extension

Waterfall is delivered as [alpha-40002594897-1](https://github.com/norandom/QOpenBB/releases/tag/alpha-40002594897-1). The owner extended verification at 18:42 Berlin, accepted the appearance and requested that the current task be finished before stopping today. No next-family work was begun.

The maintained real-FMP journey passes 1/41.4 seconds on application 789d93f87e99d6bdd51a37d9e387cdd934e4e38a and local image 46ec7b9edc92ed20deb59d6f4f011bb10c94b934aa9c8faae4c6d5ce5739769b; test-only ba03b1289f60a06269fb1a97900e61474475464f preserves the accepted application code. Publication run [40002594897](https://github.com/norandom/QOpenBB/actions/runs/40002594897) succeeded from root 15b2e782f71011a79b4ed1351386aa01133fb14c, pinning Workspace ba03 and data API cab81b16bb9ef49272a6f3b0bf04cf9f34bde0ba. Both release image identities, downloaded installation assets and six anonymous digest/tag/latest pulls are verified. See [final verification](../../../artifacts/reviewed/chart-waterfall/verification.md#published-waterfall-alpha), [manifest](../../../artifacts/reviewed/chart-waterfall/release-manifest.json) and [pull evidence](../../../artifacts/reviewed/chart-waterfall/anonymous-pulls.json).

There is no remaining blocker in the bounded Waterfall milestone. CI image-byte browser execution, assembled Compose and owner-server acceptance remain outside this delivery; broader unchecked chart/caller work stays in the [ECharts status](../../../docs/echarts-status.md) and [roadmap](../../../docs/roadmap.md). These are future scope, not work started today. The parent records the final root closure commit after committing these records. No additional chart task is scheduled in this run.
