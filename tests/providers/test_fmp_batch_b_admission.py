"""Batch B fixture admission through generated native SDK, mounted REST and Fetcher.

Fixture query declarations are loaded without invoking archive recovery or replacing
installed modules. Real registered adapter and metadata joins remain task 4.2.
"""
import asyncio
import importlib.util
import re
from copy import deepcopy
from datetime import date, datetime
from pathlib import Path
from urllib.parse import urlencode

import pytest
import test_fmp_parameter_admission as sdk
from fastapi import APIRouter, FastAPI
from openbb_core.api.router.commands import add_command_map
from openbb_core.app.provider_interface import ProviderInterface
from openbb_core.app.route_iter import iter_api_routes
from openbb_core.app.static.utils.admission_context import InvalidParameters
from openbb_core.provider.abstract.data import Data
from pydantic import ValidationError, create_model, field_validator, model_validator
from test_financial_query_policy import request

HERE = Path(__file__).parent
MODELS = dict(zip(
    ['historical_dividends', 'historical_splits', 'calendar_earnings',
     'calendar_dividend', 'calendar_splits', 'company_news', 'company_filings',
     'earnings_call_transcript'],
    ['HistoricalDividends', 'HistoricalSplits', 'CalendarEarnings',
     'CalendarDividend', 'CalendarSplits', 'CompanyNews', 'CompanyFilings',
     'EarningsCallTranscript']))


def frozen_queries():
    result = {}
    for group in ('events', 'documents'):
        spec = importlib.util.spec_from_file_location(
            'batch_b_' + group, HERE / 'fixtures/fmp_batch_b' / group / 'freeze.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        values = ({name: module.desired_query(name) for name in module.NAMES}
                  if group == 'events' else module.queries())
        result.update(values)
    return result


def selected_query(name, query):
    @model_validator(mode='before')
    @classmethod
    def typed_identity(cls, values):
        if 'symbol' in values:
            symbol = values['symbol']
            if type(symbol) is not str or not re.fullmatch(r'[A-Za-z0-9^][A-Za-z0-9.^=-]{0,49}', symbol):
                raise ValueError('Listing must be one scalar identity')
        for key in ('start_date', 'end_date'):
            value = values.get(key)
            if value is None:
                continue
            if isinstance(value, date) and not isinstance(value, datetime):
                continue
            if not isinstance(value, str) or not re.fullmatch(r'[0-9]{4}-[0-9]{2}-[0-9]{2}', value):
                raise ValueError('Civil date required')
            date.fromisoformat(value)
        return values
    validators = {'typed_identity': typed_identity}
    for key, dec in query.__pydantic_decorators__.field_validators.items():
        fn = getattr(dec.func, '__func__', dec.func)
        validators[key] = field_validator(*dec.info.fields, mode=dec.info.mode,
                                          check_fields=False)(classmethod(fn))
    for key, dec in query.__pydantic_decorators__.model_validators.items():
        fn = getattr(dec.func, '__func__', dec.func)
        validators[key] = model_validator(mode=dec.info.mode)(
            classmethod(fn) if dec.info.mode == 'before' else fn)
    result = create_model(query.__name__, __base__=sdk.standard(name),
                          __validators__=validators, **{
        key: (info.annotation, deepcopy(info)) for key, info in query.model_fields.items()})
    result.model_config = dict(query.model_config)
    result.__qopenbb_strict_admission__ = True
    result.model_rebuild(force=True)
    return result


@pytest.fixture
def batch_b(monkeypatch):
    queries = frozen_queries()
    from annotated_types import Ge, Le, MaxLen, MinLen
    from pydantic import Strict
    for cls in (Ge, Le, MinLen, MaxLen, Strict):
        monkeypatch.setattr(sdk, cls.__name__, cls, raising=False)
    monkeypatch.setattr(sdk, 'registered_query', selected_query)
    monkeypatch.setattr(sdk, 'CONTRACTS', {name: (q, Data) for name, q in queries.items()})
    monkeypatch.setattr(sdk, 'describe', lambda: {'adapters': {
        name: {'model_key': model} for name, model in MODELS.items()}})
    methods, runner, calls = sdk.native.__wrapped__(monkeypatch)
    router = APIRouter()
    add_command_map(runner, router)
    inner = FastAPI()
    inner.include_router(router, prefix='/concrete/v7')
    routes = tuple(iter_api_routes(inner))
    registry = ProviderInterface()._registry_map
    # Only routing policy is supplied here. Financial row metadata is not being
    # certified by synthetic Data rows; complete projection is a real-join gate.
    document = {'paths': {r.path: {'get': {'x-qopenbb-financial': {
        'dataset': r.openapi_extra['model'], 'provider_policy': 'explicit',
        'providers': ['fmp', 'other']}}} for r in routes}}
    from qopenbb_data.financial_errors import install_financial_error_handlers
    from qopenbb_data.financial_policy import FinancialProviderPolicy
    install_financial_error_handlers(inner, document)
    app = FastAPI()
    app.add_middleware(FinancialProviderPolicy, document=document, registry=registry, routes=routes)
    app.mount('/', inner)
    network = []
    import aiohttp
    async def forbidden(*args, **kwargs):
        network.append(True)
        raise AssertionError('No network permitted')
    monkeypatch.setattr(aiohttp.ClientSession, '_request', forbidden)
    return methods, runner, calls, app, registry, network


