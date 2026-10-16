"""Synthetic contracts for the task 1.8 image boundary."""

import json
from pathlib import Path
import subprocess
import io
import tarfile

import pytest

from qopenbb_ci.staging import stage, verify_stage
from qopenbb_ci.images import inspect_archive


def checkout(root, name):
    root.mkdir()
    def run(*args):
        return subprocess.check_output(['git', '-C', str(root), *args], text=True).strip()
    run('init', '-q')
    run('config', 'user.email', 'fixture@example.invalid')
    run('config', 'user.name', 'Synthetic Fixture')
    allow = ['lite', 'terminalpro', 'backend-api', 'LICENSE', 'NOTICE'] if name == 'workspace' else ['openbb_platform', 'LICENSE']
    for entry in allow:
        target = root / entry if '.' in entry or entry.isupper() else root / entry / 'code.py'
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text('synthetic public source')
    run('add', '.')
    run('commit', '-qm', 'synthetic snapshot')
    repository = 'https://github.com/norandom/' + name + '.git'
    run('remote', 'add', 'origin', repository)
    return {'repository': repository, 'revision': run('rev-parse', 'HEAD')}, allow


def inputs(tmp_path):
    lock, policy, roots = {}, {'schema_version': 1, 'sources': {}}, {}
    for name in ['workspace', 'data_api']:
        roots[name] = tmp_path / name
        lock[name], allow = checkout(roots[name], name)
        policy['sources'][name] = {'source_lock_key': name, 'revision': lock[name]['revision'], 'allow': allow}
    return roots, policy, lock


def test_stage_filters_before_upload_and_hashes(tmp_path):
    roots, policy, lock = inputs(tmp_path)
    (roots['workspace'] / 'terminalpro/.env').write_text('SYNTHETIC_SECRET')
    destination = tmp_path / 'stage'
    result = stage(destination, roots, policy, lock)
    assert not (destination / 'sources/workspace/terminalpro/.env').exists()
    assert verify_stage(destination) == result
    (destination / 'unlisted').write_text('SYNTHETIC_SECRET')
    with pytest.raises(ValueError, match='differ'):
        verify_stage(destination)


def test_stage_rejects_wrong_head_and_missing_essential(tmp_path):
    roots, policy, lock = inputs(tmp_path)
    lock['workspace']['revision'] = '0' * 40
    with pytest.raises(ValueError, match='HEAD'):
        stage(tmp_path / 'stage', roots, policy, lock)


def test_stage_rejects_symlink(tmp_path):
    roots, policy, lock = inputs(tmp_path)
    (roots['workspace'] / 'terminalpro/link').symlink_to('/tmp')
    with pytest.raises(ValueError, match='symlink'):
        stage(tmp_path / 'stage', roots, policy, lock)


def test_missing_or_partial_stage_rejected_before_upload(tmp_path):
    with pytest.raises(FileNotFoundError):
        verify_stage(tmp_path / 'absent')
    partial = tmp_path / 'partial'
    partial.mkdir()
    with pytest.raises(FileNotFoundError):
        verify_stage(partial)
    (partial / 'provenance.json').symlink_to(tmp_path / 'unreadable-secret')
    with pytest.raises(ValueError, match='symlink'):
        verify_stage(partial)


def test_staging_rejects_hash_tampering_and_private_manifest_paths(tmp_path):
    roots, policy, lock = inputs(tmp_path)
    destination = tmp_path / 'stage'
    result = stage(destination, roots, policy, lock)
    (destination / 'sources/workspace/LICENSE').write_text('changed')
    with pytest.raises(ValueError, match='hash'):
        verify_stage(destination, policy, lock)
    result['sources']['workspace']['files']['terminalpro/.env'] = '0' * 64
    (destination / 'provenance.json').write_text(json.dumps(result))
    with pytest.raises(ValueError):
        verify_stage(destination, policy, lock)


def test_missing_essential_and_wrong_origin_fail_closed(tmp_path):
    roots, policy, lock = inputs(tmp_path)
    subprocess.run(['git', '-C', str(roots['workspace']), 'remote', 'set-url', 'origin',
                    'https://github.com/unowned/repository.git'], check=True)
    with pytest.raises(ValueError, match='origin'):
        stage(tmp_path / 'stage', roots, policy, lock)


def archive(path, secret):
    layer = io.BytesIO()
    with tarfile.open(fileobj=layer, mode='w') as bundle:
        member = tarfile.TarInfo('safe.txt')
        member.size = len(secret)
        bundle.addfile(member, io.BytesIO(secret))
    entries = {'manifest.json': json.dumps([{'Config': 'config.json', 'Layers': ['layer.tar']}]).encode(),
               'config.json': json.dumps({'architecture': 'amd64', 'os': 'linux', 'config': {'Labels': {}}}).encode(),
               'layer.tar': layer.getvalue()}
    with tarfile.open(path, 'w') as bundle:
        for name, content in entries.items():
            member = tarfile.TarInfo(name)
            member.size = len(content)
            bundle.addfile(member, io.BytesIO(content))


