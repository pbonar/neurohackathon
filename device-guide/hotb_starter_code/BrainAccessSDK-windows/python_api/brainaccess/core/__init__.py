"""Main entry point for the BrainAccess Core Python API.

This module provides a high-level interface to the BrainAccess Core library,
allowing for device discovery, connection, and data streaming.
"""

import ctypes
import os
from typing import Any, Dict
from pathlib import Path
from brainaccess.utils.exceptions import _handle_error_bacore
from brainaccess.utils.exceptions import BrainAccessException
from brainaccess.core.log_level import LogLevel
from brainaccess.libload import load_library
from brainaccess.core.ble_device import BaBleDevice
from brainaccess.core.sBacore_config_t import BacoreConfig

_dll = load_library("bacore")

from brainaccess.core.version import Version  # noqa: E402

# init()
_dll.ba_core_init.argtypes = []
_dll.ba_core_init.restype = ctypes.c_uint8
# ba_core_get_config()
_dll.ba_core_get_config.argtypes = [ctypes.POINTER(BacoreConfig)]
_dll.ba_core_get_config.restype = ctypes.c_uint8
# ba_core_set_config()
_dll.ba_core_set_config.argtypes = [ctypes.POINTER(BacoreConfig)]
_dll.ba_core_set_config.restype = ctypes.c_uint8
# close()
_dll.ba_core_close.argtypes = []
_dll.ba_core_close.restype = None
# get_version()
_dll.ba_core_get_version.argtypes = []
_dll.ba_core_get_version.restype = ctypes.POINTER(Version)
# scan()
_dll.ba_core_scan.argtypes = [
    ctypes.POINTER(ctypes.POINTER(BaBleDevice)),
    ctypes.POINTER(ctypes.c_size_t),
]
_dll.ba_core_scan.restype = ctypes.c_uint8


def init() -> bool:
    """Initializes the BrainAccess Core library.

    This function sets up the necessary resources for the library to function,
    including reading the configuration file and initializing the logging system.

    Returns
    -------
    bool
        Returns True on successful initialization.

    Raises
    ------
    BrainAccessException
        If the library fails to initialize. This can happen if the configuration
        is invalid or if system resources cannot be allocated.

    Warning
    -------
    This function must be called once before any other function in the
    BrainAccess Core library. Calling it more than once or failing to call it
    will result in undefined behavior.
    """
    return _handle_error_bacore(_dll.ba_core_init())


def close() -> None:
    """Closes the library and releases all underlying resources.

    This function should be called when the application is finished with the
    BrainAccess Core library to ensure a clean shutdown.

    Warning
    -------
    - Must be called after all other BrainAccess Core library functions.
    - Only call this function once.
    - Do not call this function if `init()` failed.
    """
    _dll.ba_core_close()


def get_version() -> Version:
    """Retrieves the version of the installed BrainAccess Core library.

    Returns
    -------
    Version
        An object containing the major, minor, and patch version numbers.
    """
    return _dll.ba_core_get_version()[0]


def scan() -> list[BaBleDevice]:
    """Performs a Bluetooth scan to discover nearby BrainAccess devices.

    The scan duration is fixed. This function will block until the scan is

    complete.

    Returns
    -------
    list[BaBleDevice]
        A list of `BaBleDevice` objects, each representing a discovered device.
        Returns an empty list if no devices are found.

    Raises
    ------
    BrainAccessException
        If the scan fails to start, which can happen if Bluetooth is disabled
        or if there are issues with the Bluetooth adapter.
    """
    list_size = ctypes.c_size_t()
    device_list_ptr = ctypes.POINTER(BaBleDevice)()
    _handle_error_bacore(
        _dll.ba_core_scan(ctypes.pointer(device_list_ptr),
                          ctypes.pointer(list_size))
    )
    return device_list_ptr[: list_size.value]


_MAX_CSTR = 200  # includes terminating NUL in C


def _to_cstr_200(s: str) -> bytes:
    b = os.fsencode(s)
    if len(b) >= _MAX_CSTR:  # must leave room for NUL
        raise BrainAccessException(
            f"String too long ({len(b)} bytes). Max is 199 UTF-8 bytes."
        )
    return b


def _as_int_log_level(value: Any) -> int:
    # Accept IntEnum, int, etc.
    if hasattr(value, "value"):
        value = int(value.value)
    if not isinstance(value, int):
        raise BrainAccessException(
            f"log_level must be int/IntEnum, got {type(value).__name__}"
        )
    return value


def _get_config() -> BacoreConfig:
    cfg = BacoreConfig()
    _handle_error_bacore(_dll.ba_core_get_config(ctypes.byref(cfg)))
    return cfg


