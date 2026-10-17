"""Complete the referenced configuration omitted by the reviewer stage manifest."""
import hashlib
import json
import shutil
from pathlib import Path

ROOT = Path('/mnt/d/Source/QOpenBB')
OUT = ROOT / 'artifacts/task-2.44/review'
STAGE = Path('/home/mc/qopenbb-work/task244-independent-review/terminalpro')
BASE = Path('/home/mc/qopenbb-work/task241-20261017135547/terminalpro')
rel = 'tsconfig.node.json'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(BASE / rel) == sha(ROOT / 'vendor/workspace/terminalpro' / rel)
shutil.copyfile(BASE / rel, STAGE / rel)
manifest = json.loads((OUT / 'stage-manifest.json').read_text())
manifest['files'].append({'path': rel, 'sha256': sha(BASE / rel), 'origin': 'accepted-2.41'})
(OUT / 'stage-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
(OUT / 'staging-failure.md').write_text('The first independent compatibility run failed before collection because the reviewer copied the implementation\'s explicit 70-file manifest, which omitted tsconfig.node.json. Root tsconfig.json references this file. The original accepted stage already contained it. repair-stage.py copies only that configuration after verifying accepted/current SHA256 identity. compatibility.log/json preserve the failed attempt; compatibility-complete.log/json record the corrected stage run. No production or dependency bytes changed.\n')
print('Added accepted referenced tsconfig.node.json to independent closure.')
