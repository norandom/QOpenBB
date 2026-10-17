"""Capture serial SQLite checks against the frozen backend runtime."""

import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import platform
import sqlite3
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
BACKEND = ROOT / "vendor/workspace/backend-api/backend"
OUTPUT = Path(__file__).resolve().parent
os.environ["PATH"] = str(Path(sys.executable).parent) + ":/usr/bin:/bin"
label = sys.argv[1]
test = BACKEND / "tests_sqlite/test_dashboard_persistence.py"
commands = [
    [sys.executable, str(BACKEND / "tests_sqlite/run.py"), *(["-k", "persistence"] if label == "focused" else [])],
    [sys.executable, "-m", "ruff", "check", str(test)],
    [sys.executable, "-m", "ruff", "format", "--check", str(test)],
]
record = {
    "python": sys.executable,
    "version": platform.python_version(),
    "sqlite": sqlite3.sqlite_version,
    "workspace_revision": subprocess.check_output(["git", "-C", str(ROOT / "vendor/workspace"), "rev-parse", "HEAD"], text=True).strip(),
    "sources": {
        str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in [BACKEND / "api/crud.py", *(BACKEND / "tests_sqlite").glob("*.py"), BACKEND / "poetry.lock", BACKEND / "pyproject.toml"]
    },
    "distributions": {dist.metadata["Name"]: dist.version for dist in importlib.metadata.distributions()},
    "checks": [],
}
for number, command in enumerate(commands):
    output = OUTPUT / f"{label}-{number}.log"
    with output.open("w") as log:
        result = subprocess.run(command, stdout=log, stderr=subprocess.STDOUT, check=False)
    record["checks"].append({"command": command, "exit": result.returncode, "log": output.name})
    print(f"{output.name}: exit={result.returncode}", flush=True)
(OUTPUT / f"{label}.json").write_text(json.dumps(record, indent=2) + "\n")
raise SystemExit(int(any(check["exit"] for check in record["checks"])))
