"""Freeze installed financial routes and adapt only supported consumer metadata."""
from copy import deepcopy
import hashlib
import json


def canonical(value: object) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"),
                       ensure_ascii=False, allow_nan=False) + "\n").encode()


def digest(value: object) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def validate_refs(document: dict) -> None:
    def walk(value):
        if isinstance(value, dict):
            if "$ref" in value:
                ref = value["$ref"]
                if not ref.startswith("#/"):
                    raise ValueError("external schema reference: " + ref)
                target = document
                try:
                    for part in ref[2:].split("/"):
                        target = target[part.replace("~1", "/").replace("~0", "~")]
                except (KeyError, TypeError) as exc:
                    raise ValueError("unresolved schema reference: " + ref) from exc
            for item in value.values():
                walk(item)
        elif isinstance(value, list):
            for item in value:
                walk(item)
    walk(document)


def provider_choices(parameter: dict, schema: dict) -> list:
    value = parameter.get("schema", {})
    if "$ref" in value:
        value = schema["components"]["schemas"][value["$ref"].split("/")[-1]]
    if "const" in value:
        return [value["const"]]
    return value.get("enum", [])


def validate_dataset(dataset: dict, operation: dict, schema: dict) -> None:
    params = {p["name"]: p for p in operation.get("parameters", [])}
    query = dataset["parameters"]
    if query.get("provider") != dataset["provider"]:
        raise ValueError("inconsistent dataset provider")
    if dataset["provider"] not in provider_choices(params.get("provider", {}), schema):
        raise ValueError("unregistered provider: " + dataset["provider"])
    if set(query) - params.keys():
        raise ValueError("unknown dataset parameter")
    if any(p.get("required") and name not in query for name, p in params.items()):
        raise ValueError("missing required dataset parameter")
    if "200" not in operation.get("responses", {}):
        raise ValueError("missing supported success response")


def freeze_routes(schema: dict, inventory: dict) -> dict:
    validate_refs(schema)
    operation_ids = []
    for path in schema["paths"].values():
        for method, operation in path.items():
            if method in {"get", "post", "put", "delete", "patch", "head", "options"}:
                operation_ids.append(operation.get("operationId"))
    if None in operation_ids or len(operation_ids) != len(set(operation_ids)):
        raise ValueError("missing or duplicate operation IDs")
    routes, seen = [], set()
    for dataset in inventory["datasets"]:
        if dataset["id"] in seen:
            raise ValueError("duplicate dataset ID")
        seen.add(dataset["id"])
        operation = schema["paths"].get(dataset["path"], {}).get("get")
        if not operation:
            raise ValueError("dataset route absent: " + dataset["path"])
        validate_dataset(dataset, operation, schema)
        routes.append({"dataset": dataset["id"], "method": "GET", "path": dataset["path"],
                       **{k: deepcopy(operation[k]) for k in ("operationId", "parameters", "responses")}})
    return {"schema_version": 1, "status": "installed", "routes": routes,
            "components": deepcopy(schema.get("components", {}))}


def supported_widgets(raw: dict, inventory: dict, prefix: str) -> tuple[dict, list]:
    widgets, mapping = {}, []
    for dataset in inventory["datasets"]:
        matches = [(key, item) for key, item in raw.items()
                   if item.get("endpoint") == dataset["path"]
                   and key.endswith("_" + dataset["provider"] + "_obb")]
        if len(matches) != 1:
            raise ValueError("missing or ambiguous generated widget: " + dataset["id"])
        key, source = matches[0]
        widget = deepcopy(source)
        if widget.get("widgetId") != key:
            raise ValueError("widget ID mismatch")
        # Workspace composes this with the registered PUBLIC_URL/data base.
        widget["endpoint"] = dataset["path"]
        for param in widget.get("params", []):
            if param.get("paramName") == "provider":
                param["value"] = dataset["provider"]
                param["options"] = [{"label": dataset["provider"].upper(), "value": dataset["provider"]}]
        widgets[key] = widget
        mapping.append({"dataset": dataset["id"], "provider": dataset["provider"],
                        "widget": key, "path": dataset["path"]})
    return widgets, mapping


def starter(inventory: dict, mapping: list) -> dict:
    ids = {item["dataset"]: item["widget"] for item in mapping}
    layout = [{"i": ids[item["id"]], "x": 0, "y": index * 15, "w": 40, "h": 15,
               "state": {"params": deepcopy(item["parameters"])}}
              for index, item in enumerate(inventory["datasets"])]
    return {"name": "QOpenBB starter", "description": "FMP company data and FRED observations.",
            "allowCustomization": True, "tabs": {"Data": {"id": "Data", "name": "Data", "layout": layout}}}


