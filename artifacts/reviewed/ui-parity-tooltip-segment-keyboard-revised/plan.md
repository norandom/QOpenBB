# Rereview the exhausted-observation pair correction

This source-only revision dated 2026-10-17 corrects only R01 from the frozen [independent review](../ui-parity-tooltip-segment-keyboard-review/review.md). It is ready for independent rereview, not accepted collector source or a runtime grant. The [original proposal](../ui-parity-tooltip-segment-keyboard/plan.md), its review and historical evidence remain unchanged. Traffic-denial and lifecycle prerequisites still block runtime independently of R01.

## Narrow source change

The new [baseline](baseline) is an immutable byte copy of the rejected proposal's actual 13-file harness. [Executed baseline](executed-baseline) separately preserves its 12-file original executed harness. The [proposed harness](harness) differs from the rejected proposal only in `collector.mjs`'s `observe()` failure path. The [exact diff](collector.diff) and [source hashes](source-hashes.json) identify every line and source byte. No network, lifecycle, fixture, journey, retention or IO change is borrowed.

The observer keeps `previous` independently of the `prior` comparison sample. After each unequal sample, it assigns `previous=prior` before `prior=last`. On exhaustion it returns the actual final two samples, one sample when only one was read, or an empty array if none was read. It retains the existing unresolved status, count and elapsed time. The stable return still requires full raw DOM equality and retains `[prior,last]`; inspection still precedes equality on every sample. No compact projection is used as a substitute for full DOM equality.

The T06 settlement projector remains byte-identical. It now receives the actual unresolved raw pair, then retains each actual compact sample separately. Two projected failure samples can be equal when omitted hidden HTML differs; their unresolved status must remain unresolved. A one-sample failure remains one sample. The previous proposal's failure return duplicated its final sample; the new offline test reproduces that defect in the immutable baseline and rejects the same behavior in this revision.

T08's stacked finite midpoint proposal, grouped/line formulas and all exact scene-chain, identity, transform, settlement and bounds guards remain unchanged. T05 remains unexplained, with zero midpoint delta. This revision adds no diagnosis, picked-state inspection or arbitrary scene traversal. It makes no application fix, actual picked-identity or UI-parity claim.

## Unchanged bounds and the explicit coverage gap

The byte-identical contract retains the synthetic fixture, original source/image, eight cases, 396 total actions, 96 probes, 48 PNGs, 900-second total lifecycle and all startup/case/settlement deadlines. The 131,072-byte case ceiling, 115,072-byte guard, 32,768-byte prospective T06 reservation, finite projection caps and 16,000-byte tail cap are unchanged. There is no additional retry or input.

The deterministic mock still stops at Single 24 Tabs, Multiple 24 and Compact 22: 70 emitted Tabs, six synthetic setup inputs, 76 actions/inputs and 94 global probes including 24 pointer probes. Compact remains `seeking`, with no arrows. Its 82,395-byte current case plus the unchanged 32,768-byte reservation is 115,163 bytes, exceeding the 115,072-byte guard by 91. No 71st Tab or 95th probe is emitted. The mock models only Mode/Escape and Escape popup setup and repeats one retained DOM sample; it is not a browser capacity prediction. It demonstrates a permitted stop and leaves full 72-Tab coverage open.

The original proposal's [runtime prerequisites](../ui-parity-tooltip-segment-keyboard/plan.md#unchanged-runtime-bounds-and-inherited-limitations) and [review findings](../ui-parity-tooltip-segment-keyboard-review/review.md#publication-and-runtime-prerequisites) continue to apply. Backend networking and specialized browser routes do not enforce the required traffic-denial contract; owned descendant-process absence and partial lifecycle paths remain unverified. No network or lifecycle rewrite is included. Correcting R01 does not waive those independent prerequisites or make this source runtime-ready.

## Fresh offline verification

From the repository root:

```powershell
node artifacts/ui-parity-tooltip-segment-keyboard-revised/verify.mjs
node artifacts/ui-parity-tooltip-segment-keyboard-revised/freeze-check.mjs
```

The [verifier](verify.mjs) and [R01 fault tests](r01-faults.mjs) run source/data-only Node mocks and syntax checks. The [receipt](verification.json) records 177 passing checks, exit 0, all 24 historical pointer probes and 27 historical Tabs. Historical reprojection remains 41,342 bytes with the existing ledger untouched. This is evidence for the source rules, not runtime picking or keyboard reachability.

The new controlled-clock cases execute the actual observer source without changing its limits: alternating hidden raw HTML exhausts all 20 samples; another alternating sequence crosses the unchanged deadline after three samples; a single sample crosses the deadline and retains only itself. Each test checks the actual final input sequence, unresolved status, count and inspection order. A/B/B still becomes stable only on full B/B equality. The actual extracted T06 journey path retains the unresolved projected pair and stops after the first Tab without extra input. The deterministic 70-Tab mock confirms the unchanged coverage gap and exact 91-byte excess. The previous 108 source/counter/serialization checks still pass.

The freeze checker reads only named sources and confirms sourcePath/SHA-256/byte length for every source input, output and publication entry. The verifier writes only this new package's deterministic receipt and its transient IO fault directory; it does not execute or write the frozen prior proposal/review. All writes remain under `artifacts/ui-parity-tooltip-segment-keyboard-revised/`. No Git, browser, container, application, provider request, image build or dependency installation ran.

## Independent rereview and publication boundary

The reviewer must independently confirm the three-line observer correction, actual unequal failure pairs at sample/deadline exhaustion, one-sample cardinality, unchanged full-DOM stable path and inspector order, truthful T06 projection, unchanged caps/reservation, the 70-Tab gap and frozen original preservation. Rereview acceptance is not supplied by this implementer's package. The controller owns review, publication and any future grant.

The [publication allowlist](publication-allowlist.json) uses the publisher's sourcePath/hash/bytes schema and selects only the revised synthetic source, baselines, fixture, plan, diff, hashes and offline checks. Its metadata is copied separately without a self-hash. Publication can preserve a source proposal and its eventual review while runtime prerequisites remain open; it does not accept or waive them. Credentials, runtime/private state, logs, browser profiles, dependency caches, image archives and historical PNGs are excluded. Verify destination hashes and links after any approved synchronization.

If a future independent review resolves all inherited runtime prerequisites and the controller grants this exact source, create a fresh empty attempt root and reconsider this proposed WSL command from `/mnt/d/Source/QOpenBB`:

```bash
TOOLTIP_HEAVY_GRANTED=yes bash artifacts/ui-parity-tooltip-segment-keyboard-revised/harness/run.sh /mnt/d/Source/QOpenBB/artifacts/ui-parity-tooltip-segment-keyboard-revised/capture/attempt-20261017-tooltip-segment-keyboard-revised-a1
```

This is not permission to run. The environment flag is a source guard, not review or grant evidence. No automatic run, fallback or retry follows from this revision.

The owning specification language is English. Previously read testing, delegation, documentation and complexity steering remains applicable and unchanged; core product/tech/structure files are absent. `kiro-verify-completion` limits the verified claim to fresh source/offline evidence, with independent rereview pending. This research package is excluded from production size caps. Future maintained adoption still requires the executable inventory/checker foundation, 400 physical lines/file, 300 logical units/file, 50 logical units/function and a final shared-module audit. The narrow correction adds one state variable and preserves the existing component responsibilities.
