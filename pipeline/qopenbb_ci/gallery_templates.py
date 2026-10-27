"""Build native table widgets and app layouts from the reviewed saved states."""
from copy import deepcopy
import re


OVERVIEW = ("line", "groupedColumn", "stackedColumn", "normalizedArea", "donut", "radarLine",
            "bubble", "boxPlot", "heatmap", "treemap", "waterfall", "sankey")
FAMILIES = {
    "Columns and Bars": ("groupedColumn", "stackedColumn", "normalizedColumn", "groupedBar", "stackedBar", "normalizedBar"),
    "Lines and Areas": ("line", "stackedLine", "normalizedLine", "area", "stackedArea", "normalizedArea"),
    "Polar and Composition": ("pie", "donut", "radarLine", "radarArea", "nightingale", "radialColumn", "radialBar"),
    "Relationships and Distributions": ("scatter", "bubble", "boxPlot", "histogram", "rangeBar", "rangeArea", "heatmap"),
    "Hierarchy and Income": ("treemap", "sunburst", "sankey", "waterfall", "funnel", "coneFunnel", "pyramid"),
    "Combinations": ("columnLineCombo", "areaColumnCombo", "customCombo"),
}


def chart_name(chart_type):
    return re.sub(r"([a-z])([A-Z])", r"\1 \2", chart_type).title()


def widget(chart_type, chart, columns):
    title = chart_name(chart_type) + " - " + chart["title"]
    types = {"string": "text", "date": "dateString", "number": "number"}
    # Daily prices use equally spaced trading sessions, not elapsed calendar time.
    chart_types = {"string": "category", "date": "category", "number": "series"}
    widget_id = "qopenbb_gallery_" + chart_type
    return {"widgetId": widget_id, "name": title, "description": chart["title"],
            "category": "Historical Gallery", "subCategory": chart_name(chart_type), "source": ["FMP"],
            "type": "table", "endpoint": "/gallery/data/" + chart["datasetId"], "params": [],
            "gridData": {"w": 20, "h": 18},
            "data": {"dataKey": "results", "table": {"showAll": True, "enableAdvanced": True,
                "columnsDefs": [{"field": col["field"], "headerName": col["label"],
                                 "headerTooltip": col["label"] + "; " + col["unit"],
                                 "cellDataType": types[col["type"]],
                                 "chartDataType": chart_types[col["type"]]} for col in columns]}}}


def tab(name, chart_types, contract, columns):
    width = 40 // columns
    layout = [{"i": "qopenbb_gallery_" + chart_type, "x": (index % columns) * width,
               "y": (index // columns) * 18, "w": width, "h": 18,
               "state": deepcopy(contract["charts"][chart_type]["state"])}
              for index, chart_type in enumerate(chart_types)]
    return {"id": name, "name": name, "layout": layout}


def build_catalog(contract):
    chart_types = {chart for family in FAMILIES.values() for chart in family}
    if chart_types != set(contract["charts"]) or len(chart_types) != 36:
        raise ValueError("chart inventory differs from frozen 36-type contract")
    widgets = {"qopenbb_gallery_" + chart_type: widget(
        chart_type, chart, contract["datasets"][chart["datasetId"]]["columns"])
        for chart_type, chart in contract["charts"].items()}
    tabs = {"Overview": tab("Overview", OVERVIEW, contract, 4)}
    tabs.update({name: tab(name, charts, contract, 2) for name, charts in FAMILIES.items()})
    app = {"name": contract["appName"], "allowCustomization": True,
           "description": "Fixed historical FMP observations: January 2025 prices and reported Apple fiscal quarters. Open family tabs for all 36 chart types.",
           "tabs": tabs}
    return {"schemaVersion": 1, "snapshotId": contract["snapshotId"], "widgets": widgets, "apps": [app]}
