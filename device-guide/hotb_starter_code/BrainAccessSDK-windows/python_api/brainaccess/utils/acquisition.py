import typing
import time
import threading
import numpy as np
import mne  # type: ignore
import pathlib

import brainaccess.core as bacore
import brainaccess.core.eeg_channel as eeg_channel
from brainaccess.core.gain_mode import GainMode, multiplier_to_gain_mode
from brainaccess.core.eeg_manager import EEGManager
from brainaccess.core.impedance_measurement_mode import ImpedanceMeasurementMode
from brainaccess.core.device_features import DeviceFeatures
from brainaccess.utils.exceptions import BrainAccessException



class EEG:
    """EEG acquisition class.
    Gathers data from brainaccess core and converts to MNE structure.
    """

    def __init__(
        self,
        mode: str = "accumulate",
    ) -> None:
        """Creates EEG object and initializes device with default parameters.

        Parameters
        ------------
        mode: str
            Data storage modes accumulate (all data is accumulated in array)
            or roll (only last x seconds preserved)

        """
        self.directory = pathlib.Path.cwd()
        self.wait_max: int = 2
        self.time_step: float = 0.5
        self.impedances: dict = {}
        self.eeg_channels: dict = {}
        self.bias_channels: typing.Optional[list] = None
        self.mode: str = mode
        self.gain: GainMode = GainMode.X8
        bacore.init()

    def setup(
        self,
        mgr: EEGManager,
        device_name: str,
        cap: dict = {
            0: "F3",
            1: "F4",
            2: "C3",
            3: "C4",
            4: "P3",
            5: "P4",
            6: "O1",
            7: "O2",
        },
        zeros_at_start: int = 0,
        bias: typing.Optional[list] = None,
        gain: int = 8,
        sfreq: int = 250,
    ) -> None:
        """Connects to device and sets channels

        Parameters
        ------------
        mgr: EEGManager
            The EEG manager object.
        device_name: str
            The name of the device to connect to.
        cap: dict
            A dictionary mapping electrode numbers to channel names.
        zeros_at_start: int
            The number of zeros to add at the beginning of the data.
        bias: list, optional
            A list of channels to use for bias.
        gain: int
            The gain to use for the EEG channels.

        Raises
        ------
        BrainAccessException
            If no devices are found, could not connect to the device, or the stream is incompatible.
        """
        self.mgr = mgr
        self.sfreq = sfreq
        devices = bacore.scan()
        if len(devices) == 0:
            self._error("No devices found")
        self.zeros_at_start = zeros_at_start
        if bias:
            self.bias_channels = bias
        else:
            self.bias_channels = []
        if gain in [4, 6, 8, 12]:
            self.gain = multiplier_to_gain_mode(gain)
        else:
            print("Provided gain not supported. Using default 8")
        start_time = time.time()
        while time.time() < (start_time + self.wait_max):
            try:
                self.conn_error = mgr.connect(device_name)
                if self.conn_error == 0:
                    break
                elif self.conn_error == 2:
                    raise BrainAccessException(
                        "Stream is incompatible, update device firmware"
                    )
                else:
                    print("could not connect")
            except Exception as e:
                raise BrainAccessException(f"Could not connect to device {e}")
        else:
            self._error("Could not connect to Client.")
        self.eeg_channels = {}
        self.channels_type: dict = {}
        self.channels_indexes = {}
        for electrode, name in cap.items():
            self.eeg_channels[eeg_channel.ELECTRODE_MEASUREMENT + electrode] = name
            self.channels_type[eeg_channel.ELECTRODE_MEASUREMENT + electrode] = "EEG"
            self.channels_indexes[eeg_channel.ELECTRODE_MEASUREMENT + electrode] = 0
        if self.mgr.is_connected():
            info = self.mgr.get_device_info()
            features = DeviceFeatures(info)
            if features.has_accel():
                self.eeg_channels[eeg_channel.ACCELEROMETER + 0] = "Accel_x"
                self.eeg_channels[eeg_channel.ACCELEROMETER + 1] = "Accel_y"
                self.eeg_channels[eeg_channel.ACCELEROMETER + 2] = "Accel_z"
                self.channels_type[eeg_channel.ACCELEROMETER + 0] = "ACC"
                self.channels_type[eeg_channel.ACCELEROMETER + 1] = "ACC"
                self.channels_type[eeg_channel.ACCELEROMETER + 2] = "ACC"
                self.channels_indexes[eeg_channel.ACCELEROMETER + 0] = 0
                self.channels_indexes[eeg_channel.ACCELEROMETER + 1] = 0
                self.channels_indexes[eeg_channel.ACCELEROMETER + 2] = 0
        self.eeg_channels[eeg_channel.SAMPLE_NUMBER] = "Sample"
        self.channels_type[eeg_channel.SAMPLE_NUMBER] = "Sample"
        self.channels_indexes[eeg_channel.SAMPLE_NUMBER] = 0
        eeg_info = self._create_info()
        self.info = eeg_info
        self.chans = len(self.info.ch_names)
        if self.mode == "accumulate":
            self.lock = threading.Lock()
            self.data: typing.Union[EEGData, EEGData_roll] = EEGData(
                eeg_info, lock=self.lock, zeros_at_start=zeros_at_start
            )
        else:
            self.lock = threading.Lock()
            self.data = EEGData_roll(
                eeg_info, lock=self.lock, zeros_at_start=zeros_at_start
            )

    def _set_channels(self):
        """Set the channels to be enabled."""
        for chan in self.eeg_channels.keys():
            self.mgr.set_channel_enabled(chan, True)

    def get_battery(self) -> int:
        """Returns battery level in percent."""
        res = self.mgr.get_battery_info()
        return res.level

    def _error(self, extra: str = ""):
        """Raises error with extra text
        Parameters
        ----------
        extra: str  (Default value = '')

        """
        raise BrainAccessException(f"{extra}")

    def close(self):
        """Close device connection."""
        bacore.close()

    def _start_acquisition(self):
        """Starts streaming and collecting data"""
        self._set_channels()
        for chan in self.bias_channels:
            self.mgr.set_channel_bias(eeg_channel.ELECTRODE_MEASUREMENT + chan, True)
        for idx, value in enumerate(list(self.eeg_channels.keys())):
            if self.channels_type[value] == "EEG":
                self.mgr.set_channel_gain(value, self.gain)
        if self.mode == "accumulate":
            self.mgr.set_callback_chunk(self._acq)
        else:
            self.mgr.set_callback_chunk(self._acq_roll)
        self.mgr.set_sample_rate(self.sfreq)
        self.mgr.load_config()
        try:
            self.mgr.start_stream()
        except Exception:
            raise BrainAccessException("Could not start stream")
        for key in self.channels_indexes.keys():
            self.channels_indexes[key] = self.mgr.get_channel_index(key)

    def start_acquisition(self):
        """Starts streaming and collecting data."""
        self._start_acquisition()

    def _stop_acquisition(self):
        """Stops the data acquisition stream."""
        self.mgr.stop_stream()

    def stop_acquisition(self):
        """Stops the data acquisition stream."""
        self._stop_acquisition()

    def get_annotations(self) -> dict:
        """Returns annotations from the data stream."""
        self.data.annotations = self.mgr.get_annotations()
        return self.data.annotations

    def annotate(self, msg: str) -> None:
        """Adds an annotation to the data stream.
        Parameters
        ----------
        msg: str
            annotation to send

        """
        self.mgr.annotate(msg)

    def get_mne(
        self,
        tim: typing.Optional[float] = None,
        samples: typing.Optional[int] = None,
        annotations: bool = True,
    ) -> mne.io.BaseRaw:
        """Return MNE structure.
        If tim is None, returns all data; otherwise, returns the last `tim` seconds.

        Parameters
        ----------
        tim: float, optional
            Time in seconds.
        samples: int, optional
            Number of samples.
        annotations: bool
            Whether to include annotations.

        Returns
        -------
        mne.io.BaseRaw
            Raw MNE EEG data structure.

        """
        if annotations:
            self.get_annotations()
        self.data.convert_to_mne(
            tim=tim,
            samples=samples,
            channels_indexes=list(self.channels_indexes.values()),
        )
        return self.data.mne_raw

    def _acq(self, chunk, chunk_size):
        """function to acquire data with callback
        Parameters
        ----------
        chunk
            data chunk from device
        chunk_size: int
            size of the chunk
        """
        self.data.data.append(np.array(chunk))

    def _acq_roll(self, chunk, chunk_size):
        """function to acquire fixed size data with callback
        Parameters
        ----------
        chunk
            data chunk from device
        chunk_size: int
            size of the chunk
        """
        self.data.data = np.roll(self.data.data, -chunk_size, axis=1)
        self.data.data[:, -chunk_size:] = np.array(chunk)

    def _create_info(self):
        """mne info structure creation"""
        import brainaccess.core.eeg_channel as eeg_channel

        sampling_freq = self.mgr.get_sample_frequency()
        ch_names = [x for x in self.eeg_channels.values()]
        sample_channels = len(
            [
                x
                for x in list(self.eeg_channels.keys())
                if x == eeg_channel.SAMPLE_NUMBER
            ]
        )
        digital_channels = len(
            [
                x
                for x in list(self.eeg_channels.keys())
                if x == eeg_channel.DIGITAL_INPUT
            ]
        )
        acc_channels = len(
            [
                x
                for x in list(self.eeg_channels.keys())
                if x >= eeg_channel.ACCELEROMETER
            ]
        )
        non_eeg_channels = sample_channels + digital_channels + acc_channels
        ch_types = ["eeg"] * int(len(ch_names) - non_eeg_channels)
        ch_types.extend(["misc"] * acc_channels)
        ch_types.extend(["stim"] * digital_channels)
        ch_types.extend(["syst"] * sample_channels)
        eeg_info = mne.create_info(ch_names, ch_types=ch_types, sfreq=sampling_freq)
        eeg_info.set_montage("standard_1005")
        return eeg_info

    def start_impedance_measurement(self):
        """Starts impedance measurement."""
        self.mgr.set_impedance_mode(ImpedanceMeasurementMode.HZ_31_2)
        self.bias_channels = []
        self.start_acquisition()

    def stop_impedance_measurement(self):
        """Stops impedance measurement."""
        self.stop_acquisition()
        self.mgr.set_impedance_mode(ImpedanceMeasurementMode.OFF)


