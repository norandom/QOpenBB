import os
from datetime import UTC, date, datetime
from decimal import Decimal
from functools import partial
from pathlib import Path
from threading import Event
from time import monotonic, sleep

import pytest
from pydantic import ValidationError
from qopenbb_data.modeling.contracts.checks import (
    CheckOutcome,
    PolicyException,
    RuleDescriptor,
)
from qopenbb_data.modeling.contracts.descriptors import OutputDescriptor
from qopenbb_data.modeling.contracts.inputs import AssumptionSet, EvaluationCutoff
from qopenbb_data.modeling.contracts.trace import TraceEntry
from qopenbb_data.modeling.models.protocol import CandidateOutput, CandidateResult
from qopenbb_data.modeling.models.registry import ModelRegistry
from qopenbb_data.modeling.service.evaluation import EvaluationRequest
from qopenbb_data.modeling.service.execution import ExecutionError, ExecutionLimits
from qopenbb_data.modeling.service.orchestrator import MethodBinding, Orchestrator
from qopenbb_data.modeling.service.ports import AcquisitionRequest, Principal
from qopenbb_data.modeling.service.run_store import FileRunStore, RunNotFound
from qopenbb_data.modeling.validation.rules import Rule
from qopenbb_data.modeling.verification.reference import Reference
from test_model_registry import SuppliedValueFixture
from test_model_registry import inputs as registry_inputs

inputs = registry_inputs

DAY = date(2024, 1, 2)
NOW = datetime(2024, 1, 2, 16, tzinfo=UTC)
OWNER = Principal(subject="test-owner")
KEY = ("test-only-supplied-value", "1")
ASSUMPTIONS = AssumptionSet(version="1", effective_date=DAY)
ACQUISITION = {
    "dataset_id": "test-data",
    "cutoff": EvaluationCutoff(
        observation_date=DAY,
        decision_at=NOW,
        evaluated_at=NOW,
        session_timezone="UTC",
    ),
}


def dimensions(inputs, assumptions):
    return 1, 1


def expected(inputs, assumptions):
    return inputs.tables[0].rows[0].value


def mismatch(inputs, assumptions):
    return Decimal(1)


def slow_callback(marker, *args):
    marker.touch()
    sleep(8)
    raise AssertionError("the child should be stopped before this point")


def calculated(inputs, assumptions, eligible):
    assert eligible == ("value",)
    table = inputs.tables[0]
    row = table.rows[0]
    if (value := row.value) is None:
        return CandidateResult(
            outputs=(
                CandidateOutput(
                    output_id="value",
                    value=None,
                    reason="Observation value is missing",
                ),
            )
        )
    return CandidateResult(
        outputs=(CandidateOutput(output_id="value", value=value),),
        trace=(
            TraceEntry(
                trace_id="test-trace",
                output_id="value",
                formula_id="selection",
                formula_version="1",
                expression="Select the dated observation",
                input_ids=(table.table_id,),
                source_record_ids=(row.record_id,),
            ),
        ),
    )


def failed_precondition(context):
    return CheckOutcome(
        rule_id="quality",
        rule_version="1",
        severity="blocking",
        status="fail",
        output_ids=("blocked",),
        explanation="The financial precondition failed",
    )


class TestMethod(SuppliedValueFixture):
    __test__ = False

    def calculate(self, inputs, assumptions):
        return calculated(inputs, assumptions, ("value",))


class FakeSource:
    def __init__(self, snapshot):
        self.snapshot = snapshot
        self.calls = []

    def acquire(self, request, *, deadline=None, cancel=None):
        self.deadline = deadline
        self.cancel = cancel
        self.calls.append(request)
        provenance = self.snapshot.provenance.model_copy(
            update={
                "origin": "service_acquired",
                "acquisition_id": f"acquisition-{len(self.calls)}",
            }
        )
        return self.snapshot.model_copy(
            update={"provenance": provenance, "cutoff": request.cutoff}
        )


@pytest.fixture
def service(tmp_path, monkeypatch):
    paths = [str(Path(__file__).resolve().parent)]
    if current := os.environ.get("PYTHONPATH"):
        paths.append(current)
    monkeypatch.setenv("PYTHONPATH", os.pathsep.join(paths))

    def build(
        *,
        model=None,
        source=None,
        rules=(),
        reference=expected,
        calculate=None,
        timeout=5,
    ):
        reference = (
            Reference("1", {"value": reference}, {}) if reference is not None else None
        )
        return Orchestrator(
            ModelRegistry((model or TestMethod(),)),
            {
                KEY: MethodBinding(
                    ExecutionLimits(10, 1, 1, measure_dimensions=dimensions),
                    rules=rules,
                    reference=reference,
                    calculate=calculate,
                )
            },
            FileRunStore(tmp_path / "runs"),
            snapshot_source=source,
            timeout_seconds=timeout,
        )

    return build


def request(**kwargs):
    return EvaluationRequest(
        model_id=KEY[0], method_version=KEY[1], assumptions=ASSUMPTIONS, **kwargs
    )


