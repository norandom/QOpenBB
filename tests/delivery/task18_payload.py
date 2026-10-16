"""Prepare an explicit, secret-free input mount for the clean userspace experiment."""

import hashlib
import json
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[2]
DESTINATION = Path('/tmp/qopenbb-task18/runner-inputs')
PROJECT = DESTINATION / 'project'


def main():
    DESTINATION.mkdir(parents=True, exist_ok=False)
    files = ['pipeline/pyproject.toml', 'pipeline/uv.lock', 'pipeline/tools.lock.json',
             '.dagger/pyproject.toml', '.dagger/uv.lock', 'sources.lock.json',
             'contracts/sources.json', 'tests/delivery/task18_inspect.py',
             'tests/delivery/test_image_builds.py', 'tests/delivery/task18_runner.sh']
    for directory in ['pipeline/qopenbb_ci', '.dagger/src/qopenbb']:
        files += [str(path.relative_to(ROOT)) for path in (ROOT / directory).glob('*.py')]
    for name in files:
        target = PROJECT / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / name, target)
    binaries = {name: Path(shutil.which(name)) for name in ['dagger', 'uv', 'docker']}
    binaries['safe-chain'] = ROOT / 'artifacts/task-1.2/safe-chain/bin/safe-chain'
    for name, source in binaries.items():
        target = DESTINATION / ('tools/safe-chain/bin' if name == 'safe-chain' else 'tools/bin') / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
    manifest = {str(path.relative_to(DESTINATION)): hashlib.sha256(path.read_bytes()).hexdigest()
                for path in DESTINATION.rglob('*') if path.is_file()}
    (ROOT / 'artifacts/task-1.8/runner-inputs.json').write_text(json.dumps(manifest, indent=2) + '\n')


if __name__ == '__main__':
    main()
