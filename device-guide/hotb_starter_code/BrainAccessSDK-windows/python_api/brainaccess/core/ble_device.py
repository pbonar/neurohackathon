import ctypes


class BaBleDevice(ctypes.Structure):
    """Represents a Bluetooth Low Energy (BLE) device found during a scan.

    This class stores the device's name and MAC address, which are essential
    for identifying and connecting to a specific BrainAccess device.

    Attributes
    ----------
    name : str
        The broadcasted name of the BLE device.
    mac_address : str
        The unique MAC address of the BLE device.
    """

    _fields_ = [
        ("_name", ctypes.c_char_p),
        ("_mac_address", ctypes.c_char_p),
    ]

    @property
    def name(self) -> str:
        """The human-readable name of the device."""
        return self._name.decode("utf-8")

    @property
    def mac_address(self) -> str:
        """The MAC address of the device, used for connection."""
        return self._mac_address.decode("utf-8")
