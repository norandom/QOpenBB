# Investment analysis and valuation dashboards

Owner direction, 2026-10-28: deliver professional investment-analysis workflows, with CFA-level analytical discipline as a quality target, not a certification claim. A company selector supports the work; it is not the deliverable. Reuse existing OpenBB controls, layouts, charts and saved state. An embedded browser is out of scope.

This bounded contract extends the initialized analyst specification under the prototype-first workflow. The owner approved the direction; detailed implementation designs and completed functionality are not implied. Provider adapters and entitlement verification belong to `market-data-integrations`.

The shared data boundary is the existing OpenBB Python platform maintained in our owned fork, not a new ORM or notebook service. Widgets and later AI consume its command/API contracts. [Provider ownership and reuse requirements](../market-data-integrations/research.md#owned-openbb-platform-and-provider-reuse) govern FMP/yfinance adaptations and the future database extension.

## Decisions the workspace must support

Owner clarification, 2026-10-28: data acquisition and house financial modeling are separate concerns. Workspace presents their outputs; house calculations belong in a separate, extensible modeling layer. FMP DCF is an optional comparator. The [house-standard reflection](house-modeling-reflection.md) proposes the modeling requirements, module/service boundary and eventual three-year historical / five-year forecast workflow. Its detailed clauses and deployment design await the respective Kiro approvals; existing analyst acceptance obligations remain in force.

| Workflow | Analyst decision | Required evidence |
| --- | --- | --- |
| Quarterly performance | What changed in the business? | Quarterly/annual statements, segment drivers where available, margins, guidance, actuals versus estimates and comparable periods |
| Earnings quality | Do reported earnings convert into cash? | Reported/adjusted reconciliation, working capital, capex, operating cash flow and explicitly defined cash-conversion metrics |
| Peer valuation | Is the company expensive relative to appropriate peers? | Editable peer set and rationale, EV bridge, EV/revenue, EV/EBITDA, EV/EBIT and P/E with consistent periods and adjustments |
| Intrinsic valuation | What assumptions support the valuation? | FMP DCF baseline, available model inputs, analyst scenarios, enterprise-to-equity reconciliation and sensitivity ranges |
| Capital costs and macro | Has required return changed, or have business expectations changed? | Cost-of-capital components, dated rates/spreads, ROIC versus WACC and separate operating/discount-rate scenarios |
| Thesis and catalysts | What could change the investment conclusion? | Inline news and earnings-call transcripts, estimates/revisions, dated thesis assumptions, catalysts and risks |

## Acceptance criteria

- IA1: When an analyst changes the company, the dashboard shall update linked company views using a readable company name and stable identity. Macro series retain their own identifiers. Company, observation-date and fiscal-period controls shall have distinct meanings.
- IA2: Every material metric shall expose its definition, source, currency, units, period, as-of date and calculation basis. The workspace shall distinguish reported values, provider calculations/estimates and analyst overrides. Missing values shall remain missing; unsupported or unavailable data shall be explained inline.
- IA3: Quarterly comparisons shall distinguish discrete quarters, year-to-date, annual and trailing periods. Deriving a quarter from cumulative reports shall retain the derivation and fiscal-calendar basis. Restatements and historical availability shall be identified where supplied; unavailable vintages shall preclude point-in-time claims.
- IA4: Cash-conversion metrics shall name their numerator and denominator. EBITDA adjustments shall retain reported inputs, each adjustment and its rationale. Lease treatment and financial-sector differences shall remain explicit rather than forcing all companies into one industrial-company model.
- IA5: Peer analysis shall support editable membership and rationale, period-consistent historical/forward multiples and an inspectable enterprise-to-equity bridge. Negative or zero denominators shall display a meaningful unavailable/not-meaningful state and shall not silently enter peer aggregates. Currency conversions, diluted share basis, debt, cash, minority interests and other claims shall be traceable without double counting.
- IA6: FMP DCF output shall be labeled as a provider valuation with its date and available assumptions. Missing model detail shall not be invented. Analyst overrides shall be saved separately. A sensitivity surface shall be shown only when the underlying model can be recalculated or the provider demonstrably supports those inputs; multiplying a provider price by an assumed discount factor is not a DCF sensitivity.
- IA7: The capital-cost view shall expose the selected risk-free benchmark, beta method, equity risk premium, pretax borrowing-cost basis, after-tax debt cost, justified tax-shield assumption and market-value capital-structure weights. Currency, nominal/real basis, valuation date and maturity choice shall be consistent or explicitly flagged. Credit-index spreads are contextual proxies, not automatically the issuer's borrowing cost; risk premiums shall not be double counted.
- IA8: Valuation shall pair firm cash flows with WACC and equity cash flows with cost of equity. Perpetuity-growth scenarios with growth at or above the discount rate shall be rejected. Terminal growth, reinvestment, terminal-value contribution and capital returns shall have visible economic assumptions. ROIC/WACC comparisons shall disclose their invested-capital, tax and accounting conventions.
- IA9: News and transcripts shall render useful text inline with company, event/publication date and attribution. Entitlement failures, partial content and unavailable transcripts shall be visible. An external browser shall not be required to complete the supported research workflow.
- IA10: Saved research context shall retain company, periods, peer membership, assumptions, layout and linking groups through fresh authenticated reopening and retained-bind container recreation. Refresh shall not overwrite analyst assumptions silently. The UI shall show data freshness and distinguish market-input updates from a deliberately frozen valuation scenario.

## Bounded delivery sequence

- [ ] IA-A: Verify provider responses and reuse paths for a representative nonfinancial company and a small peer set. Record endpoint, entitlement, fields, units, periods and missing inputs. Gate IA-B on verified balance-sheet, cash-flow, market-price/share-count and enterprise-value inputs. Include FMP DCF/custom-DCF feasibility and FRED macro inputs; do not mistake provider documentation for working integration.
- [ ] IA-B: Deliver quarterly financial analysis and peer valuation together as the first usable analyst dashboard. Reuse existing parameter groups, tables and charts. Include explicit cash-conversion definitions, inspectable multiples and saved research context.
- [ ] IA-C: Add the FMP valuation baseline and cost-of-capital/macro bridge. Enable model sensitivities only after the model-input contract passes. Keep provider values and analyst scenarios distinct.
- [ ] IA-D: Complete the linked expectations, news, earnings-call and thesis workflow. Preserve already available content during earlier slices; do not wait for this slice to expose reusable working widgets.

All workflow rows remain target scope. Each slice gets a small design/task contract, independent financial review and affected checks before implementation. Production limits remain 400 physical lines/file, 300 logical units/file and 50/function; each code task updates the maintained inventory and runs its checker. Use disjoint provider and UI lanes only after their data contract is frozen. Publish images after a meaningful accepted slice, not every commit.

## Evidence strategy and present gaps

Reuse existing catalog, financial-transformation and isolated browser checks. Add focused numerical checks for reconciliations, missing/negative inputs, fiscal periods and valuation calculations; independently recalculate material outputs. One representative real-FMP journey per slice must demonstrate displayed values and research-context persistence with clean browser/CDP diagnostics. Synthetic edge cases supplement real data. No new test framework is required.

The [published initial financial-input batch](../../../artifacts/reviewed/financial-input-milestone/accepted.md) now includes ten FMP adapters and the generic FRED series contract, with separate live-input and packaged Income evidence. This supplies more IA-A inputs but does not close its DCF/custom-DCF feasibility or the full analyst journeys above. Existing parameter controls, linking and App export are source-confirmed in the [reuse map](../../../docs/capability-reuse.md). The [paired company-selector design](company-selector-design.md) is independently reviewed and pending owner approval; it is a bounded next UX slice, not completion of IA-B. Exact DCF response fields and plan entitlement remain unverified. Banks, insurers and other sector-specific valuation models need separate treatment before being advertised as supported.

## References

- [FMP API documentation](https://site.financialmodelingprep.com/developer/docs): standard, levered and custom DCF endpoints; documented cost-of-capital inputs. Documentation is a discovery source, not entitlement or calculation acceptance.
- [Damodaran: valuation framework](https://pages.stern.nyu.edu/~adamodar/New_Home_Page/lectures/val.html): cash-flow and discount-rate consistency.
- [Damodaran: discount-rate inputs](https://pages.stern.nyu.edu/~adamodar/pdfiles/invphiloh/valuation.pdf): currency/nominal consistency, borrowing spreads and capital-structure weights.

Independent financial review accepted this bounded direction on 2026-10-28, with the market-value weights/tax-shield distinction and IA-B input prerequisites incorporated. This is not approval of an implementation design or complete umbrella specification.
