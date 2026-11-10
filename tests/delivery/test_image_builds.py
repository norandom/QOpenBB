"""Synthetic contracts for the task 1.8 image boundary."""

import json
from pathlib import Path
import subprocess
import io
import tarfile

import pytest

@pytest.fixture(autouse=True)
def synthetic_executable_selection(monkeypatch):
    from qopenbb_ci import container_command, image_cli
    monkeypatch.setenv('QOPENBB_CONTAINER_CLI', 'docker')
    monkeypatch.setattr(container_command, 'resolve_executable', lambda value: Path(value))
    monkeypatch.setattr(image_cli, 'resolve_executable', lambda value, **kwargs: Path(value))


from qopenbb_ci.container_command import resolve_executable as REAL_EXECUTABLE_RESOLVER
from qopenbb_ci.staging import stage, verify_stage
from qopenbb_ci.images import inspect_archive


def test_sdk_export_retains_virtual_environment_launch_path(explicit_export, monkeypatch, tmp_path):
    import sys
    image_cli, args, _, _, calls, _ = explicit_export
    sdk = tmp_path / 'sdk' / 'python.exe'
    sdk.parent.mkdir()
    sdk.touch()
    args.sdk_python = sdk
    original = Path.resolve
    monkeypatch.setattr(Path, 'resolve', lambda self, **kwargs:
                        Path(sys.executable) if self == sdk else original(self, **kwargs))
    monkeypatch.setattr(image_cli, 'resolve_executable', REAL_EXECUTABLE_RESOLVER)
    args.dagger_cli = Path(sys.executable)
    # Keep the synthetic CLI version response while using real executable validation.
    original_output = image_cli.subprocess.check_output
    monkeypatch.setattr(image_cli.subprocess, 'check_output', lambda command, **kwargs:
                        'dagger v0.21.8 synthetic' if command[1:] == ['version']
                        else original_output(command, **kwargs))
    image_cli.export(args)
    probe = next(command for command, _ in calls if '-c' in command)
    runner = next(command for command, _ in calls if command[1:3] == ['run', '--'])
    assert probe[0] == str(sdk.absolute())
    assert runner[3] == probe[0]


@pytest.mark.skipif(__import__('os').name == 'nt', reason='POSIX virtual environment symlinks')
def test_sdk_resolver_runs_symlinked_virtual_environment(tmp_path):
    import sys
    import venv
    environment = tmp_path / 'sdk'
    venv.EnvBuilder(with_pip=False, symlinks=True).create(environment)
    python = environment / 'bin/python'
    assert python.is_symlink()
    metadata = environment / f'lib/python{sys.version_info.major}.{sys.version_info.minor}/site-packages/dagger_io-0.21.8.dist-info'
    metadata.mkdir(parents=True)
    (metadata / 'METADATA').write_text('Metadata-Version: 2.1\nName: dagger-io\nVersion: 0.21.8\n')
    selected = REAL_EXECUTABLE_RESOLVER(str(python), preserve_symlinks=True)
    assert selected == python.absolute()
    observed = subprocess.check_output([str(selected), '-I', '-c',
        'import sys,importlib.metadata;print(sys.prefix);print(importlib.metadata.version("dagger-io"))'], text=True)
    assert observed.splitlines() == [str(environment), '0.21.8']


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
    try:
        (roots['workspace'] / 'terminalpro/link').symlink_to('/tmp')
    except OSError as error:
        if getattr(error, 'winerror', None) != 1314:
            raise
        pytest.skip('Windows fixture requires symbolic-link creation privilege')
    with pytest.raises(ValueError, match='symlink'):
        stage(tmp_path / 'stage', roots, policy, lock)


