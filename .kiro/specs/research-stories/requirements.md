# Commodities versus technology research story

Did the selected commodity proxy outperform the selected technology proxy over the 63 trading sessions ending at the observation date? The first catalog story answers from the verified difference in price returns. Realized volatility describes the risk each proxy experienced. The change in real yields describes the macro setting during the window.

This delivery covers the Workspace story from selection through saved dashboard and export. The published models own calculations and independent checks. Provider integrations own dated observations and availability. Company FCF yield belongs to an issuer drill-down. Predictive timing studies, DCF, Events and Documents, and the Company Research story are separate deliveries. [Story brief](brief.md) · [Factor requirements](../factor-signals/requirements.md)

### 1. Select the comparison

1. When an analyst opens the story from the catalog, the App shall show the question, the two selected ETF tickers and their proxy roles, and the selected observation date before the evidence steps.
2. When the analyst changes either proxy or the observation date, the App shall apply the new selection to every step, source drill-down and conclusion, including the effective window and as-of date returned by the model.
3. While the selection is being evaluated, the App shall identify pending steps and clear the previous selection's evidence and verdict, including when an earlier request finishes late.
4. When navigating by keyboard, the analyst shall be able to change the pair and date, inspect chart evidence, and reach the conclusion using the existing Workspace controls in either theme.

### 2. Inspect the evidence

1. When a comparison is available, the App shall present the two price returns, realized volatility, and DFII10 regime in ordered steps before the conclusion. Each step shall pair its finding with a chart, a check state and access to the supporting dated rows.
2. When displaying the return comparison, the App shall show each proxy's split-adjusted price return in percent, disclose that dividends are excluded, and label the spread as commodity minus technology in percentage points. The analyst shall be able to inspect the 64 session closes, calendar, endpoints and observation count for each valid leg.
3. When displaying risk, the App shall show each eligible proxy's annualized realized volatility in percent and identify the underlying 63 daily simple returns. If the outperforming proxy also had higher realized volatility, the App shall show both findings together so the analyst can see the risk accompanying the return.
4. When displaying DFII10, the App shall show the rising, falling or flat classification, both endpoint dates and real yields in percent, and their change in percentage points. If an eligible endpoint is missing, the App shall identify it. An interior gap alone shall preserve the published endpoint classification.
5. When the analyst inspects any chart or widget, the App shall name its source in the headline or subtitle and expose the observation dates, as-of availability, freshness and verification state used by that step. The DFII10 headline shall credit the Board of Governors of the Federal Reserve System via FRED, and the view shall display the FRED notice. [Verified input sources](../../../docs/reference/cross-asset-inputs.json)

### 3. Decide whether the evidence supports outperformance

1. When the verified matched-window price-return spread is positive, the App shall report **supported** and identify the spread, pair and window supporting the verdict.
2. When that spread is zero or negative, the App shall report **not supported** and distinguish a tie from technology outperformance. The verdict shall use the verified value before display rounding.
3. If the spread is missing, unverified or withheld, the App shall report **insufficient data**, identify the affected input or check and preserve independently valid results. A gap between disjoint history windows shall preclude a spread requiring closes across that gap.
4. If volatility or DFII10 is unavailable while the return spread is verified, the App shall retain the spread-based verdict and identify the missing context at its step. The conclusion shall describe realized performance over the selected window. [Published factor contract](../factor-signals/requirements.md)

### 4. Recover, reopen and reproduce the comparison

1. If an entitlement, provider or modeling failure prevents a step from loading, the App shall show the reason inline and preserve the current selection. When service resumes and the analyst retries, the App shall refresh the affected evidence and verdict for that selection.
2. When the analyst saves and reopens the dashboard in a fresh session, the App shall restore the pair, observation date, chart settings on live and result widgets, and references to the analyst's saved model runs. The dashboard shall persist only choices, configuration and permitted references. Each referenced run shall retain its original values, checks and source dates after a provider revision.
3. When the analyst exports the story, the export shall contain only choices and configuration, including permitted references. Provider rows, response text and credentials shall be absent.

**Acceptance evidence.** Exercise the catalog App on Ubuntu with isolated Playwright and identified images. Use real provider inputs for each chart, change one proxy and then the date, and compare a displayed spread and its supporting rows with the same saved model run. Exercise a date with insufficient history, verify recovery on returning to an eligible date, interrupt modeling, restore service and retry the same selection. Then reopen a saved dashboard in a fresh session and inspect its export. Record coverage and any entitlement failures. These checks are pending. [Testing guidance](../../steering/testing.md)
