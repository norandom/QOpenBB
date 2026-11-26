"""Internal ASGI entry point packaged in the analytics runtime."""

import os
from collections.abc import Callable
from dataclasses import dataclass, replace
from functools import partial

from fastapi import FastAPI

from ..contracts.checks import CheckOutcome, RuleDescriptor
from ..contracts.descriptors import OutputDescriptor
from ..contracts.inputs import AssumptionSet, InputSnapshot
from ..models.factors.comparison import ProxyComparisonModel
from ..models.factors.diagnostics import TimingStudyModel
from ..models.factors.fcf_yield import FcfYieldModel, resolve_fcf_inputs
from ..models.factors.method_inputs import price_window
from ..models.factors.momentum import MomentumModel
from ..models.factors.real_yield import RealYieldModel, resolve_yield_inputs
from ..models.factors.sessions import WINDOW_SIZE
from ..models.factors.volatility import VolatilityModel
from ..models.protocol import Model
from ..models.registry import ModelRegistry
from ..validation.lifecycle import Calculate
from ..validation.rules import Rule, RuleContext
from ..verification.factors.etf import (
    comparison_reference,
    momentum_reference,
    volatility_reference,
)
from ..verification.factors.issuer_reference import issuer_reference
from ..verification.factors.regime_reference import regime_reference
from ..verification.factors.timing_reference import timing_reference
from ..verification.reference import Reference
from .acquisition import DataApiSnapshotSource
from .execution import ExecutionLimits
from .http import create_model_app
from .identity import IdentityVerifier
from .orchestrator import MethodBinding, Orchestrator
from .run_store import FileRunStore


def _restore_reference(
    factory: Callable[[], Reference], availability_check_ids: frozenset[str]
) -> Reference:
    return replace(factory(), availability_check_ids=availability_check_ids)


class _WorkerReference(Reference):
    def __init__(
        self, factory: Callable[[], Reference], availability_check_ids: frozenset[str]
    ) -> None:
        reference = factory()
        super().__init__(
            version=reference.version,
            calculations=reference.calculations,
            tolerances=reference.tolerances,
            availability_check_ids=availability_check_ids,
        )
        self._factory = factory

    def __reduce__(
        self,
    ) -> tuple[
        Callable[[Callable[[], Reference], frozenset[str]], Reference],
        tuple[Callable[[], Reference], frozenset[str]],
    ]:
        # Rebuild the exact verifier in the worker, including its per-run cache.
        return _restore_reference, (self._factory, self.availability_check_ids)


type _SelectInputs = Callable[[InputSnapshot, AssumptionSet], object]
type _InputIssues = Callable[[InputSnapshot, AssumptionSet], dict[str, str]]


def _shared_input_issues(
    select: _SelectInputs,
    output_ids: tuple[str, ...],
    inputs: InputSnapshot,
    assumptions: AssumptionSet,
) -> dict[str, str]:
    try:
        select(inputs, assumptions)
    except ValueError as exc:
        return dict.fromkeys(output_ids, str(exc))
    return {}


@dataclass
class _Availability:
    input_issues: _InputIssues
    _last: tuple[InputSnapshot, AssumptionSet, dict[str, str]] | None = None

    def check(
        self, rule: RuleDescriptor, output: OutputDescriptor, context: RuleContext
    ) -> CheckOutcome:
        inputs, assumptions = context.inputs, context.assumptions
        if (
            self._last is None
            or self._last[0] is not inputs
            or self._last[1] is not assumptions
        ):
            self._last = inputs, assumptions, self.input_issues(inputs, assumptions)
        reason = self._last[2].get(output.output_id)
        condition = "Eligible calculation inputs"
        return CheckOutcome(
            rule_id=rule.rule_id,
            rule_version=rule.version,
            severity=rule.severity,
            status="pass" if reason is None else "fail",
            observed=condition if reason is None else "Inputs failed eligibility",
            expected=condition,
            explanation=None if reason is None else reason[:4096],
            input_ids=output.required_input_ids,
            output_ids=(output.output_id,),
        )


