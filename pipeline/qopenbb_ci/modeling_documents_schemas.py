"""Generate modeling schemas for the actual JSON wire representations."""

from typing import Annotated, Literal

from pydantic import BaseModel, Field, TypeAdapter
from pydantic.json_schema import GenerateJsonSchema, JsonSchemaMode
from pydantic_core import CoreSchema
from qopenbb_data.modeling.contracts.checks import (
    CheckOutcome,
    PolicyException,
    RuleDescriptor,
)
from qopenbb_data.modeling.contracts.common import (
    BoundedInteger,
    Contract,
    Description,
    FinancialDate,
    FinancialDecimal,
    Identifier,
)
from qopenbb_data.modeling.contracts.descriptors import ModelDescriptor
from qopenbb_data.modeling.contracts.inputs import InputSnapshot
from qopenbb_data.modeling.contracts.results import (
    ModelRun,
    OutputResult,
    VerificationEvidence,
)
from qopenbb_data.modeling.contracts.trace import TraceEntry
from qopenbb_data.modeling.service.evaluation import EvaluationRequest

from .modeling_documents_discovery import AppDiscovery, WidgetDiscovery

DIALECT = "https://json-schema.org/draft/2020-12/schema"
_DECIMAL_PATTERN = TypeAdapter(FinancialDecimal).json_schema()["pattern"]


class SafeFieldError(Contract):
    path: tuple[str | int, ...]
    code: str


class SafeError(Contract):
    code: str
    correlation_id: Annotated[str, Field(pattern=r"^[0-9a-f]{32}$")]
    retryable: bool
    fields: Annotated[tuple[SafeFieldError, ...], Field(max_length=32)] | None = None
    run_id: str | None = None


class DisplayPrecision(Contract):
    transform: Literal["exact_binary64"]
    max_absolute_error: Literal["0"]


class ProjectedOutput(OutputResult):
    display_value: float | None
    display_text: str | None
    freshness: Literal["saved", "matched", "stale"]
    run_detail_href: str
    check_explanations: str | None
    display_numeric: DisplayPrecision


class WidgetProjection(Contract):
    run_id: Identifier
    results: tuple[ProjectedOutput]
    checks: tuple[CheckOutcome, ...]
    trace: tuple[TraceEntry, ...]
    verification: tuple[VerificationEvidence, ...]
    run_detail_href: str
    exceptions: tuple[PolicyException, ...]


class ModelListing(Contract):
    models: tuple[ModelDescriptor, ...]


SCHEMAS: dict[str, tuple[type[BaseModel], JsonSchemaMode]] = {
    "evaluation-request": (EvaluationRequest, "validation"),
    "model-run": (ModelRun, "serialization"),
    "model-descriptor": (ModelDescriptor, "serialization"),
    "rule-descriptor": (RuleDescriptor, "serialization"),
    "model-listing": (ModelListing, "serialization"),
    "input-snapshot": (InputSnapshot, "validation"),
    "widget-projection": (WidgetProjection, "serialization"),
    "safe-error": (SafeError, "serialization"),
    "widgets": (WidgetDiscovery, "serialization"),
    "apps": (AppDiscovery, "serialization"),
}


class WireSchema(GenerateJsonSchema):
    def model_schema(self, schema: CoreSchema) -> dict:
        result = super().model_schema(schema)
        name = schema["cls"].__name__
        if (
            self.mode == "serialization"
            and "properties" in result
            and name != "SafeError"
        ):
            # The saved-run and projection paths dump defaults and explicit nulls.
            result["required"] = list(result["properties"])
        if name in {"Assumption", "OutputResult", "ProjectedOutput"}:
            _typed_scalar(result, self.mode, nullable=name != "Assumption")
        if name in {"OutputResult", "ProjectedOutput"}:
            result["allOf"].extend(_output_status())
        if name == "EvaluationRequest":
            result["oneOf"] = [
                _input_source("inputs", "acquisition"),
                _input_source("acquisition", "inputs"),
            ]
        if name == "SafeError":
            # HTTP errors omit optional members entirely.
            for field in ("fields", "run_id"):
                result["properties"][field] = result["properties"][field]["anyOf"][0]
        return result


def _input_source(present: str, absent: str) -> dict:
    return {
        "required": [present],
        "properties": {
            present: {"type": "object"},
            absent: {"type": "null"},
        },
    }


def _typed_scalar(schema: dict, mode: JsonSchemaMode, *, nullable: bool) -> None:
    shapes = {
        "decimal": TypeAdapter(FinancialDecimal).json_schema(mode=mode),
        "integer": TypeAdapter(BoundedInteger).json_schema(),
        "boolean": {"type": "boolean"},
        "text": TypeAdapter(Description).json_schema(),
        "date": TypeAdapter(FinancialDate).json_schema(),
    }
    # The parent model decodes a lexical value according to its declared kind.
    # Serialization of the Scalar union alone loses those kind constraints.
    schema["properties"]["value"] = {
        "anyOf": [*shapes.values(), *([{"type": "null"}] if nullable else [])],
    }
    schema["allOf"] = [
        {
            "if": {
                "properties": {"value_type": {"const": kind}},
                **({"required": ["value_type"]} if kind != "decimal" else {}),
            },
            "then": {
                "properties": {
                    "value": {"anyOf": [shape, {"type": "null"}]}
                    if nullable
                    else shape,
                },
            },
        }
        for kind, shape in shapes.items()
    ]


def _output_status() -> list[dict]:
    return [
        {
            "if": {"properties": {"status": {"const": "withheld"}}},
            "then": {"properties": {"value": {"type": "null"}}},
            "else": {"properties": {"value": {"not": {"type": "null"}}}},
        },
        {
            "if": {"properties": {"status": {"const": "verified"}}},
            "then": {
                "required": ["trace_ids"],
                "properties": {
                    "trace_ids": {"minItems": 1},
                    "exception_ids": {"maxItems": 0},
                },
            },
            "else": {
                "required": ["reason"],
                "properties": {"reason": {"type": "string"}},
            },
        },
    ]


def _decimal_constraints(node: object, mode: JsonSchemaMode) -> None:
    if isinstance(node, list):
        for item in node:
            _decimal_constraints(item, mode)
    if isinstance(node, dict):
        if node.get("pattern") == _DECIMAL_PATTERN:
            node["pattern"] = _decimal_pattern(mode)
        for item in node.values():
            _decimal_constraints(item, mode)


def _decimal_pattern(mode: JsonSchemaMode) -> str:
    # Bound the canonical digits of the exact value. Request strings may carry
    # trailing fractional zeroes, which the runtime strips before serialization.
    end = r"(?![\s\S])"
    pad = "0*" if mode == "validation" else ""
    zero = r"-?0(?:\.0+)?" if mode == "validation" else "0"
    whole = r"[1-9][0-9]{0,37}"
    if mode == "validation":
        whole += r"(?:\.0+)?"
    fractional = rf"0\.[0-9]{{0,37}}[1-9]{pad}"
    mixed = rf"(?=(?:[0-9]\.?){{1,37}}[1-9]{pad}{end})[1-9][0-9]*\.[0-9]*[1-9]{pad}"
    return rf"^(?:{zero}|-?(?:{whole}|{fractional}|{mixed})){end}"


def standalone_schemas() -> dict[str, dict]:
    schemas = {}
    for name, (model, mode) in SCHEMAS.items():
        schema = {
            "$schema": DIALECT,
            **model.model_json_schema(mode=mode, schema_generator=WireSchema),
        }
        _decimal_constraints(schema, mode)
        schemas[name] = schema
    return schemas
