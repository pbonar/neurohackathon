import ctypes
import time
import warnings
import threading
import numpy as np
import copy
from multimethod import multimethod
import platform
from typing import Callable, Union, Optional, Any

from brainaccess.utils.exceptions import _callback, _handle_error, BrainAccessException
from brainaccess.core import _dll
from brainaccess.core.battery_info import BatteryInfo
from brainaccess.core.device_info import DeviceInfo
from brainaccess.core.device_model import DeviceModel
from brainaccess.core.gain_mode import GainMode
from brainaccess.core.stream_rate import StreamRate
from brainaccess.core.annotation import Annotation
from brainaccess.core.polarity import Polarity
from brainaccess.core.impedance_measurement_mode import ImpedanceMeasurementMode  # noqa
from brainaccess.core.device_features import DeviceFeatures


# ctypes
# new_eeg_manager
_dll.ba_eeg_manager_new.argtypes = []
_dll.ba_eeg_manager_new.restype = ctypes.c_void_p
# destructor
_dll.ba_eeg_manager_free.argtypes = [ctypes.c_void_p]
_dll.ba_eeg_manager_free.restype = None
# connect(device_name)
_dll.ba_eeg_manager_connect.argtypes = [
    ctypes.c_void_p,
    ctypes.c_char_p,
    ctypes.CFUNCTYPE(None, ctypes.c_bool, ctypes.c_void_p),
    ctypes.c_void_p,
]
_dll.ba_eeg_manager_connect.restype = ctypes.c_uint8
# is_connected()
_dll.ba_eeg_manager_is_connected.argtypes = [ctypes.c_void_p]
_dll.ba_eeg_manager_is_connected.restype = ctypes.c_bool
# disconnect()
_dll.ba_eeg_manager_disconnect.argtypes = [ctypes.c_void_p]
_dll.ba_eeg_manager_disconnect.restype = None
# start_stream()
_dll.ba_eeg_manager_start_stream.argtypes = [
    ctypes.c_void_p,
    ctypes.CFUNCTYPE(None, ctypes.c_void_p),
    ctypes.c_void_p,
]
_dll.ba_eeg_manager_start_stream.restype = ctypes.c_uint8
# stop_stream()
_dll.ba_eeg_manager_stop_stream.argtypes = [
    ctypes.c_void_p,
    ctypes.CFUNCTYPE(None, ctypes.c_void_p),
    ctypes.c_void_p,
]
_dll.ba_eeg_manager_stop_stream.restype = ctypes.c_uint8
# is_streaming()
_dll.ba_eeg_manager_is_streaming.argtypes = [ctypes.c_void_p]
_dll.ba_eeg_manager_is_streaming.restype = ctypes.c_bool
# load_config()
_dll.ba_eeg_manager_load_config.argtypes = [
    ctypes.c_void_p,
    ctypes.CFUNCTYPE(None, ctypes.c_void_p),
    ctypes.c_void_p,
]
_dll.ba_eeg_manager_load_config.restype = ctypes.c_uint8
# get_battery_info()
_dll.ba_eeg_manager_get_battery_info.argtypes = [
    ctypes.c_void_p,
]
_dll.ba_eeg_manager_get_battery_info.restype = BatteryInfo
# set_channel_enabled()
_dll.ba_eeg_manager_set_channel_enabled.argtypes = [
    ctypes.c_void_p,
    ctypes.c_uint16,
    ctypes.c_bool,
]
_dll.ba_eeg_manager_set_channel_enabled.restype = None
# set_channel_gain()
_dll.ba_eeg_manager_set_channel_gain.argtypes = [
    ctypes.c_void_p,
    ctypes.c_uint16,
    ctypes.c_uint8,
]
_dll.ba_eeg_manager_set_channel_gain.restype = None
# set_channel_bias()
_dll.ba_eeg_manager_set_channel_bias.argtypes = [
    ctypes.c_void_p,
    ctypes.c_uint16,
    ctypes.c_uint8,
]
_dll.ba_eeg_manager_set_channel_bias.restype = None
# set_impedance_mode()
_dll.ba_eeg_manager_set_impedance_mode.argtypes = [
    ctypes.c_void_p,
    ctypes.c_uint8,
]
_dll.ba_eeg_manager_set_impedance_mode.restype = None
# get_device_info()
_dll.ba_eeg_manager_get_device_info.argtypes = [ctypes.c_void_p]
_dll.ba_eeg_manager_get_device_info.restype = ctypes.POINTER(DeviceInfo)
# get_channel_index()
_dll.ba_eeg_manager_get_channel_index.argtypes = [ctypes.c_void_p, ctypes.c_uint16]
_dll.ba_eeg_manager_get_channel_index.restype = ctypes.c_size_t
# get_sample_frequency()
_dll.ba_eeg_manager_get_sample_frequency.argtypes = [ctypes.c_void_p]
_dll.ba_eeg_manager_get_sample_frequency.restype = ctypes.c_uint16
# set_callback_chunk()
_dll.ba_eeg_manager_set_callback_chunk.argtypes = [
    ctypes.c_void_p,
    ctypes.CFUNCTYPE(
        None,
        ctypes.POINTER(ctypes.c_void_p),
        ctypes.c_size_t,
        ctypes.c_void_p,
    ),
    ctypes.c_void_p,
]
_dll.ba_eeg_manager_set_callback_chunk.restype = None
# set_callback_battery()
_dll.ba_eeg_manager_set_callback_battery.argtypes = [
    ctypes.c_void_p,
    ctypes.CFUNCTYPE(None, ctypes.POINTER(BatteryInfo), ctypes.c_void_p),
    ctypes.c_void_p,
]
_dll.ba_eeg_manager_set_callback_battery.restype = None
# set_callback_disconnect()
_dll.ba_eeg_manager_set_callback_disconnect.argtypes = [
    ctypes.c_void_p,
    ctypes.CFUNCTYPE(None, ctypes.c_void_p),
    ctypes.c_void_p,
]
_dll.ba_eeg_manager_set_callback_disconnect.restype = None
# update firmware
_dll.ba_eeg_manager_start_update.argtypes = [
    ctypes.c_void_p,
    ctypes.CFUNCTYPE(None, ctypes.c_void_p, ctypes.c_size_t, ctypes.c_size_t),
    ctypes.c_void_p,
]
_dll.ba_eeg_manager_start_update.restype = ctypes.c_uint8
# annotate()
_dll.ba_eeg_manager_annotate.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
_dll.ba_eeg_manager_annotate.restype = ctypes.c_uint8
# get_annotations()
_dll.ba_eeg_manager_get_annotations.argtypes = [
    ctypes.c_void_p,
    ctypes.POINTER(ctypes.POINTER(Annotation)),
    ctypes.POINTER(ctypes.c_size_t),
]
_dll.ba_eeg_manager_get_annotations.restype = None
# clear_annotations()
_dll.ba_eeg_manager_clear_annotations.argtypes = [ctypes.c_void_p]
_dll.ba_eeg_manager_clear_annotations.restype = None

