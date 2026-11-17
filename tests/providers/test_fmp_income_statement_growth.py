"""Income growth preserves source ratios, fiscal facts and bounded provenance."""

import asyncio
import json
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

import pytest
from openbb_core.provider.standard_models.financial_annotations import (
    bind_data_annotation,
    bind_query_annotation,
)
from openbb_core.provider.standard_models.financial_metadata import (
    FINANCIAL_METADATA_KEY,
)
from openbb_core.provider.standard_models.income_statement_growth import (
    IncomeStatementGrowthData,
)
from openbb_core.provider.utils.financial_errors import FinancialError

STANDARD_SCHEMA = IncomeStatementGrowthData.model_json_schema()

from openbb_fmp.models.income_statement_growth import (
    FMPIncomeStatementGrowthData as Row,
)
from openbb_fmp.models.income_statement_growth import (
    FMPIncomeStatementGrowthFetcher as Fetcher,
)
from openbb_fmp.models.income_statement_growth import (
    FMPIncomeStatementGrowthQueryParams as Query,
)

FROZEN = json.loads(
    (
        Path(__file__).parent
        / "fixtures/fmp_batch_a/contracts/income_statement_growth.json"
    ).read_text()
)


class Response:
    def __init__(self, payload, status=200):
        self.payload, self.status, self.headers = payload, status, {"Retry-After": "23"}

    async def json(self):
        if isinstance(self.payload, Exception):
            raise self.payload
        return self.payload


def run(monkeypatch, payload, params=None, status=200):
    calls = []

    async def request(url, **kwargs):
        calls.append((url, kwargs))
        if isinstance(payload, TimeoutError):
            raise payload
        return await kwargs["response_callback"](Response(payload, status), None)

    monkeypatch.setattr("openbb_core.provider.utils.helpers.amake_request", request)
    result = asyncio.run(
        Fetcher.fetch_data(
            params or {"symbol": " msft "}, {"fmp_api_key": "canary&secret"}
        )
    )
    assert len(calls) == 1
    return result, calls


def test_frozen_schema_and_annotations():
    for mode in ["validation", "serialization"]:
        assert Query.model_json_schema(mode=mode) == FROZEN["query"][mode]
        assert Row.model_json_schema(mode=mode) == FROZEN["data"][mode]
    assert (
        bind_query_annotation(Query).model_dump(mode="json")
        == FROZEN["query_annotation"]
    )
    assert (
        bind_data_annotation(Row).model_dump(mode="json") == FROZEN["data_annotation"]
    )
    assert Query.__dict__["__qopenbb_strict_admission__"] is True


@pytest.mark.parametrize(
    "params",
    [{"symbol": v} for v in [None, True, "", "A,B", "A&x=y", "A" * 51, "A\n"]]
    + [
        {"symbol": "A", k: v}
        for k, values in {
            "limit": [None, True, 0, 101, "20", 20.0],
            "page": [0],
            "period": [None, True, "ttm", "FY", "TTM", "YTD"],
            "extra": [0],
        }.items()
        for v in values
    ],
)
def test_invalid_raw_queries_zero_io(monkeypatch, params):
    async def forbidden(*args, **kwargs):
        pytest.fail("invalid query reached transport")

    monkeypatch.setattr("openbb_core.provider.utils.helpers.amake_request", forbidden)
    with pytest.raises(FinancialError) as error:
        asyncio.run(Fetcher.fetch_data(params, {"fmp_api_key": "canary"}))
    assert error.value.code == "invalid_parameters"


