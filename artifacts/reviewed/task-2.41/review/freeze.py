import hashlib
import json
from pathlib import Path

ROOT = Path('/mnt/d/Source/QOpenBB')
OUT = ROOT / 'artifacts/task-2.41/review'
IMPL = ROOT / 'artifacts/task-2.41/implementation'
CONTROLLER = ROOT / 'artifacts/task-2.41/controller'
(OUT / 'breadth-snapshot.toml').write_bytes((ROOT / '.kiro/breadth.toml').read_bytes())
review_names = ['verify.py', 'audit.py', 'freeze.py', 'audit.json', 'verdict.md', 'command-status.json', 'frozen-scope.json', 'breadth-snapshot.toml']
review_names += [f'check-{i}.log' for i in range(6)]
paths = [OUT / name for name in review_names]
paths += [IMPL / entry['path'] for entry in json.loads((IMPL / 'publication-allowlist.json').read_text())['files']]
paths.append(IMPL / 'publication-allowlist.json')
paths += list(CONTROLLER.iterdir())
records = []
for path in sorted(paths):
    assert path.is_file()
    records.append({'path': str(path.relative_to(ROOT)), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()})
(OUT / 'publication-allowlist.json').write_text(json.dumps({'files': records, 'review': 'Contents inspected; synthetic source/test/manifests and command logs only. Includes disclosed failed attempts. Controller scripts retain original historical execution paths.', 'excluded': ['full-stage-manifest.json', 'source-stage-manifest.json', 'stage-path.txt', 'dependencies', 'private account/state files', 'environment files', 'scratch stages']}, indent=2) + '\n')
print(f'Frozen {len(records)} reviewed publication entries')
