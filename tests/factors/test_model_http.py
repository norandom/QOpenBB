import asyncio
import json
from functools import partial
from threading import Event
from time import time
from uuid import UUID

import pytest
from qopenbb_data.modeling.models.registry import ModelRegistry
from qopenbb_data.modeling.service.execution import ExecutionError
from qopenbb_data.modeling.service.http import create_model_app
from qopenbb_data.modeling.service.identity import IdentityError, IdentityVerifier
from qopenbb_data.modeling.service.ports import Principal
from qopenbb_data.modeling.service.run_store import RunPublishedError, RunStoreError
from test_model_identity import CURRENT, PREVIOUS, assertion
from test_orchestration import TestMethod, expected, mismatch, slow_callback
from test_orchestration import inputs as inputs_fixture
from test_orchestration import request as evaluation_request
from test_orchestration import service as service_fixture

inputs = inputs_fixture
service = service_fixture


class Verifier:
    def authenticate(self, authorization):
        if authorization not in ("Bearer owner", "Bearer other"):
            raise IdentityError("private token details")
        return Principal(subject=authorization.split()[1])


async def call(
    app, path, *, body=None, token="owner", receive=None, length=None, extra_headers=()
):
    events = []
    method = "POST" if path == "/evaluations" else "GET"
    headers = [] if token is None else [(b"authorization", f"Bearer {token}".encode())]
    headers.extend(extra_headers)
    if length is not None:
        headers.append((b"content-length", str(length).encode()))

    async def default_receive():
        if not events and body is not None and not sent.is_set():
            sent.set()
            return {"type": "http.request", "body": body}
        await asyncio.Future()

    async def send(event):
        events.append(event)

    sent = asyncio.Event()
    await app(
        {
            "type": "http",
            "asgi": {"version": "3.0"},
            "method": method,
            "path": path,
            "root_path": "",
            "query_string": b"",
            "headers": headers,
            "scheme": "http",
            "server": ("localhost", 80),
            "client": ("localhost", 1),
            "http_version": "1.1",
        },
        receive or default_receive,
        send,
    )
    return events[0]["status"], json.loads(events[-1]["body"])


def build(orchestrator, **options):
    return create_model_app(
        orchestrator, ModelRegistry((TestMethod(),)), Verifier(), **options
    )


def error(result, status, code, retryable):
    actual_status, body = result
    assert actual_status == status
    assert body["code"] == code
    assert body["retryable"] is retryable
    UUID(body["correlation_id"])
    return body


@pytest.mark.parametrize(
    ("reference", "status", "value"),
    [
        (expected, "verified", "12345678901234.0025"),
        (None, "unverified", "12345678901234.0025"),
        (mismatch, "withheld", None),
    ],
)
def test_save_reopen_project_and_owner(service, inputs, reference, status, value):
    app = build(service(reference=reference))
    payload = evaluation_request(inputs=inputs).model_dump_json().encode()
    models = asyncio.run(call(app, "/models"))
    assert models[0] == 200
    assert models[1]["models"][0]["input_schema_id"] == inputs.schema_id
    actual, run = asyncio.run(call(app, "/evaluations", body=payload))
    assert actual == 200
    assert run["owner_id"] == "owner"
    path = "/runs/" + run["run_id"]
    assert asyncio.run(call(app, path)) == (200, run)
    projected_status, projection = asyncio.run(call(app, path + "/outputs/value"))
    assert projected_status == 200
    assert projection["results"][0]["status"] == status
    assert projection["trace"] == run["trace"]
    assert projection["verification"] == run["verification"]
    assert projection["results"][0]["value"] == run["outputs"][0]["value"] == value
    error(asyncio.run(call(app, path, token="other")), 404, "not_found", False)
    error(
        asyncio.run(call(app, path + "/outputs/value", token="other")),
        404,
        "not_found",
        False,
    )
    error(asyncio.run(call(app, path + "/outputs/absent")), 404, "not_found", False)


