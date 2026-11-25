"""Exercise the published FRED wire shape using mocked HTTP transport."""

import asyncio
import json
from datetime import UTC, date, datetime, timedelta
from decimal import Decimal
from threading import Event
from time import monotonic

import pytest
from qopenbb_data.modeling.contracts import EvaluationCutoff
from qopenbb_data.modeling.service.acquisition import (
    AcquisitionError,
    DataApiSnapshotSource,
)
from qopenbb_data.modeling.service.ports import AcquisitionRequest

DATASET = "economy.fred_series"
BASE_URL = "http://data-api:8000"
CUTOFF = EvaluationCutoff(
    observation_date="2024-04-01",
    decision_at="2024-04-01T16:00:00Z",
    evaluated_at="2024-04-01T16:00:00Z",
    session_timezone="UTC",
)
RESPONSE = b'''{
    "provider":"fred",
    "results":[{"date":"2024-01-01","GDP":28624.069},{"date":"2024-04-01","GDP":null}],
    "extra":{"results_metadata":{"GDP":{"frequency":"Quarterly","units":"Billions of Dollars",
                                       "seasonal_adjustment":"Seasonally Adjusted Annual Rate"}}}
}'''


def request(**overrides):
    fields = {"dataset_id": DATASET, "parameters": (("symbol", "GDP"),), "cutoff": CUTOFF}
    return AcquisitionRequest(**(fields | overrides))


def test_published_fred_mapping_and_refresh():
    calls = []

    async def transport(url, params):
        calls.append((url, dict(params)))
        return RESPONSE

    adapter = DataApiSnapshotSource(BASE_URL, transport=transport)
    before = datetime.now(UTC)
    snapshot = adapter.acquire(request(parameters=(("symbol", "gdp"),)))
    refreshed = adapter.acquire(request())
    assert calls == [(BASE_URL + "/api/v1/economy/fred_series", {
        "provider": "fred", "symbol": "GDP", "end_date": "2024-04-01", "use_cache": "false",
    })] * 2
    assert snapshot.provenance.origin == "service_acquired"
    assert snapshot.provenance.source == "fred"
    assert dict(snapshot.provenance.query) == calls[0][1]
    assert before <= snapshot.provenance.retrieved_at <= datetime.now(UTC)
    assert snapshot.provenance.acquisition_id != refreshed.provenance.acquisition_id
    assert snapshot.cutoff == CUTOFF
    table, = snapshot.tables
    assert snapshot.schema_id == table.table_id == DATASET
    assert table.keys == ("entity_id", "metric_id", "observation_date")
    first, missing = table.rows
    assert first.entity_id == first.metric_id == "GDP"
    assert first.category == "provider"
    assert first.value == Decimal("28624.069")
    assert first.context.unit == "Billions of Dollars"
    assert first.context.frequency == "Quarterly"
    assert first.context.seasonal_adjustment == "Seasonally Adjusted Annual Rate"
    assert first.context.vintage_coverage == "unavailable"
    assert first.published_at is first.vintage_at is first.source_record_id is None
    assert first.transformations[0].transformation_id == "fred.wide_to_observations"
    assert missing.value is None
    assert not CUTOFF.is_eligible(first)


@pytest.mark.parametrize("fields", [
    {"dataset_id": "https://secret.invalid"},
    {"parameters": ()},
    {"parameters": (("symbol", "GDP"), ("symbol", "CPI"))},
    {"parameters": (("symbol", "GDP"), ("provider", "secret"))},
    {"parameters": (("symbol", "GDP,CPI"),)},
    {"parameters": (("symbol", "date"),)},
])
def test_invalid_request_fails_before_transport(fields):
    async def transport(url, params):
        pytest.fail("invalid requests must fail before transport")

    with pytest.raises(AcquisitionError) as caught:
        DataApiSnapshotSource(BASE_URL, transport=transport).acquire(request(**fields))
    assert caught.value.code == "invalid_request"
    assert "secret" not in str(caught.value)


