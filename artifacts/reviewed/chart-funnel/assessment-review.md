# Funnel F0 independent review

The bounded F0 characterization is approved as evidence for the next contract proposal. The retained financial fixture, original observations and proposed responsibility boundaries are sufficiently identified, with unresolved behavior listed below. An implementation contract and replacement acceptance remain pending.

## Financial reconciliation, 2026-10-26

Independent read-only Python 3 verification passed (exit 0). The verification did not invoke the fixture preparer, application helpers, or network. Both SHA-256 hashes, five ordered reported values, selected record metadata, four accounting identities and the disclosed FY2026 Q3 increase agree with retained source bytes.

Exact command (PowerShell):

```powershell
@'
import csv,hashlib,json
from pathlib import Path
from decimal import Decimal
root=Path.cwd(); p=root/'artifacts/chart-funnel/fmp'; meta=json.loads((p/'provenance.json').read_text()); raw=root/meta['source_raw_path']; data=json.loads(raw.read_text(),parse_int=Decimal,parse_float=Decimal)
assert hashlib.sha256(raw.read_bytes()).hexdigest()==meta['raw_sha256']
assert hashlib.sha256((p/'levels.csv').read_bytes()).hexdigest()==meta['csv_sha256']
r=next(x for x in data if x['symbol']=='AAPL' and x['date']=='2026-03-28')
rows=list(csv.DictReader((p/'levels.csv').open()))
fields=[('Revenue','revenue'),('Gross profit','grossProfit'),('Operating income','operatingIncome'),('Pretax income','incomeBeforeTax'),('Net income','netIncome')]
assert [(x['Stage'],Decimal(x['LevelUSD'])) for x in rows]==[(label,r[field]) for label,field in fields]
assert r['revenue']-r['costOfRevenue']==r['grossProfit']
assert r['grossProfit']-r['operatingExpenses']==r['operatingIncome']
assert r['operatingIncome']+r['totalOtherIncomeExpensesNet']==r['incomeBeforeTax']
assert r['incomeBeforeTax']-r['incomeTaxExpense']==r['netIncome']
assert all(meta['record'][k]==r[k] for k in meta['record'])
q3=next(x for x in data if x['symbol']=='AAPL' and x['fiscalYear']=='2026' and x['period']=='Q3')
assert q3['incomeBeforeTax']-q3['operatingIncome']==Decimal('572000000')
print(json.dumps({'status':'PASS','raw_sha256':meta['raw_sha256'],'csv_sha256':meta['csv_sha256'],'rows':len(rows),'identities':4,'quarter':r['date'],'q3_increase':str(q3['incomeBeforeTax']-q3['operatingIncome'])}))
'@ | py -3 -
```

Output:

```json
{"status": "PASS", "raw_sha256": "390dc8cbfc8302720a203bd9782d5e3b1f7363a4f762bdfcef079dbbe4c72f6b", "csv_sha256": "c6b74bd3da1bca8d74438cf441e5b784c40ca27cc4e70d11da42cb34d7b206e8", "rows": 5, "identities": 4, "quarter": "2026-03-28", "q3_increase": "572000000"}
```

The selected reported USD levels are 111184000000, 54781000000, 35885000000, 35833000000 and 29578000000. Their ordering is explicit and their interpretation is correctly limited to an income-statement comparison. Selecting an honestly disclosed nonincreasing quarter does not alter reported values or establish a general monotonic-data requirement. Retained response reconciliation does not independently authenticate the issuer or provider history.

## Assessment boundary

Reviewed the actual root diff, milestone, source assessment and prepared original probe. No production change is part of this review. The milestone explicitly keeps F0 through F5 unchecked and requires frozen interfaces and ownership before implementation. Production caps 400 physical lines/file, 300 logical units/file and 50/function remain mandatory for later tasks; research and test artifacts are excluded.

Initial probe limitations were reported promptly: controls were inventoried without effects, fixed hover coordinates could omit stages, reload asserted only canvas visibility, and financial versus synthetic data required distinct runs. Parent has requested a bounded follow-up. Final findings will identify which obligations remain unresolved rather than infer replacement behavior from native declarations.

