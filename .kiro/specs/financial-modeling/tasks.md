# Financial modeling foundation tasks

Design and Polars conventions owner-approved, 2026-10-28. Task approval remains pending. This session delivers the plan only. Future implementation follows verified FMP inputs for the selected slice; the broad provider workstream remains first. Repository name/remote and image coordinates are explicit bootstrap inputs, not assumed existing resources.

## Completion rules and execution lanes

Each executable task is bounded to approximately 1-3 hours of focused implementation. If inspection exceeds that bound, split the responsibility before editing. Every production task updates the maintained-file inventory and passes whole-file limits of 400 physical lines, 300 logical units and 50/function, plus owning lint/type checks. Use financial-domain names, Polars table contracts, precision policy and rationale-focused comments. No task changes house formulas without an approved model-specific spec.

Each task requires fresh verification and independent review before its checkbox and commit. Use Sol implementers and Astra for financial/shared integration review. Max four active slots including controller, one heavy build/suite; bounded xdist/browser workers. Contracts freeze before parallel lanes. Controller owns shared files, source/contract joins, commits and publication. Failed/missing/skipped checks never become accepted evidence.

## Tasks

- [ ] 1. Bootstrap the separate repository and agent extension workflow
  - Establish owner-selected repository coordinates, independent Python/uv project and locked dependencies including Polars, schema/HTTP and JWT libraries. Verify protected installs, supported wheels and Decimal operation compatibility. Transfer canonical modeling specs with revision references; QOpenBB retains integration pointers.
  - Install AGENTS.md and steering for Kiro approvals, house-method corrections, typed financial Python/Polars, COBESY comments, role-based review, bounded verification and portable delivery. No formula engine or placeholder image.
  - Done: fresh checkout can run a minimal import/contract check under the pinned environment; agent instructions identify the next approved spec rather than infer methods from templates.
  - Completion gate: measure this task's maintained production files against 400 physical / 300 logical / 50 per function and record fresh checks; docs/generated artifacts remain scoped exclusions.
  - _Boundary: New modeling repository scaffolding, dependency files, AGENTS/steering/docs only; QOpenBB transfer pointers controller-owned._
  - _Depends: Owner task approval and repository coordinates; implementation sequencing gate above._
  - _Requirements: 6.1, 6.2_

- [ ] 2. Establish executable code-quality and boundary enforcement
  - Add maintained scope inventory and the existing physical/logical checker convention, owning lint/type checks and a portable verification command. Enforce domain isolation from HTTP, storage, provider credentials and Workspace imports.
  - Done: a deliberate oversized function/import violation fails the gate; clean foundation passes. Keep test fixtures outside production inventory without hiding production helpers there.
  - Completion gate: measure this task's maintained production files against 400 physical / 300 logical / 50 per function and record fresh checks; docs/generated artifacts remain scoped exclusions.
  - _Boundary: Modeling tools, inventory, quality and architecture tests; no model methods._
  - _Depends: 1_
  - _Requirements: 1.1, 6.1, 6.2_

- [ ] 3. Freeze financial table, check, trace and run contracts
  - Implement typed snapshot, assumption, descriptor, outcome, tolerance, exception, TraceEntry and result/run contracts. Include table grain/keys/types, nulls, units/currency, periods, observation category, available accounting/vintage metadata and asserted-versus-acquired provenance.
  - Define explicit Decimal encoding and value bounds, financial completeness and duplicate/join rules at the boundary. Keep exported contracts independent of Polars runtime objects.
  - Done: round-trip examples and malformed/missing/unsupported cases demonstrate the contracts; financial origin and unrounded trace survive serialization. Freeze interface versions before tasks 4.2/5/6 fan out.
  - Completion gate: measure this task's maintained production files against 400 physical / 300 logical / 50 per function and record fresh checks; docs/generated artifacts remain scoped exclusions.
  - _Boundary: Modeling contracts package and contract fixtures/tests only._
  - _Depends: 2_
  - _Requirements: 1.2, 1.3, 2.3, 2.7, 3.1, 3.6, 6.3, 6.4_

