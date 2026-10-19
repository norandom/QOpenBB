# Roadmap

Deploy the current QOpenBB prototype next, then evolve it through small verified deliveries. This owner-approved sequence replaces the former all-features-before-release plan. Existing evidence and unfinished obligations remain intact.

## Now: deploy the prototype

Scope: existing Full Workspace and installed data API. Further provider coverage, renderer families, theme changes, commands, AI, Excel and custom sources are not prerequisites. Preserve working functionality and disclose supported capabilities and gaps.

| Slice | Deliverable | Acceptance |
| --- | --- | --- |
| P1: freeze candidate | Reconcile pending fixes, fork pins and supported-capability manifest | No unrelated edits included; source identities and known gaps recorded |
| P2: CI/CD | Portable checks/publication, thin GitHub runner and Dagger image builds | Checks fail closed; PR jobs exclude publication/provider secrets; immutable image identities |
| P3: assembled prototype | Real service images in executable Compose | Existing isolated E2E proves login, supported data/widget use, save/reopen, restart and diagnostics against candidate images |
| P4: install/recover | Pull-only instructions, release manifest, backup/restore and rollback | WSL rehearsal and state recovery; owner-run server outcome recorded separately |

Target: HTTP on `0.0.0.0:23003`, `qbb.hanse-hedge.fund` through owner-managed cloudflared, relative bind-mounted data. The owner deploys locally with Compose; no SSH, tunnel service or Jupyter dependency.

Current gaps: `.github/` is absent, Compose remains a proposal, and publication/release acceptance are open. Reuse existing Dagger build/export and browser tools. Pending bundle-script removal and axis persistence require candidate reconciliation and image verification. A local preview or source-level check is not a published release.

## Subsequent workstreams

| Spec | Responsibility | Sequence |
| --- | --- | --- |
| [openbb-self-service](../.kiro/specs/openbb-self-service/spec.json) | Foundation and prototype delivery | Active now; close with explicit scope/evidence handover |
| [market-data-integrations](../.kiro/specs/market-data-integrations/requirements.md) | FMP horizontal coverage, yfinance/FRED and future providers; shared identity and semantics | After prototype; installed adapters stay in baseline |
| [analyst-workspace](../.kiro/specs/analyst-workspace/requirements.md) | Widgets, commands, linked instrument/time views, consistent visuals and remaining renderer/table functionality | After prototype; build on existing work |
| [workspace-ai](../.kiro/specs/workspace-ai/requirements.md) | Anthropic, grounding, streaming and recovery | Independent of prototype |
| [openbb-excel](../.kiro/specs/openbb-excel/requirements.md) | Add-in, generated functions, authentication and Office acceptance | Retained dependency: Anthropic accepted first |
| [custom-data-source](../.kiro/specs/custom-data-source/requirements.md) | Own datasets and later PostgreSQL | Deferred |

Quant plugins remain later work. Successor specs are initialized scope descriptions, not approved detailed requirements or tasks. Do not generate all their implementation plans before shipping the prototype.

## Breadth and end-to-end checks

[Spec ownership](../.kiro/spec-ownership.toml) records transferred obligations. The existing [breadth map](../.kiro/breadth.toml) retains historical criteria, actual tests and evidence. New capability records need one owning spec/criterion, implementation state, actual test paths, evidence identity and release relevance. Planned checks never count as passing tests.

The [provider map](provider-coverage.md) describes horizontal scope. Track provider availability separately from adapter, widget, consistency and E2E acceptance. Shared semantics cover readable identities, units, time, provenance and linking; provider origin should not change the analyst's interaction pattern.

Keep isolated Playwright/CDP, bounded xdist, financial semantics, persistence and failure/recovery checks. Run affected checks per change and the integrated prototype journey at the release gate. Publish concise reviewed evidence; do not turn each check into another planning project.

The [agile delivery amendment](../.kiro/steering/delivery-workflow.md) supersedes older sequencing and whole-spec gates. Retain independent review, complexity caps and per-task commits. Transfer unfinished work without marking it complete.
