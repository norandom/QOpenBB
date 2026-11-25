"""Bind accepted data widgets without replacing the upstream widget schema."""
from copy import deepcopy


POLICIES = {
    "company-profile": {
        "operationId": "equity_profile", "provider": "fmp",
        "path": "/api/v1/equity/profile", "schema_id": "qopenbb.company-profile.v1",
        "columns": ["symbol", "name", "currency", "last_price", "market_cap", "sector"],
    },
    "annual-income": {
        "operationId": "equity_fundamental_income", "provider": "fmp",
        "path": "/api/v1/equity/fundamental/income", "schema_id": "qopenbb.annual-income.v1",
        "columns": ["period_ending", "symbol", "reported_currency", "revenue",
                    "gross_profit", "consolidated_net_income", "basic_earnings_per_share"],
    },
    "gdp": {
        "operationId": "economy_fred_series", "provider": "fred",
        "path": "/api/v1/economy/fred_series", "schema_id": "qopenbb.fred-series.v1",
        "columns": "all-declared",
    },
}


def keyed(items: list, field: str) -> dict:
    result = {item[field]: item for item in items}
    if len(result) != len(items):
        raise ValueError("duplicate renderer contract identity")
    return result


def binding(dataset: dict, route: dict, mapping: dict, widgets: dict) -> dict:
    policy = POLICIES[dataset["id"]]
    widget_id = policy["operationId"] + "_" + policy["provider"] + "_obb"
    widget = widgets.get(widget_id, {})
    expected_mapping = {"dataset": dataset["id"], "path": policy["path"],
                        "provider": policy["provider"], "widget": widget_id}
    if (mapping != expected_mapping or route.get("operationId") != policy["operationId"]
            or route.get("path") != policy["path"] or route.get("method") != "GET"
            or dataset.get("provider") != policy["provider"] or dataset.get("path") != policy["path"]
            or dataset.get("parameters", {}).get("provider") != policy["provider"]
            or widget.get("widgetId") != widget_id or widget.get("endpoint") != policy["path"]
            or widget.get("type") != "table"):
        raise ValueError("renderer differs from installed dataset/widget contract")
    return {"dataset": dataset["id"], "widget": widget_id,
            **{key: policy[key] for key in ("operationId", "provider", "path", "schema_id")},
            "parameters": deepcopy(dataset["parameters"]),
            "defaults": {"plugin": "Datagrid", "columns": deepcopy(policy["columns"]),
                         "group_by": [], "split_by": [], "aggregate": "unique"}}


def validate_apps(apps: list, widget_ids: set[str]) -> None:
    for app in apps:
        for tab in app.get("tabs", {}).values():
            if any(item["i"] not in widget_ids for item in tab.get("layout", [])):
                raise ValueError("unbound financial app widget")
        for group in app.get("groups", []):
            if not set(group.get("widgetIds", [])) <= widget_ids:
                raise ValueError("unbound financial app group")


def bind_renderers(outputs: dict) -> dict:
    datasets = keyed(outputs["datasets.json"]["datasets"], "id")
    routes = keyed(outputs["routes.json"]["routes"], "dataset")
    mappings = keyed(outputs["catalog-report.json"]["mapping"], "dataset")
    if any(set(items) != set(POLICIES) for items in (datasets, routes, mappings)):
        raise ValueError("renderer inventory differs from accepted financial datasets")
    bindings = [binding(datasets[key], routes[key], mappings[key], outputs["widgets.json"])
                for key in POLICIES]
    widget_ids = {item["widget"] for item in bindings}
    if set(outputs["widgets.json"]) != widget_ids:
        raise ValueError("unbound generated widget")
    validate_apps(outputs["apps.json"], widget_ids)
    result = deepcopy(outputs)
    result["renderers.json"] = {
        "schema_version": 1,
        "renderer": {"id": "perspective", "version": 1, "package_version": "5.6.0"},
        "bindings": bindings,
    }
    result["catalog-report.json"]["renderer_status"] = "bound"
    return result


def frontend_bindings(outputs: dict) -> dict:
    expected = bind_renderers(outputs)["renderers.json"]
    if outputs.get("renderers.json") != expected:
        raise ValueError("frontend renderer binding differs from installed catalog")
    return deepcopy(expected)
