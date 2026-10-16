"""Executable CLI and real Git evidence, using disposable repository fixtures."""

import json
import subprocess
import sys
from pathlib import Path

import pytest

from test_scope import BASE, HEAD, URL, manifest, scoped


ROOT = Path(__file__).resolve().parents[2]


def cli(root, *args):
    result = subprocess.run([sys.executable, "-m", "tools.quality.complexity", "--root", str(root),
                             "--python-only", *args], cwd=ROOT, capture_output=True, text=True)
    return result, json.loads(result.stdout)


def test_cli_reports_scope_errors_and_duplicate_arguments(scoped):
    root, _, _, run = scoped
    run()
    for arguments in [[], ["--base", f"workspace={BASE}"],
                      ["--changes", "workspace=absent.json"],
                      ["--base", f"workspace={BASE}", "--base", f"workspace={BASE}"]]:
        result, report = cli(root, *arguments)
        assert result.returncode == 2 and report["errors"]


def test_cli_exit_codes_and_output(scoped):
    root, config, write, run = scoped
    config["repositories"][0]["owners"][0]["files"] = ["src/big.py"]
    write("src/big.py", "x=1\n" * 301)
    run({"workspace": manifest([])})
    write("manifest.json", json.dumps(manifest([])))
    config["repositories"][0]["exclusions"].append({"patterns": ["manifest.json"], "reason": "test input", "source": "fixture"})
    run({"workspace": manifest([])})
    value = f"workspace={root / 'manifest.json'}"
    result, report = cli(root, "--changes", value)
    assert result.returncode == 0 and report["violations"]
    result, report = cli(root, "--changes", value, "--check")
    assert result.returncode == 1 and not report["errors"]
    output = root.parent / "report.json"
    result = subprocess.run([sys.executable, "-m", "tools.quality.complexity", "--root", str(root),
                             "--python-only", "--changes", value, "--output", str(output)],
                            cwd=ROOT, capture_output=True, text=True)
    assert result.returncode == 0 and json.loads(output.read_text())["files"]


def git(root, *arguments):
    return subprocess.run(["git", "-C", str(root), *arguments], capture_output=True,
                           text=True, check=True).stdout.strip()


def test_real_git_scope_verifies_origin_head_cleanliness_and_diff(scoped):
    root, config, write, run = scoped
    fork = root / "vendor/workspace"
    git(fork, "init")
    git(fork, "config", "user.name", "Fixture")
    git(fork, "config", "user.email", "fixture@example.invalid")
    git(fork, "remote", "add", "origin", URL)
    write("vendor/workspace/source.py", "x=1\n")
    git(fork, "add", ".")
    git(fork, "commit", "-m", "base")
    base = git(fork, "rev-parse", "HEAD")
    write("vendor/workspace/source.py", "x=2\n")
    git(fork, "add", ".")
    git(fork, "commit", "-m", "head")
    head = git(fork, "rev-parse", "HEAD")
    config["repositories"][1]["revision"] = base
    config["repositories"][1]["owners"][0]["files"] = ["source.py"]
    run()
    from tools.quality.complexity import inventory

    report = inventory(root, revisions={"workspace": (base, head)})
    assert not report["errors"] and report["files"][0]["logical"] == 1
    assert report["scope"][1]["provenance"] == "git-verified"
    assert inventory(root, revisions={"workspace": (base, base)})["errors"]
    write("vendor/workspace/source.py", "x=3\n")
    assert "clean" in " ".join(inventory(root, revisions={"workspace": (base, head)})["errors"])
    git(fork, "checkout", "--", "source.py")
    git(fork, "remote", "set-url", "origin", "https://example.invalid/other.git")
    assert "origin" in " ".join(inventory(root, revisions={"workspace": (base, head)})["errors"])


def test_git_scope_does_not_invent_missing_metadata(scoped):
    root, _, _, run = scoped
    run()
    from tools.quality.complexity import inventory

    assert inventory(root, revisions={"workspace": (BASE, HEAD)})["errors"]
    assert not inventory(root, changes={"workspace": manifest([])})["errors"]
