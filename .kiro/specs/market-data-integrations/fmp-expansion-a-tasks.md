# Batch A FMP implementation plan

Owner approved execution and the 48-request ceiling on 2026-11-17. Completion boxes require independent review and fresh evidence.
Design approval is recorded in spec.json; preserve design SHA-256
59ca002fc71585e20edfb9dc431b35605e8f2bff2d78b8d04543f7f552cb3a7a.
Execution workspaces: D:/BuildArtifacts/QOpenBB/fmp-expansion-a/root and sibling ../data-api; the accepted Company Research checkouts remain preserved.
Baseline root 3b47ead262aac62a1c4a9f275694bd3e72f83056; API a965f70c164fe477ce9c99654b9be48e2f1bc9fd.
Retained FMP 1.6.1 archive SHA-256: 5f6f27af6283075912df42f373c45ed37bc6970097342ed73110fb6101be5517.

## Execution contract

Every executable task is a 1-3 hour unit. Checkboxes remain open until actual acceptance.
Use controller plus at most two gpt-6.1-sol implementers and one independent reviewer;
gpt-6-astra reviews financial semantics, shared admission and joins with fresh context.
Each task: implement, independent review, fresh scoped checks, accepted evidence, selective per-task commit.
Freeze worker edits before staging; serialize commits, installs, shared mutations and heavy checks.
No worker may revert another worker's edits. One bounded adapter task per dispatch.
Worker handoffs include exact frozen contracts, writable paths, implemented commands and 400/300/50 caps.
Changed production files pass whole-file 400 physical / 300 logical units and 50 units per function.
Tests, generated contracts and evidence are excluded from production caps; generator logic is capped.
No new framework, standard-model rewrite, shared transport rewrite, dependency upgrade, AI or Excel.
Anthropic acceptance remains mandatory before any future Excel implementation.
Core steering product.md, tech.md and structure.md are absent as recorded in approved design.
This draft uses available approved requirements/design and complexity/testing/ci/delegation steering.

Controller exclusively owns shared contract fixtures, inventory/checker scope, admission, registry,
provenance, source pins, catalog projection changes and generated-contract joins.
Adapter workers own only their named provider module plus endpoint-local tests/fixtures.
Frozen contracts under tests/providers/fixtures/fmp_batch_a/contracts/ are controller-owned, read-only to workers.
Endpoint fixture additions use dedicated same-stem paths; no common conftest/helper edits during fan-out.
Any additional cohesive growth declaration module is assigned in 1.4 before dispatch; never overlap ownership.
Required route composition repairs stop the affected endpoint for bounded controller review; no oversized router edits.
Only tasks 3.1-3.11 may run concurrently; their dependencies override ordinary sequential peer ordering.
A1 and A2 each run one task at a time, with at most two adapter implementers total.
All other tasks are serial. Contract/schema/pin changes invalidate affected proofs and pause fan-out.

## 1. Characterization and executable scope foundation

- [x] 1.1 Establish reproducible source and complexity scope (1-2 hours)
  - Verify accepted roots/revisions and retained archive hash/notices; record selected recovery members only.
  - Extend existing inventory/checker to all new/modified root and API production paths with explicit base/head scope.
  - Done: actual repository complexity command is recorded and passes baseline scope; missing scope fails closed.
  - Use tools.quality.complexity --check with actual --repository-root and actual changed manifests/base-heads; no historical head reuse.
  - Production checker changes pass 400/300/50; generated inventories/test evidence are excluded.
  - _Boundary: Controller source recovery and complexity inventory_
  - _Requirements: 8.1, 8.5_

- [x] 1.2 Characterize five A1 retained contracts without production adapters (2-3 hours)
  - Recover schema/alias declarations into isolated fixture or dedicated test query classes, never production registration.
  - Record validation/serialization schemas, annotations for every field, nullable dates, units and source references.
  - Check official parameter spellings, price-target limit uncertainty, float percent convention and retained field union.
  - Done: reviewed manifests and exact focused test commands exist for the five A1 endpoints, with incompatibilities explicit.
  - Schema contradictions stop affected endpoints for reviewed design amendment; no live entitlement prerequisite or calls.
  - Fixtures/tests have no production caps; any maintained characterization helper passes 400/300/50.
  - _Boundary: Controller frozen contract fixtures_
  - _Requirements: 2.4, 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7, 6.1, 6.3_

