"""Production registration, SDK, mounted HTTP and financial discovery join offline."""
import asyncio
import json
from copy import deepcopy
from urllib.parse import urlencode

import pytest
from fmp_actual_join_support import BASELINE, EXPECTED, LATER_BATCHES, ROOT, Response, get, public_method, result_fields
from openbb_core.provider.standard_models.financial_metadata import FINANCIAL_METADATA_KEY


@pytest.fixture(scope='module')
def installed():
    from openbb_core.api.rest_api import app
    from openbb_core.app.command_runner import CommandRunner
    from openbb_core.app.route_iter import iter_api_routes
    from openbb_core.app.router import CommandMap, RouterLoader
    from openbb_core.provider.registry_map import RegistryMap
    registry = RegistryMap()
    routes = {r.openapi_extra['model']: r for r in iter_api_routes(app)
              if (getattr(r, 'openapi_extra', None) or {}).get('model') in EXPECTED | BASELINE}
    assert set(routes) == set(EXPECTED | BASELINE)
    assert set(registry.registry.providers['fmp'].fetcher_dict) == set(EXPECTED | BASELINE) | LATER_BATCHES
    runner = CommandRunner(CommandMap(RouterLoader.from_extensions()))
    runner.user_settings.credentials.fmp_api_key = 'offline-join-canary'
    methods = {key: public_method(runner, routes[key].path.removeprefix('/api/v1')) for key in EXPECTED}
    return registry, routes, runner, methods


@pytest.fixture(scope='module')
def runtime(installed):
    monkeypatch = pytest.MonkeyPatch()
    import qopenbb_data.app as application
    import qopenbb_data.config as configuration
    monkeypatch.setattr(application, 'CATALOG', ROOT / 'contracts')
    monkeypatch.setattr(configuration, 'COVERAGE', ROOT / 'docs/reference/provider-coverage.json')
    for key, value in {'FMP_API_KEY': 'offline-join-canary', 'FRED_API_KEY': 'offline-fred',
                       'OPENBB_API_AUTH': 'false', 'QOPENBB_DATA_SOURCE_REVISION': '0' * 40,
                       'QOPENBB_DATA_GENERATION_REVISION': '1' * 40}.items():
        monkeypatch.setenv(key, value)
    yield application.create_app()
    monkeypatch.undo()


@pytest.fixture
def transport(monkeypatch):
    state = {'payload': [], 'status': 200, 'calls': []}
    async def request(url, **kwargs):
        state['calls'].append(url)
        return await kwargs['response_callback'](Response(deepcopy(state['payload']), state['status']), None)
    monkeypatch.setattr('openbb_core.provider.utils.helpers.amake_request', request)
    return state


def metadata(body):
    return body['extra']['results_metadata'][FINANCIAL_METADATA_KEY]


def stable(meta):
    result = deepcopy(meta)
    result.pop('retrieved_at')
    return result


@pytest.mark.parametrize('key', EXPECTED)
def test_actual_empty_array_is_successful_native_json(installed, runtime, transport, key):
    registry, routes, _, methods = installed
    sdk = json.loads(methods[key](symbol=' msft ', provider='fmp').model_dump_json(by_alias=False))
    status, http = asyncio.run(get(runtime, routes[key].path, b'symbol=+msft+&provider=fmp'))
    assert status == 200, http
    assert sdk['results'] == http['results'] == []
    assert sdk['provider'] == http['provider'] == 'fmp'
    sm, hm = metadata(sdk), metadata(http)
    assert stable(sm) == stable(hm)
    assert sm['dataset'] == 'equity/' + EXPECTED[key][1] and sm['provider'] == 'fmp'
    assert sm['bounds']['returned_count'] == 0
    assert sm['effective_query']['symbol'] == 'MSFT'
    if key != 'HistoricalMarketCap':
        query = registry.original_models[key]['fmp']['query']
        assert sm['effective_query'] == query.model_validate({'symbol': 'MSFT'}).model_dump(mode='json')
    else:
        from datetime import date
        effective = sm['effective_query']
        assert (date.fromisoformat(effective['end_date']) - date.fromisoformat(effective['start_date'])).days == 365
    assert set(sm['fields']) == set(registry.original_models[key]['fmp']['data'].model_fields)
    assert len(transport['calls']) == 2
    assert transport['calls'][0] == transport['calls'][1]


