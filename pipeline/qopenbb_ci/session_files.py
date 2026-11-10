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


def main(argv=None) -> int:
    import argparse
    import json
    import stat
    import sys

    from .runtime_descriptor import read_private as read_descriptor, public_projection

    class PrivateArgumentParser(argparse.ArgumentParser):
        def error(self, message):
            self.exit(2, 'Invalid runtime descriptor command arguments\n')

    parser = PrivateArgumentParser(description='Read a checked runtime descriptor')
    parser.add_argument('action', choices=['read'])
    parser.add_argument('--path', required=True)
    parser.add_argument('--private-ipc', action='store_true')
    args = parser.parse_args(argv)
    try:
        if args.private_ipc and (sys.stdout.isatty()
                or not stat.S_ISFIFO(os.fstat(sys.stdout.fileno()).st_mode)):
            raise ValueError('private output requires a captured pipe')
        descriptor = read_descriptor(Path(args.path))
        result = descriptor.model_dump(mode='json') if args.private_ipc else public_projection(descriptor)
        print(json.dumps(result, ensure_ascii=True))
        return 0
    except (OSError, ValueError, TypeError, RecursionError):
        print('Runtime descriptor read refused', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
