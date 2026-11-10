from pathlib import Path
import os
import subprocess
import pytest
from qopenbb_ci.native_environment import child_environment, resolve_environment, run_command, validate_output
from qopenbb_ci.container_command import container_command, compose_command, resolve_executable


@pytest.mark.skipif(os.name != 'nt', reason='Windows native paths or junction API')
def test_output_rejects_root_outside_and_reparse(tmp_path):
    for value in [Path('D:/'), Path('C:/unowned'), Path('D:/BuildArtifacts')]:
        with pytest.raises(ValueError):
            validate_output(value)
    assert validate_output(Path('D:/BuildArtifacts/QOpenBB/path with spaces')).name == 'path with spaces'


@pytest.mark.skipif(os.name != 'nt', reason='Windows native paths or junction API')
def test_child_environment_allowlist():
    source = {'SystemRoot': 'C:/Windows', 'TEMP': 'D:/BuildArtifacts/temp',
              'UV_CACHE_DIR': 'D:/BuildArtifacts/uv', 'DOCKER_HOST': 'ssh://selected',
              'CONTAINER_CONNECTION': 'chosen', 'FMP_API_KEY': 'private',
              'ANTHROPIC_API_KEY': 'private', 'PATH': 'tools', 'COMPOSE_FILE': 'unsafe'}
    env = child_environment(Path('D:/BuildArtifacts/QOpenBB'), source)
    assert env['SystemRoot'] == source['SystemRoot']
    assert env['TEMP'] == source['TEMP']
    assert env['DOCKER_HOST'] == 'ssh://selected'
    assert env['CONTAINER_CONNECTION'] == 'chosen'
    assert env['UV_CACHE_DIR'] == source['UV_CACHE_DIR']
    assert 'FMP_API_KEY' not in env and 'ANTHROPIC_API_KEY' not in env
    assert 'COMPOSE_FILE' not in env
    assert env['HOME'].startswith('D:')
    with pytest.raises(ValueError):
        child_environment(Path('D:/BuildArtifacts/QOpenBB'), {'TEMP': 'C:/temp'})


def test_executable_and_argv(tmp_path):
    exe = tmp_path / 'space tool.exe'
    exe.write_bytes(b'executable')
    if os.name != 'nt': exe.chmod(0o700)
    assert resolve_executable(str(exe)) == exe.resolve()
    script = tmp_path / 'wrapper.cmd'
    script.write_text('echo unsafe')
    with pytest.raises(ValueError):
        resolve_executable(str(script))
    env = {'QOPENBB_CONTAINER_CLI': str(exe), 'PODMAN_COMPOSE_PROVIDER': str(exe)}
    assert container_command(['inspect', 'image with spaces'], env) == [str(exe.resolve()), 'inspect', 'image with spaces']
    assert compose_command(['--project-name', 'owned session'], env)[-2:] == ['--project-name', 'owned session']


def test_run_preserves_exit_code_and_array(monkeypatch):
    calls = []
    def fake(argv, **kwargs):
        calls.append((argv, kwargs))
        return subprocess.CompletedProcess(argv, 23, 'diagnostic', '')
    monkeypatch.setattr(subprocess, 'run', fake)
    result = run_command(['tool.exe', 'path with spaces'], Path.cwd(), {})
    assert result.returncode == 23
    assert calls[0][0] == ['tool.exe', 'path with spaces']
    assert calls[0][1]['shell'] is False
    assert calls[0][1]['timeout'] > 0


@pytest.mark.skipif(os.name != 'nt', reason='Windows native paths or junction API')
def test_repository_root_refused_before_outputs():
    with pytest.raises(ValueError):
        resolve_environment(Path('D:/'), Path('D:/BuildArtifacts/QOpenBB'))

@pytest.mark.skipif(os.name != 'nt', reason='Windows native paths or junction API')
def test_junction_rejected(tmp_path):
    target = tmp_path / 'target'
    target.mkdir()
    link = tmp_path / 'linked'
    result = subprocess.run(['cmd.exe', '/d', '/c', 'mklink', '/J', str(link), str(target)], capture_output=True)
    assert result.returncode == 0
    try:
        with pytest.raises(ValueError, match='Reparse'):
            validate_output(link / 'new output')
    finally:
        link.rmdir()


