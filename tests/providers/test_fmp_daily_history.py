"""Daily historical prices preserve source observations and bounded-query provenance."""
import asyncio
from copy import deepcopy
from datetime import UTC, datetime
from urllib.parse import parse_qs, urlsplit

import pytest
from openbb_core.provider.standard_models.financial_metadata import FINANCIAL_METADATA_KEY
from openbb_core.provider.utils.financial_errors import FinancialError, FinancialErrorCode
from openbb_fmp.models.equity_historical import FMPEquityHistoricalFetcher as Fetcher
from openbb_fmp.utils.helpers import FMPAcquisition

STAMP = datetime(2024, 3, 1, tzinfo=UTC)
BASE = {"symbol": "A", "start_date": "2020-02-29", "end_date": "2025-02-28"}


def row(date="2024-02-29", **values):
    return {"date": date, "open": 10, "high": 12, "low": 9, "close": 11,
            "volume": 0, "change": 0, "changePercent": 0, **values}


def result(payload, **params):
    return Fetcher.transform_data(Fetcher.transform_query({**BASE, **params}),
                                  FMPAcquisition(payload, STAMP))


def test_fidelity_nulls_zero_and_nonmutation():
    payload = [row(open=None, close=None, vwap=None)]
    original = deepcopy(payload)
    answer = result(payload)
    assert payload == original
    value = answer.result[0]
    assert value.open is None and value.close is None and value.vwap is None
    assert value.change_percent == 0 and value.volume == 0
    metadata = answer.metadata[FINANCIAL_METADATA_KEY]
    assert datetime.fromisoformat(metadata["retrieved_at"]) == STAMP
    assert metadata["fields"]["close"]["currency"] is None
    assert metadata["fields"]["close"]["unit"] == "currency/share"
    assert metadata["fields"]["change_percent"]["value_origin"] == "locally_derived"
    assert metadata["bounds"]["completeness"] == "unknown"
    assert metadata["point_in_time_safe"] is False


@pytest.mark.parametrize("value,expected", [(2, .02), (-2, -.02), (0, 0), (None, None)])
def test_percent_points_to_fraction(value, expected):
    assert result([row(changePercent=value)]).result[0].change_percent == expected


def test_stable_ascending_duplicates_and_no_missing_dates_inserted():
    answer = result([row("2024-02-29", close=3), row("2024-02-27", close=1),
                     row("2024-02-29", close=4)])
    assert [v.close for v in answer.result] == [1, 3, 4]
    assert [v.date.isoformat() for v in answer.result] == ["2024-02-27", "2024-02-29", "2024-02-29"]


@pytest.mark.parametrize("params", [
    {"symbol": ""}, {"symbol": "A,B"}, {"symbol": "A\n"}, {"symbol": None},
    {"symbol": "A&apikey=secret"}, {"symbol": ["A"]},
    {"start_date": None}, {"end_date": None}, {"start_date": "bad"},
    {"start_date": "2024-03-02", "end_date": "2024-03-01"},
    {"end_date": "2025-03-01"}, {"interval": "1h"}, {"interval": "1m"},
    {"adjustment": "unadjusted"}, {"adjustment": "splits_and_dividends"},
])
def test_invalid_before_io(params, monkeypatch):
    async def forbidden(*args, **kwargs):
        pytest.fail("Invalid query reached I/O")
    monkeypatch.setattr("openbb_fmp.utils.helpers.get_data_many", forbidden)
    with pytest.raises(FinancialError) as caught:
        query = Fetcher.transform_query({**BASE, **params})
        asyncio.run(Fetcher.aextract_data(query, {}))
    assert caught.value.code == FinancialErrorCode.INVALID_PARAMETERS
    assert caught.value.__context__ is None


def test_calendar_bounds_and_input_nonmutation():
    params = dict(BASE)
    query = Fetcher.transform_query(params)
    assert params == BASE
    assert query.end_date.isoformat() == "2025-02-28"
    Fetcher.transform_query({**BASE, "start_date": "2019-03-01", "end_date": "2024-03-01"})


def test_cap_is_honest():
    answer = result([row()] * 5001)
    assert len(answer.result) == 5000
    bounds = answer.metadata[FINANCIAL_METADATA_KEY]["bounds"]
    assert bounds["effective_limit"] == 5000
    assert bounds["truncated"] is True and bounds["completeness"] == "partial"


@pytest.mark.parametrize("payload", [[row(date="bad-secret")], [row(close="secret")],
                                     [row(date="2024-02-29T12:00:00")], ["secret"],
                                     {"secret": "secret"}, [row(close=float("inf"))]])
def test_invalid_response_safe(payload):
    with pytest.raises(FinancialError) as caught:
        result(payload)
    assert caught.value.code == FinancialErrorCode.INVALID_RESPONSE
    assert "secret" not in str(caught.value) and caught.value.__context__ is None


def test_empty_is_missing():
    with pytest.raises(FinancialError) as caught:
        result([])
    assert caught.value.code == FinancialErrorCode.MISSING_DATA


def test_typed_transport(monkeypatch):
    async def transport(url, **kwargs):
        parsed = urlsplit(url)
        assert parsed.path == "/stable/historical-price-eod/full"
        assert parse_qs(parsed.query) == {"symbol": ["^GSPC"], "from": ["2020-02-29"],
                                          "to": ["2025-02-28"], "apikey": ["synthetic"]}
        assert kwargs["with_provenance"] is True and kwargs["typed_errors"] is True
        return FMPAcquisition([row()], STAMP)
    monkeypatch.setattr("openbb_fmp.utils.helpers.get_data_many", transport)
    query = Fetcher.transform_query({**BASE, "symbol": " ^gspc "})
    receipt = asyncio.run(Fetcher.aextract_data(query, {"fmp_api_key": "synthetic"}))
    assert receipt.retrieved_at == STAMP
