import enum

class Polarity(enum.Enum):
    """Enumeration of the possible polarities for bipolar electrodes.

    For devices with bipolar electrodes, this enum allows for the selection of
    which contact to use for a given measurement.

    Attributes
    ----------
    NONE : int
        No polarity is selected.
    BOTH : int
        Both positive and negative contacts are used.
    POSITIVE : int
        Only the positive contact is used.
    NEGATIVE : int
        Only the negative contact is used.
    """
    NONE = 0
    BOTH = 1
    POSITIVE = 2
    NEGATIVE = 3