@pytest.mark.parametrize(
    "period,expected",
    [("annual", "annual"), ("quarter", "quarter"), ("quarterly", "quarter")],
)
def test_request_clip_and_provenance(monkeypatch, period, expected):
    payload = [
        {
            "symbol": "MSFT",
            "date": "2025-06-30",
            "growthRevenue": v,
            "calendarYear": 2025,
            "period": "Q2",
        }
        for v in [-0.25, 0, None]
    ]
    result, calls = run(
        monkeypatch, payload, {"symbol": " brk/b ", "period": period, "limit": 2}
    )
    url, _kwargs = calls[0]
    assert urlsplit(url).path == "/stable/income-statement-growth"
    assert "BRK%2FB" in url and "canary%26secret" in url
    assert parse_qs(urlsplit(url).query) == {
        "symbol": ["BRK/B"],
        "period": [expected],
        "limit": ["2"],
        "apikey": ["canary&secret"],
    }
    assert [x.growth_revenue for x in result.result] == [-0.25, 0]
    assert [x.fiscal_year for x in result.result] == [2025, 2025]
    assert all(x.fiscal_period == "Q2" for x in result.result)
    meta = result.metadata[FINANCIAL_METADATA_KEY]
    assert meta["effective_query"] == {
        "symbol": "BRK/B",
        "period": expected,
        "limit": 2,
    }
    assert (
        meta["bounds"]["truncated"] is True
        and meta["bounds"]["completeness"] == "partial"
    )
    assert meta["retrieved_at"] and "canary" not in json.dumps(meta)
    assert meta["point_in_time_safe"] is False
    assert meta["source"]["endpoint"] == "income-statement-growth"


def test_default_empty_actual_fetcher(monkeypatch):
    result, _calls = run(monkeypatch, [])
    assert result.result == []
    meta = result.metadata[FINANCIAL_METADATA_KEY]
    assert meta["effective_query"] == {
        "symbol": "MSFT",
        "period": "annual",
        "limit": 20,
    }
    assert meta["bounds"]["completeness"] == "unknown"
    assert all(f["availability"] == "missing" for f in meta["fields"].values())


@pytest.mark.parametrize("number", [-0.25, 0, 0.25, None])
def test_all_growth_fields_and_aliases(monkeypatch, number):
    payload = {
        "symbol": "MSFT",
        "date": "2025-06-30",
        "calendarYear": 2025,
        "period": "Q2",
        "reportedCurrency": "USD",
    }
    for name, field in Row.model_fields.items():
        if name.startswith("growth_"):
            payload[FROZEN["effective_aliases"].get(name, field.validation_alias)] = (
                number
            )
    result, _ = run(monkeypatch, [payload])
    row = result.result[0]
    assert not row.model_extra
    meta = result.metadata[FINANCIAL_METADATA_KEY]
    assert set(meta["fields"]) == set(Row.model_fields)
    for name in Row.model_fields:
        template = meta["fields"][name]
        assert template["observation_date_field"] == "period_ending"
        if name.startswith("growth_"):
            assert getattr(row, name) == number
            assert template["unit"] == "ratio" and template["scale"] == 1
            assert template["value_origin"] == "provider_calculation"
            assert template["availability"] == (
                "missing" if number is None else "available"
            )
            assert "year-to-date" in template["period_basis"]


def test_missing_optional_is_not_zero(monkeypatch):
    result, _ = run(
        monkeypatch, [{"symbol": "MSFT", "date": "2025-06-30", "growthRevenue": 0}]
    )
    assert result.result[0].growth_revenue == 0
    assert result.result[0].growth_ebit is None
    assert (
        result.metadata[FINANCIAL_METADATA_KEY]["bounds"]["completeness"] == "unknown"
    )


@pytest.mark.parametrize("value", [None, "malformed", True, 123, "2025-06-30T00:00:00"])
def test_required_period_validation(monkeypatch, value):
    assert_invalid(monkeypatch, [{"symbol": "MSFT", "date": value}])


def test_missing_period(monkeypatch):
    assert_invalid(monkeypatch, [{"symbol": "MSFT"}])


def assert_invalid(monkeypatch, payload):
    with pytest.raises(FinancialError) as error:
        run(monkeypatch, payload)
    assert error.value.code == "invalid_response"
    assert "canary" not in str(error.value)
    assert error.value.__context__ is None and error.value.__cause__ is None


@pytest.mark.parametrize(
    "field",
    [name for name in Row.model_fields if name.startswith("growth_")]
    + ["calendarYear"],
)
@pytest.mark.parametrize("value", [float("nan"), float("inf"), {}, "canary-malformed"])
def test_invalid_numeric_safe(monkeypatch, field, value):
    assert_invalid(
        monkeypatch, [{"symbol": "MSFT", "date": "2025-06-30", field: value}]
    )


@pytest.mark.parametrize("payload", [[None], [42], [{}]])
def test_malformed_shapes(monkeypatch, payload):
    assert_invalid(monkeypatch, payload)


