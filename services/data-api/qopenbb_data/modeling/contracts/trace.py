"""Readable formula evidence with ordered, unrounded financial values."""

from typing import Annotated, Self

from pydantic import Field, model_validator

from .common import (
    Contract,
    Currency,
    Description,
    FinancialDate,
    FinancialDecimal,
    Identifier,
    References,
    ScaleExponent,
)
from .inputs import Transformation


class TraceValue(Contract):
    name: Identifier
    value: FinancialDecimal
    unit: Identifier
    currency: Currency | None = None
    scale: ScaleExponent = 0
    period_start: FinancialDate | None = None
    period_end: FinancialDate | None = None

    @model_validator(mode="after")
    def validate_period(self) -> Self:
        if self.period_start is not None and (
            self.period_end is None or self.period_start > self.period_end
        ):
            raise ValueError("trace period start requires an end on or after it")
        return self


class TraceEntry(Contract):
    trace_id: Identifier
    formula_id: Identifier
    formula_version: Identifier
    expression: Description
    source_record_ids: References = ()
    input_ids: References = ()
    assumption_ids: References = ()
    substitutions: Annotated[tuple[TraceValue, ...], Field(max_length=256)] = ()
    intermediate_values: Annotated[tuple[TraceValue, ...], Field(max_length=256)] = ()
    transformations: Annotated[tuple[Transformation, ...], Field(max_length=32)] = ()
    output_id: Identifier
    check_ids: References = ()
