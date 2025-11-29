import ctypes
import numpy as np

from typing import Optional

from brainaccess.utils.exceptions import BrainAccessException
from brainaccess.connect import _dll


# ctypes

_dll.ba_bci_connect_get_signal_quality.argtypes = [
    ctypes.POINTER(ctypes.c_double),
    ctypes.c_size_t,
    ctypes.c_size_t,
    ctypes.POINTER(ctypes.c_double),
]
_dll.ba_bci_connect_get_signal_quality.restype = None

_dll.ba_bci_connect_detrend.argtypes = [
    ctypes.POINTER(ctypes.c_double),
    ctypes.c_size_t,
    ctypes.c_size_t,
    ctypes.POINTER(ctypes.c_double),
]
_dll.ba_bci_connect_detrend.restype = None

_dll.ba_bci_connect_median.argtypes = [
    ctypes.POINTER(ctypes.c_double),
    ctypes.c_size_t,
    ctypes.c_size_t,
    ctypes.POINTER(ctypes.c_double),
]
_dll.ba_bci_connect_median.restype = None

_dll.ba_bci_connect_mad.argtypes = [
    ctypes.POINTER(ctypes.c_double),
    ctypes.c_size_t,
    ctypes.c_size_t,
    ctypes.POINTER(ctypes.c_double),
]
_dll.ba_bci_connect_mad.restype = None

_dll.ba_bci_connect_mean.argtypes = [
    ctypes.POINTER(ctypes.c_double),
    ctypes.c_size_t,
    ctypes.c_size_t,
    ctypes.POINTER(ctypes.c_double),
]
_dll.ba_bci_connect_mean.restype = None

_dll.ba_bci_connect_std.argtypes = [
    ctypes.POINTER(ctypes.c_double),
    ctypes.c_size_t,
    ctypes.c_size_t,
    ctypes.POINTER(ctypes.c_double),
]
_dll.ba_bci_connect_std.restype = None


_dll.ba_bci_connect_demean.argtypes = [
    ctypes.POINTER(ctypes.c_double),
    ctypes.c_size_t,
    ctypes.c_size_t,
    ctypes.POINTER(ctypes.c_double),
]
_dll.ba_bci_connect_demean.restype = None

_dll.ba_bci_connect_standartize.argtypes = [
    ctypes.POINTER(ctypes.c_double),
    ctypes.c_size_t,
    ctypes.c_size_t,
    ctypes.POINTER(ctypes.c_double),
]
_dll.ba_bci_connect_standartize.restype = None

_dll.ba_bci_connect_ewma.argtypes = (
    ctypes.POINTER(ctypes.c_double),
    ctypes.c_size_t,
    ctypes.c_size_t,
    ctypes.c_double,
    ctypes.POINTER(ctypes.c_double),
)
_dll.ba_bci_connect_ewma.restype = None

_dll.ba_bci_connect_ewma_standartize.argtypes = (
    ctypes.POINTER(ctypes.c_double),
    ctypes.c_size_t,
    ctypes.c_size_t,
    ctypes.c_double,
    ctypes.c_double,
    ctypes.POINTER(ctypes.c_double),
)
_dll.ba_bci_connect_ewma_standartize.restype = None

_dll.ba_bci_connect_filter_notch.argtypes = (
    ctypes.POINTER(ctypes.c_double),
    ctypes.c_size_t,
    ctypes.c_size_t,
    ctypes.c_double,
    ctypes.c_double,
    ctypes.c_double,
)
_dll.ba_bci_connect_filter_notch.restype = None

_dll.ba_bci_connect_filter_bandpass.argtypes = (
    ctypes.POINTER(ctypes.c_double),
    ctypes.c_size_t,
    ctypes.c_size_t,
    ctypes.c_double,
    ctypes.c_double,
    ctypes.c_double,
)
_dll.ba_bci_connect_filter_bandpass.restype = None

_dll.ba_bci_connect_filter_highpass.argtypes = (
    ctypes.POINTER(ctypes.c_double),
    ctypes.c_size_t,
    ctypes.c_size_t,
    ctypes.c_double,
    ctypes.c_double,
)
_dll.ba_bci_connect_filter_highpass.restype = None

