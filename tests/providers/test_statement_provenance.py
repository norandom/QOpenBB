"""Statement evidence stays bound to acquired observations through route ordering."""
from copy import deepcopy
from datetime import UTC, datetime
import pytest
from openbb_fmp.utils.helpers import FMPAcquisition

STAMP = datetime(2025, 11, 1, tzinfo=UTC)


def fetcher(route):
    if route == "income":
        from openbb_fmp.models.income_statement import FMPIncomeStatementFetcher
        return FMPIncomeStatementFetcher
    if route == "balance":
        from openbb_fmp.models.balance_sheet import FMPBalanceSheetFetcher
        return FMPBalanceSheetFetcher
    from openbb_fmp.models.cash_flow import FMPCashFlowStatementFetcher
    return FMPCashFlowStatementFetcher


def source(marker, date="2025-09-30", period="Q3"):
    return {"date": date, "period": period, "fiscalYear": "2025",
            "filingDate": "2025-10-31", "acceptedDate": None,
            "reportedCurrency": "USD", "revenue": marker, "totalAssets": marker,
            "netIncome": marker, "cashAtBeginningOfPeriod": 0,
            "cashAtEndOfPeriod": 7, "freeCashFlow": None}


@pytest.mark.parametrize("route", ["income", "balance", "cash"])
@pytest.mark.parametrize("frequency", ["annual", "quarter"])
def test_bound_source_rows_unknown_coverage(route, frequency):
    provider = fetcher(route)
    payload = [source(1, "2024-09-30", "FY"), source(0), source(-3), source(4)]
    payload[1]["calendarYear"] = "2024"
    payload[1]["fillingDate"] = None
    payload[2].pop("acceptedDate")
    saved = deepcopy(payload)
    query = provider.transform_query({"symbol": "MSFT", "period": frequency, "limit": 2})
    result = provider.transform_data(query, FMPAcquisition(payload, STAMP))
    assert payload == saved
    meta = result.metadata["__qopenbb_financial__"]
    provenance = meta["statement_provenance"]["rows"]
    ordinals = [0, 1, 2, 3] if route == "income" else [1, 2]
    assert [item["source_ordinal"] for item in provenance] == ordinals
    assert len(provenance) == len(result.result) == meta["bounds"]["returned_count"]
    for index, (item, row, ordinal) in enumerate(zip(provenance, result.result, ordinals)):
        assert item["row_index"] == index
        assert item["period_end"] == row.period_ending.isoformat()
        assert item["fiscal_period"] == row.fiscal_period
        assert item["fiscal_year"] == row.fiscal_year
        assert item["requested_frequency"] == frequency
        assert item["flow_coverage"] == "unknown"
        assert item["coverage_status"] == ("conflicting" if ordinal == 1 else "unavailable")
        assert item["period_start"] is None and item["duration_days"] is None
        assert item["restatement_status"] == "unknown" and item["conventions"] == []
        facts = {fact["source_field"]: fact for fact in item["facts"]}
        assert ("acceptedDate" in facts) == (ordinal != 2)
        if ordinal != 2:
            assert facts["acceptedDate"]["presence"] == "null"
        if route == "cash":
            assert item["instant_dates"]["cash_at_beginning_of_period"] is None
            assert item["instant_dates"]["cash_at_end_of_period"] == item["period_end"]
        if route == "balance":
            assert item["instant_dates"]["total_assets"] == item["period_end"]
        field = {"income": "revenue", "balance": "total_assets", "cash": "net_income"}[route]
        assert getattr(row, field) == saved[ordinal][{"income": "revenue", "balance": "totalAssets", "cash": "netIncome"}[route]]
        assert meta["fields"][field]["period_basis"] == ("instant" if route == "balance" else None)
    assert meta["point_in_time_safe"] is False


@pytest.mark.parametrize("route", ["income", "balance", "cash"])
def test_unfamiliar_labels_and_safe_malformed_evidence(route):
    from openbb_core.provider.utils.financial_errors import FinancialError
    provider = fetcher(route)
    query = provider.transform_query({"symbol": "MSFT", "period": "quarter"})
    row = source(0, "2025-09-30T00:00:00", "H1")
    row["fiscalYear"] = -1
    result = provider.transform_data(query, FMPAcquisition([row], STAMP))
    item = result.metadata["__qopenbb_financial__"]["statement_provenance"]["rows"][0]
    assert item["fiscal_period"] == "H1" and item["fiscal_year"] == -1
    row["calendarYear"] = "secret-invalid-provider-value"
    with pytest.raises(FinancialError) as caught:
        provider.transform_data(query, FMPAcquisition([row], STAMP))
    assert caught.value.code == "invalid_response"
    assert "secret-invalid-provider-value" not in str(caught.value)


@pytest.mark.parametrize("period", ["q1", "q2", "q3", "q4", "fy", "ttm"])
def test_other_income_requests_preserve_baseline_contract(period):
    provider = fetcher("income")
    query = provider.transform_query({"symbol": "MSFT", "period": period})
    result = provider.transform_data(query, FMPAcquisition([source(0)], STAMP))
    meta = result.metadata["__qopenbb_financial__"]
    assert "statement_provenance" not in meta
    assert meta["fields"]["revenue"]["period_basis"] == ("trailing_twelve_months" if period == "ttm" else None)


@pytest.mark.parametrize("route", ["income", "balance", "cash"])
def test_current_null_alias_wins_without_losing_legacy_fact(route):
    provider = fetcher(route)
    row = source(0)
    row.update(fiscalYear=None, calendarYear="2024", filingDate=None,
               fillingDate="2025-10-30", arbitrarySecret="never copied",
               periodStart="2025-01-01", duration=273)
    result = provider.transform_data(provider.transform_query({"symbol": "MSFT"}),
                                     FMPAcquisition([row], STAMP))
    assert result.result[0].fiscal_year is None
    assert result.result[0].filing_date is None
    item = result.metadata["__qopenbb_financial__"]["statement_provenance"]["rows"][0]
    assert item["coverage_status"] == "conflicting"
    assert item["period_start"] is None and item["duration_days"] is None
    assert len(item["facts"]) == 7
    assert "never copied" not in str(item)


def test_builder_rejects_misbound_source_identity_safely():
    from openbb_core.provider.utils.financial_errors import FinancialError
    from openbb_fmp.models.income_statement import FMPIncomeStatementData
    from openbb_fmp.utils.statement_provenance import statement_bundles, statement_provenance
    query = fetcher("income").transform_query({"symbol": "MSFT"})
    bundles = statement_bundles(FMPIncomeStatementData, [source(1)])
    bundles[0].row.fiscal_year = 2024
    with pytest.raises(FinancialError) as caught:
        statement_provenance(query, bundles, {})
    assert caught.value.code == "invalid_response"
