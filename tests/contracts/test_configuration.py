import copy
import json
from pathlib import Path

import pytest
from qopenbb_ci.configuration import validate_configuration, validate_contracts

ROOT = Path(__file__).resolve().parents[2]

def env():
    return {'PUBLIC_URL': 'http://localhost:23003', 'WORKSPACE_IMAGE': 'qopenbb/workspace:dev',
            'DATA_API_IMAGE': 'qopenbb/data:dev', 'FMP_API_KEY': 'fixture-fmp',
            'FRED_API_KEY': 'fixture-fred'}

def contracts():
    return {name: json.loads((ROOT / 'contracts' / f'{name}.json').read_text())
            for name in ('runtime', 'datasets', 'routes')}

def test_dashboard_selected_without_optional_settings():
    result = validate_configuration(env(), selected={'workspace', 'data-api'})
    assert set(result['services']) == {'workspace', 'data-api'}
    assert result['urls']['SELFURL'] == 'http://localhost:23003/api'
    assert result['urls']['DATA_URL'] == 'http://localhost:23003/data'
    assert result['forwarded_scheme'] == 'http'
    assert result['services']['data-api']['environment'] == {
        'FMP_API_KEY': 'fixture-fmp', 'FRED_API_KEY': 'fixture-fred', 'OPENBB_API_AUTH': 'false'}
    assert 'FMP_API_KEY' not in result['services']['workspace']['environment']
    assert 'EXCEL_URL' not in result['urls']

@pytest.mark.parametrize('selected', [{'agent'}, {'workspace', 'data-api', 'agent'},
                                      {'workspace', 'data-api', 'excel'}])
def test_selected_components_require_real_configuration(selected):
    with pytest.raises(ValueError):
        validate_configuration(env(), selected=selected)

def test_full_configuration_credential_scope_and_optional_excel():
    values = env() | {'AGENT_IMAGE': 'qopenbb/agent:dev', 'EXCEL_IMAGE': 'qopenbb/excel:dev',
                      'ANTHROPIC_API_KEY': 'fixture-agent', 'ANTHROPIC_MODEL': 'explicit-model',
                      'OPENAI_API_KEY': 'unwired', 'ECONDB_API_KEY': 'unwired'}
    result = validate_configuration(values, selected={'workspace', 'data-api', 'agent', 'excel'})
    assert result['services']['agent']['environment'] == {
        'ANTHROPIC_API_KEY': 'fixture-agent', 'ANTHROPIC_MODEL': 'explicit-model'}
    assert result['services']['excel']['environment'] == {}
    assert result['urls']['EXCEL_URL'].endswith('/excel')
    assert 'agent' not in result['services']['workspace']['depends_on']
    assert [s['publish'] for s in result['services'].values() if s['publish']] == [['0.0.0.0:23003:3000']]
    assert [s['binds'] for s in result['services'].values() if s['binds']] == [['./data/workspace:/data']]

@pytest.mark.parametrize('url', ['relative', 'http://workspace:3000', 'https://agent',
    'http://example.org', 'https://user:pass@example.org', 'https://example.org/prefix',
    'https://example.org/?q=x', 'https://example.org/#x', 'ftp://example.org',
    'https://data-api:6900', 'https://example.org//', 'https://example.org/%2f',
    'https://example.org\\evil', 'https://example.org:bad'])
def test_public_url_rejects_unsafe_origin(url):
    with pytest.raises(ValueError):
        validate_configuration(env() | {'PUBLIC_URL': url}, selected={'workspace', 'data-api'})

@pytest.mark.parametrize('url', ['http://127.0.0.1:23003', 'http://[::1]:23003',
                               'https://qbb.hanse-hedge.fund/'])
def test_public_origin_normalized(url):
    result = validate_configuration(env() | {'PUBLIC_URL': url}, selected={'workspace', 'data-api'})
    assert result['urls']['DATA_URL'] == url.rstrip('/') + '/data'

@pytest.mark.parametrize('key', ['FMP_API_KEY', 'FRED_API_KEY', 'WORKSPACE_IMAGE', 'DATA_API_IMAGE'])
def test_missing_dashboard_inputs_do_not_reveal_values(key):
    values = env(); values[key] = ''
    with pytest.raises(ValueError) as caught:
        validate_configuration(values, selected={'workspace', 'data-api'})
    assert 'fixture-' not in str(caught.value)

