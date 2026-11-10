"""Actual service wiring uses installed commands and makes no provider requests."""

import asyncio
import json
import logging
import os
from copy import deepcopy
from datetime import UTC, datetime
from pathlib import Path
from urllib.parse import urlencode

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


@pytest.fixture
def statement_contract(monkeypatch):
    """Exercise the consumer independently of the provider integration lane."""
    from openbb_core.provider.standard_models.financial_metadata import FinancialResultMetadata
    from openbb_core.provider.utils.financial_validation import validate_financial_result
    from openbb_fmp.models.income_statement import FMPIncomeStatementFetcher
    from openbb_fmp.utils.helpers import FMPAcquisition

    fetcher = FMPIncomeStatementFetcher
    transform = fetcher.transform_data
    evidence = {"rows": [dict(
        row_index=index, source_ordinal=ordinal, fiscal_year=2025, fiscal_period="Q2",
        period_end="2025-06-30", requested_frequency="quarter",
        facts=[dict(semantic_key="filing_date", source_field="filingDate",
                    presence="null", value=None)],
    ) for index, ordinal in enumerate([4, 1])]}
    payload = [{"symbol": "ABC", "date": "2025-06-30", "fiscalYear": "2025",
                "period": "Q2", "revenue": value, "reportedCurrency": "EUR"}
               for value in [0, None]]

    async def extract(*args, **kwargs):
        return FMPAcquisition(deepcopy(payload), datetime(2025, 7, 1, tzinfo=UTC))

    def controlled(query, data, **kwargs):
        result = transform(query, data, **kwargs)
        common = deepcopy(result.metadata["__qopenbb_financial__"])
        common["statement_provenance"] = deepcopy(evidence)
        result.metadata = validate_financial_result(
            FinancialResultMetadata, common, provider="fmp").as_metadata()
        return result

    monkeypatch.setattr(fetcher, "extract_data", extract)
    monkeypatch.setattr(fetcher, "transform_data", controlled)
    return fetcher, evidence


def test_statement_fixture_native_and_python_metadata_are_equivalent(runtime, statement_contract):
    from openbb_core.provider.standard_models.financial_metadata import FinancialResultMetadata
    from pydantic import ValidationError, create_model

    fetcher, _ = statement_contract
    parameters = {"symbol": "ABC", "period": "quarter", "limit": 2}
    result = asyncio.run(fetcher.fetch_data(parameters, {"fmp_api_key": "synthetic"}))
    status, body = asyncio.run(get(runtime, "/api/v1/equity/fundamental/income",
                                  urlencode({"provider": "fmp", **parameters}).encode()))
    assert status == 200
    common = body["extra"]["results_metadata"]["__qopenbb_financial__"]
    assert common == result.metadata["__qopenbb_financial__"]
    assert body["results"] == [row.model_dump(mode="json", by_alias=False,
                              exclude_unset=True) for row in result.result]
    assert body["results"][0]["revenue"] == 0 and body["results"][1]["revenue"] is None
    rows = common["statement_provenance"]["rows"]
    assert [row["source_ordinal"] for row in rows] == [4, 1]
    assert [row["row_index"] for row in rows] == [0, 1]
    assert all(row["period_end"] == "2025-06-30" for row in rows)
    assert all(row["facts"][0]["presence"] == "null" and row["facts"][0]["value"] is None for row in rows)
    assert all(row["flow_coverage"] == "unknown" and row["duration_days"] is None for row in rows)
    assert common["point_in_time_safe"] is False
    old_fields = {name: (field.annotation, field) for name, field in FinancialResultMetadata.model_fields.items()
                  if name != "statement_provenance"}
    old_reader = create_model("OldStrictConsumer", __config__={"extra": "forbid"}, **old_fields)
    legacy = {key: value for key, value in common.items() if key != "statement_provenance"}
    assert old_reader.model_validate(legacy)
    assert "statement_provenance" not in FinancialResultMetadata.model_validate(legacy).model_dump(mode="json")
    with pytest.raises(ValidationError, match="extra_forbidden"):
        old_reader.model_validate(common)


