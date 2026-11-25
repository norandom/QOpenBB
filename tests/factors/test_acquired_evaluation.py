"""Verify the configured GDP acquisition path through an actual HTTP connection."""

from contextlib import contextmanager
from decimal import Decimal
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from threading import Event, Thread
from time import monotonic
from urllib.parse import parse_qs, urlsplit

import pytest
from qopenbb_data.modeling.service.acquisition import (
    AcquisitionError,
    DataApiSnapshotSource,
)
from qopenbb_data.modeling.service.execution import ExecutionError
from test_acquisition import CUTOFF, DATASET, RESPONSE
from test_orchestration import OWNER, TestMethod, request
from test_orchestration import service as service_fixture

build_service = service_fixture


@contextmanager
def data_api(*, stall=False, cancel=None):
    requests = []
    disconnected = Event()

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            target = urlsplit(self.path)
            requests.append((target.path, parse_qs(target.query)))
            if stall:
                if cancel is not None:
                    cancel.set()
                self.connection.settimeout(5)
                if self.connection.recv(1) == b"":
                    disconnected.set()
                return
            body = RESPONSE if len(requests) == 1 else RESPONSE.replace(b"28624.069", b"28625.100")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, *args):
            pass

    with ThreadingHTTPServer(("127.0.0.1", 0), Handler) as server:
        thread = Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            yield f"http://127.0.0.1:{server.server_port}", requests, disconnected
        finally:
            server.shutdown()
            thread.join()


def test_revised_gdp_is_saved_as_a_separate_verified_observation(build_service):
    model = TestMethod()
    descriptor = model.describe()
    output = descriptor.outputs[0].model_copy(update={
        "required_input_ids": (DATASET,), "unit": "USD_billions",
        "semantic_definition": "Reported GDP in billions of dollars, as retrieved",
    })
    model.descriptor = descriptor.model_copy(update={
        "input_schema_id": DATASET, "input_ids": (DATASET,), "outputs": (output,),
    })
    evaluation = request(acquisition={
        "dataset_id": DATASET, "parameters": (("symbol", "GDP"),), "cutoff": CUTOFF,
    })
    with data_api() as (url, calls, _):
        evaluate = build_service(model=model, source=DataApiSnapshotSource(url)).evaluate
        first, revised = (evaluate(evaluation, OWNER) for _ in range(2))
    assert calls == [("/api/v1/economy/fred_series", {
        "provider": ["fred"], "symbol": ["GDP"], "end_date": ["2024-04-01"],
        "use_cache": ["false"],
    })] * 2
    restored = build_service().get(first.run_id, OWNER)
    assert restored == first
    assert restored.outputs[0].value == Decimal("28624.069")
    assert revised.outputs[0].value == Decimal("28625.100")
    assert revised.outputs[0].status == restored.outputs[0].status == "verified"
    assert revised.run_id != restored.run_id
    assert revised.inputs.provenance.acquisition_id != restored.inputs.provenance.acquisition_id
    row = restored.inputs.tables[0].rows[0]
    assert row.context.vintage_coverage == "unavailable"
    assert not restored.inputs.cutoff.is_eligible(row)
    assert restored.trace[0].output_id == "value"


@pytest.mark.parametrize("reason", ["timeout", "cancelled"])
def test_stalled_acquisition_releases_connection_and_slot(build_service, tmp_path, reason):
    cancel = Event() if reason == "cancelled" else None
    with data_api(stall=True, cancel=cancel) as (url, calls, disconnected):
        service = build_service(source=DataApiSnapshotSource(url), timeout=1)
        acquisition = {"dataset_id": DATASET, "parameters": (("symbol", "GDP"),), "cutoff": CUTOFF}
        started = monotonic()
        with pytest.raises(ExecutionError, match=reason):
            service.evaluate(request(acquisition=acquisition), OWNER, cancel=cancel)
        assert monotonic() - started < 2
        assert disconnected.wait(1)
        assert len(calls) == 1
        assert not (tmp_path / "runs").exists()
        # Reusing the same slot reaches the adapter again, before opening another connection.
        with pytest.raises(AcquisitionError) as invalid:
            service.evaluate(request(acquisition={**acquisition, "dataset_id": "unknown"}), OWNER)
        assert invalid.value.code == "invalid_request"
