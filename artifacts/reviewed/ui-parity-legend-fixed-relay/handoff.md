# Review the fixed-target relay source before one topology probe

This package implements the [approved proposal](../ui-parity-legend-fixed-relay-plan/plan.md), SHA-256 `1c9a0e527acb77b808aab703df19ef8f6f8eacb1ed325987e51a5ea071703e65`, and its [independent plan review](../ui-parity-legend-fixed-relay-plan-review/review.md), SHA-256 `4a9c0a7641cad6e62d1fc4b30bdf1a07109ea60030885af7e26f65e1188c8887`. It prepares only a no-browser admission diagnostic. No Docker command, original-image executable, application, health request, socket, browser, topology probe, build, pull or install ran during source preparation. Existing frozen artifacts and application files remain unchanged.

The app joins exactly one owned internal bridge and publishes no port. Only the relay joins that bridge and one owned ordinary ingress bridge; only its port 3100 is published on host 127.0.0.1. Its read-only config fixes the admitted app numeric IPv4 and port 3000 once, with its hash recorded before relay startup. Python copies opaque bytes with backpressure, partial writes and delayed half-close. It never parses HTTP, selects a target from a client, resolves DNS or logs requests. Read-only root/source/config, nobody UID, dropped capabilities, no-new-privileges, disabled namespace forwarding, disabled inherited healthcheck and bounded `/data` tmpfs are selected admission requirements. No host firewall or daemon change is made. Existing internal-peer/host-bridge access remains possible; this is no hostile-host sandbox claim.

The candidate `/opt/.venv/bin/python` is supported by immutable original Dockerfile/supervisor source. Exact cached-image execution, Python flags, mount/inspect shapes and relay publication remain unverified and must fail without fallback. The [separately reviewed Moby diagnosis](../ui-parity-internal-network-source-review/review.md) explains the prior internal-only observation at source level; it does not verify this topology or the local daemon binary.

The fixed probe profile remains four concurrent pairs, sixteen accepted pairs, nine TCP sockets including listener, two 64-KiB buffers/pair, 4 MiB/pair, 32 MiB total and two-second connects. Capacity pauses listener admission. The sixteenth accepted pair conservatively closes admission and records an unresolved bound rather than risking an unrecorded seventeenth pair. Received bytes reserve forwarding capacity before queueing. Every bound/transport violation is retained in fixed counters. An active pair at shutdown records `transport-truncated`; a 200 cannot override it.

The host issues at most ten GETs to the single admitted loopback `/api/health`, at least three seconds apart, each limited to two seconds within thirty seconds measured from observed publication and remaining input time. It requests `Connection: close` and drains ordinary response bytes without retaining them, allowing completed health pairs to close naturally. Every 3xx or Location response stops unresolved without following. Only non-200/transport readiness results may use remaining slots on those same instances. There is no browser, login, fixture action, provider input, restart, recreation, alternate topology or automatic retry.

Selected identity/network/port/state operands persist before stopping assertions; raw inspect output, State.Error, environment, headers, bodies and credential arguments never become public receipts. Runtime/credential metadata stays private. The writer counts source copies/private bytes prospectively, reserves the relay's sole writable 4096-byte stats file, and retains at most 32 files/2 MiB, 64 KiB per public JSON and 512 KiB public JSON total. Four drained helper logs are reserved and capped at 8192 bytes each; overflow is explicit and fails final admission. Selected strings are bounded to 128 characters.

The watchdog retains the approved 90/60/150-second ceilings with conservative 85-second input, 145-second resource kill and four-second finalization sublimits. Each Docker command is bounded by five seconds and remaining stage time. Cleanup verifies exact names/IDs/labels before removing relay, app and both empty networks, then deletes only the recorded attempt state/credential paths and verifies absence. A failed graceful relay stop still attempts owned forced removal; missing final counters remain unresolved. Ownership mismatch, shared network, deadline or incomplete proof remains cleanup-unverified. No global prune, unrelated process or volume removal occurs.

Fresh [offline verification](offline-verification.json) covers injected topology/identity/state/redirect/readiness/counter/cleanup/budget faults, preassert persistence, finite log overflow and a 200 with violated relay counters. Nine Python unittest methods use fake sockets/selectors and a temporary stats file for target/byte/half-close/backpressure/socket/byte/connect/reset/stop faults. Windows Python 3.12.10 runs these stdlib tests; it is not exact-image admission evidence. JavaScript syntax and Debian `bash -n` are checked without launching the harness. [Source hashes](source-hashes.json), the [baseline diff](relay-source-diff.patch) and the [compatible publication selection](publication-allowlist.json) freeze this source handoff. Research is excluded from production size caps; future maintained code retains checker/inventory enforcement and 400 physical lines/file, 300 logical units/file and 50/function.

Canonical offline verification (read-only unless `--write` is explicit):

```powershell
node artifacts/ui-parity-legend-fixed-relay/verify-offline.mjs
```

After independent exact-source approval and a separate one-probe grant, the controller may prepare fresh attempt-local copies with the existing WSL Node:

```text
wsl -d Debian -u mc -- /mnt/d/Source/QOpenBB/artifacts/task-1.2/node-v24.22.0-linux-x64/bin/node /mnt/d/Source/QOpenBB/artifacts/ui-parity-legend-fixed-relay/prepare-run.mjs
```

Preparation verifies frozen inputs/copies, records their proof and reserves log bytes; it creates no runtime resource and grants nothing. It prints this exact hidden Windows launcher form with the actual generated attempt substituted:

```powershell
Start-Process -FilePath "$env:WINDIR\System32\wsl.exe" -WindowStyle Hidden -ArgumentList @('-d','Debian','-u','mc','--','env','LEGEND_RELAY_GRANTED=controller-granted','bash','<attempt>/supervise.sh','<attempt>') -PassThru
```

The controller must retain the returned helper PID/start identity and its actual exit status, verify helper absence, and independently inspect selected final receipts and exact owned-resource absence. The source also verifies attempt-copy hashes before its first Docker command. A topology success would approve no L01-L08 capacity or full UI retry: existing fixture, origin/redirect denial, blocked service workers, UI behavior and action/event/raster/lifecycle limits remain in the unchanged machine contract. Any future full UI transport needs separate asset/connection accounting and review. The controller owns grants, publication, documentation and Git.
