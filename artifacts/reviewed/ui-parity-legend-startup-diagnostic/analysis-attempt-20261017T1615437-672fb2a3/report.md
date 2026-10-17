# Configured loopback publication remained unallocated in this probe window

The single granted no-browser diagnostic, `attempt-20261017T1615437-672fb2a3`, retained three selected snapshots and ended `publication-not-observed-within-window`. Each runtime `NetworkSettings.Ports['3000/tcp']` was own/in=true with kind null and value null. Each configured `HostConfig.PortBindings['3000/tcp']` contained one entry with HostIp `127.0.0.1` and empty HostPort, preserving the dynamic-port request. The configured entry was present; a runtime allocated port was not observed.

| Snapshot | Planned offset | Actual selected read end after docker run returned | Container status | Runtime target |
| --- | --- | --- | --- | --- |
| 1 | 0 ms | 51.17 ms | running | null |
| 2 | 1,000 ms | 1,054.14 ms | running | null |
| 3 | 3,000 ms | 3,064.42 ms | running | null |

All three receipts recorded Running=true, Restarting=false, Dead=false, ExitCode=0 and OOMKilled=false on the same container/network IDs. Exact ownership, one attached internal bridge, driver and IPv6 checks were true. The samples were persisted before classification. These observations distinguish a present configured binding and a running container from the missing runtime allocation. They do not prove an unsupported topology, a startup-race cause or what would happen after this window.

No health GET occurred because no allocated runtime port satisfied the gate. No browser, login, dashboard, provider check, Legend case, restart, recreation or alternate topology ran. The result consumes this one diagnostic grant and gives no permission for a UI attempt or another probe.

The raw final result is exit 1, `diagnostic-closed`, with the specific unresolved publication outcome. Cleanup recorded `cleaned`: exact owned container/network/state/credential absence. A fresh read-only check independently confirmed those absences, and the hidden Windows launcher PID was absent. No browser PID was invented for this lifecycle. The heavy lane was explicitly released after these checks. The historical full-Legend attempt remains unchanged with its earlier cleanup-unverified status and unobserved operands.

The attempt used the pinned original source `38dffc33389aca0e4a87e0e88d42f7067aa220df` and image `sha256:f48eb1c9b32e1f84d5199dafc943bc1fc10f3b1745ab29860975d002dc5c8a3f`. All seven attempt-local runtime files match accepted manifest `29096d4612637299972e068e4b4d76dbe1331051e1dce7f885258cb3bc79fe3b`; source inventory `95128fc21fd7f16d230e5e7488ee32972822c00134cd045b689ff9e4ba1a4a7b` remains unchanged. Preparation and the exact attempt-local supervisor ran through existing Debian/mc Node v24.22.0 and a hidden Windows launcher.

The completed-output inventory scans actual files after watchdog completion. The source-safe allowlist includes exact executed source, selected whitelist receipts, status/preparation/cleanup proofs and bounded analysis. Raw private runtime metadata, generated credentials and every raw log remain excluded. Selected bytes are unchanged, so their hashes remain original hashes; no sanitized derivative is mislabeled. No root documentation, Git, production, owner environment or frozen source was changed.

Read-only evidence verification:

```powershell
node artifacts/ui-parity-legend-startup-diagnostic/analysis-attempt-20261017T1615437-672fb2a3/verify-evidence.mjs
```

Independent evidence review is next. Any further investigation requires a new bounded source/review/controller decision, rather than extending this finite observation window.
