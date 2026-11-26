"""Compare calculated outputs with independently implemented supplied-input references."""

from collections.abc import Callable, Mapping
from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Literal

from pydantic import TypeAdapter

from ..contracts.checks import CheckOutcome, Tolerance
from ..contracts.common import Scalar, require_subset, require_unique, serialize_scalar
from ..contracts.descriptors import ModelDescriptor, OutputDescriptor
from ..contracts.inputs import AssumptionSet, InputSnapshot, Transformation
from ..contracts.results import OutputResult, VerificationEvidence
from ..contracts.trace import TraceEntry
from ..validation.outputs import ordered_outputs
from ..validation.tolerance import within_tolerance

ReferenceCalculation = Callable[[InputSnapshot, AssumptionSet], Scalar | None]
ComparisonStatus = Literal["match", "mismatch", "unavailable"]
_REFERENCE_SCALAR: TypeAdapter[Scalar] = TypeAdapter(Scalar)
_SCALAR_TYPES = {"decimal": Decimal, "integer": int, "boolean": bool, "text": str, "date": date}


@dataclass(frozen=True)
class Reference:
    """Independent calculators and the financial availability checks they can adjudicate."""

    version: str
    calculations: Mapping[str, ReferenceCalculation]
    tolerances: Mapping[str, Tolerance]
    availability_check_ids: frozenset[str] = frozenset()


def verify_outputs(
    descriptor: ModelDescriptor, inputs: InputSnapshot, assumptions: AssumptionSet,
    outputs: tuple[OutputResult, ...], trace: tuple[TraceEntry, ...],
    checks: tuple[CheckOutcome, ...], reference: Reference | None,
) -> tuple[tuple[OutputResult, ...], tuple[VerificationEvidence, ...], tuple[TraceEntry, ...]]:
    """Recalculate and return the final outputs, evidence, and trace to save together."""
    source = {output.output_id: output for output in outputs}
    require_unique(tuple(output.output_id for output in outputs), "verification output")
    require_subset(tuple(source), {item.output_id for item in descriptor.outputs}, "verification outputs")
    if reference is not None and reference.version != descriptor.reference_version:
        reference = None
    input_ids = {table.table_id for table in inputs.tables}
    outcomes = {check.rule_id: check for check in checks}
    fingerprints = {
        "input_fingerprint": inputs.fingerprint(),
        "assumption_fingerprint": assumptions.fingerprint(),
        "descriptor_fingerprint": descriptor.fingerprint(),
    }
    final: dict[str, OutputResult] = {}
    evidence: dict[str, VerificationEvidence] = {}
    availability_checks = reference.availability_check_ids if reference is not None else frozenset()
    for definition in ordered_outputs(descriptor):
        output = source.get(definition.output_id)
        if output is None:
            continue
        dependency_status = {final[key].status for key in definition.required_output_ids if key in final}
        unavailable_dependency = any(
            final[key].status == "withheld" and evidence[key].status == "unavailable"
            for key in definition.required_output_ids if key in final
        )
        if unavailable_dependency or (output.value is not None and "withheld" in dependency_status):
            status: ComparisonStatus = "unavailable"
            explanation = "A required output was withheld"
            expected_text = None
        elif output.status == "withheld" and _has_policy_denial(output, outcomes, availability_checks):
            status = "unavailable"
            explanation = "Calculated value is unavailable"
            expected_text = None
        else:
            status, explanation, expected_text = _compare(output, inputs, assumptions, reference)
        resolved = _verified_output(
            output, definition, outcomes, input_ids, dependency_status,
            dependencies_present=set(definition.required_output_ids) <= final.keys(), status=status,
        )
        if isinstance(output.value, str) and expected_text is not None:
            comparison_trace = _text_mismatch_trace(output, output.value, expected_text, trace, descriptor)
            trace = (*trace, comparison_trace)
            resolved = resolved.model_copy(update={"trace_ids": (*resolved.trace_ids, comparison_trace.trace_id)})
        final[output.output_id] = resolved
        evidence[output.output_id] = VerificationEvidence(
            output_id=output.output_id, reference_version=descriptor.reference_version,
            status=status, explanation=explanation,
            output_fingerprint=VerificationEvidence.fingerprint_output(resolved, trace, checks),
            **fingerprints,
        )
    return (
        tuple(final[output.output_id] for output in outputs),
        tuple(evidence[output.output_id] for output in outputs),
        trace,
    )


def _has_policy_denial(
    output: OutputResult, checks: dict[str, CheckOutcome], availability_checks: frozenset[str],
) -> bool:
    # A reference may adjudicate availability checks. Other blocking checks enforce policy.
    return any(
        check.severity == "blocking"
        and check.status in ("fail", "unknown", "error")
        and check.rule_id not in availability_checks
        for rule_id in output.check_ids
        if (check := checks.get(rule_id)) is not None and output.output_id in check.output_ids
    )


