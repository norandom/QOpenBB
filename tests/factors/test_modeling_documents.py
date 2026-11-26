import json

import pytest
from jsonschema import Draft202012Validator
from qopenbb_ci.modeling_documents import documents
from qopenbb_data.modeling.contracts.results import ModelRun
from qopenbb_data.modeling.service.evaluation import EvaluationRequest
from qopenbb_data.modeling.service.http import create_model_app
from qopenbb_data.modeling.service.http_errors import failure
from qopenbb_data.modeling.service.widget_discovery import apps, widgets
from qopenbb_data.modeling.service.widget_projection import project_output
from test_model_run_evidence import run_fields as run_fields_fixture

run_fields = run_fields_fixture


@pytest.fixture(scope="module")
def bundle():
    return documents()


def validate(schema, payload):
    Draft202012Validator(
        schema, format_checker=Draft202012Validator.FORMAT_CHECKER
    ).validate(payload)


def test_payloads_are_reproducible_and_schema_documents_use_draft_2020_12(bundle):
    assert json.dumps(bundle, allow_nan=False) == json.dumps(
        documents(), allow_nan=False
    )
    assert bundle["widgets.json"] == widgets()
    assert bundle["apps.json"] == apps()
    assert {model["model_id"] for model in bundle["descriptors.json"]["models"]} == {
        "etf_momentum", "etf_realized_volatility", "real_yield_regime",
        "issuer_fcf_yield", "proxy_comparison", "timing_study",
    }
    for name, schema in bundle.items():
        if name.endswith(".schema.json"):
            assert schema["$schema"] == Draft202012Validator.META_SCHEMA["$id"]
            Draft202012Validator.check_schema(schema)


def test_openapi_covers_internal_routes_and_safe_errors(bundle):
    api = bundle["openapi.json"]
    assert api["openapi"].startswith("3.1.")
    assert api["servers"] == [{"url": "/modeling/v1"}]
    assert api["jsonSchemaDialect"] == Draft202012Validator.META_SCHEMA["$id"]
    assert api["security"] == [{"ModelingIdentity": []}]
    app = create_model_app(None, None, None)
    assert {
        (path, method.upper()) for path, ops in api["paths"].items() for method in ops
    } == {(route.path, method) for route in app.routes for method in route.methods}
    ids = [op["operationId"] for ops in api["paths"].values() for op in ops.values()]
    assert len(ids) == len(set(ids))
    widget = api["paths"]["/widget-results"]["get"]
    assert widget["operationId"] == "readSavedWidgetOutput"
    assert {p["name"]: p["required"] for p in widget["parameters"]} == {
        "run_id": True,
        "output_id": True,
        "expected_run_id": False,
    }
    for status, response in widget["responses"].items():
        if status != "200":
            schema = response["content"]["application/json"]["schema"]
            assert schema["$ref"] == "#/components/schemas/SafeError"
    schema = bundle["safe-error.schema.json"]
    validate(schema, json.loads(failure(401, "unauthorized").body))
    validate(
        schema,
        json.loads(failure(503, "publication_unconfirmed", run_id="opaque").body),
    )
    assert not Draft202012Validator(schema).is_valid({"detail": "raw exception"})


@pytest.mark.parametrize(
    "kind,value",
    [
        ("decimal", "0.1"),
        ("integer", 2**63 - 1),
        ("boolean", False),
        ("date", "2024-01-02"),
        ("text", "001"),
        ("decimal", "9" * 38),
        ("decimal", "0." + "0" * 37 + "1"),
        ("decimal", "-" + "9" * 37 + ".1"),
    ],
)
def test_saved_run_and_projection_match_embedded_and_standalone_schemas(
    bundle, run_fields, kind, value
):
    run_fields["descriptor"]["outputs"][0]["value_type"] = kind
    run_fields["outputs"][0].update(value=value, value_type=kind)
    run = ModelRun.model_validate(run_fields)
    api = bundle["openapi.json"]
    for path, name, payload in [
        ("/runs/{run_id}", "model-run", run.model_dump(mode="json")),
        ("/widget-results", "widget-projection", project_output(run, "price")),
    ]:
        validate(bundle[f"{name}.schema.json"], payload)
        schema = api["paths"][path]["get"]["responses"]["200"]["content"][
            "application/json"
        ]["schema"]
        validate(api | schema, payload)


