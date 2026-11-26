# Commodities versus technology implementation plan

Run each numbered subtask as a bounded 1–3 hour unit. Before dispatch, give its owner the relevant paths from the [design](design.md), fixtures, dependencies, and the [combined checker command](../../../docs/complexity.md) with current fork scopes. Every production change must pass the whole-file limits of 400 physical lines, 300 logical units and 50 units per function. Each subtask requires independent review and fresh verification. The controller owns shared fixtures, source pins and joins. Schedule at most two disjoint implementers and one heavy build or suite at a time. Only sibling tasks marked (P) share an execution wave. Browser acceptance uses disposable Ubuntu state and one worker. [Delegation](../../steering/delegation.md) · [Verification](../../steering/testing.md)

- [x] 1. Establish the runtime and evidence baseline
- [x] 1.1 Prepare the pinned runtime and enforce whole-file budgets
  - Identify the published baseline, owned fork checkout and explicit base/head or changed-file manifests. Exercise the existing combined checker on clean and oversized cases. Verify the isolated build, browser and provider configuration can distinguish a missing prerequisite from a pass. Register planned coverage as pending.
  - Run the combined complexity gate for this task’s maintained files and record whole-file compliance.
  - _Boundary: Controller, inventory, runtime manifests and portable verification_
  - _Requirements: 1.1, 4.1_

- [x] 1.2 Qualify the source evidence for both proxy roles
  - Inspect DBC, XLK, GLD and a genuine alternate technology ETF through existing admitted sources. Record exposure, listing calendar, entitled windows and FMP retrieval times. Inspect historical availability for the exact DFII10 endpoints and record any evidence gap. Identify a dated official schedule covering the window and any closures. [Source qualification](source-qualification.md)
  - Evidence, fixtures or test cases only. Production size caps do not apply to these artifacts.
  - _Boundary: Controller, sanitized input qualification record_
  - _Depends: 1.1_
  - _Requirements: 1.2, 2.2, 2.4, 2.5, 3.3_

- [x] 1.3 Freeze requests, run examples and saved configuration
  - Round-trip `proxy_comparison@2` and `real_yield_regime@1` requests, owner-scoped run detail, and the allowlisted dashboard and export shape against typed examples. Bind the retrieved-history basis and receipt provenance to the exact saved price rows, and carry the macro cutoff and dated withheld reason. Include a partial leg, a tiny negative spread, mismatched pair/cutoff, an unavailable macro run and a recovery run ID. Freeze schema version, catalog widget declaration and chart settings for both lanes.
  - Evidence, fixtures or test cases only. Production size caps do not apply to these artifacts.
  - _Boundary: Controller, shared fixtures and contracts_
  - _Depends: 1.1, 1.2_
  - _Requirements: 1.1, 1.2, 2.1, 3.2, 4.1, 4.2, 4.3_

- [ ] 2. Supply dated inputs and declare the catalog App
- [x] 2.1 (P) Resolve expected trading sessions
  - Package the qualified official schedule with source identity, digest, revision, coverage and publication evidence. Prove the resolver returns 64 scheduled sessions and handles holidays, early closes, non-sessions, uncovered dates and an ineligible revision. Bind the same selected session and schedule to both models. Apply the historical cutoff to DFII10. Record the actual FMP retrieval times for the retrospective price window.
  - Run the combined complexity gate for this task’s maintained files and record whole-file compliance.
  - _Boundary: services/data-api/qopenbb_data/modeling/service/story_schedule.py, its calendars/nyse_arca.json data, and tests/factors/test_story_schedule.py_
  - _Depends: 1.3_
  - _Requirements: 1.2, 2.2, 2.4, 3.3_

- [ ] 2.2 (P) Generate the story in the catalog
  - Produce one curated declaration with DBC and XLK defaults, the question, ordered views and approved chart presets. Inspect generated apps.json and verify existing curated Apps still load. Use a dedicated catalog test file.
  - Run the combined complexity gate for this task’s maintained files and record whole-file compliance.
  - _Boundary: pipeline/qopenbb_ci/catalog_story.py, pipeline/qopenbb_ci/catalog.py and tests/contracts/test_research_story.py_
  - _Depends: 1.3_
  - _Requirements: 1.1, 2.1, 4.2_

