"""Build and load the two prototype images through the existing portable commands."""
import argparse
import json
from pathlib import Path
import re
import subprocess
import sys


def release_version(value: str) -> str:
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}", value):
        raise argparse.ArgumentTypeError("release version must be a safe public identifier")
    return value


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("--output", type=Path, required=True)
    result.add_argument("--release-version", type=release_version, required=True)
    for name, default in (("lock", "sources.lock.json"),
                          ("policy", "contracts/sources.json"),
                          ("tools", "pipeline/tools.lock.json"),
                          ("sdk-python", ".dagger/.venv/bin/python")):
        result.add_argument("--" + name, type=Path, default=Path(default))
    result.add_argument("--runtime-root", type=Path, default=Path.cwd())
    return result


def invoke(arguments: list[str], log: Path) -> None:
    with log.open("x", encoding="utf-8") as stream:
        subprocess.run([sys.executable, "-m", "qopenbb_ci.image_cli", *arguments],
                       stdout=stream, check=True)


def build_service(args: argparse.Namespace, service: str) -> dict:
    directory = args.output / service
    directory.mkdir()
    staged = directory / "stage"
    archive = directory / "image.tar"
    common = ["--lock", str(args.lock), "--policy", str(args.policy)]
    stage = ["stage", *common, "--workspace", str(args.output / "sources/workspace"),
             "--data-api", str(args.output / "sources/data_api"),
             "--destination", str(staged), "--service", service]
    if service == "workspace":
        stage += ["--release-version", args.release_version]
    else:
        stage += ["--runtime-root", str(args.runtime_root)]
    invoke(stage, directory / "stage.json")
    invoke(["export", *common, "--stage", str(staged), "--service", service,
            "--tools", str(args.tools), "--sdk-python", str(args.sdk_python),
            "--archive", str(archive), "--report", str(directory / "export.json")],
           directory / "export.log")
    report = directory / "load.json"
    invoke(["load", "--archive", str(archive), "--report", str(report)],
           directory / "load.log")
    loaded = json.loads(report.read_text(encoding="utf-8"))
    if not re.fullmatch(r"sha256:[0-9a-f]{64}", loaded.get("loaded_image_id", "")):
        raise ValueError("load report lacks an exact loaded image identity")
    return {"image": loaded["loaded_image_id"], "report": str(report)}


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        # An existing directory, including an empty one, may belong to another run.
        args.output = args.output.absolute()
        args.output.mkdir(parents=True, exist_ok=False)
        invoke(["acquire", "--lock", str(args.lock), "--destination",
                str(args.output / "sources")], args.output / "acquire.json")
        images = {}
        for service in ("workspace", "data-api"):
            images[service] = build_service(args, service)
        summary = {"schema_version": 1, "release_version": args.release_version,
                   "images": images}
        (args.output / "summary.json").write_text(
            json.dumps(summary, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(summary))
        return 0
    except (OSError, ValueError, subprocess.SubprocessError) as error:
        print(json.dumps({"valid": False, "error": type(error).__name__}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