@pytest.mark.parametrize("body,code", [
    (b"secret HTML", "invalid_response"),
    (RESPONSE.replace(b'"fred"', b'"other"'), "invalid_response"),
    (RESPONSE.replace(b"28624.069", b"true"), "invalid_response"),
    (RESPONSE.replace(b"28624.069", b"NaN"), "invalid_response"),
    (RESPONSE.replace(b'"Billions of Dollars"', b"false"), "invalid_response"),
    (RESPONSE.replace(b"2024-04-01", b"2024-04-02"), "invalid_response"),
    (RESPONSE.replace(b"2024-04-01", b"2024-01-01"), "invalid_response"),
    (b'{"provider":"fred","results":[]}', "missing_data"),
])
def test_response_failure_is_safe(body, code):
    async def transport(url, params):
        return body

    with pytest.raises(AcquisitionError) as caught:
        DataApiSnapshotSource(BASE_URL, transport=transport).acquire(request())
    assert caught.value.code == code
    assert "secret" not in str(caught.value)
    assert caught.value.__context__ is caught.value.__cause__ is None


def test_response_with_no_metadata_retains_unknowns_and_decimal_precision():
    async def transport(url, params):
        return b'{"provider":"fred","results":[{"date":"2024-01-01","GDP":1.234567890123456789}]}'

    row = DataApiSnapshotSource(BASE_URL, transport=transport).acquire(request()).tables[0].rows[0]
    assert row.value == Decimal("1.234567890123456789")
    assert row.context.unit == "unknown"
    assert row.context.frequency is row.context.seasonal_adjustment is None


def test_transport_failure_discards_raw_exception():
    async def transport(url, params):
        raise OSError("secret URL")

    with pytest.raises(AcquisitionError) as caught:
        DataApiSnapshotSource(BASE_URL, transport=transport).acquire(request())
    assert caught.value.code == "upstream"
    assert caught.value.__context__ is caught.value.__cause__ is None


def test_deadline_cancels_transport():
    closed = False

    async def transport(url, params):
        nonlocal closed
        try:
            await asyncio.sleep(30)
        finally:
            closed = True

    with pytest.raises(AcquisitionError) as caught:
        DataApiSnapshotSource(BASE_URL, timeout_seconds=0.5, transport=transport).acquire(request())
    assert caught.value.code == "timeout"
    assert closed


def test_date_only_realtime_interval_is_retained_without_claiming_availability():
    async def transport(url, params):
        return b'''{
            "provider":"fred",
            "results":[{"date":"2024-01-01","GDP":28624.069}],
            "extra":{"results_metadata":{"__qopenbb_financial__":{"observation_provenance":{
                "GDP":{"2024-01-01":{"realtime_start":"2025-01-01","realtime_end":"2025-01-02"}}
            }}}}
        }'''

    row = DataApiSnapshotSource(BASE_URL, transport=transport).acquire(request()).tables[0].rows[0]
    assert "2025-01-01" in row.context.vintage_limitation
    assert "2025-01-02" in row.context.vintage_limitation
    assert row.context.vintage_coverage == "unavailable"
    assert row.vintage_at is row.published_at is None
    assert not CUTOFF.is_eligible(row)


def test_default_transport_kills_and_reaps_worker_on_deadline(monkeypatch):
    class Worker:
        returncode = None
        killed = False
        reaped = False

        async def communicate(self):
            if not self.killed:
                await asyncio.sleep(30)
            self.returncode = -9
            self.reaped = True
            return b"", None

        def kill(self):
            self.killed = True

    worker = Worker()

    async def start(*args, **kwargs):
        assert args[2] == "qopenbb_data.modeling.service.acquisition_http"
        return worker

    monkeypatch.setattr(asyncio, "create_subprocess_exec", start)
    with pytest.raises(AcquisitionError) as caught:
        DataApiSnapshotSource(BASE_URL, timeout_seconds=0.01).acquire(request())
    assert caught.value.code == "timeout"
    assert worker.killed and worker.reaped


@pytest.mark.parametrize("code", ["timeout", "cancelled"])
def test_closed_evaluation_budget_prevents_transport(code):
    async def transport(url, params):
        pytest.fail("closed evaluation must not start transport")

    cancel = Event()
    if code == "cancelled":
        cancel.set()
    deadline = monotonic() - 1 if code == "timeout" else monotonic() + 10
    with pytest.raises(AcquisitionError) as caught:
        DataApiSnapshotSource(BASE_URL, transport=transport).acquire(
            request(), deadline=deadline, cancel=cancel,
        )
    assert caught.value.code == code


