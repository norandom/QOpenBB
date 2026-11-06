# Requirements Document

## Project Description (Input)
Financial analysts need familiar research workflows across reusable widgets, commands and linked instrument/time views. Extend the existing Workspace and ECharts work with consistent semantics and a Bloomberg-inspired theme. Retain outstanding renderer/table obligations. Quant plugins are later work; provider adapters belong to market-data-integrations.

## Requirements

Owner scope clarification: this spec owns acceptance of saved research context: dashboard layouts, widget parameters, selected instruments, linked time ranges and group memberships, including reopening after container recreation. Existing persistence implementation and tests are retained. This acceptance is deferred from the prototype release, not marked passed. Infrastructure backup/restore remains a separate deferred delivery obligation.

The owner-approved investment-analysis direction is captured in the [bounded investment-analysis contract](investment-analysis-contract.md), with IA1-IA10 acceptance criteria and staged delivery. The next [IA-A input-readiness requirements](research-input-requirements.md) are owner-approved; the bounded verification design is the next approval gate. This extends the scope without declaring the umbrella requirements/design/tasks complete. Remaining umbrella requirements will be generated as needed.

Owner clarification, 2026-10-30: company selection needs a searchable **Company name** field and an adjacent linked **Symbol** field. The [company-selector requirement](company-selector-requirement.md) records the interaction, listing disambiguation and discovery API reuse. Its bounded implementation is now [accepted and published](../../../docs/company-selection.md); the future investment-analysis dashboard remains separate.


