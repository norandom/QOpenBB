# Correct four collector gaps before a runtime grant

The frozen Legend collector is not approved for runtime. Four source defects remain in traffic denial, BBox diagnostics, browser cleanup evidence and final event accounting. Correct them in a new source revision, regenerate its offline receipts/freeze, and obtain an independent source review before considering one separately granted attempt. This review grants no runtime and permits no automatic retry.

Reviewed on 2026-10-17 against the [accepted plan](../ui-parity-legend-plan-revised/plan.md) and [plan revision review](../ui-parity-legend-plan-revision-review/review.md). The collector manifest SHA256 is `9c6400819ba8d711829ba6abcc1c8b6ace2da1cd554ca01db7ea2627cb9ae1b3`; its source manifest SHA256 is `f8c4ba54c233a97fbb3a7ab5ffc5331873ff1e49532735a1e403a9b76b2e2bf6`. All recorded source hashes and byte lengths match, and the review left those files unchanged.

## Blocking findings and smallest corrections

### B01: the accepted traffic-denial boundary is not enforced

[start.mjs](../ui-parity-legend-capture/harness/start.mjs) launches Docker with its default network and no egress restriction. Browser routing does not constrain requests made by the backend. The handoff acknowledges this limitation, but the accepted plan requires external/provider denial; an expectation that the synthetic journey will not invoke a provider does not meet that requirement.

The browser rule also has a separate gap. The later sync and synthetic handlers in [journey.mjs](../ui-parity-legend-capture/harness/journey.mjs), lines 95-99, match any origin and contain no origin assertion. The sync handler calls `route.fetch()`. The offline callback counterexample supplies an external URL and observes one mock fetch and two mock fulfillments without an abort. No network was contacted in this test. A fresh context also leaves service workers at their default setting; the source does not establish a context-wide denial boundary.

Smallest correction: deny unapproved origin requests inside every specialized handler, apply the denial to the owned context, and block service workers for this finite run. Separately provide an owned backend network boundary that denies outbound/provider access while preserving the required loopback publication. An internal network or equivalent must have explicit ownership, cleanup and port-viability reasoning; its availability must not be assumed from this review. Stop before admission if isolation cannot be established. Do not amend the accepted plan to waive denial.

### B02: invalid BBox brackets disappear after subsequent samples

[settlement.mjs](../ui-parity-legend-capture/harness/settlement.mjs), lines 6-20, increments `invalidCount` but retains only the accepted pair or the final sample. An invalid sample followed by two equal valid samples returns no changed operand records. On failure, a later active sample similarly replaces the invalid sample in `diagnostic.last`.

Two offline counterexamples inject a change into one of the 14 named operands. Both reproduce loss of that finite pair; the recovery result still reports `invalidCount: 1`. This violates the accepted requirement to retain the changed bracket as a bounded diagnostic. It does not invalidate the seven-call cardinality, which is correct.

Smallest correction: retain the latest invalid 14-pair bracket, its sample index/time and invalid count in both success and failure receipts, explicitly labelling any earlier invalid samples omitted by the bounded retention rule. Keep the existing ten-sample/six-second deadline and observation-byte limit. Add offline assertions that recovery and final failure preserve this diagnostic without additional getters.

### B03: transport disconnection is treated as proof of browser-process absence

[journey.mjs](../ui-parity-legend-capture/harness/journey.mjs), lines 122-138, launches an owned browser but records no browser process identifier or independently verifiable process ownership. Its receipt derives `browserClosed` from `!browser.isConnected()` and `contextClosed` from page closure. [finalize.mjs](../ui-parity-legend-capture/harness/finalize.mjs), lines 5-7, accepts these booleans as cleanup verification. [cleanup.mjs](../ui-parity-legend-capture/harness/cleanup.mjs) verifies container/state removal only. The recorded `ownedProcessId` belongs to startup, not Chromium.

Connection/page state alone cannot prove that the owned browser processes have exited. A disconnect can therefore satisfy the receipt without the process-absence evidence required by the plan; a hard interruption has no recorded browser identity for targeted fallback cleanup.

