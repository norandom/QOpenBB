import asyncio
from copy import deepcopy
import json
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import pytest


FIXTURE = Path(__file__).with_name('fixtures') / 'income.json'
SENTINEL = 'fixture-server-key-not-a-credential'

@pytest.fixture
def income_boundary(monkeypatch):
    from openbb_core.app.model.user_settings import UserSettings
    from openbb_core.app.service.user_service import UserService
    from openbb_core.provider.utils import helpers
    data = json.loads(FIXTURE.read_text())
    calls = []
    async def request(url, **kwargs):
        parsed = urlparse(url)
        params = parse_qs(parsed.query)
        assert parsed.path == '/stable/income-statement'
        assert parsed.netloc == 'financialmodelingprep.com'
        assert params['apikey'] == [SENTINEL]
        assert set(params) == {'symbol', 'period', 'limit', 'apikey'}
        calls.append(params)
        return deepcopy(data[:int(params['limit'][0])])
    settings = UserSettings.model_construct()
    settings.credentials.fmp_api_key = SENTINEL
    monkeypatch.setattr(UserService, 'read_from_file', lambda *a, **k: settings)
    monkeypatch.setattr(helpers, 'amake_request', request)
    return data, calls

@pytest.mark.parametrize('symbol,limit', [('aapl', 1), (' aapl ', 2), ('brk.b', 2)])
def test_installed_income_annual_fidelity(income_boundary, symbol, limit):
    from openbb_core.api.rest_api import app
    data, calls = income_boundary
    status, text = asyncio.run(get_income(app, {'provider': 'fmp', 'symbol': symbol,
                                               'period': 'annual', 'limit': limit}))
    assert status == 200, text
    body = json.loads(text)
    assert body['provider'] == 'fmp'
    assert calls[0]['symbol'] == [symbol.strip().upper()]
    assert calls[0]['period'] == ['annual']
    assert calls[0]['limit'] == [str(limit)]
    assert len(body['results']) == limit
    from openbb_fmp.models.income_statement import FMPIncomeStatementData
    for raw, row in zip(data, body['results']):
        assert row['period_ending'] == raw['date']
        assert row['fiscal_period'] == raw['period']
        assert row['fiscal_year'] == int(raw['calendarYear'])
        assert row['filing_date'] == raw['filingDate']
        assert row['reported_currency'] == raw['reportedCurrency']
        for field, alias in FMPIncomeStatementData.__alias_dict__.items():
            if alias in raw and field not in {'period_ending', 'fiscal_year', 'accepted_date'}:
                assert row.get(field) == raw[alias], field
        assert row.get('net_interest_income') is None
    assert SENTINEL not in text

async def get_income(app, params):
    from urllib.parse import urlencode
    messages = []
    sent = False
    async def receive():
        nonlocal sent
        if not sent:
            sent = True
            return {'type': 'http.request', 'body': b'', 'more_body': False}
        await asyncio.Future()
    async def send(message):
        messages.append(message)
    path = '/api/v1/equity/fundamental/income'
    scope = {'type': 'http', 'asgi': {'version': '3.0'}, 'http_version': '1.1',
             'method': 'GET', 'scheme': 'http', 'path': path, 'raw_path': path.encode(),
             'root_path': '', 'query_string': urlencode(params).encode(), 'headers': [],
             'client': ('127.0.0.1', 12000), 'server': ('test', 80)}
    await app(scope, receive, send)
    status = next(m['status'] for m in messages if m['type'] == 'http.response.start')
    return status, b''.join(m.get('body', b'') for m in messages
                            if m['type'] == 'http.response.body').decode()

def test_income_query_defaults_encoding_and_nonmutation(income_boundary):
    from openbb_fmp.models.income_statement import FMPIncomeStatementFetcher as Fetcher
    data, calls = income_boundary
    query = Fetcher.transform_query({'symbol': ' ^gspc '})
    raw = asyncio.run(Fetcher.aextract_data(query, {'fmp_api_key': SENTINEL}))
    saved = deepcopy(raw)
    result = Fetcher.transform_data(query, raw).result
    assert raw == saved
    assert calls[0]['symbol'] == ['^GSPC']
    assert calls[0]['period'] == ['annual']
    assert calls[0]['limit'] == ['5']
    assert result[0].accepted_date.isoformat() == '2025-10-31T06:01:02'
    assert result[1].accepted_date is None
    zero = Fetcher.transform_query({'symbol': 'AAPL', 'limit': 0})
    from openbb_core.provider.utils.errors import EmptyDataError
    with pytest.raises(EmptyDataError):
        asyncio.run(Fetcher.aextract_data(zero, {'fmp_api_key': SENTINEL}))
    assert calls[-1]['limit'] == ['0']

@pytest.mark.parametrize('params', [{'period': 'weekly'}, {'limit': -1}])
def test_income_route_rejects_invalid_query(income_boundary, params):
    from openbb_core.api.rest_api import app
    status, _ = asyncio.run(get_income(app, {'provider': 'fmp', 'symbol': 'AAPL', **params}))
    assert status == 422
    assert income_boundary[1] == []