- [x] 2.3 Acquire eligible prices and macro observations
  - Normalize the allowlisted FMP and FRED responses into the model input tables. Implement `proxy_comparison@2` with independently verified price-return and risk calculations on retrieved history. Preserve version 1 point-in-time behavior and saved-run compatibility. Preserve exact units, received price rows, safe leg-specific failure codes, schedule markers and retrieval provenance. Keep DFII10 endpoint eligibility tied to the selected observation day's cutoff. Demonstrate a withheld leg alongside a usable leg, missing endpoint versus interior macro gap, and disjoint windows. Keep the original generic FRED dataset working.
  - Run the combined complexity gate for this task’s maintained files and record whole-file compliance.
  - _Boundary: Versioned comparison method and reference check, modeling acquisition and bounded HTTP transport_
  - _Depends: 2.1_
  - _Requirements: 2.2, 2.3, 2.4, 2.5, 3.3, 4.1_

- [ ] 2.4 Validate requests at the model boundary
  - Bind dataset, model/version, assumptions, symbols, schedule revision and cutoff before source dispatch. Prove authenticated valid requests produce separate saved runs, wrong-model and reversed-binding requests fail, and existing issuer evaluations remain compatible. Withhold the affected spread for missing retrieval provenance or an incompatible adjustment basis. Assert acquisition deadline, cancellation and size bounds.
  - Run the combined complexity gate for this task’s maintained files and record whole-file compliance.
  - _Boundary: Controller integration, orchestrator and model request contracts_
  - _Depends: 2.3_
  - _Requirements: 1.2, 2.1, 3.3, 4.1_

- [ ] 2.5 Run the real-input preflight
  - Stage the actual acquisition and schedule files in the modeling image inputs, build affected images with Dagger and start an isolated candidate with the authenticated bridge. Implement and execute the design's story_preflight.py for the default DBC/XLK pair and both role changes, verifying exact saved source rows with receipt provenance, 64 closes per leg, 63 dated returns and verified spread. Check the two macro endpoints when eligible. For November 13, verify the dated withheld DFII10 outcome and a retained spread-based verdict. Record digests, coverage and any blocked price input. Require a passing preflight before UI integration.
  - Run the combined complexity gate for this task’s maintained files and record whole-file compliance.
  - _Boundary: Controller, candidate packaging and live preflight_
  - _Depends: 2.4_
  - _Requirements: 1.2, 2.2, 2.3, 2.4, 3.1_

- [ ] 3. Bind the native Workspace views to verified runs
- [ ] 3.1 (P) Decode saved evidence and decide the verdict
  - Join output-specific reference matches, checks, trace IDs and the saved snapshot rows. Test exact signed decimals, ties, sub-display-precision spreads, mismatched run identity and blocked outputs. Return the independently valid leg and preserve the verdict when only volatility or macro context fails.
  - Run the combined complexity gate for this task’s maintained files and record whole-file compliance.
  - _Boundary: Workspace terminalpro/src/lib/modeling/storyContract.ts, storyEvidence.ts and their sibling storyContract.test.ts and storyEvidence.test.ts_
  - _Depends: 1.3, 2.5_
  - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 3.1, 3.2, 3.3, 3.4_

- [ ] 3.2 (P) Encode dashboard and template state
  - Allowlist choices, references, cutoff, schedule binding and per-view chart settings for both save and export. Exercise normal hydration, rejected extra fields and legacy dashboards. Inspect serialized writes and exported bytes for provider rows, response text and credentials.
  - Run the combined complexity gate for this task’s maintained files and record whole-file compliance.
  - _Boundary: Workspace terminalpro/src/lib/modeling/storyState.ts and storyState.test.ts, and terminalpro/src/lib/utils/exportTemplate.ts_
  - _Depends: 1.3, 2.5_
  - _Requirements: 4.2, 4.3_

