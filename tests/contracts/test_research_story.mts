import assert from "node:assert/strict";
import { readFileSync } from "node:fs";

type Cutoff = {
  observation_date: string;
  decision_at: string;
  evaluated_at: string;
  session_timezone: "America/New_York";
};

type Schedule = { calendar_id: "NYSE_ARCA"; schedule_revision: string };
type Selection = {
  commodity_symbol: "DBC" | "GLD";
  technology_symbol: "XLK" | "VGT";
  observation_date: string;
};

const charts = {
  returns: {
    input: [["left_close", "right_close"], "date", "price_usd"],
    result: [["left_momentum", "right_momentum"], "proxy", "percent"],
  },
  risk: {
    input: [["left_daily_return", "right_daily_return"], "date", "percent"],
    result: [["left_volatility", "right_volatility"], "proxy", "percent"],
  },
  real_yields: {
    input: [["dfii10"], "date", "percent"],
    result: [["change"], "window", "percentage_points"],
  },
} as const;

type Chart<Spec extends readonly [readonly string[], string, string]> = {
  chart_type: "line" | "bar";
  series: Spec[0][number][];
  x_axis: Spec[1];
  y_axis: Spec[2];
};
type Charts = {
  [View in keyof typeof charts]: {
    [Lane in "input" | "result"]: Chart<(typeof charts)[View][Lane]>;
  };
};

type Role = "comparison" | "regime";
type StoryState = {
  version: 1;
  selection: Selection;
  schedule: Schedule | null;
  cutoff: Cutoff | null;
  run_refs: Record<Role, string | null>;
  charts: Charts;
};
type Storage = { storage: { researchStory: StoryState } };
type Assumption = {
  assumption_id: string;
  value_type: "text";
  value: string;
  origin: "method_default";
  rationale: string;
};
type Request<M, V, D> = {
  model_id: M;
  method_version: V;
  assumptions: { version: "1"; effective_date: string; assumptions: Assumption[] };
  acquisition: { dataset_id: D; parameters: [string, string][]; cutoff: Cutoff };
};
type Run = {
  schema_version: "1";
  run_id: string;
  descriptor: { model_id: string; method_version: string };
  assumptions: { assumptions: Assumption[] };
  inputs: {
    cutoff: Cutoff;
    provenance: {
      origin: string;
      source: string;
      acquisition_id: string | null;
      query: [string, string][];
      retrieved_at: string;
    };
    tables: { table_id: string; rows: {
      record_id: string;
      source_record_id: string;
      observation_date: string;
      published_at: string | null;
      vintage_at: string | null;
      context: { vintage_coverage: string | null };
    }[] }[];
  };
  outputs: {
    output_id: string;
    status: "verified" | "withheld" | "unverified";
    value: string | null;
    reason: string | null;
    unit: string;
    check_ids: string[];
    trace_ids: string[];
  }[];
  verification: { output_id: string; status: "match" | "unavailable" | "mismatch" }[];
  checks: { rule_id: string; status: "pass" | "fail" | "unknown"; explanation: string | null }[];
  trace: {
    trace_id: string;
    output_id: string;
    source_record_ids: string[];
    intermediate_values: { name: string; period_end: string | null }[];
    substitutions: { value: string; period_end: string | null }[];
    transformations: { transformation_id: string; version: string; description: string }[];
  }[];
};
type SafeError = { code: string; retryable: boolean; run_id?: string };
type Retrieval = {
  retrieved_at: string;
  left_retrieved_at?: string;
  right_retrieved_at?: string;
};
type Story = {
  catalog: {
    widget: { widgetId: "research_story"; type: "research_story" };
    view_order: string[];
    default_state: StoryState;
  };
  saved_dashboard: Storage;
  template_export: Storage;
};
type RunCases = {
  requests: {
    comparison: Request<"proxy_comparison", "2", "story.etf_pair">;
    regime: Request<"real_yield_regime", "1", "story.dfii10">;
  };
  price_evidence: {
    source: "fmp";
    dataset_id: "story.etf_pair";
    retrieval: Retrieval;
    display: { basis: string; left: string; right: string };
  };
  cases: Record<string, {
    request: Role;
    verdict?: string;
    spread?: string;
    outputs?: Record<string, string>;
    withheld?: string[];
    retrieval?: Retrieval;
    leg_errors?: Record<string, string>;
  }>;
};

