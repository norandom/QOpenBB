# Canonical annotation names

Financial declarations and their field references always use canonical Python model field names. `Field(exclude=True)` fields are excluded from the contract. Input aliases and serialization aliases do not become annotation keys.

The native `Router.command` default is `response_model_by_alias=False` in `openbb_core/app/router.py`, lines 143-145. Existing provider metadata and normal native HTTP responses therefore agree with the canonical names. For `ev_to_ebitda = Field(alias="evToEBITDA")`, the annotation key is `ev_to_ebitda`. An alias-only key or currency/date reference fails binding. Provider input aliases remain intact.

The public `bind_query_annotation`, `bind_data_annotation` and `render_field_templates` signatures remain unchanged. The previous interface's alias-first lookup is superseded by this correction. Templates cover all emitted static model fields; dynamic fields remain additional runtime columns. Empty templates remain explicit unknowns, definitions derive from Field descriptions and rendered templates remain independent copies.

Projection separately reads the installed route's response alias flag and rejects `True` for the current supported contract. This core module introduces no serialization mode engine or registry. The rest of the accepted declaration types and policies remain unchanged.
