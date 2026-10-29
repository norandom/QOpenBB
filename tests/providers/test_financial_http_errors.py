"""Mounted financial failure contracts using native OpenBB wrappers and handlers."""
import asyncio
import json
import logging

import pytest
from fastapi import FastAPI
from openbb_core.api.exception_handlers import ExceptionHandlers
from openbb_core.app.model.abstract.error import OpenBBError
from openbb_core.provider.utils.financial_errors import FinancialError
from qopenbb_data.financial_errors import (
    financial_error_response,
    install_financial_error_handlers,
)


def invoke(app, path, query=b""):
    async def run():
        messages = []
        async def receive():
            return {"type": "http.request", "body": b"", "more_body": False}
        async def send(message):
            messages.append(message)
        await app({"type": "http", "asgi": {"version": "3.0"}, "http_version": "1.1",
                   "method": "GET", "scheme": "http", "path": path, "raw_path": path.encode(),
                   "root_path": "", "query_string": query, "headers": [],
                   "server": ("test", 80), "client": ("127.0.0.1", 1)}, receive, send)
        start = next(m for m in messages if m["type"] == "http.response.start")
        body = b"".join(m.get("body", b"") for m in messages if m["type"] == "http.response.body")
        return start["status"], dict(start["headers"]), json.loads(body) if body else None
    return asyncio.run(run())


@pytest.mark.parametrize("code,status", [("upstream", 400), ("authentication", 502),
                                         ("missing_data", 204), ("invalid_parameters", 422)])
def test_formatter(code, status):
    response = financial_error_response(FinancialError(code, provider="fmp"))
    assert response.status_code == status
    if status == 204:
        assert response.body == b""


def test_native_wrappers_mounted_and_unexpected_do_not_escape(caplog):
    native = FastAPI()
    native.add_exception_handler(OpenBBError, ExceptionHandlers.openbb)
    native.add_exception_handler(Exception, ExceptionHandlers.exception)

    @native.get("/financial")
    def financial(kind: str = "typed"):
        if kind == "unexpected":
            raise RuntimeError("SECRET_CANARY")
        raise OpenBBError(OpenBBError(FinancialError("throttling", provider="fmp",
                                                   retry_after_seconds=30)))

    @native.get("/legacy")
    def legacy():
        raise OpenBBError("legacy preserved")

    document = native.openapi()
    document["paths"]["/financial"]["get"]["x-qopenbb-financial"] = {"providers": ["fmp"]}
    install_financial_error_handlers(native, document)
    outer = FastAPI()
    outer.mount("/api", native)
    with caplog.at_level(logging.ERROR):
        typed = invoke(outer, "/api/financial")
        unexpected = invoke(outer, "/api/financial", b"kind=unexpected")
        legacy_response = invoke(outer, "/api/legacy")
    assert typed[0] == 400
    assert typed[1][b"retry-after"] == b"30"
    assert typed[2]["code"] == "throttling"
    assert unexpected[0] == 500
    assert len(unexpected[2]["correlation_id"]) == 32
    assert "SECRET_CANARY" not in caplog.text
    assert legacy_response[2] == {"detail": "legacy preserved"}

@pytest.mark.parametrize("value,expected", [("0", "0"), (86400, "86400"),
    (86401, None), (True, None), ("SECRET_CANARY\r\nX-Key: secret", None), (-1, None)])
def test_retry_bounds(value, expected):
    response = financial_error_response(FinancialError("throttling", retry_after_seconds=value))
    assert response.headers.get("retry-after") == expected


@pytest.mark.parametrize("status", [True, 200, 401, 403, 429, 503, "400"])
def test_invalid_status_override(status):
    with pytest.raises(ValueError):
        financial_error_response(FinancialError("upstream"), status_code=status)


def native_case(error, *, parameter=False):
    native = FastAPI()
    native.add_exception_handler(OpenBBError, ExceptionHandlers.openbb)
    native.add_exception_handler(Exception, ExceptionHandlers.exception)
    @native.get("/financial")
    def financial(limit: int = 1):
        raise error
    document = native.openapi()
    document["paths"]["/financial"]["get"]["x-qopenbb-financial"] = {"providers": ["fmp"]}
    install_financial_error_handlers(native, document)
    outer = FastAPI()
    outer.mount("/api", native)
    return invoke(outer, "/api/financial", b"limit=SECRET_CANARY" if parameter else b"")


