"""Run the source-stage analyst journey against disposable, retained Docker state."""

import argparse
import json
import os
import secrets
import shutil
import socket
import subprocess
import sysconfig
import tempfile
import time
from pathlib import Path
from urllib.request import urlopen

from modeling_lifecycle import run_browser

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def prepare(root, args):
    deps = root / "locked"
    deps.mkdir()
    packages = Path(sysconfig.get_paths()["purelib"])
    for name in ("polars", "_polars_runtime_32", "jwt"):
        shutil.copytree(packages / name, deps / name)
    for pattern in ("polars*.dist-info", "pyjwt*.dist-info"):
        for entry in packages.glob(pattern):
            shutil.copytree(entry, deps / entry.name)
    if not (args.frontend / "index.html").is_file():
        raise ValueError("Provide the compiled Full Workspace runtime frontend")
    shutil.copytree(args.frontend, root / "frontend")
    (root / "model-state").mkdir(mode=0o700)
    with socket.socket() as listener:
        listener.bind(("127.0.0.1", 0))
        port = listener.getsockname()[1]
    return {
        "JOURNEY_PORT": str(port),
        "JOURNEY_PASSWORD": secrets.token_urlsafe(32),
        "JOURNEY_SIGNER": secrets.token_hex(32),
        "JOURNEY_UID": str(os.getuid()), "JOURNEY_GID": str(os.getgid()),
        "JOURNEY_MODEL_STATE": str(root / "model-state"),
        "JOURNEY_DEPENDENCIES": str(deps), "JOURNEY_FRONTEND": str(root / "frontend"),
        "WORKSPACE_IMAGE": args.workspace_image, "DATA_API_IMAGE": args.data_image,
    }


def compose(project, env, *args, capture=False):
    return subprocess.run(
        ["docker", "compose", "--env-file", str(ROOT / ".env"), "-p", project,
         "-f", str(HERE / "compose.yaml"), *args], env={**os.environ, **env},
        capture_output=capture, text=True, check=True, timeout=180,
    ).stdout


def wait_ready(origin):
    deadline = time.monotonic() + 100
    while time.monotonic() < deadline:
        try:
            with urlopen(origin + "/api/health", timeout=2) as response:
                if response.status == 200:
                    return
        except OSError:
            pass
        time.sleep(1)
    raise RuntimeError("Workspace did not become ready")


def browser(root, phase, origin, password, *, suite="issuer", change_service=None):
    evidence = root / phase
    evidence.mkdir()
    env = {key: os.environ[key] for key in ("HOME", "PATH", "PLAYWRIGHT_BROWSERS_PATH")}
    env.update(WORKSPACE_FRONTEND_ORIGIN=origin, JOURNEY_PHASE=phase, JOURNEY_PASSWORD=password,
               JOURNEY_CHECKPOINT=str(root / "checkpoint.json"), WORKSPACE_EVIDENCE_ROOT=str(evidence),
               QOPENBB_PLAYWRIGHT_PACKAGE=str(HERE.parent / "node_modules/@playwright/test"))
    spec = {"issuer": "analyst.spec.mts", "story": "story.spec.mts"}[suite]
    command = ["node", HERE.parent / "node_modules/@playwright/test/cli.js",
               "test", "-c", HERE / "playwright.config.mts", spec]
    if change_service is None:
        subprocess.run(command, cwd=ROOT, env=env, timeout=240, check=True)
    else:
        run_browser(command, env, change_service, evidence, cwd=ROOT, timeout=240)


def run(args):
    root = Path(tempfile.mkdtemp(prefix="modeling-journey-", dir=args.evidence))
    project = "qopenbb-modeling-" + secrets.token_hex(6)
    env = prepare(root, args)
    origin = "http://127.0.0.1:" + env["JOURNEY_PORT"]
    try:
        compose(project, env, "up", "-d", "--pull", "never")
        wait_ready(origin)
        browser(root, "evaluate", origin, env["JOURNEY_PASSWORD"])
        before = compose(project, env, "ps", "-q", "workspace", "modeling", capture=True).splitlines()
        compose(project, env, "up", "-d", "--force-recreate", "--pull", "never", "modeling", "workspace")
        wait_ready(origin)
        after = compose(project, env, "ps", "-q", "workspace", "modeling", capture=True).splitlines()
        if len(before) != 2 or len(after) != 2 or set(before) & set(after):
            raise RuntimeError("Expected both Workspace and modeling container identities to change")
        browser(root, "reopen", origin, env["JOURNEY_PASSWORD"])
        compose(project, env, "stop", "modeling")
        browser(root, "unavailable", origin, env["JOURNEY_PASSWORD"])
        (root / "recreation.json").write_text(json.dumps({"before": before, "after": after}))
        print(f"Journey evidence at {root}")
    finally:
        compose(project, env, "down", "--volumes")
        for name in ("frontend", "locked", "model-state"):
            shutil.rmtree(root / name)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace-image", required=True)
    parser.add_argument("--data-image", required=True)
    parser.add_argument("--frontend", required=True, type=Path)
    parser.add_argument("--evidence", required=True, type=Path)
    run(parser.parse_args())