const story: Story = JSON.parse(readFileSync(process.argv[2], "utf8"));
const runCases: RunCases = JSON.parse(readFileSync(process.argv[3], "utf8"));
const fixture = {...story, ...runCases};
const {runs, errors}: { runs: Record<string, Run>; errors: Record<string, SafeError> } =
  JSON.parse(readFileSync(process.argv[4], "utf8"));

const runId = /^[0-9a-f]{32}$/u;
const date = /^\d{4}-\d{2}-\d{2}$/u;
const timestamp = /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{1,6})?Z$/u;
const receiptTimestamp = /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{1,6})?(?:Z|\+00:00)$/u;
const revision = /^[A-Za-z0-9._-]{1,128}$/u;

function encodeChart<Spec extends readonly [readonly string[], string, string]>(
  config: Chart<Spec>, [series, xAxis, yAxis]: Spec,
): Chart<Spec> {
  assert(["line", "bar"].includes(config.chart_type));
  assert(config.series.length > 0 && new Set(config.series).size === config.series.length);
  assert(config.series.every((item) => series.includes(item)));
  assert.equal(config.x_axis, xAxis);
  assert.equal(config.y_axis, yAxis);
  return {
    chart_type: config.chart_type,
    series: [...config.series],
    x_axis: config.x_axis,
    y_axis: config.y_axis,
  };
}

function encode(state: StoryState): Storage {
  const {selection, schedule, cutoff, run_refs, charts: config} = state;
  assert.equal(state.version, 1);
  assert(["DBC", "GLD"].includes(selection.commodity_symbol));
  assert(["XLK", "VGT"].includes(selection.technology_symbol));
  assert.match(selection.observation_date, date);
  for (const reference of Object.values(run_refs)) {
    if (reference === null) continue;
    assert.match(reference, runId);
    assert(schedule && cutoff);
  }
  assert.equal(Boolean(cutoff), Boolean(schedule));
  if (schedule && cutoff) {
    assert.equal(schedule.calendar_id, "NYSE_ARCA");
    assert.match(schedule.schedule_revision, revision);
    assert.equal(cutoff.observation_date, selection.observation_date);
    assert.equal(cutoff.session_timezone, "America/New_York");
    assert.match(cutoff.decision_at, timestamp);
    assert.match(cutoff.evaluated_at, timestamp);
  }
  return {storage: {researchStory: {
    version: 1,
    selection: {
      commodity_symbol: selection.commodity_symbol,
      technology_symbol: selection.technology_symbol,
      observation_date: selection.observation_date,
    },
    schedule: schedule && {
      calendar_id: schedule.calendar_id,
      schedule_revision: schedule.schedule_revision,
    },
    cutoff: cutoff && {
      observation_date: cutoff.observation_date,
      decision_at: cutoff.decision_at,
      evaluated_at: cutoff.evaluated_at,
      session_timezone: cutoff.session_timezone,
    },
    run_refs: {comparison: run_refs.comparison, regime: run_refs.regime},
    charts: {
      returns: {
        input: encodeChart(config.returns.input, charts.returns.input),
        result: encodeChart(config.returns.result, charts.returns.result),
      },
      risk: {
        input: encodeChart(config.risk.input, charts.risk.input),
        result: encodeChart(config.risk.result, charts.risk.result),
      },
      real_yields: {
        input: encodeChart(config.real_yields.input, charts.real_yields.input),
        result: encodeChart(config.real_yields.result, charts.real_yields.result),
      },
    },
  }}};
}

