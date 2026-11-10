"""Native dispatch must preserve checked ownership and bounded consumer scope."""
from argparse import Namespace
from pathlib import Path
import subprocess

import pytest

from qopenbb_ci import native_environment as native


def arguments(action, **values):
    defaults = dict(action=action, session_path=None, workspace_image=None, data_image=None,
                    build_selection=None, stage=None, archive=None, sdk_python=None,
                    engine_container=None, verification_source=None)
    return Namespace(**(defaults | values))


def test_dispatch_passes_start_config_and_projects_private_result(monkeypatch):
    from qopenbb_ci import native_actions as actions
    config = object()
    calls = []
    monkeypatch.setattr(actions, 'start', lambda request: calls.append(request) or object())
    monkeypatch.setattr(actions, 'public_projection', lambda descriptor: {'phase': 'ready'})
    result, code = actions.dispatch(config, arguments('start', session_path=Path('private'),
                                                    workspace_image='workspace', data_image='data'))
    assert code == 0 and result == {'phase': 'ready'}
    assert calls[0].config is config and calls[0].session_path == Path('private')
    assert (calls[0].workspace_image, calls[0].data_image) == ('workspace', 'data')


@pytest.mark.parametrize('action', ['recreate', 'stop'])
def test_lifecycle_dispatch_uses_explicit_session(monkeypatch, action):
    from qopenbb_ci import native_actions as actions
    calls = []
    monkeypatch.setattr(actions, action, lambda *args: calls.append(args) or {'phase': 'stopped'})
    monkeypatch.setattr(actions, 'public_projection', lambda value: {'phase': 'ready'})
    config, path = object(), Path('checked')
    _, code = actions.dispatch(config, arguments(action, session_path=path))
    assert code == 0 and calls == [(config, path)]


@pytest.mark.parametrize('action', ['start', 'stop', 'recreate', 'verify', 'build'])
def test_missing_inputs_fail_before_preflight(monkeypatch, action, capsys):
    monkeypatch.setattr(native, 'resolve_environment', lambda *args: pytest.fail('preflight ran'))
    assert native.main(['--action', action]) == 2
    assert 'required' in capsys.readouterr().err


def test_consumer_failure_does_not_echo_private_payload(monkeypatch, capsys):
    from qopenbb_ci import native_actions as actions
    monkeypatch.setattr(native, 'resolve_environment', lambda *args: object())
    def fail(*args):
        raise ValueError('PRIVATE_CREDENTIAL')
    monkeypatch.setattr(actions, 'dispatch', fail)
    assert native.main(['--action', 'stop', '--session-path', 'private']) == 2
    assert 'PRIVATE_CREDENTIAL' not in capsys.readouterr().err


def test_build_invokes_export_then_load_with_explicit_tools(monkeypatch, tmp_path):
    from qopenbb_ci import native_actions as actions
    config = native.NativeEnvironment(Path.cwd(), tmp_path, {'python': Path('python.exe'),
                                      'dagger_cli': Path('dagger.exe')}, {'SAFE': 'yes'})
    monkeypatch.setattr(actions, 'validate_output', lambda value: Path(value))
    monkeypatch.setattr(actions, 'resolve_executable', lambda value: Path(value))
    calls = []
    def execute(argv, repository, environment, timeout):
        calls.append((argv, repository, environment, timeout))
        return subprocess.CompletedProcess(argv, 0, 'PRIVATE_CHILD_STDOUT', '')
    monkeypatch.setattr(actions, 'run_command', execute)
    args = arguments('build', build_selection='workspace', stage=tmp_path / 'stage',
                     archive=tmp_path / 'image.tar', sdk_python=Path('sdk.exe'),
                     engine_container='qopenbb-dagger-engine-test')
    result, code = actions.dispatch(config, args)
    export, load = [call[0] for call in calls]
    assert export[:5] == ['python.exe', '-B', '-m', 'qopenbb_ci.image_cli', 'export']
    assert export[export.index('--dagger-cli') + 1] == 'dagger.exe'
    assert export[export.index('--sdk-python') + 1] == 'sdk.exe'
    assert export[export.index('--service') + 1] == 'workspace'
    assert load[4] == 'load' and code == 0
    assert all(call[2]['PYTHONPATH'] == str(Path.cwd() / 'pipeline') for call in calls)
    assert 'PRIVATE_CHILD_STDOUT' not in str(result)


