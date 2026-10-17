"""Run one reviewer check and preserve the first result without retries."""
import json
import os
import subprocess
import sys
import time
from pathlib import Path

OUT = Path('/mnt/d/Source/QOpenBB/artifacts/task-2.44/review-repair')
STAGE = Path('/home/mc/qopenbb-work/task244-independent-review-repair/terminalpro')
NODE = '/mnt/d/Source/QOpenBB/artifacts/task-1.2/node-v24.22.0-linux-x64/bin'
label, *args = sys.argv[1:]
assert not (OUT / f'{label}.json').exists()
command = [f'{NODE}/node', *args]
started = time.time()
result = subprocess.run(command, cwd=STAGE, env=dict(os.environ, PATH=NODE + ':' + os.environ['PATH']), capture_output=True, text=True)
(OUT / f'{label}.log').write_text(result.stdout + result.stderr)
(OUT / f'{label}.json').write_text(json.dumps({'command': command, 'cwd': str(STAGE), 'exit_code': result.returncode, 'duration_seconds': time.time() - started}, indent=2) + '\n')
print(label, 'exit', result.returncode)
print((result.stdout + result.stderr)[-3500:])
sys.exit(result.returncode)