def test_missing_or_partial_stage_rejected_before_upload(tmp_path):
    with pytest.raises(FileNotFoundError):
        verify_stage(tmp_path / 'absent')
    partial = tmp_path / 'partial'
    partial.mkdir()
    with pytest.raises(FileNotFoundError):
        verify_stage(partial)
    try:
        (partial / 'provenance.json').symlink_to(tmp_path / 'unreadable-secret')
    except OSError as error:
        if getattr(error, 'winerror', None) != 1314:
            raise
        pytest.skip('Windows fixture requires symbolic-link creation privilege')
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
    forbidden_keys = ['PUBLICATION_PASSWORD', 'DAGGER_CLOUD_TOKEN', 'FMP_API_KEY',
                      'ANTHROPIC_API_KEY', 'DOCKER_CONTEXT']
    for key in forbidden_keys + ['DOCKER_CONFIG', '_EXPERIMENTAL_DAGGER_RUNNER_HOST']:
        monkeypatch.setenv(key, 'synthetic-private-caller-value')
    monkeypatch.setattr(image_cli, 'verify_stage', lambda *args: {'sources': {}})
    monkeypatch.setattr(image_cli, 'inspect_archive', lambda *args: {})
    monkeypatch.setattr(image_cli, 'verify_engine', lambda *args: {'image_id': 'synthetic'})
    calls = []
    def checked(command, **kwargs):
        environment = kwargs['env']
        assert not set(forbidden_keys).intersection(environment)
        assert 'synthetic-private-caller-value' not in environment.values()
        assert environment['_EXPERIMENTAL_DAGGER_RUNNER_HOST'].startswith('docker-image://')
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
@pytest.mark.parametrize('announcement', ['Loaded image ID: ', 'Loaded image: '])
def test_loader_preserves_config_when_docker_uses_manifest_id(tmp_path, monkeypatch, kind, announcement):
    from qopenbb_ci import images
    monkeypatch.setenv('QOPENBB_CONTAINER_CLI', 'C:/container tools/podman.exe')
    expected = {'image_config_digest': 'sha256:' + '1' * 64,
                'image_manifest_digest': 'sha256:' + '2' * 64,
                'architecture': 'amd64', 'os': 'linux', 'labels': {'source': 'synthetic'}}
    loaded_id = expected['image_' + kind + '_digest']
    monkeypatch.setattr(images, 'inspect_archive', lambda *args: expected)
    def output(command, **kwargs):
        assert command[0] == str(Path('C:/container tools/podman.exe'))
        if command[2] == 'load':
            return announcement + loaded_id + '\n'
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


@pytest.mark.parametrize('store', ['classic', 'containerd'])
@pytest.mark.parametrize('mutation,code', [
    (None, None),
    ('configured', 'engine_configured_reference_mismatch'),
    ('digest', 'engine_locked_digest_missing'),
    ('identity', 'engine_image_identity_mismatch'),
    ('stopped', 'engine_not_running'),
    ('missing_field', 'engine_inspection_invalid'),
    ('missing_image', 'engine_inspection_failed'),
    ('malformed_json', 'engine_inspection_invalid'),
])
def test_engine_verifies_resolved_pinned_identity(monkeypatch, store, mutation, code):
    from qopenbb_ci import image_cli
    digest = 'sha256:' + '1' * 64
    reference = 'registry.example:5000/engine:v1@' + digest
    identity = 'sha256:' + ('2' * 64 if store == 'classic' else '1' * 64)
    observed = {'Id': 'container-id', 'Image': identity,
                'Config': {'Image': reference}, 'State': {'Running': True}}
    image = {'Id': identity, 'RepoDigests': ['registry.example:5000/engine@' + digest]}
    if mutation == 'configured':
        observed['Config']['Image'] = 'registry.example/engine:mutable'
    elif mutation == 'digest':
        image['RepoDigests'] = ['registry.example:5000/engine@sha256:' + '3' * 64]
    elif mutation == 'identity':
        observed['Image'] = 'sha256:' + '3' * 64
    elif mutation == 'stopped':
        observed['State']['Running'] = False
    elif mutation == 'missing_field':
        del image['Id']
    calls = []
    def output(command, **kwargs):
        calls.append(command)
        if command[1] == 'image' and mutation == 'missing_image':
            raise subprocess.CalledProcessError(1, command, output='synthetic-private-value')
        if mutation == 'malformed_json':
            return 'synthetic-private-value'
        return json.dumps([observed if command[1] == 'container' else image])
    monkeypatch.setattr(image_cli.subprocess, 'check_output', output)
    if code:
        with pytest.raises(image_cli.EngineVerificationError, match=code):
            image_cli.verify_engine(reference)
    else:
        result = image_cli.verify_engine(reference)
        assert result['image_id'] == identity
        assert result['verified_repository_digest'] == image['RepoDigests'][0]
        assert calls == [['docker', 'container', 'inspect', 'dagger-engine-' + '1' * 16],
                         ['docker', 'image', 'inspect', reference]]


