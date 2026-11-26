"""Verify authenticated story selection and acquisition bounds."""

import asyncio
import json
from datetime import date, timedelta
from pathlib import Path
from threading import Event
from time import monotonic

import pytest
from qopenbb_data.modeling.service.acquisition import AcquisitionError, DataApiSnapshotSource
from qopenbb_data.modeling.service.acquisition_http import MAX_RESPONSE_BYTES
from qopenbb_data.modeling.service.bootstrap import installed_methods
from qopenbb_data.modeling.service.http import create_model_app
from qopenbb_data.modeling.service.identity import IdentityVerifier
from qopenbb_data.modeling.service.orchestrator import Orchestrator
from qopenbb_data.modeling.service.run_store import FileRunStore
from qopenbb_data.modeling.service.story_schedule import REVISION
from test_model_http import call
from test_model_identity import ENV, assertion
from test_story_acquisition import request as pair_request
from test_story_acquisition import response

EXAMPLES = Path(__file__).resolve().parents[2] / "contracts/consumers/research-stories/runs.v1.json"


def selection(name):
    payload = json.loads(EXAMPLES.read_bytes())["requests"][name]
    for entry in payload["acquisition"]["parameters"]:
        if entry[0] == "schedule_revision":
            entry[1] = REVISION
    for item in payload["assumptions"]["assumptions"]:
        if item["assumption_id"] == "schedule_revision":
            item["value"] = REVISION
    payload["acquisition"]["cutoff"] = pair_request().cutoff.model_dump(mode="json")
    return payload


@pytest.fixture
def evaluation(monkeypatch, tmp_path):
    for key, value in ENV.items():
        monkeypatch.setenv(key, value)
    calls = []
    fault = {}

    async def transport(url, params):
        body = response(params)
        query = dict(params)
        metadata = body["extra"]["results_metadata"]["__qopenbb_financial__"]
        start, end = (date.fromisoformat(query[key]) for key in ("start_date", "end_date"))
        days = (start + timedelta(days=offset) for offset in range((end - start).days + 1))
        base = 100 if query["symbol"] in {"DBC", "GLD"} else 200
        body["results"] = [
            {"date": day.isoformat(), "close": base + (day - start).days}
            for day in days if day.weekday() < 5 and day.isoformat() != "2026-09-07"
        ]
        metadata["bounds"]["returned_count"] = len(body["results"])
        if query["symbol"] == "XLK":
            if fault.get("receipt"):
                metadata.pop("retrieved_at")
            if fault.get("basis"):
                metadata["effective_query"]["adjustment"] = "splits_and_dividends"
        return json.dumps(body).encode()

    class TrackingSource(DataApiSnapshotSource):
        def acquire(self, request, **kwargs):
            calls.append(request.dataset_id)
            return super().acquire(request, **kwargs)

    registry, bindings = installed_methods()
    source = TrackingSource("http://test", transport=transport)
    service = Orchestrator(registry, bindings, FileRunStore(tmp_path), snapshot_source=source)
    app = create_model_app(service, registry, IdentityVerifier.from_env())

    def exchange(path, payload=None, owner="story_analyst"):
        body = json.dumps(payload).encode() if payload is not None else None
        return asyncio.run(call(app, path, body=body, token=assertion(claims={"sub": owner})))

    return exchange, calls, fault


