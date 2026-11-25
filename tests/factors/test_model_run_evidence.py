from datetime import UTC, datetime

import pytest
from pydantic import ValidationError
from qopenbb_data.modeling.contracts import (
    CheckOutcome,
    ModelRun,
    OutputResult,
    VerificationEvidence,
)


@pytest.fixture
def run_fields():
    timestamp = datetime(2024, 1, 2, 20, tzinfo=UTC)
    row = {
        "entity_id": "ETF", "metric_id": "close", "observation_date": "2024-01-02",
        "context": {"unit": "price", "currency": "USD", "quantity": "stock", "basis": "split_adjusted"},
        "value": "10", "category": "provider", "published_at": timestamp,
    }
    tables = tuple(
        {"table_id": table, "grain": "one close per session", "keys": ("observation_date",), "nullable": False,
             "rows": (row | {"record_id": table + "-close"},)}
        for table in ("prices", "benchmark")
    )
    definitions = tuple(
        {"output_id": output_id, "semantic_definition": output_id, "unit": "price",
             "required_output_ids": dependencies}
        for output_id, dependencies in (
            ("price", ()), ("spread", ("price",)), ("adjusted", ("spread",)), ("independent", ()),
        )
    )
    outputs = [
        {"output_id": definition["output_id"], "semantic_definition": definition["semantic_definition"],
             "unit": "price", "value": "10", "status": "unverified", "reason": "Awaiting reference"}
        for definition in definitions
    ]
    outputs[0].update(trace_ids=("trace-1",), check_ids=("coverage",))
    return {
        "run_id": "run-1", "owner_id": "analyst", "created_at": timestamp,
        "descriptor": {
            "model_id": "close", "method_version": "1", "input_schema_id": "prices",
            "output_schema_id": "close", "rule_set_version": "1", "reference_version": "1",
            "entity_types": ("fund",), "period_types": ("daily",),
            "input_ids": ("prices", "benchmark", "missing"),
            "rules": tuple(
                {"rule_id": rule_id, "version": "1", "stage": "postcondition",
                     "severity": "blocking", "exception_policy_version": "1"}
                for rule_id in ("coverage", "reconciliation")
            ),
            "outputs": definitions,
        },
        "inputs": {
            "schema_id": "prices", "tables": tables,
            "provenance": {"origin": "user_supplied", "source": "fixture", "query": (), "retrieved_at": timestamp},
        },
        "assumptions": {"version": "1", "effective_date": "2024-01-02"},
        "outputs": outputs,
        "trace": [{
            "trace_id": "trace-1", "formula_id": "identity", "formula_version": "1", "expression": "close",
            "input_ids": ("prices",), "source_record_ids": ("prices-close",),
            "output_id": "price", "check_ids": ("coverage",),
        }],
        "checks": [{
            "rule_id": "coverage", "rule_version": "1", "severity": "blocking", "status": "pass",
            "input_ids": ("prices",), "output_ids": ("price",), "observed": "One close",
        }],
    }


def verify_price(fields):
    run = ModelRun.model_validate(fields)
    fields["outputs"][0].update(status="verified", reason=None)
    fields["verification"] = [VerificationEvidence(
        output_id="price", reference_version="1", status="match",
        explanation="Independent comparison of the daily close",
        input_fingerprint=run.inputs.fingerprint(),
        assumption_fingerprint=run.assumptions.fingerprint(),
        descriptor_fingerprint=run.descriptor.fingerprint(),
        output_fingerprint=VerificationEvidence.fingerprint_output(
            OutputResult.model_validate(fields["outputs"][0]), run.trace, run.checks,
        ),
    )]


def test_matching_evidence_verifies_and_round_trips(run_fields):
    verify_price(run_fields)
    run = ModelRun.model_validate(run_fields)
    assert run.outputs[0].status == "verified"
    assert ModelRun.model_validate_json(run.model_dump_json()) == run


@pytest.mark.parametrize(("section", "field", "value"), [
    ("trace", "expression", "close * 2"),
    ("checks", "observed", "Two closes"),
])
def test_changing_referenced_evidence_invalidates_match(run_fields, section, field, value):
    verify_price(run_fields)
    run_fields[section][0][field] = value
    with pytest.raises(ValidationError, match="verification fingerprints"):
        ModelRun.model_validate(run_fields)


def fail_coverage(fields):
    fields["checks"][0].update(status="fail", explanation="Close coverage below threshold")


def withhold(output):
    output.update(value=None, status="withheld", reason="Blocking coverage failure")


