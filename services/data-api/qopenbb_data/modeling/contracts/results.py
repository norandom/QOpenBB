"""Model results and immutable evaluation evidence."""

from graphlib import TopologicalSorter
from hashlib import sha256
from json import dumps
from typing import Annotated, Literal, Self

from pydantic import Field, model_validator

from .checks import CheckOutcome, PolicyException
from .common import (
    Contract,
    Description,
    Identifier,
    References,
    Scalar,
    ScalarKind,
    Timestamp,
    parse_scalar_fields,
    require_subset,
    require_unique,
)
from .descriptors import ModelDescriptor, OutputDescriptor
from .inputs import AssumptionSet, InputSnapshot
from .trace import TraceEntry

OutputStatus = Literal["verified", "unverified", "withheld"]


class OutputResult(Contract):
    output_id: Identifier
    semantic_definition: Description
    unit: Identifier
    value_type: ScalarKind = "decimal"
    value: Scalar | None
    status: OutputStatus
    reason: Description | None = None
    trace_ids: References = ()
    check_ids: References = ()
    exception_ids: References = ()

    @model_validator(mode="before")
    @classmethod
    def validate_typed_value(cls, fields: object) -> object:
        return parse_scalar_fields(fields, default_kind="decimal")

    @model_validator(mode="after")
    def validate_status(self) -> Self:
        if (self.value is None) != (self.status == "withheld"):
            raise ValueError("only withheld outputs have null values")
        if self.status != "verified" and self.reason is None:
            raise ValueError("an unverified or withheld output requires a reason")
        if self.status == "verified" and (not self.trace_ids or self.exception_ids):
            raise ValueError("verified outputs require trace and cannot carry a policy exception")
        return self


