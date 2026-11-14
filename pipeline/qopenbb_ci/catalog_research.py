"""Compose a research App without adapting away analyst-owned widget storage."""
from copy import deepcopy

RENDERER_ID = "company_research"
PRIMARY = {
    "company-profile": ("equity_profile_fmp_obb", "/api/v1/equity/profile"),
    "annual-income": ("equity_fundamental_income_fmp_obb", "/api/v1/equity/fundamental/income"),
    "annual-balance-sheet": ("equity_fundamental_balance_fmp_obb", "/api/v1/equity/fundamental/balance"),
    "annual-cash-flow": ("equity_fundamental_cash_fmp_obb", "/api/v1/equity/fundamental/cash"),
    "daily-prices": ("equity_price_historical_fmp_obb", "/api/v1/equity/price/historical"),
}
STATEMENTS = {"annual-income", "annual-balance-sheet", "annual-cash-flow"}


def primary_layout(inventory: dict, mapping: list, widgets: dict) -> list:
    datasets = {item["id"]: item for item in inventory["datasets"]}
    ids = {item["dataset"]: item["widget"] for item in mapping}
    layout = []
    for index, (dataset, (widget_id, endpoint)) in enumerate(PRIMARY.items()):
        widget = widgets.get(ids.get(dataset), {})
        if (ids.get(dataset) != widget_id or widget.get("type") != "table"
                or widget.get("widgetId") != widget_id or widget.get("endpoint") != endpoint
                or datasets[dataset]["provider"] != "fmp"):
            raise ValueError("Company research requires the accepted FMP table: " + dataset)
        params = deepcopy(datasets[dataset]["parameters"])
        params["symbol"] = "AAPL"
        groups = ["Symbol"]
        if dataset in STATEMENTS:
            params.update(period="annual", limit=3)
            groups.append("Statement period")
        layout.append({"i": widget_id, "x": 0, "y": index * 15, "w": 40, "h": 15,
                       "groups": groups, "state": {"params": params}})
    return layout


def research_app(inventory: dict, mapping: list, widgets: dict) -> tuple[list, dict]:
    missing = sorted(PRIMARY.keys() - {item["dataset"] for item in mapping})
    if missing:
        return [], {"status": "unavailable", "missing_datasets": missing}
    layout = primary_layout(inventory, mapping, widgets)
    widgets[RENDERER_ID] = {
        "widgetId": RENDERER_ID, "type": RENDERER_ID, "name": "Peer Research",
        "description": "Add candidate peers and inspect provider observations. Saved choices are not frozen data.",
        "category": "Equity", "gridData": {"w": 40, "h": 20}, "params": [],
    }
    # Peers own their frequency and selections; primary-company groups cannot rewrite them.
    layout.append({"i": RENDERER_ID, "x": 0, "y": 75, "w": 40, "h": 20, "groups": [],
                   "state": {"storage": {"companyResearch": {
                       "version": 1, "peers": [], "period": "annual", "limit": 3}}}})
    app = {
        "name": "Company Research", "allowCustomization": True,
        "description": "Research Apple Inc. (AAPL), the explicit initial example. Select or clear the company; "
                       "inspect Income, Balance, Cash, dated price context and independent candidate peers.",
        "groups": [
            {"name": "Symbol", "type": "param", "paramName": "symbol", "defaultValue": "AAPL"},
            {"name": "Statement period", "type": "param", "paramName": "period", "defaultValue": "annual"},
        ],
        "tabs": {"Research": {"id": "Research", "name": "Research", "layout": layout}},
    }
    return [app], {"status": "generated", "renderer": RENDERER_ID}
