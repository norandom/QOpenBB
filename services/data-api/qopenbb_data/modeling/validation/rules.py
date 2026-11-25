"""Run the selected lifecycle stage against the method's declared rules."""

from collections.abc import Callable
from dataclasses import dataclass

from ..contracts.checks import CheckOutcome, CheckStage, CheckStatus, RuleDescriptor
from ..contracts.common import require_subset, require_unique
from ..contracts.descriptors import ModelDescriptor
from ..contracts.inputs import AssumptionSet, InputSnapshot
from ..models.protocol import CandidateResult
from .tolerance import within_tolerance


@dataclass(frozen=True)
class RuleContext:
    inputs: InputSnapshot
    assumptions: AssumptionSet
    candidate: CandidateResult | None = None


@dataclass(frozen=True)
class Rule:
    rule_id: str
    input_ids: tuple[str, ...]
    output_ids: tuple[str, ...]
    evaluate: Callable[[RuleContext], CheckOutcome]


def evaluate_stage(
    descriptor: ModelDescriptor, rules: tuple[Rule, ...], stage: CheckStage, context: RuleContext,
) -> tuple[CheckOutcome, ...]:
    """Evaluate one stage. Pass precondition outcomes to blocked_outputs before calculation."""
    if stage == "precondition" and context.candidate is not None:
        raise ValueError("preconditions must run before calculation")
    require_unique(tuple(rule.rule_id for rule in rules), "rule implementation")
    bindings = {rule.rule_id: rule for rule in rules}
    require_subset(tuple(bindings), {rule.rule_id for rule in descriptor.rules}, "rule implementations")
    return tuple(
        _evaluate_rule(definition, bindings.get(definition.rule_id), descriptor, context)
        for definition in descriptor.rules if definition.stage == stage
    )


def _evaluate_rule(
    definition: RuleDescriptor, rule: Rule | None, descriptor: ModelDescriptor, context: RuleContext,
) -> CheckOutcome:
    required = tuple(
        output.output_id for output in descriptor.outputs
        if definition.rule_id in output.required_check_ids
    )
    if rule is None:
        return _unavailable(definition, (), required, "unknown", "Rule implementation is unavailable")
    require_subset(rule.input_ids, set(descriptor.input_ids), "rule inputs")
    require_subset(rule.output_ids, {item.output_id for item in descriptor.outputs}, "rule outputs")
    affected = tuple(dict.fromkeys((*rule.output_ids, *required)))
    if set(rule.input_ids) - {table.table_id for table in context.inputs.tables}:
        return _unavailable(definition, rule.input_ids, affected, "unknown", "Required input table is absent")
    if definition.stage != "precondition" and context.candidate is None:
        return _unavailable(definition, rule.input_ids, affected, "unknown", "Calculation evidence is unavailable")
    try:
        outcome = CheckOutcome.model_validate(rule.evaluate(context))
        if (
            (outcome.rule_id, outcome.rule_version, outcome.severity)
            != (definition.rule_id, definition.version, definition.severity)
            or set(outcome.input_ids) != set(rule.input_ids)
            or set(outcome.output_ids) != set(affected)
        ):
            raise ValueError("check evidence differs from its declared identity or scope")
        return _validate_pass_evidence(outcome)
    except Exception:  # noqa: BLE001 - expose callback failures as typed evidence.
        return _unavailable(definition, rule.input_ids, affected, "error", "Rule evaluation failed")


def _validate_pass_evidence(outcome: CheckOutcome) -> CheckOutcome:
    """Check a passing verdict against the supplied observations and expectations."""
    if outcome.status != "pass":
        return outcome
    tolerance = outcome.tolerance
    if tolerance is not None:
        observed, expected = outcome.observed_value, outcome.expected_value
        if observed is None or expected is None:
            return outcome.model_copy(update={
                "status": "unknown", "explanation": "Numerical comparison evidence is unavailable",
            })
        # The frozen check contract records one common unit and scale for both amounts and the bound.
        if not within_tolerance(observed, expected, tolerance, unit=tolerance.unit, scale=tolerance.scale):
            return outcome.model_copy(update={
                "status": "fail", "explanation": "Observed value is outside the declared tolerance",
            })
    elif outcome.observed is None or outcome.expected is None:
        return outcome.model_copy(update={
            "status": "unknown", "explanation": "Both observed and expected conditions are required",
        })
    if outcome.explanation is not None:
        return outcome
    if tolerance is not None:
        explanation = (
            f"Observed {outcome.observed_value} is within the declared tolerance of "
            f"expected {outcome.expected_value} in {tolerance.unit} at scale {tolerance.scale}"
        )
    else:
        explanation = f"Observed condition met the expectation: {outcome.expected}"
        if len(explanation) > 4096:
            explanation = "The observed condition met the recorded expectation"
    return outcome.model_copy(update={"explanation": explanation})


def _unavailable(
    definition: RuleDescriptor, input_ids: tuple[str, ...], output_ids: tuple[str, ...],
    status: CheckStatus, explanation: str,
) -> CheckOutcome:
    return CheckOutcome(
        rule_id=definition.rule_id, rule_version=definition.version, severity=definition.severity,
        input_ids=input_ids, output_ids=output_ids, status=status, explanation=explanation,
    )
