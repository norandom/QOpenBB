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
    result = Fetcher.transform_data(query, raw)
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