@pytest.mark.parametrize("name,change", [
    ("comparison", "reverse_assumptions"), ("comparison", "wrong_calendar"),
    ("comparison", "wrong_revision"), ("comparison", "outside_coverage"),
    ("comparison", "early_decision"), ("comparison", "early_evaluation"),
    ("comparison", "wrong_timezone"), ("comparison", "legacy_model"),
    ("comparison", "wrong_dataset"), ("regime", "wrong_dataset"),
    ("regime", "legacy_model"), ("regime", "duplicate_parameter"),
    ("regime", "extra_parameter"), ("regime", "wrong_calendar"),
    ("regime", "wrong_revision"), ("regime", "wrong_assumption"),
    ("regime", "early_decision"), ("comparison", "cross_dataset"),
    ("regime", "cross_dataset"), ("comparison", "duplicate_parameter"),
    ("comparison", "extra_parameter"), ("regime", "wrong_assumption_type"),
    ("regime", "future_assumptions"), ("regime", "wrong_assumptions_version"),
    ("regime", "extra_assumption"), ("comparison", "reversed_roles"),
])
def test_rejected_before_calling_source(evaluation, name, change):
    exchange, calls, _ = evaluation
    payload = selection(name)
    request = payload["acquisition"]
    assumptions = {item["assumption_id"]: item for item in payload["assumptions"]["assumptions"]}
    if change == "reverse_assumptions":
        assumptions["left_proxy"]["value"], assumptions["right_proxy"]["value"] = "XLK", "DBC"
    elif change == "reversed_roles":
        for param in request["parameters"]:
            if param[0] in ("left_proxy", "right_proxy"):
                value = "XLK" if param[0] == "left_proxy" else "DBC"
                param[1] = assumptions[param[0]]["value"] = value
    elif change in {"wrong_calendar", "wrong_revision"}:
        field = {"wrong_calendar": "calendar_id", "wrong_revision": "schedule_revision"}[change]
        assumptions[field]["value"] = "unqualified"
        next(item for item in request["parameters"] if item[0] == field)[1] = "unqualified"
    elif change == "outside_coverage":
        request["cutoff"].update(observation_date="2024-04-03", decision_at="2024-04-04T03:59:59Z")
    elif change == "early_decision":
        request["cutoff"]["decision_at"] = "2026-11-13T21:00:00Z"
    elif change == "early_evaluation":
        request["cutoff"]["evaluated_at"] = "2026-11-14T04:59:58Z"
    elif change == "wrong_timezone":
        request["cutoff"]["session_timezone"] = "America/Chicago"
    elif change == "wrong_dataset":
        request["dataset_id"] = "economy.fred_series"
    elif change == "cross_dataset":
        request["dataset_id"] = "story.dfii10" if name == "comparison" else "story.etf_pair"
    elif change == "wrong_assumption_type":
        assumptions["schedule_revision"].update(value_type="decimal", value="1")
    elif change == "future_assumptions":
        payload["assumptions"]["effective_date"] = "2026-11-14"
    elif change == "wrong_assumptions_version":
        payload["assumptions"]["version"] = "2"
    elif change == "extra_assumption":
        payload["assumptions"]["assumptions"].append(
            {**assumptions["schedule_revision"], "assumption_id": "provider_override"}
        )
    elif change == "legacy_model":
        payload.update(model_id="proxy_comparison", method_version="1")
    elif change == "duplicate_parameter":
        request["parameters"].append(request["parameters"][0])
    elif change == "extra_parameter":
        request["parameters"].append(["symbol", "DFII10"])
    elif change == "wrong_assumption":
        assumptions["schedule_revision"]["value"] = "different-revision"

    status, body = exchange("/evaluations", payload)
    assert calls == []
    assert status == 422
    assert body["fields"] == [{"path": ["acquisition"], "code": "unsupported_acquisition"}]


@pytest.mark.parametrize("fault_name", ["receipt", "basis", None])
def test_signed_runs_preserve_evidence_and_withhold_affected_spread(evaluation, fault_name):
    exchange, calls, fault = evaluation
    if fault_name:
        fault[fault_name] = True
    payload = selection("comparison")
    payload["acquisition"]["cutoff"]["decision_at"] = "2026-11-14T04:59:59.999Z"
    results = [exchange("/evaluations", payload) for _ in range(2 if fault_name is None else 1)]
    run_ids = set()
    for status, body in results:
        assert status == 200, body
        run_id = body["run_id"]
        assert exchange("/runs/" + run_id) == (200, body)
        assert exchange("/runs/" + run_id, owner="another_analyst")[0] == 404
        run_ids.add(run_id)
        outputs = {item["output_id"]: item for item in body["outputs"]}
        spread = outputs["momentum_spread"]
        assert (spread["status"], spread["value"] is None) == (
            ("withheld", True) if fault_name else ("verified", False)
        )
        query = dict(body["inputs"]["provenance"]["query"])
        assert "left_retrieved_at" in query
        if fault_name:
            assert outputs["left_momentum"]["status"] == "verified"
            assert query["right_error"] == "invalid_response"
            assert "right_retrieved_at" not in query
    assert len(run_ids) == len(results) == len(calls)


@pytest.mark.parametrize("limit,code", [
    ("deadline", "timeout"), ("cancel", "cancelled"),
    ("bytes", "invalid_response"), ("rows", "invalid_response"),
])
def test_story_acquisition_bounds(limit, code):
    cancelled = Event()
    closed = []

    async def transport(_url, params):
        if limit == "bytes":
            return b" " * (MAX_RESPONSE_BYTES + 1)
        if limit == "rows":
            body = response(params)
            body["results"] *= 5001
            body["extra"]["results_metadata"]["__qopenbb_financial__"]["bounds"]["returned_count"] = 5001
            return json.dumps(body).encode()
        if limit == "cancel":
            asyncio.get_running_loop().call_soon(cancelled.set)
        try:
            await asyncio.Future()
        finally:
            closed.append(True)

    source = DataApiSnapshotSource("http://test", transport=transport)
    started = monotonic()
    deadline = started + (0.2 if limit == "deadline" else 5)
    with pytest.raises(AcquisitionError) as caught:
        source.acquire(pair_request(), deadline=deadline, cancel=cancelled)
    assert caught.value.code == code
    if limit in ("deadline", "cancel"):
        assert closed == [True]
        assert monotonic() - started < 2
