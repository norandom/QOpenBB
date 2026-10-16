"""Workspace service selection retains the strict foundation input boundary."""
import json
from pathlib import Path
import pytest
from test_image_builds import inputs
from qopenbb_ci.staging import stage, verify_stage


def test_workspace_stage_requires_public_release(tmp_path):
    roots, policy, lock = inputs(tmp_path)
    result = stage(tmp_path / 'stage', roots, policy, lock,
                   service='workspace', release_version='qopenbb-task25')
    assert result['service'] == 'workspace'
    assert result['release_version'] == 'qopenbb-task25'
    assert verify_stage(tmp_path / 'stage', policy, lock) == result


@pytest.mark.parametrize('release', ['', 'secret value', 'x\nINJECT=bad'])
def test_invalid_release_rejected_before_staging(tmp_path, release):
    roots, policy, lock = inputs(tmp_path)
    with pytest.raises(ValueError):
        stage(tmp_path / 'stage', roots, policy, lock,
              service='workspace', release_version=release)
    assert not (tmp_path / 'stage').exists()


def test_foundation_rejects_workspace_metadata(tmp_path):
    roots, policy, lock = inputs(tmp_path)
    target = tmp_path / 'stage'
    result = stage(target, roots, policy, lock)
    result['release_version'] = 'public'
    (target / 'provenance.json').write_text(json.dumps(result))
    with pytest.raises(ValueError):
        verify_stage(target, policy, lock)

@pytest.mark.parametrize('mutation', ['missing', 'null', 'extra', 'bad'])
def test_workspace_rejects_unreviewed_metadata(tmp_path, mutation):
    roots, policy, lock = inputs(tmp_path)
    target = tmp_path / 'stage'
    result = stage(target, roots, policy, lock, service='workspace', release_version='public')
    if mutation == 'missing':
        del result['release_version']
    elif mutation == 'null':
        result['release_version'] = None
    elif mutation == 'extra':
        result['private_build_key'] = 'forbidden'
    else:
        result['release_version'] = 'private\nvalue'
    (target / 'provenance.json').write_text(json.dumps(result))
    with pytest.raises(ValueError):
        verify_stage(target, policy, lock)


def test_export_initializes_sdk_before_resolving_multiple_inputs(tmp_path, monkeypatch):
    import argparse
    import asyncio
    import importlib.util
    import sys
    import types
    events = []
    class Connection:
        async def __aenter__(self):
            events.append('connect')
        async def __aexit__(self, *args):
            pass
    class Host:
        def directory(self, path):
            assert events[-1] == 'version'
            events.append('directory')
            return object()
    class Dag:
        async def version(self):
            events.append('version')
            return '0.21.8'
        def host(self):
            return Host()
    class Image:
        async def export(self, path, **kwargs):
            events.append('export')
    async def build(*args):
        events.append('build')
        return Image()
    monkeypatch.setitem(sys.modules, 'dagger', types.SimpleNamespace(
        Connection=Connection, dag=Dag(), ImageMediaTypes=types.SimpleNamespace(DockerMediaTypes='docker')))
    monkeypatch.setitem(sys.modules, 'qopenbb.images', types.SimpleNamespace(build=build))
    path = Path(__file__).resolve().parents[2] / '.dagger/src/qopenbb/export.py'
    spec = importlib.util.spec_from_file_location('sdk_export_under_test', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    (tmp_path / 'provenance.json').write_text('{}')
    asyncio.run(module.export(argparse.Namespace(stage=tmp_path, service='workspace',
        base='pinned', archive=tmp_path / 'image.tar')))
    assert events == ['connect', 'version', 'directory', 'build', 'export']
