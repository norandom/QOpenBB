# Accept R01 closure and publication while runtime stays blocked

VERDICT: APPROVED for the narrow R01 source correction and exact source publication set. No further R01 remediation is required. This is not runtime eligibility, a run grant, complete keyboard coverage, actual picked identity or UI-parity acceptance. Inherited traffic-denial and lifecycle prerequisites remain open.

This independent rereview is dated 2026-10-17. The reviewed [revised plan](../ui-parity-tooltip-segment-keyboard-revised/plan.md) has SHA-256 `2cbf5814b0faed0c7c060ad85ba980ac8abf581c14470926ea00fe3e389c149c`. The [verification receipt](verification.json) pins the source manifest, allowlist and exact diff. The prior [rejection](../ui-parity-tooltip-segment-keyboard-review/review.md) remains immutable historical evidence. Previously read kiro-review, testing, delegation, documentation and complexity guidance applies; the owning specification language is English. The review writes only this new review directory and uses no Git, browser, container, build, installation, network request or runtime attempt.

## R01 closes without changing the stable path

Only `harness/collector.mjs` differs from the rejected 13-file harness. Independent reconstruction applies exactly three substitutions to the frozen baseline and obtains the revised file byte-for-byte: initialize `previous`, save `previous=prior` before advancing `prior`, and use `previous/last` for the unresolved return. All other collector code and every other harness file are unchanged. The separate 12-file executed baseline remains pinned by the freeze manifest.

The independent [audit](audit.mjs) reproduces the original defect, then tests the revised actual observer function with controlled clocks and synthetic DOM samples. Alternating hidden HTML differs in raw DOM while its compact projection is identical. At the unchanged 20-sample cap, the revised return holds the actual penultimate and final objects, which are unequal. At deadline exhaustion after three samples, it retains the actual final two. One-sample exhaustion retains one object; zero-sample exhaustion retains none. Unresolved projected samples stay unresolved even when their compact values are equal.

The A/B/B sequence returns stable only on the third sample, with the same result and guard/read/inspect/delay order as the rejected baseline's correct stable path. Every sampled failure case preserves sample counts and inspection coverage. An injected inspector exception still propagates. No compact equality replaces raw equality, and no sample, deadline or retry limit changed. The supplied tests additionally exercise the extracted T06 journey: it retains the unresolved projected pair and stops after its first Tab without extra input.

## Fresh evidence

| Command or check | Result |
| --- | --- |
| `node artifacts/ui-parity-tooltip-segment-keyboard-revised/verify.mjs` | Exit 0, 177 checks; historical 24 pointer probes and 27 Tabs; 41,342-byte reprojection. |
| `node artifacts/ui-parity-tooltip-segment-keyboard-revised/freeze-check.mjs` | Exit 0, 151 hash/byte checks. |
| `node artifacts/ui-parity-tooltip-segment-keyboard-revision-review/audit.mjs` | Exit 0, 324 independent identity, boundary, counterexample and publication checks. |
| Original package and review preservation | All selected prior content hashes remain unchanged. |
| Placeholder/private-material checks | No TBD/TODO/FIXME/HACK/XXX markers. No concrete private-key or common token-prefix matches in the 45 selected text files. This is a bounded content check, not a universal secret-detector claim. |

The exact verifier used the review-owned [read-only preload](read-only-verifier.mjs). It suppresses the receipt write only after comparing proposed bytes with the frozen receipt, redirects temporary IO into this review's ownership and rejects other mutations. The checker itself is read-only. To reproduce the protected verifier, preserve and restore `NODE_OPTIONS`:

```powershell
$previousNodeOptions=$env:NODE_OPTIONS
try {
  $env:NODE_OPTIONS='--import ./artifacts/ui-parity-tooltip-segment-keyboard-revision-review/read-only-verifier.mjs'
  node artifacts/ui-parity-tooltip-segment-keyboard-revised/verify.mjs
} finally { $env:NODE_OPTIONS=$previousNodeOptions }
node artifacts/ui-parity-tooltip-segment-keyboard-revised/freeze-check.mjs
node artifacts/ui-parity-tooltip-segment-keyboard-revision-review/audit.mjs
```

## Unchanged limits and publication boundary

The family-specific finite midpoint change, T05 zero delta/unexplained status, fixture, eight cases, 396 actions, 96 probes, 48 screenshots and original time caps are unchanged from the prior review. Journey, IO, retention, startup and cleanup sources are byte-identical to that review's harness. Prospective byte reservation and partial-file preservation are therefore unchanged; this rereview does not reopen their previously bounded acceptance.

The fresh supplied deterministic mock still stops at Single 24, Multiple 24 and Compact 22 Tabs, with Compact `seeking` and no arrows. It emits 70 Tabs plus six synthetic setup inputs: 76 actions and 94 global probes including 24 initial pointer probes. At 82,395 bytes, adding the 32,768-byte reservation yields 115,163, exceeding the 115,072-byte guard by 91 bytes. There is no next Tab or probe. The mock omits full browser setup and repeats one retained DOM sample; these counts prove a permitted stop, not real capacity. Full 72-Tab coverage remains open. No cap widening follows from R01 closure.

The [revised allowlist](../ui-parity-tooltip-segment-keyboard-revised/publication-allowlist.json) contains exactly 45 unique proposal-owned text files. Their sourcePath/hash/bytes match actual files; they include source, synthetic fixture, immutable baselines and offline review material. The allowlist itself is separate metadata without a self-hash. Source plan links resolve. Credentials, runtime state, profiles, logs, dependencies, images and historical screenshots are absent. Publication is approved for that exact set with this review; the controller must still verify copied destination hashes and links after synchronization. The [review allowlist](publication-allowlist.json) selects this review, audit, preload and receipt, with its own separate metadata.

**Runtime prerequisites are not waived.** The prior B01 backend/browser traffic-denial gaps and inherited lifecycle proof remain unresolved. Separate Legend B01-B04 changes are not borrowed or accepted here. Any future run requires those exact-source prerequisites to pass independent review and a separate controller grant. T05, T04, missing-value semantics, tied-value ambiguity, picking and complete keyboard behavior remain outside this narrow closure.

These research artifacts are excluded from production complexity caps. Future maintained adoption still requires the executable checker/inventory foundation, 400 physical lines per file, 300 logical units per file, 50 logical units per function and final shared-module audit. Production RED evidence is not applicable to this source-only rereview.
