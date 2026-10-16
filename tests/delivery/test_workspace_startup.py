"""Private bootstrap packaging regressions; runtime evidence is recorded separately."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LITE = ROOT / 'vendor/workspace/lite'


def test_bootstrap_does_not_print_credentials():
    entrypoint = (LITE / 'entrypoint.sh').read_text()
    assert 'Password: ${OPENBB_ADMIN_PASSWORD}' not in entrypoint
    assert 'continuing anyway' not in entrypoint
    assert 'bootstrap.py' in entrypoint


def test_backend_build_is_frozen_and_health_dependency_exists():
    dockerfile = (LITE / 'Dockerfile').read_text()
    assert 'poetry lock' not in dockerfile
    assert 'safe-chain uv' in dockerfile
    assert 'python:3.13-slim' not in dockerfile
    assert 'curl nginx' in dockerfile


def load_bootstrap():
    import importlib.util
    spec = importlib.util.spec_from_file_location('bootstrap', LITE / 'bootstrap.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_private_config_roundtrip_and_permissions(tmp_path, monkeypatch, capsys):
    import stat
    import tomllib
    bootstrap = load_bootstrap()
    monkeypatch.setenv('OPENBB_ADMIN_PASSWORD', 'Aa1!"quote\\slash')
    monkeypatch.setenv('OPENBB_ADMIN_EMAIL', 'disposable@example.invalid')
    first = bootstrap.resolve_secrets(tmp_path / 'secrets.env')
    bootstrap.write_admin_config(tmp_path / 'config.toml', first)
    parsed = tomllib.loads((tmp_path / 'config.toml').read_text())
    assert parsed['admins'][0]['password'] == first['OPENBB_ADMIN_PASSWORD']
    monkeypatch.delenv('OPENBB_ADMIN_PASSWORD')
    monkeypatch.delenv('OPENBB_ADMIN_EMAIL')
    second = bootstrap.resolve_secrets(tmp_path / 'secrets.env')
    assert first == second
    for name in ('secrets.env', 'config.toml'):
        assert stat.S_IMODE((tmp_path / name).stat().st_mode) == 0o600
    assert first['OPENBB_ADMIN_PASSWORD'] not in capsys.readouterr().out


def test_newline_in_credentials_fails_without_writing(tmp_path, monkeypatch):
    import pytest
    bootstrap = load_bootstrap()
    monkeypatch.setenv('OPENBB_ADMIN_PASSWORD', 'Aa1!\nINJECTED=value')
    with pytest.raises(ValueError, match='single-line'):
        bootstrap.resolve_secrets(tmp_path / 'secrets.env')
    assert not (tmp_path / 'secrets.env').exists()


def test_real_first_and_repeat_startup(tmp_path, monkeypatch):
    """Opt in with a protected restored backend interpreter; never owner state."""
    import os
    import shutil
    import subprocess
    import sys
    import pytest

    python = os.environ.get('QOPENBB_STARTUP_PYTHON')
    if not python:
        pytest.skip('Set QOPENBB_STARTUP_PYTHON to the restored backend interpreter')
    source = ROOT / 'vendor/workspace/backend-api/backend'
    stage = tmp_path / 'backend'
    shutil.copytree(source, stage, ignore=shutil.ignore_patterns('.env', '*.db', '__pycache__', '.venv'))
    bootstrap = load_bootstrap()
    state = tmp_path / 'state'
    state.mkdir(mode=0o700)
    (state / 'storage').mkdir()
    monkeypatch.setenv('OPENBB_ADMIN_EMAIL', 'bootstrap@example.com')
    values = bootstrap.resolve_secrets(state / 'secrets.env')
    bootstrap.write_admin_config(stage / 'scripts/cfgs/config.toml', values)
    env = {**os.environ, **values, 'PYTHONPATH': str(stage), 'DATABASE_TYPE': 'sqlite',
           'DB_PATH': str(state / 'openbb.db'), 'FOLDER_STORAGE_PATH': str(state / 'storage'),
           'REDIS_HOST': '127.0.0.1', 'REDIS_PORT': os.environ.get('QOPENBB_STARTUP_REDIS_PORT', '16379'),
           'REDIS_PASS': '', 'MODE': 'lite', 'STORAGE_PROVIDER': 'folder', 'EMAIL_PROVIDER': 'none',
           'HUBSPOT': '0', 'PROMETHEUS': '0', 'WORKERS': '1', 'DISABLE_CORS': '1',
           'SELFURL': 'http://localhost:3000/api', 'FRONTENDURL': 'http://localhost:3000',
           'PROURL': 'http://localhost:3000', 'QOPENBB_PROBE_MARKER': str(state / 'identity.json')}
    for phase in ('first', 'repeat'):
        if phase == 'repeat':
            assert bootstrap.resolve_secrets(state / 'secrets.env') == values
        for args in (['-m', 'alembic', 'upgrade', 'head'], ['-m', 'scripts.init_users'],
                     [str(Path(__file__).resolve()), '--probe']):
            result = subprocess.run([python, *args], cwd=stage, env=env, capture_output=True, text=True)
            output = result.stdout + result.stderr
            assert values['OPENBB_ADMIN_PASSWORD'] not in output, 'Bootstrap password leaked'
            assert result.returncode == 0, output.replace(values['OPENBB_ADMIN_PASSWORD'], '[REDACTED]')


def account_probe():
    import asyncio
    import json
    import os
    from uuid import UUID
    from sqlalchemy import select
    from starlette.requests import Request
    from api import schemas
    from api.models import DashboardItem, User
    from routers.entity import aget_write_db
    from routers.pro.index import login

    async def verify():
        async for db in aget_write_db():
            handler = login
            while hasattr(handler, '__wrapped__'):
                handler = handler.__wrapped__
            account_input = schemas.ProUserLogin(email=os.environ['OPENBB_ADMIN_EMAIL'],
                                                 password=os.environ['OPENBB_ADMIN_PASSWORD'])
            request = Request({'type': 'http', 'method': 'POST', 'path': '/pro/login',
                               'headers': [], 'client': ('127.0.0.1', 1)})
            result = await handler(request, account_input, db)
            assert result.status_code == 200
            authenticated = json.loads(result.body)
            assert authenticated['access_token']
            assert authenticated['email'] == account_input.email
            account = (await db.execute(select(User).where(User.email == account_input.email))).scalar_one()
            marker = Path(os.environ['QOPENBB_PROBE_MARKER'])
            content = {'name': 'startup-persistence-check', 'widgets': []}
            if marker.exists():
                previous = json.loads(marker.read_text())
                assert str(account.uuid) == previous['account_uuid']
                item = await db.get(DashboardItem, UUID(previous['dashboard_uuid']))
                assert item.content == content
                assert 'startup-persistence-check' in result.body.decode()
            else:
                item = DashboardItem(creator_uuid=account.uuid, owner_uuid=account.uuid, content=content)
                db.add(item)
                await db.commit()
                marker.write_text(json.dumps({'account_uuid': str(account.uuid), 'dashboard_uuid': str(item.uuid)}))
            break
    asyncio.run(verify())


if __name__ == '__main__':
    import sys
    if sys.argv[1:] == ['--probe']:
        account_probe()




def test_non_bmp_credentials_roundtrip(tmp_path):
    import tomllib
    bootstrap = load_bootstrap()
    values = {'OPENBB_ADMIN_EMAIL': 'owner' + chr(0x1f512) + '@example.com',
              'OPENBB_ADMIN_PASSWORD': 'Aa1!abcdef' + chr(0x1f512)}
    config = tmp_path / 'config.toml'
    bootstrap.write_admin_config(config, values)
    parsed = tomllib.loads(config.read_text())
    assert parsed['admins'][0]['email'] == values['OPENBB_ADMIN_EMAIL']
    assert parsed['admins'][0]['password'] == values['OPENBB_ADMIN_PASSWORD']