class EEGData_roll:
    """Data structure to store rolling EEG data buffer"""

    def __init__(self, info, lock, zeros_at_start: int = 1):
        """Initializes the EEGData_roll object.

        Parameters
        ----------
        info : mne.Info
            The MNE info object.
        lock : threading.Lock
            The threading lock.
        zeros_at_start : int, optional
            The number of zeros to add at the beginning of the data, by default 1.

        Raises
        ------
        BrainAccessException
            If no lock is passed.
        """
        if not lock:
            raise BrainAccessException("No lock passed")
        self.eeg_info: mne.Info = info
        self.mne_raw: mne.io.BaseRaw
        self.chans = len(info.ch_names)
        self.zeros_at_start = zeros_at_start
        self.data = np.zeros((self.chans, self.zeros_at_start))
        self.connectivity: list = []
        self.annotations: dict = {}
        self.lock = lock

    def save(self, fname: str):
        """Saves the raw data to a file.
        Parameters
        ------------
        fname: str
            filename to save data to
        """
        with self.lock:
            self.mne_raw.save(fname=fname, verbose=False, overwrite=True, fmt="double")

    def load(self, fname: str):
        """Loads raw data from a file.

        Parameters
        ----------
        fname : str
            The name of the file to load.
        """
        self.mne_raw = mne.io.read_raw(fname, verbose=False)

    def convert_to_mne(
        self,
        tim: typing.Optional[float] = None,
        samples: typing.Optional[int] = None,
        annotations: bool = True,
        channels_indexes: typing.Optional[list] = None,
    ):
        """Convert arrays to MNE.
        If tim None returns all data from acquisition start.
        Otherwise last tim seconds

        Parameters
        ------------
        tim: float, default value = None
            time in seconds or samples to cut
        samples: int, default value = None
            samples or time to cut
        annotations: bool, default value = True
            should annotations be included
        channels_indexes: list, optional
            A list of channel indexes to include.
        """
        with self.lock:
            length = len(self.data)
        if length > 0:
            if annotations:
                timestamp_correction = np.block(self.data)[0][0]
                onset = []
                description = []
                for idx, annotation in enumerate(self.annotations["annotations"]):
                    description.append(annotation)
                    timestamp = self.annotations["timestamps"][idx]
                    onset.append(
                        (timestamp + self.zeros_at_start - timestamp_correction)
                        / self.eeg_info["sfreq"]
                    )
                duration = np.repeat(0, len(onset))
            if tim:
                # convert tim to samples
                tim = int(tim * self.eeg_info["sfreq"])
                with self.lock:
                    data = np.array(self.data)  # .reshape(self.chans, -1)
                    data = data[:, -tim:]
                # fix annotations
                if annotations:
                    onset = [x - tim for x in onset]
                    duration = np.repeat(0, len(onset))
            elif samples:
                with self.lock:
                    data = np.array(self.data)  # .reshape(self.chans, -1)
                    data = data[:, -samples:]
                # fix annotations
                if annotations:
                    onset = [x - samples for x in onset]
                    duration = np.repeat(0, len(onset))
            else:
                with self.lock:
                    data = np.array(self.data)  # .reshape(self.chans, -1)
            # select right order channels
            if channels_indexes:
                data = data[channels_indexes]
            self.mne_raw = mne.io.RawArray(
                data,
                self.eeg_info,
                verbose=False,
            )
            if annotations:
                annot = mne.Annotations(onset, duration, description)
                self.mne_raw.set_annotations(annot, verbose=False)
        else:
            print("No data to convert to MNE structure")


