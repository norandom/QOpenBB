"""Compatibility entry for the checked Compose coordinator; no legacy JSON reads."""
import argparse
import json
from pathlib import Path
from urllib.parse import urlsplit

from qopenbb_ci.compose_runtime import start, StartRequest
from qopenbb_ci.compose_lifecycle import recreate, stop, status
from qopenbb_ci.native_environment import resolve_environment
from qopenbb_ci.runtime_descriptor import public_projection


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['start', 'restart', 'recreate', 'stop', 'status'])
    parser.add_argument('--private', type=Path, required=True)
    parser.add_argument('--image')
    parser.add_argument('--data-image')
    parser.add_argument('--image-only', action='store_true')
    parser.add_argument('--source', type=Path)
    parser.add_argument('--public-origin')
    parser.add_argument('--remove-state', action='store_true')
    args = parser.parse_args(argv)
    if args.source:
        parser.error('Source overlays are unsupported; use the packaged Compose image pair')
    if args.action == 'start' and (not args.image or not args.data_image or not args.image_only):
        parser.error('start requires --image, --data-image and --image-only')
    if args.remove_state and args.action != 'stop':
        parser.error('--remove-state is valid only for stop')
    port = None
    if args.public_origin:
        parsed = urlsplit(args.public_origin)
        if parsed.scheme != 'http' or parsed.hostname != '127.0.0.1' or parsed.path or not parsed.port:
            parser.error('Explicit HTTP loopback origin required')
        port = parsed.port
    config = resolve_environment(Path(__file__).resolve().parents[2])
    if args.action == 'start':
        result = public_projection(start(StartRequest(config, args.private, args.image, args.data_image, port)))
    elif args.action in {'restart', 'recreate'}:
        result = public_projection(recreate(config, args.private))
    elif args.action == 'stop':
        result = stop(config, args.private, args.remove_state)
    else:
        result = status(config, args.private)
    print(json.dumps(result))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
