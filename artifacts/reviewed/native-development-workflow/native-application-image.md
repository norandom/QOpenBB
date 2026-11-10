# Native application image qualification

The actual Workspace and data API images pass native Windows package and retained-state checks. Reuse this pair for financial browser acceptance; no rebuild is needed. Task 11.3 financial journeys and task 12 final Linux compatibility remain open.

## Image and source identity

Built once using native Dagger CLI/SDK/engine 0.21.8 from clean root 72b10f6, Workspace 18930d870caec08df12697e7858e05e8dbe9dd68 and data API 2e60c0a7aff039eda5f14a9d494beaec822fb9c4.

| Image | Loaded image ID |
| --- | --- |
| Workspace | sha256:72e207dd92dba9c12dc67854ccaea285b8a75fb9117e8d2c3c9f8495ef52da1a |
| Data API | sha256:b3e56de1878d02f894d80111ba4ecff14b98292b9045ea6cc88e793f41a5f807 |

The three offline data-image checks passed. All 428 installed Python source files match staged sources. Engine, archive, manifest and loaded identities are recorded in the retained native-app-build receipt and identities files.

## Windows state and package acceptance

On 2026-11-10 the existing package smoke passed against the same image pair: Full configuration, health 200, login 200, invalid password 401, verified bind state and secret-free logs. Container-internal configuration and bootstrap files remain mode 0600 under a non-root user. Windows-bound database and secrets files use verified owner-only Windows ACLs; guest mode 0777 is not treated as the Windows permission authority.

The state-root repair gives container-created files an inherited owner-only ACL while preserving the stricter descriptor and sentinel policies. Independent native review passed 91 tests with three POSIX-only skips. All reviewed file hashes matched before delivery. The combined size gate covered 101 controller files with zero errors or violations. Original failing-test output was not retained; the historical real ACL failure is recorded, and no replacement historical log was fabricated.

One separate actual Compose recreation passed: both containers were replaced; the account, origin, bind identity, committed SQLite marker, secrets hash and replacement file survived. Owner-only ACL checks passed for the application's real WAL/SHM files and for a disposable database during an active WAL transaction. The uncommitted transaction rolled back. No application database records were modified by this probe.

Both acceptance sessions removed only their recorded containers/networks and retained their state. No provider calls, publication or server deployment occurred. Explicit generated-state deletion remains outside this acceptance.

## Reproduction and evidence

Commands ran from D:/Source/QOpenBB with native Python at D:/BuildArtifacts/QOpenBB/native-foundation/pipeline-venv/Scripts/python.exe and PYTHONPATH pointing to repository pipeline code. The package command was `python -B -m qopenbb_ci.workspace_smoke --image <Workspace ID above> --data-image <Data API ID above> --report <external report path>`. It exited successfully. The recreation runner exited 0 and uses the checked startup/recreate/stop APIs.

Retained local evidence under D:/BuildArtifacts/QOpenBB:

- native-app-build/receipt.json, identities.json and installed-module-checks.json: build and source provenance.
- native-state-acl/packaged-resume/smoke.json: ordinary packaged acceptance and cleanup.
- native-state-acl/recreation-proof/result.json, application-auxiliary-acl.json, run.py, commands.md and hashes.json: retained-state and auxiliary-file checks.
- native-state-acl/resumed-review/review.md, reviewed-files.json and results.xml: independent patch review.
- native-state-acl/combined-gate.json: scoped complexity result.

Private descriptors, credentials and retained databases are not published. The independent image acceptance review is linked separately. These checks do not establish live financial-data behavior or deployment on the owner's Linux server.