def test_engine_failure_report_preserves_safe_diagnostic(tmp_path, monkeypatch, capsys):
    from qopenbb_ci import image_cli
    report = tmp_path / 'report.json'
    monkeypatch.setattr('sys.argv', ['image_cli', 'export', '--stage', str(tmp_path),
                                   '--tools', 'unused', '--lock', 'unused', '--policy', 'unused',
                                   '--sdk-python', 'unused', '--archive', 'unused', '--report', str(report)])
    def fail(args):
        raise image_cli.EngineVerificationError('engine_image_identity_mismatch')
    monkeypatch.setattr(image_cli, 'export', fail)
    assert image_cli.main() == 2
    assert json.loads(report.read_text()) == {
        'valid': False, 'error': 'EngineVerificationError', 'error_code': 'engine_image_identity_mismatch'}
    assert 'engine_image_identity_mismatch' in capsys.readouterr().out


@pytest.mark.parametrize('reference', ['engine:latest', 'engine@sha256:short', 'engine@sha256:' + 'A' * 64])
def test_engine_rejects_unpinned_reference_without_inspecting(monkeypatch, reference):
    from qopenbb_ci import image_cli
    def forbidden(*args, **kwargs):
        raise AssertionError('invalid reference reached Docker')
    monkeypatch.setattr(image_cli.subprocess, 'check_output', forbidden)
    with pytest.raises(image_cli.EngineVerificationError, match='engine_reference_invalid'):
        image_cli.verify_engine(reference)


def test_invalid_archive_has_value_free_error_report(tmp_path, monkeypatch, capsys):
    from qopenbb_ci import image_cli
    target, report = tmp_path / 'invalid.tar', tmp_path / 'report.json'
    target.write_text('synthetic-private-value')
    monkeypatch.setattr('sys.argv', ['image_cli', 'inspect', '--archive', str(target), '--report', str(report)])
    assert image_cli.main() == 2
    assert json.loads(report.read_text()) == {'valid': False, 'error': 'ReadError'}
    assert 'synthetic-private-value' not in capsys.readouterr().out


@pytest.mark.parametrize('engine_container', [None, 'qopenbb-dagger-engine-synthetic'])
@pytest.mark.parametrize('mutation', [
    'root_extra', 'source_extra', 'missing_license', 'boolean_version', 'bad_revision',
    'bad_digest', 'files_list', 'source_list', 'missing_smoke_hash',
    'unknown_source', 'bad_repository', 'float_version', 'uppercase_digest', 'duplicate_field',
    'unreadable_tree',
    'unlisted_empty_directory',
])
def test_export_rejects_invalid_provenance_before_any_dagger_call(tmp_path, monkeypatch, mutation, engine_container):
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
                              service='foundation-smoke', archive=tmp_path / 'image.tar',
                              engine_container=engine_container)
    with pytest.raises(ValueError) as caught:
        image_cli.export(args)
    assert 'SYNTHETIC_SECRET' not in str(caught.value)
    assert calls == []


ENGINE_NAME = 'qopenbb-dagger-engine-synthetic'


