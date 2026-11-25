"""Select dated evidence for a one-session timing study."""

from bisect import bisect_left, bisect_right
from collections import Counter, defaultdict
from collections.abc import Sequence
from dataclasses import dataclass
from datetime import date, datetime
from decimal import Context, Decimal, localcontext
from typing import Literal
from zoneinfo import ZoneInfo

from ...contracts import AssumptionSet, EvaluationCutoff, InputSnapshot, Observation
from .sessions import PRICE_BASIS, latest_observed_rows
from .study_schedule import StudyPlan, StudySession, study_plan

Regime = Literal["rising", "falling", "flat"]
Position = Literal["long", "cash"]
ExclusionScope = Literal["signal", "regime", "asset_return", "benchmark_return"]
ExclusionCode = Literal["missing", "unavailable", "invalid", "conflict", "invalid_interval"]

_REGIMES: tuple[Regime | None, ...] = ("rising", "falling", "flat", None)
_RETURN_BASIS = "open_to_open"


@dataclass(frozen=True)
class StudyExclusion:
    scope: ExclusionScope
    code: ExclusionCode
    reason: str
    record_ids: tuple[str, ...] = ()


@dataclass(frozen=True)
class StudyInterval:
    """An exposure return in percent and a benchmark difference in percentage points."""

    decision_date: date
    start: date
    end: date
    regime: Regime | None
    position: Position | None
    strategy_return: Decimal | None
    benchmark_relative_return: Decimal | None
    signal_row: Observation | None
    regime_row: Observation | None
    asset_row: Observation | None
    benchmark_row: Observation | None
    exclusions: tuple[StudyExclusion, ...]


@dataclass(frozen=True)
class StudyGroup:
    """Coverage for one partition and regime, with None marking unknown regimes."""

    partition: str
    regime: Regime | None
    intervals: tuple[StudyInterval, ...]

    @property
    def eligible_count(self) -> int:
        if self.regime is None:
            return 0
        return sum(item.benchmark_relative_return is not None for item in self.intervals)

    @property
    def excluded_count(self) -> int:
        return len(self.intervals) - self.eligible_count

    @property
    def exclusion_counts(self) -> dict[tuple[ExclusionScope, ExclusionCode], int]:
        return dict(Counter(
            (exclusion.scope, exclusion.code)
            for interval in self.intervals for exclusion in interval.exclusions
        ))


@dataclass(frozen=True)
class StudyGroups:
    plan: StudyPlan
    intervals: tuple[StudyInterval, ...]
    groups: tuple[StudyGroup, ...]


def _rows_by_date(
    rows: Sequence[Observation], entity: str, metric: str,
) -> dict[date, list[Observation]]:
    selected: dict[date, list[Observation]] = defaultdict(list)
    for row in rows:
        if (row.entity_id, row.metric_id) == (entity, metric):
            selected[row.observation_date].append(row)
    return selected


def _financial_issue(row: Observation, scope: ExclusionScope) -> str | None:
    context = row.context
    if row.value is None or not row.value.is_finite():
        return "requires a finite value"
    if context.scale != 0 or context.currency is not None or context.quantity not in ("rate", "unknown"):
        return "requires a rate with scale zero and no currency"
    if scope == "regime":
        if context.unit != "percentage_points" or context.basis not in (None, "treasury_constant_maturity"):
            return "requires the DFII10 endpoint change in percentage points"
    elif scope == "signal":
        if context.unit != "percent" or context.basis not in (None, PRICE_BASIS):
            return f"requires momentum in percent on the {PRICE_BASIS} basis"
    elif context.unit != "percent" or context.basis != _RETURN_BASIS or row.value < -100:
        return "requires a simple open-to-open return in percent of at least -100"
    if scope in ("signal", "regime") and context.period_end not in (None, row.observation_date):
        return "measurement period must end on the decision session"
    return None


