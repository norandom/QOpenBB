# Login password correction application review

## LP3: APPROVED

Independent read-only review of the final `env-update/result.json`, `verify.py`, corrected `continue.py`, bootstrap chain and storage types supports the bounded existing-account replacement claim. The controller reports continuation exit 0; retained evidence reports PASS.

The disposable Compose run uses published Workspace digest `d8414d603b9a7bd369650fbaacf71e3271367fe3e9bd6b1be02970289aeab713` and data API digest `9c46ea9954835acdc6b233cd99c6c0e5bcf918d46b6823bde9b9f4820178b6f0`. The Compose source matches the root definition, with isolated loopback port and private bind state. Literal dollar characters survive the private environment file.

Before and after editing the nonempty administrator password and force-recreating Workspace, strict read-only SQLite assertions match the same account UUID and synthetic DashboardItem UUID, decompressed content, owner and creator. The new credential authenticates with HTTP 200; the previous credential fails with HTTP 401. The owned containers were cleaned up without deleting retained state.

The first backend-import probe exited 139. Its displayed `PRO_TRIAL_USER` value is the application's stdout redaction of the actual UUID, not an identity assertion. The corrected continuation avoids backend imports, parses the real private UUID marker, normalizes SQLite UUID encodings, decompresses the stored content and compares actual values. This resolves the evidence defect without treating the earlier partial run as success.

This proves same-email bootstrap password replacement and retained synthetic database content. It does not prove UI dashboard save/reopen, a weak-password login on the old published image, or the owner's deployment.

Reviewed SHA256 identities:

- `env-update/continue.py`: `71212B5CFA0F9989ABC5E4ECB205387EA87E30E9D28833BD4D03CDCF342F3554`
- `env-update/result.json`: `3E8CB0813ADD7CFCC23AA1C6F844721D7A5C2861E7DEE90D33F08034EB39E758`

## LP4: APPROVED for the bounded configured candidate

The controller's successful Dagger build and executed headless verification identify Workspace image `sha256:9a0854a4720c099f333c4f597b594c5b327dacabdb7229590eade6015c18d358`, root `eb0b18b`, and Workspace fork `22180d8ec206e088a384f2a3c7345358b1832c7c`. The reviewer read the final verifier and retained run-1/run-2 evidence without repeating runtime work. The reviewer prepared the harness; the controller reviewed it, corrected its error-text expectation, and executed the candidate test.

Run-2 reports PASS at `complete`; controller reports exit 0. Actual browser submission preserved the weak existing password exactly, received HTTP 200 and a token, displayed authenticated Workspace tabs, and accessed the protected current-user endpoint. A wrong password was rejected and displayed the native login error. Backend requests rejected a weak new password with 422 and an incorrect current password with 401. The correct weak current password authorized a strong replacement with 200; the previous password then failed and the new password produced an authorized session. No production delta followed the reviewed fork revision.

All retained diagnostics are clean: page errors, console errors, CDP exceptions and non-network CDP errors are zero; failed requests and unexpected HTTP responses are empty. Expected negative-authentication responses are bounded exceptions, not ignored arbitrary console errors. The run used an isolated headless context, a fresh 65-second login window and four login attempts, without authentication traces, screenshots, credentials or token exports.

The first run stopped because the harness expected the 404 error text while the actual 401 path displays `Invalid login credentials.` Wrong-password rejection and clean diagnostics had already passed. The controller corrected only the expectation to cover the two native messages and restarted after a fresh rate window; this was a test expectation defect, not a production fix.

The packaged configuration explicitly sets `allowForgotPassword=false`, and the reset route redirects accordingly. The disabled reset form's warnings were **not browser-tested**. Preserved new-password validators and the existing 76-case frontend policy suite supply source evidence; actual backend new-password rejection supplies runtime evidence. This is sufficient for the bounded enabled login/current-password correction, with that UI limitation disclosed. No claim covers enabled reset-form rendering, the owner's deployment or the subsequently published CI image bytes.

Reviewed SHA256 identities:

- `browser/verify.mjs`: `1072E5610870D4D006123215618882DBAE26188D30D6AD52C2CE9611BB348AD9`
- `browser/run-2/result.json`: `710858542A34307B45E3E5F955D13961B767386699066B7D42DA5745286F36FB`

No blocking findings remain for candidate acceptance and release-pipeline dispatch. Publication identity and delivery verification remain separate gates.
