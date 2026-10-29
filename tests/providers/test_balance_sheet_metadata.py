import asyncio
from copy import deepcopy
from datetime import UTC, datetime
from urllib.parse import parse_qs, urlsplit

import pytest

from openbb_core.provider.utils.financial_errors import FinancialError
from openbb_fmp.utils.helpers import FMPAcquisition


@pytest.fixture
def row():
    return {
        "date": "2025-09-30", "symbol": "AAPL", "period": "FY",
        "fiscalYear": "2025", "filingDate": "2025-10-31",
        "acceptedDate": "2025-10-31 06:01:02", "reportedCurrency": "USD",
        "cashAndCashEquivalents": 0, "totalDebt": 100,
        "netDebt": -20, "retainedEarnings": -5, "minorityInterest": None,
        "totalAssets": 200,
    }


@pytest.mark.parametrize("period,fiscal", [("annual", "FY"), ("quarter", "Q3")])
@pytest.mark.parametrize("year,filing", [("fiscalYear", "filingDate"), ("calendarYear", "fillingDate")])
def test_statement_fidelity_and_provenance(row, period, fiscal, year, filing):
    from openbb_fmp.models.balance_sheet import FMPBalanceSheetFetcher as Fetcher
    row[year] = row.pop("fiscalYear")
    row[filing] = row.pop("filingDate")
    row["period"] = fiscal
    saved = deepcopy(row)
    query = Fetcher.transform_query({"symbol": " aapl ", "period": period})
    timestamp = datetime(2025, 11, 1, tzinfo=UTC)
    result = Fetcher.transform_data(query, FMPAcquisition([row], timestamp))
    record = result.result[0]
    assert row == saved
    assert record.period_ending.isoformat() == "2025-09-30"
    assert record.fiscal_year == 2025
    assert record.fiscal_period == fiscal
    assert record.filing_date.isoformat() == "2025-10-31"
    assert record.accepted_date.isoformat() == "2025-10-31T06:01:02"
    assert record.reported_currency == "USD"
    assert record.cash_and_cash_equivalents == 0
    assert record.net_debt == -20
    assert record.retained_earnings == -5
    assert record.minority_interest is None
    assert record.treasury_stock is None
    meta = result.metadata["__qopenbb_financial__"]
    assert meta["retrieved_at"] == "2025-11-01T00:00:00Z"
    assert meta["effective_query"] == {"symbol": "AAPL", "period": period, "limit": 5}
    assert meta["fields"]["total_debt"]["unit"] == "currency"
    assert meta["fields"]["total_debt"]["currency_field"] == "reported_currency"
    assert meta["fields"]["total_debt"]["period_basis"] == "instant"
    assert meta["fields"]["treasury_stock"]["availability"] == "missing"
    assert meta["fields"]["minority_interest"]["availability"] == "missing"
    assert meta["fields"]["cash_and_cash_equivalents"]["availability"] == "available"
    assert meta["point_in_time_safe"] is False
    assert meta["bounds"]["completeness"] == "unknown"


@pytest.mark.parametrize("params", [
    {"symbol": ""}, {"symbol": "   "}, {"symbol": "AAPL,MSFT"},
    {"symbol": "AAPL MSFT"}, {"symbol": "AAPL\n"},
    {"symbol": "AAPL", "period": "ttm"}, {"symbol": "AAPL", "period": "weekly"},
    {"symbol": "AAPL", "limit": 0}, {"symbol": "AAPL", "limit": -1},
    {"symbol": "AAPL", "limit": 1001}, {"symbol": None},
])
def test_invalid_query_fails_safely_before_io(params, monkeypatch):
    from openbb_fmp.models.balance_sheet import FMPBalanceSheetFetcher as Fetcher
    from openbb_fmp.utils import helpers
    def forbidden(*args, **kwargs):
        pytest.fail("Invalid queries must not perform I/O")
    monkeypatch.setattr(helpers, "get_data_many", forbidden)
    with pytest.raises(FinancialError) as error:
        Fetcher.transform_query(params)
    assert error.value.code == "invalid_parameters"
    assert error.value.__context__ is None


@pytest.mark.parametrize("limit", [1, 1000])
def test_acquisition_encodes_query_and_retains_original_time(row, monkeypatch, limit):
    from openbb_fmp.models.balance_sheet import FMPBalanceSheetFetcher as Fetcher
    from openbb_fmp.utils import helpers
    acquired = FMPAcquisition([row], datetime(2025, 11, 1, tzinfo=UTC))
    async def request(url, **kwargs):
        parsed = urlsplit(url)
        assert parsed.path == "/stable/balance-sheet-statement"
        assert parse_qs(parsed.query) == {
            "symbol": ["BRK.B"], "limit": [str(limit)],
            "period": ["quarter"], "apikey": ["fixture-only"],
        }
        assert kwargs["with_provenance"] is True
        assert kwargs["typed_errors"] is True
        return acquired
    monkeypatch.setattr(helpers, "get_data_many", request)
    query = Fetcher.transform_query({"symbol": "brk.b", "period": "quarter", "limit": limit})
    result = asyncio.run(Fetcher.aextract_data(query, {"fmp_api_key": "fixture-only"}))
    assert result is acquired