function bind(run: Run, role: Role, state: StoryState, pathId: string): boolean {
  const expected = fixture.requests[role];
  const params = new Map(run.assumptions.assumptions.map(({assumption_id, value}) => [assumption_id, value]));
  if (run.schema_version !== "1" || !runId.test(run.run_id) || run.run_id !== pathId
      || run.descriptor.model_id !== expected.model_id || run.descriptor.method_version !== expected.method_version
      || !state.cutoff || !state.schedule || state.cutoff.observation_date !== state.selection.observation_date
      || !Object.entries(state.cutoff).every(([key, value]) => run.inputs.cutoff[key as keyof Cutoff] === value)
      || !Object.entries(state.schedule).every(([key, value]) => params.get(key) === value)) {
    return false;
  }
  if (role === "comparison" && (
    params.get("left_proxy") !== state.selection.commodity_symbol
    || params.get("right_proxy") !== state.selection.technology_symbol
    || params.get("left_calendar") !== state.schedule.calendar_id
    || params.get("right_calendar") !== state.schedule.calendar_id
    || !priceEvidence(run, params)
  )) return false;
  const outputIds = role === "comparison"
    ? ["left_momentum", "right_momentum", "left_volatility", "right_volatility", "momentum_spread", "volatility_spread"]
    : ["regime", "change"];
  return run.outputs.length === outputIds.length
    && outputIds.every((id) => run.outputs.some(({output_id}) => output_id === id));
}

function normalizedTimestamp(value: string): string {
  const [seconds, fraction = ""] = value.replace(/(?:Z|\+00:00)$/u, "").split(".");
  return seconds + "." + fraction.padEnd(6, "0") + "Z";
}

function priceEvidence(run: Run, params: Map<string, string>) {
  const receipt = run.inputs.provenance;
  const query = new Map(receipt.query);
  if (receipt.origin !== "service_acquired" || receipt.source !== "fmp" || !receipt.acquisition_id
      || query.size !== receipt.query.length || query.get("dataset_id") !== "story.etf_pair"
      || !timestamp.test(receipt.retrieved_at)
      || !["left_proxy", "right_proxy", "calendar_id", "schedule_revision"]
        .every((key) => query.get(key) === params.get(key))) return undefined;

  const legLabel = (side: "left" | "right") => {
    const legReceipt = query.get(side + "_retrieved_at");
    const failure = query.get(side + "_error");
    if (failure !== undefined) {
      const table = run.inputs.tables.find(({table_id}) => table_id === side + "_closes");
      if (legReceipt !== undefined || table?.rows.length !== 0
          || !["missing_data", "upstream", "entitlement", "invalid_response"].includes(failure)) {
        return undefined;
      }
      return {stamp: null, label: null};
    }
    if (!legReceipt || !receiptTimestamp.test(legReceipt)) return undefined;
    return {stamp: normalizedTimestamp(legReceipt), label:
      params.get(side + "_proxy") + " history retrieved " + legReceipt.slice(0, 10)};
  };
  const left = legLabel("left");
  const right = legLabel("right");
  if (!left || !right || [left.stamp, right.stamp].filter((stamp) => stamp !== null).sort().at(-1)
      !== normalizedTimestamp(receipt.retrieved_at)) return undefined;

  return {basis: "FMP history retrieved " + receipt.retrieved_at.slice(0, 10),
    left: left.label, right: right.label};
}

function exactSign(value: string): number | null {
  const match = /^([+-]?)(\d+(?:\.\d+)?)(?:e[+-]?\d+)?$/iu.exec(value);
  if (!match) return null;
  if (!/[1-9]/u.test(match[2])) return 0;
  return match[1] === "-" ? -1 : 1;
}

