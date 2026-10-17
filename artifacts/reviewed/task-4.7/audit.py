"""Measure whole-file scope and retain actual scoped Ruff output."""

import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from tools.quality.complexity import physical_lines
from tools.quality.python_units import measure_python

OUTPUT = Path(__file__).resolve().parent
BACKEND = ROOT / "vendor/workspace/backend-api/backend"
os.environ["PATH"] = str(Path(sys.executable).parent) + ":/usr/bin:/bin"
source_path = BACKEND / "api/crud.py"
source = source_path.read_text()
units = measure_python(source, str(source_path.relative_to(ROOT)))
record = {
    "sha256": hashlib.sha256(source_path.read_bytes()).hexdigest(),
    "physical": physical_lines(source),
    "logical": units["logical"],
    "max_function": max(item["logical"] for item in units["functions"]),
    "functions": units["functions"],
    "checks": [],
}
tests = [str(BACKEND / "tests_sqlite" / name) for name in ("read_support.py", "test_dashboard_reads.py", "test_app_reads.py")]
for label, arguments in (
    ("tests-lint", ["check", *tests]),
    ("tests-format", ["format", "--check", *tests]),
    ("crud-lint", ["check", str(source_path)]),
    ("crud-format", ["format", "--check", str(source_path)]),
):
    command = [sys.executable, "-m", "ruff", *arguments]
    with (OUTPUT / f"{sys.argv[1]}-{label}.log").open("w") as log:
        result = subprocess.run(command, stdout=log, stderr=subprocess.STDOUT, check=False)
    record["checks"].append({"command": command, "exit": result.returncode, "log": f"{sys.argv[1]}-{label}.log"})
(OUTPUT / f"{sys.argv[1]}-audit.json").write_text(json.dumps(record, indent=2) + "\n")
print(json.dumps({key: record[key] for key in ("sha256", "physical", "logical", "max_function")}))
print([(item["log"], item["exit"]) for item in record["checks"]])