@pytest.mark.parametrize(
    "payload,status,code",
    [
        ({"Error Message": "canary"}, 401, "authentication"),
        ({"Error Message": "canary"}, 403, "entitlement"),
        ({"Error Message": "canary"}, 429, "throttling"),
        (TimeoutError("canary"), 200, "timeout"),
        (ValueError("canary"), 200, "invalid_response"),
    ],
)
def test_transport_errors(monkeypatch, payload, status, code):
    with pytest.raises(FinancialError) as error:
        run(monkeypatch, payload, status=status)
    assert error.value.code == code
    assert "canary" not in str(error.value)
    assert error.value.__cause__ is None and error.value.__context__ is None
    if code == "throttling":
        assert error.value.retry_after_seconds == 23


def test_formatter_ratios_preserve_parent():
    from openbb_core.provider.standard_models.income_statement_growth import (
        IncomeStatementGrowthData,
    )

    assert IncomeStatementGrowthData.model_json_schema() == STANDARD_SCHEMA
    for mode in ["validation", "serialization"]:
        for name, field in Row.model_json_schema(mode=mode)["properties"].items():
            if name.startswith("growth"):
                assert field["x-unit_measurement"] == "ratio"
                assert "x-frontend_multiply" not in field


def test_owned_package_origins():
    import importlib

    root = Path(__file__).resolve().parents[2]
    api = root.parent / "data-api/openbb_platform"
    expected = {
        "qopenbb_data": root / "services/data-api/qopenbb_data",
        "openbb_core": api / "core/openbb_core",
        "openbb_fmp": api / "providers/fmp/openbb_fmp",
        "openbb_fred": api / "providers/fred/openbb_fred",
        "openbb_equity": api / "extensions/equity/openbb_equity",
        "openbb_economy": api / "extensions/economy/openbb_economy",
    }
    for package, directory in expected.items():
        module = importlib.import_module(package)
        assert Path(module.__file__).resolve().parent == directory.resolve()


def test_empty_object_is_typed_missing_data(monkeypatch):
    with pytest.raises(FinancialError) as error:
        run(monkeypatch, {})
    assert error.value.code == "missing_data"


@pytest.mark.parametrize("limit", [1, 100])
def test_limit_boundaries(limit):
    assert Query(symbol="MSFT", limit=limit).limit == limit


@pytest.mark.parametrize("mode", ["validation", "serialization"])
def test_actual_native_formatter(mode):
    import importlib.util

    source = (
        Path.cwd().parent
        / "data-api/openbb_platform/extensions/platform_api/openbb_platform_api/utils/openapi.py"
    )
    spec = importlib.util.spec_from_file_location("a2_native_widget_openapi", source)
    native = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(native)
    schema = Row.model_json_schema(mode=mode)
    document = {
        "paths": {
            "/growth": {
                "get": {
                    "operationId": "growth",
                    "responses": {
                        "200": {"content": {"application/json": {"schema": schema}}}
                    },
                }
            }
        }
    }
    columns = native.data_schema_to_columns_defs(document, "growth", "fmp")
    by_name = {column["field"]: column for column in columns}
    for canonical, info in Row.model_fields.items():
        if not canonical.startswith("growth_"):
            continue
        alias = (
            info.validation_alias if mode == "validation" else info.serialization_alias
        )
        prop = schema["properties"][alias]
        assert prop.get("x-unit_measurement") == "ratio", canonical
        assert "x-frontend_multiply" not in prop, canonical
        projected = by_name[canonical]
        assert projected["cellDataType"] == "number"
        assert projected["formatterFn"] not in {"percent", "normalizedPercent"}, (
            canonical,
            projected,
        )


@pytest.mark.parametrize("name", list(Row.model_fields))
@pytest.mark.parametrize("spelling", ["canonical", "generated", "source"])
def test_every_accepted_field_spelling(name, spelling):
    field = Row.model_fields[name]
    key = {
        "canonical": name,
        "generated": field.validation_alias,
        "source": FROZEN["effective_aliases"].get(name, field.validation_alias),
    }[spelling]
    values = {
        "period_ending": "2025-06-30",
        "symbol": "MSFT",
        "fiscal_year": 2025,
        "fiscal_period": "Q2",
        "reported_currency": "USD",
    }
    value = values.get(name, -0.25)
    row = Row.model_validate({"symbol": "MSFT", "date": "2025-06-30", key: value})
    assert str(getattr(row, name)) == str(value)
    assert not row.model_extra
