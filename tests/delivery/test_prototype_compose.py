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
    (tmp_path / "deploy").mkdir()
    shutil.copyfile(ROOT / "deploy/compose.modeling.yaml",
                    tmp_path / "deploy/compose.modeling.yaml")
    empty = tmp_path / "empty.env"
    empty.touch()

    def config(overrides=None, *, modeling=False):
        env = {key: value for key, value in os.environ.items()
               if key not in {*INPUTS, "PUBLIC_URL", "OPENBB_ADMIN_EMAIL",
                              "OPENBB_ADMIN_PASSWORD", "QFM_IDENTITY_CURRENT_KID",
                              "QFM_IDENTITY_CURRENT_SECRET", "QFM_IDENTITY_PREVIOUS_KID",
                              "QFM_IDENTITY_PREVIOUS_SECRET", "MODELING_IMAGE",
                              "WORKSPACE_BIND_IP", "WORKSPACE_HOST_PORT", "COMPOSE_FILE",
                              "COMPOSE_PROFILES", "COMPOSE_ENV_FILES"}}
        env.update(INPUTS)
        for key, value in (overrides or {}).items():
            if value is None:
                env.pop(key, None)
            else:
                env[key] = value
        files = ["-f", str(tmp_path / "compose.yaml")]
        if modeling:
            files += ["-f", str(tmp_path / "deploy/compose.modeling.yaml")]
        return subprocess.run(
            ["docker", "compose", "--env-file", str(empty), *files,
             "config", "--format", "json"],
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
        "OPENBB_ADMIN_EMAIL": "", "OPENBB_ADMIN_PASSWORD": "",
        "QFM_IDENTITY_CURRENT_KID": "", "QFM_IDENTITY_CURRENT_SECRET": ""}
    assert selected["data-api"]["environment"] == {
        "FMP_API_KEY": "synthetic-fmp", "FRED_API_KEY": "synthetic-fred",
        "OPENBB_API_AUTH": "false"}
    changed = services(parse, {"PUBLIC_URL": "https://qopenbb.example.com",
                              "OPENBB_ADMIN_PASSWORD": "synthetic-bootstrap",
                              "QFM_IDENTITY_CURRENT_KID": "fixture",
                              "QFM_IDENTITY_CURRENT_SECRET": "synthetic-modeling-signing-key"})
    assert changed["workspace"]["environment"]["QFM_IDENTITY_CURRENT_KID"] == "fixture"
    assert changed["workspace"]["environment"]["QFM_IDENTITY_CURRENT_SECRET"] == "synthetic-modeling-signing-key"
    assert changed["data-api"]["environment"] == selected["data-api"]["environment"]
    assert changed["workspace"]["environment"]["PUBLIC_URL"] == "https://qopenbb.example.com"
    assert changed["workspace"]["environment"]["OPENBB_ADMIN_PASSWORD"] == "synthetic-bootstrap"
    probe = selected["data-api"]["healthcheck"]["test"]
    assert probe[:3] == ["CMD", "python", "-c"]
    assert "http://127.0.0.1:6900/readyz" in probe[3]


@pytest.mark.parametrize("missing", ["FMP_API_KEY", "FRED_API_KEY"])
@pytest.mark.parametrize("value", [None, ""])
def test_required_selected_service_inputs_fail_closed(parse, missing, value):
    result = parse({missing: value})
    assert result.returncode != 0
    assert missing in result.stderr
    assert not result.stdout.strip()


def test_development_images_default_to_latest(parse):
    selected = services(parse, {"WORKSPACE_IMAGE": None, "DATA_API_IMAGE": None})
    for service in ("workspace", "data-api"):
        assert selected[service]["image"] == "ghcr.io/norandom/qopenbb-" + service + ":latest"


MODELING_INPUTS = {
    "MODELING_IMAGE": "localhost:5000/modeling@sha256:" + "f" * 64,
    "QFM_IDENTITY_CURRENT_KID": "current-key",
    "QFM_IDENTITY_CURRENT_SECRET": "synthetic-modeling-key" * 2,
}


def test_modeling_overlay_is_private_and_keeps_workspace_independent(parse):
    overrides = MODELING_INPUTS | {"WORKSPACE_BIND_IP": "127.0.0.1",
                                   "WORKSPACE_HOST_PORT": "24231"}
    result = parse(overrides, modeling=True)
    assert result.returncode == 0, result.stderr
    config = json.loads(result.stdout)["services"]
    assert set(config) == {"workspace", "data-api", "modeling"}
    workspace = config["workspace"]
    model = config["modeling"]
    assert workspace["ports"][0]["host_ip"] == "127.0.0.1"
    assert workspace["ports"][0]["published"] == "24231"
    assert set(workspace["depends_on"]) == {"data-api"}
    assert model["image"] == MODELING_INPUTS["MODELING_IMAGE"]
    assert model["expose"] == ["6901"]
    assert model["user"] == "10001:10001"
    assert all(not model.get(key) for key in
               ("build", "ports", "depends_on", "env_file", "command", "entrypoint"))
    mount, = model["volumes"]
    assert mount["type"] == "bind" and mount["target"] == "/data/modeling"
    assert Path(mount["source"]).parts[-2:] == ("data", "modeling")
    # Compose v2 omits a false bind option in normalized JSON.
    overlay = (ROOT / "deploy/compose.modeling.yaml").read_text()
    assert "          create_host_path: false" in overlay.splitlines()
    assert mount.get("bind", {}).get("create_host_path", False) is False
    assert {key: value for key, value in model["environment"].items() if value is not None} == {
        **{key: value for key, value in MODELING_INPUTS.items() if key.startswith("QFM_")},
        "QOPENBB_MODEL_DATA_ORIGIN": "http://data-api:6900",
        "QOPENBB_MODEL_RUN_DIR": "/data/modeling",
    }
    assert all(not key.startswith("QFM_") for key in config["data-api"]["environment"])


def test_modeling_previous_keys_stay_in_listener(parse):
    previous = {"QFM_IDENTITY_PREVIOUS_KID": "old-key",
                "QFM_IDENTITY_PREVIOUS_SECRET": "synthetic-previous-key" * 2}
    result = parse(MODELING_INPUTS | previous, modeling=True)
    assert result.returncode == 0, result.stderr
    config = json.loads(result.stdout)["services"]
    for key, value in previous.items():
        assert config["modeling"]["environment"][key] == value
        assert key not in config["workspace"]["environment"]
        assert key not in config["data-api"]["environment"]


@pytest.mark.parametrize("missing", MODELING_INPUTS)
def test_opt_in_requires_modeling_image_and_current_key_pair(parse, missing):
    result = parse(MODELING_INPUTS | {missing: None}, modeling=True)
    assert result.returncode != 0
    assert missing in result.stderr
