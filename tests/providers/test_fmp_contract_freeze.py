"""Contract freeze checks; SDK raw-admission gaps remain explicit blockers."""
import json
import asyncio
from pathlib import Path

import pytest
from pydantic import ValidationError
from openbb_core.provider.abstract.fetcher import Fetcher

from fmp_a1_contracts import CONTRACTS as A1
from fmp_a2_contracts import CONTRACTS as A2
from fmp_freeze_support import describe, handoffs, generated_probe

CONTRACTS = A1 | A2
FIXTURES = Path(__file__).parent / 'fixtures/fmp_batch_a/contracts'


def test_all_eleven_descriptors_match_native_sources():
    frozen = json.loads((FIXTURES / 'admission.json').read_text())
    assert frozen == describe()
    assert len(frozen['adapters']) == 11
    assert frozen['status'] == 'proposal_ready_pending_independent_review'


def test_disjoint_handoffs_match_source_inventory():
    frozen = json.loads((FIXTURES / 'handoffs.json').read_text())
    assert frozen == handoffs()
    owned = [path for item in frozen['adapters'].values() for path in item['write_paths']]
    assert len(owned) == len(set(owned))
    for item in frozen['adapters'].values():
        assert item['completion_caps'] == {'physical':400,'logical':300,'function':50}
        assert item['dispatch'] == 'blocked_until_1.4_and_2.3_accepted'


@pytest.mark.parametrize('name', CONTRACTS)
def test_direct_dictionary_rejects_extras_and_invalid_supplied_bounds(name):
    query = CONTRACTS[name][0]
    with pytest.raises(ValidationError):
        query.model_validate({'symbol':'MSFT','unsupported':False})
    for field in ('limit','page'):
        if field in query.model_fields:
            for value in (None, True, False):
                with pytest.raises(ValidationError):
                    query.model_validate({'symbol':'MSFT',field:value})


@pytest.mark.parametrize('name', ['price_target','income_statement_growth','balance_sheet_growth','cash_flow_growth'])
def test_native_emitter_proves_container_cannot_recover_raw_limit(name, monkeypatch):
    method = generated_probe(name, monkeypatch)
    omitted = method(symbol='MSFT')
    explicit_null = method(symbol='MSFT',limit=None)
    boolean = method(symbol='MSFT',limit=True)
    assert omitted == explicit_null
    assert omitted['standard_params']['limit'] is None
    assert type(boolean['standard_params']['limit']) is int
    assert boolean['standard_params']['limit'] == 1


def test_native_extra_page_retains_presence_before_container(monkeypatch):
    method = generated_probe('analyst_estimates', monkeypatch)
    assert method(symbol='MSFT')['extra_params'] == {}
    assert method(symbol='MSFT',page=True)['extra_params']['page'] is True
    assert method(symbol='MSFT',page=None)['extra_params'] == {'page':None}


@pytest.mark.parametrize('name', CONTRACTS)
def test_direct_native_fetcher_dictionary_fails_before_extraction(name):
    query, row = CONTRACTS[name]
    calls = []
    class DedicatedFetcher(Fetcher[query, list[row]]):
        @staticmethod
        def transform_query(params):
            return query.model_validate(params)
        @staticmethod
        def extract_data(query, credentials):
            calls.append(query)
            return []
        @staticmethod
        def transform_data(query, data, **kwargs):
            return data
    for payload in ({'symbol':'MSFT','unsupported':False}, {'symbol':True}):
        with pytest.raises(ValidationError):
            asyncio.run(DedicatedFetcher.fetch_data(payload))
    assert calls == []
    assert asyncio.run(DedicatedFetcher.fetch_data({'symbol':'MSFT'})) == []
    assert len(calls) == 1


def test_generated_validation_can_echo_raw_value_before_container(monkeypatch):
    method = generated_probe('price_target',monkeypatch)
    with pytest.raises(Exception, match='RAW_BOUND_SENTINEL'):
        method(symbol='MSFT',limit='RAW_BOUND_SENTINEL')


def test_amended_capture_contract_is_pending_not_runtime_acceptance():
    descriptor = json.loads((FIXTURES/'admission.json').read_text())
    mechanism = descriptor['sdk_mechanism']
    assert mechanism['route_metadata'] == 'explicit command path on validate before validate_call'
    assert mechanism['raw_binding'] == 'inspect.signature bind without apply_defaults'
    assert mechanism['provider_resolution']['ordered_choices'] == 'actual Literal descriptor order; never sort'
    assert mechanism['lifecycle']['consume'] == 'exact matching frame once before async sync_run; clear raw state'
    assert mechanism['safe_errors']['selected_only'] is True
    assert descriptor['repair_verification']['status'] == 'pending_tasks_2.1_and_2.3'
    assert len(mechanism['api_write_paths']) == 5
    amendment = Path(__file__).resolve().parents[2]/'.kiro/specs/market-data-integrations/fmp-expansion-a-admission-amendment.md'
    assert amendment.is_file()
    assert 'No final emitter exception is approved' in amendment.read_text()

def test_inventory_and_approved_design_remain_bounded():
    import hashlib
    root=Path(__file__).resolve().parents[2]
    inventory=root/'.kiro/complexity-budgets.json'
    assert len(inventory.read_text().splitlines()) <= 400
    config=json.loads(inventory.read_text())
    serialized=json.dumps(config)
    for path in describe()['sdk_mechanism']['api_write_paths']:
        assert path in serialized
    for path in handoffs()['controller_inventory_patterns_needed']:
        assert path in serialized
    assert not any(item.get('path','').endswith('method_definition.py') for item in config['exceptions'])
    design=root/'.kiro/specs/market-data-integrations/fmp-expansion-a-design.md'
    assert hashlib.sha256(design.read_bytes()).hexdigest() == '59ca002fc71585e20edfb9dc431b35605e8f2bff2d78b8d04543f7f552cb3a7a'

def test_native_activation_and_eleven_scope_join_have_separate_authority():
    mechanism=describe()['sdk_mechanism']
    assert mechanism['activation'] == {
        'provider':'fmp',
        'query':'authoritative selected original query class',
        'class_owned_marker':'__qopenbb_strict_admission__',
        'marker_value':True,
        'class_owned_extra':'forbid',
        'parallel_pair_registry':False,
        'runtime_fixture_dependency':False,
    }
    boundary=mechanism['scope_join']
    assert boundary['authority'] == 'native registry/discovery expected-set assertions; not runtime activation'
    assert boundary['model_keys'] == sorted(item['model_key'] for item in describe()['adapters'].values())
    assert boundary['gates'] == ['2.3','4.2']
    for item in describe()['adapters'].values():
        assert item['strict_opt_in']['runtime_pair_membership_required'] is False