def test_doctor_rejects_wrong_version(monkeypatch):
    from qopenbb_ci import native_environment as native
    config = native.NativeEnvironment(Path.cwd(), Path('D:/BuildArtifacts/QOpenBB'),
                                      {'dagger_cli': Path('real.exe')}, {})
    monkeypatch.setattr(native, 'run_command', lambda *args: subprocess.CompletedProcess(args, 0, 'dagger v0.21.11', ''))
    with pytest.raises(ValueError, match='required 0.21.8'):
        native.doctor(config)


def test_action_arguments_and_required_build_inputs(monkeypatch, capsys):
    from qopenbb_ci import native_environment as native
    with pytest.raises(SystemExit) as error:
        native.main(['--action', 'doctor', '--session-path', 'irrelevant'])
    assert error.value.code == 2
    monkeypatch.setattr(native, 'resolve_environment', lambda *args: object())
    assert native.main(['--action', 'build']) == 2
    assert 'required inputs' in capsys.readouterr().err


def test_selected_connection_keeps_actual_endpoint(monkeypatch, tmp_path):
    from qopenbb_ci import native_environment as native
    tool = tmp_path / 'podman.exe'
    tool.write_bytes(b'executable')
    payload = '[{"Name":"chosen","URI":"ssh://selected","Identity":"key","Default":false}]'
    monkeypatch.setattr(native, 'run_command', lambda *args: subprocess.CompletedProcess(args, 0, payload, ''))
    monkeypatch.setattr(native, 'podman_compose_endpoint', lambda repository, source, *args: source)
    result = native.selected_connection(Path.cwd(), {'QOPENBB_CONTAINER_CLI': str(tool), 'CONTAINER_CONNECTION': 'chosen'})
    assert result['CONTAINER_HOST'] == 'ssh://selected'
    assert result['CONTAINER_SSHKEY'] == 'key'
    assert 'CONTAINER_CONNECTION' not in result

@pytest.mark.skipif(os.name != 'nt', reason='Windows native paths or junction API')
def test_docker_context_resolved_without_leaking_config(monkeypatch):
    from qopenbb_ci import native_environment as native
    payload = '[{"Endpoints":{"docker":{"Host":"tcp://selected:2376","SkipTLSVerify":false}},"TLSMaterial":{"docker":["ca.pem"]},"Storage":{"TLSPath":"D:/BuildArtifacts/tls"}}]'
    monkeypatch.setattr(native, 'run_command', lambda *args: subprocess.CompletedProcess(args, 0, payload, ''))
    source = native.selected_docker_context(Path.cwd(), {'DOCKER_CONTEXT': 'selected', 'DOCKER_CONFIG': 'C:/private/config'}, Path('docker.exe'))
    env = child_environment(Path('D:/BuildArtifacts/QOpenBB'), source)
    assert env['DOCKER_HOST'] == 'tcp://selected:2376'
    assert 'DOCKER_CONTEXT' not in env
    assert env['DOCKER_CONFIG'] != 'C:/private/config'
    assert env['DOCKER_TLS_VERIFY'] == '1'

@pytest.mark.parametrize('context,host,expected', [(None,None,'tcp://configured:2376'),(None,'tcp://explicit:2375','tcp://explicit:2375'),('chosen','tcp://explicit:2375','tcp://configured:2376')])
def test_docker_effective_context_precedence(monkeypatch, context, host, expected):
    from qopenbb_ci import native_environment as native
    calls = []
    def execute(argv, *args):
        calls.append(argv)
        payload = '[{"Endpoints":{"docker":{"Host":"tcp://configured:2376"}}}]'
        return subprocess.CompletedProcess(argv, 0, 'configured\n' if argv[-1] == 'show' else payload, '')
    monkeypatch.setattr(native, 'run_command', execute)
    source = {'DOCKER_CONFIG': 'operator-config'}
    if context: source['DOCKER_CONTEXT'] = context
    if host: source['DOCKER_HOST'] = host
    result = native.selected_docker_context(Path.cwd(), source, Path('docker.exe'))
    assert result['DOCKER_HOST'] == expected
    if context:
        assert calls[0][-1] == 'chosen'
    elif host:
        assert calls == []
    else:
        assert calls[0][-1] == 'show'
        assert calls[1][-1] == 'configured'


