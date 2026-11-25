"""Read the timing study's supplied calendar and point-in-time observations."""

from bisect import bisect_left, bisect_right
from collections import defaultdict
from collections.abc import Iterable
from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal
from itertools import accumulate, pairwise
from zoneinfo import ZoneInfo

from ...contracts import AssumptionSet, InputSnapshot, Observation

_METHOD = {
    "position_rule": "long_when_momentum_positive.v1",
    "horizon": "one_session_open_to_open",
    "drawdown_basis": "full_study_exposed_returns",
}
_SCOPE_CONTEXT = {
    "signal": ("percent", {None, "split_adjusted_dividends_excluded"}),
    "regime": ("percentage_points", {None, "treasury_constant_maturity"}),
    "return": ("percent", {"open_to_open"}),
}


@dataclass(frozen=True)
class Session:
    day: date
    opening: datetime
    decision: datetime


@dataclass(frozen=True)
class TimingWindow:
    sessions: tuple[Session, ...]
    as_of: datetime
    observation_date: date
    zone: ZoneInfo
    opens: dict[date, datetime]
    universe: str
    benchmark: str
    partition: str


def _sessions(settings: dict[str, str], zone: ZoneInfo) -> list[Session]:
    chunks = {key for key in settings if key == "study_schedule" or key.startswith("study_schedule.")}
    names = ["study_schedule", *(f"study_schedule.{i}" for i in range(2, len(chunks) + 1))]
    if chunks != set(names):
        raise ValueError("Invalid study calendar chunks")
    sessions = []
    for name in names:
        for entry in settings[name].split(";"):
            opening, decision = map(datetime.fromisoformat, entry.split("/"))
            if opening.utcoffset() is None or decision.utcoffset() is None:
                raise ValueError("Calendar timestamps require UTC offsets")
            day = opening.astimezone(zone).date()
            if decision.astimezone(zone).date() != day or decision <= opening:
                raise ValueError("Invalid session open or decision")
            sessions.append(Session(day, opening, decision))
    return sorted(sessions, key=lambda session: session.day)


def read_window(inputs: InputSnapshot, assumptions: AssumptionSet) -> TimingWindow:
    cutoff = inputs.cutoff
    if (inputs.schema_id != "timing_study.inputs" or inputs.schema_version != "1"
            or assumptions.version != "1" or cutoff is None):
        raise ValueError("Incompatible timing study inputs")
    settings = {item.assumption_id: item.value for item in assumptions.assumptions
                if item.value_type == "text" and isinstance(item.value, str)}
    if any(item.assumption_id.startswith("study_schedule.") and item.assumption_id not in settings
           for item in assumptions.assumptions):
        raise ValueError("Study calendar chunks require text")
    if any(settings.get(key) != value for key, value in _METHOD.items()):
        raise ValueError("Unsupported study method")
    if not all(settings[key].strip() for key in ("schedule_revision", "universe", "benchmark")):
        raise ValueError("Missing study identity")
    if settings["partition"] not in {"in_sample", "out_of_sample"}:
        raise ValueError("Unsupported study partition")
    start, end = map(date.fromisoformat, settings["study_dates"].split("/"))
    if not start < end <= cutoff.observation_date:
        raise ValueError("Invalid study dates")
    zone = ZoneInfo(cutoff.session_timezone)
    sessions = _sessions(settings, zone)
    dates = [session.day for session in sessions]
    first, last = dates.index(start), dates.index(end)
    if first == 0 or len(set(dates)) != len(dates):
        raise ValueError("Missing preceding decision or duplicate session")
    window = tuple(sessions[first - 1:last + 1])
    as_of = min(cutoff.decision_at, cutoff.evaluated_at)
    if assumptions.effective_date > window[0].day or window[-1].opening > as_of:
        raise ValueError("Study window outside historical coverage")
    if any(before.opening >= after.opening for before, after in pairwise(window)):
        raise ValueError("Outcome opens must advance chronologically")
    if any(before.decision >= after.opening for before, after in pairwise(window[:-1])):
        raise ValueError("Decision must precede the next open")
    opens = {session.day: session.opening for session in sessions}
    return TimingWindow(window, as_of, cutoff.observation_date, zone, opens,
                        settings["universe"], settings["benchmark"], settings["partition"])


