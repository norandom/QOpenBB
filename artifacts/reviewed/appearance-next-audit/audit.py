"""Reproduce the finite appearance ledger from explicitly reviewed inputs only."""
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "artifacts/appearance-next-audit"
PIN = "38dffc33389aca0e4a87e0e88d42f7067aa220df"
BASE = "artifacts/reviewed/parity/"
CASES = [
    ("stock-dark-grouped", "theme-matrix/dark-groupedColumn.json"),
    ("stock-dark-stacked", "theme-matrix/first-pass/dark-stackedColumn.json"),
    ("stock-dark-line", "theme-matrix/first-pass/dark-line.json"),
    ("stock-light-grouped", "theme-matrix/light-groupedColumn.json"),
    ("stock-light-stacked", "theme-matrix/light-stackedColumn.json"),
    ("stock-light-line", "theme-matrix/light-line.json"),
    ("custom-dark-grouped", "custom-theme-contract/dark-groupedColumn.json"),
    ("custom-light-grouped", "custom-theme-contract/light-groupedColumn.json"),
]
SOURCES = [
    "terminalpro/src/components/General/Table/Chart/themes.tsx",
    "terminalpro/src/components/General/Table/Chart/hooks/useChartOptions.tsx",
    "terminalpro/src/components/General/Table/Chart/utils.tsx",
    "terminalpro/src/components/ThemeSettings/ChartSettings.tsx",
    "terminalpro/src/lib/state/tableChartThemes.ts",
]


def digest(data):
    return hashlib.sha256(data).hexdigest()


def leaves(value, pointer=""):
    if isinstance(value, dict) and value:
        for key, child in value.items():
            escaped = key.replace("~", "~0").replace("/", "~1")
            yield from leaves(child, pointer + "/" + escaped)
    elif isinstance(value, list) and value:
        for index, child in enumerate(value):
            yield from leaves(child, pointer + "/" + str(index))
    else:
        yield pointer, value


def source_support(pointer):
    if pointer == "/background/fill":
        return "themes.tsx:218-237; custom params replacement 252-262; runtime proves effective fill"
    if pointer.startswith("/legend/") and pointer not in [
        "/legend/enabled", "/legend/item/label/fontFamily", "/legend/item/label/fontWeight"
    ]:
        return "themes.tsx:82-102; generated common legend useChartOptions.tsx:381-397"
    if pointer == "/title/fontSize":
        return "themes.tsx:214"
    if pointer.endswith("/connectMissingData") or pointer.endswith("/marker/enabled"):
        return "themes.tsx:180; no override collision exercised"
    if pointer.endswith("/label/enabled") and pointer.startswith("/series/"):
        return "utils.tsx:101-103; no override collision exercised"
    if pointer.startswith("/series/") and pointer.endswith(("/fill", "/stroke")):
        return "custom palette replacement themes.tsx:255-262; stock inheritance and allocation are runtime observations"
    if pointer.startswith("/axes/") and pointer.endswith("/label/fontSize"):
        return "utils.tsx:278-283,311-323; runtime determines final leaf"
    return "No owned source rule established for final leaf; finite runtime observation only"


def main():
    manifest = []
    ledger = []
    records = {}
    for case, relative in CASES:
        path = BASE + relative
        raw = (ROOT / path).read_bytes()
        record = json.loads(raw)
        assert record["model"]["chartOptions"] == {}
        assert len(record["effective"]["series"]) == 2
        records[case] = record
        manifest.append({"path": path, "sha256": digest(raw), "case": case})
        for pointer, value in leaves(record["effective"]):
            ledger.append({"case": case, "path": path, "pointer": "/effective" + pointer,
                           "value": value, "evidenceKind": "runtime-projection",
                           "ownedSourceSupport": source_support(pointer),
                           "precedence": "No competing saved option leaf in this case"})
    for path in SOURCES:
        raw = subprocess.check_output(["git", "-C", str(ROOT / "vendor/workspace"),
                                       "show", PIN + ":" + path])
        manifest.append({"repository": "vendor/workspace", "revision": PIN,
                         "path": path, "sha256": digest(raw), "kind": "source-only"})
    for name in ["cartesianTypes.ts", "cartesianStyle.ts"]:
        path = "vendor/workspace/terminalpro/src/components/General/Table/Chart/echarts/" + name
        manifest.append({"path": path, "sha256": digest((ROOT / path).read_bytes()),
                         "kind": "current-source-only"})
    differences = {}
    for mode in ["dark", "light"]:
        stock = dict(leaves(records[f"stock-{mode}-grouped"]["effective"]))
        custom = dict(leaves(records[f"custom-{mode}-grouped"]["effective"]))
        differences[mode] = {key: {"stock": stock.get(key), "custom": value}
                             for key, value in custom.items() if stock.get(key) != value}
    for name, data in [("input-manifest.json", manifest), ("leaf-ledger.json", ledger),
                       ("custom-differences.json", differences)]:
        (OUT / name).write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": "pass", "cases": len(records), "leaves": len(ledger),
                      "emptySavedOptions": 8, "sourceRevision": PIN}))


if __name__ == "__main__":
    main()
