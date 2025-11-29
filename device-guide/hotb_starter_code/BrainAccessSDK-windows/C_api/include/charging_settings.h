#pragma once

#ifndef __cplusplus
#include <stdbool.h> // Include for boolean type support in C
#endif               // __cplusplus
#include <stdint.h>  // Include for fixed-width integer types

/**
 * \struct ba_charging_settings
 * \brief Represents the charging settings for a device.
 *
 * This structure contains configuration options related to the device's
 * behavior while charging and its sleep timeout settings.
 */
typedef struct
{
	bool enabled_on_while_charging; ///< Indicates if the device is usable while
									///< charging.
	uint8_t
		sleep_timeout; ///< Sleep timeout in minutes.
					   ///< If the device is not used for this time, it will go
					   ///< to sleep. This is part of the charging settings.
} ba_charging_settings;
