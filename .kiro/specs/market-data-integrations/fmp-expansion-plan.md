# FMP expansion and modeling-input plan

Prepared 2026-11-17. Deliver a substantial FMP expansion in three bounded milestones: **24 additional endpoint operations**, comprising 19 retained-adapter candidates and five new-contract candidates. Start with the 11 financial/valuation operations below. These are planning targets, not implemented or entitled datasets. The existing ten registered FMP models remain the accepted baseline.

See the [source inventory](fmp-expansion-inventory.md) and [independent planning review](fmp-expansion-review.md). Batch A's detailed design is recorded separately; this plan does not approve implementation.

## Decision and boundary

The owner requested broader endpoint completion while proceeding with the financial-modeling input/bootstrap plan. This elaborates delivery under the approved market-data requirements; it does not create another data framework. Use the owned OpenBB Fetcher, standard models, Query, routers, OBBject, financial metadata, safe transport and generated discovery/catalog path.

Provider work owns acquisition, source facts, typed parameters/results, provenance and visible failures. The separate financial-modeling repository owns calendarization, cash-conversion definitions, adjusted earnings, valuation bridges and numerical validation. Workspace owns presentation and research context. Company Research is complete and is reused.

No dependency upgrade, new service, server deployment, AI/Excel work or automatic cross-provider fallback is included. No endpoint gains acceptance from a documentation page, archived adapter or catalog entry alone. The five new-contract candidates remain separate from restoration work until their schemas and routes are independently reviewed.

## Endpoint sequence

Paths in the endpoint column are relative to FMP `/stable/`. Model names identify retained OpenBB contracts, not installed FMP capabilities. The final task amendment must freeze public parameters, defaults, bounds, result fields and exact writable files before implementation fan-out.

| Batch | Endpoint operation | Retained model or contract work | Purpose and acceptance concern |
| --- | --- | --- | --- |
| A | `analyst-estimates` | AnalystEstimates | Forecast period, estimate counts, range/consensus and absent vintage; EPS and EBITDA projections do not count as extra endpoints |
| A | `price-target-news` | PriceTarget | Individual analyst target events; attribution, target currency and event date; not target-summary semantics |
| A | `price-target-consensus` | PriceTargetConsensus | Consensus range and unknown aggregation/as-of conventions remain visible |
| A | `revenue-product-segmentation` | RevenueBusinessLine | Preserve segment labels, fiscal period, reporting currency and changing segment taxonomy |
| A | `revenue-geographic-segmentation` | RevenueGeographic | Preserve geography labels and period; do not assume disjoint or exhaustive segments |
| A | `historical-market-capitalization` | HistoricalMarketCap | Dated market-cap observations; do not infer a share basis from market cap alone |
| A | `shares-float` | ShareStatistics | Float and outstanding shares retain their distinct definitions and dates |
| A | `quote` | EquityQuote | Dated market observation and currency; zero and missing values stay distinct |
| A | `income-statement-growth` | IncomeStatementGrowth | Provider-calculated growth, its source periods and units; not house growth calculations |
| A | `balance-sheet-statement-growth` | BalanceSheetGrowth | Stock-balance growth retains source dates and unknown methodology |
| A | `cash-flow-statement-growth` | CashFlowStatementGrowth | Flow growth retains period/duration uncertainty |
| B | `dividends` | HistoricalDividends | Ex/record/payment/declaration dates and cash amount/currency are distinct |
| B | `splits` | HistoricalSplits | Split ratio direction, event date and adjustment basis |
| B | `earnings-calendar` | CalendarEarnings | Scheduled versus reported events; estimate and actual remain separate |
| B | `dividends-calendar` | CalendarDividend | Bounded date window and event-date types |
| B | `splits-calendar` | CalendarSplits | Bounded event calendar, not price-adjustment calculations |
| B | `news/stock` candidate | CompanyNews | Freeze the retained adapter's explicit stock subtype; source, URL, publication timestamp, company linkage and partial-text status |
| B | `earning-call-transcript` | EarningsCallTranscript | Requested year/quarter, event time, attribution and full/partial content status |
| B | `sec-filings-search/symbol` | CompanyFilings | Filing metadata and document links; not a claim that document content is available inline |
| C | `discounted-cash-flow` | New DCF standard/query/data contract and route | Optional provider valuation reference; separate from house value |
| C | `custom-discounted-cash-flow` | New custom-DCF contract and route | Explicit supported inputs, units and assumptions; parameter echo does not prove recalculation |
| C | `income-statement-as-reported` | New/adapted reported-statement contract | Preserve source tags, units, fiscal/filing facts; no forced normalized financial equivalence |
| C | `balance-sheet-statement-as-reported` | New/adapted reported-statement contract | Preserve instant facts and taxonomy; inspect ReportedFinancials compatibility first |
| C | `cash-flow-statement-as-reported` | New/adapted reported-statement contract | Preserve duration/YTD/source facts; no fabricated discrete quarters |