@pytest.mark.parametrize('image', ['parser-only', 'example/placeholder:latest', 'qopenbb/api:dev'])
def test_production_requires_immutable_real_images(image):
    with pytest.raises(ValueError):
        validate_configuration(env() | {'DATA_API_IMAGE': image}, selected={'workspace', 'data-api'}, production=True)

def test_production_digest_and_fixed_auth():
    values = env() | {key: 'registry.example/qopenbb/image@sha256:' + 'a' * 64
                      for key in ('WORKSPACE_IMAGE', 'DATA_API_IMAGE')}
    assert validate_configuration(values, selected={'workspace', 'data-api'}, production=True)
    with pytest.raises(ValueError):
        validate_configuration(values | {'OPENBB_API_AUTH': 'true'}, selected={'workspace', 'data-api'})

def test_contracts_provisional_unique_and_fixed_topology():
    data = contracts()
    validate_contracts(**data)
    assert data['routes']['status'] == 'provisional'
    assert len({r['path'] for r in data['routes']['routes']}) == 3
    assert all('operation_id' not in r for r in data['routes']['routes'])

@pytest.mark.parametrize('mutation', ['port', 'bind', 'credential', 'dependency', 'route', 'operation', 'dataset'])
def test_tampered_contract_rejected(mutation):
    data = copy.deepcopy(contracts())
    workspace = data['runtime']['services']['workspace']
    if mutation == 'port': workspace['publish'] = ['0.0.0.0:9999:3000']
    if mutation == 'bind': workspace['binds'] += ['/var/run/docker.sock:/var/run/docker.sock']
    if mutation == 'credential': workspace['environment'] += ['FMP_API_KEY']
    if mutation == 'dependency': workspace['depends_on'] += ['agent']
    if mutation == 'route': data['routes']['routes'].append(data['routes']['routes'][0])
    if mutation == 'operation': data['routes']['routes'][0]['operation_id'] = 'invented'
    if mutation == 'dataset': data['datasets']['datasets'][0]['parameters']['symbol'] = 'MSFT'
    with pytest.raises(ValueError): validate_contracts(**data)

def test_unknown_service_and_inactive_placeholder():
    with pytest.raises(ValueError):
        validate_configuration(env(), selected={'workspace', 'data-api', 'database'})
    result = validate_configuration(env() | {'AGENT_IMAGE': 'parser-only', 'EXCEL_IMAGE': 'placeholder'},
                                    selected={'workspace', 'data-api'})
    assert 'agent' not in result['services']

@pytest.mark.parametrize('url', ['https://10.0.0.1', 'https://example..org', 'https://-bad.example'])
def test_nonpublic_or_malformed_public_host(url):
    with pytest.raises(ValueError):
        validate_configuration(env() | {'PUBLIC_URL': url}, selected={'workspace', 'data-api'})

@pytest.mark.parametrize('image', ['registry:/foo', 'example.invalid/image:dev', 'bad//image:dev', 'qopenbb/image'])
def test_development_image_syntax_and_parser_references(image):
    with pytest.raises(ValueError):
        validate_configuration(env() | {'DATA_API_IMAGE': image}, selected={'workspace', 'data-api'})

def test_public_template_credentials_are_empty():
    template = (ROOT / '.env.sample').read_text()
    entries = dict(line.split('=', 1) for line in template.splitlines()
                   if line.strip() and not line.lstrip().startswith('#'))
    for key in ('FMP_API_KEY', 'FRED_API_KEY', 'ANTHROPIC_API_KEY', 'OPENAI_API_KEY', 'ECONDB_API_KEY'):
        assert entries[key] == ''

def test_contract_numeric_types_are_strict():
    data = contracts()
    data['runtime']['schema_version'] = True
    with pytest.raises(ValueError): validate_contracts(**data)
    data = contracts()
    data['runtime']['services']['workspace']['port'] = 3000.0
    with pytest.raises(ValueError): validate_contracts(**data)
