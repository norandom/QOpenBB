"""Validate exercised wire bodies against offline bundle schemas."""

from functools import cache
from re import error as RegexError

from jsonschema import Draft202012Validator, FormatChecker
from jsonschema.exceptions import SchemaError
from referencing import Registry
from referencing.exceptions import Unresolvable

_RUN = ("get", "/runs/{run_id}", "model-run")
_WIDGET = ("get", "/widget-results", "widget-projection")
_OPERATIONS = {
    "evaluation": ("post", "/evaluations", "model-run"),
    "run": _RUN,
    "widget": _WIDGET,
    "blocked_widget": _WIDGET,
}
_DIALECT = "https://json-schema.org/draft/2020-12/schema"
_SCHEMA_ERRORS = (
    AttributeError,
    KeyError,
    TypeError,
    ValueError,
    SchemaError,
    Unresolvable,
    RecursionError,
    RegexError,
)


def response_checker(bundle: dict):
    """Reuse checked schemas for the cases that exercise the same endpoint."""

    @cache
    def openapi():
        api = bundle["openapi.json"]
        if api["openapi"] != "3.1.0" or api["jsonSchemaDialect"] != _DIALECT:
            raise ValueError("unsupported OpenAPI schema dialect")
        components = api["components"]
        for component in components["schemas"].values():
            Draft202012Validator.check_schema(component)
        root = {"components": components}
        _check_local_refs(root, root, "#/components/schemas/")
        return api

    @cache
    def validators(operation: str, status: int):
        try:
            method, path, name = _OPERATIONS[operation]
            api = openapi()
            response = api["paths"][path][method]["responses"][str(status)]
            inline = response["content"]["application/json"]["schema"]
            standalone = bundle[
                f"{name if status == 200 else 'safe-error'}.schema.json"
            ]
            if not isinstance(inline, dict) or not inline:
                return None
            if (
                not isinstance(standalone, dict)
                or standalone.get("$schema") != _DIALECT
            ):
                return None
            embedded = inline | {"components": api["components"]}
            _check_local_refs(standalone, standalone, "#/$defs/")
            _check_local_refs(inline, embedded, "#/components/schemas/")
            return tuple(_validator(schema) for schema in (standalone, embedded))
        except _SCHEMA_ERRORS:
            return None

    def valid(operation: str, status: int, body: dict) -> bool:
        schemas = validators(
            "widget" if operation == "blocked_widget" else operation, status
        )
        try:
            return schemas is not None and all(
                schema.is_valid(body) for schema in schemas
            )
        except _SCHEMA_ERRORS:
            return False

    return valid


def _validator(schema: dict) -> Draft202012Validator:
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(
        schema, registry=Registry(), format_checker=FormatChecker()
    )


def _check_local_refs(node: object, root: dict, prefix: str) -> None:
    if isinstance(node, list):
        for item in node:
            _check_local_refs(item, root, prefix)
    if isinstance(node, dict):
        if (
            node.keys() & {"$dynamicRef", "$recursiveRef", "$id"}
            or node.get("$schema", _DIALECT) != _DIALECT
        ):
            raise ValueError("unsupported schema reference scope")
        if "$ref" in node:
            reference = node["$ref"]
            if not isinstance(reference, str) or not reference.startswith(prefix):
                raise ValueError("unsupported schema reference")
            target = root
            for segment in reference[2:].split("/"):
                target = target[segment.replace("~1", "/").replace("~0", "~")]
            if not isinstance(target, (dict, bool)):
                raise ValueError("invalid schema reference target")
        for value in node.values():
            _check_local_refs(value, root, prefix)
