# Financial annotation repair tasks

Design amendment owner-approved on 2026-10-29. This subplan repairs the prerequisite of main task 4.1; it does not add research families or change the main batch's 26-task count. Task approval is pending. Existing source acceptance remains 15/26.

## Execution rules

Use the existing verification environment, scope inventory and checker; no new test framework, dependency installation or image build is needed. Every production task updates its maintained-file scope and passes whole-file 400 physical / 300 logical / 50 per function caps, owning Ruff/type checks and independent review before its per-task commit. Controller owns shared inventory, source pins, breadth and reviewed evidence. Exact existing commands are in docs/complexity.md; use current fork change manifests and Node 24.22.1 or later approved patched tooling.

Each executable unit targets 1-3 focused implementation hours. Extract cohesive declarations before accepting oversized files; do not compress finance logic. Freeze the core contract before fan-out. At most two Sol implementers plus an independent Astra reviewer and controller; one heavy suite/build at a time, bounded xdist/browser workers. Existing behavior checks are extended where useful; do not copy harnesses or rerun unchanged broad suites solely for paperwork.

All adoption tasks preserve output rows, result metadata, aliases, limits, dates, errors and retrieval timestamps. They move static definitions to one class-owned source and remove their former copies. Dynamic result properties stay runtime-owned. The new annotations are not another execution registry or financial calculation engine.

## Tasks

- [ ] 1. Freeze the declaration contract and its validation
  - Define typed query/data annotations with static field templates, runtime-resolved properties, procedural limits, response policy and provider-selection requirement. Derive ordinary parameter constraints/defaults and field descriptions from the owning models. Validate actual serialized-field references and preserve explicit unknowns.
  - Reuse FinancialFieldMetadata; make template rendering copy declarations rather than mutate shared state. Reject malformed declarations and distinguish them from missing declarations. Export an interface brief for adoption/projection workers before fan-out.
  - Done: focused tests prove serialization, field references, static/runtime distinction and independent copies. The new module has no network, registry or UI dependency. Inventory includes it and the existing executable size checker passes.
  - _Boundary: New data-fork core standard_models/financial_annotations.py and tests/providers/test_financial_annotations.py; controller owns inventory/source pin updates._
  - _Requirements: 4.1, 4.2, 6.1, 7.3_

- [ ] 2. Representative adoption
- [ ] 2.1 (P) Adopt periodic key-metrics declarations
  - Move static units, financial bases and policy to the query/data declarations. Runtime field construction reads those templates and supplies actual period, availability and provenance. Preserve modeled-only output and unknown market dates.
  - Done: existing key-metrics fixtures and declaration/runtime agreement checks pass; no duplicate unit sets remain. Whole changed files pass 400/300/50 and owning checks.
  - _Boundary: FMP models/key_metrics.py, key_metrics_data.py and tests/providers/test_fmp_key_metrics.py only._
  - _Depends: 1_
  - _Requirements: 4.1, 4.2, 4.7, 6.1, 6.2_
- [ ] 2.2 (P) Adopt daily-price declarations and single-owner bounds
  - Declare the five-calendar-year and 5000-row policies once and make existing validation/clipping read them. Preserve actual interval/adjustment choices from the model and the local percentage conversion trace.
  - Done: existing date/leap/null/zero/duplicate/percentage fixtures and declaration/runtime checks pass. No local resampling or adjustment is introduced; whole production scope passes 400/300/50 and owning checks.
  - _Boundary: FMP models/equity_historical.py and tests/providers/test_fmp_daily_history.py only._
  - _Depends: 1_
  - _Requirements: 4.2, 4.4, 6.1, 6.2, 7.3_

- [ ] 3. (P) Implement the shared schema projection
  - Read the frozen annotations and real route/model associations from installed registry types. Produce x-qopenbb-financial descriptors, namespaced metadata/response references and the actual nested result metadata location. Use actual parameter defaults/enums/provider choices and check provider-policy agreement across variants.
  - Preserve unrelated operations and input documents. Missing required or malformed annotations fail explicitly; unknown declared values remain unknown. Do not infer units from names, copy widget semantics, enumerate FRED series or assert unrestricted extra enforces the financial schema. Error components describe contracts; handler implementation remains main task 4.3.
  - Done: fixture-based projection tests verify determinism, nonmutation, idempotence, serialized aliases, resolvable references and explicit missing/invalid declaration behavior. Real-model verification belongs to task 5 below. Production scope passes 400/300/50 and owning checks.
  - _Boundary: Root services/data-api/qopenbb_data/financial_openapi.py and tests/providers/test_financial_openapi.py only. Request a cohesive companion extraction before exceeding caps; no accepted provider edits in this lane._
  - _Depends: 1_
  - _Requirements: 1.1, 4.1, 4.2, 5.1, 5.2, 5.3, 6.1, 6.3_

- [ ] 4. Remaining bounded source adoption
- [ ] 4.1 (P) Preserve income-statement baseline semantics in declarations
  - Adopt static definitions and the baseline provider policy without changing limit-zero, excess-row behavior, aliases or HTTP error compatibility. Describe the response policy instead of inventing a fixed clipping limit.
  - Done: existing income/error cases and declaration/runtime agreement pass. Whole-file caps pass; if adding declarations exceeds the current file budget, extract income data declarations into a single owned companion first.
  - _Boundary: FMP models/income_statement.py, optional cohesive income_statement_data.py and tests/providers/test_income.py only._
  - _Depends: 1_
  - _Requirements: 4.1, 4.2, 4.3, 6.1, 6.2, 6.3_