# Stream size type info super secret function thingy
_dll.ba_eeg_manager_get_stream_channel_data_types.argtypes = [
    ctypes.c_void_p,
    ctypes.POINTER(ctypes.POINTER(ctypes.c_uint8)),
    ctypes.POINTER(ctypes.c_size_t),
]
_dll.ba_eeg_manager_get_stream_channel_data_types.restype = None

# Set sample rate
_dll.ba_eeg_manager_set_data_stream_rate.argtypes = [
    ctypes.c_void_p,
    ctypes.c_uint8,
]
_dll.ba_eeg_manager_set_data_stream_rate.restype = ctypes.c_uint8

_managers_mtx = threading.Lock()
_managers: dict = dict()

_types_map = [
    ctypes.c_float,  # 0
    ctypes.c_uint8,  # 1
    ctypes.c_size_t,  # 2
    ctypes.c_double,  # 3
]


@ctypes.CFUNCTYPE(None, ctypes.c_void_p)
def _callback_stop_stream(data: ctypes.c_void_p) -> None:
    with _managers_mtx:
        mgr = _managers.get(data)
        if mgr is not None:
            with mgr._callback_stop_stream_mix:
                cbk = mgr._callback_stop_stream
                if cbk is not None:
                    cbk()


@ctypes.CFUNCTYPE(None, ctypes.c_void_p, ctypes.c_size_t, ctypes.c_size_t)
def _callback_ota_update(data: ctypes.c_void_p, progress: int, total: int) -> None:
    with _managers_mtx:
        mgr = _managers.get(data)
        if mgr is not None:
            with mgr._callback_ota_update_mtx:
                cbk = mgr._callback_ota_update
                if cbk is not None:
                    cbk(progress, total)


