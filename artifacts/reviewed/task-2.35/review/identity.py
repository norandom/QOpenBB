import hashlib
import json
import subprocess
import sys
from pathlib import Path
root = Path('/mnt/d/Source/QOpenBB')
sys.path.insert(0, str(root))
from tools.quality.ts_adapter import measure_typescript
repo = root / 'vendor/workspace/terminalpro'
stage = Path('/home/mc/qopenbb-work/task235/terminalpro')
owned = ['src/components/General/Table/Chart/application/chartRange.ts', 'src/components/General/Table/Chart/application/sessionState.ts', 'tests/unit/chart-application/chartRange.test.ts', 'tests/unit/chart-application/sessionState.test.ts']
paths = owned + ['src/components/General/Table/Chart/application/types.ts', 'tests/unit/chart-application/contracts.types.ts', 'tests/unit/chart-application/tsconfig.json', 'tests/unit/chart-application/vitest.config.mjs']
for directory in ['src/components/General/Table/Chart/compatibility', 'tests/unit/chart-compatibility', 'tests/e2e/chart-compatibility']:
    paths += [str(p.relative_to(repo)) for p in (repo / directory).rglob('*') if p.is_file()]
files = []
for path in sorted(paths):
    source = (repo / path).read_bytes()
    copied = (stage / path).read_bytes()
    assert source == copied, path
    files.append({'path': path, 'sha256': hashlib.sha256(source).hexdigest(), 'staged_sha256': hashlib.sha256(copied).hexdigest()})
assert next(f['sha256'] for f in files if f['path'].endswith('application/types.ts')) == '5e01f153244005180a284d591f0732fd24f5b1bec804c4c59a8e831cb4e8696e'
production = [str(repo / path) for path in owned[:2]]
measurements, versions = measure_typescript(production)
for path, row in measurements.items():
    row['physical'] = len(Path(path).read_text().splitlines())
    assert row['physical'] <= 400 and row['logical'] <= 300
    assert all(f['logical'] <= 50 for f in row['functions'])
result = {'workspace_head': subprocess.check_output(['git', '-C', str(repo), 'rev-parse', 'HEAD'], text=True).strip(), 'stage': str(stage.resolve()), 'files': files, 'syntax_parser': versions, 'measurements': measurements, 'scope': 'Owned A1 plus frozen inputs only; B1 excluded; no runtime activation or full-suite acceptance'}
(root / 'artifacts/task-2.35/review/identity.json').write_text(json.dumps(result, indent=2) + '\n')
print(f'{len(files)} source/stage hashes match')
for path, row in measurements.items():
    print(f'{Path(path).name}: physical={row["physical"]}, logical={row["logical"]}, max-function={max(f["logical"] for f in row["functions"])}')

