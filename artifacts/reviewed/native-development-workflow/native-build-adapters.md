# Native build and image-command adapters

Task 9 passed independent Astra review on 2026-11-10. Existing image commands now receive explicit native Dagger and SDK executables, use the selected container CLI and retain pinned CLI/SDK/engine checks. Source identity compares normalized filesystem locations while retaining repository, revision and dirty-tree checks. Child processes remain hidden and use the bounded build environment. Publication behavior is unchanged.

The consolidated native suite passed 133 tests; two symlink-fixture cases were skipped because Windows denied symlink creation. Four focused loader tests then passed for Docker and Podman image-load announcements without weakening configuration/manifest validation. Review found a Windows-only test constant that would fail on Linux; the assertion was made platform-aware and independently verified. Actual Linux execution remains task 12.

All six changed production modules and the combined 92-file controller gate passed the 400/300/50 limits. Raw results and independent review remain under `D:/BuildArtifacts/QOpenBB/native-build`: `task9-tests.log`, `task9-junit.xml`, `task9-size.json`, `task9-red-observed.json`, `task9-remediation.log`, `combined.json` and `review/final-verdict.md`. The RED record explicitly summarizes observed transcript output rather than presenting it as a saved raw log.

No image build, export or publication was performed for this source task. Task 10 must still qualify the real pinned native Dagger export/load path; passing adapter tests does not establish engine transport compatibility.
