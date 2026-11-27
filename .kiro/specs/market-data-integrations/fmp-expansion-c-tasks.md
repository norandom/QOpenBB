# FMP Batch C implementation tasks

This amendment delivers two provider valuation references and three as-reported statement commands under the [Batch C design](fmp-expansion-c-design.md) and [approved expansion plan](fmp-expansion-plan.md). Each leaf is a 1–3 hour unit. Requirements 2.1, 3.1, 3.2, 3.4, 3.5, 4.8, 5.6 and 6.4 retain their umbrella owners. Run compatibility checks on their existing surfaces where applicable. Requirement 4.4 is covered by checking that Batch C preserves raw values and their basis without introducing financial transformations.

The proposed FMP allowance is a maximum of 30 actual sends across four allocations of 9 direct, 9 installed, 6 Workspace and 6 diagnosed reruns. The ledger starts at zero. Implementation requires owner task approval. Live acquisition also requires owner approval of the proposed allowance. Count every outbound send, including errors and background traffic, on one ledger. Authentication or throttling ends all further sends for the run. An entitlement denial stops dependent cases for the affected operation. Other independent cases may continue under the ledger. Missing evidence leaves a capability unverified and a denied endpoint remains blocked. Reopen the affected contract for changes to query binding, identity, value types, financial semantics, qualifications or completeness. Custom DCF can proceed default-only after review of a revised contract that omits beta everywhere. A denied or unresolved lane stays outside the accepted milestone. At joins, a dependency resolves when the named unit is independently accepted or its affected operation is explicitly recorded as blocked or unverified and excluded. This exception applies only to individual operations. Shared transport, validation, accounting and release prerequisites still require passing evidence for every included operation.

The controller owns shared edits, the live ledger, installs, joins, heavy checks and selective commits. Only the five named adapter leaves can fan out, with at most two disjoint implementers and one reviewer in addition to the controller. Review each unit independently and verify it fresh before acceptance. In its completion commit, reconcile the task checkbox and affected README, roadmap and documentation checkboxes with observed results, keeping blocked items open. Each production leaf must pass the whole-file complexity gate using exact base/head or changed-file manifests for each affected repository. Enforce 400 physical lines/file, 300 logical units/Python or JS/TS file and 50 logical units/function. Run one heavy suite/build at a time, up to three independent verification processes, at most two xdist workers and one isolated headless Playwright worker. Record commands, results and exact source or image identities. Keep raw provider captures, keys and browser state private.

## 1. Isolate the sources and freeze the contracts

- [x] 1.1 Verify source and complexity foundations
  - Resolve the design’s pinned root, data API and Workspace baselines in owned checkouts or disposable staging. Record local baselines, lock/source, recorded archive provenance, notices and installed provenance. Use the reviewed expansion inventory and its member evidence to confirm the five operations need new contracts. Access to the historical Batch A tarball is needed only if its members must be re-examined. Reconcile the actual installed FMP set against the original 21 and Batch B’s eight.
  - Prove the locked Python and patched Node toolchain, disposable verification install and executable scoped complexity checker before production changes. Add applicable maintained ownership to `.kiro/complexity/{qopenbb,data-api,workspace}.json` and update `.kiro/complexity-budgets.json` if needed. Record whole-file scoped acceptance at 400/300/50 and any reviewed inventory exclusions. Use the established `python -m tools.quality.complexity --check` invocation and manifest options in [complexity checks](../../../docs/complexity.md).
  - _Boundary: Controller · checkout and toolchain staging, complexity inventory and baseline evidence_
  - _Requirements: 1.1, 5.5, 6.5, 8.1, 8.5_

- [x] 1.2 Rehearse the request ledger and stop conditions
  - Pin exact symbols, periods, per-statement limits, default and override beta queries and planned browser cases in the ledger before the first send. Use MSFT for the matched custom pair with beta `1.0`. Choose source-suitable statement listings and a quarterly cash-flow case that can characterize cumulative basis. Pin private credential readiness and allow a focused non-USD contrast from the diagnosed reserve.
  - Rehearse metering at the single outbound send boundary without network or real keys, including errors, startup and browser traffic. Prove isolated profile, disposable state, disabled polling, fail-closed ceiling and zero real sends before credential injection. Record skipped case prerequisites and redacted readiness.
  - Scope consists of temporary setup and verification evidence, which are excluded from production caps.
  - _Boundary: Controller · private ledger and request instrumentation_
  - _Depends: 1.1_
  - _Requirements: 2.4, 2.6, 7.1, 7.2, 7.3, 8.4_

