"""Financial rule definitions, verdicts, tolerances and scoped exceptions."""

from typing import Literal, Self

from pydantic import model_validator

from .common import (
    Contract,
    Description,
    FinancialDecimal,
    Identifier,
    References,
    ScaleExponent,
)

CheckStatus = Literal["pass", "fail", "unknown", "error", "not_applicable"]
CheckSeverity = Literal["blocking", "warning"]
CheckStage = Literal["precondition", "invariant", "postcondition"]


class Tolerance(Contract):
    unit: Identifier
    scale: ScaleExponent = 0
    absolute: FinancialDecimal
    relative: FinancialDecimal | None = None

    @model_validator(mode="after")
    def validate_bounds(self) -> Self:
        if self.absolute < 0 or (self.relative is not None and self.relative < 0):
            raise ValueError("tolerance must be nonnegative")
        return self


class RuleDescriptor(Contract):
    rule_id: Identifier
    version: Identifier
    stage: CheckStage
    severity: CheckSeverity
    exception_policy_version: Identifier | None = None


class CheckOutcome(Contract):
    rule_id: Identifier
    rule_version: Identifier
    severity: CheckSeverity
    status: CheckStatus
    input_ids: References = ()
    output_ids: References = ()
    observed: Description | None = None
    expected: Description | None = None
    observed_value: FinancialDecimal | None = None
    expected_value: FinancialDecimal | None = None
    tolerance: Tolerance | None = None
    explanation: Description | None = None

    @model_validator(mode="after")
    def validate_explanation(self) -> Self:
        if self.status != "pass" and self.explanation is None:
            raise ValueError("a non-passing check requires an explanation")
        if (self.observed_value is None) != (self.expected_value is None):
            raise ValueError("numeric evidence requires both observed and expected values")
        if self.observed_value is not None and self.tolerance is None:
            raise ValueError("numeric evidence requires a unit-aware tolerance")
        return self


class PolicyException(Contract):
    exception_id: Identifier
    rule_id: Identifier
    rule_version: Identifier
    author: Identifier
    output_ids: References
    rationale: Description
    policy_version: Identifier

    @model_validator(mode="after")
    def validate_scope(self) -> Self:
        if not self.output_ids:
            raise ValueError("an exception requires an output scope")
        return self