Smallest correction: record an ownership-scoped browser PID/process group and verify its absence after close. Add bounded fallback termination of only that recorded ownership scope, and make final status require the absence receipt. A missing identity, surviving process or failed check remains `cleanup-unverified`. Keep cleanup inside the existing 120-second reserve and preserve the 2,220-second hard deadline.

### B04: final event draining can hide an overflow and mislink late events

[projection.mjs](../ui-parity-legend-capture/harness/projection.mjs) records event overflow in `store.overflow`; `snapshot()` checks it only at entry. In [journey.mjs](../ui-parity-legend-capture/harness/journey.mjs), `collectEvents()` reads only the event array. An overflow after the final boundary snapshot is consequently absent from the final drain and can coexist with an `observed` summary. This is a source ordering counterexample; the existing event-bound test exercises a direct listener call followed by inspection and does not test final draining.

There is a related linkage gap: `eventLast` uses the latest drain count, while the after-observation has its earlier `eventSequence`. Events arriving during raster capture can be attached to an observation that predates them without a mismatch flag.

Smallest correction: drain a single bounded `{events, overflow}` envelope, persist any overflow reason and fail the attempt before a successful summary/final status. Require the final action interval to end at its recorded settled observation sequence; if later events arrive, record the mismatch and stop as unresolved or obtain a fresh bounded settlement within the existing budget. Preserve already written event prefixes. Add offline final-drain and late-event tests; do not extend event or time caps.

## Contracts supported by source inspection

The finite scene implementation follows the revised contract: two source-ordered live series, 14 distinct named scene identities, exact parent checks before conversion, seven direct BBox calls, and 14 presence-aware operands immediately before and after those calls. There is no bar-node traversal. Geometry avoids adding marker translation twice or adding seriesRect to legend coordinates. Configuration stroke values remain distinct from rendered bar-edge evidence. Actual visibility, property visibility and content-group visibility remain separately recorded.

The unchanged fixture is byte-identical to the accepted captions fixture. Guards check four quarters, all eight amounts, selected column order, source names/keys, two live identities and visible content groups. Raw absent/undefined/null/value states remain distinct. Legend controls use scoped exact names, typed numeric inputs, exact popup ownership and separate fill/Tab/range actions. Weight is read only, Color stays closed and no Shape selector is invented. Strict runtime selector/Group/canvas uncertainties may fail closed; they are not permission to broaden collection.

The eight-case action program retains restoration records and L06's unavailable-layout outcome. Rasters retain both identity-linked series and a fixed plot region. Visual effects and off/on retention still require review of actual captures; `observed` is not a UI-parity verdict. One-series behavior, other themes/families, item interaction, persistence and production acceptance remain unverified.

The incremental writer prospectively checks public retained bytes, counts and JSON limits, accounts for overwrites, preserves ordered event prefixes and reconciles its tracked files. The watchdog status is written after final reconciliation, so a future publication inventory must rescan completed actual files rather than treating the inner inventory as the complete attempt inventory. The 160 actions, 56 mutations, 360 observations, 80 PNGs, per-case/journey deadlines and outer 2,100/2,220-second bounds are present in source. No timing success or cleanup success has been executed here. B03 and B04 prevent accepting those source bounds as an end-to-end lifecycle receipt.

## Verification and publication

[verification.json](verification.json) records a fresh replay of all 16 supplied offline tests, 30 JavaScript syntax checks, fixture equality, source hashes and three additional route/settlement counterexamples. The replay changed only import/fixture resolution and redirected the test's final report to memory, avoiding writes to the frozen collector. [review-checks.mjs](review-checks.mjs) reproduces these checks. Command: `node artifacts/ui-parity-legend-collector-review/review-checks.mjs`, Node `v24.20.0`, exit code 0. Counterexample reproduction is successful verification of defects, not collector acceptance.

No browser, container, original/candidate application, image build, dependency installation or runtime attempt ran. This review and its offline script are research exclusions. Future maintained production work retains the executable inventory/checker foundation, 400 physical lines/file, 300 logical units/file, 50/function and independent review.

[publication-allowlist.json](publication-allowlist.json) contains only this review, its verification receipt and reproducible offline script, with exact sourcePath/SHA256/bytes. No raw runtime state or credentials are included. The controller owns publication and the next source revision; the frozen collector and other lanes remain untouched.
