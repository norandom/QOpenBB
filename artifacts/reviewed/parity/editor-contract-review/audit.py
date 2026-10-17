from pathlib import Path
import hashlib
import json

root = Path(__file__).parent
source = root.parent / "editor-contract-close"
read = lambda name: json.loads((source / name).read_text())
sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
manifest = read("publication-allowlist.json")
checks = []
for entry in manifest["entries"]:
    path = source / entry["path"]
    assert path.resolve().is_relative_to(source.resolve())
    assert sha(path) == entry["sha256"]
    assert path.stat().st_size == entry["bytes"]
checks.append("57 allowlisted hashes/sizes still match after scratch verification")
ledger = read("event-ledger.json")
assert [x["label"] for x in ledger] == [
    "tooltip-Single", "tooltip-Multiple", "tooltip-Compact",
    "setup/Aggregate/on", "setup/Aggregate/off",
    "setup/Switch Category / Series/on", "setup/Switch Category / Series/off",
]
for label, value in [("Single", "single"), ("Multiple", "shared"), ("Compact", "compact")]:
    action = next(x for x in ledger if x["label"] == "tooltip-" + label)
    new_events = action["after"]["events"][len(action["before"]["events"]):]
    assert any(e["type"] == "chartOptionsChanged" and
               e["chartOptions"]["bar"]["tooltip"]["mode"] == value for e in new_events)
    capture = read("tooltip-" + label + ".json")
    assert any(c["label"] == "Tooltip Mode" and c["value"] == label for c in capture["controls"])
    assert capture["state"]["model"]["chartOptions"]["bar"]["tooltip"]["mode"] == value
    assert capture["state"]["effective"]["tooltip"]["mode"] == value
checks.append("UI labels, new event payloads, model patches and effective tooltip modes agree")
initial = read("initial-chart.json")["state"]["effective"]
rows = initial["data"]
assert len(rows) == 4
assert all(type(r[k]) in (int, float) for r in rows for k in ("revenue", "operatingIncome"))
transposed = read("setup-Switch-Category-Series-on.json")["state"]["effective"]
for j, key in enumerate(["revenue", "operatingIncome"]):
    assert [transposed["data"][j][f"period:{i}"] for i in range(4)] == [r[key] for r in rows]
    assert transposed["data"][j]["AG-GRID-DEFAULT-CATEGORY"] == {
        "id": j, "value": initial["series"][j]["yName"]}
assert [s["yName"] for s in transposed["series"]] == [r["period"]["value"] for r in rows]
assert [s["yKey"] for s in transposed["series"]] == [f"period:{i}" for i in range(4)]
for name in ["setup-Aggregate-off.json", "setup-Switch-Category-Series-off.json"]:
    restored = read(name)["state"]["effective"]
    assert restored["data"] == rows
    assert [(s["xKey"], s["yKey"], s["yName"]) for s in restored["series"]] == [
        (s["xKey"], s["yKey"], s["yName"]) for s in initial["series"]]
checks.append("Transpose and both restoration paths preserve every value, category identity/order and unit-bearing series name")
grouped = {}
for row in rows:
    group = grouped.setdefault(row["period"]["value"], [0, 0])
    group[0] += row["revenue"]
    group[1] += row["operatingIncome"]
sum_rows = read("setup-Aggregate-on.json")["state"]["effective"]["data"]
assert [(r["period"]["value"], r["revenue"], r["operatingIncome"]) for r in sum_rows] == [
    (period, *values) for period, values in grouped.items()]
checks.append("Sum data agrees with independent grouping of original observation rows")
assert read("summary.json") == {"actions": 7, "failures": []}
assert read("journey-status.json")["exitCode"] == 0
assert read("attempt1/journey-status.json")["exitCode"] == 1
for name in ["cleanup-report.json", "attempt1/cleanup-report.json"]:
    assert read(name) == {"containerAbsent": True, "stateAbsent": True, "credentialAbsent": True}
assert not (source / "credential-private.json").exists()
assert not list(source.glob("state-*"))
checks.append("Failure retained; corrective run succeeds; both cleanup reports pass and local credential/state absent")
for derivative in manifest["derivativeSources"].values():
    assert sha(source / derivative["sourcePath"]) == derivative["sourceSha256"]
for name in ["verification.json", "pixel-verification.json"]:
    assert json.loads((root / "scratch" / name).read_text()) == read(name)
checks.append("Derivative source hashes match; fresh scratch numerical/pixel results equal frozen results")
result = {"passed": True, "checks": checks,
          "missingValueSemantics": "UNVERIFIED: all eight financial observations are finite and present; no null, undefined, absent, non-finite, zero or negative case was exercised",
          "manifestSha256": sha(source / "publication-allowlist.json"),
          "specSha256": sha(root.parents[2] / ".kiro/specs/openbb-self-service/chart-editor-contract-close.md")}
(root / "audit-results.json").write_text(json.dumps(result, indent=2))
print(json.dumps(result, indent=2))
