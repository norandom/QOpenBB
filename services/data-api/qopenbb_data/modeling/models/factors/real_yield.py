"""Classify the real-yield regime from dated DFII10 levels."""

from datetime import date
from decimal import Context, Decimal, localcontext

from ...contracts import (
    AssumptionSet,
    InputSnapshot,
    ModelDescriptor,
    Observation,
    TraceEntry,
)
from ..protocol import CandidateOutput, CandidateResult, Model
from .method_inputs import (
    factor_descriptor,
    input_rows,
    result_decimal,
    session_window,
    substitution,
)
from .sessions import (
    SessionWindow,
    WindowIssue,
    WindowUnavailable,
    latest_observed_rows,
)

_MODEL_ID = "real_yield_regime"
_INPUT_IDS = ("sessions", "dfii10")
_REGIME_EXPRESSION = "Sign of exact DFII10 endpoint change"
_CHANGE_EXPRESSION = "End DFII10 level minus start level"


def _level_issue(row: Observation) -> str | None:
    context = row.context
    if row.value is None or not row.value.is_finite():
        return "level must be finite"
    if context.unit != "percent" or context.quantity != "rate":
        return "level must be a rate in percent"
    if context.basis != "treasury_constant_maturity":
        return "level basis must be treasury_constant_maturity"
    if context.currency is not None or context.scale != 0:
        return "level requires no currency and scale zero"
    if any(day not in (None, row.observation_date) for day in (context.period_start, context.period_end)):
        return "level must represent the observation date"
    return None


def _select_level(rows: list[Observation], window: SessionWindow) -> Observation | str:
    # Explicit coverage is required even when the supplied timestamps pass the cutoff.
    known = [row for row in rows if row.context.vintage_coverage == "known"]
    latest = latest_observed_rows(known, window.cutoff, "DFII10 endpoint")
    if isinstance(latest, str):
        if any(row.category != "estimate" and row.context.vintage_coverage != "known"
               for row in rows):
            return "unknown historical availability for DFII10 endpoint"
        if rows and not known:
            return "only estimates for DFII10 endpoint"
        return latest
    latest.sort(key=lambda row: row.record_id)
    for row in latest:
        if issue := _level_issue(row):
            return issue
    if len({row.value for row in latest}) > 1:
        return "conflicting DFII10 levels at the same revision"
    return latest[0]


def _endpoints(inputs: InputSnapshot, window: SessionWindow) -> tuple[Observation, Observation]:
    by_date: dict[date, list[Observation]] = {day: [] for day in window.endpoints}
    try:
        rows = input_rows(inputs, "dfii10")
    except ValueError as exc:
        raise WindowUnavailable("DFII10", [
            WindowIssue(day, str(exc)) for day in by_date
        ]) from exc
    for row in rows:
        if (row.entity_id == "DFII10" and row.metric_id == "real_yield"
                and row.observation_date in by_date):
            by_date[row.observation_date].append(row)

    start, end = window.endpoints
    first, last = _select_level(by_date[start], window), _select_level(by_date[end], window)
    failures = [f"{issue} on {day}" for day, issue in ((start, first), (end, last))
                if isinstance(issue, str)]
    if failures:
        reason = ", ".join(failures)
        raise ValueError(reason[0].upper() + reason[1:])
    assert isinstance(first, Observation) and isinstance(last, Observation)
    return first, last


def _trace(output_id: str, expression: str, window: SessionWindow,
           first: Observation, last: Observation) -> TraceEntry:
    return TraceEntry(
        trace_id=output_id, formula_id=output_id, formula_version="1",
        expression=expression, output_id=output_id, check_ids=(f"eligible_inputs.{output_id}",),
        source_record_ids=window.source_record_ids + (first.record_id, last.record_id),
        input_ids=_INPUT_IDS, assumption_ids=("schedule_revision",),
        substitutions=(substitution(first), substitution(last)),
    )


def _change(first: Observation, last: Observation) -> Decimal:
    # The wire bounds are 38 integral and 38 fractional places. One extra digit
    # accommodates a carry when subtracting levels with opposite signs.
    with localcontext(Context(prec=77)):
        assert first.value is not None and last.value is not None
        try:
            return result_decimal(last.value - first.value)
        except ValueError as exc:
            raise ValueError(f"DFII10 change from {first.observation_date} to {last.observation_date}: {exc}") from exc


class RealYieldModel(Model):
    def describe(self) -> ModelDescriptor:
        return factor_descriptor(
            _MODEL_ID, "macro_series", _INPUT_IDS,
            (("regime", _REGIME_EXPRESSION, "classification", "text"),
             ("change", _CHANGE_EXPRESSION, "percentage_points", "decimal")),
        )

    def calculate(self, inputs: InputSnapshot, assumptions: AssumptionSet) -> CandidateResult:
        try:
            window = session_window(inputs, assumptions, _MODEL_ID)
            first, last = _endpoints(inputs, window)
            change = _change(first, last)
        except ValueError as exc:
            reason = str(exc)[:4096]
            return CandidateResult(outputs=(
                CandidateOutput(output_id="regime", value_type="text", value=None, reason=reason),
                CandidateOutput(output_id="change", value=None, reason=reason),
            ))

        assert first.value is not None and last.value is not None
        if last.value > first.value:
            regime = "rising"
        elif last.value < first.value:
            regime = "falling"
        else:
            regime = "flat"
        return CandidateResult(
            outputs=(CandidateOutput(output_id="regime", value_type="text", value=regime),
                     CandidateOutput(output_id="change", value=change)),
            trace=(_trace("regime", _REGIME_EXPRESSION, window, first, last),
                   _trace("change", _CHANGE_EXPRESSION, window, first, last)),
        )
