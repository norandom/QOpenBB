"""Versioned assumptions and actual session instants for a one-session timing study."""

from dataclasses import dataclass
from datetime import UTC, date, datetime
from zoneinfo import ZoneInfo

from ...contracts import AssumptionSet, EvaluationCutoff, InputSnapshot
from .method_inputs import evaluation_cutoff, text_assumption


@dataclass(frozen=True)
class StudySession:
    day: date
    opens_at: datetime
    decision_at: datetime


@dataclass(frozen=True)
class StudyPlan:
    sessions: tuple[StudySession, ...]
    calendar_opens: dict[date, datetime]
    universe: str
    benchmark: str
    partition: str
    cutoff: EvaluationCutoff
    assumptions: AssumptionSet
    start: date
    end: date


def _session(entry: str, zone: ZoneInfo) -> StudySession:
    try:
        opens, decision = (datetime.fromisoformat(stamp) for stamp in entry.split("/"))
    except ValueError as exc:
        raise ValueError("study_schedule requires open/decision timestamp pairs") from exc
    if opens.utcoffset() is None or decision.utcoffset() is None:
        raise ValueError("study_schedule timestamps require explicit UTC offsets")
    day = opens.astimezone(zone).date()
    if opens >= decision or decision.astimezone(zone).date() != day:
        raise ValueError(f"Invalid session open and decision times on {day}")
    return StudySession(day, opens.astimezone(UTC), decision.astimezone(UTC))


def _schedule_entries(assumptions: AssumptionSet) -> list[str]:
    # Each wire text field is bounded; later chunks carry longer trading calendars.
    prefix = "study_schedule."
    keys = {item.assumption_id for item in assumptions.assumptions if item.assumption_id.startswith(prefix)}
    expected = [f"{prefix}{number}" for number in range(2, len(keys) + 2)]
    if keys != set(expected):
        raise ValueError("study_schedule chunks must be numbered consecutively starting at 2")
    return [entry for key in ("study_schedule", *expected)
            for entry in text_assumption(assumptions, key).split(";")]


def _study_window(
    assumptions: AssumptionSet, cutoff: EvaluationCutoff,
) -> tuple[tuple[StudySession, ...], dict[date, datetime]]:
    try:
        start, end = (date.fromisoformat(part) for part in text_assumption(assumptions, "study_dates").split("/"))
    except ValueError as exc:
        raise ValueError("study_dates requires an inclusive start/end date pair") from exc
    if start >= end or end > cutoff.observation_date:
        raise ValueError(f"Invalid study_dates {start}/{end} at {cutoff.observation_date}")
    zone = ZoneInfo(cutoff.session_timezone)
    entries = _schedule_entries(assumptions)
    sessions = sorted((_session(entry, zone) for entry in entries), key=lambda session: session.day)
    dates = [session.day for session in sessions]
    if len(set(dates)) != len(dates):
        raise ValueError("study_schedule contains duplicate session dates")
    if start not in dates or end not in dates or start == dates[0]:
        raise ValueError("study_schedule requires both endpoints and a preceding decision session")
    window = tuple(sessions[dates.index(start) - 1:dates.index(end) + 1])
    if assumptions.effective_date > window[0].day:
        raise ValueError(f"Study assumptions were not effective on first decision date {window[0].day}")
    if window[-1].opens_at > cutoff.cutoff_at:
        raise ValueError(f"Study ends after the historical evaluation cutoff on {end}")
    return window, {session.day: session.opens_at for session in sessions}


def study_plan(inputs: InputSnapshot, assumptions: AssumptionSet) -> StudyPlan:
    cutoff = evaluation_cutoff(inputs, assumptions, "timing_study")
    text_assumption(assumptions, "schedule_revision")
    for key, expected in (
        ("position_rule", "long_when_momentum_positive.v1"), ("horizon", "one_session_open_to_open"),
        ("drawdown_basis", "full_study_exposed_returns"),
    ):
        if text_assumption(assumptions, key) != expected:
            raise ValueError(f"Study requires {key}={expected}")
    universe = text_assumption(assumptions, "universe")
    benchmark = text_assumption(assumptions, "benchmark")
    partition = text_assumption(assumptions, "partition")
    if partition not in ("in_sample", "out_of_sample"):
        raise ValueError("Study partition must be in_sample or out_of_sample")
    sessions, calendar_opens = _study_window(assumptions, cutoff)
    return StudyPlan(sessions, calendar_opens, universe, benchmark, partition, cutoff, assumptions,
                     sessions[1].day, sessions[-1].day)
