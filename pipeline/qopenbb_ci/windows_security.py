"""Windows security bindings for checked private session handles."""
import ctypes as C
from ctypes import wintypes as W
import os


class PrivateStorageError(OSError):
    """Protection or path identity could not be established."""


if os.name == 'nt':
    kernel = C.WinDLL('kernel32', use_last_error=True)
    advapi = C.WinDLL('advapi32', use_last_error=True)
else:
    kernel = advapi = None


def bind(dll, name, args, result=W.BOOL):
    if dll is None:
        return None
    function = getattr(dll, name)
    function.argtypes = args
    function.restype = result
    return function


P = C.c_void_p
D = W.DWORD
class SecurityAttributes(C.Structure):
    _fields_ = [('length', D), ('descriptor', P), ('inherit', W.BOOL)]


class FileInfo(C.Structure):
    _fields_ = [('attributes', D), ('creation', W.FILETIME), ('access', W.FILETIME),
                ('write', W.FILETIME), ('volume', D), ('size_high', D),
                ('size_low', D), ('links', D), ('index_high', D), ('index_low', D)]


class AclSize(C.Structure):
    _fields_ = [('count', D), ('used', D), ('free', D)]


create_file = bind(kernel, 'CreateFileW', [W.LPCWSTR, D, D, P, D, D, W.HANDLE], W.HANDLE)
create_directory = bind(kernel, 'CreateDirectoryW', [W.LPCWSTR, P])
close = bind(kernel, 'CloseHandle', [W.HANDLE])
local_free = bind(kernel, 'LocalFree', [P], P)
file_info = bind(kernel, 'GetFileInformationByHandle', [W.HANDLE, P])
volume_info = bind(kernel, 'GetVolumeInformationByHandleW', [W.HANDLE, W.LPWSTR, D, P, P, P, W.LPWSTR, D])
final_path = bind(kernel, 'GetFinalPathNameByHandleW', [W.HANDLE, W.LPWSTR, D, D], D)
read = bind(kernel, 'ReadFile', [W.HANDLE, P, D, P, P])
write = bind(kernel, 'WriteFile', [W.HANDLE, P, D, P, P])
flush = bind(kernel, 'FlushFileBuffers', [W.HANDLE])
set_info = bind(kernel, 'SetFileInformationByHandle', [W.HANDLE, C.c_int, P, D])
open_token = bind(advapi, 'OpenProcessToken', [W.HANDLE, D, P])
current_process = bind(kernel, 'GetCurrentProcess', [], W.HANDLE)
token_info = bind(advapi, 'GetTokenInformation', [W.HANDLE, C.c_int, P, D, P])
sid_string = bind(advapi, 'ConvertSidToStringSidW', [P, P])
sddl = bind(advapi, 'ConvertStringSecurityDescriptorToSecurityDescriptorW', [W.LPCWSTR, D, P, P])
get_security = bind(advapi, 'GetSecurityInfo', [W.HANDLE, C.c_int, D, P, P, P, P, P], D)
get_control = bind(advapi, 'GetSecurityDescriptorControl', [P, P, P])
acl_info = bind(advapi, 'GetAclInformation', [P, P, D, C.c_int])
get_ace = bind(advapi, 'GetAce', [P, D, P])
equal_sid = bind(advapi, 'EqualSid', [P, P])


def checked(result):
    if not result:
        raise PrivateStorageError('Windows private storage operation failed', C.get_last_error())
    return result


def user_sid():
    if kernel is None:
        raise PrivateStorageError('Windows security APIs unavailable')
    token = W.HANDLE()
    checked(open_token(current_process(), 8, C.byref(token)))
    try:
        length = D()
        token_info(token, 1, None, 0, C.byref(length))
        buffer = C.create_string_buffer(length.value)
        checked(token_info(token, 1, buffer, length, C.byref(length)))
        pointer = C.cast(buffer, C.POINTER(P))[0]
        value = P()
        checked(sid_string(pointer, C.byref(value)))
        try:
            return C.wstring_at(value)
        finally:
            local_free(value)
    finally:
        close(token)


class Protection:
    def __init__(self):
        self.sid = user_sid()
        self.pointer = P()
        checked(sddl(f'O:{self.sid}D:P(A;;FA;;;{self.sid})', 1, C.byref(self.pointer), None))
        self.attributes = SecurityAttributes(C.sizeof(SecurityAttributes), self.pointer, False)

    def close(self):
        if self.pointer:
            local_free(self.pointer)
            self.pointer = P()

    def verify(self, handle):
        flags = D()
        checked(volume_info(handle, None, 0, None, None, C.byref(flags), None, 0))
        if not flags.value & 8:
            raise PrivateStorageError('Filesystem does not support persistent ACLs')
        owner, acl, descriptor = P(), P(), P()
        result = get_security(handle, 1, 5, C.byref(owner), None, C.byref(acl), None, C.byref(descriptor))
        if result:
            raise PrivateStorageError('Cannot inspect private object protection', result)
        try:
            self._verify_descriptor(owner, acl, descriptor)
        finally:
            local_free(descriptor)

    def _verify_descriptor(self, owner, acl, descriptor):
        owner_text = P()
        checked(sid_string(owner, C.byref(owner_text)))
        try:
            if C.wstring_at(owner_text) != self.sid:
                raise PrivateStorageError('Private object owner mismatch')
        finally:
            local_free(owner_text)
        control, revision = W.WORD(), D()
        checked(get_control(descriptor, C.byref(control), C.byref(revision)))
        if not acl or not control.value & 0x1000 or not control.value & 4:
            raise PrivateStorageError('Private object needs a protected nonnull DACL')
        info = AclSize()
        checked(acl_info(acl, C.byref(info), C.sizeof(info), 2))
        if info.count != 1:
            raise PrivateStorageError('Private object must grant access only to its owner')
        ace = P()
        checked(get_ace(acl, 0, C.byref(ace)))
        header = C.string_at(ace, 8)
        mask = int.from_bytes(header[4:8], 'little')
        if header[0] != 0 or header[1] != 0 or mask != 0x1f01ff:
            raise PrivateStorageError('Private object has an unexpected or inherited ACE')
        if not equal_sid(owner, ace.value + 8):
            raise PrivateStorageError('Private object grants another principal access')
