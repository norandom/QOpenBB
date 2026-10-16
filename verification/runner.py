"""Run fixture-only pytest checks with a hard worker ceiling and private output."""
from __future__ import annotations

import json
import os
import re
import signal
import shutil
from pathlib import Path
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from importlib.metadata import version


def execute(command: list[str], environment: dict[str, str], timeout: float = 120) -> tuple[int, str]:
    child = subprocess.Popen(command, env=environment, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, text=True,
                             start_new_session=os.name != 'nt',
                             creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0))
    try:
        stdout, _ = child.communicate(timeout=timeout)
        return child.returncode, stdout
    except subprocess.TimeoutExpired:
        # Terminate only the process group this invocation created, including xdist children.
        if os.name == 'nt':
            subprocess.run(['taskkill', '/PID', str(child.pid), '/T', '/F'],
                           env=environment, capture_output=True, timeout=10,
                           creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0))
        else:
            os.killpg(child.pid, signal.SIGKILL)
        child.communicate()
        return 124, ''

def run_pytest(paths: list[str], workers: int = 2) -> tuple[int, Path]:
    if workers not in (0, 1, 2):
        raise ValueError('pytest workers must be between zero and two')
    if not paths or any(path.startswith('-') for path in paths):
        raise ValueError('explicit test paths required')
    root = Path('artifacts/task-1.7/pytest').resolve()
    root.mkdir(parents=True, exist_ok=True)
    output = Path(tempfile.mkdtemp(prefix='run-', dir=root))
    environment = {key: os.environ[key] for key in ('PATH', 'SYSTEMROOT', 'WINDIR') if key in os.environ}
    environment['PYTEST_DISABLE_PLUGIN_AUTOLOAD'] = '1'
    environment['QOPENBB_TEST_OUTPUT'] = str(output)
    command = [sys.executable, '-m', 'pytest', '-p', 'xdist.plugin', '-c',
               'pipeline/pyproject.toml', *paths, '-m', 'fixture and not live',
               '-n', str(workers), '--maxprocesses=2',
               '--basetemp', str(output / 'tmp'), '-p', 'no:cacheprovider']
    try:
        exit_code, stdout = execute(command, environment)
    finally:
        if (output / 'tmp').exists():
            shutil.rmtree(output / 'tmp')
    # Assertions can contain credentials; retain only known numeric result categories.
    counts = {label: int(count) for count, label in re.findall(
        r'(\d+) (passed|failed|skipped|deselected|error)', stdout)}
    revision = subprocess.check_output(['git', 'rev-parse', 'HEAD'], env=environment, text=True,
                                       creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0)).strip()
    record = {'revision': revision, 'python': sys.version.split()[0],
              'pytest': version('pytest'), 'xdist': version('pytest-xdist'),
              'timestamp': datetime.now(timezone.utc).isoformat(), 'command': command, 'exit': exit_code, 'workers': workers, 'counts': counts,
              'scope': 'fixture only', 'live': 'unverified', 'output': str(output)}
    (output / 'evidence.json').write_text(json.dumps(record, indent=2))
    return exit_code, output


if __name__ == '__main__':
    code, output = run_pytest(sys.argv[1:])
    print(json.dumps({'exit': code, 'output': str(output)}))
    raise SystemExit(code)
