"""Verify the disposable modeling lifecycle protocol without Docker or a browser."""

from pathlib import Path
import subprocess
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "verification/modeling-journey"))

from modeling_lifecycle import run_browser
from packaged import image_references


BROWSER = """
import os
import time
from pathlib import Path

directory = Path(os.environ["JOURNEY_SERVICE_CONTROL"])
for action in ("stop", "start"):
    (directory / action).touch(exist_ok=False)
    while not (directory / (action + ".done")).exists():
        time.sleep(0.01)
"""


def test_browser_waits_for_stop_then_start_in_one_process(tmp_path):
    actions = []
    run_browser([sys.executable, "-c", BROWSER], {}, actions.append, tmp_path, timeout=5)
    assert actions == ["stop", "start"]


def test_missing_lifecycle_fails_even_when_browser_exits_successfully(tmp_path):
    with pytest.raises(RuntimeError, match="Missing modeling lifecycle request"):
        run_browser([sys.executable, "-c", "pass"], {}, lambda _: None, tmp_path, timeout=5)


def test_compose_failure_terminates_waiting_browser(tmp_path):
    def fail(action):
        raise subprocess.CalledProcessError(3, action)

    with pytest.raises(subprocess.CalledProcessError):
        run_browser([sys.executable, "-c", BROWSER], {}, fail, tmp_path, timeout=5)
    assert not (tmp_path / "service-control" / "stop.done").exists()


@pytest.mark.parametrize("local", [False, True])
def test_packaged_candidates_require_one_immutable_reference_form(local):
    local_id = "sha256:" + "a" * 64
    registry_ref = "registry.example/qopenbb/image@" + local_id
    valid, invalid = (local_id, registry_ref) if local else (registry_ref, local_id)
    assert image_references((valid, valid, valid), local) == {
        "workspace": valid, "data-api": valid, "modeling": valid,
    }
    with pytest.raises(ValueError):
        image_references((valid, invalid, valid), local)
