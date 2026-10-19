"""Contract checks for disposable packaged-image and source-overlay services."""
import json
import os
from pathlib import Path
import sys
from unittest.mock import patch

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import workspace_runtime as helper


@pytest.mark.parametrize("source,image_only", [(None, False), ("source", True)])
def test_start_requires_exactly_one_mode(source, image_only):
    with pytest.raises(ValueError, match="exactly one"):
        helper.WorkspaceRuntime.start("image", source, "http://127.0.0.1:23003",
                                      image_only=image_only)


@pytest.mark.parametrize("options", [[], ["--source", "source", "--image-only"]])
def test_cli_rejects_missing_or_conflicting_modes(monkeypatch, tmp_path, options):
    monkeypatch.setattr(sys, "argv", ["workspace_runtime", "start", "--private",
                        str(tmp_path / "private.json"), "--image", "image",
                        "--public-origin", "http://127.0.0.1:23003", *options])
    with pytest.raises(SystemExit) as error:
        helper.main()
    assert error.value.code == 2


@pytest.mark.parametrize("image_only", [True, False])
def test_runtime_preserves_mode_mounts_and_identity(tmp_path, image_only):
    calls = []
    inspection = {}
    source = None
    if not image_only:
        source = tmp_path / "api"
        source.mkdir()
        (source / "database.py").touch()
        (source / "__init__.py").touch()

    def docker(*args):
        calls.append(args)
        if args[:2] == ("image", "inspect"):
            return json.dumps([{"Id": "sha256:exact"}])
        if args[0] == "run":
            state_mount = args[args.index("--mount") + 1]
            state = state_mount.removeprefix("type=bind,src=").removesuffix(",dst=/data")
            inspection.update(Id="owned", Image="sha256:exact",
                              Mounts=[dict(Source=state, Destination="/data", Type="bind", RW=True)],
                              NetworkSettings={"Ports": {"3000/tcp": [
                                  {"HostIp": "127.0.0.1", "HostPort": "23003"}]}})
            if source:
                inspection["Mounts"].append(dict(Source=str(source), Destination="/opt/code/api",
                                                  Type="bind", RW=False))
            return "owned"
        if args[0] == "inspect":
            return json.dumps([inspection])
        return "OPENBB_ADMIN_EMAIL=synthetic@example.com\nOPENBB_ADMIN_PASSWORD=synthetic"

    def request(origin, route, body=None):
        assert origin == "http://127.0.0.1:23003"
        if route == "/config.js":
            return 200, b'window.__APP_CONFIG__ = {"ui":{"isLite":false},"urls":{"backend":"/api"}};'
        return 200, b'{"access_token":"synthetic"}'

    with patch.object(helper, "docker", docker), patch.object(helper, "request", request), \
            patch.object(helper.WorkspaceRuntime, "wait_ready"):
        runtime = helper.WorkspaceRuntime.start("tag", source, "http://127.0.0.1:23003",
                                                image_only=image_only)
        try:
            command = next(call for call in calls if call[0] == "run")
            assert command.count("--mount") == (1 if image_only else 2)
            assert "PUBLIC_URL=http://127.0.0.1:23003" in command
            if image_only:
                assert "127.0.0.1:23003:3000" in command
            else:
                assert f"type=bind,src={source},dst=/opt/code/api,readonly" in command
            assert command[-1] == "sha256:exact"
            assert (runtime.descriptor["source_overlay"] is None) == image_only
            assert runtime.descriptor["packaged_image_only"] is image_only
            assert runtime.descriptor["release_image_verified"] is False
            inspection["Mounts"].append(dict(Source="unexpected", Destination="/opt/code/api"))
            if image_only:
                with pytest.raises(ValueError, match="only the disposable"):
                    runtime.validate_ownership()
            inspection["Mounts"].pop()
            inspection["Image"] = "sha256:other"
            with pytest.raises(ValueError, match="image changed"):
                runtime.validate_ownership()
        finally:
            Path(runtime.descriptor["state"]).rmdir()


@pytest.mark.parametrize("origin", [None, "https://127.0.0.1:23003", "http://localhost:23003",
                                  "http://127.0.0.1:0", "http://127.0.0.1:65536"])
def test_image_only_rejects_non_loopback_http_or_invalid_port(origin):
    with pytest.raises(ValueError):
        helper.WorkspaceRuntime.start("image", None, origin, image_only=True)


@pytest.mark.skipif(os.name != "posix", reason="Private descriptors require POSIX permissions")
def test_private_descriptor_protects_disposable_credentials(tmp_path):
    runtime = helper.WorkspaceRuntime({"credentials": {"password": "synthetic"}})
    path = tmp_path / "private.json"
    runtime.write_private(path)
    assert path.stat().st_mode & 0o777 == 0o600
    assert json.loads(path.read_text()) == runtime.descriptor
    with pytest.raises(FileExistsError):
        runtime.write_private(path)
