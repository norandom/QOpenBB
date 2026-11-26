"""Verify financial impact evidence against real pytest sessions."""

from pathlib import Path

import pytest
from qopenbb_ci.financial_impact_run import run_checks


def _write(root: Path, source: str) -> str:
    filename = "test_checks.py"
    (root / filename).write_text(source, encoding="utf-8")
    return filename


def test_exact_parametrized_evidence(tmp_path):
    filename = _write(
        tmp_path,
        "import pytest\n"
        "@pytest.mark.parametrize('value', [1, 2])\n"
        "def test_value(value): assert value\n"
        "def test_unrelated(): assert False\n",
    )
    selector = f"{filename}::test_value"
    exact = f"{selector}[2]"
    result = run_checks([selector, exact], tmp_path)
    assert result["passed"] is True
    assert [entry["selector"] for entry in result["results"]] == [selector, exact]
    assert [set(entry["nodes"]) for entry in result["results"]] == [
        {f"{selector}[1]", exact},
        {exact},
    ]
    assert result["results"][1]["nodes"][exact] == {
        "outcome": "passed",
        "phases": {"setup": "passed", "call": "passed", "teardown": "passed"},
    }


@pytest.mark.parametrize(
    ("body", "outcome"),
    [
        ("pytest.skip('unavailable')", "skipped"),
        ("pytest.xfail('expected failure')", "xfailed"),
        ("assert False", "failed"),
    ],
)
def test_one_nonpassing_node_fails_a_partly_passing_file(tmp_path, body, outcome):
    filename = _write(
        tmp_path,
        "import pytest\ndef test_good(): pass\n"
        f"def test_other(): {body}\n",
    )
    result = run_checks([filename], tmp_path)
    assert result["passed"] is False
    nodes = result["results"][0]["nodes"]
    assert nodes[f"{filename}::test_good"]["outcome"] == "passed"
    assert nodes[f"{filename}::test_other"]["outcome"] == outcome


def test_xpass_and_teardown_error_fail(tmp_path):
    filename = _write(
        tmp_path,
        "import pytest\n"
        "@pytest.mark.xfail(reason='known issue')\n"
        "def test_xpass(): pass\n"
        "@pytest.fixture\ndef resource():\n    yield\n    assert False\n"
        "def test_teardown(resource): pass\n",
    )
    result = run_checks([filename], tmp_path)
    assert result["passed"] is False
    nodes = result["results"][0]["nodes"]
    assert nodes[f"{filename}::test_xpass"]["outcome"] == "xpassed"
    assert nodes[f"{filename}::test_teardown"]["phases"]["teardown"] == "failed"


def test_deselected_node_fails_even_when_pytest_exits_zero(tmp_path):
    filename = _write(tmp_path, "def test_good(): pass\ndef test_other(): pass\n")
    (tmp_path / "conftest.py").write_text(
        "def pytest_configure(config):\n    config.option.keyword = 'test_good'\n",
        encoding="utf-8",
    )
    result = run_checks([filename], tmp_path)
    assert result["passed"] is False
    entry = result["results"][0]
    assert entry["exit_code"] == 0
    assert entry["nodes"][f"{filename}::test_other"]["outcome"] == "deselected"


def test_unevaluated_node_fails_even_when_pytest_exits_zero(tmp_path):
    filename = _write(tmp_path, "def test_good(): pass\ndef test_other(): pass\n")
    (tmp_path / "conftest.py").write_text(
        "def pytest_runtestloop(session):\n"
        "    session.config.hook.pytest_runtest_protocol(item=session.items[0], nextitem=None)\n"
        "    return True\n",
        encoding="utf-8",
    )
    result = run_checks([filename], tmp_path)
    assert result["passed"] is False
    entry = result["results"][0]
    assert entry["exit_code"] == 0
    assert entry["nodes"][f"{filename}::test_other"]["outcome"] == "unevaluated"


def test_setup_only_produces_partial_evidence(tmp_path):
    filename = _write(tmp_path, "def test_good(): pass\n")
    (tmp_path / "conftest.py").write_text(
        "def pytest_configure(config):\n    config.option.setuponly = True\n",
        encoding="utf-8",
    )
    result = run_checks([filename], tmp_path)
    assert result["passed"] is False
    entry = result["results"][0]
    assert entry["exit_code"] == 0
    assert entry["nodes"][f"{filename}::test_good"] == {
        "outcome": "partial",
        "phases": {"setup": "passed", "teardown": "passed"},
    }


