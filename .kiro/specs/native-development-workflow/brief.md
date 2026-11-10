# Native development workflow

QOpenBB developers and agents need to build and verify the application from Windows using the owner's installed Podman Desktop, Docker Compose and native Dagger. The existing workflow contains WSL launchers, Linux browser paths and Unix-only state handling. The owner requested migration of the full end-to-end workflow, including Playwright, on 2026-11-10.

## Boundary candidates

- Include native command entry points, isolated Compose runtime, browser and packaged checks, build compatibility, artifact routing and documented repeatable commands.
- Preserve existing application behavior, meaningful assertions, source/image identity, private credentials, saved-state verification and bounded worker counts.
- Preserve portable Linux CI and pull-only server deployment. Dagger owns builds only; Compose owns local service orchestration.
- Exclude application features, provider expansion, a new test framework, user VM reconfiguration and historical evidence rewriting.

## Observed baseline

Native Podman responds and Compose configuration parses with parser-only credentials. A native Dagger query connects and returns version 0.21.11. These are connectivity checks, not application or build acceptance. The project pins Dagger CLI/SDK/engine 0.21.8. Podman reports machine type `wsl`; no WSL shell was invoked and this migration does not change the owner's VM backend.

Disposable Windows outputs belong under D:/BuildArtifacts/QOpenBB. Linux dependencies stay in the Linux VM filesystem. Maintained source, documentation and selected reviewed evidence remain in the repository.
