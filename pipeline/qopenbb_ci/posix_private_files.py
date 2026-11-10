"""Owner-only POSIX session files accessed relative to checked directory fds."""
from contextlib import contextmanager
import os
from pathlib import Path
import stat
import uuid


class PrivateStorageError(OSError):
    """Private object ownership, permissions or identity could not be verified."""


def _leaf(name):
    if not isinstance(name, str) or not name or name in ('.', '..'):
        raise PrivateStorageError('Unsafe private storage filename')
    if any(character in name for character in ('/', '\\', ':', '\x00')):
        raise PrivateStorageError('Unsafe private storage filename')
    return name


def _same(first, second):
    if (first.st_dev, first.st_ino) != (second.st_dev, second.st_ino):
        raise PrivateStorageError('Private object identity changed')


def _protection(info, directory=False):
    expected = 0o700 if directory else 0o600
    kind = stat.S_ISDIR if directory else stat.S_ISREG
    if info.st_uid != os.getuid() or stat.S_IMODE(info.st_mode) != expected:
        raise PrivateStorageError('Private object owner or permissions mismatch')
    if not kind(info.st_mode) or (not directory and info.st_nlink != 1):
        raise PrivateStorageError('Private object type or link count mismatch')


class PrivateDirectory:
    def __init__(self, path, create=False):
        self.path = Path(path)
        self.handles = []
        if not self.path.is_absolute() or len(self.path.parts) < 2:
            raise PrivateStorageError('Private storage requires an absolute nonroot path')
        try:
            self._pin(create)
        except BaseException:
            self.close()
            raise

    @classmethod
    def create(cls, path):
        return cls(path, create=True)

    @classmethod
    def open(cls, path):
        return cls(path)

    @classmethod
    def open_for_removal(cls, path):
        raise PrivateStorageError('Checked directory removal is not supported on POSIX')

    def _pin(self, create):
        self.handles.append(os.open('/', os.O_RDONLY | os.O_DIRECTORY))
        for index, component in enumerate(self.path.parts[1:], 1):
            _leaf(component)
            if create and index == len(self.path.parts) - 1:
                os.mkdir(component, 0o700, dir_fd=self.handles[-1])
            fd = os.open(component, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
                         dir_fd=self.handles[-1])
            self.handles.append(fd)
        self.verify()

    @property
    def handle(self):
        if not self.handles:
            raise PrivateStorageError('Private directory is closed')
        return self.handles[-1]

    def verify(self):
        _protection(os.fstat(self.handle), directory=True)
        for index, component in enumerate(self.path.parts[1:]):
            _same(os.fstat(self.handles[index + 1]),
                  os.stat(component, dir_fd=self.handles[index], follow_symlinks=False))

    def _checked_entry(self, name, fd):
        self.verify()
        info = os.fstat(fd)
        _protection(info)
        _same(info, os.stat(name, dir_fd=self.handle, follow_symlinks=False))

    @contextmanager
    def file_handle(self, name, access=os.O_RDONLY, create=False):
        self.verify()
        _leaf(name)
        flags = access | os.O_NOFOLLOW | os.O_NONBLOCK
        if create:
            flags |= os.O_CREAT | os.O_EXCL
        fd = os.open(name, flags, 0o600, dir_fd=self.handle)
        try:
            self._checked_entry(name, fd)
            yield fd
        finally:
            os.close(fd)

    def _write_handle(self, fd, payload):
        self.verify()
        _protection(os.fstat(fd))
        remaining = memoryview(payload)
        while remaining:
            count = os.write(fd, remaining)
            if count <= 0:
                raise PrivateStorageError('Incomplete private file write')
            remaining = remaining[count:]
        os.fsync(fd)

    def create_file(self, name, payload):
        with self.file_handle(name, os.O_WRONLY, create=True) as fd:
            try:
                self._write_handle(fd, payload)
            except BaseException:
                self._checked_entry(name, fd)
                os.unlink(name, dir_fd=self.handle)
                raise

    def read_file(self, name, limit=1024 * 1024):
        if type(limit) is not int or limit < 0:
            raise ValueError('Private file size limit must be a nonnegative integer')
        with self.file_handle(name) as fd:
            chunks, total = [], 0
            while True:
                chunk = os.read(fd, 65536)
                if not chunk:
                    return b''.join(chunks)
                total += len(chunk)
                if total > limit:
                    raise PrivateStorageError('Private file exceeds size limit')
                chunks.append(chunk)

    def replace_file(self, name, payload):
        temporary = f'.replace-{uuid.uuid4().hex}'
        with self.file_handle(name) as target:
            with self.file_handle(temporary, os.O_WRONLY, create=True) as source:
                try:
                    self._write_handle(source, payload)
                    self._checked_entry(name, target)
                    self._checked_entry(temporary, source)
                    os.replace(temporary, name, src_dir_fd=self.handle, dst_dir_fd=self.handle)
                except BaseException:
                    self._checked_entry(temporary, source)
                    os.unlink(temporary, dir_fd=self.handle)
                    raise

    def remove_file(self, name):
        try:
            with self.file_handle(name) as fd:
                self._checked_entry(name, fd)
                os.unlink(name, dir_fd=self.handle)
        except FileNotFoundError:
            self.verify()

    def remove_empty(self):
        """Remove only the verified entry relative to its pinned parent fd."""
        self.verify()
        raise PrivateStorageError('Checked directory removal is not supported on POSIX')

    def close(self):
        for fd in reversed(self.handles):
            os.close(fd)
        self.handles.clear()

    def __enter__(self):
        return self

    def __exit__(self, *unused):
        self.close()
