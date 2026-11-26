"""Exercise the story adapter against bounded FMP response envelopes and qualified role bindings."""

import json
from datetime import UTC, datetime

import pytest
from qopenbb_data.modeling.contracts import AssumptionSet
from qopenbb_data.modeling.service.acquisition import (
    AcquisitionError,
    DataApiSnapshotSource,
)
from qopenbb_data.modeling.service.ports import AcquisitionRequest
from qopenbb_data.modeling.service.story_acquisition import validate_story_binding
from qopenbb_data.modeling.service.story_schedule import REVISION

STAMP = datetime(2026, 11, 16, 12, tzinfo=UTC)


def request():
    return AcquisitionRequest(dataset_id="story.etf_pair", parameters=(
        ("left_proxy", "GLD"), ("right_proxy", "VGT"), ("calendar_id", "NYSE_ARCA"),
        ("schedule_revision", REVISION),
    ), cutoff={"observation_date": "2026-11-13", "session_timezone": "America/New_York",
               "decision_at": "2026-11-14T04:59:59Z", "evaluated_at": "2026-11-16T15:00:00Z"})


def response(params):
    query = dict(params)
    assert query.pop("provider") == "fmp"
    metadata = {
        "dataset": "equity/price/historical", "provider": "fmp", "retrieved_at": STAMP.isoformat(),
        "source": {"endpoint": "historical-price-eod/full"}, "effective_query": query,
        "bounds": {"returned_count": 1, "truncated": None, "completeness": "unknown"},
        "point_in_time_safe": False, "fields": {"close": {
            "unit": "currency/share", "scale": 1, "currency": None, "value_origin": "provider_observation",
        }},
    }
    return {"provider": "fmp", "results": [{"date": query["start_date"], "close": 45}],
            "extra": {"results_metadata": {"__qopenbb_financial__": metadata}}}


def acquire(transform, selection=None):
    async def read(url, params):
        assert url == "http://test/api/v1/equity/price/historical"
        body = response(params)
        transform(body, dict(params)["symbol"])
        return json.dumps(body).encode()

    return DataApiSnapshotSource("http://test", transport=read).acquire(selection or request())


@pytest.mark.parametrize("failure", [LookupError, ConnectionError])
def test_source_preserves_other_leg_on_failed_history(failure):
    def lose_right(body, symbol):
        if symbol == "VGT":
            raise failure("private provider text")

    snap = acquire(lose_right)
    sessions, left, right = snap.tables
    assert len(sessions.rows) == 64 and sessions.rows[0].observation_date.isoformat() == "2026-08-17"
    row, = left.rows
    assert row.value == 45 and row.context.currency == "USD" and row.source_record_id
    assert row.published_at is row.vintage_at is None and right.rows == ()
    params = dict(snap.provenance.query)
    assert snap.provenance.retrieved_at == datetime.fromisoformat(params["left_retrieved_at"]) == STAMP
    assert "right_retrieved_at" not in params
    assert params["right_error"] == ("missing_data" if failure is LookupError else "upstream")


@pytest.mark.parametrize("path,value", [
    (("effective_query", "adjustment"), "splits_and_dividends"),
    (("effective_query", "symbol"), "DBC"), (("effective_query", "end_date"), "2026-11-12"),
    (("fields", "close", "currency"), "EUR"), (("source", "endpoint"), "unadjusted"),
    (("point_in_time_safe",), True), (("retrieved_at",), "2025-01-01T01:00:00Z"),
    (("retrieved_at",), "2026-11-13T20:59:59Z"), (("retrieved_at",), "2026-11-16"), (("bounds", "returned_count"), 0),
])
def test_malformed_metadata_is_refused(path, value):
    def corrupt(body, symbol):
        meta = body["extra"]["results_metadata"]["__qopenbb_financial__"]
        for part in path[:-1]:
            meta = meta[part]
        meta[path[-1]] = value
    with pytest.raises(AcquisitionError) as caught:
        acquire(corrupt)
    assert caught.value.code == "invalid_response"


