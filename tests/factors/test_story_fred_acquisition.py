"""Exercise cutoff-safe DFII10 evidence through the story acquisition adapter."""

import json
from datetime import UTC, datetime
from decimal import Decimal

import pytest
from qopenbb_data.modeling.contracts import AssumptionSet
from qopenbb_data.modeling.models.factors.real_yield import RealYieldModel
from qopenbb_data.modeling.service.acquisition import AcquisitionError, DataApiSnapshotSource
from qopenbb_data.modeling.service.ports import AcquisitionRequest
from qopenbb_data.modeling.service.story_schedule import REVISION

STAMP = datetime(2026, 11, 26, 12, tzinfo=UTC)


def request():
    return AcquisitionRequest(
        dataset_id="story.dfii10",
        parameters=(("calendar_id", "NYSE_ARCA"), ("schedule_revision", REVISION)),
        cutoff={"observation_date": "2026-11-13", "session_timezone": "America/New_York",
                "decision_at": "2026-11-14T04:59:59Z", "evaluated_at": STAMP},
    )


def assumptions(selection):
    return AssumptionSet(version="1", effective_date="2026-01-01", assumptions=tuple(
        {"assumption_id": key, "value_type": "text", "value": value,
         "origin": "method_default", "rationale": "Use the selected story schedule."}
        for key, value in selection.parameters
    ))


def response(query, rows):
    return {
        "provider": "fred",
        "results": rows,
        "extra": {"results_metadata": {"__qopenbb_financial__": {
            "dataset": "economy.fred_series", "provider": "fred", "retrieved_at": STAMP.isoformat(),
            "source": {"endpoint": "series/observations"},
            "bounds": {"returned_count": len(rows), "truncated": None},
            "effective_query": {key: value for key, value in query.items() if key != "provider"}
            | {"use_cache": False, "limit": 100000, "aggregation_method": "eop"},
            "point_in_time_safe": False, "vintage_query_supported": None,
            "fields": {"DFII10": {
                "unit": "Percent", "source_unit": "Percent", "source_frequency": "Daily",
                "effective_frequency": "Daily", "value_origin": "provider_observation",
            }},
            "observation_provenance": {"DFII10": {
                "2026-08-17": {"realtime_start": "2026-08-18", "realtime_end": "9999-12-31"},
                "2026-11-13": {"realtime_start": "2026-11-16", "realtime_end": "9999-12-31"},
            }},
        }}},
    }


def acquire(rows, selection=None, mutate=lambda *_: None):
    async def read(url, params):
        assert url == "http://test/api/v1/economy/fred_series"
        query = dict(params)
        assert query == {"provider": "fred", "symbol": "DFII10", "start_date": "2026-08-17",
                         "end_date": "2026-11-13", "use_cache": "false"}
        payload = response(query, rows)
        mutate(payload["extra"]["results_metadata"]["__qopenbb_financial__"])
        return json.dumps(payload).encode()

    return DataApiSnapshotSource("http://test", transport=read).acquire(selection or request())


def test_current_fred_values_preserved_but_not_backdated():
    snapshot = acquire([{"date": "2026-08-17", "DFII10": 1.781},
                        {"date": "2026-11-13", "DFII10": 1.921}])
    assert snapshot.schema_id == "real_yield_regime.inputs"
    assert snapshot.provenance.retrieved_at == STAMP
    session, yield_levels = snapshot.tables
    assert len(session.rows) == 64
    assert yield_levels.table_id == "dfii10"
    first, last = yield_levels.rows
    assert first.value == Decimal("1.781") and last.value == Decimal("1.921")
    for row in yield_levels.rows:
        assert row.context.unit == "percent" and row.context.quantity == "rate"
        assert row.entity_id == "DFII10" and row.metric_id == "real_yield"
        assert row.published_at is row.vintage_at is None and row.source_record_id
        assert not snapshot.cutoff.is_eligible(row)
    assert "2026-11-16" in last.context.vintage_limitation
    result = RealYieldModel().calculate(snapshot, assumptions(request()))
    assert all(output.value is None for output in result.outputs)
    assert "unknown historical availability for DFII10 endpoint on 2026-11-13" in result.outputs[0].reason


