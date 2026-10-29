"""Runtime inputs are finite, hashed and separate from owned source snapshots."""
import asyncio
import hashlib
import importlib.util
import json
import sys
import types
from pathlib import Path

import pytest
from qopenbb_ci.staging import stage, verify_stage
from test_image_builds import inputs

FINANCIAL_FILES = tuple('services/data-api/qopenbb_data/' + name for name in (
    'financial_openapi.py', 'financial_catalog.py', 'financial_policy.py',
    'financial_errors.py')) + ('docs/reference/provider-coverage.json',)

FILES = tuple('services/data-api/' + name for name in (
    'pyproject.toml', 'uv.lock', 'qopenbb_data/__init__.py',
    'qopenbb_data/config.py', 'qopenbb_data/app.py', 'qopenbb_data/gallery.py')) + (
        'contracts/widgets.json', 'contracts/apps.json',
        'contracts/gallery/data.json', 'contracts/gallery/catalog.json') + FINANCIAL_FILES


def runtime(tmp_path):
    root = tmp_path / 'runtime-root'
    for name in FILES:
        target = root / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text('public fixture')
    (root / '.env').write_text('DISPOSABLE_PRIVATE_SENTINEL')
    return root


@pytest.mark.parametrize('changed', ['services/data-api/qopenbb_data/app.py',
                                    'services/data-api/qopenbb_data/gallery.py',
                                    'contracts/widgets.json', 'contracts/apps.json',
                                    'contracts/gallery/data.json', 'contracts/gallery/catalog.json',
                                    *FINANCIAL_FILES])
def test_data_stage_has_exact_runtime_hashes(tmp_path, changed):
    roots, policy, lock = inputs(tmp_path)
    root = runtime(tmp_path)
    destination = tmp_path / 'stage'
    result = stage(destination, roots, policy, lock, 'data-api', runtime_root=root)
    assert set(result['runtime_inputs']) == set(FILES)
    assert verify_stage(destination, policy, lock) == result
    assert not (destination / 'runtime/.env').exists()
    (destination / 'runtime' / changed).write_text('changed')
    with pytest.raises(ValueError, match='hash'):
        verify_stage(destination, policy, lock)


@pytest.mark.parametrize('kind', ['extra', 'metadata', 'missing', 'symlink'])
def test_data_stage_rejects_invalid_input(tmp_path, kind):
    roots, policy, lock = inputs(tmp_path)
    root = runtime(tmp_path)
    target = root / 'services/data-api/uv.lock'
    if kind in {'missing', 'symlink'}:
        target.unlink()
        if kind == 'symlink':
            target.symlink_to(root / '.env')
        with pytest.raises((ValueError, FileNotFoundError)):
            stage(tmp_path / 'stage', roots, policy, lock, 'data-api', runtime_root=root)
        return
    destination = tmp_path / 'stage'
    result = stage(destination, roots, policy, lock, 'data-api', runtime_root=root)
    if kind == 'extra':
        (destination / 'runtime/extra').mkdir()
    else:
        result['service'] = 'foundation-smoke'
        (destination / 'provenance.json').write_text(json.dumps(result))
    with pytest.raises(ValueError):
        verify_stage(destination, policy, lock)


def test_runtime_input_requires_data_selection(tmp_path):
    roots, policy, lock = inputs(tmp_path)
    with pytest.raises(ValueError):
        stage(tmp_path / 'stage', roots, policy, lock, runtime_root=runtime(tmp_path))


@pytest.mark.parametrize('name', ['contracts/gallery/data.json', 'contracts/gallery/catalog.json'])
def test_missing_gallery_asset_cannot_be_staged(tmp_path, name):
    roots, policy, lock = inputs(tmp_path)
    root = runtime(tmp_path)
    (root / name).unlink()
    with pytest.raises(FileNotFoundError):
        stage(tmp_path / 'stage', roots, policy, lock, 'data-api', runtime_root=root)


@pytest.mark.parametrize('name', FINANCIAL_FILES)
@pytest.mark.parametrize('mutation', ['missing', 'symlink'])
def test_financial_runtime_inputs_are_required_regular_files(tmp_path, name, mutation):
    roots, policy, lock = inputs(tmp_path)
    root = runtime(tmp_path)
    target = root / name
    target.unlink()
    if mutation == 'symlink':
        target.symlink_to(root / '.env')
    with pytest.raises((ValueError, FileNotFoundError)):
        stage(tmp_path / 'stage', roots, policy, lock, 'data-api', runtime_root=root)