- [ ] 1.3 Characterize and freeze both valuation operations
  - Use up to three of the nine direct sends for one standard DCF and two MSFT custom calls. Skip the override if its baseline is unusable. Freeze dated documentation, exact parameters, key/type/scale/mapped and unmapped field observations, required identity, output basis, source uncertainty and maximum rows in sanitized fixtures. Preserve valuation date, reference price date, provider year and observed retrieval time independently.
  - Verify exact beta echo on matched unique issuer/year sets, distinguish mismatch and unavailable confirmation, and require documented binding before accepting the override. An echo only acknowledges the input. Freeze default behavior, exact tokens, unknown currency/bases, duplicate year and over-bound cases. Record sanitized receipts and hashes with per-operation status.
  - Scope consists of fixture and evidence files excluded from production caps.
  - _Boundary: Controller · tests/providers/fixtures/fmp_batch_c/valuations/ and private valuation receipts_
  - _Depends: 1.2_
  - _Requirements: 1.2, 2.2, 2.4, 2.5, 2.6, 3.3, 4.1, 4.2, 4.5, 4.6, 4.7, 8.3, 8.4_

- [ ] 1.4 Characterize and freeze all three statement operations
  - Use up to six direct sends, one annual and one quarter for each operation. Confirm independent wire support for exact period and limit forwarding. Freeze envelope paths, admitted fact types/contexts, date precision, complete filing identity, unresolved vintage identity and unknown source completeness. Account for possible non-USD contrast using the diagnosed reserve.
  - Produce annual and quarterly fixtures per operation, including balance instant, cash-flow YTD or unknown duration, same-period distinct filings, exact duplicate and conflicting complete identities, frequency conflicts, zero/null/omitted facts and adverse shapes. Record evidence for known durations, reporting currency and units. Keep point-in-time eligibility unverified where vintage/availability evidence is incomplete.
  - Freeze the statement query at required symbol, annual default or quarter, and limit 1–20 with default 5. Scope consists of fixture and evidence files excluded from production caps.
  - _Boundary: Controller · tests/providers/fixtures/fmp_batch_c/statements/ and private statement receipts_
  - _Depends: 1.3_
  - _Requirements: 1.2, 2.3, 2.4, 2.5, 2.6, 3.3, 4.1, 4.2, 4.3, 4.5, 4.6, 8.3, 8.4_

- [ ] 1.5 Review and hand off the frozen contracts
  - Independently review each operation’s source semantics, exact-number/schema examples, acquisition failures, empty-array and typed missing-data fixtures, and query/row bindings. Record allowed, unresolved and blocked cases explicitly. Freeze stable widget/dataset IDs and expected native route/renderer inputs. Identify operation-specific reopening conditions before dispatch.
  - Create one read-only handoff for the two-worker queue with owned paths, exact fixtures, test commands and join criteria. Each accepted lane receives frozen fixtures, transport interfaces and independent acceptance. Scope consists of handoffs, fixtures and evidence excluded from production caps.
  - _Boundary: Controller · tests/providers/fixtures/fmp_batch_c/handoffs.json, shared fixtures and freeze evidence_
  - _Depends: 1.3, 1.4_
  - _Requirements: 1.1, 1.2, 1.3, 2.6, 4.5, 5.4, 6.1, 6.3, 7.2, 8.4_

## 2. Implement shared exact acquisition and admission

- [ ] 2.1 Acquire exact JSON through the existing safe transport
  - Add the Batch C opt-in to safe FMP GET acquisition. Bound the decompressed read to 4 MiB, decoding depth to 32 and numeric tokens to 128 characters. Reject duplicate members at every depth and nonfinite constants. Retain exact number lexemes with integer or decimal kinds and preserve text, booleans, null and absence.
  - Prove unchanged default decoding, one GET with bounded timeout, no redirects/retries/fallback, safe failure categories and retry interval. Exercise raw numeric fidelity and malformed/duplicate/oversized payloads. Permit the success-empty opt-in only for a genuine top-level empty array. Preserve existing typed absent-payload behavior.
  - Record scoped whole-file 400/300/50 compliance.
  - _Boundary: Controller · API openbb_platform/providers/fmp/openbb_fmp/utils/{helpers,exact_financial_json}.py and root tests/providers/test_fmp_exact_financial_json.py_
  - _Depends: 1.5_
  - _Requirements: 4.2, 4.5, 5.3, 5.5, 7.1, 7.2, 7.3, 7.4, 8.4_

