"""Launch the frozen installed Events and Documents pair with a disposable send ledger."""

import argparse
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
from threading import Event, Thread

from events_documents_guard import bootstrap
from events_documents_oracle import report, Discrepancy, replay_source, report_replay
from qopenbb_ci.compose_runtime import hashed, prepare, StartRequest
from qopenbb_ci.compose_lifecycle import stop
from qopenbb_ci.portable_runtime import resolve_environment
from qopenbb_ci.session_files import replace_private

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
PACKAGE = ROOT / "verification/node_modules/@playwright/test"


def private_write(path, data):
    fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    with os.fdopen(fd, "wb") as stream:
        stream.write(data)


def configure(runtime, root, mode, key, candidate):
    data = candidate["images"]["data-api"]["image"]
    inspection = json.loads(runtime.command(["image", "inspect", data]))[0]
    if inspection["Config"]["Labels"].get("org.qopenbb.source.data_api") != candidate["sources"]["data_api"]:
        raise ValueError("Candidate Data API source mismatch")
    workspace = candidate["images"]["workspace"]["image"]
    inspection_workspace = json.loads(runtime.command(["image", "inspect", workspace]))[0]
    if inspection_workspace["Config"]["Labels"].get("org.qopenbb.source.workspace") != candidate["sources"]["workspace"]:
        raise ValueError("Candidate Workspace source mismatch")
    plan = json.loads((root / "plan.json").read_text())
    code = bootstrap(plan, mode == "live", inspection["Config"]["Entrypoint"])
    stage = root / "stage"
    stage.mkdir()
    (stage / "current").write_text("disarmed")
    (stage / "applied").write_text("disarmed")
    override = root / "guard.json"
    service = {"entrypoint": ["python", "-c", code.replace("$", "$$")], "command": [],
               "environment": {"WEB_CONCURRENCY": "1", "UVICORN_WORKERS": "1"}}
    private_write(override, json.dumps({"services": {"data-api": service}}).encode())
    descriptor = runtime.descriptor.compose.model_dump(mode="json")
    descriptor["files"].append(hashed(override))
    if key:
        path = Path(descriptor["environment_file"]["path"])
        content = path.read_bytes().replace(b"FMP_API_KEY=offline-readiness-not-a-provider-key\n",
                                            f"FMP_API_KEY={key}\n".encode())
        replace_private(path, content)
        descriptor["environment_file"] = hashed(path)
    runtime.save(compose=descriptor)


def browser(runtime, root, mode, discover, cache):
    env = {"PATH": os.environ["PATH"], "PLAYWRIGHT_BROWSERS_PATH": cache}
    env.update(WORKSPACE_FRONTEND_ORIGIN=runtime.descriptor.origin, WORKSPACE_EVIDENCE_ROOT=str(root),
               WORKSPACE_RUNTIME_PRIVATE=str(runtime.path), QOPENBB_FINANCIAL_SUITE="events-documents",
               QOPENBB_PLAYWRIGHT_PACKAGE=str(PACKAGE), EVENTS_VERIFICATION_MODE=mode,
               EVENTS_STAGE_DIR=str(root / "stage"))
    if (root / "four-inputs").exists():
        env["EVENTS_FOUR_INPUTS"] = "1"
    if (root / "supplemental").exists():
        env["EVENTS_SUPPLEMENTAL"] = "1"
    if (root / "seed-preflight").exists():
        env["EVENTS_SEED_PREFLIGHT"] = "1"
    if (root / "replay-calendar.installed").exists():
        env["EVENTS_REPLAY_CALENDAR"] = "1"
    argv = ["node", str(PACKAGE / "cli.js"), "test", "--config", "verification/financial-workspace.config.ts"]
    if discover:
        argv.append("--list")
        return subprocess.run(argv, cwd=ROOT, env=env, check=False).returncode
    stopped = Event()
    failed = Event()
    supervisor = Thread(target=apply_stages, args=(runtime, root / "stage", stopped, failed))
    supervisor.start()
    try:
        with (root / "browser.log").open("xb") as stream:
            code = subprocess.run(argv, cwd=ROOT, env=env, stdout=stream, stderr=subprocess.STDOUT,
                                  timeout=1900, check=False).returncode
    finally:
        stopped.set()
        supervisor.join()
    return 1 if failed.is_set() else code


