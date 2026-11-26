"""Ordered comparison of ETF price momentum and realized volatility."""

from dataclasses import dataclass
from datetime import date
from decimal import Context, Decimal, localcontext

from ...contracts import (
    AssumptionSet,
    EvaluationCutoff,
    InputSnapshot,
    ModelDescriptor,
    ObservationTable,
    OutputDescriptor,
    RuleDescriptor,
    TraceEntry,
)
from ..protocol import CandidateOutput, CandidateResult, Model
from .method_inputs import (
    evaluation_cutoff,
    price_window,
    result_decimal,
    text_assumption,
)
from .momentum import MomentumModel
from .sessions import PRICE_BASIS
from .volatility import VolatilityModel

_MODEL_ID = "proxy_comparison"
_LEGS = ("left", "right")
_INPUT_IDS = ("sessions", "left_closes", "right_closes")

type _TracedOutput = tuple[CandidateOutput, TraceEntry | None]


def _metric_outputs(metric: str, method: Model) -> tuple[OutputDescriptor, ...]:
    expression = method.describe().outputs[0].semantic_definition
    legs = tuple(
        OutputDescriptor(
            output_id=f"{side}_{metric}", semantic_definition=expression, unit="percent",
            required_input_ids=("sessions", f"{side}_closes"),
            required_check_ids=(f"eligible_inputs.{side}_{metric}",),
        )
        for side in _LEGS
    )
    spread_id = f"{metric}_spread"
    return (*legs, OutputDescriptor(
        output_id=spread_id, semantic_definition=f"Left minus right {metric}", unit="percentage_points",
        required_input_ids=_INPUT_IDS, required_check_ids=(f"eligible_inputs.{spread_id}",),
        required_output_ids=tuple(leg.output_id for leg in legs),
    ))


_METHOD_OUTPUTS = tuple(
    (pin, method, _metric_outputs(metric, method))
    for metric, pin, method in (
        ("momentum", ("etf_momentum", "1"), MomentumModel()),
        ("volatility", ("etf_realized_volatility", "1"), VolatilityModel()),
    )
)
_LEG_METHODS = ", ".join(f"{model_id}@{version}" for (model_id, version), _, _ in _METHOD_OUTPUTS)


def _descriptor() -> ModelDescriptor:
    outputs = tuple(output for _, _, metric_outputs in _METHOD_OUTPUTS for output in metric_outputs)
    return ModelDescriptor(
        model_id=_MODEL_ID, method_version="1", rule_set_version="1", reference_version="1",
        input_schema_id=f"{_MODEL_ID}.inputs", output_schema_id=f"{_MODEL_ID}.outputs",
        entity_types=("ordered_etf_pair",), period_types=("session",), input_ids=_INPUT_IDS,
        outputs=outputs, rules=tuple(
            RuleDescriptor(rule_id=output.required_check_ids[0], version="1",
                           stage="precondition", severity="blocking")
            for output in outputs
        ),
    )


_DESCRIPTOR = _descriptor()


@dataclass(frozen=True)
class _Leg:
    side: str
    calendar_id: str | None = None
    explicit_calendar: bool = False
    tables: tuple[ObservationTable, ...] = ()
    reason: str | None = None


def _eligible_entities(table: ObservationTable, metric: str, cutoff: EvaluationCutoff) -> set[str]:
    return {
        row.entity_id for row in table.rows
        if row.metric_id == metric and row.category != "estimate" and cutoff.is_eligible(row)
    }


def _calendar_id(
    assumptions: AssumptionSet, side: str, sessions: ObservationTable, cutoff: EvaluationCutoff,
) -> tuple[str, bool]:
    key = f"{side}_calendar"
    if any(item.assumption_id == key for item in assumptions.assumptions):
        calendar = text_assumption(assumptions, key)
        if not any(row.metric_id == "session" and row.entity_id == calendar for row in sessions.rows):
            raise ValueError(f"{key} {calendar} is absent from the sessions table")
        return calendar, True
    calendars = _eligible_entities(sessions, "session", cutoff)
    if len(calendars) == 1:
        return next(iter(calendars)), False
    raise ValueError(f"{key} requires an explicit calendar binding, found {len(calendars)} eligible schedules")


