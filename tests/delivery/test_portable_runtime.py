"""Portable selection and storage contracts without a daemon or Windows metadata."""
import os
from pathlib import Path
from types import SimpleNamespace
import sys
import subprocess
import json
import venv

import pytest
from qopenbb_ci import native_environment, portable_runtime as portable
from qopenbb_ci import compose_runtime, compose_lifecycle, session_files
from test_runtime_descriptor import valid_descriptor


@pytest.fixture
def linux_inputs(tmp_path, monkeypatch):
    # The POSIX branch is exercised on native Windows without changing pathlib's host class.
    monkeypatch.setattr(native_environment, 'os', SimpleNamespace(name='posix', environ={}))
    monkeypatch.setattr(portable, 'sys', SimpleNamespace(platform='linux', executable=sys.executable))
    executable = tmp_path / 'docker.exe'
    executable.write_bytes(b'unit-test executable boundary')
    source = {'QOPENBB_STORAGE_ROOT': str(tmp_path), 'DOCKER_HOST': 'unix:///var/run/docker.sock',
              'QOPENBB_CONTAINER_CLI': str(executable), 'PATH': os.environ.get('PATH', ''),
              'FMP_API_KEY': 'excluded-secret'}
    return Path(__file__).resolve().parents[2], source


def test_linux_selection_without_native_metadata(linux_inputs, monkeypatch):
    repository, source = linux_inputs
    monkeypatch.setattr(portable, 'resolve_native', lambda *_: pytest.fail('Windows metadata read'))
    monkeypatch.setattr(portable.os, 'environ', source)
    config = portable.resolve_environment(repository)
    assert isinstance(config, portable.LinuxEnvironment)
    assert config.environment['DOCKER_HOST'] == source['DOCKER_HOST']
    assert config.tools['python'] == Path(sys.executable).absolute()
    assert config.environment['QOPENBB_RUNTIME_READER'] == str(repository / 'verification/runtime-descriptor.ts')
    assert config.environment['PYTHONPATH'] == str(repository / 'pipeline')
    assert 'FMP_API_KEY' not in config.environment
    assert config.artifacts == config.storage / 'QOpenBB'


@pytest.mark.parametrize('updates', [
    {'QOPENBB_STORAGE_ROOT': ''}, {'QOPENBB_STORAGE_ROOT': 'relative'},
    {'QOPENBB_STORAGE_ROOT': '/mnt/c/cache'},
    {'QOPENBB_STORAGE_ROOT': '/mnt/d/cache'}, {'QOPENBB_STORAGE_ROOT': Path('/').absolute().anchor},
    {'DOCKER_HOST': ''}, {'DOCKER_HOST': 'npipe:////./pipe/docker'},
    {'DOCKER_CONTEXT': 'implicit'}, {'DOCKER_HOST': 'tcp://user:secret@host:1234'},
    {'CONTAINER_HOST': 'unix:///other.sock'}, {'TEMP': '/outside-temp'},
])
def test_linux_rejects_unsafe_inputs(linux_inputs, updates):
    repository, source = linux_inputs
    with pytest.raises(ValueError):
        portable.resolve_linux(repository, source | {k: str(v) for k, v in updates.items()})


def test_linux_symlink_storage_rejected(linux_inputs, tmp_path):
    repository, source = linux_inputs
    target = tmp_path / 'real'
    target.mkdir()
    link = tmp_path / 'link'
    try:
        link.symlink_to(target, target_is_directory=True)
    except OSError:
        pytest.skip('Host denies symlink creation')
    with pytest.raises(ValueError, match='symbolic-link'):
        portable.resolve_linux(repository, source | {'QOPENBB_STORAGE_ROOT': str(link)})


