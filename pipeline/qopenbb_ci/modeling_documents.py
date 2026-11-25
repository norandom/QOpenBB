"""Provide the version 1 modeling contract payloads for bundle assembly."""

from http import HTTPStatus

from qopenbb_data.modeling.service.bootstrap import installed_methods
from qopenbb_data.modeling.service.widget_discovery import apps, widgets

from .modeling_documents_schemas import DIALECT, SCHEMAS, standalone_schemas

_COMPONENTS = "#/components/schemas/"


def documents() -> dict[str, dict | list]:
    """Return fresh, deterministic JSON payloads keyed by bundle-root filename."""
    schemas = standalone_schemas()
    registry, _ = installed_methods()
    return {
        "openapi.json": _openapi(schemas),
        **{f"{name}.schema.json": schema for name, schema in schemas.items()},
        "descriptors.json": {
            "models": [
                descriptor.model_dump(mode="json")
                for descriptor in registry.descriptors()
            ],
        },
        "widgets.json": widgets(),
        "apps.json": apps(),
    }


def _embed(node: object, component: str) -> object:
    if isinstance(node, list):
        return [_embed(item, component) for item in node]
    if isinstance(node, dict):
        return {
            key: _COMPONENTS + component + value[1:]
            if key == "$ref" and value.startswith("#/")
            else _embed(value, component)
            for key, value in node.items()
        }
    return node


def _json_content(schema: dict) -> dict:
    return {"application/json": {"schema": schema}}


def _ref(component: str) -> dict:
    return {"$ref": _COMPONENTS + component}


def _parameter(name: str, location: str, *, required: bool = True) -> dict:
    return {
        "name": name,
        "in": location,
        "required": required,
        "schema": {"type": "string", **({"minLength": 1} if required else {})},
    }


def _operation(
    operation_id: str, success: dict, *errors: int, **options: object
) -> dict:
    unauthorized = {
        "description": "Missing or invalid signed bridge identity",
        "headers": {
            "WWW-Authenticate": {"schema": {"type": "string", "const": "Bearer"}}
        },
        "content": _json_content(_ref("SafeError")),
    }
    return {
        "operationId": operation_id,
        "responses": {
            "200": {"description": "Success", "content": _json_content(success)},
            "401": unauthorized,
            **{
                str(code): {
                    "description": HTTPStatus(code).phrase,
                    "content": _json_content(_ref("SafeError")),
                }
                for code in errors
            },
        },
        **options,
    }


def _paths() -> dict:
    expected_run = _parameter("expected_run_id", "query", required=False)
    run_path = _parameter("run_id", "path")
    return {
        "/models": {"get": _operation("listModels", _ref("ModelListing"), 503)},
        "/widgets.json": {
            "get": _operation("discoverWidgets", _ref("WidgetDiscovery"), 503),
        },
        "/apps.json": {
            "get": _operation("discoverApps", _ref("AppDiscovery"), 503),
        },
        "/evaluations": {
            "post": _operation(
                "evaluateModel",
                _ref("ModelRun"),
                413,
                422,
                500,
                503,
                requestBody={
                    "required": True,
                    "content": _json_content(_ref("EvaluationRequest")),
                },
            ),
        },
        "/runs/{run_id}": {
            "get": _operation(
                "readSavedRun", _ref("ModelRun"), 404, 503, parameters=[run_path]
            ),
        },
        "/runs/{run_id}/outputs/{output_id}": {
            "get": _operation(
                "readSavedOutput",
                _ref("WidgetProjection"),
                404,
                503,
                parameters=[run_path, _parameter("output_id", "path"), expected_run],
            ),
        },
        "/widget-results": {
            "get": _operation(
                "readSavedWidgetOutput",
                _ref("WidgetProjection"),
                404,
                422,
                503,
                parameters=[
                    _parameter("run_id", "query"),
                    _parameter("output_id", "query"),
                    expected_run,
                ],
            ),
        },
    }


def _openapi(schemas: dict[str, dict]) -> dict:
    return {
        "openapi": "3.1.0",
        "info": {"title": "QOpenBB Internal Modeling API", "version": "1.0.0"},
        "servers": [{"url": "/modeling/v1"}],
        "jsonSchemaDialect": DIALECT,
        "paths": _paths(),
        "security": [{"ModelingIdentity": []}],
        "components": {
            "securitySchemes": {
                "ModelingIdentity": {
                    "type": "http",
                    "scheme": "bearer",
                    "bearerFormat": "JWT",
                    "description": "Short-lived identity assertion signed by the Workspace bridge.",
                },
            },
            "schemas": {
                model.__name__: _embed(schemas[name], model.__name__)
                for name, (model, _) in SCHEMAS.items()
            },
        },
    }
