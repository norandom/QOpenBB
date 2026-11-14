"""Private checkpoint creation exercises the real platform storage boundary."""
import json
import os
from pathlib import Path
import runpy
import stat
import subprocess
import sys

import pytest

from qopenbb_ci import checkpoint_cli, session_files

ROOT = Path(__file__).resolve().parents[2]
valid_descriptor = runpy.run_path(str(ROOT / 'tests/delivery/test_runtime_descriptor.py'))['valid_descriptor']


@pytest.fixture
def checkpoint(tmp_path):
    raw = valid_descriptor(tmp_path)
    with session_files.create_session(tmp_path / 'private') as directory:
        runtime = directory.path / 'runtime.json'
        directory.create_file(runtime.name, json.dumps(raw).encode())
        value = {'stage': 'initial-complete', 'images': raw['images'], 'runtimeName': raw['name'],
                 'containerId': raw['container'], 'dashboardPath': '/app/synthetic-dashboard',
                 'state': {'widgets': [], 'note': 'Currency €; zero 0; signed -1'}, 'selected': {}}
        payload = (json.dumps(value, indent=2, ensure_ascii=False) + '\n').encode()
        yield runtime, directory.path / checkpoint_cli.NAME, value, payload


def invoke(runtime, target, payload):
    return subprocess.run([sys.executable, '-B', '-m', 'qopenbb_ci.checkpoint_cli',
                           '--runtime', str(runtime), '--path', str(target)],
                          cwd=ROOT, input=payload, capture_output=True, timeout=20,
                          creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0)


def test_actual_private_creation_full_bytes_and_exclusive(checkpoint):
    runtime, target, _, payload = checkpoint
    result = invoke(runtime, target, payload)
    assert result.returncode == 0 and result.stdout == result.stderr == b''
    assert session_files.read_private(target) == payload
    if os.name != 'nt':
        assert stat.S_IMODE(target.stat().st_mode) == 0o600
    before = target.stat().st_mtime_ns
    repeated = invoke(runtime, target, payload)
    assert repeated.returncode == 1 and repeated.stdout == b''
    assert repeated.stderr.splitlines() == [b'Checkpoint write refused']
    assert session_files.read_private(target) == payload and target.stat().st_mtime_ns == before


@pytest.mark.parametrize('target_kind', ['outside', 'wrong-name', 'relative', 'traversal'])
def test_path_scope_rejected_before_creation(checkpoint, target_kind):
    runtime, target, _, payload = checkpoint
    candidate = {'outside': target.parent.parent / target.name, 'wrong-name': target.with_name('other.json'),
                 'relative': Path(target.name), 'traversal': target.parent / '..' / target.name}[target_kind]
    result = invoke(runtime, candidate, payload)
    assert result.returncode == 1 and result.stdout == b''
    assert result.stderr.splitlines() == [b'Checkpoint write refused'] and not target.exists()


@pytest.mark.parametrize(('field', 'replacement'), [
    ('stage', 'incomplete'), ('images', {}), ('runtimeName', 'another-runtime'),
    ('containerId', '0' * 64), ('dashboardPath', '//foreign.invalid/app'), ('state', []),
    ('selected', []), ('dashboardPath', '/app/../escape'), ('dashboardPath', '/app/item?token=synthetic'),
])
def test_runtime_binding_refused_without_payload_output(checkpoint, field, replacement):
    runtime, target, value, _ = checkpoint
    value[field] = replacement
    result = invoke(runtime, target, json.dumps(value).encode())
    assert result.returncode == 1 and result.stdout == b''
    assert result.stderr.splitlines() == [b'Checkpoint write refused'] and not target.exists()


@pytest.mark.parametrize('phase', ['prepared', 'starting', 'recreating', 'failed', 'stopped'])
def test_nonready_phase_refused(checkpoint, phase):
    runtime, target, _, payload = checkpoint
    raw = json.loads(session_files.read_private(runtime))
    raw['phase'] = phase
    session_files.replace_private(runtime, json.dumps(raw).encode())
    assert invoke(runtime, target, payload).returncode == 1 and not target.exists()