def _bind_leg(
    side: str, assumptions: AssumptionSet, tables: dict[str, ObservationTable],
    cutoff: EvaluationCutoff,
) -> _Leg:
    try:
        proxy_key = f"{side}_proxy"
        proxy = text_assumption(assumptions, proxy_key)
        closes = tables.get(f"{side}_closes")
        if closes is None:
            raise ValueError(f"Missing required input table {side}_closes")
        entities = _eligible_entities(closes, "close", cutoff)
        if entities and entities != {proxy}:
            found = ", ".join(sorted(entities))
            raise ValueError(f"{proxy_key} {proxy} does not match eligible close entities {found}")

        sessions = tables["sessions"]
        calendar, explicit = _calendar_id(assumptions, side, sessions, cutoff)
        # Keep every version for each bound entity so the resolver can report unavailable dates.
        schedule = tuple(row for row in sessions.rows if row.entity_id == calendar)
        proxy_rows = tuple(row for row in closes.rows if row.entity_id == proxy)
        return _Leg(side, calendar, explicit, (
            sessions.model_copy(update={"rows": schedule}),
            closes.model_copy(update={"table_id": "closes", "rows": proxy_rows}),
        ))
    except ValueError as exc:
        return _Leg(side, reason=f"{side.title()} leg on {cutoff.observation_date}: {exc}")


def _withheld(output_id: str, reason: str) -> CandidateOutput:
    return CandidateOutput(output_id=output_id, value=None, reason=reason[:4096])


def _leg_snapshot(
    inputs: InputSnapshot, method: Model, pin: tuple[str, str], leg: _Leg, ending: date,
) -> InputSnapshot:
    if leg.reason is not None:
        raise ValueError(leg.reason)
    descriptor = method.describe()
    if (descriptor.model_id, descriptor.method_version) != pin:
        reason = (
            f"{leg.side.title()} leg on {ending}: expected {pin[0]}@{pin[1]}, "
            f"found {descriptor.model_id}@{descriptor.method_version}"
        )
        raise ValueError(reason)
    return inputs.model_copy(update={
        "schema_id": descriptor.input_schema_id, "tables": leg.tables,
    })


def _leg_metric(
    inputs: InputSnapshot, assumptions: AssumptionSet, method: Model, pin: tuple[str, str], leg: _Leg,
    output: OutputDescriptor, ending: date,
) -> _TracedOutput:
    try:
        leg_inputs = _leg_snapshot(inputs, method, pin, leg, ending)
    except ValueError as exc:
        return _withheld(output.output_id, str(exc)), None
    result = method.calculate(leg_inputs, assumptions)
    candidate, = result.outputs
    if candidate.value is None:
        reason = f"{leg.side.title()} leg on {ending}: {candidate.reason}"
        return _withheld(output.output_id, reason), None

    trace, = result.trace
    binding_ids = (f"{leg.side}_proxy", "leg_methods")
    if leg.explicit_calendar:
        binding_ids += (f"{leg.side}_calendar",)
    return candidate.model_copy(update={"output_id": output.output_id}), trace.model_copy(update={
        "trace_id": output.output_id,
        "formula_id": output.output_id,
        "output_id": output.output_id,
        "input_ids": output.required_input_ids,
        "check_ids": output.required_check_ids,
        "assumption_ids": trace.assumption_ids + binding_ids,
    })


def _spread_issue(legs: tuple[_Leg, _Leg], ending: date, *leg_issues: str | None) -> str | None:
    reasons = ". ".join(reason[:1950] for reason in leg_issues if reason)
    if reasons:
        return f"Spread withheld on {ending}: {reasons}"
    left, right = legs
    if left.calendar_id != right.calendar_id:
        return (f"Cross-calendar spread withheld on {ending}: left calendar {left.calendar_id} "
                f"differs from right calendar {right.calendar_id}")
    return None


def _spread(
    output: OutputDescriptor, legs: tuple[_Leg, _Leg], ending: date,
    left_metric: _TracedOutput, right_metric: _TracedOutput,
) -> _TracedOutput:
    left, left_trace = left_metric
    right, right_trace = right_metric
    issue = _spread_issue(legs, ending, left.reason, right.reason)
    if issue is not None:
        return _withheld(output.output_id, issue), None

    assert isinstance(left.value, Decimal) and isinstance(right.value, Decimal)
    # The same calendar ID selects the same schedule rows, revision, and exact ending session.
    try:
        with localcontext(Context(prec=120)):
            value = result_decimal(left.value - right.value)
    except ValueError as exc:
        return _withheld(output.output_id, f"Spread withheld on {ending}: {exc}"), None

    assert left_trace is not None and right_trace is not None
    trace = TraceEntry(
        trace_id=output.output_id, formula_id=output.output_id, formula_version="1",
        output_id=output.output_id, expression=output.semantic_definition,
        input_ids=output.required_input_ids, check_ids=output.required_check_ids,
        source_record_ids=tuple(dict.fromkeys(left_trace.source_record_ids + right_trace.source_record_ids)),
        assumption_ids=tuple(dict.fromkeys(left_trace.assumption_ids + right_trace.assumption_ids)),
        substitutions=left_trace.substitutions + right_trace.substitutions,
    )
    return CandidateOutput(output_id=output.output_id, value=value), trace


