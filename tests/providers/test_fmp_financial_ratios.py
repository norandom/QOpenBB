"""Cash-flow fixtures retain reported observations without a house cash model."""
import asyncio
from copy import deepcopy
from datetime import UTC, datetime
from urllib.parse import parse_qs, urlsplit

import pytest

from openbb_core.provider.standard_models.financial_metadata import FINANCIAL_METADATA_KEY
from openbb_core.provider.utils.financial_errors import FinancialError, FinancialErrorCode
from openbb_fmp.models.financial_ratios import FMPFinancialRatiosFetcher as Fetcher
from openbb_fmp.models.financial_ratios_data import FMPFinancialRatiosData
from openbb_fmp.utils.helpers import FMPAcquisition

STAMP = datetime(2024, 2, 3, 4, 5, tzinfo=UTC)


def fixture(period="FY", date="2023-12-31"):
    return {"date": date, "period": period, "fiscalYear": "2023", "symbol": "A",
            "reportedCurrency": "EUR", "netProfitMargin": -0.12, "currentRatio": 0,
            "dividendYield": 0.02, "dividendYieldPercentage": 2, "revenuePerShare": None}


def test_fidelity_metadata():
    query = Fetcher.transform_query({"symbol": " a ", "period": "quarterly"})
    payload = [fixture("Q4")]
    original = deepcopy(payload)
    result = Fetcher.transform_data(query, FMPAcquisition(payload, STAMP))
    row = result.result[0]
    assert payload == original
    assert row.net_profit_margin == -0.12 and row.current_ratio == 0
    assert row.revenue_per_share is None and row.fiscal_year == 2023
    assert row.dividend_yield == 0.02 and row.dividend_yield_percentage == 2
    metadata = result.metadata[FINANCIAL_METADATA_KEY]
    fields = metadata["fields"]
    assert fields["net_profit_margin"]["unit"] == "fraction"
    assert fields["current_ratio"]["unit"] == "multiple"
    assert fields["solvency_ratio"]["unit"] == "fraction"
    identity = {"symbol", "period_ending", "fiscal_year", "fiscal_period", "currency"}
    assert all(field["unit"] is not None for name, field in fields.items() if name not in identity)
    assert fields["dividend_yield_percentage"]["unit"] == "percent"
    assert fields["revenue_per_share"]["unit"] == "currency/share"
    assert fields["revenue_per_share"]["currency_field"] == "currency"
    assert fields["net_profit_margin"]["value_origin"] == "provider_calculation"
    assert datetime.fromisoformat(metadata["retrieved_at"]) == STAMP
    assert metadata["point_in_time_safe"] is False
    assert fields["price_to_earnings"]["observation_date_field"] is None
    assert fields["price_to_earnings"]["valuation_date_field"] is None
    assert fields["fiscal_year"]["period_basis"] is None
    assert any("annualization" in item for item in metadata["limitations"])


@pytest.mark.parametrize("params", [
    {"symbol": ""}, {"symbol": "   "}, {"symbol": "A,B"},
    {"symbol": "A B"}, {"symbol": "A&apikey=bad"}, {"symbol": None},
    {"symbol": "A", "period": "ttm"}, {"symbol": "A", "period": "monthly"},
    {"symbol": "A", "ttm": "only"}, {"symbol": "A", "ttm": "include"},
    {"symbol": "A", "limit": 0}, {"symbol": "A", "limit": 1001},
    {"symbol": "A", "limit": None}, {"symbol": "A", "limit": -1},
    {"symbol": "A", "limit": True}, {"symbol": "A", "limit": "5"},
    {"symbol": "A", "limit": 5.0}, {"symbol": "A\n"},
    {"symbol": "A\r"}, {"symbol": "A\x00"},
])
def test_invalid_query_fails_before_io(params, monkeypatch):
    async def forbidden(*args, **kwargs):
        pytest.fail("Invalid query reached transport")
    monkeypatch.setattr("openbb_fmp.utils.helpers.get_data_many", forbidden)
    with pytest.raises(FinancialError) as caught:
        query = Fetcher.transform_query(params)
        asyncio.run(Fetcher.aextract_data(query, {}))
    assert caught.value.code == FinancialErrorCode.INVALID_PARAMETERS
    assert caught.value.__context__ is None


