"""Repository references retain the inventory's fail-closed boundary."""

import copy
import json
import os
import subprocess

import pytest

from test_scope import HEAD, manifest, scoped


def reference(scoped, value=None):
    root, config, write, run = scoped
    repo = copy.deepcopy(config["repositories"][1])
    write(".kiro/complexity/workspace.json", json.dumps(repo if value is None else value))
    config["repositories"][1] = {"include": ".kiro/complexity/workspace.json"}
    return root, config, write, run


def test_reference_and_inline_inventory_are_equivalent(scoped):
    _, config, write, run = scoped
    write("vendor/workspace/value.py", "x=1\n")
    config["repositories"][1]["owners"][0]["files"] = ["value.py"]
    changes = {"workspace": manifest([{"status": "M", "path": "value.py"}])}
    inline = run(changes)
    reference(scoped)
    assert run(changes) == inline


def test_reference_retains_ownership_validation(scoped):
    _, config, write, run = scoped
    write("vendor/workspace/unmapped.py", "pass\n")
    reference(scoped)
    changes = {"workspace": manifest([{"status": "M", "path": "unmapped.py"}])}
    assert "unmapped" in " ".join(run(changes)["errors"])


@pytest.mark.parametrize("path", ["../outside.json", "/absolute.json", "C:/x.json",
                                     "a/../x.json", "a\\x.json", "a//x.json", "", None])
def test_unsafe_reference_paths_fail(scoped, path):
    _, config, _, run = reference(scoped)
    config["repositories"][1] = {"include": path}
    assert run({"workspace": manifest([])})["errors"]


@pytest.mark.parametrize("value", [{"include": ".kiro/complexity/workspace.json"},
                                    [], None, 42])
def test_reference_requires_one_repository_object(scoped, value):
    _, _, write, run = reference(scoped)
    write(".kiro/complexity/workspace.json", json.dumps(value))
    assert run({"workspace": manifest([])})["errors"]


@pytest.mark.parametrize("source", ["{", '{"id":"first","id":"second"}'])
def test_invalid_or_duplicate_json_fails(scoped, source):
    _, _, write, run = reference(scoped)
    write(".kiro/complexity/workspace.json", source)
    assert run({"workspace": manifest([])})["errors"]


def test_missing_and_ambiguous_reference_fail(scoped):
    root, config, _, run = reference(scoped)
    config["repositories"][1]["id"] = "workspace"
    assert run({"workspace": manifest([])})["errors"]
    config["repositories"][1].pop("id")
    (root / ".kiro/complexity/workspace.json").unlink()
    assert run({"workspace": manifest([])})["errors"]


def test_reference_preserves_duplicate_and_source_lock_checks(scoped):
    _, config, write, run = scoped
    repo = copy.deepcopy(config["repositories"][1])
    repo["id"] = "qopenbb"
    reference(scoped, repo)
    assert "duplicate" in " ".join(run({})["errors"])
    repo["id"] = "workspace"
    repo["source_lock_key"] = "workspace"
    write(".kiro/complexity/workspace.json", json.dumps(repo))
    write("sources.lock.json", json.dumps({"workspace": {"revision": HEAD}}))
    assert "source lock" in " ".join(run({})["errors"])


def test_symlink_reference_inside_root_is_rejected(scoped):
    root, config, _, run = reference(scoped)
    link = root / ".kiro/linked.json"
    try:
        link.symlink_to(root / ".kiro/complexity/workspace.json")
    except OSError:
        pytest.skip("symlink creation unavailable")
    config["repositories"][1]["include"] = ".kiro/linked.json"
    assert run({"workspace": manifest([])})["errors"]


@pytest.mark.skipif(os.name != "nt", reason="Windows junction boundary")
def test_junction_reference_inside_root_is_rejected(scoped):
    root, config, _, run = reference(scoped)
    link = root / ".kiro/junction"
    result = subprocess.run(["cmd", "/c", "mklink", "/J", str(link),
                             str(root / ".kiro/complexity")], capture_output=True)
    assert result.returncode == 0
    config["repositories"][1]["include"] = ".kiro/junction/workspace.json"
    try:
        assert run({"workspace": manifest([])})["errors"]
    finally:
        link.rmdir()


def test_exceptions_resolve_the_same_repositories(scoped):
    from datetime import date, timedelta
    _, config, write, run = scoped
    write("vendor/workspace/big.py", "x=1\n" * 301)
    config["repositories"][1]["owners"][0]["files"] = ["big.py"]
    config["exceptions"] = [{"repository": "workspace", "path": "big.py", "metric": "logical",
        "baseline": 301, "revision": HEAD, "rationale": "Reviewed fixture baseline",
        "review": "fixture", "expires_on": (date.today() + timedelta(days=1)).isoformat()}]
    changes = {"workspace": manifest([{"status": "M", "path": "big.py"}])}
    inline = run(changes)
    root, _, _, run = reference(scoped)
    assert run(changes) == inline
    assert not inline["violations"] and not inline["errors"]
    assert inline["exceptions"][0]["actual"] == 301
    from tools.quality.exceptions import apply_exceptions
    (root / ".kiro/complexity/workspace.json").unlink()
    with pytest.raises((OSError, ValueError)):
        apply_exceptions(root, copy.deepcopy(inline))
