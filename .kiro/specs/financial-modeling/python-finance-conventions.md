# Polars and financial Python conventions

Owner direction, 2026-10-28: the separate modeling repository uses Polars and idiomatic Python, with financial-domain names and explanatory comments. These conventions are part of the design and must transfer into that repository's steering and agent handoffs. They do not require rewriting the OpenBB provider layer or installing packages during this specification-only session.

## Execution and contracts

- Use Polars DataFrame/LazyFrame for financial tables and expression-based transformations. Prefer native expressions, explicit selections, joins and aggregations over Python row loops or element UDFs. Use ordinary typed Python for orchestration, scalar calculations and rule outcomes; do not turn every scalar into a dataframe.
- Use lazy plans for multi-step table transformations where useful, and collect at an explicit bounded model/validation boundary. Small already-materialized inputs may remain eager. A lazy query plan is not proof that data values passed validation.
- Keep external APIs independent of Polars objects. Typed input/output contracts define record shapes and financial semantics; model-boundary adapters construct or serialize tables. No pickled dataframe payloads or exposed Polars query plans as API contracts.
- Record each table's row grain, key columns, required columns/dtypes, nullability, units, currency, period basis and origin. Schema validation is followed by value/financial checks. A type hint of `pl.DataFrame` alone does not establish a table contract.
- Validate join cardinality and unmatched rows explicitly. Join on financial identity and period keys, never incidental row position. Preserve or deliberately resolve duplicate/restated observations; do not silently pick the first record. Check period completeness before aggregation and preserve missingness rather than accepting an aggregate of incomplete inputs as complete.
- Keep dates, actual/forecast status and data vintage distinct. Sorting or resampling must not silently change fiscal alignment, stock/flow meaning or information availability.

## Financial precision

Use explicit numeric policies per field and method. Preserve exact source amounts and authoritative decimal values; specify precision, scale, rounding point and overflow behavior. Validate the selected Polars version's decimal operations and serialization against independent Python Decimal checks before using them for a method. Reject unsupported or lossy conversions instead of silently casting to Float64.

Scalar financial calculations can use Python Decimal directly. Methods that require floating-point numerical routines must declare that choice, tolerances and conversion boundaries in their own design; they cannot claim exact decimal arithmetic merely because outputs are later serialized as decimal strings. Display rounding stays outside calculation and verification.

Independent numerical verification must not reuse the production Polars expression or helper under another name. A separately expressed Python reference checks the same inputs, including null, scale and period edge cases. This preserves the house-standard verification requirement.

Polars uses native threads: bounded calculation processes must use a compatible spawn-based start method rather than fork inherited thread state. Set and verify a bounded Polars thread budget before importing it in the worker. Existing limits on evaluation processes and xdist workers still apply; do not multiply unrestricted pools.

## Names that explain the financial model

Use snake_case functions, columns and table variables; PascalCase typed contracts; conventional `import polars as pl`. Name financial concepts and distinguish calculation stages. Avoid `df`, `df2`, `tmp`, `data` or `result` as the main names of domain tables. Established finance abbreviations such as EBITDA and WACC are acceptable when defined in the module and contract.

| Object | Preferred example | Meaning to preserve |
| --- | --- | --- |
| Historical flow table | `quarterly_income_statements` | Discrete quarters, not an unspecified annual/YTD mixture |
| Balance table | `fiscal_year_end_balance_sheets` | Point-in-time balances rather than period flows |
| Cash-flow table | `annual_cash_flow_statements` | Specified fiscal-year flows |
| Adjustment table | `ebitda_adjustments` | Separate reported values and reviewed adjustments |
| Forecast table | `forecast_operating_cash_flows` | Forecast status, scenario and fiscal period |
| Comparison table | `peer_valuation_multiples` | Peer identity, valuation date and denominator basis |
| Economic table | `risk_free_rate_observations` | Selected benchmark with observation/vintage metadata |
| Function | `reconcile_enterprise_to_equity_value` | Financial operation, not a generic `process_data` |
| Rate column | `tax_rate_fraction` | Fraction rather than a display percentage |
| Identity columns | `entity_id`, `fiscal_period_end`, `scenario_id` | Explicit keys rather than positional assumptions |

Examples illustrate naming, not new implementation scope or approved formulas. Persistent table identifiers and exported logical table names follow the same domain vocabulary. Currency and scale may be table-contract metadata or explicit columns; mixed contexts require row-level identification. Names alone do not replace schema constraints.

## Idiomatic code and useful comments

Use small typed functions, explicit return types and cohesive modules. Avoid inheritance hierarchies where a function or protocol suffices. Keep model assumptions as named inputs, not constants hidden inside expressions. Name expression stages so a reviewer can follow the financial bridge without decoding a single long method chain.

Public model functions document financial purpose, input/table grain, period and sign conventions, output semantics, applicable method version and failure behavior. Comments explain accounting choices, cash-flow direction, exclusions, proxy assumptions and the rationale for a transformation. Do not narrate obvious Python operations or use comments as a substitute for clear names.

For example, explain that an increase in the selected operating-working-capital definition consumes cash, or why a cash-flow line needs a sign normalization. Do not merely comment that the code subtracts one column from another. Keep the source definition and adjustment rationale traceable in the calculation evidence as well as the code.

Apply the existing COBESY documentation policy. Comments count toward production-file limits. Do not compress readable financial logic to satisfy caps; split cohesive responsibilities.

## Extension acceptance

Every model task identifies its Polars table contracts and numerical policy. Review checks domain names, key/join behavior, missing values, aggregation completeness, precision and comments beside meaningful financial choices. Tests target those financial failure modes rather than snapshotting query plans or mirroring expressions.

Bootstrap pins Polars in the independent uv lock and verifies supported Python/platform wheels, required operations and bounded execution. No version, runtime compatibility or performance result is claimed by this document.