def test_extraction_uses_provenance_encoded_query(monkeypatch):
    async def transport(url, **kwargs):
        parsed = urlsplit(url)
        assert parsed.path == "/stable/ratios"
        assert parse_qs(parsed.query) == {"symbol": ["^GSPC"], "period": ["quarter"],
                                          "limit": ["1000"], "apikey": ["synthetic"]}
        assert kwargs["with_provenance"] is True
        assert kwargs["typed_errors"] is True
        return FMPAcquisition([fixture("Q4")], STAMP)
    monkeypatch.setattr("openbb_fmp.utils.helpers.get_data_many", transport)
    query = Fetcher.transform_query({"symbol": "^gspc", "period": "quarter", "limit": 1000})
    assert asyncio.run(Fetcher.aextract_data(query, {"fmp_api_key": "synthetic"})).retrieved_at == STAMP




@pytest.mark.parametrize("selection", [{}, {"ttm": "exclude"}], ids=["default", "explicit"])
@pytest.mark.parametrize("period_params,expected_period", [
    ({}, "annual"), ({"period": "annual"}, "annual"),
    ({"period": "quarter"}, "quarter"), ({"period": "quarterly"}, "quarter"),
])
def test_periodic_query_provenance_preserves_requests_and_values(
    monkeypatch, selection, period_params, expected_period,
):
    calls = []
    payload = [fixture()]
    original = deepcopy(payload)

    async def transport(url, **kwargs):
        calls.append((url, kwargs))
        return FMPAcquisition(payload, STAMP)

    monkeypatch.setattr("openbb_fmp.utils.helpers.get_data_many", transport)
    params = {"symbol": " a ", **period_params, **selection}
    query = Fetcher.transform_query(params)
    acquired = asyncio.run(Fetcher.aextract_data(query, {"fmp_api_key": "synthetic"}))
    result = Fetcher.transform_data(query, acquired)
    assert len(calls) == 1
    url, kwargs = calls[0]
    assert urlsplit(url).path == "/stable/ratios"
    assert parse_qs(urlsplit(url).query) == {
        "symbol": ["A"], "period": [expected_period], "limit": ["5"], "apikey": ["synthetic"],
    }
    assert kwargs == {"with_provenance": True, "typed_errors": True}
    assert params == {"symbol": " a ", **period_params, **selection}
    assert payload == original
    assert [row.model_dump() for row in result.result] == [FMPFinancialRatiosData.model_validate(original[0]).model_dump()]
    row = result.result[0]
    assert row.net_profit_margin == -.12 and row.current_ratio == 0 and row.revenue_per_share is None
    assert row.dividend_yield == .02 and row.dividend_yield_percentage == 2
    meta = result.metadata[FINANCIAL_METADATA_KEY]
    assert meta["schema_version"] == 1
    assert meta["effective_query"] == {
        "symbol": "A", "period": expected_period, "limit": 5, "ttm": "exclude",
    }
    # Periodic selection does not establish fiscal comparability or derive a value.
    assert meta["transformations"] == [] and meta["point_in_time_safe"] is False
    assert meta["fields"]["net_profit_margin"]["period_basis"] == "annual"
    assert meta["fields"]["price_to_earnings"]["financial_basis"]["market_date"] is None


def test_order_duplicates_missing_identity_and_bounds():
    q = Fetcher.transform_query({"symbol": "A", "limit": 2})
    old, first, second = fixture(date="2022-12-31"), fixture(), fixture()
    first["netProfitMargin"], second["netProfitMargin"] = -1, -2
    result = Fetcher.transform_data(q, FMPAcquisition([old, first, second], STAMP))
    assert [r.net_profit_margin for r in result.result] == [-1, -2]
    bounds = result.metadata[FINANCIAL_METADATA_KEY]["bounds"]
    assert bounds["truncated"] is True and bounds["completeness"] == "partial"
    sparse = Fetcher.transform_data(q, FMPAcquisition([{"date": "2023-12-31"}], STAMP))
    row = sparse.result[0]
    assert row.currency is None and row.fiscal_year is None and row.fiscal_period is None
    assert sparse.metadata[FINANCIAL_METADATA_KEY]["fields"]["net_profit_margin"]["period_basis"] is None


