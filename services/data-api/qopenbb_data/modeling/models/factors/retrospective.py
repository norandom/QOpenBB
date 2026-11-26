"""Ordered ETF comparisons on the provider history received for a research story."""

from datetime import datetime

from ...contracts import AssumptionSet, InputSnapshot, ModelDescriptor, TraceEntry
from ...contracts.inputs import Transformation
from ..protocol import CandidateOutput, CandidateResult
from .comparison import ProxyComparisonModel, _withheld, spread_values
from .momentum import MomentumModel
from .retrieved_history import receipts, retrieved_window
from .volatility import VolatilityModel

_BASE = ProxyComparisonModel().describe()
_DESCRIPTOR = _BASE.model_copy(
    update={
        "method_version": "2",
        "rule_set_version": "2",
        "reference_version": "2",
        "outputs": tuple(
            output.model_copy(
                update={
                    "semantic_definition": f"Retrospective FMP price history: {output.semantic_definition}",
                }
            )
            for output in _BASE.outputs
        ),
        "rules": tuple(rule.model_copy(update={"version": "2"}) for rule in _BASE.rules),
    }
)
_METRICS = {"momentum": MomentumModel(), "volatility": VolatilityModel()}


def _leg_results(
    inputs: InputSnapshot,
    assumptions: AssumptionSet,
    side: str,
    when: datetime | None,
    eligible: tuple[str, ...],
) -> dict[str, tuple[CandidateOutput, TraceEntry | None]]:
    outputs = [
        spec
        for spec in _DESCRIPTOR.outputs
        if spec.output_id.startswith(side + "_") and spec.output_id in eligible
    ]
    if not outputs:
        return {}
    try:
        window = retrieved_window(inputs, assumptions, side, when)
    except ValueError as exc:
        return {spec.output_id: (_withheld(spec.output_id, str(exc)), None) for spec in outputs}
    assert when is not None
    receipt = Transformation(
        transformation_id=f"{side}.retrieved_history",
        version="2",
        description=f"Retrospective FMP history retrieved at {when.isoformat()}. Historical availability is unknown.",
    )
    results = {}
    for spec in outputs:
        metric = spec.output_id.removeprefix(side + "_")
        candidate = _METRICS[metric].calculate_window(window)
        value = candidate.outputs[0].model_copy(update={"output_id": spec.output_id})
        trace = (
            candidate.trace[0].model_copy(
                update={
                    "trace_id": spec.output_id,
                    "formula_id": spec.output_id,
                    "output_id": spec.output_id,
                    "formula_version": "2",
                    "expression": spec.semantic_definition,
                    "input_ids": spec.required_input_ids,
                    "check_ids": spec.required_check_ids,
                    "assumption_ids": (
                        "calendar_id",
                        "schedule_revision",
                        "price_basis",
                        "leg_methods",
                        f"{side}_proxy",
                        f"{side}_calendar",
                    ),
                    "transformations": (receipt,),
                }
            )
            if candidate.trace
            else None
        )
        results[spec.output_id] = value, trace
    return results


class RetrospectiveComparisonModel:
    def describe(self) -> ModelDescriptor:
        return _DESCRIPTOR

    def input_issues(self, inputs: InputSnapshot, assumptions: AssumptionSet) -> dict[str, str]:
        try:
            times = receipts(inputs, assumptions)
        except ValueError as exc:
            return dict.fromkeys((item.output_id for item in _DESCRIPTOR.outputs), str(exc))
        issues = {}
        for side in ("left", "right"):
            try:
                retrieved_window(inputs, assumptions, side, times.get(side))
            except ValueError as exc:
                for spec in _DESCRIPTOR.outputs:
                    if f"{side}_closes" in spec.required_input_ids:
                        issues[spec.output_id] = str(exc)
        return issues

    def calculate(self, inputs: InputSnapshot, assumptions: AssumptionSet) -> CandidateResult:
        return self.calculate_subset(
            inputs, assumptions, tuple(item.output_id for item in _DESCRIPTOR.outputs)
        )

    def calculate_subset(
        self, inputs: InputSnapshot, assumptions: AssumptionSet, eligible: tuple[str, ...]
    ) -> CandidateResult:
        try:
            times = receipts(inputs, assumptions)
        except ValueError as exc:
            return CandidateResult(outputs=tuple(_withheld(key, str(exc)) for key in eligible))
        results = {}
        for side in ("left", "right"):
            results.update(_leg_results(inputs, assumptions, side, times.get(side), eligible))
        assert inputs.cutoff is not None
        for spec in _DESCRIPTOR.outputs:
            key = spec.output_id
            if key in eligible and key.endswith("_spread"):
                if not all(dep in results for dep in spec.required_output_ids):
                    results[key] = _withheld(key, "Both ETF legs are required"), None
                    continue
                pair = tuple(results[dep] for dep in spec.required_output_ids)
                reasons = [candidate.reason for candidate, _ in pair if candidate.reason]
                if reasons:
                    results[key] = _withheld(key, ". ".join(reasons)), None
                    continue
                value, trace = spread_values(spec, inputs.cutoff.observation_date, *pair)
                if trace is not None:
                    trace = trace.model_copy(
                        update={
                            "formula_version": "2",
                            "transformations": tuple(item for _, leg in pair for item in leg.transformations),
                        }
                    )
                results[key] = value, trace
        ordered = [results[spec.output_id] for spec in _DESCRIPTOR.outputs if spec.output_id in eligible]
        return CandidateResult(
            outputs=tuple(value for value, _ in ordered),
            trace=tuple(trace for _, trace in ordered if trace is not None),
        )
