# Implementation tasks: reusable financial data, batch 1

Requirements and design were approved on 2026-10-28. This plan makes the approved first financial-input batch executable. It does not authorize all later families by implication or complete the umbrella specification. Task estimates are 1ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã¢â‚¬Â¦Ãƒâ€šÃ‚Â¡ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã¢â‚¬Â¦Ãƒâ€šÃ‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â¦ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¡ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã¢â‚¬Â¦Ãƒâ€šÃ‚Â¡ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¦ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¡ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¦ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¦ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã¢â‚¬Å“3 hours of focused work, not elapsed delivery promises. If a unit exceeds that boundary, split it at a cohesive seam before continuing; do not waive complexity limits.

## Execution contract and ownership

Use Sol for bounded implementation and Astra for financial/shared-contract integration review. Controller owns joins, source pins, generated artifacts, acceptance and per-task commits. Maximum four active agents: controller, two implementers, reviewer. Each worker receives its own exact file list, current dependencies and the design contract, and must preserve others' edits. Freeze worker edits before selective staging.

The explicit dependency graph below overrides generic sequential ordering under delegation.md. `(P)` permits overlap only after its listed prerequisites are independently accepted. Shared registration, app wiring, dependency installs, fixtures and catalog promotion remain serialized. One heavy suite/build at a time; Playwright one worker initially, xdist at most two. Never share mutable test setup between simultaneous lanes.

Production completion means whole-file caps of 400 physical lines, 300 logical units and 50/function pass. Use the existing `pipeline/.venv/bin/python -m tools.quality.complexity --check` command with actual fork change manifests or clean base/head identities as documented in [complexity checks](../../../docs/complexity.md); task 1.1 freezes concrete invocation inputs. Tests/generated evidence/docs are excluded, not hand-maintained production logic. Every task includes independent review and meaningful affected checks; no new harness. Runtime provider acceptance remains separate from deterministic fixture tests.

| Lane | Exclusive production paths from design | Join-only paths |
| --- | --- | --- |
| Shared contract | Core financial_metadata, financial_errors, financial_validation modules | Scope inventory: controller |
| FMP transport | FMP utils/helpers, errors, definitions | No provider registration |
| FMP dataset worker | Only the named model and approved companion data declarations for its task | FMP provider.py and provenance.json: controller |
| FRED acquisition | FRED utils/acquisition, cache, rate_limiter in dependency order | No simultaneous series edits |
| FRED series | FRED models/series.py | None |
| Consumer projection | qopenbb_data/financial_openapi.py | No pipeline duplicate projection |
| Runtime policy/errors | qopenbb_data/financial_policy.py or financial_errors.py, separate owners | app.py/config.py wiring: controller |
| Catalog | pipeline catalog_financial.py/catalog.py, then runtime/upstream generation adapters | Source locks and generated contracts: controller |
| Enterprise values | Core enterprise_values model, FMP enterprise_values model, small enterprise_router | Existing fundamental-router mount: controller |

Task 1.1 must reconcile the pre-existing unrelated changes in complexity inventory and catalog CLI/renderer files before assigning overlapping files. Preserve those edits; do not silently stage or revert them. Each task owns a separate behavior test file or explicitly serialized existing test file. Exact paths follow design.md; this table constrains assignment rather than creating alternate components.

## 1. Prepare and freeze shared contracts

- [x] 1.1 Establish the actual baseline, maintained scope and verification runtime
  - Controller records root/fork identities and existing dirty paths, restores/checks the existing locked environments, and prepares actual change manifests and scope inventory for this batch.
  - Characterize baseline profile/income/FRED response shapes and income zero-limit semantics. Record historical source recovery points and baseline generation provenance without claiming new live coverage.
  - Done when focused baseline checks run, original unrelated changes remain intact, and the executable complexity invocation rejects a deliberately missing maintained path using the existing checker tests. No new checker is built.
  - Caps: inventory/config changes meet 400/300/50 where applicable; evidence/tests are excluded. Any oversized planned module gets a cohesive extraction before dispatch or returns to design.
  - _Boundary: Baseline and verification setup_
  - _Requirements: 8.1, 8.5_