def test_auth_before_receiving_body_and_safe_validation(service, inputs):
    app = build(service())

    async def forbidden_receive():
        pytest.fail("request body read before authentication")

    for token in (None, "expired", "wrong-audience", "private-token"):
        result = asyncio.run(
            call(app, "/evaluations", token=token, receive=forbidden_receive)
        )
        assert "private" not in str(error(result, 401, "unauthorized", False))
    payload = evaluation_request(inputs=inputs).model_dump(mode="json")
    payload["owner_id"] = "other"
    payload["secret-supplied-key"] = "private-value"
    payload["assumptions"]["version"] = ["private-version"]
    result = asyncio.run(call(app, "/evaluations", body=json.dumps(payload).encode()))
    body = error(result, 422, "invalid_request", False)
    assert "private" not in str(body) and "secret-supplied-key" not in str(body)
    assert {"path": ["assumptions", "version"], "code": "string_type"} in body["fields"]
    error(
        asyncio.run(call(app, "/evaluations", body=b"{")), 422, "invalid_request", False
    )
    payload = evaluation_request(inputs=inputs).model_dump(mode="json")
    payload["method_version"] = "uninstalled"
    error(
        asyncio.run(call(app, "/evaluations", body=json.dumps(payload).encode())),
        422,
        "unsupported_method",
        False,
    )


def test_body_limits_and_admission_cover_inbound_reads(service):
    app = build(service(), body_timeout_seconds=0.1)

    async def exercise():
        reading = asyncio.Event()

        async def stalled():
            reading.set()
            await asyncio.Future()

        request = asyncio.create_task(call(app, "/evaluations", receive=stalled))
        await reading.wait()
        error(await call(app, "/evaluations", body=b"{}"), 503, "capacity", True)
        error(await asyncio.wait_for(request, 1), 503, "timeout", True)
        error(
            await call(app, "/evaluations", length=2**21 + 1, receive=stalled),
            413,
            "request_too_large",
            False,
        )
        chunks = iter((b"x" * 2**20, b"x" * 2**20, b"x"))

        async def stream():
            return {"type": "http.request", "body": next(chunks), "more_body": True}

        error(
            await call(app, "/evaluations", receive=stream),
            413,
            "request_too_large",
            False,
        )
        exact_limit = b"{}" + b" " * (2**21 - 2)
        error(
            await call(app, "/evaluations", body=exact_limit, length=len(exact_limit)),
            422,
            "invalid_request",
            False,
        )

    asyncio.run(exercise())


@pytest.mark.parametrize("http_deadline", [False, True])
def test_concrete_evaluation_timeout(service, inputs, tmp_path, http_deadline):
    marker = tmp_path / "worker-started"
    app = build(
        service(
            calculate=partial(slow_callback, marker),
            timeout=5 if http_deadline else 1.5,
        ),
        request_timeout_seconds=1.5 if http_deadline else 60,
    )
    payload = evaluation_request(inputs=inputs).model_dump_json().encode()

    async def exercise():
        result = await asyncio.wait_for(call(app, "/evaluations", body=payload), 3)
        error(result, 503, "timeout", True)

    asyncio.run(exercise())
    assert marker.exists()
    assert not (tmp_path / "runs").exists()


def test_envelope_hides_execution_failure(inputs):
    class FailingOrchestrator:
        def evaluate(self, request, principal, *, cancel):
            assert isinstance(cancel, Event)
            raise ExecutionError("private-provider-detail")

    app = build(FailingOrchestrator())
    payload = evaluation_request(inputs=inputs).model_dump_json().encode()
    result = asyncio.run(call(app, "/evaluations", body=payload))
    assert "private" not in str(error(result, 503, "evaluation_unavailable", True))


def test_real_assertions_and_spoofed_header_cannot_read_body(service):
    verifier = IdentityVerifier((("active", CURRENT.encode()),))
    app = create_model_app(service(), ModelRegistry((TestMethod(),)), verifier)
    now = int(time())
    rejected = (
        None,
        assertion(claims={"iat": now - 40, "exp": now - 1}),
        assertion(claims={"aud": "other-service"}),
        assertion(claims={"sub": "owner"}, secret=PREVIOUS),
    )

    async def forbidden_receive():
        pytest.fail("invalid assertion must not cause a body read")

    for token in rejected:
        result = asyncio.run(
            call(
                app,
                "/evaluations",
                token=token,
                receive=forbidden_receive,
                extra_headers=[(b"x-user-id", b"owner")],
            )
        )
        error(result, 401, "unauthorized", False)
    valid = assertion()
    assert asyncio.run(call(app, "/models", token=valid))[0] == 200
    result = asyncio.run(
        call(
            app,
            "/evaluations",
            token=valid,
            receive=forbidden_receive,
            extra_headers=[(b"authorization", f"Bearer {valid}".encode())],
        )
    )
    error(result, 401, "unauthorized", False)


