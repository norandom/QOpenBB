"""Versioned model applicability and explicit output dependencies."""

from graphlib import CycleError, TopologicalSorter
from typing import Annotated, Self

from pydantic import Field, model_validator

from .checks import RuleDescriptor
from .common import (
    Contract,
    Description,
    Identifier,
    References,
    ScalarKind,
    require_subset,
    require_unique,
)


class ParameterDefinition(Contract):
    parameter_id: Identifier
    value_type: ScalarKind
    description: Description
    unit: Identifier | None = None


class OutputDescriptor(Contract):
    output_id: Identifier
    semantic_definition: Description
    unit: Identifier
    value_type: ScalarKind = "decimal"
    required_input_ids: References = ()
    required_check_ids: References = ()
    required_output_ids: References = ()


class ModelDescriptor(Contract):
    model_id: Identifier
    method_version: Identifier
    input_schema_id: Identifier
    input_schema_version: Identifier = "1"
    output_schema_id: Identifier
    output_schema_version: Identifier = "1"
    rule_set_version: Identifier
    reference_version: Identifier
    entity_types: Annotated[References, Field(min_length=1)]
    period_types: Annotated[References, Field(min_length=1)]
    input_ids: References
    parameters: Annotated[tuple[ParameterDefinition, ...], Field(max_length=256)] = ()
    rules: Annotated[tuple[RuleDescriptor, ...], Field(max_length=256)] = ()
    outputs: Annotated[tuple[OutputDescriptor, ...], Field(min_length=1, max_length=256)]

    @model_validator(mode="after")
    def validate_dependencies(self) -> Self:
        rule_ids = tuple(rule.rule_id for rule in self.rules)
        output_ids = tuple(output.output_id for output in self.outputs)
        require_unique(self.input_ids, "input ID")
        require_unique(rule_ids, "rule ID")
        require_unique(output_ids, "output ID")
        require_unique(tuple(parameter.parameter_id for parameter in self.parameters), "parameter ID")
        inputs, checks, outputs = set(self.input_ids), set(rule_ids), set(output_ids)
        for output in self.outputs:
            require_subset(output.required_input_ids, inputs, "input dependencies")
            require_subset(output.required_check_ids, checks, "check dependencies")
            require_subset(output.required_output_ids, outputs, "output dependencies")
        graph = {output.output_id: output.required_output_ids for output in self.outputs}
        try:
            TopologicalSorter(graph).prepare()
        except CycleError as exc:
            raise ValueError("cyclic output dependencies") from exc
        return self
