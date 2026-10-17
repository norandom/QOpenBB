# The single Legend attempt stopped before browser admission

Attempt `attempt-20261017T1549043-3a567782` failed startup with `network-isolation-unresolved: loopback publication`. The original container was created, but the inspected publication did not satisfy the collector's exact loopback guard. The supervisor stopped before launching the browser journey. L01-L08 are all not run; there are no chart actions, field mutations, events, scene observations or PNGs. These zero counts are derived from the startup exit gate, not a fabricated journey counter receipt.

The exact values of `NetworkSettings.Ports['3000/tcp']` and `HostConfig.PortBindings['3000/tcp']` were not retained before the exception. Both shapes remain unobserved. This evidence cannot distinguish an unsupported internal-bridge publication from an incomplete inspect/readiness state or another publication mismatch. The container was removed; no recreation, alternate network, diagnostic topology probe or retry occurred. No renderer or original Legend control was reached, so no rendering behavior or UI parity is established.

Startup, cleanup and watchdog exited 1. The raw final result remains `cleanup-unverified`: the collector requires a browser PID identity receipt even when startup stops before browser launch, and no such receipt exists. A separate fresh read-only check verifies that the exact owned container ID, network ID, disposable state, generated credential file and startup PID are absent. Browser non-launch is supported by the source's nonzero-startup exit gate and absent journey log/status/identity; no universal browser-descendant absence claim is made. The heavy lane was explicitly released after those checks.

The run used the granted original source `38dffc33389aca0e4a87e0e88d42f7067aa220df` and image `sha256:f48eb1c9b32e1f84d5199dafc943bc1fc10f3b1745ab29860975d002dc5c8a3f`. All 21 fresh attempt-local source copies match the granted harness manifest `9ba3ebf7976b2fc8f0a027fd2823c93365cba5e297de5d988311da7c405f4531`; frozen source inventory `5b0674b7aae4e0a7c9e26fb26b7009def4e42fb73ed67865a31d71b34c502704` remains unchanged. The hidden Debian/mc supervisor used the exact granted command and existing Node v24.22.0. No candidate, production changes, live provider checks, owner environment or desktop browser were used.

The completed-output inventory rescans actual files after watchdog completion. Public selection includes exact executed source, safe raw status/proof receipts, eight explicitly derived not-run case records, this report, reproducible analysis scripts and sanitized error text. Raw logs and runtime-private data remain local. Sanitization records retain both original and derivative hashes and never assign an original hash to modified text. The proposed allowlist uses sourcePath/SHA256/bytes; the controller owns independent review and publication.

Read-only offline evidence check:

```powershell
node artifacts/ui-parity-legend-capture-redirect-guard/analysis-attempt-20261017T1549043-3a567782/verify-evidence.mjs
```

The separate owned-absence verifier ran once through existing Debian/mc Node and performs only exact-resource read checks. This failed attempt consumes the one runtime grant. Any later source or runtime work requires a new controller decision; no retry is implied by this report.
