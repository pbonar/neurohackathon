import ctypes
from enum import Enum, unique

from brainaccess.utils.exceptions import BrainAccessException


@unique
class EBaChargeStates(Enum):
    """Enumeration of the possible battery charging states."""
    e_ba_charge_states_unknown = 0
    e_ba_charge_states_charging = 1
    e_ba_charge_states_discharging_active = 2
    e_ba_charge_states_discharging_inactive = 3
    e_ba_charge_states_last = 4


@unique
class EBaChargeLevel(Enum):
    """Enumeration of the battery charge levels."""
    e_ba_charge_level_unknown = 0
    e_ba_charge_level_good = 1
    e_ba_charge_level_low = 2
    e_ba_charge_level_critical = 3
    e_ba_charge_level_last = 4


class FullBatteryInfo(ctypes.Structure):
    """Provides comprehensive information about the device's battery.

    This class extends the basic battery info with more detailed metrics such as
    health, voltage, and current, providing a complete picture of the battery's
    status.

    Attributes
    ----------
    is_charger_connected : bool
        True if a charger is connected to the device.
    level : int
        The battery charge percentage (0-100).
    health : float
        The battery health percentage (0-100).
    voltage : float
        The battery voltage in volts.
    current : float
        The current flow in amps (negative for discharge, positive for charge).
    charge_state : EBaChargeStates
        The current charging state of the battery.
    charge_level : EBaChargeLevel
        The current charge level of the battery.
    """

    _fields_ = [
        ("is_charger_connected", ctypes.c_bool),
        ("level", ctypes.c_uint8),
        ("health", ctypes.c_float),
        ("voltage", ctypes.c_float),
        ("current", ctypes.c_float),
        ("_charge_state", ctypes.c_int),
        ("_charge_level", ctypes.c_int),
    ]

    @property
    def charge_state(self):
        """The current charging state of the battery."""
        return EBaChargeStates(self._charge_state)

    @charge_state.setter
    def charge_state(self, value):
        if isinstance(value, EBaChargeStates):
            self._charge_state = value.value
        else:
            raise BrainAccessException(
                "charge_state must be an instance of EBaChargeStates Enum"
            )

    @property
    def charge_level(self):
        """The current charge level of the battery."""
        return EBaChargeLevel(self._charge_level)

    @charge_level.setter
    def charge_level(self, value):
        if isinstance(value, EBaChargeLevel):
            self._charge_level = value.value
        else:
            raise BrainAccessException(
                "charge_level must be an instance of EBaChargeLevel Enum"
            )