_dll.ba_bci_connect_filter_lowpass.argtypes = (
    ctypes.POINTER(ctypes.c_double),
    ctypes.c_size_t,
    ctypes.c_size_t,
    ctypes.c_double,
    ctypes.c_double,
)
_dll.ba_bci_connect_filter_lowpass.restype = None

_dll.ba_bci_connect_fft.argtypes = [
    ctypes.POINTER(ctypes.c_double),
    ctypes.c_size_t,
    ctypes.c_size_t,
    ctypes.c_double,
    ctypes.POINTER(ctypes.c_double),
    ctypes.POINTER(ctypes.c_double),
]
_dll.ba_bci_connect_fft.restype = None

_dll.ba_bci_connect_minmax.argtypes = [
    ctypes.POINTER(ctypes.c_double),
    ctypes.c_size_t,
    ctypes.c_size_t,
    ctypes.POINTER(ctypes.c_double),
    ctypes.POINTER(ctypes.c_double),
]
_dll.ba_bci_connect_minmax.restype = None


def get_signal_quality(x: np.ndarray) -> np.ndarray:
    """Calculate signal quality for each channel in the data
    This function estimates the EEG signal quality for each
    channel based on amplitude variation and 50/60Hz noise level.
    The supplied data should be unprocessed of 2-3 seconds length.
    If signals do not pass the quality measures of this function,
    then it means that they are really corrupted or the electrodes
    are not fitted. Eye or muscle artifacts are not evaluated by
    this function, signals containing theses should still pass the
    quality measures.

    Parameters
    -----------
    x: np.ndarray
        data array, shape (channels, time)

    Returns
    --------
    np.ndarray
        signal quality for each channel in the same order as x
        * 0 - signal is bad and did not pass any quality measure
        * 1 - signal passed amplitude related quality measures
        * 2 - signal also do not contain significant amounts of 50/60Hz noise
    """
    chans = x.shape[0]
    time_points = x.shape[1]
    _x = x.copy().ravel(order="C").astype(np.float64)
    c_result = np.ctypeslib.as_ctypes(np.zeros(chans))
    c_arr = np.ctypeslib.as_ctypes(_x)
    _dll.ba_bci_connect_get_signal_quality(c_arr, chans, time_points, c_result)
    return np.array(c_result[0:chans])


def detrend(x: np.ndarray) -> np.ndarray:
    """Remove linear trend from each channel

    Parameters
    -----------
    x: np.ndarray
        data array, shape (channels, time)

    Returns
    -----------
    np.ndarray
        data array, shape (channels, time)
    """

    chans = x.shape[0]
    time_points = x.shape[1]
    _x = x.copy().ravel(order="C").astype(np.float64)
    c_result = np.ctypeslib.as_ctypes(np.zeros(chans * time_points))
    c_arr = np.ctypeslib.as_ctypes(_x)
    _dll.ba_bci_connect_detrend(c_arr, chans, time_points, c_result)
    return np.array(c_result[: chans * time_points]).reshape((chans, time_points))


def mad(x: np.ndarray) -> np.ndarray:
    """Calculate median absolute deviation for each channel in the data

    Parameters
    -----------
    x: np.ndarray
        data array, shape (channels, time)

    Returns
    --------
    np.ndarray

    """
    chans = x.shape[0]
    time_points = x.shape[1]
    _x = x.copy().ravel(order="C").astype(np.float64)
    c_result = np.ctypeslib.as_ctypes(np.zeros(chans))
    c_arr = np.ctypeslib.as_ctypes(_x)
    _dll.ba_bci_connect_mad(c_arr, chans, time_points, c_result)
    return np.array(c_result)


def get_minmax(x: np.ndarray) -> dict[str, np.ndarray]:
    """Calculate min and max for each channel in the data

    Parameters
    -----------
    x: np.ndarray
        data array, shape (channels, time)

    Returns
    --------
    dict
        min and max for each channel in the same order as x
    """
    chans = x.shape[0]
    time_points = x.shape[1]
    _x = x.copy().ravel(order="C").astype(np.float64)
    c_arr = np.ctypeslib.as_ctypes(_x)
    result = np.zeros(chans)
    c_result_min = np.ctypeslib.as_ctypes(result.copy())
    c_result_max = np.ctypeslib.as_ctypes(result.copy())
    _dll.ba_bci_connect_minmax(c_arr, chans, time_points, c_result_min, c_result_max)
    return {
        "min": np.array(c_result_min[0:chans]),
        "max": np.array(c_result_max[0:chans]),
    }