@pytest.mark.parametrize("year_key", ["calendarYear", "fiscalYear"])
@pytest.mark.parametrize("filing_key", ["filingDate", "fillingDate"])
def test_income_metadata_aliases(income_boundary, year_key, filing_key):
    from openbb_fmp.models.income_statement import FMPIncomeStatementFetcher as Fetcher
    from openbb_fmp.utils.helpers import FMPAcquisition
    from datetime import datetime, UTC
    row = deepcopy(income_boundary[0][0])
    row[year_key] = row.pop("calendarYear")
    row[filing_key] = row.pop("filingDate")
    raw = FMPAcquisition([row], datetime(2025, 11, 1, tzinfo=UTC))
    result = Fetcher.transform_data(Fetcher.transform_query({"symbol": "AAPL", "limit": 1}), raw)
    assert result.result[0].fiscal_year == 2025
    assert result.result[0].filing_date.isoformat() == "2025-10-31"
    meta = result.metadata["__qopenbb_financial__"]
    assert meta["retrieved_at"] == "2025-11-01T00:00:00Z"
    assert meta["fields"]["revenue"]["currency_field"] == "reported_currency"
    assert meta["fields"]["weighted_average_basic_shares_outstanding"]["unit"] == "shares"
    assert meta["fields"]["basic_earnings_per_share"]["unit"] == "currency/share"
    assert meta["bounds"]["completeness"] == "unknown"
    assert meta["observation_date_field"] == "period_ending"
    assert meta["publication_date_field"] == "filing_date"


def test_income_public_metadata(income_boundary):
    from openbb_core.api.rest_api import app
    status, text = asyncio.run(get_income(app, {"provider": "fmp", "symbol": "AAPL", "limit": 1}))
    assert status == 200
    meta = json.loads(text)["extra"]["results_metadata"]["__qopenbb_financial__"]
    assert meta["bounds"]["effective_limit"] == 1
    assert SENTINEL not in text


@pytest.mark.parametrize("limit", [None, 1])
def test_income_acquisition_truncation_and_safe_failure(income_boundary, limit):
    from openbb_fmp.models.income_statement import FMPIncomeStatementFetcher as Fetcher
    from openbb_core.provider.utils.financial_errors import FinancialError
    from openbb_fmp.utils.helpers import FMPAcquisition
    from datetime import UTC, datetime
    query = Fetcher.transform_query({"symbol": "AAPL", "limit": limit})
    acquired = asyncio.run(Fetcher.aextract_data(query, {"fmp_api_key": SENTINEL}))
    result = Fetcher.transform_data(query, acquired)
    assert result.metadata["__qopenbb_financial__"]["retrieved_at"] == acquired.retrieved_at.isoformat().replace("+00:00", "Z")
    rows = deepcopy(income_boundary[0])
    rows[1]["reportedCurrency"] = "EUR"
    result = Fetcher.transform_data(query, FMPAcquisition(rows, datetime(2025, 11, 1, tzinfo=UTC)))
    meta = result.metadata["__qopenbb_financial__"]
    assert meta["bounds"]["truncated"] is None
    assert len(result.result) == 2
    assert meta["effective_query"]["limit"] == (5 if limit is None else limit)
    assert meta["fields"]["revenue"]["currency"] is None
    if limit is None:
        assert result.result[1].reported_currency == "EUR"
    rows[0]["revenue"] = "secret-invalid-provider-value"
    with pytest.raises(FinancialError) as error:
        Fetcher.transform_data(query, FMPAcquisition(rows, acquired.retrieved_at))
    assert error.value.code == "invalid_response"
    assert "secret-invalid-provider-value" not in str(error.value)
    assert error.value.__context__ is None


def test_income_zero_preserves_nonempty_provider_rows(income_boundary, monkeypatch):
    from openbb_fmp.models.income_statement import FMPIncomeStatementFetcher as Fetcher
    from openbb_core.provider.utils import helpers
    from urllib.parse import parse_qs, urlsplit
    async def request(url, **kwargs):
        assert parse_qs(urlsplit(url).query)["limit"] == ["0"]
        return deepcopy(income_boundary[0])
    monkeypatch.setattr(helpers, "amake_request", request)
    query = Fetcher.transform_query({"symbol": "AAPL", "limit": 0})
    raw = asyncio.run(Fetcher.aextract_data(query, {"fmp_api_key": SENTINEL}))
    result = Fetcher.transform_data(query, raw)
    assert len(result.result) == 2
    assert result.result[0].revenue == 416161000000
    meta = result.metadata["__qopenbb_financial__"]
    assert meta["bounds"]["requested_limit"] == 0
    assert meta["bounds"]["effective_limit"] is None
    assert meta["effective_query"]["limit"] == 0
