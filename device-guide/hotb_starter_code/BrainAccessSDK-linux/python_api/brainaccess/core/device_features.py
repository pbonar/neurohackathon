import ctypes

from brainaccess.core import _dll
from brainaccess.core.device_info import DeviceInfo
from brainaccess.utils.exceptions import BrainAccessException

# has_gyro()
_dll.ba_core_device_features_has_gyro.argtypes = [ctypes.c_void_p]
_dll.ba_core_device_features_has_gyro.restype = ctypes.c_bool

# has_accel()
_dll.ba_core_device_features_has_accel.argtypes = [ctypes.c_void_p]

_dll.ba_core_device_features_has_accel.restype = ctypes.c_bool

# is_bipolar()
_dll.ba_core_device_features_is_bipolar.argtypes = [ctypes.c_void_p]
_dll.ba_core_device_features_is_bipolar.restype = ctypes.c_bool

# electrode_count()
_dll.ba_core_device_features_electrode_count.argtypes = [ctypes.c_void_p]
_dll.ba_core_device_features_electrode_count.restype = ctypes.c_uint8

# device_features_get()
_dll.ba_core_device_features_get.argtypes = [ctypes.POINTER(DeviceInfo)]
_dll.ba_core_device_features_get.restype = ctypes.c_void_p


class DeviceFeatures:
    """Provides an interface to query the supported features of a device.

    This class allows you to check for the presence of sensors like gyroscopes
    and accelerometers, determine the electrode configuration, and get the total
    number of electrodes available on the device.

    Parameters
    ----------
    device_info : DeviceInfo
        An object containing the device's information, used to identify the
        specific model and its capabilities.

    Raises
    ------
    BrainAccessException
        If the device is not recognized or its features cannot be retrieved.
    """

    def __init__(self, device_info):
        self.handle = _dll.ba_core_device_features_get(ctypes.pointer(device_info))
        if self.handle is None:
            raise BrainAccessException("Unknown device")

    def has_gyro(self) -> bool:
        """Checks if the device is equipped with a gyroscope.

        Returns
        -------
        bool
            True if the device has a gyroscope, False otherwise.
        """
        return _dll.ba_core_device_features_has_gyro(self.handle)

    def has_accel(self) -> bool:
        """Checks if the device is equipped with an accelerometer.

        Returns
        -------
        bool
            True if the device has an accelerometer, False otherwise.
        """
        return _dll.ba_core_device_features_has_accel(self.handle)

    def is_bipolar(self) -> bool:
        """Checks if the device uses bipolar electrodes.

        Bipolar electrodes have distinct positive (P) and negative (N) contacts,
        which is important for certain types of measurements.

        Returns
        -------
        bool
            True if the electrodes are bipolar, False otherwise.
        """
        return _dll.ba_core_device_features_is_bipolar(self.handle)

    def electrode_count(self) -> int:
        """Gets the total number of EEG/EMG electrodes on the device.

        Returns
        -------
        int
            The number of electrodes available for data acquisition.
        """
        return _dll.ba_core_device_features_electrode_count(self.handle)
