"""Freeze the reviewed tooltip closure with only the authorized fixture repair."""
import hashlib
import json
import shutil
import subprocess
from pathlib import Path

ROOT = Path('/mnt/d/Source/QOpenBB')
OUT = ROOT / 'artifacts/task-2.44/review-repair'
OLD = ROOT / 'artifacts/task-2.44/review'
STAGE = Path('/home/mc/qopenbb-work/task244-independent-review-repair/terminalpro')
OLD_STAGE = Path('/home/mc/qopenbb-work/task244-independent-review/terminalpro')
SOURCE = ROOT / 'vendor/workspace/terminalpro'
REPAIR = 'tests/unit/chart-application/gridCapture.grid.test.ts'
HASH = '47c9793abc7d528d15b3fce807e669d6ef168b88d2c6f213ac316bfe5d4e41b0'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
prior = json.loads((OLD / 'stage-manifest.json').read_text())
STAGE.mkdir(parents=True, exist_ok=False)
entries = []
for item in prior['files']:
    rel = item['path']
    assert sha(OLD_STAGE / rel) == item['sha256']
    origin = SOURCE / rel if rel == REPAIR else OLD_STAGE / rel
    expected = HASH if rel == REPAIR else item['sha256']
    assert sha(origin) == expected == sha(SOURCE / rel), rel
    target = STAGE / rel
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(origin, target)
    entries.append({'path': rel, 'sha256': expected, 'origin': 'authorized-fixture-repair' if rel == REPAIR else 'frozen-prior-review'})
(STAGE / 'node_modules').symlink_to('/home/mc/qopenbb-work/appearance-deps/terminalpro/node_modules', target_is_directory=True)
(OUT / 'stage-manifest.json').write_text(json.dumps({'stage': str(STAGE), 'files': entries}, indent=2) + '\n')
diff = subprocess.run(['git', '-C', str(ROOT / 'vendor/workspace'), 'diff', '--', 'terminalpro/' + REPAIR], check=True, capture_output=True)
(OUT / 'fixture.diff').write_bytes(diff.stdout)
(OUT / 'gridCapture.grid.test.ts').write_bytes((SOURCE / REPAIR).read_bytes())
print(f'Frozen {len(entries)} files; only repaired fixture differs from prior review.')