@pytest.fixture
def explicit_export(tmp_path, monkeypatch):
    import argparse
    from qopenbb_ci import image_cli
    root = Path(__file__).resolve().parents[2]
    tools = image_cli.read(root / 'pipeline/tools.lock.json')
    reference = tools['base_images']['dagger_engine']
    repository, digest = reference.rsplit('@', 1)
    repository = repository.rsplit(':', 1)[0]
    observed = {'Id': 'a' * 64, 'Name': '/' + ENGINE_NAME, 'Image': 'sha256:' + '2' * 64,
                'Config': {'Image': reference, 'Labels': {
                    'org.qopenbb.owner': 'qopenbb', 'org.qopenbb.purpose': 'dagger-engine'}},
                'State': {'Running': True}}
    image = {'Id': observed['Image'], 'RepoDigests': [repository + '@' + digest]}
    args = argparse.Namespace(stage=tmp_path, tools=root / 'pipeline/tools.lock.json',
                              policy=root / 'contracts/sources.json', lock=root / 'sources.lock.json',
                              sdk_python=Path('/synthetic/python'), service='foundation-smoke',
                              archive=tmp_path / 'image.tar', engine_container=ENGINE_NAME)
    monkeypatch.setattr(image_cli, 'verify_stage', lambda *args: {'sources': {}})
    monkeypatch.setattr(image_cli, 'inspect_archive', lambda *args: {})
    calls = []
    def output(command, **kwargs):
        calls.append((command, kwargs))
        if command[0] == 'docker':
            assert kwargs['stderr'] == subprocess.PIPE
            return json.dumps([observed if command[1] == 'container' else image])
        return 'dagger v0.21.8 synthetic ' if command[0] == 'dagger' else '0.21.8'
    monkeypatch.setattr(image_cli.subprocess, 'check_output', output)
    monkeypatch.setattr(image_cli.subprocess, 'run', output)
    return image_cli, args, observed, image, calls, output


@pytest.mark.parametrize('store', ['classic', 'containerd'])
def test_explicit_engine_uses_one_private_environment_for_inspections_and_runner(explicit_export, monkeypatch, store):
    image_cli, args, observed, image, calls, output = explicit_export
    for key in ['PUBLICATION_PASSWORD', 'DAGGER_CLOUD_TOKEN', 'FMP_API_KEY', 'ANTHROPIC_API_KEY',
                'DOCKER_CONTEXT', 'DOCKER_CONFIG', '_EXPERIMENTAL_DAGGER_RUNNER_HOST']:
        monkeypatch.setenv(key, 'synthetic-private-caller-value')
    monkeypatch.setenv('DOCKER_HOST', 'unix:///synthetic-owned-daemon.sock')
    if store == 'containerd':
        observed['Image'] = image['Id'] = image['RepoDigests'][0].split('@')[1]
    active_homes = []
    def checked(command, **kwargs):
        if command[0] == 'docker' or command[:2] == ['dagger', 'run']:
            env = kwargs['env']
            assert Path(env['HOME']).is_dir()
            assert env['HOME'] == env['DOCKER_CONFIG']
            assert list(Path(env['HOME']).iterdir()) == []
            assert env['DOCKER_HOST'] == 'unix:///synthetic-owned-daemon.sock'
            assert 'DOCKER_CONTEXT' not in env
            assert 'synthetic-private-caller-value' not in env.values()
            active_homes.append(env['HOME'])
        return output(command, **kwargs)
    monkeypatch.setattr(image_cli.subprocess, 'check_output', checked)
    monkeypatch.setattr(image_cli.subprocess, 'run', checked)
    result = image_cli.export(args)
    selected = [(command, kwargs['env']) for command, kwargs in calls
                if command[0] == 'docker' or command[:2] == ['dagger', 'run']]
    assert len(selected) == 5
    assert all(env == selected[0][1] for _, env in selected)
    assert selected[0][1]['_EXPERIMENTAL_DAGGER_RUNNER_HOST'] == 'docker-container://' + ENGINE_NAME
    assert [command[:3] for command, _ in selected] == [
        ['docker', 'container', 'inspect'], ['docker', 'image', 'inspect'],
        ['dagger', 'run', '--'], ['docker', 'container', 'inspect'], ['docker', 'image', 'inspect']]
    assert len(set(active_homes)) == 1 and not Path(active_homes[0]).exists()
    assert result['engine_observed']['container_id'] == observed['Id']


@pytest.mark.parametrize('name', ['', 'dagger-engine-shared', 'docker-container://owned',
                                  ENGINE_NAME + ' ', ENGINE_NAME + '/bad',
                                  'qopenbb-dagger-engine-A', 'qopenbb-dagger-engine-' + 'a' * 65])
def test_explicit_engine_rejects_names_before_any_process(explicit_export, name):
    image_cli, args, _, _, calls, _ = explicit_export
    args.engine_container = name
    with pytest.raises(image_cli.EngineVerificationError, match='engine_container_invalid'):
        image_cli.export(args)
    assert calls == []


