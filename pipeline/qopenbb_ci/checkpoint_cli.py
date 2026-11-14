"""Create one private research checkpoint through bounded stdin IPC."""
import argparse
import json
from pathlib import Path
import sys
from urllib.parse import urlsplit

from . import session_files
from .runtime_descriptor import parse_descriptor

MAX_BYTES = 1024 * 1024
NAME = 'research-retention.json'
KEYS = {'stage', 'images', 'runtimeName', 'containerId', 'dashboardPath', 'state', 'selected'}


def reject_constant(value):
    raise ValueError('Invalid JSON')


def validate_payload(payload, descriptor):
    value = json.loads(payload, parse_constant=reject_constant)
    if not isinstance(value, dict) or value.keys() != KEYS:
        raise ValueError('Invalid checkpoint shape')
    path = value['dashboardPath']
    parsed = urlsplit(path) if isinstance(path, str) else None
    if (descriptor.phase != 'ready' or value['stage'] != 'initial-complete'
            or value['images'] != descriptor.images or value['runtimeName'] != descriptor.name
            or value['containerId'] != descriptor.container
            or not parsed or not path.startswith('/app/') or parsed.query or parsed.fragment
            or parsed.netloc or '..' in parsed.path.split('/')
            or not isinstance(value['state'], dict) or not isinstance(value['selected'], dict)):
        raise ValueError('Checkpoint/runtime binding mismatch')


def write_checkpoint(runtime_path, checkpoint_path, payload):
    runtime, checkpoint = Path(runtime_path), Path(checkpoint_path)
    if (not runtime.is_absolute() or not checkpoint.is_absolute() or runtime.name != 'runtime.json'
            or checkpoint.name != NAME or checkpoint.parent != runtime.parent
            or not isinstance(payload, bytes) or not 0 < len(payload) <= MAX_BYTES):
        raise ValueError('Checkpoint scope refused')
    # Pin the verified session through descriptor validation and exclusive creation.
    with session_files.PrivateDirectory.open(runtime.parent) as directory:
        descriptor = parse_descriptor(directory.read_file(runtime.name))
        validate_payload(payload, descriptor)
        directory.create_file(NAME, payload)


class PrivateParser(argparse.ArgumentParser):
    def error(self, message):
        self.exit(2, 'Invalid checkpoint command arguments\n')


def main(argv=None):
    parser = PrivateParser(description='Create a checked private research checkpoint')
    parser.add_argument('--runtime', required=True)
    parser.add_argument('--path', required=True)
    args = parser.parse_args(argv)
    try:
        if not session_files.captured_private_output(sys.stdin):
            raise ValueError('Captured stdin pipe required')
        payload = sys.stdin.buffer.read(MAX_BYTES + 1)
        write_checkpoint(args.runtime, args.path, payload)
        return 0
    except (OSError, ValueError, TypeError, RecursionError):
        print('Checkpoint write refused', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
