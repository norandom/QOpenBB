# Native application image acceptance review

- VERDICT: APPROVED
- TASK: native-development-workflow 11.2, native application image qualification.
- SCOPE: Existing packaged checks for the exact built Workspace/data API images, plus the independently reviewed Windows state ACL repair and real retained-state recreation. Tasks 11.3 and 12 remain pending.
- REMEDIATION: No blocking remediation. Controller owns sanitized evidence synchronization, breadth/spec updates and selective delivery.

## Image and build identity

The build receipt records successful native Workspace and data API builds through the qualified PowerShell entry point, with explicit stage/archive paths, SDK interpreter and owned engine. Build root revision was 72b10f6238a9530ad38ae4c24320f5258ae7aa4e. The application sources remain Workspace 18930d870caec08df12697e7858e05e8dbe9dd68 and data API 2e60c0a7aff039eda5f14a9d494beaec822fb9c4, consistent with the current source lock and export provenance. Later host ACL code does not change these image bytes.

Qualified CLI and SDK are 0.21.8. The engine receipt agrees before, between and after the builds: container 8c14466951bf9ed3b5cbb31fbe971b0ede3e9ff9dd9bcd7ee2fe728898a96c13, engine image ID 9f1537a7b5dff83c5404f199cbf73d3023bf5af0a2f3ffada4b68e26194a714f, repository digest registry.dagger.io/engine@sha256:c9c1a0a6546380983d42e8d75adde070a2a0935c54b498d8bc9045d9cb2ee336. This matches the pinned 0.21.8 engine reference.

| Service | Loaded image/config ID | Archive SHA-256 | Manifest digest |
| --- | --- | --- | --- |
| Workspace | sha256:72e207dd92dba9c12dc67854ccaea285b8a75fb9117e8d2c3c9f8495ef52da1a | e49d9495c765786a74b7dfd4eacf6799a17d6add8816a251e0e8db7c9434d82c | sha256:d4e8b79bd6df291b9cb3a64b594e3fb143f001b1e9591278f54b4769b4daabde |
| Data API | sha256:b3e56de1878d02f894d80111ba4ecff14b98292b9045ea6cc88e793f41a5f807 | b235a53cb609e889ac3dfbc92b0d994390659ccd48bbfeb1272ce4d5cc634472 | sha256:78afffd66eb89107cbe41c5eada0eac0a8caefde6f8379774b3aff151f53fb5f |

This reviewer mechanically compared receipt, identities and export reports: image/archive identities agree, exit 0. Prior archive inspection/load evidence is reused; archives were not rehashed and builds were not rerun during this audit. Neither image has registry publication evidence, and no publication claim is made.

The existing offline data runtime suite reports 3 passed, exit 0. Installed-module comparison requires exact path/hash dictionaries, not just counts; all 428 Python files match staged source (core 308, equity 22, economy 7, FRED 60, FMP 23, runtime 8). The comparison script and retained output were inspected.

## Packaged runtime and private state

The ordinary packaged-resume/smoke.json reports verified=true for these same images: health 200, Full configuration, valid login 200, wrong password 401, checked bind, sanitized logs, owned container cleanup and state retention. Both generated /data files have nonzero size, UID 1000 and checked Windows owner-only ACL authority. Their translated guest 0777 modes remain recorded. Both image-resident /opt private files retain 0600, UID 1000 and nonzero size.

The former BLOCKED receipt/qualification document remains historical failure evidence. Its blocker is superseded by the reviewed distinct state-root policy, the independent native regression run (91 passed, 3 POSIX-only skips), and this actual new-state smoke. It was not bypassed by accepting broad ACLs or repairing old state after secrets were written. All twelve hashes from resumed-review/reviewed-files.json were independently rechecked and still match.

The one-run recreation proof uses checked startup/recreate/stop APIs. Its before/after assertions compare origin, complete state/bind identity, credentials, committed SQLite rows, replacement content and secrets hash; both service container IDs must change. Readiness on each startup validates the generated files and logs into the retained account. Result verified=true and command exit 0 establish those assertions passed. Cleanup reports stopped, zero containers and zero networks, with state retained.

The separate synthetic SQLite transaction proves inherited ACLs on a live WAL/SHM pair, committed-row retention, rollback of an uncommitted row and a file renamed inside the bind directory. It is correctly distinguished from the real application's auxiliary files: application-auxiliary-acl.json separately records checked owner-only inherited ACLs for openbb.db-wal (234872 bytes) and openbb.db-shm (32768 bytes). The metadata inspection command was read; it does not alter the application database. Post-recreation checks cover openbb.db, secrets.env, the synthetic database and replacement file.

## Findings and limits

- No blocking finding for task 11.2 requirements 1.1, 4.1-4.3, 5.2 and 6.1. Actual image qualification and the Windows private-state boundary now have aligned evidence.
- The supplemental auxiliary inspection reads the already-owned descriptor locally only to locate the state directory, then uses checked state handles. It is a disposable metadata probe, not an alternate production credential reader. It does not print descriptor contents. Private session files and databases must remain excluded from published evidence.
- Original ACL RED output remains transcript-only, as disclosed in resumed-review/review.md. This audit does not reconstruct that historical output.
- This is an evidence/script review, with identity/hash consistency checks; no additional runtime, provider call, image pull, test rerun or build was performed. Reviewed production caps remain 400/300/50; no production code was added in this follow-up.
- Live financial/browser behavior is task 11.3. Final Linux compatibility and migration closeout are task 12. Registry publication, server deployment, arbitrary third-party replacements and deletion of generated inherited files are outside this acceptance.

## Evidence examined

All paths below are under D:/BuildArtifacts/QOpenBB:

- native-app-build/receipt.json, identities.json, workspace.export.json, data-api.export.json, installed-module-checks.json, data-runtime-tests.stdout.log, qualification.md, run_build.py and run_checks.py.
- native-foundation/resolved-tools.json and the build snapshot's pinned tools.lock.json.
- native-state-acl/packaged-resume/smoke.json.
- native-state-acl/recreation-proof/run.py, result.json, commands.md and application-auxiliary-acl.json.
- native-state-acl/resumed-review/review.md, reviewed-files.json and prior independent native results.

Summary: APPROVED for task 11.2; the exact native-built image pair passes packaged qualification and preserves protected state through real recreation, while financial acceptance and final Linux closeout remain open.