@pytest.mark.parametrize('mutation,code', [
    ('name', 'engine_container_invalid'), ('owner', 'engine_ownership_mismatch'),
    ('purpose', 'engine_ownership_mismatch'), ('labels', 'engine_ownership_mismatch'),
    ('configured', 'engine_configured_reference_mismatch'), ('mutable', 'engine_configured_reference_mismatch'),
    ('digest', 'engine_locked_digest_missing'), ('identity', 'engine_image_identity_mismatch'),
    ('stopped', 'engine_not_running'), ('missing', 'engine_inspection_failed'),
    ('malformed', 'engine_inspection_invalid'), ('id', 'engine_inspection_invalid'),
])
def test_explicit_engine_fails_closed_before_dagger_run(explicit_export, monkeypatch, mutation, code):
    image_cli, args, observed, image, calls, output = explicit_export
    if mutation == 'name':
        observed['Name'] += '-replacement'
    elif mutation in ['owner', 'purpose']:
        observed['Config']['Labels']['org.qopenbb.' + mutation] = 'another-project'
    elif mutation == 'labels':
        observed['Config']['Labels'] = {}
    elif mutation in ['configured', 'mutable']:
        observed['Config']['Image'] = 'engine:latest' if mutation == 'mutable' else 'engine@sha256:' + '4' * 64
    elif mutation == 'digest':
        image['RepoDigests'] = []
    elif mutation == 'identity':
        observed['Image'] = 'sha256:' + '4' * 64
    elif mutation == 'stopped':
        observed['State']['Running'] = False
    elif mutation == 'id':
        observed['Id'] = 'short-id'
    def checked(command, **kwargs):
        if command[0] == 'docker' and mutation == 'missing':
            raise subprocess.CalledProcessError(1, command, stderr='synthetic-private-inspect')
        if command[0] == 'docker' and mutation == 'malformed':
            return 'synthetic-private-inspect'
        return output(command, **kwargs)
    monkeypatch.setattr(image_cli.subprocess, 'check_output', checked)
    with pytest.raises(image_cli.EngineVerificationError, match=code):
        image_cli.export(args)
    assert not any(command[:2] == ['dagger', 'run'] for command, _ in calls)


@pytest.mark.parametrize('mutation,code', [('replacement', 'engine_instance_changed'),
                                         ('ownership', 'engine_ownership_mismatch')])
def test_explicit_engine_rechecks_identity_after_export(explicit_export, monkeypatch, mutation, code):
    image_cli, args, observed, _, _, output = explicit_export
    def run(command, **kwargs):
        result = output(command, **kwargs)
        if mutation == 'replacement':
            observed['Id'] = 'b' * 64
        else:
            observed['Config']['Labels']['org.qopenbb.owner'] = 'another-project'
        return result
    monkeypatch.setattr(image_cli.subprocess, 'run', run)
    with pytest.raises(image_cli.EngineVerificationError, match=code):
        image_cli.export(args)


def test_explicit_inspect_failure_does_not_publish_stderr(explicit_export, monkeypatch, capsys):
    image_cli, args, _, _, _, output = explicit_export
    args.command, args.report = 'export', args.stage / 'report.json'
    monkeypatch.setattr(image_cli.argparse.ArgumentParser, 'parse_args', lambda *a: args)
    def checked(command, **kwargs):
        if command[0] == 'docker':
            assert kwargs['stderr'] == subprocess.PIPE
            raise subprocess.CalledProcessError(1, command, stderr='synthetic-private-inspect')
        return output(command, **kwargs)
    monkeypatch.setattr(image_cli.subprocess, 'check_output', checked)
    assert image_cli.main() == 2
    captured = capsys.readouterr()
    assert 'synthetic-private-inspect' not in captured.out + captured.err + args.report.read_text()
    assert json.loads(args.report.read_text())['error_code'] == 'engine_inspection_failed'


