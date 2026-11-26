# Native Workspace research story

## Selection controls

The Workspace catalog can open Commodities versus Technology through the native widget dispatcher. Each widget owns its selection and sends modeling requests through the authenticated Workspace client. A fresh catalog selection evaluates the two models. A dashboard with a saved cutoff reads its existing references and offers a manual retry for a missing one.

A one-worker headless Chromium check exercised the Workspace controls in separate light and dark browser contexts. Starting from DBC, XLK and November 13, 2026, the keyboard selected GLD and VGT and changed the date to October 13. Focus stayed on the date control while the model request was pending and after the simulated capacity error arrived. Reload restored all three choices from the serialized story configuration.

The browser harness used the native dispatcher, controller, design-system controls and Workspace CSS. It supplied the widget context, authentication and modeling responses. The packaged authenticated journey is tracked in [group 4](../../../.kiro/specs/research-stories/tasks.md).

The catalog accepts the seven fields in the frozen story declaration. Tests exercise the actual connector and two vendor-cache error paths. A rejected alias cannot acquire the canonical story identity through dashboard save, template export or App artifact resolution. The pre-existing company research catalog retains its dispatch behavior.

The [accepted widget revision](https://github.com/norandom/openbb-workspace/commit/dd614f2fe3f820080eb08f1f325ecc961032daf0) passed the combined complexity gate on 237 files. Independent review passed 13 widget and catalog tests. The shell, state and modeling regression run passed 46 checks. The endpoint guard follow-up passed 24 checks.

## Financial findings and dated evidence

The story shows split-adjusted price returns, annualized realized volatility, the change in the 10-year Treasury real yield (DFII10) and the conclusion. Each chart uses the selected model run's snapshot. An analyst can change the chart type or displayed series separately for inputs and results and restore those choices on reopen.

The browser check used two saved-run fixtures. The first supplied controlled values and both DFII10 endpoints. The second replayed the previously captured November provider and model responses.

| Browser case | Observed outcome |
| --- | --- |
| Controlled DBC and XLK comparison | Returns of 20% and 10% gave a +10 percentage-point spread. DBC also had higher annualized volatility, 40% against 20%. |
| Controlled real-yield endpoints | The displayed DFII10 levels rose from 1.50% to 1.75%. The change was +0.25 percentage points. |
| November 13 captured run | DBC's +11.28 percentage-point spread over XLK remained visible. The macro view showed why the exact endpoint observations could not establish a DFII10 change by the cutoff. |
| Keyboard drill-down and reopen | Chromium opened each leg's 64 dated closes and 63 daily simple returns and both controlled macro endpoints. Chart type and series changes survived reload with reads of the saved runs. |

Both themes rendered six charts for the complete controlled case. The screenshots use synthetic financial data. [Light theme](native-story-light.png) · [Dark theme](native-story-dark.png).

Independent financial review verified the spread sign for a sub-display-precision negative result and the surviving leg when the other failed. Verification used Node 24.22.1 and isolated headless Chromium 156.0.8078.4. Group 4 promotes the source pin, builds the candidate images and exercises the packaged browser journey.

At the [group 3 Workspace revision](https://github.com/norandom/openbb-workspace/commit/3c08c76b2980ec47dd3cc1dcdd50de15e4590aa4), the joined suite passed 95 tests across 11 files, including the existing issuer-modeling and Company Documents flows. The join caught a dashboard save that consulted the connector store for ordinary widgets. Source lookup now runs only when the story serializer requests it. The two controller contract tests passed. The candidate complexity gate measured 240 files with zero errors or violations, using the [candidate inventory procedure](workspace-evidence-state.md#verification-scope). The Workspace-wide typecheck still reports baseline diagnostics.
