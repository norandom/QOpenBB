# Review the final redirect guard before any runtime

This source revision addresses only the remaining B01 path in the [latest independent review](../ui-parity-legend-collector-revision-review/review.md). The [accepted eight-case plan](../ui-parity-legend-plan-revised/plan.md), SHA256 `5a33a0237eb351df5a7a6060da2aff5c83379f89999c4a4ca82faa40c92e29ef`, remains unchanged. The previous collector sources and reviews stay frozen; only this new folder is writable. No browser, application, container, topology test, build, install or runtime attempt is part of this task.

All context handlers independently validate approved HTTP(S) origin before fetching or fulfilling. Unsupported protocols and unapproved origins abort without a fetch. Every actual HTTP(S) passthrough, including generic GET/non-GET and sync non-GET, now uses exactly one route.fetch with maxRedirects=0, maxRetries=0 and the existing four-second timeout. It leaves method and request-body overrides unset, preserving the original request semantics. There is no unrestricted route.continue path.

The collector rejects every 3xx response, every Location header regardless of status or header casing, and any invalid or foreign response identity before fulfillment. Each rejection records a fixed bounded diagnostic reason and aborts as traffic-unresolved. Location values, query strings, headers and bodies are not logged. A same-origin application redirect also stops the future attempt; no redirect chain is followed, simulated or repaired. Ordinary generic and sync non-GET responses pass the original response object to fulfill, retaining their status, headers and body. The existing sync GET synthetic-dashboard projection remains the same controlled fixture override and now retains the fetched response envelope.

All other runtime files match the previous revision after normalizing only this new artifact directory name where required by ownership checks or shell paths. Static verification enforces that comparison. The L01-L08 program, original controls, four-quarter/two-series fixture, scene identities, seven BBox getters, fourteen operands, invalid-sample diagnostics, internal owned network, PID/start-ticks cleanup, atomic event/overflow handling and all action/mutation/output/time limits remain unchanged. This is research code excluded from production size caps; future production retains the checker/inventory foundation and 400 physical lines/file, 300 logical units/file and 50/function.

The offline checks retain all 25 previous tests and add five redirect-focused tests covering generic GET/POST, sync non-GET, foreign identity, foreign and same-origin redirects, all 3xx/Location cases, ordinary response passthrough and unsupported protocols. They use synthetic route callbacks and never perform HTTP fetches. Counters assert one owned-origin mock fetch per permitted request and zero fetches for rejected initial protocols/origins. These source checks do not establish that original login/navigation works under redirect rejection.

Run the source checks:

```powershell
node artifacts/ui-parity-legend-capture-redirect-guard/offline-tests.mjs
node artifacts/ui-parity-legend-capture-redirect-guard/static-check.mjs
node artifacts/ui-parity-legend-capture-redirect-guard/freeze.mjs
```

The compatible publication-allowlist.json uses sourcePath/SHA256/bytes and is proposed source-only material for independent review. It grants no publication or runtime permission. The controller owns mirroring after review.

The canonical future command remains unexecuted and requires collector approval plus a separate controller grant:

```bash
node artifacts/ui-parity-legend-capture-redirect-guard/prepare-run.mjs
LEGEND_HEAVY_GRANTED=controller-granted bash artifacts/ui-parity-legend-capture-redirect-guard/supervise.sh /mnt/d/Source/QOpenBB/artifacts/ui-parity-legend-capture-redirect-guard/attempt-<printed-id>
```

Use the exact printed path and a hidden WSL helper. Existing admission hypotheses, cleanup reserve and hard deadlines still apply. Failure grants no alternate topology, redirect exception or automatic retry.
