"""Scope canonical HTTP quarter conversion to already admitted selected queries."""
from contextlib import contextmanager
from contextvars import ContextVar

_CANONICAL_QUARTER = ContextVar('qopenbb_canonical_http_quarter', default=False)


def canonical_quarter(value):
    """Preserve native typed Literals while admitting canonical HTTP digits."""
    if _CANONICAL_QUARTER.get() and type(value) is str and value in ('1', '2', '3', '4'):
        return int(value)
    return value


@contextmanager
def admitted_http_quarter(query):
    """Enable conversion only after strict bounded-int provider admission."""
    from openbb_core.app.parameter_admission import opted_in
    field = query.model_fields.get('quarter')
    enabled = opted_in(query, 'fmp') and field is not None and field.annotation is int
    token = _CANONICAL_QUARTER.set(enabled)
    try:
        yield
    finally:
        _CANONICAL_QUARTER.reset(token)


def prepare_http_quarter(route, query):
    """Retain native Literal schema in the selected route dependency projection."""
    from copy import deepcopy
    from typing import Annotated, get_args

    from fastapi.utils import create_model_field
    from pydantic import BeforeValidator
    field = query.model_fields.get('quarter')
    if (route.openapi_extra or {}).get('model') != 'EarningsCallTranscript':
        return
    if field is None or field.annotation is not int:
        return
    def visit(dependant):
        for index, native in enumerate(dependant.query_params):
            if native.name != 'quarter':
                continue
            if any(isinstance(item, BeforeValidator) and item.func is canonical_quarter
                   for item in (*get_args(native.field_info.annotation), *native.field_info.metadata)):
                continue
            info = deepcopy(native.field_info)
            info.annotation = Annotated[info.annotation, BeforeValidator(canonical_quarter)]
            dependant.query_params[index] = create_model_field(
                name=native.name, type_=info.annotation, field_info=info)
        for child in dependant.dependencies:
            visit(child)
    visit(route.dependant)
