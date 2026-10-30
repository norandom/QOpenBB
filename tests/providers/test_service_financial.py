"""Actual service wiring uses installed commands and makes no provider requests."""

import asyncio
import json
import logging
import os
from copy import deepcopy
from datetime import UTC, datetime

import pytest
from test_discovery import FMP_MODELS
from test_runtime import get

# Explicit fixture re-exports keep setup shared without argument-shadow warnings.
from test_runtime import packaged_catalog as packaged_catalog  # noqa: PLC0414
from test_runtime import runtime as runtime  # noqa: PLC0414

EXPLICIT = ["/equity/search", "/equity/compare/peers", "/equity/price/historical",
            *["/equity/fundamental/" + name for name in
              ("balance", "cash", "metrics", "ratios", "enterprise_values")]]
ENTERPRISE = "/api/v1/equity/fundamental/enterprise_values"
SECRET = "PRIVATE_SERVICE_CANARY"


@pytest.fixture(autouse=True)
def no_provider_io(monkeypatch):
    async def forbidden(*args, **kwargs):
        raise AssertionError("Provider transport must not run")
    monkeypatch.setattr("openbb_core.provider.utils.helpers.amake_request", forbidden)
    monkeypatch.setattr("openbb_fmp.utils.helpers.get_data_many", forbidden)


@pytest.fixture
def enterprise(monkeypatch):
    from openbb_fmp.models.enterprise_values import FMPEnterpriseValuesFetcher
    from openbb_fmp.utils.helpers import FMPAcquisition

    calls = []
    observation = {"symbol": "ABC", "date": "2025-01-01", "stockPrice": 0,
                   "numberOfShares": 10, "marketCapitalization": 100,
                   "minusCashAndCashEquivalents": 200, "addTotalDebt": -1,
                   "enterpriseValue": -7, "reportedCurrency": "EUR"}
    async def extract(*args, **kwargs):
        calls.append(True)
        return FMPAcquisition([deepcopy(observation)], datetime(2025, 1, 2, tzinfo=UTC))
    monkeypatch.setattr(FMPEnterpriseValuesFetcher, "extract_data", extract)
    return FMPEnterpriseValuesFetcher, calls


def test_served_discovery_matches_openapi_without_provider_access(runtime):
    status, catalog = asyncio.run(get(runtime, "/datasets.json"))
    assert status == 200
    assert {item["dataset"] for item in catalog["datasets"]} == FMP_MODELS | {"FredSeries"}
    assert catalog["identity"]["source_revision"] == os.environ["QOPENBB_DATA_SOURCE_REVISION"]
    assert catalog["identity"]["generation_revision"] == os.environ["QOPENBB_DATA_GENERATION_REVISION"]
    assert catalog["identity"]["image_digest"] is None
    status, schema = asyncio.run(get(runtime, "/openapi.json"))
    assert status == 200 and schema == runtime.openapi()
    assert any(path.startswith("/api/v1/economy/") and
               "x-qopenbb-financial" not in operation.get("get", {})
               for path, operation in schema["paths"].items())
    for dataset in catalog["datasets"]:
        descriptor = schema["paths"][dataset["command"]["path"]]["get"]["x-qopenbb-financial"]
        assert descriptor["variants"] == dataset["variants"]
        for states in dataset["coverage"].values():
            assert states["installed"]["status"] == "verified"
            assert states["account_access"]["status"] == "unknown"
            assert states["real_data"]["status"] == "verified"
            assert states["widget"]["status"] == "unknown"
    assert len([family for family in catalog["coverage"]["families"] if family["provider"] == "fmp"]) == 13
    assert "fixture-runtime" not in json.dumps([catalog, schema])
    assert asyncio.run(get(runtime, "/datasets.json", method="POST"))[0] in {404, 405}


@pytest.mark.parametrize("path", EXPLICIT)
def test_new_commands_require_provider_before_any_execution(runtime, path):
    status, body = asyncio.run(get(runtime, "/api/v1" + path, b"symbol=ABC&query=Apple"))
    assert status == 422 and body["code"] == "invalid_parameters"
    operation = runtime.openapi()["paths"]["/api/v1" + path]["get"]
    assert operation["responses"]["422"]["content"]["application/json"]["schema"] == (
        operation["x-qopenbb-financial"]["error_schema"])
    assert body["errors"] == [{"loc": ["query", "provider"], "msg": "Invalid parameter."}]


