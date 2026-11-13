# Company Research dashboard requirements

Status: requirements for owner review, 2026-11-13. Owner authorized this bounded requirements and gap-reconciliation step; design, tasks and implementation are not yet approved.

## Introduction

Financial engineers need one coherent research view in which a readable company selection drives statements and price context, and an editable peer set supports inspection of provider observations. The first delivery organizes the accepted data into a usable dashboard and explains comparison limits at the point of use. It is an incremental IA-B delivery, not acceptance of the full quarterly-analysis and peer-valuation workflow.

## Boundary context

- In scope: an installable Company Research App; shared company name/symbol selection; annual/quarterly Income, Balance and Cash views; dated price context; editable candidate peers with rationale; provider-observation comparison; explicit eligibility states; saved research context; familiar existing controls, themes and chart behavior.
- Adjacent expectations: the accepted data contracts retain source values and provenance. Financial-modeling owns house definitions, calculations and validated comparison methods in its separate workstream. Existing macro widgets remain independent of company selection.
- Out of scope: new house ratios, cash-conversion formulas, adjusted EBITDA, derived quarters or TTM, peer aggregate calculations, currency conversion, inferred enterprise-to-equity bridges, DCF/WACC/scenarios, forecasts, sector-specific valuation, new providers, AI, Excel, command-language implementation and a renderer redesign. News/transcripts remain later roadmap slices; this slice does not remove available widgets.
- The current finance-modeling deliverable remains a specification stub. This dashboard must remain useful without a running model service. It does not present missing financial methods as verified calculations or close umbrella IA-B criteria.

## Requirements

### Requirement 1: Familiar and usable research workspace

**Objective:** As an analyst, I want to open a coherent research layout instead of assembling disconnected raw tables.

1.1 When an analyst opens the Company Research App from the catalog, the Workspace shall present company identity, Income, Balance, Cash, price context and peer observations in a predefined layout with visible section labels and controls accessible through the existing scrolling and resizing behavior.
1.2 When an analyst uses the research App, the Workspace shall retain existing theme selection, widget editing, chart controls and dashboard navigation without removing or hiding unrelated existing features.
1.3 If a section has no data or entitlement, the Workspace shall explain its state inline and retain the usable sections and the analyst's selections.

### Requirement 2: Company and time selection

**Objective:** As an analyst, I want to investigate a company by name while keeping financial and market dates distinct.

2.1 When an analyst searches for and selects a company, the Workspace shall display its name and symbol with available listing/exchange identity and update only the explicitly linked primary-company views.
2.2 When a company selection changes or is cleared, the Workspace shall prevent responses for the previous selection from being displayed as current-company data and shall prevent empty-symbol provider queries.
2.3 When an analyst selects annual or quarterly statements, the Workspace shall apply that choice to the linked statement views and display each returned row's actual period end and fiscal label without treating matching labels as proof of matching duration.
2.4 When an analyst changes a price observation window, the Workspace shall preserve statement period selection and peer membership; when a statement period changes, it shall preserve the price window unless the analyst explicitly changes it.
2.5 While comparison peers or independent macro widgets are present, the Workspace shall preserve their identities when the primary company changes.

### Requirement 3: Financial meaning and provenance

**Objective:** As an analyst, I want to distinguish reported facts from uncertain or calculated measures.

3.1 When the Workspace displays a material statement or comparison value, it shall provide inspectable source, field definition, unit, scale, currency, period basis, observation date and value origin, explicitly marking unavailable facts as unknown.
3.2 When the Workspace displays statement-period evidence, it shall retain row attribution and distinguish provider fiscal labels from evidenced coverage, supplied filing/acceptance dates and unknown restatement or historical availability.
3.3 If a value is missing, duplicated, zero or negative, the Workspace shall preserve that state and shall not replace missing values with zero or silently collapse duplicate observations into one period.
3.4 When the Workspace displays provider ratios or multiples, it shall identify them as provider calculations rather than house calculations and show the available calculation basis and its limitations.
3.5 If currency, price/share dates, claim scope or period coverage is unavailable, the Workspace shall disclose the missing evidence rather than infer compatibility from company identity, a numeric value or matching field names.

