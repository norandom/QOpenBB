"""Compatibility helper delegates exclusively to the checked Compose coordinator."""
from pathlib import Path
import sys
from unittest.mock import Mock
import pytest
sys.path.insert(0, str(Path(__file__).resolve().parent))
from qopenbb_ci import workspace_runtime as helper


@pytest.mark.parametrize('options', [[], ['--image','tag','--image-only'], ['--source','source']])
def test_start_rejects_legacy_modes(tmp_path, options):
    with pytest.raises(SystemExit) as error:
        helper.main(['start','--private',str(tmp_path/'private'),*options])
    assert error.value.code == 2


@pytest.mark.parametrize('action,target', [('restart','recreate'),('recreate','recreate'),('status','status'),('stop','stop')])
def test_existing_session_routes_checked_coordinator(tmp_path, monkeypatch, action, target):
    monkeypatch.setattr(helper,'resolve_environment',lambda path: 'config')
    call=Mock(return_value={'phase':'stopped'})
    monkeypatch.setattr(helper,target,call)
    monkeypatch.setattr(helper,'public_projection',lambda value: value)
    path=tmp_path/'never-read-legacy.json'
    path.write_text('{"password":"legacy-secret"}')
    helper.main([action,'--private',str(path)])
    assert call.call_args.args[:2] == ('config',path)
    assert path.read_text() == '{"password":"legacy-secret"}'


def test_no_wsl_wrapper_or_unchecked_descriptor_fallback():
    source=Path(helper.__file__).read_text()
    wrapper=Path(__file__).with_name('workspace-runtime.ps1').read_text()
    assert 'wsl.exe' not in wrapper
    assert 'read_text' not in source
    assert 'json.loads' not in source
