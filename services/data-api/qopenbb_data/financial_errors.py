"""Install scoped safe failures on the native API without changing legacy routes."""

import logging
import re

from fastapi.exceptions import RequestValidationError, ResponseValidationError
from openbb_core.app.model.abstract.error import OpenBBError
from openbb_core.provider.utils.errors import EmptyDataError, UnauthorizedError
from openbb_core.provider.utils.financial_errors import (
    MAX_WRAPPER_DEPTH,
    FinancialError,
    parse_retry_after,
)
from openbb_fmp.utils.errors import FMPEmptyData, FMPError, FMPUnauthorized
from pydantic import ValidationError
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from starlette.routing import compile_path

_LOG = logging.getLogger("qopenbb.financial")
_NAME = re.compile(r"[A-Za-z_][A-Za-z0-9_]{0,79}\Z")


def financial_error_response(
    error: FinancialError, *, status_code: int | None = None,
    locations: tuple[tuple[str, ...], ...] = (),
) -> Response:
    """Serialize fixed public fields and validated retry advice only."""
    if type(error) is not FinancialError:
        raise TypeError("Expected a FinancialError")
    if status_code is not None and (type(status_code) is not int or
                                    status_code not in {204, 400, 422, 500, 502}):
        raise ValueError("Unsupported financial status override")
    safe = FinancialError(error.code, provider=error.provider,
                          retry_after_seconds=error.retry_after_seconds)
    if safe.correlation_id and type(error.correlation_id) is str and re.fullmatch(
        r"[0-9a-f]{32}", error.correlation_id
    ):
        safe.correlation_id = error.correlation_id
    status = safe.status_code if status_code is None else status_code
    if status == 204:
        return Response(status_code=204)
    content = safe.to_dict()
    if locations:
        if any(len(loc) != 2 or loc[0] not in {"query", "path", "header", "cookie"}
               or type(loc[1]) is not str or not _NAME.fullmatch(loc[1]) for loc in locations):
            raise ValueError("Unsafe financial field location")
        content["errors"] = [{"loc": list(loc), "msg": "Invalid parameter."}
                             for loc in sorted(set(locations))]
    retry = parse_retry_after(safe.retry_after_seconds)
    headers = {"Retry-After": str(retry)} if retry is not None else {}
    return JSONResponse(content, status_code=status, headers=headers)


def _unwrap(error):
    seen = set()
    for _ in range(MAX_WRAPPER_DEPTH + 1):
        if id(error) in seen:
            return None
        seen.add(id(error))
        if type(error) is not OpenBBError:
            return error
        error = error.original
    return None


def _classify(error):
    current = _unwrap(error)
    if type(error) is OpenBBError and type(current) is str:
        return FinancialError("upstream"), 400
    if type(current) is FinancialError:
        return FinancialError(current.code, provider=current.provider,
                              retry_after_seconds=current.retry_after_seconds), None
    if type(current) in {FMPError, FMPUnauthorized, FMPEmptyData}:
        status = 204 if type(current) is FMPEmptyData else (
            502 if type(current) is FMPUnauthorized else 400)
        fallback = {204: "missing_data", 502: "authentication", 400: "upstream"}[status]
        return FinancialError(getattr(current, "code", fallback), provider="fmp",
                              retry_after_seconds=getattr(current, "retry_after_seconds", None)), status
    if type(current) is EmptyDataError:
        return FinancialError("missing_data"), 204
    if type(current) is UnauthorizedError:
        return FinancialError("authentication"), 502
    if isinstance(current, RequestValidationError):
        return FinancialError("invalid_parameters"), 422
    if isinstance(current, (ResponseValidationError, ValidationError)):
        # Query/result helper failures already carry explicit FinancialError codes.
        return FinancialError("invalid_response"), 502
    return FinancialError("internal_error"), 500


def _resolve(document, value):
    seen = set()
    while "$ref" in value:
        reference = value["$ref"]
        if reference in seen or not reference.startswith("#/"):
            raise ValueError("Invalid financial parameter reference")
        seen.add(reference)
        value = document
        for part in reference[2:].split("/"):
            value = value[part.replace("~1", "/").replace("~0", "~")]
    return value