Marker/secret spot search over the milestone, fixture script/provenance and original test returned no matches. The default product.md, tech.md and structure.md steering files are absent; delegation, testing, complexity and documentation were read. No broad application suite is appropriate for this assessment-only boundary.

## Frozen original run 1

`native/run-1/run.log` records three passes in 1.9 minutes with one worker; `exit-code.txt` is 0. The original frontend is `38dffc33389aca0e4a87e0e88d42f7067aa220df`, image `sha256:f48eb1c9b32e1f84d5199dafc943bc1fc10f3b1745ab29860975d002dc5c8a3f`, with the explicitly qualified backend-only overlay. This is not a packaged-only candidate run.

I independently read all three observations. Each contains all five stage/value tooltips and drawing labels in fixture order. Funnel and Cone use compact billion formatting; Pyramid uses full integers. The visible Series groups agree with the source map. Setup exposes Aggregate and Direction; Customize exposes Chart Style, Titles and Series. Absence of Axes, Legend and Navigator from the inspected top-level snapshot is an observation of this caller, not a universal API claim.

The nested headings are enabled-state toggles: Funnel Labels changes unchecked to checked in `Series/Labels`; Stage Labels and Drop-Off change checked to unchecked in their snapshots. The second click restores the initial enabled booleans, but creates explicit chart-option overrides. Final screenshots, saved models and drawing samples are therefore post-toggle restoration, not untouched defaults. Initial Series snapshots establish the prior checkbox states only.

The original has two `Unexpected token '<'` page errors and two CSV `ERR_FAILED` console/request failures per variant. Three passed probe tests do not imply clean diagnostics. These errors remain separate from candidate acceptance and from the known first-login onboarding issue.

## Source geometry cross-check

I independently read the critical retained source ranges in `geometry-source.md` and verified the Enterprise and Community package SHA-256 values against that report. The read-only WSL command exited 0. Pyramid accumulates `yTotal` and allocates axial slice extent as `value / yTotal`; it does not equalize polygon areas. No zero-total guard appears in the inspected geometry. The custom visibility validator replaces the numeric validator through `...opts`, so `invalidValue: 0` does not establish blanket null/missing normalization. These findings are source characterization, not browser outcomes or required replacement policies.

For this financial fixture the stages are overlapping reported accounting levels. Pyramid's internal sum normalization does not make them additive components of revenue. A later contract must preserve the distinction and make any handling of native defects an explicit decision.

## Final bounded effects review

I independently inspected frozen run-4 and run-5 `effects.json`, the frozen run-5 test, run logs, and both run-5 reload PNGs. Run 2 failed on a grid-format witness (`1007` versus `1,007`); run 3 failed by sending a nonfinite observed geometry centroid to pointer dispatch. Run 4 retained the Funnel observations but failed full-model equality because chart identity and selected range changed. These are retained failures, not discarded retries. Run 5 passed one sequential test in 47.9 seconds, exit 0, after limiting its assertion to unchanged `chartOptions` for Cone and Pyramid.

Across the recorded runs, duplicate Repeated rows give separate 90 and 60 tooltips with aggregation off; Sum produces 150, and turning aggregation off restores separate values. Horizontal direction and Stage Labels removal have public drawing/model evidence for all three variants. Funnel numeric-label activation and Drop-Off removal have evidence. Cone/Pyramid numeric labels were already on, so checking them does not prove an off/on transition.

Negative Funnel/Cone values retain the -20 tooltip while yielding magnitude/inverted geometry; Pyramid -20 text crowds the apex without a negative tooltip hit. Blank-associated nonfinite paths remain in Funnel/Cone observations. A no-hit tooltip is inconclusive, and the mixed blank CSV does not isolate JavaScript null typing. Empty and all-zero cases have source findings only.

All variants retain Value as the first range field after adding Reserve; the observed values therefore remain Value. This is consistent with first-field selection and is not sufficient to diagnose a selector bug or establish switching to Reserve alone. That transition remains unresolved.

