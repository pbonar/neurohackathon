import ctypes
from enum import Enum
from brainaccess.core import _dll


class GainMode(Enum):
    """Enumeration of the available gain modes for the device's amplifiers.

    The gain mode determines the amplification factor applied to the analog
    signal before it is digitized. Higher gain values are suitable for measuring
    low-amplitude signals, while lower gain values are better for signals with
    a larger dynamic range.

    Attributes
    ----------
    X1 : int
        1x gain.
    X2 : int
        2x gain.
    X4 : int
        4x gain.
    X6 : int
        6x gain.
    X8 : int
        8x gain.
    X12 : int
        12x gain.
    UNKNOWN : int
        An unknown or unsupported gain mode.
    """

    X1 = 0
    X2 = 1
    X4 = 2
    X6 = 3
    X8 = 4
    X12 = 5
    UNKNOWN = 0xFF


_dll.ba_gain_mode_to_multiplier.argtypes = [ctypes.c_uint8]
_dll.ba_gain_mode_to_multiplier.restype = ctypes.c_int


def gain_mode_to_multiplier(gain_mode: GainMode) -> int:
    """Converts a `GainMode` enum member to its integer multiplier.

    Parameters
    ----------
    gain_mode : GainMode
        The gain mode to convert.

    Returns
    -------
    int
        The integer multiplier corresponding to the gain mode (e.g., `GainMode.X12` returns 12).
    """
    return _dll.ba_gain_mode_to_multiplier(ctypes.c_uint8(gain_mode.value))


_dll.ba_multiplier_to_gain_mode.argtypes = [ctypes.c_int]
_dll.ba_multiplier_to_gain_mode.restype = ctypes.c_uint8


def multiplier_to_gain_mode(multiplier: int) -> GainMode:
    """Converts an integer multiplier to its corresponding `GainMode` enum member.

    Parameters
    ----------
    multiplier : int
        The integer multiplier to convert.

    Returns
    -------
    GainMode
        The `GainMode` enum member corresponding to the multiplier.
    """
    return GainMode(_dll.ba_multiplier_to_gain_mode(ctypes.c_int(multiplier)))