- [ ] 4. Register and execute supplied-input methods
- [ ] 4.1 (P) Register supplied-input model methods
  - Implement protocol/registry, exact version lookup and descriptor validation, including output/check dependencies and cycles; no network or storage imports in model modules.
  - Use a clearly labeled test-only method to exercise execution; do not advertise it as a financial product. Verify table schemas, null handling, decimal conversions and lazy materialization at the declared boundary.
  - Done: supported method lookup works offline; unknown versions and invalid or cyclic dependencies fail explicitly.
  - Completion gate: measure this task's maintained production files against 400 physical / 300 logical / 50 per function and record fresh checks; docs/generated artifacts remain scoped exclusions.
  - _Boundary: Modeling models/protocol.py, registry.py and their tests; shared contracts frozen, no edits without controller join._
  - _Depends: 3_
  - _Requirements: 1.1, 1.2, 1.3, 2.1_

- [ ] 4.2 Bound Polars execution and cancellation
  - Implement spawn-based execution, native thread budget, explicit materialization and declared input limits using the frozen registry. Use a test-only method, not a published financial model.
  - Done: offline execution succeeds; unsupported numeric conversion, oversized input and timeout fail explicitly, with no detached computation left running.
  - Completion gate: maintained production files pass 400 physical / 300 logical / 50 per function and owning checks.
  - _Boundary: Modeling execution helper and process/Polars tests only; no registry or validation edits._
  - _Depends: 4.1_
  - _Requirements: 1.1, 2.1_

- [ ] 5. (P) Execute financial rules and independent verification
  - Implement precondition/invariant/postcondition lifecycle and dependent-output statuses. Preserve unknown/error/not-applicable distinctions, non-overridable mathematical failures, unit-aware tolerances and separately recorded permitted policy exceptions.
  - Add independently expressed Python reference verification on actual supplied inputs, separate from production expressions. Use test-only arithmetic to prove the lifecycle; future formulas retain their own approvals.
  - Done: failed postconditions withhold affected outputs; unavailable checks cannot pass; independent mismatches and changed inputs cannot retain verified status. Meaningful mutation of the test-only calculation is detected by the reference.
  - Completion gate: measure this task's maintained production files against 400 physical / 300 logical / 50 per function and record fresh checks; docs/generated artifacts remain scoped exclusions.
  - _Boundary: Modeling validation and verification modules/tests only; contracts frozen._
  - _Depends: 3_
  - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 3.2, 3.3, 3.5_

- [ ] 6. (P) Persist immutable owner-scoped model runs
  - Implement run-store port and atomic relative-bind file persistence with opaque run IDs. Retain snapshots, assumptions, methods/rules/reference versions, trace entries and safe fingerprints; prevent path traversal and wrong-owner retrieval.
  - Done: complete saved run round-trips, interrupted writes remain undiscoverable, old runs remain immutable and owner authorization fails closed. Tests do not use owner data.
  - Completion gate: measure this task's maintained production files against 400 physical / 300 logical / 50 per function and record fresh checks; docs/generated artifacts remain scoped exclusions.
  - _Boundary: Modeling service/ports.py run-store portion, run_store.py and store tests; no orchestration or HTTP routes._
  - _Depends: 3_
  - _Requirements: 3.1, 3.4, 3.5, 3.6_

- [ ] 7. Integrate evaluation orchestration and input mapping
  - Join registry, rule execution, independent references and store under the approved request/run contract. Add configured data API acquisition through an allowlisted mapping, separating supplied assertions from actual acquisition provenance.
  - Preserve economic-series meaning in mapping fixtures; no live EconDB adapter or silent interpolation. This task handles contract normalization, not provider fetching implementations or new house formulas.
  - Done: an offline evaluation and a mocked data-API evaluation both persist traced runs, explicit refresh yields new evidence and missing/invalid inputs produce the designed states. Verify the shared-module caps after join.
  - Completion gate: measure this task's maintained production files against 400 physical / 300 logical / 50 per function and record fresh checks; docs/generated artifacts remain scoped exclusions.
  - _Boundary: Modeling orchestrator, input port/adapter and integration tests; controller resolves coupled changes from 4-6._
  - _Depends: 4.2, 5, 6_
  - _Requirements: 1.1, 2.5, 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 6.3, 6.4_

