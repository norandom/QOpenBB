"""Bounded, hook-free transport for supplied input contracts."""

import json
from collections.abc import Callable
from datetime import date, datetime, timezone
from decimal import Decimal
from typing import BinaryIO
from zoneinfo import ZoneInfo

from ..contracts.inputs import (
    Assumption,
    AssumptionSet,
    EvaluationCutoff,
    FinancialContext,
    InputSnapshot,
    Observation,
    ObservationTable,
    SourceProvenance,
    Transformation,
)

CHUNK_BYTES = 64 * 1024
MAX_REQUEST_BYTES = 64 * 1024 * 1024
MAX_RESULT_BYTES = 16 * 1024 * 1024

_CONTRACT_TYPES = (
    Assumption,
    AssumptionSet,
    EvaluationCutoff,
    FinancialContext,
    InputSnapshot,
    Observation,
    ObservationTable,
    SourceProvenance,
    Transformation,
)


class InvalidWireValue(ValueError):
    """A request value is outside the supported input contract representation."""


class RequestTooLarge(ValueError):
    """The private request payload exceeds its byte budget."""


class InputWriter:
    def __init__(self, stream: BinaryIO, checkpoint: Callable[[], object]) -> None:
        self._stream = stream
        self._checkpoint = checkpoint
        self._bytes = 0

    def write_value(self, value: object, depth: int = 0) -> None:
        self._checkpoint()
        if depth > 16:
            raise InvalidWireValue
        kind = type(value)
        if any(kind is contract for contract in _CONTRACT_TYPES):
            value = vars(value)
            kind = dict
        if kind is dict:
            self._write_object(value, depth)
        elif kind is tuple or kind is list:
            self._write_array(value, depth)
        else:
            self._write(_encode_scalar(value))

    def _write_object(self, value: dict, depth: int) -> None:
        if len(value) > 128:
            raise InvalidWireValue
        self._write(b"{")
        for index, (key, field) in enumerate(value.items()):
            if type(key) is not str:
                raise InvalidWireValue
            if index:
                self._write(b",")
            self._write(_encode_scalar(key))
            self._write(b":")
            self.write_value(field, depth + 1)
        self._write(b"}")

    def _write_array(self, value: tuple | list, depth: int) -> None:
        if len(value) > 10_000:
            raise InvalidWireValue
        self._write(b"[")
        for index, item in enumerate(value):
            if index:
                self._write(b",")
            self.write_value(item, depth + 1)
        self._write(b"]")

    def end_document(self) -> None:
        self._write(b"\n")

    def _write(self, chunk: bytes) -> None:
        self._bytes += len(chunk)
        if self._bytes > MAX_REQUEST_BYTES:
            raise RequestTooLarge
        self._stream.write(chunk)


def _encode_scalar(value: object) -> bytes:
    kind = type(value)
    if kind is Decimal:
        _, digits, exponent = value.as_tuple()
        if type(exponent) is not int or len(digits) > 256 or abs(exponent) > 256:
            raise InvalidWireValue
        value = format(value, "f")
    elif kind is datetime:
        tz_kind = type(value.tzinfo)
        if (
            tz_kind is not timezone
            and tz_kind is not ZoneInfo
            and value.tzinfo is not None
        ):
            raise InvalidWireValue
        value = value.isoformat()
    elif kind is date:
        value = value.isoformat()
    elif kind is int:
        if value.bit_length() > 64:
            raise InvalidWireValue
    elif kind is not str and kind is not bool and value is not None:
        raise InvalidWireValue
    if type(value) is str and len(value) > 4096:
        raise InvalidWireValue
    return json.dumps(value, ensure_ascii=True).encode("ascii")
