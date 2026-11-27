"""Compose the Events and Documents App from the four accepted FMP bindings."""
import re
from datetime import date

from qopenbb_ci.catalog_batch_b import BINDINGS, query_policy

RENDERER_ID = "events_documents_story"
TITLE = "Events and Documents"
QUESTION = (
    "What earnings figures does FMP report for this company, "
    "and which filings, transcript or news items can I inspect?"
)
SOURCES = {
    "calendar": ("fmp_calendar_earnings", "CalendarEarnings"),
    "filings": ("fmp_company_filings", "CompanyFilings"),
    "transcript": ("fmp_earnings_call_transcript", "EarningsCallTranscript"),
    "news": ("fmp_company_news", "CompanyNews"),
}
SYMBOL = {"title": "Symbol", "type": "string", "minLength": 1, "maxLength": 50}
# The transcript adapter imposes the narrowest grammar of the three document queries.
LISTING = re.compile(r"[A-Za-z0-9^][A-Za-z0-9.^=-]{0,49}")


def integer(name: str, minimum: int, maximum: int, **extra: int) -> dict:
    return {"title": name, "type": "integer", "minimum": minimum, "maximum": maximum, **extra}


def accepted_query(slot: str) -> dict:
    properties = {} if slot == "calendar" else {"symbol": SYMBOL}
    required = list(properties)
    if slot == "transcript":
        properties.update(year=integer("Year", 1900, 2100), quarter=integer("Quarter", 1, 4))
        required.extend(("year", "quarter"))
    else:
        for name, title in (("start_date", "Start Date"), ("end_date", "End Date")):
            civil_date = {"type": "string", "format": "date"}
            if slot == "news":
                properties[name] = {"title": title, "anyOf": [civil_date, {"type": "null"}], "default": None}
            else:
                properties[name] = {"title": title, **civil_date}
                required.append(name)
        if slot in {"filings", "news"}:
            maximum, limit = (100, 20) if slot == "filings" else (50, 10)
            properties.update(page=integer("Page", 0, 99, default=0),
                              limit=integer("Limit", 1, maximum, default=limit))
    return {"properties": properties, "required": required}


def validated_policy(slot: str, dataset_id: str, model: str, source: dict, widgets: dict) -> dict:
    binding = BINDINGS[dataset_id]
    path = "/api/v1/" + binding["route"]
    widget_id = binding["route"].replace("/", "_") + "_fmp_obb"
    widget = widgets.get(widget_id, {})
    contract = widget.get("financialContract", {})
    expected_policy = query_policy(binding, accepted_query(slot))
    if (
        source != {"dataset": dataset_id, "widget": widget_id, "provider": "fmp", "path": path}
        or widget.get("widgetId") != widget_id
        or widget.get("endpoint") != path
        or widget.get("type") != binding["renderer"]
        or widget.get("source") != ["FMP"]
        or widget.get("data", {}).get("scope") != ("listing" if binding["company"] else "market")
        or contract.get("dataset") != model
        or contract.get("providers") != ["fmp"]
        or set(contract.get("variants", {})) != {"fmp"}
        or widget.get("queryPolicy") != expected_policy
    ):
        raise ValueError("Events and Documents requires the accepted FMP declaration: " + slot)
    return expected_policy


def validate_dates(values: dict, window: dict) -> None:
    start, end = (values.get(window[name]) for name in ("startParameter", "endParameter"))
    if start is None and end is None and window["mode"] == "optional_pair":
        return
    if not isinstance(start, str) or not isinstance(end, str):
        raise ValueError("Expected an inclusive date pair")
    first, last = date.fromisoformat(start), date.fromisoformat(end)
    if (first.isoformat() != start or last.isoformat() != end
            or not 1 <= (last - first).days + 1 <= window["maxInclusiveDays"]):
        raise ValueError("Date defaults violate the inclusive window")


def defaults(dataset: dict, policy: dict) -> dict:
    parameters = dataset["parameters"]
    values = {name: parameters.get(name, rule.get("default"))
              for name, rule in policy["parameters"].items()
              if name in parameters or rule.get("default") is not None}
    # The served query schema checks scalar types. Batch B rejects explicit
    # nulls even where OpenAPI represents an omitted optional date with null.
    if any(value is None for value in values.values()):
        raise ValueError("Explicit null in Events and Documents defaults")
    if policy["dateWindow"] is not None:
        validate_dates(values, policy["dateWindow"])
    return values


def selections(inventory: dict, mapping: list, widgets: dict) -> dict:
    datasets = {item["id"]: item for item in inventory["datasets"]}
    sources = {item["dataset"]: item for item in mapping}
    choices, symbols = {}, set()
    for slot, (dataset_id, model) in SOURCES.items():
        policy = validated_policy(slot, dataset_id, model, sources[dataset_id], widgets)
        values = defaults(datasets[dataset_id], policy)
        if policy["maxSymbols"]:
            symbol = values.pop("symbol")
            if not isinstance(symbol, str) or LISTING.fullmatch(symbol) is None:
                raise ValueError("Invalid Events and Documents default listing: " + slot)
            symbols.add(symbol.upper())
        choices[slot] = values
    if len(symbols) != 1:
        raise ValueError("Events and Documents requires one shared default listing")
    symbol, = symbols
    return {"version": 1, "symbol": symbol, **choices, "charts": {"eps": "bar", "revenue": "point"}}


def events_documents_app(inventory: dict, mapping: list, widgets: dict) -> list:
    selected = {item["dataset"] for item in mapping}
    expected = {dataset_id for dataset_id, _ in SOURCES.values()}
    if not selected & expected:
        return []
    if not expected <= selected:
        raise ValueError("Missing Events and Documents bindings")
    state = selections(inventory, mapping, widgets)
    grid = {"w": 40, "h": 24}
    widgets[RENDERER_ID] = {
        "widgetId": RENDERER_ID, "type": RENDERER_ID, "name": TITLE,
        "description": QUESTION, "category": "Research", "gridData": grid, "params": [],
    }
    layout = {
        "i": RENDERER_ID, "x": 0, "y": 0, **grid,
        "view_order": ["question", *SOURCES, "conclusion"],
        "state": {"storage": {"eventsDocuments": state}},
    }
    return [{
        "name": TITLE, "description": QUESTION, "allowCustomization": True,
        "tabs": {"Research": {"id": "Research", "name": "Research", "layout": [layout]}},
    }]
