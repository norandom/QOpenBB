"""Frozen A1 contracts exercise native models without registering providers."""
import json
from pathlib import Path

import pytest
from pydantic import ValidationError
from openbb_core.provider.standard_models.financial_annotations import (
    bind_data_annotation, bind_query_annotation, render_field_templates,
)
from fmp_a1_contracts import CONTRACTS, RETAINED_ESTIMATE_ALIASES

FIXTURES = Path(__file__).parent / 'fixtures/fmp_batch_a/contracts'

@pytest.mark.parametrize('name', CONTRACTS)
def test_frozen_native_schemas_and_complete_annotations(name):
    query, row = CONTRACTS[name]
    frozen = json.loads((FIXTURES / f'{name}.json').read_text())
    for mode in ('validation', 'serialization'):
        assert query.model_json_schema(mode=mode) == frozen['query'][mode]
        assert row.model_json_schema(mode=mode) == frozen['data'][mode]
    assert set(render_field_templates(row)) == set(row.model_fields)
    assert bind_data_annotation(row).model_dump(mode='json') == frozen['data_annotation']
    assert bind_query_annotation(query).model_dump(mode='json') == frozen['query_annotation']
    assert query(symbol=' msft ').symbol == 'MSFT'

@pytest.mark.parametrize('name', CONTRACTS)
@pytest.mark.parametrize('symbol', ['', 'A,B', 'A&apikey=x', True, None, 'A'*51, 'A\n'])
def test_single_symbol_admission(name, symbol):
    with pytest.raises(ValidationError):
        CONTRACTS[name][0](symbol=symbol)

@pytest.mark.parametrize('name', CONTRACTS)
def test_strict_extra_admission(name):
    with pytest.raises(ValidationError):
        CONTRACTS[name][0](symbol='MSFT', unsupported=False)

@pytest.mark.parametrize('name', ['analyst_estimates', 'price_target'])
@pytest.mark.parametrize('value', [None, True, False, 0, 101])
def test_limit_bounds_and_presence(name, value):
    with pytest.raises(ValidationError):
        CONTRACTS[name][0](symbol='MSFT', limit=value)

@pytest.mark.parametrize('value', [None, True, -1, 11])
def test_estimate_page_bounds(value):
    with pytest.raises(ValidationError):
        CONTRACTS['analyst_estimates'][0](symbol='MSFT', page=value)

@pytest.mark.parametrize('name', ['analyst_estimates', 'revenue_business_line', 'revenue_geographic'])
def test_period_alias_and_restricted_choices(name):
    query = CONTRACTS[name][0]
    assert query(symbol='MSFT', period='quarterly').period == 'quarter'
    for period in ['ttm', 'FY', 'YTD', None]:
        with pytest.raises(ValidationError):
            query(symbol='MSFT', period=period)

@pytest.mark.parametrize('name, required', [('analyst_estimates','date'), ('price_target','published_date'), ('revenue_business_line','period_ending'), ('revenue_geographic','period_ending')])
def test_required_dates_never_fabricated(name, required):
    row = CONTRACTS[name][1]
    for value in [None, 'not-a-date']:
        with pytest.raises(ValidationError):
            row.model_validate({'symbol':'MSFT', required:value, 'revenue':0})

def test_aliases_zero_null_and_currency_unknown():
    estimate = CONTRACTS['analyst_estimates'][1].model_validate({'symbol':'MSFT','date':'2030-06-30','epsLow':0,'epsHigh':None,'numAnalystsEps':0})
    assert estimate.estimated_eps_low == 0
    assert estimate.estimated_eps_high is None
    assert estimate.number_analysts_estimated_eps == 0
    assert 'currency' not in type(estimate).model_fields
    consensus = CONTRACTS['price_target_consensus'][1].model_validate({'symbol':'MSFT','targetHigh':0,'targetLow':None})
    assert consensus.target_high == 0 and consensus.target_low is None
    assert not any('date' in name for name in type(consensus).model_fields)

