# Native workflow migration inventory

Read-only discovery on 2026-11-10 used two independent Sol lanes: runtime/browser tooling and build/toolchain compatibility. No application tests, provider requests or image builds ran in discovery.

| Area | Existing seam | Required design decision |
| --- | --- | --- |
| Windows entry point | `tests/delivery/workspace-runtime.ps1` forces `wsl.exe`; `pipeline/ci.sh` uses POSIX interpreter paths | Native command wrapper reusing existing Python commands; retain Linux CI wrapper |
| Disposable runtime | `tests/delivery/workspace_runtime.py`, `task25_runtime.py` use direct container lifecycle | Compose project for both services using root service definitions and isolated overrides; preserve readiness and exact image identity |
| Private state and cleanup | Runtime uses `getuid`, `O_NOFOLLOW`, `fchmod`, Unix modes and direct host/daemon path equality | Windows private-file ownership and validated Podman VM mount mapping without weakening cleanup guards |
| Browser launch | `verification/runner.ts` hardcodes Linux Chromium and POSIX entry-path recognition | Platform-aware pinned Playwright browser resolution and native entry detection |
| Evidence location | `verification/runner.py`, `evidence.ts`, `playwright.config.ts` use repository scratch output | Explicit validated external output roots and preserved Windows temporary environment |
| Real application journeys | `verification/financial-workspace.config.ts`, `tests/e2e/financial-workspace.spec.mts`, fork live-chart fixtures | Reuse existing origin, package and evidence-root settings; produce the two-image descriptor expected by financial E2E |
| Dagger pin | `pipeline/qopenbb_ci/image_cli.py` rejects CLI mismatch; tools lock and SDK pin 0.21.8 | Qualify a coordinated pin update or provision the existing pin; never bypass version checks |
| Native subprocesses | `image_cli.py` strips Windows system/temp variables; `build_cli.py` defaults Linux SDK Python | Preserve required Windows execution environment and explicit SDK interpreter without exposing credentials |
| Source identity | `pipeline/qopenbb_ci/sources.py` compares raw Git path text | Normalize native paths while retaining checkout-root and symlink checks |

## Proposed implementation order, not executable tasks

1. Native invocation, toolchain protection, output roots and private state handling.
2. Compose lifecycle and native browser tooling in separate owned lanes after their descriptor/output contracts are frozen.
3. Dagger export/load qualification with the reviewed pin combination, serialized with heavy runtime checks.
4. Existing packaged and financial Workspace browser journeys, including visible values, save/reopen and retained-state recreation; independent review and documentation/breadth closeout.

Use focused path/environment/lifecycle regressions, then reuse existing end-to-end tests. Synthetic infrastructure checks need no provider calls. Live-data acceptance is a separate explicit budget. Do not rebuild every image merely to repeat unchanged assertions.

This spec is a portability amendment to the local-development obligations of `openbb-self-service`, especially requirement 3 and foundation tasks 1.2, 1.7 and 1.8. Their historical accepted WSL evidence remains unchanged. Native acceptance needs new evidence; a successful version or connection command is insufficient.
