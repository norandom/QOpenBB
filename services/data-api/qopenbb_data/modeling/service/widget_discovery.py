"""Describe the Workspace table for an explicitly selected saved model output."""

_WIDGET_ID = "qopenbb_saved_model_output"
_TITLE = "Saved model output"
_DESCRIPTION = (
    "Enter a saved run ID and output ID to inspect the result and its checks."
)
_GRID = {"w": 40, "h": 15}
_PARAMS = (
    ("run_id", "Run ID", False),
    ("output_id", "Output ID", False),
    ("expected_run_id", "Expected run ID", True),
)
_COLUMNS = (
    ("display_text", "Value"),
    ("status", "Status"),
    ("freshness", "Freshness"),
    ("reason", "Reason"),
    ("unit", "Unit"),
    ("check_explanations", "Check explanations"),
    ("run_detail_href", "Run detail reference"),
)


def widgets() -> dict:
    return {
        _WIDGET_ID: {
            "widgetId": _WIDGET_ID,
            "name": _TITLE,
            "description": _DESCRIPTION,
            "category": "Modeling",
            "type": "table",
            # Workspace resolves string endpoints as GET under the connector base.
            "endpoint": "widget-results",
            "runButton": True,
            "gridData": dict(_GRID),
            "params": [
                {
                    "paramName": name,
                    "label": label,
                    "type": "text",
                    "show": True,
                    "optional": optional,
                    "value": None,
                }
                for name, label, optional in _PARAMS
            ],
            "data": {
                "dataKey": "results",
                "table": {
                    "showAll": False,
                    "columnsDefs": [
                        {
                            "field": field,
                            "headerName": label,
                            "cellDataType": "text",
                            # The table otherwise parses numeric-looking strings as chart series.
                            "chartDataType": "excluded",
                            "formatterFn": "none",
                        }
                        for field, label in _COLUMNS
                    ],
                },
            },
        }
    }


def apps() -> list:
    tab_id = "Saved output"
    return [
        {
            "name": _TITLE,
            "description": _DESCRIPTION,
            "allowCustomization": True,
            "tabs": {
                tab_id: {
                    "id": tab_id,
                    "name": tab_id,
                    "layout": [
                        {
                            "i": _WIDGET_ID,
                            "x": 0,
                            "y": 0,
                            **_GRID,
                            "state": {"params": {}},
                        }
                    ],
                }
            },
        }
    ]
