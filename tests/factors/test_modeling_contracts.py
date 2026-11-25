from datetime import UTC, date, datetime
from decimal import Decimal

import pytest
from pydantic import ValidationError
from qopenbb_data.modeling.contracts import (
    Assumption,
    AssumptionSet,
    CheckOutcome,
    EvaluationCutoff,
    InputSnapshot,
    ModelDescriptor,
    ModelRun,
    Observation,
    ObservationTable,
    OutputResult,
    PolicyException,
    Tolerance,
    TraceEntry,
    VerificationEvidence,
)


def timestamp(day, hour=0):
    return datetime(2024, 1, day, hour, tzinfo=UTC)


EXACT = Decimal("1.1234567890123456789012345678901234567")


def observation(**changes):
    fields = {
        "record_id": "close-1",
        "entity_id": "ETF",
        "metric_id": "close",
        "observation_date": date(2024, 1, 2),
        "context": {"unit": "price", "currency": "USD", "quantity": "stock", "basis": "split_adjusted"},
        "value": EXACT,
        "category": "provider",
        "published_at": timestamp(2, 20),
    }
    return Observation(**(fields | changes))


def snapshot(*rows, nullable=False):
    table = ObservationTable(
        table_id="prices",
        grain="one close per entity, session and source revision",
        keys=("entity_id", "metric_id", "observation_date", "vintage_at"),
        nullable=nullable,
        rows=rows,
    )
    return InputSnapshot(
        schema_id="prices",
        provenance={
            "origin": "user_supplied", "source": "asserted-prices",
            "query": (("symbol", "ETF"),), "retrieved_at": timestamp(5),
        },
        tables=(table,),
    )


def test_snapshot_round_trip_and_deep_immutability():
    original = snapshot(observation())
    encoded = original.model_dump_json()
    assert f'"{EXACT}"' in encoded
    restored = InputSnapshot.model_validate_json(encoded)
    assert restored == original
    assert restored.fingerprint() == original.fingerprint()
    with pytest.raises(ValidationError):
        restored.tables[0].rows[0].value = Decimal(2)
    assert isinstance(restored.tables[0].rows, tuple)


@pytest.mark.parametrize("invalid", [1.2, True, "NaN", "Infinity", "1e9999", "1e-39", "1e38"])
def test_decimal_rejects_lossy_or_out_of_bounds_values(invalid):
    with pytest.raises(ValidationError):
        observation(value=invalid)


def test_decimal_encoding_handles_exponents_and_signed_zero():
    assert '"value":"1000"' in observation(value=Decimal("1E+3")).model_dump_json()
    assert '"value":"0"' in observation(value=Decimal("-0.00")).model_dump_json()


def test_table_requires_complete_unique_keys_and_honors_nullability():
    with pytest.raises(ValidationError, match="duplicate"):
        snapshot(observation(), observation(record_id="different", value=Decimal(2)))
    with pytest.raises(ValidationError, match="null"):
        snapshot(observation(value=None))
    initial = observation()
    revision = observation(record_id="corrected", vintage_at=timestamp(3), value=None)
    assert snapshot(initial, revision, nullable=True).tables[0].rows[1].value is None


def test_cutoff_uses_local_decision_date_and_both_availability_dates():
    cutoff = EvaluationCutoff(
        observation_date=date(2024, 1, 2),
        decision_at=timestamp(3, 1),
        evaluated_at=timestamp(5),
        session_timezone="America/New_York",
    )
    assert cutoff.is_eligible(observation())
    assert cutoff.is_eligible(observation(published_at=timestamp(3, 1)))
    assert not cutoff.is_eligible(observation(published_at=None))
    assert not cutoff.is_eligible(observation(vintage_at=timestamp(4)))
    assert not cutoff.is_eligible(observation(observation_date=date(2024, 1, 3)))
    assert not cutoff.is_eligible(observation(), return_starts_at=timestamp(2, 20))
    earlier = EvaluationCutoff.model_validate(cutoff.model_dump() | {"evaluated_at": timestamp(2, 19)})
    assert not earlier.is_eligible(observation())


def test_assumptions_are_typed_dated_and_versioned():
    assumptions = AssumptionSet(
        version="1",
        effective_date=date(2024, 1, 2),
        assumptions=({
            "assumption_id": "annualization",
            "value_type": "integer",
            "value": 252,
            "origin": "user_supplied",
            "rationale": "Trading sessions per year",
            "author": "analyst",
        },),
    )
    assert AssumptionSet.model_validate_json(assumptions.model_dump_json()) == assumptions
    invalid = assumptions.model_dump()
    invalid["assumptions"][0]["value"] = "252"
    with pytest.raises(ValidationError):
        AssumptionSet.model_validate(invalid)


