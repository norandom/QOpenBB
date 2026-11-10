import copy
from pathlib import Path
import pytest
from qopenbb_ci.compose_runtime import validate_config, checked_container


def config(state):
    return {'services': {'workspace': {'image': 'sha256:' + 'a'*64, 'ports': [{'host_ip': '127.0.0.1', 'target': 3000, 'published': '23456', 'protocol': 'tcp'}], 'volumes': [{'type': 'bind', 'source': str(state), 'target': '/data'}]}, 'data-api': {'image': 'sha256:' + 'b'*64}}, 'networks': {'default': {}}}


def test_exact_isolated_config(tmp_path):
    validate_config(config(tmp_path), {'workspace': 'sha256:'+'a'*64, 'data-api': 'sha256:'+'b'*64}, tmp_path, 23456)


@pytest.mark.parametrize('mutation', ['public', 'extra_port', 'state', 'build', 'extra_service', 'named_volume', 'extra_mount', 'data_port', 'image'])
def test_reject_unsafe_merge(tmp_path, mutation):
    value = copy.deepcopy(config(tmp_path))
    workspace = value['services']['workspace']
    if mutation == 'public': workspace['ports'][0]['host_ip'] = '0.0.0.0'
    if mutation == 'extra_port': workspace['ports'].append(dict(workspace['ports'][0]))
    if mutation == 'state': workspace['volumes'][0]['source'] = str(tmp_path / 'other')
    if mutation == 'build': workspace['build'] = '.'
    if mutation == 'extra_service': value['services']['notebook'] = {}
    if mutation == 'named_volume': value['volumes'] = {'data': {}}
    if mutation == 'extra_mount': workspace['volumes'].append({'type': 'bind', 'source': '/repo', 'target': '/opt/code'})
    if mutation == 'data_port': value['services']['data-api']['ports'] = [{'target': 6900}]
    if mutation == 'image': workspace['image'] = 'mutable:latest'
    with pytest.raises(ValueError):
        validate_config(value, {'workspace': 'sha256:'+'a'*64, 'data-api': 'sha256:'+'b'*64}, tmp_path, 23456)


def test_container_rejects_wrong_image_and_labels():
    with pytest.raises(ValueError):
        checked_container({'Id': 'a'*64, 'Image': 'sha256:'+'c'*64, 'Config': {'Labels': {}}}, 'workspace', 'qopenbb-browser-'+'d'*32, 'd'*32, 'sha256:'+'b'*64)

def test_prepared_descriptor_precedes_resource_creation(tmp_path, monkeypatch):
    import json
    from qopenbb_ci.compose_runtime import prepare, StartRequest, ComposeRuntime
    from qopenbb_ci.native_environment import NativeEnvironment
    from qopenbb_ci.runtime_descriptor import read_private
    from qopenbb_ci import compose_runtime
    repository = Path(__file__).resolve().parents[2]
    session = tmp_path / 'new-session' / 'descriptor.json'
    native = NativeEnvironment(repository, tmp_path, {}, {'CONTAINER_HOST': 'test://owned'})
    calls = []
    monkeypatch.setattr(compose_runtime, 'validate_output', lambda value: value)
    def command(self, arguments, **kwargs):
        calls.append(arguments)
        if arguments[:2] == ['image', 'inspect']:
            digest = 'a' if arguments[2] == 'workspace' else 'b'
            return json.dumps([{'Id': 'sha256:'+digest*64}])
        if arguments[0] == 'info': return json.dumps({'ID': 'owned-daemon'})
        descriptor = read_private(session)
        assert descriptor.phase == 'prepared'
        assert arguments[-3:] == ['config', '--format', 'json']
        return json.dumps(config(Path(descriptor.state.host_path)))
    monkeypatch.setattr(ComposeRuntime, 'command', command)
    runtime = prepare(StartRequest(native, session, 'workspace', 'data', 23456))
    assert runtime.descriptor.phase == 'prepared'
    assert not any('up' in call for call in calls)
    assert read_private(session).resources.containers == {}


def test_readiness_failure_retains_failed_descriptor(tmp_path, monkeypatch):
    import json
    from qopenbb_ci.compose_runtime import prepare, StartRequest, ComposeRuntime
    from qopenbb_ci.native_environment import NativeEnvironment
    from qopenbb_ci.runtime_descriptor import read_private
    from qopenbb_ci import compose_runtime
    native = NativeEnvironment(Path(__file__).resolve().parents[2], tmp_path, {}, {'CONTAINER_HOST': 'test://owned'})
    session = tmp_path / 'new-session' / 'descriptor.json'
    monkeypatch.setattr(compose_runtime, 'validate_output', lambda value: value)
    def command(self, arguments, **kwargs):
        if arguments[:2] == ['image', 'inspect']:
            return json.dumps([{'Id': 'sha256:'+('a' if arguments[2] == 'workspace' else 'b')*64}])
        if arguments[0] == 'info': return json.dumps({'ID': 'owned-daemon'})
        if 'config' in arguments: return json.dumps(config(Path(read_private(session).state.host_path)))
        if 'up' in arguments: raise ValueError('private error must not escape')
        return ''
    monkeypatch.setattr(ComposeRuntime, 'command', command)
    runtime = prepare(StartRequest(native, session, 'workspace', 'data', 23456))
    with pytest.raises(ValueError, match='protected recovery descriptor retained') as caught:
        runtime.begin()
    assert 'private error' not in str(caught.value)
    assert read_private(session).phase == 'failed'

