# SK0 independent contract and fixture review

## Review Verdict
- VERDICT: APPROVED
- TASK: SK0, bounded Sankey contract, inactive shared declarations and retained fixture only.
- MECHANICAL_RESULTS:
  - Tests: PASS. `wsl -d Debian -- bash artifacts/chart-sankey/fixture/verify.sh`, exit 0. Independent native Node raw-to-CSV BigInt assertions, exit 0: all 12 edges match the hash-proven FMP records; four quarterly residuals are exactly zero; root USD 416161000000 equals shared sinks USD 220960000000 + USD 195201000000.
  - TBD/TODO grep: CLEAN across the contract, two declarations and fixture. Secrets spot check: CLEAN.
  - Static checks: PASS. TypeScript 6.0.3 parses both declarations; normalized declaration/import comparison matches the contract after Biome formatting. Existing combined gate report `complexity.json` has no errors/violations and combined acceptance passed: declarations 84 physical/68 logical and 63 physical/41 logical; no functions. Inventory is 400 physical lines. Parent formatting check passed; root `git diff --check` exit 0.
  - Boundary: WITHIN. Controller owns shared declarations and every integration edit; SK1 data and SK2 presentation paths are disjoint and inactive. No routing changed. Tests/documentation are excluded from production size caps; future maintained modules retain all three caps and inventory enforcement.
  - Boundary audit: CLEAN. Existing imported types and capture guards are real. SK3 explicitly retains both identifier descriptors and metadata columns, extends capture guards/unions, and keeps edit context available without a valid graph.
  - RED phase: N/A, declarations/contract and test-fixture preparation establish no runtime behavior.
- FINDINGS:
  1. No blocking findings. Raw typed identities, duplicate compensated sums, finite overflow checks, zero links, self-links/cycles, mixed/unknown metadata, explicit tolerance and incomplete-flow warnings have concrete contracts. Financial equality remains distinct from a declared or verified financial reconciliation.
  2. Fixture labels retain statement dates and identify the annual root as derived. Provenance declares `currency`/`USD`/scale 1/`AAPL FY2025`/`income-allocation`; links are derived income allocations, not cash flows or FMP-supplied edges. Earlier label and metadata inconsistencies were corrected before this verdict.
  3. Existing Table/File editor, family switching, chrome/theme, refresh, stamped persistence and PNG lifecycle remain explicit join obligations. Invalid/empty recovery clears stale geometry while preserving setup; no feature reduction is authorized.
- REMEDIATION: None for SK0. SK1/SK2 and SK3/SK4 require their own independent review and fresh evidence.
- SUMMARY: SK0 is implementable and financially coherent; production behavior, identified-image/browser behavior, appearance and publication remain unverified.

Reviewed SHA256 identities:

- Contract: `5c5f863a993b4eb51fe0eb1f8bf54d215da66f4225a13eb5ca9810f816b90dc8`.
- `sankeyContracts.ts`: `2ff002bf8d631e4277d7878f17be82bd80b67cf4142046b709436ead611c0070`.
- `sankeyTypes.ts`: `0d44b66f17c61395d50950625624ba299e4b088ebaf5e98840bb27ba5112956e`.
- Fixture: `88a17bab264de46dcb0a65fc77038c0aff4ac609d01edf66833b96ca82d92278`.
- Retained raw FMP: `390dc8cbfc8302720a203bd9782d5e3b1f7363a4f762bdfcef079dbbe4c72f6b`; generated Sankey CSV: `4ecca5e85db89496b36346874168e96232eaf893b6d19e02f3d1914a567607bf`.