def test_outer_deadline_shortens_active_acquisition():
    closed = False

    async def transport(url, params):
        nonlocal closed
        try:
            await asyncio.sleep(1)
        finally:
            closed = True

    source = DataApiSnapshotSource(BASE_URL, transport=transport)
    with pytest.raises(AcquisitionError) as caught:
        source.acquire(request(), deadline=monotonic() + 0.05)
    assert caught.value.code == "timeout"
    assert closed


def test_evaluation_cancellation_kills_and_reaps_default_worker(monkeypatch):
    cancel = Event()

    class Worker:
        returncode = None
        killed = False

        async def communicate(self):
            if not self.killed:
                asyncio.get_running_loop().call_soon(cancel.set)
                await asyncio.sleep(1)
            self.returncode = -9
            return b"", None

        def kill(self):
            self.killed = True

    worker = Worker()

    async def start(*args, **kwargs):
        return worker

    monkeypatch.setattr(asyncio, "create_subprocess_exec", start)
    with pytest.raises(AcquisitionError) as caught:
        DataApiSnapshotSource(BASE_URL).acquire(request(), cancel=cancel)
    assert caught.value.code == "cancelled"
    assert worker.killed and worker.returncode == -9


@pytest.fixture
def full_fred_response():
    first_date = date(1990, 1, 1)
    return json.dumps({
        "provider": "fred",
        "results": [
            {"date": (first_date + timedelta(days=offset)).isoformat(), "GDP": 123.45}
            for offset in range(10_000)
        ],
    }).encode()


def test_large_mapping_stops_near_short_evaluation_deadline(full_fred_response):
    async def transport(url, params):
        return full_fred_response

    source = DataApiSnapshotSource(BASE_URL, transport=transport)
    started = monotonic()
    with pytest.raises(AcquisitionError) as caught:
        source.acquire(request(), deadline=started + 0.05)
    assert caught.value.code == "timeout"
    assert monotonic() - started < 0.2


def test_cancellation_during_mapping_stops_row_construction(full_fred_response, monkeypatch):
    from qopenbb_data.modeling.service import acquisition

    cancel = Event()
    build_row = acquisition._fred_row
    row_count = 0

    def cancelling_row(*args):
        nonlocal row_count
        row_count += 1
        if row_count == 20:
            cancel.set()
        return build_row(*args)

    async def transport(url, params):
        return full_fred_response

    monkeypatch.setattr(acquisition, "_fred_row", cancelling_row)
    with pytest.raises(AcquisitionError) as caught:
        DataApiSnapshotSource(BASE_URL, transport=transport).acquire(request(), cancel=cancel)
    assert caught.value.code == "cancelled"
    assert row_count == 20


def test_full_mapping_preserves_snapshot_contract(full_fred_response):
    async def transport(url, params):
        return full_fred_response

    snapshot = DataApiSnapshotSource(BASE_URL, transport=transport).acquire(request())
    assert len(snapshot.tables[0].rows) == 10_000
    assert type(snapshot).model_validate(snapshot) == snapshot


def test_cancellation_during_json_decode_stops_parser(full_fred_response, monkeypatch):
    cancel = Event()
    loads = json.loads
    parsed_numbers = 0

    def cancelling_loads(body, *, parse_float, **kwargs):
        def parse_number(token):
            nonlocal parsed_numbers
            parsed_numbers += 1
            if parsed_numbers == 20:
                cancel.set()
            return parse_float(token)

        return loads(body, parse_float=parse_number, **kwargs)

    async def transport(url, params):
        return full_fred_response

    monkeypatch.setattr(json, "loads", cancelling_loads)
    with pytest.raises(AcquisitionError) as caught:
        DataApiSnapshotSource(BASE_URL, transport=transport).acquire(request(), cancel=cancel)
    assert caught.value.code == "cancelled"
    assert parsed_numbers == 20
