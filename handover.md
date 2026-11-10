# QOpenBB session handover

Paused at the owner's request on 2026-11-10 for a session restart. Resume the remaining **native-development-workflow group (11.1-12)**, preserving the worktree. Do not restart the implementation from scratch. No live provider requests were made in this session.

## Current state

- Repository: `D:/Source/QOpenBB`, branch `main`, pushed implementation HEAD `421872c15209be9f5ee56e10077d8ed6cf8acbb5` (before the handover-only commit).
- Spec: `.kiro/specs/native-development-workflow/`; **12/15 executable tasks accepted**. Task 11.1 is accepted. Tasks 11.2, 11.3 and full task 12 remain open.
- Both application images built and loaded once through native pinned Dagger. Reuse them; no rebuild is needed for the host runtime repairs below.
- Data API offline qualification passed. Workspace readiness/login passed, but actual Windows state-file permissions failed. The repair is implemented, uncommitted and awaiting completion of independent review.
- Linux CI at HEAD passed **450 tests, 11 platform skips, one live test deselected**. This does not close the entire migration or certify the uncommitted ACL repair.
- All agents stopped; no build or verification job remains active. The owned Dagger engine/cache remain available. Disposable application sessions were stopped; their state was preserved. No workstation restart was initiated.

## Accepted commits this group

| Commit | Change |
| --- | --- |
| `589e6ac` | Native command integration and reviewed Workspace source pin |
| `77b1c73` | Correct matching build source-policy pin |
| `72b10f6` | Fix PowerShell flag/value argument packing; actual wrapper regression |
| `18cc5c7` | Acceptance-only provider-send budget helper and offline tests |
| `5275c76` | Restore Linux runtime environment, storage and checked-reader wiring |
| `421872c` | Permit anonymous connected Unix stream socketpairs for checked private IPC |

The CI failure preceding `77b1c73` was a missed policy identity, not an application defect. The Linux reader failure preceding `421872c` was Node's Unix socketpair stdout being rejected as a non-FIFO. Both corrections retain fail-closed checks.

## Built artifacts: reuse these exact identities

| Service | Loaded image ID |
| --- | --- |
| Workspace | `sha256:72e207dd92dba9c12dc67854ccaea285b8a75fb9117e8d2c3c9f8495ef52da1a` |
| Data API | `sha256:b3e56de1878d02f894d80111ba4ecff14b98292b9045ea6cc88e793f41a5f807` |

Receipts, archive/manifest digests and execution logs: `D:/BuildArtifacts/QOpenBB/native-app-build/`, especially `identities.json`, `receipt.json`, `qualification.md`.

Sources: Workspace `18930d870caec08df12697e7858e05e8dbe9dd68`; data API `2e60c0a7aff039eda5f14a9d494beaec822fb9c4`. The Workspace change is only the reviewed browser fixture. All nine targets covered by 19 complexity exceptions were unchanged; exception limits/expiry were preserved.

Dagger CLI/SDK/engine remain **0.21.8**. Do not use the workstation's global 0.21.11 wrapper. Owned engine name: `qopenbb-dagger-engine-native-qualification-20261110122244`; container ID `8c14466951bf9ed3b5cbb31fbe971b0ede3e9ff9dd9bcd7ee2fe728898a96c13`. Verify its identity/state after restart before reuse.

Data verification: three network-disabled image tests passed; all **428 installed Python files** matched staged sources. Workspace Full configuration, successful login and wrong-password rejection passed. No publication/deployment claim is made.

## Immediate next task: finish the Windows state ACL repair

Actual failure: Windows Podman bind files `openbb.db` and `secrets.env` report guest mode 0777. More importantly, host ACL inspection found current-user ownership but an unprotected DACL granting SYSTEM, the current user and another principal access. The protected parent alone is insufficient because Windows permits traverse bypass. Do not weaken the assertion or seal files after secrets have already been written.

Astra's isolated offline spike passed with both exact images: a protected owner-only OI/CI root creates owner-only inherited files and nested directories. Design/evidence:

- `D:/BuildArtifacts/QOpenBB/native-state-acl/design.md`
- `spike.json`, `spike.py`, `measurements.json`, `native-tests.xml`
- `review-pending.md`: preliminary static review found no blocker, but **no final approval was issued**.

Uncommitted implementation owns:

- `pipeline/qopenbb_ci/windows_security.py`, `windows_private_files.py`
- New `windows_state_files.py`, `state_files.py`
- `compose_runtime.py`, `compose_readiness.py`, `compose_lifecycle.py`, `workspace_smoke.py`
- `tests/delivery/test_compose_runtime.py`, `test_compose_lifecycle.py`, `test_workspace_smoke.py`
- New `tests/delivery/test_windows_state_files.py`

Contracts: descriptor/session/sentinel files remain strict protected explicit-owner objects. Only the state root uses owner-only OI/CI inheritance. Generated state files get a separate exact inherited-owner ACL check using pinned handles. State roots are revalidated before startup/recreation. Generated credentials are checked before consumption. Windows `/data` uses actual host ACL authority; Linux and image-resident `/opt` files retain 0600/nonroot/nonempty checks.

Implementer evidence: **118 passed, one skipped**; all eight production files satisfy 400 physical / 300 logical / 50 per-function caps. Combined gate passed. RED was observed initially as missing `windows_state_files`; reviewer still needs the retained output or an honest transcript-only limitation, plus focused independent verification. Do not fabricate RED evidence.

