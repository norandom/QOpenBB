"""Native catalog shape, coverage, layout and saved assignment invariants."""
from copy import deepcopy
import json
from pathlib import Path

import pytest

from qopenbb_ci.gallery_cli import canonical
from qopenbb_ci.gallery_templates import OVERVIEW, build_catalog, chart_name

ROOT = Path(__file__).resolve().parents[2]
CONTRACT = json.loads((ROOT / "contracts/gallery/chart-state.json").read_text())
CATALOG = json.loads((ROOT / "contracts/gallery/catalog.json").read_text())


def test_generated_catalog_matches_checked_in_bytes_and_contract_unchanged():
    before = deepcopy(CONTRACT)
    assert canonical(build_catalog(CONTRACT)) == (ROOT / "contracts/gallery/catalog.json").read_bytes()
    assert CONTRACT == before
    assert set(CATALOG) == {"schemaVersion", "snapshotId", "widgets", "apps"}
    assert CATALOG["schemaVersion"] == 1 and CATALOG["snapshotId"] == CONTRACT["snapshotId"]


def test_widgets_cover_exactly_36_native_charts_with_typed_columns():
    widgets = CATALOG["widgets"]
    assert set(widgets) == {"qopenbb_gallery_" + chart for chart in CONTRACT["charts"]}
    assert len(widgets) == 36
    for chart_type, chart in CONTRACT["charts"].items():
        widget = widgets["qopenbb_gallery_" + chart_type]
        assert widget["widgetId"] == "qopenbb_gallery_" + chart_type
        assert chart_name(chart_type) in widget["name"] and chart["title"] in widget["name"]
        assert widget["type"] == "table" and widget["params"] == []
        assert widget["endpoint"] == "/gallery/data/" + chart["datasetId"]
        assert widget["data"]["dataKey"] == "results"
        columns = widget["data"]["table"]["columnsDefs"]
        expected = CONTRACT["datasets"][chart["datasetId"]]["columns"]
        assert [c["field"] for c in columns] == [c["field"] for c in expected]
        assert [c["headerName"] for c in columns] == [c["label"] for c in expected]
        types = {"number": "number", "date": "dateString", "string": "text"}
        assert [c["cellDataType"] for c in columns] == [types[c["type"]] for c in expected]
        chart_types = {"number": "series", "date": "category", "string": "category"}
        assert [c["chartDataType"] for c in columns] == [chart_types[c["type"]] for c in expected]


def test_overview_is_four_columns_three_rows_and_families_cover_every_type():
    app, = CATALOG["apps"]
    assert app["name"] == "QOpenBB Historical Chart Gallery - January 2025"
    assert app["allowCustomization"] is True
    assert next(iter(app["tabs"])) == "Overview"
    overview = app["tabs"]["Overview"]["layout"]
    assert [row["i"] for row in overview] == ["qopenbb_gallery_" + x for x in OVERVIEW]
    assert len(overview) == 12 and {row["x"] for row in overview} == {0, 10, 20, 30}
    assert {row["y"] for row in overview} == {0, 18, 36}
    assert all(row["w"] == 10 and row["h"] == 18 for row in overview)
    family_ids = [row["i"] for name, tab in app["tabs"].items() if name != "Overview" for row in tab["layout"]]
    assert len(family_ids) == len(set(family_ids)) == 36
    assert set(family_ids) == set(CATALOG["widgets"])


def test_all_layouts_copy_frozen_native_states_without_instance_ids_or_invention():
    for tab in CATALOG["apps"][0]["tabs"].values():
        for row in tab["layout"]:
            chart_type = row["i"].removeprefix("qopenbb_gallery_")
            assert row["state"] == CONTRACT["charts"][chart_type]["state"]
    catalog = build_catalog(CONTRACT)
    a = catalog["apps"][0]["tabs"]["Overview"]["layout"][0]["state"]
    a["chartView"]["enabled"] = False
    line = catalog["apps"][0]["tabs"]["Lines and Areas"]["layout"][0]["state"]
    assert line["chartView"]["enabled"] is True
    assert CONTRACT["charts"]["line"]["state"]["chartView"]["enabled"] is True


def test_sensitive_family_assignments_are_preserved():
    states = {row["i"].removeprefix("qopenbb_gallery_"): row["state"]
              for tab in CATALOG["apps"][0]["tabs"].values() for row in tab["layout"]}
    sankey = states["sankey"]
    assert "chartModel" not in sankey
    assert sankey["storage"]["default"]["sankey"]["sankeySetup"]["sourceColumnId"] == "source"
    for preset in ("columnLineCombo", "areaColumnCombo"):
        assert "seriesChartTypes" not in states[preset]["chartModel"]
    assignments = states["customCombo"]["chartModel"]["seriesChartTypes"]
    assert [(s["colId"], s["secondaryAxis"]) for s in assignments] == [("revenue", False), ("netIncome", False), ("basicEps", True)]
    for chart in ("histogram", "rangeArea"):
        assert states[chart]["filterModel"]["default"]["symbol"]["filter"] == "AAPL"


def test_inventory_mismatch_fails():
    contract = deepcopy(CONTRACT)
    del contract["charts"]["customCombo"]
    with pytest.raises(ValueError, match="inventory"):
        build_catalog(contract)


def test_financial_titles_use_native_family_buckets_after_common_replacement():
    families = {
        "bar": "groupedColumn stackedColumn normalizedColumn groupedBar stackedBar normalizedBar",
        "line": "line stackedLine normalizedLine",
        "area": "area stackedArea normalizedArea",
        "radar-line": "radarLine", "radar-area": "radarArea",
        "radial-column": "radialColumn", "radial-bar": "radialBar",
        "box-plot": "boxPlot", "range-bar": "rangeBar", "range-area": "rangeArea",
        "cone-funnel": "coneFunnel",
    }
    buckets = {chart: [family] for family, charts in families.items() for chart in charts.split()}
    for chart_type, chart in CONTRACT["charts"].items():
        state = chart["state"]
        model = state.get("chartModel") or state["storage"]["default"]["chartModel"]
        options = deepcopy(model["chartOptions"])
        # Native composition replaces common with generated axes before family selection.
        options["common"] = {"axes": {}}
        expected = ["area", "bar", "line"] if chart_type.endswith("Combo") else buckets.get(chart_type, [chart_type])
        for family in expected:
            assert options[family]["title"] == {"enabled": True, "text": chart["title"]}
        assert "title" not in model["chartOptions"].get("common", {})
    assert CONTRACT["charts"]["histogram"]["state"]["chartModel"]["chartOptions"]["histogram"]["series"]["bins"]


def test_price_dates_are_admitted_as_equally_spaced_trading_categories():
    for chart_type in ("line", "area"):
        chart = CONTRACT["charts"][chart_type]
        model = chart["state"]["chartModel"]
        columns = CATALOG["widgets"]["qopenbb_gallery_" + chart_type]["data"]["table"]["columnsDefs"]
        admitted = [col["field"] for col in columns if col["chartDataType"] in ("category", "series")]
        assert admitted[0] == "date" and "date" in model["cellRange"]["columns"]
        assert columns[0]["cellDataType"] == "dateString"
        assert model["categoryAxisType"] == "category"
        assert "qopenbbAxisSettings" not in model
