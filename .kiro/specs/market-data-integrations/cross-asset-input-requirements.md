# Cross-asset and macro input verification requirements

Status: requirements owner-approved, 2026-11-18, including the candidate list with a gold proxy and no fixed request cap. Design, tasks and any live request are not yet approved.

## Introduction

The first research story, "Commodities vs tech: which regime are we in?", needs prices for two asset groups and a few macro series. None of these inputs has accepted live evidence: prices are verified only for single companies, and FRED only for the 10-year Treasury yield. This slice establishes, with real provider responses, which inputs the story may rely on and what each one means. It adds no calculation and no dashboard.

The [roadmap](../../steering/roadmap.md) places this slice first. Its results feed the `factor-signals` and `research-stories` specs.

## Boundary context

- **In scope**: verifying named ETF and FRED inputs through the existing daily-price and FRED series routes; recording identity, meaning, history depth and display status for each; updating coverage, breadth and documentation for what is verified.
- **Adjacent**: `factor-signals` owns returns, factors, regimes and diagnostics. `research-stories` owns the story App. Batch C, sector constituents and commodity futures remain separate deliveries.
- **Out of scope**: new provider adapters, unless a named input cannot be served by an existing route and the owner approves one; dividend-adjusted prices; commodity futures and roll conventions; index constituents; Yahoo Finance; any house calculation.
- **Constraint**: the tool ships no provider data. Each installation fetches with its own keys, and showing fetched data to others is governed by that installation's provider terms.

## Candidate inputs

These are the inputs to verify. A candidate that fails stays recorded as unverified or blocked; it is not replaced silently.

| Role in the story | Candidate | Source and route |
| --- | --- | --- |
| Technology equities | XLK | FMP daily prices |
| Broad commodities | DBC | FMP daily prices |
| Gold | GLD | FMP daily prices |
| Commodity-linked equities | XLE (energy), XLB (materials) | FMP daily prices |
| Market reference | SPY | FMP daily prices |
| Real yield | DFII10 | FRED series |
| Curve slope | T10Y2Y | FRED series |
| Inflation expectation | T10YIE | FRED series |
| Dollar | DTWEXBGS | FRED series |
| Oil spot, gas spot | DCOILWTICO, DHHNGSP | FRED series |
| Financial stress | STLFSI4, NFCI | FRED series |

The ICE BofA and Moody's credit-spread series on FRED are excluded: they are copyrighted, restricted to internal use, and the ICE series now carries three years of history.

## Requirements

### Requirement 1: Establish what each input is

**Objective:** As a quant, I want to know exactly which instrument or series a number refers to, so that I do not compare unlike things.

1.1 When an ETF candidate is verified, the delivery record shall state its provider symbol, instrument type, listing exchange and price currency where the provider supplies them, and shall mark any attribute the provider does not supply as unknown.
1.2 When a FRED candidate is verified, the delivery record shall state its series identifier, title, units, frequency, seasonal-adjustment status and source institution as returned by the provider.
1.3 The delivery record shall label an ETF as a fund holding a basket or futures positions, and shall not describe it as a spot commodity price or as an index level.
1.4 The delivery record shall label the oil and gas series as spot benchmarks only if the provider's series description says so; otherwise their instrument type shall remain unknown.

### Requirement 2: Establish what each price means

**Objective:** As a portfolio manager, I want to know whether a price history can be read as a return, so that performance comparisons are honest.

2.1 The delivery record shall state the adjustment basis of each ETF price history as served, and shall state that the history excludes dividends where that is the case.
2.2 If a candidate's returned history contains a gap, a duplicate date or an out-of-order row, the delivery record shall report the count and the affected date range.
2.3 The verification shall compare each returned value with the provider's own raw response for the same request and shall report any difference.
2.4 The data service shall preserve missing FRED observations as missing and shall not convert them to zero or interpolate them.

### Requirement 3: Establish how much history is available

**Objective:** As a quant, I want to know the usable history of each input on this installation, so that I do not design a test the data cannot support.

3.1 The verification shall record, for each candidate, the earliest and latest observation dates actually returned on the verifying installation.
3.2 The delivery record shall state that the earliest date reflects that installation's provider plan and may differ on another installation.
3.3 If a request for an early period returns an empty or truncated result, the delivery record shall record that outcome as observed and shall not infer the reason.
3.4 The delivery record shall state the request limits that apply to each route: one symbol per request and a five-year window for daily prices, and the row limit for FRED series.

### Requirement 4: Record provenance and display status together

**Objective:** As an operator, I want each input's licence status beside its provenance, so that a story never shows a series it should not.

4.1 The coverage record shall carry, for each verified input, its provider, route, retrieval time, effective query and the source institution named by the provider.
4.2 The coverage record shall carry a display status for each input: public-domain or government source, provider-licensed, third-party copyrighted, or unknown.
4.3 If a FRED series carries a third-party copyright notice, the coverage record shall mark it as restricted and the delivery shall exclude it from shipped stories.
4.4 The documentation shall state the notice that views using FRED data must display.

### Requirement 5: Keep verification bounded and honest

**Objective:** As the owner, I want every live request counted and every failure kept, so that the evidence can be trusted.

5.1 The verification shall record every outbound provider request, including failed requests and reruns, with its purpose.
5.2 If the provider denies a request for entitlement, the delivery record shall mark that input as blocked by entitlement and shall not retry it automatically.
5.3 The verification shall use no synthetic substitute to accept an input.
5.4 The delivery shall keep raw provider responses private and shall publish only counts, dates, hashes and field-level outcomes.
5.5 The breadth and coverage records shall mark as verified only the inputs with accepted evidence, and shall leave the others open.

## Proposed verification scope

Approved with these requirements.

- **Prices**: for each of the six ETFs, one recent window and one early-window probe for history depth. Twelve requests.
- **FRED**: one request per series for the eight series. Eight requests.
- **Reruns**: diagnosed reruns only, each recorded with its reason. No fixed cap, as the owner decided.

Expected total: about 20 requests before any rerun.

## Open questions for design

- Whether the instrument type and exchange of an ETF can be read from an existing accepted route (the profile or quote), or need a recorded manual source.
- Whether a display-status field belongs in the coverage index schema or in a separate reviewed record.
