from datetime import date, datetime, time
from zoneinfo import ZoneInfo

import pytest
from qopenbb_data.modeling.contracts import EvaluationCutoff
from qopenbb_data.modeling.service.story_schedule import (
    CALENDAR_ID,
    REVISION,
    story_sessions,
)


def cutoff(day):
    stamp = datetime.combine(date.fromisoformat(day), time(23, 59), ZoneInfo("America/New_York"))
    return EvaluationCutoff(observation_date=stamp.date(), decision_at=stamp, evaluated_at=stamp,
                            session_timezone="America/New_York")


def test_verified_window_comes_from_exchange_revision():
    selection = cutoff("2026-11-13")
    rows = story_sessions(selection, CALENDAR_ID, REVISION).rows
    assert len(rows) == 64
    assert rows[0].observation_date == date(2026, 8, 17)
    assert rows[-1].observation_date == selection.observation_date
    assert all(selection.is_eligible(row) for row in rows)
    assert date(2026, 9, 7) not in {row.observation_date for row in rows}


def test_closed_dates_and_partial_days_are_distinct():
    assert story_sessions(cutoff("2026-11-26"), CALENDAR_ID, REVISION).rows == ()
    rows = story_sessions(cutoff("2026-11-27"), CALENDAR_ID, REVISION).rows
    assert rows[-1].context.basis == "early_close_1300_eastern"
    assert len(story_sessions(cutoff("2026-01-02"), CALENDAR_ID, REVISION).rows) == 1


@pytest.mark.parametrize(("day", "cal", "revision"), [
    ("2027-01-04", CALENDAR_ID, REVISION), ("2026-06-01", "OTHER", REVISION),
    ("2026-06-01", CALENDAR_ID, "unbound"),
])
def test_uncovered_schedule_rejected(day, cal, revision):
    with pytest.raises(ValueError):
        story_sessions(cutoff(day), cal, revision)
