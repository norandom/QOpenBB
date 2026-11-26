"""Final installed snapshots bind all eight events/documents to frozen native contracts."""
import hashlib
import json
from copy import deepcopy
from pathlib import Path

import pytest
from qopenbb_ci.catalog_batch_b import controls
from qopenbb_ci.catalog_financial import resolve

ROOT = Path(__file__).resolve().parents[2]
FIXTURES = ROOT / 'tests/providers/fixtures/fmp_batch_b'
HANDOFFS = json.loads((FIXTURES / 'handoffs.json').read_text())['widgets']


def read(name):
    return json.loads((ROOT / 'contracts' / name).read_text())


@pytest.mark.parametrize('handoff', HANDOFFS, ids=lambda item: item['module'])
def test_complete_snapshot_matches_frozen_query_rows_and_mapping(handoff):
    schema = read('openapi.json')
    contract = json.loads((ROOT / handoff['fixture']).read_text())
    operation = schema['paths'][handoff['route']]['get']
    descriptor = operation['x-qopenbb-financial']
    variant = descriptor['variants']['fmp']
    assert set(descriptor['variants']) == {'fmp'}
    query = resolve(schema, variant['query_schema'])
    row = resolve(schema, variant['row_schema'])
    assert set(query['properties']) == set(handoff['controls'])
    assert set(row['properties']) == set(variant['fields'])
    if 'expected' in contract:
        assert query == contract['expected']['query_validation']
        assert set(row['properties']) == set(contract['expected']['row_validation']['properties'])
    route, = [r for r in read('routes.json')['routes'] if r['dataset'] == handoff['dataset_id']]
    assert route['path'] == handoff['route']
    for key in ('operationId', 'parameters', 'responses', 'x-qopenbb-financial'):
        assert route[key] == operation[key]
    mapping, = [m for m in read('catalog-report.json')['mapping'] if m['dataset'] == handoff['dataset_id']]
    assert mapping['path'] == handoff['route']
    assert mapping['widget'] == handoff['widget_id']
    assert mapping['provider'] == 'fmp'
    widget = read('widgets.json')[handoff['widget_id']]
    assert widget['type'] == handoff['renderer']
    assert widget['financialContract'] == descriptor
    assert widget['queryPolicy']['parameters'] == query['properties']
    assert widget['queryPolicy']['required'] == query.get('required', [])
    assert widget['queryPolicy']['maxRequests'] == 1
    assert widget['queryPolicy']['maxReturnedRows'] == handoff['max_rows']


def test_complete_snapshot_hashes_and_installed_identity():
    hashes = read('hashes.json')
    assert set(hashes) == {'openapi.json', 'routes.json', 'widgets.json', 'datasets.json',
                           'apps.json', 'catalog-report.json', 'compatibility.json', 'provenance.json'}
    for name, expected in hashes.items():
        assert hashlib.sha256((ROOT / 'contracts' / name).read_bytes()).hexdigest() == expected
    provenance = read('provenance.json')
    lock = json.loads((ROOT / 'sources.lock.json').read_text())
    publication = json.loads((ROOT / 'artifacts/reviewed/fmp-expansion-b/publication-verification.json').read_text())
    assert provenance['image'] == publication['images']['data-api']['manifest_digest']
    assert provenance['revision'] == lock['data_api']['revision']
    for source, revision in publication['sources'].items():
        assert provenance['image_labels'][f'org.qopenbb.source.{source}'] == revision
    assert provenance['repeat_identical'] is True


@pytest.mark.parametrize('handoff', HANDOFFS, ids=lambda item: item['module'])
def test_selected_controls_keep_order_after_canonical_schema_roundtrip(handoff):
    widget = read('widgets.json')[handoff['widget_id']]
    schema = read('openapi.json')
    query = resolve(schema, widget['financialContract']['variants']['fmp']['query_schema'])
    ordered = controls(widget, query, handoff['params'], widget['queryPolicy'])
    assert ordered == widget['params']
    assert controls(widget, json.loads(json.dumps(query, sort_keys=True)),
                    handoff['params'], widget['queryPolicy']) == ordered


@pytest.mark.parametrize('mutation', ['missing', 'duplicate'])
def test_selected_controls_reject_missing_or_duplicate_native_names(mutation):
    handoff = HANDOFFS[0]
    widget = deepcopy(read('widgets.json')[handoff['widget_id']])
    query = resolve(read('openapi.json'), widget['financialContract']['variants']['fmp']['query_schema'])
    if mutation == 'missing':
        widget['params'] = [p for p in widget['params'] if p['paramName'] != 'symbol']
    else:
        widget['params'].append(deepcopy(widget['params'][1]))
    with pytest.raises(ValueError, match='native Batch B query control'):
        controls(widget, query, handoff['params'], widget['queryPolicy'])