- [ ] 8. Expose the model HTTP API and widget contracts
- [ ] 8.1 Expose authenticated evaluation and saved-run HTTP routes
  - Implement discovery, evaluation, saved-run and output routes, safe errors, identity assertion validation and private run access. Enforce body/timeout/admission limits; GET operations never calculate.
  - Done: HTTP contract tests cover valid/withheld/unverified results, expired/wrong-audience/spoofed identity, wrong-owner access and bounded requests.
  - Completion gate: measure this task's maintained production files against 400 physical / 300 logical / 50 per function and record fresh checks; docs/generated artifacts remain scoped exclusions.
  - _Boundary: Modeling service routes and identity validator with service tests; no public gateway or Workspace code._
  - _Depends: 7_
  - _Requirements: 1.2, 1.3, 3.6, 4.1, 4.5_

- [ ] 8.2 Project saved outputs for widget discovery
  - Add generated widget/app discovery and read-only result projections without financial formulas.
  - Done: projection tests preserve null/check/stale states, trace links and declared numeric display bounds; GET requests never recalculate.
  - Completion gate: maintained production files pass 400 physical / 300 logical / 50 per function and owning checks.
  - _Boundary: Modeling widget_projection, discovery configuration and projection tests only._
  - _Depends: 8.1_
  - _Requirements: 1.2, 4.1, 4.5_

- [ ] 9. Cross-repository contract delivery
- [ ] 9.1 Export reproducible versioned contract bundles
  - Export OpenAPI/JSON Schemas and descriptors with source revision and hashes. Establish initial QOpenBB consumer artifacts without requiring an existing model release.
  - Done: exports reproduce, validate the supported dialect and fail on generated drift; initial counterpart contracts are explicitly pinned.
  - Completion gate: maintained production files pass 400 physical / 300 logical / 50 per function and owning checks.
  - _Boundary: Modeling export tooling and QOpenBB consumer manifests; explicit controller-owned integration._
  - _Depends: 8.2_
  - _Requirements: 4.1, 5.4_
- [ ] 9.2 Check structural and financial-semantic compatibility
  - Compare candidate contracts and exercised responses against pinned consumer expectations, including nullability, units-only changes, error/partial states and supported versions.
  - Done: compatible examples pass; incompatible or unknown changes block promotion pending migration or explicit acceptance. No general schema-subsumption claim.
  - Completion gate: maintained production files pass 400 physical / 300 logical / 50 per function and owning checks.
  - _Boundary: Modeling compatibility tooling and QOpenBB tests/contracts consumer checks; no formula or UI changes._
  - _Depends: 9.1_
  - _Requirements: 1.4, 4.2, 4.3, 4.4_
- [ ] 9.3 Select affected checks through cross-repository breadth
  - Link criteria to model/rule/operation/widget IDs and actual test selectors. Select affected checks on changes; unresolved impact invokes broader relevant verification and exposes mapping gaps.
  - Done: absent/skipped checks cannot pass; unmapped changes fail closed and exact counterpart revision/evidence identities survive the integration report.
  - Completion gate: maintained production files pass 400 physical / 300 logical / 50 per function and owning checks.
  - _Boundary: Explicit integration task: breadth/impact tooling and QOpenBB breadth mappings; controller owns shared pins._
  - _Depends: 9.2_
  - _Requirements: 5.1, 5.2, 5.3, 5.4_

- [ ] 10. Integrate the authenticated Workspace modeling bridge
  - Add the designed GetCurrentUser bridge, dedicated signed service assertions and allowlisted forwarding. Register routes, strip public identity headers, test session expiry and rotation, and keep the internal service unreachable through unauthenticated direct proxy routes.
  - Measure the upstream router registration file before edits; use an existing applicable reviewed exception or approve a narrowly scoped exception/cohesive extraction before acceptance. Do not silently waive whole-file caps.
  - Done: real session identity reaches the service; missing/expired sessions and spoofed subjects cannot retrieve or create another user's runs. Existing provider-data routes retain their behavior.
  - Completion gate: measure this task's maintained production files against 400 physical / 300 logical / 50 per function and record fresh checks; docs/generated artifacts remain scoped exclusions.
  - _Boundary: QOpenBB Workspace backend routers/modeling.py, api/modeling_identity.py, main.py registration, gateway route and bridge tests; controller-owned fork/source inventory joins._
  - _Depends: 8.1, 9.3_
  - _Requirements: 3.4, 4.5, 6.5_

