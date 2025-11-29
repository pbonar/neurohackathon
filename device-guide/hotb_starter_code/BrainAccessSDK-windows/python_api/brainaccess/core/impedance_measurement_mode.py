"""Defines the modes for impedance measurement."""
import enum


class ImpedanceMeasurementMode(enum.Enum):
    """Enumeration of the available impedance measurement modes.

    Impedance measurement is used to assess the quality of the electrode-skin
    contact. Different modes use different frequencies for the measurement.

    Attributes
    ----------
    OFF : int
        Impedance measurement is disabled.
    HZ_7_8 : int
        Uses a 7.8 Hz wave for impedance measurement.
    HZ_31_2 : int
        Uses a 31.2 Hz wave for impedance measurement.
    DR_DIV4 : int
        Uses a wave with a frequency of sample_rate / 4 for impedance measurement.
    """
    OFF = 0
    HZ_7_8 = 1
    HZ_31_2 = 2
    DR_DIV4 = 3
