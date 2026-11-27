"""Installed Batch B projection preserves selected financial and saved-view contracts."""
import importlib
import json
import sys
import types
from copy import deepcopy
from pathlib import Path

import pytest
from qopenbb_ci.catalog import generate, supported_widgets
from qopenbb_ci.catalog_batch_b import validate_bindings
from qopenbb_ci.catalog_financial import resolve
from qopenbb_ci.catalog_research import research_app
from qopenbb_ci.catalog_upstream import widget_schema

ROOT = Path(__file__).resolve().parents[2]
HANDOFFS = json.loads((ROOT / 'tests/providers/fixtures/fmp_batch_b/handoffs.json').read_text())['widgets']


@pytest.fixture(scope='module')
def inputs():
    from qopenbb_data.config import configure
    configure()
    from openbb_core.api.rest_api import app
    from openbb_core.app.route_iter import iter_api_routes
    from openbb_core.provider.registry_map import RegistryMap
    from qopenbb_data.app import _annotated_models
    from qopenbb_data.financial_openapi import (
        financial_error_responses,
        project_financial_openapi,
    )
    registry = RegistryMap()
    schema = financial_error_responses(project_financial_openapi(
        app.openapi(), iter_api_routes(app), registry, required_models=_annotated_models(registry)))
    inventory = json.loads((ROOT / 'contracts/datasets.json').read_text())
    package = types.ModuleType('batch_b_upstream')
    package.__path__ = [str(ROOT / 'vendor/data-api/openbb_platform/extensions/platform_api/openbb_platform_api/utils')]
    sys.modules[package.__name__] = package
    subset = deepcopy(schema)
    subset['paths'] = {item['path']: schema['paths'][item['path']] for item in inventory['datasets']}
    raw = importlib.import_module('batch_b_upstream.widgets').build_json(widget_schema(subset), [])
    return schema, inventory, raw


def test_exact_eight_native_bindings_and_preserved_financial_contracts(inputs):
    schema, inventory, raw = inputs
    selected = deepcopy(inventory)
    selected['datasets'] = [d for d in inventory['datasets'] if d['id'] in {h['dataset_id'] for h in HANDOFFS}]
    result = generate(schema, selected, raw, [], '/data')
    records = {item['id']: item for item in inventory['datasets']}
    frozen = {item['dataset']: item for item in result['routes.json']['routes']}
    for handoff in HANDOFFS:
        dataset = records[handoff['dataset_id']]
        assert dataset['parameters'] == handoff['params']
        assert dataset['path'] == handoff['route']
        widget = result['widgets.json'][handoff['widget_id']]
        assert widget['type'] == handoff['renderer']
        assert widget['endpoint'] == handoff['route']
        assert widget['data']['dataKey'] == 'results'
        controls = {p['paramName']: p for p in widget['params']}
        expected_controls = {'provider', *handoff['controls']}
        if handoff['module'] == 'calendar_earnings':
            expected_controls.add('symbol')
            assert controls['symbol']['optional'] and controls['symbol']['value'] is None
        assert set(controls) == expected_controls
        assert controls['provider']['options'] == [{'label': 'FMP', 'value': 'fmp'}]
        assert ('symbol' in controls) == (handoff['company_selection'] or handoff['module'] == 'calendar_earnings')
        descriptor = schema['paths'][dataset['path']]['get']['x-qopenbb-financial']
        policy = descriptor['variants']['fmp']['response_policy']
        if policy['max_rows'] is not None:
            assert policy['max_rows'] == handoff['max_rows']
        assert frozen[dataset['id']]['x-qopenbb-financial'] == descriptor
        assert widget['financialContract'] == descriptor
        query = resolve(schema, descriptor['variants']['fmp']['query_schema'])
        if 'limit' in query['properties']:
            assert query['properties']['limit']['maximum'] == handoff['max_rows']
        for name in handoff['controls']:
            assert controls[name]['validationSchema'] == query['properties'][name]
        row = resolve(schema, descriptor['variants']['fmp']['row_schema'])
        assert {c['field'] for c in widget['data']['table']['columnsDefs']} == set(row['properties'])
        assert widget['data']['scope'] == ('listing' if handoff['company_selection'] else 'market')
        assert widget['refetchInterval'] is False
        assert widget['refetchOnWindowFocus'] is False
        assert widget['refetchOnReconnect'] is False


@pytest.mark.parametrize('mutation', ['missing', 'extra', 'foreign', 'wrong-id'])
def test_batch_b_mapping_fails_closed(inputs, mutation):
    schema, inventory, raw = deepcopy(inputs)
    selected = HANDOFFS[0]
    key = selected['widget_id']
    if mutation == 'missing':
        inventory['datasets'] = [d for d in inventory['datasets'] if d['id'] != selected['dataset_id']]
    elif mutation == 'extra':
        item = deepcopy(next(d for d in inventory['datasets'] if d['id'] == selected['dataset_id']))
        item['id'] = 'extra-batch-b'
        inventory['datasets'].append(item)
    elif mutation == 'foreign':
        next(d for d in inventory['datasets'] if d['id'] == selected['dataset_id'])['provider'] = 'yfinance'
    else:
        raw[key + '_fmp_obb'] = raw.pop(key)
        raw[key + '_fmp_obb']['widgetId'] = key + '_fmp_obb'
    with pytest.raises(ValueError):
        validate_bindings(inventory)
        supported_widgets(raw, inventory, '/data', schema)


