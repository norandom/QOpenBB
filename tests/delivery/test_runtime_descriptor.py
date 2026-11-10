import json
import os
import subprocess
import sys

import pytest

from qopenbb_ci import runtime_descriptor as descriptor
from qopenbb_ci import session_files as storage


def valid_descriptor(tmp_path, phase='ready'):
    identity = 'a' * 32
    name = 'qopenbb-browser-' + identity
    image = 'sha256:' + 'a' * 64
    labels = {'com.docker.compose.project': name, 'org.qopenbb.session': identity}
    containers = {service: {'id': 'b' * 64, 'labels': {
        **labels, 'com.docker.compose.service': service}}
        for service in ['workspace', 'data-api']}
    hashed_file = {'path': str(tmp_path / 'compose.yaml'), 'sha256': 'c' * 64}
    return dict(schema_version=1, session_id=identity, backend='compose', phase=phase,
                name=name, origin='http://127.0.0.1:8080', container='b' * 64,
                credentials={'email': 'disposable@example.test', 'password': 'private-password'},
                images={'workspace': image, 'data-api': image},
                image_metadata={key: {'manifest_digest': None, 'config_digest': image}
                                for key in ['workspace', 'data-api']},
                packaged_image_only=True, source_overlay=None, release_image_verified=False,
                project=name, connection={'endpoint': 'npipe:////./pipe/podman', 'identity': 'daemon-id'},
                resources={'containers': containers, 'networks': [{'id': 'd' * 64, 'labels': labels}]},
                state={'host_path': str(tmp_path), 'daemon_path': '/mnt/state',
                       'mount_identity': '/mnt/state', 'verified': True},
                compose={'project_directory': str(tmp_path), 'files': [hashed_file],
                         'environment_file': hashed_file})


@pytest.mark.parametrize('phase', ['prepared', 'starting', 'ready', 'recreating', 'failed', 'stopped'])
def test_lifecycle_and_financial_contract(tmp_path, phase):
    raw = valid_descriptor(tmp_path, phase)
    value = descriptor.parse_descriptor(json.dumps(raw).encode())
    assert value.model_dump(mode='json') == raw
    public = json.dumps(descriptor.public_projection(value))
    for secret in ['private-password', 'disposable@example.test', 'npipe:', str(tmp_path), 'daemon-id']:
        assert secret not in public


@pytest.mark.parametrize('mutation', [
    lambda d: d.pop('schema_version'), lambda d: d.update(schema_version=2),
    lambda d: d.update(schema_version=True), lambda d: d.update(unknown='private-password'),
    lambda d: d.update(phase='other'), lambda d: d.update(origin='http://example.com'),
    lambda d: d.update(origin='http://user:pass@127.0.0.1:8080'),
    lambda d: d.update(origin='http://127.0.0.1:8080/?token=secret'),
    lambda d: d.update(container=None), lambda d: d.update(credentials=None),
    lambda d: d.update(packaged_image_only=False), lambda d: d.update(release_image_verified=True),
    lambda d: d['images'].update(workspace='mutable:latest'),
    lambda d: d['resources']['containers']['workspace']['labels'].update({'org.qopenbb.session': 'wrong'}),
    lambda d: d['state'].update(verified=False),
    lambda d: d['compose']['files'][0].update(path='relative'),
])
def test_invalid_shape_is_secret_safe(tmp_path, mutation):
    raw = valid_descriptor(tmp_path)
    mutation(raw)
    with pytest.raises(descriptor.DescriptorError) as error:
        descriptor.parse_descriptor(json.dumps(raw).encode())
    assert str(error.value) == 'Invalid runtime descriptor'


def invoke(path, *arguments):
    return subprocess.run([sys.executable, '-B', '-m', 'qopenbb_ci.session_files',
                           'read', '--path', str(path), *arguments],
                          capture_output=True, timeout=20,
                          creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0)


def test_checked_private_ipc_and_public_cli(tmp_path):
    raw = valid_descriptor(tmp_path)
    with storage.create_session(tmp_path / 'private') as session:
        path = session.path / 'descriptor.json'
        session.create_file(path.name, json.dumps(raw).encode())
    result = invoke(path, '--private-ipc')
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout) == raw
    assert result.stderr == b''
    public = invoke(path)
    assert public.returncode == 0
    assert b'private-password' not in public.stdout
    assert json.loads(public.stdout) == descriptor.public_projection(descriptor.read_private(path))