def test_engine_container_option_is_export_only():
    from qopenbb_ci import image_cli
    args = image_cli.parser().parse_args(['export', '--stage', 'stage', '--tools', 'tools',
        '--lock', 'lock', '--policy', 'policy', '--sdk-python', 'python', '--archive', 'archive',
        '--report', 'report', '--engine-container', ENGINE_NAME])
    assert args.engine_container == ENGINE_NAME
    with pytest.raises(SystemExit):
        image_cli.parser().parse_args(['inspect', '--archive', 'archive', '--report', 'report',
                                     '--engine-container', ENGINE_NAME])

def test_source_root_uses_filesystem_identity_not_git_path_spelling(tmp_path, monkeypatch):
    from qopenbb_ci import sources
    root = tmp_path / 'checkout with spaces'
    root.mkdir()
    entry = {'repository': 'https://github.com/norandom/workspace.git', 'revision': 'a' * 40}
    replies = {'--show-toplevel': root.as_posix(), 'origin': entry['repository'],
               'HEAD': entry['revision'], '--untracked-files=no': ''}
    monkeypatch.setattr(sources, 'git', lambda path, *args: replies[args[-1]])
    assert sources.identity(root, entry) == entry

@pytest.mark.parametrize('version', ['0.21.11', '0.21.80'])
def test_native_export_rejects_wrong_cli_before_runner(explicit_export, monkeypatch, version):
    image_cli, args, _, _, calls, output = explicit_export
    args.dagger_cli = Path('C:/native tools/dagger.exe')
    def checked(command, **kwargs):
        if command[:2] == [str(args.dagger_cli), 'version']:
            return 'dagger v' + version + ' synthetic '
        return output(command, **kwargs)
    monkeypatch.setattr(image_cli.subprocess, 'check_output', checked)
    with pytest.raises(ValueError, match='CLI version'):
        image_cli.export(args)
    assert not any('run' in command for command, _ in calls)


def test_native_export_uses_explicit_executable_podman_transport_and_system_environment(explicit_export, monkeypatch):
    image_cli, args, _, _, calls, output = explicit_export
    args.dagger_cli = Path('C:/native tools/dagger.exe')
    monkeypatch.setenv('QOPENBB_CONTAINER_CLI', 'C:/container tools/podman.exe')
    monkeypatch.setenv('SystemRoot', 'C:/Windows')
    monkeypatch.setenv('CONTAINER_HOST', 'ssh://selected-daemon')
    monkeypatch.setenv('TEMP', str(args.stage))
    def checked(command, **kwargs):
        if command[0] == str(args.dagger_cli):
            calls.append((command, kwargs))
            return 'dagger v0.21.8 synthetic '
        if command[0] == str(Path('C:/container tools/podman.exe')):
            return output(['docker', *command[1:]], **kwargs)
        return output(command, **kwargs)
    monkeypatch.setattr(image_cli.subprocess, 'check_output', checked)
    monkeypatch.setattr(image_cli.subprocess, 'run', checked)
    image_cli.export(args)
    runner = next((command, options) for command, options in calls if command[1] == 'run')
    assert runner[0][0] == str(args.dagger_cli)
    assert runner[1]['env']['_EXPERIMENTAL_DAGGER_RUNNER_HOST'] == 'container+podman://' + ENGINE_NAME
    for key in ('SystemRoot', 'CONTAINER_HOST', 'TEMP'):
        assert runner[1]['env'][key] == __import__('os').environ[key]
    assert runner[1]['env']['FORCE_DARK_MODE'] == '1'
    expected_flags = subprocess.CREATE_NO_WINDOW if __import__('os').name == 'nt' else 0
    assert runner[1]['creationflags'] == expected_flags


def test_native_podman_requires_owned_engine_before_process(explicit_export, monkeypatch):
    image_cli, args, _, _, calls, _ = explicit_export
    args.engine_container = None
    monkeypatch.setenv('QOPENBB_CONTAINER_CLI', 'C:/container tools/podman.exe')
    with pytest.raises(image_cli.EngineVerificationError, match='engine_container_required'):
        image_cli.export(args)
    assert calls == []


