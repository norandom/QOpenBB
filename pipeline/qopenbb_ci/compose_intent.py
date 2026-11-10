"""Protected intent distinguishes an interrupted owned replacement from tampering."""
import json
from . import session_files


NAME = 'recreation-intent.json'


def recreation_intent(descriptor):
    return {'schema_version': 1, 'session_id': descriptor.session_id,
            'origin': descriptor.origin, 'images': descriptor.images,
            'resources': descriptor.resources.model_dump(mode='json'),
            'state': descriptor.state.model_dump(mode='json'),
            'connection': descriptor.connection.model_dump(mode='json')}


def create_intent(runtime):
    payload = json.dumps(recreation_intent(runtime.descriptor)).encode()
    with session_files.PrivateDirectory.open(runtime.path.parent) as directory:
        directory.create_file(NAME, payload)


def require_intent(runtime):
    try:
        payload = session_files.read_private(runtime.path.parent / NAME)
        observed = json.loads(payload)
        expected = recreation_intent(runtime.descriptor)
        if json.dumps(observed, sort_keys=True) != json.dumps(expected, sort_keys=True):
            raise ValueError('mismatch')
    except (OSError, ValueError, TypeError, AttributeError):
        raise ValueError('Matching private recreation intent required') from None


def remove_intent(runtime):
    session_files.remove_private(runtime.path.parent / NAME)
