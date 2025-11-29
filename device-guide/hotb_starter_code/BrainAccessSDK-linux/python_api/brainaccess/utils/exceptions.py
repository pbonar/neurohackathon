import ctypes
import enum


class BrainAccessException(Exception):
    pass


def _callback() -> tuple:
    success: bool = False

    @ctypes.CFUNCTYPE(None, ctypes.c_bool, ctypes.c_void_p)
    def callback(_success: bool, user_data: ctypes.c_void_p) -> None:
        nonlocal success
        success = bool(_success)

    def get_success() -> bool:
        return success

    return callback, get_success


class _Error(enum.Enum):
    OK = 0
    CONNECTION = 1
    UNSUPPORTED_DEVICE = 2
    WRONG_VALUE = 3
    BLUETOOTH_DISABLED = 4
    BLUETOOTH_ADAPTER_NOT_FUND = 5
    ADAPTER_OUT_OF_INDEX = 6
    UPDATE_FILE_NOT_FOUND = 7
    UPDATE_INITIATED_UNSUCCESSFULLY = 8
    UPDATE_FAILED_DEVICE_DISCONNECTED = 9
    ANNOTATION_UNAVAILABLE_CALIBRATING = 10
    NO_DEVICES_FOUND = 11
    NOT_ALL_MANAGERS_CLOSED = 12
    CORE_NOT_INITIALIZED = 13
    PATH_NOT_FOUND = 14
    UNKNOWN = 0xFF


def _get_error(val) -> _Error:
    try:
        return _Error(val)
    except ValueError:
        return _Error.UNKNOWN


def _handle_error(val: int) -> bool:
    err = _get_error(val)
    if err == _Error.OK:
        return True
    elif err == _Error.CONNECTION:
        raise BrainAccessException("Connection error")
    elif err == _Error.UNSUPPORTED_DEVICE:
        raise BrainAccessException("Unsupported device")
    elif err == _Error.WRONG_VALUE:
        raise BrainAccessException("Wrong value")
    elif err == _Error.BLUETOOTH_DISABLED:
        raise BrainAccessException("Bluetooth disabled")
    elif err == _Error.BLUETOOTH_ADAPTER_NOT_FUND:
        raise BrainAccessException("Bluetooth adapter not found")
    elif err == _Error.ADAPTER_OUT_OF_INDEX:
        raise BrainAccessException("Adapter out of index")
    elif err == _Error.UPDATE_FILE_NOT_FOUND:
        raise BrainAccessException("Update file not found")
    elif err == _Error.UPDATE_INITIATED_UNSUCCESSFULLY:
        raise BrainAccessException("Update initiated unsuccessfully")
    elif err == _Error.UPDATE_FAILED_DEVICE_DISCONNECTED:
        raise BrainAccessException("Update failed device disconnected")
    elif err == _Error.ANNOTATION_UNAVAILABLE_CALIBRATING:
        print("Warning: Annotation unavailable while calibrating")
        return False
    elif err == _Error.NO_DEVICES_FOUND:
        raise BrainAccessException("No devices found")
    elif err == _Error.NOT_ALL_MANAGERS_CLOSED:
        raise BrainAccessException("Not all managers closed")
    elif err == _Error.CORE_NOT_INITIALIZED:
        raise BrainAccessException("Core not initialized")
    elif err == _Error.PATH_NOT_FOUND:
        raise BrainAccessException("Path not found")
    else:
        raise BrainAccessException("Unknown error")


class _ErrorBacore(enum.Enum):
    OK = 0
    CONFIG_TYPE = 1
    WRONG_ADAPTER_VALUE = 2
    INCOMPATIBLE_VERSION = 3
    NOT_ENALBLED = 4
    NOT_FOUND = 5
    CONFIG_PARSE = 6
    INIT_ALREADY_INITIALIZED = 7
    INVALID_FILE_PATH = 8
    UNKNOWN = 0xFF


def _get_error_bacore(val) -> _ErrorBacore:
    try:
        return _ErrorBacore(val)
    except ValueError:
        return _ErrorBacore.UNKNOWN


def _handle_error_bacore(val: int) -> bool:
    err = _get_error_bacore(val)
    if err == _ErrorBacore.OK:
        return True
    elif err == _ErrorBacore.CONFIG_TYPE:
        raise BrainAccessException(
            "Configuration file contains a value of the wrong type"
        )
    elif err == _ErrorBacore.WRONG_ADAPTER_VALUE:
        raise BrainAccessException("Bluetooth adapter value is wrong")
    elif err == _ErrorBacore.INCOMPATIBLE_VERSION:
        raise BrainAccessException("Incompatible BrainAccess version")
    elif err == _ErrorBacore.NOT_ENALBLED:
        raise BrainAccessException("Bluetooth not enabled")
    elif err == _ErrorBacore.NOT_FOUND:
        raise BrainAccessException("Bluetooth adapter not found")
    elif err == _ErrorBacore.CONFIG_PARSE:
        raise BrainAccessException("Error parsing configuration file")
    elif err == _ErrorBacore.INIT_ALREADY_INITIALIZED:
        raise BrainAccessException("Library already initialized")
    elif err == _ErrorBacore.INVALID_FILE_PATH:
        raise BrainAccessException("Invalid file path")
    else:
        raise BrainAccessException("Unknown error")
