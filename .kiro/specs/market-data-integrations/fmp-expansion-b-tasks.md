# Batch B FMP implementation plan

The [design](fmp-expansion-b-design.md) and [independent review](fmp-expansion-b-review.md) define eight operations. The owner approved execution of the [reviewed task graph](fmp-expansion-b-task-review.md) and a ceiling of 36 live FMP requests. Each checkbox records independent review and fresh verification.

## Execution contract

Use D:/BuildArtifacts/QOpenBB/fmp-expansion-b/root and isolated sibling API/Workspace worktrees. The approved design pins all three baselines. Reuse project delegation, testing, CI and documentation steering. Every unit targets 1–3 hours of engineering effort. A passing unit requires independent review, fresh scoped verification, recorded evidence and selective commit. Freeze edits before staging. Run one heavy suite or install at a time. Only the eight adapter tasks marked (P) may overlap, at most two implementers with one fresh reviewer and controller. Other steps are serial. Hold affected lanes on a contract change. Controller owns shared files, registry, evidence and joins. Frozen fixtures are read-only to adapter workers. Every handoff names exact owned paths, commands, constraints and prerequisites. Include archive provenance, baseline financial behavior, unit/period and null semantics in adapter reviews. Use Sol for routine units and Astra for financial and integration review.

Use product limits and the eight endpoint-specific public contracts in the design. At the live gates the four contrasts cover dividend dates, a reverse split, estimated vs actual earnings and transcript period. Unused Batch A quota does not transfer. Preserve accepted runtime state. The task groups contribute to the identified umbrella criteria. Existing first-slice, DCF, macro/futures, valuation-input and multi-provider obligations (2.1, 2.2, 3.4, 3.5, 4.7, 4.8, 5.4, 5.5, 5.6) retain their existing owners. Requirement 4.3 is a baseline regression check. No umbrella criterion is closed by generating this plan.

## 1. Foundation and contract freeze

- [x] 1.1 Isolate the three source trees and enforce the complexity scope
  - Resolve Batch B root, data-api and workspace worktrees and junctions. Verify baseline revisions against the approved design and source tarball SHA-256 5f6f27af6283075912df42f373c45ed37bc6970097342ed73110fb6101be5517. Record eight members, notices and hashes.
  - Run tools.quality.complexity --check with actual repository roots and explicit base/head or changed manifests. Prove missing input fails. Record exact commands, resolved paths and a baseline for existing oversized host files before edits.
  - Run the scoped whole-file complexity check on all maintained production edits. Record compliance with 400 physical lines/file, 300 logical units/file and 50/function.
  - _Boundary: Controller · source recovery, .kiro/complexity/ and budgets_
  - _Requirements: 8.1, 8.5_

- [x] 1.2 Freeze event queries, rows and financial meanings
  - Compare the five retained models with the owned standards and dated official docs. Freeze validation/serialization schemas, stable URL parameters, one-call limits, effective filters, source identity and row attribution. Include multi-day boundaries, duplicate event dates and reported vs estimated values.
  - Record the unit evidence for dividend yield, adjusted-amount nullability and split orientation. A missing unit decision blocks the affected adapter. Record clipping order and caps and distinguish a locally empty historical window from an empty acquisition.
  - This unit produces tests, contracts, documentation or evidence, excluded from production caps. Any required production repair returns to its owning unit and needs fresh 400/300/50 verification.
  - _Boundary: Controller · tests/providers/fixtures/fmp_batch_b/events/_
  - _Depends: 1.1_
  - _Requirements: 2.3, 2.4, 2.5, 4.1, 4.2, 4.4, 4.5, 4.6_

- [ ] 1.3 Freeze three document contracts
  - Freeze input and serialized row schemas, aliases, source attribution, safe links, content_status and criteria for partial/full/unknown/metadata-only. Include strict transcript coordinates, blank body, foreign and duplicate rows, CIK and distinct index/document URLs.
  - Characterize and record the current time loss in the inherited filings validator and transcript date-only standard. Freeze expected public serialization fixtures for non-midnight, offset-bearing and timezone-unspecified inputs. Accept this freeze when the observed baseline and expected values are recorded. Tasks 3.7 and 3.8 own the runtime corrections, and 4.2 verifies installed serialization.
  - This unit produces tests, contracts, documentation or evidence, excluded from production caps. Any required production repair returns to its owning unit and needs fresh 400/300/50 verification.
  - _Boundary: Controller · tests/providers/fixtures/fmp_batch_b/documents/_
  - _Depends: 1.2_
  - _Requirements: 2.3, 2.4, 3.1, 3.2, 3.3, 4.1, 4.5, 4.6, 6.4_

