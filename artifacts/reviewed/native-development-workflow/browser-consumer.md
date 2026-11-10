# Checked runtime data for browser consumers

Task 8 passed independent Astra review on 2026-11-10. Root financial tests and the owned Workspace login fixture now obtain their runtime object through the shared TypeScript bridge and the checked Python private reader. Missing configuration, malformed or non-ready responses and child failures are rejected without an unchecked file-read fallback or raw child-error output.

The checkpoint remains confined to the external evidence directory. Exclusive initial creation, session/image equality and changed-container assertions are preserved, as are the financial UI assertions. Eleven actual Windows IPC/consumer tests passed independently; strict TypeScript compilation passed. Application/provider journeys and Linux execution remain later acceptance work.

The test-only fork change is commit `18930d870caec08df12697e7858e05e8dbe9dd68` on `qopenbb/native-browser-reader` in `norandom/openbb-workspace`, based on `f832a5593223b1e702970c4de8eceda87a17fa5b`. Only `terminalpro/tests/e2e/live-chart/fixtures.ts` changed (+6/-2). The source lock is not promoted here; task 11.1 joins that identity with the other consumers.

The new reader measures 68 physical lines, 48 logical units and 10 maximum callable units. The controller combined gate passed for 93 files against the currently accepted fork pins. Separately, the actual nonempty candidate-fork manifest was validated: its sole changed file is an explicitly excluded test fixture. A full candidate-pin gate remains the integration step because existing exact-revision exception records still belong to the accepted fork revision; none were silently retargeted.

Raw commands, frozen hashes and review remain under `D:/BuildArtifacts/QOpenBB/browser-consumer`, including `frozen-scope.json`, `workspace-changes.json`, `fork-scope.json`, `combined-root.json` and `review/review.md`. Initial missing-bridge RED failures were reported from the implementer's transcript rather than retained as raw logs. No provider request, application browser run or image publication occurred.
