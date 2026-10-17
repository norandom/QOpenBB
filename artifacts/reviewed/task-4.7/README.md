# Task 4.7 read repair evidence

The seven-site CRUD repair passes all 53 SQLite tests, with zero skips, on Python 3.13.15 and SQLite 3.53.1. This verifies query behavior only. Bulk save, application restart, renderer behavior, provider access and browser persistence remain outside this task.

## Reproduce

Run from WSL Debian as `mc`:

```sh
/home/mc/qopenbb-work/sqlite-runtime/venv/bin/python /mnt/d/Source/QOpenBB/artifacts/task-4.7/verify.py review
/home/mc/qopenbb-work/sqlite-runtime/venv/bin/python /mnt/d/Source/QOpenBB/artifacts/task-4.7/audit.py review
```

`verify.py` invokes the accepted isolated launcher serially. Its explicit pytest-asyncio plugin, synthetic settings, denied private reads/network, disposable file-backed database and cleanup remain unchanged. The wrapper fixes PATH to the actual WSL venv and records the child command, exit, complete distribution identity, source SHA256 manifest and Workspace base revision. No dependency installation occurred. The frozen lock and task 4.6 infrastructure hashes are unchanged.

## Before and after

The final prepatch source was Workspace `693954f43aac8af888cfe6e7bfed6d9dcb72d2f5`, CRUD SHA256 `51fc65e7cea5938a8654f90671fd8180f81a0fea6fcd955f20d991ad6053c411`. [red-final.json](red-final.json) and [red-final.log](red-final.log) record 10 failed and 43 passed tests before any production edit. The failing cases are eight ordinary entity-shared name projections, the raw-cardinality regression and entity membership. One selected dashboard produced four actual rows and a Cartesian-product warning. Distinct owner, creator, recipient and unrelated names prevent attribution errors from hiding behind identical display values.

SQLite 3.53.1 supports the original `concat` function: the other five read functions pass their name cases on the baseline. No six-function failure or older SQLite execution is claimed. The six typed additions compile to SQLite `||` and MySQL `concat`; captured actual selects and row counts are retained in the logs. MySQL compilation is supplementary evidence, not live MySQL acceptance.

[green.json](green.json) and [green.log](green.log) record 53 passed tests, zero skips, exit 0, after exactly six name-expression replacements and the ordinary entity-shared creator join. CRUD SHA256 is `575b2cdeb0f04aab81af60b34074e4b9c2c6e21cfb6559c695e502361defc6e9`. The final RED and GREEN runs use identical tests, frozen fixtures and lock. No feature flag was introduced under the owner's parity instruction.

`seal.py` independently compares the RED/GREEN manifests, current source hashes and the original committed CRUD text after precisely the approved seven substitutions. [boundary.json](boundary.json) records those assertions and the hash of the retained [exact patch](crud.patch). Its assertions pass. The placeholder scan of the three new test modules returns no matches.

The test matrix covers eight name pairs for each of six functions: full names, either null component, both null, both empty, whitespace, empty first and empty last. Assertions cover exact display trimming/email fallback, IDs, content, dates, creator and sharing flags. Membership cases cover active/inactive shares, edit/view behavior, self-owned exclusions, unrelated recipients, multiple entities and distinct permission maps within one entity. The noex projection retains owner-permissions membership and owner display attribution. The ordinary entity projection checks creator identity, raw cardinality, exclusions and empty results. All calls delegate to actual session execution against original mapped types; the capture wrapper freezes and replays the returned real rows solely to inspect cardinality and compile the actual selects.

## Static checks and size

[baseline-audit.json](baseline-audit.json) and [final-audit.json](final-audit.json) use the project's `physical_lines` and `measure_python` functions. Both measure 1599 physical lines, 582 logical units and maximum function size 36. The patch remains within the owner-approved 1600/582 exception and the 50-unit function cap. Controller-owned exception registration and independent review remain required.

Actual scoped Ruff lint and formatting checks pass for all three new test modules. Actual CRUD Ruff lint passes before and after. Whole-file CRUD formatting fails on the unchanged baseline and repaired source; the logs retain both results. No unrelated formatting was applied to the oversized upstream file.

## Initial test corrections

[red.log](red.log) preserves the first genuine run: 35 failed, 16 passed and two bootstrap tests deselected. Besides the missing join, it exposed two incorrect test assumptions: dashboard content is a returned dictionary, and app membership fixture content must use schema-valid `widgets: []` rather than the general builder's default dictionary. These tests were corrected without changing production or the frozen builders. [red-corrected.json](red-corrected.json) and [red-corrected.log](red-corrected.log) then record 10 failed and 43 passed. Distinct display names and explicit positive creator/edit-share assertions were added before the final prepatch run. All original failure evidence is retained; setup mistakes are not presented as production defects.

The implementation supports requirements 1.1, 1.4, 4.2, 4.7, 10.5 and 10.6 only within the approved query-repair boundary. The controller owns breadth, source pins, acceptance records and commits. No task completion or integrated product acceptance is asserted here.
