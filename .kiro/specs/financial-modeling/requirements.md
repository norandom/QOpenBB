# Financial modeling foundation requirements

## Introduction

Financial engineers need independently extensible house calculations whose validity can be inspected and whose API contracts remain compatible with widgets and later consumers. The current deliverable is a specification stub; all runtime capabilities below remain unimplemented.

## Boundary context

- In scope: independently maintained model extensions, supplied-input execution, executable financial validation, reproducible evidence, consumer compatibility and agent-first extension discipline.
- Adjacent: market-data-integrations supplies provider observations and provenance; analyst-workspace owns widget bindings, display and linked research state. Each side owns its contract obligations.
- Out of scope for this foundation: implementing broad FMP acquisition, DCF or forecast formulas, new chart renderers, EconDB integration, AI/Excel execution, arbitrary untrusted plugins and a general-purpose rules language.
- Owner constraints: separate Git repository for modeling, FMP coverage before model implementation, and eventual three historical / five forecast years. Detailed method choices require their own specs. Proposed packaging and contract technology belong in the repository blueprint.

## Requirements

### Requirement 1: Independent and discoverable model extensions

**Objective:** As a financial engineer, I want to extend house methods without changing provider acquisition or widget calculations.

1.1 When supplied with a compatible input snapshot and explicit assumptions, the modeling system shall evaluate a supported method without requiring a live provider or Workspace session.
1.2 When a consumer discovers an installed model, the modeling system shall expose its identity, method version, supported input/output contract versions, required assumptions, financial scope and validation rules.
1.3 If an input or method version is unsupported, the modeling system shall reject it with an actionable compatibility failure rather than substitute another method.
1.4 When an extension is added, the delivery workflow shall verify that existing supported model and consumer contracts remain compatible or require an explicit versioned migration before publication.

### Requirement 2: Executable financial contracts

**Objective:** As an analyst, I want checks to enforce financial meaning before and after calculation.

2.1 When a calculation is requested, the modeling system shall evaluate the selected method's declared preconditions, including required inputs and applicable units, currency, periods, completeness and sign conventions, before executing the calculation.
2.2 When evaluating a supported model, the modeling system shall evaluate its declared cross-field invariants and output postconditions, including applicable reconciliations, domain constraints and independently verified numerical comparisons.
2.3 When a validation rule executes, the modeling system shall return its stable rule identity/version, applicable input/output references, observed and expected condition, tolerance where applicable, severity, outcome and explanation.
2.4 If required evidence is absent or a check does not execute successfully, the modeling system shall record an unknown or error outcome and shall not count it as a pass. A not-applicable outcome shall require an explicit applicability decision and reason.
2.5 If a blocking precondition, invariant or postcondition fails, the modeling system shall withhold dependent calculated conclusions and identify the affected outputs; independently valid outputs and original observations may remain accessible with their own status.
2.6 Where a house-policy rule permits an exception, the modeling system shall preserve the failed check and record the override's author, reason, scope and policy version separately. Mathematical invalidity and unresolved numerical mismatches shall not be overridable into verified results.
2.7 When a rule compares numerical values, the modeling system shall use the rule's declared units, scale and absolute or relative tolerance and shall retain the unrounded comparison evidence separately from display rounding.

### Requirement 3: Reproducible financial evidence

**Objective:** As a reviewer, I want to reproduce a model conclusion and understand its unresolved limitations.

3.1 The modeling system shall expose for each material calculated output its source inputs, formula and method version, assumptions, substitutions, intermediate values, units, financial period and validation results.
3.2 When a material result is submitted for verified status, the verification workflow shall independently recalculate it before assigning that status, using a separately expressed reference calculation and record the compared values, tolerance and mismatch status. Reinvoking the same production calculation shall not satisfy independence.
3.3 If independent verification is incomplete or mismatched, the modeling system shall withhold the result or explicitly identify it as an unverified estimate or open item, rather than present it as an established conclusion.
3.4 When saving a run, the modeling system shall retain immutable identities for its input snapshot, source provenance, assumption set, model version, rule set and verification evidence.
3.5 When inputs, assumptions, formulas or validation policy change, the modeling system shall create a new run identity and invalidate inherited verification claims for affected results rather than reuse their former pass status.

3.6 The modeling system and its consumers shall distinguish historical reported inputs, provider-calculated values, analyst adjustments, estimates and locally modeled outputs throughout saved runs and their presentation.

### Requirement 4: Widget and API compatibility

**Objective:** As a consumer developer, I want to detect incompatible changes before they reach an analyst's dashboard.

4.1 The integration contract shall identify, for each maintained widget integration, its API operation/version, parameter bindings, response location, required field types and nullability, supported result states and financial semantics.
4.2 When an API or consumer contract changes, the delivery workflow shall validate affected widget expectations against the supported API contract and exercised responses, including relevant missing-data, validation-failure and partial-result cases.
4.3 If a response remains structurally valid but changes a required unit, scale, currency basis, period basis or validation meaning, the compatibility gate shall treat that change as a semantic contract change requiring explicit consumer acceptance or migration.
4.4 When publishing a breaking change, the delivery workflow shall identify affected consumers and provide a versioned migration or retain the previously supported contract; saved dashboards shall not silently bind to an incompatible replacement.
4.5 When displaying model outputs, the consumer shall preserve their verification and failure states and provide access to relevant check explanations; it shall not convert missing or withheld values to zero or present stale results as a successful fresh calculation.

### Requirement 5: Horizontal breadth and change evidence

**Objective:** As a maintainer, I want each change to identify the requirements, financial rules and consumers it can affect.

5.1 The delivery workflow shall map each delivered capability to its owning criteria, method/rule identities, API contract, consumer bindings, actual tests and revision-specific evidence across repositories.
5.2 When a maintained contract, rule, model or widget changes, the delivery workflow shall identify affected mappings and run their applicable contract, financial and integration checks. If the impact cannot be resolved, the workflow shall report that gap and require a broader relevant verification set before acceptance.
5.3 If a required check is absent, skipped or unevaluated, the breadth record shall retain the capability as unverified or incomplete rather than infer a pass from schema generation or catalog presence.
5.4 When accepting an integrated release, the delivery workflow shall record the exact participating source and contract versions and image identities where images are involved, without requiring unrelated stable components to be rebuilt.

### Requirement 6: Governed extension and future providers

**Objective:** As an agent-assisted maintainer, I want additions to follow the same financial and engineering rules.

6.1 When a model extension is proposed for implementation, the extension workflow shall record approved requirements, design and bounded tasks with financial definitions, input assumptions, validation rules, consumer impacts and explicit exclusions.
6.2 When an extension is submitted for acceptance, the extension workflow shall require an independent review of financial logic and contracts and fresh evidence for its affected checks, including failure behavior.
6.3 When a new provider supplies inputs to an existing model, the integration shall validate the model's financial input contract and retain provider provenance rather than infer equivalence from matching names or types.
6.4 Where economic series are used, the integration shall preserve their frequency, seasonal-adjustment status, units, observation and release/vintage information where supplied, and shall disclose unknowns and explicit transformations rather than silently align or interpolate them.
6.5 While the modeling service is unavailable, the Workspace integration shall keep independent provider-data views usable and identify unavailable model results separately.