function verdict(run: Run, state: StoryState, pathId = run.run_id) {
  if (!bind(run, "comparison", state, pathId)) return "insufficient_data";
  const output = run.outputs.find(({output_id}) => output_id === "momentum_spread");
  if (!output || output.status !== "verified" || output.unit !== "percentage_points"
      || !output.check_ids.length || !output.trace_ids.length || output.value === null
      || !output.check_ids.every((id) => run.checks.some(({rule_id, status}) => rule_id === id && status === "pass"))
      || !output.trace_ids.every((id) => run.trace.some(({trace_id, output_id}) =>
        trace_id === id && output_id === output.output_id))
      || !run.verification.some(({output_id, status}) => output_id === output.output_id && status === "match")) {
    return "insufficient_data";
  }
  const sign = exactSign(output.value);
  if (sign === null) return "insufficient_data";
  return sign === 0 ? "tie" : sign > 0 ? "supported" : "technology_outperformance";
}

const saved = fixture.saved_dashboard.storage.researchStory;
assert.deepEqual(encode(saved), fixture.saved_dashboard);
assert.deepEqual(encode(saved), fixture.template_export);
assert.equal(fixture.catalog.widget.widgetId, "research_story");
assert.equal(fixture.catalog.widget.type, "research_story");
assert(!Object.hasOwn(fixture.catalog.widget, "endpoint"));
assert.deepEqual(fixture.catalog.view_order, ["question", "returns", "risk", "real_yields", "conclusion"]);
assert.deepEqual(encode(fixture.catalog.default_state).storage.researchStory, fixture.catalog.default_state);
assert.deepEqual(fixture.catalog.default_state.charts, saved.charts);
assert.deepEqual(fixture.catalog.default_state.run_refs, {comparison: null, regime: null});
for (const [role, request] of Object.entries(fixture.requests)) {
  assert.equal(request.method_version, role === "comparison" ? "2" : "1");
  const expected = role === "comparison"
    ? ["proxy_comparison", "story.etf_pair", ["left_proxy", "right_proxy", "calendar_id", "schedule_revision"]]
    : ["real_yield_regime", "story.dfii10", ["calendar_id", "schedule_revision"]];
  assert.deepEqual([request.model_id, request.acquisition.dataset_id, request.acquisition.parameters.map(([key]) => key)], expected);
  assert.deepEqual(request.acquisition.cutoff, saved.cutoff);
  for (const [key, value] of request.acquisition.parameters) {
    assert.equal(request.assumptions.assumptions.find(({assumption_id}) => assumption_id === key)?.value, value);
  }
}

