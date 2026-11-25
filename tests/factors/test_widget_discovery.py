"""Pin the Workspace connector mapping for saved modeling outputs."""

import json
from pathlib import Path

import pytest
from jsonschema import Draft7Validator
from qopenbb_data.modeling.service import widget_discovery

_WIDGET_ID = "qopenbb_saved_model_output"
_WORKSPACE = Path(__file__).resolve().parents[2] / "vendor/workspace/terminalpro"


@pytest.mark.parametrize(
    ("export", "schema_path"),
    [
        pytest.param(
            widget_discovery.widgets,
            "src/components/DataConnectors/WidgetsBuilder/widget-schema.json",
            id="widgets",
        ),
        pytest.param(widget_discovery.apps, "apps-schema.json", id="apps"),
    ],
)
def test_discovery_export_matches_vendored_workspace_schema(export, schema_path):
    schema = json.loads((_WORKSPACE / schema_path).read_text(encoding="utf-8"))
    Draft7Validator.check_schema(schema)
    payload = json.loads(json.dumps(export()))
    Draft7Validator(schema).validate(payload)


def test_saved_output_widget_has_one_static_route_and_unbound_text_params():
    catalog = widget_discovery.widgets()
    assert list(catalog) == [_WIDGET_ID]
    widget = catalog[_WIDGET_ID]
    assert widget["widgetId"] == _WIDGET_ID
    assert widget["type"] == "table"
    assert widget["endpoint"] == "widget-results"
    assert widget["runButton"] is True
    assert [
        (param["paramName"], param["type"], param["optional"], param["value"])
        for param in widget["params"]
    ] == [
        ("run_id", "text", False, None),
        ("output_id", "text", False, None),
        ("expected_run_id", "text", True, None),
    ]
    assert all(param["show"] for param in widget["params"])


def test_saved_output_table_uses_literal_display_and_state_columns():
    data = widget_discovery.widgets()[_WIDGET_ID]["data"]
    assert data["dataKey"] == "results"
    assert data["table"]["showAll"] is False
    assert all(
        column["chartDataType"] == "excluded" for column in data["table"]["columnsDefs"]
    )
    assert [
        (column["field"], column["cellDataType"], column["formatterFn"])
        for column in data["table"]["columnsDefs"]
    ] == [
        ("display_text", "text", "none"),
        ("status", "text", "none"),
        ("freshness", "text", "none"),
        ("reason", "text", "none"),
        ("unit", "text", "none"),
        ("check_explanations", "text", "none"),
        ("run_detail_href", "text", "none"),
    ]


def test_app_resolves_catalog_widget_without_a_saved_run_default():
    (app,) = widget_discovery.apps()
    (tab_id,) = app["tabs"]
    tab = app["tabs"][tab_id]
    assert tab["id"] == tab_id
    assert tab["name"]
    (layout,) = tab["layout"]
    assert layout["i"] == _WIDGET_ID
    widget = widget_discovery.widgets()[layout["i"]]
    assert (layout["w"], layout["h"]) == (
        widget["gridData"]["w"],
        widget["gridData"]["h"],
    )
    assert layout["state"]["params"] == {}
