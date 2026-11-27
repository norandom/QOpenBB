# Provider coverage for the research workspace

FMP is QOpenBB's primary research source across financial statements, reports, funds, ownership, analyst data, news and markets. Yahoo/yfinance supplements specific price gaps; FRED supplies named economic and benchmark series. Bloomberg guides the research workflows, while the existing Workspace application, widgets and chart work remain the implementation foundation.

Research snapshot: 2026-10-19. The [FMP endpoint inventory](reference/fmp-endpoints.csv) records 276 published examples across 29 documentation categories, with 271 distinct example URLs. Shared endpoints are retained under their respective categories. It captures the public stable catalog, not every parameter combination, account entitlement or successful response. Each row links its detailed source documentation. No API keys or live provider requests were used for this inventory.

## Periodic query metadata compatibility

The repair at data API `2e60c0a7aff039eda5f14a9d494beaec822fb9c4` adds `ttm: exclude` to the existing Metrics and Ratios effective-query metadata, including defaulted requests. Source tests, 73 native/offline checks and four real FMP queries passed, with independent integration review. Published [alpha-42231784072-1](../artifacts/reviewed/periodic-query-provenance/accepted.md) also passes public asset/image verification, canonical catalog generation, three offline packaged runtime tests and four installed Python/native cases. Independent delivery review passed on 2026-11-10 in the [bounded task plan](../.kiro/specs/market-data-integrations/periodic-query-provenance-tasks.md). These checks add no Workspace browser or owner-server acceptance; the prior owner-server confirmation belongs to alpha-42188370167-1.

Update the maintained core and FMP provider together. Older Python `FinancialResultMetadata` validators reject this added public key; they require the matching reviewed core revision. Consumers that read the effective-query dictionary generically retain the same envelope and schema version. The selector does not enable TTM requests or calculations, change financial values, or establish fiscal comparability. Unresolved duration/YTD, restatement, currency/share/claim conventions and IA-B readiness remain open.

## Published coverage versus our implementation

The [2026-11-17 expansion plan](../.kiro/specs/market-data-integrations/fmp-expansion-plan.md) targets 24 additional operations in batches of 11 financial/valuation, eight events/content and five DCF/as-reported operations. The [source inventory](../.kiro/specs/market-data-integrations/fmp-expansion-inventory.md) identifies 19 retained-adapter candidates and five new-contract candidates. Independent planning review passed. Batch A has eleven registered source adapters with accepted SDK/HTTP/discovery joins and scoped live API comparison evidence. Batch B adds eight event and document adapters with scoped live API evidence and five representative browser journeys. The five Batch C operations remain candidates. The original ten FMP models retain their earlier acceptance scope.

| Research family | Published FMP coverage to map into widgets |
| --- | --- |
| Discovery/reference | Name, symbol, CIK, ISIN and CUSIP search; screeners; directories and listing variants |
| Company intelligence | Profiles, peers, float, capitalization, employees, management, compensation and M&A |
| Markets | Quotes, batches, session data, EOD/intraday histories and explicit adjustment variants |
| Financial analysis | Income, balance sheet, cash flow, TTM, growth, ratios, metrics and segment data |
| Reports/documents | As-reported statements, annual-report JSON/XLSX and SEC filing discovery |
| Funds | ETF information, holdings, country/sector exposures and fund disclosures |
| Expectations | Estimates, broker grades, target summaries/consensus and partner analyst datasets |
| News/events | Articles, news, press releases, earnings transcripts and corporate calendars |
| Ownership | Institutional/13F, insider, beneficial ownership and congressional disclosures |
| Cross-market research | Sector/industry performance, technical indicators and index constituents/history |
| Other assets | FX, crypto and the provider's mixed commodity/futures category |
| Macro/positioning | Economic data/calendar, Treasury rates, risk premiums and COT reports/analysis |
| Additional families | ESG, fundraising disclosures, market hours and bulk delivery |

See the inventory's per-endpoint source links and [official FMP catalog](https://site.financialmodelingprep.com/developer/docs). This is a family-level map; bulk delivery is a transport option, not a separate financial asset class.

