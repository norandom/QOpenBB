"""Evaluation requests and the child-side financial lifecycle."""

from collections.abc import Callable
from typing import Annotated, Self

from pydantic import Field, model_validator

from ..contracts.checks import PolicyException
from ..contracts.common import Contract, Identifier, Timestamp, require_unique
from ..contracts.inputs import AssumptionSet, InputSnapshot
from ..contracts.results import ModelRun
from ..models.protocol import CandidateOutput, CandidateResult, Model
from ..validation.lifecycle import Calculate, evaluate_run
from ..validation.rules import Rule
from ..verification.reference import Reference
from .ports import AcquisitionRequest

Exceptions = Annotated[tuple[PolicyException, ...], Field(max_length=256)]


class EvaluationRequest(Contract):
    """An exact installed method and one explicit source of its inputs."""

    model_id: Identifier
    method_version: Identifier
    assumptions: AssumptionSet
    inputs: InputSnapshot | None = None
    acquisition: AcquisitionRequest | None = None
    exceptions: Exceptions = ()

    @model_validator(mode="after")
    def validate_source(self) -> Self:
        if (self.inputs is None) == (self.acquisition is None):
            raise ValueError("evaluation requires exactly one input source")
        require_unique(
            tuple(item.exception_id for item in self.exceptions), "policy exception"
        )
        return self


class _RunContext(Contract):
    owner_id: Identifier
    created_at: Timestamp
    exceptions: Exceptions


def _evaluate_in_child(
    model: Model,
    inputs: InputSnapshot,
    assumptions: AssumptionSet,
    context: object,
    *,
    rules: tuple[Rule, ...],
    reference: Reference | None,
    calculate: Calculate | None,
) -> ModelRun:
    descriptor = model.describe()
    output_ids = tuple(item.output_id for item in descriptor.outputs)
    run = _RunContext.model_validate(context)
    return evaluate_run(
        descriptor,
        inputs,
        assumptions,
        run_id="pending",
        owner_id=run.owner_id,
        created_at=run.created_at,
        rules=rules,
        reference=reference,
        exceptions=run.exceptions,
        calculate=calculate
        if calculate is not None
        else _whole_method(model.calculate, output_ids),
    )


def _whole_method(
    calculate: Callable[[InputSnapshot, AssumptionSet], CandidateResult],
    output_ids: tuple[str, ...],
) -> Calculate:
    def evaluate(
        inputs: InputSnapshot,
        assumptions: AssumptionSet,
        eligible: tuple[str, ...],
    ) -> CandidateResult:
        if eligible == output_ids:
            return calculate(inputs, assumptions)
        # Legacy calculators cannot safely run when any of their outputs is blocked.
        return CandidateResult(
            outputs=tuple(
                CandidateOutput(
                    output_id=output_id,
                    value=None,
                    reason="Method requires a subset-aware calculator",
                )
                for output_id in eligible
            )
        )

    return evaluate