def by_day(rows: Iterable[Observation], entity: str, metric: str) -> dict[date, list[Observation]]:
    selected: dict[date, list[Observation]] = defaultdict(list)
    for row in rows:
        if row.entity_id == entity and row.metric_id == metric:
            selected[row.observation_date].append(row)
    return selected


def _latest(rows: Iterable[Observation], limit: datetime) -> list[Observation]:
    latest: list[Observation] = []
    revision = None
    for row in rows:
        publication = row.published_at
        if (publication is None or row.category == "estimate"
                or row.context.vintage_coverage in {"unknown", "unavailable"}):
            continue
        vintage = row.vintage_at or publication
        if max(vintage, publication) > limit:
            continue
        if revision is None or vintage > revision:
            latest = [row]
            revision = vintage
        elif vintage == revision:
            latest.append(row)
    return latest


def _valid(row: Observation, scope: str) -> bool:
    context = row.context
    unit, bases = _SCOPE_CONTEXT[scope]
    if (row.value is None or not row.value.is_finite() or context.unit != unit
            or context.basis not in bases or context.scale != 0 or context.currency is not None
            or context.quantity not in {"rate", "unknown"}):
        return False
    if scope == "return":
        return row.value >= -100
    return context.period_end in (None, row.observation_date)


@dataclass(frozen=True)
class Reading:
    value: Decimal | None
    issue: str | None = None


def _amount(rows: list[Observation], scope: str) -> Reading:
    if len({row.value for row in rows}) != 1:
        return Reading(None, "conflict" if rows else "unavailable")
    if not all(_valid(row, scope) for row in rows):
        return Reading(None, "invalid")
    return Reading(rows[0].value)


def decision_amount(rows: tuple[Observation, ...] | list[Observation], limit: datetime, scope: str) -> Reading:
    return _amount(_latest(rows, limit), scope) if rows else Reading(None, "missing")


def _realized(row: Observation, window: TimingWindow) -> bool:
    publication = row.published_at
    if publication is None:
        return False
    # A claimed end can fall outside the supplied calendar. Its local date
    # still cannot be later than the date on which the return was published.
    latest_day = min(window.observation_date, publication.astimezone(window.zone).date())
    return all(
        day <= latest_day and (day not in window.opens or publication >= window.opens[day])
        for day in (row.observation_date, row.context.period_end or row.observation_date)
    )


def _overlaps(row: Observation, starts: list[date], ends: list[date], changes: list[int]) -> None:
    # Mark ranges without visiting every interval spanned by a malformed revision.
    start = row.context.period_start or row.observation_date
    end = row.context.period_end or row.observation_date
    if start < end:
        first, stop = bisect_right(ends, start), bisect_left(starts, end)
        if first < stop:
            changes[first] += 1
            changes[stop] -= 1
    for anchor in {row.observation_date, end}:
        index = bisect_left(ends, anchor)
        if index < len(ends) and starts[index] < anchor:
            changes[index] += 1
            changes[index + 1] -= 1


def _exact(row: Observation, start: date | None) -> bool:
    return start is not None and (row.context.period_start, row.context.period_end) == (start, row.observation_date)


def return_amounts(rows: tuple[Observation, ...], entity: str, window: TimingWindow) -> dict[date, Reading]:
    starts = [session.day for session in window.sessions[1:-1]]
    ends = [session.day for session in window.sessions[2:]]
    expected = dict(zip(ends, starts, strict=True))
    changes = [0] * (len(ends) + 1)
    selected = {}
    for day, revisions in by_day(rows, entity, "forward_return").items():
        if day > window.observation_date:
            continue
        start = expected.get(day)
        latest = _latest((row for row in revisions if _realized(row, window)), window.as_of)
        exact = []
        for row in latest:
            if _exact(row, start):
                exact.append(row)
            else:
                _overlaps(row, starts, ends, changes)
        if exact:
            selected[day] = _amount(exact, "return")
        elif not latest and any(_exact(row, start) for row in revisions):
            selected[day] = Reading(None, "unavailable")
    return {
        day: Reading(None, "invalid_interval") if overlap else selected.get(day, Reading(None, "missing"))
        for day, overlap in zip(ends, accumulate(changes))
    }