def test_archive_sentinel_and_config_identity(tmp_path):
    target = tmp_path / 'image.tar'
    archive(target, b'SYNTHETIC_SECRET')
    with pytest.raises(ValueError, match='secret'):
        inspect_archive(target, b'SYNTHETIC_SECRET')
    result = inspect_archive(target, b'absent')
    assert result['image_config_digest'].startswith('sha256:')
    assert result['image_config_digest'][7:] != result['archive_sha256']


def test_missing_essential_source_fails(tmp_path):
    roots, policy, lock = inputs(tmp_path)
    subprocess.run(['git', '-C', str(roots['workspace']), 'rm', 'NOTICE'], check=True,
                   stdout=subprocess.DEVNULL)
    subprocess.run(['git', '-C', str(roots['workspace']), 'commit', '-qm', 'remove notice'], check=True)
    revision = subprocess.check_output(['git', '-C', str(roots['workspace']), 'rev-parse', 'HEAD'], text=True).strip()
    lock['workspace']['revision'] = revision
    policy['sources']['workspace']['revision'] = revision
    with pytest.raises(ValueError, match='essential'):
        stage(tmp_path / 'stage', roots, policy, lock)


def test_all_dagger_invocations_have_secret_free_environment(tmp_path, monkeypatch):
    import argparse
    from qopenbb_ci import image_cli
    root = Path(__file__).resolve().parents[2]
    monkeypatch.setenv('PUBLICATION_PASSWORD', 'synthetic-publication-secret')
    monkeypatch.setenv('DAGGER_CLOUD_TOKEN', 'synthetic-cloud-secret')
    monkeypatch.setattr(image_cli, 'verify_stage', lambda *args: {'sources': {}})
    monkeypatch.setattr(image_cli, 'inspect_archive', lambda *args: {})
    monkeypatch.setattr(image_cli, 'verify_engine', lambda *args: {'image_id': 'synthetic'})
    calls = []
    def checked(command, **kwargs):
        environment = kwargs['env']
        assert 'PUBLICATION_PASSWORD' not in environment
        assert 'DAGGER_CLOUD_TOKEN' not in environment
        if command[0] == 'dagger':
            assert Path(environment['HOME']).is_dir()
            assert not list(Path(environment['DOCKER_CONFIG']).iterdir())
            calls.append(command)
        return 'dagger v0.21.8 synthetic ' if command[0] == 'dagger' else '0.21.8'
    monkeypatch.setattr(image_cli.subprocess, 'check_output', checked)
    monkeypatch.setattr(image_cli.subprocess, 'run', checked)
    args = argparse.Namespace(stage=tmp_path, tools=root / 'pipeline/tools.lock.json',
                              policy=root / 'contracts/sources.json', lock=root / 'sources.lock.json',
                              sdk_python=Path('/synthetic/python'), service='foundation-smoke',
                              archive=tmp_path / 'image.tar')
    image_cli.export(args)
    assert [call[1] for call in calls] == ['version', 'run']


@pytest.mark.parametrize('kind', ['config', 'manifest'])
def test_loader_preserves_config_when_docker_uses_manifest_id(tmp_path, monkeypatch, kind):
    from qopenbb_ci import images
    expected = {'image_config_digest': 'sha256:' + '1' * 64,
                'image_manifest_digest': 'sha256:' + '2' * 64,
                'architecture': 'amd64', 'os': 'linux', 'labels': {'source': 'synthetic'}}
    loaded_id = expected['image_' + kind + '_digest']
    monkeypatch.setattr(images, 'inspect_archive', lambda *args: expected)
    def output(command, **kwargs):
        if command[2] == 'load':
            return 'Loaded image ID: ' + loaded_id + '\n'
        return json.dumps([{'Id': loaded_id, 'Architecture': 'amd64', 'Os': 'linux',
                            'Config': {'Labels': expected['labels']}, 'RepoDigests': []}])
    monkeypatch.setattr(images.subprocess, 'check_output', output)
    monkeypatch.setattr(images.subprocess, 'run', lambda *args, **kwargs: None)
    result = images.load(tmp_path / 'archive.tar', expected)
    assert result['loaded_image_id'] == loaded_id
    assert result['image_config_digest'] == 'sha256:' + '1' * 64
    assert result['registry_digest'] is None


