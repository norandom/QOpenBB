"""Relocate the frozen assertion runner; never overwrite the original evidence."""
from pathlib import Path
import json
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent / "grid-reproduction"
BASE = ROOT / "artifacts/parity/grid-runtime-next"
OUT.mkdir(exist_ok=True)
for case in ("ordinary", "filtered-sorted-bounds", "numeric-only", "multiple-category",
             "formatted-margin", "hidden-selected", "synthetic-value-getter"):
    shutil.copyfile(BASE / (case + ".json"), OUT / (case + ".json"))
source = (BASE / "assert.mjs").read_text()
source = source.replace("/mnt/d/Source/QOpenBB/artifacts/parity/grid-runtime-next",
                        "/mnt/d/Source/QOpenBB/artifacts/runtime-contract-next/review/grid-reproduction")
(OUT / "assert.mjs").write_text(source)
command = ["wsl", "-d", "Debian", "-u", "mc", "--",
           "/mnt/d/Source/QOpenBB/artifacts/task-1.2/node-v24.22.0-linux-x64/bin/node",
           "/mnt/d/Source/QOpenBB/artifacts/runtime-contract-next/review/grid-reproduction/assert.mjs"]
result = subprocess.run(command, capture_output=True, text=True)
assert result.returncode == 0, result.stderr
assert (BASE / "assertions.json").read_bytes() == (OUT / "assertions.json").read_bytes()
(OUT.parent / "grid-replay.json").write_text(json.dumps({"command": command,
    "exitCode": result.returncode, "stdout": result.stdout, "stderr": result.stderr,
    "assertionsByteExact": True, "transformation": "Only assertion runner root redirected to review-owned directory.",
    "browserRun": False}, indent=2) + "\n")
print(result.stdout)
