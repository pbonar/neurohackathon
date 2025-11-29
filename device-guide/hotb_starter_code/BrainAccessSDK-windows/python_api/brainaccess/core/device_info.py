import ctypes
from brainaccess.core.version import Version
from brainaccess.core.device_model import DeviceModel


class DeviceInfo(ctypes.Structure):
    """Contains detailed information about a BrainAccess device.

    This class holds static information about the device, such as its model,
    hardware and firmware versions, and serial number. This is useful for
    identifying the device and understanding its capabilities.

    Attributes
    ----------
    device_model : DeviceModel
        The model of the device.
    hardware_version : Version
        The hardware version of the device.
    firmware_version : Version
        The firmware version currently installed on the device.
    serial_number : int
        The unique serial number of the device.
    sample_per_packet : int
        The number of data samples contained in each packet sent by the device.
    """
    _fields_ = [
        ("_device_model", ctypes.c_uint8),
        ("hardware_version", Version),
        ("firmware_version", Version),
        ("serial_number", ctypes.c_size_t),
        ("sample_per_packet", ctypes.c_size_t),
    ]

    @property
    def device_model(self):
        """The model of the device."""
        return DeviceModel(self._device_model)

    @device_model.setter
    def device_model(self, val):
        self._device_model = ctypes.c_uint8(val.value)
