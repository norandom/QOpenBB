"""Run required pytest selectors and return their observed evidence."""

import json
import os
import subprocess
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

_WORKER = Path(__file__).with_name("financial_impact_run_worker.py").resolve()


def run_checks(selectors: list[str], root: Path) -> dict:
    """Return ordered selector results, with node IDs relative to the checkout root."""
    results = [_run_selector(selector, root) for selector in selectors]
    return {
        "passed": bool(results) and all(result["passed"] for result in results),
        "results": results,
    }


def _run_selector(selector: str, root: Path) -> dict:
    result = {
        "selector": selector,
        "passed": False,
        "exit_code": None,
        "nodes": {},
        "collection": {},
    }
    # An empty target or option cannot establish evidence for a required selector.
    if not selector.strip() or selector.startswith("-"):
        return result
    # Ambient pytest arguments and plugins can hide files before collection.
    env = {key: value for key, value in os.environ.items() if not key.startswith("PYTEST_")}
    env["PYTEST_DISABLE_PLUGIN_AUTOLOAD"] = "1"
    with TemporaryDirectory(prefix="qopenbb-pytest-") as directory:
        report = Path(directory) / "evidence.json"
        try:
            process = subprocess.run(
                [sys.executable, str(_WORKER), str(report), selector],
                cwd=root,
                env=env,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.STDOUT,
                check=False,
            )
            result["exit_code"] = process.returncode
            evidence = json.loads(report.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return result

    nodes = evidence["nodes"]
    result.update(
        nodes=nodes,
        collection=evidence["collection"],
        passed=(
            process.returncode == 0
            and evidence["valid_selection"]
            and bool(nodes)
            and not evidence["collection"]
            and all(node["outcome"] == "passed" for node in nodes.values())
        ),
    )
    return result