def test_explicit_enterprise_matches_python_values_and_financial_metadata(runtime, enterprise):
    fetcher, calls = enterprise
    status, body = asyncio.run(get(runtime, ENTERPRISE, b"provider=fmp&symbol=ABC"))
    assert status == 200 and len(calls) == 1
    result = asyncio.run(fetcher.fetch_data({"symbol": "ABC"}, {"fmp_api_key": "synthetic"}))
    assert len(calls) == 2
    assert body["provider"] == "fmp"
    assert body["results"] == [row.model_dump(mode="json", by_alias=False) for row in result.result]
    metadata = body["extra"]["results_metadata"]["__qopenbb_financial__"]
    assert metadata["fields"] == result.metadata["__qopenbb_financial__"]["fields"]
    assert metadata["fields"]["number_of_shares"]["unit"] == "shares"
    assert metadata["fields"]["enterprise_value"]["value_origin"] == "provider_calculation"
    assert body["results"][0]["enterprise_value"] == -7
    assert body["results"][0]["stock_price"] == 0


@pytest.mark.parametrize("kind,status,code", [("typed", 400, "throttling"),
                                            ("unexpected", 500, "internal_error"),
                                            ("row", 502, "invalid_response")])
def test_actual_mounted_failures_are_safe(runtime, monkeypatch, caplog, kind, status, code):
    from openbb_core.provider.utils.financial_errors import FinancialError
    from openbb_fmp.models.enterprise_values import FMPEnterpriseValuesFetcher
    from openbb_fmp.utils.helpers import FMPAcquisition

    async def extract(*args, **kwargs):
        if kind == "typed":
            raise FinancialError("throttling", provider="fmp", retry_after_seconds=7)
        if kind == "row":
            return FMPAcquisition([{"symbol": "ABC", "stockPrice": SECRET}], datetime.now(UTC))
        raise RuntimeError(SECRET)
    monkeypatch.setattr(FMPEnterpriseValuesFetcher, "extract_data", extract)
    with caplog.at_level(logging.ERROR):
        actual_status, body = asyncio.run(get(runtime, ENTERPRISE, b"provider=fmp&symbol=ABC"))
    assert actual_status == status and body["code"] == code
    assert SECRET not in json.dumps(body) + caplog.text
    if kind == "unexpected":
        assert len(body["correlation_id"]) == 32


def test_request_validation_omits_supplied_values(runtime, caplog):
    with caplog.at_level(logging.ERROR):
        status, body = asyncio.run(get(runtime, ENTERPRISE,
                                      f"provider=fmp&symbol=ABC&limit={SECRET}".encode()))
    assert status == 422 and body["code"] == "invalid_parameters"
    assert SECRET not in json.dumps(body) + caplog.text


def test_factory_is_independent_after_native_and_service_requests(runtime, enterprise):
    from openbb_core.api.rest_api import app as template
    from qopenbb_data.app import create_app

    handlers = dict(template.exception_handlers)
    assert asyncio.run(get(template, ENTERPRISE, b"provider=fmp&symbol=ABC"))[0] == 200
    assert asyncio.run(get(runtime, ENTERPRISE, b"provider=fmp&symbol=ABC"))[0] == 200
    second = create_app()
    assert asyncio.run(get(second, "/datasets.json"))[0] == 200
    assert asyncio.run(get(second, ENTERPRISE, b"symbol=ABC"))[0] == 422
    assert template.exception_handlers == handlers
    assert not any("x-qopenbb-financial" in item.get("get", {})
                   for item in template.openapi()["paths"].values())


def test_invalid_runtime_identity_is_rejected_without_echo(monkeypatch):
    from qopenbb_data.app import create_app

    monkeypatch.setenv("QOPENBB_DATA_SOURCE_REVISION", SECRET)
    with pytest.raises(ValueError) as error:
        create_app()
    assert SECRET not in str(error.value)
