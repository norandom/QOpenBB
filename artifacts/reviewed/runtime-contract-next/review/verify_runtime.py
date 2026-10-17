"""Verify frozen public runtime projections without opening private runtime files."""
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
checks = []


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def check(name, condition):
    assert condition, name
    checks.append(name)


def flatten(obj, prefix=""):
    result = {}
    if isinstance(obj, (dict, list)):
        for key, value in (obj.items() if isinstance(obj, dict) else enumerate(obj)):
            result.update(flatten(value, f"{prefix}.{key}" if prefix else str(key)))
    else:
        result[prefix] = obj
    return result


def main():
    manifests = {}
    marker_hits = []
    for lane in ("editor-runtime-next", "grid-runtime-next"):
        base = ROOT / "artifacts/parity" / lane
        manifest = read(base / "publication-allowlist.json")
        names = [entry["path"] for entry in manifest["files"]]
        check(lane + " unique finite paths", len(names) == len(set(names)))
        hashes = []
        for entry in manifest["files"]:
            path = (base / entry["path"]).resolve()
            check(lane + "/" + entry["path"] + " within lane", path.is_relative_to(base.resolve()))
            raw = path.read_bytes()
            check(lane + "/" + entry["path"] + " hash", hashlib.sha256(raw).hexdigest() == entry["sha256"])
            check(lane + "/" + entry["path"] + " bytes", len(raw) == entry["bytes"])
            hashes.append({"path": entry["path"], "sha256": entry["sha256"]})
            if path.suffix != ".png":
                text = raw.decode("utf-8")
                for pattern in (r"-----BEGIN [^-]*PRIVATE KEY-----", r"Bearer\s+[A-Za-z0-9_.-]{12,}", r"sk-[A-Za-z0-9_-]{20,}", r"gh[pousr]_[A-Za-z0-9]{20,}", r"\b(?:TODO|TBD|FIXME|HACK|XXX)\b"):
                    if re.search(pattern, text):
                        marker_hits.append({"path": str(path.relative_to(ROOT)), "pattern": pattern})
        check(lane + " private files omitted", not any(n in names for n in ("runtime.json", "credential-private.json", "diagnostics.json", "focused/diagnostics.json", "focused/widget-writes.json")))
        check(lane + " cleanup", all(read(base / "cleanup-report.json").values()))
        manifests[lane] = hashes
    check("publication marker scan", not marker_hits)
    grid = ROOT / "artifacts/parity/grid-runtime-next"
    baseline = read(grid / "ordinary.json")
    bounded = read(grid / "filtered-sorted-bounds.json")
    check("ordinary numeric arrays", [[x["revenue"], x["operatingIncome"]] for x in baseline["chart"]["effective"]["data"]] == [[100,20],[0,0],[-5.5,-2],[75.25,None],[140,30],[160,40]])
    check("bounded node identity", [x["id"] for x in bounded["table"]["rows"]] == ["5","4","0","3","1"])
    check("bounded numeric arrays", [[x["operatingIncome"],x["revenue"]] for x in bounded["chart"]["effective"]["data"]] == [[30,140],[20,100],[None,75.25]])
    check("bounded series order", [s["yKey"] for s in bounded["chart"]["effective"]["series"]] == ["operatingIncome","revenue"])
    getter = read(grid / "synthetic-value-getter.json")
    check("getter raw independent", getter["table"]["rows"][0]["raw"]["revenue"] == 100 and getter["table"]["rows"][0]["grid"]["revenue"] == 200)
    check("getter arrays", [x["revenue"] for x in getter["chart"]["effective"]["data"]] == [200,0,-11,150.5,280,320])
    margin = read(grid / "formatted-margin.json")
    check("formatted fraction preserved", margin["chart"]["effective"]["data"][0]["margin"] == 0.2)
    check("grid recorded fifteen checks", len(read(grid / "assertions.json")["results"]) == 15 and all(x["passed"] for x in read(grid / "assertions.json")["results"]))
    editor = ROOT / "artifacts/parity/editor-runtime-next"
    ledger = read(editor / "focused/event-ledger.json")
    patch = read(editor / "patch-ledger.json")
    check("editor actions", len(ledger) == 18 and len(patch) == 18 and not read(editor / "focused/summary.json")["failures"])
    for event, derived in zip(ledger, patch):
        check(event["label"] + " events", event["after"]["events"][len(event["before"]["events"]):] == derived["newEvents"])
        for kind in ("model", "effective"):
            before, after = flatten(event["before"][kind]), flatten(event["after"][kind])
            expected = {key for key in before.keys() | after.keys() if before.get(key) != after.get(key) or (key in before) != (key in after)}
            actual = {row["path"] for row in derived[kind + "Delta"]}
            check(event["label"] + " " + kind + " exact delta keys", expected == actual)
            for row in derived[kind + "Delta"]:
                key = row["path"]
                check(event["label"] + " delta value " + key, row.get("before") == before.get(key) and row.get("after") == after.get(key) and row["beforePresent"] == (key in before) and row["afterPresent"] == (key in after))
    by = {event["label"]: event for event in ledger}
    agg = by["setup/Aggregate/on"]["after"]
    check("aggregate independent arithmetic", [[r["revenue"],r["operatingIncome"]] for r in agg["effective"]["data"]] == [[100+120,20+25],[140,30],[160,40]])
    check("legend emits two events", len(next(p for p in patch if p["label"] == "legend-weight-bold")["newEvents"]) == 2)
    check("tooltip no projected delta", not next(p for p in patch if p["label"] == "series-tooltip-single")["modelDelta"])
    check("diamond shape", [s["marker"]["shape"] for s in by["line-marker-size-9"]["after"]["effective"]["series"]] == ["diamond", "diamond"])
    check("diamond size", [s["marker"]["size"] for s in by["line-marker-size-9"]["after"]["effective"]["series"]] == [9,9])
    check("editor twenty-two recorded checks", len(read(editor / "verification.json")["checks"]) == 22 and all(x["passed"] for x in read(editor / "verification.json")["checks"]))
    result = {"status":"pass", "command":"py artifacts/runtime-contract-next/review/verify_runtime.py", "exitCode":0,
              "checks":checks, "publicationHashes":manifests, "markerHits":marker_hits,
              "privateRuntimeFilesRead":False, "scope":"Frozen finite evidence, not a fresh browser execution or candidate acceptance."}
    (OUT / "runtime-verification.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"status":"pass","checks":len(checks),"publicationFiles":sum(map(len,manifests.values()))}))


if __name__ == "__main__":
    main()
