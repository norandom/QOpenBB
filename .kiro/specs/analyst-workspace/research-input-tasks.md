# Company Research input-readiness tasks

Requirements and design are owner-approved on 2026-11-06. This plan implements the [bounded design](research-input-design.md), not a dashboard or financial model. Six executable tasks; each is sized as a focused 1-3 hour unit, subject to actual provider access. Checkboxes represent acceptance, not work started.

## Execution boundaries

The controller serializes setup, shared helpers, live calls, commits and final acceptance. After task 2 passes independent review, two Sol workers may implement 3.1 and 3.2 concurrently with exclusive files. One Astra reviewer checks financial/integration acceptance. Use fresh contexts, at most four slots and per-task commits. Workers must preserve other changes and request shared-helper changes through the controller.

| Task | Exclusive writable scope | Join |
| --- | --- | --- |
| 1 | Ignored setup/identity receipt only | Existing environment and pinned sources confirmed |
| 2 | `tests/providers/live_financial_support.py`; focused helper regressions in `tests/providers/test_service_financial.py` | Shared fixture, safe evidence and request controls frozen |
| 3.1 | `tests/providers/research_input_cases.py`, `tests/providers/test_live_financial.py` | Native journeys use the frozen helper contract |
| 3.2 | `tests/providers/test_live_dcf_feasibility.py` | Direct probes use the same shared state and safe receipt contract |
| 4 | Ignored execution receipts only; code corrections return to owning task | One reviewed run establishes actual observations or explicit gaps |
| 5 | `docs/reference/research-input-readiness.json`, spec `research-input-assessment.md`, `artifacts/reviewed/research-inputs/accepted.md`, mirror manifest and affected README/docs/spec/breadth status | Independently reviewed assessment published |

No production files, source pins, dependency locks, catalogs, model repository or service changes. The existing 400 physical/300 logical/50-per-function checker and inventory already exist; task 1 confirms scope before any changes. Tests and documentation are excluded from production caps. Any necessary production fix requires a separate reviewed scope and its executable cap check; do not hide runtime code under tests.

## Tasks

- [x] 1. Confirm the existing verification environment and freeze the execution scope
  - Confirm the installed provider environment, API pin, contract hashes and existing test collection without provider calls. The Windows Workspace vendor checkout is older; use recorded accepted source identities without building it.
  - Locate the existing private key-loading path without printing values; verify configured/missing states only. Missing credentials do not trigger substitute data or count as access acceptance.
  - Freeze the declared sample, historical references, native/direct receipt distinction and exact research node selections. Separate baseline regression selection from the 51-request research budget.
  - Done when the setup receipt records actual interpreter/configuration/source identities, successful offline collection and concrete invocations; no new environment, lock or service is introduced. If installed source differs, resolve identity before live execution.
  - Complexity completion: read-only setup and ignored evidence are excluded; confirm no maintained production scope change.
  - _Boundary: Existing verification environment_
  - _Requirements: 1.3, 1.4, 5.4, 6.3_

- [x] 2. Freeze shared request controls and source-preserving evidence
  - Extend the existing test-only helper with one shared research-run state, per-provider stop reasons, failed-attempt counting, the 51-attempt ceiling and enforced 15-second timeout. Preserve original baseline behavior when no research state is supplied.
  - Make that single session instance available to both native and DCF modules. Prove cross-module identity and shared stop/budget effects with offline checks; importing identically named fixtures is insufficient evidence.
  - Preserve source callback behavior. Add absent/null distinctions, stable source ordinals, documented alias/date/year normalization and safe native/direct receipts without logging headers, URLs or unsafe provider exception text.
  - Add focused regressions to the existing helper/service test area for ceiling denial before transport, failed calls consuming budget, authentication/throttling stopping the provider, endpoint entitlement branch handling, timeout enforcement, sanitization and unchanged baseline semantics. Keep regressions about observable safeguards, not incidental implementation structure.
  - Done when affected offline checks pass and independent review freezes the helper interface, including same-listing EV receipt/date handoff and dependent-case outcome recording. No live requests occur in this task.
  - Complexity completion: test-only helper/regressions are excluded from production caps; verify the diff contains no production changes.
  - _Boundary: Shared verification support_
  - _Depends: 1_
  - _Requirements: 1.3, 1.4, 2.2, 3.1, 5.1, 5.3, 5.4, 6.3_

