"""Supplied-input calculation interface and pre-verification results."""

from typing import Annotated, Protocol, Self

from pydantic import Field, model_validator

from ..contracts.common import (
    Contract,
    Description,
    Identifier,
    Scalar,
    ScalarKind,
    parse_scalar_fields,
    require_unique,
)
from ..contracts.descriptors import ModelDescriptor
from ..contracts.inputs import AssumptionSet, InputSnapshot
from ..contracts.trace import TraceEntry


class CandidateOutput(Contract):
    output_id: Identifier
    value_type: ScalarKind = "decimal"
    value: Scalar | None
    reason: Description | None = None

    @model_validator(mode="after")
    def validate_reason(self) -> Self:
        if self.reason is not None and self.value is not None:
            raise ValueError("a withheld reason requires a missing candidate value")
        return self

    @model_validator(mode="before")
    @classmethod
    def validate_typed_value(cls, fields: object) -> object:
        return parse_scalar_fields(fields, default_kind="decimal")


class CandidateResult(Contract):
    """Calculated values and trace awaiting checks and independent verification."""

    outputs: Annotated[tuple[CandidateOutput, ...], Field(max_length=256)]
    trace: Annotated[tuple[TraceEntry, ...], Field(max_length=1024)] = ()

    @model_validator(mode="after")
    def validate_identity(self) -> Self:
        require_unique(tuple(output.output_id for output in self.outputs), "candidate output ID")
        require_unique(tuple(entry.trace_id for entry in self.trace), "trace ID")
        return self


class Model(Protocol):
    """A supplied-input method with a stable descriptor for its installed version."""

    def describe(self) -> ModelDescriptor: ...

    def calculate(self, inputs: InputSnapshot, assumptions: AssumptionSet) -> CandidateResult: ...