class EEGData:
    """Object to store EEG data in accumulation mode"""

    def __init__(self, info, lock, zeros_at_start: int = 2):
        """Initializes the EEGData object.

        Parameters
        ----------
        info : mne.Info
            The MNE info object.
        lock : threading.Lock
            The threading lock.
        zeros_at_start : int, optional
            The number of zeros to add at the beginning of the data, by default 2.
        """
        self.eeg_info: mne.Info = info
        self.mne_raw: mne.io.BaseRaw
        self.lock = lock
        chans = len(info.ch_names)
        self.zeros_at_start = zeros_at_start
        self.data: list = [np.zeros((chans, self.zeros_at_start))]
        self.connectivity: list = []
        self.annotations: dict = {}

    def save(self, fname: str):
        """Saves the raw data to a file.
        Parameters
        ------------
        fname: str
            filename to save data to
        """
        with self.lock:
            self.mne_raw.save(fname=fname, verbose=False, overwrite=True, fmt="double")

    def load(self, fname: str):
        """Loads raw data from a file.

        Parameters
        ----------
        fname : str
            The name of the file to load.
        """
        self.mne_raw = mne.io.read_raw(fname, verbose=False)

    def convert_to_mne(
        self,
        tim: typing.Optional[float] = None,
        samples: typing.Optional[int] = None,
        annotations: bool = True,
        channels_indexes: typing.Optional[list] = None,
    ):
        """Convert arrays to MNE.
        If tim None returns all data from acquisition start.
        Otherwise last tim seconds

        Parameters
        ------------
        tim: float, default value = None
            time in seconds till the end to include in the output
        samples: int, default value = None
            time in samples till the end to include in the output
        annotations: bool, default value = True
            should annotations be included
        channels_indexes: list, optional
            A list of channel indexes to include.
        """
        with self.lock:
            _length = len(self.data)
        if _length > 0:
            if annotations:
                timestamp_correction = np.block(self.data)[0][0]
                onset = []
                description = []
                for idx, annotation in enumerate(self.annotations["annotations"]):
                    description.append(annotation)
                    timestamp = self.annotations["timestamps"][idx]
                    onset.append(
                        (timestamp + self.zeros_at_start - timestamp_correction)
                        / self.eeg_info["sfreq"]
                    )
                duration = np.repeat(0, len(onset))
            if tim:
                # convert tim to samples
                tim = int(tim * self.eeg_info["sfreq"])
                data = self._concat_data()
                data = data[:, -tim:]
                # fix annotations
                if annotations:
                    onset = [x - tim for x in onset]
                    duration = np.repeat(0, len(onset))
            elif samples:
                data = self._concat_data()
                data = data[:, -samples:]
                # fix annotations
                if annotations:
                    onset = [x - samples for x in onset]
                    duration = np.repeat(0, len(onset))
            else:
                data = self._concat_data()
            # select right order channels
            if channels_indexes:
                data = data[channels_indexes]
            self.mne_raw = mne.io.RawArray(
                data,
                self.eeg_info,
                verbose=False,
            )
            if annotations:
                annot = mne.Annotations(onset, duration, description)
                self.mne_raw.set_annotations(annot, verbose=False)
        else:
            print("No data to convert to MNE structure")

    def _concat_data(self):
        """Concatenates the data blocks."""
        with self.lock:
            data = np.block(self.data)
        return data
