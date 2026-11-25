"""Evaluate a supplied-input run through financial checks and independent verification."""

from collections.abc import Callable
from datetime import datetime

from ..contracts.checks import CheckOutcome, PolicyException
from ..contracts.common import require_subset
from ..contracts.descriptors import ModelDescriptor
from ..contracts.inputs import AssumptionSet, InputSnapshot
from ..contracts.results import ModelRun
from ..models.protocol import CandidateResult
from ..verification.reference import Reference, verify_outputs
from .outputs import blocked_outputs, ordered_outputs, resolve_outputs
from .rules import Rule, RuleContext, evaluate_stage

Calculate = Callable[[InputSnapshot, AssumptionSet, tuple[str, ...]], CandidateResult]


def evaluate_run(
    descriptor: ModelDescriptor, inputs: InputSnapshot, assumptions: AssumptionSet, *,
    run_id: str, owner_id: str, created_at: datetime, rules: tuple[Rule, ...],
    calculate: Calculate, reference: Reference | None = None,
    exceptions: tuple[PolicyException, ...] = (),
) -> ModelRun:
    """Run an installed method using the supplied snapshot and accepted policy exceptions.

    The calculator receives an ordered subset of output IDs and may return partial results.
    Calculator exceptions propagate so the caller can preserve its execution failure semantics.
    """
    if (inputs.schema_id, inputs.schema_version) != (
        descriptor.input_schema_id, descriptor.input_schema_version
    ):
        raise ValueError("run input schema is incompatible with the descriptor")
    checks = evaluate_stage(descriptor, rules, "precondition", RuleContext(inputs, assumptions))
    eligible = _eligible_outputs(descriptor, inputs, checks, exceptions)
    candidate = None
    if eligible:
        candidate = CandidateResult.model_validate(calculate(inputs, assumptions, eligible))
        require_subset(tuple(item.output_id for item in candidate.outputs), set(eligible), "eligible candidate outputs")
        require_subset(tuple(item.output_id for item in candidate.trace), set(eligible), "eligible trace outputs")

    context = RuleContext(inputs, assumptions, candidate)
    checks += evaluate_stage(descriptor, rules, "invariant", context)
    checks += evaluate_stage(descriptor, rules, "postcondition", context)
    candidate = candidate if candidate is not None else CandidateResult(outputs=())
    outputs = resolve_outputs(descriptor, candidate, checks, inputs=inputs, exceptions=exceptions)
    outputs, evidence, trace = verify_outputs(
        descriptor, inputs, assumptions, outputs, candidate.trace, checks, reference,
    )
    return ModelRun(
        run_id=run_id, owner_id=owner_id, created_at=created_at, descriptor=descriptor,
        inputs=inputs, assumptions=assumptions, outputs=outputs, trace=trace,
        checks=checks, exceptions=exceptions, verification=evidence,
    )


def _eligible_outputs(
    descriptor: ModelDescriptor, inputs: InputSnapshot, checks: tuple[CheckOutcome, ...],
    exceptions: tuple[PolicyException, ...],
) -> tuple[str, ...]:
    preconditions = {check.rule_id for check in checks}
    precondition_exceptions = tuple(item for item in exceptions if item.rule_id in preconditions)
    blocked = blocked_outputs(descriptor, checks, precondition_exceptions)
    blocked.update(
        output_id for check in checks if check.severity == "blocking" and check.status in ("unknown", "error")
        for output_id in check.output_ids
    )
    supplied = {table.table_id for table in inputs.tables}
    eligible: set[str] = set()
    for output in ordered_outputs(descriptor):
        if (
            output.output_id not in blocked
            and set(output.required_input_ids) <= supplied
            and set(output.required_output_ids) <= eligible
        ):
            eligible.add(output.output_id)
    return tuple(output.output_id for output in descriptor.outputs if output.output_id in eligible)
