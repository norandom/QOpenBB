"""Provider selection must be settled before native request execution."""

import asyncio
from copy import deepcopy

import pytest
from fastapi import FastAPI, Request
from qopenbb_data.financial_policy import FinancialProviderPolicy


def invoke(app, path="/financial", query=b"", method="GET", root_path="", response_headers=None):
    async def run():
        messages = []

        async def receive():
            return {"type": "http.request", "body": b"", "more_body": False}

        async def send(message):
            messages.append(message)

        await app({"type": "http", "asgi": {"version": "3.0"}, "http_version": "1.1",
                   "method": method, "scheme": "http", "path": path, "raw_path": path.encode(),
                   "root_path": root_path, "query_string": query, "headers": [],
                   "server": ("test", 80), "client": ("127.0.0.1", 1)}, receive, send)
        status = next(m["status"] for m in messages if m["type"] == "http.response.start")
        if response_headers is not None:
            response_headers.update(next(m["headers"] for m in messages
                                         if m["type"] == "http.response.start"))
        body = b"".join(m.get("body", b"") for m in messages if m["type"] == "http.response.body")
        return status, body

    return asyncio.run(run())


def document(policy="explicit", providers=None):
    choices = ["fmp", "other"] if providers is None else providers
    return {"paths": {"/financial": {"get": {
        "x-qopenbb-financial": {"provider_policy": policy, "providers": choices}
    }}}}


class Forwarded:
    def __init__(self):
        self.scopes = []

    async def __call__(self, scope, receive, send):
        self.scopes.append(scope)
        if scope["type"] == "http":
            await send({"type": "http.response.start", "status": 200, "headers": []})
            await send({"type": "http.response.body", "body": scope["query_string"]})


@pytest.mark.parametrize("query", ["", "provider", "provider=", "provider=%20",
    "provider=fmp&provider=fmp", "provider=fmp&provider=other",
    "provider=unknown_SECRET", "provider=FMP", "provider=fmp%00"])
def test_invalid_selection_stops_before_io(query):
    downstream = Forwarded()
    app = FinancialProviderPolicy(downstream, document=document())
    status, body = invoke(app, query=query.encode())
    assert status == 422
    assert b'"code":"invalid_parameters"' in body
    assert b"provider" in body
    assert b"SECRET" not in body
    assert downstream.scopes == []


@pytest.mark.parametrize("query", ["provider=fmp", "a=1&provider=other&a=2",
                                 "provider=%66mp&symbol=BRK%2EB"])
def test_explicit_selection_reaches_native_unchanged(query):
    downstream = Forwarded()
    app = FinancialProviderPolicy(downstream, document=document())
    status, body = invoke(app, query=query.encode())
    assert status == 200
    assert body == query.encode()
    assert len(downstream.scopes) == 1


@pytest.mark.parametrize("path,method,policy", [
    ("/financial", "POST", "explicit"), ("/financial/", "GET", "explicit"),
    ("/financial", "HEAD", "explicit"),
    ("/health", "GET", "explicit"), ("/financial/child", "GET", "explicit"),
    ("/financial", "GET", "baseline_default"),
])
def test_other_operations_and_baseline_pass_through(path, method, policy):
    downstream = Forwarded()
    app = FinancialProviderPolicy(downstream, document=document(policy))
    assert invoke(app, path, method=method)[0] == 200
    assert len(downstream.scopes) == 1


def test_mount_and_root_path_use_exact_installed_path():
    downstream = Forwarded()
    inner = FinancialProviderPolicy(downstream, document=document())
    outer = FastAPI()
    outer.mount("/api", inner)
    missing = invoke(outer, "/proxy/api/financial", root_path="/proxy")
    selected = invoke(outer, "/proxy/api/financial", query=b"provider=fmp", root_path="/proxy")
    assert missing[0] == 422
    assert selected[0] == 200
    assert len(downstream.scopes) == 1


@pytest.mark.parametrize("kind", ["websocket", "lifespan"])
def test_non_http_scope_is_forwarded_by_identity(kind):
    downstream = Forwarded()
    app = FinancialProviderPolicy(downstream, document=document())
    scope = {"type": kind}
    asyncio.run(app(scope, None, None))
    assert downstream.scopes[0] is scope


