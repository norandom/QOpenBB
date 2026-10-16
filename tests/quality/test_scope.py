"""Scope fixtures declare ownership and fork provenance without Git metadata."""

import json

import pytest


BASE = "a" * 40
HEAD = "b" * 40
URL = "https://github.com/owner/fork.git"


@pytest.fixture
def scoped(tmp_path):
    root = tmp_path / "root"
    root.mkdir()
    config = {"schema_version": 1, "metric": "project-syntax-units-v1",
              "limits": {"physical": 400, "logical": 300, "function": 50},
              "repositories": []}
    own = {"id": "qopenbb", "repository": "local:qopenbb", "root": ".", "mode": "all",
           "owners": [{"spec": "fixture", "include": ["src/**"], "files": []}],
           "exclusions": [{"patterns": [".kiro/**", "vendor/**"],
                           "reason": "fixture configuration and separate fork", "source": "fixture"}]}
    fork = {"id": "workspace", "repository": URL, "root": "vendor/workspace",
            "mode": "changed", "revision": BASE,
            "owners": [{"spec": "fixture", "include": ["**/*"], "files": []}], "exclusions": []}
    config["repositories"] = [own, fork]
    (root / "vendor/workspace").mkdir(parents=True)

    def write(path, source):
        file = root / path
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text(source)

    def run(changes=None):
        from tools.quality.complexity import inventory

        write(".kiro/complexity-budgets.json", json.dumps(config))
        return inventory(root, changes=changes, python_only=True)

    return root, config, write, run


def manifest(changes):
    return {"repository": URL, "base": BASE, "head": HEAD, "changes": changes}


def test_each_fork_needs_explicit_input_even_when_empty(scoped):
    _, _, _, run = scoped
    assert "workspace" in " ".join(run()["errors"])
    assert not run({"workspace": manifest([])})["errors"]


def test_root_new_file_requires_mapping(scoped):
    _, config, write, run = scoped
    write("src/new.py", "x=1\n")
    assert "unmapped" in " ".join(run({"workspace": manifest([])})["errors"])
    config["repositories"][0]["owners"][0]["files"] = ["src/new.py"]
    report = run({"workspace": manifest([])})
    assert not report["errors"]
    assert report["files"][0]["logical"] == 1


def test_missing_mapping_and_syntax_errors_fail(scoped):
    _, config, write, run = scoped
    config["repositories"][0]["owners"][0]["files"] = ["src/missing.py", "src/broken.py"]
    write("src/broken.py", "def broken(")
    errors = " ".join(run({"workspace": manifest([])})["errors"])
    assert "missing" in errors and "syntax" in errors


def test_modified_ignored_fork_is_measured_whole(scoped):
    _, _, write, run = scoped
    write("vendor/workspace/big.py", "x=1\n" * 401)
    report = run({"workspace": manifest([{"status": "M", "path": "big.py"}])})
    assert report["files"][0]["repository"] == "workspace"
    assert report["files"][0]["physical"] == 401
    assert report["violations"]
    assert "unmapped" in " ".join(report["errors"])


def test_delete_tombstone_and_rename_destination(scoped):
    _, config, write, run = scoped
    config["repositories"][1]["owners"][0]["files"] = ["old.py", "new.py"]
    write("vendor/workspace/new.py", "x=1\n" * 301)
    entries = [{"status": "D", "path": "old.py"},
               {"status": "R", "old_path": "prior.py", "path": "new.py"}]
    report = run({"workspace": manifest(entries)})
    assert not report["errors"]
    assert report["deleted"] == [{"repository": "workspace", "path": "old.py"}]
    assert report["violations"][0]["actual"] == 301


@pytest.mark.parametrize("path", ["../outside.py", "/tmp/file.py", "C:/x.py", "a/../b.py", "a\\b.py", "a//b.py"])
def test_unsafe_paths_fail(scoped, path):
    _, _, _, run = scoped
    assert run({"workspace": manifest([{"status": "M", "path": path}])})["errors"]


@pytest.mark.parametrize("mutate", [
    lambda m: m.update(repository="https://github.com/other/fork.git"),
    lambda m: m.update(base="c" * 40), lambda m: m.pop("head"),
    lambda m: m.update(changes=None),
    lambda m: m.update(changes=[{"status": "X", "path": "x.py"}]),
    lambda m: m.update(changes=[{"status": "R", "path": "x.py"}]),
    lambda m: m.update(changes=[{"status": "M", "path": "x.py"}, {"status": "D", "path": "x.py"}]),
])
def test_malformed_or_conflicting_manifest_fails(scoped, mutate):
    _, _, _, run = scoped
    value = manifest([])
    mutate(value)
    assert run({"workspace": value})["errors"]


def test_source_lock_identity_mismatch_fails(scoped):
    _, config, write, run = scoped
    config["repositories"][1]["source_lock_key"] = "workspace"
    write("sources.lock.json", json.dumps({"workspace": {"repository": URL, "revision": HEAD}}))
    assert "source lock" in " ".join(run({"workspace": manifest([])})["errors"])


def test_recorded_exclusions_and_declared_provenance(scoped):
    _, config, write, run = scoped
    config["repositories"][1]["exclusions"] = [{"patterns": ["tests/**"], "reason": "test fixture", "source": "upstream tests"}]
    write("vendor/workspace/tests/huge.py", "bad syntax" * 500)
    report = run({"workspace": manifest([{"status": "M", "path": "tests/huge.py"}])})
    assert not report["errors"] and not report["files"]
    assert report["excluded"][0]["reason"] == "test fixture"
    assert report["scope"][1]["provenance"] == "manifest-declared"
    assert report["coverage"]["logical"] == ["python"]


def test_symlink_escape_rejected(scoped, tmp_path):
    root, _, _, run = scoped
    external = tmp_path / "outside.py"
    external.write_text("x=1")
    try:
        (root / "vendor/workspace/escape.py").symlink_to(external)
    except OSError:
        pytest.skip("symlink creation unavailable")
    errors = run({"workspace": manifest([{"status": "M", "path": "escape.py"}])})["errors"]
    assert "escape" in " ".join(errors)


def test_unreadable_maintained_directory_blocks_inventory(scoped, monkeypatch):
    from tools.quality import scope

    _, _, _, run = scoped

    def unreadable_walk(root, *, followlinks=False, onerror=None):
        yield str(root), ["hidden"], []
        if onerror is not None:
            onerror(PermissionError(13, "Permission denied", str(root / "hidden")))

    monkeypatch.setattr(scope.os, "walk", unreadable_walk)
    errors = run({"workspace": manifest([])})["errors"]
    assert errors and "qopenbb" in errors[0] and "hidden" in errors[0]
    assert "Permission denied" in errors[0]
