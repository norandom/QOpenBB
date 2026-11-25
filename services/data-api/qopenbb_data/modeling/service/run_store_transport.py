"""Send canonical run evidence to a supervised publication worker."""

import json
import os
import selectors
import subprocess
import sys
from contextlib import suppress
from pathlib import Path
from threading import Event
from typing import BinaryIO

from .execution import ExecutionError, _await_exit, _remaining, _stop_child
from .execution_transport import CHUNK_BYTES
from .ports import Principal
from .run_store import RunPublishedError, RunStoreError, _new_run_id


def publish(
    root: Path,
    wire: bytearray,
    principal: Principal,
    deadline: float,
    cancel: Event | None,
) -> str:
    _remaining(deadline, cancel)
    run_id = _new_run_id()
    header = (
        json.dumps((str(root), principal.subject, run_id, len(wire))).encode("ascii")
        + b"\n"
    )
    try:
        child = subprocess.Popen(
            [sys.executable, "-m", f"{__package__}.run_store_worker"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            bufsize=0,
            start_new_session=os.name == "posix",
        )
        _finish(child, header, wire, run_id, deadline, cancel)
    except OSError:
        raise RunStoreError("model run storage unavailable") from None
    return run_id


def _finish(
    child: subprocess.Popen,
    header: bytes,
    wire: bytearray,
    run_id: str,
    deadline: float,
    cancel: Event | None,
) -> None:
    request, response = child.stdin, child.stdout
    assert request is not None and response is not None
    interrupted = None
    try:
        try:
            _send(request, header, wire, deadline, cancel)
            _await_exit(child, deadline, cancel)
        except (ExecutionError, OSError) as error:
            interrupted = error
        finally:
            _stop_child(child)
            status = child.wait()
        commit_started = _commit_state(response, run_id)
        if commit_started and (status != 0 or interrupted is not None):
            raise RunPublishedError(run_id)
        if interrupted is not None:
            raise interrupted
        if status != 0 or not commit_started:
            raise RunStoreError("model run storage unavailable")
    finally:
        # The worker is already reaped. A pipe-close fault cannot change the
        # outcome or replace a recovery ID with a retryable storage error.
        for stream in (request, response):
            with suppress(OSError):
                stream.close()


def _commit_state(response: BinaryIO, run_id: str) -> bool:
    try:
        os.set_blocking(response.fileno(), False)
        # One begin marker per staging path and a reset for a rejected link.
        signals = response.read(16)
    except OSError:
        raise RunPublishedError(run_id) from None
    return bool(signals and signals[-1:] == b"1")


def _send(
    request: BinaryIO,
    header: bytes,
    wire: bytearray,
    deadline: float,
    cancel: Event | None,
) -> None:
    fd = request.fileno()
    os.set_blocking(fd, False)
    with selectors.DefaultSelector() as ready:
        ready.register(fd, selectors.EVENT_WRITE)
        for document in (header, wire):
            payload = memoryview(document)
            offset = 0
            while offset < len(payload):
                remaining = _remaining(deadline, cancel)
                if not ready.select(min(remaining, 0.05)):
                    continue
                try:
                    offset += os.write(fd, payload[offset : offset + CHUNK_BYTES])
                except BlockingIOError:
                    continue
