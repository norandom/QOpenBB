"""Validate the service-owned projection without importing its runtime environment."""
import json
from copy import deepcopy

from jsonschema import Draft202012Validator, FormatChecker
from jsonschema.exceptions import SchemaError
from referencing import Registry
from referencing.exceptions import Unresolvable

EXTENSION = "x-qopenbb-financial"
LOCATION = "extra.results_metadata.__qopenbb_financial__"
PREFIX = "#/components/schemas/"


def resolve(document: dict, value: dict) -> dict:
    """Resolve local pointers only; catalogs never retrieve remote resources."""
    seen = set()
    while isinstance(value, dict) and "$ref" in value:
        ref = value["$ref"]
        if not isinstance(ref, str) or not ref.startswith("#/") or ref in seen:
            raise ValueError("Invalid local financial reference")
        seen.add(ref)
        try:
            target = document
            for part in ref[2:].split("/"):
                target = target[part.replace("~1", "/").replace("~0", "~")]
        except (KeyError, TypeError):
            raise ValueError("Unresolved financial reference") from None
        value = target
    if not isinstance(value, dict):
        raise ValueError("Financial reference requires an object")  # noqa: TRY004
    return value


def validate_value(document: dict, schema: dict, value: object) -> None:
    """Delegate JSON Schema semantics and format checks to the pinned validator."""
    try:
        json.dumps(value, allow_nan=False)
        Draft202012Validator.check_schema(schema)
        # Local refs retain their document context, even for nested combinators.
        root = {**document, "allOf": [schema]}
        validator = Draft202012Validator(root, registry=Registry(), format_checker=FormatChecker())
        if not validator.is_valid(value):
            raise ValueError("Invalid catalog example or default")
    except (ValueError, TypeError, SchemaError, Unresolvable):
        # Validator diagnostics contain user values and schema keys.
        raise ValueError("Invalid catalog example or schema") from None


def parameters(document: dict, operation: dict, path: dict) -> list[dict]:
    merged = {}
    for item in [*path.get("parameters", []), *operation.get("parameters", [])]:
        item = resolve(document, item)
        merged[(item["in"], item["name"])] = item
    return list(merged.values())


def _reference(document: dict, descriptor: dict, key: str) -> dict:
    value = descriptor.get(key)
    if not isinstance(value, dict) or set(value) != {"$ref"}:
        raise ValueError("Missing financial schema reference")
    if not isinstance(value["$ref"], str) or not value["$ref"].startswith(PREFIX):
        raise ValueError("Financial schema must reference a local component")
    target = resolve(document, value)
    _schema_contract(document, target, set())
    return target


def _schema_contract(document: dict, schema: object, seen: set) -> None:
    """Check declarations and defaults; instance semantics stay validator-owned."""
    if isinstance(schema, bool):
        return
    if not isinstance(schema, dict):
        raise ValueError("Invalid financial schema declaration")  # noqa: TRY004
    identity = id(schema)
    if identity in seen:
        return
    seen.add(identity)
    Draft202012Validator.check_schema(schema)
    if "nullable" in schema or schema.get("$schema", "https://json-schema.org/draft/2020-12/schema") != "https://json-schema.org/draft/2020-12/schema":
        raise ValueError("Unsupported financial schema dialect")
    if "default" in schema:
        validate_value(document, schema, schema["default"])
    if "$ref" in schema:
        _schema_contract(document, resolve(document, schema), seen)
    for key in ("properties", "patternProperties", "$defs", "dependentSchemas"):
        for child in schema.get(key, {}).values():
            _schema_contract(document, child, seen)
    for key in ("allOf", "anyOf", "oneOf", "prefixItems"):
        for child in schema.get(key, []):
            _schema_contract(document, child, seen)
    for key in ("items", "contains", "additionalProperties", "unevaluatedProperties", "unevaluatedItems", "not", "if", "then", "else", "propertyNames", "contentSchema"):
        if key in schema:
            _schema_contract(document, schema[key], seen)


def _fields(document: dict, variant: dict, metadata: dict) -> None:
    row = _reference(document, variant, "row_schema")
    fields = variant.get("fields")
    properties = row.get("properties", {})
    if not isinstance(fields, dict) or set(fields) != set(properties):
        raise ValueError("Financial fields differ from canonical row fields")
    if type(variant.get("dynamic_fields")) is not bool:
        raise ValueError("Missing dynamic financial field declaration")
    field_schema = metadata.get("properties", {}).get("fields")
    if not isinstance(field_schema, dict):
        raise TypeError("Missing financial metadata field schema")
    validate_value(document, field_schema, fields)
    for name, field in fields.items():
        if field.get("definition") != properties[name].get("description"):
            raise ValueError("Financial definition differs from canonical row description")
        for attribute in ("currency_field", "observation_date_field", "valuation_date_field", "publication_date_field"):
            if field.get(attribute) is not None and field[attribute] not in properties:
                raise ValueError("Financial field basis references an absent row field")


