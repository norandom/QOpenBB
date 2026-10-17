# Accept the failed-attempt evidence; the topology remains unresolved

VERDICT: APPROVED for the failed-attempt interpretation and exact 26-file publication selection. No blocking discrepancy was found. The probe stopped at relay mount admission before readiness. This is neither a healthy topology result nor permission for a retry or Legend journey.

Reviewed on 2026-10-17 against the [frozen analysis report](../ui-parity-legend-fixed-relay-revised/analysis-attempt-20261017T1700437-e5d5e603/report.md), SHA-256 `8dc1d929b2b377a55a96e8aea31d02c49f9925e620d97c5a3740ba1aebd62cb2`, and its 26-entry publication allowlist, `a0c8a3224ce04bdda3efb58c955166db805a3993f0d1191b99a75e5e58de7aa2`. All eight executed attempt copies match the accepted manifest `dcb25a5a5bcadf2d5628b0f2ebd2077586c7bde325a063b4eb5bf72f266b8700`. Accepted source manifest `7d1dbfc86d2cef42d8b8e73eacf63c85dd0c3676938c95d10210976cd5d263fb` and [source review](../ui-parity-legend-fixed-relay-revision-review/review.md) remain unchanged.

## The receipts identify the stopping condition

The [selected admission receipt](../ui-parity-legend-fixed-relay-revised/attempt-20261017T1700437-e5d5e603/admission-receipts.json) records both containers running. App identity, single internal attachment and absent publication checks pass. Both network roles pass. Relay identity, two attachments, security flags and loopback allocation pass except `exactMounts`. Runtime publication records `127.0.0.1:32807`; this is an allocation observation, not an HTTP result.

The three selected Mounts entries are the two read-only relay source/config binds and the writable stats bind. Their source identity comparisons all match. The separate HostConfig tmpfs value for `/data` is `rw,nosuid,nodev,size=1048576`, and `boundedTmpfs` is true. The executed predicate explicitly requires four Mounts entries, including `/data` with type tmpfs. Reapplying the executed classifier to the selected receipt returns `security-unresolved`, matching the raw result at `relay-inspect`.

That is evidence of a mismatch between the inspect representation and the frozen predicate. It does not inspect the live `/data` mount, establish all possible Docker representations, or justify relaxing unrelated guards. The resources have been removed. Any correction belongs in a separately reviewed source revision.

The [relay stats](../ui-parity-legend-fixed-relay-revised/attempt-20261017T1700437-e5d5e603/relay-stats.json) show a closed clean stop, one peak listener socket, zero accepted pairs, zero bytes and zero violations. The source throws on failed relay admission before its readiness call; no health-attempt receipt exists. Thus the zero harness health-GET conclusion follows from exact control flow, status and counters, not a packet capture of every possible application activity. There is no browser launch or Legend action path in this harness. The unused ten-GET allowance does not authorize another attempt.

The [final status](../ui-parity-legend-fixed-relay-revised/attempt-20261017T1700437-e5d5e603/run-status.json) correctly preserves exit 1 and `probe-unresolved`, despite admitted zero-violation relay counters. `diagnostic-closed` describes cleanup completion, not topology success.

## Cleanup and finite evidence agree

The [cleanup receipt](../ui-parity-legend-fixed-relay-revised/attempt-20261017T1700437-e5d5e603/cleanup-report.json) records graceful relay stop and exact recorded-ID plus expected-name absence for both containers and both networks, followed by state/credential absence. Its identity evidence satisfies the executed cleanup classifier. The saved [independent resource check](../ui-parity-legend-fixed-relay-revised/analysis-attempt-20261017T1700437-e5d5e603/fresh-owned-absence.json) reports eight read-only queries against those recorded IDs and names. Its source was inspected: it reads the exact attempt's private ownership record and issues only bounded list queries. This reviewer did not repeat those live queries or run its receipt-writing script. Fresh filesystem reads confirm the attempt's state directory and credential file are absent.

The saved [helper check](../ui-parity-legend-fixed-relay-revised/analysis-attempt-20261017T1700437-e5d5e603/fresh-helper-absence.json) matches PID 41536 and start ticks `639278532662379268` in the launcher receipt. It reports that exact identity absent. The launcher receipt records hidden `wsl.exe` execution and exit 1. This establishes the recorded helper scope, not absence of every possible descendant. The resource-absence timestamp minus helper start is 69,458 ms at the stored timestamp precision, below 150 seconds. It is a conservative bound through a later read-only check, not a measured probe runtime.

An independent filesystem inventory finds 24 retained attempt files, 58,083 bytes total and 13,236 public-JSON bytes. Every public JSON is below 64 KiB. The raw runtime inventory excludes its own 1,095-byte file and recorded a 225-byte helper receipt that later shrank to 221 bytes. Adding the inventory file and subtracting that four-byte change reproduces the final total exactly. Both inventories therefore remain useful without silently rewriting the earlier one. The retained set stays below 32 files, 2 MiB total and 512 KiB public JSON.

## Publication and verification

The [reviewed evidence selection](reviewed-evidence-publication-allowlist.json) is byte-identical to the supplied 26-entry list and is approved. It selects 18 executed-source/attempt-receipt files and eight analysis/provenance files. Private runtime metadata, credentials, state and all four raw logs are excluded. The logs are empty locally. Exact ownership-token exclusion, generated credential-pattern checks and bounded common-token/private-key scans found no concrete secret in the selected files. These checks do not claim exhaustive recognition of every secret format. No sanitized derivative is assigned an original file's hash.

The [read-only audit](audit.mjs) passed ten grouped checks covering frozen identity, exact copies, classifier/state evidence, mount operands, stopping control flow, cleanup scope, helper identity/timing, inventory reconciliation, secret exclusion and the supplied verifier. The supplied verifier independently exited 0 with its twelve checks. The deterministic [verification receipt](verification.json) records those results and the live checks that were not repeated.

```powershell
node artifacts/ui-parity-legend-relay-attempt-review/audit.mjs
```

The [review publication selection](publication-allowlist.json) covers this completed review package. Keep both allowlists as metadata without self-hashes; verify destination bytes and preserve relative evidence links when mirroring. The absence-check script is retained as provenance, not an instruction to recreate resources.

Only the new review directory was written. No Docker command, helper process query, runtime retry, network request, browser, build, install, source edit or Git mutation ran in this review. Research artifacts are excluded from production size caps; future maintained work retains inventory/checker enforcement and 400 physical lines/file, 300 logical units/file and 50/function. The controller owns subsequent source decisions, runtime grants, publication and commits. This failed attempt consumed its one grant.
