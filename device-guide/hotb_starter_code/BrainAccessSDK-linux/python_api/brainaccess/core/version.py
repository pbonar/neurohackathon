import ctypes
from brainaccess.core import _dll


class Version(ctypes.Structure):
    """Represents a version number with major, minor, and patch components.

    This class is used to represent software and hardware versions in a structured
    way, following the principles of semantic versioning.

    Attributes
    ----------
    major : int
        The major version number, incremented for incompatible API changes.
    minor : int
        The minor version number, incremented for new, backward-compatible
        functionality.
    patch : int
        The patch version number, incremented for backward-compatible bug fixes.
    """

    _fields_ = [
        ("major", ctypes.c_uint8),
        ("minor", ctypes.c_uint8),
        ("patch", ctypes.c_uint8),
    ]

    def __init__(self, major, minor, patch):
        self.major = major
        self.minor = minor
        self.patch = patch

    def __repr__(self):
        return "{0}.{1}.{2}".format(self.major, self.minor, self.patch)


_dll.ba_is_version_compatible.argtypes = [
    ctypes.POINTER(Version),
    ctypes.POINTER(Version),
]
_dll.ba_is_version_compatible.restype = ctypes.c_bool


def is_version_compatible(expected: Version, actual: Version) -> bool:
    """Checks if two versions are compatible.

    Compatibility is determined based on the major version number. Two versions
    are considered compatible if they share the same major version.

    Parameters
    ----------
    expected : Version
        The expected or required version.
    actual : Version
        The actual version to check.

    Returns
    -------
    bool
        True if the versions are compatible, False otherwise.
    """
    return _dll.ba_is_version_compatible(
        ctypes.pointer(expected), ctypes.pointer(actual)
    )
