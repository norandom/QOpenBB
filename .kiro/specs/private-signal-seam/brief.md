# Brief: private-signal-seam

## Problem

The owner has a proprietary computational macro model for factor timing. Its signals should appear in QOpenBB stories next to public evidence. The model, its inputs and its samples must stay private: they may not enter repositories, public contracts, catalogs, fixtures, releases or evidence mirrors.

## Current State

- No interface exists for externally computed signals.
- Published artifacts are mirrored and hash-checked; nothing marks an input as private.
- The transparent regime rule in factor-signals is the only planned regime source.

## Desired Outcome

An installation can supply regime labels and factor-timing signals from an external model through a private interface. Stories show them beside, or in place of, the transparent regime rule, clearly labelled as externally supplied. A public build of QOpenBB works unchanged without any private signal, and no public artifact reveals private content.

## Approach

Define a small, versioned signal contract: dated regime labels and factor tilts with an as-of time and a source label, and nothing about how they were produced. The installation provides signals from local, private storage. The modeling service treats them as inputs with their own check states (dated, non-overlapping, no future dates) and never copies them into public evidence.

## Scope

- **In**:
  - the signal contract and its validation checks
  - private, installation-local supply of signals
  - labelling of externally supplied signals in results and stories
  - checks that no private content reaches catalogs, fixtures, logs, exports or the evidence mirror
  - synthetic signals for tests and public evidence
- **Out**:
  - the proprietary model itself, its code, inputs and samples
  - reproducing or approximating the proprietary method
  - hosting, scheduling or running the external model

## Boundary Candidates

- signal contract and validation
- private storage and access control
- publication guards for private content

## Out of Boundary

- factor definitions and diagnostics (factor-signals)
- story layout (research-stories)

## Upstream / Downstream

- **Upstream**: factor-signals (where a regime source is consumed); financial-modeling (input and check contracts)
- **Downstream**: research-stories that display external signals

## Existing Spec Touchpoints

- **Extends**: none
- **Adjacent**: custom-data-source (user-supplied datasets, deferred); financial-modeling (owner-scoped run storage)

## Constraints

- Proprietary content is never read into public tests, evidence or documentation. Development and review use synthetic signals only.
- Private signals are excluded from exports, saved dashboards and logs by default.
- Out-of-sample honesty: a supplied signal carries its as-of time, and results never use a signal before that time.
