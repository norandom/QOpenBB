"""Execute the unchanged PowerShell entry against an isolated Python argv consumer."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

import pytest


@pytest.mark.skipif(os.name != 'nt', reason='Native Windows PowerShell entry')
@pytest.mark.parametrize('action,options', [
    ('build', {'BuildSelection': 'workspace', 'Stage': 'stage with spaces',
               'Archive': 'archive with spaces.tar', 'SdkPython': 'sdk python.exe',
               'EngineContainer': 'qopenbb-dagger-engine-owned'}),
    ('start', {'SessionPath': 'private session.json', 'WorkspaceImage': 'sha256:workspace',
               'DataImage': 'sha256:data'}),
    ('verify', {'SessionPath': 'private session.json', 'VerificationSource': 'source with spaces'}),
])
def test_native_entry_preserves_argv_boundaries_and_exit(tmp_path, action, options):
    repository = tmp_path / 'repository with spaces'
    package = repository / 'pipeline/qopenbb_ci'
    package.mkdir(parents=True)
    entry = repository / 'pipeline/dev.ps1'
    production = Path(__file__).resolve().parents[2] / 'pipeline/dev.ps1'
    shutil.copyfile(production, entry)
    (package / '__init__.py').write_text('')
    (package / 'native_environment.py').write_text(
        'import json, os, sys\n'
        'print(json.dumps({"argv": sys.argv[1:], "cwd": os.getcwd()}))\n'
        'raise SystemExit(19)\n')
    artifacts = str(tmp_path / 'artifacts with spaces')
    tools = str(tmp_path / 'tools with spaces.json')
    command = [shutil.which('pwsh'), '-NoLogo', '-NoProfile', '-NonInteractive',
               '-File', str(entry), '-Action', action, '-Python', sys.executable,
               '-Artifacts', artifacts, '-ToolsFile', tools]
    for name, value in options.items():
        command += ['-' + name, value]
    result = subprocess.run(command, cwd=Path.cwd(), capture_output=True, text=True,
                            timeout=30, creationflags=subprocess.CREATE_NO_WINDOW)
    assert result.returncode == 19, result.stderr
    captured = json.loads(result.stdout)
    expected = ['--action', action, '--repository', str(repository),
                '--artifacts', artifacts, '--tools-file', tools]
    names = {'BuildSelection': 'build-selection', 'Stage': 'stage', 'Archive': 'archive',
             'SdkPython': 'sdk-python', 'EngineContainer': 'engine-container',
             'SessionPath': 'session-path', 'WorkspaceImage': 'workspace-image',
             'DataImage': 'data-image', 'VerificationSource': 'verification-source'}
    actual = captured['argv']
    assert actual[:len(expected)] == expected
    pairs = dict(zip(actual[len(expected)::2], actual[len(expected) + 1::2], strict=True))
    assert pairs == {'--' + names[name]: value for name, value in options.items()}
    assert Path(captured['cwd']) == repository
