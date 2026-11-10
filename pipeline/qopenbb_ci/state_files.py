"""State storage boundary, distinct from private runtime descriptors."""
import os
from pathlib import Path

if os.name == 'nt':
    from .windows_state_files import StateDirectory as PrivateDirectory
else:
    from .posix_private_files import PrivateDirectory


def create_state(path):
    return PrivateDirectory.create(path)


def read_private(path, limit=1024 * 1024):
    path = Path(path)
    with PrivateDirectory.open(path.parent) as directory:
        return directory.read_file(path.name, limit)


def verify_generated(directory, names=('openbb.db', 'secrets.env')):
    """Return host ACL evidence on Windows; retain POSIX guest mode authority."""
    if os.name != 'nt':
        directory.verify()
        return {}
    return {name: directory.generated_metadata(name) for name in names}