def _fixed_dimensions(
    _inputs: InputSnapshot, _assumptions: AssumptionSet, *, horizon: int, scenarios: int
) -> tuple[int, int]:
    return horizon, scenarios


def _factor(
    model: Model,
    reference_factory: Callable[[], Reference],
    horizon: int,
    *,
    select: _SelectInputs | None = None,
    input_issues: _InputIssues | None = None,
    calculate: Calculate | None = None,
    scenarios: int = 1,
) -> tuple[Model, MethodBinding]:
    descriptor = model.describe()
    definitions = {rule.rule_id: rule for rule in descriptor.rules}
    if input_issues is None:
        if select is None:
            raise ValueError("Factor registration requires an input eligibility check")
        input_issues = partial(
            _shared_input_issues,
            select,
            tuple(output.output_id for output in descriptor.outputs),
        )
    availability = _Availability(input_issues)
    availability_rules = tuple(
        Rule(
            rule_id,
            output.required_input_ids,
            (output.output_id,),
            partial(availability.check, definitions[rule_id], output),
        )
        for output in descriptor.outputs
        for rule_id in output.required_check_ids
    )
    return model, MethodBinding(
        ExecutionLimits(
            # Bound total observations across all tables, regardless of the outcome horizon.
            10_000,
            horizon,
            scenarios,
            measure_dimensions=partial(
                _fixed_dimensions, horizon=horizon, scenarios=scenarios
            ),
        ),
        rules=availability_rules,
        reference=_WorkerReference(
            reference_factory, frozenset(rule.rule_id for rule in availability_rules)
        ),
        calculate=calculate,
    )


_COMPARISON = ProxyComparisonModel()
_TIMING = TimingStudyModel()
_INSTALLED_METHODS = (
    _factor(
        MomentumModel(),
        momentum_reference,
        WINDOW_SIZE - 1,
        select=partial(price_window, model_id="etf_momentum"),
    ),
    _factor(
        VolatilityModel(),
        volatility_reference,
        WINDOW_SIZE - 1,
        select=partial(price_window, model_id="etf_realized_volatility"),
    ),
    _factor(
        RealYieldModel(), regime_reference, WINDOW_SIZE - 1, select=resolve_yield_inputs
    ),
    _factor(FcfYieldModel(), issuer_reference, 1, select=resolve_fcf_inputs),
    _factor(
        _COMPARISON,
        comparison_reference,
        WINDOW_SIZE - 1,
        scenarios=2,
        input_issues=_COMPARISON.input_issues,
        calculate=_COMPARISON.calculate_subset,
    ),
    # Each outcome spans one open-to-open session. The supplied calendar sets the study span.
    _factor(
        _TIMING,
        timing_reference,
        1,
        input_issues=_TIMING.input_issues,
        calculate=_TIMING.calculate_subset,
    ),
)


def installed_methods() -> tuple[ModelRegistry, dict[tuple[str, str], MethodBinding]]:
    """Use one registration list for execution, discovery and contract export."""
    registry = ModelRegistry(model for model, _ in _INSTALLED_METHODS)
    bindings = {}
    for model, binding in _INSTALLED_METHODS:
        descriptor = model.describe()
        bindings[descriptor.model_id, descriptor.method_version] = binding
    return registry, bindings


def create_app() -> FastAPI:
    """Serve installed methods on a listener reserved for the Workspace bridge."""
    registry, bindings = installed_methods()
    store = FileRunStore(os.environ.get("QOPENBB_MODEL_RUN_DIR", "./data/modeling"))
    source = DataApiSnapshotSource(
        os.environ.get("QOPENBB_MODEL_DATA_ORIGIN", "http://data-api:6900")
    )
    service = Orchestrator(registry, bindings, store, snapshot_source=source)
    app = FastAPI(openapi_url=None, docs_url=None, redoc_url=None)
    app.mount(
        "/modeling/v1", create_model_app(service, registry, IdentityVerifier.from_env())
    )
    return app
