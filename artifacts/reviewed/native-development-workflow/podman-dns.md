# Native Workspace DNS portability delta

The packaged financial attempt stopped at catalog discovery: nginx dynamically resolves data-api through 127.0.0.11, but the actual Podman container DNS was 10.89.9.1. The fixed Docker-only resolver default caused a one-second DNS timeout and catalog 502 before any provider send. No financial rerun is included here.

Bounded change: lite/configure-origin.sh preserves a nonempty explicit NGINX_RESOLVER exactly. Otherwise it reads the container /etc/resolv.conf and selects the first syntactically valid IP nameserver, ignoring comments and invalid entries. IPv6 addresses are emitted in nginx brackets. Scoped IPv6 addresses are skipped because scope syntax is not supported by this automatic nginx address selection. Missing/unreadable files or no usable entry fail before routes are written with an actionable explicit-override message. No Podman subnet or Docker resolver is hardcoded as a default. Startup already requires Python; its standard-library ipaddress adds no dependency.

No fork AGENTS.md was present in the repository file inventory. QOpenBB delegation/testing/complexity/CI guidance applies. Only configure-origin.sh and its focused test were changed. Parent owns fork scope inventory, clean commit/pin promotion and Dagger build. The new lite/test_configure_origin.py is test code, not a production exemption; include its actual path in the fork changed-file manifest and test exclusion records as required by the existing inventory contract.

Verification: native pinned Python 3.13.15 plus explicit C:/Program Files/Git/bin/bash.exe; no image/app/provider/browser run. Six test methods pass (eight input cases) covering Docker DNS, first-valid Podman DNS, IPv6 brackets, explicit multi-address/port override with missing resolv.conf, empty override fallback, and missing/empty/invalid/scoped resolver failure. The harness executes the real shell startup with only the resolver file path, pinned Python executable and envsubst invocation redirected to fixtures. envsubst is a bounded fixture exposing the exported resolver; real origin_config.py and Excel-disabled startup append execute. It therefore proves resolver selection and fail-closed startup behavior, not nginx DNS runtime connectivity. Initial harness failures concerned legacy Bash/path resolution and fixture command selection, not a claimed application RED result; final test explicitly selects native Git Bash.

Exact checks from owned fork root:

`D:/BuildArtifacts/QOpenBB/native-foundation/pipeline-venv/Scripts/python.exe -B -m unittest discover -s lite -p test_configure_origin.py -v`

`"C:/Program Files/Git/bin/bash.exe" -n lite/configure-origin.sh`

Results: dns-tests.log, exit 0; Bash syntax check exit 0. Frozen source hashes: dns-freeze.json. Shell 50 physical lines; test 75 physical / 56 logical units / largest function 21, below 400/300/50. Shell receives the policy's physical-only count. Actual nginx parsing/container DNS routing and the new exact-image qualification remain pending parent-owned reviewed rebuild and offline acceptance.