- [ ] 3.3 Coordinate selection changes and retries
  - Submit the two models serially. In a delayed A → B → A test, show pending steps and prove obsolete data, errors and run references cannot win. Recover a supplied run ID by an authorized read. Drop a write response with no recovery ID and assert that the controller makes no automatic second submission. Retry an affected partial comparison at its frozen cutoff while preserving the valid leg and unrelated macro reference. On reopen read references without evaluating anew.
  - Run the combined complexity gate for this task’s maintained files and record whole-file compliance.
  - _Boundary: Workspace storyController and evaluation client_
  - _Depends: 3.1, 3.2_
  - _Requirements: 1.2, 1.3, 3.3, 3.4, 4.1, 4.2_

- [ ] 3.4 Register the native widget and selection controls
  - Admit only the validated story declaration. Mount the controller through the normal widget dispatcher, persist allowlisted state and restore controls on hydration. Demonstrate each role and date can be changed by keyboard in both themes and focus survives pending results.
  - Run the combined complexity gate for this task’s maintained files and record whole-file compliance.
  - _Boundary: Workspace widget admission, dispatch and ResearchStory shell_
  - _Depends: 2.2, 2.5, 3.3_
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 4.2_

- [ ] 3.5 Render ordered findings and dated drill-downs
  - Show price returns, risk, real yields and verdict with the selected window and check states. Open both legs' closes, the 63 dated returns and the endpoint rows from their original runs. Verify percent versus percentage points, dividend exclusion, higher-risk winner, missing context, source headlines, FRED notice and keyboard navigation. Restore the analyst's chart settings for source and result views.
  - Run the combined complexity gate for this task’s maintained files and record whole-file compliance.
  - _Boundary: Workspace story chart and evidence views_
  - _Depends: 3.4_
  - _Requirements: 1.4, 2.1, 2.2, 2.3, 2.4, 2.5, 3.1, 3.2, 3.3, 3.4, 4.2_

- [ ] 4. Accept the packaged analyst journey
- [ ] 4.1 Integrate the accepted fork and discover the story tests
  - Verify the actual owned fork revision, promote its source pin and stage all maintained inputs. Build candidate images through Dagger. Extend Playwright discovery and the packaged runner for story selection and same-session modeling-service restart. Confirm both issuer and story journeys remain discoverable.
  - Run the combined complexity gate for this task’s maintained files and record whole-file compliance.
  - _Boundary: Controller, source pins, image inputs and journey harness_
  - _Depends: 3.5_
  - _Requirements: 1.1, 4.1, 4.2_

- [ ] 4.2 Verify selections, evidence and keyboard access on Ubuntu
  - In one isolated headless browser worker, open the catalog App, change each role and the date, compare displayed spread and dated rows to the same saved run, and exercise insufficient history followed by recovery. Inspect real FMP inputs for the price and risk charts. Verify the DFII10 endpoint chart when eligible and the dated withheld context with the retained verdict for November 13. Inspect both themes, text units, focus and console/network errors.
  - Evidence, fixtures or test cases only. Production size caps do not apply to these artifacts.
  - _Boundary: Packaged story browser journey, selection and financial evidence cases_
  - _Depends: 4.1_
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 2.1, 2.2, 2.3, 2.4, 2.5, 3.1, 3.3_

- [ ] 4.3 Verify outage recovery, save, fresh reopen and export
  - Interrupt modeling, restore it and retry on the same dashboard. Save chart choices and references, introduce a controlled subsequent source revision, then reopen with fresh login and compare original values, dates, checks and chart settings. Exercise foreign/deleted references and inspect export contents. Retain real versus controlled case labels.
  - Evidence, fixtures or test cases only. Production size caps do not apply to these artifacts.
  - _Boundary: Packaged story browser journey, recovery and persistence cases_
  - _Depends: 4.2_
  - _Requirements: 3.3, 3.4, 4.1, 4.2, 4.3_

- [ ] 4.4 Reconcile acceptance evidence and rollback
  - Run the combined complexity gate over final joined revisions. Record actual test paths and outcomes for all 16 criteria in the breadth map, with image digests, sanitized evidence, source limitations and the previous working image set. Leave skipped live cases open. Obtain independent acceptance of the joined evidence.
  - Run the combined complexity gate for this task’s maintained files and record whole-file compliance.
  - _Boundary: Controller, breadth map, evidence and final shared-module audit_
  - _Depends: 4.3_
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 2.1, 2.2, 2.3, 2.4, 2.5, 3.1, 3.2, 3.3, 3.4, 4.1, 4.2, 4.3_