@pytest.mark.parametrize("malformation", ["index", "ordinal", "count", "fact", "reference"])
def test_statement_fixture_malformed_attribution_has_safe_native_error(
    runtime, statement_contract, caplog, malformation,
):
    from openbb_core.provider.utils.financial_errors import FinancialError

    fetcher, evidence = statement_contract
    if malformation == "index":
        evidence["rows"][0]["row_index"] = 1
    elif malformation == "ordinal":
        evidence["rows"][1]["source_ordinal"] = 4
    elif malformation == "count":
        evidence["rows"].pop()
    elif malformation == "fact":
        evidence["rows"][0]["facts"][0]["value"] = SECRET
    else:
        evidence["rows"][0].update(flow_coverage="annual", coverage_status="supported",
            conventions=[dict(flow_coverage="annual", documentation="https://example.test/docs?token=" + SECRET)])
    with pytest.raises(FinancialError) as failure:
        asyncio.run(fetcher.fetch_data({"symbol": "ABC", "period": "quarter", "limit": 2},
                                       {"fmp_api_key": "synthetic"}))
    assert failure.value.code.value == "invalid_response" and SECRET not in str(failure.value)
    with caplog.at_level(logging.ERROR):
        status, body = asyncio.run(get(runtime, "/api/v1/equity/fundamental/income",
                                      b"provider=fmp&symbol=ABC&period=quarter&limit=2"))
    assert status == 502 and body["code"] == "invalid_response"
    assert SECRET not in json.dumps(body) + caplog.text


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
    historic = json.loads((Path(__file__).resolve().parents[2] /
                           "docs/reference/provider-coverage.json").read_text())
    proofs = {(item["model"], item["provider"]): item["states"]["real_data"]
              for item in historic["datasets"] if "real_data" in item["states"]}
    for dataset in catalog["datasets"]:
        descriptor = schema["paths"][dataset["command"]["path"]]["get"]["x-qopenbb-financial"]
        assert descriptor["variants"] == dataset["variants"]
        for provider, states in dataset["coverage"].items():
            assert states["installed"]["status"] == "verified"
            assert states["account_access"]["status"] == "unknown"
            proof = proofs[dataset["dataset"], provider]["proof"]
            assert states["real_data"]["proof"] == proof
            current = {"source_sha256": catalog["identity"]["source_hashes"][dataset["dataset"]][provider],
                       "contract_sha256": dataset["contract_sha256"][provider]}
            matching = all(current[key] == value for key, value in proof["identity"].items())
            assert states["real_data"]["status"] == ("verified" if matching else "stale")
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
    assert "statement_provenance" not in metadata
    assert metadata["fields"] == result.metadata["__qopenbb_financial__"]["fields"]
    assert metadata["fields"]["number_of_shares"]["unit"] == "shares"
    assert metadata["fields"]["enterprise_value"]["value_origin"] == "provider_calculation"
    assert body["results"][0]["enterprise_value"] == -7
    assert body["results"][0]["stock_price"] == 0