def apply_stages(runtime, directory, stopped, failed):
    valid = set(json.loads((directory.parent / "plan.json").read_text())["groups"]) | {"disarmed"}
    active = "disarmed"
    container = runtime.descriptor.resources.containers["data-api"].id
    stage_writer = ("from pathlib import Path; import sys; p=Path('/tmp/events-stage-next'); "
                    "p.write_text(sys.argv[1]); p.replace('/tmp/events-stage')")
    try:
        while not stopped.wait(0.05):
            requested = (directory / "current").read_text()
            if requested not in valid:
                raise ValueError("Unknown acceptance stage")
            if active != requested:
                runtime.command(["exec", container, "python", "-c", stage_writer, requested], timeout=10)
                pending = directory / "ack-pending"
                pending.write_text(requested)
                pending.replace(directory / "applied")
                active = requested
    except (OSError, ValueError, subprocess.SubprocessError):
        failed.set()


def extract(runtime, root):
    resource = runtime.descriptor.resources.containers.get("data-api")
    if resource is None:
        return
    runtime.command(["stop", resource.id])
    destination = root / "provider"
    destination.mkdir(mode=0o700)
    runtime.command(["cp", resource.id + ":/tmp/events-captures/.", str(destination)])
    for capture in destination.iterdir():
        capture.chmod(0o600)


