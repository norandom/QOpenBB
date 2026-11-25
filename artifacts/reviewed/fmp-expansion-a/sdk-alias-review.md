# SDK alias repair independent review

The implemented supplied-value correction is approved in its bounded offline SDK scope. Fresh public-entry regressions now show quarter and quarterly reaching the actual Fetcher as quarter for all six periodic variants, with both explicit FMP and omitted selection resolving to FMP. The controller must still rebind the unchanged emitter exceptions to the corrective API commit and pass the final committed-source gate before re-accepting task 2.1.

## Review Verdict
- VERDICT: APPROVED
- TASK: 2.1 supplied-value alias correction
- MECHANICAL_RESULTS:
  - Tests: PASS, fresh SDK/freeze run: 186 passed, one existing aiohttp subclass warning, 110.17 seconds, exit 0; review-tests.log.
  - TBD/TODO grep: CLEAN across all four changed production files.
  - Secrets grep: CLEAN by source/diff inspection; synthetic offline test inputs only.
  - Static checks: PASS in current lint.log. Root/API git diff --check pass. Fresh reviewer audit verifies six exact package origins, current revisions/hashes/metrics and byte equality of Container/emitter against API HEAD; review-audit.json and review-audit.log, exit 0.
  - Boundary: WITHIN the four approved API repair files and root test_fmp_parameter_admission.py additions. No Container, emitter, map, standard-model, router, Query or CommandRunner change.
  - Boundary audit: CLEAN. No second validation at projection, global normalization, parallel registry, filtering bypass or HTTP repair coupling.
  - RED phase: VERIFIED. red.log contains twelve quarterly public-entry failures before production repair, with 66 other new cases passing; original failed-alias diagnosis and reviewer probes remain preserved.
- FINDINGS:
  1. No blocking implementation finding. Projection applies successful normalized values only to supplied canonical financial fields; raw membership and default precedence remain intact.
  2. FYI: The worker's first audit invocation refreshed the generic evidence/2.1/audit.json through an old wrapper. That generic file cannot serve as unchanged historical evidence. This review uses the repair-specific supplied audit and an independently generated reviewer-owned audit; historical review-r2-audit.json and failed-alias reports/probes remain separate.
  3. FYI: Parent working-complexity.json records 111 maintained files, five existing emitter exceptions and no errors/violations. Its frozen HTTP draft measurement is size evidence only, not HTTP behavior acceptance. Final actual-commit rebinding/gate remains pending.
- REMEDIATION: None for the reviewed repair. Complete the controller's selective commit, exact emitter revision rebind and committed-source combined gate before task re-acceptance.
- SUMMARY: The alias repair restores the approved periodic contract while preserving native provider resolution, filtering, baseline behavior and invocation isolation.

## Architecture and behavior verified

Reviewed proposal: .kiro/specs/market-data-integrations/fmp-expansion-a-sdk-alias-correction.md, SHA-256 0ea56f3c736f230959500014c071fc7404dfb92e27ed86887bae38fa52814ed9, and ../sdk-alias-debug/architecture-review.md. Actual git diff changes exactly parameter_admission.py, admission_context.py, decorators.py and filters.py. The filter change is one import and a projection call before the original algorithm; its original enum and multiplicity loops remain intact.

supplied_values clears the cache before validation, keeps the successful model only when validation succeeds, and copies only canonical names in the supplied-field set. Accepted missing-required validation leaves the cache empty; raw financial membership is retained. Projection checks strict state, owner, pinned selection, unconsumed/unexecuted state, resolved provider and authoritative registry query/route-model identity. It deep-copies parameter mappings and cached values, leaves controls and omitted keys alone, clears the cache and does not consume the admission frame. Baseline activation and synchronous/asynchronous finally paths clear cached values. Existing Container effective handling and the once-only native resolver remain byte-identical.

The inspected and freshly executed tests prove:

