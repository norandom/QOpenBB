"""Resolve story session dates from the packaged revision of the exchange schedule."""

import json
from datetime import date, datetime, time, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

from ..contracts import EvaluationCutoff, Observation, ObservationTable
from ..contracts.inputs import FinancialContext
from ..models.factors.sessions import WINDOW_SIZE

_SCHEDULE = json.loads(Path(__file__).with_name("calendars").joinpath("nyse_arca.json").read_bytes())
CALENDAR_ID = _SCHEDULE["calendar_id"]
REVISION = _SCHEDULE["revision"]
_START = date.fromisoformat(_SCHEDULE["coverage_start"])
_END = date.fromisoformat(_SCHEDULE["coverage_end"])
_HOLIDAYS = frozenset(map(date.fromisoformat, _SCHEDULE["holidays"]))
_EARLY = frozenset(map(date.fromisoformat, _SCHEDULE["early_close_1300_eastern"]))
# ICE dates the release to a day. Midnight the following day is a conservative availability bound.
_AVAILABLE = datetime.combine(date.fromisoformat(_SCHEDULE["announcement_date"]) + timedelta(days=1),
                              time.min, ZoneInfo(_SCHEDULE["session_timezone"]))


def _open(day: date) -> bool:
    return day.weekday() < 5 and day not in _HOLIDAYS


def _marker(day: date) -> Observation:
    return Observation(
        record_id=f"{REVISION}.{day}", entity_id=CALENDAR_ID, metric_id="session", observation_date=day,
        category="provider", published_at=_AVAILABLE, value="1", source_record_id=f"NYSE.{REVISION}.{day}",
        context=FinancialContext(unit="session", vintage_coverage="known",
                                 basis="early_close_1300_eastern" if day in _EARLY else "regular_session"),
    )


def story_sessions(cutoff: EvaluationCutoff, calendar_id: str, revision: str) -> ObservationTable:
    day = cutoff.observation_date
    if (calendar_id, revision, cutoff.session_timezone) != (CALENDAR_ID, REVISION, _SCHEDULE["session_timezone"]):
        raise ValueError("Unknown story calendar, revision or session timezone")
    if not _START <= day <= _END or cutoff.cutoff_at < _AVAILABLE:
        raise ValueError(f"Exchange schedule {revision} is unavailable for {day}")
    rows = []
    if _open(day):
        while day >= _START and len(rows) < WINDOW_SIZE:
            if _open(day):
                rows.append(_marker(day))
            day -= timedelta(days=1)
    return ObservationTable(table_id="sessions", grain="One open exchange session per date in the pinned revision.",
                            keys=("entity_id", "observation_date"), nullable=False, rows=tuple(reversed(rows)))