@pytest.mark.parametrize('module_name', ['catalog_runtime', 'publication'])
def test_container_adapters_preserve_selected_executable_and_literal_arguments(monkeypatch, module_name):
    import importlib
    module = importlib.import_module('qopenbb_ci.' + module_name)
    selected = str(Path('C:/container tools/podman.exe'))
    monkeypatch.setenv('QOPENBB_CONTAINER_CLI', selected)
    observed = []
    def run(command, **options):
        observed.append((command, options))
        return subprocess.CompletedProcess(command, 0, stdout='synthetic', stderr='')
    monkeypatch.setattr(module.subprocess, 'run', run)
    assert module.docker('image', 'inspect', 'literal;$(no shell)') == 'synthetic'
    assert observed[0][0] == [selected, 'image', 'inspect', 'literal;$(no shell)']
    assert not observed[0][1].get('shell', False)


def test_native_export_rejects_wrong_sdk_without_cli_execution(explicit_export, monkeypatch):
    image_cli, args, _, _, calls, _ = explicit_export
    monkeypatch.setattr(image_cli.subprocess, 'check_output', lambda *a, **kw: '0.21.11')
    with pytest.raises(ValueError, match='SDK version'):
        image_cli.export(args)
    assert calls == []


def test_native_export_rejects_shell_wrapper_before_process(explicit_export, monkeypatch, tmp_path):
    image_cli, args, _, _, calls, _ = explicit_export
    wrapper = tmp_path / 'dagger.cmd'
    wrapper.write_text('@echo forbidden')
    args.dagger_cli = wrapper
    monkeypatch.setattr(image_cli, 'resolve_executable', REAL_EXECUTABLE_RESOLVER)
    with pytest.raises(ValueError, match='shell wrapper'):
        image_cli.export(args)
    assert calls == []

@pytest.mark.parametrize('status', [' M tracked.py', 'M  tracked.py'])
def test_source_rejects_modified_tracked_files_after_normalizing_root(tmp_path, monkeypatch, status):
    from qopenbb_ci import sources
    root = tmp_path / 'checkout'
    root.mkdir()
    entry = {'repository': 'https://github.com/norandom/workspace.git', 'revision': 'a' * 40}
    replies = {'--show-toplevel': root.as_posix(), 'origin': entry['repository'],
               'HEAD': entry['revision'], '--untracked-files=no': status}
    monkeypatch.setattr(sources, 'git', lambda path, *args: replies[args[-1]])
    with pytest.raises(ValueError, match='tracked source'):
        sources.identity(root, entry)

@pytest.mark.parametrize('formatting', ['podman', 'docker-prefix', 'mixed-prefix'])
def test_owned_engine_accepts_equivalent_native_inspection_forms(monkeypatch, formatting):
    from qopenbb_ci import image_cli
    name = 'qopenbb-dagger-engine-native-qualification-20261110122244'
    reference = 'registry.dagger.io/engine:v0.21.8@sha256:c9c1a0a6546380983d42e8d75adde070a2a0935c54b498d8bc9045d9cb2ee336'
    canonical = reference.replace(':v0.21.8@', '@')
    image_id = '9f1537a7b5dff83c5404f199cbf73d3023bf5af0a2f3ffada4b68e26194a714f'
    # These identity fields were observed in the qualification engine's Podman
    # inspection payload, not inferred from Docker-shaped fixtures.
    observed = {'Id': '8c14466951bf9ed3b5cbb31fbe971b0ede3e9ff9dd9bcd7ee2fe728898a96c13',
                'Name': name, 'Image': image_id, 'State': {'Running': True},
                'Config': {'Image': canonical, 'Labels': {
                    'org.qopenbb.owner': 'qopenbb', 'org.qopenbb.purpose': 'dagger-engine',
                    'org.qopenbb.session': name}}}
    image = {'Id': image_id, 'RepoDigests': [canonical]}
    if formatting != 'podman':
        observed['Name'] = '/' + name
        observed['Image'] = 'sha256:' + image_id
    if formatting == 'docker-prefix':
        image['Id'] = 'sha256:' + image_id
        observed['Config']['Image'] = reference
    monkeypatch.setattr(image_cli.subprocess, 'check_output', lambda command, **kw:
                        json.dumps([observed if command[1] == 'container' else image]))
    result = image_cli.verify_engine(reference, name, None, observed['Id'])
    assert result['container_id'] == observed['Id']
    assert result['verified_repository_digest'] == canonical
    assert result['image_id'].removeprefix('sha256:') == image_id


