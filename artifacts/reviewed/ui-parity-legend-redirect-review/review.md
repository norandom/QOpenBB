# Accept the final collector source for one separately granted attempt

The final redirect guard closes the remaining B01 finding. B02-B04 remain closed at source level because their reviewed implementations are unchanged. This exact frozen collector is eligible for one bounded original-runtime attempt if the controller separately grants it. This review does not grant execution, establish UI parity or accept a production/spec task. No runtime has run.

Reviewed on 2026-10-17 against the [remaining B01 finding](../ui-parity-legend-collector-revision-review/review.md) and unchanged [eight-case plan](../ui-parity-legend-plan-revised/plan.md). Inputs include the final [plan](../ui-parity-legend-capture-redirect-guard/plan.md), [handoff](../ui-parity-legend-capture-redirect-guard/handoff.md), [source diff](../ui-parity-legend-capture-redirect-guard/source-diff.patch) and [provenance](../ui-parity-legend-capture-redirect-guard/provenance.json).

| Frozen input | SHA256 |
| --- | --- |
| Harness manifest | `9ba3ebf7976b2fc8f0a027fd2823c93365cba5e297de5d988311da7c405f4531` |
| Source manifest | `5b0674b7aae4e0a7c9e26fb26b7009def4e42fb73ed67865a31d71b34c502704` |
| Proposed 57-entry source allowlist | `5eca0931671e3543291e42a66b4000a5a0786414169c4747e69a6c61b1874841` |

## The remaining redirect counterexample is closed

[routes.mjs](../ui-parity-legend-capture-redirect-guard/harness/routes.mjs) has no `route.continue()` path. Every real HTTP(S) passthrough, including generic GET/POST and sync non-GET, performs one fetch with `maxRedirects: 0`, `maxRetries: 0` and `timeout: 4000`. Initial protocol/origin checks precede fetching or synthetic fulfillment. Every 3xx response, any case-insensitive Location header, invalid response identity or foreign response origin aborts before fulfillment. A fetch failure uses a fixed bounded diagnostic rather than retaining the exception's potentially sensitive URL/body details.

An allowed first URL therefore cannot hand a redirect to Chromium for automatic continuation. The earlier source counterexample is eliminated without relying on Playwright to route later hops. An original same-origin redirect is rejected too: it remains an explicit unresolved admission/case outcome, with no redirect emulation, navigation repair or new attempt.

Ordinary generic and sync non-GET responses pass their original response object to `fulfill`, preserving response status, headers and body. Fetch options omit method and postData overrides. The existing sync GET dashboard projection and synthetic financial endpoint remain the only fixture substitutions; no new application data or UI response is synthesized. Synthetic tests confirm these call contracts, not actual login or rendering compatibility.

## Prior closures and bounded scope remain intact

All active runtime files other than routes.mjs match the previous reviewed revision, allowing only the necessary owned-directory spelling change in start.mjs. Frozen baseline files match that prior revision exactly. The B02 invalid-bracket receipts, B03 recorded browser-parent PID/start-ticks verification and bounded fallback, B04 atomic event/overflow drain and final status guards are unchanged. This preserves their source-level closure, including the limited process-identity scope rather than a universal descendant-absence claim.

The owned internal network, exact attachment/loopback inspection, service-worker blocking, cleanup ownership and deadline mechanisms are unchanged. Internal bridge/port viability, Linux process inspection and cleanup, original controls/canvas/scene identities and visible Legend effects remain future admission or interpretation questions. The disclosed internal-network host-gateway residual remains as recorded in the prior review; this revision adds no relay/provider path.

The unchanged contract permits one original instance, one isolated headless browser/context and one worker, L01-L08, 160 chart actions, 56 mutations, 256 events, 360 observations, 80 PNGs and the existing byte limits. Startup remains 180 seconds, each case 240 seconds, journey 1,920 seconds, stop-input 2,100 seconds and hard attempt 2,220 seconds with at most 120 seconds cleanup. Failure does not authorize an alternate topology, redirect exception, expanded collector or automatic retry.

## Fresh evidence and publication verdict

[verification.json](verification.json) records a fresh replay of all 30 offline tests, 42 JavaScript syntax checks, fixture equality, prior inventory/provenance hashes and final frozen-file preservation. Independent additional checks reject every status from 300 through 399 across generic GET, generic POST and sync PUT: 300 cases, each with exactly one mock fetch, one abort and no fulfillment. A fetch-error check confirms a fixed diagnostic without the injected sensitive sentinel. No actual network request was made by these tests.

Command: `node artifacts/ui-parity-legend-redirect-review/review-checks.mjs`, Node `v24.20.0`, exit code 0. The [review script](review-checks.mjs) redirects the supplied tests' final report to memory and resolves imports/fixture reads to frozen originals; it does not rewrite the collector or its receipts. No freeze command, application, browser, container, topology test, build or installation ran.

The [reviewed collector allowlist](reviewed-collector-publication-allowlist.json) is an exact copy of the verified 57-entry proposed allowlist and is approved for source-only publication. Every selected path, hash and byte length matches. It contains source, synthetic fixtures, tests, offline receipts, provenance and frozen comparison files. Source credential references generate disposable random values; no generated credentials, runtime-private state, logs, profiles, environment files, archives or dependency caches are selected. No sanitization is needed. The controller owns mirroring and final destination-byte verification. Publication conveys the source-review decision, not a runtime grant or behavioral acceptance.

These research artifacts are excluded from production complexity caps. Future maintained code still requires the executable checker/inventory foundation, 400 physical lines/file, 300 logical units/file, 50/function and independent review. The controller may now consider one separately granted attempt using this exact frozen source and its stated failure policy.