- [ ] 11. Bind model evaluations to existing Workspace widgets
  - Implement evaluationClient/runBindings and freeze the exact existing widget control call site before edits. Use a POST-capable parameter adapter and read-only run-result widgets with readable assumptions, trace/check details and saved run IDs.
  - Done: test-only integration fixture demonstrates explicit evaluation, refresh, failure/stale states and saved parameter restoration. Verify consumers against the pinned API bundle and retain direct provider views when modeling is unavailable.
  - Completion gate: measure this task's maintained production files against 400 physical / 300 logical / 50 per function and record fresh checks; docs/generated artifacts remain scoped exclusions.
  - _Boundary: QOpenBB consumer adapter files, declared widget call site, consumer manifests and existing unit/browser tests; no financial formulas or new renderer._
  - _Depends: 10, 8.2_
  - _Requirements: 4.1, 4.2, 4.4, 4.5, 6.5_

- [ ] 12. First real-model integration milestone
- [ ] 12.1 Verify the real-model analyst journey
  - Prerequisite: a separately approved and implemented real method, independent reference and verified FMP inputs. Test fixtures alone cannot close this task.
  - Done: bounded real-data numerical and isolated Playwright/CDP checks demonstrate assumptions, traced results, failure states, fresh saved reopen and retained-state recreation. Record actual image/source identities; resolve failures before acceptance.
  - Completion gate: affected production files pass 400 physical / 300 logical / 50 per function; tests/docs are scoped exclusions.
  - _Boundary: Cross-repository acceptance integration using existing browser fixtures and real-model evidence; controller-owned joins._
  - _Depends: 11; separate real-model spec completion and verified provider inputs_
  - _Requirements: 4.2, 4.5, 5.1, 5.3, 6.2, 6.3, 6.5_
- [ ] 12.2 Build the independent model image and Compose integration
  - Add Dagger-only model image build and independent lock, plus Compose service, relative bind and runtime inventory. Keep unchanged OpenBB images pinned.
  - Done: assembled image/contract set passes startup, authenticated model access and unavailable-model/direct-data behavior; pull-only candidate procedure works. No placeholder model image.
  - Completion gate: changed build/runtime production files pass 400 physical / 300 logical / 50 per function, with explicit generated exclusions.
  - _Boundary: Explicit cross-repository integration: model image belongs to modeling repo; Compose/gateway/runtime inventory belongs to controller in QOpenBB._
  - _Depends: 12.1_
  - _Requirements: 5.4, 6.5_
- [ ] 12.3 Publish the accepted feature milestone
  - Extend portable publication commands and thin CI wrappers to publish the independently versioned image and hash-verified contracts. Pin counterpart revisions and run the integrated checks against the actual final image set; record any candidate-versus-published verification distinction.
  - Done: tagged release assets and pulls match the manifest, numerical/consumer evidence is linked and checkboxes/docs/breadth are updated. Breaking contracts retain supported versions or an accepted migration; absent/skipped checks stay open. Owner-server acceptance requires its own evidence.
  - Completion gate: any changed publication code passes 400 physical / 300 logical / 50 per function; evidence/docs remain excluded.
  - _Boundary: Controller publication and integration identities; model repo owns its release artifacts. No provider or financial formula changes._
  - _Depends: 12.2_
  - _Requirements: 1.4, 4.4, 5.1, 5.2, 5.3, 5.4, 6.1, 6.2_

Parallel wave: after task 3 freezes the shared contracts, tasks 4.1/5/6 have disjoint writable scopes. At most two implementers run concurrently, keeping a slot for independent review. Task 7 joins them; later integration remains sequential. Task 12 remains blocked on a real model; it cannot be marked complete through the foundation plan alone.