- [x] 1.3 Characterize six A2 retained contracts without production adapters (2-3 hours)
  - Apply 1.2 recovery/schema/alias/annotation method to cap, float, quote and three growth variants using dedicated test classes.
  - Confirm float percentage/nullable dates, cap date windows, quote epochs and growth fraction/fiscal meanings against frozen policies.
  - Done: six A2 manifests, source references and focused commands pass independent review; contradictions stop affected endpoints.
  - Fixtures/tests excluded from production caps; maintained characterization helpers pass 400/300/50.
  - _Boundary: Controller A2 frozen contract fixtures_
  - _Requirements: 2.4, 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7, 6.1, 6.3_

- [x] 1.4 Freeze admission descriptors and adapter handoffs (1-2 hours)
  - Freeze canonical fields/accepted aliases, actual native controls and endpoint-local ownership from 1.2 and 1.3.
  - Follow [explicit-route admission amendment](fmp-expansion-a-admission-amendment.md): native-selected class-owned opt-in with separate eleven-variant registry/discovery expected-set joins, pre-validate raw binding, safe selected errors, context lifecycle/provider reuse, effective validation and direct Fetcher cases.
  - Freeze proposal descriptors and pending 2.1/2.3 verification matrix; native defect characterization is not repaired-admission acceptance.
  - Assign any cohesive declaration extraction before fan-out; standards and routers stay read-only absent reviewed blocker.
  - Done: independent reviewer accepts all eleven contracts plus disjoint handoffs; test descriptors support prereq testing.
  - This resolves the chicken-and-egg: prerequisites use fixture/dedicated query classes; later real subclasses match schemas.
  - Contract artifacts are excluded; maintained support code passes 400/300/50.
  - _Boundary: Controller frozen contract and handoff integration_
  - _Requirements: 2.4, 5.4, 6.1, 6.3, 7.3_

## 2. Public admission prerequisites

- [x] 2.1 Enforce selected-provider admission through public native SDK (2-3 hours)
  - Implement [explicit-route admission amendment](fmp-expansion-a-admission-amendment.md) in its exact five controller-owned API paths: admission helper/context, decorators, Container and metadata-only method emitter. The [supplied-value correction](fmp-expansion-a-sdk-alias-correction.md) adds only the scoped native filter hook and its listed repair paths.
  - Preserve native validate_call/signatures/arbitrary_types and provider resolution; capture raw supplied membership before validation, reuse matching provider once, consume owned context frame once and reset token in finally.
  - Resolve installed descriptors/RegistryMap; use dedicated registered strict query variants with actual Container/CommandRunner descriptors and public generated entry, without intercepted _run or fake selection.
  - Replace/adapt known-defect characterization assertions after repair; historical reproduction is not admission acceptance.
  - Reject caller unsupported keys even at default values; preserve null/bool presence and reject invalid effective defaults.
  - Done: public generated SDK tests prove zero-I/O rejection, valid controls and unchanged baseline/provider resolution. Re-acceptance also requires all six periodic variants to pass quarter/quarterly/default/precedence cases through explicit and omitted FMP selection.
  - Direct Fetcher dictionaries use the same strict selected query contract; Query/CommandRunner are not certification surfaces.
  - Prove all amendment matrix cases: safe selected early/effective errors with DEBUG_MODE on/off, defaults, positional/alias/control semantics, nested/thread/task lifecycle and unchanged baseline variants.
  - Whole new/other modified files pass 400/300/50; emitter change requires independent review of exact final metrics and any narrow revision/expiry-bound exception before acceptance. No speculative exception or CommandRunner rewrite.
  - _Boundary: Controller core admission and public SDK tests_
  - _Depends: 1.4_
  - _Requirements: 2.4, 5.1, 5.2, 5.4, 6.3, 7.1, 7.2, 7.3_