def test_request_requires_exactly_one_input_path(inputs):
    for fields in (
        {},
        {"inputs": inputs, "acquisition": AcquisitionRequest(**ACQUISITION)},
    ):
        with pytest.raises(ValidationError):
            request(**fields)


def test_supplied_provenance_is_asserted_and_saved_with_ids(service, inputs):
    fields = inputs.model_dump()
    fields["provenance"].update(origin="service_acquired", acquisition_id="asserted-id")
    run = service().evaluate(request(inputs=type(inputs).model_validate(fields)), OWNER)
    assert run.outputs[0].status == "verified"
    assert run.trace[0].trace_id == "test-trace"
    assert run.trace[0].source_record_ids == ("present",)
    assert run.inputs.provenance.origin == "user_supplied"
    assert run.inputs.provenance.acquisition_id is None
    assert run.inputs.provenance.source == inputs.provenance.source
    assert run.inputs.tables == inputs.tables
    assert run.owner_id == OWNER.subject
    assert service().get(run.run_id, OWNER) == run
    with pytest.raises(RunNotFound):
        service().get(run.run_id, Principal(subject="different-owner"))


def test_refresh_preserves_actual_acquisitions_and_original_run(service, inputs):
    source = FakeSource(inputs)
    orchestrator = service(source=source)
    refresh = request(acquisition=AcquisitionRequest(**ACQUISITION))
    first = orchestrator.evaluate(refresh, OWNER)
    second = orchestrator.evaluate(refresh, OWNER)
    assert source.calls == [refresh.acquisition, refresh.acquisition]
    assert first.run_id != second.run_id
    assert first.inputs.provenance.acquisition_id == "acquisition-1"
    assert second.inputs.provenance.acquisition_id == "acquisition-2"
    assert (
        first.verification[0].input_fingerprint
        != second.verification[0].input_fingerprint
    )
    assert first.inputs.cutoff == refresh.acquisition.cutoff
    assert first.outputs[0].status == second.outputs[0].status == "verified"
    assert orchestrator.get(first.run_id, OWNER) == first
    assert source.calls == [refresh.acquisition, refresh.acquisition]


def test_rejects_invalid_identity_and_uninstalled_exact_method_before_acquiring(
    service, inputs
):
    source = FakeSource(inputs)
    orchestrator = service(source=source)
    refresh = request(acquisition=AcquisitionRequest(**ACQUISITION))
    for principal in (
        {"subject": OWNER.subject},
        Principal.model_construct(subject=""),
    ):
        with pytest.raises((TypeError, ValueError)):
            orchestrator.evaluate(refresh, principal)
    with pytest.raises(LookupError):
        orchestrator.evaluate(
            refresh.model_copy(update={"method_version": "latest"}), OWNER
        )
    assert source.calls == []


def test_registered_method_without_binding_cannot_acquire(tmp_path, inputs):
    source = FakeSource(inputs)
    orchestrator = Orchestrator(
        ModelRegistry((TestMethod(),)),
        {},
        FileRunStore(tmp_path),
        snapshot_source=source,
    )
    with pytest.raises(ExecutionError, match="missing_method_binding"):
        orchestrator.evaluate(
            request(acquisition=AcquisitionRequest(**ACQUISITION)), OWNER
        )
    assert source.calls == []


def test_rejects_reference_from_a_different_method_binding(tmp_path, inputs):
    source = FakeSource(inputs)
    binding = MethodBinding(
        ExecutionLimits(10, 1, 1, measure_dimensions=dimensions),
        reference=Reference("different-version", {"value": expected}, {}),
    )
    with pytest.raises(ValueError, match="reference version"):
        Orchestrator(
            ModelRegistry((TestMethod(),)),
            {KEY: binding},
            FileRunStore(tmp_path),
            snapshot_source=source,
        )
    assert source.calls == []


def partial_method():
    model = TestMethod()
    fields = model.describe().model_dump()
    fields["rules"] = (
        RuleDescriptor(
            rule_id="quality",
            version="1",
            stage="precondition",
            severity="blocking",
        ),
    )
    fields["outputs"] += (
        OutputDescriptor(
            output_id="blocked",
            semantic_definition="Blocked synthetic output",
            unit="amount",
            required_check_ids=("quality",),
        ),
    )
    model.descriptor = type(model.descriptor).model_validate(fields)
    return model


def test_blocked_output_never_reaches_calculator(service, inputs):
    rules = (Rule("quality", (), ("blocked",), failed_precondition),)
    run = service(model=partial_method(), rules=rules, calculate=calculated).evaluate(
        request(inputs=inputs),
        OWNER,
    )
    assert [output.status for output in run.outputs] == ["verified", "withheld"]
    assert [item.status for item in run.verification] == ["match", "unavailable"]
    assert run.checks[0].status == "fail"
    assert [entry.output_id for entry in run.trace] == ["value"]