Batch A has 11 operations; B has eight; C has five. These counts exclude the accepted ten-model baseline, duplicates, aliases and alternate projections. Batch order prioritizes reusable modeling inputs and retained code; C requires more contract work and is not silently absorbed into A. Funds/ETF, institutional/insider ownership, cross-market, other assets, macro/COT and remaining FMP families stay open in the existing coverage inventory. They follow this tranche with their own endpoint briefs.

Batch B must explicitly install and lock the retained news extension before exposing `news/company`. An existing source router is not proof of an installed route. Its exact stock-news subtype must be frozen before the candidate count becomes an implementation acceptance target.

## Source basis and recovery

Use accepted QOpenBB source `3b47ead262aac62a1c4a9f275694bd3e72f83056`, API `a965f70c164fe477ce9c99654b9be48e2f1bc9fd` and Workspace `bf180ef506286886da224df9ff184cd1ace2397e`. The clean implementation checkout is `D:/BuildArtifacts/QOpenBB/company-research/root`; API and Workspace are siblings. The original checkout intentionally retains older source and unrelated dirty work. Do not implement against that old source by accident.

The retained FMP 1.6.1 archive contains 67 model modules and has SHA-256 `5f6f27af6283075912df42f373c45ed37bc6970097342ed73110fb6101be5517`. Its retained adapters are migration inputs, not automatically compatible code. Recover individual modules with provenance/notices and adapt to current core and safe transport; never register the whole archive. No retained DCF adapter establishes the new contracts in C.

The historical endpoint catalog contains 276 documentation examples and 271 distinct example URLs. That is not a count of implemented endpoints or entitlements. Current official pages were checked on 2026-11-17 for estimates, product/geographic segmentation, target consensus, DCF, transcript, growth and historical market cap. Detailed task preparation must recheck the remaining selected endpoints and actual parameter schemas. No new live requests were made for this plan.

