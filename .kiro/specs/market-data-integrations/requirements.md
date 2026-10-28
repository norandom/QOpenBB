# Market data integration requirements

## Introduction

Financial engineers need exploratory access to FMP, complementary Yahoo Finance prices and FRED economic series through consistent contracts. A dataset must be usable outside any single demonstration dashboard. The same financial meaning must reach widgets and later AI consumers, while the chosen provider remains visible.

This specification supplies data for the [investment-analysis workflow](../analyst-workspace/investment-analysis-contract.md). Its first delivery supports quarterly financial analysis and peer valuation; the complete roadmap retains broader FMP research coverage. Requirements and design are owner-approved. The first implementation task batch is owner-approved; implementation and provider entitlement acceptance remain in progress.

## Boundary context

- In scope: discoverable provider coverage, named instruments/series, parameterized data access, typed financial results, provenance, visible failures and reusable consumer contracts.
- Adjacent: analyst-workspace owns dashboards, peer-selection UX, assumption editing, research context and commands. The separate-repository [financial-modeling workstream](../financial-modeling/brief.md) owns house calculation/scenario execution and financial validation. This spec supplies financial inputs and provider-calculated outputs; FMP DCF is an optional comparison, not the house model. This ownership clarification does not expand the approved provider implementation tasks.
- Deferred: database connectors/PostgreSQL, AI execution, Excel, Quant plugins, Jupyter hosting, new chart engines, automatic cross-provider fallback and a general-purpose SQL/ORM interface.
- Binding owner constraint: reuse the owned OpenBB Provider/Fetcher, standard query/data models, Query execution, routers and OBBject; widgets and later AI shall use the same maintained command/API schemas. Adapt existing provider code. The [reuse research](research.md#owned-openbb-platform-and-provider-reuse) retains the technical decisions and earlier MD-F1-MD-F5 mapping for design. This is not a new query framework.

## Requirements

### Requirement 1: Discover coverage before making a request

**Objective:** As an analyst, I want to discover usable datasets and their limits without knowing provider-specific URLs.

1.1 When a consumer requests the dataset catalog, the data service shall return dataset identity, financial purpose, supported providers, parameter definitions, result-field definitions and known query limits.
1.2 The data service shall distinguish documented provider availability, implemented adapter, verified account access and verified consumer behavior; lack of evidence shall be labeled unverified.
1.3 When a provider capability is unavailable or not implemented, the catalog shall identify that state without advertising it as a working dataset.
1.4 The coverage record shall map the agreed FMP research families in the [provider inventory](../../../docs/provider-coverage.md) to their implementation state and outstanding work, including documents, ETFs, ownership, futures/commodities and COT rather than reducing scope to equity prices.

### Requirement 2: Supply reusable research datasets

**Objective:** As an analyst, I want parameterized financial datasets that support exploration and professional valuation workflows.

2.1 The data service shall provide the first analyst slice with company discovery/profile, peer references, historical prices, income statements, balance sheets, cash-flow statements, share-count/capitalization inputs and enterprise-value/ratio inputs through reusable queries.
2.2 The data service shall expose FMP DCF values and the documented model inputs and customization parameters that its verified integration supports, separately from analyst-created valuations.
2.3 The data service shall progressively provide supported datasets across the agreed estimates/ratings, quarterly/segment detail, filings/reports, news/transcripts, fund, ownership, cross-market, other-asset and macro/positioning families. Concrete dataset acceptance shall be assigned to bounded delivery batches; unimplemented and entitlement-blocked datasets shall remain open rather than satisfying this obligation through catalog entries alone.
2.4 When a request specifies supported symbols, dates, fiscal periods, frequency, fields or pagination parameters, the data service shall apply their documented semantics or reject unsupported combinations explicitly.
2.5 When data is paginated or limited, the data service shall expose continuation or truncation information sufficient to distinguish a complete result from a partial result.
2.6 If an account lacks access to a required dataset, the delivery record shall identify that acceptance as blocked by entitlement rather than passing it using a synthetic substitute.

### Requirement 3: Resolve names and preserve instrument meaning

**Objective:** As an analyst, I want to select recognizable instruments and economic series while preserving their identity across providers.

3.1 When a consumer searches by a supported name or identifier, the data service shall return readable names, provider identifiers and available distinguishing attributes such as exchange, currency, instrument type or series units.
3.2 If a name or symbol resolves to multiple instruments, the data service shall expose the alternatives rather than silently selecting one.
3.3 The data service shall distinguish issuer identity from security/listing identity and preserve the mapping used by each request.
3.4 The data service shall distinguish spot benchmarks, dated futures, provider-selected futures references, verified continuous series, equity-index futures and COT positioning; an undocumented roll convention shall remain unknown.
3.5 When a dashboard supplies a company and date context, the data service shall preserve the independent series identity of macro observations rather than treating an equity symbol as a macro-series identifier.

### Requirement 4: Preserve financial semantics and provenance

**Objective:** As an analyst, I want comparable and auditable financial observations rather than merely matching column names.

4.1 The data service shall identify each result's provider, retrieval time, query context and available observation/valuation/publication dates, with unavailable metadata marked explicitly.
4.2 The data service shall expose each financial field's definition, unit/scale and currency where applicable; the service shall distinguish raw provider observations, provider calculations, estimates and locally derived values.
4.3 When returning statements, the data service shall distinguish annual, discrete-quarter, year-to-date and trailing periods, retaining fiscal end dates and available filing/restatement information.
4.4 If a transformation derives a quarter, converts units or currency, adjusts prices or calculates a ratio, the result shall retain its input basis and transformation definition.
4.5 The data service shall preserve missing values without converting them to zero and shall distinguish a missing datum, an empty result and a failed request.
4.6 If historical vintages or publication dates are unavailable, the service shall disclose that limitation and shall not label the response point-in-time safe.
4.7 When providing valuation inputs, the service shall identify the relevant share-count, debt/cash, lease, minority-interest, forecast-period and market-date bases where available, leaving unknown conventions explicit.
4.8 When returning FRED or other economic series, the service shall preserve source, frequency, seasonal-adjustment status and units where available; time alignment shall not silently imply interpolation or equal fiscal periods.

### Requirement 5: Keep provider selection explicit and extensible

**Objective:** As an operator, I want to add or change supported providers without rewriting every consumer.

5.1 When a query selects an installed provider supporting its dataset, the service shall execute that selection and identify the actual provider in the result.
5.2 When no provider is selected, the service shall use an explicitly configured default for the dataset or return an actionable selection requirement.
5.3 If a selected provider fails or lacks the dataset, the service shall not silently substitute another provider or financially different instrument.
5.4 Where providers implement a shared dataset contract, consumers shall receive the same documented common-field meanings while provider-specific fields and limitations remain discoverable.
5.5 When a compatible provider extension is added, existing consumers of its supported shared datasets shall remain usable without provider-specific fetching logic in each consumer.
5.6 The maintained coverage shall identify Yahoo Finance as a complementary price source and FRED as an economic/benchmark source without implying that Yahoo futures aliases are physical spot prices.

### Requirement 6: Support widgets and later AI through one contract

**Objective:** As a consumer developer, I want one discoverable data contract for exploratory widgets and later AI tools.

6.1 When a consumer discovers a supported dataset, the service shall supply parameter names, types, required/default values, allowed choices where defined, and output-field descriptions suitable for constructing an exploratory query.
6.2 When widget and programmatic consumers submit the same effective query, the data service shall return consistent financial values, provenance and error meanings regardless of presentation.
6.3 When an existing public contract changes incompatibly, the delivery shall identify the change and provide an explicit migration or compatibility path before advertising affected consumers as supported.
6.4 When returning news, filings or transcripts, the service shall expose available readable content, attribution, company linkage and event/publication dates; metadata-only or partial content shall be identified as such.
6.5 The service shall expose the supported query and result contracts without requiring Jupyter, an embedded browser or an AI service to be running.

### Requirement 7: Fail clearly and protect credentials

**Objective:** As an operator, I want predictable provider failures and bounded requests without exposing credentials.

7.1 If authentication, entitlement, throttling, timeout, unsupported input or provider-response validation fails, the service shall return a distinguishable actionable error without credentials or private upstream request details.
7.2 The service shall keep provider credentials server-side and exclude them from public catalogs, schemas, logs, error text and committed evidence.
7.3 The data service shall document result/request bounds for each supported query; when a caller exceeds them, the service shall reject the request or return explicitly marked partial results rather than silently truncating data.
7.4 If a provider reports a retry interval, the service shall preserve actionable retry information; it shall not perform unbounded retries.
7.5 If cached results are served, the service shall expose their retrieval/freshness information rather than presenting them as freshly fetched observations.

### Requirement 8: Retain independent operation and prove accepted coverage

**Objective:** As the maintainer, I want reproducible owned-source releases and evidence that distinguishes working data from planned coverage.

8.1 The maintained platform and adapted providers shall be committed to owner-controlled repositories with exact source revisions, upstream provenance and applicable notices retained.
8.2 The released data service shall provide its supported capabilities from published images without uncommitted local patches or an upstream-hosted OpenBB service.
8.3 When assessing a dataset for acceptance, the verification process shall compare representative real-provider responses with its displayed/programmatic result, including identity, values, units, periods and provenance.
8.4 The verification process shall include relevant missing/invalid input and provider-failure cases; synthetic edge cases shall supplement rather than replace real-provider acceptance.
8.5 The breadth record shall link each accepted capability to its owning criteria, actual checks and source/image evidence, and shall retain unverified capabilities as open.

## Approval and delivery boundary

The requirements review checks scope, financial semantics and testability. It does not establish working endpoints, subscription access or implementation completion. After owner approval, the gap/design phase defines the first bounded provider batch, consumer contracts and disjoint implementation lanes. Existing complexity enforcement and background verification are mandatory; no new testing framework is prescribed here.
