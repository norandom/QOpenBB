"""Measure owned whole production files with the existing project syntax checker."""
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path('/mnt/d/Source/QOpenBB')
OUT = ROOT / 'artifacts/task-2.44/implementation'
BASE = ROOT / 'vendor/workspace/terminalpro/src/components/General/Table/Chart'
PATHS = [BASE / path for path in [
    'compatibility/optionStateTypes.ts',
    'compatibility/editorEvents.ts',
    'application/sessionState.ts',
]]
command = [str(ROOT / 'artifacts/task-1.2/node-v24.22.0-linux-x64/bin/node'),
           str(ROOT / 'tools/quality/syntax_units.ts')]
result = subprocess.run(command, input=json.dumps([str(path) for path in PATHS]),
                        capture_output=True, text=True, cwd=ROOT)
(OUT / 'size-parser.log').write_text(result.stdout + result.stderr)
if result.returncode:
    raise SystemExit(result.returncode)
measurements = json.loads(result.stdout)
for item, path in zip(measurements, PATHS):
    item['physical'] = len(path.read_text().splitlines())
    item['sha256'] = hashlib.sha256(path.read_bytes()).hexdigest()
    item['max_function'] = max((fn['logical'] for fn in item['functions']), default=0)
    assert item['physical'] <= 400 and item['logical'] <= 300 and item['max_function'] <= 50
report = {'command': command, 'exit_code': result.returncode, 'files': measurements,
          'scope': 'Owned whole files only; parent owns complete inventory acceptance.'}
(OUT / 'size.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps([{key: item[key] for key in ['path', 'physical', 'logical', 'max_function']} for item in measurements], indent=2))