def test_baseline_ids_and_company_research_saved_layout_are_stable(inputs):
    schema, inventory, raw = inputs
    baseline_inventory = deepcopy(inventory)
    ids = {h['dataset_id'] for h in HANDOFFS}
    baseline_inventory['datasets'] = [d for d in inventory['datasets'] if d['id'] not in ids]
    before, old_mapping = supported_widgets(raw, baseline_inventory, '/data', schema)
    after, new_mapping = supported_widgets(raw, inventory, '/data', schema)
    assert all(after[key] == value for key, value in before.items())
    assert research_app(baseline_inventory, old_mapping, before) == research_app(inventory, new_mapping, after)
    assert len(new_mapping) == len(old_mapping) + 8
    saved_widgets = json.loads((ROOT / 'contracts/widgets.json').read_text())
    assert set(saved_widgets) == set(after) | {"research_story", "events_documents_story"}
    assert set(after) - set(before) == {h["widget_id"] for h in HANDOFFS}
    for key, value in before.items():
        saved = deepcopy(saved_widgets[key])
        current = deepcopy(value)
        if 'table' in saved.get('data', {}):
            for descriptor in (saved, current):
                columns = descriptor['data']['table']['columnsDefs']
                descriptor['data']['table']['columnsDefs'] = {c['field']: c for c in columns}
                assert len(columns) == len(descriptor['data']['table']['columnsDefs'])
        assert saved == current
    saved_apps = json.loads((ROOT / 'contracts/apps.json').read_text())
    saved_research = next(app for app in saved_apps if app['name'] == 'Company Research')
    assert research_app(baseline_inventory, old_mapping, before)[0] == [saved_research]


@pytest.mark.parametrize('handoff', HANDOFFS, ids=lambda h: h['module'])
def test_widget_query_policy_matches_installed_admission(inputs, handoff):
    from datetime import date, timedelta

    from pydantic import ValidationError

    schema, inventory, raw = inputs
    widgets, _ = supported_widgets(raw, inventory, '/data', schema)
    widget = widgets[handoff['widget_id']]
    policy = widget['queryPolicy']
    assert policy['maxReturnedRows'] == handoff['max_rows']
    assert policy['maxRequests'] == 1
    assert policy['maxSymbols'] == int(handoff['company_selection'] or handoff['module'] == 'calendar_earnings')
    assert policy['rejectExplicitNull'] is True
    assert widget['description'] and widget['description'] != 'None'
    for param in widget['params']:
        if param['paramName'] != 'provider':
            assert param['label'] and param['description'] and param['description'] != 'None'
    module = importlib.import_module('openbb_fmp.models.' + handoff['module'])
    model = next(value for name, value in vars(module).items()
                 if name.startswith('FMP') and name.endswith('QueryParams'))
    assert model.model_json_schema() == resolve(
        schema, widget['financialContract']['variants']['fmp']['query_schema'])
    values = {key: value for key, value in handoff['params'].items() if key != 'provider'}
    model.model_validate(values)
    for key, value in ((next(iter(values)), None), ('symbol', 'AAPL,MSFT')):
        if key == 'symbol' and not policy['maxSymbols']:
            continue
        with pytest.raises(ValidationError):
            model.model_validate({**values, key: value})
    properties = policy['parameters']
    for key in ('page', 'limit', 'year', 'quarter'):
        if key in properties:
            bound = properties[key]
            for value in (bound['minimum'] - 1, bound['maximum'] + 1, True):
                with pytest.raises(ValidationError):
                    model.model_validate({**values, key: value})
    if 'page' in properties:
        assert properties['page']['default'] == 0
        assert next(p for p in widget['params'] if p['paramName'] == 'page')['value'] == 0
    window = policy['dateWindow']
    if window is not None:
        without_dates = {k: v for k, v in values.items() if k not in ('start_date', 'end_date')}
        if window['mode'] == 'required_pair':
            with pytest.raises(ValidationError):
                model.model_validate(without_dates)
        else:
            model.model_validate(without_dates)
        begin = date(2025, 1, 1)
        if window['maxInclusiveDays'] is not None:
            last = begin + timedelta(days=window['maxInclusiveDays'] - 1)
            model.model_validate({**values, 'start_date': begin.isoformat(), 'end_date': last.isoformat()})
            with pytest.raises(ValidationError):
                model.model_validate({**values, 'start_date': begin.isoformat(), 'end_date': (last + timedelta(days=1)).isoformat()})
        with pytest.raises(ValidationError):
            model.model_validate({**values, 'start_date': '2025-01-02', 'end_date': '2025-01-01'})
        for removed in ('start_date', 'end_date'):
            partial = {k: v for k, v in values.items() if k != removed}
            partial.setdefault('end_date' if removed == 'start_date' else 'start_date', '2025-01-01')
            if window['mode'] in ('required_pair', 'optional_pair'):
                with pytest.raises(ValidationError):
                    model.model_validate(partial)
            else:
                model.model_validate(partial)