@pytest.mark.parametrize("dataset", ["metrics", "ratios"])
@pytest.mark.parametrize("period_parameters,period", [
    ({}, "annual"), ({"period": "annual"}, "annual"), ({"period": "quarter"}, "quarter"),
], ids=["default-annual", "annual", "quarter"])
@pytest.mark.parametrize("selection", [{}, {"ttm": "exclude"}], ids=["default", "explicit"])
def test_periodic_native_and_python_values_share_effective_query(
    runtime, monkeypatch, dataset, period_parameters, period, selection,
):
    from openbb_fmp.models.financial_ratios import FMPFinancialRatiosFetcher
    from openbb_fmp.models.key_metrics import FMPKeyMetricsFetcher
    from openbb_fmp.utils.helpers import FMPAcquisition

    fetcher = {"metrics": FMPKeyMetricsFetcher, "ratios": FMPFinancialRatiosFetcher}[dataset]
    stamp = datetime(2025, 10, 16, tzinfo=UTC)
    payload = [{"symbol": "ABC", "date": "2025-06-30", "fiscalYear": "2025",
                "period": "FY" if period == "annual" else "Q4", "reportedCurrency": "EUR",
                "enterpriseValue": -7, "evToEBITDA": 0, "priceToEarningsRatio": -7,
                "netProfitMargin": 0}]
    original = deepcopy(payload)
    queries = []

    async def extract(query, *args, **kwargs):
        queries.append(query.model_dump())
        return FMPAcquisition(deepcopy(payload), stamp)

    monkeypatch.setattr(fetcher, "extract_data", extract)
    parameters = {"symbol": "ABC", "limit": 1, **period_parameters, **selection}
    path = "/api/v1/equity/fundamental/" + dataset
    status, body = asyncio.run(get(runtime, path, urlencode({"provider": "fmp", **parameters}).encode()))
    result = asyncio.run(fetcher.fetch_data(parameters, {"fmp_api_key": "synthetic"}))
    assert status == 200 and len(queries) == 2 and queries[0] == queries[1]
    assert body["results"] == [row.model_dump(mode="json", by_alias=False,
                                             exclude_unset=True, exclude_none=True) for row in result.result]
    common = body["extra"]["results_metadata"]["__qopenbb_financial__"]
    assert common == result.metadata["__qopenbb_financial__"]
    assert common["effective_query"] == {"symbol": "ABC", "period": period, "limit": 1, "ttm": "exclude"}
    assert common["schema_version"] == 1 and datetime.fromisoformat(common["retrieved_at"]) == stamp
    field, zero, absent = {"metrics": ("enterprise_value", "ev_to_ebitda", "market_cap"),
                           "ratios": ("price_to_earnings", "net_profit_margin", "price_to_book")}[dataset]
    assert body["results"][0][field] == -7 and body["results"][0][zero] == 0
    # Native serialization omits missing fields; the Python model retains None.
    assert absent not in body["results"][0] and getattr(result.result[0], absent) is None
    assert common["fields"][absent]["availability"] == "missing" and payload == original
    # Periodic selection preserves source values; it establishes no fiscal comparability.
    assert common["transformations"] == [] and common["point_in_time_safe"] is False
    assert common["fields"][field]["value_origin"] == "provider_calculation"
    assert all(value is None for value in common["fields"][field]["financial_basis"].values())


@pytest.mark.parametrize("dataset", ["metrics", "ratios"])
def test_periodic_discovery_retains_existing_choices_and_widget_identity(runtime, dataset):
    root = Path(__file__).resolve().parents[2]
    path = "/api/v1/equity/fundamental/" + dataset
    operation = runtime.openapi()["paths"][path]["get"]
    canonical = json.loads((root / "contracts/openapi.json").read_text())["paths"][path]["get"]
    assert operation["parameters"] == canonical["parameters"]
    assert operation["x-qopenbb-financial"] == canonical["x-qopenbb-financial"]
    parameters = {item["name"]: item["schema"] for item in operation["parameters"]}
    assert parameters["ttm"]["const"] == parameters["ttm"]["default"] == "exclude"
    assert parameters["ttm"]["fmp"]["choices"] == ["exclude"]
    assert parameters["period"]["default"] == "annual"
    assert parameters["period"]["enum"] == ["annual", "quarter"]
    status, widgets = asyncio.run(get(runtime, "/widgets.json"))
    widget_id = "equity_fundamental_" + dataset + "_fmp_obb"
    assert status == 200 and widgets[widget_id]["widgetId"] == widget_id
    assert widgets[widget_id] == json.loads((root / "contracts/widgets.json").read_text())[widget_id]
    selection = next(item for item in widgets[widget_id]["params"] if item["paramName"] == "ttm")
    assert selection["value"] == "exclude" and selection["options"] == [{"label": "exclude", "value": "exclude"}]


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


def test_research_attempt_ceiling_counts_failures_before_transport(monkeypatch):
    from live_financial_support import ResearchRequestBlocked, ResearchRunState, SourceCapture
    from openbb_core.provider.utils import helpers

    reached = []
    async def failing(*args, **kwargs):
        reached.append(True)
        raise RuntimeError(SECRET)
    monkeypatch.setattr(helpers, "amake_request", failing)
    state = ResearchRunState()
    for _ in range(51):
        with monkeypatch.context() as patch:
            SourceCapture(patch, "fmp", state, endpoint="income")
            with pytest.raises(RuntimeError):
                asyncio.run(helpers.amake_request(response_callback=None))
    with monkeypatch.context() as patch:
        SourceCapture(patch, "fred", state, endpoint="DGS10")
        with pytest.raises(ResearchRequestBlocked, match="request_ceiling"):
            asyncio.run(helpers.amake_request(response_callback=None))
    assert state.attempts == len(reached) == 51


