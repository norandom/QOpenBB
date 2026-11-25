"""Resolve affected values against rule outcomes and output dependencies."""

from graphlib import TopologicalSorter

from ..contracts.checks import CheckOutcome, PolicyException
from ..contracts.common import require_subset, require_unique
from ..contracts.descriptors import ModelDescriptor, OutputDescriptor
from ..contracts.inputs import InputSnapshot
from ..contracts.results import OutputResult
from ..models.protocol import CandidateOutput, CandidateResult


def ordered_outputs(descriptor: ModelDescriptor) -> tuple[OutputDescriptor, ...]:
    definitions = {item.output_id: item for item in descriptor.outputs}
    graph = {key: item.required_output_ids for key, item in definitions.items()}
    return tuple(definitions[key] for key in TopologicalSorter(graph).static_order())


def blocked_outputs(
    descriptor: ModelDescriptor, checks: tuple[CheckOutcome, ...],
    exceptions: tuple[PolicyException, ...] = (),
) -> set[str]:
    """Identify outputs to skip after preconditions or withhold after calculation."""
    authorized = _authorized_exceptions(descriptor, checks, exceptions)
    blocked = {
        output_id for check in checks if check.severity == "blocking" and check.status == "fail"
        for output_id in check.output_ids if (check.rule_id, output_id) not in authorized
    }
    for output in ordered_outputs(descriptor):
        if blocked.intersection(output.required_output_ids):
            blocked.add(output.output_id)
    return blocked


def _authorized_exceptions(
    descriptor: ModelDescriptor, checks: tuple[CheckOutcome, ...], exceptions: tuple[PolicyException, ...],
) -> set[tuple[str, str]]:
    require_unique(tuple(check.rule_id for check in checks), "check outcome")
    require_unique(tuple(item.exception_id for item in exceptions), "policy exception")
    rules = {rule.rule_id: rule for rule in descriptor.rules}
    outcomes = {check.rule_id: check for check in checks}
    output_ids = {item.output_id for item in descriptor.outputs}
    for check in checks:
        rule = rules.get(check.rule_id)
        if rule is None or (check.rule_version, check.severity) != (rule.version, rule.severity):
            raise ValueError("check outcome differs from its rule")
        require_subset(check.output_ids, output_ids, "check outputs")
        require_subset(check.input_ids, set(descriptor.input_ids), "check inputs")

    authorized = set()
    for item in exceptions:
        check = outcomes.get(item.rule_id)
        if (
            check is None or check.status != "fail" or check.rule_version != item.rule_version
            or rules[item.rule_id].exception_policy_version != item.policy_version
        ):
            raise ValueError("exception requires a failed check with a matching house policy")
        require_subset(item.output_ids, set(check.output_ids), "policy exception outputs")
        authorized.update((item.rule_id, output_id) for output_id in item.output_ids)
    return authorized


def resolve_outputs(
    descriptor: ModelDescriptor, candidate: CandidateResult, checks: tuple[CheckOutcome, ...], *,
    inputs: InputSnapshot, exceptions: tuple[PolicyException, ...] = (),
) -> tuple[OutputResult, ...]:
    """Project candidate values before independent verification."""
    blocked = blocked_outputs(descriptor, checks, exceptions)
    definitions = {item.output_id for item in descriptor.outputs}
    candidates = {item.output_id: item for item in candidate.outputs}
    require_subset(tuple(candidates), definitions, "candidate outputs")
    require_subset(tuple(entry.output_id for entry in candidate.trace), definitions, "trace outputs")
    input_ids = {table.table_id for table in inputs.tables}
    resolved: dict[str, OutputResult] = {}
    for definition in ordered_outputs(descriptor):
        output_id = definition.output_id
        item = candidates.get(output_id)
        reason = _withholding_reason(definition, item, blocked, input_ids, resolved)
        resolved[output_id] = OutputResult(
            output_id=output_id, semantic_definition=definition.semantic_definition,
            unit=definition.unit, value_type=definition.value_type,
            value=item.value if reason is None and item is not None else None,
            status="withheld" if reason else "unverified",
            reason=reason or "Awaiting independent verification",
            trace_ids=tuple(entry.trace_id for entry in candidate.trace if entry.output_id == output_id),
            check_ids=tuple(check.rule_id for check in checks if output_id in check.output_ids),
            exception_ids=tuple(item.exception_id for item in exceptions if output_id in item.output_ids),
        )
    return tuple(resolved[item.output_id] for item in descriptor.outputs)


def _withholding_reason(
    definition: OutputDescriptor, candidate: CandidateOutput | None, blocked: set[str],
    input_ids: set[str], resolved: dict[str, OutputResult],
) -> str | None:
    if any(resolved[key].status == "withheld" for key in definition.required_output_ids):
        return "A required output was withheld"
    if definition.output_id in blocked:
        return "A blocking financial rule failed"
    if set(definition.required_input_ids) - input_ids:
        return "A required input table is absent"
    if candidate is None or candidate.value is None:
        return (candidate.reason if candidate else None) or "Calculation value is unavailable"
    if candidate.value_type != definition.value_type:
        raise ValueError("candidate value type differs from its output definition")
    return None
