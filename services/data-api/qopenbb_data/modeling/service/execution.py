"""Synchronous, bounded execution of installed supplied-input model methods."""

import os
import pickle
import signal
import subprocess
import sys
from collections.abc import Callable, Mapping
from dataclasses import dataclass, field
from functools import partial
from math import isfinite
from tempfile import TemporaryFile
from threading import BoundedSemaphore, Event
from time import monotonic, sleep
from typing import BinaryIO

from pydantic import ValidationError

from ..contracts.inputs import AssumptionSet, InputSnapshot
from ..models.protocol import CandidateResult
from ..models.registry import ModelRegistry
from .execution_transport import (
    CHUNK_BYTES,
    MAX_RESULT_BYTES,
    InputWriter,
    InvalidWireValue,
    RequestTooLarge,
)

_WORKER_FAILURES = {
    2: "unsupported_numeric_conversion",
    3: "invalid_input_snapshot",
    4: "invalid_assumptions",
    5: "input_schema_mismatch",
    6: "row_limit",
    7: "horizon_limit",
    8: "scenario_limit",
    9: "result_limit",
}


class ExecutionError(RuntimeError):
    """Stable failure code for the service boundary."""

    def __init__(self, code: str) -> None:
        self.code = code
        super().__init__(code)


def _positive_int(value: int) -> bool:
    return type(value) is int and value > 0


def _positive_timeout(value: float) -> bool:
    return type(value) in (float, int) and 0 < value and isfinite(value)


@dataclass(frozen=True)
class ExecutionLimits:
    """Execution metadata declared alongside an installed model version.

    The sizing callback returns horizon in the method's declared periods and
    the number of scenarios to evaluate.
    """

    max_rows: int
    max_horizon: int
    max_scenarios: int
    timeout_seconds: float | None = None
    measure_dimensions: Callable[[InputSnapshot, AssumptionSet], tuple[int, int]] = (
        field(kw_only=True)
    )

    def __post_init__(self) -> None:
        if not callable(self.measure_dimensions):
            raise TypeError("method sizing callback is required")
        if not all(
            map(_positive_int, (self.max_rows, self.max_horizon, self.max_scenarios))
        ):
            raise ValueError("method limits must be positive integers")
        if self.timeout_seconds is not None and not _positive_timeout(
            self.timeout_seconds
        ):
            raise ValueError("method timeout must be finite and positive")

    def check(self, inputs: InputSnapshot, assumptions: AssumptionSet) -> None:
        if sum(len(table.rows) for table in inputs.tables) > self.max_rows:
            raise ExecutionError("row_limit")
        horizon, scenarios = self.measure_dimensions(inputs, assumptions)
        if not _positive_int(horizon) or horizon > self.max_horizon:
            raise ExecutionError("horizon_limit")
        if not _positive_int(scenarios) or scenarios > self.max_scenarios:
            raise ExecutionError("scenario_limit")


