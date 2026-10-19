"""Parse the deployment topology without reading private dotenv or starting services."""
import json
import os
from pathlib import Path
import shutil
import subprocess

import pytest

ROOT = Path(__file__).resolve().parents[2]
INPUTS = {
    "WORKSPACE_IMAGE": "registry.example/workspace@sha256:" + "a" * 64,
    "DATA_API_IMAGE": "registry.example/data-api@sha256:" + "b" * 64,
    "FMP_API_KEY": "synthetic-fmp",
    "FRED_API_KEY": "synthetic-fred",
}


@pytest.fixture
def parse(tmp_path):
    shutil.copyfile(ROOT / "compose.yaml", tmp_path / "compose.yaml")
    empty = tmp_path / "empty.env"
    empty.touch()

    def config(overrides=None):
        env = {key: value for key, value in os.environ.items()
               if key not in {*INPUTS, "PUBLIC_URL", "OPENBB_ADMIN_EMAIL",
                              "OPENBB_ADMIN_PASSWORD", "COMPOSE_FILE",
                              "COMPOSE_PROFILES", "COMPOSE_ENV_FILES"}}
        env.update(INPUTS)
        for key, value in (overrides or {}).items():
            if value is None:
                env.pop(key, None)
            else:
                env[key] = value
        return subprocess.run(
            ["docker", "compose", "--env-file", str(empty), "-f",
             str(tmp_path / "compose.yaml"), "config", "--format", "json"],
            env=env, capture_output=True, text=True, check=False)

    return config


def services(parse, overrides=None):
    result = parse(overrides)
    assert result.returncode == 0, result.stderr
    return json.loads(result.stdout)["services"]


def test_only_reviewed_image_services_and_private_state(parse):
    selected = services(parse)
    assert set(selected) == {"workspace", "data-api"}
    for name, service in selected.items():
        assert service["image"] == INPUTS[
            "WORKSPACE_IMAGE" if name == "workspace" else "DATA_API_IMAGE"]
        assert all(not service.get(key) for key in
                   ("build", "env_file", "command", "entrypoint", "profiles"))
    workspace = selected["workspace"]
    assert workspace["ports"] == [{"mode": "ingress", "target": 3000,
                                     "published": "23003", "protocol": "tcp",
                                     "host_ip": "0.0.0.0"}]
    mount, = workspace["volumes"]
    assert mount["type"] == "bind" and mount["target"] == "/data"
    assert Path(mount["source"]).parts[-2:] == ("data", "workspace")
    assert not selected["data-api"].get("ports")
    assert not selected["data-api"].get("volumes")
    assert workspace["depends_on"] == {
        "data-api": {"condition": "service_healthy", "required": True}}


def test_credentials_stay_with_service_and_bootstrap_remains_optional(parse):
    selected = services(parse)
    assert selected["workspace"]["environment"] == {
        "PUBLIC_URL": "http://127.0.0.1:23003", "EXCEL_ENABLED": "false",
        "OPENBB_ADMIN_EMAIL": "", "OPENBB_ADMIN_PASSWORD": ""}
    assert selected["data-api"]["environment"] == {
        "FMP_API_KEY": "synthetic-fmp", "FRED_API_KEY": "synthetic-fred",
        "OPENBB_API_AUTH": "false"}
    changed = services(parse, {"PUBLIC_URL": "https://qopenbb.example.com",
                              "OPENBB_ADMIN_PASSWORD": "synthetic-bootstrap"})
    assert changed["workspace"]["environment"]["PUBLIC_URL"] == "https://qopenbb.example.com"
    assert changed["workspace"]["environment"]["OPENBB_ADMIN_PASSWORD"] == "synthetic-bootstrap"
    probe = selected["data-api"]["healthcheck"]["test"]
    assert probe[:3] == ["CMD", "python", "-c"]
    assert "http://127.0.0.1:6900/readyz" in probe[3]


@pytest.mark.parametrize("missing", INPUTS)
@pytest.mark.parametrize("value", [None, ""])
def test_required_selected_service_inputs_fail_closed(parse, missing, value):
    result = parse({missing: value})
    assert result.returncode != 0
    assert missing in result.stderr
    assert not result.stdout.strip()
