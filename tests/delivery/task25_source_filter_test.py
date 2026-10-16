"""Keep required maintained source files without opening generated/state directories."""
from pathlib import PurePosixPath
import subprocess
import pytest
from test_image_builds import inputs
from qopenbb_ci.source_filter import excluded
from qopenbb_ci.staging import stage, verify_stage

RETAINED = ['terminalpro/build/runtimeConfig.ts',
            'terminalpro/src/components/DataConnectors/NewComponents/Data/Content.tsx']


@pytest.mark.parametrize('name', RETAINED)
def test_exact_required_source_is_retained(tmp_path, name):
    assert not excluded(PurePosixPath(name), tmp_path / name)


@pytest.mark.parametrize('name', [
    'terminalpro/build/generated.ts', 'terminalpro/build/runtimeConfig.ts.key',
    'terminalpro/build/.env', 'terminalpro/Build/runtimeConfig.ts',
    'terminalpro/build/RuntimeConfig.ts',
    'terminalpro/src/components/DataConnectors/NewComponents/Data/generated.tsx',
    'terminalpro/src/components/DataConnectors/NewComponents/data/Content.tsx',
    'terminalpro/src/components/DataConnectors/NewComponents/Data/Content.tsx.db',
    'terminalpro/src/components/DataConnectors/NewComponents/Data/.env'])
def test_adjacent_generated_private_and_case_variants_stay_excluded(tmp_path, name):
    assert excluded(PurePosixPath(name), tmp_path / name)


def test_exact_source_bytes_survive_stage_and_verification(tmp_path):
    roots, policy, lock = inputs(tmp_path)
    root = roots['workspace']
    for name in RETAINED:
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(b'// maintained source\nexport const value = 17;\n')
    subprocess.run(['git', '-C', str(root), 'add', '.'], check=True)
    subprocess.run(['git', '-C', str(root), 'commit', '-qm', 'required source fixtures'], check=True)
    revision = subprocess.check_output(['git', '-C', str(root), 'rev-parse', 'HEAD'], text=True).strip()
    lock['workspace']['revision'] = revision
    policy['sources']['workspace']['revision'] = revision
    target = tmp_path / 'stage'
    result = stage(target, roots, policy, lock, service='workspace', release_version='public')
    assert verify_stage(target, policy, lock) == result
    for name in RETAINED:
        assert (target / 'sources/workspace' / name).read_bytes() == (root / name).read_bytes()
