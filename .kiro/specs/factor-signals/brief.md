# Brief: factor-signals

## Problem

A macro investor wants to see whether simple factors behave differently across regimes, and whether simple timing rules add anything. Today QOpenBB shows provider tables but computes nothing: there are no returns, factors, regimes or diagnostics. A quant or portfolio manager cannot check a claim such as "tech momentum fades when real yields rise" inside the tool.

## Current State

- 29 FMP models and a generic FRED series route are registered. Only single-company equity inputs and one FRED series have live evidence.
- Daily prices are split-adjusted only, one symbol per request, in five-year windows.
- The financial-modeling spec is approved (requirements, design, 18 tasks) but its repository does not exist and nothing is implemented.
- Project rules forbid financial formulas in widgets.

## Desired Outcome

A small set of factors that a quant can audit: each states its rule, universe, window, inputs and limits, and each result carries check states. The first delivery supports one story with momentum, realized volatility and one FRED-based regime rule. Later deliveries add FCF yield, sector rotation, carry and credit stress, and an expected-returns decomposition in the style of Ilmanen's *Expected Returns*.

Every signal reports hit rate, slugging ratio (average winner over average loser across the universe), drawdown, and its validation limits.

## Approach

Implement factors as models in the financial-modeling service, using its validation and run contracts. Start with the thinnest set that serves the first story. Use ETF or index proxies for asset groups until constituents data is accepted. Regime rules are transparent thresholds on public macro series; a private signal can replace them later through `private-signal-seam`.

## Scope

- **In**:
  - return construction from accepted price inputs, with the not-total-return caveat stated
  - momentum, realized volatility and a regime rule (first delivery)
  - FCF yield, sector rotation, carry, credit stress and an expected-returns decomposition (later deliveries)
  - regime-conditioned factor results and simple timing rules
  - diagnostics: hit rate, slugging ratio, drawdown
  - validation: look-ahead safety, explicit date ordering, coverage and survivorship limits, in-sample versus out-of-sample separation
- **Out**:
  - provider adapters and input verification (market-data-integrations)
  - the service foundation itself (financial-modeling)
  - dashboards and narrative (research-stories)
  - the owner's proprietary model and any of its content
  - portfolio, trade or position inputs

## Boundary Candidates

- return and universe construction from provider inputs
- individual factor definitions, one model each
- regime classification
- timing rules and their diagnostics
- validation checks shared by all factors

## Out of Boundary

- deciding what a provider value means (owned by the provider contracts)
- rendering, layout and story text
- any optimisation, portfolio construction or advice

## Upstream / Downstream

- **Upstream**: market-data-integrations (verified cross-asset and macro inputs, licence status); financial-modeling (service foundation, validation and result contracts)
- **Downstream**: research-stories; private-signal-seam; a later DCF drill-down

## Existing Spec Touchpoints

- **Extends**: none
- **Adjacent**: financial-modeling (foundation and house-method rules); analyst-workspace investment-analysis contract (metric disclosure rules IA2, IA5)

## Constraints

- Sort by date explicitly and pin the Polars major version; Polars 2.x does not preserve row order by default.
- Credit stress must use inputs that may be displayed; ICE BofA and Moody's spread series on FRED are restricted.
- History depth depends on each installation's provider plan; results state the window actually covered.
- Zero or negative denominators show as not meaningful, never as a number.
- 400/300/50 complexity caps; independent review and recalculation by a separate reference for every model.