def median(x: np.ndarray) -> np.ndarray:
    """Calculate median for each channel in the data

    Parameters
    -----------
    x: np.ndarray
        data array, shape (channels, time)

    Returns
    --------
    np.ndarray
        medians for each channel in the same order as x
    """
    chans = x.shape[0]
    time_points = x.shape[1]
    _x = x.copy().ravel(order="C").astype(np.float64)
    result = np.zeros(chans)
    c_result = np.ctypeslib.as_ctypes(result)
    c_arr = np.ctypeslib.as_ctypes(_x)
    _dll.ba_bci_connect_median(c_arr, chans, time_points, c_result)
    return np.array(c_result[0:chans])


def mean(x: np.ndarray) -> np.ndarray:
    """Calculate mean for each channel in the data

    Parameters
    -----------
    x: np.ndarray
        data array, shape (channels, time)

    Returns
    --------
    np.ndarray
        means for each channel in the same order as x
    """
    chans = x.shape[0]
    time_points = x.shape[1]
    _x = x.copy().ravel(order="C").astype(np.float64)
    result = np.zeros(chans)
    c_result = np.ctypeslib.as_ctypes(result)
    c_arr = np.ctypeslib.as_ctypes(_x)
    _dll.ba_bci_connect_mean(c_arr, chans, time_points, c_result)
    return np.array(c_result[0:chans])


def std(x: np.ndarray) -> np.ndarray:
    """Calculate standard deviation for each channel in the data

    Parameters
    -----------
    x: np.ndarray
        data array, shape (channels, time)

    Returns
    --------
    np.ndarray
        standard deviation for each channel in the same order as x
    """
    chans = x.shape[0]
    time_points = x.shape[1]
    _x = x.copy().ravel(order="C").astype(np.float64)
    result = np.zeros(chans)
    c_result = np.ctypeslib.as_ctypes(result)
    c_arr = np.ctypeslib.as_ctypes(_x)
    _dll.ba_bci_connect_std(c_arr, chans, time_points, c_result)
    return np.array(c_result[0:chans])


def demean(x: np.ndarray) -> np.ndarray:
    """Subtract mean from each channel

    Parameters
    -----------
    x: np.ndarray
        data array, shape (channels, time)

    Returns
    -----------
    np.ndarray
        data array, shape (channels, time)
    """

    chans = x.shape[0]
    time_points = x.shape[1]
    _x = x.copy().ravel(order="C").astype(np.float64)
    c_result = np.ctypeslib.as_ctypes(np.zeros(chans * time_points))
    c_arr = np.ctypeslib.as_ctypes(_x)
    _dll.ba_bci_connect_demean(c_arr, chans, time_points, c_result)
    return np.array(c_result[: chans * time_points]).reshape((chans, time_points))


def standardize(x: np.ndarray) -> np.ndarray:
    """Data standardization

    Parameters
    -----------
    x: np.ndarray
        data array, shape (channels, time)

    Returns
    -----------
    np.ndarray
        data array, shape (channels, time)

    """

    chans = x.shape[0]
    time_points = x.shape[1]
    _x = x.copy().ravel(order="C").astype(np.float64)
    c_result = np.ctypeslib.as_ctypes(np.zeros(chans * time_points))
    c_arr = np.ctypeslib.as_ctypes(_x)
    _dll.ba_bci_connect_standartize(c_arr, chans, time_points, c_result)
    return np.array(c_result[: chans * time_points]).reshape((chans, time_points))


def ewma(x: np.ndarray, alpha: float = 0.001) -> np.ndarray:
    """Exponential weighed moving average helper_function

    Parameters
    -----------
    x: np.ndarray
        data array, shape (channels, time)
    alpha: float
        new factor

    Returns
    -----------
    np.ndarray
        data array, shape (channels, time)

    """
    chans = x.shape[0]
    time_points = x.shape[1]
    _x = x.copy().ravel(order="C").astype(np.float64)
    c_result = np.ctypeslib.as_ctypes(np.zeros(chans * time_points))
    c_arr = np.ctypeslib.as_ctypes(_x)
    _dll.ba_bci_connect_ewma(c_arr, chans, time_points, np.float64(alpha), c_result)
    return np.array(c_result[: chans * time_points]).reshape((chans, time_points))


