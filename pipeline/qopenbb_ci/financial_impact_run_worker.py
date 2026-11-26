"""Capture pytest hook evidence in a fresh interpreter for each selector."""

import json
import sys
from collections import defaultdict
from pathlib import Path

import pytest

_PHASES = {"setup", "call", "teardown"}


class Evidence:
    def __init__(self, selector: str):
        self.selector = selector
        self.valid_selection = False
        self.collected = set()
        self.selected = set()
        self.deselected = set()
        self.collection = {}
        self.reports = defaultdict(list)

    def pytest_sessionstart(self, session):
        config = session.config
        # Last-failed mode can omit entire files before any deselection hook fires.
        self.valid_selection = (
            config.args == [self.selector]
            and not config.getoption("runxfail", False)
            and not config.getoption("lf", False)
        )

    def pytest_itemcollected(self, item):
        self.collected.add(item.nodeid)

    def pytest_deselected(self, items):
        self.deselected.update(item.nodeid for item in items)

    def pytest_collection_finish(self, session):
        self.selected.update(item.nodeid for item in session.items)

    def pytest_collectreport(self, report):
        if not report.passed:
            self.collection[report.nodeid] = report.outcome

    def pytest_runtest_logreport(self, report):
        outcome = report.outcome
        if hasattr(report, "wasxfail"):
            outcome = "xfailed" if report.skipped else "xpassed"
        self.reports[report.nodeid].append((report.when, outcome))

    def as_dict(self) -> dict:
        node_ids = self.collected | self.selected | self.deselected | self.reports.keys()
        return {
            "valid_selection": self.valid_selection,
            "collection": self.collection,
            "nodes": {node_id: self.node(node_id) for node_id in sorted(node_ids)},
        }

    def node(self, node_id: str) -> dict:
        reports = self.reports.get(node_id, [])
        phases = dict(reports)
        state = "unevaluated"
        if node_id in self.deselected or node_id not in self.selected:
            state = "deselected"
        elif len(phases) != len(reports):
            state = "partial"
        elif phases.keys() == _PHASES:
            state = "passed"
        elif phases:
            state = "partial"
        if state in {"passed", "partial"}:
            state = next((outcome for outcome in phases.values() if outcome != "passed"), state)
        return {"outcome": state, "phases": phases}


def main() -> int:
    report_path, selector = sys.argv[1:]
    root = Path.cwd()
    sys.path.insert(0, str(root))
    evidence = Evidence(selector)
    args = ["-q", "--rootdir", str(root), "-o", "addopts="]
    pipeline_config = root / "pipeline" / "pyproject.toml"
    if pipeline_config.is_file():
        args.extend(["-c", str(pipeline_config), "--strict-markers", "-m", "not live"])
    exit_code = pytest.main([*args, "--", selector], plugins=[evidence])
    Path(report_path).write_text(json.dumps(evidence.as_dict()), encoding="utf-8")
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