def authorize_coverage(fields):
    fields["exceptions"] = [{
        "exception_id": "waiver", "rule_id": "coverage", "rule_version": "1", "author": "reviewer",
        "output_ids": ("price",), "rationale": "Approve limited use", "policy_version": "1",
    }]
    fields["outputs"][0]["exception_ids"] = ("waiver",)


def test_blocking_failure_withholds_value_and_transitive_dependents(run_fields):
    fail_coverage(run_fields)
    with pytest.raises(ValidationError, match="blocking failure requires a withheld output"):
        ModelRun.model_validate(run_fields)
    for output in run_fields["outputs"][:2]:
        withhold(output)
    with pytest.raises(ValidationError, match="withheld dependency"):
        ModelRun.model_validate(run_fields)
    withhold(run_fields["outputs"][2])
    run = ModelRun.model_validate(run_fields)
    assert [output.value for output in run.outputs[:3]] == [None, None, None]
    assert run.outputs[3].status == "unverified"


def test_withholding_propagates_through_an_omitted_intermediate(run_fields):
    fail_coverage(run_fields)
    withhold(run_fields["outputs"][0])
    del run_fields["outputs"][1]
    with pytest.raises(ValidationError, match="withheld dependency"):
        ModelRun.model_validate(run_fields)


def test_exception_preserves_the_failure_and_permits_unverified_use(run_fields):
    fail_coverage(run_fields)
    authorize_coverage(run_fields)
    run = ModelRun.model_validate(run_fields)
    assert run.outputs[0].value is not None
    assert run.outputs[0].status == "unverified"
    assert run.checks[0].status == "fail"


@pytest.mark.parametrize("other_output", ["price", "independent"])
def test_exception_cannot_cover_another_rule_or_output(run_fields, other_output):
    fail_coverage(run_fields)
    authorize_coverage(run_fields)
    if other_output == "price":
        run_fields["checks"].append(run_fields["checks"][0] | {"rule_id": "reconciliation"})
        run_fields["outputs"][0]["check_ids"] += ("reconciliation",)
    else:
        run_fields["checks"][0]["output_ids"] += ("independent",)
        run_fields["outputs"][3]["check_ids"] = ("coverage",)
    with pytest.raises(ValidationError, match="blocking failure requires a withheld output"):
        ModelRun.model_validate(run_fields)


@pytest.mark.parametrize("cited_tables", [("prices",), ()])
def test_trace_record_must_come_from_cited_table(run_fields, cited_tables):
    run_fields["trace"][0].update(
        input_ids=cited_tables, source_record_ids=("benchmark-close",),
    )
    with pytest.raises(ValidationError, match="trace source records"):
        ModelRun.model_validate(run_fields)


def test_trace_check_must_apply_to_its_output(run_fields):
    run_fields["checks"].append(run_fields["checks"][0] | {
        "rule_id": "reconciliation", "output_ids": ("independent",),
    })
    run_fields["outputs"][3]["check_ids"] = ("reconciliation",)
    run_fields["trace"][0]["check_ids"] = ("reconciliation",)
    with pytest.raises(ValidationError, match="trace checks"):
        ModelRun.model_validate(run_fields)


@pytest.mark.parametrize(("field", "references", "message"), [
    ("trace_ids", (), "trace entries"),
    ("trace_ids", ("trace-unknown",), "trace entries"),
    ("check_ids", (), "affecting checks"),
    ("check_ids", ("coverage", "reconciliation"), "affecting checks"),
])
def test_output_references_must_match_backlinks(run_fields, field, references, message):
    run_fields["trace"][0]["check_ids"] = ()
    run_fields["outputs"][0][field] = references
    with pytest.raises(ValidationError, match=message):
        ModelRun.model_validate(run_fields)


def test_evaluated_required_check_must_name_the_dependent_output(run_fields):
    run_fields["descriptor"]["outputs"][1]["required_check_ids"] = ("coverage",)
    with pytest.raises(ValidationError, match="required affecting checks"):
        ModelRun.model_validate(run_fields)


def test_missing_input_can_be_named_by_a_nonpassing_check(run_fields):
    check = run_fields["checks"][0]
    check["input_ids"] = ("missing",)
    with pytest.raises(ValidationError, match="passing check snapshot inputs"):
        ModelRun.model_validate(run_fields)
    check.update(status="unknown", explanation="No supplied input")
    run = ModelRun.model_validate(run_fields)
    assert run.checks[0] == CheckOutcome.model_validate(check)
