"""Assemble the owned monorepo using upstream packaging layout without ignore rules."""
import dagger
import hashlib
import json
from dagger import dag
from qopenbb.dockerfile import remote_assets


async def workspace_image(source: dagger.Directory, release: str) -> dagger.Container:
    original = await source.file('lite/Dockerfile').contents()
    translated, assets = remote_assets(original)
    context = (dag.directory()
               .with_directory('/', source.directory('lite'))
               .with_directory('/lite', source.directory('lite'))
               .with_directory('/terminalpro', source.directory('terminalpro'))
               .with_directory('/backend', source.directory('backend-api/backend'))
               .with_file('/LICENSE', source.file('LICENSE'))
               .with_file('/NOTICE', source.file('NOTICE')))
    # Input filtering already protected retained application state-module namespaces.
    context = context.without_file('.dockerignore')
    context = context.with_new_file('/Dockerfile', translated)
    for asset in assets:
        context = context.with_file(asset['path'], dag.http(
            asset['url'], checksum='sha256:' + asset['digest']))
    image = context.docker_build(
        dockerfile='Dockerfile', platform=dagger.Platform('linux/amd64'),
        build_args=[dagger.BuildArg(name='OPENBB_IMAGE_VARIANT', value='full'),
                    dagger.BuildArg(name='VITE_RELEASE_VERSION', value=release)])
    for name, text in [('source', original), ('derived', translated)]:
        image = image.with_label('org.qopenbb.dockerfile.' + name + '.sha256',
                                hashlib.sha256(text.encode()).hexdigest())
    return image.with_label('org.qopenbb.build-assets', json.dumps(assets, sort_keys=True))
