"""Exercise orchestration and fail-fast behavior without building images."""
import json
from pathlib import Path
import subprocess
import sys

import pytest

from qopenbb_ci import build_cli


def fake_commands(monkeypatch, fail=None):
    calls = []

    def run(argv, *, stdout, check):
        assert argv[:3] == [sys.executable, "-m", "qopenbb_ci.image_cli"]
        assert check is True
        calls.append(argv[3:])
        if len(calls) == fail:
            raise subprocess.CalledProcessError(2, argv)
        if argv[3] == "load":
            Path(argv[argv.index("--report") + 1]).write_text(json.dumps({
                "loaded_image_id": "sha256:" + "a" * 64}))
        stdout.write("{}\n")

    monkeypatch.setattr(build_cli.subprocess, "run", run)
    return calls


def options(tmp_path):
    return ["--output", str(tmp_path / "run"), "--release-version", "prototype-1"]


def test_serial_services_use_exact_sources_and_build_inputs(monkeypatch, tmp_path):
    calls = fake_commands(monkeypatch)
    root = tmp_path / "runtime"
    assert build_cli.main([*options(tmp_path), "--runtime-root", str(root)]) == 0
    assert [call[0] for call in calls] == ["acquire", "stage", "export", "load",
                                         "stage", "export", "load"]
    output = tmp_path / "run"
    assert calls[0] == ["acquire", "--lock", "sources.lock.json",
                        "--destination", str(output / "sources")]
    for offset, service in ((1, "workspace"), (4, "data-api")):
        stage, export, load = calls[offset:offset + 3]
        assert stage[:5] == ["stage", "--lock", "sources.lock.json",
                             "--policy", "contracts/sources.json"]
        assert stage[5:9] == ["--workspace", str(output / "sources/workspace"),
                              "--data-api", str(output / "sources/data_api")]
        assert stage[9:13] == ["--destination", str(output / service / "stage"),
                                "--service", service]
        assert stage[13:] == (["--release-version", "prototype-1"] if offset == 1
                              else ["--runtime-root", str(root)])
        assert export[export.index("--service") + 1] == service
        assert export[export.index("--tools") + 1] == "pipeline/tools.lock.json"
        assert export[export.index("--sdk-python") + 1] == ".dagger/.venv/bin/python"
        assert load == ["load", "--archive", str(output / service / "image.tar"),
                        "--report", str(output / service / "load.json")]
    summary = json.loads((output / "summary.json").read_text())
    assert set(summary["images"]) == {"workspace", "data-api"}


@pytest.mark.parametrize("failure", range(1, 8))
def test_failure_stops_later_commands_and_never_writes_summary(monkeypatch, tmp_path, failure):
    calls = fake_commands(monkeypatch, failure)
    assert build_cli.main(options(tmp_path)) == 2
    assert len(calls) == failure
    assert not (tmp_path / "run/summary.json").exists()


def test_existing_run_is_never_reused(monkeypatch, tmp_path):
    calls = fake_commands(monkeypatch)
    (tmp_path / "run").mkdir()
    assert build_cli.main(options(tmp_path)) == 2
    assert not calls


@pytest.mark.parametrize("release", ["", "../other", "a b", "$(command)", "a" * 129])
def test_invalid_public_release_rejected_before_work(monkeypatch, tmp_path, release):
    calls = fake_commands(monkeypatch)
    with pytest.raises(SystemExit):
        build_cli.main(["--output", str(tmp_path / "run"), "--release-version", release])
    assert not calls
    assert not (tmp_path / "run").exists()
