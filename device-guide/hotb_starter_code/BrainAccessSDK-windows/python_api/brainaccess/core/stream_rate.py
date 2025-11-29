from enum import Enum


class StreamRate(Enum):
    """Enumeration of the available sample rates for the device's amplifiers.

    Attributes
    ----------
    X16kHz : int
        16000 samples per second.
    X8kHz : int
        8000 samples per second.
    X4kHz : int
        4000 samples per second.
    X2kHz : int
        2000 samples per second.
    X1kHz : int
        1000 samples per second.
    X500Hz : int
        500 samples per second.
    X250Hz : int
        250 samples per second.
    UNKNOWN : int
        An unknown or unsupported stream rate.
    """
    X16kHz = 0
    X8kHz = 1
    X4kHz = 2
    X2kHz = 3
    X1kHz = 4
    X500Hz = 5
    X250Hz = 6
    UNKNOWN = 0xFF

    @property
    def to_hz(self) -> int:
        """Gets the sample rate frequency in Hz.

        Returns
        -------
        int
            The frequency in Hertz, or -1 if the rate is unknown.
        """
        _map = {
            StreamRate.X16kHz: 16000,
            StreamRate.X8kHz: 8000,
            StreamRate.X4kHz: 4000,
            StreamRate.X2kHz: 2000,
            StreamRate.X1kHz: 1000,
            StreamRate.X500Hz: 500,
            StreamRate.X250Hz: 250,
        }
        return _map.get(self, -1)

    @classmethod
    def from_hz(cls, hz: int) -> "StreamRate":
        """Creates a StreamRate instance from a frequency in Hz.

        Parameters
        ----------
        hz : int
            The frequency in Hertz.

        Returns
        -------
        StreamRate
            The corresponding StreamRate member, or UNKNOWN if not found.
        """
        _hz_map = {
            16000: cls.X16kHz,
            8000: cls.X8kHz,
            4000: cls.X4kHz,
            2000: cls.X2kHz,
            1000: cls.X1kHz,
            500: cls.X500Hz,
            250: cls.X250Hz,
        }
        return _hz_map.get(hz, cls.UNKNOWN)
