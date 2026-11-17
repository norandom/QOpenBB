"""HTTP admission reaches real native dependencies and Fetcher execution offline."""
import asyncio
import json
from urllib.parse import urlencode

import pytest
from fastapi import APIRouter, FastAPI
from fmp_freeze_support import CONTRACTS, describe
from openbb_core.api.router.commands import add_command_map
from openbb_core.app.command_runner import CommandRunner
from openbb_core.app.model.command_context import CommandContext
from openbb_core.app.model.obbject import OBBject
from openbb_core.app.provider_interface import (
    ExtraParams,
    ProviderChoices,
    ProviderInterface,
    StandardParams,
)
from openbb_core.app.query import Query
from openbb_core.app.route_iter import iter_api_routes
from openbb_core.app.router import CommandMap, RouterLoader
from test_fmp_parameter_admission import native as native  # noqa: PLC0414


@pytest.fixture
def http_native(native, monkeypatch):
    from qopenbb_data.financial_errors import install_financial_error_handlers
    from qopenbb_data.financial_openapi import project_financial_openapi
    from qopenbb_data.financial_policy import FinancialProviderPolicy
    _, runner, calls = native
    network = []
    import aiohttp
    async def forbidden_network(*args, **kwargs):
        network.append(True)
        raise AssertionError('Offline admission tests must not use network')
    monkeypatch.setattr(aiohttp.ClientSession, '_request', forbidden_network)
    native_router = RouterLoader.from_extensions()
    async def controlled(cc: CommandContext, provider_choices: ProviderChoices,
                         standard_params: StandardParams, extra_params: ExtraParams,
                         chart: bool = False, chart_params: str | None = None) -> OBBject:
        result = await OBBject.from_query(Query(cc, provider_choices, standard_params, extra_params))
        result.extra['accepted_control'] = chart_params
        return result
    native_router.command(model='PriceTarget', path='/controlled')(controlled)
    from openbb_core.app.command_runner import ExecutionContext
    from openbb_core.app.static.package_builder.path_handler import PathHandler
    monkeypatch.setattr(ExecutionContext, '_route_map', PathHandler.build_route_map())
    runner = CommandRunner(CommandMap(native_router), runner.system_settings, runner.user_settings)
    router = APIRouter()
    add_command_map(runner, router)
    inner = FastAPI()
    inner.include_router(router, prefix='/concrete/v7')
    routes = tuple(iter_api_routes(inner))
    registry = ProviderInterface()._registry_map
    for name, descriptor in describe()['adapters'].items():
        selected = registry.original_models[descriptor['model_key']]['fmp']['query']
        selected.financial_query_annotation = CONTRACTS[name][0].financial_query_annotation
    document = project_financial_openapi(inner.openapi(), routes, registry,
                                         required_models=set(registry.original_models))
    install_financial_error_handlers(inner, document)
    app = FastAPI()
    app.add_middleware(FinancialProviderPolicy, document=document, registry=registry, routes=routes)
    app.mount('/', inner)
    return app, calls, network, registry


async def request(app, name, query, method='GET', root_path=''):
    messages = []
    scope = {'type': 'http', 'asgi': {'version':'3.0'}, 'http_version': '1.1',
                 'method': method, 'scheme': 'http', 'path': root_path+'/concrete/v7/'+name,
                 'raw_path': b'/', 'root_path': root_path, 'query_string': query.encode(),
                 'headers': [], 'server': ('offline',80), 'client': ('127.0.0.1',1)}
    async def receive():
        return {'type':'http.request', 'body':b'', 'more_body':False}
    async def send(message):
        messages.append(message)
    await app(scope, receive, send)
    assert scope['query_string'] == query.encode(), 'Admission must copy the caller scope'
    status = next(m['status'] for m in messages if m['type']=='http.response.start')
    body = b''.join(m.get('body',b'') for m in messages)
    return status, body


@pytest.mark.parametrize('name', CONTRACTS)
def test_all_eleven_reject_raw_before_fetcher(http_native, name):
    app, calls, network, _ = http_native
    bad = ['symbol=MSFT', 'provider=&symbol=MSFT', 'provider=bogus&symbol=MSFT',
           'provider=fmp&provider=fmp&symbol=MSFT', 'provider=fmp&symbol=MSFT&symbol=AAPL',
           'provider=fmp&symbol=MSFT&PRIVATE_KEY_SENTINEL=PRIVATE_VALUE_SENTINEL',
           'provider=fmp&symbol=MSFT&chart_params={}',
           'provider=fmp&symbol=MSFT,AAPL', 'provider=fmp&symbol=',
           'provider=fmp&symbol=MSFT%26apikey%3DSECRET']
    query = CONTRACTS[name][0]
    for field in ('limit','page'):
        if field in query.model_fields:
            bad += [f'provider=fmp&symbol=MSFT&{field}={v}' for v in
                    ('', 'null','true','false','-1','10001','1.2')]
            bad += [f'provider=fmp&symbol=MSFT&{field}=1&{field}=1']
        else:
            bad += [f'provider=fmp&symbol=MSFT&{field}=0']
    for value in bad:
        status, body = asyncio.run(request(app, name, value))
        assert status == 422, (value, status, body)
        assert json.loads(body)['code'] == 'invalid_parameters'
        assert all(v not in body for v in (b'PRIVATE_',b'SECRET',b'pydantic.dev'))
    assert calls == []
    assert network == []
    print(f'{name}: rejected={len(bad)} extraction=0 network=0')