def _set_config(cfg: BacoreConfig) -> bool:
    _handle_error_bacore(_dll.ba_core_set_config(ctypes.byref(cfg)))
    return True


def get_config() -> Dict[str, Any]:
    """
    Return current config as a Python dict
    """
    cfg = _get_config()
    fsdec = os.fsdecode
    return {
        "log_buffer_size": int(cfg.log_buffer_size),
        "log_path": fsdec(bytes(cfg.log_path).split(b"\0", 1)[0]),
        "log_level": int(cfg.log_level),
        "append_logs": bool(cfg.append_logs),
        "timestamps_enabled": bool(cfg.timestamps_enabled),
        "autoflush": bool(cfg.autoflush),
        "thread_ids_enabled": bool(cfg.thread_ids_enabled),
        "chunk_size": int(cfg.chunk_size),
        "enable_logs": bool(cfg.enable_logs),
        "update_path": fsdec(bytes(cfg.update_path).split(b"\0", 1)[0]),
        "adapter_index": int(cfg.adapter_index),
    }


def set_config_fields(**fields) -> bool:
    """
    Update one or more core configuration settings in a single call.

    This function provides a flexible way to modify the behavior of the
    BrainAccess core library. You can pass any combination of keyword
    arguments to change multiple settings at once. Fields not provided
    remain unchanged.

    Parameters
    ----------
    **fields : dict
        Supported keys and expected value types:

        - log_buffer_size : int
            Size of the log buffer in bytes (must be ≥ 0).
        - log_path : str
            Path to the log file (max 199 UTF-8 bytes).
        - log_level : int or LogLevel
            Logging verbosity level (e.g., Error, Warning, Info, Debug).
        - append_logs : bool
            Whether to append to an existing log file (True) or overwrite (False).
        - timestamps_enabled : bool
            Include timestamps in log entries if True.
        - autoflush : bool
            Flush logs to disk immediately if True; may reduce performance.
        - thread_ids_enabled : bool
            Include thread IDs in log entries if True.
        - chunk_size : int
            Number of data samples per EEG streaming chunk (must be > 0).
        - enable_logs : bool
            Master switch for logging; disables all logging if False.
        - update_path : str
            Path to the firmware update file. Must exist and be ≤199 UTF-8 bytes.
        - adapter_index : int
            Index of the Bluetooth adapter to use (0–255).

    Returns
    -------
    bool
        True if the configuration was updated successfully.

    Raises
    ------
    BrainAccessException
        If an unknown field is passed, a value has the wrong type or range,
        a string is too long, or the firmware update file does not exist.

    Examples
    --------
    Enable detailed logging and set a custom log file:

    >>> set_config_fields(
    ...     log_level=LogLevel.DEBUG,
    ...     log_path="logs/session.log",
    ...     append_logs=False
    ... )

    """
    if not fields:
        return True

    cfg = _get_config()

    for k, v in fields.items():
        if k == "log_buffer_size":
            if not (isinstance(v, int) and v >= 0):
                raise BrainAccessException(
                    "log_buffer_size must be a non-negative int")
            cfg.log_buffer_size = v

        elif k == "log_path":
            cfg.log_path = _to_cstr_200(str(v))

        elif k == "log_level":
            cfg.log_level = _as_int_log_level(v)

        elif k == "append_logs":
            cfg.append_logs = bool(v)

        elif k == "timestamps_enabled":
            cfg.timestamps_enabled = bool(v)

        elif k == "autoflush":
            cfg.autoflush = bool(v)

        elif k == "thread_ids_enabled":
            cfg.thread_ids_enabled = bool(v)

        elif k == "chunk_size":
            if not (isinstance(v, int) and v > 0):
                raise BrainAccessException(
                    "chunk_size must be a positive int")
            cfg.chunk_size = v

        elif k == "enable_logs":
            cfg.enable_logs = bool(v)

        elif k == "update_path":
            p = Path(str(v))
            cfg.update_path = _to_cstr_200(str(p))

        elif k == "adapter_index":
            if not (isinstance(v, int) and 0 <= v <= 255):
                raise BrainAccessException(
                    "adapter_index must be in [0, 255]")
            cfg.adapter_index = ctypes.c_uint8(v)

        else:
            raise BrainAccessException(f"Unknown config field: {k}")

    return _set_config(cfg)


def config_set_log_level(log_level: LogLevel) -> bool:
    """Sets the logging level for the core library.

    This controls the verbosity of the log output.

    Parameters
    ----------
    log_level : LogLevel
        The desired logging level from the `LogLevel` enum.

    Returns
    -------
    bool
        True if the log level was set successfully.

    Raises
    ------
    BrainAccessException
        If the provided `log_level` is not a valid `LogLevel` member.
    """
    return set_config_fields(log_level=log_level)