def _comparison_legs(
    inputs: InputSnapshot, assumptions: AssumptionSet,
) -> tuple[date, tuple[_Leg, _Leg]]:
    try:
        cutoff = evaluation_cutoff(inputs, assumptions, _MODEL_ID)
        if text_assumption(assumptions, "leg_methods") != _LEG_METHODS:
            raise ValueError(f"leg_methods must be {_LEG_METHODS}")
        text_assumption(assumptions, "schedule_revision")
        if text_assumption(assumptions, "price_basis") != PRICE_BASIS:
            raise ValueError(f"price_basis must be {PRICE_BASIS}")
        tables = {table.table_id: table for table in inputs.tables}
        if "sessions" not in tables:
            raise ValueError("Missing required input table sessions")
    except ValueError as exc:
        day = f" on {inputs.cutoff.observation_date}" if inputs.cutoff is not None else ""
        raise ValueError(f"Comparison{day}: {exc}") from exc

    return cutoff.observation_date, (
        _bind_leg("left", assumptions, tables, cutoff),
        _bind_leg("right", assumptions, tables, cutoff),
    )


def _leg_input_issue(
    inputs: InputSnapshot, assumptions: AssumptionSet, method: Model, pin: tuple[str, str],
    leg: _Leg, ending: date,
) -> str | None:
    try:
        snapshot = _leg_snapshot(inputs, method, pin, leg, ending)
    except ValueError as exc:
        return str(exc)
    try:
        price_window(snapshot, assumptions, pin[0])
    except ValueError as exc:
        return f"{leg.side.title()} leg on {ending}: {exc}"
    return None


class ProxyComparisonModel(Model):
    def describe(self) -> ModelDescriptor:
        return _DESCRIPTOR

    def input_issues(self, inputs: InputSnapshot, assumptions: AssumptionSet) -> dict[str, str]:
        try:
            ending, legs = _comparison_legs(inputs, assumptions)
        except ValueError as exc:
            return dict.fromkeys((output.output_id for output in _DESCRIPTOR.outputs), str(exc))

        issues = {}
        for pin, method, (left_spec, right_spec, spread_spec) in _METHOD_OUTPUTS:
            left_issue = _leg_input_issue(inputs, assumptions, method, pin, legs[0], ending)
            right_issue = _leg_input_issue(inputs, assumptions, method, pin, legs[1], ending)
            spread_issue = _spread_issue(legs, ending, left_issue, right_issue)
            for spec, issue in zip((left_spec, right_spec, spread_spec),
                                   (left_issue, right_issue, spread_issue), strict=True):
                if issue is not None:
                    issues[spec.output_id] = issue
        return issues

    def calculate(self, inputs: InputSnapshot, assumptions: AssumptionSet) -> CandidateResult:
        return self.calculate_subset(inputs, assumptions, tuple(
            output.output_id for output in _DESCRIPTOR.outputs
        ))

    def calculate_subset(
        self, inputs: InputSnapshot, assumptions: AssumptionSet, eligible: tuple[str, ...],
    ) -> CandidateResult:
        """Calculate selected outputs in descriptor order with eligible legs for each spread."""
        if not eligible:
            return CandidateResult(outputs=())
        try:
            ending, legs = _comparison_legs(inputs, assumptions)
        except ValueError as exc:
            return CandidateResult(outputs=tuple(
                _withheld(output.output_id, str(exc))
                for output in _DESCRIPTOR.outputs if output.output_id in eligible
            ))

        results: dict[str, _TracedOutput] = {}
        for pin, method, (left_spec, right_spec, spread_spec) in _METHOD_OUTPUTS:
            for leg, spec in zip(legs, (left_spec, right_spec), strict=True):
                if spec.output_id in eligible:
                    results[spec.output_id] = _leg_metric(
                        inputs, assumptions, method, pin, leg, spec, ending,
                    )
            if spread_spec.output_id in eligible:
                left = results.get(left_spec.output_id)
                right = results.get(right_spec.output_id)
                if left is None or right is None:
                    reason = f"Spread withheld on {ending}: both leg outputs must be eligible"
                    results[spread_spec.output_id] = _withheld(spread_spec.output_id, reason), None
                else:
                    results[spread_spec.output_id] = _spread(spread_spec, legs, ending, left, right)

        return CandidateResult(
            outputs=tuple(output for output, _ in results.values()),
            trace=tuple(entry for _, entry in results.values() if entry is not None),
        )
