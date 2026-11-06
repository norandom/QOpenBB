# Company Research input readiness

Status: requirements proposal, 2026-11-06. This is the next bounded IA-A slice under [investment analysis](investment-analysis-contract.md). It establishes which existing inputs can support the first quarterly and peer dashboard; it does not implement that dashboard or a financial model.

## Introduction

Financial engineers need to know whether the deployed data can support a research decision before arranging it into a dashboard. The initial provider batch and company selector are accepted. Reuse their evidence and identify the remaining financial gaps, rather than repeat their acceptance or treat a provider peer list as a valuation analysis.

## Boundary context

- In scope: a reviewable input-readiness assessment for a representative nonfinancial listed company and at least two candidate peers, covering statements, market inputs, provider metrics, DCF feasibility and Treasury context.
- Source scope: FMP supplies the company and provider-valuation inputs; FRED supplies the Treasury context. This slice introduces no Yahoo, EconDB or custom-source expansion.
- Out of scope: new provider adapters or widgets, dashboard implementation, a house calculation engine, financial-model repository creation, forecasts, investment recommendations, AI, Excel, new themes and infrastructure changes. Missing capabilities become explicitly owned follow-on work.
- Adjacent expectations: market-data-integrations owns acquisition and provider contracts; analyst-workspace owns this workflow assessment and later presentation. Financial-modeling owns house definitions and calculations. Existing deployments and independent macro/comparison widgets continue to work.
- Evidence boundary: historical accepted observations establish only their recorded queries and dates. Published endpoint documentation, source availability, current account access and a complete analyst workflow remain separate claims.

## Requirements

### Requirement 1: Identify the research sample and reuse accepted inputs

**Objective:** As a financial engineer, I want a bounded company sample and an honest coverage record so that further development addresses actual gaps.

1.1 When an input-readiness assessment is prepared, QOpenBB shall identify the primary nonfinancial company and at least two candidate peers by readable name, source-qualified listing, exchange where available and reporting currency.
1.2 When candidate peers are listed, QOpenBB shall distinguish provider suggestions from analyst-selected comparables and record the inclusion rationale and material business or accounting differences.
1.3 When existing acceptance is reused, QOpenBB shall retain its query, observation and acquisition dates, tested source or image identity and original scope rather than relabeling it as a new live check.
1.4 If a required input lacks applicable evidence, QOpenBB shall identify it as unverified, unavailable, access-blocked or semantically unsuitable with the specific missing proof and owning follow-on workstream.

### Requirement 2: Establish comparable statement inputs

**Objective:** As an analyst, I want the reporting basis visible so that apparent trends are not caused by mixing incompatible periods or units.

2.1 When statement inputs are assessed, QOpenBB shall record availability of income, balance-sheet and cash-flow observations for the primary company and each candidate peer, identifying fiscal year, fiscal period, period end, duration or instant basis, currency and units.
2.2 When quarterly and annual observations are assessed, QOpenBB shall distinguish discrete quarters, cumulative year-to-date and annual values, and identify any unavailable duration or restatement information rather than assume comparable periods.
2.3 When earnings-quality inputs are assessed, QOpenBB shall map reported revenue, operating earnings, net income, depreciation/amortization, operating cash flow, capital expenditure and working-capital inputs to their supplied definitions or mark them missing; provider-calculated EBITDA or free cash flow shall remain separately labeled.
2.4 If the supplied statements do not support an unambiguous cash-conversion definition or adjustment basis, QOpenBB shall record the unresolved numerator, denominator, sign, lease or accounting treatment as a modeling prerequisite rather than calculate a substitute.

### Requirement 3: Establish market and valuation input compatibility

**Objective:** As an analyst, I want valuation inputs assessed on their actual basis so that an available field is not mistaken for a defensible multiple.

