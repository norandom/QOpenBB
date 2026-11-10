# Native command and source integration

Task 11.1 is accepted on 2026-11-10. The PowerShell entry now routes build, start, verify, recreate and stop to the reviewed native consumers. Build takes explicit staged sources, archive, pinned SDK and owned engine. Verify checks current container health and readiness, then runs synthetic infrastructure checks; it does not claim financial acceptance.

Source promotion is limited to Workspace fixture commit `18930d870caec08df12697e7858e05e8dbe9dd68`, whose parent is `f832a5593223b1e702970c4de8eceda87a17fa5b`. The only fork difference is the checked private-reader fixture (+6/-2). Independent Astra review confirmed identical blobs for all nine targets covered by 19 size exceptions. Only revision identities change; limits, baselines and expiry remain intact.

Verification: 54 focused checks passed, one POSIX case skipped. Review reproduced and verified fixes for stale-ready exited containers and lost actionable diagnostics; arbitrary private exception payloads remain suppressed. Independent Astra review approved. Both the actual nonempty fork transition scope and final promoted-pin combined gates passed; production code remains within 400/300/50.

Financial inputs are frozen to the existing Income journey once, company initial/reopen around recreation, and synthetic company failure journey once. The owner approved a shared ceiling of 80 FMP requests for company search/profile/income and 16 FRED GDP requests, without automatic reruns. Credentials are present but untested. Actual upstream budget enforcement and live execution remain task 11.3; redirects and internal retries must count toward the ceiling.

Raw dispatch evidence, pin review and exact candidate manifests remain under D:/BuildArtifacts/QOpenBB/native-join. No application build, financial browser acceptance, Linux integration acceptance or publication is established by this record.
