/**
 * @file full_battery_info.h
 * @author Neurotechnology (brainaccess@neurotechnology.com)
 * @brief Full battery info
 *
 * @copyright Copyright (c) 2022 Neurotechnology
 */

#pragma once

#ifndef __cplusplus
#include <stdbool.h>
#endif //__cplusplus

#include <stdint.h>

/**
 * @brief Enumerator containing battery charging state
 */
typedef enum e_ba_charge_states_t
{
	e_ba_charge_states_first = 0, ///< Battery charging state first element
	e_ba_charge_states_unknown =
		e_ba_charge_states_first,          ///< Battery charging state unknown
	e_ba_charge_states_charging,           ///< Battery charging state charging
	e_ba_charge_states_discharging_active, ///< Battery charging state
										   ///< discharging active
	e_ba_charge_states_discharging_inactive, ///< Battery charging state
											 ///< discharging inactive
	e_ba_charge_states_last ///< Battery charging state last element
} e_ba_charge_states_t;

/**
 * @brief Enumerator containing battery level status
 */
typedef enum e_ba_charge_level_t
{
	e_ba_charge_level_first = 0, ///< Battery level status first
	e_ba_charge_level_unknown =
		e_ba_charge_level_first, ///< Battery level status unknown
	e_ba_charge_level_good,      ///< Battery level status good
	e_ba_charge_level_low,       ///< Battery level status low
	e_ba_charge_level_critical,  ///< Battery level status critical
	e_ba_charge_level_last       ///< Battery level last
} e_ba_charge_level_t;

/**
 * @brief Struct containing extended battery information received from the
 * device
 */
typedef struct
{
	bool is_charger_connected; ///< True if charger is connected to the device
	uint8_t level;             ///< Battery charge percentage, 0-100
	float health;              ///< Battery health percentage, 0-100
	float voltage;             ///< Battery voltage in volts
	float current; ///< Current flow in amps (negative means discharge)
	e_ba_charge_states_t charging_state; ///< Charging state
	e_ba_charge_level_t charge_level;    ///< Charging level
} ba_full_battery_info;