@pytest.mark.parametrize("code", ["authentication", "throttling", "entitlement"])
def test_research_typed_failures_stop_provider_or_endpoint(monkeypatch, code):
    from live_financial_support import ResearchRequestBlocked, ResearchRunState, SourceCapture
    from openbb_core.provider.utils import helpers
    from openbb_core.provider.utils.financial_errors import FinancialError

    reached = []
    async def failing(*args, **kwargs):
        reached.append(True)
        raise FinancialError(code, provider="fmp")
    monkeypatch.setattr(helpers, "amake_request", failing)
    state = ResearchRunState()
    with monkeypatch.context() as patch:
        SourceCapture(patch, "fmp", state, endpoint="custom_dcf", kind="direct_provider")
        with pytest.raises(FinancialError):
            asyncio.run(helpers.amake_request(response_callback=None))
    with pytest.raises(ResearchRequestBlocked, match=code):
        state.before_request("fmp", "custom_dcf")
    if code == "entitlement":
        state.before_request("fmp", "income")
        assert state.blocked_providers == {}
    else:
        with pytest.raises(ResearchRequestBlocked, match=code):
            state.before_request("fmp", "income")
    state.before_request("fred", "DGS10")
    assert len(reached) == 1


@pytest.mark.parametrize("status,code", [(401, "authentication"), (403, "entitlement"), (429, "throttling")])
def test_research_http_failure_preserves_callback_and_source(monkeypatch, status, code):
    from live_financial_support import ResearchRequestBlocked, ResearchRunState, SourceCapture
    from openbb_core.provider.utils import helpers

    payload = [{"date": "2025-01-01", "amount": None}]
    response = type("Response", (), {"status": status})()
    callback_calls = []
    async def callback(actual, session):
        assert actual is response and session == "original-session"
        callback_calls.append(True)
        return payload
    async def transport(*args, **kwargs):
        return await kwargs["response_callback"](response, "original-session")
    monkeypatch.setattr(helpers, "amake_request", transport)
    state = ResearchRunState()
    capture = SourceCapture(monkeypatch, "fmp", state, endpoint="income")
    result = asyncio.run(helpers.amake_request(response_callback=callback))
    assert result is payload and callback_calls == [True]
    payload[0]["amount"] = 2
    assert capture.source_rows()[0]["amount"] is None
    with pytest.raises(ResearchRequestBlocked, match=code):
        state.before_request("fmp", "income")


@pytest.mark.parametrize("status,code", [(401, "authentication"), (403, "entitlement"), (429, "throttling")])
def test_research_legacy_callback_failure_retains_observed_http_category(monkeypatch, tmp_path, status, code):
    from live_financial_support import ResearchRunState, SourceCapture, evidence
    from openbb_core.provider.utils import helpers
    from openbb_fmp.utils.helpers import response_callback

    response = type("Response", (), {"status": status})()
    async def transport(*args, **kwargs):
        return await kwargs["response_callback"](response, None)
    monkeypatch.setattr(helpers, "amake_request", transport)
    monkeypatch.setenv("QOPENBB_LIVE_EVIDENCE_DIR", str(tmp_path))
    state = ResearchRunState()
    capture = SourceCapture(monkeypatch, "fmp", state, endpoint="income")
    with pytest.raises(pytest.fail.Exception, match=code):
        with evidence("legacy-" + code, capture):
            asyncio.run(helpers.amake_request(response_callback=response_callback))
    receipt = json.loads((tmp_path / ("legacy-" + code + ".json")).read_text())
    assert receipt["failure"] == receipt["source_receipts"][0]["code"] == code
    assert capture.receipts[0]["status"] == status and state.attempts == 1
    if code == "entitlement":
        assert state.blocked_endpoints == {("fmp", "income"): code}
    else:
        assert state.blocked_providers == {"fmp": code}


