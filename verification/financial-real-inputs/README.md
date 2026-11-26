# Real FMP inputs for the FCF yield journey

Read [journey-inputs.json](journey-inputs.json) to select a case. Paths in each entry are relative to the registry. Submit the `request` JSON to authenticated Workspace `POST /modeling/v1/evaluations`. Look up the expected result in the `expected` JSON using `expected_key`. Compare the status, reference and check outcomes, value and full trace, then reopen the saved run in a fresh session. Both requests use frozen inputs and require no provider credentials in the browser.

- `sap-de-live` is the default and verifies the yield from a same-session FMP snapshot whose availability is bounded by an actual response receipt.
- `aapl-historical-strict` verifies withholding when FMP historical market capitalization has no publication timestamp.

## SAP.DE same-session evidence

The [capture receipt](sap-de-fmp-capture.json) records three authenticated HTTP 200 responses. The FMP SAP.DE Xetra quote returned EUR 192.64 per share and EUR 222,345,903,252 in issuer market capitalization. The simultaneous profile matched the symbol, venue and capitalization, and confirmed EUR. The quote event was 2026-11-26 10:13:43 CET. Quote receipt was 10:28:47.186599 CET and the last input arrived at 10:28:49.223710 CET. These times fall inside the same Xetra session. The request uses the quote receipt as market-value availability and the last input receipt as the decision and evaluation cutoff. Quote event time establishes the measurement date. [FMP quote](https://site.financialmodelingprep.com/developer/docs/stable/quote), [FMP profile](https://site.financialmodelingprep.com/developer/docs/stable/profile-symbol), [Xetra 2026 calendar](https://www.xetra.com/resource/blob/4580826/3e974decb414d6769cc2bc8e601f6c9a/data/xetra-trading-calendar-2026.pdf)

The FMP annual cash-flow row agrees with SAP's audited FY2025 consolidated statement for January 1 through December 31. Continuing-operations operating cash flow was EUR 9,156,000,000 and purchases of intangible assets and PP&E were EUR −739,000,000. The request uses the EDGAR Form 20-F acceptance on 2026-02-26 at 07:01:22 Eastern for publication and the FMP cash-flow receipt as its observed vintage. The FMP filing-date fields coincide with the fiscal year end, so EDGAR supplies the publication evidence. Method FCF is EUR 8,417,000,000 before any adjustments from SAP's own FCF measure. The independent decimal oracle computes `100 × 8417000000 / 222345903252` = **3.7855431005897290522658664811512252004 percent** at wire precision. [SAP consolidated cash flows](https://www.sap.com/integrated-reports/2025/en/datahub/financial-data/cash-flows.html), [SAP Form 20-F](https://www.sec.gov/Archives/edgar/data/1000184/000110465926020058/sap-20251231x20f.htm), [EDGAR acceptance receipt](https://www.sec.gov/Archives/edgar/data/1000184/000110465926020058/0001104659-26-020058-index.html)

## Apple historical withholding

- The FY2026 annual cash-flow row from FMP matches Apple's filed consolidated 10-K. Operating cash flow was USD 145,097,000,000 and purchases of PP&E were a cash outflow of USD 9,041,000,000. FCF is USD 136,056,000,000. The 52-week period ran from 2025-09-28 through 2026-09-26. EDGAR confirms acceptance at 08:05:15 Eastern on 2026-11-03. [FMP cash flow documentation](https://site.financialmodelingprep.com/developer/docs/stable/cashflow-statement), [10-K cash flows and note 1](https://www.sec.gov/Archives/edgar/data/320193/000032019326000026/aapl-20260926.htm), [EDGAR acceptance receipt](https://www.sec.gov/Archives/edgar/data/320193/000032019326000026/0000320193-26-000026-index.html)
- FMP's live quote endpoint returned AAPL at USD 355.58, market capitalization 5,167,359,676,000 and epoch seconds 1795640402. The simultaneous profile matched the symbol, NASDAQ venue and capitalization, identified USD as the trading currency and matched CIK 0000320193 to the filing. The denominator uses the issuer capitalization supplied by FMP. The arithmetic oracle is `100 × 136056000000 / 5167359676000`, approximately **2.632989%**. [FMP quote documentation](https://site.financialmodelingprep.com/developer/docs/stable/quote), [FMP profile documentation](https://site.financialmodelingprep.com/developer/docs/stable/profile-symbol)
- The provider quote event was 2026-11-25 21:00:02 UTC (16:00:02 New York). Retrieval was 2026-11-26 09:25:26.137401 UTC (04:25:26 New York), on the next local date. The quote request uses the actual provider quote event as the observation and decision timestamp and maps it to the method's `published_at` eligibility field. The input provenance retains the later retrieval time, and the receipt records both the quote and profile receipt times. This establishes the numerical result for the timestamped snapshot served at retrieval. First delivery to subscribers and revisions between the event and retrieval remain unverified. Applying retrieval time as the availability bound makes the row ineligible for the November 25 decision. The method requires the market-value observation date and decision's local date to match, so a retrieval-day decision cannot use this previous-day quote.
- The FMP historical capitalization endpoint supplied 5,180,869,938,100 for 2026-11-25 with a date alone. Its adapter leaves currency, share-count basis, publication and vintage unresolved. The strict request preserves that uncertainty, passes no publication time and produces a withheld output with no calculation trace. Each endpoint's capitalization stays associated with its own provenance. [FMP historical capitalization documentation](https://site.financialmodelingprep.com/insights/platform/how-to-retrieve-historical-market-capitalization-using-a-free-api)

The [SAP receipt](sap-de-fmp-capture.json) and [Apple receipt](aapl-fmp-capture.json) hold selected non-secret provider fields, sanitized query parameters, HTTP status, UTC receipt time and SHA-256 of each complete response at capture. The retained excerpts support offline reproduction. The digests refer to the original response bodies, which are outside this bundle.

## Verification

The existing FMP fetchers back OpenBB's equity fundamentals `cash` and equity `historical_market_cap` routes. Both fetchers reproduced the captured values on 2026-11-26 and reported `point_in_time_safe=false`. The Modeling service's acquired-input allowlist covers FRED only, so the browser input uses its supplied-snapshot route. The quote and profile values were obtained directly from the authenticated FMP stable endpoints.

Run the offline numerical, trace, independent-reference and signed save/reopen checks from the repository root.

```sh
env -u FMP_API_KEY -u FRED_API_KEY PYTHONPATH=services/data-api \
  services/data-api/.venv/bin/python -m pytest -c pipeline/pyproject.toml \
  tests/factors/test_real_fmp_fcf_acceptance.py tests/factors/test_issuer_reference.py \
  tests/factors/test_fcf_yield.py -q
```

Run the live adapter comparison with the existing FMP credential in the environment or local `.env`. Quote and profile snapshots can change as trading resumes. The offline request remains frozen.

```sh
PYTHONPATH=vendor/data-api/openbb_platform/providers/fmp:vendor/data-api/openbb_platform/core \
  services/data-api/.venv/bin/python verification/financial-real-inputs/check_live_fmp.py
```

On 2026-11-26, 65 focused tests passed under Python 3.13.15 at QOpenBB `d77a695142474b9476c75b9971f3d034af044fbb` and vendored Data API `5583c958d35282cb59037aae8218cec31d540697`. The retained cases reopened through fresh signed requests after restarting the isolated Modeling listener over the same run directory. The [source-stage Workspace journey](../modeling-journey/README.md) exercised the registered SAP and strict Apple cases. The [acceptance receipt](../../artifacts/reviewed/factor-signals/workspace-modeling-journey.md) identifies the container images and the source overlay. Release image assembly belongs to task 12.2.
