"""Exercise production factor bindings through the installed execution worker."""

import pickle
from decimal import Decimal

import pytest
from fixtures.factor_examples import EXAMPLES, build_run
from qopenbb_data.modeling.models.factors import comparison
from qopenbb_data.modeling.models.factors.fcf_yield import FcfYieldModel
from qopenbb_data.modeling.models.factors.study_schedule import study_plan
from qopenbb_data.modeling.service.bootstrap import installed_methods
from qopenbb_data.modeling.service.evaluation import EvaluationRequest
from qopenbb_data.modeling.service.execution import ExecutionError
from qopenbb_data.modeling.service.orchestrator import Orchestrator, _bind
from qopenbb_data.modeling.service.ports import Principal
from qopenbb_data.modeling.service.run_store import FileRunStore


def test_production_registry_binds_all_six_exact_versions():
    registry, bindings = installed_methods()
    keys = {(name, "1") for name in EXAMPLES}
    assert {
        (item.model_id, item.method_version) for item in registry.descriptors()
    } == keys
    assert bindings.keys() == keys

    for key, binding in bindings.items():
        descriptor = registry.resolve(*key).describe()
        assert descriptor.rule_set_version == "1"
        assert binding.reference.version == descriptor.reference_version == "1"
        assert binding.reference.calculations.keys() == {
            item.output_id for item in descriptor.outputs
        }
        assert {
            item.rule_id: item.version for item in descriptor.rules
        } == dict.fromkeys((item.rule_id for item in binding.rules), "1")
        with pytest.raises(LookupError):
            registry.resolve(key[0], "2")


@pytest.mark.parametrize("model_id", EXAMPLES)
def test_worker_reference_pickle_preserves_declared_availability(model_id):
    registry, bindings = installed_methods()
    key = (model_id, "1")
    descriptor = registry.resolve(*key).describe()
    reference = bindings[key].reference
    expected = frozenset(output.rule_id for output in EXAMPLES[model_id].outputs)
    assert reference.availability_check_ids == expected
    assert expected <= {rule.rule_id for rule in descriptor.rules}

    restored = pickle.loads(pickle.dumps(reference, protocol=pickle.HIGHEST_PROTOCOL))
    assert restored.availability_check_ids == expected
    assert restored.version == descriptor.reference_version == "1"
    assert restored.calculations.keys() == reference.calculations.keys()
    assert restored.tolerances == reference.tolerances
    assert all(callable(calculate) for calculate in restored.calculations.values())


def test_timing_bounds_outcome_horizon_and_combined_observation_rows():
    _, bindings = installed_methods()
    limits = bindings["timing_study", "1"].limits
    fixture = build_run(EXAMPLES["timing_study"], missing=False)
    plan = study_plan(fixture.inputs, fixture.assumptions)
    assert len(plan.sessions) - 2 > 1
    assert limits.measure_dimensions(fixture.inputs, fixture.assumptions) == (1, 1)
    assert limits.max_horizon == 1
    limits.check(fixture.inputs, fixture.assumptions)

    first, second = fixture.inputs.tables[:2]
    # Bypass snapshot validation to exercise the execution guard at both sides of its limit.
    first = first.model_copy(update={"rows": (first.rows[0],) * 5_000})
    for count in (5_000, 5_001):
        other = second.model_copy(update={"rows": (second.rows[0],) * count})
        snapshot = fixture.inputs.model_copy(update={"tables": (first, other)})
        if count == 5_000:
            limits.check(snapshot, fixture.assumptions)
        else:
            with pytest.raises(ExecutionError) as error:
                limits.check(snapshot, fixture.assumptions)
            assert error.value.code == "row_limit"


def _run_installed_lifecycle(model_id):
    registry, bindings = installed_methods()
    key = model_id, "1"
    model = registry.resolve(*key)
    _, job = _bind(model, key, bindings[key])
    fixture = build_run(EXAMPLES[model_id], missing=True)
    return pickle.loads(job)(
        model,
        fixture.inputs,
        fixture.assumptions,
        {
            "owner_id": fixture.owner_id,
            "created_at": fixture.created_at,
            "exceptions": (),
        },
    )


def test_failed_fcf_precondition_never_calls_calculate(monkeypatch):
    calls = []
    calculate = FcfYieldModel.calculate

    def track(self, inputs, assumptions):
        calls.append(inputs)
        return calculate(self, inputs, assumptions)

    monkeypatch.setattr(FcfYieldModel, "calculate", track)
    run = _run_installed_lifecycle("issuer_fcf_yield")
    assert calls == []
    assert run.checks[0].status == "fail"
    assert run.outputs[0].status == "withheld"


def test_partial_pair_executes_only_the_eligible_left_leg(monkeypatch):
    calls = []
    calculate_leg = comparison._leg_metric
    calculate_spread = comparison._spread

    def track_leg(*args, **kwargs):
        result = calculate_leg(*args, **kwargs)
        calls.append(result[0].output_id)
        return result

    def track_spread(*args, **kwargs):
        result = calculate_spread(*args, **kwargs)
        calls.append(result[0].output_id)
        return result

    monkeypatch.setattr(comparison, "_leg_metric", track_leg)
    monkeypatch.setattr(comparison, "_spread", track_spread)
    run = _run_installed_lifecycle("proxy_comparison")
    assert calls == ["left_momentum", "left_volatility"]
    assert {item.output_id for item in run.outputs if item.status == "verified"} == set(
        calls
    )


@pytest.mark.parametrize("model_id", EXAMPLES)
@pytest.mark.parametrize("missing", [False, True], ids=["complete", "missing-input"])
def test_installed_worker_applies_real_rules_and_references(
    model_id, missing, tmp_path
):
    registry, bindings = installed_methods()
    assert (model_id, "1") in bindings
    service = Orchestrator(registry, bindings, FileRunStore(tmp_path / "runs"))
    example = EXAMPLES[model_id]
    fixture = build_run(example, missing)
    run = service.evaluate(
        EvaluationRequest(
            model_id=model_id,
            method_version="1",
            inputs=fixture.inputs,
            assumptions=fixture.assumptions,
        ),
        Principal(subject="factor-reviewer"),
    )

    withheld = {output.output_id for output in fixture.outputs if output.value is None}
    checks = {check.rule_id: check for check in run.checks}
    verification = {item.output_id: item for item in run.verification}
    expected_outputs = {item.output_id: item for item in fixture.outputs}
    tolerances = {item.output_id: item.absolute_tolerance for item in example.outputs}
    assert {item.output_id for item in run.outputs} == expected_outputs.keys()
    for output in run.outputs:
        check = checks[f"eligible_inputs.{output.output_id}"]
        proof = verification[output.output_id]
        assert (check.rule_version, proof.reference_version) == ("1", "1")
        if output.output_id in withheld:
            assert (output.status, output.value, proof.status) == (
                "withheld",
                None,
                "unavailable",
            )
            assert check.status in ("fail", "unknown")
            assert check.explanation
        else:
            assert (output.status, proof.status, check.status) == (
                "verified",
                "match",
                "pass",
            )
            assert output.value is not None and output.trace_ids
            expected = expected_outputs[output.output_id]
            assert output.unit == expected.unit
            if tolerance := tolerances[output.output_id]:
                assert output.value == pytest.approx(
                    expected.value, abs=Decimal(tolerance), rel=0
                )
            else:
                assert output.value == expected.value