def test_upstream_failure_and_empty_with_receipt_are_distinct():
    def denied(body, symbol):
        raise OSError("private detail")

    with pytest.raises(AcquisitionError) as caught:
        acquire(denied)
    assert caught.value.code == "upstream"

    def empty(body, symbol):
        if symbol == "VGT":
            body["results"] = []
            body["extra"]["results_metadata"]["__qopenbb_financial__"]["bounds"]["returned_count"] = 0

    snap = acquire(empty)
    assert snap.tables[-1].rows == ()
    assert "right_retrieved_at" in dict(snap.provenance.query)


def test_model_and_assumptions_validated_before_acquisition():
    assumptions = AssumptionSet(version="1", effective_date="2026-01-01")
    for key in (("proxy_comparison", "1"), ("real_yield_regime", "1"), ("proxy_comparison", "2")):
        with pytest.raises(AcquisitionError) as caught:
            validate_story_binding(key, request(), assumptions)
        assert caught.value.code == "invalid_request"


def test_corrupt_single_leg_retains_independent_history():
    def wrong_symbol(body, symbol):
        if symbol == "GLD":
            body["results"][0]["symbol"] = "XLK"

    snap = acquire(wrong_symbol)
    params = dict(snap.provenance.query)
    assert params["left_error"] == "invalid_response"
    assert "left_retrieved_at" not in params
    assert snap.tables[1].rows == () and snap.tables[2].rows[0].value == 45


@pytest.mark.parametrize("date,decision,sessions", [
    ("2026-11-14", "2026-11-15T04:59:59Z", 0),
    ("2026-01-05", "2026-01-06T04:59:59Z", 2),
])
def test_window_boundary_keeps_selected_cutoff(date, decision, sessions):
    selection = request().model_dump(mode="json")
    selection["cutoff"].update(observation_date=date, decision_at=decision)
    snap = acquire(lambda *_: None, AcquisitionRequest.model_validate(selection))
    assert snap.cutoff.observation_date.isoformat() == date
    assert len(snap.tables[0].rows) == sessions


def test_disjoint_price_coverage_evaluates_each_window_without_bridging():
    from datetime import date
    from pathlib import Path

    from qopenbb_data.modeling.models.factors.retrospective import RetrospectiveComparisonModel
    from qopenbb_data.modeling.service.story_schedule import story_sessions
    from qopenbb_data.modeling.verification.factors.retrospective_reference import retrospective_reference

    example = Path(__file__).resolve().parents[2] / "contracts/consumers/research-stories/runs.v1.json"
    raw_assumptions = json.loads(example.read_bytes())["requests"]["comparison"]["assumptions"]
    params = dict(request().parameters)
    for item in raw_assumptions["assumptions"]:
        item["value"] = params.get(item["assumption_id"], item["value"])
    assumptions = AssumptionSet.model_validate(raw_assumptions)

    def selected(day, decision):
        raw = request().model_dump(mode="json")
        raw["cutoff"].update(observation_date=day, decision_at=decision)
        return AcquisitionRequest.model_validate(raw)

    first = selected("2026-07-31", "2026-08-01T03:59:59Z")
    gap = selected("2026-08-07", "2026-08-08T03:59:59Z")
    last = request()
    available = []
    for selection in (first, last):
        table = story_sessions(selection.cutoff, "NYSE_ARCA", REVISION)
        available.extend(row.observation_date for row in table.rows)
    assert len(available) == len(set(available)) == 128

    def return_window(body, symbol):
        meta = body["extra"]["results_metadata"]["__qopenbb_financial__"]
        query = meta["effective_query"]
        start, end = (date.fromisoformat(query[key]) for key in ("start_date", "end_date"))
        denominator = 100 if symbol == "GLD" else 200
        body["results"] = [
            {"date": day.isoformat(), "close": denominator + index}
            for index, day in enumerate(available) if start <= day <= end
        ]
        meta["bounds"]["returned_count"] = len(body["results"])

    for selection in (first, gap, last):
        snapshot = acquire(return_window, selection)
        outcomes = RetrospectiveComparisonModel().calculate(snapshot, assumptions).outputs
        spread = next(item for item in outcomes if item.output_id == "momentum_spread")
        assert retrospective_reference().calculations["momentum_spread"](snapshot, assumptions) == spread.value
        if selection == gap:
            assert spread.value is None
            assert "2026-08-" in spread.reason
        else:
            assert spread.value > 0
            assert all(len(table.rows) == 64 for table in snapshot.tables)


