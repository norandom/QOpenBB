# Roadmap

Updated 2026-11-25. The Ubuntu financial dashboard journey passed. The company FCF yield definition is agreed. The factor requirements are approved. The [factor design](../specs/factor-signals/design.md) is owner-approved. The [factor task plan](../specs/factor-signals/tasks.md) is owner-approved. The modeling foundation has an approved task plan. The story spec remains at discovery.

## Delivery sequence

1. **Ubuntu dashboard baseline completed, 2026-11-25.** The canonical Company Research Playwright test passed its initial and retained-recreation phases on packaged release `alpha-44340458084-1` with native Docker Compose. All 54 required captures matched. The owner waived the FMP request ceiling for this run. [Handover](../handover.md)
2. **Factor task plan approved.** The owner selected company-level FCF yield using trailing twelve-month operating cash flow less capital expenditures, equity market value on the observation date and filings available by that date. Both price factors use 64 consecutive closes over 63 trading sessions. The [factor requirements](../specs/factor-signals/requirements.md) are approved. The agreed regime compares DFII10 with its value 63 trading sessions earlier; a positive, negative or zero change means rising, falling or flat. A missing DFII10 endpoint yields insufficient data. [Factor brief](../specs/factor-signals/brief.md)
3. **Extend the existing data API.** The owner identified `qopenbb-data-api` as the analytics runtime. Inventory reusable calculations in the locked OpenBB fork and trace the packaged app and catalog entry points. Map the factor contracts, tests and task paths to this backend before implementing the first factor. The earlier foundation plan describes the calculation and verification contracts; its separate-repository bootstrap is superseded for this slice.
4. **Verify the calculations.** Independently recalculate each factor and the regime classification. Check price-return labeling, date ordering, look-ahead safety and insufficient history. The verified fund inputs cover two disjoint windows; derive each lookback only from adequate history within its window. [Input checkpoint](../../docs/provider-coverage.md#cross-asset-and-macro-inputs-checkpoint-2026-11-18)
5. **Build and accept the commodities-versus-technology App.** Review the story requirements, design and tasks. Connect subject and date controls to all steps, preserve live chart settings, and show source rows, counter-evidence and a conclusion. Repeat the Ubuntu browser journey on this App, including subject changes and insufficient data. [Story brief](../specs/research-stories/brief.md)
6. **Follow with Events and Documents, then DCF.** Events and Documents can reuse the published Batch B inputs. Before building the DCF drill-down, review Batch C design, tasks and request allowance, then verify provider DCF, custom DCF and as-reported statement inputs. Use the accepted inputs for a step-by-step valuation story. [Expansion plan](../specs/market-data-integrations/fmp-expansion-plan.md)

## Overview

QOpenBB should demonstrate step-by-step finance that makes sense to quants and portfolio managers. The owner invests from a macro, regime-based perspective and compares asset groups, for example commodities against technology. The goal is a set of shipped research stories: each opens with one question, walks through evidence in ordered steps with charts and source rows, and ends in a stated conclusion (supported, not supported or insufficient data). The subject of a story can be changed, and the whole story re-runs.

The chosen approach is narrow first. Verify the cross-asset and macro inputs with live requests, then build one thin end-to-end slice: a minimal calculation service with three simple factors and one regime rule, each with validation checks, feeding one story App. Wider scope follows in later slices.

## Approach Decision

- **Chosen**: verify inputs, then a thin modeling slice. One story ("Commodities vs tech: which regime are we in?") with momentum, realized volatility, FCF yield and one macro regime rule, computed in the financial-modeling service and shown in one App with a changeable pair.
- **Why**:
  - The accepted checkpoint covers six ETFs and eight FRED series. Missing observations, weekly series and disjoint fund windows constrain which comparisons the first story can support.
  - Project rules keep financial formulas out of widgets, and no calculation service exists yet. A thin slice builds that service once, in the right place.
  - Timing signals look good in-sample easily. Validation diagnostics in the first slice keep the demo credible to a quant.
- **Rejected alternatives**:
  - *Verified snapshot story*: pre-computed from captured data with saved charts, as the chart gallery does. Fast, but fixed baskets and date; a quant may read it as canned.
  - *Live widgets without calculations*: changeable, but shows no factors and is not convincing.
  - *All seven factors and every App at once*: several specs of work before any demo.

## Scope

- **In**:
  - live verification of cross-asset and macro inputs, with licence status recorded beside provenance
  - a minimal financial-modeling service and simple, transparent factors: momentum, volatility, FCF yield and a FRED-based regime rule first; then sector rotation, carry and credit stress
  - diagnostics per signal: hit rate, slugging ratio (average winner over average loser across a universe), drawdown, and look-ahead, survivorship and coverage limits
  - an expected-returns decomposition in the style of Ilmanen's *Expected Returns*, as a later model
  - story Apps shipped in the catalog, with a changeable subject, charts from the existing library and drill-down to source rows
  - later stories: Events and Documents (Batch B inputs), a DCF drill-down with gated validation steps (Batch C inputs), and an upgraded Company Research App
  - a private interface through which an external owner model can supply regime and factor-timing signals
- **Out**:
  - re-implementing or publishing the owner's proprietary factor-timing system; its content never enters repositories, contracts, fixtures, releases or evidence mirrors
  - shipping provider data: the tool ships none, and each installation fetches with its own keys
  - portfolio or trade inputs, order execution, and investment advice
  - a visual redesign of the Workspace; stories stay inside the existing shell and controls
  - constituent-level sector baskets in the first slice; ETF or index proxies stand in until constituents data is accepted

## Constraints

- Formulas live in the modeling service, never in widgets (`analyst-workspace/house-modeling-reflection.md`). Every metric shows definition, source, units, period, as-of date and basis.
- Prices are split-adjusted only, one symbol per request, in five-year windows. Returns built on them are not total returns and must say so.
- Credit-spread series from ICE BofA and Moody's on FRED are copyrighted, restricted to internal use, and ICE history is cut to three years. Credit stress needs inputs that may be shown, such as Federal Reserve stress indexes or Treasury-based measures, to be verified.
- FRED-based views carry the required FRED notice and per-series copyright text.
- Showing fetched provider data to other people is governed by each installation's own provider terms. FMP history depth and asset-class access depend on the plan tier; verification records the earliest date returned per symbol class.
- Polars 2.x does not preserve row order by default: sort by date explicitly, pin the major version and test it.
- Existing gates apply: requirements, design and tasks approval per spec; independent review per task; real-data browser acceptance per story; 400/300/50 complexity caps; one delivery slice active at a time.
- Curated Apps currently drop saved chart state on live widgets. Story Apps need that restriction lifted in a reviewed way.

## Boundary Strategy

- **Why this split**: inputs, calculations and presentation change for different reasons and are reviewed by different checks. Provider adapters prove what the data is. Factor models prove what a number means and when it is valid. Stories prove that an analyst can follow the reasoning. Keeping the private model behind its own interface lets public work proceed without touching proprietary content.
- **Shared seams to watch**:
  - the result contract between the modeling service and Workspace widgets (values, check states, provenance)
  - licence status and provenance carried from provider inputs through to story steps
  - the shared subject and date context that drives every step of a story
  - the point where a private signal replaces a transparent regime rule, without leaking into public artifacts

## Existing Spec Updates

- [x] market-data-integrations -- Accepted the bounded six-ETF and eight-series FRED input checkpoint on 2026-11-18. Rights-label enforcement, WTI typing and the recent-window row-count label remain open. [Handover](../handover.md)
- [ ] financial-modeling -- Extend the existing data API with the foundation subset needed to run and validate one model and project its results to widgets. Confirm the existing module boundaries and method inputs before execution.
- [ ] openbb-self-service -- Shared date-range context across widgets, and saved chart state on live widgets in curated Apps. Dependencies: none
- [ ] market-data-integrations -- Batch C: provider DCF, custom DCF and as-reported statements. Dependencies: none
- [ ] market-data-integrations -- Sector classification, sector performance and constituents for sector rotation beyond ETF proxies. Dependencies: cross-asset and macro input verification
- [ ] analyst-workspace -- Bring the Company Research App to the story standard and link it to the shared subject context. Dependencies: research-stories

## Direct Implementation Candidates

- [ ] fred-attribution-notice -- Add the required FRED notice and per-series copyright text to FRED-based views; a small display change with no new boundary.

## Specs (dependency order)

- [ ] factor-signals -- Simple, transparent factors with regime conditioning, timing signals and validation diagnostics, computed in the modeling service. Execution depends on the modeling foundation and accepted inputs for each factor.
- [ ] research-stories -- Step-by-step story Apps with a stated question, ordered evidence steps, a changeable subject and a stated conclusion. Dependencies: factor-signals
- [ ] private-signal-seam -- A private interface for externally computed regime and factor-timing signals, kept out of all public artifacts. Dependencies: factor-signals
