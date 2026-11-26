# Published issuer FCF yield milestone

On 2026-11-26, QOpenBB released the independent modeling package at version 0.1.0. The lightweight tag `modeling-v0.1.0` resolves to accepted product revision `5407b3f335d9de413f3d988b7a11fbc2a77e7f62`. The deployment combined the new Workspace and modeling images with the existing data API. [GitHub prerelease](https://github.com/norandom/QOpenBB/releases/tag/modeling-v0.1.0) · [Image promotion](https://github.com/norandom/QOpenBB/actions/runs/45806150772)

| GHCR package under norandom | Published manifest SHA-256 |
| --- | --- |
| qopenbb-workspace | `49748d9f90d064073187feb8bc1208e1a84d5b08c4b89ad80cea80d24e9f4b01` |
| qopenbb-modeling | `0c19913678b029794eac117a4a58512c826f4779c5e6d77dbdd7a5d5ffa80e43` |
| qopenbb-data-api | `79d46d09a913a1b6583ae823961ca87b9e4a6bb112739ca738567b131ca79a73` |

Both promoted images retained the accepted configuration digests. Their published manifests differed from the local candidate manifests. Anonymous registry requests confirmed all three published digest references. Ubuntu Compose pulled the published set, and a single isolated Playwright worker exercised it.

* **Evaluate and save.** SAP.DE displayed the independently verified 3.78554% FCF yield for the dated observations. The historical AAPL case withheld the output. Workspace saved the result and displayed its trace and assumptions.
* **Reopen.** Workspace and modeling were recreated. The data API container retained its identity. A fresh session reopened the saved result with zero evaluation requests.
* **Provider continuity.** With modeling stopped, Workspace reported the model outage and displayed the live Apple company profile from the data API.

The first published run passed evaluation and reopen, then timed out waiting for the company option. The verification harness at `3baf1aa` waits for the restored selector before measuring the profile request. A fresh run on the same images passed all three phases with zero Playwright retries. The release attachment `published-acceptance.json` records the container identities and phase-report hashes. The isolated deployment and its containers were removed after the run.

The public release contains the deterministic 20-file provider and consumer contract ZIP, the release manifest, the deployment ZIP and the published-image acceptance record. The manifest binds contract bytes to their Git source, counterpart revisions, reviewed evidence and image identities. The controller downloaded and compared all four release assets with the local originals. The sorted asset name/digest inventory has SHA-256 `8a8047337aca782a1ec1d1fdbb4e5ab7125caa1cecff5add098c3c826c6b24fb`.

The local portable suite recorded 1,759 passed, 12 skipped and one deselected. The published-image acceptance ran separately. Testing covered the disposable Ubuntu host. Owner-server deployment and acceptance remain separate work.

The local change-impact gate passed all 97 selected checks on verification revision `3baf1aa` and classified the saved-output contract as compatible. An earlier local run reported failures in installed-factor HTTP cases. All nine cases passed in isolation before the full successful repeat. The hosted portable and contract gates passed on the same revision. [Hosted checks](https://github.com/norandom/QOpenBB/actions/runs/45808067047) · [Release finalization](https://github.com/norandom/QOpenBB/actions/runs/45809214013)