def publish_summary(summary, root, guard_smoke, replay, seed_preflight):
    ledger = json.loads((root / "provider/ledger.json").read_text())
    summary.update(provider_sends=ledger["count"], denials=ledger["denials"], provider_ledger=ledger["entries"])
    if seed_preflight:
        observation = json.loads((root / "observations.json").read_text())
        summary["seed_preflight"] = observation["scenarios"]
        summary["seed_aborts"] = observation["seedAborts"]
        print(json.dumps(summary), flush=True)
        return int(bool(summary["browser_exit"] or ledger["count"] or ledger["denials"] or observation["browserRequests"]))
    if guard_smoke:
        print(json.dumps(summary), flush=True)
        return int(bool(ledger["count"] or ledger["denials"]))
    try:
        browser_observations = json.loads((root / "observations.json").read_text())
        summary["browser_requests"] = browser_observations["browserRequests"]
        summary.update(report_replay(root, replay) if replay else report(root))
    except Discrepancy as error:
        summary["check"] = str(error)
    except (OSError, ValueError, KeyError, TypeError):
        summary["check"] = "invalid private evidence"
    print(json.dumps(summary), flush=True)
    incomplete_live = summary["mode"] == "live" and not all(summary.get("final_inputs", {}).get(slot) for slot in ("calendar", "filings", "transcript", "news"))
    blocked_live = summary["mode"] == "live" and bool(summary.get("blocked"))
    return int(bool(summary.get("browser_exit") or summary.get("check") or blocked_live or incomplete_live))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("controlled", "live"))
    verification = parser.add_mutually_exclusive_group()
    verification.add_argument("--list", action="store_true", help="Discover tests without booting or accessing the provider")
    verification.add_argument("--replay-launch-calendar", type=Path, help="Inspect real captured earnings rows without provider sends")
    verification.add_argument("--guard-smoke", action="store_true", help="Boot and inspect the controlled guard without browser or provider traffic")
    profile = parser.add_mutually_exclusive_group()
    profile.add_argument("--supplemental", action="store_true", help="Use the frozen DRQ-to-MORN supplemental plan")
    profile.add_argument("--four-inputs", action="store_true", help="Use the frozen four-input CVNA proof plan")
    verification.add_argument("--seed-preflight", action="store_true", help="Exercise supplemental Workspace setup with provider requests disarmed")
    args = parser.parse_args()
    if args.four_inputs and (args.mode != "live" or args.replay_launch_calendar):
        parser.error("Four-input proof runs in live mode")
    if args.seed_preflight and (args.mode != "controlled" or not args.supplemental):
        parser.error("Seed preflight requires controlled supplemental mode")
    if args.supplemental and args.mode == "controlled" and not args.seed_preflight:
        parser.error("Controlled supplemental mode requires seed preflight")
    if (args.guard_smoke or args.replay_launch_calendar) and args.mode != "controlled":
        parser.error("Guard smoke and replay run in controlled mode")
    os.umask(0o077)
    artifacts = ROOT / "artifacts"
    if artifacts.resolve() != artifacts or not artifacts.is_dir():
        raise ValueError("Expected local ignored repository artifact directory")
    os.environ["QOPENBB_STORAGE_ROOT"] = str(artifacts)
    configured_key = os.environ.pop("FMP_API_KEY", "")
    key = "" if args.list or args.mode == "controlled" else configured_key
    cache = os.environ.pop("PLAYWRIGHT_BROWSERS_PATH", "")
    if not Path(cache).is_absolute():
        raise ValueError("Explicit isolated Playwright browser cache required")
    if args.mode == "live" and not args.list and not re.fullmatch(r"[A-Za-z0-9_-]+", key):
        raise ValueError("An explicit live FMP credential is required")
    root = Path(tempfile.mkdtemp(prefix="events-documents-run-", dir=artifacts))
    plan_name = ("events-documents-four-input-plan.json" if args.four_inputs else
                 "events-documents-supplemental-plan.json" if args.supplemental else "events-documents-plan.json")
    private_write(root / "plan.json", (HERE / plan_name).read_bytes())
    if args.four_inputs:
        private_write(root / "four-inputs", b"")
    if args.supplemental:
        private_write(root / "supplemental", b"")
    if args.seed_preflight:
        private_write(root / "seed-preflight", b"")
    if args.replay_launch_calendar:
        replay = args.replay_launch_calendar.resolve()
        if replay.parent != artifacts or not re.fullmatch(r"events-documents-run-[a-z0-9_]+", replay.name):
            raise ValueError("Expected owned private capture directory")
        path, _, _ = replay_source(replay)
        private_write(root / "replay-calendar.installed", path.read_bytes())
    os.environ["QOPENBB_ARTIFACTS"] = str(root)
    summary = {"mode": args.mode, "private_directory": str(root)}
    print(json.dumps(summary), flush=True)
    candidate = json.loads((artifacts / "reviewed/events-and-documents/candidate.json").read_text())
    config = resolve_environment(ROOT)
    images = candidate["images"]
    runtime = prepare(StartRequest(config, root / "runtime/session.json", images["workspace"]["image"], images["data-api"]["image"]))
    configure(runtime, root, args.mode, key, candidate)
    summary["candidate"] = {"sources": candidate["sources"],
                            "images": {service: item["image"] for service, item in images.items()}}
    if args.list:
        return browser(runtime, root, args.mode, True, cache)
    try:
        runtime.begin()
        if args.guard_smoke:
            summary["runtime"] = "ready"
        else:
            summary["browser_exit"] = browser(runtime, root, args.mode, False, cache)
    finally:
        try:
            extract(runtime, root)
        finally:
            summary["cleanup"] = stop(config, runtime.path)
    return publish_summary(summary, root, args.guard_smoke, args.replay_launch_calendar, args.seed_preflight)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ValueError, OSError, Discrepancy, subprocess.SubprocessError):
        print('Events runner failed; inspect the owned private runtime or browser diagnostics.', file=sys.stderr)
        raise SystemExit(1) from None
