"""Translate packaged Workspace templates into the saved dashboard API format."""

from copy import deepcopy
from datetime import UTC, datetime
import re
from urllib.parse import urlsplit
from uuid import NAMESPACE_URL, uuid5


COLORS = ("#00AAFF", "#EF6689", "#16A34A", "#FB923C", "#CCBE00",
          "#337DBA", "#998E00", "#917DB0", "#FB923C")


class ProvisionError(Exception):
    pass


def seed_id(owner, key):
    return str(uuid5(NAMESPACE_URL, f"qopenbb/workspace/setup/{owner}/{key}"))


def group_definitions(template, dashboard_id):
    groups = {}
    for index, group in enumerate(template.get("groups") or []):
        kind = group.get("type", "endpointParam")
        if kind not in ("param", "endpointParam"):
            raise ProvisionError("A packaged app uses an unsupported dashboard group type")
        name = group["name"]
        groups[name] = {
            "id": seed_id(dashboard_id, "group/" + name), "name": name, "type": kind,
            "groupById": group["paramName"], "color": COLORS[index % len(COLORS)],
            "value": group["defaultValue"],
        }
    return groups


def parameter(raw):
    param = {
        "type": "text", "label": raw["paramName"], "show": True, "value": None,
        "options": [], **raw,
    }
    if param["type"] == "boolean" and not param["options"]:
        param["options"] = [{"label": "True", "value": True}, {"label": "False", "value": False}]
    return param


def widget_state(definition, state, group_values):
    params = [parameter(raw) for raw in definition.get("params", [])]
    storage = {**definition.get("storage", {}), **state.get("storage", {})}
    values = {p["paramName"]: p["value"] for p in params}
    storage["params"] = {**values, **state.get("params", {}), **group_values}
    data = deepcopy(definition.get("data", {}))
    if definition.get("queryPolicy"):
        data["financialQueryPolicy"] = definition["queryPolicy"]
    if definition.get("financialContract"):
        data["financialContract"] = definition["financialContract"]

    if definition["type"] == "table":
        table = data.setdefault("table", {})
        table.setdefault("enableCharts", True)
        for key in ("columnState", "filterModel", "chartView"):
            if key in state:
                table[key] = state[key]
        storage["chartView"] = {"enabled": False, "chartType": "line",
                                **table.get("chartView", {})}
        storage.setdefault("chartSettingsOpen", False)
        if "enableAdvanced" in table:
            storage["enableAdvanced"] = table["enableAdvanced"]
        if table.get("transpose"):
            storage["transpose"] = True

    chart = state.get("chartModel")
    if chart:
        # The template stores chart models under Workspace's active table state key.
        state_key = "_".join(str(part) for part in (
            storage.get("period", "default"), "transpose" if storage.get("transpose") else "",
            storage.get("selectedGroup"), "reversed" if storage.get("reversed") else "",
            (storage.get("currentSheet") or {}).get("name"), storage.get("selectedRatio"),
            "pivot" if storage.get("isPivotMode") else "",
        ) if part)
        storage.setdefault(state_key, {}).update({
            "chartModel": chart, chart["chartType"]: {"cellRange": chart.get("cellRange")},
        })
    return params, storage, data


def source_endpoint(source_url, endpoint):
    if not isinstance(endpoint, str) or not endpoint or endpoint.startswith("//"):
        raise ProvisionError("A packaged app uses an invalid widget endpoint")
    parsed = urlsplit(endpoint)
    if parsed.scheme or parsed.netloc or parsed.fragment or ".." in parsed.path.split("/"):
        raise ProvisionError("A packaged app uses a widget endpoint outside the data connection")
    return f"{source_url}/{endpoint.lstrip('/')}"


def document_widget(widget):
    values = {key: value for key, value in widget["storage"]["params"].items()
              if value is not None and value != ""}
    widget["storage"] = {"params": values}
    widget["data"] = {"financialQueryPolicy": widget["data"]["financialQueryPolicy"]}
    widget["params"] = [
        {**{key: param[key] for key in ("paramName", "type", "label", "show")},
         "value": values.get(param["paramName"])} for param in widget["params"]
    ]
    widget.update(refetchInterval=False, refetchOnWindowFocus=False, refetchOnReconnect=False)
    widget["endpoint"] = {"url": widget["endpoint"]["url"].split("?")[0], "method": "GET"}
    return widget