def test_last_failed_filter_cannot_verify_a_whole_directory(tmp_path, monkeypatch):
    filename = _write(tmp_path, "def test_good(): pass\n")
    (tmp_path / "test_other.py").write_text("def test_other(): assert False\n", encoding="utf-8")
    cache = tmp_path / ".pytest_cache/v/cache"
    cache.mkdir(parents=True)
    (cache / "lastfailed").write_text(f'{{"{filename}::test_good": true}}', encoding="utf-8")
    monkeypatch.setenv("PYTEST_ADDOPTS", "--lf")
    result = run_checks(["."], tmp_path)
    assert result["passed"] is False
    assert result["results"][0]["nodes"]["test_other.py::test_other"]["outcome"] == "failed"


@pytest.mark.parametrize("source", ["environment", "configuration", "explicit_plugin", "autoload"])
def test_collection_cannot_hide_a_failing_file(tmp_path, monkeypatch, source):
    filename = _write(tmp_path, "def test_good(): pass\n")
    (tmp_path / "test_red.py").write_text("def test_red(): assert False\n", encoding="utf-8")
    if source == "environment":
        monkeypatch.setenv("PYTEST_ADDOPTS", "--ignore=test_red.py")
    elif source == "configuration":
        (tmp_path / "pytest.ini").write_text("[pytest]\naddopts = --ignore=test_red.py\n")
    else:
        (tmp_path / "omit_red.py").write_text(
            "def pytest_ignore_collect(collection_path):\n"
            "    return collection_path.name == 'test_red.py' or None\n",
            encoding="utf-8",
        )
        monkeypatch.setenv("PYTHONPATH", str(tmp_path))
        if source == "explicit_plugin":
            monkeypatch.setenv("PYTEST_PLUGINS", "omit_red")
        else:
            monkeypatch.delenv("PYTEST_DISABLE_PLUGIN_AUTOLOAD", raising=False)
            metadata = tmp_path / "omit_red-1.0.dist-info"
            metadata.mkdir()
            (metadata / "entry_points.txt").write_text("[pytest11]\nomit_red = omit_red\n")
    result = run_checks(["."], tmp_path)
    assert result["passed"] is False
    entry = result["results"][0]
    assert entry["exit_code"] == 1
    assert entry["nodes"][f"{filename}::test_good"]["outcome"] == "passed"
    assert entry["nodes"]["test_red.py::test_red"]["outcome"] == "failed"


def test_missing_and_option_like_selectors_fail_separately(tmp_path):
    filename = _write(tmp_path, "def test_good(): pass\n")
    selectors = [f"{filename}::test_missing", "--collect-only", filename]
    result = run_checks(selectors, tmp_path)
    assert result["passed"] is False
    assert [entry["passed"] for entry in result["results"]] == [False, False, True]
    assert not result["results"][0]["nodes"]
    assert run_checks([], tmp_path) == {"passed": False, "results": []}


def test_selector_is_passed_as_a_literal(tmp_path):
    filename = "test_checks with space; touch side_effect.py"
    (tmp_path / filename).write_text("def test_good(): pass\n", encoding="utf-8")
    result = run_checks([f"{filename}::test_good"], tmp_path)
    assert result["passed"] is True
    assert not (tmp_path / "side_effect.py").exists()


def test_collection_skip_fails_a_partly_passing_directory(tmp_path):
    _write(tmp_path, "def test_pass(): pass\n")
    (tmp_path / "test_skipped.py").write_text(
        "import pytest\npytest.skip('unavailable', allow_module_level=True)\n",
        encoding="utf-8",
    )
    result = run_checks(["."], tmp_path)
    assert result["passed"] is False
    assert result["results"][0]["collection"] == {"test_skipped.py": "skipped"}


def test_pipeline_fallback_never_runs_live_checks(tmp_path, monkeypatch):
    root = Path(__file__).resolve().parents[2]
    config = tmp_path / "pipeline" / "pyproject.toml"
    config.parent.mkdir()
    config.write_bytes((root / "pipeline" / "pyproject.toml").read_bytes())
    monkeypatch.setenv("PYTEST_ADDOPTS", "-m live")
    factors = tmp_path / "tests" / "factors"
    factors.mkdir(parents=True)
    filename = _write(
        factors,
        "from pathlib import Path\n"
        "import pytest\n"
        "def test_offline(): pass\n"
        "@pytest.mark.live\n"
        "def test_live(): Path('provider-called').touch()\n",
    )
    prefix = f"tests/factors/{filename}"
    exact_live = f"{prefix}::test_live"
    result = run_checks(["tests/factors", exact_live], tmp_path)
    assert result["passed"] is False
    fallback, exact = result["results"]
    assert fallback["exit_code"] == 0
    assert fallback["passed"] is False
    assert fallback["nodes"][f"{prefix}::test_offline"]["outcome"] == "passed"
    assert fallback["nodes"][exact_live] == {"outcome": "deselected", "phases": {}}
    assert exact["passed"] is False
    assert exact["nodes"][exact_live] == {"outcome": "deselected", "phases": {}}
    assert not (tmp_path / "provider-called").exists()