def valid(name):
    if name.startswith('calendar'):
        return {'start_date': '2025-01-01', 'end_date': '2025-01-07'}
    if name == 'company_filings':
        return {'symbol': 'MSFT', 'start_date': '2025-01-01', 'end_date': '2025-01-07'}
    if name == 'earnings_call_transcript':
        return {'symbol': 'MSFT', 'year': 2025, 'quarter': 1}
    return {'symbol': 'MSFT'}


def invoke(batch, name, entry, payload):
    methods, _, _, app, registry, _ = batch
    if entry == 'sdk':
        return methods[name](provider='fmp', **payload)
    if entry == 'http':
        status, body = asyncio.run(request(app, name, urlencode(dict(payload, provider='fmp'))))
        assert status == 200, body
        return body
    fetcher = registry.registry.providers['fmp'].fetcher_dict[MODELS[name]]
    return asyncio.run(fetcher.fetch_data(payload))


@pytest.mark.parametrize('name', MODELS)
@pytest.mark.parametrize('entry', ['sdk', 'http', 'fetcher'])
def test_valid_batch_b_single_dispatch(batch_b, name, entry):
    invoke(batch_b, name, entry, valid(name))
    assert len(batch_b[2]) == 1 and batch_b[5] == []


@pytest.mark.parametrize('quarter', [1, 2, 3, 4])
@pytest.mark.parametrize('entry', ['sdk', 'http', 'fetcher'])
def test_bounded_quarter_wire_and_typed(batch_b, quarter, entry):
    invoke(batch_b, 'earnings_call_transcript', entry,
           dict(valid('earnings_call_transcript'), quarter=quarter))
    assert batch_b[2] == [{'symbol': 'MSFT', 'year': 2025, 'quarter': quarter}]




def invalid_payloads(name):
    payload = valid(name)
    bad = [dict(payload, PRIVATE_KEY_SENTINEL='PRIVATE_VALUE_SENTINEL')]
    if 'symbol' in payload:
        bad += [dict(payload, symbol=value) for value in
                (True, None, '', 'MSFT,AAPL', 'MSFT&apikey=SECRET', ['MSFT'], {'symbol': 'MSFT'})]
    else:
        bad.append(dict(payload, symbol='MSFT'))
    query = frozen_queries()[name]
    for field in ('quarter', 'year', 'page', 'limit'):
        if field in query.model_fields:
            info = query.model_json_schema()['properties'][field]
            values = [True, False, None, -1, 0.5, '1', 1.0, 'PRIVATE_VALUE_SENTINEL', {}, []]
            values += [info.get('minimum', 0)-1, info.get('maximum', 10000)+1]
            bad += [dict(payload, **{field: value}) for value in values]
        else:
            bad.append(dict(payload, **{field: 1}))
    if 'start_date' in query.model_fields:
        bad += [dict(payload, start_date='2025-02-30'),
                dict(payload, start_date='2025-02-01', end_date='2025-01-01')]
        if name.startswith('calendar'):
            bad.append(dict(payload, end_date='2025-01-08'))
    return bad


@pytest.mark.parametrize('name', MODELS)
@pytest.mark.parametrize('entry', ['sdk', 'fetcher'])
def test_typed_invalid_zero_dispatch(batch_b, name, entry):
    for payload in invalid_payloads(name):
        error = InvalidParameters if entry == 'sdk' else ValidationError
        with pytest.raises(error):
            invoke(batch_b, name, entry, payload)
    assert batch_b[2] == [] and batch_b[5] == []


@pytest.mark.parametrize('name', MODELS)
def test_wire_invalid_zero_dispatch(batch_b, name):
    app = batch_b[3]
    payload = valid(name)
    wire = [urlencode(dict(item, provider='fmp')) for item in invalid_payloads(name)
            if not ('symbol' in item and not isinstance(item['symbol'], str))
            and not any(item.get(key) == '1' for key in ('quarter', 'year', 'page', 'limit'))]
    base = urlencode(dict(payload, provider='fmp'))
    wire += [base + '&provider=fmp', base + '&' + next(iter(payload)) + '=1']
    if name == 'earnings_call_transcript':
        wire += [base.replace('quarter=1', 'quarter=' + value) for value in
                 ('null', 'true', 'false', '1.0', '1e0', '', '9'*5000)]
    for encoded in wire:
        status, body = asyncio.run(request(app, name, encoded))
        assert status == 422, (encoded, status, body)
        assert b'PRIVATE_' not in body
    assert batch_b[2] == [] and batch_b[5] == []