def test_research_timeout_is_enforced_and_baseline_timeout_is_preserved(monkeypatch):
    import live_financial_support as support
    from openbb_core.provider.utils import helpers

    timeouts = []
    cancelled = []
    real_wait_for = asyncio.wait_for
    async def shortened_wait(awaitable, timeout):
        timeouts.append(timeout)
        return await real_wait_for(awaitable, timeout=0.01)
    async def hung(*args, **kwargs):
        assert kwargs["timeout"] == 15
        try:
            await asyncio.Event().wait()
        finally:
            cancelled.append(True)
    monkeypatch.setattr(helpers, "amake_request", hung)
    monkeypatch.setattr(support.asyncio, "wait_for", shortened_wait)
    state = support.ResearchRunState()
    with monkeypatch.context() as patch:
        capture = support.SourceCapture(patch, "fmp", state, endpoint="income")
        with pytest.raises(TimeoutError):
            asyncio.run(helpers.amake_request(response_callback=None, timeout=90))
    assert timeouts == [15] and cancelled == [True] and state.attempts == 1
    assert capture.receipts[0]["code"] == "timeout"
    async def baseline(*args, **kwargs):
        return kwargs["timeout"]
    monkeypatch.setattr(helpers, "amake_request", baseline)
    support.SourceCapture(monkeypatch, "fmp")
    assert asyncio.run(helpers.amake_request(response_callback=None, timeout=90)) == 90
    assert timeouts == [15]


def test_source_comparisons_keep_duplicate_ordinals_nulls_aliases_and_normalization():
    from datetime import date
    from live_financial_support import pairs

    source = [{"symbol": "MSFT", "date": date(2025, 6, 30), "fiscalYear": "2025",
               "calendarYear": "1999", "filingDate": "2025-07-30", "fillingDate": "1999-01-01", "value": None},
              {"symbol": "ORCL", "date": "2025-06-30", "value": 999},
              {"symbol": "MSFT", "date": "2025-06-30", "value": -7}]
    rows = [{"symbol": "MSFT", "period_ending": "2025-06-30", "fiscal_year": 2025,
             "filing_date": "2025-07-30", "amount": None},
            {"symbol": "MSFT", "period_ending": "2025-06-30", "fiscal_year": None,
             "filing_date": None, "amount": -7}]
    compared = pairs(rows, source, {"amount": "value", "fiscal_year": "calendarYear",
                                    "filing_date": "fillingDate", "period_ending": "date",
                                    "missing": "absent"}, "period_ending")
    assert [item["source_ordinal"] for item in compared if item["field"] == "amount"] == [0, 2]
    year = next(item for item in compared if item["field"] == "fiscal_year")
    assert year["source_field"] == "fiscalYear" and year["value"] == "2025"
    assert year["normalization"] == "integer_fiscal_year"
    assert compared[0]["source_state"] == "null"
    assert next(item for item in compared if item["field"] == "missing")["source_state"] == "absent"
    assert source[0]["calendarYear"] == "1999"
    with pytest.raises(pytest.fail.Exception):
        pairs([{"amount": 0}], [{"value": None}], {"amount": "value"})
    with pytest.raises(pytest.fail.Exception):
        pairs([{"amount": 0}], [{}], {"amount": "value"})
    with pytest.raises(pytest.fail.Exception):
        pairs([{"symbol": "MSFT", "date": "2025-06-30", "amount": 999}], source,
              {"amount": "value"}, "date")


def test_fiscal_year_preserves_exact_route_string_before_normalizing_integer():
    from live_financial_support import pairs

    source = [{"fiscalYear": "2025"}]
    for actual, rule in [("2025", None), (2025, "integer_fiscal_year")]:
        compared = pairs([{"fiscal_year": actual}], source, {"fiscal_year": "fiscalYear"})
        assert compared[0]["value"] == "2025" and compared[0]["normalization"] == rule
    for invalid in (2025.0, 2025.1, True):
        with pytest.raises(pytest.fail.Exception):
            pairs([{"fiscal_year": invalid}], source, {"fiscal_year": "fiscalYear"})


