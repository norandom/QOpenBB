# FMP Batch A SDK admission amendment

Freeze the explicit-route admission proposal for independent architecture review before task 2.1 implements it. This addendum supersedes only the Container-only prescription in the approved [Batch A design](fmp-expansion-a-design.md#input-admission-before-native-filtering). The base design remains byte-for-byte unchanged, SHA-256 `59ca002fc71585e20edfb9dc431b35605e8f2bff2d78b8d04543f7f552cb3a7a`. Requirements 2.4, 5.4, 6.1, 6.3 and 7.3 retain their outcomes. The 26-task plan and 48-call ceiling remain unchanged. This proposal is not independent acceptance or new owner approval.

## Proven failure and chosen mechanism

At API `a965f70c164fe477ce9c99654b9be48e2f1bc9fd`, generated public methods apply exception_handler outside validate. validate_call runs before the body packs standard fields and invokes filter_inputs/Container._run. Native generated-method characterization proves omitted standard limit and explicit None become identical dictionaries, while True becomes integer1. Extra page retains membership and raw type. Existing validation formatting can expose input before Container. Container hooks alone cannot enforce raw presence, type or safe errors.

Task 1.4's native-emitter tests characterize this defect. Their passing result is not repaired admission. The following bounded mechanism is the chosen implementation proposal for task 2.1:

1. Emit explicit command-path metadata in the existing validate invocation from build_command_method_signature. Consume this private option before passing remaining options to validate_call. Preserve arbitrary_types_allowed settings, wraps and the public callable signature. No route inference from function/class names, stack, bytecode or fuzzy matching.
2. Resolve the authoritative route/model through CommandMap.commands_model and get_command, and selected original query through RegistryMap.original_models[model][provider]['query']. Read actual command/dependency descriptors and native Annotated provider dataclasses. Use provider Literal choices in their existing order, without sorting. Use Container._get_provider's existing explicit/default/credential priority resolution. HTTP still requires explicit FMP; SDK omission retains native selection.
3. Opt in only when the authoritative native-selected provider is fmp and the exact resolved original query class owns both `__qopenbb_strict_admission__ = True` and `model_config['extra'] = 'forbid'`. Test ownership through the class namespace, not inherited markers or financial annotation alone. Only the eleven intended production query classes receive the marker in this batch. Dedicated registered test classes use the same native selection and class-owned opt-in rule. Enforce the exact eleven marked production variants through native registry/discovery expected-set assertions at prerequisite gate 2.3 and final join 4.2, separately from runtime activation. No literal route/model pair membership check, parallel pair registry, runtime fixture JSON dependency or function-name inference may select admission. Route/model/query identity still comes exclusively from the native maps. Other providers and classes without their own marker retain native behavior.
4. At the selected wrapper bind raw positional/keyword inputs against inspect.signature without applying defaults. Preserve supplied membership, accepted aliases and original null/bool values in a copy. Separate controls exposed by this concrete command/dependency from selected financial parameters. Reject unsupported supplied standard/extra keys even when equal to native defaults, null/bool bounds and alias/canonical collisions. Do not require absent fields or insert query defaults. If binding cannot uniquely establish selection, do not guess the provider. Never bypass native validation or call the raw body to rescue failure.
5. Carry a context-local frame with exact Container identity, authoritative route/model/query/provider, original provider choice, ordered priority descriptor, supplied keys/raw values, invocation identity and thread/task owner. Reuse the resolved provider only for the matching generated _get_provider call. Match Container, route, choice, priorities, owner and invocation; selected-frame mismatches fail closed. Without a matching selected frame ordinary native resolution remains unchanged.
6. Set the context token before selected validation and reset it in finally on every success/failure. Nested calls install and restore their own frame. Consume a matching frame once at Container._run before configured defaults; reject reuse. Clear raw state before sync_run crosses into async work. Inherited child-task context cannot adopt a consumed frame. If selected wrapping supports an actual async callable, its lifecycle must surround await, not just coroutine creation.
7. Use raw membership to distinguish synthetic optional standard None from explicit supplied null. After configured defaults validate effective selected financial values against the same strict query class, before sync_run. Reject unsupported configured fields and invalid null/bool/range/date defaults. Preserve selected schema defaults and ISO effective dates. Keep actual controls outside query validation. Direct Fetcher transform_query validates the untouched dictionary with that selected strict class.
8. Normalize only selected input/binding/native-validation/filtering and effective-admission failures to a constant safe invalid_parameters OpenBBError (or existing equivalent). Do not include raw inputs, user-controlled keys/locations, arbitrary validator message/context, URLs or chained raw exception text. DEBUG_MODE must not restore raw exceptions. Do not remap provider entitlement/transport failures as parameter errors. Nonselected variants retain native wrappers and errors.

## Exclusive implementation ownership

Task 2.1 owns exactly these five API paths:

- `openbb_platform/core/openbb_core/app/parameter_admission.py`: authoritative selection and supplied/effective checks.
- `openbb_platform/core/openbb_core/app/static/utils/admission_context.py`: context frame, lifecycle and scoped safe input failures.
- `openbb_platform/core/openbb_core/app/static/utils/decorators.py`: selected wrapper around retained native validate_call.
- `openbb_platform/core/openbb_core/app/static/container.py`: frame consumption, effective pass and matching pinned provider reuse.
- `openbb_platform/core/openbb_core/app/static/package_builder/method_definition.py`: explicit path metadata emission only; no body/schema/parameter redesign.

Standard models, routers, ProviderInterface, RegistryMap, CommandMap, filters, Query and CommandRunner remain read-only. Root task 2.2 retains HTTP financial_query_policy/financial_policy ownership. Adapter workers retain only their frozen endpoint-local paths. Three cohesive growth Data modules are assigned now: income_statement_growth_data.py, balance_sheet_growth_data.py and cash_flow_growth_data.py beneath the FMP models directory. They own their endpoint's declarations, aliases and schema/financial annotation overrides; query/acquisition/transformation stays with its adapter. No shared declaration owner is introduced.

## Complexity review condition

The authoritative tools.quality.python_units.measure_python baseline at the API revision above is:

| File | Physical | Logical | Oversized callable baselines |
| --- | ---: | ---: | --- |
| method_definition.py | 1649 | 731 | format_params 656:5=110; add_field_custom_annotations 975:5=52; build_command_method_body 1342:5=86 |
| decorators.py | 107 | 51 | None |
| container.py | 122 | 57 | None |

No final emitter exception is approved. Its metadata-only patch must receive independent review of exact post-change physical/logical totals and the positions/metrics of the three untouched oversized callables. Any exception must record exact fork revision, expiry and review reference. Prefer no-growth changes without compressed statements; independently approve any measured final delta. Do not enter a speculative allowance in the inventory. If a bounded exception is not accepted, return for a cohesive extraction decision before implementation acceptance. All other new/modified maintained files and callables must pass 400 physical/300 logical/50 per function whole-file checks. The future ownership inventory authorizes measurement, not a cap exemption.

## Pending verification and joins

The following matrix belongs to tasks 2.1/2.3 and is pending. Task 1.4 tests only freeze descriptors, native-source facts and the known defect. No case below is certified by a descriptor assertion.

| Surface | Required cases and evidence |
| --- | --- |
| Generated SDK, all eleven dedicated variants | Keyword/positional inputs, omission versus None, True/False, unsupported standard/extra keys even at native defaults, alias collisions, required symbol; zero-I/O rejection and valid native types/defaults |
| Provider selection | Explicit FMP, omitted provider/default, native credential priority, another provider and non-opted/unregistered strict class; exactly one matching selection, original order and unchanged baseline behavior |
| Configured defaults | Valid values; invalid null/bool/range/date/unknown field; explicit invalid values that defaults would overwrite; raw rejection first, effective rejection before sync_run |
| Native controls/signatures | Concrete command/dependency controls only, chart where actually exposed, unsupported chart_params, inspect.signature, positional duplicate behavior and arbitrary_types configuration; no validation bypass |
| Safe early errors | Pre-body ValidationError, supplied-key/value sentinels, malformed list/filter choice, selected required/binding failures, DEBUG_MODE on/off; constant safe selected error without raw causes and no network calls |
| Context lifecycle | Nested same/different routes and Containers, two threads, async tasks, failures at each stage, subsequent baseline calls, inherited child contexts, actual async wrapper if supported; token restoration, owner matching and no consumed-frame reuse |
| HTTP and direct Fetcher | Repeated symbol/page, unsupported/default-valued keys, null/bool, malformed provider and untouched raw dictionaries; established HTTP422 envelope and zero extraction on rejection |
| Final native composition | After real registration, retest all eleven actual SDK/HTTP paths, schemas and OBBject metadata, plus baseline variants; fixture proof does not replace this join |
| Complexity | Explicit current fork scope, exact independently reviewed measured emitter exception if used, whole-file/helper caps and executable gate |

Task 2.1 must replace or adapt the known-defect characterization expectations once the wrapper changes; the historical 30-pass reproduction must never become acceptance of unsafe behavior. Public-entry acceptance in tasks 2.1/2.3 must use actual Container/CommandRunner descriptors and dedicated registered query variants, with native selection and no intercepted _run or suppressed selection metadata. The current generated probe is limited defect evidence.

Task 2.3 remains the acceptance gate before adapter fan-out. Tasks 4.1/4.2 still retest production registration/classes. Any schema, selection, lifecycle or control change pauses affected lanes and invalidates the affected proof. No live-call budget is consumed by this amendment.
