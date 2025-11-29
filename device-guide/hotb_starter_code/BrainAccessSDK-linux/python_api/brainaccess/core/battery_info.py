import ctypes


class BatteryInfo(ctypes.Structure):
    """Provides essential information about the device's battery status.

    This class includes the current charge level, whether a charger is connected,
    and if the battery is actively charging. This is useful for monitoring the
    device's power state and ensuring it remains operational during data
    acquisition.

    Attributes
    ----------
    level : int
        The battery charge percentage, ranging from 0 to 100.
    is_charger_connected : bool
        True if a charger is connected to the device, False otherwise.
    is_charging : bool
        True if the battery is currently charging, False otherwise.
    """
    _fields_ = [
        ("level", ctypes.c_uint8),
        ("is_charger_connected", ctypes.c_bool),
        ("is_charging", ctypes.c_bool),
    ]