@ctypes.CFUNCTYPE(None, ctypes.c_void_p)
def _callback_start_stream(data: ctypes.c_void_p) -> None:
    with _managers_mtx:
        mgr = _managers.get(data)
        if mgr is not None:
            with mgr._callback_start_stream_mix:
                cbk = mgr._callback_start_stream
                if cbk is not None:
                    cbk()


@ctypes.CFUNCTYPE(
    None, ctypes.POINTER(ctypes.c_void_p), ctypes.c_size_t, ctypes.c_void_p
)
def _callback_chunk(chunk_data: list, chunk_size: int, data: Any) -> None:
    with _managers_mtx:
        mgr = _managers.get(data)
        if mgr is not None:
            with mgr._callback_chunk_mtx:
                cbk = mgr._callback_chunk
                if cbk is not None:
                    # Get channel sizes and type information
                    types_ptr = ctypes.POINTER(ctypes.c_uint8)()
                    types_size = ctypes.c_size_t()
                    _dll.ba_eeg_manager_get_stream_channel_data_types(
                        data, ctypes.byref(types_ptr), ctypes.byref(types_size)
                    )
                    types = [_types_map[types_ptr[i]] for i in range(types_size.value)]

                    chunk_arrays = []
                    for i, ctype in enumerate(types):
                        data_pointer = ctypes.cast(
                            chunk_data[i], ctypes.POINTER(ctype * chunk_size)
                        )
                        np_array = np.ctypeslib.as_array(
                            data_pointer.contents, shape=(chunk_size,)
                        )
                        chunk_arrays.append(np_array)

                    cbk(chunk_arrays, chunk_size)


@ctypes.CFUNCTYPE(None, ctypes.POINTER(BatteryInfo), ctypes.c_void_p)
def _callback_battery(b_info, data) -> None:
    with _managers_mtx:
        mgr = _managers.get(data)
        if mgr is not None:
            with mgr._callback_battery_mtx:
                cbk = mgr._callback_battery
                if cbk is not None:
                    cbk(copy.copy(b_info[0]))


@ctypes.CFUNCTYPE(None, ctypes.c_void_p)
def _callback_load_config(data) -> None:
    with _managers_mtx:
        mgr = _managers.get(data)
        if mgr is not None:
            with mgr._callback_load_config_mtx:
                cbk = mgr._callback_load_config
                if cbk is not None:
                    cbk()


@ctypes.CFUNCTYPE(None, ctypes.c_void_p)
def _callback_disconnect(data) -> None:
    with _managers_mtx:
        mgr = _managers.get(data)
        if mgr is not None:
            with mgr._callback_disconnect_mtx:
                cbk = mgr._callback_disconnect
                if cbk is not None:
                    cbk()


