"""Admit raw HTTP inputs against the exact installed native query variant."""

import re
from datetime import date
from typing import get_args
from urllib.parse import urlencode

from openbb_core.app.parameter_admission import accepted_names, opted_in
from openbb_core.provider.utils.financial_errors import (
    FinancialError,
    FinancialErrorCode,
)
from pydantic import ValidationError


def _invalid():
    return FinancialError(FinancialErrorCode.INVALID_PARAMETERS)


def _controls(dependant):
    """Read query controls from concrete FastAPI dependency descriptors only."""
    controls = {field.alias for field in dependant.query_params}
    for child in dependant.dependencies:
        if child.name not in {'standard_params', 'extra_params', 'provider_choices'}:
            controls.update(_controls(child))
    return frozenset(controls | {'provider'})


def compile_queries(document, registry, routes):
    """Bind projected operations to their original models and concrete routes."""
    operations = {}
    for route in routes:
        dataset = (getattr(route, 'openapi_extra', None) or {}).get('model')
        variants = registry.original_models.get(dataset, {})
        query = variants.get('fmp', {}).get('query')
        if query is None or not opted_in(query, 'fmp'):
            continue
        for method in route.methods or ():
            operation = document.get('paths', {}).get(route.path, {}).get(method.lower(), {})
            descriptor = operation.get('x-qopenbb-financial', {})
            if descriptor.get('dataset') != dataset or descriptor.get('provider_policy') != 'explicit':
                raise ValueError('Strict financial route requires matching explicit projection')
            operations[route.path, method] = (query, _controls(route.dependant))
    return operations


def _http_value(info, value):
    types = set(get_args(info.annotation) or (info.annotation,))
    if int in types:
        if not re.fullmatch(r'[+-]?[0-9]+', value.strip()):
            raise _invalid()
        try:
            return int(value)
        except ValueError:
            raise _invalid() from None
    if date in types and not re.fullmatch(r'[0-9]{4}-[0-9]{2}-[0-9]{2}', value):
        raise _invalid()
    return value


def admit_query(parameters, query, controls):
    """Return canonical effective values for native dependency parsing and execution."""
    names = accepted_names(query)
    financial, native, seen = {}, {}, set()
    for key, values in parameters.items():
        if len(values) != 1:
            raise _invalid()
        if key in controls:
            native[key] = values[0]
            continue
        canonical = names.get(key)
        if canonical is None or canonical in seen:
            raise _invalid()
        seen.add(canonical)
        financial[key] = _http_value(query.model_fields[canonical], values[0])
    try:
        effective = query.model_validate(financial).model_dump(mode='json')
    except (ValidationError, ValueError, TypeError):
        raise _invalid() from None
    native.update({key: value for key, value in effective.items() if value is not None})
    return urlencode(native).encode('ascii')
