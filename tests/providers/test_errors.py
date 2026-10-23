"""FMP response failures through installed routes; synthetic credentials only."""
import asyncio
import json
import pytest
from urllib.parse import urlsplit
from test_income import get_income

SENTINEL = 'failure-fixture-key-only'

@pytest.mark.parametrize('status,payload,category', [
    (401, {}, 'authentication'), (403, {}, 'entitlement'),
    (429, {}, 'throttling'), (400, {}, 'invalid_parameters'),
    (404, {}, 'missing_data'), (500, {}, 'upstream'),
    (200, {'Error Message': f'Invalid API KEY https://fmp.test/?apikey={SENTINEL}'}, 'authentication'),
    (200, {'Error Message': 'Upgrade your subscription'}, 'entitlement'),
    (200, {'error': 'Limit Reach. Please upgrade'}, 'throttling'),
    (200, {'error': 'Invalid symbol parameter'}, 'invalid_parameters'),
    (200, {'Error Message': f'Upgrade your subscription: https://financialmodelingprep.com/stable/profile?apikey={SENTINEL}'}, 'entitlement'),
    (200, {'error': f'Invalid symbol parameter: https://financialmodelingprep.com/stable/profile?apikey={SENTINEL}'}, 'invalid_parameters'),
    (200, {'error': f'No data found: https://financialmodelingprep.com/stable/profile?apikey={SENTINEL}'}, 'missing_data'),
    (200, [], 'missing_data'),
])
@pytest.mark.parametrize('route', ['income', 'profile'])
def test_failure_routes(monkeypatch, caplog, capsys, status, payload, category, route):
    from openbb_core.app.model.user_settings import UserSettings
    from openbb_core.app.service.user_service import UserService
    from openbb_core.provider.utils import helpers
    from openbb_core.api.rest_api import app
    from test_profile import _get_profile
    calls = []
    class Response:
        async def json(self):
            return payload
        async def text(self):
            return f'https://financialmodelingprep.com/stable/?apikey={SENTINEL}'
    response = Response()
    response.status = status
    async def request(url, **kwargs):
        calls.append(url)
        return await kwargs['response_callback'](response, None)
    settings = UserSettings.model_construct()
    settings.credentials.fmp_api_key = SENTINEL
    monkeypatch.setattr(UserService, 'read_from_file', lambda *a, **k: settings)
    monkeypatch.setattr(helpers, 'amake_request', request)
    if route == 'profile':
        code, text = asyncio.run(_get_profile(app))
    else:
        code, text = asyncio.run(get_income(app, {'provider': 'fmp', 'symbol': 'AAPL'}))
    if category == 'missing_data':
        assert code == 204
        assert text == ''
    else:
        assert code >= 400, text
        assert f'FMP[{category}]' in text
    assert len(calls) == (2 if route == 'profile' else 1)
    assert all(urlsplit(url).hostname == 'financialmodelingprep.com' for url in calls)
    output = capsys.readouterr()
    assert SENTINEL not in text + caplog.text + output.out + output.err

@pytest.mark.parametrize('error,category', [(TimeoutError, 'timeout'), (ConnectionError, 'connection')])
def test_transport_redaction(monkeypatch, caplog, capsys, error, category):
    from openbb_fmp.utils.helpers import get_data
    from openbb_core.provider.utils import helpers
    async def request(url, **kwargs):
        raise error(f'{url} Authorization: Bearer {SENTINEL}')
    monkeypatch.setattr(helpers, 'amake_request', request)
    with pytest.raises(Exception) as caught:
        asyncio.run(get_data(f'https://financialmodelingprep.com/?apikey={SENTINEL}'))
    assert f'FMP[{category}]' in str(caught.value)
    import traceback
    output = capsys.readouterr()
    rendered = ''.join(traceback.format_exception(caught.value))
    assert SENTINEL not in rendered + caplog.text + output.out + output.err


@pytest.mark.parametrize('error,category', [(TimeoutError, 'timeout'), (ConnectionError, 'connection')])
@pytest.mark.parametrize('route', ['income', 'profile'])
def test_route_transport_failure(monkeypatch, caplog, capsys, error, category, route):
    from openbb_core.app.model.user_settings import UserSettings
    from openbb_core.app.service.user_service import UserService
    from openbb_core.provider.utils import helpers
    from openbb_core.api.rest_api import app
    from test_profile import _get_profile
    settings = UserSettings.model_construct()
    settings.credentials.fmp_api_key = SENTINEL
    monkeypatch.setattr(UserService, 'read_from_file', lambda *a, **k: settings)
    async def request(url, **kwargs):
        raise error(f'{url} Authorization: Bearer {SENTINEL}')
    monkeypatch.setattr(helpers, 'amake_request', request)
    if route == 'profile':
        code, text = asyncio.run(_get_profile(app))
    else:
        code, text = asyncio.run(get_income(app, {'provider': 'fmp', 'symbol': 'AAPL'}))
    assert code >= 400
    assert f'FMP[{category}]' in text
    output = capsys.readouterr()
    assert SENTINEL not in text + caplog.text + output.out + output.err


def test_malformed_response_drops_exception_context():
    from openbb_fmp.utils.helpers import response_callback
    class Response:
        status = 200
        async def json(self):
            raise ValueError(f'Invalid JSON at https://fmp.test/?apikey={SENTINEL}')
    with pytest.raises(Exception) as caught:
        asyncio.run(response_callback(Response(), None))
    import traceback
    assert 'FMP[invalid_response]' in str(caught.value)
    assert SENTINEL not in ''.join(traceback.format_exception(caught.value))
