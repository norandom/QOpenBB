# Native workflow foundation

Task 1 passed independent review on 2026-11-10. Pinned Windows tools and the existing combined code-size checker are usable. This is prerequisite acceptance, not an image build, browser run or application deployment.

The isolated environment uses Python 3.13.15, uv 0.12.5, pnpm 10.32.1, Safe Chain 1.5.25, Node 24.22.1, TypeScript 6.0.3 and Dagger CLI/SDK 0.21.8. Four Windows asset URL/checksum pairs were added to `pipeline/tools.lock.json`; existing version pins remain unchanged. Native Podman and its explicit Compose provider respond. Workstation configuration and Linux dependencies were preserved.

Both Safe Chain verification probes blocked the harmless malware-test packages before restoration. Protected frozen pipeline, verification and Dagger SDK restores exited 0. Dagger's real native executable reports the pinned version with process-local `FORCE_DARK_MODE=1`; actual engine execution remains task 10.

The existing `python -P -m tools.quality.complexity --check` command passed against a clean committed controller snapshot at `ef7422930ad712d0338a1f6bd639e877a496f2de`, with explicit fork scope and external output. It checked 79 controller baseline files with no errors or violations. An independent reviewer repeated the gate successfully. Unchanged accepted Workspace `f832a5593223b1e702970c4de8eceda87a17fa5b` and data API `2e60c0a7aff039eda5f14a9d494beaec822fb9c4` identities were checked separately; no fork remeasurement is claimed.

The promoted metadata matches the verified proposal and has 66 physical lines, below the 400-line cap. Metadata has no logical/function metric. Unrelated inventory and renderer edits were excluded from the baseline and left untouched.

Raw commands, restore/protection logs, source identities and fresh review results remain under `D:/BuildArtifacts/QOpenBB/native-foundation`. Independent review SHA256: `649dcea8484f7a027018466c1a0ea39313361f82a565e726e52b86be1b87fa2e`. No application build, provider request, WSL shell or VM reconfiguration was performed.

The [task plan](../../../.kiro/specs/native-development-workflow/tasks.md) owns remaining implementation and acceptance. Historical WSL evidence is unchanged.