@pytest.mark.skipif(os.name == 'nt', reason='POSIX storage contract')
def test_posix_explicit_storage_and_environment(tmp_path):
    root = tmp_path / 'linux-storage'
    artifacts = root / 'qopenbb'
    cache = root / 'cache'
    env = child_environment(artifacts, {'TMPDIR': str(cache), 'FMP_API_KEY': 'secret'}, storage=root)
    assert env['TMPDIR'] == str(cache)
    assert env['HOME'] == str(artifacts / 'home')
    assert 'FMP_API_KEY' not in env
    with pytest.raises(ValueError, match='explicit POSIX storage'):
        validate_output(artifacts)
    with pytest.raises(ValueError):
        validate_output(tmp_path / 'outside', storage=root)


def test_working_directory_filesystem_root_refused():
    from qopenbb_ci.native_environment import checked_path
    with pytest.raises(ValueError, match='roots are forbidden'):
        checked_path(Path(Path.cwd().anchor))

def test_entry_suppresses_bytecode_before_module_import():
    script = (Path(__file__).resolve().parents[2] / 'pipeline/dev.ps1').read_text()
    assert "$arguments = @('-B','-m'" in script


@pytest.mark.skipif(os.name != 'nt', reason='Windows storage contract')
def test_child_bytecode_stays_external():
    root = Path('D:/BuildArtifacts/QOpenBB')
    assert child_environment(root, {})['PYTHONDONTWRITEBYTECODE'] == '1'
    configured = 'D:/BuildArtifacts/QOpenBB/cache/python'
    assert child_environment(root, {'PYTHONPYCACHEPREFIX': configured})['PYTHONPYCACHEPREFIX'] == configured
    with pytest.raises(ValueError):
        child_environment(root, {'PYTHONPYCACHEPREFIX': 'C:/unsafe-cache'})


@pytest.mark.parametrize('rootful', [True, False])
def test_podman_compose_pipe_matches_selected_machine(monkeypatch, tmp_path, rootful):
    from qopenbb_ci import native_environment as native
    import json
    tool = tmp_path / 'podman.exe'
    tool.write_bytes(b'executable')
    connection = {'Name': 'chosen-root', 'URI': 'ssh://root@127.0.0.1:1234/run/podman/podman.sock',
                  'Identity': 'key', 'Default': True, 'IsMachine': True}
    machine = {'Name': 'chosen', 'Rootful': True, 'State': 'running',
               'SSHConfig': {'Port': 1234, 'IdentityPath': 'key', 'RemoteUsername': 'user'},
               'ConnectionInfo': {'PodmanPipe': {'Path': r'\\.\pipe\chosen'}}}
    if not rootful:
        connection.update(Name='chosen', URI='ssh://user@127.0.0.1:1234/run/user/1000/podman/podman.sock')
        machine['Rootful'] = False
    def execute(argv, *args):
        if argv[1:3] == ['machine', 'inspect']:
            assert argv[3:] == ['chosen']
        payload = [machine] if argv[1:3] == ['machine', 'inspect'] else [connection]
        return subprocess.CompletedProcess(argv, 0, json.dumps(payload), '')
    monkeypatch.setattr(native, 'run_command', execute)
    source = {'QOPENBB_CONTAINER_CLI': str(tool), 'CONTAINER_HOST': connection['URI'],
              'CONTAINER_SSHKEY': 'key', 'DOCKER_CONTEXT': 'wrong', 'DOCKER_HOST': 'tcp://wrong'}
    result = native.selected_connection(Path.cwd(), source)
    assert result['DOCKER_HOST'] == 'npipe:////./pipe/chosen'
    assert result['CONTAINER_HOST'] == connection['URI']
    assert result['CONTAINER_SSHKEY'] == 'key'
    assert 'DOCKER_CONTEXT' not in result
    assert 'DOCKER_CONTEXT' in source


