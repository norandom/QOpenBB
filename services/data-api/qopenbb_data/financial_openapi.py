"""Project class-owned financial declarations without changing native execution."""

from collections.abc import Iterable
from copy import deepcopy

from openbb_core.provider.registry_map import RegistryMap
from openbb_core.provider.standard_models.financial_annotations import (
    FINANCIAL_METADATA_LOCATION,
    InvalidFinancialAnnotation,
    bind_data_annotation,
    bind_query_annotation,
    render_field_templates,
)
from openbb_core.provider.standard_models.financial_metadata import (
    FinancialResultMetadata,
)
from openbb_core.provider.utils.financial_errors import FinancialErrorCode
from pydantic import BaseModel

EXTENSION = "x-qopenbb-financial"
PREFIX = "#/components/schemas/"


def _name(*parts: str) -> str:
    return "QOpenBBFinancial_" + "_".join(part.encode().hex() for part in parts)


def _put(schemas: dict, name: str, value: dict) -> dict:
    if name in schemas and schemas[name] != value:
        raise InvalidFinancialAnnotation(f"Financial schema collision: {name}")
    schemas[name] = value
    return {"$ref": PREFIX + name}


def _rewrite(value, definitions: dict):
    if isinstance(value, list):
        return [_rewrite(item, definitions) for item in value]
    if not isinstance(value, dict):
        return value
    result = {}
    for key, item in value.items():
        if key == "$ref" and isinstance(item, str) and item.startswith("#/$defs/"):
            target = item.removeprefix("#/$defs/")
            if target not in definitions:
                raise InvalidFinancialAnnotation("Unresolved model definition reference")
            result[key] = PREFIX + definitions[target]
        else:
            result[key] = _rewrite(item, definitions)
    return result


def _model_schema(model, schemas: dict, *namespace: str, mode="serialization", by_alias=False) -> dict:
    schema = model.model_json_schema(by_alias=by_alias, mode=mode)
    definitions = schema.pop("$defs", {})
    names = {key: _name(*namespace, key) for key in definitions}
    for key, definition in sorted(definitions.items()):
        _put(schemas, names[key], _rewrite(definition, names))
    return _put(schemas, _name(*namespace), _rewrite(schema, names))


def _query_schema(query, annotation, schemas: dict, dataset: str, provider: str) -> dict:
    reference = _model_schema(query, schemas, dataset, provider, "query",
                              mode="validation", by_alias=True)
    properties = schemas[reference["$ref"].removeprefix(PREFIX)].get("properties", {})
    required = set()
    if annotation.response_policy.limit_parameter:
        required.add(annotation.response_policy.limit_parameter)
    if annotation.procedural_bounds.max_calendar_years is not None:
        required.update(("start_date", "end_date"))
    if annotation.procedural_bounds.max_symbols is not None:
        required.add("symbol" if "symbol" in query.model_fields else "symbols")
    if not required.issubset(properties):
        raise InvalidFinancialAnnotation("Declared query bound lacks a public parameter reference")
    return reference


def _variant(dataset: str, provider: str, models: dict, schemas: dict) -> tuple:
    try:
        query, data = models["query"], models["data"]
    except (KeyError, TypeError) as exc:
        raise InvalidFinancialAnnotation("Registry variant lacks query/data classes") from exc
    query_annotation = bind_query_annotation(query)
    data_annotation = bind_data_annotation(data)
    fields = render_field_templates(data)
    descriptor = {
        "query_schema": _query_schema(query, query_annotation, schemas, dataset, provider),
        "row_schema": _model_schema(data, schemas, dataset, provider, "row"),
        "fields": {name: value.model_dump(mode="json") for name, value in sorted(fields.items())},
        "dynamic_fields": data_annotation.dynamic_fields,
        "runtime_properties": sorted(set(data_annotation.runtime_properties)
                                     | set(query_annotation.runtime_properties)),
        "procedural_bounds": query_annotation.procedural_bounds.model_dump(mode="json"),
        "response_policy": query_annotation.response_policy.model_dump(mode="json"),
    }
    return query_annotation.provider_policy, descriptor


def _resolve(document: dict, value: dict) -> dict:
    if "$ref" not in value:
        return value
    ref = value["$ref"]
    if not ref.startswith("#/"):
        raise InvalidFinancialAnnotation("Financial projection requires local parameter references")
    target = document
    try:
        for part in ref[2:].split("/"):
            target = target[part.replace("~1", "/").replace("~0", "~")]
    except (KeyError, TypeError) as exc:
        raise InvalidFinancialAnnotation("Unresolved OpenAPI reference") from exc
    return deepcopy(target)


def _provider_parameter(document: dict, operation: dict, path_item: dict,
                        policy: str, providers: list[str]) -> None:
    parameters = [_resolve(document, item) for item in operation.get("parameters", [])]
    inherited = [_resolve(document, item) for item in path_item.get("parameters", [])]
    provider = next((item for item in parameters if item.get("name") == "provider"
                     and item.get("in") == "query"), None)
    if provider is None:
        provider = next((deepcopy(item) for item in inherited if item.get("name") == "provider"
                         and item.get("in") == "query"), None)
        if provider is not None:
            parameters.append(provider)
    if provider is None:
        raise InvalidFinancialAnnotation("Financial operation lacks provider parameter")
    schema = _resolve(document, provider.get("schema", {}))
    schema["enum"] = providers
    if policy == "explicit":
        provider["required"] = True
        schema.pop("default", None)
    elif "default" in schema and schema["default"] not in providers:
        raise InvalidFinancialAnnotation("Provider default is absent from registry variants")
    provider["schema"] = schema
    operation["parameters"] = parameters