- [x] 1.2 Define typed financial metadata without changing existing result envelopes
  - Own the common metadata module and a focused metadata serialization test. Freeze reserved namespace, UTC acquisition timestamps, field semantics, unknown completeness, source identifiers and nonsecret effective queries.
  - Done when AnnotatedResult preserves validated metadata through OBBject and legacy FRED series keys remain collision-free in the fixture; invalid metadata and secret-bearing source/query fields are rejected.
  - Caps: common production model meets 400/300/50; schema output/tests are excluded.
  - _Boundary: Financial metadata_
  - _Depends: 1.1_
  - _Requirements: 4.1, 4.2, 4.4, 4.5, 4.6, 4.7, 4.8, 6.2, 7.2_

- [x] 1.3 (P) Define safe typed failures and result validation
  - Own the core error and validation helpers; freeze category/status/retry attributes and bounded recognized-wrapper unwrapping. No arbitrary exception-string parsing or unsafe cause retention.
  - Done when malformed provider rows and nested wrappers produce safe categories, request/result failures remain distinct, and secret canaries never appear in serialized errors.
  - Caps: both helpers meet 400/300/50; focused tests excluded.
  - _Boundary: Financial failures_
  - _Depends: 1.1_
  - _Requirements: 7.1, 7.2, 7.4, 8.4_

## 2. Restore FMP financial inputs

- [x] 2.1 Harden shared extraction and freeze provider query conventions
  - Own shared FMP transport/classification/period definitions. Reuse safe encoded requests, timestamp successful acquisition, and remove the unsafe multi-request bypass before any restored fetcher uses it.
  - Done when timeout, entitlement, throttling, malformed payload and bounded multi-request fixtures preserve safe categories; annual/quarterly bounds and no-new-retry behavior are stable for downstream adapters.
  - Caps: modified utilities meet 400/300/50, extracting cohesive transport code only if needed; tests excluded.
  - _Boundary: FMP transport_
  - _Depends: 1.2, 1.3_
  - _Requirements: 2.4, 2.5, 7.1, 7.2, 7.3, 7.4_

- [x] 2.2 Adapt existing profile and income behavior to the shared contract
  - Own existing profile/income modules and their existing focused tests, serially. Preserve accepted multi-symbol profile behavior and characterized income zero-limit handling; support verified fiscalYear/calendarYear and filingDate/fillingDate aliases.
  - Done when baseline values remain unchanged and metadata, missing values, acquisition time and query bounds survive serialization; any incompatible baseline behavior returns for explicit compatibility review.
  - Caps: both production files meet 400/300/50; split this unit into profile/income if whole-file extraction cannot fit its timebox.
  - _Boundary: Baseline FMP models_
  - _Depends: 2.1_
  - _Requirements: 2.1, 2.4, 4.1, 4.2, 4.3, 4.5, 6.3_

- [x] 2.3 (P) Restore annual and quarterly balance sheets
  - Own only balance-sheet fetcher/companion declarations. Adapt retained source, bound queries and preserve fiscal dates, currency, signed values and nulls.
  - Done when representative response fixtures validate and normalize without invented periods, and invalid bounds fail before I/O.
  - Caps: each production file meets 400/300/50; generated fixtures/tests excluded.
  - _Boundary: FMP balance sheets_
  - _Depends: 2.1_
  - _Requirements: 2.1, 2.4, 4.3, 4.5, 4.7_

- [x] 2.4 (P) Restore annual and quarterly cash-flow statements
  - Own only cash-flow fetcher/companion declarations. Preserve sign conventions, zero values, fiscal dates and units; do not infer cash conversion from unspecified definitions.
  - Done when signed/null/quarterly fixtures and pre-I/O bounds pass, with acquisition and financial metadata intact.
  - Caps: each production file meets 400/300/50; tests excluded.
  - _Boundary: FMP cash flows_
  - _Depends: 2.1_
  - _Requirements: 2.1, 2.4, 4.2, 4.3, 4.5_

- [x] 2.5 (P) Provide named discovery and provider peer candidates
  - Own search/peers models. Preserve provider-qualified listing/issuer attributes and ambiguous alternatives, with bounded search results and peer provenance.
  - Done when name and symbol cases return distinguishable identities, ambiguous results are retained, and peers are labeled provider suggestions rather than analyst selections.
  - Caps: models meet 400/300/50; tests excluded.
  - _Boundary: FMP discovery models_
  - _Depends: 2.1_
  - _Requirements: 2.1, 3.1, 3.2, 3.3_

