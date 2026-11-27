# Events and Documents implementation plan

Deliver one catalog App that answers the approved earnings question using the four installed FMP inputs. Each numbered subtask is a 1–3 hour work unit. The [design](design.md) identifies the exact source files and the [requirements](requirements.md) define acceptance. Checked tasks have passed independent review.

The controller freezes shared interfaces, fixtures and ownership before fan-out, stages reviewed changes selectively, and serializes commits, source pins and joins. Use fresh Sol implementers and independent reviewers; use Astra for financial semantics and difficult integration. Dispatch only the marked pairs together, with at most two implementers. Give each worker its named files, frozen inputs, focused checks and the [combined complexity command](../../../docs/complexity.md) with actual base/head revisions or explicit change manifests for both forks. Measure whole maintained files against 400 physical lines, 300 logical units per file and 50 per function. One heavy suite or build runs at a time. Require fresh verification after independent review. Workspace test paths below are relative to `vendor/workspace/terminalpro/`. Reserve the shared Events and Documents unit and integration suites named in the design for sequential joins. [Delegation](../../steering/delegation.md) · [Testing](../../steering/testing.md)

- [x] 1. Establish the candidate baseline and shared contracts
- [x] 1.1 Prepare the pinned runtime and complexity inventory
  - Verify the owned Workspace checkout, installed Batch B route and catalog baselines, pinned toolchains, disposable login, one-worker headless browser, guarded provider capture and candidate build entry point. Use offline smoke checks. A missing live entitlement remains a recorded prerequisite for the live journey.
  - Register planned maintained paths and test/generated exclusions before feature edits. Run the existing combined checker and its oversized-file regression. Record the two fork scopes and confirm the inventory changes pass applicable caps.
  - _Boundary: Controller, runtime preflight, root and fork scope inventories_
  - _Requirements: 1.1, 5.3, 5.4_

- [x] 1.2 Freeze the declaration, request, receipt and saved-state examples
  - Bind the exact endpointless type, four dataset IDs and installed policies to versioned choices, transient slot outcomes and layout. Freeze callback and prop contracts for selection, reader, controller, charts and documents so either UI lane can run from fixtures.
  - Round-trip shared examples for a 204, a bounded empty envelope, duplicate issuer dates, a typed failure, an exact transcript, and a config-only saved story. Verify the candidate browser exposes raw JSON numeric tokens using 9007199254740993. Preserve this number as literal bytes in fixtures.
  - Fixtures and contract tests only. Production code caps do not apply.
  - _Boundary: Controller, shared contract fixtures and compatibility assertions_
  - _Depends: 1.1_
  - _Requirements: 1.1, 1.2, 1.4, 2.2, 2.3, 3.2, 4.5, 5.2_

- [ ] 2. Establish catalog and acquisition boundaries
- [ ] 2.1 (P) Generate the curated catalog entry
  - Use all four validated FMP declarations and existing defaults. Emit the ordered App once. Missing or foreign inputs must prevent its admission. Regenerate affected catalog artifacts and hashes and compare unchanged Apps and individual widgets.
  - Pass the combined caps for the maintained generator and registration modules. Document generator provenance for excluded outputs.
  - _Boundary: Root catalog_events_documents.py, catalog.py, catalog_cli.py, generated contracts and test_events_documents_catalog.py_
  - _Depends: 1.2_
  - _Requirements: 1.1, 1.2_

- [x] 2.2 (P) Validate the listing and independent query choices
  - Use the fixed calendar, filings, transcript and news policies. Validate inclusive date pairs, genuine dates, scalar types, pages, limits and year/quarter. Preserve exact listing suffixes. Omit absent optional news dates.
  - Exercise each boundary and its first invalid neighbor. Return a field-specific issue with the actual limit and keep all other effective selections. Pass the combined caps for the selection module and any financial query validator changes.
  - _Boundary: Workspace selection.ts, financialQuery.ts and tests/unit/events-documents-selection.test.ts_
  - _Depends: 1.2_
  - _Requirements: 1.2, 1.3, 2.1, 3.1, 3.2, 3.3_

- [ ] 2.3 (P) Read authorized responses without losing HTTP status or numeric tokens
  - Check dashboard, source and underlying widget permission before dispatch on the installed connection. Preserve normal session-header scope. Handle cancellation and safe failure codes. Read the body once, bind a bodyless 204 to the request and retain exact calendar tokens by original ordinal and field.
  - Verify denied reads send nothing, 204 supplies no provider timestamp, and typed failures, malformed JSON and missing token support cannot yield usable evidence. Check existing transport callers and pass the combined caps for reader and transport files.
  - _Boundary: Workspace reader.ts, status-aware transport in lib/api.tsx and tests/unit/events-documents-reader.test.ts_
  - _Depends: 2.1, 2.2_
  - _Requirements: 1.3, 1.4, 2.3, 2.6, 4.4, 4.5_

