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

## Design discovery and synthesis, 2026-11-10

The owner approved requirements and requested the project subagent model for implementation. Two fresh Sol research contexts checked runtime/browser contracts and build toolchain behavior. The controller synthesized the design; Astra independently reviewed the integration seams. Applied skills: `kiro-spec-design` and its discovery, synthesis and review rules; project documentation, complexity, testing and delegation steering. The default product/tech/structure steering files are absent; the existing project-specific steering and accepted specs supply context.

### Design decisions

- **Generalize only the repeated boundary:** one checked private descriptor reader serves root financial tests and the fork's shared login fixture. One explicit container executable selection serves existing commands. Do not add a plugin system or a parallel test harness.
- **Adopt existing mechanisms:** Compose owns service lifecycle; Playwright resolves its bundled platform browser; Windows security APIs protect private files. Python and TypeScript wrappers carry project ownership and typed contracts rather than reimplement these tools.
- **Keep bind state:** a named volume would avoid Windows mount translation but depart from the owner's bind-mount deployment preference. Use an owned bind directory and prove the host-to-daemon mapping with a nonsecret sentinel. Failed mapping remains a qualification failure.
- **Keep Dagger pins together:** retain 0.21.8 CLI/SDK/engine, supplying a real native executable explicitly. The installed 0.21.11 wrapper overwrites runner selection, so it cannot transparently execute the existing locked build. A coordinated version upgrade is separate from this migration.
- **Preserve browser assertions:** the exact session name/image pair and changed Workspace container ID drive retained-state checks. Only descriptor access and checkpoint location change. The shared fork fixture's direct JSON read is an explicit test-only fork delta requiring independent review and pin promotion.

### External contracts

Compose's ordinary merge may retain an existing published port; use explicit replacement and inspect effective configuration before starting services. The supported `!override` tag requires Compose 2.24.4 or later. [Docker Compose merge reference](https://docs.docker.com/reference/compose-file/merge/).

Playwright exposes bundled browser resolution and configurable browser storage. Use those mechanisms instead of a Linux executable suffix. [BrowserType API](https://playwright.dev/docs/api/class-browsertype), [browser installation and storage](https://playwright.dev/docs/browsers).

### Qualification risks

The pinned Dagger transport must actually execute through Podman with verified engine identity; CLI connectivity alone is insufficient. Windows Safe Chain support and noninteractive interception must be demonstrated before dependency restores. Protected bind directories must remain accessible to the VM without weakening their owner-only Windows ACL. If either fails, retain a scoped blocker and review the exact design change rather than silently changing VM configuration, access controls or version pins.
