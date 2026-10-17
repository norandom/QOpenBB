"""Run one bounded check without shell quoting or shared output files."""
import json
import os
import subprocess
import sys
import time
from pathlib import Path

OUT = Path('/mnt/d/Source/QOpenBB/artifacts/task-2.44/implementation')
STAGE = Path('/home/mc/qopenbb-work/task244-20261017140641/terminalpro')
NODE = '/mnt/d/Source/QOpenBB/artifacts/task-1.2/node-v24.22.0-linux-x64/bin'
label, *args = sys.argv[1:]
command = [f'{NODE}/node', *args]
env = dict(os.environ, PATH=f'{NODE}:' + os.environ['PATH'])
started = time.time()
result = subprocess.run(command, cwd=STAGE, env=env, capture_output=True, text=True)
(OUT / f'{label}.log').write_text(result.stdout + result.stderr)
(OUT / f'{label}.json').write_text(json.dumps({
    'command': command, 'cwd': str(STAGE), 'exit_code': result.returncode,
    'duration_seconds': time.time() - started,
}, indent=2) + '\n')
print(f'{label}: exit {result.returncode}')
print((result.stdout + result.stderr)[-2600:])
sys.exit(result.returncode)