- [x] 2.2 Reject invalid HTTP requests before filtering and upstream dispatch (2-3 hours)
  - Extend financial_query_policy and financial_policy using selected installed schema/aliases and actual control signatures.
  - Reject missing explicit FMP, repeated symbol/page, unknown/other-provider keys, explicit null/bool and malformed symbols.
  - Preserve safe invalid_parameters/422 envelopes without raw values/credentials and baseline variant behavior.
  - Done: mounted HTTP tests against dedicated registered test models reject before Fetcher/network; valid controls pass.
  - Whole changed production files/functions pass 400/300/50; serialize shared test fixture edits.
  - _Boundary: Controller HTTP admission and mounted policy tests_
  - _Depends: 2.1_
  - _Requirements: 2.4, 5.1, 5.2, 5.3, 6.3, 7.1, 7.2, 7.3_

- [ ] 2.3 Accept joined prerequisites before adapter fan-out (1-2 hours)
  - Exercise SDK, HTTP and raw Fetcher surfaces with frozen test variants and shared baseline variants.
  - Include unsupported explicit defaults, invalid configured defaults, repeated scalars and no-I/O request counters.
  - Done: independent Astra review plus fresh focused admission/compatibility checks pass at recorded revisions.
  - Freeze interfaces and test fixtures; any later contract change repeats affected prerequisite checks before dispatch.
  - Test-only proof is excluded from production caps; audit changed admission files against 400/300/50.
  - _Boundary: Controller prerequisite integration gate_
  - _Depends: 1.4, 2.1, 2.2_
  - _Requirements: 2.4, 5.4, 6.2, 6.3, 7.1, 8.4_

## 3. Disjoint retained adapters

All tasks below depend on 1.4 and 2.3; no adapter may start on an unreviewed prerequisite.
Each task adapts the retained module to FMPAcquisition, typed safe errors and AnnotatedResult metadata v1.
Each validates its real new strict query subclass against frozen schemas before accepting production behavior.
Common endpoint checks: aliases, exactly one request, invalid inputs before I/O, empty/missing/null/zero,
bounds/completeness, financial annotation coverage, auth/entitlement/throttle/retry-after/timeout/malformed errors.
Do not introduce new metadata fields, infer missing currency/vintage, or deduplicate by date.

- [ ] 3.1 (P) Restore analyst-estimates financial behavior (2-3 hours)
  - Freeze annual/quarter alias, limit 20 (1..100), page 0 (0..10); forward once and clip to limit.
  - Forecast fiscal end is not publication; retain low/high/average/count, estimate origin and unknown vintage.
  - Done: AnalystEstimates matches frozen query/result schemas and endpoint-specific plus common offline checks pass.
  - Own only models/analyst_estimates.py, test_fmp_analyst_estimates.py and same-stem endpoint fixtures; frozen contracts read-only.
  - Changed production module/declaration files pass 400/300/50; tests/fixtures excluded; independent review then fresh checks.
  - _Boundary: A1 AnalystEstimates adapter_
  - _Depends: 1.4, 2.3_
  - _Requirements: 2.3, 2.4, 2.5, 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7, 5.1, 5.3, 5.4, 6.1, 7.1, 7.2, 7.3, 7.4, 7.5, 8.4_

- [ ] 3.2 (P) Restore price-target-news financial behavior (2-3 hours)
  - Require symbol, limit 20 (1..100); no public page; stop on documented limit-contract contradiction.
  - Keep event publication precision/timezone, attribution, adjustments and posted-price versus target origins.
  - Done: PriceTarget matches frozen query/result schemas and endpoint-specific plus common offline checks pass.
  - Own only models/price_target.py, test_fmp_price_target.py and same-stem endpoint fixtures; frozen contracts read-only.
  - Changed production module/declaration files pass 400/300/50; tests/fixtures excluded; independent review then fresh checks.
  - _Boundary: A1 PriceTarget adapter_
  - _Depends: 1.4, 2.3_
  - _Requirements: 2.3, 2.4, 2.5, 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7, 5.1, 5.3, 5.4, 6.1, 7.1, 7.2, 7.3, 7.4, 7.5, 8.4_

