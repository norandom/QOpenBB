# Source-filter repair review

APPROVED for task 2.93. The implementation restores exactly seven required AI artifact TSX source files to staged image inputs, without broadening directory admission. Controller may now restage the locked sources and retry the ordinary build.

- Diff reviewed directly: `pipeline/qopenbb_ci/source_filter.py` adds only seven exact `PUBLIC_SOURCE_FILES` entries. `tests/contracts/test_source_filter.py` verifies all seven survive and rejects generated siblings, private/environment/database files, alternate extensions, nested artifact/evidence/state paths and unrelated artifact directories.
- Independent verification on 2026-10-19: `wsl -d Debian -u mc -- bash -lc 'cd /mnt/d/Source/QOpenBB && PYTHONPATH=pipeline /home/mc/qopenbb-work/sqlite-runtime/venv/bin/python -m pytest tests/contracts/test_source_filter.py -q'` exited 0: **12 passed in 0.37s**.
- RED phase: verified `source-filter-red.txt`, one failed and eleven deselected. The required seven-file set was empty before the exceptions. Worker GREEN evidence also records twelve passing tests.
- Whole production file independently measured with `tools.quality.python_units.measure_python`: **133 physical lines / 83 logical units / 18 maximum function units**, within 400/300/50 limits. Scoped `git diff --check` passed. Placeholder and concrete secret-pattern scans were clean; runtime-sensitive imports were spot-checked.
- Boundary audit: clean against task 2.93 and its approved repair design. Global artifact exclusions, private filename/suffix checks and symlink rejection remain active. No application, PWA, dependency or Dagger changes appear in this repair. No mandatory remediation or blocking findings.

This approves the input-filter repair only. It does not establish successful frontend compilation, image export, packaged-page behavior, release readiness or task 2.91 completion; those require fresh build/runtime evidence.
