"""Dagger image builds only; the caller uploads an already filtered directory."""

import json
import hashlib
import re

import dagger
from dagger import dag


async def build(service: str, context: dagger.Directory, base: str, provenance: dict) -> dagger.Container:
    if service not in {'foundation-smoke', 'workspace', 'data-api'} or provenance['service'] != service:
        raise ValueError('unsupported service or mismatched provenance')
    if not re.fullmatch(r'.+@sha256:[0-9a-f]{64}', base):
        raise ValueError('digest-pinned base image required')
    image = (dag.container(platform=dagger.Platform('linux/amd64')).from_(base)
             .with_directory('/qopenbb-foundation', context)
             .with_entrypoint(['python', '/qopenbb-foundation/smoke.py'])
             .with_label('org.qopenbb.service', service)
             .with_label('org.qopenbb.scope', 'foundation-only'))
    if service == 'workspace':
        from qopenbb.workspace import workspace_image
        image = await workspace_image(context.directory('sources/workspace'), provenance['release_version'])
        image = image.with_label('org.qopenbb.service', service).with_label('org.qopenbb.scope', 'provisional-full')
        image = image.with_label('org.qopenbb.release', provenance['release_version'])
    if service == 'data-api':
        from qopenbb.data_api import data_image
        image = await data_image(context, base, provenance['runtime_inputs'])
        image = image.with_label('org.qopenbb.service', service).with_label('org.qopenbb.scope', 'data-runtime')
    for source, identity in sorted(provenance['sources'].items()):
        image = image.with_label('org.qopenbb.source.' + source, identity['revision'])
        image = image.with_label('org.qopenbb.repository.' + source, identity['repository'])
    digest = hashlib.sha256((json.dumps(provenance, sort_keys=True) + '\n').encode()).hexdigest()
    return image.with_label('org.qopenbb.provenance.sha256', digest)
