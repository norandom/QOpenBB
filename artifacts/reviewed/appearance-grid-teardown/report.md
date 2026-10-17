# Grid fixture teardown repair

The test fixture now executes its pending AG Grid callbacks before jsdom is released. The focused fixture passed 11 tests, and the current chart-application suite passed 134 tests with exit code 0. Independent review and parent-owned acceptance remain required.

## Debug report

- ROOT_CAUSE: AG Grid 34.1.1 enables row animation by default. Filtering and sorting schedule a 400 ms callback in `RowRenderer.destroyRowCtrls`; `api.destroy()` does not cancel it. That callback dispatches `displayedRowsChanged`, and `LocalEventService.dispatchAsync` schedules another callback through `window.setTimeout`. The original fixture released jsdom before this chain finished, allowing `window is not defined` after otherwise successful assertions.
- CATEGORY: LOGIC_ERROR in the test fixture lifecycle.
- FIX_PLAN: Own timers from grid construction; destroy the grid, await `vi.runAllTimersAsync()`, assert `vi.getTimerCount() === 0`, then release the host, restore timers, and restore stubbed globals in `finally`.
- NEXT_ACTION: RETRY_TASK through fresh independent review and parent-owned full verification.
- CONFIDENCE: HIGH.
- NOTES: Only the fixture changed. Default animations, financial assertions, grid options, dependencies, and production behavior are preserved. Tests are outside production complexity caps. No callback is discarded and no exception is suppressed.

## Evidence

The [original independent-review failure](original-review-application.log) records 96 assertions passing with process exit 1 and the `LocalEventService`/`RowRenderer` stack. A fresh original focused run passed; this is consistent with the recorded intermittent failure and is not counted as reproduction of the exception.

The [callback probe](callback-lifecycle-probe.log) deterministically exposes the pending-work condition. It records 400 ms `RowRenderer.destroyRowCtrls` callbacks followed by 0 ms `LocalEventService` flushes from `dispatchDisplayedRowsChanged`, all after grid destruction and with `windowAlive: true`. All 11 teardowns drain to zero pending timers. The final empty-data test also owns three pending callbacks after its explicit destroy; the observed animation chain originates in filtering/sorting tests, so the defect is not limited to the final test.

The probe adds callback observations only in the isolated workspace. Its generated [probe fixture](probe.test.ts) is diagnostic evidence; the maintained fixture contains only timer ownership, awaited cleanup, the empty-queue assertion, and explanatory comments.

- [Focused run](fixed-focused.log): 11 passed; exit 0.
- [Chart-application run](fixed-application.log): 134 passed across 6 files; exit 0. This includes the current appearance tests copied with the frozen chart closure; it is broader than the historical 96-assertion review run.
- [Lifecycle summary](lifecycle-summary.json) checks callback origins, live-window observations, all teardown queue counts, exit codes, and final test hash.
- [Locked dependency excerpts](locked-ag-grid-excerpts.txt) show the default animation option, 400 ms constant, uncancelled callback, and event queue implementation.

Reproduce in WSL Debian as user `mc`:

```sh
/mnt/d/Source/QOpenBB/pipeline/.venv/bin/python /mnt/d/Source/QOpenBB/artifacts/appearance-grid-teardown/run-focused.py
/mnt/d/Source/QOpenBB/pipeline/.venv/bin/python /mnt/d/Source/QOpenBB/artifacts/appearance-grid-teardown/summarize.py
```

The runner uses pinned Node 24.22.0, Vitest 4.1.11, the pinned dependency cache, and an isolated baseline plus current chart source/test closure. Exact commands, working directories, exit codes, durations, and test hashes are recorded in the matching JSON files. It does not install dependencies or mutate production files. The diagnostic `--probe-only` option skips the baseline and fixed suites when only callback observations need refreshing.

## Verification result

- STATUS: VERIFIED for the focused lifecycle repair and recorded chart-application test command.
- CLAIM_TYPE: FIX and TEST_OR_BUILD.
- CLAIM: The fixture executes the observed pending animation/event chain while jsdom remains available and asserts an empty timer queue before teardown finishes.
- GAPS: Fresh independent Astra review and parent-owned final acceptance are pending. These results do not certify the full application, browser behavior, or product release.
- NOTES: The heavy verification slot was released after the focused and callback checks. No commits were created. [Safe allowlist](allowlist.json) freezes the maintained test and synthetic evidence; dependency caches and the isolated source tree are excluded.

Reference semantics: [Vitest timer API](https://v3.vitest.dev/api/vi) documents that `runAllTimersAsync` executes initiated and newly scheduled timers, while `getTimerCount` reports pending timers. The locked dependency, rather than current online AG Grid versions, is authoritative for the lifecycle finding.
