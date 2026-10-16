"""Dagger image builds only; the caller uploads an already filtered directory."""

import json
import hashlib
import re

import dagger
from dagger import dag


def build(service: str, context: dagger.Directory, base: str, provenance: dict) -> dagger.Container:
    if service != 'foundation-smoke' or provenance['service'] != service:
        raise ValueError('only the foundation smoke build is implemented')
    if not re.fullmatch(r'.+@sha256:[0-9a-f]{64}', base):
        raise ValueError('digest-pinned base image required')
    image = (dag.container(platform=dagger.Platform('linux/amd64')).from_(base)
             .with_directory('/qopenbb-foundation', context)
             .with_entrypoint(['python', '/qopenbb-foundation/smoke.py'])
             .with_label('org.qopenbb.service', service)
             .with_label('org.qopenbb.scope', 'foundation-only'))
    for source, identity in sorted(provenance['sources'].items()):
        image = image.with_label('org.qopenbb.source.' + source, identity['revision'])
        image = image.with_label('org.qopenbb.repository.' + source, identity['repository'])
    digest = hashlib.sha256((json.dumps(provenance, sort_keys=True) + '\n').encode()).hexdigest()
    return image.with_label('org.qopenbb.provenance.sha256', digest)