def _bounds(variant: dict, query: dict) -> None:
    bounds, policy = variant.get("procedural_bounds"), variant.get("response_policy")
    if not isinstance(bounds, dict) or not isinstance(policy, dict):
        raise TypeError("Missing financial query policies")
    properties = query.get("properties", {})
    required = set()
    for key in ("max_calendar_years", "max_symbols"):
        value = bounds.get(key)
        if value is not None and (type(value) is not int or value <= 0):
            raise ValueError("Invalid procedural bound")
    if bounds.get("max_calendar_years") is not None:
        required.update(("start_date", "end_date"))
    if bounds.get("max_symbols") is not None and not {"symbol", "symbols"}.intersection(properties):
        raise ValueError("Missing bounded symbol query parameter")
    mode, cap, limit = policy.get("mode"), policy.get("max_rows"), policy.get("limit_parameter")
    if mode not in {"clip", "provider", "income_compatibility"}:
        raise ValueError("Invalid response policy")
    if cap is not None and (type(cap) is not int or cap <= 0):
        raise ValueError("Invalid response row cap")
    if (int(cap is not None) + int(limit is not None)) != (1 if mode == "clip" else 0):
        raise ValueError("Inconsistent response row policy")
    if limit is not None:
        if not isinstance(limit, str):
            raise ValueError("Invalid limit parameter reference")
        required.add(limit)
    if not required.issubset(properties):
        raise ValueError("Financial policy references an absent query parameter")


def _runtime(document: dict, variant: dict, metadata: dict) -> None:
    paths = variant.get("runtime_properties")
    if not isinstance(paths, list) or any(not isinstance(path, str) for path in paths):
        raise ValueError("Invalid runtime financial declarations")
    if len(paths) != len(set(paths)):
        raise ValueError("Duplicate runtime financial declarations")
    for path in paths:
        parts = path.split(".")
        properties = metadata.get("properties", {})
        if not parts or parts[0] not in properties or len(parts) > 2:
            raise ValueError("Runtime declaration references absent metadata")
        if len(parts) == 2:
            nested = [resolve(document, properties[parts[0]])]
            if parts[0] == "fields":
                # Identifier-constrained maps project patternProperties; plain
                # string-keyed maps project additionalProperties instead.
                mapping = nested[0]
                candidates = list(mapping.get("patternProperties", {}).values())
                additional = mapping.get("additionalProperties")
                if isinstance(additional, dict):
                    candidates.append(additional)
                nested = [resolve(document, schema) for schema in candidates]
            if not nested or any(parts[1] not in schema.get("properties", {}) for schema in nested):
                raise ValueError("Runtime declaration references absent nested metadata")


def _provider(document: dict, descriptor: dict, params: list, selected: str) -> None:
    providers, variants = descriptor.get("providers"), descriptor.get("variants")
    if (not isinstance(providers, list) or not providers
            or any(not isinstance(item, str) or not item for item in providers)
            or len(set(providers)) != len(providers) or not isinstance(variants, dict)
            or set(providers) != set(variants) or selected not in variants):
        raise ValueError("Inconsistent financial provider associations")
    parameter = next((p for p in params if p.get("name") == "provider" and p.get("in") == "query"), None)
    if parameter is None:
        raise ValueError("Missing financial provider parameter")
    schema = resolve(document, parameter.get("schema", {}))
    if schema.get("enum") != providers:
        raise ValueError("Provider choices differ from financial variants")
    policy = descriptor.get("provider_policy")
    if policy == "explicit":
        if parameter.get("required") is not True or "default" in schema:
            raise ValueError("Explicit provider policy disagrees with parameter")
    elif policy == "baseline_default":
        if schema.get("default") not in providers:
            raise ValueError("Baseline provider default lacks an installed variant")
    else:
        raise ValueError("Invalid financial provider policy")


def validate_financial(document: dict, operation: dict, dataset: dict, params: list) -> None:
    if EXTENSION not in operation:
        return
    descriptor = operation[EXTENSION]
    try:
        if (not isinstance(descriptor, dict) or type(descriptor.get("schema_version")) is not int
                or descriptor["schema_version"] != 1 or not isinstance(descriptor.get("dataset"), str)
                or not descriptor["dataset"] or descriptor.get("metadata_location") != LOCATION):
            raise ValueError("Invalid financial descriptor identity")
        _provider(document, descriptor, params, dataset["provider"])
        metadata = _reference(document, descriptor, "metadata_schema")
        _reference(document, descriptor, "response_schema")
        _reference(document, descriptor, "error_schema")
        success = resolve(document, operation["responses"]["200"])
        if success["content"]["application/json"]["schema"] != descriptor["response_schema"]:
            raise ValueError("Financial response reference differs from served schema")
        for provider, variant in descriptor["variants"].items():
            query = _reference(document, variant, "query_schema")
            public = {item["name"] for item in params if item.get("in") == "query"}
            if not query.get("properties", {}).keys() <= public:
                raise ValueError("Financial query references an absent public parameter")
            _fields(document, variant, metadata)
            _bounds(variant, query)
            _runtime(document, variant, metadata)
            if provider == dataset["provider"]:
                values = {k: v for k, v in dataset["parameters"].items() if k != "provider"}
                if set(values) - query.get("properties", {}).keys():
                    raise ValueError("Example contains an unknown model query parameter")
                validate_value(document, variant["query_schema"], values)
    except (ValueError, TypeError, KeyError, AttributeError, SchemaError, Unresolvable):
        raise ValueError("Invalid projected financial contract") from None


def validate_parameters(document: dict, params: list, values: dict) -> None:
    """Validate example values and declared defaults without coercing HTTP types."""
    query = {item["name"]: item for item in params if item.get("in") == "query"}
    if set(values) - query.keys():
        raise ValueError("Unknown dataset query parameter")
    for name, parameter in query.items():
        if parameter.get("required") and name not in values:
            raise ValueError("Missing required dataset query parameter")
        schema = parameter.get("schema", {})
        try:
            _schema_contract(document, schema, set())
        except (SchemaError, ValueError, TypeError, Unresolvable):
            raise ValueError("Invalid catalog parameter schema") from None
        if name in values:
            validate_value(document, schema, values[name])


def frozen_extension(operation: dict) -> dict:
    return {EXTENSION: deepcopy(operation[EXTENSION])} if EXTENSION in operation else {}
