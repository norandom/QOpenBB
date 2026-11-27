"""Check the Events and Documents declaration against the frozen consumer example."""
import json
from pathlib import Path

import pytest
from qopenbb_ci.catalog import generate
from qopenbb_ci.catalog_events_documents import events_documents_app

ROOT = Path(__file__).resolve().parents[2]
EXAMPLE = json.loads((ROOT / "tests/contracts/fixtures/events_documents/story.v1.json").read_text())


def read(name):
    return json.loads((ROOT / "contracts" / name).read_text())


def inputs():
    inventory = read("datasets.json")
    report = read("catalog-report.json")
    widgets = read("widgets.json")
    raw = {item["widget"]: widgets[item["widget"]] for item in report["mapping"]}
    return read("openapi.json"), inventory, raw


def assert_story(outputs):
    widget = EXAMPLE["catalog"]["widget"]
    assert outputs["widgets.json"][widget["widgetId"]] == widget
    app, = [app for app in outputs["apps.json"] if app["name"] == widget["name"]]
    assert app["description"] == widget["description"]
    tab, = app["tabs"].values()
    assert tab["layout"] == [EXAMPLE["layout"]]
    for binding in EXAMPLE["catalog"]["bindings"].values():
        source = outputs["widgets.json"][binding["widgetId"]]
        assert "/data" + source["endpoint"] == binding["route"]
        assert source["type"] == binding["type"]
        assert source["endpoint"].removeprefix("/api/v1/") == binding["metadataDataset"]
        assert source["financialContract"]["providers"] == ["fmp"]
        assert source["queryPolicy"] == binding["queryPolicy"]


def test_story_is_generated_once_and_checked_in():
    schema, inventory, raw = inputs()
    assert_story(generate(schema, inventory, raw, [], "/data"))
    assert_story({name: read(name) for name in ("widgets.json", "apps.json")})


@pytest.mark.parametrize("slot", EXAMPLE["catalog"]["bindings"])
def test_missing_source_widget_fails_generation(slot):
    _, inventory, raw = inputs()
    missing_id = EXAMPLE["catalog"]["bindings"][slot]["dataset"]
    mapping = [item for item in read("catalog-report.json")["mapping"] if item["dataset"] != missing_id]
    with pytest.raises(ValueError, match="Missing Events and Documents bindings"):
        events_documents_app(inventory, mapping, raw)


@pytest.mark.parametrize("mutation", ["route", "alias", "source", "variant", "policy"])
def test_foreign_calendar_fails_admission(mutation):
    _, inventory, raw = inputs()
    mapping = read("catalog-report.json")["mapping"]
    binding = EXAMPLE["catalog"]["bindings"]["calendar"]
    widget = raw[binding["widgetId"]]
    if mutation == "route":
        widget["endpoint"] += "/foreign"
    elif mutation == "alias":
        widget["widgetId"] = "alias_fmp_obb"
    elif mutation == "source":
        widget["source"] = ["FRED"]
    elif mutation == "variant":
        widget["financialContract"]["variants"]["fred"] = {}
    else:
        widget["queryPolicy"]["dateWindow"]["maxInclusiveDays"] = 8
    with pytest.raises(ValueError, match="accepted FMP declaration: calendar"):
        events_documents_app(inventory, mapping, raw)
    assert EXAMPLE["catalog"]["widget"]["widgetId"] not in raw


def test_existing_declaration_defaults_seed_independent_choices():
    _, inventory, raw = inputs()
    mapping = read("catalog-report.json")["mapping"]
    filings = next(dataset for dataset in inventory["datasets"] if dataset["id"] == "fmp_company_filings")
    filings["parameters"].update(page=2, limit=50)
    app, = events_documents_app(inventory, mapping, raw)
    defaults = app["tabs"]["Research"]["layout"][0]["state"]["storage"]["eventsDocuments"]
    expected = EXAMPLE["layout"]["state"]["storage"]["eventsDocuments"]
    assert defaults == {**expected, "filings": {**expected["filings"], "page": 2, "limit": 50}}


@pytest.mark.parametrize(("symbols", "expected"), [
    (("A/B", "A/B", "A/B"), None),
    (("brk.b", "BRK.B", "Brk.b"), "BRK.B"),
])
def test_public_generation_requires_one_canonical_listing(symbols, expected):
    schema, inventory, raw = inputs()
    listings = {
        EXAMPLE["catalog"]["bindings"][slot]["dataset"]: symbol
        for slot, symbol in zip(("filings", "transcript", "news"), symbols, strict=True)
    }
    for dataset in inventory["datasets"]:
        if dataset["id"] in listings:
            dataset["parameters"]["symbol"] = listings[dataset["id"]]

    if expected is None:
        with pytest.raises(ValueError, match="default listing"):
            generate(schema, inventory, raw, [], "/data")
        return

    outputs = generate(schema, inventory, raw, [], "/data")
    app, = [app for app in outputs["apps.json"] if app["name"] == EXAMPLE["catalog"]["widget"]["name"]]
    layout, = app["tabs"]["Research"]["layout"]
    assert layout["state"]["storage"]["eventsDocuments"]["symbol"] == expected
