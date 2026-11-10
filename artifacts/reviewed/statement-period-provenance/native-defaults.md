# Native statement Limit defaults repaired

A newly added Balance widget returned HTTP 422 with its optional Limit control left blank. The standard native query supplied `None`; the FMP adapter rejected it before acquisition. Cash already supplies 5 for an omitted HTTP limit, but its optional Python value had the same adapter inconsistency.

API revision `a965f70c164fe477ce9c99654b9be48e2f1bc9fd` normalizes only missing/None limits to each adapter's declared default 5. Explicit zero, booleans, floats and malformed raw Python strings remain invalid. Literal HTTP `null`, `None`, empty and nonnumeric limits remain safe 422 responses; numeric HTTP query strings still parse normally. No generic query, monetary transformation, provenance rule, transport or widget layout changed.

Installed RED: three failures and 19 passes. After the protected FMP package refresh, all three affected test files passed: **144 tests**. Independent financial review passed **66 selected tests**. All nine maintained installed core/FMP hashes match source; the final combined gate checks **110 files**, with zero errors or violations. One checker invocation used the wrong working directory and could not find its TypeScript parser; the corrected clean-root invocation passed. Both records remain external.

The original browser failure is retained: five FMP sends, zero FRED, zero budget denials, and confirmed owned-session cleanup. Income checks passed before Balance failed. This source repair is accepted; a rebuilt API image and corrected browser journey are still required. Workspace source is unchanged.

External evidence: `task6/native-defaults/{red.txt,green.txt,review-tests.txt,refresh.log,all-installed-hashes.json,combined-complexity-final.json}` under `D:/BuildArtifacts/QOpenBB/statement-period-provenance`.
