import os
import pytest
from qopenbb_ci import session_files as storage


def test_exclusive_create_update_remove(tmp_path):
    root = tmp_path / 'private session'
    with storage.create_session(root) as session:
        session.create_file('descriptor', b'original')
        with pytest.raises(OSError):
            session.create_file('descriptor', b'collision')
    path = root / 'descriptor'
    assert storage.read_private(path) == b'original'
    storage.replace_private(path, b'updated')
    assert storage.read_private(path) == b'updated'
    storage.remove_private(path)
    storage.remove_private(path)
    assert root.is_dir()


def test_interrupted_replace_keeps_last_valid_bytes(tmp_path, monkeypatch):
    with storage.create_session(tmp_path / 'private') as session:
        session.create_file('descriptor', b'last valid')
        original = type(session)._write_handle
        def interrupt(self, handle, payload):
            original(self, handle, payload)
            raise KeyboardInterrupt('synthetic interruption before commit')
        monkeypatch.setattr(type(session), '_write_handle', interrupt)
        with pytest.raises(KeyboardInterrupt):
            session.replace_file('descriptor', b'uncommitted')
        assert session.read_file('descriptor') == b'last valid'
        assert sorted(p.name for p in session.path.iterdir()) == ['descriptor']


def test_confined_names_and_missing_target(tmp_path):
    outside = tmp_path / 'unrelated'
    outside.write_bytes(b'keep')
    with storage.create_session(tmp_path / 'private') as session:
        for name in ['../unrelated', 'a/b', '.', '..', 'a\\b', 'a:b']:
            with pytest.raises(OSError):
                session.remove_file(name)
        with pytest.raises(OSError):
            session.replace_file('missing', b'new')
    assert outside.read_bytes() == b'keep'


def test_checked_hardlinks_refused(tmp_path):
    with storage.create_session(tmp_path / 'private') as session:
        session.create_file('descriptor', b'keep')
        os.link(session.path / 'descriptor', tmp_path / 'alias')
        for operation in [lambda: session.read_file('descriptor'),
                          lambda: session.replace_file('descriptor', b'bad'),
                          lambda: session.remove_file('descriptor')]:
            with pytest.raises(OSError):
                operation()
    assert (tmp_path / 'alias').read_bytes() == b'keep'


def test_read_limit(tmp_path):
    with storage.create_session(tmp_path / 'private') as session:
        session.create_file('descriptor', b'12345')
        with pytest.raises(OSError):
            session.read_file('descriptor', limit=4)
        for limit in [-1, True, 1.5, None]:
            with pytest.raises(ValueError):
                session.read_file('descriptor', limit=limit)


def test_unicode_name_atomic_update(tmp_path):
    with storage.create_session(tmp_path / 'private') as session:
        names = ['descriptor', 'descriptor-\U0001f4c8']
        for name in names:
            session.create_file(name, b'old')
        for iteration in range(16):
            payload = str(iteration).encode()
            for name in names:
                session.replace_file(name, payload)
                assert session.read_file(name) == payload
                assert sorted(p.name for p in session.path.iterdir()) == sorted(names)


@pytest.mark.skipif(os.name != 'nt', reason='native Windows commit failure')
def test_windows_failed_commit_preserves_old(tmp_path, monkeypatch):
    with storage.create_session(tmp_path / 'private') as session:
        session.create_file('descriptor', b'old')
        def refuse(*unused):
            raise OSError('synthetic commit failure')
        monkeypatch.setattr(type(session), '_rename_handle', refuse)
        with pytest.raises(OSError):
            session.replace_file('descriptor', b'new')
        assert session.read_file('descriptor') == b'old'
        assert sorted(p.name for p in session.path.iterdir()) == ['descriptor']


@pytest.mark.skipif(os.name != 'nt', reason='native Windows postcommit interruption')
def test_windows_postcommit_interruption_keeps_committed_file(tmp_path, monkeypatch):
    with storage.create_session(tmp_path / 'private') as session:
        session.create_file('descriptor', b'old')
        original = type(session)._rename_handle
        def interrupt(self, handle, name):
            original(self, handle, name)
            raise KeyboardInterrupt('synthetic interruption after commit')
        monkeypatch.setattr(type(session), '_rename_handle', interrupt)
        with pytest.raises(KeyboardInterrupt):
            session.replace_file('descriptor', b'committed')
        assert session.read_file('descriptor') == b'committed'
        assert sorted(p.name for p in session.path.iterdir()) == ['descriptor']


@pytest.mark.skipif(os.name != 'nt', reason='Windows UTF16 API buffer contract')
def test_windows_rename_buffer_includes_terminator(tmp_path, monkeypatch):
    import ctypes as C
    from qopenbb_ci import windows_security as api
    class Header(C.Structure):
        _fields_ = [('flags', api.D), ('root', api.W.HANDLE),
                    ('length', api.D), ('name', api.W.WCHAR * 1)]
    def check_buffer(handle, kind, pointer, size):
        header = C.cast(pointer, C.POINTER(Header)).contents
        data = C.string_at(pointer, size)
        end = Header.name.offset + header.length
        assert data[end:end + 2] == b'\x00\x00'
        return True
    with storage.create_session(tmp_path / 'private') as session:
        monkeypatch.setattr(api, 'set_info', check_buffer)
        for length in range(1, 9):
            session._rename_handle(0, 'x' * length)


@pytest.mark.skipif(os.name == 'nt', reason='native POSIX descriptor and mode checks')
def test_posix_permissions_symlinks_and_changed_directory(tmp_path):
    root = tmp_path / 'private'
    with storage.create_session(root) as session:
        session.create_file('descriptor', b'keep')
        assert root.stat().st_mode & 0o777 == 0o700
        assert (root / 'descriptor').stat().st_mode & 0o777 == 0o600
        os.chmod(root / 'descriptor', 0o644)
        with pytest.raises(OSError):
            session.read_file('descriptor')
        os.chmod(root / 'descriptor', 0o600)
        (root / 'link').symlink_to(root / 'descriptor')
        with pytest.raises(OSError):
            session.remove_file('link')
        root.rename(tmp_path / 'old')
        root.mkdir(mode=0o700)
        with pytest.raises(OSError):
            session.create_file('new', b'never')
    assert not (root / 'new').exists()
