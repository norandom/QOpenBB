"""Portable publication command; authentication must already exist in Docker."""

import argparse
import json
from pathlib import Path
import subprocess
import tarfile

from qopenbb_ci.publication import publish


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--archive', type=Path, required=True)
    parser.add_argument('--load-report', type=Path, required=True)
    parser.add_argument('--repository', required=True)
    parser.add_argument('--tag', required=True)
    parser.add_argument('--report', type=Path, required=True)
    args = parser.parse_args()
    try:
        # Refuse stale evidence instead of overwriting an earlier success.
        if args.report.exists():
            raise ValueError('publication report already exists')
        result = publish(args.archive, json.loads(args.load_report.read_text()), args.repository, args.tag)
        args.report.parent.mkdir(parents=True, exist_ok=True)
        with args.report.open('x') as stream:
            stream.write(json.dumps(result, indent=2) + '\n')
        print(json.dumps({'valid': True, 'reference': result['reference']}))
        return 0
    except (OSError, ValueError, KeyError, TypeError, IndexError, tarfile.TarError,
            subprocess.SubprocessError) as error:
        print(json.dumps({'valid': False, 'error': type(error).__name__}))
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
