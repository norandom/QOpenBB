"""Isolate task 2.42 checks and retain each exact command result."""

import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import time

ROOT = Path("/mnt/d/Source/QOpenBB")
OUT = ROOT / "artifacts/task-2.42/implementation"
WORKSPACE = ROOT / "vendor/workspace/terminalpro"
NODE = "/mnt/d/Source/QOpenBB/artifacts/task-1.2/node-v24.22.0-linux-x64/bin/node"
OWNED = [
    "src/components/General/Table/Chart/application/appearanceComposition.ts",
    "tests/unit/chart-application/appearanceComposition.test.ts",
]


def identity(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def prepare():
    stage = Path(f"/home/mc/qopenbb-work/task242-{time.time_ns()}/terminalpro")
    shutil.copytree(
        "/home/mc/qopenbb-work/task241-20261017135547/terminalpro",
        stage,
        symlinks=True,
        ignore=shutil.ignore_patterns("node_modules"),
    )
    (stage / "node_modules").symlink_to(
        "/home/mc/qopenbb-work/appearance-deps/terminalpro/node_modules",
        target_is_directory=True,
    )
    paths = []
    for directory in [
        "src/components/General/Table/Chart/application",
        "src/components/General/Table/Chart/compatibility",
        "src/components/General/Table/Chart/echarts",
        "tests/unit/chart-application",
        "tests/unit/chart-compatibility",
        "tests/e2e/chart-compatibility",
    ]:
        for source in sorted((WORKSPACE / directory).rglob("*")):
            if source.is_file():
                relative = source.relative_to(WORKSPACE)
                target = stage / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, target)
                paths.append({"path": relative.as_posix(), "sha256": identity(target)})
    for relative in ["package.json", "biome.json"]:
        shutil.copy2(WORKSPACE / relative, stage / relative)
        paths.append({"path": relative, "sha256": identity(stage / relative)})
    (OUT / "stage.json").write_text(json.dumps({
        "stage": str(stage), "inputs": paths,
        "node": NODE,
        "nodeSha256": identity(Path(NODE)),
        "dependencies": str((stage / "node_modules").resolve()),
    }, indent=2) + "\n")
    return stage


phase = sys.argv[1]
stage = prepare() if phase == "red" else Path(json.loads((OUT / "stage.json").read_text())["stage"])
if phase == "restore-accepted-sibling-closure":
    paths = [
        "src/components/General/Table/Chart/compatibility/optionStateTypes.ts",
        "src/components/General/Table/Chart/compatibility/editorEvents.ts",
        "src/components/General/Table/Chart/application/sessionState.ts",
        "src/components/General/Table/Chart/application/types.ts",
        "tests/unit/chart-compatibility/editorEvents.test.ts",
        "tests/unit/chart-application/sessionState.test.ts",
    ]
    restored = []
    for relative in paths:
        source = Path("/home/mc/qopenbb-work/task241-20261017135547/terminalpro") / relative
        before = identity(stage / relative)
        shutil.copy2(source, stage / relative)
        restored.append({
            "path": relative, "source": str(source), "previousSha256": before,
            "acceptedSha256": identity(source), "stagedSha256": identity(stage / relative),
        })
    (OUT / f"accepted-sibling-overlay-{time.time_ns()}.json").write_text(json.dumps({
        "reason": "Use accepted 2.41 source/test pairs for all sibling-owned paths during isolated 2.42 checks; final joined current verification belongs to the independent reviewer.",
        "inputs": restored,
    }, indent=2) + "\n")
    print("Restored accepted sibling closure", len(restored), "paths")
    sys.exit(0)
if phase != "red":
    for relative in OWNED:
        shutil.copy2(WORKSPACE / relative, stage / relative)

commands = {
    "red": [[NODE, "node_modules/vitest/vitest.mjs", "run", "--config", "tests/unit/chart-application/vitest.config.mjs", "tests/unit/chart-application/appearanceComposition.test.ts"]],
    "green": [[NODE, "node_modules/vitest/vitest.mjs", "run", "--config", "tests/unit/chart-application/vitest.config.mjs", "tests/unit/chart-application/appearanceComposition.test.ts"]],
    "strict": [
        [NODE, "node_modules/typescript/bin/tsc", "--project", "tests/unit/chart-application/tsconfig.json", "--noEmit"],
        [NODE, "node_modules/typescript/bin/tsc", "--project", "tests/unit/chart-compatibility/tsconfig.json", "--noEmit"],
    ],
    "lint": [[NODE, "node_modules/@biomejs/biome/bin/biome", "check", *OWNED]],
    "format": [[NODE, "node_modules/@biomejs/biome/bin/biome", "check", "--write", *OWNED]],
}
results = []
for index, command in enumerate(commands[phase], 1):
    log = OUT / f"{phase}-{index}-{time.time_ns()}.log"
    with log.open("w") as output:
        output.write("cwd: " + str(stage) + "\ncommand: " + " ".join(command) + "\n")
        output.flush()
        result = subprocess.run(command, cwd=stage, stdout=output, stderr=subprocess.STDOUT, check=False)
        output.write(f"\nexit: {result.returncode}\n")
    results.append({
        "command": command, "exit": result.returncode,
        "log": log.relative_to(ROOT).as_posix(), "sha256": identity(log),
        "ownedInputs": [{"path": p, "sha256": identity(stage / p)} for p in OWNED if (stage / p).is_file()],
    })
    print(log.name, "exit", result.returncode, flush=True)
    print(log.read_text(), flush=True)
if phase == "format":
    for relative in OWNED:
        shutil.copy2(stage / relative, WORKSPACE / relative)
(OUT / f"{phase}-status-{time.time_ns()}.json").write_text(json.dumps(results, indent=2) + "\n")
sys.exit(any(item["exit"] != 0 for item in results))
