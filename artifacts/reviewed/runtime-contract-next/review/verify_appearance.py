"""Independent, read-only verification of the frozen appearance audit."""
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
AUDIT = ROOT / "artifacts/appearance-next-audit"


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def flattened(value, path=""):
    result = {}
    if isinstance(value, dict) and value:
        for key, item in value.items():
            result.update(flattened(item, path + "/" + key.replace("~", "~0").replace("/", "~1")))
    elif isinstance(value, list) and value:
        for index, item in enumerate(value):
            result.update(flattened(item, path + "/" + str(index)))
    else:
        result[path] = value
    return result


def main():
    manifest = json.loads((AUDIT / "input-manifest.json").read_text())
    inputs = []
    cases = {}
    for entry in manifest:
        if entry.get("repository"):
            raw = subprocess.check_output(["git", "-C", str(ROOT / entry["repository"]),
                                           "show", entry["revision"] + ":" + entry["path"]])
        else:
            raw = (ROOT / entry["path"]).read_bytes()
        assert sha(raw) == entry["sha256"], entry["path"]
        inputs.append({"path": entry["path"], "sha256": sha(raw)})
        if "case" in entry:
            cases[entry["case"]] = json.loads(raw)
    ledger = json.loads((AUDIT / "leaf-ledger.json").read_text())
    actual = {(entry["case"], entry["pointer"]): entry["value"] for entry in ledger}
    expected = {}
    for case, record in cases.items():
        assert record["model"]["chartOptions"] == {}
        assert len(record["effective"]["series"]) == 2
        for pointer, value in flattened(record["effective"], "/effective").items():
            expected[case, pointer] = value
    assert actual == expected
    assert len(actual) == len(ledger), "duplicate ledger keys"
    differences = {}
    for mode in ("dark", "light"):
        stock = flattened(cases[f"stock-{mode}-grouped"]["effective"])
        custom = flattened(cases[f"custom-{mode}-grouped"]["effective"])
        assert stock.keys() == custom.keys(), "asymmetric projection would need explicit absence handling"
        differences[mode] = {key: {"stock": stock[key], "custom": value}
                             for key, value in custom.items() if stock[key] != value}
    assert differences == json.loads((AUDIT / "custom-differences.json").read_text())
    published = json.loads((AUDIT / "verification.json").read_text())["publishedCandidates"]
    for entry in published:
        assert sha((ROOT / entry["path"]).read_bytes()) == entry["sha256"], entry["path"]
    before = {path.name: sha(path.read_bytes()) for path in AUDIT.iterdir() if path.is_file()}
    module_spec = importlib.util.spec_from_file_location("frozen_audit", AUDIT / "audit.py")
    module = importlib.util.module_from_spec(module_spec)
    # Execute compiled source to avoid writing __pycache__ into the frozen lane.
    exec(compile((AUDIT / "audit.py").read_text(), str(AUDIT / "audit.py"), "exec"), module.__dict__)
    module.OUT = OUT / "appearance-reproduction"
    module.OUT.mkdir(exist_ok=True)
    module.main()
    for name in ("input-manifest.json", "leaf-ledger.json", "custom-differences.json"):
        assert (module.OUT / name).read_bytes() == (AUDIT / name).read_bytes(), name
    assert before == {path.name: sha(path.read_bytes()) for path in AUDIT.iterdir() if path.is_file()}
    result = {"status": "pass", "command": "py artifacts/runtime-contract-next/review/verify_appearance.py",
              "exitCode": 0, "inputHashes": inputs, "cases": len(cases), "ledgerEntries": len(ledger),
              "independentFlattenAndDiff": "pass", "byteExactAuditReproduction": "pass",
              "frozenLaneUnchanged": True,
              "sourcePin": module.PIN, "auditHashes": before,
              "scope": "Research evidence only; no browser, production, candidate parity or full B2 acceptance."}
    (OUT / "appearance-verification.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"status": "pass", "cases": len(cases), "entries": len(ledger), "hashes": len(inputs)}))


if __name__ == "__main__":
    main()