- [x] 3. Implement the two independent verification lanes
- [x] 3.1 (P) Verify the declared company and candidate-peer inputs
  - Define MSFT, ORCL and ADBE discovery/profile cases and explicit candidate rationale; preserve listing identity, exchange and separate trading/reporting currencies.
  - Cover Income, Balance, Cash, Metrics, Ratios and Enterprise Values in annual/quarter modes, bounded to two/four rows. Use dataset-based semantic dispatch and source mappings for required earnings, cash, working-capital, debt/share and EV fields. Keep unknown duration/YTD/restatement and valuation bases visible.
  - Execute each company journey in declared prerequisite order: identity, financial inputs, then one price window based on its latest successful annual/quarter EV observation. No refetch, fallback price or assumption that pytest parameter order supplies prerequisites. Preserve original baseline node IDs.
  - Retain the existing DGS10 check and historical evidence; a new query is needed only for a new access claim. Provider peer suggestions remain separate from sample rationale.
  - Done when offline collection/fixture-backed assertions cover all case paths, source mappings, unresolved identity and missing-EV behavior; the worker returns exact node IDs for task 4 and independent review accepts the lane without any live-data claim.
  - Complexity completion: test/case files are excluded from production caps; no provider, widget or calculation code changes.
  - _Boundary: Native research cases and assertions_
  - _Depends: 2_
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 2.1, 2.2, 2.3, 2.4, 3.1, 3.2, 3.3, 3.4, 4.3, 5.1, 5.2, 5.3_

- [x] 3.2 (P) Assess standard and custom DCF through bounded direct probes
  - Use the existing stable-URL transport with explicit GET, API-key header, no redirects and the frozen shared request controls. The FMP-only prerequisite must not require a FRED key.
  - Sequence at most three MSFT requests within one test function: standard DCF, custom defaults and the documented beta=1.0 variation only after a usable baseline. Reset capture context between requests; preserve the shared run state.
  - Record source integration, published documentation, observed access, assumption fields and tested input binding separately. Forecast year is not valuation date, Profile currency is not DCF currency, and an echoed beta is not validated sensitivity support.
  - Done when offline cases prove blocked/missing credentials, entitlement, unusable baseline and unknown binding remain explicit; success cannot masquerade as native API/widget integration. Independent review accepts the direct-probe scope and exact task-4 node selection. No live requests occur in this task.
  - Complexity completion: test-only probes are excluded from production caps; no adapter restoration, registration or local valuation arithmetic.
  - _Boundary: Direct DCF feasibility checks_
  - _Depends: 2_
  - _Requirements: 4.1, 4.2, 4.4, 5.1, 5.2, 5.3, 5.4_

- [x] 4. Join the lanes and collect the bounded real-provider evidence
  - Controller verifies both independently accepted lanes share one actual request-state instance and selects their exact collected nodes in one serial research invocation. Run affected baseline regressions separately; do not reset the research budget between modules.
  - Execute no more than 46 native FMP, three direct DCF and two FRED upstream attempts, fewer when reusing historical evidence or prerequisites fail. Use configured private credentials, original callbacks and sanitized receipts; no automatic retries.
  - Record command, source/contract identity, actual exit code, attempt count and each observation/gap. Authentication/throttling stops further provider requests; required blocked cases remain unverified/failed. A blocked DCF feasibility finding may be conclusive but is not a passed integration.
  - Done when all declared sample cases have inspected evidence or an explicit reason they could not execute, and independent review checks values/provenance, current versus historical evidence and native versus direct claims. Code defects return to their owning task; provider/semantic gaps remain findings instead of broadening scope.
  - Complexity completion: execution produces ignored receipts only; no production changes or image rebuilds.
  - _Boundary: Native and direct verification integration_
  - _Depends: 3.1, 3.2_
  - _Requirements: 1.1, 1.3, 1.4, 2.1, 2.2, 2.3, 3.1, 3.2, 3.3, 4.1, 4.2, 4.3, 4.4, 5.1, 5.3, 5.4, 6.3_