- [x] 2.6 (P) Restore bounded daily price history
  - Own daily-history model only. Require ordered dates within the designed five-calendar-year window; retain price adjustment meaning, deterministic order and honest completeness.
  - Done when zero percentage change remains zero, inputs are not mutated, missing observations remain missing and excess ranges fail before I/O; unsupported intraday stays explicit.
  - Caps: production model meets 400/300/50; tests excluded.
  - _Boundary: FMP daily history_
  - _Depends: 2.1_
  - _Requirements: 2.1, 2.4, 2.5, 4.2, 4.4, 4.5, 7.3_

- [x] 2.7 (P) Restore periodic key metrics
  - Own key-metrics model and scoped companion declarations. Fetch only requested periodic data; remove inherited TTM date/currency fabrication rather than carrying it forward.
  - Done when provider-derived metrics retain their period, units, definitions and unknown bases; unsupported TTM fails explicitly.
  - Caps: production files meet 400/300/50; tests excluded.
  - _Boundary: FMP key metrics_
  - _Depends: 2.1_
  - _Requirements: 2.1, 4.2, 4.3, 4.6, 4.7_

- [x] 2.8 (P) Restore periodic financial ratios
  - Own ratio model and scoped companion declarations. Preserve fraction/percentage conventions and distinguish provider calculations from local analyst metrics.
  - Done when periodic, zero, negative and missing-value cases match source semantics and unsupported modes are rejected.
  - Caps: production files meet 400/300/50; tests excluded.
  - _Boundary: FMP ratios_
  - _Depends: 2.1_
  - _Requirements: 2.1, 4.2, 4.3, 4.5, 4.7_

- [x] 2.9 (P) Add the typed enterprise-value input dataset
  - Explicit model/adapter integration task: own new core standard model, FMP fetcher and isolated enterprise subrouter. Controller mounts it later; do not edit shared router/registration yet.
  - Done when price, shares, market cap, cash, debt and EV fixtures retain available dates/currency and unknown conventions; this does not assert an analyst-adjusted valuation bridge.
  - Caps: each changed production file meets 400/300/50; tests excluded.
  - _Boundary: Enterprise-value input contract integration_
  - _Depends: 2.1_
  - _Requirements: 2.1, 4.1, 4.2, 4.7, 5.4_

## 3. Preserve FRED semantics and cache provenance

- [x] 3.1 (P) Define acquisition envelopes and disk-cache compatibility
  - Own FRED acquisition/cache modules and isolated disk-cache tests. Version records/keys, preserve original retrieval timestamps and treat old records as misses without deleting unrelated cache data.
  - Done when opt-in acquisition envelopes round-trip and the default raw payload API remains compatible; disk-cache-off remains the installed default.
  - Caps: modified production files meet 400/300/50; tests excluded.
  - _Boundary: FRED acquisition storage_
  - _Depends: 1.2, 1.3_
  - _Requirements: 4.1, 6.3, 7.5_

- [x] 3.2 Propagate provenance through FRED memory and in-flight requests
  - Own rate-limiter integration after the envelope freezes. Preserve finite retries, coalescing and default raw callers; opt-in callers receive actual acquisition provenance.
  - Done when network/memory/disk/coalesced/bypass tests preserve original timestamps, bounded retry behavior and payload compatibility.
  - Caps: changed rate-limiter/helper scope meets 400/300/50; no broad unrelated rewrite.
  - _Boundary: FRED transport integration_
  - _Depends: 3.1_
  - _Requirements: 4.1, 7.4, 7.5_

- [x] 3.3 Preserve generic-series metadata, vintages and transformed units
  - Own the generic-series model. Preserve existing per-series metadata keys and wide columns; add the reserved common metadata, retained real-time intervals and separate source/effective units/frequency.
  - Done when levels, percent changes and aggregation have truthful semantics; unknown effective units are explicit, and original timestamps survive mixed-age inputs. No point-in-time claim follows from intervals alone.
  - Caps: changed series module/helpers meet 400/300/50; tests excluded.
  - _Boundary: FRED generic series_
  - _Depends: 3.2_
  - _Requirements: 3.5, 4.1, 4.4, 4.6, 4.8, 5.6, 6.3, 7.5_

