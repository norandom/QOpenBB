"""Packaged smoke retains checks while delegating all resource lifecycle ownership."""
import ast
import json
import os
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock
import pytest
from qopenbb_ci import workspace_smoke as smoke


def test_packaged_smoke_requires_explicit_pair(tmp_path):
    with pytest.raises(SystemExit) as error:
        smoke.main(['--image','workspace','--report',str(tmp_path/'report.json')])
    assert error.value.code == 2


def test_packaged_smoke_routes_start_and_checked_stop(tmp_path,monkeypatch):
    config=SimpleNamespace()
    descriptor=SimpleNamespace()
    monkeypatch.setattr(smoke,'validate_output',lambda path:path)
    monkeypatch.setattr(smoke,'resolve_environment',lambda path:config)
    start=Mock(return_value=descriptor)
    stop=Mock(return_value={'phase':'stopped'})
    monkeypatch.setattr(smoke,'start',start)
    monkeypatch.setattr(smoke,'stop',stop)
    monkeypatch.setattr(smoke,'check_packaged',lambda *args:None)
    monkeypatch.setattr(smoke,'capture_logs',lambda *args:True)
    private=tmp_path/'private.json'
    private.touch()
    report=tmp_path/'report.json'
    smoke.main(['--image','workspace','--data-image','data','--private',str(private),'--report',str(report)])
    request=start.call_args.args[0]
    assert request.workspace_image=='workspace' and request.data_image=='data'
    assert request.session_path==private
    stop.assert_called_once_with(config,private)
    assert json.loads(report.read_text())['state_preserved'] is True


def test_packaged_probe_is_valid_python():
    tree=ast.parse(Path(smoke.__file__).read_text())
    probe=next(node.value.value for node in ast.walk(tree) if isinstance(node,ast.Assign)
               and any(isinstance(target,ast.Name) and target.id=='probe' for target in node.targets))
    compile(probe,'<packaged-private-state-probe>','exec')


@pytest.mark.skipif(os.name != 'nt', reason='POSIX checked directory removal fails closed')
def test_empty_directory_removal_refuses_nonempty(tmp_path):
    from qopenbb_ci import session_files
    state=tmp_path/'owned'
    with session_files.create_session(state) as directory:directory.create_file('marker',b'retained')
    with session_files.PrivateDirectory.open_for_removal(state) as directory:
        with pytest.raises(OSError):directory.remove_empty()
        assert directory.read_file('marker')==b'retained'
