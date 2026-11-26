# Native Workspace research story

## Selection controls

The Workspace catalog can open Commodities versus Technology through the native widget dispatcher. Each widget owns its selection and sends modeling requests through the authenticated Workspace client. A fresh catalog selection evaluates the two models. A dashboard with a saved cutoff reads its existing references and offers a manual retry for a missing one.

A one-worker headless Chromium check exercised the Workspace controls in separate light and dark browser contexts. Starting from DBC, XLK and November 13, 2026, the keyboard selected GLD and VGT and changed the date to October 13. Focus stayed on the date control while the model request was pending and after the simulated capacity error arrived. Reload restored all three choices from the serialized story configuration.

The browser harness used the native dispatcher, controller, design-system controls and Workspace CSS. It supplied the widget context, authentication and modeling responses. The packaged authenticated journey is tracked in [group 4](../../../.kiro/specs/research-stories/tasks.md).

The catalog accepts the seven fields in the frozen story declaration. Tests exercise the actual connector and two vendor-cache error paths. A rejected alias cannot acquire the canonical story identity through dashboard save, template export or App artifact resolution. The pre-existing company research catalog retains its dispatch behavior.

The [accepted widget revision](https://github.com/norandom/openbb-workspace/commit/dd614f2fe3f820080eb08f1f325ecc961032daf0) passed the combined complexity gate on 237 files. Independent review passed 13 widget and catalog tests. The shell, state and modeling regression run passed 46 checks. The endpoint guard follow-up passed 24 checks.
