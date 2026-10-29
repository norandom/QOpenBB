# Authoritative financial annotations: prerequisite repair

2026-10-29. Status: design amendment owner-approved on 2026-10-29 after independent gpt-6-astra review. Existing requirements and numerical adapter acceptance remain intact. Task 4.1 is open because its source-declaration prerequisite was not implemented. This document does not approve new implementation tasks.

## Finding and consequence

The approved design requires runtime metadata and the API projection to use the same query/data declarations. Accepted adapters validate result metadata, but their static financial semantics still live in runtime helpers and module-level sets. Ordinary Pydantic field schemas do not expose the full units, provider-selection policy or procedural query/response limits.

For example, key-metrics units are assigned by `_fields` using category sets. Daily history enforces five calendar years in a validator and clips at a literal 5000. FRED names, units and effective frequencies depend on acquired series metadata. Copying these into `financial_openapi.py` would create a second owner of financial meaning.

Independent inspection confirmed that route/model association is already available: `route.openapi_extra['model']` identifies the standard model, and `RegistryMap.original_models` supplies installed provider query/data classes. There is no need for a new registry or generic query service.

## Minimal contract

Add one typed, declaration-only core module: `openbb_platform/core/openbb_core/provider/standard_models/financial_annotations.py` in the owned data fork. Leave `financial_metadata.py` responsible for actual result metadata.

Provider query/data classes attach validated declarations through typed `ClassVar` attributes:

| Declaration | Owns | Must derive elsewhere |
| --- | --- | --- |
| Query annotation | Explicit-provider requirement, procedural bounds, response-cap policy and runtime-resolved properties | Actual field defaults, enums, requiredness and numeric constraints from the query model; provider choices from installed registry |
| Data annotation | Field templates keyed by actual serialized fields, runtime-resolved properties and dynamic-column declaration | Financial definitions already in Field descriptions; actual availability, dates and observed values from results |

Reuse `FinancialFieldMetadata` for static field templates rather than creating another unit/type vocabulary. Validate references against the owning model's actual fields and distinguish declared unknowns from absent annotations. Do not infer missing semantics from field names, docstrings, widgets or function bodies.

Move existing static unit/category templates into the class declarations and make runtime helpers consume them. Runtime rendering copies templates and never mutates shared class declarations across requests. Remove displaced copies. Procedural limits become single declared constants read by both validation/clipping and projection. This is a source-of-truth repair, not a new financial calculation.

Provider policy must agree across installed variants of an operation before publication. Preserve existing baseline defaults and read actual defaults from installed schemas; do not introduce another handwritten default-provider table. New-operation explicit-provider requirements feed both projection and the later request guard.

## Preserve runtime meaning

Actual receipt timestamps, availability, returned counts, observed truncation and completeness remain runtime-owned. Fiscal-period inference remains runtime-owned. Static annotations disclose the property and metadata location, not a fabricated value.

FRED dynamic columns, source/effective units, seasonal adjustment, transforms and vintages cannot be enumerated as fixed fields. Declare their runtime resolution through `extra.results_metadata.__qopenbb_financial__`; preserve existing per-series legacy metadata. Do not move transform mappings merely for architectural symmetry.

Income's accepted limit-zero and excess-response behavior is a compatibility policy, not an ordinary fixed response cap. The annotation must describe that behavior without changing it. Existing profile multi-symbol behavior, statement aliases, typed errors and cache freshness remain unchanged.

## Bounded implementation sequence after approval

These are repair slices for task-plan generation, not newly approved executable tasks. Every production slice keeps the existing 400 physical / 300 logical / 50 per function caps and requires independent review plus affected checks.

| Slice | Exclusive ownership | Done evidence |
| --- | --- | --- |
| A: freeze the annotation types | New core `financial_annotations.py`, focused contract tests | Validated serialization, model-field references and static/runtime distinction; no I/O dependencies |
| B: representative adoption | FMP key-metrics model/data and daily-history model | Existing result metadata preserved; runtime/projection share declarations; five-year/5000 behavior unchanged |
| C: projection after A | Root `services/data-api/qopenbb_data/financial_openapi.py` and its focused tests | Deterministic namespaced references, real route/registry associations, actual aliases, safe response/metadata schemas, including referenced error components where applicable, and explicit missing-annotation failure |
| D1: statements | Income, balance-sheet and cash-flow modules/companions | Existing bounds, period/sign/null and baseline compatibility fixtures retained; declarations match runtime metadata |
| D2: identity and peers | Profile, search, peers and their declaration companion | Identity ambiguity, currency/share, source dates and provider policy retained |
| D3: remaining inputs | Ratios and enterprise-value modules | Fraction/percentage, per-share and valuation-date conventions preserved |
| D4: economic series | FRED generic-series declaration and runtime metadata helper | Dynamic fields/units remain runtime-resolved; existing wide rows and timestamp/vintage checks preserved |
| E: controller join | Inventory, exact fork/source pins, breadth and projection acceptance | First-batch declarations present and resolvable; one authoritative projection used for runtime and generation |

C can run alongside source adoption once A is frozen. Full task 4.1 acceptance requires adopted real models, including static FMP and dynamic FRED cases. Fixture-only projection does not close the source-of-truth gap. Installed integration must reject missing required annotations instead of advertising incomplete semantics.

Enterprise task 2.9 finishes in its existing exclusive ownership first. Its annotation adoption then belongs to D3; no concurrent writer is introduced. Existing unrelated catalog renderer changes remain outside this repair.

## Review and next decision

The independent architecture review confirmed this prerequisite gap and the sequence above without requesting a new registry or a broad provider rewrite. No production code or tests were added for the blocked projection. The existing 26-task batch count remains unchanged; task 4.1 stays unchecked. The [11-unit repair plan](financial-annotations-tasks.md) passed independent graph review. Owner task approval is required before implementation.