def config_set_chunk_size(chunk_size: int) -> bool:
    """Configures the size of data chunks for EEG streaming.

    This setting affects how much data is buffered before being made
    available for processing. Larger chunks can improve efficiency but
    increase latency.

    Parameters
    ----------
    chunk_size : int
        The desired number of data samples per chunk.

    Returns
    -------
    bool
        True if the chunk size was set successfully.

    Raises
    ------
    BrainAccessException
        If the provided `chunk_size` is invalid (e.g., zero, negative, or
        outside an acceptable range).
    """
    return set_config_fields(chunk_size=chunk_size)


def config_set_adapter_index(adapter_index: int) -> bool:
    """Selects the Bluetooth adapter to be used for scanning and connections.

    Parameters
    ----------
    adapter_index : int
        The zero-based index of the Bluetooth adapter to use.

    Returns
    -------
    bool
        True if the adapter was selected successfully.

    Raises
    ------
    BrainAccessException
        If the `adapter_index` is out of bounds for the number of available
        adapters.
    """
    return set_config_fields(adapter_index=adapter_index)


def config_enable_logging(enable: bool) -> bool:
    """Enables or disables the core library's internal logging.

    Parameters
    ----------
    enable : bool
        Set to True to enable logging, False to disable it.

    Returns
    -------
    bool
        True if the logging state was changed successfully.

    Raises
    ------
    BrainAccessException
        If the logging state cannot be changed.
    """
    return set_config_fields(enable_logs=bool(enable))


def set_config_path(
    file_path: str, append: bool = True, buffer_size: int = 512
) -> bool:
    """Sets the file path for the core library's log output.

    By default, logs may be disabled or go to a standard location. Use this
    function to specify a custom file for logging.

    Parameters
    ----------
    file_path : str
        The absolute or relative path to the desired log file.
    append : bool, optional
        If True (default), new logs will be appended to the file if it
        already exists. If False, the file will be overwritten.
    buffer_size : int, optional
        The size of the log buffer in bytes. A larger buffer can improve
        performance by reducing the frequency of disk writes. Defaults to 512.

    Returns
    -------
    bool
        True if the log file path was configured successfully.

    Raises
    ------
    BrainAccessException
        If the path is invalid or not writable.
    """
    return set_config_fields(
        log_path=str(file_path),
        append_logs=bool(append),
        log_buffer_size=int(buffer_size),
    )


def set_config_timestamp(enable: bool = True) -> bool:
    """Enables or disables timestamps in the log file entries.

    Parameters
    ----------
    enable : bool, optional
        True to include timestamps (default), False to omit them.

    Returns
    -------
    bool
        True if the setting was applied successfully.

    Raises
    ------
    BrainAccessException
        If the timestamp configuration fails.
    """
    return set_config_fields(timestamps_enabled=bool(enable))


def set_config_autoflush(enable: bool = True) -> bool:
    """Enables or disables automatic flushing of the log buffer.

    When autoflush is enabled, log messages are written to disk immediately.
    Disabling it can improve performance by buffering writes, but may result
    in lost log messages if the application crashes.

    Parameters
    ----------
    enable : bool, optional
        True to enable autoflush (default), False to disable it.

    Returns
    -------
    bool
        True if the setting was applied successfully.

    Raises
    ------
    BrainAccessException
        If the autoflush configuration fails.
    """
    return set_config_fields(autoflush=bool(enable))


def set_config_thread_id(enable: bool = True) -> bool:
    """Enables or disables the inclusion of thread IDs in log entries.

    This can be useful for debugging multi-threaded applications.

    Parameters
    ----------
    enable : bool, optional
        True to include the thread ID (default), False to omit it.

    Returns
    -------
    bool
        True if the setting was applied successfully.

    Raises
    ------
    BrainAccessException
        If the thread ID configuration fails.
    """
    return set_config_fields(thread_ids_enabled=bool(enable))


def set_config_update_path(file_path: str) -> bool:
    """Sets the file path for firmware update files.

    Parameters
    ----------
    file_path : str
        The path to the firmware update file.

    Returns
    -------
    bool
        True if the path was set successfully.

    Raises
    ------
    BrainAccessException
        If the path is invalid or the file does not exist.
    """
    return set_config_fields(update_path=str(file_path))


def get_config_ctypes() -> BacoreConfig:
    """Return the current configuration as a BacoreConfig ctypes struct."""
    return _get_config()
