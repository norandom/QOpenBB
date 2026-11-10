# Native Compose startup

Task 5 passed independent Astra review on 2026-11-10. It starts the published Workspace/data API pair through native Podman and Docker Compose. The owned session reached `ready` at a loopback origin. Both services were healthy; data readiness, Workspace health, Full same-origin configuration and disposable login passed. The sentinel written on Windows was read through the container's `/data` bind mount.

The pair uses the accepted alpha's immutable manifests: Workspace `6dd6fc83cb46248fdc2e62e582547c3efd25e152640ce931e6bba873d6706ea1` and data API `51f28fb741431767dac2385b13ca15faafec3885e7b08af55591cce073e42232`. Their inspected local configuration IDs are `d44b08c0e7e16d35a1ed498332a0f8a19a1b491df4ad184e3d3f1fc2c4705450` and `8501c9118a8919aca81cc50c3e65a18dadfc5b82fbdba5f366c7c556a078cf57`. No application rebuild or provider request was performed.

Protected prepared state and configuration hashes precede resource creation. Effective configuration must contain exactly the two images, one loopback Workspace port, an owned network and the intended bind mount. It rejects builds, inherited public ports, extra mounts and unexpected services. Startup failures retain an allowlisted stage/code without copying arbitrary command or service output into public diagnostics.

Independent read-only inspection verified the actual descriptor, selected daemon, configuration hashes, exact container/network IDs and ownership labels, image IDs, health, port isolation, mount identity and host/container sentinel. It performed no extra login or resource creation. Focused Compose/descriptor checks passed 61 cases. The combined size gate passed for 92 maintained controller files with no errors or violations.

The real run exposed and repaired Podman's bare image-ID/lowercase network-field differences; the separately reviewed native endpoint correction provides Compose's local pipe. Earlier provider failures created no containers or networks. The successful session remains available for task 6's recreation/cleanup checks; this record does not claim those behaviors or application browser acceptance.

Raw records remain under `D:/BuildArtifacts/QOpenBB/compose-native`: `approved-images.json`, `startup-public.json`, `focused-tests.txt`, `combined.json` and `review/readonly.json`. Private descriptors and command diagnostics are excluded from publication. The maintained override lives in `pipeline/compose.runtime.yaml` so it receives production-size checks rather than a test exclusion.
