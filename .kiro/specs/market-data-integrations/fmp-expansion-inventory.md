# FMP expansion: 24 candidate operations, 10 current registrations

Read-only inventory, 2026-11-17. Root `3b47ead262aac62a1c4a9f275694bd3e72f83056`; data API `a965f70c164fe477ce9c99654b9be48e2f1bc9fd`. No provider request, installation, build, test execution or source edit occurred. Candidate operations below require contract review and acceptance; static source inspection is not live verification.

## Verified baseline

- `data-api/openbb_platform/providers/fmp/openbb_fmp/provider.py:21-31` registers exactly 10 models: EquityInfo, IncomeStatement, BalanceSheet, CashFlowStatement, EquitySearch, EquityPeers, EquityHistorical, KeyMetrics, FinancialRatios, EnterpriseValues.
- Provider code has 10 fetcher modules plus companion data modules; broad historical models are absent from the working provider tree.
- `D:/Source/QOpenBB/artifacts/task-1.1/openbb_fmp-1.6.1.tar.gz` contains 67 non-init model modules. SHA256 verified `5f6f27af6283075912df42f373c45ed37bc6970097342ed73110fb6101be5517`, matching provider `provenance.json:3-5`. Historical registry has reuse aliases; module count is not operation count.
- Published coverage inventory records 276 examples/29 categories/271 distinct example URLs (`docs/provider-coverage.md:5`). This is documentation, not installed coverage.
- First-batch route fixtures are in `tests/providers/test_{profile,income,discovery,errors,fmp_discovery,fmp_daily_history,fmp_key_metrics,fmp_financial_ratios,enterprise_values,balance_sheet_metadata,cash_flow_metadata}.py`, plus shared metadata/error/runtime contracts.
- `tests/providers/test_live_financial.py:33-53` enumerates baseline native API journeys. Historical accepted research-input assessment records 46 native FMP and 3 direct DCF attempts, five journeys and 73 offline checks; it is not a fresh execution here.
- `research-input-assessment.md:25-31` identifies unresolved fiscal duration/YTD/restatement, capex sign, market/share/claim/date and currency semantics. Later periodic-query acceptance repairs `ttm=exclude` metadata; the earlier assessment's TTM omission is superseded (`docs/provider-coverage.md:9-11`). IA-B input readiness remains false.

## Proposed first expansion tranche

All paths in the table are below `openbb_platform/providers/fmp/openbb_fmp/models/`; retained files are archive members, not current adapters. Routes have `/api/v1` prefix. Existing route association means a standard model/router exists, not that FMP implements it. Endpoint names below use `/stable/` prefix.

| Operation | Retained model/file | Existing route or new contract | State and main contract gap |
| --- | --- | --- | --- |
| discounted-cash-flow | None | New provider DCF contract | Direct feasibility only; provider valuation/date/inputs, never house DCF |
| custom-discounted-cash-flow | None | New custom DCF contract | Only verified supported parameters; echoed input does not prove recalculation |
| analyst-estimates | AnalystEstimates / analyst_estimates.py | equity/estimates/historical | Restore; forecast fiscal period, analyst counts, estimate dates |
| price-target-news | PriceTarget / price_target.py | equity/estimates/price_target | Retained URL confirmed; not price-target-summary; content/as-of/attribution |
| price-target-consensus | PriceTargetConsensus / price_target_consensus.py | equity/estimates/consensus | Restore; target horizon, currency and contributor basis |
| revenue-product-segmentation | RevenueBusinessLine / revenue_business_line.py | equity/fundamental/revenue_per_segment | Restore; dynamic keys, restatement, currency/scale, totals overlap |
| revenue-geographic-segmentation | RevenueGeographic / revenue_geographic.py | equity/fundamental/revenue_per_geography | Restore; geographic definition, source ordering and totals |
| historical-market-capitalization | HistoricalMarketCap / historical_market_cap.py | equity/historical_market_cap | Restore; date windows/completeness; dated cap is provider calculation |
| shares-float | ShareStatistics / share_statistics.py | equity/ownership/share_statistics | Restore; float/outstanding distinction and actual observation dates |
| quote | EquityQuote / equity_quote.py | equity/price/quote | Restore; timestamp/timezone/currency and market/share date mismatch |
| income-statement-growth | IncomeStatementGrowth / income_statement_growth.py | equity/fundamental/income_growth | Restore; provider ratios/fractions, denominator and fiscal basis |
| balance-sheet-statement-growth | BalanceSheetGrowth / balance_sheet_growth.py | equity/fundamental/balance_growth | Restore; instant comparisons and missing/zero distinction |
| cash-flow-statement-growth | CashFlowStatementGrowth / cash_flow_growth.py | equity/fundamental/cash_growth | Restore; cumulative versus discrete source convention |
| income-statement-as-reported | None | Explicit new typed contract or reviewed ReportedFinancials adaptation | Native statement keys, units, filing/amendment basis |
| balance-sheet-statement-as-reported | None | Explicit new typed contract or reviewed ReportedFinancials adaptation | Native taxonomy/units; no fabricated reconciliation |
| cash-flow-statement-as-reported | None | Explicit new typed contract or reviewed ReportedFinancials adaptation | Native duration/YTD and units; availability may remain unknown |
| dividends | HistoricalDividends / historical_dividends.py | equity/fundamental/dividends | Restore; ex/record/payment dates and adjusted/unadjusted amounts |
| splits | HistoricalSplits / historical_splits.py | equity/fundamental/historical_splits | Restore; ratio orientation and corporate-action date |
| earnings-calendar | CalendarEarnings / calendar_earnings.py | equity/calendar/earnings | Restore; timezone, estimated/actual and finite date-window fan-out |
| dividends-calendar | CalendarDividend / calendar_dividend.py | equity/calendar/dividend | Restore; calendar bounds and multiple date meanings |
| splits-calendar | CalendarSplits / calendar_splits.py | equity/calendar/splits | Restore; bounded calendar and split ratio |
| news/stock candidate | CompanyNews / company_news.py | news/company | Restore; retained news/ base needs explicit stock subtype contract; partial article content |
| earning-call-transcript | EarningsCallTranscript / earnings_call_transcript.py | equity/fundamental/transcript | Restore; year/quarter/content completeness/event attribution |
| sec-filings-search/symbol | CompanyFilings / company_filings.py | equity/fundamental/filings | Restore; typed form/date/page bounds; content versus filing links |

