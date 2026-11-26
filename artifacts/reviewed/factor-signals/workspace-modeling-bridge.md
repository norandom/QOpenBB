# Authenticated Workspace modeling bridge

Financial-modeling task 10 connects seven Workspace routes to the private modeling API. QOpenBB baseline `faeb6fa` advances the existing Workspace integration pin to `cf344880760633fec13ce83d49ecad1a3ab17a86`. The same seven changed files have identical contents on Workspace main at `9cf2e7ac3f3f0eb7ae88bf34d377e8e89d5fcd6d`.

The locked Workspace backend on Python 3.13.15 passed all 15 bridge cases. These exercised native session authentication and renewal, revocation, signing-key rotation, forwarding and failure handling. The cross-service test used the registered Workspace app, SQLite sessions and separate modeling processes. Two users each saved an evaluation under their authenticated UUID. The owner reopened a verified 5% free cash flow yield. Cross-owner requests returned 404.

All eight origin-routing cases passed using native Docker with Workspace image `sha256:c2e9869c5756b689069dfaaac9c53bc17e876d4e2edd1619533ed96927c99fd9`. Nginx forwarded modeling to Workspace, preserved the provider routes and returned 404 at the provider-side modeling path. The isolated cross-service harness relays ASGI requests over subprocess pipes. Browser widget binding and release packaging remain subsequent tasks.

Independent implementation review approved the frozen bridge. Physical lines, logical units and largest callable measured 288/134/22 for the router, 41/19/11 for signing, 375/155/16 for app registration and 64/31/22 for request logging. All fit the 400/300/50 budgets.
