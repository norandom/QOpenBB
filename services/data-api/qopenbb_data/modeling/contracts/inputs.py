"""Dated financial observations, source provenance and model assumptions."""

from datetime import datetime
from typing import Annotated, Literal, Self
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from pydantic import Field, StrictBool, model_validator

from .common import (
    Contract,
    Currency,
    Description,
    FinancialDate,
    FinancialDecimal,
    Identifier,
    Scalar,
    ScalarKind,
    ScaleExponent,
    Timestamp,
    parse_scalar_fields,
    require_unique,
)


class FinancialContext(Contract):
    unit: Identifier
    currency: Currency | None = None
    scale: ScaleExponent = 0
    quantity: Literal["stock", "flow", "rate", "unknown"] = "unknown"
    basis: Identifier | None = None
    period_start: FinancialDate | None = None
    period_end: FinancialDate | None = None
    fiscal_period: Identifier | None = None
    accounting_standard: Identifier | None = None
    consolidation_scope: Identifier | None = None
    frequency: Identifier | None = None
    seasonal_adjustment: Identifier | None = None
    vintage_coverage: Literal["known", "unknown", "unavailable"] | None = None
    vintage_limitation: Description | None = None

    @model_validator(mode="after")
    def validate_period(self) -> Self:
        if self.period_start is not None and (
            self.period_end is None or self.period_start > self.period_end
        ):
            raise ValueError("period start requires an end on or after it")
        if self.quantity == "flow" and self.period_start is None:
            raise ValueError("flow observations require a measurement interval")
        return self


class Transformation(Contract):
    transformation_id: Identifier
    version: Identifier
    description: Description


class Observation(Contract):
    record_id: Identifier
    entity_id: Identifier
    metric_id: Identifier
    observation_date: FinancialDate
    context: FinancialContext
    value: FinancialDecimal | None
    category: Literal["raw", "provider", "estimate"]
    published_at: Timestamp | None = None
    vintage_at: Timestamp | None = None
    source_record_id: Identifier | None = None
    transformations: Annotated[tuple[Transformation, ...], Field(max_length=32)] = ()


class EvaluationCutoff(Contract):
    observation_date: FinancialDate
    decision_at: Timestamp
    evaluated_at: Timestamp
    session_timezone: Identifier

    @model_validator(mode="after")
    def validate_local_date(self) -> Self:
        try:
            session_timezone = ZoneInfo(self.session_timezone)
        except (ZoneInfoNotFoundError, ValueError) as exc:
            raise ValueError("unknown session time zone") from exc
        if self.decision_at.astimezone(session_timezone).date() != self.observation_date:
            raise ValueError("decision timestamp must fall on the local observation date")
        return self

    @property
    def cutoff_at(self) -> datetime:
        return min(self.decision_at, self.evaluated_at)

    def is_eligible(
        self, observation: Observation, *, return_starts_at: datetime | None = None
    ) -> bool:
        """Require dated evidence available by the cutoff and before any return begins."""
        if observation.observation_date > self.observation_date:
            return False
        if observation.published_at is None or observation.context.vintage_coverage in (
            "unknown", "unavailable"
        ):
            return False
        available_at = max(
            observation.published_at, observation.vintage_at or observation.published_at
        )
        if return_starts_at is not None and return_starts_at.utcoffset() is None:
            raise ValueError("return start requires a UTC offset")
        return available_at <= self.cutoff_at and (
            return_starts_at is None or self.decision_at < return_starts_at
        )


ObservationKey = Literal["entity_id", "metric_id", "observation_date", "vintage_at", "published_at"]


class ObservationTable(Contract):
    table_id: Identifier
    grain: Description
    keys: Annotated[tuple[ObservationKey, ...], Field(min_length=1, max_length=5)]
    nullable: StrictBool
    rows: Annotated[tuple[Observation, ...], Field(max_length=10_000)]

    @model_validator(mode="after")
    def validate_rows(self) -> Self:
        require_unique(self.keys, "table key column")
        require_unique(tuple(row.record_id for row in self.rows), "record ID")
        require_unique(
            tuple(tuple(getattr(row, key) for key in self.keys) for row in self.rows),
            "observation key",
        )
        if not self.nullable and any(row.value is None for row in self.rows):
            raise ValueError("null value in non-nullable observation table")
        return self


class SourceProvenance(Contract):
    origin: Literal["user_supplied", "service_acquired"]
    source: Identifier
    query: Annotated[tuple[tuple[Identifier, Description], ...], Field(max_length=128)]
    retrieved_at: Timestamp
    acquisition_id: Identifier | None = None

    @model_validator(mode="after")
    def validate_origin(self) -> Self:
        require_unique(tuple(name for name, _ in self.query), "query parameter")
        if (self.origin == "service_acquired") != (self.acquisition_id is not None):
            raise ValueError("acquisition identity is required exclusively for service acquisition")
        return self


class InputSnapshot(Contract):
    schema_id: Identifier
    schema_version: Literal["1"] = "1"
    provenance: SourceProvenance
    tables: Annotated[tuple[ObservationTable, ...], Field(min_length=1, max_length=64)]
    cutoff: EvaluationCutoff | None = None

    @model_validator(mode="after")
    def validate_identity(self) -> Self:
        require_unique(tuple(table.table_id for table in self.tables), "table ID")
        record_ids = tuple(row.record_id for table in self.tables for row in table.rows)
        if len(record_ids) > 10_000:
            raise ValueError("snapshot exceeds 10,000 observations")
        require_unique(record_ids, "snapshot record ID")
        return self


class Assumption(Contract):
    assumption_id: Identifier
    value_type: ScalarKind
    value: Scalar
    origin: Literal["user_supplied", "method_default"]
    rationale: Description
    author: Identifier | None = None
    unit: Identifier | None = None
    adjusts_record_id: Identifier | None = None

    @model_validator(mode="before")
    @classmethod
    def validate_typed_value(cls, fields: object) -> object:
        return parse_scalar_fields(fields, default_kind="decimal")

    @model_validator(mode="after")
    def validate_author(self) -> Self:
        if self.origin == "user_supplied" and self.author is None:
            raise ValueError("user-supplied assumptions require an author")
        return self


class AssumptionSet(Contract):
    version: Identifier
    effective_date: FinancialDate
    assumptions: Annotated[tuple[Assumption, ...], Field(max_length=256)] = ()

    @model_validator(mode="after")
    def validate_identity(self) -> Self:
        require_unique(tuple(item.assumption_id for item in self.assumptions), "assumption ID")
        return self