- [ ] 2.2 Preserve decimal beta through native admission
  - Apply positive beta admission and fidelity work only when 1.5 accepts the override. For a reviewed default-only contract, omit the beta parameter and verify that an explicit beta is rejected before transport. If custom DCF is excluded, record that the beta-specific unit is inapplicable.
  - Prove the scoped opt-in through raw admission and generated dependency parsing. Admit only bounded ASCII numeric tokens on HTTP using exact decimal validation, and retain the actual HTTP token through native parsing, effective metadata and transport. Use bounded Decimal/int or shortest round-tripping float representation for typed SDK/direct callers. Reject typed strings, bool/null, nonfinites, repeated/unknown controls, unsupported period/provider, multiple symbols and out-of-range beta before send.
  - Use a fixture query to exercise omitted/zero/exponent/trailing-zero/precise beta and near-but-unequal values before the real app join. Preserve previous integer/date/quarter behavior. If a scoped runtime helper is necessary, add it to the packaging allowlists and verify image-input coverage in this same unit.
  - Record scoped whole-file 400/300/50 compliance.
  - _Boundary: Controller · root services/data-api/qopenbb_data/financial_query_policy.py and optional scoped HTTP helper, pipeline/qopenbb_ci/runtime_inputs.py, tests/delivery/test_data_image.py and tests/providers/test_fmp_batch_c_admission.py. Controller alone owns any narrowly scoped native admission/generation seam identified by this fixture review_
  - _Depends: 2.1_
  - _Requirements: 2.2, 2.4, 5.1, 5.2, 5.3, 6.1, 7.1, 7.3_

- [ ] 2.3 Share typed statement identities and fact mapping
  - Run this unit for eligible statements only. If all three are excluded, record that outcome and proceed with eligible valuation work.
  - Implement wire-independent statement data and a separate shared FMP mapper. Preserve distinct listing/issuer/statement coordinates, filing, accession, fiscal context and exact fact values. Preserve tag, taxonomy, dimensions, unit/scale/currency and temporal context only where evidenced. Require supported row periods and validate all rows before clipping.
  - Prove the 4,096-fact bound, source order, exact source numbers, zero/null/omission, invalid known values, foreign symbol, unresolved vintage identity and repeated complete identity. Test identical duplicate and conflicting records separately, retaining legitimate distinct vintages. Record direct effective query, retrieval, counts and observed clipping. A result equal to the limit alone leaves completeness unknown.
  - Record scoped whole-file 400/300/50 compliance.
  - _Boundary: Controller · API openbb_platform/{core/openbb_core/provider/standard_models,providers/fmp/openbb_fmp/models}/statement_as_reported.py and root tests/providers/test_fmp_statement_as_reported.py_
  - _Depends: 2.1_
  - _Requirements: 2.3, 2.5, 3.3, 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 5.4, 7.3_

## 3. Implement the five independent adapters

Each lane owns only the two API modules named for its operation stem below (one in `openbb_platform/core/openbb_core/provider/standard_models/` and one in `openbb_platform/providers/fmp/openbb_fmp/models/`) and its matching root `tests/providers/test_fmp_<stem>.py`. Shared modules, fixtures, package allowlists, registration, routing and catalog remain controller-owned. Each lane uses the production Fetcher and intercepted raw transport, asserting exact payload and metadata, zero sends for invalid admission and one send for an admitted acquisition.

- [ ] 3.1 (P) Deliver the standard DCF snapshot
  - Prove zero or one validated row and reject oversized/foreign/malformed results. Preserve exact provider value and valuation date. Map any frozen reference price and per-share evidence separately. Leave unknown currency and market observation date explicit.
  - Record scoped whole-file 400/300/50 compliance.
  - _Boundary: Adapter worker · discounted_cash_flow modules and test_
  - _Depends: 2.1_
  - _Requirements: 2.2, 2.5, 3.3, 4.1, 4.2, 4.5, 4.7, 7.3_