## 4. Expose consistent consumer contracts

- [x] 4.1 (P) Generate the authoritative financial schema projection
  - Own financial_openapi only. Project installed model annotations to metadata schema references and operation descriptors; do not reconstruct semantics from widgets or add a registry.
  - Done when fixture OpenAPI documents disclose metadata location, query bounds/provider choices and safe response schemas, with resolvable references and deterministic output.
  - Caps: projection meets 400/300/50; generated schemas/tests excluded.
  - _Boundary: Financial schema projection_
  - _Depends: 1.2, 1.3_
  - _Requirements: 1.1, 5.4, 6.1, 6.2, 6.3_

- [x] 4.2 (P) Enforce provider selection before request execution
  - Own financial_policy only. Use generated installed operation descriptors to enforce explicit provider selection on the designed non-baseline paths; preserve three baseline defaults.
  - Done when omitted-provider requests fail before I/O, explicit selection is retained and failures cannot trigger a silent provider substitution. App wiring belongs to task 5.2.
  - Caps: guard meets 400/300/50; tests excluded.
  - _Boundary: Runtime provider policy_
  - _Depends: 4.1_
  - _Requirements: 5.1, 5.2, 5.3, 6.2_

- [x] 4.3 (P) Sanitize mounted-API failures and logs
  - Own service financial_errors only. Cover typed provider errors, request validation, invalid result rows, response validation and unexpected exceptions using the approved status/detail compatibility.
  - Done when nested wrapper and secret-canary tests prove safe categories/logs and bounded Retry-After; handlers are installation-ready for the upstream app, not only the outer service.
  - Caps: service handler meets 400/300/50; tests excluded.
  - _Boundary: Runtime financial failures_
  - _Depends: 1.3_
  - _Requirements: 7.1, 7.2, 7.4, 8.4_

- [x] 4.4 (P) Preserve financial descriptors in catalog snapshots and drift checks
  - Own catalog_financial and scoped catalog.py changes. Consume the single projection from 4.1; validate parameter values, provider associations, metadata references and compatibility changes.
  - Done when incompatible field/descriptor/default changes flag affected consumers and invalid parameter examples fail generation; no parallel schema source is created.
  - Caps: changed pipeline scope meets 400/300/50; fixtures/generated snapshots excluded.
  - _Boundary: Catalog contract validation_
  - _Depends: 4.1, 1.1_
  - _Requirements: 1.1, 5.4, 5.5, 6.1, 6.3_

- [x] 4.5 Build installed discovery with truthful coverage states
  - Own financial_catalog and the versioned coverage index, after catalog schema validation. Keep documented/retained/adapted/installed/access/data/widget/AI states independent; link evidence without exposing account details.
  - Done when /datasets.json fixture output identifies installed datasets, unknown access, unsupported families and schema/source identity; historical gallery examples cannot masquerade as live coverage.
  - Caps: discovery code meets 400/300/50; coverage data/tests excluded.
  - _Boundary: Installed discovery_
  - _Depends: 4.4_
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 2.6, 8.5_

## 5. Join the installed runtime and generated widgets

- [x] 5.1 Register the independently accepted provider models
  - Controller-only fork join: mount enterprise subrouter, register first-batch FMP models and retain provenance/notices. Prepare an isolated candidate source/dependency lock from the accepted committed fork and resolve/install it in the existing verification environment, serially. Do not promote root pins or activate later families yet.
  - Done when import/source identity checks prove that the candidate environment uses the exact committed fork and its locked dependencies, and installed-route/model checks expose all accepted first-batch commands with baseline compatibility intact. Task 5.2 uses this identified environment; final root pin/catalog promotion remains atomic in 5.3.
  - Caps: entire changed registration/router/provenance scope passes applicable 400/300/50; generated records excluded.
  - _Boundary: Provider registration integration_
  - _Depends: 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8, 2.9, 3.3_
  - _Requirements: 2.1, 5.1, 5.4, 5.5, 8.1_

