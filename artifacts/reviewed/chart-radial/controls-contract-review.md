# RC0C independent controls/interface review

- VERDICT: APPROVED
- TASK: bounded inactive controls freeze only, 2026-10-24. This does not complete RC0, accept numerical behavior or activate either Radial family.
- Frozen declarations SHA256: `dc25c1598d9ff8d9d260ca0eb063c17db2e34489d2992b7681b76b53cc0e5743`; fixture SHA256: `b19ae418b989645a65cb716e22125819164b96f4a93a3948177f836db1eb7af1`. Fresh hashes match validation.json.

## Scope and findings

The maintained Bounded controls overlap amendment authorizes separate RC0C acceptance and assigns radialAssignments to RC2. Selection, appearance, editor state/transactions and RadialControls can be implemented inactive without consuming an unfinished renderer. RC1 and shared routing remain blocked on the complete numerical freeze.

Two initial gaps were repaired before approval: the assignment resolver now has explicit input/result/callable exports and unknown-input admission semantics; source-derived color/typography target arrays are explicit. Admission rejects other families, malformed or duplicate IDs including unselected entries, nonboolean selection and getter failures. Selection retains order without truncation; empty selection is valid. Family-to-option mapping and runtime family/axis-pair validation remain required implementation checks, not assumptions inferred from broad unions.

Inspected both original run-3 observation files, 19 records each, and the retained run result. Actual saved paths agree with the fixture: Column padding/orientation on angle-category; Bar padding on radius-category and orientation on angle-number; thickness and inner radius on both family axes. The edited series and family axis options survive reload. Root Group Type is separate, defaults to grouped when absent, and absent versus explicit grouped remains a stale-identity distinction. Runtime-generated chart IDs and later navigator flags are not evidence that family control options changed.

The declarations preserve distinct effective category/numerical defaults and first-axis editor values, avoiding Bar's projected zero-padding versus effective 0.2-padding conflation. Palette fills/strokes are supplied palette values, not Nightingale background-stroke inference. Unexposed Column width ratios, inactive corner-radius bytes and unrelated family options remain preserved. Color and label typography on both family axes are explicitly source-derived; no browser edit claim is made for them. Angular-only orientation is independently observed.

## Mechanical results and remaining gates

Retained strict TypeScript candidate and imported-source baseline both exit 2 with identical four inherited typography/Zod diagnostics; no added interface diagnostics. Syntax exit 0. Declarations measure 247 physical lines, 163 logical units, no executable functions; fixture 153/10, test-only scope. Production declaration caps remain 400/300/50. No browser, build or broad suite was run in this review; RED phase is not applicable to inactive declarations.

Original Bar passes; original Column retains the normalized-missing later-valid suppression failure. That failure is not waived or converted to a pass. Renderer geometry, signed/normalized/missing semantics and any correction decision remain outside this approval. RC2 requires focused admission/default/target/preservation tests, scoped static comparison, full-file complexity plus controller inventory gate, and independent implementation review. Source-level controls acceptance will not establish visible parity.

REMEDIATION: None blocking RC0C. The draft README's older 221/147 count paragraph is historical/stale; validation.json is the reviewed current measurement authority. Controller materialization should identify these exact bytes as RC0C-approved while keeping full RC0 pending.

Summary: the repaired frozen interface supports the authorized inactive RC2 lane independently of the unresolved numerical owner decision.