@pytest.mark.parametrize('mismatch', ['rootful', 'port', 'identity', 'state', 'name', 'pipe'])
def test_podman_pipe_mapping_rejects_mismatch(monkeypatch, tmp_path, mismatch):
    from qopenbb_ci import native_environment as native
    import json
    tool = tmp_path / 'podman.exe'
    tool.write_bytes(b'executable')
    connection = {'Name': 'chosen-root', 'URI': 'ssh://root@127.0.0.1:1234/run/podman/podman.sock',
                  'Identity': 'key', 'Default': True, 'IsMachine': True}
    machine = {'Name': 'chosen', 'Rootful': True, 'State': 'running',
               'SSHConfig': {'Port': 1234, 'IdentityPath': 'key', 'RemoteUsername': 'user'},
               'ConnectionInfo': {'PodmanPipe': {'Path': r'\\.\pipe\chosen'}}}
    if mismatch == 'rootful': machine['Rootful'] = False
    if mismatch == 'port': machine['SSHConfig']['Port'] = 4321
    if mismatch == 'identity': machine['SSHConfig']['IdentityPath'] = 'other'
    if mismatch == 'state': machine['State'] = 'stopped'
    if mismatch == 'name': machine['Name'] = 'other'
    if mismatch == 'pipe': machine['ConnectionInfo']['PodmanPipe']['Path'] = ''
    def execute(argv, *args):
        payload = [machine] if argv[1:3] == ['machine', 'inspect'] else [connection]
        return subprocess.CompletedProcess(argv, 0, json.dumps(payload), '')
    monkeypatch.setattr(native, 'run_command', execute)
    with pytest.raises(ValueError, match='matching native Podman pipe'):
        native.selected_connection(Path.cwd(), {'QOPENBB_CONTAINER_CLI': str(tool)})


def test_doctor_rejects_compose_daemon_access_failure(monkeypatch):
    from qopenbb_ci import native_environment as native
    config = native.NativeEnvironment(Path.cwd(), Path('D:/BuildArtifacts/QOpenBB'), {}, {})
    monkeypatch.setattr(native, 'container_command', lambda args, env: ['podman', *args])
    monkeypatch.setattr(native, 'compose_command', lambda args, env: ['compose', *args])
    def execute(argv, *args):
        payload = '{}' if argv[1] == 'info' else '5.7.0'
        return subprocess.CompletedProcess(argv, 255 if argv[1] == 'ls' else 0, payload, '')
    monkeypatch.setattr(native, 'run_command', execute)
    with pytest.raises(ValueError, match='Compose.*daemon'):
        native.doctor(config)


@pytest.mark.parametrize('selection', ['unregistered-host', 'wrong-key', 'ambiguous'])
def test_podman_selection_never_falls_back_to_default(monkeypatch, tmp_path, selection):
    from qopenbb_ci import native_environment as native
    import json
    tool = tmp_path / 'podman.exe'
    tool.write_bytes(b'executable')
    connection = {'Name': 'chosen', 'URI': 'ssh://selected', 'Identity': 'key', 'Default': True}
    source = {'QOPENBB_CONTAINER_CLI': str(tool)}
    if selection == 'unregistered-host': source['CONTAINER_HOST'] = 'ssh://other'
    if selection == 'wrong-key': source['CONTAINER_SSHKEY'] = 'other'
    entries = [connection, connection] if selection == 'ambiguous' else [connection]
    monkeypatch.setattr(native, 'run_command', lambda *args: subprocess.CompletedProcess(args, 0, json.dumps(entries), ''))
    with pytest.raises(ValueError):
        native.selected_connection(Path.cwd(), source)
