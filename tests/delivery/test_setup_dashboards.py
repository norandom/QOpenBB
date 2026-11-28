"""Verify that installing the released catalogs preserves the authored dashboard data."""

from collections import Counter
from copy import deepcopy
import importlib
import json
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[2]
CONNECTION = {"id": "local-data", "url": "http://127.0.0.1:23003/data", "name": "QOpenBB Data"}


def read(name):
    return json.loads((ROOT / "contracts" / name).read_text(encoding="utf-8"))


def bundled():
    data = read("widgets.json")
    gallery = read("gallery/catalog.json")
    for app in read("apps.json"):
        yield app, data, CONNECTION
    for app in gallery["apps"]:
        yield app, gallery["widgets"], CONNECTION
    for app in read("modeling/v1/apps.json"):
        yield app, read("modeling/v1/widgets.json"), {**CONNECTION, "id": "modeling"}


def test_seed_preserves_authored_widgets_and_layouts(monkeypatch):
    monkeypatch.syspath_prepend(str(ROOT / "deploy/setup"))
    render = importlib.import_module("provision_render")
    for app, catalog, source in bundled():
        original = deepcopy(app)
        data = render.make_dashboard(app, "dashboard", catalog, source, "root")["data"]
        widgets = {widget["id"]: widget for widget in data["widgets"]}
        assert list(data["gridLayout"]) == list(app["tabs"])
        for tab, definition in app["tabs"].items():
            installed = [widgets[slot["i"]] for slot in data["gridLayout"][tab]]
            installed = [w for w in installed if w["widgetId"] != "navigation_bar"]
            authored = [w for w in definition["layout"] if w["i"] != "navigation_bar"]
            assert Counter(w["widgetId"] for w in installed) == Counter(w["i"] for w in authored)
            for widget, layout in zip(installed, authored, strict=True):
                assert widget["widgetId"] == layout["i"] and widget["innerTab"] == tab
                state = layout.get("state", {})
                if "chartModel" in state:
                    assert any(isinstance(obj, dict) and obj.get("chartModel") == state["chartModel"]
                               for obj in widget["storage"].values())
                if widget["widgetId"] == "research_story":
                    assert widget["storage"]["researchStory"] == state["storage"]["researchStory"]
                if widget["widgetId"] == "qopenbb_saved_model_output":
                    assert widget["endpoint"]["url"] == "/modeling/v1/widget-results"
                    assert not widget.get("sourceId")
        assert app == original


def test_setup_preserves_edits_and_deletions_when_a_new_app_arrives(monkeypatch):
    pytest.importorskip("fcntl", reason="The provisioning helper executes in a Linux container")
    monkeypatch.syspath_prepend(str(ROOT / "deploy/setup"))
    seed = importlib.import_module("provision")
    rows = {}
    def sync(path, *, data=None, token=None):
        if data is None:
            return {"owned": deepcopy(rows)}
        rows.update({key: {"content": item} for key, item in data["items"].items()})
    monkeypatch.setattr(seed, "request", sync)
    apps = list(bundled())
    assert seed.save_apps("session", "owner", apps[:2], set()) == 2
    edited, deleted = [seed.seed_id("owner", "app/" + app[0]["name"]) for app in apps[:2]]
    rows[edited]["content"]["data"]["name"] = "My saved research"
    del rows[deleted]
    parent = rows[seed.seed_id("owner", "root")]["content"]
    parent["children"].remove(deleted)
    previously_seeded = {app[0]["name"] for app in apps[:2]}
    assert seed.save_apps("session", "owner", apps, previously_seeded) == len(apps) - 2
    assert rows[edited]["content"]["data"]["name"] == "My saved research"
    assert deleted not in rows
    before = deepcopy(rows)
    assert seed.save_apps("session", "owner", apps, {app[0]["name"] for app in apps}) == 0
    assert rows == before


def test_full_install_uses_named_storage_and_honors_image_override(tmp_path):
    import os
    import shutil
    import subprocess

    if not shutil.which("docker"):
        pytest.skip("Requires the Docker Compose CLI")
    env = {key: os.environ[key] for key in ("PATH", "HOME", "USERPROFILE", "SYSTEMROOT") if key in os.environ}
    env.update(FMP_API_KEY="fixture", FRED_API_KEY="fixture", WORKSPACE_HOST_PORT="23789",
               QFM_IDENTITY_CURRENT_KID="setup-test", QFM_IDENTITY_CURRENT_SECRET="fixture",
               QOPENBB_SETUP_MODELING_IMAGE="modeling:from-checkout")
    dotenv = tmp_path / "empty.env"
    dotenv.touch()
    command = ["docker", "compose", "--env-file", str(dotenv), "-f", "compose.yaml",
               "-f", "deploy/setup/compose.full.yaml", "config", "--format", "json"]
    def services():
        return json.loads(subprocess.check_output(command, env=env, cwd=ROOT))["services"]
    installed = services()
    assert installed["workspace"]["environment"]["PUBLIC_URL"] == "http://127.0.0.1:23789"
    assert installed["workspace"]["image"].endswith(":latest")
    assert installed["data-api"]["image"].endswith(":latest")
    assert installed["modeling"]["image"] == env["QOPENBB_SETUP_MODELING_IMAGE"]
    assert installed["modeling"]["volumes"][0]["type"] == "volume"
    assert any(v["target"] == "/opt/qopenbb-setup" and v["read_only"] for v in installed["workspace"]["volumes"])
    env.update(MODELING_IMAGE="modeling:owner-pin", QOPENBB_MODELING_STORAGE="./data/modeling")
    model = services()["modeling"]
    assert model["image"] == "modeling:owner-pin"
    assert model["volumes"][0]["type"] == "bind"
