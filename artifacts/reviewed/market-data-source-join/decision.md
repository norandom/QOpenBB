# Accepted baseline source join

The data source pin advances to the independently accepted component commits through d1bb4821a659e6a9d28b9554ba670e72d80a69fb. CI measures every maintained file at the pinned source; retaining the old pin would omit the new helpers and fail its missing-file guard. Workspace remains at c652b909627d7634241eee2ed13a561fbb4f177b with Node 24.22.1.

Only the three existing baseline dataset commands remain registered; no later family is activated. Profile/income errors and values retain compatibility; FRED legacy outputs remain. The generated catalog keeps its historical generator/image identity until the reviewed proposal in task 5.3. This source synchronization does not complete that task, advertise live provider access, or claim a new image release. Local path dependency declarations and resolved versions are unchanged.

Owning tasks 1.1–1.3, 2.1–2.2 and 3.1–3.3 have independent source reviews and focused checks. The canonical CI maintained-scope gate and portable delivery checks are run on Node 24.22.1 for this join. Unrelated renderer edits remain unstaged.

The first canonical join attempt exited 1: all 657 maintained files were measured physically, but the 549-file JavaScript/TypeScript batch exceeded its global 60-second deadline. The original failed report is retained locally. The existing subprocess deadline is extended to 180 seconds; no file is excluded, no cap or assertion changes, and timeout remains a failed gate. A single canonical rerun verifies the adjustment.

Final verification, 2026-10-28: `PATH="$PWD/artifacts/task-1.2/node-v24.22.1-linux-x64/bin:$PATH" bash pipeline/ci.sh check` exited 0. The canonical maintained-scope report passed all 657 files with Node 24.22.1/TypeScript 6.0.3 and no errors or violations; all 193 portable delivery tests passed in 39.67 seconds. Independent adapter checks passed 17 tests. Source join review is recorded beside this decision. These checks do not establish live-provider entitlement or a rebuilt-image release.
