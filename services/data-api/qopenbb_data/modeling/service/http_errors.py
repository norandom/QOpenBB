"""Safe HTTP errors for the modeling service."""

from uuid import uuid4

from fastapi.responses import JSONResponse
from pydantic import ValidationError

from .evaluation import EvaluationRequest

_MAX_FIELDS = 32
_SCHEMA = EvaluationRequest.model_json_schema()
_FIELD_NAMES = frozenset(
    field
    for schema in (_SCHEMA, *_SCHEMA.get("$defs", {}).values())
    for field in schema.get("properties", {})
)
_INPUT_FAILURE_FIELDS = {
    "horizon_limit": "assumptions",
    "invalid_assumptions": "assumptions",
    "invalid_input_snapshot": "inputs",
    "input_schema_mismatch": "inputs",
    "row_limit": "inputs",
    "scenario_limit": "assumptions",
    "unsupported_numeric_conversion": "inputs",
}


def failure(
    status: int,
    code: str,
    fields: list[dict] | None = None,
    *,
    retryable: bool | None = None,
    run_id: str | None = None,
) -> JSONResponse:
    content = {
        "code": code,
        "correlation_id": uuid4().hex,
        "retryable": status == 503 if retryable is None else retryable,
    }
    if fields is not None:
        content["fields"] = fields
    if run_id is not None:
        content["run_id"] = run_id
    headers = {"WWW-Authenticate": "Bearer"} if status == 401 else None
    return JSONResponse(status_code=status, content=content, headers=headers)


def validation_failure(error: ValidationError) -> JSONResponse:
    fields = []
    for issue in error.errors(
        include_url=False, include_context=False, include_input=False
    )[:_MAX_FIELDS]:
        code = issue["type"]
        location = issue["loc"]
        if code == "extra_forbidden":
            location = location[:-1]
        path = []
        for element in location:
            if not isinstance(element, int) and element not in _FIELD_NAMES:
                break
            path.append(element)
        fields.append({"path": path, "code": code})
    return failure(422, "invalid_request", fields)


def execution_failure(code: str) -> JSONResponse:
    if field := _INPUT_FAILURE_FIELDS.get(code):
        return failure(422, code, [{"path": [field], "code": code}])
    if code == "request_limit":
        return failure(413, "request_too_large")
    if code in ("capacity", "cancelled", "timeout"):
        return failure(503, code)
    return failure(503, "evaluation_unavailable")
