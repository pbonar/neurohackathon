import ctypes


class BacoreConfig(ctypes.Structure):
    """
    Python equivalent of the C struct `sBACORE_Config_t`.

    This structure defines configuration options for the BrainAccess system,
    including logging, data processing, and adapter selection.
    It mirrors the C layout exactly, for use in `ctypes` bindings.

    Attributes
    ----------
    log_buffer_size : ctypes.c_size_t
        Size of the log buffer in bytes.
    log_path : ctypes.c_char * 200
        Absolute/relative path to the log file (max length 200 chars).
    log_level : ctypes.c_int
        Logging verbosity level (e.g., 2 = Warning).
        Typically corresponds to a `ba_log_level` enum.
    append_logs : ctypes.c_bool
        If True, append to existing log files; if False, overwrite.
    timestamps_enabled : ctypes.c_bool
        If True, include timestamps in log entries.
    autoflush : ctypes.c_bool
        If True, automatically flush logs after every write.
    thread_ids_enabled : ctypes.c_bool
        If True, include thread IDs in log entries.
    chunk_size : ctypes.c_size_t
        Chunk size (in bytes) for internal data processing.
    enable_logs : ctypes.c_bool
        Master switch: if False, disables all logging regardless of other flags.
    update_path : ctypes.c_char * 200
        Path to the firmware update file (max length 200 chars).
    adapter_index : ctypes.c_uint8
        Index of the Bluetooth adapter to use (default = 0).
    """

    _fields_ = [
        ("log_buffer_size", ctypes.c_size_t),
        ("log_path", ctypes.c_char * 200),
        ("log_level", ctypes.c_int),
        ("append_logs", ctypes.c_bool),
        ("timestamps_enabled", ctypes.c_bool),
        ("autoflush", ctypes.c_bool),
        ("thread_ids_enabled", ctypes.c_bool),
        ("chunk_size", ctypes.c_size_t),
        ("enable_logs", ctypes.c_bool),
        ("update_path", ctypes.c_char * 200),
        ("adapter_index", ctypes.c_uint8),
    ]