- [ ] 5.2 Wire discovery, policy and error handling into the actual service
  - Controller-only runtime join in the identified candidate environment from 5.1: install projection and handlers on the upstream app, guard before forwarding and discovery before the mount. Retain health, credential isolation and baseline routes.
  - Done when ASGI tests prove mounted-app error sanitization, omitted-provider rejection, disclosure and Python/API agreement for actual installed models; no AI/browser service is required to query.
  - Caps: whole changed app/config scope meets 400/300/50; tests excluded.
  - _Boundary: Runtime contract integration_
  - _Depends: 5.1, 4.2, 4.3, 4.5_
  - _Requirements: 1.1, 5.1, 5.2, 5.3, 6.2, 6.5, 7.1, 7.2_

- [ ] 5.3 Regenerate native consumer proposals from the identified runtime
  - Controller owns root source/dependency pins and generated contracts; generation adapter changes are serialized. Reuse upstream widget generation and current proposal/drift tooling, preserving unrelated renderer work.
  - Done when fresh proposal artifacts resolve every installed route/schema, carry exact generator/source provenance, retain baseline widget IDs and can drive parameterized queries beyond AAPL examples.
  - Caps: maintained generation adapters meet 400/300/50; generated JSON excluded. Promote only after independent compatibility review.
  - _Boundary: Generated consumer integration_
  - _Depends: 5.2_
  - _Requirements: 1.1, 2.4, 6.1, 6.3, 8.1, 8.5_

## 6. Verify and deliver the bounded batch

- [ ] 6.1 Verify real financial inputs and endpoint access
  - Use existing marked provider tests with private configuration; collect sanitized actual responses for one nonfinancial company and a small peer set, plus FRED context. Check statement periods, shares/EV bases, price units and provenance.
  - Done when displayed/programmatic values can be compared with actual provider observations and relevant edge/failure tests pass; denied entitlement stays blocked, not replaced by gallery snapshots. Later-family criteria remain open.
  - Caps: tests/evidence-only excluded; any production repair returns to its owning capped task.
  - _Boundary: Financial acceptance_
  - _Depends: 5.3_
  - _Requirements: 2.1, 2.6, 4.1, 4.2, 4.3, 4.5, 4.7, 4.8, 8.3, 8.4_

- [ ] 6.2 Verify the packaged exploratory widget journey
  - Build the candidate through existing Dagger tooling after source checks; reuse the isolated Workspace harness for installed discovery, changing company/period and comparing visible real values with the accepted API data. Keep browser/CDP diagnostics clean.
  - Done when a second supported symbol works without dashboard-specific plumbing and visible errors/metadata are truthful. New shared-dashboard/scenario persistence remains analyst-workspace scope.
  - Caps: tests/evidence/generated output excluded; production fixes reopen their capped task. This is one integrated journey, not a separate harness per dataset.
  - _Boundary: Packaged consumer acceptance_
  - _Depends: 6.1_
  - _Requirements: 2.4, 3.1, 6.1, 6.2, 6.5, 8.2, 8.3, 8.4_

- [ ] 6.3 Independently accept and publish the financial-input milestone
  - Controller joins scoped checks, whole-file caps, source/image identities and independent review; updates breadth and affected README/docs checkboxes with exact limits before the per-task commit.
  - Done when one feature-complete pipeline publishes both images and its tagged release, assets and anonymous pulls are verified. Do not rebuild on each source or documentation commit; do not claim owner-server deployment.
  - Caps: evidence/docs only excluded; existing implemented checker and actual current manifests must pass for the joined production scope.
  - _Boundary: Milestone delivery integration_
  - _Depends: 6.2_
  - _Requirements: 8.1, 8.2, 8.5_

## Follow-on scope: not executable in this batch

The approved design explicitly requires separate concrete endpoint/file briefs before these later batches. They remain unchecked scope obligations; this task plan does not pretend that research or a coverage index implements them. Task approval here authorizes only 1.1ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã¢â‚¬Â¦Ãƒâ€šÃ‚Â¡ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã¢â‚¬Â¦Ãƒâ€šÃ‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â¦ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¡ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã¢â‚¬Â¦Ãƒâ€šÃ‚Â¡ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¦ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¡ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¦ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¦ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã¢â‚¬Å“6.3. Before starting any row below, generate its bounded design/task amendment using retained OpenBB code and the same independent review.

