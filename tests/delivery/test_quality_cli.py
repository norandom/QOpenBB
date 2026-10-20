"""Full maintained scope is explicit and never inferred from an empty Git diff."""
import json
import os
from pathlib import Path
import subprocess
import sys
import textwrap

import pytest

from qopenbb_ci import quality_cli
from qopenbb_ci.source_filter import ALLOW, source_scope


@pytest.mark.parametrize("source", ["workspace", "data_api"])
def test_repository_build_policy_matches_locked_source_revision(source):
    root = Path(__file__).resolve().parents[2]
    policy = json.loads((root / "contracts/sources.json").read_text())
    lock = json.loads((root / "sources.lock.json").read_text())

    assert source_scope(source, lock[source]["revision"], policy, lock) == ALLOW[source]


@pytest.fixture
def project(tmp_path, monkeypatch):
    (tmp_path / ".kiro").mkdir()
    repos, lock = [], {}
    for name in ("workspace", "data_api"):
        entry = {"repository": "https://github.com/norandom/" + name + ".git",
                 "revision": "a" * 40}
        lock[name] = entry
        repo = {"id": name, **entry, "source_lock_key": name,
                "root": "vendor/" + name,
                "owners": [{"files": ["a.py", "b.py"]}]}
        repos.append(repo)
        checkout = tmp_path / repo["root"]
        checkout.mkdir(parents=True)
        for file in ("a.py", "b.py"):
            (checkout / file).write_text("pass\n")
    inventory = tmp_path / ".kiro/complexity-budgets.json"
    inventory.write_text(json.dumps({"repositories": repos}))
    (tmp_path / "sources.lock.json").write_text(json.dumps(lock))
    identities = []
    monkeypatch.setattr(quality_cli, "identity", lambda root, entry: identities.append((root, entry)))
    return tmp_path, repos, identities


def options(root):
    return ["--inventory", str(root / ".kiro/complexity-budgets.json"),
            "--lock", str(root / "sources.lock.json"),
            "--output", str(root / "artifacts/result.json")]


def test_exact_full_scopes_and_checker_exit_code(project, monkeypatch):
    root, repos, identities = project
    calls = []

    def run(command, *, check):
        calls.append(command)
        assert check is False
        assert command[:5] == [sys.executable, "-m", "tools.quality.complexity", "--check", "--root"]
        assert command[5:8] == [str(root), "--output", str(root / "artifacts/result.json")]
        for offset, repo in ((8, repos[0]), (10, repos[1])):
            assert command[offset] == "--changes"
            name, path = command[offset + 1].split("=", 1)
            assert name == repo["id"]
            scope = json.loads(Path(path).read_text())
            assert scope == {"repository": repo["repository"], "base": "a" * 40,
                             "head": "a" * 40, "changes": [
                                 {"status": "M", "path": "a.py"},
                                 {"status": "M", "path": "b.py"}]}
        return type("Result", (), {"returncode": 1})()

    monkeypatch.setattr(quality_cli.subprocess, "run", run)
    assert quality_cli.main(options(root)) == 1
    assert len(calls) == 1 and len(identities) == 2


@pytest.mark.parametrize("problem", ["missing", "glob", "revision", "identity", "empty"])
def test_incomplete_or_unverified_scope_fails_before_checker(project, monkeypatch, problem):
    root, repos, _ = project
    if problem == "missing":
        (root / "vendor/workspace/b.py").unlink()
    elif problem == "glob":
        repos[0]["owners"][0]["files"] = ["*.py"]
    elif problem == "revision":
        repos[0]["revision"] = "b" * 40
    elif problem == "empty":
        repos[0]["owners"][0]["files"] = []
    else:
        def reject(*args):
            raise ValueError("tracked source differs from locked commit")
        monkeypatch.setattr(quality_cli, "identity", reject)
    (root / ".kiro/complexity-budgets.json").write_text(json.dumps({"repositories": repos}))
    monkeypatch.setattr(quality_cli.subprocess, "run", lambda *a, **k: pytest.fail("checker must not run"))
    assert quality_cli.main(options(root)) == 2


def test_noncanonical_inputs_fail_instead_of_checker_using_other_files(project, monkeypatch):
    root, _, _ = project
    other = root / "other.json"
    other.write_text("{}")
    monkeypatch.setattr(quality_cli.subprocess, "run", lambda *a, **k: pytest.fail("checker must not run"))
    assert quality_cli.main([*options(root), "--lock", str(other)]) == 2


@pytest.mark.skipif(os.name != "posix", reason="CI acquisition block runs in a Linux shell")
def test_ci_acquisition_maps_source_keys_to_actual_inventory_roots(tmp_path):
    root = Path(__file__).resolve().parents[2]
    workflow = (root / ".github/workflows/prototype.yml").read_text()
    step = workflow.split(
        "- name: Acquire pinned sources for maintained-scope verification\n", 1)[1]
    block = textwrap.dedent(step.split("run: |\n", 1)[1].split("      - name:", 1)[0])
    fake_python = tmp_path / "pipeline/.venv/bin/python"
    fake_python.parent.mkdir(parents=True)
    fake_python.write_text("#!" + sys.executable + "\n" + textwrap.dedent('''\
        from pathlib import Path
        import sys
        assert sys.argv[1:] == ["-m", "qopenbb_ci.image_cli", "acquire",
                                "--lock", "sources.lock.json", "--destination", "vendor"]
        for key in ("workspace", "data_api"):
            target = Path("vendor") / key
            target.mkdir(parents=True)
            (target / "source-key").write_text(key)
        '''))
    fake_python.chmod(0o700)
    subprocess.run(["bash", "-euo", "pipefail", "-c", block], cwd=tmp_path, check=True)
    config = json.loads((root / ".kiro/complexity-budgets.json").read_text())
    repos = {repo["id"]: repo for repo in config["repositories"]}
    for name in ("workspace", "data_api"):
        checkout = tmp_path / repos[name]["root"]
        assert checkout.is_dir()
        assert (checkout / "source-key").read_text() == name
    assert not (tmp_path / "vendor/data_api").exists()