def test_loader_rejects_arbitrary_loaded_id(tmp_path, monkeypatch):
    from qopenbb_ci import images
    expected = {'image_config_digest': 'sha256:' + '1' * 64, 'image_manifest_digest': 'sha256:' + '2' * 64}
    monkeypatch.setattr(images, 'inspect_archive', lambda *args: expected)
    monkeypatch.setattr(images.subprocess, 'check_output',
                        lambda *args, **kwargs: 'Loaded image ID: sha256:' + '3' * 64 + '\n')
    with pytest.raises(ValueError, match='does not match'):
        images.load(tmp_path / 'archive.tar', expected)


def test_invalid_archive_has_value_free_error_report(tmp_path, monkeypatch, capsys):
    from qopenbb_ci import image_cli
    target, report = tmp_path / 'invalid.tar', tmp_path / 'report.json'
    target.write_text('synthetic-private-value')
    monkeypatch.setattr('sys.argv', ['image_cli', 'inspect', '--archive', str(target), '--report', str(report)])
    assert image_cli.main() == 2
    assert json.loads(report.read_text()) == {'valid': False, 'error': 'ReadError'}
    assert 'synthetic-private-value' not in capsys.readouterr().out


@pytest.mark.parametrize('mutation', [
    'root_extra', 'source_extra', 'missing_license', 'boolean_version', 'bad_revision',
    'bad_digest', 'files_list', 'source_list', 'missing_smoke_hash',
    'unknown_source', 'bad_repository', 'float_version', 'uppercase_digest', 'duplicate_field',
    'unreadable_tree',
    'unlisted_empty_directory',
])
def test_export_rejects_invalid_provenance_before_any_dagger_call(tmp_path, monkeypatch, mutation):
    import argparse
    from qopenbb_ci import image_cli
    roots, policy, lock = inputs(tmp_path)
    destination = tmp_path / 'stage'
    result = stage(destination, roots, policy, lock)
    source = result['sources']['workspace']
    if mutation == 'root_extra':
        result['unexpected_metadata'] = 'SYNTHETIC_SECRET'
    elif mutation == 'source_extra':
        source['unexpected_metadata'] = 'SYNTHETIC_SECRET'
    elif mutation == 'missing_license':
        (destination / 'sources/workspace/LICENSE').unlink()
        del source['files']['LICENSE']
    elif mutation == 'boolean_version':
        result['schema_version'] = True
    elif mutation == 'bad_revision':
        source['revision'] = 123
    elif mutation == 'bad_digest':
        source['files']['LICENSE'] = 123
    elif mutation == 'files_list':
        source['files'] = []
    elif mutation == 'source_list':
        result['sources'] = []
    elif mutation == 'unknown_source':
        result['sources']['unreviewed'] = source
    elif mutation == 'bad_repository':
        source['repository'] = 123
    elif mutation == 'float_version':
        result['schema_version'] = 1.0
    elif mutation == 'uppercase_digest':
        source['files']['LICENSE'] = 'A' * 64
    elif mutation == 'unreadable_tree':
        import os
        import glob
        hidden = destination / 'unlisted'
        hidden.mkdir()
        (hidden / 'secret.txt').write_text('SYNTHETIC_SECRET')
        original_scandir = os.scandir
        def scandir(path):
            if Path(path) == hidden:
                raise PermissionError('synthetic unreadable directory')
            return original_scandir(path)
        monkeypatch.setattr(os, 'scandir', scandir)
        monkeypatch.setattr(glob._StringGlobber, 'scandir', staticmethod(scandir))
    elif mutation == 'unlisted_empty_directory':
        (destination / 'SYNTHETIC_SECRET').mkdir()
    elif mutation == 'duplicate_field':
        pass
    else:
        del result['smoke_sha256']
    content = json.dumps(result)
    if mutation == 'duplicate_field':
        content = content[:-1] + ', "service": "foundation-smoke"}'
    (destination / 'provenance.json').write_text(content)
    policy_path, lock_path = tmp_path / 'policy.json', tmp_path / 'lock.json'
    policy_path.write_text(json.dumps(policy))
    lock_path.write_text(json.dumps(lock))
    calls = []
    def forbidden(command, **kwargs):
        calls.append(command)
        raise AssertionError('export started a process before rejecting invalid provenance')
    monkeypatch.setattr(image_cli.subprocess, 'check_output', forbidden)
    monkeypatch.setattr(image_cli.subprocess, 'run', forbidden)
    args = argparse.Namespace(stage=destination, tools=Path(__file__).resolve().parents[2] / 'pipeline/tools.lock.json',
                              policy=policy_path, lock=lock_path, sdk_python=Path('/unused/python'),
                              service='foundation-smoke', archive=tmp_path / 'image.tar')
    with pytest.raises(ValueError) as caught:
        image_cli.export(args)
    assert 'SYNTHETIC_SECRET' not in str(caught.value)
    assert calls == []