def _select(
    rows: Sequence[Observation],
    cutoff: EvaluationCutoff,
    scope: ExclusionScope,
) -> Observation | StudyExclusion:
    subject = scope.replace("_", " ")
    latest = latest_observed_rows(rows, cutoff, subject)
    if isinstance(latest, str):
        timely_ids = tuple(sorted(row.record_id for row in rows if cutoff.is_eligible(row)))
        return StudyExclusion(scope, "unavailable" if rows else "missing", latest, timely_ids)
    return _validate_latest(latest, scope)


def _validate_latest(
    latest: list[Observation], scope: ExclusionScope,
) -> Observation | StudyExclusion:
    subject = scope.replace("_", " ")
    latest.sort(key=lambda row: row.record_id)
    if len({row.value for row in latest}) > 1:
        return StudyExclusion(scope, "conflict", f"conflicting {subject} values at the same revision",
                              tuple(row.record_id for row in latest))
    for row in latest:
        if issue := _financial_issue(row, scope):
            return StudyExclusion(scope, "invalid", f"{subject} {issue}", (row.record_id,))
    return latest[0]


def _affected_ends(
    row: Observation, starts: tuple[date, ...], ends: tuple[date, ...],
) -> set[date]:
    period_end = row.context.period_end or row.observation_date
    period_start = row.context.period_start or row.observation_date
    affected: set[date] = set()
    if period_start < period_end:
        # The intervals intersect only when their interiors overlap.
        first = bisect_right(ends, period_start)
        stop = bisect_left(starts, period_end)
        affected.update(ends[first:stop])
    for anchor in (row.observation_date, period_end):
        index = bisect_left(ends, anchor)
        if index < len(ends) and starts[index] < anchor:
            affected.add(ends[index])
    return affected


def _can_be_realized(row: Observation, opens: dict[date, datetime], zone: ZoneInfo) -> bool:
    publication = row.published_at
    if publication is None:
        # The observed-vintage selector supplies the missing availability reason.
        return True
    claimed_days = (row.observation_date, row.context.period_end)
    # A revision can name an end beyond the supplied calendar. Even there,
    # its return cannot have been realized on an earlier local publication date.
    local_day = publication.astimezone(zone).date()
    return all(
        publication >= opens[day] if day in opens else local_day >= day
        for day in claimed_days if day is not None
    )


def _matches_interval(row: Observation, start: date | None) -> bool:
    return (start is not None
            and (row.context.period_start, row.context.period_end) == (start, row.observation_date))


def _return_index(
    rows: Sequence[Observation],
    entity: str,
    plan: StudyPlan,
    scope: ExclusionScope,
) -> dict[date, Observation | StudyExclusion]:
    subject = scope.replace("_", " ")
    starts = tuple(session.day for session in plan.sessions[1:-1])
    ends = tuple(session.day for session in plan.sessions[2:])
    start_by_end = dict(zip(ends, starts, strict=True))
    zone = ZoneInfo(plan.cutoff.session_timezone)
    selected: dict[date, Observation | StudyExclusion] = {
        day: StudyExclusion(scope, "missing", f"missing {subject}") for day in ends
    }
    malformed: dict[date, set[str]] = defaultdict(set)
    for day, revisions in _rows_by_date(rows, entity, "forward_return").items():
        expected_start = start_by_end.get(day)
        timely = [row for row in revisions if _can_be_realized(row, plan.calendar_opens, zone)]
        # Period boundaries can change in a correction. Resolve the revision by
        # observation identity before inspecting its interval.
        latest = latest_observed_rows(timely, plan.cutoff, subject)
        if isinstance(latest, str):
            if any(_matches_interval(row, expected_start) for row in revisions):
                reason = latest if timely else "return published before the ending open"
                selected[day] = StudyExclusion(scope, "unavailable", reason)
            continue
        exact: list[Observation] = []
        for row in latest:
            if _matches_interval(row, expected_start):
                exact.append(row)
            else:
                for end in _affected_ends(row, starts, ends):
                    malformed[end].add(row.record_id)
        if exact:
            selected[day] = _validate_latest(exact, scope)
    for day, record_ids in malformed.items():
        selected[day] = StudyExclusion(
            scope, "invalid_interval", "return period conflicts with the dated one-session interval",
            tuple(sorted(record_ids)),
        )
    return selected


