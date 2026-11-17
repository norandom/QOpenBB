# Task 3.4 independent review, round 1

RevenueBusinessLine meets its bounded offline adapter contract. The review read the actual untracked production/test sources, frozen schemas and aliases, source recovery, task 3.4, design and referenced requirements. Registration, generated SDK/HTTP, live entitlement and Workspace acceptance remain controller-owned and unverified here.

Source identity: root 28790d793fad68224d3a0f24bb2ed376ca669799; API a16f40c5ab051aa0afcb37fc7f4382701e26c02b. Production SHA256 3d80c658c78a0326356e7605cad5b64c93ebd161f88b683323da6759f9ffcc04. Test SHA256 ca3b69575148812248a6bf27da02f3b83a536cc4fac11e9923ae828edcdce0fd. Frozen contract SHA256 cd12c8661df5f9c0374f4f6f447211353719a5cfa368055ac5c670227bf39e05. Source recovery hash matches b30886d058e7556d7a2ce6211a677faec9e79273774a3352f1066cfa4f1c9b4b; retained native base and source notice checked.

## Review Verdict
- VERDICT: APPROVED
- TASK: 3.4
- MECHANICAL_RESULTS:
  - Tests: PASS, run.ps1 exit 0; 189 tests (endpoint plus financial errors, annotations and metadata), tests.log. Independent probes.ps1 exit 0, 20 adversarial checks, probes.log.
  - TBD/TODO grep: CLEAN, including FIXME/HACK/XXX.
  - Secrets grep: CLEAN; manual inspection finds synthetic secret test sentinels only, no credentials.
  - Static checks: PASS, verify.ps1 exit 0; Ruff clean; six source origins asserted. Whole production file 248 physical / 88 logical / 10 maximum function units, within 400/300/50.
  - Boundary: WITHIN; two endpoint-owned untracked sources only; review writes confined to external evidence/3.4-review.
  - Boundary audit: CLEAN; native Query/Data/Fetcher and existing acquisition, validation and metadata used; no shared framework, standard-field expansion, registry mutation or consumer logic.
  - RED phase: VERIFIED, ../3.4/red.log records missing production module during collection before implementation.
- FINDINGS:
  1. No blocking findings. Exact validation and serialization schemas, aliases, query annotation and every canonical field annotation match the frozen contract. Class-owned strict admission rejects unsupported parameters before I/O.
  2. Financial preservation verified: exact labels and repeated observations remain in outer-row/inner-label order; negative, zero, fractional and large integer numeric facts survive; required dates/revenue fail safely when invalid, while optional fiscal facts remain null. Independent two-period clipping confirms row 1000 can split a fiscal period and metadata reports partial only for observed excess.
  3. Empty-state distinction verified: actual top-level HTTP [] returns annotated empty success with the real acquisition receipt. Valid dated empty inner mappings return zero rows; missing/nonmapping data or invalid outer facts cannot disappear during flattening. Shared {} and null remain missing_data failures.
  4. One encoded fixed-structure request, annual/quarterly semantics, safe typed failures, retry-after and receipt provenance pass through real shared helpers. Currency, fiscal duration and vintage remain unknown; there is no aggregation, reconciliation, deduplication or disjoint/exhaustive taxonomy claim.
  5. Evidence limit: offline tests use controlled transport callbacks; this verdict does not certify live responses, registration/discovery, generated SDK/HTTP or consumer joins. Existing aiohttp ClientSession deprecation warning remains unrelated.
- REMEDIATION: None required for task 3.4; retain controller-owned integration gates.
- SUMMARY: Bounded offline RevenueBusinessLine behavior is independently approved at the recorded hashes.

Reproduction: run run.ps1, probes.ps1 and verify.ps1 from D:/BuildArtifacts/QOpenBB/fmp-expansion-a/root. Scripts use the supplied provider virtual environment, disabled bytecode/plugin autoload, explicit source paths, zero xdist workers and unique external temporary output. No live request, install, build or commit was made.