def test_failed_export_never_loads(monkeypatch, tmp_path):
    from qopenbb_ci import native_actions as actions
    config = native.NativeEnvironment(Path.cwd(), tmp_path, {'python': Path('python.exe'),
                                      'dagger_cli': Path('dagger.exe')}, {})
    monkeypatch.setattr(actions, 'validate_output', lambda value: Path(value))
    monkeypatch.setattr(actions, 'resolve_executable', lambda value: Path(value))
    calls = []
    def execute(argv, *args):
        calls.append(argv)
        return subprocess.CompletedProcess(argv, 17, 'PRIVATE', 'PRIVATE')
    monkeypatch.setattr(actions, 'run_command', execute)
    result, code = actions.dispatch(config, arguments('build', build_selection='foundation',
        stage=tmp_path / 'stage', archive=tmp_path / 'image.tar', sdk_python=Path('sdk.exe'),
        engine_container='qopenbb-dagger-engine-test'))
    assert code == 17 and len(calls) == 1 and 'PRIVATE' not in str(result)


def test_verify_is_bounded_and_drops_child_payload(monkeypatch, tmp_path):
    from types import SimpleNamespace
    from qopenbb_ci import native_actions as actions
    config = native.NativeEnvironment(Path.cwd(), tmp_path, {'python': Path('python.exe'),
        'node': Path('node.exe')}, {'PLAYWRIGHT_BROWSERS_PATH': str(tmp_path / 'browser')})
    monkeypatch.setattr(actions, 'load', lambda *args: SimpleNamespace(descriptor=SimpleNamespace(phase='ready')))
    pair = {service: {'State': {'Running': True, 'Health': {'Status': 'healthy'}}}
            for service in ('workspace', 'data-api')}
    monkeypatch.setattr(actions, 'inventory', lambda runtime: (pair, ['owned']))
    monkeypatch.setattr(actions, 'wait_health', lambda runtime: pair)
    monkeypatch.setattr(actions, 'verification_source', lambda *args: tmp_path)
    calls = []
    def execute(argv, repository, environment, timeout):
        calls.append((argv, environment))
        return subprocess.CompletedProcess(argv, 0, 'PRIVATE', 'PRIVATE')
    monkeypatch.setattr(actions, 'run_command', execute)
    result, code = actions.dispatch(config, arguments('verify', session_path=Path('private')))
    assert code == 0 and len(calls) == 2 and 'PRIVATE' not in str(result)
    assert result['scope'] == 'synthetic infrastructure only'
    assert result['financial_acceptance'] == 'unverified'
    assert calls[0][0][-1].endswith('::test_synthetic_provider_observation')
    assert calls[1][0][-1] == str(tmp_path / 'verification/playwright.config.ts')
    assert calls[1][1]['QOPENBB_RUNTIME_PYTHON'] == 'python.exe'
    assert 'WORKSPACE_RUNTIME_PRIVATE' not in calls[1][1]


def test_verify_rejects_partial_session_before_test_process(monkeypatch):
    from types import SimpleNamespace
    from qopenbb_ci import native_actions as actions
    monkeypatch.setattr(actions, 'load', lambda *args: SimpleNamespace(descriptor=SimpleNamespace(phase='ready')))
    monkeypatch.setattr(actions, 'inventory', lambda runtime: ({'workspace': {}}, ['owned']))
    monkeypatch.setattr(actions, 'run_command', lambda *args: pytest.fail('test launched'))
    with pytest.raises(ValueError, match='ready owned'):
        actions.dispatch(object(), arguments('verify', session_path=Path('private')))


