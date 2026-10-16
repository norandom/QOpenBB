"""Reviewed exceptions are exact, bounded and tied to the measured fork revision."""

import copy
import json
from datetime import date, timedelta

import pytest

from test_scope import HEAD, manifest, scoped
from test_combined import prepare


def exception(metric="logical", baseline=301):
    return {"repository": "workspace", "path": "big.ts", "metric": metric,
            "baseline": baseline, "revision": HEAD, "rationale": "Cohesive extraction scheduled in owning task",
            "review": ".kiro/specs/openbb-self-service/design-review.md#measured-extraction",
            "expires_on": (date.today() + timedelta(days=7)).isoformat()}


def run_with(scoped, exceptions, source="a();" * 301):
    from tools.quality.complexity import inventory

    root, config, write = prepare(scoped, fork={"big.ts": source})
    config["exceptions"] = exceptions
    write(".kiro/complexity-budgets.json", json.dumps(config))
    return inventory(root, changes={"workspace": manifest([{"status": "M", "path": "big.ts"}])})


def test_reviewed_exact_baseline_exception_is_reported(scoped):
    report = run_with(scoped, [exception()])
    assert not report["errors"] and not report["violations"]
    assert report["coverage"]["combined_acceptance"] == "passed"
    assert report["exceptions"][0]["actual"] == 301
    assert report["exceptions"][0]["review"].endswith("#measured-extraction")


@pytest.mark.parametrize("mutate", [
    lambda e: e.update(path="*.ts"),
    lambda e: e.update(repository="unknown"),
    lambda e: e.update(metric="any"),
    lambda e: e.update(baseline=True),
    lambda e: e.update(baseline=300),
    lambda e: e.update(revision="a" * 40),
    lambda e: e.update(revision="HEAD"),
    lambda e: e.update(rationale=""),
    lambda e: e.update(review=""),
    lambda e: e.update(expires_on="2000-01-01"),
    lambda e: e.update(expires_on="never"),
    lambda e: e.pop("revision"),
])
def test_invalid_or_stale_exception_cannot_suppress_violation(scoped, mutate):
    entry = exception()
    mutate(entry)
    report = run_with(scoped, [entry])
    assert report["errors"] and report["violations"]
    assert report["coverage"]["combined_acceptance"] == "unverified"


def test_exception_does_not_allow_growth_above_reviewed_baseline(scoped):
    report = run_with(scoped, [exception()], "a();" * 302)
    assert not report["errors"]
    assert report["violations"][0]["actual"] == 302
    assert not report["exceptions"]


def test_function_exception_targets_one_exact_callable(scoped):
    entry = exception("function", 51)
    entry["function"] = {"name": "f", "line": 1, "column": 1}
    report = run_with(scoped, [entry], "function f(){" + "a();" * 51 + "}function g(){" + "a();" * 51 + "}")
    assert not report["errors"]
    assert [row["name"] for row in report["violations"]] == ["g"]
    assert report["exceptions"][0]["name"] == "f"


def test_duplicate_exception_keys_fail_closed(scoped):
    entry = exception()
    report = run_with(scoped, [entry, copy.deepcopy(entry)])
    assert report["errors"] and report["violations"]