- [ ] 3.3 (P) Restore price-target-consensus financial behavior (2-3 hours)
  - One matching-symbol singleton; duplicate or foreign-symbol rows fail; no extra query parameters.
  - Keep high/low/median/consensus separate; dated methodology is limitation text, not response lineage/date.
  - Done: PriceTargetConsensus matches frozen query/result schemas and endpoint-specific plus common offline checks pass.
  - Own only models/price_target_consensus.py, test_fmp_price_target_consensus.py and same-stem endpoint fixtures; frozen contracts read-only.
  - Changed production module/declaration files pass 400/300/50; tests/fixtures excluded; independent review then fresh checks.
  - _Boundary: A1 PriceTargetConsensus adapter_
  - _Depends: 1.4, 2.3_
  - _Requirements: 2.3, 2.4, 2.5, 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7, 5.1, 5.3, 5.4, 6.1, 7.1, 7.2, 7.3, 7.4, 7.5, 8.4_

- [ ] 3.4 (P) Restore revenue-product-segmentation financial behavior (2-3 hours)
  - Annual/quarter alias, fixed structure=flat; flatten outer-row/inner-label order then first 1000 rows.
  - Retain period association and duplicate labels across rows; clipping may split period; no reconciliation.
  - Done: RevenueBusinessLine matches frozen query/result schemas and endpoint-specific plus common offline checks pass.
  - Own only models/revenue_business_line.py, test_fmp_revenue_business_line.py and same-stem endpoint fixtures; frozen contracts read-only.
  - Changed production module/declaration files pass 400/300/50; tests/fixtures excluded; independent review then fresh checks.
  - _Boundary: A1 RevenueBusinessLine adapter_
  - _Depends: 1.4, 2.3_
  - _Requirements: 2.3, 2.4, 2.5, 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7, 5.1, 5.3, 5.4, 6.1, 7.1, 7.2, 7.3, 7.4, 7.5, 8.4_

- [ ] 3.5 (P) Restore revenue-geographic-segmentation financial behavior (2-3 hours)
  - Annual/quarter alias, fixed structure=flat; flatten outer-row/inner-label order then first 1000 rows.
  - Preserve region labels/taxonomy changes over two periods and unknown currency/completeness.
  - Done: RevenueGeographic matches frozen query/result schemas and endpoint-specific plus common offline checks pass.
  - Own only models/revenue_geographic.py, test_fmp_revenue_geographic.py and same-stem endpoint fixtures; frozen contracts read-only.
  - Changed production module/declaration files pass 400/300/50; tests/fixtures excluded; independent review then fresh checks.
  - _Boundary: A1 RevenueGeographic adapter_
  - _Depends: 1.4, 2.3_
  - _Requirements: 2.3, 2.4, 2.5, 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7, 5.1, 5.3, 5.4, 6.1, 7.1, 7.2, 7.3, 7.4, 7.5, 8.4_

- [ ] 3.6 (P) Restore historical-market-capitalization financial behavior (2-3 hours)
  - Resolve UTC omitted dates, start=end-365 days; ordered <=366 days; from/to and fixed 5000 limit once.
  - Effective dates are ISO strings; cap is provider calculation, no inferred share/price/currency basis.
  - Done: HistoricalMarketCap matches frozen query/result schemas and endpoint-specific plus common offline checks pass.
  - Own only models/historical_market_cap.py, test_fmp_historical_market_cap.py and same-stem endpoint fixtures; frozen contracts read-only.
  - Changed production module/declaration files pass 400/300/50; tests/fixtures excluded; independent review then fresh checks.
  - _Boundary: A2 HistoricalMarketCap adapter_
  - _Depends: 1.4, 2.3_
  - _Requirements: 2.3, 2.4, 2.5, 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7, 5.1, 5.3, 5.4, 6.1, 7.1, 7.2, 7.3, 7.4, 7.5, 8.4_

