# QOpenBB documentation

## Install and operate

| What you need to do | Where to start |
| --- | --- |
| Install Workspace, the data API and modeling with Docker Compose | [Quick start](../README.md#start-with-docker-compose) · [Installation settings](install.md#configure) |
| Sign in, connect a backend or diagnose an empty dashboard | [First login](install.md#first-login-and-onboarding) · [Startup checks](install.md#check-startup-problems) |
| Update the images and keep account connections and saved dashboards | [Persistence and updates](install.md#persistence-and-updates) |
| Set up remote access or change administrator credentials | [Remote access](tips-and-tricks.md) · [Password update](install.md#update-the-bootstrap-administrator-password) |
| Operate the modeling service independently | [Modeling deployment](modeling-deployment.md) |

## Research companies and markets

| Analyst question | Guide |
| --- | --- |
| How do I select the same listing across widgets and inspect its financial statements? | [Company selection](company-selection.md) · [Company Research](company-research.md) |
| Which earnings figures, filings, transcripts and news can I inspect? | [Events and Documents earnings example](../verification/earnings-calendar/README.md) · [Provider coverage](provider-coverage.md) |
| What do the reporting period and source fields mean? | [Statement-period provenance](reference/statement-period-provenance.md) |
| Which chart suits my data, and what does it show? | [36 historical financial chart examples](chart-gallery.md) |
| How are ETF returns compared with dated real yields? | [Commodities versus Technology worked example](../artifacts/reviewed/research-stories/packaged-acceptance.md) |

## Evaluate scope and evidence

- Assess what the workspace is designed to do and which capabilities have been exercised. [Goals](goals.md) · [Capability and test coverage](../.kiro/breadth.toml)
- Check which images were published and what passed on those images. [Release history](prototype-delivery.md) · [Published earnings and Range checks](../verification/earnings-calendar/README.md#published-alpha)
- Trace an individual result to its test or supporting data. [Evidence conventions](evidence.md) · [Reviewed artifacts](../artifacts/reviewed/README.md)

## Develop and extend

- Find planned work, dependencies and the specification that owns a change. [Roadmap](roadmap.md) · [Milestone checklists and workstreams](delivery-history.md) · [Specification ownership](../.kiro/spec-ownership.toml)
- Set up a development environment, contribute a change or run verification. [Development](development.md) · [Contributing](contributing.md) · [Verification](verification.md)
- Extend data sources, models or visualizations. [Data runtime](data-runtime.md) · [Modeling contract](modeling-contract.md) · [Renderer capabilities](renderer-capability-matrix.md)
- Look up build contracts, chart behavior, compatibility decisions and historical tests. [Implementation reference index](implementation-references.md)
