# Task 1.3 independent financial re-review

The two blocking findings from review.md are corrected. Task 1.3 is approved for offline contract characterization only; this does not accept production adapters, entitlement or consumer behavior.

## Review Verdict
- VERDICT: APPROVED
- TASK: 1.3
- MECHANICAL_RESULTS:
  - Tests: PASS. From D:/BuildArtifacts/QOpenBB/fmp-expansion-a/root, `& ../evidence/1.3/run.ps1 reviewer-astra-r2` exited 0: 112 passed, zero skips, one existing aiohttp deprecation warning. Exact six package-origin assertions passed. Log: reviewer-astra-r2.log.
  - TBD/TODO grep: CLEAN across eight current files.
  - Secrets grep: CLEAN for selected credential/private-key patterns; manual inspection found no credentials.
  - Static checks: SPOT_CHECKED. Provider-only schema overrides, validators, aliases and actual native widget formatter projection reviewed.
  - Boundary: WITHIN. Precisely eight untracked additions; git diff empty because additions remain untracked. API working tree clean. No production registration or standard-model changes.
  - Boundary audit: CLEAN. Existing public field union preserved; no hidden production dependency. Test/fixture code excluded from production complexity caps.
  - RED phase: VERIFIED. Original red.log retained; remediation-red.log independently shows seven relevant failures and 105 passes before correction.
- FINDINGS:
  1. Resolved: All 117 growth fields now advertise ratio and omit x-frontend_multiply in both validation and serialization schemas. Dedicated provider model rebuilding updates the actual generated schemas; native data_schema_to_columns_defs projects numeric columns without percent/normalizedPercent. The compatibility records preserve retained percent behavior and explain migration.
  2. Resolved: Quote absolute change is provider_calculation, retaining currency/share and scale1. The independent financial-family assertion now expects that meaning.
  3. FYI: Float and cash-flow documentary examples are explicitly identified as indexed official documentation excerpts, not direct HTML or live provider payload captures. The preserved search capture contains the numeric float example and all four exact Activites spellings. Direct page HTML did not reproduce those examples in the first review; this narrower evidence claim is appropriate.
- REMEDIATION: None required for this bounded task. Carry the frozen schema overrides, financial annotations and documentary limitations into subsequent adapter handoffs.
- SUMMARY: The six offline A2 contracts now satisfy the reviewed financial semantics and frozen schema boundary, with production and live acceptance remaining separate.

## Verification scope

Source identity remains root eb82968242b766391a568dfdded0f95d1d1fdd23 and API a965f70c164fe477ce9c99654b9be48e2f1bc9fd. The runner uses D:/BuildArtifacts/QOpenBB/statement-period-provenance/provider-venv/Scripts/python.exe with:
`-B -m pytest -p xdist.plugin -c verification/provider/pyproject.toml tests/providers/test_fmp_a2_contracts.py -n0 --maxprocesses=2 -p no:cacheprovider --basetemp D:/BuildArtifacts/QOpenBB/fmp-expansion-a/evidence/1.3/tmp-reviewer-astra-r2`.
It disables bytecode and plugin autoload, and checks core/FMP/FRED/equity/economy origins in the sibling API and qopenbb_data in this root before pytest. The new projection regression loads the actual sibling platform_api/utils/openapi.py file by absolute path.

Fresh tests again verify exact validation/serialization snapshots, native-standard-plus-retained field union, archive/member/license hashes, canonical/generated/source aliases, missing/null/zero distinctions, ten required-nullable balance growth fields, corrected balance currency destination, and the four cash-flow spelling pairs with conflict rejection. Float percentages divide by100 without losing zero; nullable source dates preserve supplied precision and do not become retrieval dates. Quote epoch0 remains UTC; market capitalization and share-count dates are not inferred from it. Capitalization defaults resolve at acquisition, ordered windows are bounded at366 days, fixed response cap is5000, and fiscal growth fractions remain scale1 with duration/denominator/restatement uncertainty explicit.

I read the current changed declaration and test sections, all changed compatibility/limitation records, the original review, remediation report/results and failing regressions. The fresh suite checks the original financial branches as well as the fixes. No production code, task checkbox or commit changed during review. No live provider requests, installs, builds or UI runs occurred. Native formatter projection is offline evidence only.

The supplied official-search-capture.json SHA-256 is de71eef3bb014a06c34d5d2922d0091600e3afbbb304fa969f60b58107ec7011; independently recomputed and matched. Its declared retrieval is indexed excerpts on2026-11-17. The float arithmetic independently agrees with floatShares/outstandingShares times100; the four documented spellings are supported only as aliases to existing canonical fields. No claim of current account entitlement or current response completeness follows from these excerpts. The original rejection and raw evidence remain preserved.

Hash verification command read remediation-results.json, recomputed Get-FileHash for each named file and the search capture, and failed on mismatches; exit0 with all matches. Scoped rg searches returned no placeholders or selected secret patterns. Root/API git identity checks exited0; API status was empty.

## Reviewed current SHA-256 hashes


- tests/providers/fmp_a2_contracts.py: 8bcda0e145bedc713e2e52009573b4774142907a0661c08ab445b962c05e28d2
- tests/providers/test_fmp_a2_contracts.py: cfdf22463352d74dff76bc12f3d53495cf778675bb848e75b72815e064df503f
- tests/providers/fixtures/fmp_batch_a/contracts/historical_market_cap.json: b9537130dec7cefd57fa0220d4f44805c78272aaedc2a53f557e13dc3e595184
- tests/providers/fixtures/fmp_batch_a/contracts/share_statistics.json: 7c9e2c749a9dcca83aef51db66872650c042f8a314754bef673b32c27539cc67
- tests/providers/fixtures/fmp_batch_a/contracts/equity_quote.json: 396bf06aa833d37ee1e3bb86b1258b055911547271c7682465c55bfa64942023
- tests/providers/fixtures/fmp_batch_a/contracts/income_statement_growth.json: 941a42259594cb43b243ffb121d5f019f58311e39b2963286f8858d8fd2570e7
- tests/providers/fixtures/fmp_batch_a/contracts/balance_sheet_growth.json: dc2263bf326de40b8af0387baf843bf03f47e5ff4c46c7727b3837208233ab6f
- tests/providers/fixtures/fmp_batch_a/contracts/cash_flow_growth.json: dcb92511cbf7d033afb4413e45590adf64afd2b83aaf00c9a78eec602b8db50e
