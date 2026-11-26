"""Export and load the independently locked Modeling runtime with the pinned Dagger tools."""

import argparse
import hashlib
import json
import re
import subprocess
import tempfile
from pathlib import Path

from .container_command import resolve_executable
from .image_cli import build_environment, verify_engine
from .images import inspect_archive, load
from .runtime_inputs import RUNTIME_FILES, copy_inputs

ROOT = Path(__file__).resolve().parents[2]


MODELING_FILES = frozenset(name for name in RUNTIME_FILES
                          if name.startswith("services/data-api/qopenbb_data/modeling/")) | {
    "services/data-api/qopenbb_data/__init__.py", "services/modeling/pyproject.toml", "services/modeling/uv.lock",
}


def stage_modeling(root, stage):
    return copy_inputs(root, stage, MODELING_FILES)


def build(output, cli, sdk_python):
    tools = json.loads((ROOT / "pipeline/tools.lock.json").read_bytes())
    reference = tools["base_images"]["dagger_engine"]
    env = build_environment(None, reference)
    with tempfile.TemporaryDirectory(prefix="qopenbb-modeling-build-") as home:
        env.update(HOME=home, USERPROFILE=home, DOCKER_CONFIG=home, XDG_CONFIG_HOME=home)
        version = subprocess.check_output([cli, "version"], env=env, text=True)
        if not re.match(r"^dagger v" + re.escape(tools["tools"]["dagger_cli"]["version"]) + r"\s", version):
            raise ValueError("Dagger CLI differs from the tools lock")
        sdk = subprocess.check_output([sdk_python, "-c",
                                      "import importlib.metadata; print(importlib.metadata.version('dagger-io'))"],
                                     env=env, text=True).strip()
        if sdk != tools["tools"]["dagger_python_sdk"]["version"]:
            raise ValueError("Dagger SDK differs from the tools lock")
        output.mkdir(parents=True, exist_ok=False)
        archive = output / "modeling.tar"
        stage = Path(home) / "stage"
        inputs = stage_modeling(ROOT, stage)
        base = tools["base_images"]["python"]
        manifest = {"base": base, "runtime_inputs": inputs}
        (stage / "inputs.json").write_text(json.dumps(manifest, sort_keys=True) + "\n")
        (output / "inputs.json").write_bytes((stage / "inputs.json").read_bytes())
        subprocess.run([cli, "run", "--", sdk_python, "-m", "qopenbb.modeling_export",
                        "--stage", stage, "--archive", archive], env=env, check=True)
    engine = verify_engine(reference)
    observed = inspect_archive(archive)
    fingerprint = hashlib.sha256((json.dumps(inputs, sort_keys=True) + "\n").encode()).hexdigest()
    if observed["labels"].get("org.qopenbb.runtime-inputs.sha256") != fingerprint:
        raise ValueError("Modeling image input fingerprint differs from its staged sources")
    report = {**load(archive, observed), "engine": engine, "runtime_inputs_sha256": fingerprint,
              "runtime_lock_sha256": inputs["services/modeling/uv.lock"], "sdk_version": sdk}
    (output / "image.json").write_text(json.dumps(report, indent=2) + "\n")
    return report["loaded_image_id"]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--dagger-cli", default="dagger")
    parser.add_argument("--sdk-python", default=str(ROOT / ".dagger/.venv/bin/python"))
    args = parser.parse_args()
    print(build(args.output.resolve(), str(resolve_executable(args.dagger_cli)),
                str(resolve_executable(args.sdk_python, preserve_symlinks=True))))


if __name__ == "__main__":
    main()