assert.deepEqual(Object.keys(runs), Object.keys(fixture.cases).filter((name) => name !== "macro_service_unavailable"));
for (const [name, run] of Object.entries(runs)) {
  const scenario = fixture.cases[name];
  const accepted = name !== "mismatched_pair" && name !== "mismatched_cutoff";
  assert.equal(bind(run, scenario.request, saved, run.run_id), accepted, name);
  assert.equal(errors[name + "_cross_owner"].code, "not_found");
  assert.deepEqual(run.outputs.filter(({status}) => status === "withheld").map(({output_id}) => output_id).sort(),
    [...(scenario.withheld ?? [])].sort());
  const outputs = new Map(run.outputs.map((output) => [output.output_id, output]));
  for (const [id, value] of Object.entries(scenario.outputs ?? {})) {
    assert.equal(outputs.get(id)?.value, value);
  }
  if (scenario.verdict) assert.equal(verdict(run, saved), scenario.verdict, name);
  if (scenario.spread) assert.equal(outputs.get("momentum_spread")?.value, scenario.spread);
  if (scenario.request === "comparison") {
    const {retrieved_at, ...legReceipts} = scenario.retrieval ?? fixture.price_evidence.retrieval;
    const provenance = run.inputs.provenance;
    const query = new Map(provenance.query);
    assert.equal(provenance.retrieved_at, retrieved_at);
    assert.equal(provenance.source, fixture.price_evidence.source);
    assert.equal(query.get("dataset_id"), fixture.price_evidence.dataset_id);
    for (const [key, value] of Object.entries(legReceipts)) assert.equal(query.get(key), value);
    for (const [key, value] of Object.entries(scenario.leg_errors ?? {})) {
      assert.equal(query.get(key), value);
      const side = key.replace(/_error$/u, "");
      assert(!query.has(side + "_retrieved_at"));
      assert.equal(run.inputs.tables.find(({table_id}) => table_id === side + "_closes")?.rows.length, 0);
    }
    for (const table of run.inputs.tables.filter(({table_id}) => table_id.endsWith("_closes"))) {
      assert(table.rows.every((row) => row.published_at === null && row.vintage_at === null
        && row.context.vintage_coverage === "unknown"));
    }
  }
  const records = new Map(run.inputs.tables.flatMap(({table_id, rows}) =>
    rows.map((row) => [row.record_id, {table_id, ...row}] as const)));
  for (const output of run.outputs) {
    if (output.status === "withheld") {
      assert(output.reason);
      assert.equal(output.value, null);
      continue;
    }
    assert.equal(output.status, "verified", name);
    assert(output.trace_ids.length > 0);
    for (const id of output.trace_ids) {
      const trace = run.trace.find(({trace_id}) => trace_id === id);
      assert(trace && trace.output_id === output.output_id);
      const citedTables = trace.source_record_ids.map((id) => records.get(id)?.table_id);
      for (const id of trace.source_record_ids) {
        const row = records.get(id);
        assert(row && row.record_id !== row.source_record_id);
      }
      for (const [leg, table] of [["left", "left_closes"], ["right", "right_closes"]]) {
        if (!output.output_id.startsWith(leg + "_")) continue;
        assert.equal(citedTables.filter((id) => id === table).length, 64);
        if (output.output_id.endsWith("_volatility")) {
          const returns: Run["trace"][number]["intermediate_values"] = trace.intermediate_values.filter(({name}) => name.startsWith("simple_return."));
          assert.equal(returns.length, 63);
          assert(returns.every(({name, period_end}) => name === "simple_return." + period_end));
        }
      }
      if (scenario.request === "comparison") {
        const expectedLegs = output.output_id.endsWith("_spread")
          ? ["left", "right"]
          : [output.output_id.split("_")[0]];
        assert.deepEqual(trace.transformations.map(({transformation_id}) => transformation_id),
          expectedLegs.map((side) => side + ".retrieved_history"));
        const query = new Map(run.inputs.provenance.query);
        for (const [index, receipt] of trace.transformations.entries()) {
          const stamp = query.get(expectedLegs[index] + "_retrieved_at");
          assert(stamp);
          assert.equal(receipt.version, "2");
          assert(receipt.description.includes(stamp.replace(/Z$/u, "+00:00")));
        }
      }
      if (output.output_id === "regime" || output.output_id === "change") {
        assert.equal(citedTables.filter((id) => id === "dfii10").length, 2);
        assert.deepEqual(trace.substitutions.map(({period_end, value}) => [period_end, value]),
          [["2024-01-02", "1.5"], ["2024-04-03", "1.75"]]);
      }
    }
  }
}

assert.equal(exactSign("-1e-400"), -1);
assert.equal(exactSign("-0.0e+9"), 0);
assert.equal(exactSign("NaN"), null);
assert(!Object.hasOwn(runs, "macro_service_unavailable"));
assert.equal(errors.macro_service_unavailable.code, "acquisition_unavailable");
assert(runs.partial_leg.checks.some(({explanation}) => explanation?.includes("XLK")));
assert(runs.failed_leg.checks.some(({explanation}) =>
  explanation?.includes("XLK") && explanation.includes("entitlement")));
assert(runs.unavailable_macro.checks.every(({explanation}) => explanation?.includes("DFII10 endpoint on 2024-04-03")));
assert(errors.recovery.run_id && bind(runs.recovery, "comparison", saved, errors.recovery.run_id));
assert(!bind(runs.recovery, "comparison", saved, runs.comparison.run_id));

