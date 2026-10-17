# Correct the relay mount representation without weakening admission

Propose a source correction that admits exactly three expected bind entries in Docker's runtime `Mounts` array and exactly one configured `/data` entry in `HostConfig.Tmpfs`. Keep the existing tmpfs value `rw,nosuid,nodev,size=1048576`, bind source identity checks, read/write flags and every other admission guard. This package contains a proposal and read-only source audit. It implements no predicate and authorizes no further probe.

The [frozen failed-attempt report](../ui-parity-legend-fixed-relay-revised/analysis-attempt-20261017T1700437-e5d5e603/report.md), SHA-256 `8dc1d929b2b377a55a96e8aea31d02c49f9925e620d97c5a3740ba1aebd62cb2`, records two running containers and relay loopback allocation, followed by `security.exactMounts=false` as the sole false security comparison. Its [selected observations](../ui-parity-legend-fixed-relay-revised/analysis-attempt-20261017T1700437-e5d5e603/observations.json) show the three expected runtime binds and the exact configured `/data` tmpfs string separately. The current receipt does not establish the total configured tmpfs key count. No health GET ran. Independent failed-attempt review is pending; this proposal neither accepts that attempt nor changes its unresolved outcome. No mutable analysis, private metadata or raw log was read.

The frozen [admission source](../ui-parity-legend-fixed-relay-revised/harness/admission.mjs) currently requires four runtime entries, including `/data` with type tmpfs. The frozen [probe source](../ui-parity-legend-fixed-relay-revised/harness/probe.mjs) instead invokes three `--mount` bind arguments and one `--tmpfs /data:rw,nosuid,nodev,size=1048576`. The [approved plan](../ui-parity-legend-fixed-relay-plan/plan.md) requires read-only source/config, a writable stats file and bounded `/data` tmpfs. It does not prescribe a fourth runtime `Mounts` entry. The proposed check preserves that contract while distinguishing the two inspect representations already selected by the source.

## Keep the predicate narrow

Name the proposed responsibility `exactRelayMountLayout(raw, runtime)`. Its acceptance is the conjunction of these two local checks; no fallback representation is accepted:

| Owner | Exact acceptance condition |
| --- | --- |
| Runtime bind layout, retaining `security.exactMounts` | `raw.Mounts` is an array of exactly three entries. It contains exactly the three destination/source/RW/type tuples below. Array order is irrelevant; extra or duplicate entries fail. |
| Configured tmpfs layout, retaining `security.boundedTmpfs` | `HostConfig.Tmpfs` is a nonnull, nonarray object with exactly one own enumerable key, `/data`, whose value is exactly `rw,nosuid,nodev,size=1048576`. A missing, inherited, reordered, larger or otherwise different value fails. |

The three bind tuples remain:

| Destination | Expected source identity | RW | Type |
| --- | --- | --- | --- |
| `/relay/relay.py` | Existing private `runtime.relaySourcePath` equality | false | bind |
| `/relay/config.json` | Existing private `runtime.configPath` equality | false | bind |
| `/evidence/relay-stats.json` | Existing private `runtime.statsPath` equality | true | bind |

Exactly three entries and one match for each distinct expected destination exclude duplicates without a new mount inventory framework. Do not accept a fourth runtime tmpfs or anonymous-volume entry as an alternative. Do not add a fourth bind, weaken source comparisons, normalize the tmpfs option string, accept additional tmpfs paths, increase size, change flags or retry another topology.

`relayArgs` and its create/start/network sequence need no proposed change. Root filesystem read-only, nobody UID, capability drop, no-new-privileges, forwarding sysctls, inherited healthcheck disablement, Python entrypoint/command, image/source identity, ownership, networks, port binding and running state checks retain their exact source conditions. Cleanup, relay transport, finite request profile, output bounds and lifecycle limits are outside this correction.

## Retain enough operands before evaluating the correction

The current selected receipt already keeps bounded runtime Mounts destination/type/RW fields, mount-source presence/type and private-path equality booleans. Its Tmpfs receipt keeps parent presence/type and the selected `/data` value. Retain those fields and add only a narrow shape summary for unexpected configured tmpfs keys:

