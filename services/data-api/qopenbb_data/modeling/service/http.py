"""Serve /modeling/v1 on the internal ASGI listener, separate from wildcard /data."""

from collections.abc import Callable
from math import isfinite
from threading import BoundedSemaphore, Event
from typing import Protocol

from anyio import Event as AsyncEvent
from anyio import create_task_group, current_time, move_on_after, to_thread
from anyio.lowlevel import checkpoint
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from starlette.requests import ClientDisconnect

from ..contracts.results import ModelRun
from ..models.registry import ModelRegistry
from .acquisition import AcquisitionError
from .evaluation import EvaluationRequest
from .execution import ExecutionError
from .http_errors import execution_failure, failure, validation_failure
from .identity import IdentityError
from .orchestrator import Orchestrator
from .ports import Principal
from .run_store import RunNotFound, RunPublishedError, RunStoreError
from .widget_discovery import apps, widgets
from .widget_projection import project_output

_MAX_BODY_BYTES = 2 * 1024 * 1024


class IdentityVerifier(Protocol):
    def authenticate(self, authorization: str | None) -> Principal: ...


def create_model_app(
    orchestrator: Orchestrator,
    registry: ModelRegistry,
    verifier: IdentityVerifier,
    *,
    capacity: int = 1,
    body_timeout_seconds: float = 30,
    request_timeout_seconds: float = 60,
) -> FastAPI:
    """Apply a process-local admission limit from body receipt until cleanup."""
    if type(capacity) is not int or capacity < 1:
        raise ValueError("HTTP evaluation capacity must be a positive integer")
    for timeout in (body_timeout_seconds, request_timeout_seconds):
        if not isfinite(timeout) or timeout <= 0:
            raise ValueError("HTTP deadlines must be finite and positive")

    # Fall back to safe envelopes at the HTTP boundary if a dependency raises
    # an unexpected exception carrying private provider or request details.
    admission = BoundedSemaphore(capacity)
    app = FastAPI(
        docs_url=None, redoc_url=None, openapi_url=None, redirect_slashes=False
    )

    @app.get("/models")
    def models(request: Request) -> Response:
        return _discovery(
            request,
            verifier,
            lambda: {
                "models": [
                    item.model_dump(mode="json") for item in registry.descriptors()
                ]
            },
        )

    @app.get("/widgets.json")
    def discover_widgets(request: Request) -> Response:
        return _discovery(request, verifier, widgets)

    @app.get("/apps.json")
    def discover_apps(request: Request) -> Response:
        return _discovery(request, verifier, apps)

    @app.get("/widget-results")
    def widget_results(request: Request) -> Response:
        params = request.query_params
        return _read_saved(
            request,
            orchestrator,
            verifier,
            params.get("run_id", ""),
            params.get("output_id", ""),
            widget=True,
        )

    @app.post("/evaluations")
    async def evaluate(request: Request) -> Response:
        try:
            principal = _authenticate(request, verifier)
        except IdentityError:
            return failure(401, "unauthorized")
        except Exception:  # noqa: BLE001
            return failure(500, "internal_error")

        if not admission.acquire(blocking=False):
            return failure(503, "capacity")
        try:
            deadline = current_time() + request_timeout_seconds
            body = await _read_body(
                request, min(body_timeout_seconds, request_timeout_seconds)
            )
            return await _evaluate(
                request, orchestrator, registry, principal, body, deadline
            )
        except ClientDisconnect:
            return failure(503, "cancelled")
        except ExecutionError as error:
            return execution_failure(error.code)
        except Exception:  # noqa: BLE001
            return failure(500, "internal_error")
        finally:
            admission.release()

    @app.get("/runs/{run_id}", response_model=ModelRun)
    def saved_run(request: Request, run_id: str) -> Response:
        return _read_saved(request, orchestrator, verifier, run_id)

    @app.get("/runs/{run_id}/outputs/{output_id}")
    def saved_output(request: Request, run_id: str, output_id: str) -> Response:
        return _read_saved(request, orchestrator, verifier, run_id, output_id)

    return app


def _discovery(
    request: Request, verifier: IdentityVerifier, load: Callable[[], dict | list]
) -> Response:
    try:
        _authenticate(request, verifier)
        return JSONResponse(load())
    except IdentityError:
        return failure(401, "unauthorized")
    except Exception:  # noqa: BLE001 - Keep internal configuration errors private.
        return failure(503, "discovery_unavailable")


def _authenticate(request: Request, verifier: IdentityVerifier) -> Principal:
    headers = request.headers.getlist("authorization")
    principal = verifier.authenticate(headers[0] if len(headers) == 1 else None)
    return Principal.model_validate(principal)


