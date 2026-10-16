"""Translate checksum-pinned HTTP ADD for the locked Dagger Dockerfile frontend."""
import re


REMOTE = re.compile(r'^ADD (?:--chmod=(?P<mode>[0-7]{3,4}) )?--checksum=sha256:(?P<digest>[0-9a-f]{64}) (?P<url>https://\S+) (?P<target>/\S+)$')


def remote_assets(content: str) -> tuple[str, list[dict]]:
    lines, assets = [], []
    for line in content.splitlines():
        if re.match(r'^\s*ADD\b', line, re.IGNORECASE):
            match = REMOTE.fullmatch(line)
            if not match:
                raise ValueError('unsupported ADD syntax; checksum enforcement required')
            entry = match.groupdict()
            entry['path'] = '.qopenbb-build-assets/' + entry['digest']
            assets.append(entry)
            mode = '--chmod=' + entry['mode'] + ' ' if entry['mode'] else ''
            lines.append('COPY ' + mode + entry['path'] + ' ' + entry['target'])
        else:
            lines.append(line)
    return '\n'.join(lines) + '\n', assets