- [ ] 3.2 (P) Deliver the custom DCF result
  - Validate required exact equity value per share, selected normalised symbol and canonical four-digit provider year before preserving source order up to 25. Reject duplicate integer/string year identity. Preserve exact frozen assumption/output keys, value tokens and their evidenced or unknown bases and valuation dates.
  - Test default omission. With an accepted override, test separate requested and returned beta tokens, exact numeric equality and near-unequal values without tolerance or another request. Exercise unavailable and mismatched acknowledgement. Use the reviewed default-only contract if applicable.
  - Record scoped whole-file 400/300/50 compliance.
  - _Boundary: Adapter worker · custom_discounted_cash_flow modules and test_
  - _Depends: 2.1, 2.2_
  - _Requirements: 2.2, 2.4, 2.5, 3.3, 4.1, 4.2, 4.5, 4.7, 7.3_

- [ ] 3.3 (P) Deliver as-reported income statements
  - Send exact admitted symbol, period and limit in one request. Prove annual/quarter source labels and duration known only from evidence, preserve native tags and separate filing vintages, and exercise conflicting period/facts and zero/null/omitted cases.
  - Record scoped whole-file 400/300/50 compliance.
  - _Boundary: Adapter worker · income_statement_as_reported modules and test_
  - _Depends: 2.3_
  - _Requirements: 2.3, 2.4, 2.5, 3.3, 4.1, 4.2, 4.3, 4.5, 4.6, 7.3_

- [ ] 3.4 (P) Deliver as-reported balance sheets
  - Send exact admitted symbol, period and limit in one request. Prove annual and quarterly balance snapshots at period end, distinct per-fact context and unknown units. Keep same-period distinct vintages and reject repeated complete identity.
  - Record scoped whole-file 400/300/50 compliance.
  - _Boundary: Adapter worker · balance_sheet_as_reported modules and test_
  - _Depends: 2.3_
  - _Requirements: 2.3, 2.4, 2.5, 3.3, 4.1, 4.2, 4.3, 4.5, 4.6, 7.3_

- [ ] 3.5 (P) Deliver as-reported cash-flow statements
  - Send exact admitted symbol, period and limit in one request. Prove annual and quarterly label handling, YTD versus unknown duration and beginning/end cash instant semantics where evidenced. Compare source order and precision without deriving discrete quarters.
  - Record scoped whole-file 400/300/50 compliance.
  - _Boundary: Adapter worker · cash_flow_statement_as_reported modules and test_
  - _Depends: 2.3_
  - _Requirements: 2.3, 2.4, 2.5, 3.3, 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 7.3_

## 4. Join installed routes, discovery and Workspace

- [ ] 4.1 Register accepted models and bind a single native router
  - Add frozen operations to the installed registry and annotate selected query/data pairs. Use the new single prefix-empty `financial_inputs_router.py` instance for the existing enterprise command as well as Batch C. Preserve the one child inclusion in `equity_router.py`. Verify repeated application construction and existing enterprise, legacy reported and normalised statement paths.
  - Reconcile exact installed types, source bytes, path and unique native bindings for the 29 baseline FMP identities plus accepted additions, 34 when all five join. Update shared exact-set expectations without weakening historical A/B membership, archive or source-origin assertions. Verify unaffected FMP, Intrinio, FRED and Yahoo surfaces or documented unavailable state against the pinned baseline.
  - Record scoped whole-file 400/300/50 compliance. Keep the 534-line main fundamental router outside the edit.
  - _Boundary: Controller · API provider.py, equity/fundamental/{financial_inputs_router,enterprise_router}.py, root tests/providers/fmp_actual_join_support.py and tests/providers/{test_discovery,test_fmp_batch_a_registration,test_fmp_batch_b_registration,test_fmp_batch_c_registration}.py_
  - _Depends: 3.1, 3.2, 3.3, 3.4, 3.5_
  - _Requirements: 1.1, 1.3, 5.1, 5.4, 5.5, 6.3, 6.5, 8.1_

- [ ] 4.2 Verify mounted HTTP admission and result serialization
  - Exercise actual app with production installed classes, raw mocked transport and explicit FMP selection. Prove no send for rejection and one for accepted calls. For accepted beta, assert exact forwarding and metadata. For default-only, assert rejection before any send. Verify `9007199254740993`, precise decimals, numeric kind, zero/null/omission and date precision. Distinguish real empty-array success with metadata from typed empty 204 with no metadata and malformed/duplicate/conflicting responses.
  - Verify safe failures, actionable retry interval, unknown source completeness and provenance, and schema agreement with selected routes. Any scoped projection changes must preserve the installed baseline and pass whole-file 400/300/50 checks. Hand durable cases to the SDK comparison in 4.3.
  - _Boundary: Controller · services/data-api/qopenbb_data/{financial_openapi,financial_catalog}.py and tests/providers/test_fmp_batch_c_installed_join.py_
  - _Depends: 4.1_
  - _Requirements: 1.1, 2.4, 2.5, 3.3, 4.1, 4.5, 5.1, 5.2, 5.3, 6.2, 7.1, 7.2, 7.3, 7.4_

