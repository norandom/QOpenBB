"""Measure this lane's complete production file; the controller owns inventory acceptance."""
import hashlib
import json
import os
from pathlib import Path
import sys

root = Path("/mnt/d/Source/QOpenBB")
sys.path.insert(0, str(root))
from tools.quality.complexity import physical_lines, violations
from tools.quality.ts_adapter import measure_typescript

os.environ["PATH"] = str(root / "artifacts/task-1.2/node-v24.22.0-linux-x64/bin") + os.pathsep + os.environ["PATH"]
path = root / "vendor/workspace/terminalpro/src/components/General/Table/Chart/application/appearanceColors.ts"
rows, versions = measure_typescript([str(path)])
measurement = rows[str(path)]
measurement["physical"] = physical_lines(path.read_text())
report = {"scope": "Task-local whole file; not the combined maintained inventory gate",
          "metric": "project-syntax-units-v1", "versions": versions,
          "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
          "measurement": measurement,
          "violations": violations(measurement, {"physical": 400, "logical": 300, "function": 50})}
target = root / "artifacts/task-2.43/implementation/size.json"
if target.exists():
    raise SystemExit("Preserve existing size evidence")
target.write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps(report, indent=2))
raise SystemExit(bool(report["violations"]))