- [ ] 4.2 (P) Adopt balance-sheet and cash-flow declarations
  - Move static templates and declared policy for the two statement families. Preserve instant balances, flow-period inference and the unknown opening-cash date, alongside query bounds and observed clipping.
  - Done: existing balance/cash fixtures and agreement checks pass with unchanged result metadata; all changed production files pass 400/300/50 and owning checks.
  - _Boundary: FMP balance_sheet.py/balance_sheet_data.py and cash_flow.py/cash_flow_data.py, with their existing focused metadata tests only._
  - _Depends: 1_
  - _Requirements: 4.1, 4.2, 4.3, 4.7, 6.1, 6.2_
- [ ] 4.3 (P) Adopt profile declarations with baseline defaults
  - Preserve multi-symbol behavior, mixed row currencies, price/market-cap semantics, baseline defaults and typed-error compatibility. Declare unknown quote dates without inferring them from financial dates.
  - Done: existing profile/transport checks and agreement cases pass; metadata remains unchanged and whole-file caps/owning checks pass.
  - _Boundary: FMP models/equity_profile.py and tests/providers/test_profile.py only; shared transport helpers remain frozen._
  - _Depends: 1_
  - _Requirements: 4.1, 4.2, 5.2, 6.1, 6.2, 6.3_
- [ ] 4.4 (P) Adopt discovery and peer declarations
  - Declare identity-field semantics, provider-selection requirement and local bounds. Preserve ambiguous listings, issuer separation and provider-suggestion labels; keep actual source values and missing dates runtime-owned.
  - Done: existing discovery fixtures and agreement checks pass with no parallel unit definitions; production files pass 400/300/50 and owning checks.
  - _Boundary: FMP models/equity_search.py, equity_peers.py, discovery_data.py and tests/providers/test_fmp_discovery.py only._
  - _Depends: 1_
  - _Requirements: 4.1, 4.2, 5.1, 6.1, 6.2_
- [ ] 4.5 (P) Adopt ratio and enterprise-input declarations
  - Preserve fraction/percentage distinctions, per-share units and unknown valuation dates/bases. Source annotations and runtime metadata share templates. Keep enterprise core schema and isolated router unchanged unless a concrete contract defect requires controller review.
  - Done: existing ratio/enterprise fixtures and agreement checks pass; no house valuation is added. Changed production files pass 400/300/50 and owning checks.
  - _Boundary: FMP financial_ratios.py/financial_ratios_data.py and enterprise_values.py, plus their existing focused tests only._
  - _Depends: 1_
  - _Requirements: 4.1, 4.2, 4.7, 6.1, 6.2_
- [ ] 4.6 (P) Declare dynamic FRED financial metadata
  - Describe dynamically named columns and runtime-resolved source/effective units, frequency, transformations, vintage and availability. Static declarations identify the resolution location; do not enumerate series IDs or copy runtime transformation mappings into projection code.
  - Preserve wide results, legacy per-series keys, oldest acquisition time and baseline selection policy. No cache behavior changes.
  - Done: existing FRED series/provenance checks and static/dynamic agreement cases pass; no fabricated fixed units or point-in-time claim. Whole changed file passes 400/300/50 and owning checks; request a cohesive provider-local metadata extraction if necessary.
  - _Boundary: FRED models/series.py, approved provider-local metadata companion if caps require, and existing series metadata tests only; cache/rate-limiter files remain frozen._
  - _Depends: 1_
  - _Requirements: 4.1, 4.4, 4.8, 6.1, 6.2, 7.5_

- [ ] 5. Join real declarations and accept the projection component
  - Validate projection against actual registered baseline models and their route associations, plus an isolated native registry/router test assembled from the accepted first-batch classes. Keep production provider.py and router mounts unchanged until main task 5.1; record this distinction explicitly.
  - Check first-batch coverage, field references, variant policy consistency, static FMP and dynamic FRED descriptors, actual serialized metadata and rejected missing annotations. Fixture-only success cannot close this task. Preserve safe response schema references and existing results/extra locations.
  - Done: one combined affected verification set and independent review establish authoritative declaration/runtime/projection agreement. The controller synchronizes exact source pins, maintained inventory, breadth and concise reviewed evidence before accepting main task 4.1. Its later installed-runtime wiring remains main task 5.2. Whole-file caps and shared-module audit pass.
  - _Boundary: Explicit controller integration: tests/providers/test_financial_openapi.py and agreement tests, source locks/inventory/breadth/evidence; no new registry implementation, generation wiring or public runtime activation._
  - _Depends: 2.1, 2.2, 3, 4.1, 4.2, 4.3, 4.4, 4.5, 4.6_
  - _Requirements: 1.1, 4.1, 4.2, 4.4, 4.8, 5.1, 5.2, 5.3, 6.1, 6.2, 6.3, 7.3, 7.5, 8.1, 8.4_

After task 1 is independently accepted, the adoption/projection tasks have disjoint production paths and can be scheduled in any dependency-safe order, at most two implementers concurrently. Shared test setup, contract changes, installation, joins and commits stay serialized. Remaining main tasks 4.2-6.3 keep their existing approvals and responsibilities; local subtask IDs here are scoped to this repair document.