class VerificationEvidence(Contract):
    output_id: Identifier
    reference_version: Identifier
    input_fingerprint: Identifier
    assumption_fingerprint: Identifier
    descriptor_fingerprint: Identifier
    output_fingerprint: Identifier
    status: Literal["match", "mismatch", "unavailable"]
    explanation: Description

    @staticmethod
    def fingerprint_output(
        output: OutputResult, trace: tuple[TraceEntry, ...], checks: tuple[CheckOutcome, ...]
    ) -> str:
        """Hash the final output and its referenced evidence before building the run."""
        entries = {entry.trace_id: entry for entry in trace}
        outcomes = {check.rule_id: check for check in checks}
        payload = {
            "output": output.model_dump(mode="json"),
            "trace": [entries[trace_id].model_dump(mode="json") for trace_id in output.trace_ids],
            "checks": [outcomes[rule_id].model_dump(mode="json") for rule_id in output.check_ids],
        }
        return sha256(dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


class ModelRun(Contract):
    schema_version: Literal["1"] = "1"
    run_id: Identifier
    owner_id: Identifier
    created_at: Timestamp
    descriptor: ModelDescriptor
    inputs: InputSnapshot
    assumptions: AssumptionSet
    outputs: Annotated[tuple[OutputResult, ...], Field(min_length=1, max_length=256)]
    trace: Annotated[tuple[TraceEntry, ...], Field(max_length=1024)] = ()
    checks: Annotated[tuple[CheckOutcome, ...], Field(max_length=256)] = ()
    exceptions: Annotated[tuple[PolicyException, ...], Field(max_length=256)] = ()
    verification: Annotated[tuple[VerificationEvidence, ...], Field(max_length=256)] = ()

    @model_validator(mode="after")
    def validate_evidence(self) -> Self:
        if (self.inputs.schema_id, self.inputs.schema_version) != (
            self.descriptor.input_schema_id, self.descriptor.input_schema_version
        ):
            raise ValueError("run input schema is incompatible with the descriptor")
        outputs = {output.output_id: output for output in self.outputs}
        require_unique(tuple(output.output_id for output in self.outputs), "run output ID")
        require_unique(tuple(entry.trace_id for entry in self.trace), "trace ID")
        require_unique(tuple(check.rule_id for check in self.checks), "check outcome")
        require_unique(tuple(item.exception_id for item in self.exceptions), "policy exception ID")
        require_unique(tuple(item.output_id for item in self.verification), "verification output")
        definitions = {output.output_id: output for output in self.descriptor.outputs}
        require_subset(tuple(outputs), set(definitions), "run outputs")
        self.validate_trace(outputs)
        self.validate_checks(set(outputs))
        self.validate_withholding(outputs, definitions)
        for output in self.outputs:
            self.validate_output(output, definitions[output.output_id], outputs)
        self.validate_verification(outputs)
        return self

    def validate_trace(self, outputs: dict[str, OutputResult]) -> None:
        inputs = {table.table_id for table in self.inputs.tables}
        record_tables = {
            row.record_id: table.table_id for table in self.inputs.tables for row in table.rows
        }
        assumptions = {item.assumption_id for item in self.assumptions.assumptions}
        output_ids = set(outputs)
        for entry in self.trace:
            require_subset((entry.output_id,), output_ids, "trace result")
            require_subset(entry.input_ids, inputs, "trace inputs")
            cited_tables = set(entry.input_ids)
            if any(record_tables.get(record_id) not in cited_tables for record_id in entry.source_record_ids):
                raise ValueError("trace source records must belong to cited input tables")
            require_subset(entry.assumption_ids, assumptions, "trace assumptions")
            require_subset(entry.check_ids, set(outputs[entry.output_id].check_ids), "trace checks")

    def validate_checks(self, output_ids: set[str]) -> None:
        rules = {rule.rule_id: rule for rule in self.descriptor.rules}
        checks = {check.rule_id: check for check in self.checks}
        snapshot_inputs = {table.table_id for table in self.inputs.tables}
        require_subset(tuple(checks), set(rules), "run checks")
        for check in self.checks:
            rule = rules[check.rule_id]
            if (check.rule_version, check.severity) != (rule.version, rule.severity):
                raise ValueError("check outcome differs from its rule version or severity")
            require_subset(check.input_ids, set(self.descriptor.input_ids), "check inputs")
            if check.status == "pass":
                require_subset(check.input_ids, snapshot_inputs, "passing check snapshot inputs")
            require_subset(check.output_ids, output_ids, "check outputs")
        for exception in self.exceptions:
            check = checks.get(exception.rule_id)
            if check is None or check.status != "fail" or (
                check.rule_version != exception.rule_version
                or rules[check.rule_id].exception_policy_version != exception.policy_version
            ):
                raise ValueError("policy exception requires a failed check and matching rule policy")
            require_subset(exception.output_ids, set(check.output_ids), "exception outputs")

    def validate_withholding(
        self, outputs: dict[str, OutputResult], definitions: dict[str, OutputDescriptor]
    ) -> None:
        authorized = {
            (exception.rule_id, output_id)
            for exception in self.exceptions
            for output_id in exception.output_ids
        }
        for check in self.checks:
            if (check.severity, check.status) != ("blocking", "fail"):
                continue
            for output_id in check.output_ids:
                if (check.rule_id, output_id) not in authorized and outputs[output_id].status != "withheld":
                    raise ValueError("blocking failure requires a withheld output")

        withheld = {output.output_id for output in outputs.values() if output.status == "withheld"}
        graph = {output_id: definition.required_output_ids for output_id, definition in definitions.items()}
        for output_id in TopologicalSorter(graph).static_order():
            if withheld.intersection(graph[output_id]):
                if output_id in outputs and outputs[output_id].status != "withheld":
                    raise ValueError("withheld dependency requires a withheld output")
                withheld.add(output_id)

    def validate_verification(self, outputs: dict[str, OutputResult]) -> None:
        if not self.verification:
            return
        fingerprints = (
            self.inputs.fingerprint(), self.assumptions.fingerprint(), self.descriptor.fingerprint()
        )
        for evidence in self.verification:
            output = outputs.get(evidence.output_id)
            if output is None or evidence.reference_version != self.descriptor.reference_version:
                raise ValueError("unknown verification output or incompatible reference version")
            if fingerprints != (
                evidence.input_fingerprint, evidence.assumption_fingerprint,
                evidence.descriptor_fingerprint,
            ) or evidence.fingerprint_output(output, self.trace, self.checks) != evidence.output_fingerprint:
                raise ValueError("verification fingerprints do not match the saved run")
            if evidence.status == "mismatch" and output.status != "withheld":
                raise ValueError("reference mismatch requires a withheld output")

    def validate_output(
        self, output: OutputResult, definition: OutputDescriptor, outputs: dict[str, OutputResult]
    ) -> None:
        if (output.unit, output.value_type, output.semantic_definition) != (
            definition.unit, definition.value_type, definition.semantic_definition
        ):
            raise ValueError("output semantics differ from the descriptor")
        output_id = output.output_id
        affected_checks = {check.rule_id: check for check in self.checks if output_id in check.output_ids}
        affected_exceptions = {item.exception_id for item in self.exceptions if output_id in item.output_ids}
        trace_ids = {entry.trace_id for entry in self.trace if entry.output_id == output_id}
        if set(output.trace_ids) != trace_ids:
            raise ValueError("output must reference exactly its trace entries")
        if set(output.check_ids) != set(affected_checks):
            raise ValueError("output must reference exactly its affecting checks")
        evaluated_required_checks = tuple(
            check.rule_id for check in self.checks if check.rule_id in definition.required_check_ids
        )
        require_subset(evaluated_required_checks, set(affected_checks), "required affecting checks")
        if set(output.exception_ids) != affected_exceptions:
            raise ValueError("output must reference its affecting policy exceptions")
        if output.status != "verified":
            return
        require_subset(definition.required_input_ids, {table.table_id for table in self.inputs.tables}, "required inputs")
        require_subset(definition.required_output_ids, {
            other.output_id for other in outputs.values() if other.status == "verified"
        }, "required verified outputs")
        require_subset(definition.required_check_ids, set(output.check_ids), "required check references")
        check_ids = set(definition.required_check_ids) | {
            check.rule_id for check in affected_checks.values() if check.severity == "blocking"
        }
        if any(affected_checks[check_id].status != "pass" for check_id in check_ids):
            raise ValueError("non-passing required check prevents verified output")
        if not any(item.output_id == output_id and item.status == "match" for item in self.verification):
            raise ValueError("verified output requires matching reference evidence")
