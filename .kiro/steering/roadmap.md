# Roadmap

Discovery record, 2026-11-18. Owner-confirmed direction; no spec below is approved for design or implementation yet.

## Overview

QOpenBB should demonstrate step-by-step finance that makes sense to quants and portfolio managers. The owner invests from a macro, regime-based perspective and compares asset groups, for example commodities against technology. The goal is a set of shipped research stories: each opens with one question, walks through evidence in ordered steps with charts and source rows, and ends in a stated conclusion (supported, not supported or insufficient data). The subject of a story can be changed, and the whole story re-runs.

The chosen approach is narrow first. Verify the cross-asset and macro inputs with live requests, then build one thin end-to-end slice: a minimal calculation service with two simple factors and one regime rule, each with validation checks, feeding one story App. Wider scope follows in later slices.

## Approach Decision

- **Chosen**: verify inputs, then a thin modeling slice. One story ("Commodities vs tech: which regime are we in?") with momentum, realized volatility and one macro regime rule, computed in the financial-modeling service and shown in one App with a changeable pair.
- **Why**:
  - No commodity, index, ETF or sector input has accepted live evidence, and only one FRED series is verified. Designing before verifying would build on assumptions.
  - Project rules keep financial formulas out of widgets, and no calculation service exists yet. A thin slice builds that service once, in the right place.
  - Timing signals look good in-sample easily. Validation diagnostics in the first slice keep the demo credible to a quant.
- **Rejected alternatives**:
  - *Verified snapshot story*: pre-computed from captured data with saved charts, as the chart gallery does. Fast, but fixed baskets and date; a quant may read it as canned.
  - *Live widgets without calculations*: changeable, but shows no factors and is not convincing.
  - *All seven factors and every App at once*: several specs of work before any demo.

## Scope

- **In**:
  - live verification of cross-asset and macro inputs, with licence status recorded beside provenance
  - a minimal financial-modeling service and simple, transparent factors: momentum, volatility, a FRED-based regime rule first; then FCF yield, sector rotation, carry and credit stress
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

- [ ] market-data-integrations -- Cross-asset and macro input verification: index, ETF and commodity prices on the existing daily route; FRED real yield, curve slope, commodity spot and a displayable stress measure; licence status per input. Dependencies: none
- [ ] financial-modeling -- Create the repository and deliver the foundation subset needed to run and validate one model and project its results to widgets. Dependencies: none
- [ ] openbb-self-service -- Shared date-range context across widgets, and saved chart state on live widgets in curated Apps. Dependencies: none
- [ ] market-data-integrations -- Batch C: provider DCF, custom DCF and as-reported statements. Dependencies: none
- [ ] market-data-integrations -- Sector classification, sector performance and constituents for sector rotation beyond ETF proxies. Dependencies: cross-asset and macro input verification
- [ ] analyst-workspace -- Bring the Company Research App to the story standard and link it to the shared subject context. Dependencies: research-stories

## Direct Implementation Candidates

- [ ] fred-attribution-notice -- Add the required FRED notice and per-series copyright text to FRED-based views; a small display change with no new boundary.

## Specs (dependency order)

- [ ] factor-signals -- Simple, transparent factors with regime conditioning, timing signals and validation diagnostics, computed in the modeling service. Dependencies: none
- [ ] research-stories -- Step-by-step story Apps with a stated question, ordered evidence steps, a changeable subject and a stated conclusion. Dependencies: factor-signals
- [ ] private-signal-seam -- A private interface for externally computed regime and factor-timing signals, kept out of all public artifacts. Dependencies: factor-signals