def adapt_apps(bundled: list, widgets: dict) -> tuple[list, list]:
    apps, omitted = [], []
    for source in bundled:
        app = deepcopy(source)
        external_previews = [field for field in ("img", "img_light", "img_dark")
                             if isinstance(app.get(field), str)
                             and app[field].lower().startswith(("http://", "https://", "//"))]
        for field in external_previews:
            app.pop(field)
        if external_previews:
            omitted.append({"app": app["name"], "reason": "external-preview-image",
                            "fields": external_previews})
        if "authentication" in app:
            app.pop("authentication")
            omitted.append({"app": app["name"], "reason": "server-owned-provider-credentials",
                            "fields": ["authentication"]})
        tabs = {}
        for key, tab in app.get("tabs", {}).items():
            layout = []
            for item in tab.get("layout", []):
                if item["i"] not in widgets:
                    omitted.append({"app": app["name"], "tab": key, "widget": item["i"],
                                    "reason": "outside-supported-inventory"})
                    continue
                state = item.get("state", {})
                removed = sorted(set(state) - {"params"})
                if removed:
                    omitted.append({"app": app["name"], "tab": key, "widget": item["i"],
                                    "reason": "renderer-state-pending-task-2.9", "fields": removed})
                item["state"] = {"params": state.get("params", {})}
                layout.append(item)
            if layout:
                tabs[key] = {**tab, "layout": layout}
        if tabs:
            app["tabs"] = tabs
            app["groups"], excluded = adapt_groups(app.get("groups", []), widgets, app["name"])
            omitted.extend(excluded)
            apps.append(app)
    return apps, omitted


def adapt_groups(groups: list, widgets: dict, app: str) -> tuple[list, list]:
    supported, omitted = [], []
    for group in groups:
        accepted = [key for key in group.get("widgetIds", []) if key in widgets]
        rejected = sorted(set(group.get("widgetIds", [])) - widgets.keys())
        if rejected:
            omitted.append({"app": app, "group": group["name"], "widgets": rejected,
                            "reason": "group-outside-supported-inventory"})
        if accepted:
            supported.append({**group, "widgetIds": accepted})
    return supported, omitted


def contract_dependencies(value: object, document: dict) -> dict:
    references = {}
    def walk(item):
        if isinstance(item, dict):
            ref = item.get("$ref")
            if ref and ref not in references:
                target = document
                for part in ref[2:].split("/"):
                    target = target[part.replace("~1", "/").replace("~0", "~")]
                references[ref] = target
                walk(target)
            for child in item.values():
                walk(child)
        elif isinstance(item, list):
            for child in item:
                walk(child)
    walk(value)
    return {"value": value, "references": references}


def compatibility(before: dict | None, after: dict) -> dict:
    old = {item["dataset"]: item for item in (before or {}).get("routes", [])}
    new = {item["dataset"]: item for item in after["routes"]}
    changes = []
    for key in sorted(old.keys() | new.keys()):
        fields = [field for field in ("path", "method", "operationId", "parameters", "responses")
                  if contract_dependencies(old.get(key, {}).get(field), before or {})
                  != contract_dependencies(new.get(key, {}).get(field), after)]
        if fields:
            changes.append({"dataset": key, "fields": fields})
    return {"requires_revalidation": bool(changes), "changes": changes,
            "affected_consumers": ["workspace", "agent", "future-excel"] if changes else []}


def generate(schema: dict, inventory: dict, raw: dict, bundled: list, prefix: str) -> dict:
    if not prefix.startswith("/") or prefix.endswith("/") or ".." in prefix or "?" in prefix:
        raise ValueError("invalid public prefix")
    routes = freeze_routes(schema, inventory)
    installed = {**deepcopy(inventory), "status": "installed"}
    widgets, mapping = supported_widgets(raw, inventory, prefix)
    apps, omitted = adapt_apps(bundled, widgets)
    return {"openapi.json": deepcopy(schema), "routes.json": routes, "widgets.json": widgets,
            "datasets.json": installed,
            "apps.json": [starter(inventory, mapping), *apps],
            "catalog-report.json": {"schema_version": 1, "mapping": mapping, "omitted": omitted,
                                    "renderer_status": "pending-task-2.9",
                                    "served_schema_hash": digest(schema), "public_prefix": prefix,
                                    "endpoint_base": "registered-connector-base"}}