def test_configured_defaults_and_caller_precedence(batch_b):
    methods, runner, calls, *_ = batch_b
    runner.user_settings.defaults.commands['earnings_call_transcript'] = {
        'provider': ['fmp'], 'symbol': 'MSFT', 'year': 2025, 'quarter': 2}
    methods['earnings_call_transcript'](symbol='MSFT', quarter=4)
    assert calls[-1]['quarter'] == 4
    methods['earnings_call_transcript'](symbol='MSFT')
    assert calls[-1]['quarter'] == 2
    for value in (True, None, 0, 5):
        runner.user_settings.defaults.commands['earnings_call_transcript']['quarter'] = value
        with pytest.raises(Exception, match='invalid_parameters'):
            methods['earnings_call_transcript'](symbol='MSFT')
    assert len(calls) == 2




def test_quarter_projection_keeps_native_schema_and_other_provider(batch_b):
    from qopenbb_data.financial_http_quarter import _CANONICAL_QUARTER
    schema = sdk.standard('earnings_call_transcript').model_json_schema()
    assert schema['properties']['quarter']['anyOf'][0]['enum'] == [1, 2, 3, 4]
    app = batch_b[3]
    for quarter in (1, 2, 3, 4):
        query = urlencode(dict(valid('earnings_call_transcript'), provider='other', quarter=quarter))
        status, _ = asyncio.run(request(app, 'earnings_call_transcript', query))
        assert status == 422
        assert _CANONICAL_QUARTER.get() is False
    assert batch_b[2] == []
    batch_b[0]['earnings_call_transcript'](provider='other', **valid('earnings_call_transcript'))
    assert len(batch_b[2]) == 1
    invoke(batch_b, 'earnings_call_transcript', 'http', valid('earnings_call_transcript'))
    assert len(batch_b[2]) == 2 and _CANONICAL_QUARTER.get() is False


@pytest.mark.parametrize('name', ['historical_dividends', 'company_news'])
@pytest.mark.parametrize('entry', ['sdk', 'http', 'fetcher'])
def test_omitted_dates_and_explicit_null_are_distinct(batch_b, name, entry):
    invoke(batch_b, name, entry, valid(name))
    assert len(batch_b[2]) == 1
    if entry == 'http':
        status, _ = asyncio.run(request(batch_b[3], name,
            urlencode(dict(valid(name), provider='fmp', start_date='null'))))
        assert status == 422
    else:
        with pytest.raises(InvalidParameters if entry == 'sdk' else ValidationError):
            invoke(batch_b, name, entry, dict(valid(name), start_date=None))
    assert len(batch_b[2]) == 1 and batch_b[5] == []


@pytest.mark.parametrize('entry', ['sdk', 'http', 'fetcher'])
@pytest.mark.parametrize('name,limit', [('company_news', 50), ('company_filings', 100)])
def test_document_maximum_page_and_limit(batch_b, entry, name, limit):
    invoke(batch_b, name, entry, dict(valid(name), page=99, limit=limit))
    assert len(batch_b[2]) == 1
    assert batch_b[2][0]['page'] == 99 and batch_b[2][0]['limit'] == limit


def test_projection_idempotency_schema_and_context_cleanup(batch_b):
    from qopenbb_data.financial_http_quarter import (
        _CANONICAL_QUARTER,
        admitted_http_quarter,
        prepare_http_quarter,
    )
    inner = batch_b[3].routes[-1].app
    route = next(r for r in iter_api_routes(inner)
                 if (r.openapi_extra or {}).get('model') == 'EarningsCallTranscript')
    query = batch_b[4].original_models['EarningsCallTranscript']['fmp']['query']
    prepare_http_quarter(route, query)
    before = inner.openapi()
    def quarter_field(dependant):
        for field in dependant.query_params:
            if field.name == 'quarter':
                return field
        for child in dependant.dependencies:
            found = quarter_field(child)
            if found is not None:
                return found
    original = quarter_field(route.dependant)
    for _ in range(2):
        prepare_http_quarter(route, query)
        assert quarter_field(route.dependant) is original
    assert inner.openapi() == before
    assert original._type_adapter.json_schema()['anyOf'][0]['enum'] == [1, 2, 3, 4]
    with pytest.raises(RuntimeError), admitted_http_quarter(query):
        assert _CANONICAL_QUARTER.get() is True
        raise RuntimeError('synthetic failure')
    assert _CANONICAL_QUARTER.get() is False



@pytest.mark.parametrize('name,days', [('company_news', 31), ('company_filings', 365)])
@pytest.mark.parametrize('entry', ['sdk', 'http', 'fetcher'])
def test_inclusive_document_windows(batch_b, name, days, entry):
    from datetime import timedelta
    start = date(2025, 1, 1)
    payload = dict(valid(name), start_date=start.isoformat(),
                   end_date=(start + timedelta(days=days-1)).isoformat())
    invoke(batch_b, name, entry, payload)
    assert len(batch_b[2]) == 1
    payload['end_date'] = (start + timedelta(days=days)).isoformat()
    if entry == 'http':
        status, _ = asyncio.run(request(batch_b[3], name, urlencode(dict(payload, provider='fmp'))))
        assert status == 422
    else:
        with pytest.raises(InvalidParameters if entry == 'sdk' else ValidationError):
            invoke(batch_b, name, entry, payload)
    assert len(batch_b[2]) == 1 and batch_b[5] == []
