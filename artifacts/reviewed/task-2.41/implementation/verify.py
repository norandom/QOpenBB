import hashlib
import json
import os
import pathlib
import subprocess

ROOT = pathlib.Path('/mnt/d/Source/QOpenBB')
OUT = ROOT / 'artifacts/task-2.41/implementation'
stage = pathlib.Path((OUT / 'stage-path.txt').read_text().strip())
env = dict(os.environ, PATH=str(ROOT / 'artifacts/task-1.2/node-v24.22.0-linux-x64/bin') + ':' + os.environ['PATH'])
commands = [
    ['node', '--version'],
    ['node', 'node_modules/typescript/bin/tsc', '--project', 'tests/unit/chart-application/tsconfig.json', '--noEmit'],
    ['node', 'node_modules/typescript/bin/tsc', '--project', 'tests/unit/chart-compatibility/tsconfig.json', '--noEmit'],
    ['node', 'node_modules/vitest/vitest.mjs', 'run', '--config', 'tests/unit/chart-application/vitest.config.mjs'],
    ['node', 'node_modules/vitest/vitest.mjs', 'run', '--config', 'tests/unit/chart-compatibility/vitest.config.mjs'],
    ['node', 'node_modules/@biomejs/biome/bin/biome', 'check', 'src/components/General/Table/Chart/application', 'src/components/General/Table/Chart/compatibility/editorEvents.ts', 'src/components/General/Table/Chart/compatibility/optionStateTypes.ts', 'tests/unit/chart-application', 'tests/unit/chart-compatibility/editorEvents.test.ts'],
]
results = []
for index, command in enumerate(commands):
    result = subprocess.run(command, cwd=stage, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    log = OUT / f'check-{index}.log'
    log.write_text(result.stdout)
    results.append({'command': command, 'cwd': str(stage), 'exitCode': result.returncode,
                    'log': str(log.relative_to(ROOT)), 'sha256': hashlib.sha256(log.read_bytes()).hexdigest()})
    (OUT / 'command-status.json').write_text(json.dumps(results, indent=2) + '\n')
    print(index, result.returncode, flush=True)