def _decision_cutoff(
    cutoff: EvaluationCutoff, decision: StudySession, start: StudySession,
) -> EvaluationCutoff:
    if decision.decision_at >= start.opens_at:
        raise ValueError(f"Decision on {decision.day} must precede the open on {start.day}")
    return EvaluationCutoff(
        observation_date=decision.day,
        decision_at=decision.decision_at,
        evaluated_at=cutoff.cutoff_at,
        session_timezone=cutoff.session_timezone,
    )


def _regime(row: Observation | None) -> Regime | None:
    if row is None or row.value is None:
        return None
    if row.value > 0:
        return "rising"
    if row.value < 0:
        return "falling"
    return "flat"


def _row_or_exclusion(
    selected: Observation | StudyExclusion,
    exclusions: list[StudyExclusion],
) -> Observation | None:
    if isinstance(selected, StudyExclusion):
        exclusions.append(selected)
        return None
    return selected


def _relative(strategy: Decimal | None, benchmark: Observation | None) -> Decimal | None:
    if strategy is None or benchmark is None or benchmark.value is None:
        return None
    # Preserve differences across the full financial decimal input range.
    with localcontext(Context(prec=77)):
        return strategy - benchmark.value


def _interval(
    decision: StudySession,
    start: StudySession,
    end: StudySession,
    global_cutoff: EvaluationCutoff,
    signals: Sequence[Observation],
    regimes: Sequence[Observation],
    asset_selection: Observation | StudyExclusion,
    benchmark_selection: Observation | StudyExclusion,
) -> StudyInterval:
    exclusions: list[StudyExclusion] = []
    cutoff = _decision_cutoff(global_cutoff, decision, start)
    signal = _row_or_exclusion(_select(signals, cutoff, "signal"), exclusions)
    trend = _row_or_exclusion(_select(regimes, cutoff, "regime"), exclusions)
    position: Position | None = None
    strategy = None
    asset = None
    if signal is not None and signal.value is not None:
        if signal.value > 0:
            position = "long"
            asset = _row_or_exclusion(asset_selection, exclusions)
            if asset is not None:
                strategy = asset.value
        else:
            position, strategy = "cash", Decimal(0)
    benchmark = _row_or_exclusion(benchmark_selection, exclusions)
    return StudyInterval(
        decision_date=decision.day, start=start.day, end=end.day, regime=_regime(trend),
        position=position, strategy_return=strategy,
        benchmark_relative_return=_relative(strategy, benchmark),
        signal_row=signal, regime_row=trend, asset_row=asset, benchmark_row=benchmark,
        exclusions=tuple(exclusions),
    )


def build_study_groups(inputs: InputSnapshot, assumptions: AssumptionSet) -> StudyGroups:
    """Resolve the expected return path and group coverage under the validated study plan."""
    plan = study_plan(inputs, assumptions)
    tables = {table.table_id: table.rows for table in inputs.tables}
    signals = _rows_by_date(tables.get("dated_signals", ()), plan.universe, "momentum")
    regimes = _rows_by_date(tables.get("dated_regimes", ()), "DFII10", "endpoint_change")
    returns = tables.get("forward_returns", ())
    assets = _return_index(returns, plan.universe, plan, "asset_return")
    benchmarks = _return_index(returns, plan.benchmark, plan, "benchmark_return")
    intervals = tuple(
        _interval(decision, start, end, plan.cutoff, signals.get(decision.day, ()),
                  regimes.get(decision.day, ()), assets[end.day], benchmarks[end.day])
        for decision, start, end in zip(plan.sessions[:-2], plan.sessions[1:-1], plan.sessions[2:], strict=True)
    )
    groups = tuple(StudyGroup(plan.partition, regime, tuple(item for item in intervals if item.regime == regime))
                   for regime in _REGIMES)
    return StudyGroups(plan, intervals, groups)
