# Financial annotation interface

Task 1 declares financial semantics on the provider query/data classes. Adoption and projection use `bind_query_annotation(Model)` and `bind_data_annotation(Model)`; missing declarations raise `MissingFinancialAnnotation`, malformed declarations or unknown serialized references raise `InvalidFinancialAnnotation`. No inference from names or provider imports is performed.

## Class attributes

Use `financial_query_annotation: ClassVar[FinancialQueryAnnotation]` and `financial_data_annotation: ClassVar[FinancialDataAnnotation]`. The exported attribute constants name those members. `FINANCIAL_METADATA_LOCATION` is `extra.results_metadata.__qopenbb_financial__`.

`provider_policy` is `explicit` or `baseline_default`. The installed query schema remains authoritative for defaults, enum choices, requiredness and ordinary constraints. The annotation contains no provider name/default table.

`procedural_bounds` exposes optional positive strict integers `max_calendar_years` and `max_symbols`. Calendar bounds require modeled start/end dates; symbol bounds require symbol/symbols. Runtime validators consume the same instance constants. `ResponsePolicy` modes are `clip`, `provider`, and `income_compatibility`. Clipping uses exactly one fixed `max_rows` or numeric query `limit_parameter`; other modes claim neither cap. Income compatibility retains the accepted zero-limit and excess-row behavior.

Daily history example: `ProceduralBounds(max_calendar_years=5)` and `ResponsePolicy(mode="clip", max_rows=5000)`. A limit-clipped statement uses `ResponsePolicy(mode="clip", limit_parameter="limit")`, deriving its default and bounds from the modeled limit field.

## Templates and runtime properties

`FinancialDataAnnotation.fields` maps serialized output names to `FinancialFieldTemplate`, a subclass of existing `FinancialFieldMetadata` with an optional definition. `render_field_templates(Model)` obtains each definition from that model's `Field.description` and returns fresh `FinancialFieldMetadata` objects. An explicitly repeated definition must match. Templates and their currency/date references use `serialization_alias`, then `alias`, then the Python name; excluded fields are not valid references. Every emitted static field needs a template; an empty template explicitly declares unknown semantics while inheriting the definition. Dynamic fields cover additional runtime columns, never missing static templates. No field metadata vocabulary is duplicated.

For a key-metrics field described as `Field(description="Provider return on equity")`, use `FinancialFieldTemplate(unit="fraction", scale=1, value_origin="provider_calculation")`. Rendering supplies the definition. The adapter supplies actual availability, period, provenance and result observations afterward. Nested financial-basis dictionaries are independent across renders and bindings.

`runtime_properties` lists potential runtime resolution under the common metadata object. Roots must be real `FinancialResultMetadata` properties; optional second segments are real field metadata or bounds properties, e.g. `fields.availability`, `fields.period_basis`, `bounds.truncated`. These are disclosures, never instructions to erase known static template values, and do not assert that every field has the property resolved. Unknown values remain `None` or `unknown`; absent declarations are errors.

FRED can declare `FinancialDataAnnotation(dynamic_fields=True, runtime_properties=["fields", "observation_provenance", "retrieved_at", "bounds"])`. This permits actual series columns/units/frequencies to remain runtime-owned. It does not enumerate series or manufacture dates, transforms, availability or units. Receipt timestamps, returned counts, actual truncation, completeness and fiscal inference remain runtime-owned for all providers.

Bindings return validated deep copies. Adapters may enrich rendered copies with runtime values; they must not mutate class declarations. Annotations do not fetch, register routes or replace result metadata validation.
