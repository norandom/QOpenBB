"""Runtime inputs are finite, hashed and separate from owned source snapshots."""
import json
import pytest
from qopenbb_ci.staging import stage, verify_stage
from test_image_builds import inputs

FILES = ('pyproject.toml', 'uv.lock', 'qopenbb_data/__init__.py',
         'qopenbb_data/config.py', 'qopenbb_data/app.py')


def runtime(tmp_path):
    root = tmp_path / 'runtime-root'
    for name in FILES:
        target = root / 'services/data-api' / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text('public fixture')
    (root / '.env').write_text('DISPOSABLE_PRIVATE_SENTINEL')
    return root


def test_data_stage_has_exact_runtime_hashes(tmp_path):
    roots, policy, lock = inputs(tmp_path)
    root = runtime(tmp_path)
    destination = tmp_path / 'stage'
    result = stage(destination, roots, policy, lock, 'data-api', runtime_root=root)
    assert set(result['runtime_inputs']) == {'services/data-api/' + name for name in FILES}
    assert verify_stage(destination, policy, lock) == result
    assert not (destination / 'runtime/.env').exists()
    (destination / 'runtime/services/data-api/qopenbb_data/app.py').write_text('changed')
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