@pytest.mark.parametrize('name,label', [('revenue_business_line','business_line'),('revenue_geographic','region')])
def test_segment_retained_nullable_filing_and_required_revenue(name, label):
    row = CONTRACTS[name][1]
    value = row.model_validate({'period_ending':'2025-06-30',label:' Exact label ','revenue':0})
    assert getattr(value,label) == ' Exact label '
    assert value.revenue == 0 and value.filing_date is None
    with pytest.raises(ValidationError):
        row.model_validate({'period_ending':'2025-06-30','revenue':None})

@pytest.mark.parametrize('name', CONTRACTS)
def test_retained_source_union_aliases_and_source_hash(name):
    import ast
    import hashlib
    import tarfile
    from importlib import import_module
    manifest = json.loads((FIXTURES.parent / 'source_manifest.json').read_text())
    member = next(item for item in manifest['members'] if item['member'].endswith(f'/{name}.py'))
    with tarfile.open(manifest['archive']['path']) as archive:
        source = archive.extractfile(member['member']).read()
    assert hashlib.sha256(source).hexdigest() == member['sha256']
    declaration = next(node for node in ast.parse(source).body if isinstance(node, ast.ClassDef) and node.name.endswith('Data'))
    additions = {node.target.id for node in declaration.body if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name)}
    aliases = next((ast.literal_eval(node.value) for node in declaration.body if isinstance(node, ast.Assign) and any(isinstance(target, ast.Name) and target.id == '__alias_dict__' for target in node.targets)), {})
    standard = getattr(import_module(f'openbb_core.provider.standard_models.{name}'), declaration.bases[0].id)
    row = CONTRACTS[name][1]
    assert set(row.model_fields) == set(standard.model_fields) | additions
    assert (RETAINED_ESTIMATE_ALIASES if name == 'analyst_estimates' else row.__alias_dict__) == aliases


def test_independent_financial_family_meaning():
    estimates = render_field_templates(CONTRACTS['analyst_estimates'][1])
    for name, field in estimates.items():
        assert field.currency is None and field.currency_field is None
        assert field.publication_date_field is None
        assert field.valuation_date_field is None
        assert field.observation_date_field is None
        assert 'forecast fiscal period' in field.financial_basis['forecast_period']
        if name.startswith('estimated_'):
            assert field.value_origin == 'estimate'
            assert field.unit == ('currency/share' if 'eps' in name else 'currency')
            assert field.scale == 1
        if name.startswith('number_'):
            assert field.unit == 'count' and field.scale == 1
    targets = render_field_templates(CONTRACTS['price_target'][1])
    for name in ['price_target','adj_price_target','price_target_previous','previous_adj_price_target','price_when_posted']:
        assert targets[name].unit == 'currency/share'
        assert targets[name].currency_field == 'currency'
        assert targets[name].value_origin == ('provider_observation' if name == 'price_when_posted' else 'estimate')
        assert targets[name].publication_date_field == 'published_date'
    consensus = render_field_templates(CONTRACTS['price_target_consensus'][1])
    for name in ['target_high','target_low','target_median','target_consensus']:
        assert consensus[name].unit == 'currency/share'
        assert consensus[name].scale == 1 and consensus[name].value_origin == 'estimate'
        assert consensus[name].currency is None and consensus[name].currency_field is None
        assert consensus[name].publication_date_field is None
        assert consensus[name].valuation_date_field is None
    for dataset in ['revenue_business_line','revenue_geographic']:
        fields = render_field_templates(CONTRACTS[dataset][1])
        assert fields['revenue'].unit == 'currency' and fields['revenue'].scale == 1
        assert fields['revenue'].value_origin == 'provider_observation'
        assert fields['revenue'].currency is None and fields['revenue'].currency_field is None
        assert fields['revenue'].observation_date_field == 'period_ending'
        assert fields['revenue'].publication_date_field == 'filing_date'
        assert 'year-to-date duration unknown' in fields['revenue'].period_basis