def descriptor():
    return {
        "model_id": "synthetic-contract-example",
        "method_version": "1",
        "input_schema_id": "prices",
        "output_schema_id": "metric",
        "rule_set_version": "1",
        "reference_version": "1",
        "entity_types": ("etf",),
        "period_types": ("session",),
        "input_ids": ("prices",),
        "rules": ({"rule_id": "coverage", "version": "1", "stage": "precondition", "severity": "blocking"},),
        "outputs": ({
            "output_id": "metric", "semantic_definition": "Synthetic price", "unit": "price",
            "required_input_ids": ("prices",), "required_check_ids": ("coverage",),
        },),
    }


def test_descriptor_declares_dependencies():
    assert ModelDescriptor(**descriptor()).outputs[0].required_check_ids == ("coverage",)
    fields = descriptor()
    fields["outputs"][0]["required_check_ids"] = ("missing",)
    with pytest.raises(ValidationError, match="unknown"):
        ModelDescriptor(**fields)


def test_check_exception_and_withheld_output_invariants():
    tolerance = Tolerance(absolute="0.001", unit="percent")
    assert tolerance.absolute == Decimal("0.001")
    with pytest.raises(ValidationError):
        Tolerance(absolute="-0.001", unit="percent")
    with pytest.raises(ValidationError, match="explanation"):
        CheckOutcome(rule_id="coverage", rule_version="1", severity="blocking", status="not_applicable")
    with pytest.raises(ValidationError):
        OutputResult(output_id="metric", semantic_definition="Price", unit="price", status="withheld", value=EXACT)
    exception = PolicyException(
        exception_id="review-1", rule_id="coverage", rule_version="1",
        author="analyst", output_ids=("metric",), rationale="Approved limited use", policy_version="1",
    )
    assert PolicyException.model_validate_json(exception.model_dump_json()) == exception


def test_run_round_trip_keeps_unrounded_trace_and_source_references():
    inputs = snapshot(observation())
    assumptions = AssumptionSet(version="1", effective_date=date(2024, 1, 2))
    trace = TraceEntry(
        trace_id="trace-1", formula_id="identity", formula_version="1", expression="close",
        source_record_ids=("close-1",), input_ids=("prices",),
        substitutions=({"name": "close", "value": EXACT, "unit": "price", "period_end": date(2024, 1, 2)},),
        intermediate_values=({"name": "price", "value": EXACT, "unit": "price", "period_end": date(2024, 1, 2)},),
        output_id="metric", check_ids=("coverage",),
    )
    output = OutputResult(
        output_id="metric", semantic_definition="Synthetic price", value=EXACT, unit="price",
        status="unverified", reason="Reference evidence unavailable",
        trace_ids=("trace-1",), check_ids=("coverage",),
    )
    run = ModelRun(
        run_id="opaque-run", owner_id="analyst", created_at=timestamp(5),
        descriptor=ModelDescriptor(**descriptor()), inputs=inputs, assumptions=assumptions,
        outputs=(output,), trace=(trace,),
        checks=(CheckOutcome(
            rule_id="coverage", rule_version="1", severity="blocking", status="pass",
            input_ids=("prices",), output_ids=("metric",),
        ),),
    )
    assert ModelRun.model_validate_json(run.model_dump_json()) == run
    assert run.trace[0].intermediate_values[0].value == EXACT
    assert run.inputs.fingerprint() == inputs.fingerprint()
    missing_trace = run.model_dump() | {"trace": ()}
    with pytest.raises(ValidationError, match="trace"):
        ModelRun.model_validate(missing_trace)

    verified_output = OutputResult.model_validate(
        output.model_dump() | {"status": "verified", "reason": None}
    )
    verified_fields = run.model_dump() | {"outputs": (verified_output,)}
    with pytest.raises(ValidationError, match="matching reference"):
        ModelRun.model_validate(verified_fields)
    evidence = VerificationEvidence(
        output_id="metric", reference_version="1", status="match",
        explanation="Independent synthetic comparison",
        input_fingerprint=inputs.fingerprint(),
        assumption_fingerprint=assumptions.fingerprint(),
        descriptor_fingerprint=run.descriptor.fingerprint(),
        output_fingerprint=VerificationEvidence.fingerprint_output(verified_output, run.trace, run.checks),
    )
    verified_fields["verification"] = (evidence,)
    verified = ModelRun.model_validate(verified_fields)
    assert ModelRun.model_validate_json(verified.model_dump_json()) == verified
    with pytest.raises(ValidationError, match="fingerprints"):
        ModelRun.model_validate(verified_fields | {"inputs": snapshot(observation(value="2"))})
    failed_check = run.checks[0].model_dump() | {"status": "fail", "explanation": "Missing close"}
    with pytest.raises(ValidationError, match="blocking failure"):
        ModelRun.model_validate(verified_fields | {"checks": (failed_check,)})