- Six periodic variants, both selection modes, canonical and alias values, one extraction with actual Fetcher period=quarter, one native provider resolution, supplied precedence over configured annual, and unchanged caller/configuration mappings (test_periodic_public_supplied_alias_reaches_fetcher_with_caller_precedence).
- Omitted period stays absent at the filter boundary; schema annual or configured quarter/quarterly becomes the expected Fetcher value (test_periodic_omitted_period_schema_and_configured_defaults).
- Null, ttm, ytd and invalid period inputs fail safely without extraction with DEBUG on/off. Explicit other, omitted other and non-opted FMP retain native canonical success and native alias rejection.
- Projection performs no model validation, preserves raw quarterly, clears only its cache before Container, and leaves incoming mappings unchanged. Failure probes still execute native enum/multiplicity rejection and provider mismatch rejection.
- Nested same/different routes, threads, async tasks and inherited child contexts retain ownership and cleanup. Failure before/inside filtering is followed by a successful baseline call. Nonperiodic configured-symbol behavior keeps missing-only state empty until effective validation.
- Prior null/bool/unknown/field-alias collision, native validation, baseline selection/error-order and changing-credential provider-drift regressions remain in the passing suite.

These use actual registered native descriptors, emitted SDK methods, Container/CommandRunner/Query and dedicated offline Fetchers. Observer wrappers call the real filter; no intercepted _run or raw-body validation rescue is used. Async ownership tests supplement, rather than replace, the generated public-method acceptance matrix.

## Reproducible check and exact source identity

Root HEAD d1c63a4174e61254973e77a907eb9329f48392c8; API HEAD 0c544ace4d177cc6ff833619ad520bf806b90d91 plus the four reviewed working files. From the root repository, the fresh run used run.ps1's environment with only its basetemp changed to evidence/sdk-alias-repair/tmp-review:

    D:/BuildArtifacts/QOpenBB/statement-period-provenance/provider-venv/Scripts/python.exe -B -m pytest -p xdist.plugin -c verification/provider/pyproject.toml tests/providers/test_fmp_parameter_admission.py tests/providers/test_fmp_contract_freeze.py -n0 --maxprocesses=2 -p no:cacheprovider --basetemp D:/BuildArtifacts/QOpenBB/fmp-expansion-a/evidence/sdk-alias-repair/tmp-review

PYTHONDONTWRITEBYTECODE=1 and PYTEST_DISABLE_PLUGIN_AUTOLOAD=1. PYTHONPATH explicitly selects this root's services/data-api and pipeline plus sibling API core, FMP, FRED, equity and economy sources. review-audit.py uses the same interpreter/environment and independently asserts all six origins, Git revisions and unchanged-file byte equality. No installs, builds, source edits, commits or live requests were performed. No broad quality suite was repeated.

| API app-relative file | SHA-256 | Physical / logical / largest function |
| --- | --- | --- |
| parameter_admission.py | 02302ca0fefd0b32bae189928cef25279dcf3c888ad6f8b650de5c0ac87797ca | 261 / 151 / 23 |
| static/utils/admission_context.py | 67e777cde8bf88da3b583cba8af086de3e0f5a50fa8b474a26e954be2ea8da64 | 95 / 55 / 9 |
| static/utils/decorators.py | 9f14a88e7473fe6b6e31e7d1c22bd77458acd61c7a6ff22d705b2b2c56daf75b | 185 / 103 / 30 |
| static/utils/filters.py | 9c47353aa94976054ff29af8550af572ce11e47a8db2219cf92e64fee4acfb67 | 93 / 44 / 39 |
| static/container.py, unchanged | a9cd16352bd74b6bdfc7b187ae56bfa675ad90247e7156d6295951a096eec494 | 160 / 83 / 37 |
| static/package_builder/method_definition.py, unchanged | 0483543eee4f290706e1e563fbe8443639af21e28bb389226f3079a3afa03d57 | 1649 / 731 / 110 |

Root test_fmp_parameter_admission.py SHA-256: 8551f100162638349a9f1a8d6b4e04c1b94bef88c3059ca13cf44ddfb7a78eb6. No repair file needs an exception. Existing emitter exceptions remain exactly physical 1649, logical 731, format_params 656:5=110, add_field_custom_annotations 975:5=52 and build_command_method_body 1342:5=86, expiring 2026-12-17. Rebinding to a new actual API revision requires identical emitter bytes/counts/positions; any emitter source change requires renewed review.

This review does not accept the frozen HTTP task, production adapter registration, actual provider entitlement, browser behavior or deployment. Frozen contracts remain the basis for later production registration joins. The preserved failed-alias evidence remains a valid historical failure record, and this fresh passing evidence establishes the bounded correction only.
