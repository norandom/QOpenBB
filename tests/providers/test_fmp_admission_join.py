"""Prerequisite composition proof; production registration is verified at the final join."""
import asyncio
import json
from copy import deepcopy
from pathlib import Path
from urllib.parse import urlencode

import pytest
from fmp_freeze_support import CONTRACTS
from openbb_core.app.parameter_admission import opted_in
from pydantic import ValidationError

# Import native HTTP commands before the patched registry can populate its cache.
from test_financial_query_policy import http_native as http_native  # noqa: PLC0414
from test_financial_query_policy import request
from test_fmp_parameter_admission import native as native  # noqa: PLC0414

EXPECTED = {
    'analyst_estimates': 'AnalystEstimates',
    'price_target': 'PriceTarget',
    'price_target_consensus': 'PriceTargetConsensus',
    'revenue_business_line': 'RevenueBusinessLine',
    'revenue_geographic': 'RevenueGeographic',
    'historical_market_cap': 'HistoricalMarketCap',
    'share_statistics': 'ShareStatistics',
    'equity_quote': 'EquityQuote',
    'income_statement_growth': 'IncomeStatementGrowth',
    'balance_sheet_growth': 'BalanceSheetGrowth',
    'cash_flow_growth': 'CashFlowStatementGrowth',
}
FROZEN = Path(__file__).parent / 'fixtures/fmp_batch_a/contracts'


def test_native_registered_scope_and_schemas_are_exactly_the_frozen_eleven(http_native, native):
    _, _, _, registry = http_native
    methods, runner, _ = native
    assert set(CONTRACTS) == set(methods) == set(EXPECTED)
    routes = {'/' + name: model for name, model in EXPECTED.items()}
    assert runner.command_map.commands_model == dict(routes, **{'/controlled': 'PriceTarget'})
    selected = {
        model for model, providers in registry.original_models.items()
        if opted_in(providers['fmp']['query'], 'fmp')
    }
    assert selected == set(EXPECTED.values())
    for name, model in EXPECTED.items():
        query = registry.original_models[model]['fmp']['query']
        row = registry.original_models[model]['fmp']['data']
        frozen = json.loads((FROZEN / f'{name}.json').read_text())
        assert frozen['model_key'] == model
        assert vars(query)['__qopenbb_strict_admission__'] is True
        assert vars(query)['model_config']['extra'] == 'forbid'
        assert not opted_in(query, 'other')
        assert registry.registry.providers['fmp'].fetcher_dict[model].query_params_type is query
        for mode in ('validation', 'serialization'):
            assert query.model_json_schema(mode=mode) == frozen['query'][mode]
            assert row.model_json_schema(mode=mode) == frozen['data'][mode]


@pytest.mark.parametrize('name', EXPECTED)
def test_same_effective_query_reaches_sdk_http_and_raw_fetcher(http_native, native, name):
    app, calls, network, registry = http_native
    methods, runner, _ = native
    runner.user_settings.defaults.commands[name] = {'provider': ['fmp']}
    query = registry.original_models[EXPECTED[name]]['fmp']['query']
    fetcher = registry.registry.providers['fmp'].fetcher_dict[EXPECTED[name]]
    supplied = {'symbol': ' msft '}
    supplied.update({key: value for key, value in {
        'limit': 7, 'page': 2, 'period': 'quarterly',
        'start_date': '2025-01-01', 'end_date': '2025-02-01',
    }.items() if key in query.model_fields})
    for payload in ({'symbol': 'MSFT'}, supplied):
        original = deepcopy(payload)
        expected = query.model_validate(payload).model_dump(mode='json')
        before = len(calls)
        methods[name](**payload)  # SDK retains native omitted-provider selection.
        status, body = asyncio.run(request(app, name, urlencode(dict(payload, provider='fmp'))))
        assert status == 200, body
        assert asyncio.run(fetcher.fetch_data(payload)) == []
        assert calls[before:] == [expected, expected, expected]
        assert payload == original
    assert network == []


@pytest.mark.parametrize('name', EXPECTED)
def test_unsupported_native_defaults_fail_at_all_three_entries(http_native, native, name):
    app, calls, network, registry = http_native
    methods, _, _ = native
    query = registry.original_models[EXPECTED[name]]['fmp']['query']
    fetcher = registry.registry.providers['fmp'].fetcher_dict[EXPECTED[name]]
    # Native standards expose fields omitted by the stricter endpoint contract.
    unsupported = next((key for key in ('limit', 'page') if key not in query.model_fields), 'chart_params')
    payload = {'symbol': 'MSFT', unsupported: 0 if unsupported == 'page' else None}
    original = deepcopy(payload)
    with pytest.raises(Exception, match='^invalid_parameters$') as error:
        methods[name](provider='fmp', **payload)
    assert error.value.__cause__ is None
    status, body = asyncio.run(request(app, name, urlencode(dict(payload, provider='fmp'))))
    assert status == 422 and json.loads(body)['code'] == 'invalid_parameters'
    with pytest.raises(ValidationError):
        asyncio.run(fetcher.fetch_data(payload))
    assert payload == original
    assert calls == [] and network == []


def test_baseline_selected_baseline_sequence_preserves_native_results(http_native, native):
    app, calls, network, registry = http_native
    methods, _, _ = native
    method = methods['price_target']
    fetcher = registry.registry.providers['other'].fetcher_dict['PriceTarget']
    payload = {'symbol': 'MSFT', 'limit': 3}
    expected = {'symbol': 'MSFT', 'limit': 3}
    for _ in range(2):
        before = len(calls)
        method(provider='other', **payload)
        status, body = asyncio.run(request(app, 'price_target', urlencode(dict(payload, provider='other'))))
        assert status == 200, body
        assert asyncio.run(fetcher.fetch_data(payload)) == []
        assert calls[before:] == [expected, expected, expected]
        with pytest.raises(Exception, match='^invalid_parameters$'):
            method(symbol='MSFT', provider='fmp', limit=True)
        assert len(calls) == before + 3
    assert payload == expected and network == []
