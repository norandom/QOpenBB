"""Issuer free cash flow yield from trailing filings and observation-date equity value."""

from decimal import Context, localcontext
from zoneinfo import ZoneInfo

from ...contracts import (
    AssumptionSet,
    EvaluationCutoff,
    InputSnapshot,
    ModelDescriptor,
    Observation,
    TraceEntry,
    TraceValue,
)
from ..protocol import CandidateOutput, CandidateResult, Model
from .filings import CashFlows, resolve_cash_flows
from .method_inputs import (
    evaluation_cutoff,
    factor_descriptor,
    input_rows,
    result_decimal,
    substitution,
    text_assumption,
)
from .sessions import WindowIssue, WindowUnavailable, latest_observed_rows

_MODEL = "issuer_fcf_yield"
_OUTPUT = "fcf_yield"
_INPUTS = ("cash_flows", "market_value")
_EXPRESSION = "100 × (operating cash flow − capex spending) / equity market value"


def _market_value(rows: tuple[Observation, ...], flows: CashFlows,
                  cutoff: EvaluationCutoff) -> Observation:
    day = cutoff.observation_date
    candidates = [row for row in rows if row.entity_id == flows.issuer_id
                  and row.metric_id == "equity_market_value" and row.observation_date == day]
    if not candidates:
        raise ValueError(f"Missing issuer equity market value on {day}")
    zone = ZoneInfo(cutoff.session_timezone)
    observed = [row for row in candidates if row.published_at is None
                or row.published_at.astimezone(zone).date() >= day]
    latest = latest_observed_rows(observed, cutoff, "issuer equity market value")
    if isinstance(latest, str):
        raise WindowUnavailable("Issuer equity market value", [WindowIssue(day, latest)])
    for row in latest:
        context = row.context
        if context.quantity != "stock" or context.unit != "currency":
            raise ValueError(f"{day} issuer equity market value must be a currency stock")
        if context.consolidation_scope != "issuer_consolidated":
            raise ValueError(f"{day} market value requires consolidated issuer scope")
        if context.currency != flows.currency or context.scale != flows.scale:
            raise ValueError(f"{day} market value and cash flows require matching currency and scale")
        if any(bound not in (None, day) for bound in (context.period_start, context.period_end)):
            raise ValueError(f"{day} market value must measure equity on the observation date")
        if row.value is None or not row.value.is_finite() or row.value <= 0:
            raise ValueError(f"{day} issuer equity market value must be finite and positive")
    if len({row.value for row in latest}) != 1:
        raise ValueError(f"{day} conflicting issuer equity market values at the same revision")
    return min(latest, key=lambda row: row.record_id)


def resolve_fcf_inputs(
    inputs: InputSnapshot, assumptions: AssumptionSet,
) -> tuple[EvaluationCutoff, CashFlows, Observation]:
    """Select compatible trailing filings and observation-date equity evidence."""
    cutoff = evaluation_cutoff(inputs, assumptions, _MODEL)
    flows = resolve_cash_flows(input_rows(inputs, "cash_flows"), cutoff,
                               text_assumption(assumptions, "capex_sign"))
    market = _market_value(input_rows(inputs, "market_value"), flows, cutoff)
    return cutoff, flows, market


def _calculate(inputs: InputSnapshot, assumptions: AssumptionSet) -> CandidateResult:
    cutoff, flows, market = resolve_fcf_inputs(inputs, assumptions)
    assert market.value is not None
    # Preserve cancellation between separately aggregated flows before division.
    with localcontext(Context(prec=160)):
        capex_spending = flows.capex_spending
        free_cash_flow = flows.operating_cash_flow - capex_spending
        try:
            value = result_decimal(100 * free_cash_flow / market.value)
            intermediates = tuple(
                TraceValue(name=name, value=amount, unit="currency", currency=flows.currency,
                           scale=flows.scale)
                for name, amount in (("capex_spending", capex_spending), ("free_cash_flow", free_cash_flow))
            )
        except ValueError as exc:
            raise ValueError(f"{cutoff.observation_date} FCF yield or its monetary components exceed financial decimal range") from exc
    rows = (*flows.rows, market)
    trace = TraceEntry(
        trace_id=_OUTPUT, formula_id=_OUTPUT, formula_version="1", expression=_EXPRESSION,
        output_id=_OUTPUT, input_ids=_INPUTS, check_ids=("eligible_inputs.fcf_yield",),
        assumption_ids=("capex_sign",), source_record_ids=tuple(row.record_id for row in rows),
        substitutions=tuple(map(substitution, rows)), intermediate_values=intermediates,
    )
    return CandidateResult(outputs=(CandidateOutput(output_id=_OUTPUT, value=value),), trace=(trace,))


class FcfYieldModel(Model):
    def describe(self) -> ModelDescriptor:
        return factor_descriptor(_MODEL, "company", _INPUTS, ((_OUTPUT, _EXPRESSION, "percent", "decimal"),),
                                 period_type="trailing_fiscal_year")

    def calculate(self, inputs: InputSnapshot, assumptions: AssumptionSet) -> CandidateResult:
        try:
            return _calculate(inputs, assumptions)
        except ValueError as exc:
            return CandidateResult(outputs=(CandidateOutput(output_id=_OUTPUT, value=None, reason=str(exc)[:4096]),))