def test_cap_sort_and_missing_dates(row):
    from openbb_fmp.models.balance_sheet import FMPBalanceSheetFetcher as Fetcher
    query = Fetcher.transform_query({"symbol": "AAPL", "limit": 1})
    older = {**row, "date": "2024-09-30", "fiscalYear": 2024}
    result = Fetcher.transform_data(query, FMPAcquisition([older, row], datetime.now(UTC)))
    assert result.result[0].fiscal_year == 2025
    bounds = result.metadata["__qopenbb_financial__"]["bounds"]
    assert bounds["returned_count"] == 1
    assert bounds["truncated"] is True
    assert bounds["completeness"] == "partial"
    row.pop("date")
    with pytest.raises(FinancialError) as error:
        Fetcher.transform_data(query, FMPAcquisition([row], datetime.now(UTC)))
    assert error.value.code == "invalid_response"


def test_missing_period_remains_unknown_and_bad_amount_is_safe(row):
    from openbb_fmp.models.balance_sheet import FMPBalanceSheetFetcher as Fetcher
    query = Fetcher.transform_query({"symbol": "AAPL"})
    row.pop("period")
    row.pop("fiscalYear")
    result = Fetcher.transform_data(query, FMPAcquisition([row], datetime.now(UTC)))
    assert result.result[0].fiscal_period is None
    assert result.result[0].fiscal_year is None
    row["netDebt"] = "private-invalid-value"
    with pytest.raises(FinancialError) as error:
        Fetcher.transform_data(query, FMPAcquisition([row], datetime.now(UTC)))
    assert error.value.code == "invalid_response"
    assert "private-invalid-value" not in str(error.value)
    assert error.value.__context__ is None


def test_quarterly_alias_and_strict_limit():
    from openbb_fmp.models.balance_sheet import FMPBalanceSheetFetcher as Fetcher
    query = Fetcher.transform_query({"symbol": "aapl", "period": "quarterly"})
    assert query.period == "quarter"
    for limit in (True, 1.5, "2", None):
        with pytest.raises(FinancialError):
            Fetcher.transform_query({"symbol": "AAPL", "limit": limit})


@pytest.mark.parametrize("labels", [["FY"], ["Q1"], ["FY", "Q1"], [None], ["YTD"], []])
def test_class_declarations_agree_with_runtime_and_are_independent(labels):
    from openbb_core.provider.standard_models.financial_annotations import (
        bind_data_annotation, bind_query_annotation, render_field_templates,
    )
    from openbb_fmp.models.balance_sheet import (
        FMPBalanceSheetQueryParams as Query, FMPBalanceSheetData as Data,
        FMPBalanceSheetFetcher as StatementFetcher,
    )
    query = StatementFetcher.transform_query({"symbol": "A", "period": "quarter"})
    declaration = bind_query_annotation(Query)
    assert declaration.provider_policy == "explicit"
    assert declaration.response_policy.mode == "clip"
    assert declaration.response_policy.limit_parameter == "limit"
    assert declaration.response_policy.max_rows is None
    assert Query.model_fields["limit"].default == 5
    templates = bind_data_annotation(Data)
    assert set(templates.fields) == set(Data.model_fields)
    assert "fields.availability" in templates.runtime_properties
    before = templates.model_dump()
    rows = [{"date": "2025-09-30", "period": label, "reportedCurrency": "EUR",
             "totalDebt": -5, "netIncome": -7, "cashAtBeginningOfPeriod": 0}
            for label in labels]
    receipt = datetime(2025, 11, 1, tzinfo=UTC)
    result = StatementFetcher.transform_data(query, FMPAcquisition(rows, receipt))
    actual = result.metadata["__qopenbb_financial__"]["fields"]
    rendered = render_field_templates(Data)
    for name, template in rendered.items():
        runtime = actual[name]
        for attribute in ("definition", "unit", "scale", "currency_field", "value_origin",
                          "observation_date_field", "publication_date_field", "financial_basis"):
            assert runtime[attribute] == getattr(template, attribute)
        amount = name not in {"period_ending", "fiscal_period", "fiscal_year", "filing_date",
                              "accepted_date", "cik", "symbol", "reported_currency"}
        assert runtime["period_basis"] == ("instant" if amount else None)
        assert runtime["availability"] == (
            "available" if any(getattr(row, name) is not None for row in result.result) else "missing"
        )
    first = next(iter(rendered.values()))
    first.financial_basis["mutated"] = "request-local"
    assert bind_data_annotation(Data).model_dump() == before
    assert all("mutated" not in field.financial_basis for field in render_field_templates(Data).values())