@pytest.mark.parametrize('key', EXPECTED)
def test_actual_defaults_aliases_and_explicit_bounds(installed, runtime, transport, key):
    registry, routes, runner, methods = installed
    query = registry.original_models[key]['fmp']['query']
    params = {'symbol': ' msft '}
    params.update({k: v for k, v in {'period': 'quarterly', 'limit': 7, 'page': 2,
                                  'start_date': '2025-01-01', 'end_date': '2025-02-01'}.items()
                   if k in query.model_fields})
    expected = query.model_validate(params).model_dump(mode='json')
    sdk = json.loads(methods[key](provider='fmp', **params).model_dump_json(by_alias=False))
    status, http = asyncio.run(get(runtime, routes[key].path, urlencode(dict(params, provider='fmp')).encode()))
    assert status == 200, http
    assert metadata(sdk)['effective_query'] == metadata(http)['effective_query'] == expected
    assert len(transport['calls']) == 2
    assert transport['calls'][0] == transport['calls'][1]


@pytest.mark.parametrize('key', EXPECTED)
def test_actual_raw_invalid_before_transport_and_safe_provider_failure(installed, runtime, transport, key):
    registry, routes, _, methods = installed
    fetcher = registry.registry.providers['fmp'].fetcher_dict[key]
    for params in ({'symbol': True}, {'symbol': 'MSFT', 'unknown': None}):
        with pytest.raises(Exception, match='invalid_parameters'):
            methods[key](provider='fmp', **params)
        from openbb_core.provider.utils.financial_errors import FinancialError
        with pytest.raises(FinancialError) as error:
            asyncio.run(fetcher.fetch_data(params, {'fmp_api_key': 'offline-join-canary'}))
        assert error.value.code == 'invalid_parameters'
    for query in (b'symbol=MSFT&symbol=AAPL&provider=fmp', b'symbol=MSFT&provider=fmp&unknown='):
        status, body = asyncio.run(get(runtime, routes[key].path, query))
        assert status == 422 and body['code'] == 'invalid_parameters'
    assert transport['calls'] == []
    transport.update(status=401, payload={'Error Message': 'offline-join-canary private upstream'})
    status, body = asyncio.run(get(runtime, routes[key].path, b'symbol=MSFT&provider=fmp'))
    assert status == 502 and body['code'] == 'authentication'
    assert 'offline-join-canary' not in json.dumps(body) and 'private upstream' not in json.dumps(body)
    assert len(transport['calls']) == 1


@pytest.mark.parametrize('key', EXPECTED)
def test_actual_invalid_bounds_and_configured_defaults(installed, runtime, transport, key):
    registry, routes, runner, methods = installed
    query = registry.original_models[key]['fmp']['query']
    bad = [{'symbol': 'A,B'}]
    for name in ('limit', 'page'):
        if name in query.model_fields:
            bad.extend({'symbol': 'MSFT', name: value} for value in (True, None, -1, 101))
    if 'period' in query.model_fields:
        bad.append({'symbol': 'MSFT', 'period': 'ttm'})
    if 'start_date' in query.model_fields:
        bad.append({'symbol': 'MSFT', 'start_date': '2025-02-01', 'end_date': '2025-01-01'})
    fetcher = registry.registry.providers['fmp'].fetcher_dict[key]
    from openbb_core.provider.utils.financial_errors import FinancialError
    for params in bad:
        with pytest.raises(Exception, match='invalid_parameters'):
            methods[key](provider='fmp', **params)
        with pytest.raises(FinancialError) as error:
            asyncio.run(fetcher.fetch_data(params))
        assert error.value.code == 'invalid_parameters'
        # HTTP has textual scalars; null/boolean values are sent literally.
        status, body = asyncio.run(get(runtime, routes[key].path, urlencode(dict(params, provider='fmp')).encode()))
        assert status == 422 and body['code'] == 'invalid_parameters'
    assert transport['calls'] == []
    command = routes[key].path.removeprefix('/api/v1/').replace('/', '.')
    original = deepcopy(runner.user_settings.defaults.commands)
    runner.user_settings.defaults.commands[command] = {'provider': ['fmp'], 'symbol': 'MSFT'}
    try:
        supplied = {'symbol': ' aapl '}
        if 'period' in query.model_fields:
            runner.user_settings.defaults.commands[command]['period'] = 'quarterly'
        sdk = json.loads(methods[key](**supplied).model_dump_json(by_alias=False))
        assert metadata(sdk)['effective_query']['symbol'] == 'AAPL'
        if 'period' in query.model_fields:
            assert metadata(sdk)['effective_query']['period'] == 'quarter'
        assert supplied == {'symbol': ' aapl '}
        assert len(transport['calls']) == 1
    finally:
        runner.user_settings.defaults.commands = original