- [ ] 2.4 (P) Admit the native story identity through Workspace discovery
  - Extract the schema responsibility from the near-cap shared form module. Admit the exact type and catalog identity only when the declaration and its four source bindings agree. Check fresh and cached launch validation, aliases, overridden endpoints and existing research story admission.
  - Deliver validated discovery data for later widget dispatch. Run the combined caps on the schema, type and admission modules.
  - _Boundary: Workspace nativeStorySchema.ts, zodForms.ts, widgetTypes.ts, backendValidation/catalog.ts and nativeWidget.ts and tests/unit/events-documents-admission.test.ts_
  - _Depends: 2.1, 2.2_
  - _Requirements: 1.1, 5.2_

- [ ] 3. Bind the evidence to the active selection
- [ ] 3.1 Validate financial receipts and project issuer earnings
  - Verify dataset, provider, endpoint, normalized tuple, timestamp, count and bounds before promoting a success. Keep 200 empty metadata. Project each exact-symbol match after the source-order cap with its original ordinal, report date, update, units and four source fields.
  - Assert distinct states for empty market, no issuer match and rows without figures. Test clipping with a match, a full slice with unknown coverage, duplicate dates, zero, null and exact numeric tokens. Verify all three document response kinds against issuer, content and applicable period, including duplicate or blank transcripts.
  - Pass the combined caps on evidence, calendar and affected financial-envelope modules.
  - _Boundary: Workspace receipt decoding, calendar projection and dedicated decoder tests_
  - _Depends: 2.3, 2.4_
  - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 3.1, 3.2, 3.3, 3.4, 4.4_

- [ ] 3.2 Implement per-input acquisition and recovery
  - Keep only current authorized receipts. Cancel superseded work where possible and guard completions by tuple and generation. On issuer change reproject the unchanged market receipt or filter its pending response for the new company. Clear superseded details and contributions immediately.
  - Simulate A/B/A with late successes and failures, permission revocation during a request, simultaneous independent edits and successful explicit retry. Count dispatches and verify coalescing, no auto retries or background refresh and no invalid reads.
  - Pass the combined caps for the controller.
  - _Boundary: Workspace controller.ts and controller lifecycle tests_
  - _Depends: 3.1_
  - _Requirements: 1.2, 1.3, 1.4, 4.1, 4.4, 4.5_

- [ ] 3.3 Derive the conclusion and cite its evidence
  - Calculate usable inputs from the four current slots. Cover every count, including zero with pending versus zero fully resolved. A metadata item can support filing/news availability while a transcript needs valid exact-period text. A matching calendar row needs a supplied figure.
  - Trace each amount and availability claim to a current field or result. Retain clipping, missing fields, content qualifications, empty conditions and safe failure reasons. Pass the combined caps for the conclusion module.
  - _Boundary: Workspace conclusion.ts and conclusion tests_
  - _Depends: 3.2_
  - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5_

- [ ] 4. Present and persist the native App
- [ ] 4.1 (P) Render the earnings rows and paired charts
  - Present every matching row separately with FMP attribution, bounds, market count, clipping, dates and unknowns. Use separate EPS and revenue scales and selectable bar/point views. Keep actual and estimated values distinct.
  - Resolve each mark and keyboard-accessible value to its own exact source token. Show no mark for missing data. Check duplicate dates, missing versus zero, and focus return in both themes. Pass the combined caps for the earnings view.
  - _Boundary: Workspace Earnings.tsx and tests/integration/eventsDocumentsEarnings.test.tsx_
  - _Depends: 3.3_
  - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 4.4, 5.1_

- [ ] 4.2 (P) Present the independently queried documents
  - Preserve filing form, timestamps, string CIK and document/index links; exact transcript timestamp, whitespace and completeness; and news headline, time, site, publisher and excerpt status. Show issuer, effective bounds, freshness and FMP attribution at inspection.
  - Exercise keyboard detail/return, full-page uncertainty, literal markup, absent and unsafe links and typed upstream rejection. Verify that only explicit activation opens validated HTTP(S) and that no embedded or prefetched request occurs. Pass the combined caps for both document view modules.
  - _Boundary: Workspace Documents.tsx, CompanyDocuments.tsx and tests/integration/eventsDocumentsDetails.test.tsx_
  - _Depends: 3.3_
  - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 4.4, 5.1_

- [ ] 4.3 Integrate controls, views and conclusion in the catalog-launched widget
  - Register the native dispatcher and compose the ordered views in the existing frame. Provide keyboard-operable local company choices, explicit custom symbol Apply and four independent groups of query controls. Show the effective symbol and the actual invalid field and bound.
  - Open the generated App in a component integration test. Verify draft keystrokes, selecting an earnings row and chart-only changes issue zero reads. Verify independent updates, conclusion announcements, retry, focus return or section fallback, and both themes.
  - Pass the combined caps for the controls, composition root and dispatcher.
  - _Boundary: Workspace Story.tsx, Controls.tsx, Widgets/index.ts and story integration tests_
  - _Depends: 2.4, 3.3, 4.1, 4.2_
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 3.4, 4.1, 4.2, 4.3, 4.4, 4.5, 5.1_

