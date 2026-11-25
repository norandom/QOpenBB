"""Trading-session windows and point-in-time ETF close selection."""

from collections import defaultdict
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from datetime import date, datetime

from ...contracts import EvaluationCutoff, Observation

WINDOW_SIZE = 64
PRICE_BASIS = "split_adjusted_dividends_excluded"


@dataclass(frozen=True)
class SessionWindow:
    calendar_id: str
    schedule_revision: str
    cutoff: EvaluationCutoff
    session_dates: tuple[date, ...]

    @property
    def endpoints(self) -> tuple[date, date]:
        return self.session_dates[0], self.session_dates[-1]


@dataclass(frozen=True)
class PriceWindow:
    window: SessionWindow
    proxy_id: str
    closes: tuple[Observation, ...]

    @property
    def basis(self) -> str:
        return PRICE_BASIS


@dataclass(frozen=True)
class WindowIssue:
    session_date: date
    reason: str


class WindowUnavailable(ValueError):
    def __init__(self, subject: str, issues: Iterable[WindowIssue]) -> None:
        self.issues = tuple(issues)
        details = ", ".join(f"{issue.session_date} {issue.reason}" for issue in self.issues)
        super().__init__(f"{subject} has insufficient history ({details})")


def _revision_at(row: Observation) -> datetime:
    # The publication timestamp still gates eligibility when a vintage timestamp is supplied.
    assert row.published_at is not None
    return row.vintage_at or row.published_at


def _latest_observed_rows(
    rows: Sequence[Observation], cutoff: EvaluationCutoff, subject: str
) -> list[Observation] | str:
    if not rows:
        return f"missing {subject}"
    observed = [row for row in rows if row.category != "estimate"]
    if not observed:
        return f"only estimates for {subject}"
    eligible = [row for row in observed if cutoff.is_eligible(row)]
    if not eligible:
        return _availability_reason(observed, subject)
    latest = max(map(_revision_at, eligible))
    return [row for row in eligible if _revision_at(row) == latest]


def _availability_reason(rows: Sequence[Observation], subject: str) -> str:
    if any(
        row.published_at is None or row.context.vintage_coverage in ("unknown", "unavailable")
        for row in rows
    ):
        return f"unknown historical availability for {subject}"
    return f"{subject} available after cutoff"


def _schedule_issue(rows: Sequence[Observation], cutoff: EvaluationCutoff) -> str | None:
    latest = _latest_observed_rows(rows, cutoff, "schedule session")
    if isinstance(latest, str):
        return latest
    for row in latest:
        marker = row.value
        if row.context.unit != "session" or marker is None or not marker.is_finite() or marker != 1:
            return "invalid schedule marker (expected value 1 with session unit)"
    return None


def resolve_session_window(
    schedule: Iterable[Observation],
    *,
    calendar_id: str,
    schedule_revision: str | None,
    cutoff: EvaluationCutoff,
) -> SessionWindow:
    """Resolve the exact ending date using schedule rows pinned to the supplied revision."""
    ending = cutoff.observation_date
    if not schedule_revision or not schedule_revision.strip():
        reason = "requires a named schedule revision"
        raise WindowUnavailable(f"Calendar {calendar_id}", [WindowIssue(ending, reason)])
    subject = f"Calendar {calendar_id} revision {schedule_revision}"

    by_date: dict[date, list[Observation]] = defaultdict(list)
    for row in schedule:
        if row.entity_id == calendar_id and row.metric_id == "session" and row.observation_date <= ending:
            by_date[row.observation_date].append(row)
    if ending not in by_date:
        raise WindowUnavailable(subject, [WindowIssue(ending, "ending session is absent from schedule")])

    # Pin the dates before checking evidence so an unconfirmed session cannot shift the window.
    dates = tuple(sorted(by_date)[-WINDOW_SIZE:])
    if len(dates) < WINDOW_SIZE:
        reason = f"requires {WINDOW_SIZE} scheduled sessions, found {len(dates)}"
        raise WindowUnavailable(subject, [WindowIssue(ending, reason)])
    issues = []
    for day in dates:
        if reason := _schedule_issue(by_date[day], cutoff):
            issues.append(WindowIssue(day, reason))
    if issues:
        raise WindowUnavailable(subject, issues)
    return SessionWindow(calendar_id, schedule_revision, cutoff, dates)


def _price_basis(row: Observation) -> tuple[str, str | None, str | None, int]:
    context = row.context
    return context.unit, context.basis, context.currency, context.scale


def _select_close(rows: Sequence[Observation], cutoff: EvaluationCutoff) -> Observation | str:
    latest = _latest_observed_rows(rows, cutoff, "close")
    if isinstance(latest, str):
        return latest
    for row in latest:
        close = row.value
        if close is None or not close.is_finite() or close <= 0:
            return "close must be finite positive"
    if len(latest) == 1:
        return latest[0]
    if len({(row.value, _price_basis(row)) for row in latest}) > 1:
        return "conflicting duplicate closes at the same revision"
    return min(latest, key=lambda row: (row.record_id, row.fingerprint()))


def resolve_price_window(
    window: SessionWindow,
    observations: Iterable[Observation],
    *,
    proxy_id: str,
) -> PriceWindow:
    """Join one proxy's closes to the validated calendar dates at the same cutoff."""
    by_date: dict[date, list[Observation]] = {day: [] for day in window.session_dates}
    for row in observations:
        if row.entity_id == proxy_id and row.metric_id == "close" and row.observation_date in by_date:
            by_date[row.observation_date].append(row)

    closes: list[Observation] = []
    issues: list[WindowIssue] = []
    for day, rows in by_date.items():
        close = _select_close(rows, window.cutoff)
        if isinstance(close, str):
            issues.append(WindowIssue(day, close))
        elif close.context.unit != "price" or close.context.basis != PRICE_BASIS:
            issues.append(WindowIssue(day, f"price basis must be {PRICE_BASIS} with price unit"))
        elif closes and _price_basis(close) != _price_basis(closes[0]):
            issues.append(WindowIssue(day, f"price basis differs from {closes[0].observation_date}"))
        else:
            closes.append(close)
    if issues:
        raise WindowUnavailable(f"Proxy {proxy_id}", issues)
    return PriceWindow(window, proxy_id, tuple(closes))
