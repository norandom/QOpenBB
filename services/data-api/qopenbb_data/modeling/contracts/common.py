"""Immutable boundary types and exact financial scalar encoding."""

import re
from datetime import UTC, date, datetime
from decimal import Decimal
from hashlib import sha256
from typing import Annotated, Literal

from pydantic import (
    AfterValidator,
    BaseModel,
    BeforeValidator,
    ConfigDict,
    Field,
    PlainSerializer,
    StrictBool,
    StringConstraints,
    ValidatorFunctionWrapHandler,
    WithJsonSchema,
    WrapValidator,
)

Identifier = Annotated[str, StringConstraints(strict=True, min_length=1, max_length=128, pattern=r"\S")]
Description = Annotated[str, StringConstraints(strict=True, min_length=1, max_length=4096, pattern=r"\S")]
References = Annotated[tuple[Identifier, ...], Field(max_length=256)]
ScaleExponent = Annotated[int, Field(strict=True, ge=-18, le=18)]
Currency = Annotated[str, StringConstraints(strict=True, pattern=r"^[A-Z]{3}$")]

_DECIMAL_PATTERN = r"^-?(?:0|[1-9][0-9]*)(?:\.[0-9]+)?$"
_DECIMAL_SCHEMA = {"type": "string", "pattern": _DECIMAL_PATTERN, "maxLength": 78}


def canonical_decimal(value: Decimal) -> str:
    if value.is_zero():
        return "0"
    fixed = format(value, "f")
    return fixed.rstrip("0").rstrip(".") if "." in fixed else fixed


def parse_decimal(value: object) -> Decimal:
    if isinstance(value, str) and len(value) <= 78 and re.fullmatch(_DECIMAL_PATTERN, value):
        value = Decimal(value)
    if not isinstance(value, Decimal) or not value.is_finite():
        raise ValueError("provide a finite Decimal or fixed-point decimal string")
    if value.is_zero():
        return Decimal(0)
    if not -38 <= value.adjusted() <= 37:
        raise ValueError("decimal magnitude is outside the supported range")
    # Check scale and significant digits without applying the active Decimal context.
    sign, digits, exponent = value.as_tuple()
    significant_digits = len(digits)
    while digits[significant_digits - 1] == 0:
        significant_digits -= 1
    scale = max(0, -int(exponent) - len(digits) + significant_digits)
    if scale > 38 or significant_digits > 38:
        raise ValueError("decimal exceeds 38 significant digits or 38 fractional places")
    canonical_exponent = int(exponent) + len(digits) - significant_digits
    return Decimal((sign, digits[:significant_digits], canonical_exponent))


FinancialDecimal = Annotated[
    Decimal,
    BeforeValidator(parse_decimal),
    PlainSerializer(canonical_decimal, return_type=str, when_used="json"),
    WithJsonSchema(_DECIMAL_SCHEMA),
]


def parse_financial_date(value: object) -> date:
    if type(value) is date:
        return value
    if isinstance(value, str) and re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", value):
        return date.fromisoformat(value)
    raise ValueError("provide a calendar date")


def parse_timestamp(value: object) -> object:
    if isinstance(value, datetime) or (
        isinstance(value, str) and re.match(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}T", value)
    ):
        return value
    raise ValueError("provide a timestamp with a UTC offset")


def utc_timestamp(value: datetime) -> datetime:
    if value.utcoffset() is None:
        raise ValueError("timestamp requires a UTC offset")
    return value.astimezone(UTC)


FinancialDate = Annotated[date, BeforeValidator(parse_financial_date)]
Timestamp = Annotated[datetime, BeforeValidator(parse_timestamp), AfterValidator(utc_timestamp)]


class Contract(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, revalidate_instances="always")

    def fingerprint(self) -> str:
        """Hash the versioned wire representation, including ordered evidence."""
        return sha256(self.model_dump_json().encode("utf-8")).hexdigest()


def require_unique(values: tuple, label: str) -> None:
    if len(set(values)) != len(values):
        raise ValueError(f"duplicate {label}")


def require_subset(values: tuple[str, ...], allowed: set[str], label: str) -> None:
    if unknown := set(values) - allowed:
        raise ValueError(f"unknown {label}: {sorted(unknown)}")


ScalarKind = Literal["decimal", "integer", "boolean", "text", "date"]
BoundedInteger = Annotated[int, Field(strict=True, ge=-(2**63), lt=2**63)]


def serialize_scalar(value: Decimal | int | bool | str | date | None) -> str | int | bool | None:
    if isinstance(value, Decimal):
        return canonical_decimal(value)
    if isinstance(value, date):
        return value.isoformat()
    return value


def validate_scalar(value: object, handler: ValidatorFunctionWrapHandler) -> object:
    # Decimal and date strings are decoded by the declared kind before union validation.
    # Keep text lexically intact when validating JSON directly.
    if isinstance(value, str):
        if not value.strip() or len(value) > 4096:
            raise ValueError("text scalar requires 1 to 4096 characters")
        return value
    return handler(value)


Scalar = Annotated[
    FinancialDecimal | BoundedInteger | StrictBool | Description | FinancialDate,
    WrapValidator(validate_scalar),
    PlainSerializer(serialize_scalar, when_used="json"),
]


def parse_scalar_fields(fields: object, *, default_kind: ScalarKind) -> object:
    if not isinstance(fields, dict) or fields.get("value") is None:
        return fields
    value = fields["value"]
    match fields.get("value_type", default_kind):
        case "decimal":
            value = parse_decimal(value)
        case "date":
            value = parse_financial_date(value)
        case "integer" if type(value) is not int or not -(2**63) <= value < 2**63:
            raise ValueError("integer scalar requires a signed 64-bit integer")
        case "boolean" if type(value) is not bool:
            raise ValueError("boolean scalar requires a boolean")
        case "text" if not isinstance(value, str):
            raise ValueError("text scalar requires a string")
    return fields | {"value": value}
