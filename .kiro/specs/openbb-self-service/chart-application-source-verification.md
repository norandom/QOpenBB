# Chart application helper verification

Tasks 2.34-2.37 are independently accepted with scoped GO and VERIFIED completion for source-safe contracts, session/range adapters and financial display callbacks. The helpers are not connected to the application yet.

## Accepted boundary

| Task | Behavior | Evidence |
| --- | --- | --- |
| 2.34 | Frozen typed contracts and isolated strict/test configuration | `artifacts/reviewed/task-2.34/review/verdict.md` |
| 2.35 | Source range precedence, immutable provenance, stale-session rejection and latest-state reducer composition | `artifacts/reviewed/task-2.35/review/verdict.md` |
| 2.36 | Six display callbacks preserving original numeric, date, fiscal and precision behavior | `artifacts/reviewed/task-2.36/review/verdict.md` |

Range persistence uses resolved visible columns while keeping original range data as provenance. Stale edits are rejected before reading storage. The financial policy leaves observations at their original scale and applies formatting only to display values. Exact original helper excerpts and explicit expected strings provide the financial reference.

## Verification limits

The formatting worker wrote tests first, but its first execution failed during shell setup. A subsequent missing-module replay supplies RED evidence; it is not an uninterrupted preimplementation RED run. Historical failures and the corrected nonfinite expectation remain in the published handoff.

No new build, browser capture, live-provider request or release image is claimed. Original controls, themes and flags are untouched. Grid capture, effective appearance, editor integration, renderer invocation, export and application save/restart/reopen remain unverified. Full product and deployment acceptance remain open.

## Joined evidence

On 2026-10-17, Workspace `945e438a9a65c3eeef7073dbce64a03b02f0ff6f` passed the joined check: 36 application tests across three files, 260 compatibility tests across nine files, both strict TypeScript configurations and scoped Biome across eleven files. No tests were skipped. The stage matches 62 source/configuration files byte for byte. The full maintained audit measures 172 files with no errors or violations; existing reviewed exceptions remain bound to unchanged bytes.

| Module | Physical lines | Logical units | Largest function |
| --- | --- | --- | --- |
| types.ts | 181 | 111 | No functions |
| chartRange.ts | 47 | 19 | 13 |
| sessionState.ts | 166 | 96 | 16 |
| financialFormatting.ts | 52 | 25 | 5 |

The boundary audit shows eleven additions since the pre-slice Workspace revision, all under application helpers or their test directory. Existing reducer, mapper, snapshot, host, controls and feature flags are unchanged. Unrelated dirty catalog/renderer work remains outside acceptance.

Reproduce with `wsl -d Debian -u mc -- bash /mnt/d/Source/QOpenBB/artifacts/task-2.37/check.sh` in the recorded pinned environment. Identity verification uses the existing `pipeline/.venv/bin/python`; bare `python3` was unavailable in Debian, so the first identity invocation failed before execution and was rerun with that explicit interpreter. Commands in the public mirror retain their original local paths. Test and source evidence is under `artifacts/reviewed/task-2.37/`; the final independent verdict owns joined acceptance.

Independent Astra review reproduced all joined checks, identity and full maintained quality with exit 0. [Final verdict](../../../artifacts/reviewed/task-2.37/review/verdict.md) accepts this helper boundary only.