Controller inventory candidate: `native-state-acl/clean-inventory.json`. Add only its two new maintained paths using a clean staged blob; do not stage unrelated working inventory changes.

After review: selectively commit/push, then run the ordinary offline Workspace smoke on **new state** using the same images and updated host code. Check actual generated/replaced file ACLs and retained-state recreation. Do not repair or migrate the old broad-ACL test directories. Finish task 11.2 only after that real acceptance passes.

## Financial acceptance: authorization and remaining preparation

Owner explicitly approved the revised aggregate budget: **80 FMP sends and 16 FRED sends**, one acceptance batch, no automatic reruns. This supersedes the earlier 40-FMP-only answer.

Scope: company searches/profiles and annual/quarterly income for AAPL/MSFT, including existing AAP prefix behavior; FRED GDP. Keys are present/nonempty in ignored `.env`, but validity is not yet checked. Never print or copy values into reports.

Preserve these existing tests in `tests/e2e/financial-workspace.spec.mts`:

1. `local packaged financial widgets support native company period recovery and saved reopen` once.
2. `real FMP company name MSFT then symbol AAPL linked research survives fresh login and retained recreation` initial, then reopen around recreation.
3. `synthetic company keyboard cancel entitlement failure and stale search cannot relabel committed data` once.

The committed `tests/delivery/financial_budget.py` wraps actual aiohttp sends, including redirects/retries, with durable cumulative counters and an exact destination/query allowlist. Set `OPENBB_FRED_MAX_RETRIES=0`. Never reset a failed run's allowance.

Exact-image transport proof passed offline with networking disabled: real redirects, persistent retry, concurrent ceiling and rejected redirect. Evidence: `native-financial/transport/{run.py,proof.py,receipt.json,stdout.json}`. Astra accepted this narrow proof in `native-financial/budget-helper-review.md`. Initial fixture port-443 binding failed under the image's nonroot user; the corrected fixture maps approved HTTPS hosts to local port 8443. Failure logs are retained. No provider traffic occurred.

Still required before live execution:

- Review and exercise guard installation in the sole packaged API process.
- Prove stopped-container counter extraction and cumulative handoff across recreation. Validate exact API identity, stop without removal, confirm exit, extract ledger, persist with protected host storage, then update checked private bootstrap/config hashes and recreate. Never snapshot a live counter or grant a fresh budget.
- Distinguish instrumented financial acceptance from the ordinary noninstrumented image qualification.

External **unreviewed, unexecuted drafts**:

- `D:/BuildArtifacts/QOpenBB/native-financial/controller.py`
- `D:/BuildArtifacts/QOpenBB/native-financial/prepare_snapshot.py`

Do not run the controller before independent review. Snapshot preparation failed copying the historical `verification/provider/.venv/lib64` link. **`native-financial/snapshot` is partial and unusable.** Build a fresh `snapshot-v2`, copying only required verification source files, tests and the reviewed fork fixtures. Reuse existing native dependencies; do not copy Linux virtual environments or install another toolchain.

Use explicit `QOPENBB_VERIFICATION_ROOT`, `WORKSPACE_EVIDENCE_ROOT`, checked reader/Python and retained checkpoint paths. One browser worker, zero retries, fresh contexts and the existing five-per-minute login budget remain mandatory.

## Linux and closing the group

Successful nonpublishing workflow: https://github.com/norandom/QOpenBB/actions/runs/42817139649 at `421872c`. It exercised actual Linux symlink-venv selection and Node/Python IPC, alongside the expanded portable checks. Re-run the final reviewed scope after the ACL repair; do not treat this earlier result as verification of later changes.

Full task 12 remains open until integrated acceptance, final relevant Linux checks, documentation and evidence closeout. Update README/docs checkboxes, `.kiro/breadth.toml` and spec progress only from actual results. Sync one concise reviewed evidence record per completed delivery, then selective commits/push. No release/image publication is authorized solely by this migration.

## Preserve unrelated work and workstation rules

Preexisting unrelated changes must remain untouched:

- `pipeline/qopenbb_ci/catalog_cli.py`
- Untracked `pipeline/qopenbb_ci/catalog_renderers.py`, `tests/contracts/test_renderers.py`
- Preexisting semantic changes in `.kiro/complexity-budgets.json` and `.kiro/complexity/workspace.json`

Do not use `git add .`, reset, or overwrite those files wholesale. The inventory also contains the current uncommitted ACL path additions, which need selective staging.

Use native Windows Podman/Compose and Dagger; no WSL. Read AGENTS and steering delegation/testing/complexity. Use fresh Sol implementers and Astra difficult/security reviewers, at most two implementers plus one reviewer and controller. Serialize heavy builds/suites. Agents from this session are stopped; recreate them as needed from this handover.

Tools: `D:/BuildArtifacts/QOpenBB/native-foundation/resolved-tools.json`. Python: `native-foundation/pipeline-venv/Scripts/python.exe`; use `-B` and explicit repository `pipeline` in `PYTHONPATH`. Put all disposable outputs under `D:/BuildArtifacts` and run commands from a repository. Native dependency snapshot: `native-foundation/snapshot/verification/node_modules`; Chromium cache: `D:/BuildArtifacts/playwright`. Historical root `verification/node_modules` and `vendor/workspace` are unsuitable for these native runs; preserve them. Reviewed LF fork: `native-join/workspace`.

Memory checkpoint identity: project `QOpenBB`, harness `codex`, task `QOpenBB-1793950576439`. This file and current git status take precedence over an older checkpoint.
