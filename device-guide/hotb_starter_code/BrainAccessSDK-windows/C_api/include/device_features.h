/**
 * @file device_features.h
 * @author Neurotechnology (brainaccess@neurotechnology.com)
 * @brief Device features query functionality
 *
 * @copyright Copyright (c) 2022 Neurotechnology
 */

#pragma once

#include "device_info.h"
#include "dllexport.h"
#include <stdint.h>

#ifndef __cplusplus
#include <stdbool.h>
#endif

#ifdef __cplusplus
extern "C"
{
#endif

	/**
	 * @brief Handle to class allowing the user to check what features a
	 * particular device supports
	 */
	typedef void ba_device_features;

	/**
	 * @brief Whether the device can capture accelerometer data
	 *
	 * @param f Device features handle
	 *
	 * @return true if a device has an accelerometer, false otherwise
	 */
	BA_CORE_DLL_EXPORT bool
	ba_core_device_features_has_accel(const ba_device_features* f) NOEXCEPT;

	/**
	 * @brief Whether the device can capture gyroscope data
	 *
	 * @param f Device features handle
	 *
	 * @return true if a device has a gyroscope, false otherwise
	 */
	BA_CORE_DLL_EXPORT bool
	ba_core_device_features_has_gyro(const ba_device_features* f) NOEXCEPT;

	/**
	 * @brief Whether the device's electrodes are bipolar
	 *
	 * @details Bipolar electrodes have separate P (positive) and N
	 * (negative) contacts
	 *
	 * @param f Device features handle
	 *
	 * @return true if electrodes are bipolar, false otherwise
	 */
	BA_CORE_DLL_EXPORT bool
	ba_core_device_features_is_bipolar(const ba_device_features* f) NOEXCEPT;

	/**
	 * @brief Gets the number of EEG/EMG electrodes supported by the device
	 *
	 * @param f Device features handle
	 *
	 * @return Number of electrodes
	 */
	BA_CORE_DLL_EXPORT uint8_t ba_core_device_features_electrode_count(
		const ba_device_features* f) NOEXCEPT;

	/**
	 * @brief Gets a pointer to ba_device_features instance
	 *
	 * @details The pointer is guaranteed to be statically allocated, so no need
	 * to delete or do any kind of memory management.
	 *
	 * @param info Device for which to get features. The serial number is ignored.
	 * @return Pointer to the corresponding ba_device_features instance, or NULL if
	 * the device is not supported
	 */
	BA_CORE_DLL_EXPORT const ba_device_features*
	ba_core_device_features_get(const ba_device_info* info) NOEXCEPT;

#ifdef __cplusplus
}
#endif