def ewma_standardize(
    x: np.ndarray, alpha: float = 0.001, epsilon: float = 1e-4
) -> np.ndarray:
    """Exponential weighed moving average standardization

    First-order infinite impulse response filter that applies weighting factors which decrease exponentially

    Parameters
    -----------
    x: np.ndarray
        data array, shape (channels, time)
    alpha: float
        Represents the degree of weighting decrease, a constant smoothing factor between 0 and 1. A higher alpha discounts older observations faster.
    epsilon: float
        Stabilizer for division by zero variance

    Returns
    -----------
    np.ndarray
        data array, shape (channels, time)

    """
    chans = x.shape[0]
    time_points = x.shape[1]
    _x = x.copy().ravel(order="C").astype(np.float64)
    c_result = np.ctypeslib.as_ctypes(np.zeros(chans * time_points))
    c_arr = np.ctypeslib.as_ctypes(_x)
    _dll.ba_bci_connect_ewma_standartize(
        c_arr, chans, time_points, np.float64(alpha), np.float64(epsilon), c_result
    )
    return np.array(c_result[: chans * time_points]).reshape((chans, time_points))


def filter_notch(
    x: np.ndarray, sampling_freq: float, center_freq: float, width_freq: float
) -> np.ndarray:
    """Notch filter at desired frequency

    Butterworth 4th order zero phase bandpass filter

    Parameters
    -----------
    x: np.ndarray
        data array, shape (channels, time)
    sampling_freq: float
        data sampling rate
    center_freq: float
        notch filter center frequency
    width_freq: float
        notch filter width


    Returns
    -----------
    np.ndarray
        data array, shape (channels, time)

    Warnings
    ---------
    Data must be detrended or passed through ba_bci_connect_ewma_standartize
    before applying notch filter

    """
    chans = x.shape[0]
    time_points = x.shape[1]
    _x = x.copy().ravel(order="C").astype(np.float64)
    c_arr = np.ctypeslib.as_ctypes(_x)
    _dll.ba_bci_connect_filter_notch(
        c_arr,
        ctypes.c_size_t(chans),
        ctypes.c_size_t(time_points),
        ctypes.c_double(sampling_freq),
        ctypes.c_double(center_freq),
        ctypes.c_double(width_freq),
    )
    return np.array(c_arr[: chans * time_points]).reshape((chans, time_points))


def filter_bandpass(
    x: np.ndarray, sampling_freq: float, freq_low: float, freq_high: float
) -> np.ndarray:
    """Bandpass filter

    Butterworth 5th order zero phase bandpass filter

    Parameters
    -----------
    x: np.ndarray
        data array, shape (channels, time)
    sampling_freq: float
        data sampling rate
    freq_low: float
        frequency to filter from
    freq_high: float
        frequency to filter to


    Returns
    -----------
    np.ndarray
        filtered data, shape (channels, time)

    Warnings
    ---------
    Data must be detrended or passed through ba_bci_connect_ewma_standartize
    before applying notch filter

    """
    chans = x.shape[0]
    time_points = x.shape[1]
    _x = x.copy().ravel(order="C").astype(np.float64)
    c_arr = np.ctypeslib.as_ctypes(_x)
    _dll.ba_bci_connect_filter_bandpass(
        c_arr,
        ctypes.c_size_t(chans),
        ctypes.c_size_t(time_points),
        ctypes.c_double(sampling_freq),
        ctypes.c_double(freq_low),
        ctypes.c_double(freq_high),
    )
    return np.array(c_arr[: chans * time_points]).reshape((chans, time_points))


