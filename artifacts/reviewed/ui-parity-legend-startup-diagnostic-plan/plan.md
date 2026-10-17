# Capture selected startup facts before another admission decision

Review this plan before preparing one minimal no-browser probe. The consumed Legend attempt failed at the loopback publication assertion without retaining either target port-map value. That evidence cannot identify a startup race, container exit or missing binding. This proposal adds only the facts needed to separate those observations. No runtime, topology probe, image build or dependency install is authorized here; the failed attempt and every frozen collector remain unchanged.

## Boundary commitments

This research plan owns a selected receipt contract and a finite future probe of the same original image on the same owned internal-network pattern. It owns no Legend interaction, financial fixture change, browser, alternate topology or production implementation. The original four-quarter/two-series fixture and L01-L08 remain untouched and unexecuted. A diagnostic result cannot automatically grant a full UI attempt.

Allowed dependencies are existing Debian/mc Node v24.22.0, the already loaded original image `sha256:f48eb1c9b32e1f84d5199dafc943bc1fc10f3b1745ab29860975d002dc5c8a3f`, original source label `38dffc33389aca0e4a87e0e88d42f7067aa220df`, the reviewed owned-network/cleanup patterns and selected Docker inspect fields. No new library, image pull, host firewall setting, gateway relay or daemon configuration is introduced. A change to image, network flags, selected paths, sampling bounds, deadlines or cleanup ownership requires a new independent review.

The kiro-spec-design skill's boundary-first, light-discovery and synthesis guidance informed this artifact. This is a research proposal, not a generated specification phase: no spec.json, requirements, design or task approval is changed. The owning specification language is English. Core product/tech/structure steering files are absent; the applicable testing, CI, documentation, delegation and complexity policies remain the project guidance.

## Selected receipt before assertions

One inspect of the exact owned container produces a bounded scalar projection and persists it successfully before any publication/state assertion. Full inspect JSON exists only transiently in memory with a 256-KiB command-output bound; it is never written, returned in diagnostics or published. Receipt writing is prospective and bounded. If projection or persistence fails, stop and clean up; a later assertion cannot erase the failure.

| Selected fact | Retained representation | Discriminator |
| --- | --- | --- |
| NetworkSettings, Ports and only key 3000/tcp | Parent/key own/in/kind/type; absent/undefined/null/value remain distinct. At most four entries, each with presence-aware HostIp and HostPort. Preserve array length and exact scalar strings. | Actual runtime publication at that read, including null, absent or empty arrays. |
| HostConfig, PortBindings and only key 3000/tcp | Same bounded representation; no enumeration of other ports. | Configured publication request independently from runtime allocation. |
| State and exactly Status, Running, Restarting, Dead, ExitCode, OOMKilled, StartedAt, FinishedAt | Presence-aware scalar leaves; maximum 128 characters/string. | Created/running/restarting/exited/dead observations and exit metadata, without container logs or State.Error. |
| Context for each receipt | Sample index, planned offset, actual monotonic start/end times, elapsed since docker run returned, exact owned resource IDs and selected ownership/isolation-match booleans. | Source/instance/time linkage and bounds, without publishing the ownership token. |

Unexpected scalar types retain their type/presence, not an object serialization. An array over four entries retains its actual length plus an explicit bound failure and stops; no truncated array is presented as complete. Do not inspect all port keys, all labels, environment, command, entrypoint, health-check content or logs. No HTTP header/body is retained. Configured dynamic HostPort can differ from an allocated runtime HostPort, including an empty configured string: preserve it rather than coercing it to zero or treating it as proof that no mapping was requested. The source launch argument remains exactly `-p 127.0.0.1::3000`.

Ownership and network isolation are checked before container creation and again for each observation. A sample records exact container/network identity matches, selected ownership-label match, one attached network, bridge driver, Internal=true and IPv6=false. Wrong ownership, a broad host binding or an extra network stops immediately. This diagnostic permits only observation of a missing allocation on the same verified isolated container; it does not relax the chart collector's admission guard.

## Finite no-browser probe

Create at most one disposable original container and one randomly named ownership-labeled internal bridge, using the existing DNS/proxy restrictions, state mount and loopback publication argument. Verify the exact loaded image and original-source label first. Persist private ownership identity before creation and actual IDs immediately after each creation. Fresh synthetic credentials remain in a mode-0600 private receipt, are never echoed or embedded in exception text, and are deleted during cleanup. Docker errors expose only fixed stage/reason and numeric exit status; raw argument/error dumps can contain credentials and are prohibited.

Take the immediate selected snapshot after docker run returns. Stop when it discriminates the operands: a valid runtime mapping, configured target absence, exit/dead state, security mismatch or malformed projection needs no further snapshot. Only a missing runtime allocation with an otherwise valid configured target and still-running verified instance admits the remaining read-only slots at target offsets +1,000 ms and +3,000 ms, stopping early if discriminated. Three is a maximum, not a readiness policy. Actual timestamps govern interpretation; slow commands create no extra samples or deadline extensions. Every stopping outcome retains its selected receipt first. These slots observe one instance; they are not restarts or recreate-until-pass.