The published initial batch registers ten FMP models and the generic FRED series contract, with eleven reusable native widget definitions, discovery and safeguards. Its scoped real-provider observations, packaged Income journey and image publication are accepted; [company selection](company-selection.md) adds bounded linked Profile/Income acceptance. This does not establish every widget's complete research workflow or access for every installation. The earlier price/statement/news demo used uploaded snapshots. Every integration retains separate published-coverage, entitlement, adapter, widget and end-to-end status.

## Batch A live input checkpoint, 2026-11-17

The [accepted native join](../artifacts/reviewed/fmp-expansion-a/actual-join-review.md) covers analyst estimates, price-target events and consensus, business-line and geographic revenue, historical market capitalization, share statistics, a single-listing quote and three statement-growth datasets. The [coverage index](reference/provider-coverage.json) records each adapter separately under its research family. Its documented, retained-source and adapted proofs establish source scope; installed state is derived from the actual service projection.

The maintained consumer inventory adds eleven MSFT examples to the existing eleven datasets. Periodic examples request annual periods, row-limited queries use limit 3, estimates use page 0, and historical capitalization requests 2025-01-02 through 2025-01-31. These examples select reusable native routes and retain provider financial metadata; they add no calculations or provider fetching logic. Portable catalog generation has produced 22 native endpoint widgets plus the retained Peer Research renderer from the exact installed source. The generation-only image is `sha256:58686a7e8be19990181ad534b411f95f970d013d6d01811e46da0c06cf5e7769`, using data API `04acdb09ed76f432f4091a61630213e19f2d655c` and Workspace `bf180ef506286886da224df9ff184cd1ace2397e`. Repeated generation is deterministic; the original twelve widget definitions and the FRED and Company Research app definitions remain unchanged. The starter adds the eleven examples. The curated Company Research five primary datasets remain unchanged. Task 4.3 was independently accepted in the [consumer catalog review](../artifacts/reviewed/fmp-expansion-a/consumer-catalog-review.md). The generation-only image above is historical; corrected candidate generation retains the canonical widget bodies while updating source provenance. Catalog acceptance does not establish widget behavior.

The [accepted live matrix](../artifacts/reviewed/fmp-expansion-a/live-matrix-verification.json) establishes scoped account access and nonempty source-fact comparisons for all eleven Batch A operations. The combined evidence contains 29 valid cases from the original local image and three corrected cash-flow cases from the successor image; the original cases were not rerun on the successor. The three original cash-flow 404 attempts remain diagnosed failures and consumed budget. The matrix gate recorded 35 of the approved 48 FMP requests, zero FRED requests, 1,019 rows and 5,052 independent source-fact checks. The subsequent accepted eight-call browser journey ended at cumulative 43/48 FMP requests; it does not rerun the matrix or renew historical image identities. Access applies to the recorded symbols, periods, dates and limits on that account, not every installation or parameter combination.

The [accepted native browser journey](../artifacts/reviewed/fmp-expansion-a/native-browser-verification.json) verifies four representative widgets on the recorded local candidate: analyst estimates, geographic revenue, income statement growth and equity quote. It covers displayed response facts, CSV export, pre-I/O failure/recovery, native save and fresh-context reopening. The other seven widgets and all future AI consumers remain unknown. API acceptance is not widget acceptance, and neither establishes later CI image bytes or publication. Family completion remains open, including broader financial analysis and expectations.

Coverage proofs bind the actual adapter source and current installed financial contract. A later widget proof also binds the tested local API image digest. The coverage JSON is itself a packaged runtime input, so updating this index changes subsequent image bytes. Discovery intentionally marks widget evidence stale on another image digest; retain that signal instead of copying local acceptance onto new CI images.

## Batch B events and documents checkpoint, 2026-11-18

Batch B registers eight FMP operations as bounded source adapters:
- **Events:** dividend history, split history, and the earnings, dividend and split calendars.
- **Documents:** company news, earnings-call transcripts and SEC filing metadata.

