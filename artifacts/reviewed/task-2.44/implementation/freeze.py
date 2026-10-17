"""Freeze owned review bytes and a safe publication allowlist after verification."""
import hashlib
import json
import shutil
import subprocess
from pathlib import Path

ROOT = Path('/mnt/d/Source/QOpenBB')
OUT = ROOT / 'artifacts/task-2.44/implementation'
REPO = ROOT / 'vendor/workspace'
FILES = [
    'terminalpro/src/components/General/Table/Chart/compatibility/optionStateTypes.ts',
    'terminalpro/src/components/General/Table/Chart/compatibility/editorEvents.ts',
    'terminalpro/src/components/General/Table/Chart/application/sessionState.ts',
    'terminalpro/tests/unit/chart-compatibility/editorEvents.test.ts',
    'terminalpro/tests/unit/chart-application/sessionState.test.ts',
]
records = []
for relative in FILES:
    source = REPO / relative
    target = OUT / 'source' / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)
    records.append({'source': str(source.relative_to(ROOT)),
                    'snapshot': str(target.relative_to(ROOT)),
                    'sha256': hashlib.sha256(source.read_bytes()).hexdigest()})
diff = subprocess.run(['git', '-C', str(REPO), 'diff', '--', *FILES],
                      check=True, capture_output=True, text=True)
(OUT / 'owned.diff').write_text(diff.stdout)
(OUT / 'source-manifest.json').write_text(json.dumps({
    'base': 'bc42d604855a6b5d943ce05ee9fcce11e356435a', 'files': records,
}, indent=2) + '\n')
allowlist = []
for path in sorted(OUT.rglob('*')):
    if path.is_file() and path.name != 'publication-allowlist.json':
        allowlist.append({'path': str(path.relative_to(ROOT)),
                          'sha256': hashlib.sha256(path.read_bytes()).hexdigest()})
(OUT / 'publication-allowlist.json').write_text(json.dumps({
    'scope': 'Synthetic tests, owned source, deterministic scripts and check logs only; no credentials or private state.',
    'files': allowlist,
}, indent=2) + '\n')
for item in allowlist:
    assert hashlib.sha256((ROOT / item['path']).read_bytes()).hexdigest() == item['sha256']
print(f'Frozen {len(records)} owned files and {len(allowlist)} safe artifact hashes.')