@pytest.mark.parametrize('mutation', ['missing', 'null', 'extra', 'traversal', 'release', 'bad-digest'])
def test_runtime_provenance_rejects_unreviewed_metadata(tmp_path, mutation):
    roots, policy, lock = inputs(tmp_path)
    destination = tmp_path / 'stage'
    result = stage(destination, roots, policy, lock, 'data-api', runtime_root=runtime(tmp_path))
    if mutation == 'missing':
        del result['runtime_inputs']
    elif mutation == 'null':
        result['runtime_inputs'] = None
    elif mutation == 'release':
        result['release_version'] = None
    elif mutation == 'bad-digest':
        result['runtime_inputs']['services/data-api/uv.lock'] = 'nope'
    else:
        name = '../private' if mutation == 'traversal' else 'services/data-api/private.py'
        result['runtime_inputs'][name] = '0' * 64
    (destination / 'provenance.json').write_text(json.dumps(result))
    with pytest.raises(ValueError):
        verify_stage(destination, policy, lock)


class ImageCalls:
    """Record build selections without installing or calling the Dagger SDK."""

    def __init__(self):
        self.calls = []

    def __getattr__(self, name):
        def record(*args, **kwargs):
            self.calls.append((name, args, kwargs))
            return self
        return record


def build_module(monkeypatch, name):
    fake = types.ModuleType('dagger')
    fake.Directory = fake.Container = ImageCalls
    fake.Platform = str
    fake.dag = types.SimpleNamespace(
        container=lambda **kwargs: ImageCalls(),
        http=lambda url, **kwargs: ('http', url, kwargs))
    monkeypatch.setitem(sys.modules, 'dagger', fake)
    path = Path(__file__).resolve().parents[2] / '.dagger/src/qopenbb' / (name + '.py')
    spec = importlib.util.spec_from_file_location('isolated_' + name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_data_image_bakes_native_revision_coverage_and_runtime_hash(monkeypatch):
    module = build_module(monkeypatch, 'data_api')
    context = types.SimpleNamespace(directory=lambda path: ('directory', path),
                                    file=lambda path: ('file', path))
    runtime_inputs = {name: hashlib.sha256(name.encode()).hexdigest() for name in FILES}
    source_revision = '13e41631bdef0ee98bfa23bda68d329224b56eb1'
    image = asyncio.run(module.data_image(context, 'python@sha256:' + 'a' * 64,
                                         runtime_inputs, source_revision))
    env = {args[0]: args[1] for name, args, _ in image.calls if name == 'with_env_variable'}
    expected_hash = hashlib.sha256((json.dumps(runtime_inputs, sort_keys=True) + '\n').encode()).hexdigest()
    assert {key: value for key, value in env.items() if key.startswith('QOPENBB_DATA_')} == {
        'QOPENBB_DATA_SOURCE_REVISION': source_revision,
        'QOPENBB_DATA_GENERATION_REVISION': source_revision,
        'QOPENBB_DATA_RUNTIME_SHA256': expected_hash,
    }
    assert ('with_file', ('/app/qopenbb_data/provider-coverage.json',
                          ('file', 'runtime/docs/reference/provider-coverage.json')), {}) in image.calls
    labels = {args[0]: args[1] for name, args, _ in image.calls if name == 'with_label'}
    assert labels['org.qopenbb.runtime-inputs.sha256'] == expected_hash
    assert not any('image' in key and 'digest' in key for key in labels)


def test_build_passes_native_source_revision_to_data_image(monkeypatch):
    module = build_module(monkeypatch, 'images')
    received = []

    async def data_image(*args):
        received.append(args)
        return ImageCalls()

    package = types.ModuleType('qopenbb')
    package.__path__ = []
    data_api = types.ModuleType('qopenbb.data_api')
    data_api.data_image = data_image
    monkeypatch.setitem(sys.modules, 'qopenbb', package)
    monkeypatch.setitem(sys.modules, 'qopenbb.data_api', data_api)
    context = ImageCalls()
    base = 'python@sha256:' + 'a' * 64
    provenance = {'service': 'data-api', 'runtime_inputs': {'public': 'b' * 64},
                  'sources': {'data_api': {'revision': 'c' * 40,
                                            'repository': 'https://example.invalid/data.git'}}}
    asyncio.run(module.build('data-api', context, base, provenance))
    assert received == [(context, base, provenance['runtime_inputs'], 'c' * 40)]
