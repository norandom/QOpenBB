# Statement period provenance: bounded acceptance contract

Proposed next provider slice, 2026-11-10. Make the time basis of existing FMP Income, Balance and Cash results explicit to downstream consumers. Reuse the accepted routes and financial metadata. A quarterly selector is a requested frequency, not proof that every returned flow covers one discrete quarter.

This elaborates approved market-data-integrations requirements 4.1-4.7 and the accepted IA-A input assessment and its unresolved IA-B input prerequisites. It does not reopen the completed periodic-query repair or native development migration. Implementation remains pending review of the bounded design and task plan.

## Scope

Include the existing annual and quarterly Income, Balance and Cash datasets, using MSFT, ORCL and ADBE as the established acceptance sample. Preserve reported figures, field identities, fiscal labels, ordering and existing query controls. Consumers are existing widgets and future modeling/AI clients; this slice adds no new dashboard or service.

Exclude quarter derivation from cumulative flows, annualization, fiscal synchronization, restatement selection, valuation/market/share reconciliation, cash-conversion formulas, provider expansion and house modeling. Those remain separately owned work. FMP figures remain provider observations or provider calculations, not house results.

## Requirement 1: Identify the period represented by each observation

**Objective:** Consumers can distinguish requested frequency from the time basis supported by evidence.

1.1 When returning a statement observation, the data service shall retain its reported fiscal year, fiscal period label and period end separately from the requested annual or quarterly frequency.
1.2 When returning a flow observation, the data service shall identify whether its actual coverage is annual, discrete-quarter, cumulative year-to-date, trailing or unknown, together with the evidence supporting any known classification.
1.3 When returning an instant observation, the data service shall identify its supplied as-of date, or explicitly mark that date unavailable, without treating it as a flow over the requested period or assigning the statement end to beginning cash.
1.4 If a period start or duration is unavailable, the data service shall disclose that absence without constructing a start date or fixed quarter duration from the period label.

## Requirement 2: Keep source support and uncertainty visible

**Objective:** A consumer can audit an assertion without treating a convention as observed fact.

2.1 When asserting a statement time basis, the data service shall distinguish information supplied for that observation from a documented provider convention and retain a traceable reference to that support.
2.2 If period evidence is absent or conflicting, the data service shall report the time basis as unknown or conflicting and preserve the conflicting supplied facts rather than silently choose a basis.
2.3 When returning filing, acceptance or restatement information, the data service shall retain the available source information and explicitly identify unavailable restatement or historical-vintage knowledge.
2.4 If historical availability cannot be established, the data service shall disclose that the observations are not verified as point-in-time safe; retrieval or filing time alone shall not establish that claim.

## Requirement 3: Preserve observations and consumer compatibility

**Objective:** Existing research remains usable while new consumers receive an honest input contract.

3.1 When enriching a response with period provenance, the data service shall preserve reported values, units, currencies, missing/null/zero distinctions and observation ordering, including duplicate fiscal labels.
3.2 When a consumer inspects period provenance, the data service shall make each item unambiguously attributable to its corresponding observation, including repeated period ends.
3.3 When serving the same query through supported Python and HTTP interfaces, the data service shall expose equivalent period provenance and disclose any required consumer-version migration before publication.

## Requirement 4: Establish bounded acceptance

**Objective:** Delivery proves the changed contract without expanding the verification framework.

4.1 When accepting this slice, QOpenBB shall verify annual and quarterly Income, Balance and Cash results for the established sample against retained source evidence, explicitly recording unsupported or contradictory period facts rather than declaring those inputs comparable.
4.2 When accepting this slice, QOpenBB shall demonstrate preservation of existing widget discovery and the affected statement rendering, query controls and save/reopen behavior through the existing native workflow.
4.3 When reporting completion, QOpenBB shall distinguish accepted provenance behavior from unresolved financial compatibility and shall leave IA-B analytical readiness open until its remaining criteria pass.

## Delivery constraints

Use the existing provider/core models, contract checks, native Compose/Playwright flow and per-task independent review. Design must identify the smallest affected files and compatibility consequences; task generation must carry the 400 physical / 300 logical / 50 function production caps. Avoid a parallel schema registry, a new verification framework or unrelated infrastructure changes. Documentation and review records are outside production caps.

No new financial calculations are specified, so no numerical valuation result is claimed. Corporate-finance guidance is applied to period, unit and evidence discipline. Subsequent modeling must separately define and validate formulas and adjustments.