@pytest.mark.parametrize('key', [key for key in EXPECTED if key in {
    'AnalystEstimates', 'PriceTarget', 'IncomeStatementGrowth',
    'BalanceSheetGrowth', 'CashFlowStatementGrowth'}])
def test_actual_row_limit_clips_with_consistent_partial_metadata(installed, runtime, transport, key):
    registry, routes, _, methods = installed
    row = deepcopy(ROWS[key][0])
    if key == 'BalanceSheetGrowth':
        frozen = json.loads((ROOT / 'tests/providers/fixtures/fmp_batch_a/contracts/balance_sheet_growth.json').read_text())
        required = {frozen['effective_aliases'].get(name, item['generated_schema_alias']): None
                    for name, item in frozen['accepted_validation_aliases'].items()
                    if name.startswith('growth_') and frozen['field_presence'][name]['required']}
        row = {**required, **row}
    transport['payload'] = [row, deepcopy(row)]
    sdk = json.loads(methods[key](symbol='MSFT', provider='fmp', limit=1).model_dump_json(by_alias=False))
    status, http = asyncio.run(get(runtime, routes[key].path, b'symbol=MSFT&provider=fmp&limit=1'))
    assert status == 200 and len(sdk['results']) == len(http['results']) == 1
    assert stable(metadata(sdk)) == stable(metadata(http))
    bounds = metadata(http)['bounds']
    assert bounds['truncated'] is True and bounds['completeness'] == 'partial'
    assert bounds['returned_count'] == 1
    assert len(transport['calls']) == 2


ROWS = {
    'AnalystEstimates': ({'symbol': 'MSFT', 'date': '2025-12-31', 'revenueAvg': 0}, 'estimated_revenue_avg', 0),
    'PriceTarget': ({'symbol': 'MSFT', 'publishedDate': '2025-01-02T12:30:00Z', 'priceTarget': 0}, 'price_target', 0),
    'PriceTargetConsensus': ({'symbol': 'MSFT', 'targetHigh': 12, 'targetLow': 0, 'targetConsensus': 7}, 'target_consensus', 7),
    'RevenueBusinessLine': ({'date': '2025-12-31', 'fiscalYear': 2025, 'period': 'FY', 'data': {'Exact label ': 0}}, 'revenue', 0),
    'RevenueGeographic': ({'date': '2025-12-31', 'fiscalYear': 2025, 'period': 'FY', 'data': {'Exact label ': 0}}, 'revenue', 0),
    'HistoricalMarketCap': ({'symbol': 'MSFT', 'date': '2025-01-02', 'marketCap': 0}, 'market_cap', 0),
    'ShareStatistics': ({'symbol': 'MSFT', 'freeFloat': 25, 'floatShares': 0}, 'free_float', .25),
    'EquityQuote': ({'symbol': 'MSFT', 'price': 0, 'timestamp': 0}, 'last_price', 0),
    'IncomeStatementGrowth': ({'symbol': 'MSFT', 'date': '2025-12-31', 'growthRevenue': -.125}, 'growth_revenue', -.125),
    'BalanceSheetGrowth': ({'symbol': 'MSFT', 'date': '2025-12-31', 'growthTotalAssets': -.125}, 'growth_total_assets', -.125),
    'CashFlowStatementGrowth': ({'symbol': 'MSFT', 'date': '2025-12-31', 'growthNetIncome': -.125}, 'growth_net_income', -.125),
}


@pytest.mark.parametrize('key', EXPECTED)
def test_actual_financial_values_and_runtime_fields_match_sdk_http(installed, runtime, transport, key):
    registry, routes, _, methods = installed
    row, field, value = ROWS[key]
    if key == 'BalanceSheetGrowth':
        frozen = json.loads((ROOT / 'tests/providers/fixtures/fmp_batch_a/contracts/balance_sheet_growth.json').read_text())
        required = {frozen['effective_aliases'].get(name, item['generated_schema_alias']): None
                    for name, item in frozen['accepted_validation_aliases'].items()
                    if name.startswith('growth_') and frozen['field_presence'][name]['required']}
        row = {**required, **row}
    transport['payload'] = [row]
    params = {'symbol': 'MSFT'}
    if key == 'HistoricalMarketCap':
        params.update(start_date='2025-01-01', end_date='2025-02-01')
    sdk = json.loads(methods[key](provider='fmp', **params).model_dump_json(by_alias=False))
    status, http = asyncio.run(get(runtime, routes[key].path, urlencode(dict(params, provider='fmp')).encode()))
    assert status == 200, http
    # HTTP omits nulls; source validators must not run twice on transformed ratios/epochs.
    model = registry.original_models[key]['fmp']['data']
    public_rows = [{name: value for name, value in row.items() if value is not None} for row in sdk['results']]
    http_rows = [{name: value for name, value in row.items() if value is not None} for row in http['results']]
    assert public_rows == http_rows and len(http['results']) == 1
    assert all(sdk['results'][0][name] is None for name in set(model.model_fields) - set(http['results'][0]))
    assert http['results'][0][field] == value
    assert set(sdk['results'][0]) == set(model.model_fields)
    assert stable(metadata(sdk)) == stable(metadata(http))
    assert metadata(http)['fields'][field]['availability'] == 'available'
    assert metadata(http)['bounds']['returned_count'] == 1
    assert len(transport['calls']) == 2