def test_enterprise_reference_is_latest_valid_same_listing_and_keeps_receipt():
    from live_financial_support import ResearchRunState

    state = ResearchRunState()
    for value, case in [("2025-01-31", "annual"), ("2025-04-30", "quarter"),
                        ("invalid", "bad"), (None, "missing"), ("2024-12-31", "older")]:
        state.record_enterprise_date("MSFT", value, listing_id="fmp:MSFT:NASDAQ",
                                     case_id=case, receipt_ref=case + ".json")
    assert state.enterprise_dates == {"MSFT": "2025-04-30"}
    assert state.enterprise_reference("MSFT", "fmp:MSFT:NASDAQ") == {
        "date": "2025-04-30", "listing_id": "fmp:MSFT:NASDAQ",
        "case_id": "quarter", "receipt_ref": "quarter.json"}
    assert state.enterprise_reference("MSFT", "fmp:MSFT:OTHER") is None
    assert state.enterprise_reference("ORCL", "fmp:ORCL:NYSE") is None
    with pytest.raises(pytest.fail.Exception):
        state.record_enterprise_date("MSFT", "2025-06-30", listing_id="fmp:MSFT:OTHER",
                                     case_id="other", receipt_ref="other.json")
    state.record_outcome("prices-ORCL", "unavailable", reason="missing_enterprise_date",
                         missing_proof="dated same-listing EV observation", prerequisite="enterprise-ORCL")
    assert state.outcomes["prices-ORCL"]["status"] == "unavailable"
    with pytest.raises(pytest.fail.Exception):
        state.record_outcome("prices-ORCL", "verified")
    assert state.attempts == 0


def test_research_receipts_keep_native_direct_boundary_and_redact_unsafe_text(monkeypatch, tmp_path):
    from live_financial_support import ResearchRunState, SourceCapture, evidence, write_evidence

    monkeypatch.setenv("QOPENBB_LIVE_EVIDENCE_DIR", str(tmp_path))
    monkeypatch.setenv("FMP_API_KEY", SECRET)
    state = ResearchRunState()
    with monkeypatch.context() as patch:
        capture = SourceCapture(patch, "fmp", state, endpoint="income")
        write_evidence("native", capture, 200, {"currency": "USD"}, [{"value": 0}])
        with pytest.raises(FileExistsError):
            write_evidence("native", capture, 500, failure="upstream")
    with monkeypatch.context() as patch:
        capture = SourceCapture(patch, "fmp", state, endpoint="dcf", kind="direct_provider")
        with pytest.raises(pytest.fail.Exception):
            with evidence("direct", capture, query={"symbol": "MSFT", "beta": 1.0, "apikey": SECRET}) as record:
                record["observation"] = {"year": 2030, "date": None, "currency": None,
                                          "headers": {"apikey": SECRET}, "url": "https://private.example/"}
                raise RuntimeError("unsafe provider " + SECRET)
    native = json.loads((tmp_path / "native.json").read_text())
    direct_text = (tmp_path / "direct.json").read_text()
    direct = json.loads(direct_text)
    assert native["kind"] == "native_api" and native["financial_metadata"] == {"currency": "USD"}
    assert direct["kind"] == "direct_provider" and direct["observation"]["year"] == 2030
    assert direct["query"] == {"symbol": "MSFT", "beta": 1.0}
    assert direct["failure"] == "acceptance validation error"
    assert "financial_metadata" not in direct
    assert SECRET not in direct_text and "private.example" not in direct_text and "headers" not in direct_text


@pytest.mark.parametrize("dataset,field_names", [
    ("balance", ("accounts_payable",)),
    ("cash", ("change_in_account_receivables", "change_in_account_payable")),
])
def test_research_receipts_preserve_native_accounting_field_metadata(monkeypatch, tmp_path, dataset, field_names):
    from live_financial_support import ResearchRunState, SourceCapture, write_evidence
    from openbb_core.provider.standard_models.financial_annotations import render_field_templates
    from openbb_fmp.models.balance_sheet import FMPBalanceSheetData
    from openbb_fmp.models.cash_flow import FMPCashFlowStatementData

    model = {"balance": FMPBalanceSheetData, "cash": FMPCashFlowStatementData}[dataset]
    fields = {name: item.model_dump(mode="json") for name, item in render_field_templates(model).items()}
    common = {"dataset": "equity/fundamental/" + dataset, "fields": fields}
    comparisons = [{"field": name, "definition": fields[name]["definition"],
                    "value_origin": fields[name]["value_origin"], "value": None} for name in field_names]
    monkeypatch.setenv("QOPENBB_LIVE_EVIDENCE_DIR", str(tmp_path))
    capture = SourceCapture(monkeypatch, "fmp", ResearchRunState(), endpoint=dataset)
    write_evidence(dataset, capture, 200, common, comparisons)
    receipt = json.loads((tmp_path / (dataset + ".json")).read_text())
    assert receipt["financial_metadata"] == common
    assert receipt["comparisons"] == comparisons
    for name in field_names:
        assert receipt["financial_metadata"]["fields"][name]["definition"] == model.model_fields[name].description
        assert receipt["financial_metadata"]["fields"][name]["value_origin"] == "provider_observation"