@pytest.mark.parametrize('name', CONTRACTS)
def test_all_eleven_native_effective_values(http_native, name):
    app, calls, network, _ = http_native
    values = {'provider': 'fmp', 'symbol': ' msft '}
    fields = CONTRACTS[name][0].model_fields
    values.update({k:v for k,v in {'limit': '7','page': '2','period': 'quarterly',
                  'start_date': '2025-01-01','end_date': '2025-02-01'}.items() if k in fields})
    status, body = asyncio.run(request(app, name, urlencode(values)))
    assert status == 200, body
    assert len(calls) == 1
    assert calls[0]['symbol'] == 'MSFT'
    for key in ('limit','page'):
        if key in values:
            assert calls[0][key] == int(values[key])
    if 'period' in fields:
        assert calls[0]['period'] == 'quarter'
    if 'start_date' in fields:
        assert calls[0]['start_date'] == '2025-01-01'
        assert calls[0]['end_date'] == '2025-02-01'
    assert network == []
    print(f'{name}: valid=1 extraction=1 network=0 effective={calls[0]}')


def test_root_path_and_exact_method(http_native):
    app, calls, network, _ = http_native
    assert asyncio.run(request(app,'price_target','provider=fmp&symbol=MSFT',root_path='/origin'))[0] == 200
    assert asyncio.run(request(app,'price_target','',method='POST'))[0] == 405
    assert len(calls) == 1
    assert network == []


@pytest.mark.parametrize('name', CONTRACTS)
def test_omitted_selected_defaults_execute(http_native, name):
    app, calls, network, _ = http_native
    status, body = asyncio.run(request(app, name, 'provider=fmp&symbol=MSFT'))
    assert status == 200, body
    expected = CONTRACTS[name][0].model_validate({'symbol':'MSFT'}).model_dump(mode='json')
    assert calls == [expected]
    assert network == []
    print(f'{name}: omitted defaults extraction=1 network=0 effective={expected}')


def test_only_concrete_native_controls_allowed(http_native):
    app, calls, network, _ = http_native
    status, body = asyncio.run(request(app, 'controlled', 'provider=fmp&symbol=MSFT&chart=false&chart_params=native'))
    assert status == 200, body
    assert json.loads(body)['extra']['accepted_control'] == 'native'
    assert calls == [{'symbol':'MSFT','limit':20}]
    for query in ('chart=false&chart=false', 'chart_params=x&chart_params=y', 'chart=PRIVATE_VALUE_SENTINEL'):
        status, body = asyncio.run(request(app,'controlled','provider=fmp&symbol=MSFT&'+query))
        assert status == 422, body
        assert b'PRIVATE_' not in body
    assert len(calls) == 1 and network == []


def test_selected_aliases_and_collisions(http_native, monkeypatch):
    from pydantic import AliasChoices
    app, calls, network, registry = http_native
    query = registry.original_models['PriceTarget']['fmp']['query']
    monkeypatch.setattr(query.model_fields['symbol'], 'validation_alias', AliasChoices('symbol','ticker'))
    query.model_rebuild(force=True)
    status, body = asyncio.run(request(app,'price_target','provider=fmp&ticker=msft'))
    assert status == 200, body
    assert calls == [{'symbol':'MSFT','limit':20}]
    assert asyncio.run(request(app,'price_target','provider=fmp&symbol=MSFT&ticker=MSFT'))[0] == 422
    assert len(calls) == 1 and network == []


def test_other_provider_and_nonopted_query_keep_native_behavior(http_native, monkeypatch):
    app, calls, network, registry = http_native
    status, body = asyncio.run(request(app,'price_target','provider=other&symbol=MSFT&limit=3&unknown_native=0'))
    assert status == 200, body
    query = registry.original_models['PriceTarget']['fmp']['query']
    monkeypatch.delattr(query, '__qopenbb_strict_admission__')
    # Rebuild the middleware from the now non-opted installed class.
    app.middleware_stack = None
    status, body = asyncio.run(request(app,'price_target','provider=fmp&symbol=MSFT&limit=3&unknown_native=0'))
    assert status == 200, body
    assert len(calls) == 2 and network == []


@pytest.mark.parametrize('suffix', [
    'start_date=2025-02-30', 'start_date=20250101', 'start_date=null',
    'start_date=true', 'start_date=2025-03-01&end_date=2025-02-01',
    'start_date=2023-01-01&end_date=2025-02-01',
    'start_date=2025-01-01&start_date=2025-01-01',
])
def test_http_dates_fail_before_native_extraction(http_native, suffix):
    app, calls, network, _ = http_native
    status, body = asyncio.run(request(app, 'historical_market_cap',
                                      'provider=fmp&symbol=MSFT&'+suffix))
    assert status == 422, body
    assert json.loads(body)['code'] == 'invalid_parameters'
    assert calls == [] and network == []


def test_oversized_numeric_string_is_safe_before_native_extraction(http_native):
    app, calls, network, _ = http_native
    status, body = asyncio.run(request(app, 'price_target',
                                      'provider=fmp&symbol=MSFT&limit='+'9'*5000))
    assert status == 422, body
    assert json.loads(body)['code'] == 'invalid_parameters'
    assert b'99999999' not in body
    assert calls == [] and network == []