- [ ] 4.3 Verify SDK and Fetcher parity against installed source
  - Run generated SDK discovery and execute each eligible command with raw intercepted transport. For accepted beta, rehearse SDK Decimal and direct Fetcher near-unequal beta with exact forwarding and serialization. For default-only, verify explicit beta fails before transport at both entries. Check strict typed rejection, native provider resolution and no fallback for eligible routes. Confirm metadata and date/token round trips and safe missing/invalid/failure outcomes against HTTP.
  - Run focused shared admission/transport, installed join and FMP/Intrinio/FRED/Yahoo regressions. Record command counts and exact installed source. Test/evidence scope is excluded from production caps. Return any repair to the owning unit for a fresh scoped 400/300/50 check.
  - _Boundary: Controller · tests/providers/test_fmp_batch_c_sdk.py and installed parity evidence_
  - _Depends: 4.2_
  - _Requirements: 2.4, 4.1, 4.5, 5.1, 5.2, 5.3, 5.4, 5.5, 6.2, 6.5, 7.1, 7.3, 8.4_

- [ ] 4.4 Project and regenerate the native consumer catalog
  - For default-only custom DCF, omit the beta control from the schema and widget. Bind only frozen selected-provider variants to stable widgets and generated query/result contracts. Expose provider, bounds, defaults, exact numeric kind/string semantics, date and native-fact shape. Documented/installed/entitled/browser evidence remains distinct. Keep 204 absent without fabricated metadata. Preserve all baseline schemas, paths, widget IDs, defaults and legacy widgets. Compare deterministic generation twice from an exact-source installed image.
  - Run the portable catalog CLI, exact-set/schema checks, historical Batch A/B consumers and compatibility diff. Pin API source for generation and give Workspace the generated contracts. Review compatible additions and explain any baseline differences before accepting. Record scoped whole-file 400/300/50 compliance.
  - _Boundary: Controller · sources.lock.json API pin, contracts/, pipeline/qopenbb_ci/{catalog,catalog_cli,catalog_batch_c}.py, conditional catalog_financial.py and tests/contracts/test_fmp_batch_c_consumers.py_
  - _Depends: 4.3_
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 5.5, 6.1, 6.2, 6.3, 6.5, 8.1_

- [ ] 4.5 Verify renderer fit and bind native widget views
  - Exercise standard and custom valuation rows and a nested statement fact collection using the existing Workspace table on the generated descriptors. Record whether exact text survives and whether tag, filing/fiscal context, provenance and unknown units are legible. If generic presentation fails, have the controller review and freeze the smallest detail view and exact writable paths before Workspace production work.
  - Deliver readable exact values with original token inspection/copy if display rounds, provider origin and assumption versus output context, and a readable native fact view. Use normal widget acquisition and save query/view choices. Preserve established refresh/failure behavior, including stale acquisition time and no invented 204 metadata. Prove existing saved widgets reopen unchanged.
  - Record scoped whole-file 400/300/50 compliance for any maintained Workspace edits, or evidence of generic renderer fit when no production edits are required. If renderer work exceeds this leaf, review a split of presentation and host wiring before starting it.
  - _Boundary: Controller · Workspace renderer selection and exclusively assigned Workspace paths recorded before editing. Root catalog/config stays with its assigned owner_
  - _Depends: 4.4_
  - _Requirements: 4.1, 4.2, 4.5, 6.1, 6.2, 6.3, 7.1, 7.5_

- [ ] 4.6 Exercise offline Workspace acquisition, persistence and fidelity
  - Add a selected runner suite using the existing financial Playwright configuration and mounted app. Verify initial acquisition, save/reopen and relevant refresh errors for standard DCF, custom DCF and quarterly cash flow with offline interception. Verify native facts context, selected query restoration, missing/empty behavior and exact output tokens. With an accepted override, verify near-unequal beta tokens that can round to the same display. For default-only, verify the absence of a beta control on launch, save and reopen. Skip cases for excluded routes.
  - Use one hidden isolated browser and private outputs. Prove baseline widgets unchanged. Pin accepted Workspace source and verify the compatible generated catalog on the exact candidate. Check scoped 400/300/50 compliance on maintained selector/config changes.
  - _Boundary: Controller · tests/e2e/fmp-batch-c-workspace.spec.mts, verification/financial-workspace.config.ts and sources.lock.json Workspace pin_
  - _Depends: 4.5_
  - _Requirements: 4.1, 4.5, 6.2, 6.3, 7.1, 7.2, 7.5, 8.1, 8.4_