def test_verification_snapshot_must_match_reviewed_source(tmp_path):
    from qopenbb_ci import native_actions as actions
    repository, snapshot = tmp_path / 'repo', tmp_path / 'snapshot'
    for root in (repository, snapshot):
        (root / 'verification').mkdir(parents=True)
        (root / 'tests/e2e').mkdir(parents=True)
        for relative in ('verification/runner.ts', 'verification/package.json',
                         'verification/pnpm-lock.yaml', 'tests/e2e/infrastructure.spec.mts'):
            (root / relative).write_text('reviewed')
    entry = snapshot / 'verification/node_modules/@playwright/test/cli.js'
    entry.parent.mkdir(parents=True)
    entry.write_text('dependency')
    config = native.NativeEnvironment(repository, tmp_path, {}, {})
    assert actions.verification_source(config, snapshot) == snapshot.resolve()
    (snapshot / 'verification/runner.ts').write_text('stale')
    with pytest.raises(ValueError, match='differs'):
        actions.verification_source(config, snapshot)


def test_main_preserves_dispatched_exit_and_projects_result(monkeypatch, capsys):
    from qopenbb_ci import native_actions as actions
    monkeypatch.setattr(native, 'resolve_environment', lambda *args: object())
    monkeypatch.setattr(actions, 'dispatch', lambda *args: ({'exit': 19}, 19))
    assert native.main(['--action', 'stop', '--session-path', 'private']) == 19
    assert '19' in capsys.readouterr().out


@pytest.mark.parametrize('state', [
    {'Running': False, 'Health': {'Status': 'healthy'}},
    {'Running': True, 'Health': {'Status': 'unhealthy'}},
    {'Running': True},
])
def test_stale_ready_descriptor_cannot_launch_verification(monkeypatch, state):
    from types import SimpleNamespace
    from qopenbb_ci import native_actions as actions
    monkeypatch.setattr(actions, 'load', lambda *args: SimpleNamespace(descriptor=SimpleNamespace(phase='ready')))
    monkeypatch.setattr(actions, 'inventory', lambda runtime: (
        {service: {'State': state} for service in ('workspace', 'data-api')}, ['owned']))
    monkeypatch.setattr(actions, 'verification_source', lambda *args: pytest.fail('verification setup ran'))
    with pytest.raises(ValueError, match='running and healthy'):
        actions.dispatch(object(), arguments('verify', session_path=Path('private')))


@pytest.mark.parametrize('message', ['Explicit browser cache required',
    'Verification snapshot differs from reviewed source', 'Owned packaged services readiness timeout'])
def test_known_safe_failure_explains_actionable_prerequisite(monkeypatch, capsys, message):
    from qopenbb_ci import native_actions as actions
    monkeypatch.setattr(native, 'resolve_environment', lambda *args: object())
    def fail(*args):
        raise ValueError(message)
    monkeypatch.setattr(actions, 'dispatch', fail)
    assert native.main(['--action', 'stop', '--session-path', 'private']) == 2
    assert message in capsys.readouterr().err


def test_current_readiness_failure_prevents_verification_launch(monkeypatch):
    from types import SimpleNamespace
    from qopenbb_ci import native_actions as actions
    monkeypatch.setattr(actions, 'load', lambda *args: SimpleNamespace(descriptor=SimpleNamespace(phase='ready')))
    pair = {service: {'State': {'Running': True, 'Health': {'Status': 'healthy'}}}
            for service in ('workspace', 'data-api')}
    monkeypatch.setattr(actions, 'inventory', lambda runtime: (pair, ['owned']))
    def unavailable(runtime):
        raise ValueError('Owned packaged services readiness timeout')
    monkeypatch.setattr(actions, 'wait_health', unavailable)
    monkeypatch.setattr(actions, 'verification_source', lambda *args: pytest.fail('verification setup ran'))
    with pytest.raises(ValueError, match='readiness timeout'):
        actions.dispatch(object(), arguments('verify', session_path=Path('private')))


@pytest.mark.parametrize('message,diagnostic', [
    ('Required executable not found: PRIVATE_CREDENTIAL', 'Required executable missing'),
    ('Output/cache path must be project-specific beneath PRIVATE_CREDENTIAL', 'D:/BuildArtifacts'),
    ('Selected container daemon is unavailable (exit 7)', 'Selected container daemon unavailable'),
    ('dagger_cli version preflight failed; required 0.21.8', 'required 0.21.8'),
])
def test_safe_preflight_diagnostics_exclude_dynamic_private_values(message, diagnostic):
    result = native.safe_failure(ValueError(message))
    assert diagnostic in result
    assert 'PRIVATE_CREDENTIAL' not in result
