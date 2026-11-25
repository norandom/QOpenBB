"""Benchmark-relative timing scores and whole-study strategy drawdown."""

from bisect import bisect_right
from collections import Counter
from dataclasses import dataclass
from decimal import Decimal
from fractions import Fraction
from itertools import batched
from operator import attrgetter

from ...contracts import (
    AssumptionSet,
    InputSnapshot,
    ModelDescriptor,
    Observation,
    OutputDescriptor,
    RuleDescriptor,
    TraceEntry,
    TraceValue,
)
from ..protocol import CandidateOutput, CandidateResult, Model
from .method_inputs import substitution
from .study_groups import StudyGroup, StudyGroups, StudyInterval, build_study_groups

_MODEL_ID = "timing_study"
_INPUTS = ("dated_signals", "dated_regimes", "forward_returns")
_DRAWDOWN_INPUTS = ("dated_signals", "forward_returns")
_COMMON_ASSUMPTIONS = {"schedule_revision", "position_rule", "horizon", "partition", "study_dates", "universe"}
_ROW_FIELDS = (
    ("signal", "signal_row"),
    ("regime", "regime_row"),
    ("asset_return", "asset_row"),
    ("benchmark_return", "benchmark_row"),
)
_SCORE_SCOPES = {scope for scope, _ in _ROW_FIELDS}
_DRAWDOWN_SCOPES = {"signal", "asset_return"}
_WIRE_POWERS = tuple(Fraction(10) ** exponent for exponent in range(-38, 39))


def _descriptor() -> ModelDescriptor:
    definitions = tuple(
        (f"{regime}_{metric}", f"{regime.title()} group {formula}", "ratio", _INPUTS)
        for regime in ("rising", "falling")
        for metric, formula in (
            ("hit_rate", "winners / eligible outcomes including ties"),
            ("slugging", "mean winner / absolute mean loser"),
        )
    ) + (("study_drawdown", "Maximum peak-to-trough loss on the full exposed wealth path",
          "percent", _DRAWDOWN_INPUTS),)
    return ModelDescriptor(
        model_id=_MODEL_ID, method_version="1", rule_set_version="1", reference_version="1",
        input_schema_id=f"{_MODEL_ID}.inputs", output_schema_id=f"{_MODEL_ID}.outputs",
        entity_types=("etf_study",), period_types=("study_interval",), input_ids=_INPUTS,
        outputs=tuple(OutputDescriptor(
            output_id=name, semantic_definition=expression, unit=unit,
            required_input_ids=inputs, required_check_ids=(f"eligible_inputs.{name}",),
        ) for name, expression, unit, inputs in definitions),
        rules=tuple(RuleDescriptor(
            rule_id=f"eligible_inputs.{name}", version="1", stage="precondition", severity="blocking",
        ) for name, _, _, _ in definitions),
    )


_DESCRIPTOR = _descriptor()


def _wire_decimal(value: Fraction) -> Decimal:
    if not value:
        return Decimal(0)
    magnitude = abs(value)
    # Round the exact fraction once at the wire's 38-digit precision and scale.
    index = bisect_right(_WIRE_POWERS, magnitude)
    if not 0 < index < len(_WIRE_POWERS):
        raise ValueError("value exceeds financial decimal range")
    adjusted = index - 1 - 38
    exponent = max(-38, adjusted - 37)
    coefficient = Decimal(round(magnitude / (Fraction(10) ** exponent)))
    digits = coefficient.as_tuple().digits
    if len(digits) + exponent > 38:
        raise ValueError("value exceeds financial decimal range after rounding")
    return Decimal((int(value < 0), digits, exponent))


def _candidate(output: OutputDescriptor, value: Fraction | None, reason: str | None) -> CandidateOutput:
    decimal_value = None
    if value is not None:
        try:
            decimal_value = _wire_decimal(value)
        except ValueError as exc:
            reason = str(exc)
    return CandidateOutput(output_id=output.output_id, value=decimal_value, reason=reason)