@pytest.mark.parametrize('mutation,code', [
    ('name', 'engine_container_invalid'), ('digest', 'engine_configured_reference_mismatch'),
    ('repository', 'engine_configured_reference_mismatch'), ('image', 'engine_image_identity_mismatch'),
    ('replacement', 'engine_instance_changed'), ('running', 'engine_not_running'),
    ('malformed_image', 'engine_inspection_invalid')])
def test_native_engine_normalization_retains_exact_identity_guards(explicit_export, monkeypatch, mutation, code):
    image_cli, args, observed, image, _, _ = explicit_export
    reference = observed['Config']['Image']
    observed['Name'] = args.engine_container
    observed['Config']['Image'] = reference.replace(':v0.21.8@', '@')
    expected_id = observed['Id']
    if mutation == 'name':
        observed['Name'] = '//' + args.engine_container
    elif mutation == 'digest':
        observed['Config']['Image'] = observed['Config']['Image'].split('@')[0] + '@sha256:' + 'f' * 64
    elif mutation == 'repository':
        observed['Config']['Image'] = 'unowned.example/engine@' + reference.split('@')[1]
    elif mutation == 'image':
        observed['Image'] = 'sha256:' + 'f' * 64
    elif mutation == 'replacement':
        observed['Id'] = 'b' * 64
    elif mutation == 'running':
        observed['State']['Running'] = 1
    elif mutation == 'malformed_image':
        observed['Image'] = image['Id'] = 'sha256:short'
    monkeypatch.setattr(image_cli.subprocess, 'check_output', lambda command, **kw:
                        json.dumps([observed if command[1] == 'container' else image]))
    with pytest.raises(image_cli.EngineVerificationError, match=code):
        image_cli.verify_engine(reference, args.engine_container, None, expected_id)

@pytest.mark.parametrize('mutation', [None, 'inspected_id', 'labels', 'saved_config'])
def test_loader_normalizes_observed_podman_id_without_losing_config_proof(tmp_path, monkeypatch, mutation):
    from qopenbb_ci import images
    digest = '87d67aca398f8d3115666245dfc103a8f14a367ec60f8e2ea02ee46ae8435ca6'
    config = 'sha256:' + digest
    expected = {'image_config_digest': config,
                'image_manifest_digest': 'sha256:71768c590cd37e604f152038903baf3c1a70f0b676e74d07288e16b3d1c50ef7',
                'architecture': 'amd64', 'os': 'linux', 'labels': {'org.qopenbb.scope': 'foundation-only'}}
    # Podman qualification observed the announcement prefixed and inspect Id bare.
    loaded = {'Id': digest, 'Architecture': 'amd64', 'Os': 'linux',
              'Config': {'Labels': dict(expected['labels'])}, 'RepoDigests': []}
    if mutation == 'inspected_id':
        loaded['Id'] = 'f' * 64
    elif mutation == 'labels':
        loaded['Config']['Labels']['org.qopenbb.scope'] = 'different'
    inspected, saved = [], []
    def inspect(path):
        inspected.append(path)
        if path.name == 'loaded.tar' and mutation == 'saved_config':
            return {**expected, 'image_config_digest': 'sha256:' + 'f' * 64}
        return expected
    monkeypatch.setattr(images, 'inspect_archive', inspect)
    monkeypatch.setattr(images.subprocess, 'check_output', lambda command, **kw:
                        'Loaded image: ' + config + '\n' if command[2] == 'load' else json.dumps([loaded]))
    monkeypatch.setattr(images.subprocess, 'run', lambda command, **kw: saved.append(command))
    if mutation is not None:
        with pytest.raises(ValueError, match='differ'):
            images.load(tmp_path / 'image.tar', expected)
        assert bool(saved) is (mutation == 'saved_config')
        assert (inspected[-1].name == 'loaded.tar') is (mutation == 'saved_config')
        return
    result = images.load(tmp_path / 'image.tar', expected)
    assert result['loaded_image_id'] == config
    assert result['image_config_digest'] == config
    assert saved[0][1:3] == ['image', 'save']
    assert saved[0][-1] == config
    assert [path.name for path in inspected] == ['image.tar', 'loaded.tar']
