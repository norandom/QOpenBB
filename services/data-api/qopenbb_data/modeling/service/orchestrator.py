"""Authenticate, evaluate and persist an exact installed financial method."""

import pickle
from collections.abc import Mapping
from dataclasses import KW_ONLY, dataclass
from datetime import UTC, datetime
from functools import partial
from threading import Event
from time import monotonic

from ..contracts.common import require_subset, require_unique
from ..contracts.descriptors import ModelDescriptor
from ..contracts.inputs import InputSnapshot
from ..contracts.results import ModelRun
from ..models.protocol import Model
from ..models.registry import ModelRegistry
from ..validation.lifecycle import Calculate
from ..validation.rules import Rule
from ..verification.reference import Reference
from .acquisition import AcquisitionError
from .evaluation import EvaluationRequest, _evaluate_in_child, _RunContext
from .execution import ExecutionError, ExecutionLimits, ModelExecutor, _remaining
from .ports import Principal, RunStore, SnapshotSource
from .run_store import FileRunStore, RunPublishedError


@dataclass(frozen=True)
class MethodBinding:
    """Trusted execution policy and importable callbacks for one exact registry key."""

    limits: ExecutionLimits
    _: KW_ONLY
    rules: tuple[Rule, ...] = ()
    reference: Reference | None = None
    calculate: Calculate | None = None


class Orchestrator:
    def __init__(
        self,
        registry: ModelRegistry,
        bindings: Mapping[tuple[str, str], MethodBinding],
        run_store: RunStore,
        *,
        snapshot_source: SnapshotSource | None = None,
        polars_threads: int = 1,
        timeout_seconds: float = 60,
        capacity: int = 1,
    ) -> None:
        self._store = run_store
        self._source = snapshot_source
        bindings = dict(bindings)
        self._methods = {
            key: _bind(registry.resolve(*key), key, binding)
            for key, binding in bindings.items()
        }
        self._executor = ModelExecutor(
            registry,
            {key: binding.limits for key, binding in bindings.items()},
            polars_threads=polars_threads,
            timeout_seconds=timeout_seconds,
            capacity=capacity,
        )
        self._registry = registry

    def evaluate(
        self,
        request: EvaluationRequest,
        principal: Principal,
        *,
        cancel: Event | None = None,
    ) -> ModelRun:
        started = monotonic()
        principal = _principal(principal)
        request = EvaluationRequest.model_validate(request)
        key = request.model_id, request.method_version
        if key not in self._methods:
            self._registry.resolve(*key)
            raise ExecutionError("missing_method_binding")
        descriptor, job = self._methods[key]
        if request.acquisition is not None:
            from .story_acquisition import validate_story_binding

            validate_story_binding(key, request.acquisition, request.assumptions)
        _validate_exceptions(request, principal, descriptor)
        context = _RunContext(
            owner_id=principal.subject,
            created_at=datetime.now(UTC),
            exceptions=request.exceptions,
        )
        wire = bytearray()
        deadline = started

        def capture_result(payload: bytearray, execution_deadline: float) -> None:
            nonlocal wire, deadline
            wire = payload
            deadline = execution_deadline

        run = self._executor._evaluate(
            *key,
            request.assumptions,
            started=started,
            cancel=cancel,
            prepare_inputs=partial(self._prepare_inputs, request, cancel),
            result_type=ModelRun,
            job_payload=job,
            context=context.model_dump(mode="json"),
            capture_result=capture_result,
        )
        return self._publish(run, principal, wire, deadline, cancel)

    def _publish(
        self, run: ModelRun, principal: Principal, wire: bytearray, deadline: float, cancel: Event | None
    ) -> ModelRun:
        _remaining(deadline, cancel)
        if type(self._store) is FileRunStore:
            run_id = self._store._publish_evaluated(wire, principal, deadline=deadline, cancel=cancel)
            return run.model_copy(update={"run_id": run_id})
        run_id = self._store.save(run, principal)
        try:
            return self._store.get(run_id, principal)
        except Exception:  # noqa: BLE001 - Saving succeeded, so every readback failure needs the ID.
            raise RunPublishedError(run_id) from None

    def get(self, run_id: str, principal: Principal) -> ModelRun:
        """Return the persisted original under its authenticated owner."""
        return self._store.get(run_id, _principal(principal))

    def _prepare_inputs(
        self,
        request: EvaluationRequest,
        cancel: Event | None,
        deadline: float,
    ) -> InputSnapshot:
        if request.inputs is not None:
            snapshot = request.inputs
            provenance = snapshot.provenance.model_copy(
                update={"origin": "user_supplied", "acquisition_id": None},
            )
            return snapshot.model_copy(update={"provenance": provenance})
        if self._source is None or request.acquisition is None:
            raise ExecutionError("snapshot_source_unavailable")
        try:
            snapshot = self._source.acquire(
                request.acquisition, deadline=deadline, cancel=cancel
            )
        except AcquisitionError as error:
            if error.code in ("timeout", "cancelled"):
                raise ExecutionError(error.code) from None
            raise
        if not isinstance(snapshot, InputSnapshot):
            raise ExecutionError("invalid_input_snapshot")
        # The bounded worker validates the complete snapshot from the wire.
        provenance = getattr(snapshot, "provenance", None)
        if (
            getattr(provenance, "origin", None) != "service_acquired"
            or getattr(snapshot, "cutoff", None) != request.acquisition.cutoff
        ):
            raise ExecutionError("invalid_acquisition_evidence")
        return snapshot


