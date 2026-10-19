import json
from pathlib import Path

import pytest
from qopenbb_ci.source_filter import select_source

ROOT = Path(__file__).resolve().parents[2]
POLICY = json.loads((ROOT / 'contracts/sources.json').read_text())
LOCK = json.loads((ROOT / 'sources.lock.json').read_text())

def put(root, path, content='synthetic'):
    target = root / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content)

def test_recursive_filter_preserves_code_locks_notices(tmp_path):
    keep = ['terminalpro/src/app.ts', 'terminalpro/pnpm-lock.yaml', 'LICENSE', 'NOTICE', 'lite/Dockerfile']
    reject = ['unowned/file.py', 'terminalpro/.env', 'terminalpro/deep/.env.production',
        'terminalpro/deep/private.key', 'terminalpro/deep/key.pem', 'terminalpro/.git/config',
        'terminalpro/deep/data/account.db', 'terminalpro/backups/archive',
        'terminalpro/artifacts/trace.zip', 'terminalpro/playwright-report/index.html',
        'terminalpro/.codex/browser/state.json', 'terminalpro/node_modules/lib.js',
        'terminalpro/.venv/bin/python', 'terminalpro/__pycache__/a.pyc',
        'terminalpro/deep/id_rsa', 'terminalpro/.env.sample']
    for path in keep + reject: put(tmp_path, path)
    put(tmp_path, 'backend-api/.env.sample', 'FMP_API_KEY=\nFRED_API_KEY=\n')
    chosen = select_source(tmp_path, 'workspace', LOCK['workspace']['revision'], POLICY, LOCK)
    assert set(chosen) == set(keep + ['backend-api/.env.sample'])

def test_symlink_and_path_escape_rejected(tmp_path):
    put(tmp_path, 'terminalpro/src/code.ts')
    outside = tmp_path.parent / (tmp_path.name + '-outside')
    outside.mkdir(); put(outside, 'secret.txt')
    (tmp_path / 'terminalpro/link').symlink_to(outside, target_is_directory=True)
    with pytest.raises(ValueError):
        select_source(tmp_path, 'workspace', LOCK['workspace']['revision'], POLICY, LOCK)

@pytest.mark.parametrize('change', ['revision', 'lock', 'escape', 'root', 'unknown'])
def test_source_scope_fails_closed(tmp_path, change):
    policy = json.loads(json.dumps(POLICY)); lock = json.loads(json.dumps(LOCK))
    revision = LOCK['workspace']['revision']; source = 'workspace'
    if change == 'revision': revision = 'a' * 40
    if change == 'lock': lock['workspace']['revision'] = 'a' * 40
    if change == 'escape': policy['sources']['workspace']['allow'] = ['../outside']
    if change == 'root': policy['sources']['workspace']['allow'] = ['.']
    if change == 'unknown': source = 'unknown'
    with pytest.raises(ValueError): select_source(tmp_path, source, revision, policy, lock)

def test_data_source_ownership_and_empty_sample_values(tmp_path):
    for path in ['openbb_platform/providers/fred/code.py', 'openbb_platform/uv.lock', 'LICENSE']:
        put(tmp_path, path)
    put(tmp_path, 'terminalpro/unowned.ts')
    put(tmp_path, 'openbb_platform/.env.example', 'ANTHROPIC_API_KEY=synthetic-secret')
    put(tmp_path, 'openbb_platform/empty/.env.example', '# public\nFMP_API_KEY=""\n')
    result = select_source(tmp_path, 'data_api', LOCK['data_api']['revision'], POLICY, LOCK)
    assert result == ['LICENSE', 'openbb_platform/empty/.env.example',
                      'openbb_platform/providers/fred/code.py', 'openbb_platform/uv.lock']

def test_scan_errors_fail_closed(tmp_path, monkeypatch):
    put(tmp_path, 'terminalpro/code.ts')
    def failed_walk(start, *, followlinks, onerror):
        onerror(PermissionError('synthetic unreadable directory'))
        return iter(())
    monkeypatch.setattr('qopenbb_ci.source_filter.os.walk', failed_walk)
    with pytest.raises(ValueError, match='completely scan'):
        select_source(tmp_path, 'workspace', LOCK['workspace']['revision'], POLICY, LOCK)

@pytest.mark.parametrize('source,keep', [
    ('workspace', ['backend-api/backend/api/storage/abstract.py',
                   'backend-api/backend/api/storage/local.py',
                   'terminalpro/src/lib/state/auth.ts',
                   'terminalpro/src/lib/state/tutorial.tsx',
                   'terminalpro/src/lib/state/main.json',
                   'terminalpro/public/assets/data/indices_fmp.json',
                   'terminalpro/public/assets/data/tickers_fmp.json']),
    ('data_api', ['openbb_platform/core/openbb_core/app/logs/logging_service.py',
                  'openbb_platform/core/openbb_core/app/logs/handlers/path_tracking_file_handler.py']),
])
def test_production_paths_named_like_runtime_state_are_retained(tmp_path, source, keep):
    for path in keep:
        put(tmp_path, path)
    parents = {str(Path(path).parent) for path in keep}
    reject = [f'{parent}/{name}' for parent in parents for name in (
        '.env', 'private.key', 'account.sqlite', 'session.json', 'trace.log',
        'evidence/session.ts', 'state/account.ts', 'data/private.py', 'id_rsa')]
    for path in reject:
        put(tmp_path, path)
    assert set(select_source(tmp_path, source, LOCK[source]['revision'], POLICY, LOCK)) == set(keep)


def test_ai_artifact_components_are_exact_public_source_exceptions(tmp_path):
    prefix = 'terminalpro/src/components/AI/artifacts/'
    keep = [prefix + name + '.tsx' for name in (
        'AppArtifact', 'ArtifactShared', 'ChartArtifact', 'HTMLArtifact',
        'SnowflakeArtifact', 'TableArtifact', 'TextArtifact')]
    reject = [prefix + name for name in (
        'GeneratedArtifact.tsx', 'session.json', '.env', '.env.production',
        'private.key', 'account.sqlite', 'AppArtifact.ts', 'AppArtifact.tsx.bak',
        'artifacts/AppArtifact.tsx', 'nested/AppArtifact.tsx',
        'evidence/AppArtifact.tsx', 'state/AppArtifact.tsx', 'id_rsa')]
    reject += ['terminalpro/artifacts/AppArtifact.tsx',
               'terminalpro/src/components/Other/artifacts/AppArtifact.tsx']
    for path in keep + reject:
        put(tmp_path, path)
    chosen = select_source(tmp_path, 'workspace', LOCK['workspace']['revision'], POLICY, LOCK)
    assert set(chosen) == set(keep)
