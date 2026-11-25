"""Version 1 timing diagnostics rebuilt from dated inputs and study assumptions."""

from collections import defaultdict
from dataclasses import dataclass
from datetime import date
from decimal import Context, Decimal, localcontext
from fractions import Fraction

from ...contracts import AssumptionSet, InputSnapshot, Tolerance
from ..reference import Reference
from .timing_inputs import (
    Reading,
    TimingWindow,
    by_day,
    decision_amount,
    read_window,
    return_amounts,
)

_REGIMES = ("rising", "falling", "flat", None)
_UNITS = {
    "rising_hit_rate": "ratio", "rising_slugging": "ratio",
    "falling_hit_rate": "ratio", "falling_slugging": "ratio",
    "study_drawdown": "percent",
}


@dataclass(frozen=True)
class TimingInterval:
    decision: date
    start: date
    end: date
    regime: str | None
    position: str | None
    strategy: Decimal | None
    relative: Fraction | None
    exclusions: tuple[tuple[str, str], ...]


@dataclass(frozen=True)
class TimingGroup:
    eligible_count: int
    excluded_count: int
    winners: int
    ties: int
    mean_winner: Fraction | None
    absolute_mean_loser: Fraction | None


@dataclass(frozen=True)
class TimingReconstruction:
    partition: str
    universe: str
    benchmark: str
    intervals: tuple[TimingInterval, ...]
    groups: dict[str | None, TimingGroup]
    values: dict[str, Decimal | None]


def _interval(
    decision: date, start: date, end: date, signal: Reading, trend: Reading,
    asset: Reading, benchmark: Reading,
) -> TimingInterval:
    regime = None
    if trend.value is not None:
        regime = "rising" if trend.value > 0 else "falling" if trend.value < 0 else "flat"
    position = strategy = None
    readings = [("signal", signal), ("regime", trend)]
    if signal.value is not None:
        position = "long" if signal.value > 0 else "cash"
        strategy = asset.value if position == "long" else Decimal(0)
        if position == "long":
            readings.append(("asset_return", asset))
    readings.append(("benchmark_return", benchmark))
    relative = None if strategy is None or benchmark.value is None else Fraction(strategy) - Fraction(benchmark.value)
    return TimingInterval(
        decision, start, end, regime, position, strategy, relative,
        tuple((scope, reading.issue) for scope, reading in readings if reading.issue is not None),
    )


def _path(inputs: InputSnapshot, window: TimingWindow) -> tuple[TimingInterval, ...]:
    tables = {table.table_id: table.rows for table in inputs.tables}
    signals = by_day(tables.get("dated_signals", ()), window.universe, "momentum")
    regimes = by_day(tables.get("dated_regimes", ()), "DFII10", "endpoint_change")
    returns = tables.get("forward_returns", ())
    assets = return_amounts(returns, window.universe, window)
    benchmarks = return_amounts(returns, window.benchmark, window)
    path = []
    for decision, start, end in zip(window.sessions, window.sessions[1:], window.sessions[2:]):
        limit = min(decision.decision, window.as_of)
        path.append(_interval(
            decision.day, start.day, end.day,
            decision_amount(signals.get(decision.day, ()), limit, "signal"),
            decision_amount(regimes.get(decision.day, ()), limit, "regime"),
            assets[end.day], benchmarks[end.day],
        ))
    return tuple(path)


def _group(intervals: list[TimingInterval], regime: str | None) -> TimingGroup:
    eligible = [item.relative for item in intervals if regime is not None and item.relative is not None]
    wins = [value for value in eligible if value > 0]
    losses = [-value for value in eligible if value < 0]
    return TimingGroup(
        len(eligible), len(intervals) - len(eligible), len(wins), len(eligible) - len(wins) - len(losses),
        sum(wins, Fraction()) / len(wins) if wins else None,
        sum(losses, Fraction()) / len(losses) if losses else None,
    )


def _wire(value: Decimal) -> Decimal | None:
    if not value:
        return Decimal(0)
    if not -38 <= value.adjusted() <= 37:
        return None
    rounded = round(value, min(38, 37 - value.adjusted()))
    return rounded if rounded.adjusted() <= 37 else None


def _ratio(ratio: Fraction) -> Decimal | None:
    # Keep rounding exact at both the minimum magnitude and wire precision boundaries.
    if ratio and not Fraction(1, 10**38) <= ratio < 10**38:
        return None
    with localcontext(Context(prec=160)):
        estimate = Decimal(ratio.numerator) / Decimal(ratio.denominator)
        exponent = max(-38, estimate.adjusted() - 37)
        coefficient = round(ratio / Fraction(10) ** exponent)
        rounded = Decimal(coefficient).scaleb(exponent)
        return rounded if rounded.adjusted() <= 37 else None


def _drawdown(intervals: tuple[TimingInterval, ...]) -> Decimal | None:
    # Wealth is dimensionless. Fixed precision bounds the work even for long
    # paths with extreme returns and preserves ratios far below the V1 tolerance.
    with localcontext(Context(prec=160)):
        wealth = peak = Decimal(1)
        worst = Decimal(0)
        for interval in intervals:
            if interval.strategy is None:
                return None
            wealth *= 1 + interval.strategy / 100
            peak = max(peak, wealth)
            # A single-session loss bounds peak-to-trough drawdown from below.
            # Preserve that bound when rounding a minimum-size wire return.
            worst = max(worst, interval.strategy.copy_negate(), 100 * (1 - wealth / peak))
        return _wire(worst)


def rebuild_timing(inputs: InputSnapshot, assumptions: AssumptionSet) -> TimingReconstruction | None:
    """Return the reconstructed coverage, exposures and independently calculated outputs."""
    try:
        window = read_window(inputs, assumptions)
    except (KeyError, ValueError, OverflowError):
        return None
    intervals = _path(inputs, window)
    grouped: dict[str | None, list[TimingInterval]] = defaultdict(list)
    for interval in intervals:
        grouped[interval.regime].append(interval)
    groups = {regime: _group(grouped[regime], regime) for regime in _REGIMES}
    values = {"study_drawdown": _drawdown(intervals)}
    for regime in ("rising", "falling"):
        group = groups[regime]
        hit_rate = Fraction(group.winners, group.eligible_count) if group.eligible_count else None
        win, loss = group.mean_winner, group.absolute_mean_loser
        slugging = win / loss if win is not None and loss is not None else None
        values[f"{regime}_hit_rate"] = _ratio(hit_rate) if hit_rate is not None else None
        values[f"{regime}_slugging"] = _ratio(slugging) if slugging is not None else None
    return TimingReconstruction(window.partition, window.universe, window.benchmark, intervals, groups, values)


def timing_reference() -> Reference:
    """Bind the five timing outputs and the frozen V1 tolerances."""
    # Foundation calls each scalar separately for the same immutable snapshot.
    last: tuple[InputSnapshot, AssumptionSet, TimingReconstruction | None] | None = None

    def callback(output_id: str):
        def calculate(inputs: InputSnapshot, assumptions: AssumptionSet) -> Decimal | None:
            nonlocal last
            cached = last
            if cached is None or cached[0] is not inputs or cached[1] is not assumptions:
                cached = (inputs, assumptions, rebuild_timing(inputs, assumptions))
                last = cached
            study = cached[2]
            return study.values[output_id] if study is not None else None

        return calculate

    return Reference(
        "1", {name: callback(name) for name in _UNITS},
        {name: Tolerance(unit=unit, absolute=Decimal("0.000000001" if unit == "ratio" else "0.00000001"))
         for name, unit in _UNITS.items()},
    )
