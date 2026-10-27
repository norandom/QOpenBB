"""Supported consumer generation must fail closed before renderer acceptance."""
from copy import deepcopy
import json
from pathlib import Path
import subprocess

import pytest

from qopenbb_ci.catalog import canonical, freeze_routes, generate, compatibility


@pytest.fixture
def inputs():
    operation = {"operationId": "profile", "parameters": [
        {"name": "provider", "in": "query", "schema": {"enum": ["fmp"]}},
        {"name": "symbol", "in": "query", "required": True, "schema": {"type": "string"}},
    ], "responses": {"200": {"content": {"application/json": {"schema": {"$ref": "#/components/schemas/Result"}}}}}}
    schema = {"paths": {"/api/v1/profile": {"get": operation}},
              "components": {"schemas": {"Result": {"type": "object"}}}}
    inventory = {"datasets": [{"id": "profile", "path": "/api/v1/profile", "provider": "fmp",
                               "parameters": {"provider": "fmp", "symbol": "AAPL"}}]}
    widgets = {"profile_fmp_obb": {"widgetId": "profile_fmp_obb", "endpoint": "/api/v1/profile",
               "params": [{"paramName": "provider", "value": "fmp"}], "type": "table"}}
    return schema, inventory, widgets


def test_freeze_preserves_exact_served_contract(inputs):
    schema, inventory, _ = inputs
    route = freeze_routes(schema, inventory)["routes"][0]
    assert route["operationId"] == "profile"
    assert route["parameters"] == schema["paths"][route["path"]]["get"]["parameters"]
    assert route["responses"] == schema["paths"][route["path"]]["get"]["responses"]


@pytest.mark.parametrize("mutation", ["path", "provider", "parameter", "ref", "duplicate"])
def test_invalid_supported_mapping_rejected(inputs, mutation):
    schema, inventory, _ = inputs
    if mutation == "path":
        inventory["datasets"][0]["path"] = "/absent"
    elif mutation == "provider":
        inventory["datasets"][0]["provider"] = "unknown"
    elif mutation == "parameter":
        inventory["datasets"][0]["parameters"]["secret"] = "x"
    elif mutation == "ref":
        schema["components"]["schemas"] = {}
    else:
        schema["paths"]["/duplicate"] = deepcopy(schema["paths"]["/api/v1/profile"])
    with pytest.raises(ValueError):
        freeze_routes(schema, inventory)


def test_canonical_repeat_and_app_reference_adaptation(inputs):
    schema, inventory, widgets = inputs
    bundled = [{"name": "FRED", "description": "Retained source metadata", "tabs": {
        "Data": {"id": "Data", "name": "Data", "layout": [
            {"i": "profile_fmp_obb", "x": 0, "y": 0, "w": 20, "h": 10,
             "state": {"params": {"symbol": "GDP"}, "chartView": {"enabled": True}}},
            {"i": "unaccepted_widget", "x": 0, "y": 10, "w": 20, "h": 10}]}}}]
    first = generate(schema, inventory, widgets, bundled, "/data")
    assert canonical(first) == canonical(generate(schema, inventory, widgets, bundled, "/data"))
    assert first["widgets.json"]["profile_fmp_obb"]["endpoint"] == "/api/v1/profile"
    assert first["apps.json"][1]["description"] == "Retained source metadata"
    assert first["apps.json"][1]["tabs"]["Data"]["layout"][0]["state"] == {"params": {"symbol": "GDP"}}
    report = first["catalog-report.json"]
    assert report["renderer_status"] == "pending-task-2.9"
    assert any(item["widget"] == "unaccepted_widget" for item in report["omitted"])
    for app in first["apps.json"]:
        for tab in app["tabs"].values():
            assert all(item["i"] in first["widgets.json"] for item in tab["layout"])


def test_dangling_generated_widget_or_provider_rejected(inputs):
    schema, inventory, widgets = inputs
    widgets["profile_fmp_obb"]["endpoint"] = "/not-installed"
    with pytest.raises(ValueError):
        generate(schema, inventory, widgets, [], "/data")


def test_contract_drift_reports_affected_datasets(inputs):
    schema, inventory, _ = inputs
    before = freeze_routes(schema, inventory)
    schema["paths"]["/api/v1/profile"]["get"]["responses"]["200"]["description"] = "changed"
    report = compatibility(before, freeze_routes(schema, inventory))
    assert report["requires_revalidation"] is True
    assert report["changes"] == [{"dataset": "profile", "fields": ["responses"]}]