- [ ] 3.7 (P) Restore shares-float financial behavior (2-3 hours)
  - Exactly one matching-symbol row; duplicate/foreign symbols fail; nullable source dates match frozen schema.
  - Divide provider free-float percentage by 100; retain zero/null distinction and explicit transformation.
  - Done: ShareStatistics matches frozen query/result schemas and endpoint-specific plus common offline checks pass.
  - Own only models/share_statistics.py, test_fmp_share_statistics.py and same-stem endpoint fixtures; frozen contracts read-only.
  - Changed production module/declaration files pass 400/300/50; tests/fixtures excluded; independent review then fresh checks.
  - _Boundary: A2 ShareStatistics adapter_
  - _Depends: 1.4, 2.3_
  - _Requirements: 2.3, 2.4, 2.5, 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7, 5.1, 5.3, 5.4, 6.1, 7.1, 7.2, 7.3, 7.4, 7.5, 8.4_

- [ ] 3.8 (P) Restore quote financial behavior (2-3 hours)
  - Exactly one matching-symbol row; duplicates fail; epoch conversion uses supported UTC semantics.
  - Preserve OHLC/bid/ask/close meanings, zero/null, share volume and separate market-cap/share date uncertainty.
  - Done: EquityQuote matches frozen query/result schemas and endpoint-specific plus common offline checks pass.
  - Own only models/equity_quote.py, test_fmp_equity_quote.py and same-stem endpoint fixtures; frozen contracts read-only.
  - Changed production module/declaration files pass 400/300/50; tests/fixtures excluded; independent review then fresh checks.
  - _Boundary: A2 EquityQuote adapter_
  - _Depends: 1.4, 2.3_
  - _Requirements: 2.3, 2.4, 2.5, 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7, 5.1, 5.3, 5.4, 6.1, 7.1, 7.2, 7.3, 7.4, 7.5, 8.4_

- [ ] 3.9 (P) Restore income-statement-growth financial behavior (2-3 hours)
  - Annual/quarter alias and limit 20 (1..100); forward once, clip, reject other period choices.
  - Ratios scale 1, negative/zero/missing retained; flow growth does not establish discrete-quarter methodology.
  - Done: IncomeStatementGrowth matches frozen query/result schemas and endpoint-specific plus common offline checks pass.
  - Own only models/income_statement_growth.py, test_fmp_income_statement_growth.py and same-stem endpoint fixtures; frozen contracts read-only.
  - Changed production module/declaration files pass 400/300/50; tests/fixtures excluded; independent review then fresh checks.
  - _Boundary: A2 IncomeStatementGrowth adapter_
  - _Depends: 1.4, 2.3_
  - _Requirements: 2.3, 2.4, 2.5, 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7, 5.1, 5.3, 5.4, 6.1, 7.1, 7.2, 7.3, 7.4, 7.5, 8.4_

- [ ] 3.10 (P) Restore balance-sheet-statement-growth financial behavior (2-3 hours)
  - Annual/quarter alias and limit 20 (1..100); forward once, clip, reject other period choices.
  - Stock comparison ratios scale 1; retain fiscal end and unknown denominator/restatement/source periods.
  - Done: BalanceSheetGrowth matches frozen query/result schemas and endpoint-specific plus common offline checks pass.
  - Own only models/balance_sheet_growth.py, test_fmp_balance_sheet_growth.py and same-stem endpoint fixtures; frozen contracts read-only.
  - Changed production module/declaration files pass 400/300/50; tests/fixtures excluded; independent review then fresh checks.
  - _Boundary: A2 BalanceSheetGrowth adapter_
  - _Depends: 1.4, 2.3_
  - _Requirements: 2.3, 2.4, 2.5, 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7, 5.1, 5.3, 5.4, 6.1, 7.1, 7.2, 7.3, 7.4, 7.5, 8.4_

- [ ] 3.11 (P) Restore cash-flow-statement-growth financial behavior (2-3 hours)
  - Annual/quarter alias and limit 20 (1..100); forward once, clip, reject other period choices.
  - Flow growth ratios scale 1; no multiplication by 100 or assertion of discrete-quarter/YTD basis.
  - Done: CashFlowStatementGrowth matches frozen query/result schemas and endpoint-specific plus common offline checks pass.
  - Own only models/cash_flow_growth.py, test_fmp_cash_flow_growth.py and same-stem endpoint fixtures; frozen contracts read-only.
  - Changed production module/declaration files pass 400/300/50; tests/fixtures excluded; independent review then fresh checks.
  - _Boundary: A2 CashFlowStatementGrowth adapter_
  - _Depends: 1.4, 2.3_
  - _Requirements: 2.3, 2.4, 2.5, 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7, 5.1, 5.3, 5.4, 6.1, 7.1, 7.2, 7.3, 7.4, 7.5, 8.4_