def test_target_publication_precision_and_attribution_aliases():
    row = CONTRACTS['price_target'][1].model_validate({
        'symbol':'MSFT','publishedDate':'2025-06-30T15:20:31+02:00',
        'publishedTime':'15:20:31+02:00','analystCompany':'Exact firm',
        'newsURL':'https://example.org/report','newGrade':'Buy','priceTarget':0,
    })
    assert row.published_date.isoformat() == '2025-06-30T15:20:31+02:00'
    assert row.published_time.isoformat() == '15:20:31+02:00'
    assert row.analyst_firm == 'Exact firm' and row.rating_current == 'Buy'
    assert row.price_target == 0 and row.currency is None
    assert row.news_url == 'https://example.org/report'


@pytest.mark.parametrize('counts', [(9,7),(0,0),(None,None)])
def test_canonical_estimate_counts_have_no_dynamic_extras(counts):
    row = CONTRACTS['analyst_estimates'][1]
    value = row.model_validate({'symbol':'MSFT','date':'2030-06-30', 'numAnalystsRevenue':counts[0], 'numAnalystsEps':counts[1]})
    assert value.number_analyst_estimated_revenue == counts[0]
    assert value.number_analysts_estimated_eps == counts[1]
    assert not value.model_extra
    assert value.model_dump()['number_analyst_estimated_revenue'] == counts[0]
    assert value.model_dump()['number_analysts_estimated_eps'] == counts[1]
    fields = render_field_templates(row)
    for name in ['number_analyst_estimated_revenue','number_analysts_estimated_eps']:
        assert fields[name].unit == 'count' and fields[name].scale == 1

@pytest.mark.parametrize('name', CONTRACTS)
def test_every_retained_source_alias_serializes_to_canonical_without_extras(name):
    row = CONTRACTS[name][1]
    aliases = dict(row.__alias_dict__)
    if name == 'analyst_estimates':
        aliases.pop('number_analysts_estimated_revenue', None)
        aliases.pop('number_analysts_eps', None)
        aliases.update(number_analyst_estimated_revenue='numAnalystsRevenue', number_analysts_estimated_eps='numAnalystsEps')
    for canonical, source in aliases.items():
        payload = {'symbol':'MSFT','date':'2030-06-30','publishedDate':'2025-06-30','period_ending':'2025-06-30','revenue':0}
        payload = {key:value for key,value in payload.items() if key in row.model_fields or key in ['publishedDate'] and 'published_date' in row.model_fields}
        probe = 9 if canonical.startswith(('estimated_', 'number_')) else 'Exact source value'
        payload[source] = probe
        value = row.model_validate(payload)
        assert getattr(value,canonical) == probe
        assert value.model_dump(by_alias=False)[canonical] == probe
        assert not value.model_extra

@pytest.mark.parametrize('name', CONTRACTS)
def test_date_manifest_matches_native_requiredness_and_nullability(name):
    query, row = CONTRACTS[name]
    frozen = json.loads((FIXTURES / f'{name}.json').read_text())
    for field, contract in frozen['date_contracts'].items():
        assert contract['required'] == row.model_fields[field].is_required()
        payload = {'symbol':'MSFT','date':'2030-06-30','published_date':'2025-06-30','period_ending':'2025-06-30','revenue':0,field:None}
        try:
            row.model_validate(payload)
            nullable = True
        except ValidationError:
            nullable = False
        assert contract['nullable'] == nullable

@pytest.mark.parametrize('name', CONTRACTS)
def test_alias_manifest_separates_source_schema_and_canonical_names(name):
    row = CONTRACTS[name][1]
    frozen = json.loads((FIXTURES / f'{name}.json').read_text())
    assert frozen['effective_aliases'] == row.__alias_dict__
    assert set(frozen['accepted_validation_aliases']) == set(row.model_fields)
    for canonical, field in row.model_fields.items():
        item = frozen['accepted_validation_aliases'][canonical]
        assert item['canonical'] == canonical
        assert item['generated_schema_alias'] == field.validation_alias
        assert item['source_aliases'] == [source for target,source in row.__alias_dict__.items() if target == canonical]
        assert item['serialization'] == field.serialization_alias
    if name == 'analyst_estimates':
        assert frozen['retained_aliases'] == RETAINED_ESTIMATE_ALIASES
        assert frozen['compatibility']['incompatibilities']
        assert 'number_analysts_eps' not in frozen['effective_aliases']
        assert 'number_analysts_estimated_revenue' not in frozen['effective_aliases']