def test_both_denied_http_response_and_pre_io_validation(tmp_path):
    import asyncio
    from pathlib import Path

    from qopenbb_data.modeling.service.acquisition_http import ProviderDenied
    from qopenbb_data.modeling.service.bootstrap import installed_methods
    from qopenbb_data.modeling.service.http import create_model_app
    from qopenbb_data.modeling.service.orchestrator import Orchestrator
    from qopenbb_data.modeling.service.run_store import FileRunStore
    from test_model_http import Verifier, call

    symbols = []

    async def deny(url, params):
        symbols.append(dict(params)["symbol"])
        raise ProviderDenied("private data API details")

    registry, bindings = installed_methods()
    source = DataApiSnapshotSource("http://test", transport=deny)
    service = Orchestrator(registry, bindings, FileRunStore(tmp_path), snapshot_source=source)
    app = create_model_app(service, registry, Verifier())
    example = Path(__file__).resolve().parents[2] / "contracts/consumers/research-stories/runs.v1.json"
    payload = json.loads(example.read_bytes())["requests"]["comparison"]
    selection = request()
    payload["acquisition"] = selection.model_dump(mode="json")
    params = dict(selection.parameters)
    for item in payload["assumptions"]["assumptions"]:
        if item["assumption_id"] in params:
            item["value"] = params[item["assumption_id"]]

    def evaluate():
        return asyncio.run(call(app, "/evaluations", body=json.dumps(payload).encode()))

    status, body = evaluate()
    assert symbols == ["GLD", "VGT"]
    assert status == 422 and body["retryable"] is False
    assert body["code"] == "unsupported_acquisition"
    assert body["fields"] == [{"path": ["acquisition"], "code": "entitlement"}]
    assert "private" not in str(body)

    payload["assumptions"]["assumptions"][0]["value"] = "VGT"
    assert evaluate()[0] == 422
    payload["method_version"] = "1"
    assert evaluate()[0] == 422
    assert symbols == ["GLD", "VGT"]


@pytest.mark.parametrize("status,code,expected", [
    (204, None, "missing_data"), (403, None, "entitlement"), (502, "entitlement", "entitlement"),
    (400, "throttling", "throttling"), (400, "timeout", "timeout"), (502, "invalid_response", "invalid_response"),
    (502, "private-unexpected", "upstream"),
])
def test_http_worker_classifies_fmp_failure(status, code, expected):
    from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
    from threading import Thread

    class Endpoint(BaseHTTPRequestHandler):
        def do_GET(self):
            if "symbol=GLD" in self.path:
                self.send_response(status)
                self.end_headers()
                if code:
                    self.wfile.write(json.dumps({"code": code, "provider": "fmp", "detail": "private"}).encode())
                return
            from urllib.parse import parse_qsl, urlsplit

            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps(response(parse_qsl(urlsplit(self.path).query))).encode())

        def log_message(self, *args):
            pass

    with ThreadingHTTPServer(("127.0.0.1", 0), Endpoint) as server:
        thread = Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            snapshot = DataApiSnapshotSource(f"http://127.0.0.1:{server.server_port}").acquire(request())
        finally:
            server.shutdown()
            thread.join()
    params = dict(snapshot.provenance.query)
    assert params["left_error"] == expected
    assert "left_retrieved_at" not in params and "right_retrieved_at" in params