@pytest.mark.parametrize('payload', [b'{private-password', b'{"schema_version":99,"password":"private-password"}'])
def test_private_ipc_rejects_malformed_without_payload(tmp_path, payload):
    with storage.create_session(tmp_path / 'private') as session:
        path = session.path / 'descriptor.json'
        session.create_file(path.name, payload)
    result = invoke(path, '--private-ipc')
    assert result.returncode != 0
    assert result.stdout == b''
    assert b'private-password' not in result.stderr


def test_private_ipc_rejects_unprotected_and_missing(tmp_path):
    path = tmp_path / 'descriptor.json'
    path.write_text(json.dumps(valid_descriptor(tmp_path)))
    for target in [path, tmp_path / 'missing-private-password']:
        result = invoke(target, '--private-ipc')
        assert result.returncode != 0
        assert result.stdout == b''
        assert str(target).encode() not in result.stderr


def test_private_ipc_refuses_terminal_before_read(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(sys.stdout, 'isatty', lambda: True)
    monkeypatch.setattr(storage, 'read_private', lambda *args: pytest.fail('read before terminal refusal'))
    assert storage.main(['read', '--private-ipc', '--path', str(tmp_path / 'missing')]) != 0
    assert capsys.readouterr().out == ''


def test_typed_replace_validates_before_mutation(tmp_path):
    with storage.create_session(tmp_path / 'private') as session:
        path = session.path / 'descriptor.json'
        session.create_file(path.name, json.dumps(valid_descriptor(tmp_path)).encode())
    value = descriptor.read_private(path)
    descriptor.replace_private(path, value)
    assert descriptor.read_private(path) == value
    with pytest.raises(descriptor.DescriptorError):
        descriptor.replace_private(path, value.model_copy(update={'phase': 'invalid'}))
    assert descriptor.read_private(path) == value


def test_prepared_allows_only_undiscovered_facts(tmp_path):
    raw = valid_descriptor(tmp_path, 'prepared')
    raw.update(origin=None, container=None, credentials=None)
    raw['resources'] = {'containers': {}, 'networks': []}
    raw['state'].update(verified=False, daemon_path=None, mount_identity=None)
    value = descriptor.parse_descriptor(json.dumps(raw).encode())
    assert value.phase == 'prepared'
    raw['phase'] = 'ready'
    with pytest.raises(descriptor.DescriptorError):
        descriptor.parse_descriptor(json.dumps(raw).encode())


@pytest.mark.parametrize('mutation', [
    lambda d: d['image_metadata']['workspace'].update(config_digest='sha256:' + 'e' * 64),
    lambda d: d['images'].pop('data-api'),
    lambda d: d['resources']['containers'].pop('data-api'),
    lambda d: d.update(container='e' * 64),
    lambda d: d.update(name='qopenbb-browser-other'),
    lambda d: d.update(packaged_image_only=1),
    lambda d: d.update(release_image_verified=0),
    lambda d: d['state'].update(host_path='D:/safe/../other'),
    lambda d: d['credentials'].update(token='private-password'),
])
def test_exact_ownership_and_image_pair(tmp_path, mutation):
    raw = valid_descriptor(tmp_path)
    mutation(raw)
    with pytest.raises(descriptor.DescriptorError):
        descriptor.parse_descriptor(json.dumps(raw).encode())


def test_ambiguous_json_rejected():
    with pytest.raises(descriptor.DescriptorError):
        descriptor.parse_descriptor(b'{"schema_version":1,"schema_version":2}')


def test_private_ipc_refuses_redirected_file(tmp_path):
    with storage.create_session(tmp_path / 'private') as session:
        path = session.path / 'descriptor.json'
        session.create_file(path.name, json.dumps(valid_descriptor(tmp_path)).encode())
    output = tmp_path / 'redirected.json'
    with output.open('wb') as stream:
        result = subprocess.run([sys.executable, '-B', '-m', 'qopenbb_ci.session_files',
                                 'read', '--private-ipc', '--path', str(path)],
                                stdout=stream, stderr=subprocess.PIPE, timeout=20,
                                creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0)
    assert result.returncode != 0
    assert output.read_bytes() == b''
    assert b'private-password' not in result.stderr


@pytest.mark.parametrize('arguments', [
    ['private-password', '--path', 'unused'],
    ['read', '--path', 'unused', '--private-password'],
])
def test_argument_errors_do_not_echo_private_input(arguments):
    result = subprocess.run([sys.executable, '-B', '-m', 'qopenbb_ci.session_files', *arguments],
                            capture_output=True, timeout=20,
                            creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0)
    assert result.returncode == 2
    assert result.stdout == b''
    assert b'private-password' not in result.stderr
