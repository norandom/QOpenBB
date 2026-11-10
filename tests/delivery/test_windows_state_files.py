import os
import pytest
from qopenbb_ci.windows_private_files import PrivateDirectory, PrivateStorageError

pytestmark = pytest.mark.skipif(os.name != 'nt', reason='real Windows ACLs')

def test_state_inheritance_keeps_sessions_strict(tmp_path):
    from qopenbb_ci.windows_state_files import StateDirectory
    root = tmp_path / 'state'
    with StateDirectory.create(root) as directory:
        directory.create_file('qopenbb-sentinel', b'session')
        (root / 'generated').write_bytes(b'synthetic')
        assert directory.generated_metadata('generated')['bytes'] == 9
        assert directory.read_file('qopenbb-sentinel') == b'session'
        directory.replace_file('qopenbb-sentinel', b'replaced')
        assert directory.read_file('qopenbb-sentinel') == b'replaced'
        with pytest.raises(PrivateStorageError):
            directory.read_file('generated')
        directory.remove_file('qopenbb-sentinel')
    with pytest.raises(PrivateStorageError):
        PrivateDirectory.open(root)

@pytest.mark.parametrize('dacl', [
    'D:NO_ACCESS_CONTROL', 'D:P', 'D:P(A;;FA;;;{sid})',
    'D:P(A;OICIIO;FA;;;{sid})', 'D:P(A;OICINP;FA;;;{sid})',
    'D:P(A;OICI;FR;;;{sid})', 'D:P(A;OICI;FA;;;WD)',
    'D:P(D;OICI;FR;;;WD)(A;OICI;FA;;;{sid})',
    'D:P(A;OICI;FA;;;{sid})(A;OICI;FR;;;WD)',
])
def test_state_root_exact_policy_rejects_unsafe_actual_acl(tmp_path, dacl):
    import ctypes as C
    from qopenbb_ci import windows_security as api
    from qopenbb_ci.windows_state_files import StateDirectory
    protection, pointer = api.Protection(), api.P()
    root = tmp_path / 'unsafe'
    try:
        api.checked(api.sddl(f'O:{protection.sid}' + dacl.format(sid=protection.sid), 1, C.byref(pointer), None))
        attributes = api.SecurityAttributes(C.sizeof(api.SecurityAttributes), pointer, False)
        api.checked(api.create_directory(str(root), C.byref(attributes)))
        with pytest.raises(PrivateStorageError):
            StateDirectory.open(root)
    finally:
        if pointer:
            api.local_free(pointer)
        protection.close()


def test_generated_file_broad_acl_and_hardlink_rejected(tmp_path):
    import subprocess
    from qopenbb_ci.windows_state_files import StateDirectory
    root = tmp_path / 'state'
    with StateDirectory.create(root) as directory:
        (root / 'generated').write_bytes(b'synthetic')
        os.link(root / 'generated', tmp_path / 'alias')
        with pytest.raises(PrivateStorageError):
            directory.generated_metadata('generated')
        (tmp_path / 'alias').unlink()
        result = subprocess.run(['icacls', str(root / 'generated'), '/grant', '*S-1-1-0:(R)'], capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
        assert result.returncode == 0
        with pytest.raises(PrivateStorageError):
            directory.generated_metadata('generated')
        with pytest.raises(PrivateStorageError):
            directory.generated_metadata('../escape')
        with pytest.raises(OSError):
            root.rename(tmp_path / 'substituted')


def test_changed_root_refuses_before_compose(tmp_path, monkeypatch):
    from types import SimpleNamespace
    from unittest.mock import Mock
    from qopenbb_ci.compose_runtime import ComposeRuntime
    from qopenbb_ci.windows_state_files import StateDirectory
    root = tmp_path / 'state'
    with PrivateDirectory.create(root):
        pass
    runtime = ComposeRuntime(None, tmp_path / 'descriptor')
    runtime.descriptor = SimpleNamespace(state=SimpleNamespace(host_path=root))
    runtime.command = Mock()
    with pytest.raises(PrivateStorageError):
        runtime.begin()
    runtime.command.assert_not_called()

@pytest.mark.parametrize('dacl', [
    'D:P(A;;FA;;;{sid})', 'D:P(A;ID;FA;;;{sid})',
    'D:P(A;OI;FA;;;{sid})', 'D:P(A;ID;FR;;;{sid})',
    'D:P(A;ID;FA;;;WD)', 'D:P', 'D:NO_ACCESS_CONTROL',
])
def test_generated_exact_policy_rejects_actual_unsafe_files(tmp_path, dacl):
    import ctypes as C
    from types import SimpleNamespace
    from qopenbb_ci import windows_security as api
    from qopenbb_ci.windows_private_files import _open, WRITE, READ_CONTROL
    from qopenbb_ci.windows_state_files import StateDirectory
    pointer, protection = api.P(), api.Protection()
    try:
        api.checked(api.sddl(f'O:{protection.sid}' + dacl.format(sid=protection.sid), 1, C.byref(pointer), None))
        attributes = api.SecurityAttributes(C.sizeof(api.SecurityAttributes), pointer, False)
        with StateDirectory.create(tmp_path / 'state') as directory:
            handle = _open(directory.path / 'generated', WRITE | READ_CONTROL, 1, SimpleNamespace(attributes=attributes))
            api.close(handle)
            with pytest.raises(PrivateStorageError):
                directory.generated_metadata('generated')
    finally:
        if pointer:
            api.local_free(pointer)
        protection.close()


def test_readiness_refuses_broad_generated_credentials_before_payload(tmp_path, monkeypatch):
    import json
    import subprocess
    from types import SimpleNamespace
    from qopenbb_ci import compose_readiness
    from qopenbb_ci.windows_state_files import StateDirectory
    root = tmp_path / 'state'
    with StateDirectory.create(root) as directory:
        directory.create_file('qopenbb-sentinel', b'session')
        (root / 'openbb.db').write_bytes(b'synthetic')
        (root / 'secrets.env').write_bytes(b'synthetic')
        result = subprocess.run(['icacls', str(root / 'secrets.env'), '/grant', '*S-1-1-0:(R)'], capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
        assert result.returncode == 0
    pair = {'workspace': {'NetworkSettings': {'Ports': {'3000/tcp': [{'HostIp': '127.0.0.1', 'HostPort': '23456'}]}}},
            'data-api': {'NetworkSettings': {'Ports': {}}}}
    descriptor = SimpleNamespace(origin='http://127.0.0.1:23456', state=SimpleNamespace(host_path=str(root)), container='owned')
    calls = []
    runtime = SimpleNamespace(descriptor=descriptor, command=lambda args: calls.append(args), save=lambda **kw: None)
    monkeypatch.setattr(compose_readiness, 'wait_health', lambda runtime: pair)
    monkeypatch.setattr(compose_readiness, 'verify_mapping', lambda *args: None)
    configuration = {'ui': {'isLite': False}, 'urls': {'backend': '/api'}, 'copilot': {'openbbCopilot': False}}
    monkeypatch.setattr(compose_readiness, 'request', lambda *args: (200, ('window.__APP_CONFIG__ = '+json.dumps(configuration)+';').encode()))
    with pytest.raises(PrivateStorageError):
        compose_readiness.ready(runtime)
    assert calls == []