The [accepted live matrix](../artifacts/reviewed/fmp-expansion-b/live-matrix-verification.json) compares 20 planned calls with each call's own acquired response, using 13,527 independent field checks. The comparisons cover these financial semantics:
- Cash amounts per share and adjusted amounts stay distinct.
- Yields are converted from percentage points to ratios.
- Split ratios keep their orientation.
- Actuals and estimates stay separate, and a missing value is never turned into zero.
- Transcript text and fiscal period are preserved exactly.
- Filing dates become civil dates without inventing a timezone.

The two original filings failures (padded-midnight `filingDate`) remain recorded. The repaired adapter's two rechecks pass. Market-wide calendar queries return the first 250 rows in source order. On the earnings calendar, supplying a listing selects matching rows before applying the cap. The Events and Documents App supplies its selected listing. Access applies to the recorded symbols, windows and limits on that account.

The [accepted native browser journey](../artifacts/reviewed/fmp-expansion-b/native-browser-verification.json) covers five representative widgets: dividend history, earnings calendar, news, transcript and filings. The data API image is `sha256:409e11697cad2378e2bb6c2cdca61d2f8cebd310a70a6a0a2c183820854c74c2`. Each widget passes initial load, save, safe app-template export and an isolated fresh-context reopen. The checks cover:
- displayed values, links and content status (partial excerpt, metadata-only, completeness unknown)
- keyboard access and saved query controls
- typed timeout and entitlement failures with recovery

The browser itself fulfils those failure cases, so they make no provider request.

Saved dashboards and exports hold query choices only, never response text. Split history and the dividend and split calendars have API acceptance only, and their widgets remain unknown. Future AI use is unknown for all eight. Live usage is 42 FMP requests with no other-provider requests and no guard denials.