def _response(operation: dict, schemas: dict, dataset: str, metadata: dict,
              response_model=None) -> dict:
    response = operation.get("responses", {}).get("200", {})
    media = response.get("content", {}).get("application/json")
    if media is None or "schema" not in media:
        raise InvalidFinancialAnnotation("Financial operation lacks JSON success schema")
    base = deepcopy(media["schema"])
    if response_model is not None:
        if not isinstance(response_model, type) or not issubclass(response_model, BaseModel):
            raise InvalidFinancialAnnotation("Financial operation requires a supported response model")
        # Native OpenAPI aliases can differ from the route's canonical output.
        base = _model_schema(response_model, schemas, dataset, "native_response")
    name = _name(dataset, "response")
    reference = {"$ref": PREFIX + name}
    if media["schema"] == reference:
        if name not in schemas:
            raise InvalidFinancialAnnotation("Missing projected response component")
        if response_model is None:
            return reference
    overlay = {"type": "object", "properties": {"extra": {
        "type": "object", "properties": {"results_metadata": {
            "type": "object", "properties": {"__qopenbb_financial__": metadata}
        }}
    }}}
    reference = _put(schemas, name, {"allOf": [base, overlay]})
    media["schema"] = reference
    return reference


def _error_schema(schemas: dict) -> dict:
    return _put(schemas, _name("error"), {
        "type": "object", "description": "Public financial error contract; handler installation is separate.",
        "required": ["detail", "code", "provider", "retryable"],
        "properties": {
            "detail": {"type": "string"},
            "code": {"type": "string", "enum": [code.value for code in FinancialErrorCode]},
            "provider": {"type": ["string", "null"]},
            "retryable": {"type": "boolean"},
            "retry_after_seconds": {"type": "integer", "minimum": 0},
            "correlation_id": {"type": "string"},
        },
    })


def _operation(document: dict, operation: dict, path_item: dict, dataset: str,
               variants: dict, schemas: dict, metadata: dict, error: dict,
               response_model=None) -> None:
    descriptors, policies = {}, set()
    for provider, models in sorted(variants.items()):
        policy, descriptors[provider] = _variant(dataset, provider, models, schemas)
        policies.add(policy)
    if len(policies) != 1:
        raise InvalidFinancialAnnotation("Provider policy disagreement or empty variants")
    policy = policies.pop()
    _provider_parameter(document, operation, path_item, policy, sorted(variants))
    operation[EXTENSION] = {
        "schema_version": 1, "dataset": dataset, "providers": sorted(variants),
        "provider_policy": policy, "variants": descriptors,
        "metadata_location": FINANCIAL_METADATA_LOCATION, "metadata_schema": metadata,
        "metadata_enforcement": "Fetcher validation; unrestricted extra alone does not enforce this schema.",
        "response_schema": _response(operation, schemas, dataset, metadata, response_model),
        "error_schema": error,
    }


def project_financial_openapi(document: dict, routes: Iterable, registry_map: RegistryMap,
                              *, required_models: set[str]) -> dict:
    """Return an additive copy for explicitly advertised installed model associations.

    This function documents contracts only. Provider guards, error handlers and
    validation of actual serialized results belong to their runtime owners.
    """
    result = deepcopy(document)
    if not required_models:
        return result
    schemas = result.setdefault("components", {}).setdefault("schemas", {})
    metadata = _model_schema(FinancialResultMetadata, schemas, "metadata")
    error = _error_schema(schemas)
    found = set()
    for route in routes:
        dataset = (getattr(route, "openapi_extra", None) or {}).get("model")
        if dataset not in required_models:
            continue
        if getattr(route, "response_model_by_alias", None) is not False:
            raise InvalidFinancialAnnotation("Unsupported or missing response_model_by_alias; expected False")
        variants = registry_map.original_models.get(dataset)
        if not variants:
            raise InvalidFinancialAnnotation("Required model has no installed variants")
        path_item = result.get("paths", {}).get(route.path, {})
        methods = sorted(method.lower() for method in route.methods or ())
        for method in methods:
            operation = path_item.get(method)
            if operation is None:
                raise InvalidFinancialAnnotation("Required route lacks OpenAPI operation")
            _operation(result, operation, path_item, dataset, variants, schemas, metadata, error,
                       getattr(route, "response_model", None))
            found.add(dataset)
    if found != required_models:
        raise InvalidFinancialAnnotation("Required model lacks route association")
    return result


def financial_error_responses(document: dict) -> dict:
    """Bind response references when the corresponding handlers are installed.

    A standalone projection preserves native response definitions; activation
    describes the safe envelopes that the installed service actually returns.
    """
    result = deepcopy(document)
    for path_item in result.get("paths", {}).values():
        for operation in path_item.values():
            if not isinstance(operation, dict) or EXTENSION not in operation:
                continue
            error = operation[EXTENSION]["error_schema"]
            for status in ("400", "422", "500", "502"):
                operation["responses"][status] = {
                    "description": "Financial request or provider failure; inspect the code field.",
                    "content": {"application/json": {"schema": error}},
                }
            operation["responses"]["204"] = {"description": "No provider observations available."}
    return result