def _operations(document):
    operations = []
    for path, item in document.get("paths", {}).items():
        for method, operation in item.items():
            if not isinstance(operation, dict) or "x-qopenbb-financial" not in operation:
                continue
            parameters = [_resolve(document, p) for p in
                          item.get("parameters", []) + operation.get("parameters", [])]
            locations = {(p.get("in"), p.get("name")) for p in parameters
                         if type(p.get("name")) is str and _NAME.fullmatch(p["name"])}
            providers = operation["x-qopenbb-financial"].get("providers", [])
            operations.append((compile_path(path)[0], method.upper(),
                               operation.get("operationId", "financial"), locations, providers))
    return operations


def _operation(scope, operations):
    # Mounted apps retain the mount prefix in scope.path on current Starlette.
    path = scope.get("path", "")
    root = scope.get("root_path", "")
    if root and path.startswith(root):
        path = path[len(root):] or "/"
    return next((op for op in operations if op[1] == scope.get("method")
                 and op[0].fullmatch(path)), None)


def _response(error, operation):
    safe, status = _classify(error)
    locations = ()
    current = _unwrap(error)
    if isinstance(current, RequestValidationError):
        locations = tuple(tuple(entry.get("loc", ())) for entry in current.errors()
                          if tuple(entry.get("loc", ())) in operation[3])
    if safe.provider not in operation[4]:
        safe = FinancialError(safe.code, retry_after_seconds=safe.retry_after_seconds)
    response = financial_error_response(safe, status_code=status, locations=locations)
    _LOG.error("financial_failure code=%s provider=%s operation=%s correlation_id=%s",
               safe.code.value, safe.provider, operation[2], safe.correlation_id)
    return response


class _FinancialBoundary:
    """Catch before ServerErrorMiddleware can rethrow to raw server logging."""

    def __init__(self, app, operations):
        self.app = app
        self.operations = operations

    async def __call__(self, scope, receive, send):
        operation = _operation(scope, self.operations) if scope["type"] == "http" else None
        if operation is None:
            return await self.app(scope, receive, send)
        started = False
        completed = False
        abort = False

        async def tracked_send(message):
            nonlocal started, completed
            if message["type"] == "http.response.start":
                started = True
            if message["type"] == "http.response.body" and not message.get("more_body", False):
                completed = True
            await send(message)

        try:
            await self.app(scope, receive, tracked_send)
        except Exception as error:  # noqa: BLE001 - boundary must contain unknown provider failures.
            response = _response(error, operation)
            if not started:
                await response(scope, receive, send)
            elif not completed:
                abort = True
        if abort:
            # Leave the raw exception handler before raising: no unsafe context survives.
            raise FinancialError("invalid_response") from None


def install_financial_error_handlers(app, document):
    """Install before startup, preserving handlers outside advertised operations."""
    if app.middleware_stack is not None:
        raise RuntimeError("Install financial handlers before application startup")
    operations = _operations(document)
    originals = dict(app.exception_handlers)

    def scoped_handler(legacy):
        async def handler(request: Request, error):
            operation = _operation(request.scope, operations)
            if operation is not None:
                return _response(error, operation)
            if legacy is None:
                raise error
            return await legacy(request, error)
        return handler

    classes = set(originals) | {OpenBBError, EmptyDataError, UnauthorizedError,
                               RequestValidationError, ResponseValidationError, ValidationError}
    # Generic exceptions belong to the inner boundary, avoiding server rethrows.
    for cls in classes - {Exception, 500}:
        legacy = originals.get(cls)
        if legacy is None and isinstance(cls, type):
            legacy = next((originals[base] for base in cls.__mro__[1:]
                           if base in originals and base is not Exception), None)
        app.add_exception_handler(cls, scoped_handler(legacy))
    app.add_middleware(_FinancialBoundary, operations=operations)