A production repair of the document query controls (Workspace `ba03ec7`) was required and is part of this image. The coverage index binds each live claim to the shipped adapter source and financial contract. Each widget claim also binds to the browser image above, so a CI-built image reports it as stale until that image is verified. Batch B is published in [alpha-44340458084-1](https://github.com/norandom/QOpenBB/releases/tag/alpha-44340458084-1). Its data image `sha256:3db18506631972b3a3a176f45069cdac6574af7c35543e261ce7153b58ed25e4` passed 20 synthetic Batch B cases under network isolation with zero provider requests, but no browser journey has run on it, so its widget claims project as stale.

## Cross-asset and macro inputs checkpoint, 2026-11-18

The first research story asks which regime favours commodities or technology. This checkpoint verifies the inputs that story needs before any factor is modelled. The [result record](reference/cross-asset-inputs.json) describes each input. The [verification summary](../artifacts/reviewed/cross-asset-inputs/live-verification.json) and the [financial review](../artifacts/reviewed/cross-asset-inputs/5-6-review.md) hold the evidence.

One guarded live run from the published data image sent exactly 34 provider requests (18 FMP, 16 FRED); the image is `sha256:3db18506631972b3a3a176f45069cdac6574af7c35543e261ce7153b58ed25e4`. An independent comparison matched 40,020 price fields and 54,146 series rows to each call's own provider response, with no mismatch.

| Input | Description | Source | Dates returned |
| --- | --- | --- | --- |
| XLK | State Street Technology Select Sector SPDR ETF | FMP | 2007-01-03 to 2026-11-13 |
| DBC | Invesco DB Commodity Index Tracking Fund | FMP | 2007-01-03 to 2026-11-13 |
| GLD | SPDR Gold Shares | FMP | 2007-01-03 to 2026-11-13 |
| XLE | State Street Energy Select Sector SPDR ETF | FMP | 2007-01-03 to 2026-11-13 |
| XLB | State Street Materials Select Sector SPDR ETF | FMP | 2007-01-03 to 2026-11-13 |
| SPY | State Street SPDR S&P 500 ETF | FMP | 2007-01-03 to 2026-11-13 |
| DFII10 | Market Yield on U.S. Treasury Securities at 10-Year Constant Maturity, Quoted on an Investment Basis, Inflation-Indexed | Board of Governors of the Federal Reserve System (US) | 2003-01-02 to 2026-11-16 |
| T10Y2Y | 10-Year Treasury Constant Maturity Minus 2-Year Treasury Constant Maturity | Federal Reserve Bank of St. Louis | 1976-06-01 to 2026-11-17 |
| T10YIE | 10-Year Breakeven Inflation Rate | Federal Reserve Bank of St. Louis | 2003-01-02 to 2026-11-17 |
| DTWEXBGS | Nominal Broad U.S. Dollar Index | Board of Governors of the Federal Reserve System (US) | 2006-01-02 to 2026-11-13 |
| DCOILWTICO | Crude Oil Prices: West Texas Intermediate (WTI) - Cushing, Oklahoma | U.S. Energy Information Administration | 1986-01-02 to 2026-11-11 |
| DHHNGSP | Henry Hub Natural Gas Spot Price | U.S. Energy Information Administration | 1997-01-07 to 2026-11-11 |
| STLFSI4 | St. Louis Fed Financial Stress Index | Federal Reserve Bank of St. Louis | 1993-12-31 to 2026-11-13 |
| NFCI | Chicago Fed National Financial Conditions Index | Federal Reserve Bank of Chicago | 1971-01-08 to 2026-11-13 |

How to read the fund prices:
- **They are funds, not spot prices or indexes.** The provider describes GLD as holding bullion and DBC as holding futures. All six list on NYSE Arca; "AMEX" in the record is only the provider's exchange code.
- **Prices are split-adjusted and exclude dividends.** Returns built on them are price returns, not total returns.
- **Two windows were requested:** 2007-01-03 to 2011-12-30 and 2026-08-03 to 2026-11-13. The earliest date is the window start, not the start of the fund's history. History depth depends on the installation's provider plan.
- **Weekday gaps are exchange holidays:** 43 in the early window and one in the recent window.

How to read the FRED series:
- **Missing observations stay missing.** None becomes zero. Henry Hub (DHHNGSP) has about 1,400 missing days across the 2000s and WTI (DCOILWTICO) has 122 in 2003, so factor work must handle them.
- **STLFSI4 and NFCI are weekly,** ending Friday. The other six series are daily.
- **Only Henry Hub is typed as a spot benchmark,** because only its provider title says so. The WTI title does not.
- **Each series has its full served history,** with units, frequency and seasonal adjustment as the provider states them.

Source attribution: every story chart names its source in the headline, using the institution in the record. All eight FRED series are usable in stories (owner decision of 2026-11-18). Views that use FRED data must display: "This product uses the FRED® API but is not endorsed or certified by the Federal Reserve Bank of St. Louis." The tool ships no provider data; each installation fetches with its own keys.

This checkpoint covers data API results only. It adds no widget, factor or story, and no image was built or published. Live usage for this checkpoint is 18 FMP and 16 FRED requests with no guard denial.

## Company Research input verification, 2026-11-06

One bounded run verified 46 native FMP requests for Microsoft, Oracle and Adobe and three direct MSFT DCF probes. These checks extend the earlier sample to six annual/quarterly financial datasets, same-listing discovery/profile and EV-dated price windows. DCF access and a beta echo do not establish a native DCF widget, house valuation or sensitivity support. FRED DGS10 evidence remains historical-only from 2026-10-30.

The [input assessment](../.kiro/specs/analyst-workspace/research-input-assessment.md) records reusable widget IDs, financial compatibility gaps and follow-on ownership. Independent financial review accepted the gap assessment; IA-B input and workflow readiness remain false. No new provider adapter or image is delivered by this verification work.

## Discovery checkpoint, 2026-10-29

The [machine-readable coverage index](reference/provider-coverage.json) records family scope and source evidence separately from installed command discovery. The [accepted discovery component](../artifacts/reviewed/market-financial-discovery/accepted.md) reads authoritative financial schemas and preserves unknown access and consumer states. The [installed service integration](../artifacts/reviewed/market-runtime-integration/accepted.md) activates discovery, provider selection and safe errors. The [accepted native consumer catalog](../artifacts/reviewed/market-financial-consumers/accepted.md) preserves baseline widget IDs and editable company/series/period parameters. The initial batch was subsequently published in [alpha-41030227140-1](../artifacts/reviewed/financial-input-milestone/accepted.md) and is retained in the current periodic-query alpha; wider families remain unverified.

## Commodity prices and futures are different instruments

| Instrument/series | Treatment |
| --- | --- |
| Physical spot benchmark | Retain location, grade, unit, currency and observation convention. FRED's EIA WTI Cushing and Henry Hub series are explicit examples |
| Dated futures contract | Retain exchange, contract month/expiry, underlying and price/settlement convention |
| Provider-selected futures reference | Preserve the provider identity; do not claim a fixed expiry or known roll rule |
| Continuous futures series | Use this label only with evidence of construction and adjustment methodology |
| Equity-index future | Keep separate from physical commodities, the cash index and index-tracking ETFs |
| COT positioning | Keep market/report family, trader categories, reporting/release dates and futures-only/combined scope separate from price history |

FMP's [commodity directory](https://site.financialmodelingprep.com/developer/docs/stable/commodities-list) includes financial futures, so its category and a USD suffix do not prove spot-price semantics. Its [COT report](https://site.financialmodelingprep.com/developer/docs/stable/cot-report) is positioning data, not a commodity price. The exact FMP financial-futures symbol mappings and coverage of CFTC report variants remain to verify.

Yahoo labels GC=F and CL=F as futures in its [commodity table](https://ca.finance.yahoo.com/commodities/). Its [crude-oil contract chain](https://uk.finance.yahoo.com/quote/CL%3DF/futures/) demonstrates dated symbols on the website, not guaranteed yfinance history for every contract. Neither generic alias establishes a verified roll/back-adjustment rule. Yahoo is therefore a potential price supplement, not an automatic spot-price substitute.

FRED explicitly identifies [WTI Cushing spot](https://fred.stlouisfed.org/series/DCOILWTICO) and [Henry Hub spot](https://fred.stlouisfed.org/series/DHHNGSP), including units and source. For positioning, preserve the distinctions in the [CFTC report definitions](https://www.cftc.gov/MarketReports/CommitmentsofTraders/index.htm). The owner's "ftc" reference is provisionally interpreted as CFTC.

## From coverage to a working dashboard

The [widget requirements](../.kiro/specs/openbb-self-service/parameterized-widget-requirements.md) own named selection, inline news, command-line navigation and shared time context. The catalog must support research tasks across these families rather than stop at a price-chart starter set. Detailed implementation order and visual acceptance remain to be designed; this map does not approve or claim completed integrations.

## Adapter checkpoint, 2026-10-28

- [x] Balance-sheet and cash-flow source adapters: [accepted statement contracts](../artifacts/reviewed/market-data-statements/accepted.md).
- [x] Name/symbol discovery, provider peer candidates and bounded daily-price source adapters: [accepted discovery and price contracts](../artifacts/reviewed/market-data-discovery-prices/accepted.md).
- [x] Periodic key-metrics and ratio source adapters: [accepted financial metadata](../artifacts/reviewed/market-data-metrics-ratios/accepted.md).
- [x] Enterprise-value source contract and isolated command: [accepted input semantics](../artifacts/reviewed/market-data-enterprise-schema/accepted.md).
- [x] Register the restored first-batch adapters in an exact-source installed candidate: [acceptance](../artifacts/reviewed/market-provider-registration/accepted.md).
- [x] Install service safeguards and discovery in the exact-source candidate: [acceptance](../artifacts/reviewed/market-runtime-integration/accepted.md).
- [x] Regenerate eleven reusable native widgets and promote source/catalog pins: [acceptance](../artifacts/reviewed/market-financial-consumers/accepted.md).
- [x] Validate the initial eleven datasets with real provider observations: [scope and evidence](../artifacts/reviewed/market-live-financial-inputs/accepted.md). Access succeeded for the recorded verification queries; each installation still needs its own entitlement check.
- [x] Verify the packaged Income journey across AAPL/MSFT and annual/quarterly periods, including visible financial values, errors and save/reopen. [Acceptance](../artifacts/reviewed/market-packaged-financial/accepted.md). Eleven native definitions are discovered; the other ten do not gain full UI acceptance from this test.
- [x] Publish the first financial-input image pair and verify its eleven native definitions. [alpha-41030227140-1](../artifacts/reviewed/financial-input-milestone/accepted.md) includes the accepted initial adapters and contracts; wider provider families and installer-specific access remain open.

These checks track source acceptance, not completion of the broader research families.
