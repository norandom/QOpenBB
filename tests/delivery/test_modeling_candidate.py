"""Use real Compose interpolation and record the candidate pull/start boundary."""
import os
from pathlib import Path
import shutil
import subprocess

import pytest

ROOT = Path(__file__).resolve().parents[2]
PINS = {
    "WORKSPACE_IMAGE": f"localhost:5000/candidate/workspace@sha256:{'a' * 64}",
    "DATA_API_IMAGE": f"ghcr.io/norandom/qopenbb-data-api@sha256:{'b' * 64}",
    "MODELING_IMAGE": f"localhost:5000/candidate/modeling@sha256:{'c' * 64}",
}


@pytest.fixture
def candidate(tmp_path):
    deployment = tmp_path / "deployment"
    (deployment / "deploy").mkdir(parents=True)
    (deployment / "data/modeling").mkdir(parents=True, mode=0o700)
    for name in ("compose.yaml", "deploy/compose.modeling.yaml", "deploy/pull-modeling-candidate.sh"):
        shutil.copyfile(ROOT / name, deployment / name)
    binaries = tmp_path / "bin"
    binaries.mkdir()
    calls = tmp_path / "calls"
    docker = binaries / "docker"
    docker.write_text(
        '#!/usr/bin/env bash\n'
        'for argument; do\n'
        '  case "$argument" in\n'
        '    config) exec "$REAL_DOCKER" "$@" ;;\n'
        '    pull|up) printf "%s\\n" "$*" >> "$CALLS"; exit 0 ;;\n'
        '  esac\n'
        'done\nexit 99\n'
    )
    stat = binaries / "stat"
    stat.write_text('#!/usr/bin/env bash\nprintf "%s\\n" "$STATE_METADATA"\n')
    for executable in (docker, stat):
        executable.chmod(0o700)

    def invoke(*, pins=None, state="10001:10001:700", shell_image=None):
        private = deployment / "candidate.env"
        values = (PINS if pins is None else pins) | {
            "FMP_API_KEY": "synthetic-fmp", "FRED_API_KEY": "synthetic-fred",
            "QFM_IDENTITY_CURRENT_KID": "test-current",
            "QFM_IDENTITY_CURRENT_SECRET": "synthetic-key" * 4,
        }
        private.write_text("".join(f"{key}={value}\n" for key, value in values.items()))
        private.chmod(0o600)
        env = {
            "PATH": os.pathsep.join([str(binaries), os.environ["PATH"]]),
            "REAL_DOCKER": shutil.which("docker"),
            "CALLS": str(calls),
            "STATE_METADATA": state,
        }
        if shell_image is not None:
            env["MODELING_IMAGE"] = shell_image
        result = subprocess.run(
            ["bash", str(deployment / "deploy/pull-modeling-candidate.sh"),
             "fixture-candidate", str(private)],
            cwd=tmp_path, env=env, check=False, capture_output=True, text=True,
        )
        return result, calls.read_text().splitlines() if calls.exists() else []

    return invoke


def test_local_registry_digests_pull_before_start_and_never_build(candidate):
    result, calls = candidate()
    assert result.returncode == 0, result.stderr
    pull, start = calls
    assert pull.endswith("pull --policy always")
    assert start.endswith("up -d --no-build --pull never --wait --wait-timeout 180")
    assert all("--project-name fixture-candidate" in call for call in calls)


@pytest.mark.parametrize("key", PINS)
def test_each_candidate_image_must_be_pinned(candidate, key):
    result, calls = candidate(pins=PINS | {key: "localhost:5000/candidate/modeling:latest"})
    assert result.returncode != 0 and not calls
    assert "registry/repository@sha256" in result.stderr


def test_shell_override_cannot_replace_digest_with_tag(candidate):
    result, calls = candidate(shell_image="localhost:5000/modeling:latest")
    assert result.returncode != 0 and not calls


@pytest.mark.parametrize("state", ["0:0:700", "10001:10001:755"])
def test_candidate_requires_private_owned_state_before_pull(candidate, state):
    result, calls = candidate(state=state)
    assert result.returncode != 0 and not calls
    assert "owner 10001:10001 and mode 0700" in result.stderr
