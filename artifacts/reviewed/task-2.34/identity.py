import hashlib
import json
import subprocess
from pathlib import Path

root = Path('/mnt/d/Source/QOpenBB')
repo = root / 'vendor/workspace'
stage = Path('/home/mc/qopenbb-work/task234/terminalpro')
chart = Path('terminalpro/src/components/General/Table/Chart')
paths = sorted(p.relative_to(repo) for p in (repo / chart).rglob('*') if p.is_file())
paths += sorted(p.relative_to(repo) for p in (repo / 'terminalpro/tests/unit/chart-application').rglob('*') if p.is_file())
for directory in ('terminalpro/tests/unit/chart-compatibility', 'terminalpro/tests/e2e/chart-compatibility'):
    paths += sorted(p.relative_to(repo) for p in (repo / directory).rglob('*') if p.is_file())
paths += [Path('terminalpro/src/lib/utils/utils.ts'),
          Path('terminalpro/src/components/General/Table/AgGridUtils.tsx')]

def git(*args):
    return subprocess.check_output(['git', '-C', str(repo), *args])

def digest(data):
    return hashlib.sha256(data).hexdigest()

files = []
for path in paths:
    local = repo / path
    copied = stage / path.relative_to('terminalpro')
    sha = digest(local.read_bytes())
    staged_sha = digest(copied.read_bytes())
    assert sha == staged_sha, path
    files.append({'path': str(path), 'sha256': sha, 'staged_sha256': staged_sha})
pin = '38dffc33389aca0e4a87e0e88d42f7067aa220df'
originals = [str(chart / 'utils.tsx'),
             str(chart / 'hooks/useChartOptions.tsx'),
             'terminalpro/src/components/General/Table/hooks/useTableContext.tsx',
             'terminalpro/src/components/General/Table/hooks/useUpdateColumnState.ts',
             'terminalpro/src/lib/utils/utils.ts']
result = {
    'head': git('rev-parse', 'HEAD').decode().strip(),
    'original_pin': pin,
    'stage': str(stage.resolve()),
    'node_version': subprocess.check_output([str(root / 'artifacts/task-1.2/node-v24.22.0-linux-x64/bin/node'), '--version']).decode().strip(),
    'dirty_tracked_paths': git('diff', '--name-only', 'HEAD').decode().splitlines(),
    'untracked_paths': git('ls-files', '--others', '--exclude-standard').decode().splitlines(),
    'exact_source_and_config_bytes': files,
    'original_source_hashes': {p: digest(git('show', f'{pin}:{p}')) for p in originals},
    'scope_note': 'Dirty path lists describe concurrent work, not ownership or acceptance. Only application/types.ts and the new application test configurations/contracts belong to 2.34.',
}
(root / 'artifacts/task-2.34/identity.json').write_text(json.dumps(result, indent=2) + '\n')
print(f'{len(files)} staged source/config hashes match current bytes; HEAD {result["head"]}')