## 4. Controller registration and consumer integration

- [ ] 4.1 Register reviewed adapters and advance reproducible source pins (1-2 hours)
  - Integrate all eleven accepted modules into provider.py and provenance; preserve baseline registrations/routes/notices.
  - Done: installed RegistryMap contains exact expected keys; source recovery hashes and actual commits/pins agree.
  - Offline registration smoke only; no unbudgeted provider request. Shared source pins/inventory remain exclusive.
  - Changed production passes 400/300/50; lock/provenance/generated artifacts record exclusions.
  - _Depends: 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8, 3.9, 3.10, 3.11_
  - _Boundary: Controller provider/source-pin integration_
  - _Requirements: 1.2, 5.4, 5.5, 8.1_

- [ ] 4.2 Prove actual SDK/HTTP/OBBject and installed discovery join (2-3 hours)
  - Retest public SDK/native Fetcher admission against actual eleven classes; compare effective queries/metadata with HTTP.
  - Assert all eleven expected keys in installed financial projection, OpenAPI x-qopenbb-financial, catalog and native widgets; 4.3 owns generated snapshots.
  - Done: missing/invalid annotation fails expected-set checks; aliases/defaults/bounds and baseline identities stay compatible.
  - Reuse financial annotation/metadata/policy/openapi/catalog, transport/service and catalog_financial contract tests.
  - Changed production passes 400/300/50; generated contracts excluded; controller reviews any projection repair.
  - _Boundary: Controller installed SDK/HTTP/discovery integration_
  - _Requirements: 1.1, 1.3, 5.2, 5.5, 6.1, 6.2, 6.3, 6.5, 8.4_

- [ ] 4.3 Integrate Workspace discovery and portable generated consumer contracts (1-3 hours)
  - Generate snapshots from exact 4.1 source pins and 4.2 installed projection; inspect provider parameters/results and actual diffs.
  - If generation requires an image, Dagger builds a generation-only image first; record its sources/digest, distinct from 5.1 final packaged candidate.
  - Done: consumers use installed routes/schemas without provider fetching logic; baseline search/listing identity regressions pass.
  - Preserve unsupported/unverified states; run shared-module complexity audit and actual scoped integration gate once.
  - Generator/handwritten production passes 400/300/50; generated output/test evidence excluded with generator identity.
  - _Boundary: Controller generated-contract/Workspace integration_
  - _Requirements: 1.4, 2.1, 3.1, 3.2, 3.3, 5.5, 6.2, 6.5, 8.5_

## 5. Bounded acceptance and existing delivery cadence

- [ ] 5.1 Package exact-source runtime candidate and freeze offline readiness/ledger (2-3 hours)
  - Dagger builds final candidate data API/Workspace images from committed 4.3 inputs; portable commands load/orchestrate them.
  - Done: source/package/digest identities, credential readiness and offline route/schema checks pass in isolated Compose runtime.
  - Initialize the ledger and freeze the exact matrix before startup; disable polling/unrelated widgets and automatic provider calls, counting any unexpected startup call.
  - Task approval approves 48-call cap; controller freezes exact symbols/dates/period/page/limits before calls, no routine extra approval.
  - New ledger: 22 direct/native +10 contrasts +8 browser +8 diagnosed reruns shared across live/browser=48; old 291 budget never transfers.
  - Build/runtime configuration passes applicable 400/300/50; generated images/evidence excluded; no owner-server deployment.
  - _Boundary: Controller source/image/runtime integration_
  - _Depends: 4.3_
  - _Requirements: 7.2, 8.1, 8.2, 8.4_

