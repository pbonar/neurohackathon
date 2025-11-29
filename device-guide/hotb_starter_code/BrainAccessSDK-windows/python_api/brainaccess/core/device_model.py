import enum


class DeviceModel(enum.Enum):
    """Enumeration of the different BrainAccess device models.

    This enum provides a clear and standardized way to identify the specific
    model of a BrainAccess device.

    Attributes
    ----------
    MINI : int
        BrainAccess MINI
    MIDI : int
        BrainAccess MIDI (16 Channels)
    MAXI : int
        BrainAccess MAXI (32 Channels)
    EMG : int
        BrainAccess EMG
    HALO1 : int
        BrainAccess Halo v1
    HALO : int
        BrainAccess Halo
    UNKNOWN : int
        An unknown or unsupported device.
    """
    MINI = 0
    MIDI = 1
    MAXI = 2
    EMG = 3
    HALO1 = 4
    HALO = 5
    UNKNOWN = 0xFF
