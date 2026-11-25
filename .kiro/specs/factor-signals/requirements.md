# First-slice factor requirements

An analyst comparing commodity and technology proxies needs to distinguish relative price performance, risk and the real-yield environment. Company FCF yield supplies a separate valuation drill-down. The modeling service owns calculations. The story App owns subject controls, charts and conclusions.

### 1. ETF price factors

1. When 64 consecutive trading-session closes are available for a selected proxy, the service shall report momentum as the ending split-adjusted close divided by the starting close minus one, expressed as a percentage.
2. Given the same 64 closes ordered by session, the service shall calculate 63 daily simple returns and report their sample standard deviation (divisor 62) multiplied by the square root of 252, expressed as annualized percentage volatility.
3. If a required session close is missing, the service shall return insufficient history for that proxy. A window spanning a gap between verified history segments fails this check.
4. When reporting either factor, the service shall identify the proxy, trading calendar, window endpoints, observation count and price-return basis, including the exclusion of dividends.

### 2. Real-yield regime

1. When DFII10 observations exist for the comparison session and the session 63 trading sessions earlier, the service shall classify the later value minus the earlier value as rising for a positive difference, falling for a negative difference and flat for zero.
2. If either endpoint lacks an observation available as of the evaluation time, the service shall report insufficient data and identify the missing endpoint. An interior gap alone shall not invalidate the endpoint comparison.
3. When reporting a classification, the service shall identify the trading calendar, FRED series, two observation dates, yield levels in percent and change in percentage points.

### 3. Company free cash flow yield

1. When a selected company has eligible inputs, the service shall report 100 times trailing twelve-month operating cash flow less capital expenditures, divided by observation-date equity market value, with the subtraction performed before division.
2. When constructing the numerator, the service shall deduct capital expenditures as a positive spending amount and identify the cash-flow periods and filings available by the observation date.
3. If free cash flow is negative and market value is positive, the service shall preserve the negative yield. A zero numerator with a positive denominator shall produce zero percent.
4. If the trailing period is incomplete, filing availability cannot be established, currencies cannot be reconciled, or dated market value is missing or nonpositive, the service shall withhold the yield and identify the failed check.
5. When an analyst inspects the result, the service shall identify the issuer, numerator components, currency, market value, dates, sources and as-of basis. The first slice applies this measure to companies only.

### 4. Evidence and interpretation

1. When comparing two proxies, the service shall report their observation windows and check states beside the results. If either proxy lacks a valid result, the comparison shall identify which input prevents a conclusion.
2. When evaluating subsequent performance by regime, the service shall use only signals available before the evaluated return and disclose the evaluation period, sample count, universe and coverage limits.
3. When presenting timing diagnostics, the service shall disclose the outcome horizon, benchmark, hit-rate denominator, average winner and absolute average loser used for the slugging ratio, drawdown basis, and in-sample or out-of-sample status. If a ratio has no valid denominator, the service shall report it as undefined.
4. Before a model result is accepted, an independent recalculation shall verify the value and check state against the same dated inputs, including missing-history and boundary cases.

The [discovery brief](brief.md) retains later factor candidates. The [input checkpoint](../../../docs/provider-coverage.md#cross-asset-and-macro-inputs-checkpoint-2026-11-18) records the scope of verified provider history. Historical company market value and point-in-time filing coverage require evidence before numerical FCF yield acceptance.
