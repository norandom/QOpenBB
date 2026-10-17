# Preserve the unequal failure pair before accepting the collector

VERDICT: REJECTED for collector-source acceptance. One important correction is required: exhausted DOM observation currently duplicates the final sample and discards its preceding unequal sample. The stable path, family-specific midpoint calculation and bounded keyboard retention otherwise pass this offline review. The exact 31-file proposal allowlist plus its separate metadata are safe to publish as a rejected proposal accompanied by this review. Publication does not grant runtime execution.

This independent review is dated 2026-10-17 and covers the frozen [plan](../ui-parity-tooltip-segment-keyboard/plan.md), SHA-256 `6e53998013eaf92fd3041143a5ed73d3fdfd55a27ce1840cb1d0146e3d6ba7c7`. [Verification](verification.json) pins the source manifest and publication allowlist. The review read the [geometry diagnosis](../ui-parity-tooltip-geometry-diagnosis/report.md), its [independent review](../ui-parity-tooltip-geometry-review/review.md), the exact diff and all changed source. The twelve baseline files match the executed harness. English is the owning specification language.

## R01: exhausted observation does not preserve the actual final pair

**Important; blocks collector acceptance.** In [collector.mjs](../ui-parity-tooltip-segment-keyboard/harness/collector.mjs), lines 44-45, each unsuccessful iteration assigns `prior=last`. The exhaustion return then constructs `[prior,last]`. Both entries reference the same final object, although the actual penultimate sample can differ. This behavior is inherited, but the new plan explicitly promises both actual pair members. The new T06 settlement projector retains the duplicated members under an unresolved status. It does not reconstruct the missing sample.

The independent fault test alternates two raw DOM samples whose hidden tooltip HTML differs and whose compact projections are identical. The observed run reads 19 samples before its existing deadline, returns `tooltip-observation-unresolved`, and exposes the same final object twice. The actual final two inputs are unequal. This is not false stable acceptance: the status correctly remains unresolved. It is loss and misrepresentation of failure evidence. A separate three-sample sequence A/B/B correctly becomes stable only on B/B, proving that the full-DOM equality path itself is sound.

Smallest correction in a new source revision: retain the previous actual sample independently of the comparison variable. For example, initialize `previous=null`; immediately before the existing `prior=last`, assign `previous=prior`; return `previous ? [previous,last] : last ? [last] : []` on exhaustion. Keep the successful `[prior,last]` return unchanged. Do not invent a second sample when only one was read. Add offline tests for alternating samples at sample exhaustion, deadline exhaustion, and one-sample exhaustion. Preserve counts, timing, inspection order and all existing caps. Regenerate the diff, manifests and offline receipt, then obtain independent rereview. Do not edit this frozen proposal.

## Mechanical evidence and boundaries

| Check | Result |
| --- | --- |
| Exact proposal verifier | Exit 0; 108 checks, 24 pointer probes, 27 historical Tabs, 41,342-byte historical reprojection. |
| Exact freeze checker | Exit 0; 89 hash/byte checks. |
| Independent [audit](audit.mjs) | Exit 0; 328 checks, including the successful R01 counterexample. Passing this audit means the rejection evidence reproduced, not that the collector is approved. |
| Exact diff and provenance | All four sections reconstruct the proposed source from baseline; changes are limited to collector, journey, IO and the new retention module. Twelve executed baseline files match byte-for-byte. |
| Frozen package preservation | All 31 content files and publication metadata retain their original hashes. |
| Placeholder and private-material checks | No TBD/TODO/FIXME/HACK/XXX markers in the proposal. All selected files are bounded proposal-owned text; no concrete private-key or common token-prefix patterns were found. Runtime credential filenames in source are references, not captured credentials. |
| Boundary and RED evidence | Source/offline research only. Production RED evidence and application suites are not applicable. No Git, browser, container, build, installation, network request or runtime attempt occurred. |

The local kiro-review protocol was applied within the controller's explicit no-Git, offline boundary. Documentation, testing, delegation and complexity steering were read. Core product/tech/structure steering is absent, as recorded in the proposal. This review writes only its new owned directory.

The exact verifier normally writes its receipt and a temporary IO directory. The review-owned [preload](read-only-verifier.mjs) suppressed the receipt write only after exact-byte equality and redirected temporary IO into the review directory. It rejects other mutations. Its first attempt failed before verifier execution because the wrapper did not handle Node URL paths; that wrapper defect was corrected, and the exact commands then passed. An initial independent unreachable-path test assumed all 72 Tabs fit; the real reservation stopped earlier. The assertion was corrected to test the stated conditional-capacity contract. Neither event changed proposal bytes or launched a runtime.

Reproduce the exact verifier with the preload, preserving any existing `NODE_OPTIONS`, then run the independent audit:

