"""Byte-level private session storage; descriptor schema belongs to its consumer."""
import os
from pathlib import Path
import socket
import stat

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


def captured_private_output(stream) -> bool:
    if stream.isatty():
        return False
    fd = stream.fileno()
    mode = os.fstat(fd).st_mode
    if stat.S_ISFIFO(mode):
        return True
    if os.name == 'nt' or not stat.S_ISSOCK(mode):
        return False
    # Node uses anonymous Unix stream socketpairs for captured child stdio.
    duplicate = os.dup(fd)
    try:
        connection = socket.socket(fileno=duplicate)
    except OSError:
        os.close(duplicate)
        return False
    try:
        with connection:
            return (connection.family == socket.AF_UNIX and connection.type == socket.SOCK_STREAM
                    and connection.getsockname() == '' and connection.getpeername() == '')
    except OSError:
        return False


def main(argv=None) -> int:
    import argparse
    import json
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
        if args.private_ipc and not captured_private_output(sys.stdout):
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
