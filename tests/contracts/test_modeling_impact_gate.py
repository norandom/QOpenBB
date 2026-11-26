import json

import pytest
from qopenbb_ci import financial_impact as impact


def test_wrong_checkout_blocks_without_running_checks(tmp_path, monkeypatch):
    head = impact._revision("HEAD")
    monkeypatch.setattr(impact, "_exercise", lambda *_: pytest.fail("wrong checkout"))
    report = impact.evaluate(head, head + "^", tmp_path / "report.json")
    assert report["decision"] == "blocked"
    assert "candidate checkout" in report["error"]


@pytest.mark.parametrize(
    ("gaps", "passed", "compatibility", "decision"),
    [
        ([], True, "compatible", "passed"),
        (["unknown model"], True, "compatible", "blocked"),
        ([], False, "compatible", "blocked"),
        ([], True, "blocked", "blocked"),
    ],
)
def test_integration_preserves_selection_and_evidence(
    monkeypatch, tmp_path, gaps, passed, compatibility, decision
):
    selection = {
        "changed_ids": ["operation:evaluate"],
        "criteria": ["5.2"],
        "selectors": ["test"],
        "gaps": gaps,
    }
    monkeypatch.setattr(impact, "_verify_checkout", lambda _: None)
    monkeypatch.setattr(impact, "_verify_forks", lambda _: None)
    monkeypatch.setattr(impact, "select", lambda *_: selection)

    def exercise(head, selectors, output, report):
        assert selectors == ["test"]
        report["checks"] = {"passed": passed, "results": ["required case"]}
        report["compatibility"] = {
            "decision": compatibility,
            "candidate_revision": head,
        }

    monkeypatch.setattr(impact, "_exercise", exercise)
    output = tmp_path / "report.json"
    status = impact.main(["--base", "HEAD^", "--output", str(output)])
    report = json.loads(output.read_bytes())
    assert report["decision"] == decision
    assert status == int(decision == "blocked")
    assert report["selection"] == selection
    assert report["compatibility"]["candidate_revision"] == report["head"]
    assert report["locked_sources"]["workspace"]["revision"]
    assert len(report["source_lock_sha256"]) == 64


def test_failed_export_still_exercises_broader_selection(monkeypatch, tmp_path):
    observed = []
    monkeypatch.setattr(impact, "bundle_main", lambda _: 1)

    def checks(selectors, root):
        observed.extend(selectors)
        return {"passed": False, "results": []}

    monkeypatch.setattr(impact, "run_checks", checks)
    report = {}
    impact._exercise(
        impact._revision("HEAD"), ["tests/factors"], tmp_path / "report.json", report
    )
    assert set(observed) == {"tests/factors", impact.EXERCISE}
    assert report["error"] == "could not export selected candidate"
    assert report["compatibility"]["decision"] == "blocked"


def test_different_fork_checkout_blocks_even_when_selected_checks_pass(
    monkeypatch, tmp_path
):
    monkeypatch.setattr(impact, "_verify_checkout", lambda _: None)

    def wrong_revision(*_):
        raise ValueError("source HEAD differs from lock")

    monkeypatch.setattr(impact, "identity", wrong_revision)
    monkeypatch.setattr(
        impact,
        "select",
        lambda *_: {"changed_ids": ["widget:saved"], "selectors": ["test"], "gaps": []},
    )
    monkeypatch.setattr(
        impact,
        "_exercise",
        lambda _h, _s, _o, report: report.update(
            checks={"passed": True}, compatibility={"decision": "compatible"}
        ),
    )
    report = impact.evaluate("HEAD^", "HEAD", tmp_path / "report.json")
    assert report["decision"] == "blocked"
    assert "source HEAD differs" in report["error"]
    assert report["checks"]["passed"]
