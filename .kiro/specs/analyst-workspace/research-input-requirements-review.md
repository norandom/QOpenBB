# IA-A requirements review

APPROVED for the requirements review gate after one bounded repair pass. This is reviewer acceptance of the proposal, not owner approval or implementation authorization.

Reviewed on 2026-11-06: all 75 lines of `artifacts/research-input-readiness/requirements-draft.md`, SHA256 `50B4FF53AEF6F9B5328AC10F41F6723E7B5B1E0F7CAE7CD78F9054DE4CBA568E`. Intended destination: `.kiro/specs/analyst-workspace/research-input-requirements.md`; the introduction's relative link is correct for that destination.

## Resolved repair

The original draft never named FMP or FRED. The controller restored the binding source scope without adding implementation detail:

- Boundary context now specifies FMP company/provider-valuation inputs and FRED Treasury context, with no Yahoo, EconDB or custom-source expansion.
- Criteria 4.1 and 4.3 now explicitly name FMP DCF/custom-DCF feasibility and FRED Treasury context. Criterion 5.3 retains the prohibition on silent provider substitution.

Basis: `financial-modeling/brief.md` requires broad FMP acquisition first, while `analyst-workspace/investment-analysis-contract.md` IA-A explicitly includes FMP DCF/custom-DCF feasibility and FRED macro inputs. Provider identity is financially observable and affects entitlement evidence; it is not an invented technology choice.

## Findings retained

- Six numeric requirement headings and 24 uniquely numbered criteria, four per requirement. Each criterion has an event, unwanted-behavior or ubiquitous EARS structure with a concrete subject and mandatory response. No missing requirement criteria or technology-stack prescriptions found.
- The deliverable is one reviewable readiness assessment, not a dashboard or engine. The matrix and next bounded contract are useful outputs; no extra framework, repository, broad test suite or repeated milestone acceptance is requested. Existing workstream ownership and the prohibition on provider/widget house formulas preserve approved boundaries rather than introduce a new architecture.
- Candidate peers remain distinct from curated comparables. Fiscal periods, YTD versus discrete quarters, duration/instant basis, restatements, currency, market dates, share bases, EV claims and invalid denominators have explicit assessment behavior. Cash-conversion ambiguities become modeling prerequisites rather than invented formulas.
- DCF source integration, documentation, account access and observed output are separate claims. A benchmark Treasury series cannot stand in for a curve or company cost of capital. Unknown DCF or macro conventions have separate IA-C and IA-B consequences, avoiding a blanket DCF prerequisite for the first dashboard.
- Historical acceptance remains tied to its recorded query and date. The accepted live file demonstrates MSFT statement/market queries, AAPL/GOOGL profiles and DGS10 observations, not verified peer financial histories or current installer entitlement. The draft does not inflate these observations into IA-A completion.
- Criteria 6.2-6.4 preserve the existing IA-B prerequisites and distinguish a raw/provider-data dashboard from house analysis. A future raw-data presentation must not be described as completing IA-B's cash-conversion, inspectable-multiple and saved-context obligations.
- Future production work remains subject to the 400 physical lines/file, 300 logical units/file and 50/function caps and existing checker/inventory duties. This review changes no production code.

## Mechanical evidence

Executed in PowerShell against the reviewed draft:

```powershell
Get-FileHash artifacts/research-input-readiness/requirements-draft.md -Algorithm SHA256
$draft = Get-Content artifacts/research-input-readiness/requirements-draft.md
$heads = @($draft | Select-String '^### Requirement \d+:')
$criteria = @($draft | Select-String '^\d+\.\d+ ')
Write-Output ('Numeric headings: ' + $heads.Count)
Write-Output ('Numbered criteria: ' + $criteria.Count)
$draft | Select-String '^\d+\.\d+ (?!When |If |While |Where |The )'
```

Results on the final repaired bytes: six numeric headings; 24 numbered criteria; no non-EARS-prefix matches. Criteria sequence and content were reviewed directly. The final SHA256 above was captured after rereading the entire repaired draft. The original draft hash was `B3639C251C60FB0505F1D3E752C5CF7E63C30710E595956F4FBE904CDCA36A46`; an intermediate link-only correction had hash `A28136C56246D5CE6ABFCE39A613CD72E77DE7941110D68B5008E9C9CA1D3D98`.

## Evidence and limits

Reviewed the requirements skill, EARS/review-gate rules, investment-analysis contract, financial-modeling requirements/brief, market-data requirements, initial financial-input publication acceptance, live-input acceptance and all 339 lines of `docs/reference/live-financial-acceptance.json`. Read the relevant documentation, delivery and delegation steering. The configured `product.md`, `tech.md` and `structure.md` steering files are absent; repository inventory confirms that absence. Analyst-workspace language is `en`.

This is independent requirements review only. No network queries, runtime checks, builds or tests were performed. Historical test counts are source evidence, not newly executed checks. Approval of a repaired requirements document does not approve design/tasks or establish input readiness, consumer behavior, current account access or implementation completion.