def test_json_has_no_nonfinite_or_timestamp_injection():
    with pytest.raises(ValueError):
        canonical({"value": float("nan")})
    assert canonical({"b": 2, "a": 1}) == b'{"a":1,"b":2}\n'


def test_actual_workspace_url_composition(inputs, tmp_path):
    root = Path(__file__).resolve().parents[2]
    source = (root / "vendor/workspace/terminalpro/src/lib/utils/widgetParams.ts").read_text()
    functions = ["export function " + source.split("export function " + name, 1)[1].split("\n}", 1)[0] + "\n}"
                 for name in ("cleanURL", "createURLString")]
    # Prefix the original names stripped by the extraction split; Node strips TS annotations.
    functions = [body.replace("export function ", "export function " + name, 1)
                 for body, name in zip(functions, ("cleanURL", "createURLString"))]
    endpoint = generate(*inputs, [], "/data")["widgets.json"]["profile_fmp_obb"]["endpoint"]
    script = tmp_path / "composition.ts"
    script.write_text("\n".join(functions) + "\nconsole.log(createURLString(" + json.dumps(endpoint) + ", 'https://qbb.example/data'))")
    node = root / "artifacts/task-1.2/node-v24.22.0-linux-x64/bin/node"
    result = subprocess.run([str(node), str(script)], text=True, capture_output=True, check=True)
    assert result.stdout.strip() == "https://qbb.example/data/api/v1/profile"


def test_bundled_groups_have_no_dangling_widget_ids(inputs):
    schema, inventory, widgets = inputs
    bundled = [{"name": "FRED", "authentication": "Get browser API key", "tabs": {
        "Data": {"layout": [{"i": "profile_fmp_obb", "state": {"params": {"symbol": "GDP"}}}]}},
        "groups": [{"name": "Series", "widgetIds": ["profile_fmp_obb", "missing"]},
                   {"name": "Other", "widgetIds": ["missing"]}]}]
    output = generate(schema, inventory, widgets, bundled, "/data")
    app = output["apps.json"][1]
    assert app["groups"] == [{"name": "Series", "widgetIds": ["profile_fmp_obb"]}]
    assert "authentication" not in app


def test_external_app_previews_use_existing_workspace_fallback(inputs):
    schema, inventory, widgets = inputs
    source = {"name": "FRED", "img": "https://example.invalid/fred.png",
              "img_light": "//example.invalid/light.png", "img_dark": "HTTP://example.invalid/dark.png",
              "tabs": {"Data": {"layout": [{"i": "profile_fmp_obb",
                       "state": {"params": {"symbol": "GDP"}}}]}}}
    original = deepcopy(source)
    output = generate(schema, inventory, widgets, [source], "/data")
    app = output["apps.json"][1]
    assert all(field not in app for field in ("img", "img_light", "img_dark"))
    assert app["tabs"] == source["tabs"]
    assert source == original
    assert {"app": "FRED", "reason": "external-preview-image",
            "fields": ["img", "img_light", "img_dark"]} in output["catalog-report.json"]["omitted"]
    source.update(img="/assets/fred.png", img_light="assets/fred-light.png", img_dark="")
    local = generate(schema, inventory, widgets, [source], "/data")["apps.json"][1]
    assert all(local[field] == source[field] for field in ("img", "img_light", "img_dark"))


def test_frozen_routes_resolve_refs_independently(inputs):
    from qopenbb_ci.catalog import validate_refs
    schema, inventory, _ = inputs
    validate_refs(freeze_routes(schema, inventory))


def test_response_shape_drift_behind_unchanged_ref_requires_revalidation(inputs):
    schema, inventory, _ = inputs
    before = freeze_routes(schema, inventory)
    schema["components"]["schemas"]["Result"]["properties"] = {"price": {"type": "number"}}
    after = freeze_routes(schema, inventory)
    assert before["routes"] == after["routes"]
    assert compatibility(before, after)["changes"] == [{"dataset": "profile", "fields": ["responses"]}]


def test_const_provider_has_one_allowed_generated_choice(inputs):
    schema, inventory, widgets = inputs
    schema["paths"]["/api/v1/profile"]["get"]["parameters"][0]["schema"] = {"const": "fmp", "type": "string"}
    before = deepcopy(schema)
    output = generate(schema, inventory, widgets, [], "/data")
    assert output["openapi.json"] == before == schema
    provider = output["widgets.json"]["profile_fmp_obb"]["params"][0]
    assert provider["value"] == "fmp"
    assert provider["options"] == [{"label": "FMP", "value": "fmp"}]
