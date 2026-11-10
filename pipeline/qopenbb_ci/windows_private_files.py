"""Pinned, user-only Windows objects; payloads never use unchecked path I/O."""
from contextlib import contextmanager
import ctypes as C
from ctypes import wintypes as W
import os
from pathlib import Path
import re
import uuid
from . import windows_security as api
from .windows_security import PrivateStorageError


READ_CONTROL = 0x20000
DELETE = 0x10000
READ = 0x80000000
WRITE = 0x40000000
FLAGS = 0x02000000 | 0x00200000


def _path(value):
    path = Path(value)
    if not path.is_absolute() or path.anchor.startswith('\\\\') or len(path.parts) < 2:
        raise PrivateStorageError('Private storage requires an absolute local nonroot path')
    if any(part in ('.', '..') or ':' in part or part.endswith(('.', ' ')) for part in path.parts[1:]):
        raise PrivateStorageError('Unsafe private storage path')
    for component in path.parts[1:]:
        _leaf(component)
    return path


def _leaf(name):
    if not isinstance(name, str) or not name or re.search(r'[\\/:<>"|?*\x00-\x1f]', name):
        raise PrivateStorageError('Unsafe private storage filename')
    if name.endswith(('.', ' ')) or name in ('.', '..'):
        raise PrivateStorageError('Unsafe private storage filename')
    if name.split('.')[0].upper() in {'CON', 'PRN', 'AUX', 'NUL', *(f'COM{i}' for i in range(10)), *(f'LPT{i}' for i in range(10))}:
        raise PrivateStorageError('Reserved private storage filename')
    return name


def _identity(handle, path, directory):
    info = api.FileInfo()
    api.checked(api.file_info(handle, C.byref(info)))
    if info.attributes & 0x400 or bool(info.attributes & 0x10) != directory:
        raise PrivateStorageError('Reparse points or wrong object types are forbidden')
    if not directory and info.links != 1:
        raise PrivateStorageError('Private files must not have hard links')
    buffer = C.create_unicode_buffer(32768)
    length = api.final_path(handle, buffer, len(buffer), 0)
    if not length or length >= len(buffer):
        raise PrivateStorageError('Cannot establish private object final path')
    actual = buffer.value.removeprefix('\\\\?\\')
    if os.path.normcase(os.path.normpath(actual)) != os.path.normcase(os.path.normpath(str(path))):
        raise PrivateStorageError('Private object path identity mismatch')


def _open(path, access=READ_CONTROL | 1, disposition=3, protection=None, sharing=3):
    attributes = C.byref(protection.attributes) if protection else None
    handle = api.create_file(str(path), access, sharing, attributes, disposition, FLAGS, None)
    if handle == C.c_void_p(-1).value:
        raise PrivateStorageError('Cannot open private storage object', C.get_last_error())
    return handle


def _delete(handle):
    disposition = W.BOOL(True)
    api.checked(api.set_info(handle, 4, C.byref(disposition), C.sizeof(disposition)))