class ModelExecutor:
    """One shared instance per service process owns its evaluation slots.

    Installed methods and sizing callbacks must be importable and picklable.
    The child measures the same validated inputs and assumptions it supplies
    to the calculation.
    """

    def __init__(
        self,
        registry: ModelRegistry,
        limits: Mapping[tuple[str, str], ExecutionLimits],
        *,
        polars_threads: int = 1,
        timeout_seconds: float = 60,
        capacity: int = 1,
    ) -> None:
        if not _positive_int(polars_threads) or not _positive_int(capacity):
            raise ValueError("thread budget and capacity must be positive integers")
        if not _positive_timeout(timeout_seconds):
            raise ValueError("service timeout must be finite and positive")
        self._registry = registry
        self._methods = {
            key: (
                pickle.dumps((registry.resolve(*key), policy)),
                policy.timeout_seconds,
            )
            for key, policy in limits.items()
        }
        self._polars_threads = polars_threads
        self._timeout_seconds = timeout_seconds
        self._slots = BoundedSemaphore(capacity)

    def evaluate(
        self,
        model_id: str,
        method_version: str,
        inputs: InputSnapshot,
        assumptions: AssumptionSet,
        *,
        cancel: Event | None = None,
    ) -> CandidateResult:
        started = monotonic()
        if not self._slots.acquire(blocking=False):
            raise ExecutionError("capacity")
        try:
            _remaining(started + self._timeout_seconds, cancel)
            configured = self._methods.get((model_id, method_version))
            if configured is None:
                self._registry.resolve(model_id, method_version)
                raise ExecutionError("missing_limits")
            method_payload, method_timeout = configured
            timeout = min(
                self._timeout_seconds, method_timeout or self._timeout_seconds
            )
            return self._execute(
                method_payload, inputs, assumptions, started + timeout, cancel
            )
        finally:
            self._slots.release()

    def _execute(
        self,
        method_payload: bytes,
        inputs: InputSnapshot,
        assumptions: AssumptionSet,
        deadline: float,
        cancel: Event | None,
    ) -> CandidateResult:
        try:
            checkpoint = partial(_remaining, deadline, cancel)
            checkpoint()
            # File-backed IPC lets the parent enforce the deadline independently
            # of how much input the child has read or output it has written.
            with TemporaryFile() as request, TemporaryFile() as response:
                for offset in range(0, len(method_payload), CHUNK_BYTES):
                    checkpoint()
                    request.write(method_payload[offset : offset + CHUNK_BYTES])
                writer = InputWriter(request, checkpoint)
                _write_contract(writer, inputs, "invalid_input_snapshot")
                _write_contract(writer, assumptions, "invalid_assumptions")
                checkpoint()
                request.seek(0)
                self._run_child(request, response, deadline, cancel)
                response.seek(0)
                result = CandidateResult.model_validate_json(
                    _read_result(response, checkpoint)
                )
                checkpoint()
                return result
        except (
            OSError,
            pickle.PickleError,
            TypeError,
            AttributeError,
            ValidationError,
        ):
            raise ExecutionError("execution_failed") from None

    def _run_child(
        self,
        request: BinaryIO,
        response: BinaryIO,
        deadline: float,
        cancel: Event | None,
    ) -> None:
        # A fresh interpreter gets its budget before importing service or model
        # code, even if the parent already initialized its own Polars pool.
        with subprocess.Popen(
            [sys.executable, "-m", f"{__package__}.execution_worker"],
            stdin=request,
            stdout=response,
            stderr=subprocess.DEVNULL,
            start_new_session=os.name == "posix",
            env={**os.environ, "POLARS_MAX_THREADS": str(self._polars_threads)},
        ) as child:
            try:
                _await_exit(child, deadline, cancel)
            finally:
                _stop_child(child)
                status = child.wait()
        if status != 0:
            raise ExecutionError(_WORKER_FAILURES.get(status, "execution_failed"))


def _write_contract(writer: InputWriter, value: object, code: str) -> None:
    try:
        writer.write_value(value)
        writer.end_document()
    except InvalidWireValue:
        raise ExecutionError(code) from None
    except RequestTooLarge:
        raise ExecutionError("request_limit") from None


def _read_result(stream: BinaryIO, checkpoint: Callable[[], object]) -> bytearray:
    payload = bytearray()
    while True:
        checkpoint()
        chunk = stream.read(min(CHUNK_BYTES, MAX_RESULT_BYTES - len(payload) + 1))
        if not chunk:
            return payload
        payload.extend(chunk)
        if len(payload) > MAX_RESULT_BYTES:
            raise ExecutionError("result_limit")


def _stop_child(child: subprocess.Popen) -> None:
    if os.name != "posix":
        child.kill()
        return
    # Normal subprocesses inherit this session's process group and can
    # outlive its leader even when the worker returns a valid result.
    try:
        os.killpg(child.pid, signal.SIGKILL)
    except ProcessLookupError:
        pass


def _remaining(deadline: float, cancel: Event | None) -> float:
    if cancel is not None and cancel.is_set():
        raise ExecutionError("cancelled")
    remaining = deadline - monotonic()
    if remaining <= 0:
        raise ExecutionError("timeout")
    return remaining


def _await_exit(child: subprocess.Popen, deadline: float, cancel: Event | None) -> None:
    if hasattr(os, "waitid") and hasattr(os, "WNOWAIT"):
        # Keep the leader's PID reserved until its group has been signalled.
        flags = os.WEXITED | os.WNOHANG | os.WNOWAIT
        while True:
            remaining = _remaining(deadline, cancel)
            if os.waitid(os.P_PID, child.pid, flags) is not None:
                _remaining(deadline, cancel)
                return
            sleep(min(remaining, 0.05))

    while True:
        remaining = _remaining(deadline, cancel)
        try:
            child.wait(
                timeout=min(remaining, 0.05) if cancel is not None else remaining
            )
        except subprocess.TimeoutExpired:
            continue
        _remaining(deadline, cancel)
        return
