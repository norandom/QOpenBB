# Documentation and code-comment policy

Apply the COBESY composition approach to QOpenBB documentation and code comments. The audience is financial engineers evaluating, operating, and extending a private data workspace. The aim is an observable action or a reviewable decision, supported by evidence.

## Reader and framing

- Lead with the conclusion or next action, then give its rationale and evidence. Group detail by the reader's problem; move reference detail behind links.
- Respect domain experience. Explain project-specific data, authentication, persistence, and delivery contracts rather than teaching generic finance or programming.
- Treat proposals as testable hypotheses. Distinguish observed facts, design choices, assumptions, and untested behavior. State a disproof condition for consequential proposals and readiness claims.
- Make uncertainty safe to report. Describe the failing contract and its consequence without blaming the person who found it. Do not imply that a configured key, a selected build flag, or a passing HTTP probe proves the integrated product.
- The working audience assumption is that reviewers value reproducibility and data meaning over promotional completeness. Revise the presentation if readers cannot locate the next action or distinguish evidence from planned work.

## Information ownership

README.md gives purpose, current status, essential constraints, and a link to docs/index.md. The docs index routes readers to goals, roadmap, contribution guidance, and authoritative specs. Requirements own acceptance criteria; spec research/feasibility files own findings; spec.json owns approval state; the breadth map owns capability-to-check/evidence traceability. Summaries link these sources rather than duplicating them.

Write project Markdown in the owning specification's configured language. Keep links relative and verify them after moves. Date experimental evidence and identify its source revision or runtime when relevant. Do not describe untested commands as a working installation procedure.

## Financial explanations and comments

Document applicable financial units, currencies, periods, date/frequency conventions, transformations, provenance, missing values, and provider entitlement boundaries. Separate an observed datum from a derived result. Use explicit formulas and comparison evidence where a numerical transformation requires explanation.

Apply the same clarity at the point of change in code. Comments explain why: domain constraints, invariants, compatibility decisions, or failure handling that the code alone does not make clear. Keep them close to the relevant decision. Do not narrate obvious syntax, duplicate names, or attach a process rubric to each function. Use durable spec links for longer rationale and remove stale comments when behavior changes. Code comments remain part of physical production-file counts under complexity.md.

## Review and adoption

Let the implementing engineer use the relevant page at the point of work, then let an independent reviewer try to disprove its claim using the linked criteria. Carry successful guidance into the contribution guide and worker handoffs. A general broadcast or a longer document does not substitute for usable guidance beside the decision.

Before delivery, check that the opening gives a useful conclusion, headings match their content, each paragraph serves the reader's action, and links expose the evidence. Run a humanizer pass on drafted prose: remove inflated claims, vague authorities, forced patterns, filler, decorative emphasis, and generic conclusions. Prefer plain words and straight quotes; avoid decorative symbols and em/en dashes. Preserve precise technical terms and financial distinctions.

This policy is a portable adaptation of COBESY's conclusion-first structure, adult learning, falsifiable framing, and in-workflow guidance. It requires clear writing and reviewable claims, not extra paperwork for routine comments.
