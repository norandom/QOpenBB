"""Cash-flow fixtures retain reported observations without a house cash model."""
import asyncio
from copy import deepcopy
from datetime import UTC, datetime
from urllib.parse import parse_qs, urlsplit

import pytest

from openbb_core.provider.standard_models.financial_metadata import FINANCIAL_METADATA_KEY
from openbb_core.provider.utils.financial_errors import FinancialError, FinancialErrorCode
from openbb_fmp.models.cash_flow import FMPCashFlowStatementFetcher as Fetcher
from openbb_fmp.utils.helpers import FMPAcquisition

STAMP = datetime(2024, 2, 3, 4, 5, tzinfo=UTC)


def fixture(period="FY", date="2023-12-31"):
    return {"date": date, "period": period, "fiscalYear": "2023",
            "filingDate": "2024-02-01", "acceptedDate": "2024-02-01 18:00:00",
            "reportedCurrency": "EUR", "symbol": "EXAMPLE", "netIncome": -7,
            "operatingCashFlow": 0, "capitalExpenditure": -15,
            "freeCashFlow": None, "cashAtEndOfPeriod": 42, "cashAtBeginningOfPeriod": 39,
            "incomeTaxesPaid": -2, "interestPaid": 0}


@pytest.mark.parametrize("period,fiscal", [("annual", "FY"), ("quarter", "Q4")])
def test_fidelity_metadata_and_nonmutation(period, fiscal):
    query = Fetcher.transform_query({"symbol": " example ", "period": period})
    payload = [fixture(fiscal)]
    original = deepcopy(payload)
    result = Fetcher.transform_data(query, FMPAcquisition(payload, STAMP))
    row = result.result[0]
    assert payload == original
    assert row.period_ending.isoformat() == "2023-12-31"
    assert row.fiscal_period == fiscal and row.fiscal_year == 2023
    assert row.filing_date.isoformat() == "2024-02-01"
    assert row.accepted_date.isoformat() == "2024-02-01T18:00:00"
    assert row.net_income == -7 and row.operating_cash_flow == 0
    assert row.capital_expenditure == -15 and row.free_cash_flow is None
    assert row.income_taxes_paid == -2 and row.interest_paid == 0
    metadata = result.metadata[FINANCIAL_METADATA_KEY]
    assert datetime.fromisoformat(metadata["retrieved_at"]) == STAMP
    assert metadata["effective_query"] == {"symbol": "EXAMPLE", "period": period, "limit": 5}
    assert metadata["point_in_time_safe"] is False
    assert set(metadata["fields"]) == set(type(row).model_fields)
    amount = metadata["fields"]["capital_expenditure"]
    assert amount["unit"] == "currency" and amount["scale"] == 1
    assert amount["currency_field"] == "reported_currency"
    assert amount["financial_basis"]["cash"] is None
    assert amount["period_basis"] == ("annual" if period == "annual" else "discrete_quarter")
    assert metadata["fields"]["free_cash_flow"]["value_origin"] == "provider_calculation"
    assert metadata["fields"]["free_cash_flow"]["availability"] == "missing"
    assert metadata["bounds"]["completeness"] == "unknown"
    assert metadata["transformations"] == []


