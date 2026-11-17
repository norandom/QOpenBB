# Task 3.5 independent financial review

RevenueGeographic meets its bounded offline adapter contract at the exact hashes below. The review inspected git diff/status (the two additions are untracked), read full production and test sources, task 3.5, the frozen contract and retained recovery, and checked the design against requirements 2.3-2.5, 4.1-4.7, 5.1, 5.3-5.4, 6.1, 7.1-7.5 and 8.4. Integration and live acceptance remain separate.

Source identity: root 676847f6c6c4a215ad32a1cda29276ef8e5ce227; API 905bd72d1ca1f3bd7a2007d90c8d14b0fcfd61b9. Production SHA256 894167fe1938b1a4916c66ff992adc669ecb836f2e43c1828054e4c738d614dd; test SHA256 2f26874ce7d5fe947afad5989a3efe4a6bf5c12d9c9333fa7f24ebe0bf7acb45; frozen contract SHA256 498b35ae7cdf776ab50bf26b0a3a8c44fdaebc8bcc7be8a056de4b597846ce91. Retained recovery at ../1.1/recovery/revenue_geographic.py matches SHA256 7b96b026784b778977b1ef2d525613794c0ec53d39082b02de469b3052607c5f. The adaptation preserves native model ownership while replacing archived label normalization, integer truncation, row sorting and null dropping with the approved preservation and validation rules.

## Review Verdict
- VERDICT: APPROVED
- TASK: 3.5
- MECHANICAL_RESULTS:
  - Tests: PASS. run.ps1 exit 0, 214 endpoint/shared tests; probes.ps1 exit 0, 24 independent adversarial checks. Logs: tests.log and probes.log.
  - TBD/TODO grep: CLEAN, also checked FIXME/HACK/XXX (rg exit 1 means no matches).
  - Secrets grep: CLEAN by source inspection; only synthetic test sentinels, no credentials.
  - Static checks: PASS. verify.ps1 exit 0; Ruff clean; six source origins checked. Whole production file 248 physical / 88 logical / 10 maximum function units, within 400/300/50.
  - Boundary: WITHIN; one provider module and one endpoint test addition. Reviewer writes only evidence/3.5-review.
  - Boundary audit: CLEAN; native Query/Data/Fetcher, shared acquisition/validation and existing metadata reused; no shared-schema, router, registry, formatter or consumer modifications.
  - RED phase: VERIFIED; ../3.5/red.log records the absent production module before implementation, rather than an unrelated failing assertion.
- FINDINGS:
  1. No blocking findings. Both schema modes, accepted aliases, query annotation and all result-field annotations match the frozen contract. Strict direct admission rejects invalid symbols/frequency and unsupported bounds, structure and credentials before transport.
  2. Exact geographic labels, Unicode, whitespace, empty labels, changing taxonomy and repeated labels across periods survive in source order. Signed, zero, fractional and large integer numeric values are retained. Required null/malformed/nonfinite revenue and required invalid dates fail safely, including facts in empty mappings and invalid rows beyond the clipping boundary.
  3. Independent 999/1000/1001-row transport probes preserve fiscal association and prove clipping may split a period; truncation/partial status is asserted only for observed excess. Optional fiscal year/period/filing date remain null. No sum, taxonomy reconciliation, currency inference or invented financial totals appear.
  4. Real Fetcher/shared-helper tests cover one encoded request with fixed structure, period alias/default, the actual acquisition receipt, HTTP [] annotated empty success, valid empty inner mappings, missing/nonmapping data and safe typed errors including retry-after. Independent error probes assert absent cause/context. All result fields retain observation/publication associations; currency and fiscal duration/vintage uncertainty stay explicit.
  5. Native standard schema remains identical before/after provider import, with no standard file change. No formatter mutation or dynamic field expansion was introduced. Offline evidence does not certify provider registration, SDK/HTTP joins, entitlement, real-provider values or Workspace behavior. One existing aiohttp ClientSession deprecation warning is unrelated.
- REMEDIATION: None for task 3.5. Retain controller-owned integration and live acceptance gates.
- SUMMARY: Bounded offline RevenueGeographic behavior is independently approved at the recorded hashes.

Reproduce from D:/BuildArtifacts/QOpenBB/fmp-expansion-a/root with ../evidence/3.5-review/run.ps1, probes.ps1 and verify.ps1. These scripts pin the supplied provider virtual environment and explicit worktree source paths, disable bytecode and plugin autoload, and keep temporary output external. The test command is python -B -m pytest -p xdist.plugin -c verification/provider/pyproject.toml tests/providers/test_fmp_revenue_geographic.py tests/providers/test_financial_errors.py tests/providers/test_financial_metadata.py tests/providers/test_financial_annotations.py tests/providers/test_fmp_transport.py -n0 --maxprocesses=2 -p no:cacheprovider --basetemp D:/BuildArtifacts/QOpenBB/fmp-expansion-a/evidence/3.5-review/tmp. verify.ps1 reuses the worker audit script with the repository checker and writes independent logs. No live request, install, build or commit was made.
