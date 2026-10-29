"""Enforce installed financial provider selection before native execution."""

from urllib.parse import parse_qs

from openbb_core.provider.utils.financial_errors import (
    FinancialError,
    FinancialErrorCode,
)
from starlette._utils import get_route_path
from starlette.types import ASGIApp, Receive, Scope, Send

from qopenbb_data.financial_errors import financial_error_response


def _compile(document: dict) -> dict[tuple[str, str], frozenset[str]]:
    operations = {}
    for path, path_item in document.get("paths", {}).items():
        for method, operation in path_item.items():
            if method not in {"get", "put", "post", "delete", "options", "head", "patch", "trace"}:
                continue
            if not isinstance(operation, dict) or "x-qopenbb-financial" not in operation:
                continue
            descriptor = operation["x-qopenbb-financial"]
            if not isinstance(descriptor, dict):
                raise TypeError("Financial operation requires a policy descriptor")
            policy = descriptor.get("provider_policy")
            choices = descriptor.get("providers")
            if policy not in ("explicit", "baseline_default"):
                raise ValueError("Financial operation has an invalid provider policy")
            if (not isinstance(choices, list) or not choices
                    or any(not isinstance(value, str) or not value or value.strip() != value
                           for value in choices)
                    or len(set(choices)) != len(choices)):
                raise ValueError("Financial operation has invalid provider choices")
            if policy == "explicit":
                operations[path, method.upper()] = frozenset(choices)
    return operations


class FinancialProviderPolicy:
    """Compile projected exact operations; preserve native defaults and dispatch."""

    def __init__(self, app: ASGIApp, *, document: dict):
        self.app = app
        self.operations = _compile(document)

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] == "http":
            choices = self.operations.get((get_route_path(scope), scope["method"]))
            if choices is not None:
                # Decoding is for validation only; downstream receives the original scope.
                parameters = parse_qs(scope.get("query_string", b"").decode("latin-1"),
                                      keep_blank_values=True)
                selected = parameters.get("provider", [])
                if len(selected) != 1 or selected[0] not in choices:
                    response = financial_error_response(
                        FinancialError(FinancialErrorCode.INVALID_PARAMETERS),
                        locations=(("query", "provider"),),
                    )
                    await response(scope, receive, send)
                    return
        await self.app(scope, receive, send)
