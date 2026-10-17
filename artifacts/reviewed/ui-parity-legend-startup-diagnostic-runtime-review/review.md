# Accept the finite diagnostic evidence; publication remains unresolved

VERDICT: APPROVED for the evidence interpretation and exact 27-file publication selection. No blocking discrepancy was found. The completed probe observed a configured loopback/dynamic binding and a null runtime allocation on three samples of one running owned instance. This is not a root-cause finding, application-health pass or grant for another probe or Legend journey.

Reviewed on 2026-10-17 against the [frozen report](../ui-parity-legend-startup-diagnostic/analysis-attempt-20261017T1615437-672fb2a3/report.md), [raw selected samples](../ui-parity-legend-startup-diagnostic/attempt-20261017T1615437-672fb2a3/samples.json) and [accepted exact source review](../ui-parity-legend-startup-diagnostic-review/review.md). The supplied evidence allowlist SHA-256 is `7c846fea4bc194c8ad83ae32829ee85022af7d3b25beaee2795744b3a2fbb0b1`. All seven executed runtime files match manifest `29096d4612637299972e068e4b4d76dbe1331051e1dce7f885258cb3bc79fe3b`; source inventory `95128fc21fd7f16d230e5e7488ee32972822c00134cd045b689ff9e4ba1a4a7b` remains unchanged.

## What the receipts establish

The runtime target `NetworkSettings.Ports['3000/tcp']` is own/in=true, kind=null, value=null in all three samples. The configured target has one entry with HostIp `127.0.0.1` and HostPort `""`. Those distinct operands support a configured dynamic-port request with no allocated runtime binding observed in this window.

| Sample | Planned offset after run return | Actual selected read end after run return |
| --- | --- | --- |
| 1 | 0 ms | 51.171405 ms |
| 2 | 1,000 ms | 1,054.140286 ms |
| 3 | 3,000 ms | 3,064.424519 ms |

Read start/end times are ordered, and the same container/network IDs and StartedAt appear throughout. Every sample records Status=running, Running=true, Restarting=false, Dead=false, ExitCode=0 and OOMKilled=false. Ownership, attached-network count, exact network identity, internal bridge and IPv6 checks all pass; projection errors are empty. These are observations at the selected reads, not continuous monitoring or proof of the daemon's internal cause. The derived observation values match the raw receipts.

The exact executed classifier returns allocation-pending for each sample. Its finite sequence therefore finishes `publication-not-observed-within-window`, with no health result. The source gate makes the health call unreachable on these receipts; the zero-health count is a derivation from that source and result, not packet capture. The executed harness has no browser launch or Legend actions, and no restart/recreation path. No application or provider acceptance follows.

The [run status](../ui-parity-legend-startup-diagnostic/attempt-20261017T1615437-672fb2a3/run-status.json) and watchdog preserve exit 1. `diagnostic-closed` denotes completed cleanup around the unresolved observation, not a healthy publication result. The derived 5,940 ms to watchdog completion uses file modification time minus recorded startup time; it is not a separate monotonic process-lifetime measurement. Sample timings and the retained status agree with completion within the accepted limits.

## Cleanup and publication scope

The raw [cleanup report](../ui-parity-legend-startup-diagnostic/attempt-20261017T1615437-672fb2a3/cleanup-report.json) says cleaned, with container/network/state/credential absent and no failure. The saved [owned-resource absence check](../ui-parity-legend-startup-diagnostic/analysis-attempt-20261017T1615437-672fb2a3/owned-absence.json), timestamped 16:16:47.415Z, independently queried the exact recorded container/network IDs and checked owned filesystem paths. Its source was read but not executed in this review. The saved [launcher check](../ui-parity-legend-startup-diagnostic/analysis-attempt-20261017T1615437-672fb2a3/launcher-absence.json), timestamped 16:16:45.5133496Z, names the same Windows launcher PID as launch.json and reports absence. These receipts have exact resource/process scope; they do not prove absence of every possible descendant. Current filesystem reads also found no state directory or credential file. No nonexistent browser PID is required for this lifecycle, and the old full-Legend failure remains unchanged.

An independent actual scan found 25 retained attempt files totaling 33,226 bytes, including omitted private metadata and six empty raw logs. Public JSON totals 11,474 bytes; every JSON is below 64 KiB. These satisfy 32 files, 2 MiB retained and 512 KiB public JSON limits. The runtime inventory's 24 files/32,070 bytes exclude its own 1,156-byte receipt explicitly; adding that receipt reproduces the completed scan exactly.

The [reviewed evidence selection](reviewed-evidence-publication-allowlist.json) is byte-identical to the supplied 27-entry allowlist and is approved. It contains 18 exact attempt-source/selected-receipt files and nine analysis/provenance files. It excludes runtime-private.json, credentials, state and all raw logs. Selected values contain neither the private ownership token nor generated credential patterns; the bounded common-token/private-key scan is clean. No sanitized derivative claims an original hash. Source scripts for packaging and owned-absence checking are reproducibility evidence, not permission to execute them. Copy the source allowlist separately as metadata without a self-hash.

## Verification and boundary

The [review audit](audit.mjs) exited 0 under Windows Node v24.20.0 with 11 grouped checks, including exact identities, selected scalar values/timings, derived/raw agreement, status, cleanup receipt scope, actual inventory, secret exclusion, supplied read-only verifier and frozen preservation. The supplied verifier also exited 0. The [facts receipt](verification.json) records results and explicitly states that the reviewer did not repeat live absence checks.

```powershell
node artifacts/ui-parity-legend-startup-diagnostic-runtime-review/audit.mjs
```

Only this new review directory was written. No Docker command, network/health request, process probe, runtime retry, build, install or Git mutation ran. Applicable testing, delegation, documentation and complexity steering remain in force. These are research artifacts excluded from production caps; future maintained work still requires the inventory/checker foundation and 400 physical lines/file, 300 logical units/file and 50/function. The [review publication allowlist](publication-allowlist.json) is compatible with the controller's publisher. The controller owns destination hash/link verification, publication and commits. This completed diagnostic consumed its one grant; further work requires its own bounded decision.