class PrivateDirectory:
    """Hold ancestor handles until all checked operations have finished.

    Sharing excludes deletion, so ordinary callers cannot rename any ancestor
    between path validation and file creation. Administrative takeover is excluded.
    """
    root_protection_type = api.Protection

    def __init__(self, path, create=False, delete=False):
        self.path = _path(path)
        self.delete = delete
        self.handles = []
        self.protection = api.Protection()
        self.root_protection = (self.protection if self.root_protection_type is api.Protection
                                else self.root_protection_type())
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
        return cls(path, delete=True)

    def _pin(self, create):
        current = Path(self.path.anchor)
        handle = _open(current)
        self.handles.append(handle)
        _identity(handle, current, True)
        for component in self.path.parts[1:]:
            current /= component
            if create and current == self.path:
                api.checked(api.create_directory(str(current), C.byref(self.root_protection.attributes)))
            handle = _open(current, READ_CONTROL | 1 | (DELETE if current == self.path and self.delete else 0))
            self.handles.append(handle)
            _identity(handle, current, True)
        self.root_protection.verify(self.handles[-1])

    @property
    def handle(self):
        if not self.handles:
            raise PrivateStorageError('Private directory is closed')
        return self.handles[-1]

    def verify(self):
        _identity(self.handle, self.path, True)
        self.root_protection.verify(self.handle)

    @contextmanager
    def file_handle(self, name, access=READ, create=False, sharing=3):
        """Yield a checked handle; exclusive creation occurs before any payload write."""
        self.verify()
        path = self.path / _leaf(name)
        handle = _open(path, access | READ_CONTROL | DELETE, 1 if create else 3,
                       self.protection if create else None, sharing)
        try:
            _identity(handle, path, False)
            self.protection.verify(handle)
            yield handle
        finally:
            api.close(handle)

    def create_file(self, name, payload):
        with self.file_handle(name, WRITE, create=True) as handle:
            try:
                self._write_handle(handle, payload)
            except BaseException:
                _delete(handle)
                raise

    def _write_handle(self, handle, payload):
        self.verify()
        self.protection.verify(handle)
        buffer = C.create_string_buffer(payload)
        written = W.DWORD()
        api.checked(api.write(handle, buffer, len(payload), C.byref(written), None))
        if written.value != len(payload):
            raise PrivateStorageError('Incomplete private file write')
        api.checked(api.flush(handle))

    def read_file(self, name, limit=1024 * 1024):
        if type(limit) is not int or limit < 0:
            raise ValueError('Private file size limit must be a nonnegative integer')
        with self.file_handle(name) as handle:
            chunks, total = [], 0
            while True:
                buffer, count = C.create_string_buffer(65536), W.DWORD()
                api.checked(api.read(handle, buffer, len(buffer), C.byref(count), None))
                if not count.value:
                    return b''.join(chunks)
                total += count.value
                if total > limit:
                    raise PrivateStorageError('Private file exceeds size limit')
                chunks.append(buffer.raw[:count.value])

    def remove_file(self, name):
        try:
            with self.file_handle(name, 0) as handle:
                self.verify()
                self.protection.verify(handle)
                _delete(handle)
        except PrivateStorageError as error:
            if len(error.args) < 2 or error.args[1] != 2:
                raise

    def replace_file(self, name, payload):
        temporary = f'.replace-{uuid.uuid4().hex}'
        with self.file_handle(name, 0, sharing=7) as target:
            with self.file_handle(temporary, WRITE, create=True) as source:
                try:
                    self._write_handle(source, payload)
                    self.verify()
                    _identity(source, self.path / temporary, False)
                    self.protection.verify(source)
                    _identity(target, self.path / name, False)
                    self.protection.verify(target)
                    self._rename_handle(source, name)
                except BaseException:
                    self._discard_temporary(source, temporary)
                    raise

    def _discard_temporary(self, handle, name):
        # An interruption can arrive after the rename committed. Never delete
        # the source handle unless it still identifies the owned temporary name.
        try:
            self.verify()
            _identity(handle, self.path / name, False)
            self.protection.verify(handle)
        except PrivateStorageError:
            return
        _delete(handle)

    def _rename_handle(self, handle, name):
        # Replacement requires delete sharing on the retained checked target.
        # Renaming replaces the entry itself; it never follows a substituted link.
        name = str(self.path / name)
        length = len(name.encode('utf-16-le'))
        class RenameInfo(C.Structure):
            _fields_ = [('flags', W.DWORD), ('root', W.HANDLE),
                        ('length', W.DWORD), ('name', W.WCHAR * (length // 2 + 1))]
        info = RenameInfo(3, None, length, name)
        api.checked(api.set_info(handle, 22, C.byref(info), C.sizeof(info)))

    def remove_empty(self):
        """Delete the checked directory by handle; nonempty directories fail."""
        self.verify()
        _delete(self.handle)

    def close(self):
        for handle in reversed(self.handles):
            api.close(handle)
        self.handles.clear()
        self.protection.close()
        if self.root_protection is not self.protection:
            self.root_protection.close()

    def __enter__(self):
        return self

    def __exit__(self, *unused):
        self.close()