- [ ] 1.4 Freeze Workspace integration and lane handoffs
  - Trace an authenticated endpoint-backed widget through renderer registration, typing, validation, data acquisition, persisted query settings and export/import. Identify exact host paths, endpoints, IDs, inputs, output shape and catalog inclusion for eight widgets. Packaged app defaults must remain usable.
  - Record exclusive paths, checked commands and reviewers per task. Measure whole existing shared files, design cohesive extraction or obtain a narrow reviewed exception before edits. Frozen handoffs must leave no unowned registration, storage or catalog steps.
  - This unit produces tests, contracts, documentation or evidence, excluded from production caps. Any required production repair returns to its owning unit and needs fresh 400/300/50 verification.
  - _Boundary: Controller · host inventory and tests/providers/fixtures/fmp_batch_b/handoffs.json_
  - _Depends: 1.3_
  - _Requirements: 6.1, 6.2, 6.3, 6.4, 8.1_

## 2. Installation and public input admission

- [ ] 2.1 Install the owned company-news extension
  - Compose only the retained company command. Review feedparser/lxml/core extras and lock the owned openbb-news 2.0.0 path with the pinned toolchain. Update installed-origin and image dependency assertions. Retain a deterministic locked install from a clean tree.
  - Verify extension import and entry point, absence of new RSS/world surfaces and unchanged installed routes. Use an isolated fixture registry to characterize company registration if the real provider has not yet joined. Assert real route discovery in 4.2.
  - Run the scoped whole-file complexity check on all maintained production edits. Record compliance with 400 physical lines/file, 300 logical units/file and 50/function.
  - _Boundary: Controller · services/data-api/{pyproject.toml,uv.lock}, owned news extension entry point and installation tests_
  - _Depends: 1.4_
  - _Requirements: 1.1, 1.3, 6.5, 7.2, 8.1_

- [ ] 2.2 Prove strict public admission before provider dispatch
  - Use selected FMP fixture variants to exercise generated SDK, mounted HTTP and raw Fetcher admission. Cover valid HTTP quarters 1–4, strings on the wire, explicit bool/null in typed callers, out-of-range quarter, repeated scalars, unknown keys, date bounds, default precedence and unsupported multi-symbols.
  - Freeze a bounded int query type or narrowly repair financial_query_policy.py for the actual quarter annotation. Assert one mocked send on valid calls, zero on rejection, existing 21-provider-model behavior and SDK/REST provider selection. Repeat with real registered classes at the join.
  - Run the scoped whole-file complexity check on all maintained production edits. Record compliance with 400 physical lines/file, 300 logical units/file and 50/function.
  - _Boundary: Controller · SDK admission, root HTTP policy and dedicated admission tests_
  - _Depends: 2.1_
  - _Requirements: 2.4, 5.1, 5.2, 5.3, 7.1, 7.3, 7.5_

## 3. Eight disjoint FMP adapters

- [ ] 3.1 (P) Historical dividends
  - Preserve ex-, record, declaration and payment dates, adjusted/unadjusted amount and zero yield. Test optional local filters after the upstream limit, empty acquisition vs empty filter and currency uncertainty.
  - Exercise the frozen schema via the production Fetcher, intercepted safe transport and typed metadata. Assert zero sends for invalid input, exactly one for success, and distinguish safe errors, empty/malformed responses and absence of results. Verify source order, applicable clipping and effective query.
  - Run the scoped whole-file complexity check on all maintained production edits. Record compliance with 400 physical lines/file, 300 logical units/file and 50/function.
  - _Boundary: Adapter worker · openbb_platform/providers/fmp/openbb_fmp/models/historical_dividends.py and root tests/providers/test_fmp_historical_dividends.py_
  - _Depends: 2.2_
  - _Requirements: 2.3, 2.4, 2.5, 4.1, 4.2, 4.5, 7.1, 7.3_

