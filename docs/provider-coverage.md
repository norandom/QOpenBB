# Provider coverage for the research workspace

FMP is QOpenBB's primary research source across financial statements, reports, funds, ownership, analyst data, news and markets. Yahoo/yfinance supplements specific price gaps; FRED supplies named economic and benchmark series. Bloomberg guides the research workflows, while the existing Workspace application, widgets and chart work remain the implementation foundation.

Research snapshot: 2026-10-19. The [FMP endpoint inventory](reference/fmp-endpoints.csv) records 276 published examples across 29 documentation categories, with 271 distinct example URLs. Shared endpoints are retained under their respective categories. It captures the public stable catalog, not every parameter combination, account entitlement or successful response. Each row links its detailed source documentation. No API keys or live provider requests were used for this inventory.

## Published coverage versus our implementation

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

The installed QOpenBB FMP adapter currently registers only company profile and income statements. FRED series also has a catalog widget. The demonstrated price/statement/news dashboard uses uploaded snapshots. Broader published FMP coverage must not be presented as installed or accepted. Every integration needs separate published-coverage, entitlement, adapter, widget and end-to-end status.

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
- [ ] Register these restored adapters and verify installed API/widget behavior and live account entitlement. The installed baseline described above remains the registered surface until that join.

These checks track source acceptance, not completion of the broader research families.