def filter_highpass(x: np.ndarray, sampling_freq: float, freq: float) -> np.ndarray:
    """High-pass filter

    Butterworth 5th order zero phase high-pass filter

    Parameters
    -----------
    x: np.ndarray
        data array, shape (channels, time)
    sampling_freq: float
        data sampling rate
    freq: float
        edge frequency

    Returns
    -----------
    np.ndarray
        filtered data, shape (channels, time)

    Warnings
    ---------
    Data must be detrended or passed through ba_bci_connect_ewma_standartize
    before applying notch filter

    """
    chans = x.shape[0]
    time_points = x.shape[1]
    _x = x.copy().ravel(order="C").astype(np.float64)
    c_arr = np.ctypeslib.as_ctypes(_x)
    _dll.ba_bci_connect_filter_highpass(
        c_arr,
        ctypes.c_size_t(chans),
        ctypes.c_size_t(time_points),
        ctypes.c_double(sampling_freq),
        ctypes.c_double(freq),
    )
    return np.array(c_arr[: chans * time_points]).reshape((chans, time_points))


def filter_lowpass(x: np.ndarray, sampling_freq: float, freq: float) -> np.ndarray:
    """Low-pass filter

    Butterworth 5th order zero phase low-pass filter

    Parameters
    -----------
    x: np.ndarray
        data array, shape (channels, time)
    sampling_freq: float
        data sampling rate
    freq: float
        edge frequency

    Returns
    -----------
    np.ndarray
        filtered data, shape (channels, time)

    Warnings
    ---------
    Data must be detrended or passed through ba_bci_connect_ewma_standartize
    before applying notch filter

    """
    chans = x.shape[0]
    time_points = x.shape[1]
    _x = x.copy().ravel(order="C").astype(np.float64)
    c_arr = np.ctypeslib.as_ctypes(_x)
    _dll.ba_bci_connect_filter_lowpass(
        c_arr,
        ctypes.c_size_t(chans),
        ctypes.c_size_t(time_points),
        ctypes.c_double(sampling_freq),
        ctypes.c_double(freq),
    )
    return np.array(c_arr[: chans * time_points]).reshape((chans, time_points))


def fft(x: np.ndarray, sampling_freq: float) -> dict:
    """Compute the discrete Fourier Transform (DFT) with the efficient Fast Fourier Transform (FFT) algorithm

    Parameters
    -----------
    x: np.ndarray
        data array, shape (channels, time)
    sampling_freq: float
        data sampling rate

    Returns
    -----------
    dict
        dictionary (key: value)
        - freq: frequencies
        - mag: amplitudes
        - phase: phases

    """
    chans = x.shape[0]
    time_points = x.shape[1]
    _x = x.copy().ravel(order="C").astype(np.float64)
    c_arr = np.ctypeslib.as_ctypes(_x)
    n_time_steps = (time_points - (time_points % 2)) // 2 + 1
    c_result_mag = np.ctypeslib.as_ctypes(np.zeros(chans * n_time_steps))
    c_result_phase = np.ctypeslib.as_ctypes(np.zeros(chans * n_time_steps))
    _dll.ba_bci_connect_fft(
        c_arr, chans, time_points, sampling_freq, c_result_mag, c_result_phase
    )
    freqs = np.linspace(0, sampling_freq / 2, n_time_steps)
    mags = np.array(c_result_mag[: chans * n_time_steps]).reshape((chans, n_time_steps))
    phases = np.array(c_result_phase[: chans * n_time_steps]).reshape(
        (chans, n_time_steps)
    )
    return {"freq": freqs, "mag": mags * 2, "phase": phases}


def cut_into_epochs(
    data: np.ndarray,
    sfreq: float,
    epoch_length: Optional[float] = None,
    overlap: float = 0.5,
) -> np.ndarray:
    """Cut data into epochs

    Args:
      data: np.ndarray: (n_channels, n_times)
      sfreq: float:
        sampling frequency
      epoch_len: float:  (Default value = 1.0)
        length of epoch in seconds
      overlap: float:  (Default value = 0.0)
        ratio of overlap between epochs

    Returns:
      output: np.ndarray: (n_epochs, n_channels, n_times)

    """
    if data.ndim == 1:
        data = data.reshape((1, -1))
    if data.ndim > 2:
        raise BrainAccessException("data must be 1D or 2D")
    n_channels = data.shape[0]
    n_times = data.shape[1]
    if epoch_length is None:
        _epoch_length = n_times / sfreq
        if _epoch_length > 15.0:
            _epoch_length = 5
    else:
        _epoch_length = epoch_length
    _epoch_length = int(_epoch_length * sfreq)
    if overlap < 1:
        overlap = 1 - overlap
    else:
        overlap = 1
    n_epochs = int(np.floor(n_times / _epoch_length / overlap))
    epochs = np.zeros((n_epochs, n_channels, _epoch_length))
    for idx, _ in enumerate(epochs):
        dat = data[
            :,
            int(idx * _epoch_length * overlap) : int(idx * _epoch_length * overlap)
            + _epoch_length,
        ]
        if dat.shape[1] == _epoch_length:
            epochs[idx] = dat
    return epochs


