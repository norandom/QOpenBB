# Research story input qualification

The installation returned all 64 scheduled closes for DBC, XLK, GLD and VGT from August 17 through November 13, 2026. VGT is the alternate technology ETF. The FMP history retrieved on November 26 qualifies this window for the planned `proxy_comparison@2` evaluation on the retrieved-history basis. FRED's November 13 vintage omits the ending DFII10 observation, so the context for that window must report the unavailable endpoint. The packaged preflight verified all three spreads against their saved FMP rows and confirmed the dated withheld DFII10 outcome. [Packaged evidence](../../../artifacts/reviewed/research-stories/packaged-preflight.json) [Requirements 1.2, 2.2, 2.4, 2.5 and 3.3](requirements.md) · [Selection and acquisition contract](design.md#selection-and-acquisition-contract)

## Listing calendar and window

All four proxies use the NYSE Arca cash-equity calendar in `America/New_York`. The December 23, 2025 ICE announcement explicitly covers NYSE Arca and publishes its 2026 holidays and early closes. The official 2026 NYSE trading calendar PDF is marked current as of December 10, 2025. Its downloaded bytes have SHA-256 `70f5577eb43e60a9dbbecaae3cec23d0f02028c05c7f175013bb3e97816d394f`. This is the PDF digest. [ICE dated announcement](https://ir.theice.com/press/news-details/2025/NYSE-Group-Announces-2026-2027-and-2028-Holiday-and-Early-Closings-Calendar/) · [NYSE 2026 calendar PDF](https://www.nyse.com/publicdocs/nyse/ICE_NYSE_2026_Yearly_Trading_Calendar.pdf)

The selected date is November 13, the end of the earlier entitled comparison window. Counting weekdays back from that date and excluding the exchange's September 7 Labor Day closure yields 64 sessions starting August 17. The published schedule lists no early closes in that interval. Thanksgiving Day, November 26, is closed. November 27 and December 24 are 13:00 Eastern core closes and fall outside the qualification window. The end of November 13 in New York is the decision cutoff used for the vintage check. [Existing entitled-window record](../../../docs/reference/cross-asset-inputs.json) · [Exchange hours](https://www.nyse.com/trade/hours-calendars)

## Entitled observations

On 2026-11-26, a disposable Data API container bound to loopback used the installation's configured FMP and FRED entitlements. The published image was `ghcr.io/norandom/qopenbb-data-api@sha256:79d46d09a913a1b6583ae823961ca87b9e4a6bb112739ca738567b131ca79a73`. The qualification used repository revision `97289b1f2615f697bb310c725acac83e05553f1a` and bounded Python standard-library HTTP calls. All calls listed below returned HTTP 200. Receipt times are UTC and digests cover the Data API response bytes. The probe retained no private response bodies.

The price probe used `GET /api/v1/equity/price/historical` with `provider=fmp`, `interval=1d`, `adjustment=splits_only`, one symbol per request, and inclusive bounds `start_date=2026-08-17` and `end_date=2026-11-13`. Each returned date set matched the independent schedule exactly, with no duplicate dates. A second isolated probe confirmed 64 finite positive close values per symbol. The route supplies USD split-adjusted closes excluding dividends. Comparison returns calculated on these closes measure price performance. [FMP EOD documentation](https://site.financialmodelingprep.com/developer/docs/stable/historical-price-eod-full)

| Symbol | Exposure | Rows | Receipt time | Response SHA-256 |
| --- | --- | ---: | --- | --- |
| DBC | Broad commodity futures through the Invesco DB Commodity Index Tracking Fund | 64 | 12:32:25.899725 | `ba7c2c99620a574094783c3e73466c34e5d20551831e127ef724633be5961955` |
| XLK | S&P 500 information technology sector equities through the State Street Technology Select Sector SPDR ETF | 64 | 12:32:26.029949 | `ae42181c4847e5b6e82975c168795632abcd24cf5e66322d4ca720bb3051aacd` |
| GLD | Gold bullion exposure through SPDR Gold Shares | 64 | 12:32:26.390007 | `43ed011dda125a1e839250a26c82a7164d69aa677505da5b207c14a82737957f` |
| VGT | US information technology sector equities across market caps through Vanguard Information Technology ETF | 64 | 12:32:26.518654 | `97c544b0fcf08e1de0de9457884b4ecf1d63144675feb9a6c06e766b318a2755` |

FMP `GET /api/v1/equity/profile?symbol=VGT&provider=fmp` confirmed VGT is a USD ETF, received at 12:32:26.898913, digest `72d72d6d5e1f191b4edecbf3e89aa728903092f6fcf0c8e0de7bf20ff34fc386`. Vanguard establishes the NYSE Arca listing and MSCI US Investable Market Information Technology 25/50 benchmark. FMP's generic profile classification describes the fund entity. [Vanguard fund and listing](https://advisors.vanguard.com/investments/products/vgt/vanguard-information-technology-etf)

With the same date bounds, `GET /api/v1/economy/fred_series?symbol=DFII10&provider=fred&use_cache=false` returned 65 dated rows including the September 7 exchange holiday and numeric observations at both exact endpoints. Receipt was 12:32:27.514430, digest `8143ac6ba8115927a8ac8d6b451d4920cef557d7e3b847ae12944938216dce0d`. DFII10 is the Board of Governors' 10-year constant-maturity inflation-indexed Treasury yield, in percent, via FRED. The endpoint difference uses percentage points. [DFII10 series](https://fred.stlouisfed.org/series/DFII10)

A signed source-candidate evaluation through the published data API saved 64 session markers and 65 DFII10 observations. The regime and change were withheld. Their blocking checks name August 17 and November 13 because the returned observations lack verified historical availability at those endpoints.

> This product uses the FRED® API but is not endorsed or certified by the Federal Reserve Bank of St. Louis.

## Retrospective price comparison

A direct check of FMP's full end-of-day endpoint on November 26 returned 64 closes for each of the four funds for the same window. Using the last close divided by the first close minus one, DBC returned +0.7526% and XLK returned -10.5296%. DBC led by approximately 11.28 percentage points on the retrieved history. FMP documents these closes as split-adjusted with dividends excluded. This direct probe calculated historical price performance from the data served on November 26. The packaged preflight reproduced the comparison from the closes and dated simple returns in each saved run. [FMP price and volume endpoint](https://site.financialmodelingprep.com/developer/docs/stable/historical-price-eod-full) · [FMP price adjustment conventions](https://site.financialmodelingprep.com/faqs?code=chart)

A source-candidate check submitted each pair through the authenticated modeling evaluation route, then reopened its saved run. The published Data API acquired the prices. All six outputs per run passed independent verification. Each leg contained 64 closes. The dates below are the latest FMP receipts in UTC. Packaged Workspace acceptance is pending.

| Commodity proxy | Technology proxy | Return spread (percentage points) | FMP history retrieved (UTC) |
|---|---|---:|---|
| DBC | XLK | +11.28225 | 2026-11-26 13:45:12 |
| GLD | XLK | -1.81099 | 2026-11-26 13:45:16 |
| DBC | VGT | +10.02306 | 2026-11-26 13:45:19 |

## Price retrieval provenance and DFII10 cutoff evidence

- **FMP** returned trading dates and close levels. The admitted historical route supplies retrieval provenance and explicitly reports `point_in_time_safe=false`. It exposes no row-level publication timestamp or cutoff-covering vintage. The market closing time describes the observation. The November 18 published receipt and November 26 probe both postdate the November 13 cutoff. Using one of those times as evidence of publication by November 13 would backdate availability. The story uses the retrieved version for historical price performance. Point-in-time price comparisons under version 1 still require evidence of the price versions available by the cutoff. The direct full EOD response included date, symbol, OHLC, volume, VWAP and price changes. It contained no row-level revision or publication time. This finding applies to the endpoint exercised.
- **FRED** provides date-granular real-time periods through its documented observations API. In the same disposable container, a direct authenticated probe of `/fred/series/observations` asked for the November 13 vintage by setting `realtime_start=realtime_end=2026-11-13` and bounding observations to the selected interval. It contained the August 17 observation and omitted the November 13 endpoint. Receipt was 12:32:52.412942 with digest `bd2fa4c52c61030637f20d66269a332d377498383b64df963cf115bb48af761b`. Separate initial-release queries with `output_type=4`, one observation date per call and a real-time period from that date to November 26, returned August 18 as the first vintage for August 17 and November 16 as the first vintage for November 13. Those receipts were 12:32:52.779053 and 12:32:55.946138, with digests `d5133a8e5d5aeda07ac71b10525fd337a226545ee43d83b204d351925399a29b` and `f1097e6c32fec51b8afdec36060fb7e2d97467b7df35028b6cfbbad572a5ecbe`. These dates do not establish intraday publication times. The generic admitted series route returned present-day history and reports `point_in_time_safe=false`. The direct probe establishes the historical FRED gap, and the regime must withhold for the missing ending observation unless an admitted, timestamped source establishes publication and a covering vintage by the cutoff. [FRED observations API](https://fred.stlouisfed.org/docs/api/fred/series_observations.html) · [Board of Governors H.15 release description](https://www.federalreserve.gov/releases/h15/about.htm)

## Packaged preflight

On November 26, 2026, an isolated Workspace signed in and submitted three comparisons and one DFII10 evaluation through its session bridge. Each saved run reopened with the same inputs and outputs. The Dagger-built Data API served the story from its catalog. The modeling image used the same NYSE Arca schedule revision for all four requests.

Each ETF leg supplied 64 closes and 63 dated simple returns. The independent reference matched all six outputs for each pair. The price-return spreads were +11.28225 percentage points for DBC/XLK, -1.81099 for GLD/XLK and +10.02306 for DBC/VGT. The macro run retained 65 FRED observations. Both endpoint checks withheld the regime and its change because historical availability was unknown. The November 13 endpoint was identified, and the verified default spread supported DBC outperformance.

The [packaged evidence](../../../artifacts/reviewed/research-stories/packaged-preflight.json) records each leg's receipt time, row and return-trace hashes, the four run IDs, output checks and local image identities. The [verification instructions](../../../verification/modeling-journey/README.md) cover the authenticated preflight. Native Workspace rendering and browser acceptance are pending.
