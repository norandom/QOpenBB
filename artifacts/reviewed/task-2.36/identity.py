import hashlib
import json
import subprocess
from pathlib import Path

root = Path('/mnt/d/Source/QOpenBB')
repo = root / 'vendor/workspace'
stage = Path('/home/mc/qopenbb-work/task236/terminalpro')
paths = []
for directory in ('src/components/General/Table/Chart/compatibility', 'src/components/General/Table/Chart/echarts', 'tests/unit/chart-compatibility', 'tests/e2e/chart-compatibility'):
    paths += sorted(p.relative_to(repo) for p in (repo / 'terminalpro' / directory).rglob('*') if p.is_file())
paths += [Path('terminalpro') / p for p in ('src/components/General/Table/Chart/application/types.ts', 'src/components/General/Table/Chart/application/financialFormatting.ts', 'tests/unit/chart-application/financialFormatting.test.ts', 'tests/unit/chart-application/financialFormatting.sources.json', 'tests/unit/chart-application/contracts.types.ts', 'tests/unit/chart-application/tsconfig.json', 'tests/unit/chart-application/vitest.config.mjs')]
def git(*args):
    return subprocess.check_output(['git', '-C', str(repo), *args])
def sha(data):
    return hashlib.sha256(data).hexdigest()
files = []
for p in paths:
    actual = sha((repo / p).read_bytes())
    staged = sha((stage / p.relative_to('terminalpro')).read_bytes())
    assert actual == staged, p
    files.append({'path': str(p), 'sha256': actual, 'staged_sha256': staged})
pin = '38dffc33389aca0e4a87e0e88d42f7067aa220df'
originals = ['terminalpro/src/components/General/Table/Chart/utils.tsx', 'terminalpro/src/components/General/Table/Chart/hooks/useChartOptions.tsx', 'terminalpro/src/components/General/Table/AgGridUtils.tsx', 'terminalpro/src/lib/utils/utils.ts']
helpers = json.loads((repo / 'terminalpro/tests/unit/chart-application/financialFormatting.sources.json').read_text())
for item in helpers['sources']:
    assert item['fullSourceSha256'] == sha(git('show', f"{pin}:{item['path']}"))
    assert item['codeSha256'] == sha(item['code'].encode())
result = {'head': git('rev-parse', 'HEAD').decode().strip(), 'original_pin': pin, 'stage': str(stage), 'exact_source_and_config_bytes': files, 'original_source_hashes': {p: sha(git('show', f'{pin}:{p}')) for p in originals}, 'dirty_tracked_paths': git('diff', '--name-only', 'HEAD').decode().splitlines(), 'untracked_paths': git('ls-files', '--others', '--exclude-standard').decode().splitlines(), 'scope_note': 'Only financialFormatting.ts, its test and parent-approved test-only source fixture belong to B1. A1 runtime files excluded from staged application inputs. Dirty paths are not acceptance.', 'node_version': subprocess.check_output([str(root / 'artifacts/task-1.2/node-v24.22.0-linux-x64/bin/node'), '--version']).decode().strip()}
(root / 'artifacts/task-2.36/identity.json').write_text(json.dumps(result, indent=2) + '\n')
print(f'{len(files)} current/staged source hashes match; original source/fixture hashes verified; HEAD {result["head"]}')
