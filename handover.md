# QOpenBB handover

Updated 2026-11-10. Native Docker and Compose work directly on Windows through Podman. The native-development-workflow specification has 13/15 executable tasks accepted. Tasks 11.3 (financial browser acceptance) and 12 (whole-migration closeout) remain open.

## Current result

- Root 537a5da accepted the Windows private-state repair and native application image qualification. Actual recreation retained account, origin, bind identity and SQLite state; application WAL/SHM files had owner-only Windows ACLs.
- The first authorized financial browser attempt failed at catalog discovery: /data/widgets.json returned 502 because nginx defaulted to Docker DNS 127.0.0.11 on Podman. Its stopped ledger records FMP 0 / FRED 0, with no denials. No retry occurred.
- Owned Workspace fork e1a12c3a031a23598f41166a0f91b8fb24ac2387 fixes DNS selection using the container's first valid nameserver while preserving explicit overrides. Six focused shell tests, baseline regression sensitivity, independent source review and pin/complexity checks passed. Branch: qopenbb/native-podman-dns.
- Root 0f4a8c9 promotes that reviewed source. Both Linux CI and CodeQL passed. The corrected Workspace image built once and passed actual host catalog/readiness, login and private-file checks. All eleven native widget definitions are available. See [accepted result](artifacts/reviewed/native-development-workflow/podman-dns-acceptance.md).

## Next action and authorization

Ask the owner to approve one additional financial browser batch, bounded at 80 FMP and 16 FRED attempted sends with no automatic reruns. The previous approval explicitly covered one run, so its zero usage does not authorize another execution.

After approval, update the external financial runner's immutable Workspace image binding and use a distinct explicitly authorized attempt identity. Preserve the original live-once claim and failed session; do not delete them to reset a run. Review the narrow image/attempt change and its compatibility with existing offline guard evidence before execution. Run the unchanged selected Income, company-selection initial/reopen and synthetic failure journeys. Record stopped cumulative ledgers before recreation/removal. A failed test is not acceptance.

Then obtain independent financial acceptance, update README/docs/spec/breadth checkboxes, sync concise evidence, commit and push. Task 12 still needs final cleanup/evidence closeout; Linux compatibility itself has passing evidence. No server deployment or registry publication has been performed for these local images.

## Exact current image pair

- Workspace: sha256:05e16ad56e7275a71edb3aadd4449063f3df40073713588b1f0dedee55e60053
- Data API: sha256:b3e56de1878d02f894d80111ba4ecff14b98292b9045ea6cc88e793f41a5f807
- Workspace source: e1a12c3a031a23598f41166a0f91b8fb24ac2387
- Data API source: 2e60c0a7aff039eda5f14a9d494beaec822fb9c4
- Build root: 0f4a8c9af13be0829e3be34220e882f29a8ecdfc, clean LF checkout D:/BuildArtifacts/QOpenBB/native-dns/source.

Do not rebuild either image without a source change. The earlier Workspace 72e207dd... is superseded for financial acceptance because of the DNS defect.

## Local evidence and tooling

All paths below are under D:/BuildArtifacts/QOpenBB unless stated otherwise.

- native-dns/: build receipt/export/load reports, actual qualification.json, source/pin/runtime reviews, clean pin candidates and exception proof. All 19 exception target blobs remained unchanged; only their source identities were promoted. No size baseline or expiry was relaxed.
- native-state-acl/: reviewed private-state repair, package smoke, real recreation and Linux evidence. Root 537a5da Linux run 42821688357 passed 450 tests, 12 skipped, one live deselected.
- Corrected source CI: https://github.com/norandom/QOpenBB/actions/runs/42827481611. CodeQL: https://github.com/norandom/QOpenBB/actions/runs/42827481547. Both succeeded; image publication was skipped.
- native-financial/: frozen external controller.py, handoff.py, batch_driver.py, offline_proof.py, inherited_reader.py and offline_readiness.py; driver-freeze.json; independent reviews; snapshot-v2 and its 76-file manifest. The runner still binds the older Workspace image until an approved retry update.
- native-financial/live-session/: private failed-run evidence. failed-final-ledger.json confirms zero requests; failed-stop.json confirms API stop. Parent also stopped Workspace. Never publish descriptors, runtime.env, credentials, browser raw logs or databases.
- native-financial/offline-session/: original failed isolated rehearsal, retained and stopped. Podman internal-only networking prevented host ingress; Podman remote cp-to-stdout was unsupported. Those rehearsal transport problems were corrected without changing application behavior.
- native-financial/offline-v2-session/: successful isolated rehearsal, resources removed and private evidence retained. It used container-local HTTP for the three fixed readiness paths, native copy into protected storage and a same-handle inherited-file reader. Original strict descriptor/sentinel storage remains unchanged.
- offline-proof-receipt.json SHA-256: 31e147119de19d6e9079b608a48a9388621f41ad857601647b9d8ca438f69cb0. Synthetic counts continued 1/1 to 80/16, with two expected ceiling denials and zero provider sends. This is guard/handoff evidence, not financial acceptance.
- Native Python: native-foundation/pipeline-venv/Scripts/python.exe. Use -B, PYTHONDONTWRITEBYTECODE=1 and PYTHONPATH=D:/Source/QOpenBB/pipeline from the repository cwd.
- Node: C:/Program Files/nodejs/node.exe, 24.22.1. Native dependencies: native-foundation/snapshot/verification/node_modules. Chromium: D:/BuildArtifacts/playwright. Do not use historical Linux dependency directories.
- Native Dagger CLI/SDK/engine: pinned 0.21.8, tools in native-foundation/resolved-tools.json. Retained owned engine qopenbb-dagger-engine-native-qualification-20261110122244, ID 8c14466951bf9ed3b5cbb31fbe971b0ede3e9ff9dd9bcd7ee2fe728898a96c13. Keep its cache; do not prune globally.

## Working-tree boundaries

Preserve unrelated preexisting work in .kiro/complexity-budgets.json, .kiro/complexity/workspace.json, pipeline/qopenbb_ci/catalog_cli.py, pipeline/qopenbb_ci/catalog_renderers.py and tests/contracts/test_renderers.py. The source-pin promotions were selectively staged from clean candidates, leaving these changes intact.

Use the clean owned Workspace checkout at D:/BuildArtifacts/QOpenBB/native-join/workspace. Root vendor/workspace is historical and must not be overwritten. Follow the project Sol implementer / Astra integration-review scheme, one heavy build or suite at a time, and 400/300/50 production caps. No WSL, global container cleanup, machine restart or unrelated Compose project changes are needed.