- [ ] 4.4 Integrate choices-only storage, template exchange and fresh reopen
  - Use one versioned positive encoder on widget writes, ordinary dashboard save, export, import and hydration. Validate geometry, order, all query choices and both chart enums. Present a reset action for malformed or incompatible choices before any request.
  - Inspect both serialized forms with nested injected values and verify evidence, credentials, links and computed results cannot survive. Reopen in a fresh authorized context, verify restored choices, four new reads and the reopened export menu. Regression-check other widget types.
  - Pass the combined caps across all modified storage, layout, schema, menu and story modules.
  - _Boundary: Workspace state.ts and the design's dashboard, template and reopened-menu integration paths_
  - _Depends: 4.3_
  - _Requirements: 1.1, 1.2, 5.1, 5.2_

- [ ] 5. Verify the installed candidate
- [ ] 5.1 Integrate the reviewed fork and build the candidate
  - Push accepted Workspace changes before updating the root source lock. Validate catalog provenance against the integrated revision, freeze both service image identities and use Dagger for any needed image build. Use portable verification to launch the disposable authenticated pair.
  - Run affected type, catalog and persisted-story regressions; confirm all four mounted routes and native App discovery offline. Audit the combined whole-file caps across the final change set including shared modules.
  - _Boundary: Controller, source lock, build and verification integration_
  - _Depends: 4.4_
  - _Requirements: 1.1, 5.2, 5.3_

- [ ] 5.2 Establish the independent financial comparison and guarded browser runner
  - Extend the financial Workspace Playwright target with the story journey and a raw-response Python verifier using Decimal and arbitrary-precision integers. Compare provider fields, installed normalization and UI values from the same send. Demonstrate detection of a one-unit error in 9007199254740993 and a wrong row with the same report date.
  - Exercise the guarded ledger offline. Count every outbound send including failures separately from browser requests; reject unexpected tuples before dispatch, suppress raw licensed content and credentials in reviewed output. Verify one-worker test discovery on the intended candidate.
  - Tests and verifier fixtures are excluded from production caps. Check the maintained runner configuration against the applicable caps.
  - _Boundary: Root events_documents_oracle.py, events-documents-workspace.spec.mts and financial-workspace.config.ts_
  - _Depends: 5.1_
  - _Requirements: 2.2, 2.3, 2.6, 5.3, 5.4_

- [ ] 5.3 Run the controlled packaged journey
  - Drive the candidate from catalog through per-input changes, recovery, save, fresh authenticated reopen and safe export. Exercise empty, partial, denied, invalid, superseded and clipped evidence, duplicate dates, zero/null, same-query retry and focus navigation in both themes. Include disappearing invoking rows.
  - Require zero live provider sends. Inspect displayed facts, network effects, saved content and isolated browser diagnostics; record controlled results independently of the live ledger. Tests and sanitized evidence only, excluded from production caps.
  - _Boundary: Controlled story browser scenarios and isolated candidate evidence_
  - _Depends: 5.2_
  - _Requirements: 1.4, 2.5, 2.6, 3.2, 3.5, 4.3, 4.5, 5.1, 5.2, 5.4_

- [ ] 5.4 Verify the earnings answer against real FMP responses
  - Freeze witnessed listing/window, document tuples and send allowance before launch. The minimal journey plans 15 sends across launch (4), listing change (3), one bound edit per input (4) and fresh reopen (4). Save, export and invalid edits add zero. Stop on a budget breach and report the actual ledger.
  - On the identified candidate, compare all four inputs, row/field chart marks, missing labels, provenance, conclusion and persisted choices against that journey's own acquired responses. Record per-field coverage, entitlement failures, candidate revisions/digests, browser and safe discrepancies. Leave unobserved live cases open, including missing-value display when every live field was populated.
  - Include a representative real-FMP earnings chart sample in the milestone record after independent review for credentials and private information. Caption the measure, unit, report date and tested revision; link the reviewed artifact and record its exact source hash in the sync manifest. If live verification is unavailable, mark the sample pending. Reconcile breadth and completion checkboxes with observed outcomes. Test and evidence artifacts are outside production caps; any corrective production change returns to its owning task for fresh review and cap checks.
  - _Boundary: Controller and independent financial reviewer, live journey and acceptance evidence_
  - _Depends: 5.3_
  - _Requirements: 1.1, 1.2, 2.1, 2.3, 2.6, 3.1, 3.2, 3.3, 3.4, 4.1, 4.4, 5.2, 5.3_

## Implementation notes

Workspace commit `2ac14a0` verifies task 2.2 with 49 focused passing cases. Unchanged app-shape assertions and a chart mock also fail on the preceding Workspace revision. The candidate pin and integrated browser checks belong to group 5.