@pytest.mark.parametrize("rows", [[], [{"date": "2026-08-17", "DFII10": 1.781}]])
def test_missing_endpoint_returns_dated_outcome(rows):
    snapshot = acquire(rows)
    result = RealYieldModel().calculate(snapshot, assumptions(request()))
    assert "missing DFII10 endpoint on 2026-11-13" in result.outputs[0].reason


@pytest.mark.parametrize("mutate", [
    lambda meta: meta["fields"]["DFII10"].update(unit="Percent Change"),
    lambda meta: meta["effective_query"].update(symbol="DGS10"),
    lambda meta: meta["effective_query"].update(start_date="2026-08-18"),
    lambda meta: meta["effective_query"].update(frequency="w"),
    lambda meta: meta.update(point_in_time_safe=True),
    lambda meta: meta["bounds"].update(returned_count=0),
])
def test_mismatched_fred_receipt_rejected(mutate):
    with pytest.raises(AcquisitionError) as caught:
        acquire([{"date": "2026-08-17", "DFII10": 1.781}], mutate=mutate)
    assert caught.value.code == "invalid_response"


@pytest.fixture
def loopback_fred():
    from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
    from threading import Thread

    def acquire_status(status, code=None, *, provider="fred", selection=None):
        class Endpoint(BaseHTTPRequestHandler):
            def do_GET(self):
                assert self.path.startswith("/api/v1/economy/fred_series?")
                self.send_response(status)
                self.end_headers()
                if code:
                    self.wfile.write(json.dumps({"code": code, "provider": provider,
                                                 "detail": "private upstream text"}).encode())

            def log_message(self, *args):
                pass

        with ThreadingHTTPServer(("127.0.0.1", 0), Endpoint) as server:
            thread = Thread(target=server.serve_forever, daemon=True)
            thread.start()
            try:
                source = DataApiSnapshotSource(f"http://127.0.0.1:{server.server_port}")
                return source.acquire(selection or request())
            finally:
                server.shutdown()
                thread.join()

    return acquire_status


@pytest.mark.parametrize("status,code", [(204, None), (400, "missing_data")])
def test_fred_no_observations_have_dated_outcomes_and_local_receipt(loopback_fred, status, code):
    before = datetime.now(UTC)
    snapshot = loopback_fred(status, code)
    query = dict(snapshot.provenance.query)
    assert query["receipt_basis"] == "service_received_at" and query["source_outcome"] == "missing_data"
    assert before <= snapshot.provenance.retrieved_at <= datetime.now(UTC)
    assert not snapshot.tables[-1].rows
    output = RealYieldModel().calculate(snapshot, assumptions(request())).outputs[0]
    assert "missing DFII10 endpoint on 2026-11-13" in output.reason


@pytest.mark.parametrize("status,code,provider,expected", [
    (502, "authentication", "fred", "entitlement"),
    (502, "authentication", None, "entitlement"),
    (400, "authentication", "fred", "entitlement"),
    (502, "timeout", "fred", "timeout"),
    (400, "timeout", "fred", "timeout"),
    (400, "throttling", "fred", "throttling"),
    (502, "throttling", "fred", "throttling"),
    (429, None, None, "throttling"),
    (502, "invalid_response", "fred", "invalid_response"),
    (502, "authentication", "fmp", "upstream"),
    (502, "unexpected", "fred", "upstream"),
])
def test_fred_http_failures_are_allowlisted(loopback_fred, status, code, provider, expected):
    with pytest.raises(AcquisitionError) as caught:
        loopback_fred(status, code, provider=provider)
    assert caught.value.code == expected
    assert "private" not in str(caught.value)


@pytest.mark.parametrize("status,code", [(204, None), (502, "authentication"), (400, "missing_data")])
def test_generic_fred_keeps_legacy_failure_categories(loopback_fred, status, code):
    generic = AcquisitionRequest(dataset_id="economy.fred_series", parameters=(("symbol", "DFII10"),),
                                 cutoff=request().cutoff)
    with pytest.raises(AcquisitionError) as caught:
        loopback_fred(status, code, selection=generic)
    assert caught.value.code == "upstream"
