import json
import os
from pathlib import Path
import subprocess

import pytest
from qopenbb_ci import session_files
from test_runtime_descriptor import valid_descriptor

ROOT = Path(__file__).resolve().parents[2]
READER = ROOT / 'verification/runtime-descriptor.ts'


def invoke(path, tmp_path, **updates):
    script = tmp_path / 'consumer.mts'
    script.write_text('import {readRuntimeDescriptor} from ' + json.dumps(READER.as_uri()) + ';\n'
                      'try {const value = await readRuntimeDescriptor(process.argv[2]); '
                      'console.log(JSON.stringify({name:value.name,email:value.credentials.email}));} '
                      'catch(error) {console.error(String(error)); process.exitCode=1;}', encoding='utf-8')
    env = dict(os.environ, QOPENBB_RUNTIME_PYTHON=os.sys.executable) | updates
    return subprocess.run(['node', str(script), str(path)], capture_output=True,
                          env=env, timeout=30, creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0)


def test_checked_reader_private_pipe(tmp_path):
    raw = valid_descriptor(tmp_path)
    with session_files.create_session(tmp_path / 'private') as session:
        path = session.path / 'runtime.json'
        session.create_file(path.name, json.dumps(raw).encode())
    result = invoke(path, tmp_path)
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout) == dict(name=raw['name'], email=raw['credentials']['email'])
    assert result.stderr == b''


@pytest.mark.parametrize('payload', [b'{private-password', b'{"schema_version":999,"password":"private-password"}'])
def test_reader_refusal_is_secret_safe(tmp_path, payload):
    with session_files.create_session(tmp_path / 'private') as session:
        path = session.path / 'private-password.json'
        session.create_file(path.name, payload)
    result = invoke(path, tmp_path)
    assert result.returncode != 0
    assert result.stdout == b''
    assert b'private-password' not in result.stderr
    assert b'Runtime descriptor read refused' in result.stderr


def test_reader_missing_interpreter_is_secret_safe(tmp_path):
    result = invoke(tmp_path / 'private-password.json', tmp_path,
                    QOPENBB_RUNTIME_PYTHON=str(tmp_path / 'private-password.exe'))
    assert result.returncode != 0
    assert b'private-password' not in result.stderr


def test_checkpoint_confined_to_external_evidence_root(tmp_path):
    script = tmp_path / 'checkpoint.mts'
    script.write_text('import {checkpointPath} from ' + json.dumps(READER.as_uri()) + ';\n'
                      'try {console.log(checkpointPath(process.argv[2]));} '
                      'catch {console.error("confined"); process.exitCode=1;}', encoding='utf-8')
    env = dict(os.environ, QOPENBB_VERIFICATION_ROOT=str(tmp_path))
    for path, accepted in [(tmp_path / 'checkpoint.json', True), (tmp_path, False),
                           (tmp_path.parent / 'escape.json', False),
                           (ROOT / 'artifacts/checkpoint.json', False)]:
        result = subprocess.run(['node', str(script), str(path)], capture_output=True,
                                env=env, timeout=20,
                                creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0)
        assert (result.returncode == 0) is accepted


def test_reader_rejects_unprotected_descriptor(tmp_path):
    path = tmp_path / 'private-password.json'
    path.write_text(json.dumps(valid_descriptor(tmp_path)))
    if os.name != 'nt':
        path.chmod(0o644)
    result = invoke(path, tmp_path)
    assert result.returncode != 0
    assert result.stdout == b''
    assert b'private-password' not in result.stderr

@pytest.mark.parametrize('payload', ['not-json-private-password', '{}', '[]', '{"schema_version":true}'])
def test_reader_checks_child_shape_and_discards_stderr(tmp_path, payload):
    package = tmp_path / 'shadow package' / 'qopenbb_ci'
    package.mkdir(parents=True)
    (package / '__init__.py').write_text('')
    (package / 'session_files.py').write_text(
        'import sys\nprint(' + repr(payload) + ')\nprint("private-password",file=sys.stderr)\n')
    result = invoke(tmp_path / 'descriptor with spaces.json', tmp_path,
                    PYTHONPATH=str(package.parent))
    assert result.returncode != 0
    assert result.stdout == b''
    assert b'private-password' not in result.stderr
    assert b'Runtime descriptor read refused' in result.stderr

def test_reader_rejects_checked_but_not_ready_state(tmp_path):
    with session_files.create_session(tmp_path / 'private with spaces') as session:
        path = session.path / 'descriptor with spaces.json'
        session.create_file(path.name, json.dumps(valid_descriptor(tmp_path, 'prepared')).encode())
    result = invoke(path, tmp_path)
    assert result.returncode != 0
    assert result.stdout == b''
    assert b'Runtime descriptor read refused' in result.stderr


@pytest.mark.skipif(os.name == 'nt', reason='Linux Node child stdout transport diagnosis')
def test_node_captured_stdout_is_anonymous_unix_stream():
    probe = ("import os,socket,json; "
             "s=socket.socket(fileno=os.dup(1)); "
             "print(json.dumps([int(s.family),int(s.type),s.getsockname(),s.getpeername()]))")
    script = ("const {execFile}=require('node:child_process'); "
              "execFile(process.argv[1],['-B','-c',process.argv[2]],"
              "{encoding:'utf8'},(error,stdout)=>{if(error)process.exitCode=1;"
              "else process.stdout.write(stdout);});")
    result = subprocess.run(['node', '-e', script, os.sys.executable, probe],
                            capture_output=True, text=True, timeout=30)
    assert result.returncode == 0, result.stderr
    import socket
    assert json.loads(result.stdout) == [int(socket.AF_UNIX), int(socket.SOCK_STREAM), '', '']
