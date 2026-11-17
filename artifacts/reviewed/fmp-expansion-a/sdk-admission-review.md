# SDK admission remediation review

The reviewed task 2.1 runtime patch is approved. The three selection defects in review.md are resolved: omitted selection occurs once at the native generated resolver call, baseline providers receive no strict admission, and unresolved native validation failures preserve native ordering. Task completion still requires the controller's final combined executable complexity gate with the exact approved emitter exceptions.

Reviewed on 2026-11-17 against root HEAD 153ee780da34df5174a771cc013ec74f0e34dad9 and API HEAD a965f70c164fe477ce9c99654b9be48e2f1bc9fd plus the five permitted working production files. This supersedes the runtime rejection in review.md, which remains preserved with its original probes. The original requirements, task, design and admission amendment remain the review basis; the controller's explicit clarification permits unresolved omitted-provider pre-body failures to retain native errors without guessing the provider.

## Review Verdict
- VERDICT: APPROVED
- TASK: 2.1
- MECHANICAL_RESULTS:
  - Tests: PASS, fresh 99-test SDK/freeze suite, exit 0, review-r2-tests.log. Fresh original stable-baseline probe and error-order probe both exit 0, review-r2-probe.log and review-r2-order-probe.log.
  - TBD/TODO grep: CLEAN for new production sources; no introduced placeholders in tracked production diffs.
  - Secrets grep: CLEAN by source/diff inspection; evidence uses synthetic sentinels and offline extraction only.
  - Static checks: PASS in current r1-lint.log; reviewer import/origin/metric/hash audit exits 0, review-r2-audit.log and review-r2-audit.json. Root and API git diff --check pass.
  - Boundary: WITHIN the exact five API paths and authorized tests/inventory/documentation scope.
  - Boundary audit: CLEAN; no parallel runtime endpoint registry, financial fixture dependency, raw-body rescue, provider-union controls, Query/CommandRunner rewrite or unrelated production changes.
  - RED phase: VERIFIED, r1-red.log contains the three failing selection/order regressions before remediation; earlier missing-required RED remains preserved.
- FINDINGS:
  1. FYI: No blocking runtime finding remains. The drift regression identifies actual other-provider extraction and makes FMP extraction fail, rather than inferring provider identity from an identical fixture result.
  2. FYI: r1-report.md names r1-audit.json, but that historical file is absent. The actual supplied JSON evidence is r1-audit.log. The fresh reviewer-owned review-r2-audit.json exists and independently verifies current sources; no historical file was manufactured.
  3. FYI: Final combined complexity acceptance remains pending. This review approves the source patch and exact exception design, not completion before that gate.
- REMEDIATION: None for the reviewed runtime patch. Controller must apply the exact reviewed exceptions, retain their review reference and run the final combined gate against actual fork identities before marking task 2.1 complete.
- SUMMARY: Native once-only selection, baseline validation order and strict FMP raw admission now compose correctly in the reviewed offline scope.

## Why the remediation closes the findings

select_frame reads authoritative descriptors and captures supplied membership into a pending frame without resolving an omitted provider. Native validate_call runs normally. The generated _get_provider call matches Container, route, original choice, priority order and task/thread owner, then invokes the unchanged native resolution algorithm exactly once. Activation uses its result: strict FMP validates the untouched raw snapshot before filtering; a baseline result clears the snapshot and skips strict query checks. The container consumes either frame once and performs strict effective reconstruction only for strict FMP. Both paths clear raw values before sync_run and restore context tokens in finally.

The original stable-baseline probe now records exactly ['other']. The updated drift regression changes credential availability but observes only ['other'] and only other-provider extraction; FMP extraction is explicitly forbidden. A separate regression selecting FMP through native fallback rejects raw True before extraction. The original error-order probe now reports native_validation with zero credential checks both with and without the eligible FMP marker. DEBUG on/off tests compare actual exception type and text for unresolved native errors. This honors the controller-confirmed no-guess boundary: those unresolved errors are not represented as selected-FMP redaction evidence.

Explicit FMP is identifiable before native validation and retains constant invalid_parameters errors without raw causes. Valid configured financial defaults reach native Query/Fetcher, caller values retain precedence, and invalid defaults stop before extraction. Native validation is never bypassed. Existing all-eleven schema, positional/alias, null/bool, unsupported-key, nested invocation, inherited child context, thread, async, provider/filter mismatch and transport distinction checks remain in the passing suite. Added create_task ownership and nested baseline-await tests verify frame restoration through actual await, not coroutine creation alone.

