"""Child entry point for the executor's private, trusted local IPC."""

import json
import os
import pickle
import sys

from pydantic import ValidationError

from ..contracts.inputs import AssumptionSet, InputSnapshot
from ..models.protocol import CandidateResult, Model
from .execution import _WORKER_FAILURES, ExecutionError
from .execution_decimal import UnsupportedNumericConversion
from .execution_transport import MAX_RESULT_BYTES

_EXIT_CODES = {code: status for status, code in _WORKER_FAILURES.items()}


def _validate_inputs(
    model: Model, inputs: object, assumptions: object
) -> tuple[InputSnapshot, AssumptionSet]:
    try:
        inputs = InputSnapshot.model_validate(inputs)
    except ValidationError:
        raise ExecutionError("invalid_input_snapshot") from None
    try:
        assumptions = AssumptionSet.model_validate(assumptions)
    except ValidationError:
        raise ExecutionError("invalid_assumptions") from None

    descriptor = model.describe()
    if (inputs.schema_id, inputs.schema_version) != (
        descriptor.input_schema_id,
        descriptor.input_schema_version,
    ):
        raise ExecutionError("input_schema_mismatch")
    return inputs, assumptions


def main() -> int:
    import polars as pl

    if pl.thread_pool_size() != int(os.environ["POLARS_MAX_THREADS"]):
        return 1

    # Only pre-serialized installed configuration uses pickle. Caller
    # contracts and per-run metadata arrive as JSON documents.
    stream = sys.stdin.buffer
    model, limits = pickle.load(stream)
    job = pickle.load(stream)
    try:
        inputs, assumptions = _validate_inputs(
            model, json.loads(stream.readline()), json.loads(stream.readline())
        )
        limits.check(inputs, assumptions)
    except ExecutionError as error:
        return _EXIT_CODES.get(error.code, 1)

    try:
        if job is None:
            result = CandidateResult.model_validate(
                model.calculate(inputs, assumptions)
            )
        else:
            result = job(model, inputs, assumptions, json.loads(stream.readline()))
    except UnsupportedNumericConversion:
        return _EXIT_CODES["unsupported_numeric_conversion"]
    payload = result.model_dump_json().encode("utf-8")
    if len(payload) > MAX_RESULT_BYTES:
        return _EXIT_CODES["result_limit"]
    sys.stdout.buffer.write(payload)
    return 0


if __name__ == "__main__":
    sys.exit(main())
