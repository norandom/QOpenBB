# Stacked Line candidate progress review

2026-10-26. **APPROVED: the three bounded journeys in amount-3, normalized-1 and recovery-2, including the final browser test for selective commit. SL3 remains open for the gaps below.** Recovery-2 resolves the earlier test failure without a production change. Recovery-1 remains a retained failed run, not a product defect or a passing journey.

Both runs qualify the same packaged Workspace source `94d09d1380c787a27c7c369f54213dd625275859`, image `sha256:580475f5f7cde1948508e31bcba59fb70fbcf6d8fef9ac42454f584d38ba7afb`, running on the owned loopback origin with only the disposable data mount. Read qualified identity, frozen test/evidence, logs, source-integrity results and recorded observations; inspected normalized light/dark screenshots, its export and the recovery capture. No reviewer browser/heavy checks or production changes ran.

## Normalized financial journey

`normalized-1` passes one case in approximately 1.1 minutes, exit 0. All four retained AAPL FY2025 quarters are checked against source hashes, raw reported-USD observations and independent cumulative percentage positions. Q1 starts at 53.1174577635% and ends at 100%; raw tooltip values remain USD 66.03 B cost of revenue and USD 58.28 B gross profit. This verifies cumulative percentages rather than replacing observations with percentages.

Hiding Gross Profit moves the surviving cost line to 100% and removes the hidden raw value from tooltip output. Restoring, refresh and ordinary-Line/back transitions recover the original geometry. Miniature retention and drag/restore assertions pass. Reordering makes Q1's first endpoint 46.8825422365%; fresh-context reopen preserves the model and rechecks reordered endpoint paint and raw values. Both initial and reopened diagnostic arrays are empty.

The exported PNG has the expected saved title, reordered legend, markers and cumulative percentage lines on visual inspection. Automated export checks establish download success, PNG signature and dimensions; exact content/pixel parity is still not established. The controller relayed the owner's acceptance of both amount and normalized appearances through qView decision `41cacb9c`; that visual decision does not waive the remaining behavior gates.

## Recovery-2 acceptance and corrected diagnosis

`recovery-2` passes one case in 24.0 seconds, exit 0, on the same qualified image/source. Independently inspected its log, identity, records and source-integrity results. Executed frozen test SHA-256 is `3eefc281150f239b095516cc12a87e440e001e7d377b91af0a1021e807ef6e8b`; the final formatted source is qualified separately below.

After final-series removal, native Table return is asserted. After one chart-view reentry, the records show one canvas and `editorOpenOnReentry:true`; the saved model still has category-only columns. The existing caller/session fallback therefore recovers without resetting saved ranges. The old helper unconditionally toggled Chart settings, closing this already-open editor and then waiting for it to appear. The corrected test asserts the actual open editor directly instead of clicking that toggle a second time. There is no demonstrated host reentry defect and no range-reset production repair is warranted.

The final case repeats every initial signed/missing/zero endpoint and raw-tooltip check after reentry. Initial and recovered records match for Mixed `[100,-100/3,0]`, Missing `[66.6667,100]`, positive-denominator raw zero and all-zero no-hit/no-paint. The exact normalized token remains saved, and the final clean-diagnostics assertion completes with empty error/failure/console/request arrays. This accepts actual post-empty recovery, not merely transient canvas presence.

## Historical recovery-1 failure (test cause resolved)

`recovery-1` exits 1. Before failure, its completed initial probes establish:

- Mixed raw `[60,-80,20]` has paint at normalized `[100,-100/3,0]`, with all three original raw tooltip values.
- Missing first contribution remains absent from tooltip content; later raw 20 and 10 produce the expected 66.6667% and 100% endpoints.
- A real raw zero with positive denominator is retained in the Positive tooltip. The all-zero category has no colored paint at the probed zero endpoint and no visible tooltip hit.
- Removing all selected series returns to Table, closes the editor/canvas and records `noSeriesReturnedToTable:true`.

The test then fails while opening Chart settings: the expected `Chart editor` does not become visible within 30 seconds, at frozen test line 253 via `editor.ts:13`. No recovered observation record was written. At that review the cause was unresolved; recovery-2 now demonstrates the extra toggle described above. Any earlier characterization of this as an actual host reentry failure is superseded. Recovery-1's final clean-diagnostics assertion was not reached; keep its raw failure intact.

## Remaining SL3 boundaries

The accepted three journeys do not establish signed unnormalized browser geometry, duplicate/number/time original comparison, aggregation/category switching, saved-false missing topology or exact export pixel equivalence. Keep the earlier setup and recovery failures as historical evidence, with their resolved test causes explicit.

One source diagnostic gap also remains: J preserves the typed legend-overflow code/message through its callback, but `useApplicationChartSession.onError` currently replaces interaction errors with generic `Chart rendering failed`. Initial translator diagnostics are specific; the user-visible legend-overflow explanation is not established by the source callback test. Do not claim that financial diagnosis reaches the UI until this boundary is addressed and verified. SL3 and publication remain open; no new production repair or complete-feature claim is approved here.

Only this review file was written.

## Final test-format qualification

Final test SHA-256 is `2fd0536e76c2106d10d5551e68c343cb49a80b53347c6d95ec55c28a6f7ddf87`. Compared it with recovery-2's frozen source. Changes are formatting/import ordering, splitting multi-declaration statements, and Biome's equivalent `-Infinity` to `Number.NEGATIVE_INFINITY` replacement. Independently transpiled both with TypeScript 6.0.3 and compared normalized JavaScript ASTs, preserving operation order/operators and literal contents while normalizing parentheses, declaration splitting and that infinity spelling: equality passes, exit 0. No behavioral difference was found. `browser/lint-final.log` reports one checked file and no fixes. No browser rerun is warranted for these equivalent edits; approval for selective test commit remains valid. This was a small parser comparison, not a suite or application execution.