def test_evidence_sanitizer_excludes_private_accounts_transport_and_configured_secrets(monkeypatch):
    from live_financial_support import safe_evidence

    monkeypatch.setenv("FMP_API_KEY", SECRET)
    monkeypatch.setenv("FRED_API_KEY", "PRIVATE_FRED_CANARY")
    private = {name: "private-identity-canary" for name in (
        "account", "accounts", "account_id", "accountIds", "account_identifier", "accountNumber",
        "account_name", "account_email", "account_holder", "account_owner", "account_details",
        "account_identity", "provider_account", "brokerage_account", "private_account")}
    private.update(headers={"Authorization": "Bearer transport-canary"},
                   api_key="credential-canary", access_token="token-canary", password="password-canary",
                   cookies="cookie-canary", request_url="https://private.example/request")
    observation = {"accounts_payable": 0, "change_in_account_receivables": None,
                   "change_in_account_payable": -7, "accounting_basis": "provider reported"}
    payload = {"observation": observation, "nested": [{**private, "observation": observation}],
               "notes": ["prefix " + SECRET, "PRIVATE_FRED_CANARY suffix", "https://private.example/value"]}
    assert safe_evidence(payload) == {
        "observation": observation, "nested": [{"observation": observation}],
        "notes": ["[redacted]", "[redacted]", "[redacted]"]}


def test_research_fixture_aliases_share_session_object_budget_and_stops(tmp_path):
    import subprocess
    import sys
    from pathlib import Path

    directory = Path(__file__).parent.resolve()
    (tmp_path / "pytest.ini").write_text("[pytest]\n", encoding="utf-8")
    (tmp_path / "conftest.py").write_text(
        "import socket\ndef pytest_sessionstart(session):\n"
        "    def forbidden(*args, **kwargs):\n        raise AssertionError('offline only')\n"
        "    socket.socket.connect = forbidden\n", encoding="utf-8")
    (tmp_path / "test_native.py").write_text(
        "from live_financial_support import research_run_state as native_state\n"
        "def test_native(native_state, request):\n"
        "    request.session.research_identity = native_state\n"
        "    native_state.before_request('fmp', 'income')\n"
        "    native_state.block_provider('fmp', 'throttling')\n"
        "    native_state.record_outcome('native-marker', 'verified')\n", encoding="utf-8")
    (tmp_path / "test_dcf.py").write_text(
        "import pytest\nfrom live_financial_support import research_run_state as direct_state, ResearchRequestBlocked\n"
        "def test_direct(direct_state, request):\n"
        "    assert direct_state is request.session.research_identity\n"
        "    assert direct_state.attempts == 1\n"
        "    assert direct_state.outcomes['native-marker']['status'] == 'verified'\n"
        "    with pytest.raises(ResearchRequestBlocked, match='throttling'):\n"
        "        direct_state.before_request('fmp', 'dcf')\n"
        "    for _ in range(50): direct_state.before_request('fred', 'DGS10')\n"
        "    with pytest.raises(ResearchRequestBlocked, match='request_ceiling'):\n"
        "        direct_state.before_request('fred', 'DGS10')\n", encoding="utf-8")
    environment = {**os.environ, "PYTHONPATH": str(directory), "PYTEST_DISABLE_PLUGIN_AUTOLOAD": "1"}
    for key in ("FMP_API_KEY", "FRED_API_KEY", "QOPENBB_LIVE_ACCEPTANCE"):
        environment.pop(key, None)
    result = subprocess.run([sys.executable, "-m", "pytest", "-c", str(tmp_path / "pytest.ini"),
                             str(tmp_path / "test_native.py"), str(tmp_path / "test_dcf.py"), "-q"],
                            env=environment, capture_output=True, text=True, timeout=45, check=False)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "2 passed" in result.stdout