@pytest.mark.parametrize('module,entry', [(compose_runtime, 'prepare'), (compose_lifecycle, 'load')])
def test_coordinators_apply_linux_storage_before_commands(linux_inputs, module, entry, tmp_path):
    repository, source = linux_inputs
    config = portable.resolve_linux(repository, source)
    outside = tmp_path.parent / 'outside-session' / 'descriptor.json'
    with pytest.raises(ValueError, match='project-specific'):
        if entry == 'prepare':
            module.prepare(compose_runtime.StartRequest(config, outside, 'workspace', 'data'))
        else:
            module.load(config, outside)


def test_windows_dispatch_retains_native_resolver(monkeypatch):
    monkeypatch.setattr(portable, 'sys', SimpleNamespace(platform='win32'))
    monkeypatch.setattr(portable, 'resolve_native', lambda path: ('native', path))
    assert portable.resolve_environment(Path('repository')) == ('native', Path('repository'))


def test_interpreter_invocation_preserves_virtual_environment(linux_inputs, tmp_path, monkeypatch):
    repository, source = linux_inputs
    invocation = tmp_path / 'venv-python.exe'
    invocation.write_bytes(b'interpreter path fixture')
    original = Path.resolve
    monkeypatch.setattr(Path, 'resolve', lambda path, *args, **kwargs:
                        Path(sys.executable) if path == invocation else original(path, *args, **kwargs))
    monkeypatch.setattr(portable, 'sys', SimpleNamespace(executable=str(invocation), platform='linux'))
    config = portable.resolve_linux(repository, source)
    assert config.tools['python'] == invocation
    assert config.environment['QOPENBB_RUNTIME_PYTHON'] == str(invocation)


@pytest.mark.skipif(sys.platform != 'linux', reason='Real Linux virtual environment symlink execution')
def test_linux_symlink_interpreter_imports_venv_only_module(linux_inputs, tmp_path, monkeypatch):
    repository, source = linux_inputs
    root = tmp_path / 'venv'
    venv.EnvBuilder(with_pip=False, symlinks=True).create(root)
    python = root / 'bin/python'
    assert python.is_symlink()
    site = root / f'lib/python{sys.version_info.major}.{sys.version_info.minor}/site-packages'
    site.mkdir(parents=True, exist_ok=True)
    (site / 'qopenbb_venv_marker.py').write_text('VALUE = "venv-only"\n')
    monkeypatch.setattr(portable, 'sys', SimpleNamespace(executable=str(python), platform='linux'))
    config = portable.resolve_linux(repository, source)
    result = subprocess.run([config.environment['QOPENBB_RUNTIME_PYTHON'], '-B', '-c',
        'import sys,json,qopenbb_venv_marker as m; print(json.dumps([sys.prefix,m.VALUE]))'],
        env=config.environment, cwd=repository, text=True, capture_output=True, timeout=30)
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout) == [str(root), 'venv-only']


def test_selected_interpreter_imports_checked_reader_dependencies(linux_inputs, tmp_path):
    repository, source = linux_inputs
    config = portable.resolve_linux(repository, source)
    result = subprocess.run([config.environment['QOPENBB_RUNTIME_PYTHON'], '-B', '-c',
        'import pydantic,qopenbb_ci.session_files; print("reader dependencies ready")'],
        env=config.environment, cwd=repository, text=True, capture_output=True, timeout=30,
        creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0)
    assert result.returncode == 0, result.stderr
    assert result.stdout.strip() == 'reader dependencies ready'
    with session_files.create_session(tmp_path / 'private-reader') as directory:
        path = directory.path / 'runtime.json'
        raw = valid_descriptor(tmp_path)
        directory.create_file(path.name, json.dumps(raw).encode())
    result = subprocess.run([config.environment['QOPENBB_RUNTIME_PYTHON'], '-B', '-m',
        'qopenbb_ci.session_files', 'read', '--private-ipc', '--path', str(path)],
        env=config.environment, cwd=repository, text=True, capture_output=True, timeout=30,
        creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0)
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)['session_id'] == raw['session_id']
