"""Exact comparisons in the declared financial unit and scale."""

from decimal import Decimal
from fractions import Fraction

from ..contracts.checks import Tolerance


def within_tolerance(
    observed: Decimal, expected: Decimal, tolerance: Tolerance, *, unit: str, scale: int = 0,
) -> bool:
    """Compare at the larger of the absolute bound and the expected-value relative bound."""
    if unit != tolerance.unit:
        raise ValueError("comparison unit differs from tolerance unit")
    # Rational arithmetic preserves the full contract precision even under a low Decimal context.
    observed_amount = Fraction(observed) * Fraction(10) ** scale
    expected_amount = Fraction(expected) * Fraction(10) ** scale
    absolute = Fraction(tolerance.absolute) * Fraction(10) ** tolerance.scale
    relative = Fraction(tolerance.relative or 0) * abs(expected_amount)
    return abs(observed_amount - expected_amount) <= max(absolute, relative)
