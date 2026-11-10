# Dagger SDK launch-path repair review

Decision: accept this bounded repair for a corrected publication attempt. No blocking findings in the five-file diff against root 885b97c. This decision does not accept task 7 publication; its tagged release, public image identity, installed catalog and portable Linux gates remain required.

The failed workflow 42876893136 reported missing dagger-io metadata because resolving the Linux virtual-environment Python symlink selected the base interpreter. The resolver now validates the resolved target with its existing file/wrapper/platform checks, then optionally returns the absolute original launch path. Default container/compose tool resolution remains unchanged. Both SDK entry points opt in: native_actions.build passes the launch path to image_cli, and image_cli.export uses it for both the metadata probe and Dagger-run Python command. Existing fail-closed SDK version validation remains present.

Independent review examined container_command.py, image_cli.py, native_actions.py and the two delivery-test diffs. The export regression asserts identical retained launch paths for probe and runner; native action coverage requires the preservation option. The POSIX regression creates a real symlinked virtual environment without pip, supplies synthetic dagger-io distribution metadata inside that environment, and verifies its prefix and metadata through the selected interpreter. Synthetic metadata proves interpreter environment selection; it does not prove an installed real SDK can build an image.

Fresh independent Linux evidence: native C:/Program Files/RedHat/Podman/podman.exe ran the loaded API image sha256:9b1649810b0d83500f5bb1219adcb6aed8eeb6e674163f1b1d72f6d0f98f63e0 with --rm --pull=never --network=none --read-only --tmpfs /tmp:rw,size=64m --workdir /tmp --entrypoint python. Only the actual changed resolver and sdk_linux_regression.py were mounted read-only under /review. The harness extracts the actual test function via Python AST, removes its pytest skip decorator and supplies standard-library setup; no installed pytest or source package is required. Command tail: -I -B /review/sdk_linux_regression.py. Exit 0; PASS actual Linux symlinked venv metadata test, CPython 3.13.15. See sdk-linux.log and sdk_linux_regression.py beside this report. Dependencies and virtual-environment temporary files remained in the container Linux tmpfs; no network, installation, WSL, image build or live provider was used.

Whole-file independent project-syntax-units-v1 measurements are recorded with source SHA-256 in sdk-review-caps.json:

| Production file | Physical | Logical | Largest callable |
| --- | ---: | ---: | ---: |
| container_command.py | 38 | 30 | 10 |
| image_cli.py | 218 | 167 | 28 |
| native_actions.py | 104 | 70 | 19 |

All pass the 400/300/50 caps. Tests are excluded by policy. The controller's corrected combined gate sdk-complexity-corrected.json passed with errors=[] and violations=[] after explicitly copying current production files to its clean checker root. sdk-complexity.json used stale source and is not evidence.

The implementer/controller report the focused native delivery selection passed 170 tests with 4 skips in 89.56 seconds, followed by 2 final focused tests passing. That native suite is attributed evidence, not independently rerun here; the POSIX test skipped on native Windows was executed independently in Linux as described above. The unrelated dirty renderer/catalog/inventory work was not modified or accepted by this review. Preserve this boundary during selective staging.