import ctypes


class ChargingSettings(ctypes.Structure):
    _fields_ = [
        ("_sleep_timeout", ctypes.c_int8),
        ("_enabled_on_while_charging", ctypes.c_bool),
    ]

    @property
    def sleep_timeout(self):
        """Sleep timeout in minutes.
        If the device is not used for this time it will go to sleep."""
        return self._sleep_timeout

    @property
    def enabled_on_while_charging(self):
        """ Indicates if the device is usable while charging"""
        return self._enabled_on_while_charging
