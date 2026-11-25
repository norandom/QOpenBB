"""Dated schedule and point-in-time inputs for ETF factor windows."""

from datetime import date, timedelta
from decimal import Decimal

import pytest
from fixtures.factor_inputs import END, SESSIONS, START, cutoff, prices, schedule, utc
from qopenbb_data.modeling.models.factors.sessions import (
    WindowUnavailable,
    resolve_price_window,
    resolve_session_window,
)

CALENDAR = "fixture_us_listing"
REVISION = "fixture_us_listing.2024r1"
PROXY = "fixture_left"
BASIS = "split_adjusted_dividends_excluded"


def session_window(rows=None, *, evaluation=None, revision=REVISION):
    return resolve_session_window(
        schedule().rows if rows is None else rows,
        calendar_id=CALENDAR,
        schedule_revision=revision,
        cutoff=cutoff(END) if evaluation is None else evaluation,
    )


def close_rows():
    return prices("closes", PROXY, "120", False).rows


def price_window(rows, *, window=None):
    return resolve_price_window(session_window() if window is None else window, rows, proxy_id=PROXY)


def test_resolves_ordered_prices_and_preserves_holiday_adjacency():
    days = schedule().rows
    older = days[0].model_copy(update={"observation_date": date(2023, 12, 29)})
    later = days[-1].model_copy(update={"observation_date": date(2024, 4, 4)})
    foreign = days[-1].model_copy(update={
        "entity_id": "other_listing", "observation_date": date(2024, 3, 29),
    })
    window = session_window([later, *reversed(days), older, foreign])
    closes = close_rows()
    holiday = closes[-1].model_copy(update={"observation_date": date(2024, 3, 29)})
    resolved = price_window([holiday, *reversed(closes)], window=window)

    assert window.calendar_id == CALENDAR
    assert window.schedule_revision == REVISION
    assert window.cutoff == cutoff(END)
    assert window.endpoints == (START, END)
    assert window.session_dates == SESSIONS
    assert window.session_dates[-5:] == (date(2024, 3, 27), date(2024, 3, 28),
                                        date(2024, 4, 1), date(2024, 4, 2), END)
    assert resolved.window == window
    assert resolved.proxy_id == PROXY
    assert resolved.basis == BASIS
    assert resolved.closes == closes


@pytest.mark.parametrize("revision", [None, "", " \t"])
def test_requires_named_schedule_revision(revision):
    with pytest.raises(WindowUnavailable, match=f"{END}.*schedule revision"):
        session_window(revision=revision)


def test_ending_session_must_match_exactly():
    holiday = date(2024, 3, 29)
    foreign_session = schedule().rows[-1].model_copy(update={
        "entity_id": "other_listing", "observation_date": holiday,
    })
    with pytest.raises(WindowUnavailable, match=f"{holiday}.*ending session"):
        session_window((*schedule().rows, foreign_session), evaluation=cutoff(holiday))


def test_schedule_needs_64_distinct_sessions_even_with_duplicates():
    rows = schedule().rows[1:]
    with pytest.raises(WindowUnavailable, match=f"{END}.*64.*63"):
        session_window((*rows, rows[0]))


@pytest.mark.parametrize(("position", "change", "reason"), [
    (20, {"published_at": None}, "unknown historical availability"),
    (20, {"published_at": utc(END, 23)}, "after cutoff"),
    (-1, {"vintage_at": utc(END, 23)}, "after cutoff"),
])
def test_unavailable_required_schedule_row_does_not_backfill(position, change, reason):
    rows = list(schedule().rows)
    original = rows[position]
    rows[position] = original.model_copy(update=change)
    older = rows[0].model_copy(update={"observation_date": date(2023, 12, 29)})
    with pytest.raises(WindowUnavailable, match=f"{original.observation_date}.*{reason}") as error:
        session_window([older, *rows])
    assert error.value.issues[0].session_date == original.observation_date
    assert "schedule session" in error.value.issues[0].reason


