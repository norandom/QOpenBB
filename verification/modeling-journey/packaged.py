"""Exercise the pull-only candidate on a disposable loopback deployment."""

import argparse
import json
import os
import re
import secrets
import shutil
import socket
import subprocess
import tempfile
from pathlib import Path

from run import ROOT, browser, wait_ready

STATE_UID = 10001
SERVICES = ("workspace", "data-api", "modeling")


def inspect_one(container, field):
    return subprocess.check_output(
        ["docker", "inspect", "--format", field, container], text=True
    ).strip()


def inventory(compose, references, env):
    records = {}
    for service, reference in references.items():
        container = subprocess.check_output([*compose, "ps", "-q", service], env=env, text=True).strip()
        if inspect_one(container, "{{.Config.Image}}") != reference:
            raise ValueError(f"{service} did not start from its selected reference")
        pinned = subprocess.check_output(
            ["docker", "image", "inspect", "--format", "{{.Id}}", reference], text=True
        ).strip()
        if inspect_one(container, "{{.Image}}") != pinned:
            raise ValueError(f"{service} container image mismatch")
        mounts = json.loads(inspect_one(container, "{{json .Mounts}}"))
        expected = {"workspace": ["/data"], "data-api": [], "modeling": ["/data/modeling"]}
        if [mount["Destination"] for mount in mounts] != expected[service]:
            raise ValueError(f"unexpected {service} mounts")
        records[service] = {"container": container, "image": pinned, "reference": reference}
    return records


def settings(port, refs):
    return {
        **os.environ, **{key.upper().replace("-", "_") + "_IMAGE": ref for key, ref in refs.items()},
        "OPENBB_ADMIN_EMAIL": "analyst@example.com", "OPENBB_ADMIN_PASSWORD": secrets.token_urlsafe(32),
        "QFM_IDENTITY_CURRENT_KID": "journey", "QFM_IDENTITY_CURRENT_SECRET": secrets.token_hex(32),
        "PUBLIC_URL": f"http://127.0.0.1:{port}", "WORKSPACE_BIND_IP": "127.0.0.1",
        "WORKSPACE_HOST_PORT": str(port),
    }


def state_command(root, image, code):
    subprocess.run(["docker", "run", "--rm", "--pull", "never", "--network", "none",
                    "--user", "0:0", "--mount", f"type=bind,src={root},dst=/owned",
                    "--entrypoint", "python", image, "-c", code], check=True)


def exercise(root, compose, env, references):
    origin, password = env["PUBLIC_URL"], env["OPENBB_ADMIN_PASSWORD"]
    def command(*args):
        subprocess.run([*compose, *args], env=env, check=True, timeout=240)
    wait_ready(origin)
    before = inventory(compose, references, env)
    browser(root, "evaluate", origin, password)
    command("up", "-d", "--no-build", "--pull", "never", "--force-recreate",
            "--no-deps", "--wait", "workspace", "modeling")
    after = inventory(compose, references, env)
    for service in SERVICES:
        replaced = before[service]["container"] != after[service]["container"]
        if replaced != (service != "data-api"):
            raise ValueError(f"unexpected {service} recreation state")
    browser(root, "reopen", origin, password)
    command("stop", "modeling")
    browser(root, "unavailable", origin, password)
    (root / "images.json").write_text(json.dumps({"before": before, "after": after}, indent=2))


def run(args):
    refs = dict(zip(SERVICES, (args.workspace_image, args.data_image, args.modeling_image), strict=True))
    if not all(re.fullmatch(r"[^\s@]+@sha256:[0-9a-f]{64}", ref) for ref in refs.values()):
        raise ValueError("Use immutable registry image references")
    root = Path(tempfile.mkdtemp(prefix="packaged-", dir=args.evidence)).resolve()
    (root / "data").mkdir()
    shutil.copy(ROOT / "compose.yaml", root)
    (root / "deploy").mkdir()
    for name in ("compose.modeling.yaml", "pull-modeling-candidate.sh"):
        shutil.copy(ROOT / "deploy" / name, root / "deploy" / name)
    with socket.socket() as listener:
        listener.bind(("127.0.0.1", 0))
        env = settings(listener.getsockname()[1], refs)
    project = "qopenbb-packaged-" + secrets.token_hex(6)
    private = str(args.env_file.resolve())
    compose = ["docker", "compose", "--project-directory", str(root), "-p", project,
               "--env-file", private, "-f", str(root / "compose.yaml"),
               "-f", str(root / "deploy/compose.modeling.yaml")]
    # A disposable copy of the real bind must have the image user's numeric owner.
    subprocess.run(["docker", "pull", refs["data-api"]], check=True)
    state_command(root / "data", refs["data-api"],
                  f"import os; os.mkdir('/owned/modeling',0o700); os.chown('/owned/modeling',{STATE_UID},{STATE_UID})")
    try:
        subprocess.run(["bash", root / "deploy/pull-modeling-candidate.sh", project, private],
                       env=env, timeout=600, check=True)
        exercise(root, compose, env, refs)
        print(f"Image-only evidence at {root}")
    finally:
        subprocess.run([*compose, "down", "--volumes"], env=env, check=True, timeout=180)
        state_command(root / "data", refs["data-api"],
                      "import shutil,pathlib; [shutil.rmtree(p) for p in pathlib.Path('/owned').iterdir()]")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("workspace", "data", "modeling"):
        parser.add_argument(f"--{name}-image", required=True)
    parser.add_argument("--evidence", type=Path, required=True)
    parser.add_argument("--env-file", type=Path, default=ROOT / ".env")
    run(parser.parse_args())