@pytest.mark.parametrize("change", [{"date": "invalid"}, {"date": None}, {"netProfitMargin": "bad"}, {"currentRatio": float("inf")}])
def test_invalid_response_is_safe(change):
    with pytest.raises(FinancialError) as caught:
        Fetcher.transform_data(Fetcher.transform_query({"symbol": "A"}),
                               FMPAcquisition([{**fixture(), **change}], STAMP))
    assert caught.value.code == FinancialErrorCode.INVALID_RESPONSE
    assert caught.value.__context__ is None


def test_legacy_year_and_actual_period_basis():
    data = fixture("Q4")
    data["calendarYear"] = data.pop("fiscalYear")
    result = Fetcher.transform_data(Fetcher.transform_query({"symbol": "A"}), FMPAcquisition([data], STAMP))
    assert result.result[0].fiscal_year == 2023
    assert result.metadata[FINANCIAL_METADATA_KEY]["fields"]["net_profit_margin"]["period_basis"] == "discrete_quarter"


@pytest.mark.parametrize("period,basis", [("FY", "annual"), ("Q4", "discrete_quarter"), (None, None)])
def test_declarations_match_runtime_and_keep_request_copies(period, basis):
    from openbb_core.provider.standard_models.financial_annotations import (
        bind_query_annotation, render_field_templates,
    )
    from openbb_fmp.models.financial_ratios import FMPFinancialRatiosQueryParams
    from openbb_fmp.models.financial_ratios_data import FMPFinancialRatiosData

    query = Fetcher.transform_query({"symbol": "A", "limit": 1})
    declaration = bind_query_annotation(FMPFinancialRatiosQueryParams)
    assert declaration.provider_policy == "explicit"
    assert declaration.response_policy.mode == "clip"
    assert declaration.response_policy.limit_parameter == "limit"
    templates = render_field_templates(FMPFinancialRatiosData)
    result = Fetcher.transform_data(query, FMPAcquisition([fixture(period), fixture(period)], STAMP))
    metadata = result.metadata[FINANCIAL_METADATA_KEY]
    assert metadata["bounds"]["truncated"] is True
    assert len(result.result) == 1
    for name, template in templates.items():
        expected = template.model_dump(mode="json")
        expected["availability"] = "available" if getattr(result.result[0], name) is not None else "missing"
        if template.value_origin == "provider_calculation":
            expected["period_basis"] = basis
        assert metadata["fields"][name] == expected
    templates["dividend_yield"].financial_basis["share_count"] = "changed"
    templates["dividend_yield"].unit = "changed"
    assert render_field_templates(FMPFinancialRatiosData)["dividend_yield"].unit == "fraction"
    assert render_field_templates(FMPFinancialRatiosData)["dividend_yield"].financial_basis["share_count"] is None
    empty = Fetcher.transform_data(query, FMPAcquisition([], STAMP))
    assert all(field["availability"] == "missing" for field in empty.metadata[FINANCIAL_METADATA_KEY]["fields"].values())


def test_clipping_and_bounds_read_the_declared_limit_parameter():
    from openbb_core.provider.standard_models.financial_annotations import ResponsePolicy
    from openbb_fmp.models.financial_ratios import FMPFinancialRatiosQueryParams
    from pydantic import create_model

    alternate = create_model("AlternateRatioLimit", __base__=FMPFinancialRatiosQueryParams, row_cap=(int, 2))
    alternate.financial_query_annotation = FMPFinancialRatiosQueryParams.financial_query_annotation.model_copy(
        update={"response_policy": ResponsePolicy(mode="clip", limit_parameter="row_cap")}, deep=True,
    )
    query = alternate(symbol="A", limit=1)
    result = Fetcher.transform_data(query, FMPAcquisition([fixture()] * 3, STAMP))
    assert len(result.result) == 2
    bounds = result.metadata[FINANCIAL_METADATA_KEY]["bounds"]
    assert bounds["requested_limit"] == bounds["effective_limit"] == 2
    assert bounds["truncated"] is True