def test_reject_changed_generated_configuration_before_up(tmp_path, monkeypatch):
    from types import SimpleNamespace
    from qopenbb_ci.compose_runtime import ComposeRuntime
    runtime = ComposeRuntime(None, tmp_path / 'descriptor')
    runtime.descriptor = SimpleNamespace(compose=SimpleNamespace(files=[SimpleNamespace(path=str(tmp_path/'missing'), sha256='a'*64)], environment_file=None))
    with pytest.raises(ValueError, match='configuration identity'):
        runtime.verify_configuration()

def test_podman_bare_image_identity_normalizes_digest():
    import json
    from types import SimpleNamespace
    from qopenbb_ci.compose_runtime import image_identity
    runtime = SimpleNamespace(command=lambda args: json.dumps([{'Id': 'a'*64}]))
    digest, metadata = image_identity(runtime, 'approved')
    assert digest == 'sha256:'+'a'*64
    assert metadata['config_digest'] == digest

def test_mapping_rejects_wrong_sentinel(tmp_path):
    from types import SimpleNamespace
    from qopenbb_ci.compose_readiness import verify_mapping
    from qopenbb_ci import session_files
    state = tmp_path / 'private-state'
    with session_files.create_session(state) as directory:
        directory.create_file('qopenbb-sentinel', b'expected')
    descriptor = SimpleNamespace(state=SimpleNamespace(host_path=str(state)), container='owned', session_id='expected')
    runtime = SimpleNamespace(descriptor=descriptor, command=lambda args: 'wrong', save=lambda **kwargs: pytest.fail('must not save verified mapping'))
    workspace = {'Mounts': [{'Type': 'bind', 'Destination': '/data', 'RW': True, 'Source': '/daemon/owned'}]}
    with pytest.raises(ValueError, match='sentinel mismatch'):
        verify_mapping(runtime, workspace)


def test_partial_discovery_failure_still_marks_failed(tmp_path, monkeypatch):
    from qopenbb_ci.compose_runtime import ComposeRuntime
    runtime = ComposeRuntime(None, tmp_path/'unused')
    phases = []
    monkeypatch.setattr(runtime, 'record_failure', lambda stage, code: {'stage': stage, 'code': code})
    monkeypatch.setattr(runtime, 'verify_configuration', lambda: None)
    monkeypatch.setattr(runtime, 'save', lambda **kwargs: phases.append(kwargs.get('phase')))
    monkeypatch.setattr(runtime, 'invocation', lambda *args: list(args))
    monkeypatch.setattr(runtime, 'command', lambda *args, **kwargs: (_ for _ in ()).throw(ValueError('failure')))
    monkeypatch.setattr(runtime, 'discover', lambda: (_ for _ in ()).throw(ValueError('discovery failure')))
    with pytest.raises(ValueError, match='protected recovery'):
        runtime.begin()
    assert phases == ['starting', 'failed']

def test_podman_lowercase_network_inspection():
    from qopenbb_ci.compose_checks import checked_network
    labels = {'com.docker.compose.project': 'owned', 'org.qopenbb.session': 'session'}
    resource = checked_network({'id': 'a'*64, 'labels': labels}, 'owned', 'session')
    assert resource.id == 'a'*64
    with pytest.raises(ValueError):
        checked_network({'id': 'a'*64, 'labels': {}}, 'owned', 'session')

def test_noncommand_readiness_failure_retains_sanitized_stage(tmp_path, monkeypatch):
    import json
    from types import SimpleNamespace
    from qopenbb_ci import compose_readiness, session_files
    from qopenbb_ci.compose_runtime import ComposeRuntime
    private = tmp_path/'recovery'
    with session_files.create_session(private) as directory:
        directory.create_file('failure.json', b'{}')
    runtime = ComposeRuntime(None, private/'descriptor.json')
    monkeypatch.setattr(runtime, 'verify_configuration', lambda: None)
    monkeypatch.setattr(runtime, 'save', lambda **kwargs: None)
    monkeypatch.setattr(runtime, 'invocation', lambda *args: list(args))
    monkeypatch.setattr(runtime, 'command', lambda *args, **kwargs: '')
    monkeypatch.setattr(runtime, 'discover', lambda: None)
    def reject(runtime):
        runtime.stage = 'bind_mapping'
        raise ValueError('private-password-response-must-not-escape')
    monkeypatch.setattr(compose_readiness, 'ready', reject)
    with pytest.raises(ValueError) as caught:
        runtime.begin()
    diagnostic = json.loads(session_files.read_private(private/'failure.json'))
    assert diagnostic == {'stage': 'bind_mapping', 'code': 'runtime_check_rejected'}
    assert 'bind_mapping' in str(caught.value)
    assert 'private-password' not in str(caught.value)
    assert 'private-password' not in json.dumps(diagnostic)
