import asyncio
import os
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from threading import Event
from time import monotonic, sleep

import pytest
from qopenbb_data.modeling.contracts import ModelRun
from qopenbb_data.modeling.service import execution, run_store_transport
from qopenbb_data.modeling.service.execution import ExecutionError
from qopenbb_data.modeling.service.run_store import (
    FileRunStore,
    RunNotFound,
    RunPublishedError,
)
from test_model_http import build, call, error
from test_orchestration import OWNER, TestMethod, request
from test_orchestration import inputs as model_inputs
from test_orchestration import service as orchestration_service

inputs = model_inputs
service = orchestration_service

_BLOCK_STORAGE = """
import errno
import os
import runpy
import stat
from pathlib import Path
import sys
from time import sleep

operation, marker_path, fallback = sys.argv[1:]
marker = Path(marker_path)
original_sync = os.fsync
original_link = os.link
original_open = os.open

def block():
    marker.write_text(str(os.getpid()))
    sleep(15)

def sync(fd):
    if operation == 'directory_sync' and stat.S_ISDIR(os.fstat(fd).st_mode):
        block()
    if operation == 'file_sync' and stat.S_ISREG(os.fstat(fd).st_mode):
        block()
    return original_sync(fd)

def link(*args, **kwargs):
    if fallback == 'proc' and args[0].startswith('/proc/self/fd/'):
        raise OSError(errno.ENOENT, 'proc unavailable')
    if operation == 'link':
        block()
    return original_link(*args, **kwargs)

def open_file(path, flags, *args, **kwargs):
    tmpfile = getattr(os, 'O_TMPFILE', 0)
    if fallback == 'filesystem' and tmpfile and flags & tmpfile == tmpfile:
        raise OSError(errno.EOPNOTSUPP, 'anonymous staging unavailable')
    if operation == 'readback' and isinstance(path, str) and path.endswith('.json'):
        raise OSError(errno.EIO, 'readback failed')
    return original_open(path, flags, *args, **kwargs)

os.fsync = sync
os.link = link
os.open = open_file
if operation == 'receive':
    block()
runpy.run_module('qopenbb_data.modeling.service.run_store_worker', run_name='__main__')
"""


def install_storage_fault(
    monkeypatch, operation, marker, fallback="", close_fault=False
):
    start = run_store_transport.subprocess.Popen

    def process(command, *args, **kwargs):
        if command[-1].endswith(".run_store_worker"):
            command = [
                sys.executable,
                "-c",
                _BLOCK_STORAGE,
                operation,
                str(marker),
                fallback,
            ]
            child = start(command, *args, **kwargs)
            if close_fault:
                child.stdout = CloseFault(child.stdout)
            return child
        return start(command, *args, **kwargs)

    monkeypatch.setattr(run_store_transport.subprocess, "Popen", process)


class CloseFault:
    def __init__(self, stream):
        self.stream = stream

    def __getattr__(self, name):
        return getattr(self.stream, name)

    def close(self):
        self.stream.close()
        raise OSError("pipe close failed")


def wait_for_worker(marker: Path, future):
    deadline = monotonic() + 10
    while not future.done() and monotonic() < deadline:
        if marker.exists() and (pid := marker.read_text()):
            return int(pid)
        sleep(0.01)
    pytest.fail("the real storage path did not reach the injected stall")


@pytest.mark.parametrize("operation", ["file_sync", "link", "directory_sync"])
def test_disconnect_stops_and_reaps_real_publication(
    service, inputs, tmp_path, monkeypatch, operation
):
    marker = tmp_path / "blocked"
    install_storage_fault(monkeypatch, operation, marker)
    orchestrator = service(timeout=8)
    cancel = Event()
    outcome = ExecutionError if operation == "file_sync" else RunPublishedError
    with ThreadPoolExecutor(max_workers=1) as pool:
        future = pool.submit(
            orchestrator.evaluate, request(inputs=inputs), OWNER, cancel=cancel
        )
        pid = wait_for_worker(marker, future)
        cancel.set()
        with pytest.raises(outcome) as failure:
            future.result(timeout=2)
    with pytest.raises(ProcessLookupError):
        os.kill(pid, 0)

    saved = list((tmp_path / "runs").iterdir())
    if operation == "file_sync":
        assert failure.value.code == "cancelled"
        assert saved == []
    elif operation == "link":
        assert len(failure.value.run_id) == 32
        assert saved == []
    else:
        run_id = failure.value.run_id
        assert saved == [tmp_path / "runs" / f"{run_id}.json"]
        assert orchestrator.get(run_id, OWNER).run_id == run_id


def test_deadline_covers_calculation_and_publication(
    service, inputs, tmp_path, monkeypatch
):
    marker = tmp_path / "blocked"
    install_storage_fault(monkeypatch, "file_sync", marker)
    deadlines = []
    publish = run_store_transport.publish

    def capture(root, wire, principal, deadline, cancel):
        deadlines.append(deadline)
        return publish(root, wire, principal, deadline, cancel)

    monkeypatch.setattr(run_store_transport, "publish", capture)
    budget = 20
    expired = Event()
    monkeypatch.setattr(
        execution,
        "monotonic",
        lambda: monotonic() + (budget if expired.is_set() else 0),
    )
    orchestrator = service(model=SlowMethod(), timeout=budget)
    started = monotonic()
    with ThreadPoolExecutor(max_workers=1) as pool:
        future = pool.submit(orchestrator.evaluate, request(inputs=inputs), OWNER)
        try:
            pid = wait_for_worker(marker, future)
        finally:
            # Advance the executor clock only after the real stage reached fsync.
            expired.set()
        with pytest.raises(ExecutionError, match="^timeout$"):
            future.result(timeout=2)
    assert deadlines[0] == pytest.approx(started + budget, abs=0.2)
    with pytest.raises(ProcessLookupError):
        os.kill(pid, 0)
    assert list((tmp_path / "runs").iterdir()) == []