## 5. Verify live eligibility and publish the accepted milestone

- [ ] 5.1 Compare installed native responses to their own source receipts
  - Stage a Dagger-built isolated candidate from the reviewed source, confirm lock/image and contract hashes and prove ledger hookup and readiness with no sends. Use up to nine installed sends on the characterized matrix after offline parity. Compare each response to its own receipt including query, identity, raw values, dates, financial context, units and acquisition metadata.
  - Confirm native default and beta 1.0 cases where approved, and both annual and quarter for each accepted statement. Record exact inputs, image/runtime identity, retrieval time, counts and private receipt hashes. Retain skipped cases and their prerequisites. Log diagnosed reserve usage against the common ceiling. Evidence scope is excluded from production caps.
  - _Boundary: Controller · isolated installed candidate and private native receipts_
  - _Depends: 1.2, 4.3, 4.6_
  - _Requirements: 1.2, 2.2, 2.3, 2.5, 2.6, 3.3, 4.1, 4.2, 4.3, 4.7, 8.1, 8.3, 8.4_

- [ ] 5.2 Verify representative live Workspace journeys
  - Use up to six Workspace sends for initial acquisition and saved reopen of standard DCF, custom DCF with supported beta and quarterly as-reported cash flow. Require the respective installed live acceptance. Skip the custom beta browser journey if only defaults are accepted or the custom operation is excluded. Record the unused allocation. Keep other widgets unverified unless covered by independently reviewed relevant evidence.
  - Compare values and meaning to the candidate’s own acquisitions. Verify the selected symbol, provider, query, fiscal/filing context and unknowns. Record source/contract identities, actual browser and background sends and intentionally skipped cases. Use only the shared six-send diagnosed reserve for observed discrepancies. Evidence scope is excluded from production caps.
  - _Boundary: Controller · isolated Workspace journey and private browser receipts_
  - _Depends: 5.1_
  - _Requirements: 1.2, 2.6, 4.1, 4.2, 6.2, 6.3, 7.1, 7.2, 8.3, 8.4_

- [ ] 5.3 Reconcile coverage and verify the release source
  - If an operation loses eligibility after integration, regenerate the accepted subset and its discovery status, rebuild the affected candidate, and verify its installed identities, runtime payload equivalence and offline compatibility before publication. Any changed runtime behavior needs fresh affected financial checks within the remaining allowance. With insufficient evidence or budget, leave release of that capability open.
  - Reconcile actual test paths, criteria and reviewed evidence in `.kiro/breadth.toml`, `docs/reference/provider-coverage.json` and relevant coverage documentation. Preserve prior reviewed coverage and open work. Publish sanitized comparison receipts, hashes and scope in the reviewed mirror. Audit raw evidence exclusions and the sync manifest.
  - Run portable check-only CI at exact source pins, including relevant packaging, provider, consumer and Workspace regressions. Audit joined complexity across all changed trees at 400/300/50 and confirm immutable revisions. Only the independently accepted source set may proceed to publication. Any production repair returns to its owning unit.
  - _Boundary: Controller · breadth, provider coverage, maintained verification evidence and check-only release gate_
  - _Depends: 5.1, 5.2_
  - _Requirements: 1.2, 1.3, 1.4, 2.6, 6.3, 7.2, 8.1, 8.3, 8.4, 8.5_

- [ ] 5.4 Verify the published milestone from immutable images
  - Use the existing milestone workflow at an accepted main revision with Dagger-only image builds and portable verification/publication. Verify manifest, source provenance, release asset hashes, published digests and pullability.
  - Exercise identified images with network-isolated installed API cases and packaged Workspace/API readiness with zero real FMP sends. Record release and cleanup receipts and separate local live/browser evidence from packaged checks. Scope consists of release verification and evidence, which are excluded from production caps. Private-server deployment remains a separate operation.
  - _Boundary: Controller · existing prototype workflow and immutable publication receipts_
  - _Depends: 5.3_
  - _Requirements: 6.5, 7.2, 8.1, 8.2, 8.5_