@dataclass(frozen=True)
class _Trace:
    output: OutputDescriptor
    input_ids: tuple[str, ...]
    assumption_ids: tuple[str, ...]

    def entry(
        self, expression: str, *, suffix: str = "", records: tuple[Observation, ...] = (),
        values: tuple[TraceValue, ...] = (),
    ) -> TraceEntry:
        return TraceEntry(
            trace_id=self.output.output_id + suffix, formula_id=self.output.output_id, formula_version="1",
            expression=expression, output_id=self.output.output_id, check_ids=self.output.required_check_ids,
            input_ids=self.input_ids, assumption_ids=self.assumption_ids,
            source_record_ids=tuple(row.record_id for row in records),
            substitutions=tuple(substitution(row) for row in records if row.value is not None),
            intermediate_values=values,
        )


def _trace_context(
    output: OutputDescriptor, inputs: InputSnapshot, assumptions: AssumptionSet,
) -> _Trace:
    tables = {table.table_id for table in inputs.tables}
    extra = "drawdown_basis" if output.output_id == "study_drawdown" else "benchmark"
    keys = _COMMON_ASSUMPTIONS | {extra, "study_schedule"}
    return _Trace(
        output, tuple(table_id for table_id in output.required_input_ids if table_id in tables),
        tuple(item.assumption_id for item in assumptions.assumptions
              if item.assumption_id in keys or item.assumption_id.startswith("study_schedule.")),
    )


def _record_evidence(
    trace: _Trace, intervals: tuple[StudyInterval, ...], scopes: set[str],
    originals: dict[str, Observation], *, suffix: str = "",
) -> tuple[TraceEntry, ...]:
    ids: dict[str, None] = {}
    for interval in intervals:
        for scope, field in _ROW_FIELDS:
            if scope in scopes and (row := getattr(interval, field)) is not None:
                ids[row.record_id] = None
        for issue in interval.exclusions:
            if issue.scope in scopes:
                ids.update(dict.fromkeys(issue.record_ids))
    # A malformed return can affect multiple intervals. Cite each original row once.
    return tuple(
        trace.entry("Original observations used or rejected within this output's scope.",
                    suffix=f"{suffix}.records.{index}", records=chunk)
        for index, chunk in enumerate(batched((originals[key] for key in ids), 256), 1)
    )


def _count_values(counts: dict[str, int], prefix: str = "") -> tuple[TraceValue, ...]:
    return tuple(TraceValue(name=prefix + name, value=Decimal(value), unit="count")
                 for name, value in counts.items())


def _exclusion_summary(intervals: tuple[StudyInterval, ...], scopes: set[str]) -> str:
    reasons = Counter(
        (issue.scope, issue.code, issue.reason)
        for interval in intervals for issue in interval.exclusions if issue.scope in scopes
    )
    if not reasons:
        return "No recorded input exclusions."
    detail = "; ".join(f"{scope}.{code} ({reason}) × {count}"
                       for (scope, code, reason), count in sorted(reasons.items()))
    return f"Exclusions by input and reason (an interval may have several). {detail}."


def _group_counts(group: StudyGroup) -> dict[str, int]:
    return {"eligible_count": group.eligible_count, "excluded_count": group.excluded_count}


@dataclass(frozen=True)
class _Score:
    winners: int
    losers: int
    ties: int
    mean_winner: Fraction | None
    absolute_mean_loser: Fraction | None

    @classmethod
    def from_group(cls, group: StudyGroup) -> "_Score":
        relative = tuple(Fraction(item.benchmark_relative_return) for item in group.intervals
                         if item.benchmark_relative_return is not None)
        wins = tuple(value for value in relative if value > 0)
        losses = tuple(-value for value in relative if value < 0)
        return cls(len(wins), len(losses), len(relative) - len(wins) - len(losses),
                   sum(wins, Fraction(0)) / len(wins) if wins else None,
                   sum(losses, Fraction(0)) / len(losses) if losses else None)