- [ ] 3.2 (P) Historical splits
  - Require one symbol. Preserve new:old numerator/denominator, require finite positive supplied components, check foreign rows and the 100-row cap without repricing history.
  - Exercise the frozen schema via the production Fetcher, intercepted safe transport and typed metadata. Assert zero sends for invalid input, exactly one for success, and distinguish safe errors, empty/malformed responses and absence of results. Verify source order, applicable clipping and effective query.
  - Run the scoped whole-file complexity check on all maintained production edits. Record compliance with 400 physical lines/file, 300 logical units/file and 50/function.
  - _Boundary: Adapter worker · openbb_platform/providers/fmp/openbb_fmp/models/historical_splits.py and root tests/providers/test_fmp_historical_splits.py_
  - _Depends: 2.2_
  - _Requirements: 2.3, 2.4, 2.5, 4.1, 4.2, 4.5, 7.1, 7.3_

- [ ] 3.3 (P) Earnings calendar
  - Check inclusive seven-day bounds and exact from/to, no company filter, at most 250 rows. Keep actual, estimated, missing and zero EPS/revenue distinct and leave event confirmation unknown.
  - Exercise the frozen schema via the production Fetcher, intercepted safe transport and typed metadata. Assert zero sends for invalid input, exactly one for success, and distinguish safe errors, empty/malformed responses and absence of results. Verify source order, applicable clipping and effective query.
  - Run the scoped whole-file complexity check on all maintained production edits. Record compliance with 400 physical lines/file, 300 logical units/file and 50/function.
  - _Boundary: Adapter worker · openbb_platform/providers/fmp/openbb_fmp/models/calendar_earnings.py and root tests/providers/test_fmp_calendar_earnings.py_
  - _Depends: 2.2_
  - _Requirements: 2.3, 2.4, 2.5, 4.1, 4.2, 4.5, 7.1, 7.3_

- [ ] 3.4 (P) Dividend calendar
  - Keep each date role, nullable adjusted/actual amount and yield scale. Exercise market-wide symbol attribution, blank optional dates, an eighth day rejection and observed clipping above 250.
  - Exercise the frozen schema via the production Fetcher, intercepted safe transport and typed metadata. Assert zero sends for invalid input, exactly one for success, and distinguish safe errors, empty/malformed responses and absence of results. Verify source order, applicable clipping and effective query.
  - Run the scoped whole-file complexity check on all maintained production edits. Record compliance with 400 physical lines/file, 300 logical units/file and 50/function.
  - _Boundary: Adapter worker · openbb_platform/providers/fmp/openbb_fmp/models/calendar_dividend.py and root tests/providers/test_fmp_calendar_dividend.py_
  - _Depends: 2.2_
  - _Requirements: 2.3, 2.4, 2.5, 4.1, 4.2, 4.5, 7.1, 7.3_

- [ ] 3.5 (P) Split calendar
  - Require dated market-wide rows with symbol and positive finite ratio components. Exercise a reverse split, a missing required component, a seven-day window and the 250-row cutoff.
  - Exercise the frozen schema via the production Fetcher, intercepted safe transport and typed metadata. Assert zero sends for invalid input, exactly one for success, and distinguish safe errors, empty/malformed responses and absence of results. Verify source order, applicable clipping and effective query.
  - Run the scoped whole-file complexity check on all maintained production edits. Record compliance with 400 physical lines/file, 300 logical units/file and 50/function.
  - _Boundary: Adapter worker · openbb_platform/providers/fmp/openbb_fmp/models/calendar_splits.py and root tests/providers/test_fmp_calendar_splits.py_
  - _Depends: 2.2_
  - _Requirements: 2.3, 2.4, 2.5, 4.1, 4.2, 4.5, 7.1, 7.3_