def test_timing_excludes_signals_decided_at_or_after_return_start():
    cutoff = EvaluationCutoff(
        observation_date=date(2024, 1, 2), decision_at=timestamp(2, 22),
        evaluated_at=timestamp(5), session_timezone="UTC",
    )
    early = observation(published_at=timestamp(2, 18))
    assert not cutoff.is_eligible(early, return_starts_at=timestamp(2, 21))
    assert not cutoff.is_eligible(early, return_starts_at=timestamp(2, 22))
    assert cutoff.is_eligible(early, return_starts_at=timestamp(2, 23))


@pytest.mark.parametrize(("value_type", "value", "wire"), [
    ("text", "001.20", "001.20"), ("text", "1.20", "1.20"),
    ("text", "2024-01-02", "2024-01-02"), ("text", "falling", "falling"),
    ("decimal", EXACT, str(EXACT)), ("integer", 4, 4), ("boolean", False, False),
    ("date", date(2024, 1, 2), "2024-01-02"),
])
def test_scalar_contracts_preserve_type_and_wire_value(value_type, value, wire):
    assumption = Assumption(
        assumption_id="scalar", value_type=value_type, value=value,
        origin="method_default", rationale="Synthetic scalar fixture",
    )
    output = OutputResult(
        output_id="regime", semantic_definition="Synthetic scalar", unit="classification",
        value_type=value_type, value=value, status="unverified", reason="Synthetic fixture",
    )
    for contract in (assumption, output):
        assert contract.model_dump(mode="json")["value"] == wire
        restored = type(contract).model_validate_json(contract.model_dump_json())
        assert type(restored.value) is type(value)
        assert restored.value == value
        assert restored.fingerprint() == contract.fingerprint()


def test_decimal_discards_unbounded_insignificant_coefficient_without_rounding():
    row = observation(value=Decimal("1." + "0" * 10_000))
    assert row.value.as_tuple() == Decimal(1).as_tuple()
    assert row.fingerprint() == observation(value=Decimal(1)).fingerprint()


def test_earlier_evaluation_does_not_make_a_late_decision_eligible():
    cutoff = EvaluationCutoff(
        observation_date=date(2024, 1, 2), decision_at=timestamp(2, 22),
        evaluated_at=timestamp(2, 19), session_timezone="UTC",
    )
    row = observation(published_at=timestamp(2, 18))
    assert cutoff.is_eligible(row)
    assert not cutoff.is_eligible(row, return_starts_at=timestamp(2, 21))
    assert not cutoff.is_eligible(row, return_starts_at=timestamp(2, 22))


def test_check_retains_unrounded_comparison_with_units_and_scale():
    check = CheckOutcome(
        rule_id="reference", rule_version="1", severity="blocking", status="pass",
        observed_value=EXACT, expected_value=EXACT,
        tolerance={"unit": "USD", "scale": 6, "absolute": "0"},
    )
    assert CheckOutcome.model_validate_json(check.model_dump_json()) == check
    assert check.model_dump(mode="json")["observed_value"] == str(EXACT)


def test_unknown_provenance_and_schema_versions_fail_closed():
    supplied = snapshot(observation())
    with pytest.raises(ValidationError, match="acquisition"):
        InputSnapshot.model_validate(
            supplied.model_dump() | {
                "provenance": supplied.provenance.model_dump() | {"acquisition_id": "forged"}
            }
        )
    with pytest.raises(ValidationError, match="schema_version"):
        InputSnapshot.model_validate(supplied.model_dump() | {"schema_version": "2"})


def test_descriptor_rejects_cyclic_outputs():
    fields = descriptor()
    fields["outputs"][0]["required_output_ids"] = ("metric",)
    with pytest.raises(ValidationError, match="cyclic"):
        ModelDescriptor(**fields)
