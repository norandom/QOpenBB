"""Annualized realized volatility from split-adjusted ETF closes."""

from datetime import date
from decimal import Context, Decimal, localcontext
from itertools import pairwise

from ...contracts import AssumptionSet, InputSnapshot, ModelDescriptor, TraceValue
from ..protocol import CandidateOutput, CandidateResult, Model
from .method_inputs import factor_descriptor, price_trace, price_window, result_decimal
from .sessions import PriceWindow

MODEL_ID = "etf_realized_volatility"
OUTPUT_ID = "realized_volatility"
EXPRESSION = "100 × √252 × sample standard deviation of 63 adjacent simple returns (divisor 62)"
ANNUALIZATION_SESSIONS = 252


def _dated_decimal(value: Decimal, session: date, field: str) -> Decimal:
    try:
        return result_decimal(value)
    except ValueError as exc:
        raise ValueError(f"{session} {field}: {exc}") from exc


def _calculate_volatility(window: PriceWindow) -> tuple[Decimal, tuple[TraceValue, ...]]:
    # Guard digits keep the variance independent of trace serialization and caller precision.
    with localcontext(Context(prec=120)):
        returns = []
        intermediates = []
        for previous, current in pairwise(window.closes):
            assert previous.value is not None and current.value is not None
            simple_return = (current.value - previous.value) / previous.value
            returns.append(simple_return)
            intermediates.append(TraceValue(
                name=f"simple_return.{current.observation_date}",
                value=_dated_decimal(simple_return, current.observation_date, "simple return"),
                unit="ratio",
                period_start=previous.observation_date, period_end=current.observation_date,
            ))

        count = len(returns)
        divisor = count - 1
        # Shift before summing so identical recurring decimals have exactly zero variance.
        anchor = returns[0]
        centered_returns = [value - anchor for value in returns]
        centered_mean = sum(centered_returns) / count
        variance = sum((value - centered_mean) ** 2 for value in centered_returns) / divisor
        annualized = 100 * (ANNUALIZATION_SESSIONS * variance).sqrt()
        intermediates.extend((
            TraceValue(name="return_count", value=Decimal(count), unit="count"),
            TraceValue(name="sample_divisor", value=Decimal(divisor), unit="count"),
            TraceValue(name="annualization_sessions", value=Decimal(ANNUALIZATION_SESSIONS), unit="count"),
        ))
        value = _dated_decimal(annualized, window.window.endpoints[-1], "annualized volatility")
        return value, tuple(intermediates)


class VolatilityModel(Model):
    def describe(self) -> ModelDescriptor:
        return factor_descriptor(
            MODEL_ID, "etf", ("sessions", "closes"),
            ((OUTPUT_ID, EXPRESSION, "percent", "decimal"),),
        )

    def calculate(self, inputs: InputSnapshot, assumptions: AssumptionSet) -> CandidateResult:
        try:
            window = price_window(inputs, assumptions, MODEL_ID)
            return self.calculate_window(window)
        except ValueError as exc:
            return CandidateResult(outputs=(
                CandidateOutput(output_id=OUTPUT_ID, value=None, reason=str(exc)[:4096]),
            ))

    def calculate_window(self, window: PriceWindow) -> CandidateResult:
        try:
            value, intermediates = _calculate_volatility(window)
        except ValueError as exc:
            return CandidateResult(outputs=(
                CandidateOutput(output_id=OUTPUT_ID, value=None, reason=str(exc)[:4096]),
            ))

        return CandidateResult(
            outputs=(CandidateOutput(output_id=OUTPUT_ID, value=value),),
            trace=(price_trace(window, OUTPUT_ID, EXPRESSION, intermediates),),
        )