def test_unprotected_descriptor_refused(checkpoint):
    runtime, target, _, payload = checkpoint
    raw = json.loads(session_files.read_private(runtime))
    unprotected = runtime.parent.parent / 'runtime.json'
    unprotected.write_bytes(json.dumps(raw).encode())
    other_target = unprotected.parent / target.name
    assert invoke(unprotected, other_target, payload).returncode == 1 and not other_target.exists()


@pytest.mark.parametrize('payload', [b'{synthetic-private-token', b'NaN', b'x' * (checkpoint_cli.MAX_BYTES + 1)],
                         ids=['malformed', 'nonfinite', 'oversized'])
def test_invalid_or_oversized_input_has_finite_error(checkpoint, payload):
    runtime, target, _, _ = checkpoint
    result = invoke(runtime, target, payload)
    assert result.returncode == 1 and result.stdout == b''
    assert result.stderr.splitlines() == [b'Checkpoint write refused'] and not target.exists()


def test_terminal_input_refused_before_private_write(checkpoint, monkeypatch, capsys):
    runtime, target, _, _ = checkpoint
    monkeypatch.setattr(session_files, 'captured_private_output', lambda _: False)
    monkeypatch.setattr(checkpoint_cli, 'write_checkpoint', lambda *a: pytest.fail('write before pipe validation'))
    assert checkpoint_cli.main(['--runtime', str(runtime), '--path', str(target)]) == 1
    captured = capsys.readouterr()
    assert captured.out == '' and captured.err == 'Checkpoint write refused\n'


def test_failed_write_removes_owned_partial_without_descriptor_change(checkpoint, monkeypatch):
    runtime, target, _, payload = checkpoint
    descriptor = session_files.read_private(runtime)
    original = session_files.PrivateDirectory._write_handle

    def fail_after_write(directory, handle, value):
        original(directory, handle, value)
        raise OSError('synthetic-private-token')

    monkeypatch.setattr(session_files.PrivateDirectory, '_write_handle', fail_after_write)
    with pytest.raises(OSError):
        checkpoint_cli.write_checkpoint(runtime, target, payload)
    assert not target.exists() and session_files.read_private(runtime) == descriptor


@pytest.mark.parametrize('python_kind', ['configured', 'missing', 'relative'])
def test_actual_node_bridge_uses_configured_python_and_private_stdin(checkpoint, tmp_path, python_kind):
    runtime, target, value, payload = checkpoint
    script = tmp_path / 'writer.mts'
    reader = ROOT / 'verification/runtime-descriptor.ts'
    script.write_text('import {writeResearchCheckpoint} from ' + json.dumps(reader.as_uri()) + ';\n'
                      'import {readFileSync} from "node:fs";\n'
                      'try {await writeResearchCheckpoint(process.argv[2], JSON.parse(readFileSync(0,"utf8")));}\n'
                      'catch {console.error("Checkpoint write refused");process.exitCode=1;}', encoding='utf-8')
    environment = dict(os.environ, QOPENBB_RUNTIME_PYTHON=sys.executable, WORKSPACE_RUNTIME_PRIVATE=str(runtime),
                       QOPENBB_VERIFICATION_ROOT=str(runtime.parent), PYTHONPATH=str(ROOT / 'pipeline'))
    if python_kind != 'configured':
        environment['QOPENBB_RUNTIME_PYTHON'] = '' if python_kind == 'missing' else 'python'
    result = subprocess.run(['node', str(script), str(target)], cwd=ROOT, env=environment,
                            input=json.dumps(value, ensure_ascii=False).encode(), capture_output=True, timeout=30,
                            creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0)
    if python_kind == 'configured':
        assert result.returncode == 0 and result.stdout == result.stderr == b''
        assert session_files.read_private(target) == payload
    else:
        assert result.returncode == 1 and result.stdout == b'' and not target.exists()
        assert result.stderr.splitlines() == [b'Checkpoint write refused']