@pytest.mark.parametrize("value", [None, Decimal(0), Decimal(2)])
def test_requires_affirmative_schedule_marker(value):
    rows = list(schedule().rows)
    day = rows[20].observation_date
    rows[20] = rows[20].model_copy(update={"value": value})
    with pytest.raises(WindowUnavailable, match=f"{day}.*schedule marker"):
        session_window(rows)


def test_requires_session_unit_on_schedule_marker():
    rows = list(schedule().rows)
    context = rows[-1].context.model_copy(update={"unit": "price"})
    rows[-1] = rows[-1].model_copy(update={"context": context})
    with pytest.raises(WindowUnavailable, match=f"{END}.*schedule marker"):
        session_window(rows)


def test_later_estimate_preserves_observed_schedule_marker():
    rows = schedule().rows
    estimate = rows[20].model_copy(update={
        "record_id": "estimated_marker", "category": "estimate",
        "value": Decimal(0), "published_at": utc(END, 21),
    })
    assert session_window([estimate, *rows]).session_dates == SESSIONS


def test_estimate_only_schedule_date_fails_without_backfill():
    rows = list(schedule().rows)
    marker = rows[20]
    rows[20] = marker.model_copy(update={"category": "estimate"})
    older = rows[0].model_copy(update={"observation_date": date(2023, 12, 29)})
    with pytest.raises(
        WindowUnavailable, match=f"{marker.observation_date}.*only estimates.*schedule session"
    ):
        session_window([older, *rows])


def test_reports_both_missing_dates_and_keeps_calendar_endpoints():
    window = session_window()
    closes = close_rows()
    first_gap, second_gap = closes[12], closes[-1]
    foreign = first_gap.model_copy(update={"entity_id": "fixture_right"})
    off_session = second_gap.model_copy(update={"observation_date": date(2024, 3, 29)})
    with pytest.raises(WindowUnavailable, match="missing close") as error:
        price_window([foreign, *closes[:12], *closes[13:-1], off_session], window=window)
    assert [issue.session_date for issue in error.value.issues] == [
        first_gap.observation_date, second_gap.observation_date,
    ]
    assert window.endpoints == (START, END)


@pytest.mark.parametrize("bad_value", [None, Decimal(0), Decimal(-1), Decimal("NaN"), Decimal("Infinity")])
def test_requires_finite_positive_close(bad_value):
    closes = close_rows()
    # Nonfinite values are also rejected at the wire boundary.
    bad = closes[-1].model_copy(update={"value": bad_value})
    with pytest.raises(WindowUnavailable, match=f"{END}.*finite positive"):
        price_window([*closes[:-1], bad])


@pytest.mark.parametrize("change", [
    {"basis": None}, {"basis": "total_return"}, {"basis": "unadjusted"},
    {"unit": "percent"}, {"currency": "CAD"}, {"scale": 3},
])
def test_requires_consistent_split_adjusted_price_basis(change):
    closes = close_rows()
    bad = closes[-1].model_copy(update={"context": closes[-1].context.model_copy(update=change)})
    with pytest.raises(WindowUnavailable, match=f"{END}.*price basis"):
        price_window([*closes[:-1], bad])


def test_chooses_newest_eligible_revision_in_either_input_order():
    closes = close_rows()
    original = closes[-1]
    evaluation = cutoff(END)
    revised = original.model_copy(update={
        "record_id": "at_decision", "vintage_at": evaluation.decision_at, "value": Decimal("121.03"),
    })
    intervening = original.model_copy(update={
        "record_id": "later_publication_older_vintage", "published_at": evaluation.decision_at,
        "vintage_at": original.published_at + timedelta(minutes=30), "value": Decimal(119),
    })
    too_late = revised.model_copy(update={
        "record_id": "after_decision", "published_at": evaluation.decision_at + timedelta(microseconds=1),
        "vintage_at": evaluation.decision_at + timedelta(microseconds=1), "value": Decimal(140),
    })
    three_revisions = [too_late, original, revised, intervening]
    assert price_window([*closes[:-1], *three_revisions]).closes[-1] == revised
    assert price_window([*reversed(three_revisions), *closes[:-1]]).closes[-1] == revised


