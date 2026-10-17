from pathlib import Path
import hashlib
import json
root=Path(__file__).parent
names=["report.md","source-analysis.md","fixture.json","start.mjs","cleanup.mjs","journey.mjs","run.sh","verify.mjs","verify_pixels.py","publication.py","start-status.json","journey-status.json","cleanup-status.json","cleanup-report.json","summary.json","verification.json","verification-status.json","verification.log","pixel-verification.json","pixel-verification-status.json","event-ledger.json","diagnostic-summary.json","outgoing-storage-projection.json","initial-projection-assertion.json","attempt1/journey.log","attempt1/journey-status.json","attempt1/cleanup-status.json","attempt1/cleanup-report.json"]
for stem in ["initial-chart","tooltip-Single","tooltip-Multiple","tooltip-Compact","setup-default","setup-Aggregate-on","setup-Aggregate-off","setup-Switch-Category-Series-on","setup-Switch-Category-Series-off"]:
    names.extend([stem+".json",stem+".png"])
for mode in ["Single","Multiple","Compact"]:
    names.extend(["tooltip-"+mode+"-hover.json","tooltip-"+mode+"-hover.png","tooltip-"+mode+"-geometry.json"])
names.extend(["setup-Aggregate-on-geometry.json","setup-Switch-Category-Series-on-geometry.json"])
entries=[]
for name in sorted(names):
    data=(root/name).read_bytes()
    entries.append({"path":name,"sha256":hashlib.sha256(data).hexdigest(),"bytes":len(data),"sanitization":"finite derivative" if name in ["diagnostic-summary.json","outgoing-storage-projection.json"] else "none; synthetic fixture/code/status"})
result={"status":"frozen pending independent review","originalSource":"38dffc33389aca0e4a87e0e88d42f7067aa220df","originalImage":"sha256:f48eb1c9b32e1f84d5199dafc943bc1fc10f3b1745ab29860975d002dc5c8a3f","candidateReference":"76edf85a46298f7bc5212ff9944e4b66e9baa4af","entries":entries,"omitted":["credential-private.json (removed)","state-* (removed)","runtime.json","diagnostics.json","widget-writes.json","failure-ui.txt","raw attempt1 screenshots/projections/diagnostics/runtime"],"derivativeSources":{name:{"sourcePath":source,"sourceSha256":hashlib.sha256((root/source).read_bytes()).hexdigest()} for name,source in [("diagnostic-summary.json","diagnostics.json"),("outgoing-storage-projection.json","widget-writes.json")]}}
(root/"publication-allowlist.json").write_text(json.dumps(result,indent=2))
print(f"PASS {len(entries)} allowlisted file hashes; raw runtime/credentials/requests excluded")