- [ ] 3.6 (P) Company stock news
  - Send only news/stock with symbols. Check paired dates, page/limit, attribution vs author, partial excerpt and headline-only status. Preserve link and literal text without retrieving articles or images.
  - Exercise the frozen schema via the production Fetcher, intercepted safe transport and typed metadata. Assert zero sends for invalid input, exactly one for success, and distinguish safe errors, empty/malformed responses and absence of results. Verify source order, applicable clipping and effective query.
  - Run the scoped whole-file complexity check on all maintained production edits. Record compliance with 400 physical lines/file, 300 logical units/file and 50/function.
  - _Boundary: Adapter worker · openbb_platform/providers/fmp/openbb_fmp/models/company_news.py and root tests/providers/test_fmp_company_news.py_
  - _Depends: 2.2_
  - _Requirements: 2.3, 2.4, 2.5, 4.1, 4.2, 4.5, 7.1, 7.3, 6.4_

- [ ] 3.7 (P) Earnings-call transcript
  - Implement the provider-specific timestamp-preserving transcript mapping alongside the standard civil date. Verify exact symbol, year and quarter, duplicate and wrong-period failure, nonblank verbatim text and original event-time precision. Valid empty acquisition means unavailable. Zero fallback/discovery calls.
  - Exercise the frozen schema via the production Fetcher, intercepted safe transport and typed metadata. Assert zero sends for invalid input, exactly one for success, and distinguish safe errors, empty/malformed responses and absence of results. Verify source order, applicable clipping and effective query.
  - Run the scoped whole-file complexity check on all maintained production edits. Record compliance with 400 physical lines/file, 300 logical units/file and 50/function.
  - _Boundary: Adapter worker · openbb_platform/providers/fmp/openbb_fmp/models/earnings_call_transcript.py and root tests/providers/test_fmp_earnings_call_transcript.py_
  - _Depends: 2.2_
  - _Requirements: 2.3, 2.4, 2.5, 4.1, 4.2, 4.5, 7.1, 7.3, 6.4_

- [ ] 3.8 (P) Company filings
  - Implement the FMP provider override that bypasses inherited accepted-date truncation while preserving filing-date semantics. Test explicit symbol, inclusive dates, page zero, rejection beyond bounds, form type output, leading-zero CIK, filing date vs accepted timestamp with offset, and distinct links. No filing-body fetch.
  - Exercise the frozen schema via the production Fetcher, intercepted safe transport and typed metadata. Assert zero sends for invalid input, exactly one for success, and distinguish safe errors, empty/malformed responses and absence of results. Verify source order, applicable clipping and effective query.
  - Run the scoped whole-file complexity check on all maintained production edits. Record compliance with 400 physical lines/file, 300 logical units/file and 50/function.
  - _Boundary: Adapter worker · openbb_platform/providers/fmp/openbb_fmp/models/company_filings.py and root tests/providers/test_fmp_company_filings.py_
  - _Depends: 2.2_
  - _Requirements: 2.3, 2.4, 2.5, 4.1, 4.2, 4.5, 7.1, 7.3, 6.4_

## 4. Installed application and consumer integration

- [ ] 4.1 Join the eight adapters into the real registry
  - Check archive hashes and actual installed fetcher types and origin. Extend the exact-set assertion to preserve the original 21 identities and add the eight reviewed ones. Refresh API revision and source pin once the fork work is accepted.
  - In an isolated install enumerate exactly 29 FMP models, all eight native bindings and explicit provider-qualified routes. No unintended news commands. Verify applicability of annotations and field descriptors for all eight.
  - Run the scoped whole-file complexity check on all maintained production edits. Record compliance with 400 physical lines/file, 300 logical units/file and 50/function.
  - _Boundary: Controller · provider.py, provenance.json and tests/providers/test_fmp_batch_a_registration.py plus Batch B registration tests_
  - _Depends: 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8_
  - _Requirements: 1.1, 1.3, 5.1, 8.1_

- [ ] 4.2 Verify public execution and financial envelopes on the installed API
  - Repeat admission and body/time serialization through actual mounted routes and generated SDK with intercepted acquisitions. Validate selected FMP schemas, OBBject fields, dates, safe errors, empty metadata and baseline identity. Compare against synthetic upstream values for all eight.
  - Run existing transport, financial metadata/policy and SDK/HTTP regression selections. Prove valid and invalid quarter at public entry points, preserve timestamps, block credentials and disallow implicit provider substitution. Record exact commands and counts.
  - This unit produces tests, contracts, documentation or evidence, excluded from production caps. Any required production repair returns to its owning unit and needs fresh 400/300/50 verification.
  - _Boundary: Controller · Batch B actual-join tests under tests/providers/_
  - _Depends: 4.1_
  - _Requirements: 1.1, 2.4, 2.5, 3.3, 4.1, 4.3, 4.5, 4.6, 5.1, 5.2, 5.3, 6.2, 7.1, 7.2, 7.3, 7.4, 7.5_

