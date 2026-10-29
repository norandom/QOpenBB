"""Enterprise inputs retain source observations without a local EV calculation."""
import asyncio
from copy import deepcopy
from datetime import UTC, datetime
from urllib.parse import parse_qs, urlsplit

import pytest

from openbb_core.provider.standard_models.financial_metadata import FINANCIAL_METADATA_KEY
from openbb_core.provider.utils.financial_errors import FinancialError
from openbb_fmp.models.enterprise_values import FMPEnterpriseValuesFetcher as Fetcher
from openbb_fmp.utils.helpers import FMPAcquisition

STAMP = datetime(2024, 2, 3, tzinfo=UTC)


def observation(**extra):
    return {"symbol": "ABC", "date": "2023-12-31", "stockPrice": 0,
            "numberOfShares": 10, "marketCapitalization": 100,
            "minusCashAndCashEquivalents": 200, "addTotalDebt": -1,
            "enterpriseValue": -7, **extra}


@pytest.mark.parametrize("params", [
    {"symbol": x} for x in [None, "", "A,B", "A&apikey=secret", "A\n"]
] + [{"symbol": "A", "limit": x} for x in [0, 1001, True, "5", 5., None]]
  + [{"symbol": "A", "period": "ttm"}, {"symbol": "A", "ttm": "include"},
     {"symbol": "A", "fields": "enterprise_value"}])
def test_invalid_queries(params):
    with pytest.raises(FinancialError):
        Fetcher.transform_query(params)


def test_components_dates_currency_and_unknown_basis():
    payload = [observation(reportedCurrency="EUR")]
    original = deepcopy(payload)
    result = Fetcher.transform_data(Fetcher.transform_query({"symbol": " abc "}),
                                    FMPAcquisition(payload, STAMP))
    row = result.result[0]
    assert payload == original
    assert (row.stock_price, row.number_of_shares, row.market_cap) == (0, 10, 100)
    assert (row.cash_and_cash_equivalents, row.total_debt, row.enterprise_value) == (200, -1, -7)
    assert row.date.isoformat() == "2023-12-31" and row.currency == "EUR"
    meta = result.metadata[FINANCIAL_METADATA_KEY]
    assert datetime.fromisoformat(meta["retrieved_at"]) == STAMP
    assert set(meta["fields"]) == set(type(row).model_fields)
    assert meta["fields"]["stock_price"]["unit"] == "currency/share"
    assert meta["fields"]["number_of_shares"]["unit"] == "shares"
    assert meta["fields"]["enterprise_value"]["value_origin"] == "provider_calculation"
    assert all(v is None for v in meta["fields"]["enterprise_value"]["financial_basis"].values())
    assert meta["valuation_date_field"] is None and meta["point_in_time_safe"] is False


def test_missing_and_stable_duplicates_clipped():
    query = Fetcher.transform_query({"symbol": "ABC", "limit": 2})
    payload = [{"symbol": "ABC"}, observation(enterpriseValue=1), observation(enterpriseValue=2)]
    result = Fetcher.transform_data(query, FMPAcquisition(payload, STAMP))
    assert [r.enterprise_value for r in result.result] == [1, 2]
    assert result.metadata[FINANCIAL_METADATA_KEY]["bounds"]["truncated"] is True
    missing = Fetcher.transform_data(query, FMPAcquisition(payload[:1], STAMP))
    assert all(getattr(missing.result[0], f) is None for f in type(missing.result[0]).model_fields if f != "symbol")
    assert missing.metadata[FINANCIAL_METADATA_KEY]["bounds"]["completeness"] == "unknown"


@pytest.mark.parametrize("field,value", [("stockPrice", "bad"), ("date", "bad"),
                                         ("enterpriseValue", float("nan")), ("numberOfShares", float("inf"))])
def test_safe_bad_rows(field, value):
    with pytest.raises(FinancialError):
        Fetcher.transform_data(Fetcher.transform_query({"symbol": "ABC"}),
                               FMPAcquisition([observation(**{field: value})], STAMP))


@pytest.mark.parametrize("period,expected", [("annual", "annual"), ("quarter", "quarter"), ("quarterly", "quarter")])
def test_documented_transport(monkeypatch, period, expected):
    calls = []
    async def transport(url, **kwargs):
        calls.append((url, kwargs))
        return FMPAcquisition([observation()], STAMP)
    monkeypatch.setattr("openbb_fmp.utils.helpers.get_data_many", transport)
    query = Fetcher.transform_query({"symbol": "abc", "period": period})
    result = asyncio.run(Fetcher.aextract_data(query, {"fmp_api_key": "test"}))
    assert result.retrieved_at == STAMP
    url, kwargs = calls[0]
    assert urlsplit(url).path == "/stable/enterprise-values"
    assert parse_qs(urlsplit(url).query) == {"symbol": ["ABC"], "period": [expected], "limit": ["5"], "apikey": ["test"]}
    assert kwargs == {"with_provenance": True, "typed_errors": True}


def test_canonical_aliases_and_empty_result():
    query = Fetcher.transform_query({"symbol": "ABC"})
    row = Fetcher.transform_data(query, FMPAcquisition([{"symbol": "ABC", "stock_price": -2,
        "number_of_shares": 0, "market_cap": None, "currency": "GBP"}], STAMP)).result[0]
    assert row.stock_price == -2 and row.number_of_shares == 0 and row.market_cap is None
    assert row.currency == "GBP"
    assert Fetcher.transform_data(query, FMPAcquisition([], STAMP)).result == []
