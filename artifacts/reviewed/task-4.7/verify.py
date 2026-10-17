"""Record the bounded read suite, runtime and exact source identities."""

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
paths = [BACKEND / "api/crud.py", *(BACKEND / "tests_sqlite").glob("*.py"), BACKEND / "poetry.lock", BACKEND / "pyproject.toml"]
record = {
    "python": sys.executable,
    "version": platform.python_version(),
    "sqlite": sqlite3.sqlite_version,
    "workspace_revision": subprocess.check_output(["git", "-C", str(ROOT / "vendor/workspace"), "rev-parse", "HEAD"], text=True).strip(),
    "sources": {str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest() for path in paths},
    "distributions": {dist.metadata["Name"]: dist.version for dist in importlib.metadata.distributions()},
}
command = [sys.executable, str(BACKEND / "tests_sqlite/run.py"), "-s"]
with (OUTPUT / f"{label}.log").open("w") as log:
    result = subprocess.run(command, stdout=log, stderr=subprocess.STDOUT, check=False)
record.update(command=command, exit=result.returncode)
(OUTPUT / f"{label}.json").write_text(json.dumps(record, indent=2) + "\n")
print(f"{label}: exit={result.returncode}; {OUTPUT / (label + '.log')}")
raise SystemExit(result.returncode)
