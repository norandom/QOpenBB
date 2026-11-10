import os
from pathlib import Path
import subprocess
import pytest
from qopenbb_ci.windows_private_files import PrivateDirectory, PrivateStorageError

pytestmark = pytest.mark.skipif(os.name != 'nt', reason='real Windows security APIs')


def test_create_read_remove_and_exclusive(tmp_path):
    root = tmp_path / 'private space'
    with PrivateDirectory.create(root) as directory:
        directory.create_file('credentials.json', b'synthetic secret')
        assert directory.read_file('credentials.json') == b'synthetic secret'
        with pytest.raises(PrivateStorageError):
            directory.create_file('credentials.json', b'replacement')
        for name in ['../escape', 'x/y', 'x:y', 'CON', 'a.', 'a ']:
            with pytest.raises(PrivateStorageError):
                directory.read_file(name)
        directory.remove_file('credentials.json')
        assert not (root / 'credentials.json').exists()
    with PrivateDirectory.open(root) as directory:
        directory.create_file('empty', b'')


def test_pinned_directory_cannot_be_replaced(tmp_path):
    root = tmp_path / 'private'
    with PrivateDirectory.create(root):
        with pytest.raises(OSError):
            root.rename(tmp_path / 'moved')


def test_broad_acl_rejected_before_read_or_write(tmp_path):
    root = tmp_path / 'private'
    with PrivateDirectory.create(root) as directory:
        directory.create_file('secret', b'synthetic')
    result = subprocess.run(['icacls', str(root / 'secret'), '/grant', '*S-1-1-0:(R)'], capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
    assert result.returncode == 0
    with PrivateDirectory.open(root) as directory:
        with pytest.raises(PrivateStorageError):
            directory.read_file('secret')
        with pytest.raises(PrivateStorageError):
            directory.remove_file('secret')


def test_unprotected_directory_rejected(tmp_path):
    with pytest.raises(PrivateStorageError):
        PrivateDirectory.open(tmp_path)


def test_junction_rejected(tmp_path):
    target = tmp_path / 'target'
    with PrivateDirectory.create(target):
        pass
    link = tmp_path / 'junction'
    result = subprocess.run(['cmd', '/c', 'mklink', '/J', str(link), str(target)], capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
    assert result.returncode == 0
    try:
        with pytest.raises(PrivateStorageError):
            PrivateDirectory.open(link)
    finally:
        link.rmdir()

@pytest.mark.parametrize('dacl', ['D:NO_ACCESS_CONTROL', 'D:P(A;ID;FA;;;{sid})', 'D:P(D;;FR;;;WD)(A;;FA;;;{sid})'])
def test_unsafe_actual_security_descriptors_rejected(tmp_path, dacl):
    import ctypes as C
    from qopenbb_ci import windows_security as api
    protection = api.Protection()
    pointer = api.P()
    root = tmp_path / 'unsafe'
    try:
        text = f'O:{protection.sid}' + dacl.format(sid=protection.sid)
        api.checked(api.sddl(text, 1, C.byref(pointer), None))
        attributes = api.SecurityAttributes(C.sizeof(api.SecurityAttributes), pointer, False)
        api.checked(api.create_directory(str(root), C.byref(attributes)))
        with pytest.raises(PrivateStorageError):
            PrivateDirectory.open(root)
        assert not (root / 'secret').exists()
    finally:
        if pointer:
            api.local_free(pointer)
        protection.close()


def test_verification_failure_precedes_payload_write(tmp_path, monkeypatch):
    from qopenbb_ci import windows_security as api
    root = tmp_path / 'private'
    with PrivateDirectory.create(root) as directory:
        original = directory.protection.verify
        def refuse_file(handle):
            if handle != directory.handle:
                raise PrivateStorageError('synthetic unsupported file protection')
            original(handle)
        monkeypatch.setattr(directory.protection, 'verify', refuse_file)
        with pytest.raises(PrivateStorageError):
            directory.create_file('secret', b'must never be written')
        assert (root / 'secret').stat().st_size == 0


def test_ancestor_is_pinned_and_stale_directory_fails(tmp_path):
    parent = tmp_path / 'parent'
    parent.mkdir()
    root = parent / 'private'
    directory = PrivateDirectory.create(root)
    try:
        with pytest.raises(OSError):
            parent.rename(tmp_path / 'replacement')
    finally:
        directory.close()
    root.rename(parent / 'old')
    root.mkdir()
    with pytest.raises(PrivateStorageError):
        PrivateDirectory.open(root)


def test_hardlinked_file_rejected(tmp_path):
    root = tmp_path / 'private'
    with PrivateDirectory.create(root) as directory:
        directory.create_file('secret', b'synthetic')
        os.link(root / 'secret', tmp_path / 'alias')
        with pytest.raises(PrivateStorageError):
            directory.read_file('secret')
        with pytest.raises(PrivateStorageError):
            directory.remove_file('secret')



def test_unprotected_dacl_reset_rejected(tmp_path):
    import ctypes as C
    from qopenbb_ci import windows_security as api
    from qopenbb_ci.windows_private_files import _open
    root = tmp_path / 'private'
    with PrivateDirectory.create(root):
        pass
    handle = _open(root, 0x60000)
    try:
        set_security = api.bind(api.advapi, 'SetSecurityInfo', [api.W.HANDLE, C.c_int, api.D, api.P, api.P, api.P, api.P], api.D)
        acl, descriptor = api.P(), api.P()
        assert api.get_security(handle, 1, 4, None, None, C.byref(acl), None, C.byref(descriptor)) == 0
        try:
            assert set_security(handle, 1, 0x20000004, None, None, acl, None) == 0
        finally:
            api.local_free(descriptor)
    finally:
        api.close(handle)
    with pytest.raises(PrivateStorageError):
        PrivateDirectory.open(root)


def test_owner_sid_mismatch_on_actual_handle_rejected(tmp_path):
    from qopenbb_ci import windows_security as api
    root = tmp_path / 'private'
    with PrivateDirectory.create(root) as directory:
        # Assigning a different owner requires a privilege outside this contract;
        # compare the real handle owner against another expected identity instead.
        directory.protection.sid = 'S-1-5-32-544'
        with pytest.raises(PrivateStorageError, match='owner mismatch'):
            directory.create_file('secret', b'must never be written')
        assert not (root / 'secret').exists()
