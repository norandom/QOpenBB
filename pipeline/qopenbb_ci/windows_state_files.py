"""Explicit bind-state policy; session and host-written files remain strict."""
import ctypes as C
from . import windows_security as api
from .windows_private_files import PrivateDirectory, _identity, _leaf, _open, READ_CONTROL


class StateDirectory(PrivateDirectory):
    root_protection_type = api.StateRootProtection

    def generated_metadata(self, name):
        """Inspect a direct inherited leaf without reading its payload."""
        self.verify()
        path = self.path / _leaf(name)
        handle = _open(path, READ_CONTROL)
        protection = api.GeneratedStateProtection()
        try:
            _identity(handle, path, False)
            protection.verify(handle)
            self.verify()
            info = api.FileInfo()
            api.checked(api.file_info(handle, C.byref(info)))
            return {'bytes': (info.size_high << 32) | info.size_low,
                    'permission_authority': 'windows-owner-only-acl'}
        finally:
            protection.close()
            api.close(handle)