Important native persistence limitation: Cone and Pyramid reload PNGs visibly contain no numeric labels, although the before-reload drawings contain them and `chartOptions` compares equal. Pyramid tooltip formatting also gains the Value field-name line after reload. This is an observed public rendering difference; equal option keys do not prove rendered defaults survive recreation. Chart IDs regenerate and range columns reduce from Stage/Value/Reserve to Stage/Value. These native limitations must remain explicit in the matrix and later policy discussion.

The integration map is a suitable proposal: shared capture/session/lifecycle remains the owner, geometry and editor responsibilities are disjoint after interfaces freeze, and near-cap shared modules are inventoried. This review approves neither exact module names nor implementation interfaces.

## Decisions carried into contract design

- Define financial admission explicitly. The controller's pending owner proposal retains missing stages as gaps without fabricated zero tooltips or cross-gap connectors; Funnel/Cone encode magnitude while preserving explicitly signed labels/tooltips; Pyramid requires nonnegative values with a positive total. These are defensible explicit rules. The reviewer's earlier stricter rejection suggestion is optional, not a requirement. No monotonic restriction is warranted.
- Preserve numeric labels and tooltip policy through recreation. Decide to correct the observed native reload differences rather than inherit them implicitly.
- Confirm choosing another numeric field alone; retain aggregation and duplicate identity as separate semantics. Do not promote mixed-range observations into a selector contract.
- Common cosmetics, fresh-context reopen, empty/all-zero browser cases and remaining control effects belong to the reviewed implementation/acceptance plan. They are not completed by F0.

## Review Verdict
- VERDICT: APPROVED
- TASK: F0 bounded original characterization and financial fixture review; implementation contract excluded
- MECHANICAL_RESULTS:
  - Tests: PASS (independent read-only Python reconciliation above, exit 0; original run-1 recorded Playwright command, exit 0, 3 passed; original run-5 recorded command, exit 0, 1 passed). Historical runs 2-4 failed for the documented reasons and remain evidence.
  - TBD/TODO grep: CLEAN
  - Secrets grep: CLEAN (targeted assessment/fixture/test spot search; raw browser artifacts are not approved for publication)
  - Static checks: SPOT_CHECKED
  - Boundary: WITHIN
  - Boundary audit: CLEAN
  - RED phase: N/A
- FINDINGS:
  1. FYI: Five retained USD levels, source/CSV hashes, record metadata and accounting identities independently reconcile; no new provider request.
  2. FYI: Source geometry and public synthetic observations establish distinct variants, duplicate/aggregate behavior and problematic native signed/blank cases, with explicitly bounded limits.
  3. Important for later contract: Equal saved options do not preserve numeric-label rendering or Pyramid tooltip formatting on observed reload. The candidate must receive an explicit persistence contract.
  4. Important for later contract: Admission policy and alternate numeric-field selection remain decisions or unresolved behavior, not replacement acceptance.
- REMEDIATION: None for bounded characterization. Preserve the identified limitations in the final matrix; resolve the contract decisions before production implementation.
- SUMMARY: F0 provides reviewable original evidence and a financially reconciled fixture for contract design, without approving implementation or candidate behavior.

## Implementation proposal review

Read `.kiro/specs/analyst-workspace/funnel-contract.md` as a proposal only. Its existing-session boundary, duplicate/aggregation ownership, missing-stage gaps, signed-magnitude policy and Pyramid axial geometry are coherent. Admission approval remains the owner's decision. No production implementation is approved by this review.

Two numerical details need freezing before F1: Funnel/Cone magnitude normalization must use the maximum absolute finite value rather than the native maximum signed value, including all-negative and all-zero inputs. Pyramid must reject a nonfinite accumulated total or use stable normalization, since finite individual inputs do not guarantee a finite sum. Preserve the existing requirement that no nonfinite coordinate reaches ECharts.

The proposal and final behavior matrix should describe numeric-label absence in the inspected reload PNGs as an observed rendering difference, not just an incomplete canvas observer. Candidate persistence requirements already correctly require visible results beyond option equality.