## Commands and current identity

The fresh suite used run.ps1's explicit source environment and D:/BuildArtifacts/QOpenBB/statement-period-provenance/provider-venv/Scripts/python.exe from this root repository:

    python -B -m pytest -p xdist.plugin -c verification/provider/pyproject.toml tests/providers/test_fmp_parameter_admission.py tests/providers/test_fmp_contract_freeze.py -n0 --maxprocesses=2 -p no:cacheprovider --basetemp D:/BuildArtifacts/QOpenBB/fmp-expansion-a/evidence/2.1/tmp-review-r2

PYTHONDONTWRITEBYTECODE=1 and PYTEST_DISABLE_PLUGIN_AUTOLOAD=1. PYTHONPATH selects this root's services/data-api and pipeline plus this sibling API's core, FMP, FRED, equity and economy sources. Fresh result: 99 passed, one existing aiohttp subclass warning, 18.84 seconds, exit 0. The original review-probe.py and review-order-probe.py ran unchanged under the same interpreter/environment, each exit 0. Drift proof is the newly inspected test_omitted_provider_cannot_drift_into_fmp_after_raw_coercion in the fresh suite; the old probe's blanket zero-extraction assertion is inappropriate once baseline-only execution is correctly preserved.

review-r2-audit.py independently checks all six package origins, Git identities, byte hashes and authoritative measure_python metrics. No installs, image builds, live calls, production edits or repeated broad quality suite were performed. Existing 102-pass/two-platform-skip quality evidence remains applicable to the unchanged checker implementation.

| API app-relative file | SHA-256 | Physical / logical / largest function |
| --- | --- | --- |
| parameter_admission.py | b5e95df7ddcaf3eb1807bf1fab87698c65f45c05f46925f55267028122d71505 | 220 / 125 / 20 |
| static/utils/admission_context.py | 527b44520025bf11a18dc7d4a684475e524585fa0fb71d835d0fc85f53c4427c | 94 / 54 / 9 |
| static/utils/decorators.py | 384460edd43ee369d7d04aa67e5d02e5cf11e969e3d4e9d433c62c4e3c012e54 | 181 / 101 / 30 |
| static/container.py | a9cd16352bd74b6bdfc7b187ae56bfa675ad90247e7156d6295951a096eec494 | 160 / 83 / 37 |
| static/package_builder/method_definition.py | 0483543eee4f290706e1e563fbe8443639af21e28bb389226f3079a3afa03d57 | 1649 / 731 / 110 |

Current test_fmp_parameter_admission.py SHA-256: af732b379390790240bb755b1068001d0c8d10fac26f27268cdb3da725ba580b. Other reviewed root test and inventory changes retain the first review's bounded scope.

## Exact emitter exception approval retained

All five entries previously reviewed in exception-proposal.json remain APPROVED under complexity.md's narrow oversized-upstream exception rule. They apply only to repository data_api, path openbb_platform/core/openbb_core/app/static/package_builder/method_definition.py, API revision a965f70c164fe477ce9c99654b9be48e2f1bc9fd with exact working-file SHA-256 0483543eee4f290706e1e563fbe8443639af21e28bb389226f3079a3afa03d57. Expiry remains 2026-12-17. The intended maintained review reference remains artifacts/reviewed/fmp-expansion-a/sdk-admission-review.md when the controller mirrors this decision there.

| Metric | Exact allowance | Position |
| --- | ---: | --- |
| Physical | 1649 | Whole file |
| Logical | 731 | Whole file |
| Function | 110 | format_params, 656:5 |
| Function | 52 | add_field_custom_annotations, 975:5 |
| Function | 86 | build_command_method_body, 1342:5 |

The actual emitter diff remains only two replaced decorator argument strings carrying explicit _command_path metadata and preserving arbitrary_types_allowed. There is no physical/logical growth, no oversized callable body change, no source compression and no body/schema rewrite. All other production files pass ordinary caps. The controller may mechanically rebind these five entries to a new actual API HEAD only after verifying identical emitter bytes, counts and callable positions. Any emitter source change requires renewed independent review. Inventory extraction through the existing include loader remains approved; no exemption applies to its maintained configuration files.

The final combined executable gate has not yet run with these approved entries. Unchanged upstream source is not newly certified. Dedicated registered native variants establish task-local SDK behavior; actual production adapter registration, HTTP parity, live entitlement, browser behavior and final task 4.2 composition remain separate pending gates.