Count: 24 distinct candidate operations = 19 retained-source operations + 5 explicit new-contract operations. Do not count annual/quarterly choices, multiple symbols, forward EPS/EBITDA projections of analyst-estimates, or filings CIK selector as additional operations. The news subtype requires exact endpoint freeze before this count becomes an implementation acceptance target.

## Candidate lanes and shared prerequisites

The lane groupings below identify reusable ownership boundaries. The controller's A/B/C grouping at the end of this report supersedes their original numbered delivery order.

1. Freeze shared metadata/errors/bounds/registration/catalog contracts and source recovery manifest; preserve all 10 baseline adapters. Controller owns registry, common helpers, provenance, generated contracts, breadth and complexity inventories.
2. Financial research lane: estimates, targets and segment adapters (5); market/claim lane: quote, dated capitalization and float (3). Distinct model/test ownership; source joining and registration remain serialized.
3. Financial depth lane: three growth adapters plus three as-reported contracts (6). DCF lane: standard/custom provider comparison (2). Both consume frozen date/unit/origin contracts; independent financial review required.
4. Corporate-action/calendar lane (5); narrative lane news/transcript/filings (3). News extension installation/lock impact is a prerequisite, not assumed by an existing source router.
5. Later queue follows design line197: ETF info/holdings/countries/sectors/search/exposure, institutional/insider/government/NPORT ownership, index/FX/crypto, futures/commodities/COT. Restore from retained members when present; documented-only endpoints need new contracts. Levered/custom-levered DCF, ratings/grades and transcript discovery remain named later candidates, not counted above.

Each executable task needs pre-I/O validation; finite pagination/window fan-out; null/zero/sign/date/unit/currency/origin and safe-failure fixtures; native Python/API/catalog consistency; narrowly budgeted real-provider comparison; independent review; fresh verification; exact source/evidence linkage. Missing entitlement is blocked, not passed. Production whole-file caps remain 400 physical/300 logical/50 function units; use existing checker/inventory and split cohesive data declarations before touching oversized legacy routers. Existing fundamental_router.py exceeds400 lines: reuse existing routes without modifying it, or mount new bounded child routers through the small composition root as enterprise values already does.

## Evidence references

- `data-api/.../provider.py:21-31`; `provenance.json:3-5,18-27`; retained archive member `openbb_fmp-1.6.1/openbb_fmp/models/<file>` URLs inspected for all19 retained candidates.
- `data-api/openbb_platform/extensions/equity/openbb_equity/{fundamental/fundamental_router,estimates/estimates_router,calendar/calendar_router,price/price_router,ownership/ownership_router,equity_router}.py`; `extensions/news/openbb_news/news_router.py` supply the route/model associations.
- Root `.kiro/specs/market-data-integrations/{requirements.md:22-35,52-58,76-100,design.md:61-81,195-197,233}` requires progressive bounded delivery and separate documented/retained/installed/account/consumer states.
- Root `.kiro/specs/analyst-workspace/research-input-assessment.md:11,25-31`; `docs/provider-coverage.md:5,9-11,33-43`; `docs/reference/fmp-endpoints.csv` supplies documented endpoint examples only.

mmhmem resumed exact project QOpenBB. Its provider-coverage JSON summary timed out once; bounded native references were used instead, without retry. No credentials were inspected.

Controller batch grouping: A11 retained = estimates3 + segments2 + market/share/quote3 + growth3; B8 retained = corporate actions2 + calendars3 + narrative3; C5 new = DCF2 + as-reported3. These are expansion/input/bootstrap planning groups, not executable implementation tasks or completed design approval for all24.
