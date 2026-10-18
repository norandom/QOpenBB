# Dashboard save failure repair review

The standalone baseline save repair is approved for integration. A rejected dashboard save now preserves ordinary-session edits and the cloud snapshot, reports failure, and permits retry without an unhandled rejection or false success notification. This record does not complete task 2.77 or certify the actual Full browser journey.

Reviewed on 2026-10-18 against Workspace HEAD `49e9cb25a1ef1b7c9c35a1dad030281a97c2ecb8` plus these two working-tree files. Paths are relative to `vendor/workspace/`.

| File | SHA-256 |
| --- | --- |
| `terminalpro/src/api/dashboard.api.ts` | `69c45e23424d7408055379870644551686bfdfcffad59959e633f06f03d43cc7` |
| `terminalpro/tests/unit/api/dashboard.api.test.ts` | `40173950c4f367f859a9a58da89e637716397c573b64ef6a16dc0ad67df9d3ba` |

The production change awaits the existing POST before advancing the cloud snapshot. Its catch path reports an error and returns before the success notification. The existing explicit `logout:true` failure policy remains; the reviewer identified the explicit menu logout action as its observed caller. Ordinary save defaults to `logout:false`, and the regression asserts that a failed ordinary save does not log out. Explicit logout failure has no new runtime coverage.

## Verification

Run the commands below from the repository root in Debian WSL. No dependencies were installed. The Vitest run uses one worker.

```sh
cd vendor/workspace/terminalpro
/mnt/d/Source/QOpenBB/artifacts/task-1.2/node-v24.22.0-linux-x64/bin/node node_modules/vitest/vitest.mjs run tests/unit/api/dashboard.api.test.ts --maxWorkers=1 --environment=jsdom
/mnt/d/Source/QOpenBB/artifacts/task-1.2/node-v24.22.0-linux-x64/bin/node node_modules/@biomejs/biome/bin/biome lint src/api/dashboard.api.ts tests/unit/api/dashboard.api.test.ts
cd ../../..
printf '["vendor/workspace/terminalpro/src/api/dashboard.api.ts"]' | artifacts/task-1.2/node-v24.22.0-linux-x64/bin/node tools/quality/syntax_units.ts
git -C vendor/workspace diff --check
```

| Check | Observed result |
| --- | --- |
| RED before repair | Focused failure/retry and deferred-persistence regressions both failed; Vitest reported the unhandled HTTP 500 rejection. Exit 1. |
| Full dashboard API unit file | 12/12 passed, exit 0; no unhandled errors. |
| Biome lint, both assigned files | Passed, exit 0; no fixes applied. |
| Whole production file complexity | 209 physical lines, 110 logical syntax units, maximum function 27; within 400/300/50 caps. Parser exit 0. |
| Whitespace check | Passed, exit 0. |

The focused tests cover rejected save, unchanged local work and cloud snapshot, no success notification, successful retry, and waiting for persistence before recording success. Raw RED and GREEN logs remain local under `artifacts/task-2.77-save-repair/`; they are not part of the publication set.

## Independent decision and remaining gate

Fresh-context reviewer `/root/save_failure_repair/review`, model `gpt-6.1-sol`, returned `VERDICT: APPROVED` after reading the actual two-file diff and independently rerunning the 12 tests, lint and complexity checks. The reviewer verified RED evidence, found no new placeholder or secret markers, and found no boundary spillover or new flags. No remediation was required.

The controller owns the actual Full browser join and its console/network evidence. A failed save that loses edits, reports success, produces an unhandled rejection, or prevents retry would disprove this bounded repair claim and require reopening the owning save contract. Neither a unit pass nor this review substitutes for the remaining task 2.77 acceptance gate.