@pytest.mark.parametrize("cancel_request_task", [False, True])
def test_disconnect_holds_admission_until_worker_finishes(inputs, cancel_request_task):
    active = Event()
    cancelled = Event()
    release = Event()

    class RunningOrchestrator:
        def evaluate(self, request, principal, *, cancel):
            active.set()
            assert cancel.wait(2)
            cancelled.set()
            assert release.wait(2)
            raise ExecutionError("cancelled")

    app = build(RunningOrchestrator())
    payload = evaluation_request(inputs=inputs).model_dump_json().encode()

    async def exercise():
        disconnect = asyncio.Event()
        sent = False

        async def receive():
            nonlocal sent
            if not sent:
                sent = True
                return {"type": "http.request", "body": payload}
            await disconnect.wait()
            return {"type": "http.disconnect"}

        running = asyncio.create_task(call(app, "/evaluations", receive=receive))
        try:
            assert await asyncio.to_thread(active.wait, 1)
            if cancel_request_task:
                running.cancel()
            else:
                disconnect.set()
            assert await asyncio.to_thread(cancelled.wait, 1)
            error(await call(app, "/evaluations", body=payload), 503, "capacity", True)
        finally:
            release.set()
        if cancel_request_task:
            with pytest.raises(asyncio.CancelledError):
                await asyncio.wait_for(running, 1)
        else:
            error(await asyncio.wait_for(running, 1), 503, "cancelled", True)

    asyncio.run(exercise())


@pytest.mark.parametrize("unconfirmed", [False, True])
@pytest.mark.parametrize("disconnect", [False, True])
def test_committed_result_remains_recoverable_after_cancellation(
    service,
    inputs,
    unconfirmed,
    disconnect,
):
    orchestrator = service()
    request = evaluation_request(inputs=inputs)
    saved = orchestrator.evaluate(request, Principal(subject="owner"))
    active = Event()

    class CommittedOrchestrator:
        get = orchestrator.get

        def evaluate(self, request, principal, *, cancel):
            active.set()
            assert cancel.wait(2)
            if unconfirmed:
                raise RunPublishedError(saved.run_id)
            return saved

    app = build(
        CommittedOrchestrator(), request_timeout_seconds=2 if disconnect else 0.15
    )
    payload = request.model_dump_json().encode()

    async def exercise():
        if not disconnect:
            return await call(app, "/evaluations", body=payload)
        sent = False

        async def receive():
            nonlocal sent
            if not sent:
                sent = True
                return {"type": "http.request", "body": payload}
            assert await asyncio.to_thread(active.wait, 1)
            return {"type": "http.disconnect"}

        return await call(app, "/evaluations", receive=receive)

    result = asyncio.run(exercise())
    if unconfirmed:
        body = error(result, 503, "publication_unconfirmed", False)
    else:
        assert result[0] == 200
        body = result[1]
    assert body["run_id"] == saved.run_id
    assert asyncio.run(call(app, "/runs/" + body["run_id"])) == (
        200,
        saved.model_dump(mode="json"),
    )


def test_unexpected_and_read_failures_are_safe(inputs):
    class FailingOrchestrator:
        def evaluate(self, request, principal, *, cancel):
            raise RuntimeError("private exception")

        def get(self, run_id, principal):
            raise RunStoreError("private stored evidence")

    app = build(FailingOrchestrator())
    payload = evaluation_request(inputs=inputs).model_dump_json().encode()
    result = asyncio.run(call(app, "/evaluations", body=payload))
    assert "private" not in str(error(result, 500, "internal_error", False))
    result = asyncio.run(call(app, "/runs/unavailable"))
    assert "private" not in str(error(result, 503, "storage_unavailable", True))
