/**
 * @file battery_info.h
 * @author Neurotechnology (brainaccess@neurotechnology.com)
 * @brief Battery info
 *
 * @copyright Copyright (c) 2022 Neurotechnology
 */

#pragma once

#ifndef __cplusplus
#include <stdbool.h>
#endif //__cplusplus

#include <stdint.h>

/**
 * @brief Struct containing standard battery information received from the
 * device
 */
typedef struct
{
	uint8_t level;             ///< Battery charge percentage, 0-100
	bool is_charger_connected; ///< True if charger is connected to the device
	bool is_charging;          ///< True if battery is charging
} ba_battery_info;