@pytest.mark.parametrize("hour", [21, 22], ids=["same-revision", "later-revision"])
def test_estimate_preserves_observed_close(hour):
    closes = close_rows()
    observed = closes[-1].model_copy(update={"category": "provider"})
    estimate = observed.model_copy(update={
        "record_id": "estimated_close", "category": "estimate",
        "value": Decimal(140), "published_at": utc(END, hour),
    })
    assert price_window([estimate, *closes[:-1], observed]).closes[-1] == observed


@pytest.mark.parametrize("include_late_close", [False, True])
def test_estimate_cannot_supply_a_required_close(include_late_close):
    closes = close_rows()
    estimated = closes[-1].model_copy(update={
        "record_id": "estimated_close", "category": "estimate",
    })
    candidates = [*closes[:-1], estimated]
    reason = "only estimates for close"
    if include_late_close:
        candidates.append(closes[-1].model_copy(update={"published_at": utc(END, 23)}))
        reason = "close available after cutoff"
    with pytest.raises(WindowUnavailable, match=f"{END}.*{reason}"):
        price_window(candidates)


def test_uses_evaluation_time_when_it_precedes_decision_time():
    closes = close_rows()
    first_eligible = utc(END, 20)
    final = closes[-1].model_copy(update={"published_at": first_eligible})
    evaluation = cutoff(END).model_copy(update={"evaluated_at": first_eligible})
    window = session_window(evaluation=evaluation)
    assert price_window([*closes, final], window=window).closes[-1] == final
    with pytest.raises(WindowUnavailable, match=f"{END}.*after cutoff"):
        price_window(closes, window=window)


@pytest.mark.parametrize(("change", "reason"), [
    ({"published_at": None}, "unknown historical availability"),
    ({"vintage_at": utc(END, 23)}, "after cutoff"),
    ({"published_at": utc(END + timedelta(days=1), 16)}, "after cutoff"),
])
def test_withholds_when_required_version_is_unavailable(change, reason):
    closes = close_rows()
    bad = closes[-1].model_copy(update=change)
    with pytest.raises(WindowUnavailable, match=f"{END}.*{reason}"):
        price_window([*closes[:-1], bad])


@pytest.mark.parametrize("coverage", ["unknown", "unavailable"])
def test_explicit_unproven_coverage_overrides_a_publication_time(coverage):
    closes = close_rows()
    context = closes[-1].context.model_copy(update={"vintage_coverage": coverage})
    bad = closes[-1].model_copy(update={"context": context})
    with pytest.raises(WindowUnavailable, match=f"{END}.*unknown historical availability"):
        price_window([*closes[:-1], bad])


def test_identical_closes_at_same_revision_have_stable_source_selection():
    closes = close_rows()
    duplicate = closes[-1].model_copy(update={"record_id": "a_duplicate"})
    assert price_window([*closes, duplicate]).closes[-1] == duplicate
    assert price_window([duplicate, *closes]).closes[-1] == duplicate


@pytest.mark.parametrize("change", [{"value": Decimal(125)}, {"currency": "CAD"}])
def test_conflicting_closes_at_same_revision_fail_in_either_order(change):
    closes = close_rows()
    original = closes[-1].model_copy(update={"vintage_at": utc(END, 20)})
    duplicate = original.model_copy(update={"record_id": "conflicting", "published_at": utc(END, 22)})
    if "currency" in change:
        duplicate = duplicate.model_copy(update={"context": duplicate.context.model_copy(update=change)})
    else:
        duplicate = duplicate.model_copy(update=change)
    for candidates in ([original, duplicate], [duplicate, original]):
        with pytest.raises(WindowUnavailable, match=f"{END}.*conflicting duplicate"):
            price_window([*closes[:-1], *candidates])


def test_invalid_current_revision_cannot_fall_back_to_older_price():
    closes = close_rows()
    revised = closes[-1].model_copy(update={
        "record_id": "invalid_revision", "vintage_at": utc(END, 22), "value": Decimal(0),
    })
    with pytest.raises(WindowUnavailable, match=f"{END}.*finite positive"):
        price_window([*closes, revised])
