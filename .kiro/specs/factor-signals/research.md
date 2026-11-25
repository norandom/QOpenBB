# Factor input and integration findings

The [input checkpoint](../../../docs/reference/cross-asset-inputs.json) identifies six ETF price histories and eight macro series. Its two fund windows leave a multi-year gap. A row-count or earliest-date check cannot establish 64 consecutive sessions. Calendar identity and session adjacency must come from a dated schedule independent of the returned prices.

The [Ubuntu checkpoint](../../handover.md) establishes live statement display and dashboard persistence. It does not establish a historical equity market value matched to each observation date, the availability time of every filing version, or point-in-time FRED vintages. Fixture calculations can be verified while a live output remains withheld for missing provenance.

The [foundation design](../financial-modeling/design.md) already specifies a model registry, typed input snapshots, versioned assumptions, per-output checks, traces, independent verification and authenticated immutable runs. Implement those contracts within the existing data API package. Its current provider routes and gallery catalog do not themselves implement authenticated immutable evaluations.

Discovery followed the Kiro design workflow for an extension. The evidence above comes from repository contracts and acceptance records. This design introduces no new external package or provider integration.

## Existing analytics code and delivery path

The data API fork at `5583c958d35282cb59037aae8218cec31d540697` contains OpenBB technical and quantitative extensions. The technical realized-volatility route defaults to Yang-Zhang over 30 bars. Before adopting any estimator, demonstrate parity with 63 simple close-to-close returns, divisor 62, and the approved calendar and availability rules. The FMP key-metrics adapter already maps `freeCashFlowYield`; use it as a provider observation with its own definition. The house calculation requires dated cash-flow components and market value. Existing provider tests include daily history, historical market cap, filing metadata and FRED acquisition.

The data image installs the extensions listed in [the runtime manifest](../../../services/data-api/pyproject.toml); technical and quantitative are absent. The [app factory](../../../services/data-api/qopenbb_data/app.py) mounts the OpenBB application at the root and exposes its OpenAPI document. Register house routes before the catch-all mount and explicitly include their contracts in the exposed schema. The gallery serves packaged widgets and apps; defer story catalog changes to story integration.

The [runtime input allowlist](../../../pipeline/qopenbb_ci/runtime_inputs.py) stages individual source files into the existing Dagger data image. Include each new production module and verify its hash through [the staging tests](../../../tests/delivery/test_data_image.py). Start from the approved 64-close momentum fixture, verify unavailable inputs and compare with an independent reference before enabling a live story.

## Source fields for the first six descriptor examples

These mappings were checked against the data API revision above. Eligibility is evaluated per observation at its decision timestamp. The public checkpoint establishes which routes returned data; its summary cannot supply a missing filing version, trading schedule or availability timestamp.

| Model input | Provider field and financial meaning | Condition for a historical result |
| --- | --- | --- |
| ETF momentum and volatility | FMP `equity_historical.py` exposes `date` and nullable `close`, a split-adjusted price per share. The requested symbol identifies the proxy. | Require a dated exchange calendar, the eligible version of each of 64 closes and their availability times. Check actual calendar gaps. |
| DFII10 endpoint levels | FRED `series.py` returns dated series values and preserves real-time intervals when supplied. Its metadata identifies vintage-query capability and publication dates as unknown. | Require independently evidenced availability for the two level observations. A retrieval timestamp or real-time interval alone cannot establish the historical signal. |
| Issuer cash-flow numerator | FMP `cash_flow_data.py` maps `operatingCashFlow`, `capitalExpenditure`, `acceptedDate`, `fillingDate` and `reportedCurrency`. | Identify each standalone fiscal interval, the available filing version, time zone and capex sign convention. Reject overlapping year-to-date flows. |
| Issuer market-value denominator | FMP `historical_market_cap.py` maps `marketCap` to `market_cap` and preserves its observation date. The adapter explicitly flags currency, share count, price basis and vintage availability as unknown. | Withhold the live yield until the dated issuer scope, comparable currency and availability are evidenced. |
| Ordered ETF comparison | Derived from the two identified ETF legs and versioned methods. | Require matching metric, schedule, window and basis. Preserve the valid leg when the spread is withheld. |
| Timing study | Derived from historical decision-time regimes and signals, subsequent returns and an explicitly named benchmark. | Require the declared position rule, exposure and horizon, evaluation partition and non-overlapping return path for compounding. |

## Ordered comparison inputs

The `left_proxy` and `right_proxy` assumptions identify the minuend and subtrahend. Each close table belongs to its named proxy. For a shared calendar, both legs use the single eligible calendar in `sessions`. A snapshot containing multiple calendars can identify the listing calendar for each leg with the text assumptions `left_calendar` and `right_calendar`, whose values are calendar entity IDs. Each leg can still report its own metrics when the calendars differ. A spread requires a shared calendar, the same revision and a complete window for that metric on both sides.
