"""Percentage price return across the eligible ETF close window."""

from decimal import Context, Decimal, localcontext

from ...contracts import AssumptionSet, InputSnapshot, ModelDescriptor, TraceValue
from ..protocol import CandidateOutput, CandidateResult, Model
from .method_inputs import factor_descriptor, price_trace, price_window, result_decimal
from .sessions import PriceWindow

_MODEL_ID = "etf_momentum"
_OUTPUT_ID = "momentum"
_EXPRESSION = "100 × (last close / first close − 1), excluding dividends"


def _percentage_return(first: Decimal, last: Decimal) -> Decimal:
    # Subtract before dividing to retain small changes between nearly equal closes.
    # Guard digits preserve the quotient for rounding to the wire contract.
    with localcontext(Context(prec=160)):
        return result_decimal((last - first) * 100 / first)


def _withheld(reason: str) -> CandidateResult:
    return CandidateResult(outputs=(
        CandidateOutput(output_id=_OUTPUT_ID, value=None, reason=reason[:4096]),
    ))


class MomentumModel(Model):
    def describe(self) -> ModelDescriptor:
        return factor_descriptor(
            _MODEL_ID, "etf", ("sessions", "closes"),
            ((_OUTPUT_ID, _EXPRESSION, "percent", "decimal"),),
        )

    def calculate(self, inputs: InputSnapshot, assumptions: AssumptionSet) -> CandidateResult:
        try:
            window = price_window(inputs, assumptions, _MODEL_ID)
        except ValueError as exc:
            return _withheld(str(exc))

        return self.calculate_window(window)

    def calculate_window(self, window: PriceWindow) -> CandidateResult:
        first, last = window.closes[0].value, window.closes[-1].value
        assert isinstance(first, Decimal) and isinstance(last, Decimal)
        start, end = window.window.endpoints
        try:
            percent = _percentage_return(first, last)
            observation_count = result_decimal(Decimal(len(window.closes)))
        except ValueError as exc:
            return _withheld(f"Momentum from {start} to {end}: {exc}")

        intermediates = (
            TraceValue(
                name="observation_count", value=observation_count, unit="count",
                period_start=start, period_end=end,
            ),
        )
        return CandidateResult(
            outputs=(CandidateOutput(output_id=_OUTPUT_ID, value=percent),),
            trace=(price_trace(window, _OUTPUT_ID, _EXPRESSION, intermediates),),
        )