def test_all_precondition_blocked_outputs_skip_calculation(service, inputs, tmp_path):
    model = partial_method()
    blocked = model.descriptor.outputs[-1]
    model.descriptor = model.descriptor.model_copy(update={"outputs": (blocked,)})
    marker = tmp_path / "calculation-started"
    rules = (Rule("quality", (), ("blocked",), failed_precondition),)
    run = service(
        model=model,
        rules=rules,
        reference=None,
        calculate=partial(slow_callback, marker),
    ).evaluate(request(inputs=inputs), OWNER)
    assert not marker.exists()
    assert run.outputs[0].status == "withheld"
    assert run.checks[0].status == "fail"
    assert run.trace == ()


def test_policy_exception_keeps_authenticated_author_and_original_failed_check(
    service, inputs
):
    model = partial_method()
    rule = model.descriptor.rules[0].model_copy(
        update={"exception_policy_version": "policy-1"}
    )
    model.descriptor = model.descriptor.model_copy(update={"rules": (rule,)})
    rules = (Rule("quality", (), ("blocked",), failed_precondition),)
    exception = PolicyException(
        exception_id="exception-1",
        rule_id="quality",
        rule_version="1",
        author=OWNER.subject,
        output_ids=("blocked",),
        rationale="Use as an open item only",
        policy_version="policy-1",
    )
    orchestrator = service(
        model=model, rules=rules, calculate=calculated_with_exception
    )
    run = orchestrator.evaluate(request(inputs=inputs, exceptions=(exception,)), OWNER)
    assert run.exceptions == (exception,)
    assert run.checks[0].status == "fail"
    assert run.outputs[1].status == "unverified"
    assert run.outputs[1].exception_ids == ("exception-1",)
    assert orchestrator.get(run.run_id, OWNER) == run


def calculated_with_exception(inputs, assumptions, eligible):
    assert eligible == ("value", "blocked")
    original = calculated(inputs, assumptions, ("value",))
    return CandidateResult(
        outputs=(
            *original.outputs,
            CandidateOutput(output_id="blocked", value=Decimal(1)),
        ),
        trace=original.trace,
    )


def test_missing_invalid_and_reference_mismatch_have_distinct_evidence(service, inputs):
    table = inputs.tables[0].model_copy(update={"rows": inputs.tables[0].rows[1:]})
    missing = inputs.model_copy(update={"tables": (table,)})
    orchestrator = service(reference=mismatch)
    withheld = orchestrator.evaluate(request(inputs=missing), OWNER)
    assert withheld.outputs[0].reason == "Observation value is missing"
    assert withheld.verification[0].status == "unavailable"
    compared = orchestrator.evaluate(request(inputs=inputs), OWNER)
    assert compared.outputs[0].status == "withheld"
    assert compared.verification[0].status == "mismatch"
    invalid = inputs.model_copy(update={"schema_id": "different-schema"})
    with pytest.raises(ExecutionError, match="input_schema_mismatch"):
        orchestrator.evaluate(request(inputs=invalid), OWNER)


@pytest.mark.parametrize("stage", ["rule", "reference"])
def test_slow_lifecycle_callbacks_share_the_service_deadline(
    service, inputs, stage, tmp_path
):
    marker = tmp_path / "callback-started"
    slow = partial(slow_callback, marker)
    config = {"timeout": 2}
    if stage == "rule":
        config.update(
            model=partial_method(), rules=(Rule("quality", (), ("blocked",), slow),)
        )
    else:
        config.update(reference=slow)
    orchestrator = service(**config)
    started = monotonic()
    with pytest.raises(ExecutionError, match="timeout"):
        orchestrator.evaluate(request(inputs=inputs), OWNER)
    assert marker.exists()
    assert monotonic() - started < 5
    assert not (tmp_path / "runs").exists()


def test_acquisition_receives_absolute_service_deadline_and_same_cancellation_event(
    service, inputs
):
    source = FakeSource(inputs)
    cancelled = Event()
    orchestrator = service(source=source)
    started = monotonic()
    orchestrator.evaluate(
        request(acquisition=AcquisitionRequest(**ACQUISITION)), OWNER, cancel=cancelled
    )
    assert started < source.deadline <= started + 5.1
    assert source.cancel is cancelled


@pytest.mark.parametrize(
    ("row_count", "code"),
    [(2, "invalid_input_snapshot"), (10_000, "row_limit")],
)
def test_worker_validates_acquired_rows_without_parent_revalidation(
    service, inputs, monkeypatch, tmp_path, row_count, code
):
    table = inputs.tables[0]
    first = table.rows[0]
    if row_count == 2:
        rows = (first, first)
    else:
        rows = tuple(
            first.model_copy(
                update={"record_id": f"row-{i}", "entity_id": f"entity-{i}"}
            )
            for i in range(row_count)
        )
    snapshot = inputs.model_copy(
        update={"tables": (table.model_copy(update={"rows": rows}),)}
    )
    orchestrator = service(source=FakeSource(snapshot))
    evaluation = request(acquisition=AcquisitionRequest(**ACQUISITION))

    def fail_parent_validation(*args, **kwargs):
        pytest.fail("the parent revalidated the acquired snapshot")

    monkeypatch.setattr(type(snapshot), "model_validate", fail_parent_validation)
    with pytest.raises(ExecutionError, match=f"^{code}$"):
        orchestrator.evaluate(evaluation, OWNER)
    assert not (tmp_path / "runs").exists()