```powershell
$previousNodeOptions=$env:NODE_OPTIONS
try {
  $env:NODE_OPTIONS='--import ./artifacts/ui-parity-tooltip-segment-keyboard-review/read-only-verifier.mjs'
  node artifacts/ui-parity-tooltip-segment-keyboard/verify.mjs
} finally { $env:NODE_OPTIONS=$previousNodeOptions }
node artifacts/ui-parity-tooltip-segment-keyboard/freeze-check.mjs
node artifacts/ui-parity-tooltip-segment-keyboard-review/audit.mjs
```

The audit uses actual source functions with synthetic pages and extracted journey functions in a VM. It exercises no browser APIs against a browser. Exact elapsed sample count may vary with the unchanged observation deadline; the unequal-input/duplicated-output counterexample does not depend on that count.

## Supported source contracts

Only `stackedColumn` uses the retained finite midpoint. Missing, nonnumeric and nonfinite x/y stop; other geometry guards remain. Grouped centers and line points retain their original formulas. T08.p52 moves 28.275 CSS pixels vertically. T05.p17 has zero delta and remains unexplained. The intended wrapper/ordinal/series identity does not establish actual picked identity, and neither T04 omission nor missing-value/tied-value semantics is accepted by this review.

For stable T06 observations, raw full-DOM equality precedes retention projection. The optional inspector checks every sample first; the projector independently rejects an unequal claimed stable pair. Active-element and live-status fields survive projection. Visible tooltip heading, rows, compact texts and pagination survive; absent/hidden content becomes explicit hidden visibility. Baseline changes stop without overwriting the retained baseline. Both additional swapchain-change and escaped-character byte tests pass.

The prospective check occurs before the Tab/arrow probe increment and again inside input before action counters, started receipts or emitted input. The exact boundary is accepted and one extra byte is rejected with counters and persisted receipts unchanged. The independent long traversal stops within the shared limits without an extra Tab; the three reached branches retain one Tab plus seven conditional keys each. This supports conditional paths, not a promise that 72 Tabs fit.

The frozen unreachable simulation retains Single 24 Tabs, Multiple 24 and Compact 22, with no arrow keys. It stops `not-run-budget` while Compact is still `seeking`: 70 emitted Tabs, six synthetic setup inputs, 76 emitted inputs/actions, and global probe count 94 including the 24 initial pointer probes. The current case is 82,395 bytes; adding the 32,768-byte reservation gives 115,163, which exceeds the unchanged 115,072-byte guard by 91 bytes. No 71st Tab or 95th probe is emitted. The VM's setup models only Mode/Escape and Escape popup per mode, and repeats one retained DOM sample; it does not reproduce all real control actions. These precise numbers demonstrate a permitted early stop, not runtime capacity. Even this smaller setup does not close all 72 Tabs, so a corrected collector must not be presented as complete keyboard coverage.

The 32,768-byte reservation exceeds `14,336 + 6,144 + 2,048 + 2*1,024 + 2,048 = 26,624` bytes for invocation, ledger, baseline, two control receipts and scaffold. Mode setup actions each re-enter the reservation; Series expansion has two bounded receipts. Final events/elapsed data is checked against 16,000 bytes before assignment. Case, invocation, baseline and ledger writer overflows all preserve the exact preceding file bytes. After-input projection overflow correctly records an emitted action and a bounded failed receipt; where serialization cannot retain that receipt, the already persisted started prefix remains the truthful lower bound. These source checks do not establish filesystem crash atomicity.

The fixture, eight cases, original source/image, 396 actions, 96 probes, 48 screenshots and all case/lifecycle/settlement deadlines are byte-identical in the contract. The new reservation is conservative and may stop sooner. No retry, larger cap or additional input is justified.

## Publication and runtime prerequisites

The [proposal allowlist](../ui-parity-tooltip-segment-keyboard/publication-allowlist.json) contains exactly 31 content files with matching sourcePath/hash/bytes; its metadata is copied separately without a self-hash. Plan links resolve at source. Historical case JSON and installed chart dependencies remain referenced local prerequisites rather than copied inputs. The controller must verify the destination mirror's hashes and links after synchronization, including the separate allowlist metadata. The [review allowlist](publication-allowlist.json) contains only this report, the independent audit, preload and receipt.

**Runtime remains blocked independently of R01.** The [Legend review's B01](../ui-parity-legend-collector-review/review.md) traffic-denial problem is inherited: default backend networking, any-origin specialized routes, redirect-capable fetches, page-scoped routing and default service workers do not prove the required denial boundary. Inherited lifecycle proof also remains open. The tooltip's recorded PID/start tick does not prove descendant-process absence, and helper/partial cleanup paths need their own review. Separate Legend B01-B04 remediation is neither borrowed nor waived by this review. A corrected source proposal still requires those prerequisites and a separate exact-source controller grant; this review grants none.

Research artifacts are excluded from production complexity caps. Future maintained adoption still requires the executable checker/inventory foundation, 400 physical lines per file, 300 logical units per file, 50 logical units per function and the final shared-module audit.