### Requirement 4: Editable peers and comparison eligibility

**Objective:** As an analyst, I want to inspect candidate peers without mistaking a populated table for a defensible comparable set.

4.1 When an analyst adds, removes or reorders a candidate peer, the Workspace shall retain that peer's name, source-qualified listing identity and editable rationale independently of the primary-company selector.
4.2 When the Workspace displays peer observations, it shall use consistent field labels, units and value-origin labels across companies while retaining each observation's actual currency, fiscal period and dates.
4.3 If a required financial compatibility fact is missing or conflicting, the Workspace shall label the affected comparison as unverified or incompatible, show the reason, and keep the original observation inspectable.
4.4 If a multiple's denominator is missing, zero, negative or unsupported by available evidence, the Workspace shall withhold any valid-comparable claim for that multiple and explain the reason; a provider-supplied numeric multiple may remain visible with its provider and unverified/not-meaningful status.
4.5 While no separately accepted financial method supplies a validated eligibility result, the Workspace shall keep peer observations explicitly unverified for aggregation and shall not present aggregates or rankings as validated peer valuations; any retained generic table/chart aggregation shall remain explicitly unverified for that purpose.
4.6 When the analyst changes peer membership or rationale, the Workspace shall preserve source observations and their failure/unknown states rather than treating analyst selection as financial validation.

### Requirement 5: Saved context and refresh

**Objective:** As an analyst, I want to continue a research session without losing my choices or confusing refreshed data with frozen evidence.

5.1 When an analyst saves and reopens the App in a fresh authenticated session, the Workspace shall restore the primary company, statement period selection, price window, peer identities/order/rationales, layout and explicit linking groups.
5.2 When the application containers are recreated with their retained data directory, the Workspace shall restore the same saved research context.
5.3 When an analyst refreshes data, the Workspace shall retain analyst-owned selections and peer rationales, show the resulting data freshness or failure state, and invalidate any affected inherited comparison-status claim.
5.4 If a refresh fails while older data remains displayed, the Workspace shall identify that data as stale and distinguish its observation/acquisition dates from the failed refresh attempt.
5.5 While no immutable data snapshot is supported for this slice, the Workspace shall describe saving as persistence of research configuration rather than a frozen valuation or point-in-time dataset.
5.6 When an analyst exports and imports the research App template, the Workspace shall preserve the primary company identity and coherent name/symbol display, statement period, price window, peer identities/order/rationales, layout and linking groups as research configuration without exporting credentials or session tokens; unavailable identities shall be shown as unresolved rather than silently substituted.

### Requirement 6: Contract and delivery evidence

**Objective:** As a maintainer, I want changes to preserve analyst-visible meaning without creating a new verification framework.

6.1 When a participating data or consumer contract changes, the delivery workflow shall identify affected research views and verify their field types, nullability, units, periods and failure states against the supported contract before acceptance.
6.2 When this slice is submitted for acceptance, the delivery workflow shall demonstrate a representative primary company and two candidate peers using real FMP observations, company/period changes, missing or incompatible comparison evidence, refresh, saved reopening and App-template export/import, with visible values checked against source evidence.
6.3 When claiming persisted research context, the delivery workflow shall demonstrate retained-data container recreation without representing that test as backup/restore or owner-server deployment.
6.4 When publishing an accepted feature milestone, the delivery workflow shall bind actual checks and independent financial review to the participating source and image identities and update the roadmap and breadth record; planned or skipped checks shall not count as completed evidence.

## Approval boundary

The original IA-A assessment and its receipts remain dated evidence. The accompanying reconciliation identifies resolved acquisition defects and remaining financial prerequisites. Design must map these requirements to existing widget/linking/state mechanisms and split remaining gaps into bounded tasks, carrying the existing 400 physical / 300 logical / 50-per-function caps and executable inventory checks. This document neither approves a new model implementation nor waives IA3-IA8 financial acceptance in the investment-analysis contract.