- [ ] 4.3 Bind eight datasets to the consumer catalog
  - Project native routes and FMP selected params, result types, field descriptions, limits and known coverage into five event tables and three endpoint-backed document widget descriptors. Bind an agreed renderer type and stable IDs using 1.4. Keep calendar controls independent of company selection.
  - Test missing/extra mappings, actual controls, no foreign provider, unchanged baseline widget IDs and preservation of existing Company Research layouts. Mark account and browser state unknown until their evidence arrives.
  - Run the scoped whole-file complexity check on all maintained production edits. Record compliance with 400 physical lines/file, 300 logical units/file and 50/function.
  - _Boundary: Controller · existing input inventory, pipeline/qopenbb_ci/catalog family and tests/contracts/_
  - _Depends: 4.2_
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 2.3, 6.1, 6.3, 6.5_

- [ ] 4.4 Implement keyboard-accessible inline documents
  - Build row selection, readable text with wrapping and focus return, company/source/date/period and availability status. Expose filing/index links as optional navigation. Reject unsafe URL schemes. Treat provider markup as text; no image loads or prefetch.
  - Exercise keyboard-only selection and close, missing attribution, excerpts, metadata-only filings and literal transcript whitespace. Component fixtures prove readable inline behavior for each narrative type.
  - Run the scoped whole-file complexity check on all maintained production edits. Record compliance with 400 physical lines/file, 300 logical units/file and 50/function.
  - _Boundary: Workspace worker · terminalpro/src/components/Widgets/CompanyDocuments/CompanyDocuments.tsx and its focused component tests_
  - _Depends: 4.3_
  - _Requirements: 3.3, 4.1, 6.2, 6.4, 7.2_

- [ ] 4.5 Connect the renderer to acquisition and saved widget state
  - Bind Widgets/index.ts, lib/types/app/widgetTypes.ts and utils/zodForms.ts under terminalpro/src as required by the host contract. Reuse authenticated widget acquisition and save only dataset/query choices. Do not persist text, tokens or stale evidence. Retain peer state and app layout.
  - Mounted integration tests prove no duplicate send, context switch clears evidence, late response is ignored, same-context refresh error labels stale data, and save/export/reopen restores choices. Verify existing saved widgets still load.
  - Run the scoped whole-file complexity check on all maintained production edits. Record compliance with 400 physical lines/file, 300 logical units/file and 50/function.
  - _Boundary: Controller · Workspace host registry, typing, validation, persistence and integration tests frozen in 1.4_
  - _Depends: 4.4_
  - _Requirements: 5.1, 6.1, 6.2, 6.3, 6.4, 7.1, 7.4_

- [ ] 4.6 Regenerate contracts and verify cross-repository compatibility
  - Pin accepted API and Workspace commits. Generate the complete catalog from identified installed sources twice using the existing generator. Review actual before/after schemas, routes, widget IDs, compatibility and hashes.
  - Validate tests/contracts/test_catalog*.py, existing Batch A consumers and new Batch B mappings. Explain every diff, compare required/date bounds across SDK/HTTP/catalog and run whole-file audit on changed generators and integration modules.
  - Run the scoped whole-file complexity check on all maintained production edits. Record compliance with 400 physical lines/file, 300 logical units/file and 50/function.
  - _Boundary: Controller · root sources.lock.json, contracts/, installed catalog and consumer tests_
  - _Depends: 4.5_
  - _Requirements: 1.1, 1.2, 5.1, 6.1, 6.2, 6.3, 6.5, 8.1_

## 5. Candidate, acceptance and publication

