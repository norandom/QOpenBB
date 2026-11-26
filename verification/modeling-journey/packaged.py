"""Exercise immutable candidate images on a disposable loopback deployment."""

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
from story_revision import controlled_revision

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


def exercise(root, compose, env, references, suite):
    origin, password = env["PUBLIC_URL"], env["OPENBB_ADMIN_PASSWORD"]

    def command(*args):
        subprocess.run([*compose, *args], env=env, check=True, timeout=240)

    def snapshot():
        return inventory(compose, references, env)

    wait_ready(origin)
    before = snapshot()
    if suite == "story":
        def change_service(action):
            if action == "stop":
                command("stop", "modeling")
            else:
                command("start", "--wait", "--wait-timeout", "60", "modeling")

        browser(root, "story", origin, password, suite=suite, change_service=change_service)
        after = snapshot()
        if before != after:
            raise ValueError("Story outage must preserve the running container identities")
    elif suite == "story-persistence":
        exercise_persistence(root, compose, env, origin)
        after = snapshot()
        if before != after:
            raise ValueError("Story persistence must preserve container identities")
    elif suite == "story-selection":
        browser(root, suite, origin, password, suite=suite)
        after = snapshot()
        if before != after:
            raise ValueError("Story selection must preserve the running container identities")
    else:
        after = exercise_issuer(root, command, origin, password, before, snapshot)
    (root / "images.json").write_text(json.dumps({"before": before, "after": after}, indent=2))


def exercise_persistence(root, compose, env, origin):
    # Ordinary user roles exercise ownership through the packaged session bridge.
    owner_password, peer_password = secrets.token_urlsafe(32), secrets.token_urlsafe(32)
    seed_env = {**env, "STORY_OWNER_PASSWORD": owner_password, "STORY_PEER_PASSWORD": peer_password}
    script = (Path(__file__).with_name("story_users.py")).read_text()
    subprocess.run([*compose, "exec", "-T", "-u", "appuser", "-e", "STORY_OWNER_PASSWORD", "-e",
                    "STORY_PEER_PASSWORD", "workspace", "python", "-"],
                   input=script, env=seed_env, text=True, check=True, timeout=30)
    browser(root, "save", origin, owner_password, suite="story-persistence")
    controlled_revision(root, compose, env, origin, peer_password)
    browser(root, "reopen", origin, owner_password, suite="story-persistence")
    macro = json.loads((root / "checkpoint.json").read_text())["state"]["run_refs"]["regime"]
    if not re.fullmatch(r"[0-9a-f]{32}", macro):
        raise ValueError("Invalid disposable macro run reference")
    subprocess.run([*compose, "exec", "-T", "modeling", "python", "-c",
                    "import pathlib,sys; pathlib.Path(sys.argv[1]).unlink()",
                    f"/data/modeling/{macro}.json"], env=env, check=True, timeout=30)
    browser(root, "unavailable", origin, owner_password, suite="story-persistence")


def exercise_issuer(root, command, origin, password, before, snapshot):
    browser(root, "evaluate", origin, password)
    command("up", "-d", "--no-build", "--pull", "never", "--force-recreate",
            "--no-deps", "--wait", "workspace", "modeling")
    after = snapshot()
    for service in SERVICES:
        replaced = before[service]["container"] != after[service]["container"]
        if replaced != (service != "data-api"):
            raise ValueError(f"unexpected {service} recreation state")
    browser(root, "reopen", origin, password)
    command("stop", "modeling")
    browser(root, "unavailable", origin, password)
    return after


def image_references(images, local):
    pattern = r"sha256:[0-9a-f]{64}" if local else r"[^\s@]+@sha256:[0-9a-f]{64}"
    if not all(re.fullmatch(pattern, image) for image in images):
        raise ValueError("Use full local content IDs with --local-images, or immutable registry references")
    return dict(zip(SERVICES, images, strict=True))


def run(args):
    refs = image_references((args.workspace_image, args.data_image, args.modeling_image), args.local_images)
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
    if args.local_images:
        subprocess.run(["docker", "image", "inspect", "--format", "{{.Id}}", *refs.values()], check=True)
    else:
        subprocess.run(["docker", "pull", refs["data-api"]], check=True)
    state_command(root / "data", refs["data-api"],
                  f"import os; os.mkdir('/owned/modeling',0o700); os.chown('/owned/modeling',{STATE_UID},{STATE_UID})")
    try:
        if args.local_images:
            subprocess.run([*compose, "up", "-d", "--no-build", "--pull", "never", "--wait",
                            "--wait-timeout", "180"], env=env, timeout=240, check=True)
        else:
            subprocess.run(["bash", root / "deploy/pull-modeling-candidate.sh", project, private],
                           env=env, timeout=600, check=True)
        exercise(root, compose, env, refs, args.suite)
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
    parser.add_argument("--suite", choices=("issuer", "story", "story-selection", "story-persistence"), default="issuer")
    parser.add_argument("--local-images", action="store_true", help="Use already-built full local image content IDs")
    run(parser.parse_args())