@pytest.mark.parametrize("kind,code,status", [
    ("provider", "invalid_parameters", 400), ("provider", "invalid_response", 400),
    ("auth", "entitlement", 502), ("empty", "missing_data", 204),
])
def test_exact_fmp_legacy_statuses(kind, code, status, caplog):
    from openbb_fmp.utils.errors import FMPEmptyData, FMPError, FMPUnauthorized
    cls = {"provider": FMPError, "auth": FMPUnauthorized, "empty": FMPEmptyData}[kind]
    error = cls("SECRET_CANARY")
    error.code = code
    error.provider = "fmp"
    response = native_case(OpenBBError(error))
    assert response[0] == status
    if status != 204:
        assert response[2]["code"] == code
    assert "SECRET_CANARY" not in caplog.text


@pytest.mark.parametrize("kind", ["unknown", "cycle", "deep", "subclass"])
def test_unrecognized_and_bounded_wrappers_fail_closed(kind, caplog):
    class Unknown(OpenBBError):
        pass
    error = FinancialError("upstream", provider="fmp")
    if kind == "unknown":
        error = RuntimeError("SECRET_CANARY")
        error.original = FinancialError("upstream")
    elif kind == "cycle":
        error = OpenBBError(None)
        error.original = error
    elif kind == "deep":
        for _ in range(10):
            error = OpenBBError(error)
    else:
        error = Unknown(error)
    response = native_case(error)
    assert response[0] == 500
    assert response[2]["code"] == "internal_error"
    assert "SECRET_CANARY" not in caplog.text


def test_request_validation_locations_and_logs(caplog):
    response = native_case(RuntimeError("unreached"), parameter=True)
    assert response[0] == 422
    assert response[2]["errors"] == [{"loc": ["query", "limit"], "msg": "Invalid parameter."}]
    assert "SECRET_CANARY" not in json.dumps(response[2]) + caplog.text


@pytest.mark.parametrize("boundary,code,status", [("query", "invalid_parameters", 422),
                                                ("result", "invalid_response", 502)])
def test_explicit_validation_boundaries(boundary, code, status, caplog):
    from openbb_core.provider.utils.financial_validation import (
        validate_financial_query,
        validate_financial_result,
    )
    from pydantic import BaseModel
    class Row(BaseModel):
        value: int
    validator = validate_financial_query if boundary == "query" else validate_financial_result
    try:
        validator(Row, {"value": "SECRET_CANARY"}, provider="fmp")
    except FinancialError as error:
        response = native_case(OpenBBError(error))
    assert response[0] == status
    assert response[2]["code"] == code
    assert "SECRET_CANARY" not in json.dumps(response[2]) + caplog.text


def test_response_validation_and_raw_model_validation(caplog):
    from fastapi.exceptions import ResponseValidationError
    from pydantic import BaseModel, ValidationError
    errors = [{"type": "int_parsing", "loc": ("response", "value"),
               "msg": "SECRET_CANARY", "input": "SECRET_CANARY"}]
    assert native_case(ResponseValidationError(errors))[2]["code"] == "invalid_response"
    class QueryParamsMisleadingTitle(BaseModel):
        value: int
    try:
        QueryParamsMisleadingTitle(value="SECRET_CANARY")
    except ValidationError as error:
        response = native_case(OpenBBError(error))
    assert response[0] == 502
    assert response[2]["code"] == "invalid_response"
    assert "SECRET_CANARY" not in caplog.text


