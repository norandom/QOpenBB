# Data-only agent discovery

Independent Sol review accepted this source on 2026-10-27; rebuilt-image/browser acceptance remains pending.

The fresh published-image journey reached ordinary onboarding, live AAPL annual income, displayed-value comparison and refresh. Its strict diagnostics then exposed two `/data/agents.json` 404 responses. Prior network-error assertions had reported the external thumbnail first; complete diagnostic attachments now expose all categories together. No errors are filtered.

The data backend now returns HTTP 200 with an empty array from fixed GET `/agents.json`, before the upstream mount. This matches the active Workspace connection validator and the other agent-list consumer. It truthfully advertises no configured agents; Anthropic implementation remains in its separate spec. No provider call, extra packaged asset, readiness change or frontend change is introduced.

The new regression failed before the change (eight existing cases passed); all nine runtime cases pass afterward. It checks the exact empty response, no provider transport and unchanged upstream OpenAPI. Production size is 52 physical lines, 26 logical units and largest function 11. App SHA-256: `62ce001bef504053736e098f8968c8211eb37cf2cf961ef614ffee2c7d06fb71`; test SHA-256: `ad227cd5a223897fd7bb8cb9f4d068dbe359b15e2897b303fd48b34226af3b86`.
