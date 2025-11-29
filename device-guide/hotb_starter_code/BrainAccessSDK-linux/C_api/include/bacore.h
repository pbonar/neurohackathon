/**
 * @file bacore.h
 * @author Neurotechnology (brainaccess@neurotechnology.com)
 * @brief Core library info and lifecycle API
 *
 * @copyright Copyright (c) 2022 Neurotechnology
 */

#pragma once

#include "ble_device.h"
#include "dllexport.h"
#include "error.h"
#include "log_level.h"
#include "version.h"

typedef struct sBACORE_Config_t
{
	size_t log_buffer_size;  /** Size of the log buffer (in bytes). */
	char log_path[200];      /** Path to the log file. Max length is 200*/
	ba_log_level log_level;  /** Log level (2 = Warning). */
	bool append_logs;        /** Appending to log files (false = overwrite). */
	bool timestamps_enabled; /** Enabling timestamps in logs. */
	bool autoflush;          /** Enabling autoflush of logs. */
	bool thread_ids_enabled; /** Including thread IDs in logs. */
	size_t chunk_size;       /** Chunk size for data processing. */
	bool enable_logs;        /** Enabling logging. */
	char update_path[200];   /** Path to the firmware update file. Max length is
								200 */
	uint8_t adapter_index;   /** Bluetooth adapter index (default 0). */
} sBACORE_Config_t;

// Error codes for initialization
#define BA_INIT_ERROR_UNKNOWN              0xFF // Unknown error
#define BA_INIT_ERROR_OK                   0    // Initialized successfully
#define BA_INIT_ERROR_CONFIG_TYPE          1    // Invalid config value type
#define BA_INIT_ERROR_WRONG_ADAPTER_VALUE  2 // Invalid Bluetooth adapter value
#define BA_INIT_ERROR_INCOMPATIBLE_VERSION 3 // Incompatible library version
#define BA_INIT_ERROR_NOT_ENABLED          4 // Bluetooth isn't enabled
#define BA_INIT_ERROR_NOT_FOUND            5 // Bluetooth adapter not found
#define BA_INIT_ERROR_CONFIG_PARSE         6 // Invalid or missing config file
#define BA_INIT_ERROR_INVALID_PATH         8 // Invalid file path

// Warning codes for initialization
#define BA_INIT_WARNING_ALREADY_INITIALIZED 7 // Already initialized

typedef uint8_t ba_init_error; // Type for initialization error codes

#ifdef __cplusplus
extern "C"
{
#endif //__cplusplus

	/**
	 * @brief Initializes the core system of the application.
	 *
	 * This function sets up the core system, ensuring that all necessary
	 * parts and resources are properly initialized. It must be called
	 * before performing any operations that depend on the core system.
	 *
	 * @return A `ba_error` indicating the success or failure of the
	 * initialization. Possible error codes include:
	 *         - error::ALREADY_INITIALIZED: If the core system has already been
	 *           initialized.
	 *         - error::OK: If the core system was successfully initialized.
	 */
	BA_CORE_DLL_EXPORT ba_init_error ba_core_init() NOEXCEPT;

	/**
	 * @brief Retrieves the current core configuration.
	 *
	 * Copies the library's current configuration into the caller-provided
	 * sBACORE_Config_t structure. The core must be initialized with
	 * ba_core_init() before calling this function.
	 *
	 * @param[out] config Pointer to a pre-allocated sBACORE_Config_t structure
	 * that receives the current configuration. Must not be NULL.
	 *
	 * @return A ba_error indicating the result:
	 *         - error::OK: Configuration successfully copied.
	 *         - error::COREX_NOT_INITIALIZED: Core has not been initialized.
	 */
	BA_CORE_DLL_EXPORT ba_error
	ba_core_get_config(sBACORE_Config_t* config) NOEXCEPT;
	/**
	 * @brief Sets the core configuration.
	 *
	 * Applies the provided configuration to the library. The core must be
	 * initialized with ba_core_init() before calling this function. On success,
	 * the logging subsystem is reinitialized, according to the new settings
	 * (log_buffer_size, log_path, append_logs, log_level, timestamps_enabled,
	 * thread_ids_enabled, enable_logs, autoflush). Other fields (e.g.,
	 * adapter_index, chunk_size) affect later operations where relevant.
	 *
	 * @param[in] config Pointer to the configuration to apply. Must not be
	 * NULL.
	 *
	 * @return A ba_error indicating the result:
	 *         - error::OK: Configuration successfully applied.
	 *         - error::COREX_NOT_INITIALIZED: Core has not been initialized.
	 */
	BA_CORE_DLL_EXPORT ba_error
	ba_core_set_config(sBACORE_Config_t* config) NOEXCEPT;

	/**
	 * @brief Retrieves a pointer to the library's version information.
	 *
	 * @details Provides the library's version information, including major,
	 * minor, and patch numbers using semantic versioning. This information can
	 * be used to ensure compatibility.
	 *
	 * @return Pointer to a `ba_version` structure containing the library's
	 * version information.
	 */
	BA_CORE_DLL_EXPORT const ba_version* ba_core_get_version() NOEXCEPT;

	/**
	 * @brief Scans for available Bluetooth devices.
	 *
	 * This function triggers a scan to discover nearby Bluetooth devices and
	 *populates the provided device list with the scan results.
	 *
	 * @param device_list Pointer to an array of ba_ble_device pointers that
	 *will store the discovered devices
	 * @param device_list_size Pointer to size_t that will store the number of
	 *discovered devices
	 *
	 * @return A `ba_error` indicating the success or failure of the scanning
	 * process. Possible error codes include:
	 *	   - error::NOT_INITIALIZED: If the core system has not been
	 *		 initialized before the scan.
	 *	   - error::OK: If the scan was successfully completed.
	 *	   - error::ALREADY_SCANNING: If a scan is already in progress
	 *	   - error::BLUETOOTH_NOT_ENABLED: If Bluetooth is disabled
	 *	   - error::BLUETOOTH_NOT_AVAILABLE: If no Bluetooth adapter is
	 *available
	 *	   - error::INVALID_PARAMETERS: If device_list or device_list_size are
	 *NULL
	 */
	BA_CORE_DLL_EXPORT ba_error ba_core_scan(
		ba_ble_device** device_list, size_t* device_list_size) NOEXCEPT;

	/**
	 * @brief Shuts down the core system of the application.
	 *
	 * This function performs cleanup operations, releasing all resources and
	 * components initialized by the core system. It should be called when
	 * the core system is no longer needed or before application termination.
	 *
	 * @return A `ba_error` indicating the success or failure of the shutdown
	 * process. Possible error codes include:
	 *         - error::NOT_INITIALIZED: If the core system was not initialized
	 * before calling this function.
	 *         - error::OK: If the core system was successfully shut down.
	 */
	BA_CORE_DLL_EXPORT ba_init_error ba_core_close() NOEXCEPT;

#ifdef __cplusplus
}
#endif //__cplusplus