@pytest.mark.parametrize("params", [
    {"symbol": ""}, {"symbol": "   "}, {"symbol": "A,B"},
    {"symbol": "A B"}, {"symbol": "A&apikey=bad"}, {"symbol": None},
    {"symbol": "A", "period": "ttm"}, {"symbol": "A", "period": "monthly"},
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
        assert parsed.path == "/stable/cash-flow-statement"
        assert parse_qs(parsed.query) == {"symbol": ["^GSPC"], "period": ["quarter"],
                                          "limit": ["1000"], "apikey": ["synthetic"]}
        assert kwargs["with_provenance"] is True
        assert kwargs["typed_errors"] is True
        return FMPAcquisition([fixture("Q4")], STAMP)
    monkeypatch.setattr("openbb_fmp.utils.helpers.get_data_many", transport)
    query = Fetcher.transform_query({"symbol": "^gspc", "period": "quarter", "limit": 1000})
    assert asyncio.run(Fetcher.aextract_data(query, {"fmp_api_key": "synthetic"})).retrieved_at == STAMP


def test_legacy_aliases_order_duplicates_and_observed_truncation():
    old = fixture("Q3", "2023-09-30")
    old["calendarYear"] = old.pop("fiscalYear")
    old["fillingDate"] = old.pop("filingDate")
    alias_result = Fetcher.transform_data(Fetcher.transform_query({"symbol": "A"}),
                                         FMPAcquisition([old], STAMP)).result[0]
    assert alias_result.fiscal_year == 2023
    assert alias_result.filing_date.isoformat() == "2024-02-01"
    query = Fetcher.transform_query({"symbol": "A", "limit": 2, "period": "quarter"})
    result = Fetcher.transform_data(query, FMPAcquisition([old, fixture("Q4"), fixture("Q4")], STAMP))
    assert [row.fiscal_period for row in result.result] == ["Q4", "Q4"]
    bounds = result.metadata[FINANCIAL_METADATA_KEY]["bounds"]
    assert bounds["truncated"] is True and bounds["completeness"] == "partial"
    assert bounds["returned_count"] == 2


def test_invalid_row_is_safe():
    query = Fetcher.transform_query({"symbol": "A"})
    with pytest.raises(FinancialError) as caught:
        Fetcher.transform_data(query, FMPAcquisition([{"date": "private-invalid-date"}], STAMP))
    assert caught.value.code == FinancialErrorCode.INVALID_RESPONSE
    assert "private-invalid-date" not in str(caught.value)
    assert caught.value.__context__ is None


@pytest.mark.parametrize("periods,expected", [(["FY"], "annual"),
    (["Q2"], "discrete_quarter"), (["FY", "Q2"], None), ([None], None), (["YTD"], None)])
def test_basis_uses_observed_period_labels(periods, expected):
    query = Fetcher.transform_query({"symbol": "A", "period": "quarterly"})
    assert query.period == "quarter"
    result = Fetcher.transform_data(query, FMPAcquisition([fixture(p) for p in periods], STAMP))
    assert result.metadata[FINANCIAL_METADATA_KEY]["fields"]["net_income"]["period_basis"] == expected


def test_all_retained_amount_aliases_preserve_signed_values():
    from openbb_fmp.models.cash_flow import FMPCashFlowStatementData
    non_amounts = {"period_ending", "fiscal_period", "fiscal_year", "filing_date",
                   "accepted_date", "cik", "symbol", "reported_currency"}
    amounts = set(FMPCashFlowStatementData.model_fields) - non_amounts
    source = fixture()
    for i, name in enumerate(sorted(amounts)):
        source[FMPCashFlowStatementData.__alias_dict__[name]] = -i
    result = Fetcher.transform_data(Fetcher.transform_query({"symbol": "A"}),
                                    FMPAcquisition([source], STAMP)).result[0]
    for name in amounts:
        assert getattr(result, name) == source[FMPCashFlowStatementData.__alias_dict__[name]]


@pytest.mark.parametrize("payload,code", [([], "missing_data"),
    ({"unexpected": "private-canary"}, "invalid_response"),
    (TimeoutError("private-canary"), "timeout")])
def test_real_transport_boundary_uses_typed_failures(payload, code, monkeypatch):
    async def request(url, **kwargs):
        if isinstance(payload, Exception):
            raise payload
        return payload
    monkeypatch.setattr("openbb_core.provider.utils.helpers.amake_request", request)
    query = Fetcher.transform_query({"symbol": "A"})
    with pytest.raises(FinancialError) as caught:
        asyncio.run(Fetcher.aextract_data(query, {"fmp_api_key": "synthetic"}))
    assert caught.value.code.value == code
    assert caught.value.__context__ is None
    assert "private-canary" not in str(caught.value)


@pytest.mark.parametrize("period,fiscal", [("annual", "FY"), ("quarter", "Q4")])
def test_cash_stocks_are_instants_and_beginning_date_is_unknown(period, fiscal):
    query = Fetcher.transform_query({"symbol": "A", "period": period})
    result = Fetcher.transform_data(query, FMPAcquisition([fixture(fiscal)], STAMP))
    metadata = result.metadata[FINANCIAL_METADATA_KEY]
    beginning = metadata["fields"]["cash_at_beginning_of_period"]
    ending = metadata["fields"]["cash_at_end_of_period"]
    assert beginning["period_basis"] == ending["period_basis"] == "instant"
    assert beginning["observation_date_field"] is None
    assert ending["observation_date_field"] == "period_ending"
    assert result.result[0].cash_at_beginning_of_period == 39
    assert any("Beginning cash" in limitation for limitation in metadata["limitations"])


@pytest.mark.parametrize("labels", [["FY"], ["Q1"], ["FY", "Q1"], [None], ["YTD"], []])
def test_class_declarations_agree_with_runtime_and_are_independent(labels):
    from openbb_core.provider.standard_models.financial_annotations import (
        bind_data_annotation, bind_query_annotation, render_field_templates,
    )
    from openbb_fmp.models.cash_flow import (
        FMPCashFlowStatementQueryParams as Query, FMPCashFlowStatementData as Data,
        FMPCashFlowStatementFetcher as StatementFetcher,
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
        basis = "annual" if labels == ["FY"] else "discrete_quarter" if labels == ["Q1"] else None
        expected = "instant" if name in {"cash_at_beginning_of_period", "cash_at_end_of_period"} else basis
        assert runtime["period_basis"] == expected
        assert runtime["availability"] == (
            "available" if any(getattr(row, name) is not None for row in result.result) else "missing"
        )
    first = next(iter(rendered.values()))
    first.financial_basis["mutated"] = "request-local"
    assert bind_data_annotation(Data).model_dump() == before
    assert all("mutated" not in field.financial_basis for field in render_field_templates(Data).values())
