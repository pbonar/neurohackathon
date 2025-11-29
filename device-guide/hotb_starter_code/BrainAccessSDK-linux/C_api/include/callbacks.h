/**
 * @file callbacks.h
 * @author Neurotechnology (brainaccess@neurotechnology.com)
 * @brief Callback function typedefs
 *
 * @copyright Copyright (c) 2022 Neurotechnology
 */

#pragma once

#ifndef __cplusplus
#include <stdbool.h>
#endif //__cplusplus
#include "battery_info.h"
#include "full_battery_info.h"
#include <stddef.h>
// #include <functional.h>

/**
 * @brief Callback function for handling EEG data stream chunks
 *
 * @param data Pointer to the array of EEG data stream chunk values
 * @param data_size Size of the EEG data stream chunk array
 * @param user_data User-defined data passed to the callback function
 */
typedef void (*ba_callback_chunk)(const void* const*, size_t, void*);

/**
 * @brief Callback function for handling battery information updates
 *
 * @param battery_info Pointer to the battery information structure
 * @param user_data User-defined data passed to the callback function
 */
typedef void (*ba_callback_battery)(const ba_battery_info*, void*);

/**
 * @brief Callback function for handling device disconnection events
 *
 * @param user_data User-defined data passed to the callback function
 */
typedef void (*ba_callback_disconnect)(void*);

/**
 * @brief Callback function for handling future void results
 *
 * @param user_data User-defined data passed to the callback function
 */
typedef void (*ba_callback_future_void)(void*);

typedef void (*ba_callback_ota_update)(void*, const size_t, const size_t);

/**
 * @brief Callback function for handling future boolean results
 *
 * @param result Boolean result
 * @param user_data User-defined data passed to the callback function
 */
typedef void (*ba_callback_future_bool)(bool, void*);

/**
 * @brief Callback function for handling future float results
 *
 * @param result Float result
 * @param user_data User-defined data passed to the callback function
 */
typedef void (*ba_callback_future_float)(float, void*);

/**
 * @brief Callback function for handling future full battery information results
 *
 * @param result Pointer to the full battery information structure
 * @param user_data User-defined data passed to the callback function
 */
typedef void (*ba_callback_future_full_battery_info)(
	const ba_full_battery_info*, void*);