const oldMethod = structuredClone(runs.comparison);
oldMethod.descriptor.method_version = "1";
assert(!bind(oldMethod, "comparison", saved, oldMethod.run_id));
assert.equal(verdict(oldMethod, saved), "insufficient_data");

const mislabeled = structuredClone(runs.comparison);
mislabeled.inputs.provenance.retrieved_at = mislabeled.inputs.cutoff.evaluated_at;
assert(!bind(mislabeled, "comparison", saved, mislabeled.run_id));
const unverifiable = structuredClone(runs.comparison);
const reference = unverifiable.verification.find(({output_id}) => output_id === "momentum_spread");
assert(reference);
reference.status = "mismatch";
assert.equal(verdict(unverifiable, saved), "insufficient_data");

const liveState = structuredClone(saved);
liveState.run_refs = {comparison: runs.recovery.run_id, regime: runs.regime.run_id};
const expectedExport = encode(liveState);
const restored: Storage = JSON.parse(JSON.stringify(expectedExport));
assert.deepEqual(restored, expectedExport);
const byId = new Map(Object.values(runs).map((run) => [run.run_id, run]));
function reopen(state: StoryState, role: Role, read: (id: string) => Run | undefined) {
  const id = state.run_refs[role];
  const run = id && read(id);
  return run && id && bind(run, role, state, id) ? run : undefined;
}
const getRun = (id: string) => byId.get(id);
assert.equal(reopen(restored.storage.researchStory, "comparison", getRun), runs.recovery);
assert.equal(reopen(restored.storage.researchStory, "regime", getRun), runs.regime);
assert.equal(reopen(restored.storage.researchStory, "regime", () => undefined), undefined);
const mismatched = {...liveState, run_refs: {
  comparison: runs.mismatched_pair.run_id,
  regime: runs.mismatched_cutoff.run_id,
}};
assert.equal(reopen(mismatched, "comparison", getRun), undefined);
assert.equal(reopen(mismatched, "regime", getRun), undefined);

const withStrictMacroGap = {...liveState, run_refs: {
  comparison: runs.comparison.run_id,
  regime: runs.unavailable_macro.run_id,
}};
const reopenedMacro = reopen(withStrictMacroGap, "regime", getRun);
const reopenedPrices = reopen(withStrictMacroGap, "comparison", getRun);
assert(reopenedMacro?.outputs.every(({status}) => status === "withheld"));
assert(reopenedPrices);
assert.equal(verdict(reopenedPrices, withStrictMacroGap), "supported");
const comparisonAssumptions = (run: Run) => new Map(run.assumptions.assumptions
  .map(({assumption_id, value}) => [assumption_id, value]));
assert.deepEqual(priceEvidence(reopenedPrices, comparisonAssumptions(reopenedPrices)),
  fixture.price_evidence.display);
assert.equal(priceEvidence(runs.recovery, comparisonAssumptions(runs.recovery))?.basis,
  "FMP history retrieved 2024-05-08");
assert.deepEqual(priceEvidence(runs.failed_leg, comparisonAssumptions(runs.failed_leg)), {
  basis: "FMP history retrieved 2024-05-04",
  left: "DBC history retrieved 2024-05-04",
  right: null,
});

const dirty = {
  ...liveState,
  bearer_token: "synthetic-secret",
  generated_narrative: "synthetic response text",
  inputs: runs.recovery.inputs,
  cached_response: runs.recovery,
  retrieval: runs.recovery.inputs.provenance,
  charts: {
    ...liveState.charts,
    returns: {
      ...liveState.charts.returns,
      input: {...liveState.charts.returns.input, rows: runs.recovery.inputs.tables},
    },
  },
};
assert.deepEqual(encode(dirty), expectedExport);
for (const field of ["chart_type", "series", "x_axis", "y_axis"] as const) {
  const invalid = structuredClone(liveState);
  Object.assign(invalid.charts.returns.input, {[field]: field === "series" ? ["synthetic-secret"] : "synthetic-secret"});
  assert.throws(() => encode(invalid), {name: "AssertionError"});
}