After the last needed sample, permit at most one GET of `/api/health`, only if that sample proves a running owned container and exactly one runtime mapping to 127.0.0.1 with a numeric allocated port in 1..65535. Reject redirects, every 3xx and any Location header, including same-origin transitions. Record only status or a fixed timeout/transport reason. There is no browser routing, app login, dashboard substitution or provider request. Existing browser redirect/security guards remain frozen and are not weakened for this probe.

| Observation | Permitted conclusion | Limit |
| --- | --- | --- |
| Target runtime mapping is initially missing and later becomes valid while the same container is running | Delayed publication was observed at those times. | Does not prove the cause is a race or establish a general readiness delay. |
| Container is exited/dead/not running | The selected state/exit metadata explains why publication cannot be admitted at that read. | No exit root cause is inferred from ExitCode or OOMKilled alone. |
| Configured target entry is absent/null/empty | No configured target entry was observed in that bounded projection. | Source argument and actual map remain separate evidence; no repair is attempted. |
| Runtime target stays missing throughout the finite window | Publication was not observed within that window. | Does not prove the internal bridge cannot publish ports. |
| Valid runtime mapping but health is non-200, rejected redirect or transport failure | Mapping shape is supported; loopback health remains unresolved. | Does not collapse application readiness and binding behavior into one cause. |
| Valid mapping and exact loopback health 200 | The one topology/application origin passed this probe at that time. | Does not establish browser admission, Legend behavior or authorization to rerun L01-L08. |

## Executable bounds and cleanup contract

The machine-readable [probe contract](probe-contract.json) is authoritative for these proposed ceilings: one container/network, zero browsers, at most three snapshots, at most one health request, no restarts/recreation and no alternate topology. Stop new input at 90 seconds from probe start; reserve at most 60 seconds for cleanup; an independent watchdog hard-stops at 150 seconds. Docker calls are at most five seconds, the one health call at most two seconds, always further bounded by remaining stage time. These limits are below the consumed full-journey ceilings and cannot increase during implementation or a future run.

Retained output after state cleanup is at most 32 files/2 MiB, public JSON at most 512 KiB total and 64 KiB/file. Prospective checks cover each write; an actual final inventory includes the completed watchdog receipt. Private state lifetime is bounded by cleanup and is not represented as public retained evidence or falsely claimed to meet a public JSON quota.

Cleanup only recorded resources whose exact name, ID and selected ownership label match. Remove the owned container before its now-empty network, resolve the state path inside its exact new attempt prefix before deletion, delete the private credential, and verify absence. Refuse cleanup of any mismatched or still-shared resource and report cleanup-unverified. A separate no-browser probe records browserCreated=false from its source/lifecycle contract and does not require a nonexistent browser PID to prove container cleanup; that changes no status in the already failed Legend run. Hidden helper ownership and process cleanup stay bounded and exact. Missing proof never becomes a pass.

## Future file responsibilities and review gates

Any implementation is confined to a new `artifacts/ui-parity-legend-startup-diagnostic/` folder. Proposed files are `harness/probe.mjs` for pinned startup, selected projection, three slots and one health check; `harness/cleanup.mjs` for exact owned cleanup; `harness/run.sh` for the 90/60/150-second watchdog; `verify-offline.mjs` for synthetic failure tests; and source manifests/preparation/evidence scripts needed to freeze exact copies. Reuse the reviewed ownership pattern; do not introduce a generic discovery, polling or state framework.

1. After independent plan approval, prepare only this bounded source and offline tests. Test absent/undefined/null/empty/valid target maps, configured empty dynamic HostPort versus allocated runtime port, malformed/oversized arrays, exited/restarting states, later mapping, selected receipt persisted before failed assertions, wrong ownership/extra network refusal, sentinel credentials excluded from errors, redirect rejection, prospective output/deadline limits and cleanup failures. Planned tests are not completed evidence.
2. Independently review exact implemented source, synthetic fault receipts, manifests and the future canonical command. A reviewer must attempt to disprove the preassert persistence, same-instance sampling, no-browser/no-provider boundary and safe cleanup. Freeze any repaired source and repeat review; no runtime follows automatically.
3. Only a separate controller one-probe grant permits one hidden original-only probe. Preserve every partial receipt on failure, perform owned cleanup, release the heavy lane and independently interpret the result. Any subsequent UI-source change or new UI attempt is another review/grant decision.

Research documents/harnesses/tests are excluded from maintained production complexity caps. No production checker pass is claimed. Future production remains subject to the executable scope inventory/checker foundation, 400 physical lines/file, 300 logical units/file, 50/function and independent review. The controller owns documentation publication and commits.