@pytest.mark.parametrize("dataset,path,module,fetcher,provider", [
    ("EquityInfo", "/api/v1/equity/profile", "openbb_fmp.models.equity_profile", "FMPEquityProfileFetcher", "fmp"),
    ("IncomeStatement", "/api/v1/equity/fundamental/income", "openbb_fmp.models.income_statement", "FMPIncomeStatementFetcher", "fmp"),
    ("FredSeries", "/api/v1/economy/fred_series", "openbb_fred.models.series", "FredSeriesFetcher", "fred"),
])
def test_installed_baseline_routes_execute_native_wrappers(
    monkeypatch, caplog, dataset, path, module, fetcher, provider,
):
    from importlib import import_module

    from openbb_core.api.app_loader import AppLoader
    from openbb_core.api.rest_api import app as installed
    from openbb_core.app.model.user_settings import UserSettings
    from openbb_core.app.route_iter import iter_api_routes
    from openbb_core.app.service.user_service import UserService
    from openbb_core.provider.registry_map import RegistryMap
    from qopenbb_data.financial_openapi import project_financial_openapi

    settings = UserSettings.model_construct()
    settings.credentials.fmp_api_key = "synthetic-key"
    settings.credentials.fred_api_key = "synthetic-key"
    monkeypatch.setattr(UserService, "read_from_file", lambda *a, **k: settings)
    async def forbidden_network(*args, **kwargs):
        raise AssertionError("Native fixture must not access a provider")
    monkeypatch.setattr("openbb_core.provider.utils.helpers.amake_request", forbidden_network)
    seen = []
    async def failing_extract(*args, **kwargs):
        seen.append(True)
        raise FinancialError("timeout", provider=provider, retry_after_seconds=7)
    cls = getattr(import_module(module), fetcher)
    monkeypatch.setattr(cls, "extract_data", failing_extract)
    native = FastAPI()
    native.router.routes = list(installed.router.routes)
    AppLoader.add_exception_handlers(native)
    routes = [r for r in iter_api_routes(installed)
              if (getattr(r, "openapi_extra", None) or {}).get("model") == dataset]
    assert len(routes) == 1
    document = project_financial_openapi(installed.openapi(), routes, RegistryMap(),
                                         required_models={dataset})
    install_financial_error_handlers(native, document)
    outer = FastAPI()
    outer.mount("/mounted", native)
    response = invoke(outer, "/mounted" + path,
                      f"provider={provider}&symbol=AAPL&use_cache=false".encode())
    assert seen
    assert response[0] == 400, response
    assert response[2]["code"] == "timeout"
    assert response[2]["provider"] == provider
    assert response[1][b"retry-after"] == b"7"
    assert "synthetic-key" not in caplog.text


@pytest.mark.parametrize("depth", [1, 3, 8])
def test_recognized_legacy_string_wrappers_preserve_400(depth, caplog):
    error = "SECRET_CANARY"
    for _ in range(depth):
        error = OpenBBError(error)
    response = native_case(error)
    assert response[0] == 400
    assert response[2]["code"] == "upstream"
    assert "SECRET_CANARY" not in json.dumps(response[2]) + caplog.text


def test_started_response_failure_aborts_without_exception_leak(caplog):
    from qopenbb_data.financial_errors import _FinancialBoundary, _operations
    async def stream(scope, receive, send):
        await send({"type": "http.response.start", "status": 200, "headers": []})
        await send({"type": "http.response.body", "body": b'{"results":', "more_body": True})
        raise RuntimeError("SECRET_CANARY")
    async def run():
        messages = []
        async def send(message):
            messages.append(message)
        async def receive():
            return {"type": "http.request"}
        document = {"paths": {"/stream": {"get": {"operationId": "stream",
                    "x-qopenbb-financial": {"providers": ["fmp"]}}}}}
        boundary = _FinancialBoundary(stream, _operations(document))
        with pytest.raises(FinancialError) as caught:
            await boundary({"type": "http", "path": "/stream", "method": "GET"}, receive, send)
        assert caught.value.__context__ is None
        assert caught.value.__cause__ is None
        assert caught.value.code == "invalid_response"
        return messages
    messages = asyncio.run(run())
    assert messages[0]["status"] == 200
    assert messages[-1]["more_body"] is True
    assert len([m for m in messages if m["type"] == "http.response.start"]) == 1
    assert "SECRET_CANARY" not in repr(messages) + caplog.text
    assert "internal_error" in caplog.text

def test_mounted_started_response_aborts_safely_through_server_middleware(caplog):
    from starlette.responses import Response
    class BrokenResponse(Response):
        async def __call__(self, scope, receive, send):
            await send({"type": "http.response.start", "status": 200, "headers": []})
            await send({"type": "http.response.body", "body": b'{"results":', "more_body": True})
            raise RuntimeError("SECRET_CANARY")
    native = FastAPI()
    native.add_exception_handler(Exception, ExceptionHandlers.exception)
    @native.get("/stream")
    def stream():
        return BrokenResponse()
    document = native.openapi()
    document["paths"]["/stream"]["get"]["x-qopenbb-financial"] = {"providers": ["fmp"]}
    install_financial_error_handlers(native, document)
    outer = FastAPI()
    outer.mount("/mounted", native)
    with pytest.raises(FinancialError) as caught:
        invoke(outer, "/mounted/stream")
    assert caught.value.__context__ is None
    assert caught.value.__cause__ is None
    assert "SECRET_CANARY" not in caplog.text
    assert "invalid_response" == caught.value.code
