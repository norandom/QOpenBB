"""Check the frozen Events and Documents worker handoff against Batch B."""

import json
import subprocess
from pathlib import Path

import pytest
from qopenbb_ci.catalog_financial import validate_value

ROOT = Path(__file__).resolve().parents[2]
FIXTURES = Path(__file__).parent / "fixtures/events_documents"


def read(path):
    return json.loads(path.read_bytes())


def test_declaration_and_queries_match_installed_batch_b():
    story = read(FIXTURES / "story.v1.json")
    widgets = read(ROOT / "contracts/widgets.json")
    datasets = {item["id"]: item for item in read(ROOT / "contracts/datasets.json")["datasets"]}
    catalog = story["catalog"]
    assert catalog["widget"]["widgetId"] == catalog["widget"]["type"] == "events_documents_story"
    assert "endpoint" not in catalog["widget"]
    assert list(catalog["bindings"]) == ["calendar", "filings", "transcript", "news"]
    for slot, binding in catalog["bindings"].items():
        widget = widgets[binding["widgetId"]]
        dataset = datasets[binding["dataset"]]
        assert dataset["provider"] == "fmp"
        assert binding["type"] == widget["type"]
        assert binding["route"] == "/data" + dataset["path"] == "/data" + widget["endpoint"]
        assert binding["metadataDataset"] == dataset["path"].removeprefix("/api/v1/")
        assert binding["queryPolicy"] == widget["queryPolicy"]
        assert set(widget["financialContract"]["variants"]) == {"fmp"}
        params = {p["paramName"]: p["value"] for p in widget["params"] if p["value"] is not None}
        assert story["queries"][slot] == {"slot": slot, "parameters": params}
        assert ("symbol" in params) == (widget["data"]["scope"] == "listing")
        choices = story["layout"]["state"]["storage"]["eventsDocuments"]
        assert params == {
            "provider": "fmp", **({"symbol": choices["symbol"]} if slot != "calendar" else {}),
            **choices[slot],
        }


def test_saved_story_config_round_trip():
    story = read(FIXTURES / "story.v1.json")
    layout = story["layout"]
    assert json.loads(json.dumps(layout)) == layout
    assert set(layout) == {"i", "x", "y", "w", "h", "view_order", "state"}
    assert layout["i"] == story["catalog"]["widget"]["widgetId"]
    assert layout["view_order"] == ["question", "calendar", "filings", "transcript", "news", "conclusion"]
    assert {key: layout[key] for key in ("w", "h")} == story["catalog"]["widget"]["gridData"]
    assert layout["state"].keys() == {"storage"}
    assert layout["state"]["storage"].keys() == {"eventsDocuments"}
    saved = layout["state"]["storage"]["eventsDocuments"]
    assert saved.keys() == {"version", "symbol", "calendar", "filings", "transcript", "news", "charts"}
    assert saved["version"] == 1
    assert saved["charts"].keys() == {"eps", "revenue"}
    assert set(saved["charts"].values()) <= {"bar", "point"}


@pytest.mark.parametrize("name", [
    "calendar-duplicate", "filings-empty", "filings-success", "transcript-exact",
    "news-204", "news-failure", "news-success",
])
def test_wire_examples_round_trip_and_match_the_dispatched_binding(name):
    story = read(FIXTURES / "story.v1.json")
    case = read(FIXTURES / "receipts.v1.json")[name]
    assert json.loads(json.dumps(case)) == case
    receipt = case["receipt"]
    scope = receipt["scope"]
    slot = scope["query"]["slot"]
    binding = story["catalog"]["bindings"][slot]
    assert scope["query"] == story["queries"][slot]
    assert scope["dataset"] == binding["dataset"]
    assert scope["route"] == binding["route"]
    assert scope["provider"] == "fmp"
    assert scope["generation"] > 0
    assert receipt["httpStatus"] == case["status"]
    api = read(ROOT / "contracts/openapi.json")
    descriptor = api["paths"][binding["route"].removeprefix("/data")]["get"]["x-qopenbb-financial"]
    params = {k: v for k, v in scope["query"]["parameters"].items() if k != "provider"}
    validate_value(api, descriptor["variants"]["fmp"]["query_schema"], params)
    if case["status"] == 204:
        assert case["body"] is None
        assert receipt == {"status": "empty", "httpStatus": 204, "scope": scope,
                           "providerRetrievedAt": None, "respondedAt": "2026-11-27T09:00:02Z"}
        return
    if case["status"] != 200:
        assert receipt == {"status": "failure", "scope": scope, "httpStatus": 502,
                           "code": "entitlement", "retryable": False}
        validate_value(api, descriptor["error_schema"], case["body"])
        assert {key: case["body"][key] for key in ("code", "retryable")} == {
            key: receipt[key] for key in ("code", "retryable")
        }
        return
    body = case["body"]
    meta = body["extra"]["results_metadata"]["__qopenbb_financial__"]
    validate_value(api, descriptor["metadata_schema"], meta)
    for row in body["results"]:
        validate_value(api, descriptor["variants"]["fmp"]["row_schema"], row)
    assert meta["schema_version"] == 1
    assert meta["provider"] == "fmp"
    assert meta["dataset"] == binding["metadataDataset"]
    assert meta["source"]["endpoint"] == binding["sourceEndpoint"]
    if name == "news-success":
        assert meta["effective_query"] == params | {"start_date": None, "end_date": None}
    else:
        assert meta["effective_query"] == params
    assert len(body["results"]) == meta["bounds"]["returned_count"]
    assert len(body["results"]) <= binding["queryPolicy"]["maxReturnedRows"]
    assert receipt["providerRetrievedAt"] == meta["retrieved_at"]
    assert receipt["status"] == ("success" if body["results"] else "empty")
    if name == "filings-empty":
        assert meta["bounds"]["effective_limit"] == scope["query"]["parameters"]["limit"]
        assert meta["bounds"]["completeness"] == "unknown"
    if name == "calendar-duplicate":
        rows = body["results"]
        assert b'"revenue_actual": 9007199254740993' in (FIXTURES / "receipts.v1.json").read_bytes()
        assert rows[1]["report_date"] == rows[3]["report_date"]
        matches = [i for i, row in enumerate(rows) if row["symbol"] == "AAPL"]
        assert matches == [1, 3]
        assert rows[1]["eps_actual"] == 0 and rows[3]["eps_consensus"] is None
        assert rows[1]["revenue_actual"] == 9007199254740993
        assert receipt["tokens"]["1"]["revenue_actual"] == str(rows[1]["revenue_actual"])
    if name == "filings-success":
        row, = body["results"]
        assert row["content_status"] == "metadata_only"
        assert row["cik"] == "0000320193"
        assert row["filing_url"] != row["report_url"]
        assert row["accepted_date"] == "2026-01-02T16:35:42-05:00"
    if name == "news-success":
        row, = body["results"]
        assert row["content_status"] == "partial"
        assert row["excerpt"] == "  Literal <b>excerpt</b>\n"
        assert row["source"] != row["publisher"]
    if name == "transcript-exact":
        row, = body["results"]
        params = scope["query"]["parameters"]
        assert (row["symbol"], row["year"], row["quarter"]) == (
            params["symbol"], params["year"], f"Q{params['quarter']}",
        )
        assert row["content"] == "  Operator: Hello\n\nCEO: <b>Literal</b>\t\n"
        assert row["event_datetime"] == "2025-01-30T16:35:42-05:00"


def test_candidate_browser_recovers_wire_tokens():
    subprocess.run(["node", str(FIXTURES / "reviver.mjs")], cwd=ROOT, check=True, timeout=45)