async def _read_body(request: Request, timeout: float) -> bytearray:
    length = request.headers.get("content-length", "").lstrip("0")
    if (
        length.isascii()
        and length.isdecimal()
        and (len(length) > len(str(_MAX_BODY_BYTES)) or int(length) > _MAX_BODY_BYTES)
    ):
        raise ExecutionError("request_limit")
    body = bytearray()
    with move_on_after(timeout) as scope:
        while True:
            await checkpoint()
            message = await request.receive()
            if message["type"] == "http.disconnect":
                raise ClientDisconnect
            chunk = message.get("body", b"")
            if len(body) + len(chunk) > _MAX_BODY_BYTES:
                raise ExecutionError("request_limit")
            body.extend(chunk)
            if not message.get("more_body", False):
                break
    if scope.cancel_called:
        raise ExecutionError("timeout")
    return body


async def _watch_disconnect(request: Request, cancel: Event, deadline: float) -> None:
    try:
        with move_on_after(max(0, deadline - current_time())):
            while (await request.receive())["type"] != "http.disconnect":
                await checkpoint()
    finally:
        cancel.set()


async def _evaluate(
    request: Request,
    orchestrator: Orchestrator,
    registry: ModelRegistry,
    principal: Principal,
    body: bytearray,
    deadline: float,
) -> Response:
    if current_time() >= deadline:
        return failure(503, "timeout")
    cancel = Event()
    finished = AsyncEvent()
    response: Response

    async def evaluate_and_signal() -> None:
        nonlocal response
        response = await _run_evaluation(
            orchestrator, registry, principal, body, cancel, deadline
        )
        finished.set()

    # A separate task shields the worker from direct cancellation of the ASGI
    # request task. The group joins it before the admission slot is released.
    async with create_task_group() as tasks:
        tasks.start_soon(_watch_disconnect, request, cancel, deadline)
        tasks.start_soon(evaluate_and_signal)
        await finished.wait()
        tasks.cancel_scope.cancel()
    return response


async def _run_evaluation(
    orchestrator: Orchestrator,
    registry: ModelRegistry,
    principal: Principal,
    body: bytearray,
    cancel: Event,
    deadline: float,
) -> Response:
    try:
        response = await to_thread.run_sync(
            _evaluate_body, orchestrator, registry, principal, body, cancel
        )
    except RunPublishedError as error:
        return failure(
            503,
            "publication_unconfirmed",
            retryable=False,
            run_id=error.run_id,
        )
    # A response for an already persisted run wins a cancellation race.
    if response.status_code == 200:
        return response
    if current_time() >= deadline:
        return failure(503, "timeout")
    return failure(503, "cancelled") if cancel.is_set() else response


def _evaluate_body(
    orchestrator: Orchestrator,
    registry: ModelRegistry,
    principal: Principal,
    body: bytearray,
    cancel: Event,
) -> Response:
    try:
        request = EvaluationRequest.model_validate_json(body)
    except ValidationError as error:
        return validation_failure(error)

    try:
        registry.resolve(request.model_id, request.method_version)
    except LookupError:
        return failure(
            422,
            "unsupported_method",
            [
                {"path": ["model_id"], "code": "unsupported_method"},
                {"path": ["method_version"], "code": "unsupported_method"},
            ],
        )
    try:
        if cancel.is_set():
            return failure(503, "cancelled")
        return _run_response(orchestrator.evaluate(request, principal, cancel=cancel))
    except ExecutionError as error:
        return execution_failure(error.code)
    except AcquisitionError as error:
        if error.code in ("timeout", "cancelled"):
            return execution_failure(error.code)
        if error.code in {"invalid_request", "entitlement"}:
            field_code = "entitlement" if error.code == "entitlement" else "unsupported_acquisition"
            return failure(
                422,
                "unsupported_acquisition",
                [
                    {"path": ["acquisition"], "code": field_code},
                ],
            )
        return failure(503, "acquisition_unavailable")
    except RunPublishedError:
        raise
    except RunStoreError:
        return failure(503, "storage_unavailable")
    except ValueError:
        if not request.exceptions:
            raise
        return failure(
            422,
            "invalid_request",
            [
                {"path": ["exceptions"], "code": "invalid_policy_exception"},
            ],
        )


def _run_response(run: ModelRun) -> Response:
    return Response(content=run.model_dump_json(), media_type="application/json")


def _read_saved(
    request: Request,
    orchestrator: Orchestrator,
    verifier: IdentityVerifier,
    run_id: str,
    output_id: str | None = None,
    *,
    widget: bool = False,
) -> Response:
    try:
        principal = _authenticate(request, verifier)
        if widget and (not run_id or not output_id):
            return failure(
                422,
                "invalid_request",
                [
                    {"path": [name], "code": "missing"}
                    for name, value in (("run_id", run_id), ("output_id", output_id))
                    if not value
                ],
            )
        run = orchestrator.get(run_id, principal)
        if output_id is None:
            return _run_response(run)
        expected = request.query_params.get("expected_run_id") or None
        return JSONResponse(project_output(run, output_id, expected_run_id=expected))
    except IdentityError:
        return failure(401, "unauthorized")
    except RunNotFound:
        return failure(404, "not_found")
    except Exception:  # noqa: BLE001
        return failure(503, "storage_unavailable")
