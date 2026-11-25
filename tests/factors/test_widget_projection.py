import json
from decimal import Decimal
from urllib.parse import urljoin

import pytest
from qopenbb_data.modeling.contracts import ModelRun
from qopenbb_data.modeling.service.run_store import RunNotFound
from test_model_run_evidence import (
    authorize_coverage,
    fail_coverage,
    verify_price,
    withhold,
)
from test_model_run_evidence import run_fields as run_fields_fixture

run_fields = run_fields_fixture


@pytest.fixture
def project():
    from qopenbb_data.modeling.service.widget_projection import project_output

    return project_output


@pytest.mark.parametrize(
    ("kind", "value", "display_text", "numeric"),
    [
        ("decimal", "10.125", "10.125", Decimal("10.125")),
        ("decimal", "-10.125", "-10.125", Decimal("-10.125")),
        ("decimal", "-0.1", "-0.1", None),
        ("integer", -(2**53 + 1), str(-(2**53 + 1)), None),
        ("decimal", "0.1", "0.1", None),
        ("decimal", "12345678901234.0025", "12345678901234.0025", None),
        ("decimal", "0", "0", Decimal(0)),
        ("integer", 2**60, str(2**60), Decimal(2**60)),
        ("integer", 2**53 + 1, str(2**53 + 1), None),
        ("boolean", False, "false", None),
        ("date", "2024-01-02", "2024-01-02", None),
        ("text", "001", "001", None),
    ],
)
def test_display_uses_saved_value_and_exact_binary64(
    run_fields, project, kind, value, display_text, numeric
):
    run_fields["descriptor"]["outputs"][0]["value_type"] = kind
    run_fields["outputs"][0].update(value=value, value_type=kind)
    run = ModelRun.model_validate(run_fields)
    envelope = json.loads(json.dumps(project(run, "price"), allow_nan=False))
    row = envelope["results"][0]
    assert row["value"] == run.outputs[0].model_dump(mode="json")["value"]
    assert row["display_text"] == display_text
    assert row["display_numeric"] == {
        "transform": "exact_binary64",
        "max_absolute_error": "0",
    }
    if numeric is None:
        assert row["display_value"] is None
    else:
        assert type(row["display_value"]) in {float, int}
        assert Decimal(row["display_value"]) == numeric


@pytest.mark.parametrize(
    ("expected_id", "freshness"),
    [(None, "saved"), ("run-1", "matched"), ("another-run", "stale"), ("", "stale")],
)
def test_freshness_preserves_saved_status_and_old_envelope(
    run_fields, project, expected_id, freshness
):
    verify_price(run_fields)
    run = ModelRun.model_validate(run_fields)
    saved = run.model_dump(mode="json")
    envelope = project(run, "price", expected_run_id=expected_id)
    row = envelope["results"][0]
    assert row["freshness"] == freshness
    assert row["status"] == "verified"
    assert envelope["run_id"] == saved["run_id"]
    assert {key: row[key] for key in saved["outputs"][0]} == saved["outputs"][0]
    for field in ("checks", "trace", "verification"):
        assert envelope[field] == saved[field]
    assert envelope["exceptions"] == []
    assert envelope["run_detail_href"] == "runs/run-1"
    assert row["run_detail_href"] == envelope["run_detail_href"]
    assert row["check_explanations"] is None
    assert "owner_id" not in envelope
    assert "another-run" not in json.dumps(envelope)


def test_detail_href_remains_inside_modeling_base(run_fields, project):
    run_fields["run_id"] = "https://caller.invalid/../?data=#"
    run = ModelRun.model_validate(run_fields)
    detail = project(run, "price")["run_detail_href"]
    base = "https://workspace.invalid/modeling/v1/"
    assert (
        urljoin(base, detail)
        == base + "runs/https%3A%2F%2Fcaller.invalid%2F..%2F%3Fdata%3D%23"
    )


def test_withheld_output_preserves_explanation_and_nulls(run_fields, project):
    fail_coverage(run_fields)
    for output in run_fields["outputs"][:3]:
        withhold(output)
    run = ModelRun.model_validate(run_fields)
    envelope = project(run, "price", expected_run_id="old-run")
    row = envelope["results"][0]
    assert (row["status"], row["freshness"]) == ("withheld", "stale")
    assert row["value"] is row["display_value"] is row["display_text"] is None
    assert row["reason"] == "Blocking coverage failure"
    assert envelope["checks"] == [run.checks[0].model_dump(mode="json")]
    assert row["run_detail_href"] == envelope["run_detail_href"] == "runs/run-1"
    assert row["check_explanations"] == "coverage: Close coverage below threshold"


def test_warning_explanations_are_joined_in_selected_check_order(run_fields, project):
    for rule in run_fields["descriptor"]["rules"]:
        rule["severity"] = "warning"
    first = run_fields["checks"][0]
    first.update(
        severity="warning", status="fail", explanation="Close coverage is thin"
    )
    run_fields["checks"].append(
        first | {"rule_id": "reconciliation", "explanation": "Inputs did not reconcile"}
    )
    run_fields["outputs"][0]["check_ids"] = ("coverage", "reconciliation")
    run = ModelRun.model_validate(run_fields)
    envelope = json.loads(json.dumps(project(run, "price"), allow_nan=False))
    row = envelope["results"][0]
    assert envelope["checks"] == [check.model_dump(mode="json") for check in run.checks]
    assert row["status"] == "unverified"
    assert row["display_value"] == 10
    assert row["run_detail_href"] == envelope["run_detail_href"] == "runs/run-1"
    assert row["check_explanations"] == (
        "coverage: Close coverage is thin\nreconciliation: Inputs did not reconcile"
    )
    assert project(run, "independent")["results"][0]["check_explanations"] is None


def test_projection_scopes_policy_exceptions_and_evidence(run_fields, project):
    fail_coverage(run_fields)
    authorize_coverage(run_fields)
    run = ModelRun.model_validate(run_fields)
    selected = project(run, "price")
    assert selected["results"][0]["status"] == "unverified"
    assert selected["checks"][0]["status"] == "fail"
    assert selected["exceptions"] == [run.exceptions[0].model_dump(mode="json")]
    unrelated = project(run, "independent")
    for field in ("checks", "trace", "verification", "exceptions"):
        assert unrelated[field] == []


def test_absent_output_raises_saved_run_not_found(run_fields, project):
    run = ModelRun.model_validate(run_fields)
    with pytest.raises(RunNotFound):
        project(run, "absent")
