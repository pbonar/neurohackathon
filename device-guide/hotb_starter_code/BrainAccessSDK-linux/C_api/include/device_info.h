/**
 * @file device_info.h
 * @author Neurotechnology (brainaccess@neurotechnology.com)
 * @brief BrainAccess device info
 *
 * @copyright Copyright (c) 2022 Neurotechnology
 */

#pragma once

#include "device_model.h"
#include "version.h"
#include <stddef.h>

/**
 * @brief Struct containing device information
 */
typedef struct
{
	ba_device_model id;          ///< Device model number
	ba_version hardware_version; ///< Hardware version
	ba_version firmware_version; ///< Firmware version
	size_t serial_number;        ///< Device serial number
	size_t sample_per_packet;    ///< Samples per packet
} ba_device_info;
