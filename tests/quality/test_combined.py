"""Combined language gate fixtures use explicit fork scope without Git metadata."""

import json
import subprocess
import sys

from test_scope import manifest, scoped


def prepare(scoped, own=None, fork=None):
    root, config, write, run = scoped
    for index, files in enumerate([own or {}, fork or {}]):
        config["repositories"][index]["owners"][0]["files"] = list(files)
        prefix = "" if index == 0 else "vendor/workspace/"
        for path, source in files.items():
            write(prefix + path, source)
    run()
    return root, config, write


def test_default_combines_python_and_real_tsx_from_a_different_cwd(scoped, monkeypatch):
    from tools.quality.complexity import inventory

    root, _, _ = prepare(scoped, {"src/value.py": "x=1\n"},
                         {"view.tsx": "const View = () => <div>{items.map(x => <span/>)}</div>;"})
    monkeypatch.chdir(root.parent)
    report = inventory(root, changes={"workspace": manifest([{"status": "M", "path": "view.tsx"}])})
    assert not report["errors"] and not report["violations"]
    assert report["coverage"]["mode"] == "combined"
    assert report["coverage"]["logical"] == ["python", "javascript", "typescript"]
    assert report["coverage"]["combined_acceptance"] == "passed"
    assert report["coverage"]["parsers"]["typescript"] == "6.0.3"
    assert report["coverage"]["parsers"]["node"] == "24.22.1"
    assert [(file["repository"], file["path"], file["logical"]) for file in report["files"]] == [
        ("qopenbb", "src/value.py", 1), ("workspace", "view.tsx", 3)]


def test_combined_cli_fails_oversized_whole_fork_and_missing_scope(scoped):
    from tools.quality.complexity import ROOT

    root, _, _ = prepare(scoped, fork={"big.ts": "a();" * 301 + "\nfunction f(){" + "a();" * 51 + "}"})
    scope_file = root.parent / "changes.json"
    scope_file.write_text(json.dumps(manifest([{"status": "M", "path": "big.ts"}])))
    command = [sys.executable, "-m", "tools.quality.complexity", "--root", str(root), "--check"]
    missing = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
    assert missing.returncode == 2 and json.loads(missing.stdout)["errors"]
    result = subprocess.run([*command, "--changes", f"workspace={scope_file}"],
                            cwd=ROOT, capture_output=True, text=True)
    report = json.loads(result.stdout)
    assert result.returncode == 1 and not report["errors"]
    assert report["coverage"]["combined_acceptance"] == "failed"
    assert {item["metric"] for item in report["violations"]} == {"logical", "function"}
    assert report["files"][0]["logical"] == 353
    assert report["files"][0]["functions"][0]["logical"] == 51


def test_javascript_parse_failures_block_combined_certification(scoped):
    from tools.quality.complexity import inventory

    root, _, _ = prepare(scoped, {"src/broken.jsx": "const bad = <div>"})
    report = inventory(root, changes={"workspace": manifest([])})
    assert report["errors"] and "broken.jsx" in " ".join(report["errors"])
    assert report["coverage"]["combined_acceptance"] == "unverified"


def test_python_only_mode_is_explicitly_partial(scoped):
    from tools.quality.complexity import inventory

    root, _, _ = prepare(scoped, {"src/broken.ts": "function broken( {"})
    report = inventory(root, changes={"workspace": manifest([])}, python_only=True)
    assert not report["errors"]
    assert report["coverage"]["mode"] == "python-only"
    assert report["coverage"]["logical"] == ["python"]
    assert report["coverage"]["combined_acceptance"].startswith("unverified")
