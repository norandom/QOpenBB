# Accept the narrow startup diagnostic plan

VERDICT: APPROVED for the source plan and exact publication set. No blocking issue or required plan correction was found. The proposed selected-read diagnostic is sufficient to distinguish the missing startup operands without extending into a browser journey or a general polling framework. This review grants neither implementation nor runtime execution.

Reviewed on 2026-10-17 against [plan.md](../ui-parity-legend-startup-diagnostic-plan/plan.md), SHA-256 `efa8a5f3befea5ea6ba5c2494a7370e93f663567c977236521574985f7316eb0`. The [verification receipt](verification.json) pins the source manifest and allowlist. The review read the failed startup report, [its independent review](../ui-parity-legend-startup-review/review.md), frozen startup/network/cleanup source, and testing, CI, documentation, delegation and complexity steering. English is the owning specification language. The local review protocol is applied to a research plan, not a specification-phase approval or implemented behavior.

## Why the plan is bounded and useful

The prior attempt failed its loopback predicate before browser launch and did not retain either target port-map shape. The proposed projection records the two distinct operands, `NetworkSettings.Ports['3000/tcp']` and `HostConfig.PortBindings['3000/tcp']`, before the assertion that previously discarded that distinction. Presence and scalar shape remain explicit. Configured empty dynamic HostPort is preserved separately from allocated runtime HostPort; the plan does not infer a missing launch request from an empty configured string.

The source/image pins, internal bridge, DNS/proxy restrictions and `-p 127.0.0.1::3000` agree with the frozen failed startup source. No alternate network, relay, browser or image is introduced. The immediate snapshot can close the probe. Only a still-running, verified same instance with valid configured target but missing runtime allocation allows the +1,000 ms and +3,000 ms slots. Actual timestamps and existing deadlines determine interpretation; the three slots do not become a readiness policy or an automatic retry.

Eight named State leaves provide enough status/exit context to interpret the binding observations. Raw State.Error, environment, commands, entrypoint, health details, logs and full inspect output are excluded from retained receipts. Four-entry target arrays, 128-character scalar limits and the 256-KiB transient inspect bound keep projection finite. An excessive or malformed value stops rather than presenting clipped content as a complete observation. Full inspect data stays transient, and errors expose only fixed reason/stage and numeric status.

The single optional health GET requires a validated running owned container and one allocated loopback mapping. All redirects, 3xx responses and Location headers are rejected; no headers/body are retained. This can distinguish mapping evidence from application health at one time. It cannot establish browser admission, Legend behavior, a root cause or permission for another UI attempt.

## Bounds, ownership and next gates

The machine contract and prose agree: one container, one internal network, zero browsers/providers/restarts/recreations, at most three snapshots and one health request. New input stops at 90 seconds, cleanup has at most 60 seconds, and the independent hard bound is 150 seconds. Five-second Docker calls and a two-second health call are further limited by remaining stage time. The 32-file/2-MiB retained ceiling, 512-KiB public JSON total and 64-KiB public file ceiling are compatible and prospective, with a final completed-output inventory. Private state is not mislabeled as bounded public JSON evidence.

Cleanup is restricted to the recorded name, ID and ownership label; the container is removed before its empty network, state deletion remains inside the exact new attempt prefix, and absence is verified. Mismatched/shared resources or missing proof remain cleanup-unverified. A separate no-browser lifecycle does not need an invented browser PID. This changes neither the old attempt's cleanup-unverified status nor the fact that its single runtime grant was consumed.

The proposed probe/cleanup/supervisor/offline-test responsibilities are concrete and small. The next source review must verify the already specified projection, preassert persistence, same-instance stop rules, command/output/deadline enforcement, secret exclusion, redirect rejection and partial cleanup paths against executable code and synthetic faults. Those tests are currently planned, not passed. No additional framework or broader process guarantee is required by this plan review. A separate controller decision governs source preparation, followed by independent exact-source review and a separate one-probe runtime grant.

## Mechanical checks and publication

The supplied `freeze-plan.mjs` completed with exit 0 under the review-owned [read-only preload](read-only-freeze.mjs). Its three writes to verification, source hashes and allowlist were suppressed only after matching the frozen bytes exactly. The independent [audit](audit.mjs) completed with exit 0 and 66 checks: dispatch pins, 18 named input hashes, selected source/publication bytes, contract/source consistency, bounds, exclusions and source links. No probe, Docker command, health request, browser, build, installation, Git operation or frozen mutation ran. No placeholder or concrete private-key/common-token pattern was found in selected content; this is a bounded content check.

Reproduce the protected plan checks from the repository root:

```powershell
$previousNodeOptions=$env:NODE_OPTIONS
try {
  $env:NODE_OPTIONS='--import ./artifacts/ui-parity-legend-startup-diagnostic-plan-review/read-only-freeze.mjs'
  node artifacts/ui-parity-legend-startup-diagnostic-plan/freeze-plan.mjs
} finally { $env:NODE_OPTIONS=$previousNodeOptions }
node artifacts/ui-parity-legend-startup-diagnostic-plan-review/audit.mjs
```

The exact [six-entry plan allowlist](../ui-parity-legend-startup-diagnostic-plan/publication-allowlist.json) is approved for publication. Entries use sourcePath/hash/bytes; its array format remains compatible with the publisher. Copy the allowlist separately as metadata without a self-hash. Its selected files contain the plan, research, contract, freezer and receipts, with no private runtime values. The [review allowlist](publication-allowlist.json) similarly selects this review, audit, preload and receipt. The controller must verify destination hashes and links after synchronization. The supplied freezer is checked at its original source location; no relocated-command portability claim is made.

All review writes stay in this new review directory. Research artifacts are excluded from production complexity caps; future maintained work still requires the executable inventory/checker foundation, 400 physical lines/file, 300 logical units/file, 50 logical units/function and final shared-module audit. Production RED and runtime acceptance are not applicable to this plan-only gate.