def get_bands(
    data: np.ndarray,
    sfreq: float,
    epoch_length: Optional[float] = None,
    overlap: float = 0.1,
    normalize: bool = False,
):
    """EEG power in delta, theta, alpha, beta and gamma frequency bands for each channel

    Args:
      data: np.ndarray: (n_channels, n_times)
      sfreq: float:
        sampling frequency
      epoch_length: Optional[float]:  (Default value = None)
        To reduce noise, data is cut into epochs and mean power values calculated
        If None, epoch length is 5 seconds for data longer then 15 seconds,
        otherwise all data is used without epoching
      overlap: float:  (Default value = 0.1)
        Ratio of overlap between epochs
      normalize: bool:  (Default value = False)
        Normalize power in each frequency band by total power

    Returns:
        output: dict:
            - delta: np.ndarray (n_channels)
            - theta: np.ndarray (n_channels)
            - alpha: np.ndarray (n_channels)
            - beta: np.ndarray (n_channels)
            - gamma: np.ndarray (n_channels)

    """
    # cut into epochs to average out noise
    data = cut_into_epochs(data, sfreq, epoch_length=epoch_length, overlap=overlap)
    # calculate power in each frequency band
    _bands = []
    for epoch in data:
        epoch = demean(epoch)
        _bands.append(
            get_pow_freq_bands(
                epoch,
                sfreq,
                freq_bands=np.array([0.5, 4.0, 8.0, 13.0, 30.0, 100.0]),
                normalize=normalize,
            )
        )
    # average over epochs
    bands = np.array(_bands)
    bands = np.mean(bands, axis=0)
    return {
        "delta": list(bands[:, 0]),
        "theta": list(bands[:, 1]),
        "alpha": list(bands[:, 2]),
        "beta": list(bands[:, 3]),
        "gamma": list(bands[:, 4]),
    }


def get_pow_freq_bands(
    data: np.ndarray,
    sfreq: float,
    freq_bands: np.ndarray = np.array([0.5, 4.0, 8.0, 13.0, 30.0, 100.0]),
    normalize: bool = False,
) -> np.ndarray:
    """Power Spectrum (computed by frequency bands).

    Args:
      data: np.ndarray: (n_channels, n_times)
      sfreq: float:
        sampling frequency
      freq_bands: np.ndarray:  (Default value = np.array([0.5, 4.0, 8.0, 13.0, 30.0,
      100.0])):
        frequency intervals defining bands: delta, theta, alpha, beta, gamma (default)
      normalize: bool:  (Default value = True)
        normalize power in each frequency band by total power

    Returns:
      output: ndarray, shape (n_channels, (len(freq_bands)- 1),)

    """
    n_channels = data.shape[0]
    fb = np.zeros((len(freq_bands) - 1, 2))
    for idx, x in enumerate(freq_bands[:-1]):
        fb[idx, 0] = x
        fb[idx, 1] = freq_bands[idx + 1]
    n_freq_bands = fb.shape[0]
    # fft
    fft_data = fft(data, sfreq)
    freqs = fft_data["freq"]
    psd = fft_data["mag"] ** 2
    # power in each frequency band
    pow_freq_bands = np.empty((n_channels, n_freq_bands))
    for j in range(n_freq_bands):
        mask = np.logical_and(freqs >= fb[j, 0], freqs <= fb[j, 1])
        psd_band = psd[:, mask]
        pow_freq_bands[:, j] = np.sum(psd_band, axis=-1)
    if normalize:
        pow_freq_bands = np.divide(pow_freq_bands, np.sum(psd, axis=-1)[:, None])
    return pow_freq_bands