def widget_for(definition, layout, identity, source, groups):
    widget_id = layout["i"]
    state = layout.get("state") or {}
    group_values = {group["groupById"]: group["value"] for group in groups.values()}
    params, storage, data = widget_state(definition, state, group_values)
    widget = {
        **identity, "widgetId": widget_id, "type": definition["type"],
        "name": definition["name"], "params": params, "storage": storage,
        "showTitle": definition.get("showTitle", True),
    }
    if widget_id == "research_story":
        return {**widget, "disableRetrievalForCopilot": True,
                "storage": {"researchStory": storage["researchStory"]}}
    widget.update(external=True, sourceId=source["id"], sourceName=source["name"],
                  connectionType="advanced-backend")
    if widget_id == "events_documents_story":
        return {**widget, "category": definition["category"],
                "description": definition["description"], "isSharedWidget": False,
                "disableRetrievalForCopilot": True,
                "storage": {"eventsDocuments": storage["eventsDocuments"]}}

    for key in ("description", "source", "category", "subCategory", "raw", "staleTime",
                "refetchInterval", "dataUpdateDisplay", "disableRetrievalForCopilot"):
        if key in definition:
            widget[key] = definition[key]
    widget.update(data=data, groupId="", runButton=definition.get("runButton", False),
                  exportable=definition.get("exportable", True))
    if groups:
        widget["paramGroups"] = {group["groupById"]: group["id"] for group in groups.values()}
    if "endpoint" in definition:
        url = source_endpoint(source["url"].rstrip("/"), definition["endpoint"])
        widget["endpoint"] = {"url": url, "method": "GET", "headers": {}, "query": {}}
    if widget_id == "qopenbb_saved_model_output":
        widget.pop("sourceId")
        widget["endpoint"]["url"] = "/modeling/v1/widget-results"
        widget["disableRetrievalForCopilot"] = True
        widget["runButton"] = False
        return widget
    if widget["type"] == "company_documents":
        return document_widget(widget)
    if widget.get("runButton") or widget.get("refetchInterval") is False:
        widget.setdefault("staleTime", False)
        widget.setdefault("refetchInterval", False)
    else:
        widget.setdefault("refetchInterval", 900000)
    return widget


def grid_item(definition, layout, instance):
    size = {**definition.get("gridData", {}), **layout}
    grid = {key: size[key] for key in
            ("x", "y", "h", "w", "maxH", "maxW", "minimized", "static") if key in size}
    grid.update(i=instance, minH=min(size.get("minH", 4), size.get("maxH", float("inf"))),
                minW=size.get("minW", 8))
    grid["w"] = max(grid["w"], grid["minW"])
    if layout.get("minimized") or layout["h"] == 1:
        grid.update(h=1.4, minH=1.4, originalMinH=grid["minH"])
    else:
        grid["h"] = max(grid["h"], grid["minH"])
    return grid


def tab_widgets(tab, dashboard_id, catalog, source, groups, group_members):
    for index, layout in enumerate(tab["layout"]):
        widget_id = layout["i"]
        if widget_id == "navigation_bar":
            continue
        if widget_id not in catalog or catalog[widget_id].get("disabled"):
            raise ProvisionError("A packaged app references an unavailable data widget")
        definition = catalog[widget_id]
        instance = seed_id(dashboard_id, f'{tab["id"]}/{index}/{widget_id}')
        minimized = layout.get("minimized", False) or layout["h"] == 1
        identity = {
            "id": instance, "innerTab": tab["id"], "isMinimized": minimized,
            "originalH": layout["h"] if minimized else definition.get("gridData", {}).get("h", layout["h"]),
        }
        group_names = layout.get("groups")
        if group_names is None:
            group_names = [name for name, members in group_members.items() if widget_id in members]
        bindings = {name: group for name, group in groups.items() if name in group_names}
        yield widget_for(definition, layout, identity, source, bindings), grid_item(definition, layout, instance)


def add_navigation(dashboard_id, tabs, widgets, grid):
    if len(tabs) < 2 and not any(item["i"] == "navigation_bar" for tab in tabs for item in tab["layout"]):
        return
    instance = seed_id(dashboard_id, "navigation")
    widgets.append({
        "id": instance, "widgetId": "navigation_bar", "innerTab": tabs[0]["id"],
        "name": "Navigation Bar", "description": "Create nested tabs inside the main tab for navigation.",
        "groupId": "", "params": [], "showTitle": True, "disableRetrievalForCopilot": True,
        "storage": {"params": {}, "tabs": [{k: tab[k] for k in ("id", "name")} for tab in tabs]},
    })
    for items in grid.values():
        items.insert(0, {"i": instance, "x": 0, "y": 0, "w": 40, "h": 2,
                         "minW": 40, "minH": 2, "maxH": 2, "static": True})


def app_template_id(source, name):
    slug = re.sub(r"[^\w-]", "", re.sub(r"\s", "-", name.strip().lower()), flags=re.ASCII)
    return f'custom-{source["id"]}-{slug}'


def make_dashboard(template, dashboard_id, catalog, source, root_id):
    tabs = list(template["tabs"].values())
    if not tabs:
        raise ProvisionError("A packaged app contains no dashboard tabs")
    groups = group_definitions(template, dashboard_id)
    members = {group["name"]: group.get("widgetIds", []) for group in template.get("groups") or []}
    widgets = []
    grid = {}
    for tab in tabs:
        grid[tab["id"]] = []
        for widget, item in tab_widgets(tab, dashboard_id, catalog, source, groups, members):
            widgets.append(widget)
            grid[tab["id"]].append(item)
    add_navigation(dashboard_id, tabs, widgets, grid)
    now = datetime.now(UTC)
    return {
        "index": dashboard_id, "parentId": root_id, "isFolder": False,
        "created_date": now.isoformat(timespec="milliseconds").replace("+00:00", "Z"),
        "data": {
            "name": template["name"], "type": "template", "templateId": app_template_id(source, template["name"]),
            "widgets": widgets, "gridLayout": grid, "groups": list(groups.values()),
            "storedFileUUIDs": [], "currentTab": tabs[0]["id"], "numberOfChanges": 0,
            "lastUpdated": int(now.timestamp() * 1000),
        },
    }
