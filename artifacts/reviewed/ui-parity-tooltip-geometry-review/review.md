# Publish the source diagnosis with the runtime questions open

VERDICT: APPROVED for the exact source proposal and publication package identified in [verification.json](verification.json). No blocking finding was found. This review does not approve a collector change, a runtime grant, actual picked identity, a discrepancy cause, complete keyboard behavior or UI parity.

This independent review is dated 2026-10-17. The [diagnosis](../ui-parity-tooltip-geometry-diagnosis/report.md) has SHA-256 `9e689aeea647a239314bef20c38a97ab8821fe29732e55f42521255c831d5f94`. Its six frozen files, including publication metadata, are pinned in the review receipt. The owning specification language is English. The local kiro-review protocol was applied within the controller's explicit source-only scope: files were read directly, with no Git, browser, container, build, provider or private picked-state access. Behavioral RED evidence and production test suites are not applicable to this research review.

## Mechanical evidence

| Check | Result and limit |
| --- | --- |
| Exact report command | `node artifacts/ui-parity-tooltip-geometry-diagnosis/verify.mjs`, exit 0, 1,255 checks. A review-owned `NODE_OPTIONS` preload suppressed the one receipt write after confirming its requested bytes exactly equalled the frozen receipt. This was an offline execution, not a runtime test. |
| Independent audit | `node artifacts/ui-parity-tooltip-geometry-review/audit.mjs`, exit 0, 402 checks. It independently reconstructs all 24 recorded points, intended-node uniqueness, grouped deltas, T08 segment intervals, all 27 full settled keyboard pairs and the compact serialization. |
| Source and preservation | All 29 source inputs and three manifest outputs match their hashes and byte lengths. All five selected publication content files match their allowlist. All six frozen package files remain byte-identical during review. |
| Publication safety | The six frozen text files were inspected and scanned for concrete private-key/token patterns and placeholder markers; none were found. They contain synthetic retained-data calculations and source references, not dependency contents, credentials or private runtime state. This is a bounded content review, not a universal secret-detector claim. |
| Links and copying | All seven report links resolve against their intended publication sources. The publisher's inspected source separately includes each passed allowlist as metadata, which preserves the report's allowlist link without a self-hash. The controller must verify actual destination hashes and links after synchronization. |
| Maintained summary | The final two source-diagnosis paragraphs in `chart-tooltip-invocation-findings.md` preserve the coordinate-hypothesis, zero-delta and conditional-size limits. They do not claim a fix or authorize another run. |

To repeat the protected exact command in PowerShell, preserve and restore any existing `NODE_OPTIONS`:

```powershell
$priorNodeOptions=$env:NODE_OPTIONS
try {
  $env:NODE_OPTIONS='--import ./artifacts/ui-parity-tooltip-geometry-review/read-only-verifier.mjs'
  node artifacts/ui-parity-tooltip-geometry-diagnosis/verify.mjs
} finally { $env:NODE_OPTIONS=$priorNodeOptions }
node artifacts/ui-parity-tooltip-geometry-review/audit.mjs
```

The [preload](read-only-verifier.mjs) rejects an unexpected output path or any changed receipt bytes. The [audit](audit.mjs) writes only this review's verification receipt and requires the original diagnosis directory and named installed-source prerequisites. Its rerun does not update the frozen package.

## Source contract and independent arithmetic

AG Charts 12.1.1's installed distribution separates the segment `rect`, its `clipBBox` and center `midPoint` from `barRect`, which spans zero to the stack's aggregate range. Returned datum rectangle fields come from `barRect`. Shape reset carries `clipBBox`; `Rect.computeBBox()` uses it when present. The frozen projection reads datum fields and does not retain a shape bbox. These claims match the inspected source sections and do not imply that installed package bytes independently attest the recorded image.

The named content-group, managed-layer, series-root and terminal scene-root construction matches the source. Local points require the content and series-root translations plus canvas origin. Transformable bbox helpers distinguish an already transformed bbox from a supplied local bbox; the report correctly avoids applying a node transform twice. The retained translation-only case has CSS origin `(320.3125,124.453125)`, DPR 1 and inactive paired geometry. This review accepts that finite conversion, with the existing chain, identity-transform, positive-envelope, finite-point, settlement and bounds guards preserved.

For T08.p52, independent raw-value accumulation gives a scale of 2.9 local pixels per synthetic USD million. The derived cash interval is `[150.4375,174]`, income is `[114.55,150.4375]`, and revenue is `[34.4375,114.55]`. Their centers match the retained midpoints. The old local y of 104.21875 is inside the revenue interval; the proposed income y of 132.49375 is inside income. The CSS shift is 28.275 pixels. These are inferred intervals from retained data and matching source, not new shape bounds or actual picked-object receipts.

T05.p17 has identical rectangle center and midpoint. Its zero delta independently rules out this midpoint substitution as a remedy for that observation. The unequal displayed prior value can motivate a later event, picking or tooltip-cache investigation, but does not choose among them. T04's omission remains separate. The displayed Revenue label, tied values and intended wrapper identity do not establish actual picked identity.

## Keyboard capacity remains conditional

The independent reprojection preserves all 27 actual Tab records, both members of each full equal settled pair, active-element fields, live status and visible tooltip content. Hidden tooltip content is reduced to visibility. Every retained baseline comparison is equal; the mode baselines remain bounded by two swapchain entries. The per-input ledger is unchanged.

The compact case is 41,350 bytes. Observed maxima are 745 bytes per projected Tab record, 440 per Tab ledger entry, 452 per other ledger entry and 562 per baseline. Recomputing `41350 + 45*(745+440+2) + 6*(452+1) + 562 + 2048` gives 100,093 bytes. This validates the reported observed-maxima extrapolation only. Unseen focus names, status text, tooltip contents, baseline changes and metadata can exceed the assumed sizes. A finite reservation rule and an actual collector diff remain prerequisites to implementation approval.

The unchanged reserve guard is 115,072 bytes and the hard case ceiling is 131,072. Twenty-four pointer probes plus 72 Tabs exactly consume the hard 96-probe ceiling; 72 Tabs plus 18 setup actions fit the 120 keyboard-action cap. This arithmetic provides no allowance for extra probes, retries or unconditional arrow sequences. The historical extra loop counter emitted no Tab. Runtime reachability, later modes, elapsed time and complete keyboard behavior remain unverified.

## Findings and delivery boundary

1. **FYI:** The diagnostic package's source/version agreement supports source interpretation only. It does not independently verify the recorded image bytes or prove a runtime cause. The report states this limit correctly.
2. **FYI:** Publication requires the publisher's separate allowlist-metadata copy and a final destination hash/link audit. No existing historical artifact should be rewritten. The seven-link source audit is not a claim that copying has already occurred.
3. **Important for future implementation, not a publication blocker:** Keep family-specific midpoint selection, full equality before projection, explicit baseline-change handling, finite serialization reservations and all existing hard limits in a separately reviewed collector proposal. Neither this review nor the diagnosis grants a run.

No remediation is required for the reviewed source proposal. The [review allowlist](publication-allowlist.json) selects only the review, independent audit, read-only preload and receipt. Research documentation and verification artifacts are outside production size caps; future maintained code still requires the checker/inventory foundation, 400 physical lines per file, 300 logical units per file, 50 logical units per function and final shared-module audit. Documentation, testing, delegation and complexity steering were read. Production files, spec approvals and frozen evidence were not edited.
