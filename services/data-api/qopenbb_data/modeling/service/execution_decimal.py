"""Checks for exact representation at a method's Polars decimal boundary."""

from decimal import Decimal


class UnsupportedNumericConversion(ValueError):
    """The declared decimal dtype cannot represent a supplied amount exactly."""


def require_exact_decimal(value: Decimal, *, precision: int, scale: int) -> None:
    """Reject amounts requiring rounding or exceeding the declared dtype."""
    if not 0 <= scale <= precision <= 38 or precision == 0:
        raise ValueError("invalid decimal precision or scale")
    if not isinstance(value, Decimal) or not value.is_finite():
        raise UnsupportedNumericConversion("expected a finite Decimal")
    if value.is_zero():
        return

    # Ignore trailing zeroes without rounding under the active Decimal context.
    _, digits, exponent = value.as_tuple()
    fractional_places = -exponent
    for digit in reversed(digits):
        if digit != 0:
            break
        fractional_places -= 1
    if fractional_places > scale or value.adjusted() >= precision - scale:
        raise UnsupportedNumericConversion("amount exceeds decimal precision or scale")
