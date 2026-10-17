"""Independently freeze the accepted closure plus the five reviewed task files."""
import hashlib
import json
import shutil
import subprocess
from pathlib import Path

ROOT = Path('/mnt/d/Source/QOpenBB')
OUT = ROOT / 'artifacts/task-2.44/review'
IMPL = ROOT / 'artifacts/task-2.44/implementation'
SOURCE = ROOT / 'vendor/workspace/terminalpro'
BASE = Path('/home/mc/qopenbb-work/task241-20261017135547/terminalpro')
STAGE = Path('/home/mc/qopenbb-work/task244-independent-review/terminalpro')
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
owned = json.loads((IMPL / 'source-manifest.json').read_text())
owned_map = {e['source'].removeprefix('vendor/workspace/terminalpro/'): e for e in owned['files']}
entries = json.loads((IMPL / 'final-stage-manifest.json').read_text())['files']
STAGE.mkdir(parents=True, exist_ok=False)
closure = []
for entry in entries:
    rel = entry['path']
    assert not Path(rel).is_absolute() and '..' not in Path(rel).parts
    source = SOURCE / rel if rel in owned_map else BASE / rel
    assert sha(source) == entry['sha256'], rel
    assert sha(SOURCE / rel) == entry['sha256'], f'current closure changed: {rel}'
    if rel in owned_map:
        assert sha(source) == owned_map[rel]['sha256'] == sha(ROOT / owned_map[rel]['snapshot'])
    target = STAGE / rel
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)
    assert sha(target) == entry['sha256']
    closure.append({**entry, 'origin': 'owned-current' if rel in owned_map else 'accepted-2.41'})
(STAGE / 'node_modules').symlink_to('/home/mc/qopenbb-work/appearance-deps/terminalpro/node_modules', target_is_directory=True)
diff = subprocess.run(['git', '-C', str(ROOT / 'vendor/workspace'), 'diff', 'bc42d604855a6b5d943ce05ee9fcce11e356435a', '--', *['terminalpro/' + p for p in owned_map]], capture_output=True, check=True)
(OUT / 'actual-owned.diff').write_bytes(diff.stdout)
assert diff.stdout.decode().replace('\r\n', '\n') == (IMPL / 'owned.diff').read_text()
(OUT / 'stage-manifest.json').write_text(json.dumps({'base': str(BASE), 'stage': str(STAGE), 'files': closure}, indent=2) + '\n')
publication = json.loads((IMPL / 'publication-allowlist.json').read_text())['files']
for entry in publication:
    path = ROOT / entry['path']
    assert path.is_relative_to(IMPL) and sha(path) == entry['sha256']
(OUT / 'input-audit.json').write_text(json.dumps({'owned_files': len(owned_map), 'closure_files': len(closure), 'implementation_artifacts_hash_verified': len(publication), 'actual_diff_matches_frozen': True}, indent=2) + '\n')
print(f'Frozen {len(closure)} closure files and verified {len(publication)} implementation artifacts.')