| New operand | Supported object | Missing/null/array/scalar parent |
| --- | --- | --- |
| `parentSupported` | true | false |
| `keyCount` | Nonnegative count of own enumerable keys | null |
| `dataOwn` | Whether `/data` is an own key | false |
| `unexpectedKeyCount` | Number of own enumerable keys other than `/data` | null |

Counts are scalar safe integers obtained from the already bounded inspect JSON, not arrays or copied key strings. Exact acceptance requires `keyCount===1`, `dataOwn===true`, `unexpectedKeyCount===0` and the unchanged selected `/data` string. Parent presence/type still distinguishes absence, null, arrays and scalars. Do not retain unexpected key names, their values, mount source paths, ownership-label values, raw inspect, environment or credential arguments. Existing selected `/data` string handling retains at most 128 characters and otherwise records unsupported/length; no new arbitrary-value copier is needed. Persist these operands through the existing `observeContainer` callback before evaluating security, including failures. This addition closes an operand gap; it does not claim the consumed attempt already proved the new exact-key condition.

## Required offline matrix for a separately authorized source revision

These are planned disproof tests, not completed candidate tests. Exercise the actual revised `projectContainer`, `observeContainer` and `admitContainer` functions with the existing injected fixtures. No Docker, socket or network is needed.

| Synthetic fixture change | Expected result and retained evidence |
| --- | --- |
| Exactly the three binds and sole exact `/data` config, in any bind order | Mount checks pass; fully valid remaining fixture admits. Unrelated security comparisons remain identical. |
| Current four-entry runtime fixture including tmpfs; missing bind; duplicate bind; extra bind or volume | Runtime mount check fails. Bounded count and available selected runtime tuple operands survive before assertion. |
| Each expected bind has wrong destination, source identity, RW or type | Runtime mount check fails. Private source identity is a comparison only; no path is published. |
| Tmpfs absent, undefined, null, array or scalar | Tmpfs check fails; parent shape is distinguishable, key counts are null and `/data` unavailable. |
| Empty object; different sole key; own `/data` plus any extra key; inherited `/data` without own key | Tmpfs check fails; key count, dataOwn and unexpected count identify the shape without exposing names or values. |
| `/data` size/flags/order/value type changed, or value is oversized | Tmpfs check fails; selected presence/type/value or unsupported/length survives within existing bounds. |
| Extra tmpfs key/value and private mount source contain synthetic secret sentinels | Failure is persisted; serialized public receipts contain none of those sentinels or raw paths. |
| Missing versus false unchanged security flags; malformed ports, ownership/network/image drift or nonrunning state | Existing guards continue to fail with unchanged meanings; the correction cannot admit an unrelated security failure. |

Source tests should confirm the copied fixture represents exactly three runtime binds and one configured tmpfs, rather than rewriting an observed receipt or allowing both representations. A successful synthetic admission would establish only the proposed source predicate under mocks. It would neither reinterpret the consumed probe as successful nor establish actual tmpfs mounting/isolation on another engine.

## Evidence and approval boundary

The proposed change addresses inspect representation. It does not need a claim that all Docker engines omit configured tmpfs from runtime Mounts, and this package makes no such universal claim. No external Docker source was fetched. A future explanation about engine internals should inspect the pinned Docker 29.7.2/Moby commit `6a43e3d5afddf4111da0f864bbc7cae5d7e95001` separately; API compatibility alone would not attest the local daemon binary or prove actual mount isolation.

[source-hashes.json](source-hashes.json) pins the exact local source and approved plan read here. [verification.json](verification.json) records a read-only textual/source-pin audit, not execution of the proposed predicate. The [publication allowlist](publication-allowlist.json) selects only this safe proposal, audit, receipt and manifest. This source investigation reads no mutable run/private data and performs no container command, topology action, provider request, browser action, install, build or runtime probe. Original/frozen artifacts and production source remain unchanged. No future probe grant follows; controller review, a separately authorized minimal source revision, offline regressions and independent exact-source review remain required.

The owning specification language is English. Project delegation/testing/documentation/complexity/CI guidance applies. Research proposal files are excluded from production size caps; future maintained adoption retains inventory/checker enforcement and 400 physical lines per file, 300 logical units per file, 50 per function. Root owns documentation, publication and Git.