class SlowMethod(TestMethod):
    __test__ = False

    def calculate(self, inputs, assumptions):
        sleep(1)
        return super().calculate(inputs, assumptions)


def test_publication_reuses_parent_validated_run(service, inputs, monkeypatch):
    validations = []
    validate = ModelRun.model_validate_json

    def track(wire):
        validations.append(len(wire))
        return validate(wire)

    def unexpected_encoding(*args, **kwargs):
        pytest.fail("the parent re-encoded the evaluated run")

    orchestrator = service()
    with monkeypatch.context() as patch:
        patch.setattr(ModelRun, "model_validate_json", track)
        patch.setattr(ModelRun, "model_dump_json", unexpected_encoding)
        saved = orchestrator.evaluate(request(inputs=inputs), OWNER)
    assert len(validations) == 1
    assert orchestrator.get(saved.run_id, OWNER) == saved


def test_legacy_store_readback_failure_preserves_saved_id(service, inputs, tmp_path):
    real = FileRunStore(tmp_path)

    class Store:
        def save(self, run, principal):
            return real.save(run, principal)

        def get(self, run_id, principal):
            raise OSError("private storage details")

    orchestrator = service()
    orchestrator._store = Store()
    with pytest.raises(RunPublishedError) as failure:
        orchestrator.evaluate(request(inputs=inputs), OWNER)
    assert real.get(failure.value.run_id, OWNER).owner_id == OWNER.subject


@pytest.mark.parametrize("fallback", ["filesystem", "proc"])
def test_named_fallback_saves_and_removes_staging(
    service, inputs, tmp_path, monkeypatch, fallback
):
    install_storage_fault(monkeypatch, "", tmp_path / "blocked", fallback)
    orchestrator = service()
    saved = orchestrator.evaluate(request(inputs=inputs), OWNER)
    assert orchestrator.get(saved.run_id, OWNER) == saved
    assert list((tmp_path / "runs").iterdir()) == [
        tmp_path / "runs" / f"{saved.run_id}.json"
    ]


def test_cancelled_named_stage_is_private_and_undiscoverable(
    service, inputs, tmp_path, monkeypatch
):
    marker = tmp_path / "blocked"
    install_storage_fault(monkeypatch, "file_sync", marker, "filesystem")
    orchestrator = service(timeout=8)
    cancel = Event()
    with ThreadPoolExecutor(max_workers=1) as pool:
        future = pool.submit(
            orchestrator.evaluate, request(inputs=inputs), OWNER, cancel=cancel
        )
        pid = wait_for_worker(marker, future)
        cancel.set()
        with pytest.raises(ExecutionError, match="^cancelled$"):
            future.result(timeout=2)
    with pytest.raises(ProcessLookupError):
        os.kill(pid, 0)
    [staging] = (tmp_path / "runs").iterdir()
    assert staging.name.startswith(".pending-")
    assert staging.stat().st_mode & 0o777 == 0o600
    with pytest.raises(RunNotFound):
        orchestrator.get(staging.name, OWNER)


@pytest.mark.parametrize(
    ("operation", "fallback", "close_fault"),
    [
        ("readback", "", False),
        ("directory_sync", "filesystem", True),
    ],
)
def test_http_publication_failure_is_non_retryable_and_recoverable(
    service, inputs, tmp_path, monkeypatch, operation, fallback, close_fault
):
    marker = tmp_path / "blocked"
    install_storage_fault(monkeypatch, operation, marker, fallback, close_fault)
    app = build(service(timeout=20), request_timeout_seconds=15)
    payload = request(inputs=inputs).model_dump_json().encode()

    sent = False

    async def disconnect_after_sync():
        nonlocal sent
        if not sent:
            sent = True
            return {"type": "http.request", "body": payload}
        while not marker.exists() or not marker.read_text():
            await asyncio.sleep(0.01)
        return {"type": "http.disconnect"}

    async def exercise():
        response = await call(
            app,
            "/evaluations",
            body=payload,
            receive=disconnect_after_sync if operation == "directory_sync" else None,
        )
        reason = error(response, 503, "publication_unconfirmed", False)
        path = "/runs/" + reason["run_id"]
        status, saved = await call(app, path)
        assert status == 200
        assert saved["run_id"] == reason["run_id"]
        error(await call(app, path, token="other"), 404, "not_found", False)

    asyncio.run(exercise())
    if operation == "directory_sync":
        with pytest.raises(ProcessLookupError):
            os.kill(int(marker.read_text()), 0)


def test_cancelled_delivery_reaps_worker_blocked_before_reading_frame(
    tmp_path, monkeypatch
):
    marker = tmp_path / "blocked"
    private_bind = tmp_path / "runs"
    install_storage_fault(monkeypatch, "receive", marker, close_fault=True)
    cancel = Event()
    with ThreadPoolExecutor(max_workers=1) as pool:
        future = pool.submit(
            run_store_transport.publish,
            private_bind,
            bytearray(4 * 1024 * 1024),
            OWNER,
            monotonic() + 8,
            cancel,
        )
        pid = wait_for_worker(marker, future)
        cancel.set()
        with pytest.raises(ExecutionError, match="^cancelled$"):
            future.result(timeout=2)
    with pytest.raises(ProcessLookupError):
        os.kill(pid, 0)
    assert not private_bind.exists()
