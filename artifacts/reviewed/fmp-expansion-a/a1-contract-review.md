# Task 1.2 independent remediation review

The corrected five-endpoint characterization is accepted. This supersedes the rejected verdict in review.md without removing that record. Acceptance is limited to offline schemas, financial annotations and compatibility mappings; adapters remain unimplemented by this task.

Source identity: root `0a7e936be4eb401a209e640f3e00337ed85a92a9`; sibling API `a965f70c164fe477ce9c99654b9be48e2f1bc9fd`. Root tracked diff remains empty; untracked scope remains two test modules and five JSON manifests. API status remains clean. Reviewed actual complete Python sources and all five manifests, including schema equality exercised natively, aliases, date contracts, limitations and compatibility decisions. Original task/spec/steering review context remains applicable.

## Review Verdict
- VERDICT: APPROVED
- TASK: 1.2
- MECHANICAL_RESULTS:
  - Tests: PASS; fresh independent focused suite, 94 passed in 0.71s, exit 0; existing aiohttp deprecation warning only.
  - TBD/TODO grep: CLEAN, including FIXME/HACK/XXX; rg exit 1 means no matches.
  - Secrets review: CLEAN; synthetic inputs and public documentation references only.
  - Static checks: SPOT_CHECKED; native imports and model execution succeed.
  - Boundary: WITHIN; dedicated tests and frozen contracts only, production caps excluded.
  - Boundary audit: CLEAN; no production adapters, registry, shared runtime or public field additions.
  - RED phase: VERIFIED; remediation-red.log contains 9 failures / 80 passes for canonical count values, units, source mapping and missing date characterization; subsequent native proof passes.
- FINDINGS:
  1. Resolved: provider numAnalystsRevenue and numAnalystsEps now populate existing canonical number_analyst_estimated_revenue and number_analysts_estimated_eps. Both source-original and effective aliases remain recorded. The incompatibility record explains the inherited defect and instructs future adapters to use the corrected effective mapping. This bounded compatibility correction is accepted without widening the standard-plus-retained public field union.
  2. Resolved: both canonical analyst-count fields have count units and scale 1; explicit tests cover nonzero, zero and null with no undeclared extras and canonical serialization.
  3. Resolved: published_date and both period_ending fields are required/nonnullable; filing_date and published_time remain optional/nullable. date_contracts now separates requiredness and nullability, checked against native fields and validation. Independent omission probes additionally confirm rejection of missing required dates.
  4. Resolved: each field now distinguishes canonical name, generated schema alias, retained source aliases and serialization name. Every effective source dictionary entry is exercised through native model validation and canonical output with no extras. Frozen schema checks no longer stand alone as the financial proof.
- REMEDIATION: None required for task 1.2. Adapter handoffs must carry effective_aliases and this accepted compatibility decision.
- SUMMARY: All four original blockers are resolved within the unchanged public field union, with fresh native evidence.

## Commands and origins

Run from `D:/BuildArtifacts/QOpenBB/fmp-expansion-a/root`:

`& D:/BuildArtifacts/QOpenBB/fmp-expansion-a/evidence/1.2/run.ps1 review-r2-20261117`

The inspected runner invokes provider-venv Python 3.13.15 with `-B -m pytest -p xdist.plugin -c verification/provider/pyproject.toml tests/providers/test_fmp_a1_contracts.py -n0 --maxprocesses=2 -p no:cacheprovider --basetemp D:/BuildArtifacts/QOpenBB/fmp-expansion-a/evidence/1.2/tmp-review-r2-20261117`; PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 and PYTHONDONTWRITEBYTECODE=1. No suite was repeated.

Independent Python stdin probe used the same interpreter, source overrides plus root/tests/providers, and resolved openbb_core to sibling data-api/openbb_platform/core, FMP/FRED to that sibling providers tree, equity/economy to its extensions tree and qopenbb_data to root/services/data-api. Probe asserted source counts 9/7 become canonical values with empty model_extra, and omitted required dates raise ValidationError. Probe completed successfully; the surrounding shell returned 1 only because the final clean marker rg found no matches.

Commands also included `git diff`, `git status --short`, `git rev-parse HEAD`, sibling API status/revision, complete source reads, JSON parsing across all five manifests, and `Get-FileHash -Algorithm SHA256` for all seven reviewed files.

## Limits retained

No installation, build, live FMP call or consumer validation occurred. Official-reference status is inherited from the approved design and manifest disclosures; a missing dedicated news documentation page does not prove endpoint removal. Unknown estimates vintage/currency/mixed inputs, consensus response-specific methodology and segment currency/duration remain explicit. Geographic ISO-string validator behavior is retained. Float belongs to task 1.3. Query filtering/transport/adapters remain separate tasks. The production 400/300/50 caps do not apply to these dedicated tests and generated contract fixtures.

## Reviewed file SHA-256
- tests\providers\fmp_a1_contracts.py: ad6447e3a425e1f93b68a82492cb590fb3281e786a00e1042bdd5b5de6eaac79
- tests\providers\test_fmp_a1_contracts.py: 80f275f7009c2349077a0c3865a0289daf91f9c35dd3117f73c14e04372cda54
- tests\providers\fixtures\fmp_batch_a\contracts\analyst_estimates.json: 91586de0a77c2317d0477bc1528da2cbdaf7fbe24644c9a105992facbe35f4fa
- tests\providers\fixtures\fmp_batch_a\contracts\price_target_consensus.json: ad0f48d8df3de4c3f8c3f7fd96267a8abacec5b382e5dda30c3b83fb472b4579
- tests\providers\fixtures\fmp_batch_a\contracts\price_target.json: ed5ac21ec95af8012bb03761b76c0221b3982986f02de556f872c22da4dce0e3
- tests\providers\fixtures\fmp_batch_a\contracts\revenue_business_line.json: cd12c8661df5f9c0374f4f6f447211353719a5cfa368055ac5c670227bf39e05
- tests\providers\fixtures\fmp_batch_a\contracts\revenue_geographic.json: 498b35ae7cdf776ab50bf26b0a3a8c44fdaebc8bcc7be8a056de4b597846ce91