@pytest.mark.parametrize("descriptor", [None, {}, {"provider_policy": "automatic", "providers": ["fmp"]},
    {"provider_policy": "explicit", "providers": []},
    {"provider_policy": "explicit", "providers": "fmp"},
    {"provider_policy": "explicit", "providers": [""]},
    {"provider_policy": "baseline_default", "providers": ["fmp", "fmp"]},
    {"provider_policy": "explicit", "providers": [3]},
    {"provider_policy": "explicit", "providers": [" fmp"]}])
def test_malformed_advertisement_fails_configuration(descriptor):
    source = document()
    source["paths"]["/financial"]["get"]["x-qopenbb-financial"] = descriptor
    with pytest.raises((TypeError, ValueError), match="[Ff]inancial"):
        FinancialProviderPolicy(Forwarded(), document=source)


def test_compilation_does_not_mutate_openapi():
    source = document()
    before = deepcopy(source)
    FinancialProviderPolicy(Forwarded(), document=source)
    assert source == before


def test_failed_selected_provider_is_not_retried_or_replaced():
    calls = []

    async def failing(scope, receive, send):
        calls.append(scope["query_string"])
        raise RuntimeError("selected provider failed")

    guard = FinancialProviderPolicy(failing, document=document())
    with pytest.raises(RuntimeError, match="selected provider failed"):
        invoke(guard, query=b"provider=other")
    assert calls == [b"provider=other"]


def test_baseline_query_and_original_scope_are_retained():
    downstream = Forwarded()
    guard = FinancialProviderPolicy(downstream, document=document("baseline_default"))
    query = b"provider=unknown&provider=&symbol=BRK%2EB"
    assert invoke(guard, query=query) == (200, query)


def test_compiled_choices_do_not_follow_later_document_mutation():
    source = document()
    downstream = Forwarded()
    guard = FinancialProviderPolicy(downstream, document=source)
    source["paths"]["/financial"]["get"]["x-qopenbb-financial"]["providers"].append("late")
    assert invoke(guard, query=b"provider=late")[0] == 422
    assert downstream.scopes == []


def test_real_installed_baseline_descriptors_retain_native_defaults():
    from openbb_core.api.rest_api import app
    from openbb_core.app.route_iter import iter_api_routes
    from openbb_core.provider.registry_map import RegistryMap
    from qopenbb_data.financial_openapi import project_financial_openapi

    required = {"EquityInfo", "IncomeStatement", "FredSeries"}
    routes = [route for route in iter_api_routes(app)
              if (getattr(route, "openapi_extra", None) or {}).get("model") in required]
    assert {route.openapi_extra["model"] for route in routes} == required
    source = project_financial_openapi(app.openapi(), routes, RegistryMap(),
                                       required_models=required)
    downstream = Forwarded()
    guard = FinancialProviderPolicy(downstream, document=source)
    for route in routes:
        assert invoke(guard, route.path)[0] == 200
    assert len(downstream.scopes) == 3


@pytest.mark.parametrize("code,retry", [("throttling", 37), ("timeout", None)])
def test_outer_guard_and_mounted_safe_failures_share_selection_contract(code, retry, caplog):
    from openbb_core.provider.utils.financial_errors import FinancialError
    from qopenbb_data.financial_errors import install_financial_error_handlers

    calls = []
    native = FastAPI()

    @native.get("/financial")
    def financial(provider: str, request: Request):
        calls.append((provider, request.scope["query_string"]))
        raise FinancialError(code, provider=provider, retry_after_seconds=retry)

    source = native.openapi()
    descriptor = document()["paths"]["/financial"]["get"]["x-qopenbb-financial"]
    source["paths"]["/financial"]["get"]["x-qopenbb-financial"] = descriptor
    install_financial_error_handlers(native, source)
    mounted = FastAPI()
    mounted.mount("/api", native)
    outer_source = deepcopy(source)
    outer_source["paths"] = {"/api/financial": source["paths"]["/financial"]}
    guard = FinancialProviderPolicy(mounted, document=outer_source)
    assert invoke(guard, "/api/financial")[0] == 422
    assert calls == []
    headers = {}
    status, body = invoke(guard, "/api/financial", query=b"provider=fmp&unused=SECRET_CANARY",
                          response_headers=headers)
    assert status == 400
    assert calls == [("fmp", b"provider=fmp&unused=SECRET_CANARY")]
    assert code.encode() in body
    assert b"SECRET_CANARY" not in body
    assert "SECRET_CANARY" not in caplog.text
    if retry is not None:
        assert b'"retry_after_seconds":37' in body
        assert headers[b"retry-after"] == b"37"
    else:
        assert b"retry-after" not in headers