| Open delivery | Requirements still open in whole or in part | Next concrete planning input |
| --- | --- | --- |
| FMP DCF/custom-DCF, estimates and segment detail | 2.2, 2.3, 4.2, 4.7 | Actual endpoints/entitlement, declared model assumptions and safe provider parameter schema; no local valuation engine |
| Inline news, transcripts and filing/report content | 2.3, 6.4 | Content/attribution/partial-text contracts and native text-widget mapping |
| Funds, ownership, cross-market and remaining agreed FMP families | 1.4, 2.3, 8.3 | Dataset-by-dataset restoration/API gap map from retained source and endpoint inventory |
| Yahoo price supplementation and extended FRED exposure | 3.4, 5.4, 5.5, 5.6 | Compatible owned-source dependency lock, explicit spot/futures/roll semantics and installed route coverage |

All 44 criteria are referenced in executable tasks or this explicit follow-on map. Mapping is not completion. No task may close the umbrella requirements while these obligations remain open. Database and AI execution remain in their separate specs.

## Implementation notes

- 1.1 accepted 2026-10-28: [baseline and independent review](../../../artifacts/reviewed/market-data-foundation/result.md). Existing provider environment restored; source overrides are required for new fork edits. Income zero-limit remains unchanged. Real-provider access remains unverified.

- 1.2 accepted: data fork `08978188584`, 34 metadata checks and independent review; [evidence](../../../artifacts/reviewed/market-data-metadata/result.md). Final whole-file size 193/115/9 (physical/logical/max function); shared 77-file gate passes. Runtime consumers and source pin promotion remain later joins.

- 1.3 accepted: data fork `ee6e37a7dc1`, 27 safe-error/validation checks plus independent verification and owning-fork lint; [evidence](../../../artifacts/reviewed/market-data-errors/result.md). Final helpers measure 120/67/17 and 36/13/4. API handlers and fetcher adoption remain later tasks. Include owning-fork Ruff configuration in subsequent worker validation.

- 3.1 accepted: data fork `852a80f1b82`, 16 disk/acquisition tests, owning-fork lint and independent review; [evidence](../../../artifacts/reviewed/market-data-fred-acquisition/result.md). Joined 82-file gate passes. Old cache records miss without deletion; raw payload shape remains compatible. Memory/in-flight integration follows in 3.2.

- 2.1 accepted: data fork `20e2ef1b1b4`, 62 transport/profile/income/error checks, independent review and lint; [evidence](../../../artifacts/reviewed/market-data-fmp-transport/result.md). Joined 82-file gate passes. Default callers retain legacy error compatibility; provenance opt-in uses exact typed financial errors and acquisition timestamps. Dataset truncation/completeness belongs to subsequent adapters.

- 3.2 accepted: data fork `a41fbb40273`, 30 propagation/acquisition/FRED tests, independent review and owning-fork lint; [evidence](../../../artifacts/reviewed/market-data-fred-propagation/result.md). Joined 85-file gate passes. Original timestamps survive cache/coalesced paths; raw defaults and finite retry behavior remain. Generic-series financial metadata follows in 3.3.

- 2.2 accepted: data fork `c4de6b13505`, 79 baseline/error/transport checks, independent financial review, lint and Node 24.22.1 combined gate; [evidence](../../../artifacts/reviewed/market-data-fmp-baseline-metadata/result.md). A narrowly reviewed helper option separates acquisition provenance from typed errors, preserving baseline HTTP categories, zero-limit rows and multi-symbol values. No new provider registration is activated.

- 3.3 accepted: data fork `d1bb4821a65`, 21 series/legacy tests, independent review, lint and Node 24.22.1 combined gate; [evidence](../../../artifacts/reviewed/market-data-fred-series/result.md). Legacy wide rows and per-series metadata remain; common metadata preserves available observation intervals, oldest component freshness and explicit unknown transform units. This does not establish point-in-time safety or live access.

- CI source identity: the portable gate checks every maintained file in the locked fork. When accepted new helper/model files enter the inventory, synchronize the accepted fork revision and both root source mirrors before pushing. Keep provider registration and catalog proposal promotion in their owning tasks; a component source-pin join does not complete 5.1 or 5.3.

- 2.3 accepted: data fork `072a6c6c2bf374d4f33b43bbed5d95c5eff34275`; [statement evidence](../../../artifacts/reviewed/market-data-statements/accepted.md), independent review and focused numerical/schema checks. Source adapters only; registration/live acceptance remain open.

