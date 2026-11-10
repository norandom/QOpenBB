"""Byte-level private session storage; descriptor schema belongs to its consumer."""
import os
from pathlib import Path

if os.name == 'nt':
    from .windows_private_files import PrivateDirectory, PrivateStorageError
else:
    from .posix_private_files import PrivateDirectory, PrivateStorageError


def create_session(root: Path) -> PrivateDirectory:
    """Create a private directory and retain its checked handles until closed."""
    return PrivateDirectory.create(root)


def read_private(path: Path, limit=1024 * 1024) -> bytes:
    path = Path(path)
    with PrivateDirectory.open(path.parent) as directory:
        return directory.read_file(path.name, limit)


def replace_private(path: Path, payload: bytes) -> None:
    path = Path(path)
    with PrivateDirectory.open(path.parent) as directory:
        directory.replace_file(path.name, payload)


def remove_private(path: Path) -> None:
    path = Path(path)
    with PrivateDirectory.open(path.parent) as directory:
        directory.remove_file(path.name)