def _score_candidate(output: OutputDescriptor, group: StudyGroup, score: _Score) -> CandidateOutput:
    eligible = group.eligible_count
    context = f"({eligible} eligible, {group.excluded_count} excluded)"
    if not eligible:
        return _candidate(output, None, f"No eligible {group.regime}-group outcomes {context}")
    if output.output_id.endswith("_hit_rate"):
        return _candidate(output, Fraction(score.winners, eligible), None)
    if score.mean_winner is not None and score.absolute_mean_loser is not None:
        result = _candidate(output, score.mean_winner / score.absolute_mean_loser, None)
        if result.reason is None:
            return result
        return _candidate(output, None, f"Slugging {context}: {result.reason}")
    missing = "winner" if score.losers else "loser"
    if not (score.winners or score.losers):
        missing = "winner or loser"
    return _candidate(output, None, f"No eligible {group.regime}-group {missing} {context}")


def _mean_evidence(score: _Score, prefix: str) -> tuple[str, tuple[TraceValue, ...]]:
    descriptions, values = [], []
    for name, mean in (("mean_winner", score.mean_winner), ("absolute_mean_loser", score.absolute_mean_loser)):
        label = name.replace("_", " ")
        if mean is None:
            descriptions.append(f"{label} undefined")
            continue
        descriptions.append(f"{label} = {mean} percentage points")
        try:
            decimal_mean = _wire_decimal(mean)
        except ValueError:
            # The exact fraction stays visible even if the mean itself exceeds wire precision or magnitude.
            continue
        values.append(TraceValue(name=prefix + name, value=decimal_mean, unit="percentage_points"))
    return ". ".join(descriptions) + ".", tuple(values)


def _group_evidence(
    trace: _Trace, group: StudyGroup, score: _Score | None, study: StudyGroups,
    originals: dict[str, Observation], *, coverage: str | None = None,
) -> tuple[TraceEntry, ...]:
    prefix = f"{coverage}." if coverage else ""
    suffix = f".coverage.{coverage}" if coverage else ""
    title = f"{coverage.title()} regime coverage" if coverage else trace.output.semantic_definition
    counts = _group_counts(group)
    description = f"{title}. {group.partition} from {study.plan.start} to {study.plan.end}."
    mean_values = ()
    scopes = {"regime"}
    if score is not None:
        counts.update({
            "hit_rate_denominator": group.eligible_count, "winner_count": score.winners,
            "loser_count": score.losers, "tie_count": score.ties,
        })
        means, mean_values = _mean_evidence(score, prefix)
        description += f" Outcomes are strategy minus benchmark return in percentage points. {means}"
        scopes = _SCORE_SCOPES
    detail = _exclusion_summary(group.intervals, _SCORE_SCOPES)
    summary = trace.entry(
        f"{description} {detail}", suffix=suffix,
        values=_count_values(counts, prefix) + mean_values,
    )
    records = _record_evidence(trace, group.intervals, scopes, originals, suffix=suffix)
    return (summary, *records)


def _path_issue(study: StudyGroups, intervals: tuple[StudyInterval, ...]) -> str | None:
    expected_start = study.plan.start
    for interval in intervals:
        if interval.start < expected_start:
            return f"overlapping interval {interval.start}/{interval.end}"
        if interval.start > expected_start or interval.end <= interval.start:
            return f"noncontiguous or invalid interval {interval.start}/{interval.end}"
        if interval.strategy_return is None:
            issues = ", ".join(issue.reason for issue in interval.exclusions if issue.scope in _DRAWDOWN_SCOPES)
            return f"missing strategy return for {interval.start}/{interval.end}" + (f" ({issues})" if issues else "")
        expected_start = interval.end
    if expected_start != study.plan.end:
        return f"path ends on {expected_start}, expected {study.plan.end}"
    return None