- 2.4 accepted: data fork `93d34aebaef3d1c0ddaaa981f5aefd9bdb2f546d`; [statement evidence](../../../artifacts/reviewed/market-data-statements/accepted.md), independent review and focused numerical/schema checks. Source adapters only; registration/live acceptance remain open.

- 2.5 accepted: data fork `39f504c0c452903e684122699497eb79606c108e`; [discovery and price evidence](../../../artifacts/reviewed/market-data-discovery-prices/accepted.md), independent review and focused numerical/schema checks. Source adapters only; registration/live acceptance remain open.

- 2.6 accepted: data fork `1907741737d7d2d71f4fa3534610857da56674f7`; [discovery and price evidence](../../../artifacts/reviewed/market-data-discovery-prices/accepted.md), independent review and focused numerical/schema checks. Source adapters only; registration/live acceptance remain open.

- 2.7 accepted: data fork `e5cfbd5a2c96698dbc22347befa2521a88d90e7e`; [metrics and ratio evidence](../../../artifacts/reviewed/market-data-metrics-ratios/accepted.md), independent review and focused numerical/schema checks. Source adapters only; registration/live acceptance remain open.

- 2.8 accepted: data fork `4bef44cd5622f834df0b9afdb20c0d1f1183f013`; [metrics and ratio evidence](../../../artifacts/reviewed/market-data-metrics-ratios/accepted.md), independent review and focused numerical/schema checks. Source adapters only; registration/live acceptance remain open.

- 2.9 accepted 2026-10-29: data fork `d8589764cfd03a4fca40cabd14de9620a194f0eb`; [enterprise-value source acceptance](../../../artifacts/reviewed/market-data-enterprise-schema/accepted.md), 24 focused/independent tests, owning Ruff and 77-file combined gate. Isolated router is unmounted; registration/live/consumer acceptance remain open.

- 4.1 accepted 2026-10-29: all eleven annotation repair tasks complete; [native projection acceptance](../../../artifacts/reviewed/annotations-native-join/accepted.md), independent 389-test combined suite, final native/lint verification and shared-module audit. Main progress 16/26.
- Native API integration note: use upstream `iter_api_routes` for lazy route contexts; derive canonical success schemas from actual `route.response_model` rather than retaining alias-based native schemas under `allOf`.

- Main4.3 accepted 2026-10-29: [safe mounted API failure component](../../../artifacts/reviewed/market-http-errors/accepted.md), independent38 tests, sensitivity control and caps. Shared formatter is the policy guard dependency; activation remains main5.2.

- Main4.2 accepted 2026-10-29: [descriptor-driven provider guard](../../../artifacts/reviewed/market-provider-policy/accepted.md), independent126-test guard/handler/core/projection join and caps. Main source progress18/26; runtime wiring remains5.2.

- Main4.4 accepted 2026-10-29: [catalog validation and drift](../../../artifacts/reviewed/market-financial-catalog/accepted.md), independent54-test verification and native three-model projection probe after metadata-map repair. Runtime/catalog promotion remain later tasks.

- Main4.5 accepted 2026-10-29: [installed discovery and coverage index](../../../artifacts/reviewed/market-financial-discovery/accepted.md), independent discovery/projection join, public proof identities and capped source. Main20/26; registration, mounted discovery and reusable widget generation remain5.1-5.3.

- Main5.1 accepted: [installed registration candidate](../../../artifacts/reviewed/market-provider-registration/accepted.md), exact candidate fork13e41631bdef0ee98bfa23bda68d329224b56eb1, independent76-test join and81-file cap gate. Main21/26. Root source/catalog pins remain at the deployed baseline until5.3.

## Implementation Notes

- Candidate5.1: `artifacts/market-registration/candidate-private.json` identifies the retained source/project snapshot. Acceptance uses installed provider/core packages; inject only the root service into PYTHONPATH. Project only the eleven annotated first-batch models, preserving other existing FRED routes. Prefer host Git or immutable blob/archive reads over WSL worktree scans on the mounted fork.

- HTTP verification: the pinned provider environment has no httpx; reuse the direct ASGI helpers. Native Fetcher classes alias extraction at class creation, so patch `extract_data` and retain a transport tripwire. Normalize UTF-8/LF and one EOF newline before freezing hashes; record subprocess return codes directly.
