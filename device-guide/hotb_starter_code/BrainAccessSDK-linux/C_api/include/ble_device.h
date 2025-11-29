/**
 * @file ble_device.h
 * @author Neurotechnology (brainaccess@neurotechnology.com)
 * @brief BrainAccess BLE device
 *
 * @copyright Copyright (c) 2024 Neurotechnology
 */

#pragma once

#include <stddef.h>

/**
 * @brief Struct containing ble device
 */
typedef struct
{
	char* name;        ///< Device name
	char* mac_address; ///< Device MAC address
} ba_ble_device;
