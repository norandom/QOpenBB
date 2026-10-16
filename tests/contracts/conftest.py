import copy
import json
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[2]


@pytest.fixture
def bundle():
    digest = "sha256:" + "a" * 64
    identity = {
        "release_id": "checkpoint-1", "run_id": "run-1",
        "revisions": {name: "b" * 40 for name in ("qopenbb", "workspace", "data_api", "agent")},
        "images": {name: {"digest": f"ghcr.io/example/{name}@{digest}", "architecture": "linux/amd64"}
                   for name in ("workspace", "data-api", "agent")},
        "lock_hashes": {name: digest for name in ("source", "tools", "dependencies")},
        "contract_hashes": {"openapi": digest, "widgets": digest},
        "model": {"provider": "anthropic", "name": "claude-configured-model"},
    }
    checks = [
        {"capability": "workspace", "requirements": ["4.3", "4.7"], "evidence_class": "live"},
        {"capability": "data_api", "requirements": ["5.1", "5.6"], "evidence_class": "live"},
        {"capability": "anthropic", "requirements": ["12.1", "12.2", "12.5"], "evidence_class": "live"},
    ]
    expected = {"schema_version": 1, "identity": identity, "required_checks": checks}
    records = [{
        "schema_version": 1, "record_id": f"record-{check['capability']}", **check,
        "status": "passed", "identity": copy.deepcopy(identity),
        "command": "recorded acceptance procedure", "timestamp": "2026-10-16T10:00:00Z",
        "exit_code": 0, "result": "observed expected financial output",
        "artifacts": [{"path": "artifacts/acceptance/result.json", "sha256": digest}],
    } for check in checks]
    manifest = {
        "schema_version": 1, "status": "candidate", "identity": copy.deepcopy(identity),
        "profiles": [], "required_configuration": ["ANTHROPIC_API_KEY"],
        "state_compatibility": {"format": "workspace-v1", "restore_from": ["workspace-v1"]},
        "acceptance_refs": [record["record_id"] for record in records],
    }
    backup = {
        "schema_version": 1, "backup_id": "backup-1", "identity": copy.deepcopy(identity),
        "captured_at": "2026-10-16T10:00:00Z", "state_format": "workspace-v1",
        "archive": {"path": "artifacts/backups/workspace.tar", "sha256": digest},
        "services_stopped": True, "private_configuration_ref": "private:deployment-configuration-1",
        "restore_compatibility": ["workspace-v1"],
    }
    return {"expected": expected, "records": records, "manifest": manifest, "backup": backup}


@pytest.fixture
def invoke(tmp_path):
    def run(scope, payload, expected=None, records=()):
        import subprocess
        import sys

        def write(name, value):
            path = tmp_path / name
            path.write_text(json.dumps(value), encoding="utf-8")
            return str(path)

        args = [sys.executable, "-m", "qopenbb_ci.cli", "check", "--scope", scope,
                "--input", write("input.json", payload)]
        if expected is not None:
            args.extend(["--expected", write("expected.json", expected)])
        for index, record in enumerate(records):
            args.extend(["--evidence", write(f"record-{index}.json", record)])
        report = tmp_path / "report.json"
        args.extend(["--report", str(report)])
        process = subprocess.run(args, capture_output=True, text=True)
        return process, json.loads(report.read_text()) if report.exists() else None
    return run