def assert_expected_annotations(registry):
    from openbb_core.provider.standard_models.financial_annotations import bind_data_annotation, bind_query_annotation
    assert set(EXPECTED).issubset(registry.original_models)
    for key in EXPECTED:
        models = registry.original_models[key]['fmp']
        assert bind_query_annotation(models['query']) is not None
        assert bind_data_annotation(models['data']) is not None


def test_actual_projection_catalog_native_widget_and_baseline_contracts(installed, runtime, transport):
    from qopenbb_ci.catalog_upstream import widget_schema
    from openbb_core.provider.standard_models.financial_annotations import bind_data_annotation
    registry, routes, _, _ = installed
    # Check the fixed required set before deriving anything from annotations.
    assert len(EXPECTED) == 11
    assert_expected_annotations(registry)
    document = runtime.openapi()
    status, catalog = asyncio.run(get(runtime, '/datasets.json'))
    assert status == 200
    discovered = {item['dataset']: item for item in catalog['datasets']}
    assert set(EXPECTED).issubset(discovered)
    widgets = widget_schema(document)
    for key, (name, suffix) in EXPECTED.items():
        path = routes[key].path
        assert path == '/api/v1/equity/' + suffix
        operation = document['paths'][path]['get']
        descriptor = operation['x-qopenbb-financial']
        assert descriptor['dataset'] == key and descriptor['provider_policy'] == 'explicit'
        assert discovered[key]['variants'] == descriptor['variants']
        assert discovered[key]['command']['path'] == path
        assert discovered[key]['coverage']['fmp']['installed']['status'] == 'verified'
        models = registry.original_models[key]['fmp']
        frozen = json.loads((ROOT / 'tests/providers/fixtures/fmp_batch_a/contracts' / (name + '.json')).read_text())
        for kind in ('query', 'data'):
            for mode in ('validation', 'serialization'):
                assert models[kind].model_json_schema(mode=mode) == frozen[kind][mode]
        fields = set(models['data'].model_fields)
        assert set(descriptor['variants']['fmp']['fields']) == fields
        assert set(bind_data_annotation(models['data']).fields) == fields
        schema = operation['responses']['200']['content']['application/json']['schema']
        assert list(result_fields(document, schema)) == [fields]
        widget = widgets['paths'][path]['get']
        assert widget['widget_config']['data']['dataKey'] == 'results'
        assert list(result_fields(widgets, widget['responses']['200']['content']['application/json']['schema'])) == [fields]
    for key, suffix in BASELINE.items():
        assert routes[key].path == '/api/v1/equity/' + suffix
        assert key in discovered and 'fmp' in registry.original_models[key]
    assert transport['calls'] == []


@pytest.mark.parametrize('key', EXPECTED)
@pytest.mark.parametrize('mutation', ['missing_both', 'invalid_query', 'invalid_data'])
def test_missing_or_invalid_actual_annotation_cannot_silently_drop_endpoint(installed, monkeypatch, key, mutation):
    from openbb_core.api.rest_api import app
    from openbb_core.app.route_iter import iter_api_routes
    from qopenbb_data.financial_openapi import project_financial_openapi
    registry = installed[0]
    models = registry.original_models[key]['fmp']
    if mutation == 'missing_both':
        monkeypatch.setattr(models['query'], 'financial_query_annotation', None)
        monkeypatch.setattr(models['data'], 'financial_data_annotation', None)
    else:
        kind = mutation.removeprefix('invalid_')
        monkeypatch.setattr(models[kind], 'financial_' + kind + '_annotation', {'invalid': True})
    with pytest.raises(ValueError):
        assert_expected_annotations(registry)
    with pytest.raises(ValueError):
        project_financial_openapi(app.openapi(), iter_api_routes(app), registry, required_models=set(EXPECTED))