- [ ] 5.2 Execute bounded real-provider/native comparison matrix (2-3 hours)
  - Use 5.1 exact-source candidate; execute 22 direct/native comparisons plus 10 frozen contrasting calls, MSFT primary.
  - Done: identity/value/unit/period/provenance comparisons exist per endpoint or explicit entitlement-blocked acceptance.
  - Compare changing quotes to their own acquisitions; count failures/startup/background/refresh against 48; no automatic retries.
  - Eight diagnosed reruns are shared with 5.3; stop at cap and revise budget before excess calls. Test/evidence-only cap exclusion.
  - _Boundary: Controller packaged API/provider acceptance integration_
  - _Depends: 5.1_
  - _Requirements: 1.2, 2.6, 4.1, 4.2, 4.3, 4.7, 8.3, 8.4_

- [ ] 5.3 Verify representative isolated Workspace lifecycle (2-3 hours)
  - On 5.1 candidate, eight browser calls cover estimate/segment/growth/market display, recovery and save/reopen/export.
  - One headless worker reuses existing browser/CDP harness, disposable state, hidden helpers and bounded login scheduling.
  - Done: displayed/programmatic facts, persistence and console/network outcomes recorded with exact local source/image identity.
  - Consumer-blocked endpoints stay blocked; API pass is not widget pass; count startup/refresh/recovery within shared 48 cap.
  - Test/evidence-only production exclusion; never claim these local candidate checks exercised later CI image bytes.
  - _Boundary: Controller packaged Workspace/API consumer integration_
  - _Depends: 5.1, 5.2_
  - _Requirements: 1.2, 6.2, 7.1, 7.2, 8.3, 8.4_

- [ ] 5.4 Complete scoped release checks and reviewed sanitized mirror (1-3 hours)
  - Run relevant portable contract/regression/complexity release gates once; reuse valid evidence without unrelated suite repeats.
  - Done: independent acceptance review and sanitized mirror manifest verify actual hashes, commands/exits, revisions and limitations.
  - Update truthful breadth/inventory/coverage/source pins; explicit staging and per-task commits retain existing cadence.
  - One heavy job, pytest at most two workers; evidence/generated artifacts excluded, maintained logic passes 400/300/50.
  - _Boundary: Controller cross-repository acceptance/evidence integration_
  - _Depends: 5.2, 5.3_
  - _Requirements: 1.2, 1.3, 1.4, 8.1, 8.5_

- [ ] 5.5 Publish one milestone through existing CI and verify release identity (1-3 hours)
  - Run existing milestone publication cadence: Dagger image builds only; portable commands publish immutable images and actual release assets.
  - Done: actual release assets are downloaded and published images are pulled through the intended public access path; digests/source revisions/manifest agree with accepted source and reviewed mirror hashes.
  - Retain local candidate versus CI build identities explicitly; source agreement does not imply identical bytes or CI browser acceptance.
  - If published images differ from accepted local bytes, run existing offline packaged identity/readiness checks; any new live calls stay within ledger.
  - No deployment; release manifest retains rollback identity. Generated assets excluded; changed publication logic passes 400/300/50.
  - _Boundary: Controller CI/publication/source-image identity integration_
  - _Depends: 5.4_
  - _Requirements: 8.1, 8.2, 8.5_

## Coverage boundary

The numeric mappings identify bounded contribution, not closure of all 44 umbrella criteria.
Unchanged baseline: 2.1 existing first-slice coverage, 3.1-3.2 search/disambiguation, 3.3 listing identity,
5.2 native provider defaults, 7.5 cache semantics; retain regression evidence rather than claim new implementations.
Outside Batch A: 2.2 DCF, 3.4 other-asset identities, 3.5 macro identity, 4.8 macro semantics,
5.6 supplementary providers, 6.4 broader narrative remain unchanged/deferred under umbrella design.
2.3 broader families and 1.4 inventory remain open beyond these eleven; B/C batches are not accepted here.
All eleven installed/account/consumer states remain independent; skipped/fixture checks never certify live acceptance.
Task review must PASS independently before maintained tasks/spec metadata are written; owner task approval precedes implementation.

## Implementation notes

