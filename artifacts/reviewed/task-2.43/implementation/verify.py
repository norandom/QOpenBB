"""Run a named task-local check without shell interpolation."""
import json
import os
from pathlib import Path
import subprocess
import sys

evidence = Path("/mnt/d/Source/QOpenBB/artifacts/task-2.43/implementation")
stage = Path("/home/mc/qopenbb-work/task243-colors-20261017/terminalpro")
node = "/mnt/d/Source/QOpenBB/artifacts/task-1.2/node-v24.22.0-linux-x64/bin/node"
name = sys.argv[1]
checks = {
    "red-vitest": [node, "node_modules/vitest/vitest.mjs", "run", "--config",
                   "tests/unit/chart-application/vitest.config.mjs",
                   "tests/unit/chart-application/appearanceColors.test.ts"],
    "green-vitest": [node, "node_modules/vitest/vitest.mjs", "run", "--config",
                     "tests/unit/chart-application/vitest.config.mjs",
                     "tests/unit/chart-application/appearanceColors.test.ts"],
    "strict-application": [node, "node_modules/typescript/bin/tsc", "--project",
                           "tests/unit/chart-application/tsconfig.json", "--noEmit"],
    "strict-compatibility": [node, "node_modules/typescript/bin/tsc", "--project",
                             "tests/unit/chart-compatibility/tsconfig.json", "--noEmit"],
    "biome": [node, "node_modules/@biomejs/biome/bin/biome", "check",
              "src/components/General/Table/Chart/application/appearanceColors.ts",
              "tests/unit/chart-application/appearanceColors.test.ts"],
    "format": [node, "node_modules/@biomejs/biome/bin/biome", "format", "--write",
               "src/components/General/Table/Chart/application/appearanceColors.ts",
               "tests/unit/chart-application/appearanceColors.test.ts"],
}
if name.endswith("-retry1"):
    checks[name] = checks[name.removesuffix("-retry1")]
log = evidence / f"{name}.log"
meta = evidence / f"{name}.json"
if log.exists() or meta.exists():
    raise SystemExit("Preserve existing run; choose a unique name")
environment = os.environ.copy()
environment["PATH"] = str(Path(node).parent) + os.pathsep + environment["PATH"]
with log.open("w") as stream:
    result = subprocess.run(checks[name], cwd=stage, env=environment,
                            stdout=stream, stderr=subprocess.STDOUT, check=False)
meta.write_text(json.dumps({"command": checks[name], "cwd": str(stage),
                           "exit_code": result.returncode, "log": str(log)}, indent=2) + "\n")
print(log.read_text())
raise SystemExit(result.returncode)
