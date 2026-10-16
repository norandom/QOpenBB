"""Explicit opt-in runtime acceptance of the exact portable-loaded data image."""
import json
import os
from pathlib import Path
import subprocess
import time

import pytest

IMAGE = os.environ.get('QOPENBB_DATA_IMAGE')
pytestmark = pytest.mark.skipif(not IMAGE, reason='requires explicitly identified loaded data image')
SENTINEL = 'qopenbb-disposable-task36-never-a-real-key'


def docker(*args, check=True):
    return subprocess.run(['docker', *args], text=True, capture_output=True, check=check)


def probe(cid, path):
    code = '''import json,urllib.request,urllib.error
try:
 r=urllib.request.urlopen('http://127.0.0.1:6900'+PATH,timeout=5)
except urllib.error.HTTPError as e:
 r=e
print(json.dumps({'status':r.status,'body':json.load(r)}))
'''.replace('PATH', repr(path))
    return json.loads(docker('exec', cid, 'python', '-c', code).stdout)


@pytest.mark.parametrize('keys', [False, True])
def test_image_health_routes_credentials_and_dependencies(keys, tmp_path):
    args = ['run', '-d', '--network', 'none']
    if keys:
        args += ['-e', 'FMP_API_KEY=' + SENTINEL, '-e', 'FRED_API_KEY=' + SENTINEL]
    cid = docker(*args, IMAGE).stdout.strip()
    try:
        for _ in range(90):
            try:
                health = probe(cid, '/healthz')
                break
            except (subprocess.CalledProcessError, json.JSONDecodeError):
                time.sleep(1)
        else:
            pytest.fail('data process did not become healthy: ' + docker('logs', cid).stdout)
        assert health['status'] == 200
        ready = probe(cid, '/readyz')
        assert ready['status'] == (200 if keys else 503)
        assert ready['body']['missing_routes'] == []
        assert ready['body']['missing'] == ([] if keys else ['FMP_API_KEY', 'FRED_API_KEY'])
        schema = probe(cid, '/openapi.json')
        assert schema['status'] == 200
        for path in ['/api/v1/equity/profile', '/api/v1/equity/fundamental/income', '/api/v1/economy/fred_series']:
            assert path in schema['body']['paths']
        assert SENTINEL not in json.dumps(schema)
        script = '''import importlib.metadata as m,json
names=['openbb-core','openbb-equity','openbb-economy','openbb-fred','openbb-fmp']
print(json.dumps({'versions':{n:m.version(n) for n in names},'entries':{n:[e.name for e in m.distribution(n).entry_points] for n in names},'origins':{n:json.loads(m.distribution(n).read_text('direct_url.json')) for n in names},'installed':[d.metadata['Name'].lower() for d in m.distributions()]}))'''
        packages = json.loads(docker('exec', cid, 'python', '-c', script).stdout)
        assert list(packages['versions'].values()) == ['2.0.1', '2.0.0', '2.0.0', '2.0.0', '1.6.1+qopenbb.1']
        assert all(packages['entries'][name] for name in ['openbb-equity', 'openbb-economy', 'openbb-fred', 'openbb-fmp'])
        assert all(value['url'].startswith('file:///build/vendor/data-api/openbb_platform/')
                   and not value.get('dir_info', {}).get('editable') for value in packages['origins'].values())
        assert not {'pytest', 'pytest-xdist', 'pluggy'} & set(packages['installed'])
        assert docker('exec', cid, 'sh', '-c', 'command -v uv || command -v safe-chain', check=False).returncode != 0
        logs = docker('logs', cid)
        assert SENTINEL not in logs.stdout + logs.stderr
        report = {'image': IMAGE, 'keys_configured': keys, 'health': health, 'readiness': ready,
                  'schema_sha256': __import__('hashlib').sha256(json.dumps(schema['body'], sort_keys=True).encode()).hexdigest(),
                  'packages': packages}
        destination = os.environ.get('QOPENBB_DATA_EVIDENCE')
        if destination:
            Path(destination, 'runtime-' + str(keys).lower() + '.json').write_text(json.dumps(report, indent=2) + '\n')
    finally:
        docker('rm', '-f', cid)


def test_image_rejects_unsupported_auth():
    result = docker('run', '--rm', '--network', 'none', '-e', 'OPENBB_API_AUTH=true', IMAGE, check=False)
    assert result.returncode != 0
    assert 'OPENBB_API_AUTH must be false' in result.stderr
    assert SENTINEL not in result.stdout + result.stderr