def _principal(principal: Principal) -> Principal:
    if type(principal) is not Principal:
        raise TypeError("authenticated principal required")
    return Principal.model_validate(principal)


def _bind(
    model: Model,
    key: tuple[str, str],
    binding: MethodBinding,
) -> tuple[ModelDescriptor, bytes]:
    descriptor = ModelDescriptor.model_validate(model.describe())
    if (descriptor.model_id, descriptor.method_version) != key:
        raise ValueError("installed descriptor differs from its registry key")
    if not isinstance(binding.limits, ExecutionLimits):
        raise TypeError("execution limits required")
    if binding.calculate is not None and not callable(binding.calculate):
        raise TypeError("subset calculator must be callable")
    rule_ids = tuple(rule.rule_id for rule in binding.rules)
    require_unique(rule_ids, "rule implementation")
    require_subset(
        rule_ids, {rule.rule_id for rule in descriptor.rules}, "rule implementations"
    )
    output_ids = {item.output_id for item in descriptor.outputs}
    for rule in binding.rules:
        require_subset(rule.input_ids, set(descriptor.input_ids), "rule inputs")
        require_subset(rule.output_ids, output_ids, "rule outputs")
        if not callable(rule.evaluate):
            raise TypeError("rule evaluator must be callable")
    if (reference := binding.reference) is not None:
        if reference.version != descriptor.reference_version:
            raise ValueError("reference version differs from the installed descriptor")
        require_subset(
            tuple(reference.calculations), output_ids, "reference calculations"
        )
        require_subset(
            tuple(reference.tolerances),
            set(reference.calculations),
            "reference tolerances",
        )
        for calculate in reference.calculations.values():
            if not callable(calculate):
                raise TypeError("reference calculator must be callable")
            if calculate in (model.calculate, binding.calculate):
                raise ValueError(
                    "reference must be independent of the production calculator"
                )
    # Snapshot the trusted callbacks before handling any caller input or acquiring data.
    job = partial(
        _evaluate_in_child,
        rules=binding.rules,
        reference=reference,
        calculate=binding.calculate,
    )
    return descriptor, pickle.dumps(job)


def _validate_exceptions(
    request: EvaluationRequest,
    principal: Principal,
    descriptor: ModelDescriptor,
) -> None:
    rules = {rule.rule_id: rule for rule in descriptor.rules}
    outputs = {output.output_id for output in descriptor.outputs}
    for item in request.exceptions:
        rule = rules.get(item.rule_id)
        if (
            item.author != principal.subject
            or rule is None
            or rule.version != item.rule_version
            or rule.exception_policy_version != item.policy_version
        ):
            raise ValueError(
                "exception differs from the authenticated author or installed policy"
            )
        require_subset(item.output_ids, outputs, "exception outputs")