def _compare(
    output: OutputResult, inputs: InputSnapshot, assumptions: AssumptionSet, reference: Reference | None,
) -> tuple[ComparisonStatus, str, str | None]:
    calculate = reference.calculations.get(output.output_id) if reference is not None else None
    if calculate is None or reference is None:
        if output.value is None:
            return "unavailable", "Calculated value is unavailable", None
        return "unavailable", "Compatible independent calculation is unavailable", None
    tolerance = reference.tolerances.get(output.output_id)
    try:
        expected = calculate(inputs, assumptions)
        if expected is None:
            return "unavailable", "Independent calculation has insufficient evidence", None
        if type(expected) is not _SCALAR_TYPES[output.value_type]:
            return "unavailable", "Independent value has an incompatible type", None
        expected = _REFERENCE_SCALAR.validate_python(expected)
        if output.value is None:
            explanation = (
                "Calculated text was withheld although the independent value is available"
                if isinstance(expected, str)
                else f"Calculated value was withheld, expected {serialize_scalar(expected)} in {output.unit}"
            )
            return "mismatch", explanation, None
        matches = _matches(output, expected, tolerance)
    except Exception:  # noqa: BLE001 - expose callback failures as typed evidence.
        return "unavailable", "Independent comparison failed", None
    bound = (
        f"absolute {tolerance.absolute} at scale {tolerance.scale}, relative {tolerance.relative or 0}"
        if tolerance is not None else "exact equality"
    )
    if isinstance(output.value, str):
        comparison = "Compared the calculated and independent text values for exact equality"
    else:
        comparison = f"Observed {output.value}, expected {expected} in {output.unit}, using {bound}"
    expected_text = expected if not matches and isinstance(expected, str) else None
    return ("match" if matches else "mismatch"), comparison, expected_text


def _text_mismatch_trace(
    output: OutputResult, observed: str, expected: str, trace: tuple[TraceEntry, ...],
    descriptor: ModelDescriptor,
) -> TraceEntry:
    if len(trace) >= 1024 or len(output.trace_ids) >= 256:
        raise ValueError("Trace capacity exhausted while recording independent text comparison")
    occupied = {entry.trace_id for entry in trace}
    trace_id = next(
        candidate for index in range(len(occupied) + 1)
        if (candidate := f"verification-text-{index}") not in occupied
    )
    version = descriptor.reference_version
    # Each description can hold one complete operand, including a maximum-length text value.
    return TraceEntry(
        trace_id=trace_id, output_id=output.output_id, formula_id="independent-text-comparison",
        formula_version=version, expression="Compare calculated and independent text for exact equality",
        transformations=(
            Transformation(transformation_id="observed-text", version=version, description=observed),
            Transformation(transformation_id="expected-text", version=version, description=expected),
        ),
    )


def _matches(output: OutputResult, expected: Scalar, tolerance: Tolerance | None) -> bool:
    value = output.value
    if tolerance is None:
        return value == expected
    if not isinstance(value, Decimal | int) or isinstance(value, bool):
        raise TypeError("numerical tolerance requires a numerical output")
    if not isinstance(expected, Decimal | int) or isinstance(expected, bool):
        raise TypeError("independent value must be numeric")
    return within_tolerance(Decimal(value), Decimal(expected), tolerance, unit=output.unit)


def _verified_output(
    output: OutputResult, definition: OutputDescriptor, checks: dict[str, CheckOutcome], input_ids: set[str],
    dependency_status: set[str], *, dependencies_present: bool, status: ComparisonStatus,
) -> OutputResult:
    if output.status == "withheld":
        return output
    if status == "mismatch" or "withheld" in dependency_status:
        reason = "Independent comparison mismatched" if status == "mismatch" else "A required output was withheld"
        return output.model_copy(update={"value": None, "status": "withheld", "reason": reason})
    reason = _unverified_reason(output, definition, checks, input_ids, dependency_status, dependencies_present)
    if reason is None and status == "match":
        return output.model_copy(update={"status": "verified", "reason": None})
    return output.model_copy(update={
        "status": "unverified", "reason": reason or "Independent comparison is unavailable",
    })


def _unverified_reason(
    output: OutputResult, definition: OutputDescriptor, checks: dict[str, CheckOutcome],
    input_ids: set[str], dependency_status: set[str], dependencies_present: bool,
) -> str | None:
    if output.exception_ids:
        return "A house-policy exception was applied"
    if not output.trace_ids:
        return "Calculation trace is unavailable"
    if not dependencies_present or dependency_status - {"verified"}:
        return "A required output has no verified value"
    if set(definition.required_input_ids) - input_ids:
        return "A required input table is absent"
    if set(definition.required_check_ids) - set(output.check_ids):
        return "A required check is unavailable"
    required = set(definition.required_check_ids)
    for rule_id in output.check_ids:
        check = checks.get(rule_id)
        if check is None or output.output_id not in check.output_ids:
            return "Check evidence is unavailable"
        if (
            (rule_id in required or check.severity == "blocking")
            and (check.status != "pass" or set(check.input_ids) - input_ids)
        ):
            return "A required or blocking check did not pass"
    return None