class EEGManager:
    """Manages all communication with a BrainAccess device.

    The `EEGManager` is the primary interface for connecting to, configuring,
    and streaming data from a BrainAccess device. It handles the low-level
    details of Bluetooth communication and provides a high-level API for
    controlling the device.
    """

    def __init__(self) -> None:
        """Initializes a new EEGManager instance.

        Warning
        -------
        The BrainAccess Core library must be initialized with `init()` before
        creating an `EEGManager`.
        """
        self.conenction_success: int = 0
        self._callback_chunk_mtx = threading.Lock()
        self._callback_battery_mtx = threading.Lock()
        self._callback_disconnect_mtx = threading.Lock()
        self._callback_start_stream_mtx = threading.Lock()
        self._callback_stop_stream_mtx = threading.Lock()
        self._callback_load_config_mtx = threading.Lock()
        self._callback_ota_update_mtx = threading.Lock()
        self._manager = _dll.ba_eeg_manager_new()
        with _managers_mtx:
            _managers[self._manager] = self

        self._callback_disconnect = lambda: None
        _dll.ba_eeg_manager_set_callback_disconnect(
            self._manager, _callback_disconnect, self._manager
        )

    def __enter__(self) -> "EEGManager":
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.destroy()

    def destroy(self) -> None:
        """Releases all resources associated with the EEG manager.

        This method should be called when the manager is no longer needed to
        ensure a clean shutdown.

        Warning
        -------
        This method must be called exactly once.
        """
        self.disconnect()  # prevent callback deadlock by disconnecting first.
        with _managers_mtx:
            _dll.ba_eeg_manager_free(self._manager)
            del _managers[self._manager]

    def disconnect(self) -> None:
        """Disconnects from the device, if a connection is active."""
        _dll.ba_eeg_manager_disconnect(self._manager)
        platform_name = platform.uname()[0]
        if platform_name == "Windows":
            # Windows Bluetooth takes longer
            # to cleanup
            time.sleep(5)
        else:
            time.sleep(1)

    def connect(self, bt_device_name: str) -> int:
        """Connects to a BrainAccess device.

        Parameters
        ----------
        bt_device_name : str
            The name of the device to connect to (e.g., "HALO 001", "MINI 001").

        Returns
        -------
        int
            - 0: Connection successful.
            - 2: Connection successful, but the data stream is incompatible.
                 A firmware update is recommended.

        Raises
        ------
        BrainAccessException
            If the connection could not be established.
        """
        cbk, _ = _callback()
        self.connection_success = _dll.ba_eeg_manager_connect(
            self._manager, ctypes.c_char_p(bt_device_name.encode("ascii")), cbk, None)
        if self.connection_success == 2:
            warnings.warn("Stream is incompatible. Update the firmware.")
            return self.connection_success
        _handle_error(self.connection_success)
        return self.connection_success

    def is_connected(self) -> bool:
        """Checks if a connection to a device is currently active.

        Returns
        -------
        bool
            True if connected, False otherwise.
        """
        return _dll.ba_eeg_manager_is_connected(self._manager)

    def start_stream(self, callback: Union[Callable, None] = None) -> bool:
        """Starts streaming data from the device.

        Parameters
        ----------
        callback : callable, optional
            A function to be called when the stream has successfully started.

        Returns
        -------
        bool
            True if the stream was started successfully.

        Raises
        ------
        BrainAccessException
            If the stream is already running or could not be started.
        """
        if self.connection_success == 2:
            raise BrainAccessException("Stream is incompatible. Update the firmware.")
        if callback is not None:
            with self._callback_start_stream_mtx:
                self._callback_start_stream = callback
        else:
            with self._callback_start_stream_mtx:
                self._callback_start_stream = lambda: None

        if self.is_streaming():
            raise BrainAccessException("Stream already running")
        return _handle_error(
            _dll.ba_eeg_manager_start_stream(
                self._manager, _callback_start_stream, self._manager
            )
        )

    def stop_stream(self, callback: Union[Callable, None] = None) -> bool:
        """Stops the data stream from the device.

        Parameters
        ----------
        callback : callable, optional
            A function to be called when the stream has successfully stopped.

        Returns
        -------
        bool
            True if the stream was stopped successfully.

        Raises
        ------
        BrainAccessException
            If the stream is not currently running or could not be stopped.
        """
        if callback is not None:
            with self._callback_stop_stream_mtx:
                self._callback_stop_stream = callback
        else:
            with self._callback_stop_stream_mtx:
                self._callback_stop_stream = lambda: None

        if not self.is_connected():
            return _handle_error(1)
        if not self.is_streaming():
            raise BrainAccessException("Stream not running")
        return _handle_error(
            _dll.ba_eeg_manager_stop_stream(self._manager, _callback_stop_stream, None)
        )

    def is_streaming(self) -> bool:
        """Checks if the device is currently streaming data.

        Returns
        -------
        bool
            True if the stream is active, False otherwise.
        """
        return _dll.ba_eeg_manager_is_streaming(self._manager)

    def load_config(self, callback: Union[Callable, None] = None) -> None:
        """Applies the current channel and other settings to the device.

        Parameters
        ----------
        callback : callable, optional
            A function to be called when the configuration has been successfully
            loaded onto the device.
        """
        if callback is not None:
            with self._callback_load_config_mtx:
                self._callback_load_config = callback
        else:
            with self._callback_load_config_mtx:
                self._callback_load_config = lambda: None

        _handle_error(
            _dll.ba_eeg_manager_load_config(
                self._manager, _callback_load_config, self._manager
            )
        )

    def get_battery_info(self) -> BatteryInfo:
        """Retrieves the current battery status from the device.

        Returns
        -------
        BatteryInfo
            An object containing battery level and charging status.
        """
        return _dll.ba_eeg_manager_get_battery_info(self._manager)

    def set_channel_enabled(self, channel: int, state: bool) -> None:
        """Enables or disables a specific data channel.

        Warning
        -------
        Channel settings are reset when the stream is stopped. This method
        must be called before each stream start to configure the desired
        channels.

        Parameters
        ----------
        channel : int
            The ID of the channel to enable or disable (see `brainaccess.core.eeg_channel`).
        state : bool
            True to enable the channel, False to disable it.

        Raises
        ------
        BrainAccessException
            If the device is currently streaming.
        """
        if self.is_streaming():
            raise BrainAccessException("Cannot change channel state while streaming")
        _dll.ba_eeg_manager_set_channel_enabled(
            self._manager, ctypes.c_uint16(channel), ctypes.c_bool(state)
        )

    def set_channel_gain(self, channel: int, gain: GainMode) -> None:
        """Sets the gain mode for a specific channel.

        Lower gain values increase the measurable voltage range at the cost of
        reduced amplitude resolution. A gain of X12 is optimal for most use cases.

        Warning
        -------
        This setting takes effect on stream start and is reset on stream stop.
        It only affects channels that support gain control, such as electrode
        measurement channels.

        Parameters
        ----------
        channel : int
            The ID of the channel to configure.
        gain : GainMode
            The desired gain mode.

        Raises
        ------
        BrainAccessException
            If the device is streaming or the channel number is invalid.
        """
        if channel < 0 or channel > 33:
            raise BrainAccessException("Invalid channel number")
        if self.is_streaming():
            raise BrainAccessException("Cannot change channel gain while streaming")
        _dll.ba_eeg_manager_set_channel_gain(
            self._manager, ctypes.c_uint16(channel), ctypes.c_uint8(gain.value)
        )

    @multimethod
    def set_channel_bias(self, channel: int, bias: bool) -> None:
        """
        DEPRECATED: Use the version with `Polarity` instead.

        Configures an electrode channel for bias feedback. The signals from
        bias channels are inverted and fed back into the bias electrode to
        reduce common-mode noise (e.g., from power lines).

        Warning
        -------
        This setting takes effect on stream start and is reset on stream stop.
        Only select channels with good skin contact for bias feedback.

        Parameters
        ----------
        channel : int
            The ID of the channel to use for bias feedback.
        bias : bool
            True to enable bias feedback for this channel, False to disable.

        Raises
        ------
        BrainAccessException
            If the device is currently streaming.
        """
        warnings.warn(
            "This function is deprecated, use the version with Polarity instead.",
            DeprecationWarning,
        )
        if self.is_streaming():
            raise BrainAccessException("Cannot change channel bias while streaming")
        self.set_channel_bias(channel, Polarity.BOTH if bias else Polarity.NONE)

    @set_channel_bias.register  # type: ignore
    def set_channel_bias(self, channel: int, p: Polarity) -> None:
        """Configures an electrode channel for bias feedback.

        The signals from bias channels are inverted and fed back into the bias
        electrode to reduce common-mode noise (e.g., from power lines).

        Warning
        -------
        This setting takes effect on stream start and is reset on stream stop.
        Only select channels with good skin contact for bias feedback.

        Parameters
        ----------
        channel : int
            The ID of the channel to use for bias feedback.
        p : Polarity
            The polarity to use for the bias signal. If the device is not
            bipolar, use `Polarity.BOTH`.

        Raises
        ------
        BrainAccessException
            If the device is currently streaming.
        """
        if self.is_streaming():
            raise BrainAccessException("Cannot change channel bias while streaming")
        _dll.ba_eeg_manager_set_channel_bias(
            self._manager, ctypes.c_uint16(channel), ctypes.c_uint8(p.value)
        )

    def set_impedance_mode(self, mode: ImpedanceMeasurementMode):
        """Configures the device for impedance measurement.

        This mode injects a small, known current through the bias electrodes
        and measures the resulting voltage at each electrode. The impedance can
        then be calculated using Ohm's law (Impedance = Voltage / Current).

        Warning
        -------
        This setting takes effect on stream start and is reset on stream stop.

        Parameters
        ----------
        mode : ImpedanceMeasurementMode
            The impedance measurement mode to set.

        Raises
        ------
        BrainAccessException
            If the device is currently streaming.
        """
        if self.is_streaming():
            raise BrainAccessException("Cannot change impedance mode while streaming")
        _dll.ba_eeg_manager_set_impedance_mode(
            self._manager, ctypes.c_uint8(mode.value)
        )

    def get_device_info(self) -> DeviceInfo:
        """Retrieves static information about the connected device.

        Warning
        -------
        This method should only be called after a successful connection has
        been established.

        Returns
        -------
        DeviceInfo
            An object containing the device model, hardware/firmware versions,
            and other static information.
        """
        return _dll.ba_eeg_manager_get_device_info(self._manager).contents

    def get_channel_index(self, channel: int) -> int:
        """Gets the index of a specific channel within the data chunk.

        This allows you to locate the data for a particular channel within the
        array provided by the chunk callback.

        Parameters
        ----------
        channel : int
            The ID of the channel.

        Returns
        -------
        int
            The index of the channel's data in the chunk array.

        Raises
        ------
        BrainAccessException
            If the channel does not exist or is not currently being streamed.
        """
        val = _dll.ba_eeg_manager_get_channel_index(
            self._manager, ctypes.c_uint16(channel)
        )
        if val == ctypes.c_size_t(-1).value:
            raise BrainAccessException(
                "Channel does not exist or is not currently streaming"
            )
        return val

    def get_sample_frequency(self) -> int:
        """Gets the sampling frequency of the device.

        Returns
        -------
        int
            The sampling frequency.
        """
        rate_value = StreamRate(_dll.ba_eeg_manager_get_sample_frequency(self._manager))
        return rate_value.to_hz

    def set_callback_chunk(self, f: Callable) -> None:
        """Sets a callback function to be executed when a new data chunk is available.

        Warning
        -------
        The callback may be executed in a different thread. Ensure that any
        shared data is properly synchronized and that the callback executes
        quickly to avoid blocking communication with the device.

        Parameters
        ----------
        f : callable
            The function to be called. It should accept a list of NumPy arrays
            (one for each channel) and the chunk size as arguments.
            Set to `None` to disable the callback.
        """
        with self._callback_chunk_mtx:
            self._callback_chunk = f
            _dll.ba_eeg_manager_set_callback_chunk(
                self._manager, _callback_chunk if f is not None else None, self._manager
            )

    def set_callback_battery(self, callback: Union[Callable, None] = None) -> None:
        """Sets a callback function to be executed when the battery status is updated.

        Warning
        -------
        The callback may be executed in a different thread. Ensure that any
        shared data is properly synchronized and that the callback executes
        quickly to avoid blocking communication with the device.

        Parameters
        ----------
        callback : callable, optional
            The function to be called. It should accept a `BatteryInfo` object
            as an argument. Set to `None` to disable.

        Raises
        ------
        BrainAccessException
            If the callback is `None`.
        """
        if callback is not None:
            with self._callback_battery_mtx:
                self._callback_battery = callback
        else:
            raise BrainAccessException("Callback cannot be null")
        _dll.ba_eeg_manager_set_callback_battery(
            self._manager,
            _callback_battery,
            self._manager,
        )

    def set_callback_disconnect(self, callback: Optional[Callable] = None) -> None:
        """Sets a callback function to be executed when the device disconnects.

        Warning
        -------
        The callback may be executed in a different thread. Ensure that any
        shared data is properly synchronized and that the callback executes
        quickly.

        Parameters
        ----------
        callback : callable, optional
            The function to be called on disconnect. Set to `None` to disable.
        """
        if callback is None:
            with self._callback_disconnect_mtx:
                self._callback_disconnect = lambda: None
        else:
            with self._callback_disconnect_mtx:
                self._callback_disconnect = callback
        _dll.ba_eeg_manager_set_callback_disconnect(
            self._manager, _callback_disconnect, self._manager
        )

    def annotate(self, annotation: str) -> None:
        """Adds a timestamped annotation to the data stream.

        Warning
        -------
        Annotations are cleared when the device is disconnected.

        Parameters
        ----------
        annotation : str
            The text of the annotation.

        Raises
        ------
        BrainAccessException
            If the annotation is `None` or empty.
        """
        if annotation is None:
            raise BrainAccessException("Annotation cannot be None")
        if len(annotation) == 0:
            raise BrainAccessException("Annotation cannot be empty")
        _handle_error(
            _dll.ba_eeg_manager_annotate(
                self._manager, ctypes.c_char_p(annotation.encode("ascii"))
            )
        )

    def get_device_features(self) -> DeviceFeatures:
        """Retrieves the features and capabilities of the connected device.

        Returns
        -------
        DeviceFeatures
            An object with methods to query for features like gyroscope,
            accelerometer, bipolar electrodes, and electrode count.
        """
        info = self.get_device_info()
        return DeviceFeatures(info)

    def get_annotations(self) -> dict:
        """Retrieves all accumulated annotations.

        Warning
        -------
        Annotations are cleared when the device is disconnected.

        Returns
        -------
        dict
            A dictionary with two keys:
            - "annotations": A list of annotation strings.
            - "timestamps": A list of corresponding timestamps.
        """
        ae = ctypes.POINTER(Annotation)()
        size = ctypes.c_size_t()
        _dll.ba_eeg_manager_get_annotations(
            self._manager, ctypes.pointer(ae), ctypes.pointer(size)
        )
        annotations = [ae[i] for i in range(size.value)]
        timestamps = [x.timestamp for x in annotations]
        annotations = [x.annotation for x in annotations]
        return {"annotations": annotations, "timestamps": timestamps}

    def clear_annotations(self) -> None:
        """Clears all existing annotations."""
        _dll.ba_eeg_manager_clear_annotations(self._manager)

    def start_update(self, callback: Union[Callable, None] = None) -> None:
        """Starts a firmware update for the device.

        Parameters
        ----------
        callback : callable, optional
            A function to be called with the progress of the update. It should
            accept two arguments: the number of bytes sent and the total
            number of bytes.

        Raises
        ------
        BrainAccessException
            If the update cannot be started.
        """
        if callback is not None:
            with self._callback_ota_update_mtx:
                self._callback_ota_update = callback
        else:
            with self._callback_ota_update_mtx:
                self._callback_ota_update = lambda x, y: None

        _handle_error(
            _dll.ba_eeg_manager_start_update(
                self._manager, _callback_ota_update, self._manager
            )
        )

    def set_sample_rate(self, sample_rate: int) -> bool:
        """Sets the data stream sample rate for the device.

        The available sample rates may depend on the device model and firmware
        version. Refer to the `brainaccess.core.stream_rate.StreamRate` enum
        for available options.

        Warning
        -------
        This setting takes effect on stream start and is reset on stream stop.

        Parameters
        ----------
        sample_rate : int
            The desired data stream sample rate.

        Raises
        ------
        BrainAccessException
            If the device is currently streaming.
            If the device sample rate is not possible
        """
        if self.is_streaming():
            raise BrainAccessException("Cannot change sample rate while streaming")

        _sample_rate = StreamRate.from_hz(sample_rate)

        if _sample_rate == StreamRate.UNKNOWN:
            raise BrainAccessException("Wrong sample rate")

        device_info = self.get_device_info()
        device_model = device_info.device_model

        if device_model in [DeviceModel.MAXI, DeviceModel.MIDI]:
            if sample_rate != StreamRate.X250Hz.to_hz:
                raise BrainAccessException(
                    f"{device_model.name} only supports 250Hz sample rate."
                )
        elif device_model in [DeviceModel.HALO, DeviceModel.MINI]:
            if sample_rate > StreamRate.X500Hz.to_hz:
                raise BrainAccessException(
                    f"{device_model.name} supports sample rates up to 500Hz."
                )
        return _handle_error(
            _dll.ba_eeg_manager_set_data_stream_rate(
                self._manager, ctypes.c_uint8(_sample_rate.value)
            )
        )