- 1.1 accepted 2026-11-17: [independent foundation review](../../../artifacts/reviewed/fmp-expansion-a/foundation-review.md). Fresh quality: 102 passed, two platform skips; combined complexity: 103 maintained root files, zero violations; missing fork scope exits 2. Empty current fork manifests do not remeasure unchanged fork files. Selected archive/member/license hashes verified. Narrow future ownership patterns retain fail-closed scope checks; native Windows Git root identity now compares resolved paths. Reuse the native snapshot verification dependencies, not the original checkout's unusable cross-platform link.


1.2 accepted 2026-11-17: [A1 contract review](../../../artifacts/reviewed/fmp-expansion-a/a1-contract-review.md), 94 focused native checks. Correct retained estimate aliases to canonical number_analyst_estimated_revenue and number_analysts_estimated_eps; retain source-original mappings separately. Reuse statement-period-provenance/provider-venv with explicit new-worktree source overrides; pipeline-venv lacks provider dependencies.

1.3 accepted 2026-11-17: [A2 contract review](../../../artifacts/reviewed/fmp-expansion-a/a2-contract-review.md), 112 focused native checks. Preserve corrected balance currency/cash-flow aliases, float and quote zero/UTC behavior, and required-nullable balance fields. Growth provider schemas use ratio without the retained frontend multiplier; actual native column projection verifies that distinction. Official float/cash examples are indexed documentation excerpts, not direct or live payload captures.

1.4 accepted 2026-11-17: [contract and architecture review](../../../artifacts/reviewed/fmp-expansion-a/contract-freeze-review.md), 33 focused native characterization checks, 102 quality checks/two platform skips and combined complexity within scope. The additive admission amendment repairs the Container-only prescription while preserving approved outcomes. Reviewed proposal bytes retain their authored status; spec.json records acceptance. Runtime SDK admission and exact final emitter exception remain task 2.1 obligations; no adapter dispatch before 2.3.

2.1 accepted 2026-11-17: [SDK review](../../../artifacts/reviewed/fmp-expansion-a/sdk-admission-review.md) and [committed-source gate](../../../artifacts/reviewed/fmp-expansion-a/sdk-admission-verification.json). API 0c544ace4d177cc6ff833619ad520bf806b90d91; 99 SDK/freeze tests, 102 quality tests/two platform skips, combined 109 files with five exact reviewed emitter exceptions and no remaining violations. Preserve pending/strict/baseline provider selection stages; unresolved omitted-provider pre-body errors retain native ordering. Native RegistryMap rejects plain characterization mixins: adapter queries must use compatible native-standard inheritance while preserving frozen schemas and validators. Rebind emitter exceptions to later actual API heads only after identical-byte/metric checks under the recorded approval; no source-change waiver.

2.1 reopened 2026-11-17 after [targeted public SDK alias verification](../../../artifacts/reviewed/fmp-expansion-a/sdk-period-followup.md): quarterly fails for all six periodic variants at native filtering before Container normalization. Prior passing checks remain historical evidence but omit this required alias. Task 2.2 edits are frozen pending a bounded SDK repair and re-acceptance.

2.1 re-accepted 2026-11-17: [independent alias correction review](../../../artifacts/reviewed/fmp-expansion-a/sdk-alias-review.md), 186 fresh SDK/freeze tests, all six periodic variants through actual Fetcher execution, and final 111-file combined gate with zero errors/violations. API corrective commit 403323aee033dfcd30b7b24dda5f0f5efc35a339. Five unchanged emitter exceptions rebound to that revision. Historical failed alias evidence remains preserved; generic historical audit refresh is disclosed in the review. HTTP task 2.2 resumes without acceptance.

2.2 accepted 2026-11-17: [HTTP admission review](../../../artifacts/reviewed/fmp-expansion-a/http-admission-review.md), 399 joined checks plus 12 independent probes and clean 111-file combined gate. Uses original installed query classes and concrete native controls, rejects invalid raw inputs before extraction, and forwards canonical effective values through copied scopes. Fixture command-router import timing is isolated before dedicated registry patching. Task 2.3 joins these prerequisites before adapter fan-out.