def _max_drawdown(intervals: tuple[StudyInterval, ...]) -> Fraction:
    # Wealth divided by its running peak is sufficient to measure the loss.
    wealth_to_peak = lowest = Fraction(1)
    for interval in intervals:
        value = interval.strategy_return
        assert value is not None
        if value == -100:
            return Fraction(100)
        if not value:
            continue
        wealth_to_peak = min(Fraction(1), wealth_to_peak * (1 + Fraction(value) / 100))
        if value < 0 and wealth_to_peak < lowest:
            lowest = wealth_to_peak
    return 100 * (1 - lowest)


def _drawdown_output(
    trace: _Trace, study: StudyGroups, originals: dict[str, Observation],
) -> tuple[CandidateOutput, tuple[TraceEntry, ...]]:
    intervals = tuple(sorted(study.intervals, key=attrgetter("start", "end")))
    issue = _path_issue(study, intervals)
    returns = tuple(TraceValue(
        name=f"strategy_return.{item.end}", value=item.strategy_return, unit="percent",
        period_start=item.start, period_end=item.end,
    ) for item in intervals if item.strategy_return is not None)
    counts = _count_values({
        "interval_count": len(intervals), "intervals_with_return": len(returns),
        "intervals_without_return": len(intervals) - len(returns),
        "cash_intervals": sum(item.position == "cash" for item in intervals),
    })
    candidate = _candidate(
        trace.output, None if issue else _max_drawdown(intervals),
        f"Drawdown path incomplete: {issue}" if issue else None,
    )
    detail = _exclusion_summary(intervals, _DRAWDOWN_SCOPES)
    if candidate.reason is not None:
        detail = f"{candidate.reason}. {detail}"
    summary = trace.entry(
        f"{trace.output.semantic_definition}. {study.plan.partition} from {study.plan.start} to {study.plan.end}. "
        "Starting with wealth and peak of 1, multiply wealth by (1 + strategy return / 100) "
        "in interval order, carrying zero returns for cash. Set peak to max(peak, wealth). "
        f"Drawdown is max(100 × (1 − wealth / peak)). {detail}",
        values=counts + (
            TraceValue(name="initial_wealth", value="1", unit="ratio"),
            TraceValue(name="initial_peak", value="1", unit="ratio"),
        ),
    )
    path_label = ("Available strategy returns for the incomplete path." if issue
                  else "Chronological strategy returns used for the wealth path.")
    path = tuple(trace.entry(path_label, suffix=f".returns.{index}", values=chunk)
                 for index, chunk in enumerate(batched(returns, 256), 1))
    records = _record_evidence(trace, intervals, _DRAWDOWN_SCOPES, originals)
    return candidate, (summary, *path, *records)


class TimingStudyModel(Model):
    def describe(self) -> ModelDescriptor:
        return _DESCRIPTOR

    def calculate(self, inputs: InputSnapshot, assumptions: AssumptionSet) -> CandidateResult:
        try:
            study = build_study_groups(inputs, assumptions)
        except ValueError as exc:
            return CandidateResult(outputs=tuple(
                _candidate(output, None, str(exc)[:4096]) for output in _DESCRIPTOR.outputs
            ))

        groups = {group.regime: group for group in study.groups}
        scores = {regime: _Score.from_group(group) for regime, group in groups.items() if regime is not None}
        originals = {row.record_id: row for table in inputs.tables if table.table_id in _INPUTS for row in table.rows}
        outputs, entries = [], []
        for output in _DESCRIPTOR.outputs:
            trace = _trace_context(output, inputs, assumptions)
            if output.output_id == "study_drawdown":
                candidate, evidence = _drawdown_output(trace, study, originals)
            else:
                regime = output.output_id.split("_", 1)[0]
                candidate = _score_candidate(output, groups[regime], scores[regime])
                evidence = (
                    *_group_evidence(trace, groups[regime], scores[regime], study, originals),
                    *_group_evidence(trace, groups["flat"], scores["flat"], study, originals, coverage="flat"),
                    *_group_evidence(trace, groups[None], None, study, originals, coverage="unknown"),
                )
            outputs.append(candidate)
            entries.extend(evidence)
        return CandidateResult(outputs=tuple(outputs), trace=tuple(entries))