- [ ] 5.1 Stage an isolated exact-source candidate and request ledger
  - Freeze all eight direct/native cases, four contrasts, five named widget cases and exact inputs. Ledger starts at zero. Instrument outbound transport before network-enabled startup, cap at 36 including all startup, failures and reruns; disable polling. Use a separate profile, ports and state.
  - Verify source/lock/image and contract hashes, guarded counters, capacity enforcement and readiness offline. Record installed origins, run IDs and rehearsal with zero real calls. Load credentials only under the approved ledger.
  - This unit produces tests, contracts, documentation or evidence, excluded from production caps. Any required production repair returns to its owning unit and needs fresh 400/300/50 verification.
  - _Boundary: Controller · local candidate and private evidence directory_
  - _Depends: 4.6_
  - _Requirements: 2.6, 7.2, 7.3, 8.1, 8.2, 8.5_

- [ ] 5.2 Compare live responses across all eight operations
  - Use 16 direct/native sends and four focused contrasts under the shared ledger. Compare each native result with its own acquired rows and confirm amounts/dates, split orientation, missing vs zero, transcript period/text, excerpt or filing metadata. Record source-specific status per operation.
  - Stop the affected case on denial and dependent cases pending entitlement. Record real counts, retrieval times, private evidence hashes and redacted comparison outcomes. Shared six-send reserve requires a diagnosed reason per use. No substitute data for acceptance.
  - This unit produces tests, contracts, documentation or evidence, excluded from production caps. Any required production repair returns to its owning unit and needs fresh 400/300/50 verification.
  - _Boundary: Controller · approved provider matrix and private captures_
  - _Depends: 5.1_
  - _Requirements: 1.2, 2.3, 2.5, 2.6, 3.3, 4.1, 4.2, 4.4, 4.5, 4.6, 6.2, 7.1, 7.2, 8.3, 8.4_

- [ ] 5.3 Verify five real widgets through save and reopen
  - Use one hidden isolated browser, one history, one calendar and all three documents. Compare displayed data to captured responses and verify links/status, keyboard access, filter controls, reopen and safe export. Exercise race and failure/recovery via isolated offline interception if needed.
  - Allocate ten real sends, initial and reopen for five widgets. Count unexpected sends and stop before the cap. Report API vs UI evidence separately, preserve unsampled widget status and keep licensed text private.
  - This unit produces tests, contracts, documentation or evidence, excluded from production caps. Any required production repair returns to its owning unit and needs fresh 400/300/50 verification.
  - _Boundary: Controller · tests/e2e/ Batch B journey using the established Workspace harness_
  - _Depends: 5.2_
  - _Requirements: 1.2, 6.2, 6.3, 6.4, 7.1, 7.2, 8.3, 8.4_

- [ ] 5.4 Reconcile source verification and sanitized delivery evidence
  - Run affected provider, consumer, Workspace and Linux verification selections at exact source revisions. Audit complexity/inventory across all three trees. Record failures, fixes and unverified scopes. Reconcile breadth, README and docs with accepted checks.
  - Verify sanitized mirror hashes, omission of credentials and licensed content, and immutable commits. Check-only CI must pass at the intended release source before publication.
  - This unit produces tests, contracts, documentation or evidence, excluded from production caps. Any required production repair returns to its owning unit and needs fresh 400/300/50 verification.
  - _Boundary: Controller · verification, .kiro/breadth.toml, docs and reviewed evidence mirror_
  - _Depends: 5.3_
  - _Requirements: 1.2, 1.4, 7.2, 8.1, 8.3, 8.4, 8.5_

- [ ] 5.5 Publish the accepted milestone and verify distributed images
  - Dispatch the established milestone build on the accepted main revision after all applicable gates pass. Verify actual release assets, registry digests, pullability and source identities. Run network-isolated offline installed-API cases on published images and packaged pair readiness with zero FMP sends.
  - Record CI image vs local browser evidence, cleanup and release receipt. Update final checkboxes and handover with verified outcomes. Deployment to the owner's server is a separate operation.
  - This unit produces tests, contracts, documentation or evidence, excluded from production caps. Any required production repair returns to its owning unit and needs fresh 400/300/50 verification.
  - _Boundary: Controller · existing Dagger build, portable publication and release receipts_
  - _Depends: 5.4_
  - _Requirements: 7.2, 8.1, 8.2, 8.5_