3.1 When market inputs are assessed, QOpenBB shall record price date, currency, adjustment basis and share-count type/date where supplied, and identify mismatches with statement periods or enterprise-value dates.
3.2 When enterprise-value inputs are assessed, QOpenBB shall identify the supplied market-capitalization, debt, cash and enterprise-value fields and their definitions, and record missing minority, preferred, lease or other claims without assuming a complete enterprise-to-equity bridge.
3.3 When provider ratios or key metrics are assessed, QOpenBB shall retain their supplied names, units, period basis and calculation limitations and distinguish provider outputs from house-recalculated multiples.
3.4 If currency, fiscal-calendar, trailing/forward basis, share basis or denominator validity prevents comparison, QOpenBB shall flag the affected comparison as unsuitable or unresolved; negative, zero and missing denominators shall not qualify as accepted peer-aggregate inputs merely because a numeric provider ratio exists.

### Requirement 4: Assess DCF feasibility and macro context

**Objective:** As a financial engineer, I want the remaining valuation prerequisites explicit so that the next phase does not invent a model behind a provider price.

4.1 When FMP DCF and custom-DCF feasibility are assessed, QOpenBB shall separately record available source integration, documented capabilities, verified account access and observed output/assumption coverage, preserving unknown states where no permitted query has established them.
4.2 If a provider DCF response is available, QOpenBB shall identify its valuation date, currency, available assumptions and missing model detail and label it as a provider valuation; availability shall not establish house DCF or sensitivity support.
4.3 When FRED Treasury context is assessed, QOpenBB shall identify each series by readable name and ID, maturity, observation date, units, frequency and source, and distinguish a single benchmark series from a yield curve or a complete company cost of capital.
4.4 If DCF access, custom-input behavior or macro conventions remain unknown, QOpenBB shall record the consequence for IA-C and any IA-B prerequisite separately rather than treat unknown capability as either supported or disproved.

### Requirement 5: Preserve data meaning and the calculation boundary

**Objective:** As a financial engineer, I want acquisition and house modeling to remain distinct so that independently maintained methods can later consume the same verified inputs.

5.1 The QOpenBB readiness assessment shall distinguish reported values, documented normalization, provider calculations and proposed house calculations for every required input family.
5.2 If a research view needs a newly derived margin, growth rate, EBITDA adjustment, cash-conversion ratio, peer aggregate, valuation bridge or forecast, QOpenBB shall record its financial-modeling dependency and required input contract rather than introduce the calculation in the provider or widget.
5.3 If an input is missing, access-restricted or returned with an unknown convention, QOpenBB shall preserve that state and its provenance without supplying zero, an invented assumption or a silent alternative provider.
5.4 When evidence is shared, QOpenBB shall omit credentials, authentication state and private account identifiers while retaining the nonsecret query parameters, retrieval time and source references needed to inspect the claim.

### Requirement 6: Give a bounded readiness decision

**Objective:** As the project owner, I want one actionable decision so that the next delivery yields a useful research dashboard without reopening infrastructure work.

6.1 When IA-A is reviewed, QOpenBB shall present one coverage matrix linking required inputs, existing reusable widgets, actual evidence, unresolved semantics and owning follow-on work.
6.2 When IA-B readiness is decided, QOpenBB shall require verified balance-sheet, cash-flow, market-price/share-count and enterprise-value inputs for the declared sample, and shall distinguish a supported raw/provider-data dashboard from unimplemented house analysis.
6.3 If required evidence or semantics are missing, QOpenBB shall leave IA-B readiness open and identify the smallest corrective scope; a documentation-only assessment shall not mark a provider integration, calculation or dashboard test as passed.
6.4 When the assessment is complete, QOpenBB shall propose the next bounded dashboard/provider contract for owner review, retaining existing name/symbol selection, independent macro context, native controls and the requirement for saved research-context acceptance.

## Acceptance and next phase

The proposal fails if it treats prior sample access as universal coverage, describes candidate peers as a curated comparable set, introduces house formulas into data/widgets, or declares the next dashboard complete without its own real-data journey. Requirements approval precedes the bounded verification design and tasks. Existing source, provider, catalog and browser checks remain the verification foundation; this phase introduces no new test harness.