- [x] 5. Publish the financial input assessment and next delivery decision
  - Join the actual receipts and scoped historical evidence into the designed JSON record and one analyst-facing matrix. Include exact widget IDs, sample rationale, source-qualified identities, units/currencies/periods, explicit missing conventions and owning corrective work.
  - Obtain independent financial review of cash-conversion and peer input adequacy, invalid denominators, share/date alignment and DCF/macro limitations. No house calculation or invented financial convention is permitted.
  - Keep assessment completion, IA-B input readiness and workflow implementation separate. A conclusive gap assessment can be complete while IA-B remains blocked; this task always leaves IA-B workflow implementation false.
  - Record the next bounded dashboard/provider/model dependencies, paired controls, independent macro context and fresh-login/container-recreation/template identity obligations. Preserve existing receipts and do not replace historical evidence identities.
  - Done when the assessment matches the receipts, independent review passes, reviewed artifacts are sanitized and hash-synchronized, links/metadata validate, and the controller commits/pushes only owned files with README/docs/spec/breadth checkboxes reconciled. No Dagger dispatch for this verification-only milestone.
  - Complexity completion: evidence/docs/status files are excluded from production caps; production inventory and unrelated work remain untouched.
  - _Boundary: Evidence integration and readiness decision_
  - _Depends: 4_
  - _Requirements: 1.2, 1.3, 1.4, 2.4, 3.4, 4.4, 5.1, 5.2, 5.3, 5.4, 6.1, 6.2, 6.3, 6.4_

## Existing command foundation

Use the installed environment proven by the earlier financial-input review. From repository root, the existing offline entry point is:

```sh
env PYTHONPATH=services/data-api verification/provider/.venv/bin/python -m pytest -c verification/provider/pyproject.toml tests/providers/test_service_financial.py -n0 --maxprocesses=2
```

Task 1 confirms this environment's current source identity and collection. Tasks 3.1/3.2 return actual collected research node IDs, then task 4 supplies those to this same pytest entry point with `QOPENBB_LIVE_ACCEPTANCE=1`, private configured keys and a unique ignored output directory. Never include key values in commands, receipts or reports. This plan does not claim future nodes exist or commands ran. If owner execution is needed, place the exact operation in ignored `run_this.sh` and syntax-check it.

The project delivery rules require the evidence/documentation completion task despite the generic task skill's code-only default: this approved slice's deliverable is an executable verification and readiness assessment. No additional paperwork-only tasks are introduced.

## Implementation Notes

- Task 1 accepted 2026-11-06: 31 tests collected, 16 offline service checks passed; independent Sol review approved. Existing installed API/source and eight contract hashes match. Ignored setup receipt SHA256: `33cd4eda1e50bc50b4d7513d58db9f57f8b2316b1dc7807c00dd6a1ce7c38920`. Research selectors await task 3; no live-access claim.
- Task 2 accepted 2026-11-06: 28 offline checks passed, including independent Astra rerun. Shared session state, bounded transport, source comparisons and immutable sanitized receipts are frozen; no live-provider acceptance claimed. Lane handoff is retained locally at `artifacts/research-input-readiness/helper-api-handoff.md`.
- Task 3.2 accepted 2026-11-06: 18 offline DCF checks passed, live case skipped; independent Astra review approved. Direct probes are implemented, but provider access and custom-input behavior await task 4.
- Task 2 integration repair accepted 2026-11-06: preserve recognized HTTP failures through legacy callbacks and exact fiscal-year strings before optional integer normalization. 32 offline checks passed; independent Astra review passed the four new regressions. No interface or production change.
- Task 3.1 accepted 2026-11-06 after one review repair: 23 offline checks passed; independent Astra review verified seven exchange-identity and blocked-prerequisite regressions. Four live nodes collect; actual provider inputs await task 4. Metrics/ratios omit `ttm` from effective-query metadata and retain that explicit finding.
- Task 4 accepted 2026-11-06: one serial run at `b597df7` passed five live journeys and recorded 49 attempts (46 native FMP, three direct DCF), all HTTP 200. Combined offline join: 73 passed. Independent Astra review approved the evidence; financial compatibility and IA-B readiness remain open. FRED evidence is historical-only. Local run: `artifacts/research-input-readiness/live-20261106T112507Z`.
- Task 5 accepted 2026-11-06: independent Astra financial review approved the 50-observation assessment and all 24 criteria. IA-A assessment is complete; IA-B inputs/workflow remain false. Public evidence: `artifacts/reviewed/research-inputs/accepted.md`. No runtime change or image build.
- Task 2 accounting-field correction accepted 2026-11-06: three regressions reproduce the overly broad `account` key filter; the corrected sanitizer preserves native financial definitions and zero/null/negative values while removing private account identity and credentials. Existing service suite: 35 passed. Independent Astra review approved; no production change or new live run. Review: `artifacts/reviewed/research-inputs/accounting-correction-review.md`.
- Task 5 accounting assessment correction accepted 2026-11-06: withdrew false native-field gaps using retained receipt semantics and separately identified pinned-source evidence. All 50 receipt hashes are unchanged; independent Astra review approved. Public static audit and correction review accompany the accepted record. IA-B flags remain false.
