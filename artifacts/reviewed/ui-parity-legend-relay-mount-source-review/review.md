# Accept the exact mount correction for a separate runtime decision

VERDICT: APPROVED for this frozen source revision and its exact 20-file publication selection. No blocking finding was identified. The correction implements the [approved proposal](../ui-parity-legend-relay-mount-correction/proposal.md) and [proposal review](../ui-parity-legend-relay-mount-correction-review/review.md): exactly three runtime bind tuples and one separately configured `/data` tmpfs entry. A new topology probe remains a separate controller grant; no probe or full UI capacity is approved by this source review alone.

Reviewed on 2026-10-17 against [handoff.md](../ui-parity-legend-relay-mount-source/handoff.md), harness manifest SHA-256 `b03ba2f0939a637d02937326caa24b1287514d6463efd369fa67361c53e99831`, source manifest `64eecc7260f1c9a269cffe919f73405fda94d645b9667705072402a0ea4019c2`, and publication allowlist `514eef21dcad5d3cc2a1956eeee363abf33a3e6d86a39af8a7d9b0d5b52ae79e`. The [failed-attempt review](../ui-parity-legend-relay-attempt-review/review.md) is accepted separately; its unresolved result remains unchanged.

## The correction preserves the intended boundary

The helper requires an array of exactly three entries and a matching destination, private source identity, type `bind` and RW flag for each of the three distinct expected destinations. That excludes duplicates, missing binds, extras and the former fourth tmpfs entry. Array order is irrelevant. The configured tmpfs check requires a nonnull nonarray object, one own enumerable key, own `/data`, zero unexpected keys and the unchanged `rw,nosuid,nodev,size=1048576` string. There is no normalization, alternate layout, larger size or fallback.

Projection adds only the approved tmpfs shape scalars. Unexpected keys and values are not copied. Existing selected parent and `/data` handling remains bounded; source paths and ownership tokens remain comparisons. Optional access handles null/scalar mount entries without throwing before persistence. A string-type guard prevents malformed destination objects from invoking property-key coercion. The actual observation callback saves the projected receipt before a rejecting admission decision.

The independent audit admitted all six bind permutations, rejected all twelve individual tuple-field changes and a duplicate, and exercised seven malformed entries plus an array-like parent. A destination object with a throwing coercion hook was never invoked. Further checks rejected inherited `/data`, an extra own `__proto__` key carrying a private sentinel, missing/scalar tmpfs parents and the old fourth-entry layout. A null-prototype object with only the exact own `/data` key admitted. Saved receipts excluded private source/token/sentinel values and distinguished missing from scalar parents. These 33 focused cases use actual projection/observation/admission functions and no runtime.

## RED evidence, regression checks and limits

The actual baseline command exits 1 with `valid-three-bind-layout-rejected`; the corrected source passes the same valid-layout test. The canonical verifier checks this negative control rather than merely recording a claimed earlier failure. It then passes 25 inherited JavaScript groups, 11 mount groups, ten fake-socket Python methods, ten JavaScript syntax checks and two separate shell syntax checks. The mount matrix covers the required missing/extra/inherited keys, option/type/size/length drift, malformed inputs, persistence, private sentinels and unrelated guard failures.

The source diff was inspected directly. Python transport, cleanup, IO, finalization, run script, Python tests and machine contract are byte-identical to the accepted baseline. Probe, supervisor and preparation differences are only the new revision path. Container admission decisions, stats decisions, health handling and readiness code after the projection are byte-identical. Creation arguments, source identity, ownership, networking and all unrelated security conditions remain unchanged. No production refactor or broader inspect framework was added.

The same no-browser profile therefore remains: ten GET starts with three-second spacing, two-second requests within 30 seconds; four concurrent/sixteen accepted pairs, nine sockets, 4 MiB/pair, 32 MiB aggregate; and 90/60/150-second lifecycle ceilings with existing watchdog sublimits. The source-only tests do not establish a real tmpfs mount, successful HTTP origin, external-traffic guarantee or L01-L08 capacity. Historical receipts do not retroactively prove the new exact tmpfs key count.

## Verification and safe publication

The [audit](audit.mjs) verifies frozen source/input/selection bytes, unchanged scope, actual baseline failure, the complete offline matrix, the 33 independent cases, local links and bounded token/private-key/placeholder scans. The supplied freeze verifier passes 64 pinned entries and eight runtime-file checks. The deterministic [receipt](verification.json) records fresh command results. All source bytes are checked again after execution.

```powershell
node artifacts/ui-parity-legend-relay-mount-source-review/audit.mjs
```

The [reviewed source selection](reviewed-source-publication-allowlist.json) is byte-identical to the supplied 20-entry list and is approved. It contains source, synthetic tests and offline evidence, with no private attempt state, credentials or raw runtime logs. Synthetic private-value sentinels are test data. No concrete token or private-key pattern was found; the scan is bounded rather than exhaustive for every secret format. The [review selection](publication-allowlist.json) selects this completed review package. Preserve allowlists as metadata without self-hashes, verify copied bytes and retain relative evidence links during publication.

Only the new review directory was written. No mutable/private attempt input, Docker command, real socket, application, browser, preparation launcher, freeze generator, build, install, Git mutation or runtime probe was used. Offline fixtures use temporary files and injected dependencies. Research code is excluded from production size caps; future maintained adoption retains the scope inventory/checker and 400 physical lines/file, 300 logical units/file and 50/function. The controller owns runtime grants, documentation, publication and commits.