Additional official checks confirmed quote, shares-float and balance-sheet growth documentation. The guessed `developer/docs/stable/price-target-news` page returned 404, while FMP's [own endpoint article](https://site.financialmodelingprep.com/education/other/price-target-news-api-endpoint-make-smarter-buy-or-sell-decisions) still documents the retained URL. This is documentation uncertainty, not proof of an API outage or entitlement. FMP's [consensus FAQ](https://site.financialmodelingprep.com/faqs?code=marketPerformance) describes a six-month/latest-per-analyst-company methodology; preserve this as dated provider documentation, not independently verified response lineage. Its [analyst-data FAQ](https://site.financialmodelingprep.com/developer/docs/stable/tipranks-search) also describes internal projections/manual adjustments, so the estimates contract must not call every field a direct analyst consensus observation.

## Shared contract and file ownership

Dependency direction remains core types -> FMP adapters -> installed commands/service -> generated catalog -> Workspace. The provider never imports catalog or UI code. Keep `AnnotatedResult` financial metadata under the existing OBBject envelope; preserve baseline route/widget identities and explicit provider selection.

| Owner | Files/responsibility | Join condition |
| --- | --- | --- |
| Controller/contract lane | API `core/openbb_core/provider/standard_models/` selected contracts; common financial metadata/transport only if an evidenced gap requires change | Freeze query/result schemas, bounds and financial annotations before workers start |
| Financial expectations worker | API `providers/fmp/openbb_fmp/models/` selected estimates, price-target and segmentation modules plus their dedicated tests | No registry, router composition, shared helper or root-catalog writes |
| Market/fundamentals worker | API same directory, disjoint selected market-cap, float, quote and growth modules plus their dedicated tests | Same common contract; no overlapping files |
| Controller integration | API `provider.py`, `provenance.json`, required router composition; root `services/data-api/qopenbb_data/`, `contracts/`, `sources.lock.json`, coverage and complexity inventories | Register only reviewed adapters; compare generated catalog/API and test mounted service |
| Independent reviewer | Read source, focused checks and financial evidence; no implementation ownership | Accept or return concrete defects before task completion |

The endpoint inventory companion supplies retained module/route mappings. Before each implementation task, its brief names individual files and tests; directory-level ownership above is a planning boundary, not permission for overlapping edits. Oversized existing routers require bounded child composition rather than adding to a file above the cap.

Use Sol implementers, Astra for financial/architecture review, at most two implementers and one reviewer with the controller. Freeze shared interfaces before fan-out; serialize joins, installs and heavy checks. Every changed production file must meet 400 physical lines, 300 logical units and 50 logical units/function. Extend the existing executable complexity inventory/checker, not policy text alone.

## Acceptance contract for each batch

1. Freeze each endpoint's explicit provider selection, supported symbols/dates/fiscal periods, native versus local row bounds, pagination and maximum outbound request count. Reject unsupported combinations before I/O. No hidden multi-symbol request fan-out or unbounded auto-pagination.
2. Preserve provider/retrieval/query/source-row identity, financial units/currency, relevant observation/forecast/filing dates and raw versus provider-calculated origin. Missing, null, zero, empty response and failed request remain distinguishable. Unknown duration, restatement, vintage or calculation basis stays unknown.
3. Exercise meaningful offline cases: alias compatibility, zero/null, conflicting periods, truncation, empty responses, malformed rows, entitlement/authentication/rate-limit/timeout failures and secret-safe errors. Verify affected core/provider tests and mounted pre-I/O guards. Synthetic checks do not establish entitlement.
4. Compare bounded real responses with the installed native API for every claimed endpoint, recording exact parameters, retrieval time, source/image identity, count and financial values without credentials. A denied endpoint stays blocked and its family obligation stays open. Do not repeatedly probe a denied endpoint or call it completed because its adapter works offline.
5. Verify generated discovery and native widgets against the installed schemas. Use one isolated headless browser worker for representative batch workflows, including parameters, units/dates, failures, save/reopen and export where promised. Label per-endpoint API and widget acceptance separately; a representative browser run does not certify all widgets.
6. Independent review checks source and financial semantics; update actual test paths and evidence in breadth/coverage and reconcile maintained checkboxes. Publish only the accepted milestone, once, following existing Dagger and release-identity checks. Keep any blocked endpoints explicitly outside the accepted set.

Live verification needs a new bounded request ledger and selected query matrix in the task amendment. The completed Company Research ledger (291 of 320 FMP calls) is historical and must not be reused as the budget for this expansion. Determine a new cap from the actual request fan-out, symbols/windows and representative browser journeys before calling the provider. Routine verification uses the existing owned runtime authorization and hidden helpers.

## First model: readiness and bootstrap

Select a narrow historical quarterly-performance/cash-conversion method and an explicit peer-comparison input contract. The existing MSFT/ORCL/ADBE evidence supplies examples, not synchronized periods or three complete historical years. The later query/provenance repairs and completed Company Research UI must be reused rather than commissioned again.

| Input | Already available to reuse | Still required before numerical acceptance |
| --- | --- | --- |
| Identity | Search/Profile, source-qualified company and listing context | Eligible company scope, listing/issuer distinction and reporting/trading currencies |
| Income/balance/cash | Accepted native annual/quarterly datasets and source-row provenance | Actual duration, discrete/YTD classification, fiscal alignment, restatements and sufficient history/opening balances |
| Cash conversion/working capital | OCF, capex, FCF, AR/inventory/AP and working-capital changes | Method-approved numerator/denominator, capex signs/scope, averaging/day counts and treatment of missing/accounting adjustments |
| Peer valuation | Provider metrics/ratios/EV, dated historical prices | Denominator window/eligibility, valuation date, shares/currency and complete applicable signed claims bridge |
| SBC lens | SBC, EBITDA/OCF/FCF, basic/diluted shares and repurchases | Explicit existing SBC treatment to avoid double subtraction; aggregate buybacks do not prove dilution sterilization |
| Forward context | Batch A estimates and segments | Forecast date/vintage limitations; no automatic substitution for historical denominators |

The modeling foundation's approved 18-task plan begins with repository bootstrap, executable quality/import-boundary checks and frozen contracts. Only then do registry/execution, verification rules and immutable runs fan out. Orchestration, authenticated HTTP, widget projection, contract export/compatibility/breadth, Workspace identity and consumer bindings follow. The real-model journey requires a separately approved implemented method plus verified selected inputs; synthetic foundation fixtures cannot close it. Image/Compose and publication follow that journey.

Repository name/remote and image coordinates remain unassigned. Proposed repository name for owner review: `qopenbb-financial-modeling`; `qfm` remains only the package placeholder in the existing design. No remote or repository is created by this plan. Bootstrap must transfer the authoritative specs with a source revision, resolve protected Python/uv/Polars/Pydantic/service dependency pins and wheel/Decimal compatibility, and retain the house-standard source/correction ledger. Do not treat candidate versions as a verified lock.

Run the provider expansion first, then bootstrap when the selected first-method input gate is satisfied. All 24 endpoints, DCF and FRED/WACC are not mandatory prerequisites for a historical cash-conversion method. Preserve the broader endpoint queue rather than converting it into an indefinite modeling blocker.

## Requirement and status mapping

This plan elaborates existing 1.1-1.4, 2.1-2.6, 4.1-4.7, 5.1-5.3, 6.1-6.5, 7.1-7.5 and 8.1-8.5. Company/listing handling retains 3.1-3.3. Unchanged 3.4-3.5, 4.8 and 5.4-5.6 remain owned by the umbrella design and their existing/deferred provider work. No umbrella requirement is closed by this document.

Next executable planning unit: generate Batch A's concrete endpoint/file design amendment and task graph, independently review it, and record owner phase approval before implementation. The original task approval only authorizes initial tasks 1.1-6.3; see `tasks.md` follow-on scope. This document is the reviewable expansion/input/bootstrap plan, not an approved executable task list. Batch B/C remain queued for their own bounded contracts, including content/UI ownership and new standard-model compatibility.

## Research references

- Existing requirements/design/tasks and `docs/provider-coverage.md` own scope and historical evidence.
- Official [estimates](https://site.financialmodelingprep.com/developer/docs/stable/financial-estimates), [product segments](https://site.financialmodelingprep.com/developer/docs/stable/revenue-product-segmentation), [geographic segments](https://site.financialmodelingprep.com/developer/docs/stable/revenue-geographic-segments) and [target consensus](https://site.financialmodelingprep.com/developer/docs/stable/price-target-consensus) document the selected provider operations.
- Official [income growth](https://site.financialmodelingprep.com/developer/docs/stable/income-statement-growth), [cash-flow growth](https://site.financialmodelingprep.com/developer/docs/stable/cashflow-statement-growth) and [historical market cap](https://site.financialmodelingprep.com/developer/docs/stable/historical-market-cap) support the corresponding candidates.
- Official [DCF](https://site.financialmodelingprep.com/developer/docs/stable/dcf-advanced) and [transcripts](https://site.financialmodelingprep.com/developer/docs/stable/search-transcripts) establish documented operations, not account access or validated model behavior.
- Applied discovery and design-extension guidance: existing spec boundary, retained-source reuse, explicit interfaces/ownership and independent review. No new library is selected. Reuse the existing result/error/transport contracts; a parallel provider framework would duplicate accepted behavior.
