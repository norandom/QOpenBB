"""Reject invalid evidence even when the wire marks the output verified."""

import asyncio
import json
from copy import deepcopy
from datetime import UTC, datetime
from decimal import Decimal
from pathlib import Path
import sys

import pytest
from qopenbb_data.modeling.contracts import Observation
from qopenbb_data.modeling.service.bootstrap import installed_methods
from qopenbb_data.modeling.service.http import create_model_app
from qopenbb_data.modeling.service.identity import IdentityVerifier
from qopenbb_data.modeling.service.orchestrator import Orchestrator
from qopenbb_data.modeling.service.run_store import FileRunStore
from qopenbb_data.modeling.service.story_acquisition import _yield_evidence
from qopenbb_data.modeling.service.story_schedule import CALENDAR_ID, REVISION, story_sessions
from test_model_http import call
from test_model_identity import ENV, assertion
from test_story_binding import evaluation, selection

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "verification/modeling-journey"))
from story_preflight_evidence import END, START, PreflightFailure, digest, verify_comparison, verify_context


@pytest.mark.parametrize("corruption", [None, "close", "date", "receipt", "basis", "trace", "reference"])
def test_preflight_verifies_live_wire_shape(evaluation, corruption):
    exchange, _, _ = evaluation
    request = selection("comparison")
    status, run = exchange("/evaluations", request)
    assert status == 200
    request["acquisition"]["cutoff"] = run["inputs"]["cutoff"]
    if corruption is None:
        evidence = verify_comparison(run, request)
        assert [leg["row_count"] for leg in evidence["legs"]] == [64, 64]
        assert "rows" not in str(evidence)
        return

    altered = deepcopy(run)
    rows = altered["inputs"]["tables"][1]["rows"]
    if corruption == "close":
        rows[1]["value"] = "1234"
    elif corruption == "date":
        rows[1]["observation_date"] = rows[0]["observation_date"]
    elif corruption == "receipt":
        query = altered["inputs"]["provenance"]["query"]
        query[:] = [entry for entry in query if entry[0] != "left_retrieved_at"]
    elif corruption == "basis":
        rows[1]["context"]["basis"] = "dividend_adjusted"
    elif corruption == "trace":
        trace = next(item for item in altered["trace"] if item["output_id"] == "left_volatility")
        trace["intermediate_values"][0]["period_end"] = "2026-01-01"
    else:
        altered["verification"][0]["status"] = "mismatch"
    if corruption != "reference":
        refresh_fingerprints(altered)
    with pytest.raises(PreflightFailure):
        verify_comparison(altered, request)



def refresh_fingerprints(run):
    inputs = digest(run["inputs"], sorted_keys=False, ascii_only=False)
    outputs = {item["output_id"]: item for item in run["outputs"]}
    traces = {item["trace_id"]: item for item in run["trace"]}
    checks = {item["rule_id"]: item for item in run["checks"]}
    for ref in run["verification"]:
        output = outputs[ref["output_id"]]
        ref["input_fingerprint"] = inputs
        ref["output_fingerprint"] = digest({
            "output": output, "checks": [checks[key] for key in output["check_ids"]],
            "trace": [traces[key] for key in output["trace_ids"]],
        })


def fred_row(day, value, published):
    return Observation(
        record_id=f"fred:preflight:{day}", source_record_id=f"fred:DFII10:{day}",
        entity_id="DFII10", metric_id="real_yield", observation_date=day, category="provider",
        context={"unit": "percent", "basis": "treasury_constant_maturity", "quantity": "rate",
                 "vintage_coverage": "known" if published else "unavailable"},
        value=Decimal(value), published_at=published, vintage_at=published,
    )


@pytest.mark.parametrize("publication, expected", [
    (None, "withheld"),
    ("2026-11-16T20:30:00Z", "withheld"),
    ("2026-11-13T20:30:00Z", "verified"),
])
def test_preflight_verifies_dated_macro_context(monkeypatch, tmp_path, publication, expected):
    for key, value in ENV.items():
        monkeypatch.setenv(key, value)

    class SnapshotSource:
        def acquire(self, request, **kwargs):
            sessions = story_sessions(request.cutoff, CALENDAR_ID, REVISION)
            return _yield_evidence(
                request, sessions, {"provider": "fred", "symbol": "DFII10",
                                    "start_date": START, "end_date": END},
                datetime.now(UTC), "preflight", (
                    fred_row(START, "2.4", "2026-08-18T20:30:00Z"),
                    fred_row(END, "1.9", publication),
                ),
            )

    registry, bindings = installed_methods()
    source = SnapshotSource()
    service = Orchestrator(registry, bindings, FileRunStore(tmp_path), snapshot_source=source)
    app = create_model_app(service, registry, IdentityVerifier.from_env())
    request = selection("regime")
    status, run = asyncio.run(call(app, "/evaluations", body=json.dumps(request).encode(), token=assertion()))
    assert status == 200
    evidence = verify_context(run, request)
    assert evidence["context_status"] == expected
    if expected == "verified":
        assert [row["observation_date"] for row in evidence["endpoints"]] == [START, END]
        assert evidence["outputs"]["regime"]["value"] == "falling"
        assert Decimal(evidence["outputs"]["change"]["value"]) == Decimal("-.5")
    else:
        assert evidence["unavailable_endpoint"] == END