def test_request_rejects_wrong_wire_scalar_types_and_has_one_input_source(
    bundle, run_fields
):
    request = {
        "model_id": "factor",
        "method_version": "1",
        "assumptions": {
            "version": "1",
            "effective_date": "2024-01-02",
            "assumptions": [
                {
                    "assumption_id": "threshold",
                    "value_type": "decimal",
                    "value": "-10.100",
                    "origin": "method_default",
                    "rationale": "Example",
                }
            ],
        },
        "inputs": ModelRun.model_validate(run_fields).inputs.model_dump(mode="json"),
    }
    schema = bundle["evaluation-request.schema.json"]
    EvaluationRequest.model_validate_json(json.dumps(request))
    validate(schema, request)
    api = bundle["openapi.json"]
    embedded = api["paths"]["/evaluations"]["post"]["requestBody"]["content"][
        "application/json"
    ]["schema"]
    validate(api | embedded, request)
    validator = Draft202012Validator(schema)
    assert not validator.is_valid(request | {"inputs": None})
    assumption = request["assumptions"]["assumptions"][0]
    for invalid in (0.1, "1e-1", True, 1):
        assumption["value"] = invalid
        assert not validator.is_valid(request)


def test_every_openapi_schema_reference_resolves(bundle):
    api = bundle["openapi.json"]

    def visit(node):
        if isinstance(node, list):
            for item in node:
                visit(item)
        elif isinstance(node, dict):
            if "$ref" in node:
                ref = node["$ref"]
                assert ref.startswith("#/")
                target = api
                for token in ref[2:].split("/"):
                    target = target[token.replace("~1", "/").replace("~0", "~")]
                assert isinstance(target, dict)
            for item in node.values():
                visit(item)

    visit(api)
    for schema in api["components"]["schemas"].values():
        Draft202012Validator.check_schema(schema)


@pytest.mark.parametrize(
    "kind,invalid",
    [
        ("decimal", "-0"),
        ("decimal", "1.00"),
        ("decimal", "1\n"),
        ("decimal", "0." + "0" * 38 + "1"),
        ("decimal", "9" * 39),
        ("decimal", "9" * 38 + ".1"),
        ("integer", 2**63),
        ("integer", True),
        ("boolean", "false"),
        ("date", "2024-02-30"),
        ("text", " "),
    ],
)
def test_projection_rejects_non_wire_values(bundle, run_fields, kind, invalid):
    run = ModelRun.model_validate(run_fields)
    payload = project_output(run, "price")
    payload["results"][0].update(value=invalid, value_type=kind)
    validator = Draft202012Validator(
        bundle["widget-projection.schema.json"],
        format_checker=Draft202012Validator.FORMAT_CHECKER,
    )
    assert not validator.is_valid(payload)


def test_output_nullability_matches_saved_status(bundle, run_fields):
    run = ModelRun.model_validate(run_fields)
    payload = project_output(run, "price")
    row = payload["results"][0]
    validator = Draft202012Validator(bundle["widget-projection.schema.json"])
    row["value"] = None
    assert not validator.is_valid(payload)
    row.update(status="withheld", display_value=None, display_text=None)
    assert validator.is_valid(payload)
    row["value"] = "1"
    assert not validator.is_valid(payload)


@pytest.mark.parametrize(
    "name,missing",
    [
        ("widgets", path)
        for path in (
            ("widgetId",),
            ("endpoint",),
            ("data",),
            ("data", "dataKey"),
            ("data", "table", "columnsDefs"),
            ("params", 0, "paramName"),
        )
    ]
    + [
        ("apps", path)
        for path in (
            ("name",),
            ("description",),
            ("allowCustomization",),
            ("tabs",),
            ("tabs", "Saved output", "layout"),
            ("tabs", "Saved output", "layout", 0, "i"),
        )
    ],
)
def test_discovery_schemas_require_workspace_fields(bundle, name, missing):
    api = bundle["openapi.json"]
    response = api["paths"][f"/{name}.json"]["get"]["responses"]["200"]
    embedded = api | response["content"]["application/json"]["schema"]
    standalone = bundle[f"{name}.schema.json"]
    payload = json.loads(json.dumps(bundle[f"{name}.json"]))
    validate(embedded, payload)
    validate(standalone, payload)
    entry = next(iter(payload.values())) if name == "widgets" else payload[0]
    for token in missing[:-1]:
        entry = entry[token]
    del entry[missing[-1]]
    assert not Draft202012Validator(embedded).is_valid(payload)
    assert not Draft202012Validator(standalone).is_valid(payload)


@pytest.mark.parametrize(
    "created_at",
    [
        "2024-01-02",
        "2024-01-02T20:00:00",
        "2024-02-30T20:00:00Z",
        "2024-01-02T25:00:00Z",
        "2024-01-02T20:00:00+25:00",
        "",
    ],
)
def test_saved_run_schema_rejects_malformed_created_at(bundle, run_fields, created_at):
    payload = ModelRun.model_validate(run_fields).model_dump(mode="json")
    schema = bundle["model-run.schema.json"]
    validate(schema, payload)
    payload["created_at"] = created_at
    validator = Draft202012Validator(
        schema, format_checker=Draft202012Validator.FORMAT_CHECKER
    )
    assert not validator.is_valid(payload)
