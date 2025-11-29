/**
 * @file eeg_manager.h
 * @author Neurotechnology (brainaccess@neurotechnology.com)
 * @brief EEG device manager
 *
 * @copyright Copyright (c) 2022 Neurotechnology
 */

#pragma once
#include "charging_settings.h"

#ifndef __cplusplus
#include <stdbool.h>
#endif //__cplusplus

#include "annotation.h"
#include "battery_info.h"
#include "callbacks.h"
#include "device_info.h"
#include "dllexport.h"
#include "eeg_channel.h"
#include "error.h"
#include "gain_mode.h"
#include "impedance_measurement_mode.h"
#include "polarity.h"
#include "stream_rate.h"
/**
 * @brief EEG manager typedef. Note that the EEG manager is not thread-safe.
 */
typedef void ba_eeg_manager;

#ifdef __cplusplus
extern "C"
{
#endif //__cplusplus

	/**
	 * @brief Creates a new instance of an EEG manager.
	 * @return A pointer to a new instance of the EEG manager. Returns nullptr
	 * if the allocation fails.
	 */
	BA_CORE_DLL_EXPORT ba_eeg_manager* ba_eeg_manager_new() NOEXCEPT;

	/**
	 * @brief Frees the memory associated with the specified EEG manager
	 * instance.
	 *
	 * This function deallocates the resources used by the provided EEG manager.
	 * Ensure that the instance is no longer in use before calling this
	 * function.
	 *
	 * @param instance A pointer to the EEG manager instance to be freed. The
	 * pointer must point to an instance created earlier, and it should not be
	 * accessed after this function is called.
	 */
	BA_CORE_DLL_EXPORT void
	ba_eeg_manager_free(ba_eeg_manager* instance) NOEXCEPT;

	/**
	 * @brief Connects to a device and attempts to initialize it.
	 *
	 * @details
	 * You must wait for the callback to complete before doing anything else
	 * with the EEG manager. The boolean parameter of the callback is true if
	 * the connection is successful, false otherwise.
	 *
	 * @param instance Handle of the EEG manager instance to connect to the port
	 * @param device_name Brainaccess device name
	 * @param callback Function to be called after the connection succeeds
	 * @param data Data to be passed to the callback
	 * @return status if device compatible
	 */
	BA_CORE_DLL_EXPORT ba_error ba_eeg_manager_connect(
		ba_eeg_manager* instance, const char* device_name,
		ba_callback_future_bool callback, void* data) NOEXCEPT;

	/**
	 * @brief Disconnects the EEG manager instance, terminating any active
	 * connection.
	 *
	 * @param instance A pointer to the EEG manager instance to disconnect.
	 */
	BA_CORE_DLL_EXPORT void
	ba_eeg_manager_disconnect(ba_eeg_manager* instance) NOEXCEPT;

	/**
	 * @brief Checks if the EEG manager instance is currently connected.
	 *
	 * @param instance A pointer to the EEG manager instance to check. Must not
	 * be null.
	 *
	 * @return True if the EEG manager is connected, false otherwise.
	 */
	BA_CORE_DLL_EXPORT bool
	ba_eeg_manager_is_connected(ba_eeg_manager* instance) NOEXCEPT;

	/**
	 * @brief Starts streaming EEG data using the given EEG manager instance.
	 *
	 * @details
	 * Initiates data streaming using the current in-memory configuration
	 * (enabled channels, gains, bias, impedance mode, and data stream rate).
	 * If not explicitly configured since the last stop or disconnect, defaults
	 * are used where applicable (e.g., impedance measurement off; default data
	 * stream rate is 250 Hz).
	 *
	 * Requirements:
	 * - The manager must be connected.
	 * - Do not call if a stream is already running.
	 * - Wait for the callback to complete before issuing further streaming
	 *   calls.
	 *
	 * @param instance A pointer to the EEG manager instance.
	 * @param callback The callback function invoked after the stream start
	 * completes.
	 * @param data User-defined data passed to the callback.
	 * @return A ba_error indicating the outcome of the operation.
	 *
	 * Possible return values:
	 * @retval BA_ERROR_OK Streaming started successfully.
	 * @retval BA_ERROR_CONNECTION The device is not connected, or a connection
	 * error occurred while starting the stream.
	 * @retval BA_ERROR_WRONG_VALUE The current configuration is invalid for
	 * streaming.
	 * @retval BA_ERROR_CORE_NOT_INITIALIZED Core isn't initialized.
	 * @retval BA_ERROR_BLUETOOTH_DISABLED Bluetooth is disabled on the host.
	 * @retval BA_ERROR_BLUETOOTH_ADAPTER_NOT_FOUND No Bluetooth adapter found.
	 * @retval BA_ERROR_ADAPTER_OUT_OF_INDEX Selected adapter index is invalid.
	 * @retval BA_ERROR_UNKNOWN An unspecified error occurred.
	 */

	BA_CORE_DLL_EXPORT ba_error ba_eeg_manager_start_stream(
		ba_eeg_manager* instance, ba_callback_future_void callback,
		void* data) NOEXCEPT;

	/**
	 * @brief Stops streaming EEG data using the given EEG manager instance.
	 *
	 * @details
	 * Requests the device to stop data streaming. After a successful stop,
	 * volatile per-stream configuration is cleared. To start streaming again,
	 * re-apply channel enables, gains, bias selection, impedance mode, and
	 * data stream rate as needed.
	 *
	 * Requirements:
	 * - The manager must be connected.
	 * - A stream must be currently running.
	 * - Do not call repeatedly without a new start in between.
	 * - Wait for the callback to complete before issuing further streaming
	 *   calls.
	 *
	 * @param instance A pointer to the EEG manager instance.
	 * @param callback The callback function invoked after the stream stop
	 * completes.
	 * @param data User-defined data passed to the callback.
	 * @return A ba_error indicating the outcome of the operation.
	 *
	 * Possible return values:
	 * @retval BA_ERROR_OK Streaming stopped successfully.
	 * @retval BA_ERROR_CONNECTION The device is not connected, or a connection
	 * error occurred while stopping the stream.
	 * @retval BA_ERROR_WRONG_VALUE The operation is invalid in the current
	 * state (e.g., stream not running).
	 * @retval BA_ERROR_CORE_NOT_INITIALIZED Core isn't initialized.
	 * @retval BA_ERROR_BLUETOOTH_DISABLED Bluetooth is disabled on the host.
	 * @retval BA_ERROR_BLUETOOTH_ADAPTER_NOT_FOUND No Bluetooth adapter found.
	 * @retval BA_ERROR_ADAPTER_OUT_OF_INDEX Selected adapter index is invalid.
	 * @retval BA_ERROR_UNKNOWN An unspecified error occurred.
	 */

	BA_CORE_DLL_EXPORT ba_error ba_eeg_manager_stop_stream(
		ba_eeg_manager* instance, ba_callback_future_void callback,
		void* data) NOEXCEPT;

	/**
	 * @brief Checks whether EEG data streaming is currently active.
	 *
	 * @details
	 * Provides a non-blocking snapshot of the streaming state. During
	 * start/stop transitions, the state may not reflect the final result until
	 * the corresponding callback has completed.
	 *
	 * Usage notes:
	 * - Safe to call after the manager is created.
	 * - For definitive state after a start/stop request, wait for the
	 *   associated callback and then query this function if needed.
	 *
	 * @param instance A pointer to the EEG manager instance.
	 * @return true if the device is currently streaming, false otherwise.
	 */

	BA_CORE_DLL_EXPORT bool
	ba_eeg_manager_is_streaming(const ba_eeg_manager* instance) NOEXCEPT;

	/**
	 * @brief ba_eeg_manager_get_battery_info — Retrieves the latest battery
	 * status reported by the device.
	 *
	 * @details
	 * Returns the most recently cached battery information. The device
	 * periodically reports its battery status, which the manager stores
	 * internally. This call is synchronous and does not request an update from
	 * the device; it only returns the last known values.
	 *
	 * Defaults and freshness:
	 * - If no battery report has been received yet for this session, the
	 *   returned structure may contain default-initialized values (e.g., zeros
	 *   or unspecified fields depending on the platform).
	 * - To receive updates as they arrive, register a battery update callback
	 *   with ba_eeg_manager_set_callback_battery (pass NULL to unregister),
	 *   and call this function after the callback has been triggered.
	 *
	 * @param instance Handle of the EEG manager to get the battery info of.
	 * @return A ba_battery_info structure with the cached battery information.
	 *
	 * @see ba_eeg_manager_set_callback_battery
	 */

	BA_CORE_DLL_EXPORT ba_battery_info
	ba_eeg_manager_get_battery_info(ba_eeg_manager* instance) NOEXCEPT;

	/**
	 * @brief Loads the current in-memory configuration to the EEG device.
	 *
	 * @details
	 * Sends the manager's current configuration to the device, including
	 * enabled channels, channel gains, bias selection, impedance measurement
	 * mode, and data stream rate. The operation is asynchronous; wait for the
	 * provided callback to complete before issuing additional configuration or
	 * streaming requests.
	 *
	 * How to set values:
	 * - Enable or disable channels with
	 * ba_eeg_manager_set_channel_enabled(instance, ch, state).
	 * - Set channel gains with ba_eeg_manager_set_channel_gain(instance, ch,
	 * gain).
	 * - Select the bias electrode with
	 * ba_eeg_manager_set_channel_bias(instance, ch, polarity).
	 * - Configure impedance measurement with
	 * ba_eeg_manager_set_impedance_mode(instance, mode).
	 * - Set the data stream rate with
	 * ba_eeg_manager_set_data_stream_rate(instance, rate).
	 * - Then call ba_eeg_manager_load_config(instance, callback, data) and wait
	 * for the callback.
	 *
	 * Defaults:
	 * - If a setting has not been explicitly configured since the last stop or
	 *   disconnect, device defaults are applied:
	 *   - Impedance measurement: off by default.
	 *   - Data stream rate: 250 Hz by default.
	 *   - Channels: all enabled.
	 *   - Bias: all disabled.
	 *   - Gains: all set to 8.
	 *
	 * Requirements:
	 * - The manager must be connected.
	 * - Recommended to call when streaming is stopped. If called while a stream
	 *   is running, the device may defer or reject the request; rely on the
	 *   callback result.
	 *
	 * @param instance A pointer to the EEG manager instance.
	 * @param callback The callback invoked once the configuration load
	 * completes.
	 * @param data User-defined data passed to the callback.
	 * @return A ba_error indicating the outcome of the operation.
	 *
	 * Possible return values:
	 * @retval BA_ERROR_OK Configuration applied successfully.
	 * @retval BA_ERROR_CONNECTION The device is not connected, or a connection
	 * error occurred while applying the configuration.
	 * @retval BA_ERROR_WRONG_VALUE The configuration is invalid for the current
	 * state (e.g., not supported while streaming).
	 * @retval BA_ERROR_CORE_NOT_INITIALIZED Core isn't initialized.
	 * @retval BA_ERROR_BLUETOOTH_DISABLED Bluetooth is disabled on the host.
	 * @retval BA_ERROR_BLUETOOTH_ADAPTER_NOT_FOUND No Bluetooth adapter found.
	 * @retval BA_ERROR_ADAPTER_OUT_OF_INDEX Selected adapter index is invalid.
	 * @retval BA_ERROR_UNKNOWN An unspecified error occurred.
	 */

	BA_CORE_DLL_EXPORT ba_error ba_eeg_manager_load_config(
		ba_eeg_manager* instance, ba_callback_future_void callback,
		void* data) NOEXCEPT;

	/**
	 * @brief Retrieves the charging settings of the EEG device.
	 *
	 * @details
	 * Returns the current charging behavior of the device, including whether
	 * the device is allowed to be enabled while charging and the sleep timeout
	 * (in minutes) while charging.
	 *
	 * Defaults and persistence:
	 * - After the device powers off, charging settings revert to defaults:
	 *   - enabled = false
	 *   - timeout = 20 minutes
	 * - If a timeout value of 0 is provided, it is automatically treated as
	 *   1 minute.
	 *
	 * How to set values:
	 * - Prepare a ba_charging_settings structure:
	 *   - settings.enabled = true or false
	 *   - settings.timeout_minutes = desired timeout in minutes (0 becomes 1)
	 * - Apply it with ba_eeg_manager_set_charging_settings(instance, settings).
	 *
	 * @param instance Handle of the EEG Manager instance to retrieve the
	 * charging settings from.
	 * @return A ba_charging_settings structure containing the current
	 * charging settings on the device.
	 *
	 * @see ba_eeg_manager_set_charging_settings
	 */
	BA_CORE_DLL_EXPORT ba_charging_settings
	ba_eeg_manager_get_charging_settings(ba_eeg_manager* instance) NOEXCEPT;

	/**
	 * @brief Updates the charging settings of the EEG device.
	 *
	 * @details
	 * Applies new charging behavior to the device:
	 * - Whether the device is allowed to remain enabled while charging
	 *   (settings.enabled).
	 * - The sleep timeout in minutes while charging (settings.timeout_minutes).
	 *
	 * Defaults and constraints:
	 * - After the device powers off, settings revert to defaults:
	 *   - enabled = false
	 *   - timeout = 20 minutes
	 * - If settings.timeout_minutes is set to 0, it is automatically treated
	 *   as 1 minute.
	 *
	 * How to set values:
	 * - Construct a ba_charging_settings value:
	 *   - ba_charging_settings s; s.enabled = true; s.timeout_minutes = 15;
	 * - Call ba_eeg_manager_set_charging_settings(instance, s).
	 * - Optionally call ba_eeg_manager_get_charging_settings afterward to
	 *   confirm what the device accepted.
	 *
	 * Requirements:
	 * - The manager must be connected.
	 *
	 * @param instance Handle of the EEG Manager instance to configure.
	 * @param settings A ba_charging_settings structure with desired values.
	 * @return true if the settings were successfully applied, false otherwise.
	 *
	 * @see ba_eeg_manager_get_charging_settings
	 */
	BA_CORE_DLL_EXPORT bool ba_eeg_manager_set_charging_settings(
		ba_eeg_manager* instance, ba_charging_settings settings) NOEXCEPT;

	/**
	 * @brief Enables the channel on the device and adds the data to the stream
	 * chunks
	 *
	 * @details This function takes effect on stream start, and its effects are
	 * reset by stream stop. Therefore, it must be called with the appropriate
	 * arguments before every stream starts.
	 *
	 * @param instance Handle of the EEG Manager instance for which to
	 * enable/disable the channel
	 * @param ch Channel ID of the channel to enable/disable
	 * @param state True for enabling, false for disable
	 */

	BA_CORE_DLL_EXPORT void ba_eeg_manager_set_channel_enabled(
		ba_eeg_manager* instance, ba_eeg_channel ch, bool state) NOEXCEPT;

	/**
	 * @brief Sets the gain mode for a specific channel.
	 *
	 * @details
	 * Configures the amplification applied to the selected channel. This
	 * setting is applied on the next stream start and is reset when the stream
	 * stops.
	 *
	 * Notes:
	 * - the configured gain already scales The returned channel data during
	 * streaming.
	 * - If not explicitly configured before the stream starts, the device uses
	 * its default gain for that channel. The default value is 8.
	 *
	 * How to set values:
	 * - Choose the target channel (BA_EEG_CHANNEL_ID_ELECTRODE_MEASUREMENT +
	 * ch) and a supported gain mode (g).
	 * - Call ba_eeg_manager_set_channel_gain(instance,
	 * BA_EEG_CHANNEL_ID_ELECTRODE_MEASUREMENT + ch, g) for each channel you
	 * wish to configure.
	 * - Call ba_eeg_manager_load_config(instance, callback, data) and wait for
	 *   the callback, then start the stream.
	 *
	 * Requirements:
	 * - Call before starting the stream (changes take effect on stream start).
	 * - The manager must be connected for the configuration to be applied to
	 *   the device via load_config.
	 *
	 * @param instance Handle of the EEG Manager instance to configure.
	 * @param ch Channel ID to modify.
	 * @param g Gain mode to set for the specified channel.
	 */
	BA_CORE_DLL_EXPORT void ba_eeg_manager_set_channel_gain(
		ba_eeg_manager* instance, ba_eeg_channel ch, ba_gain_mode g) NOEXCEPT;

	/**
	 * @brief Sets an electrode channel to be used as the bias reference.
	 *
	 * @details
	 * This setting takes effect on the next stream start and is
	 * reset when the stream stops.
	 *
	 * Channel selection:
	 * - Use BA_EEG_CHANNEL_ID_ELECTRODE_MEASUREMENT + ch to target an
	 *   electrode measurement channel, where ch is the zero-based electrode
	 *   index. This ensures the bias is applied to a valid electrode channel.
	 *
	 *
	 * How to set values:
	 * - Compute the target channel as BA_EEG_CHANNEL_ID_ELECTRODE_MEASUREMENT +
	 * ch.

	 * - Call ba_eeg_manager_set_channel_bias(instance, computed_channel).
	 * - Apply settings with ba_eeg_manager_load_config(instance, callback,
	 * data) and wait for the callback, then start streaming.
	 *
	 * Requirements:
	 * - Call before starting the stream (changes take effect on stream start).
	 * - The manager must be connected for the configuration to be pushed using
	 *   load_config.
	 *
	 * @param instance Handle of the EEG Manager instance to configure.
	 * @param ch Channel ID of the electrode to set as bias (use
	 * BA_EEG_CHANNEL_ID_ELECTRODE_MEASUREMENT + index).
	 */

	BA_CORE_DLL_EXPORT void ba_eeg_manager_set_channel_bias(
		ba_eeg_manager* instance, ba_eeg_channel ch) NOEXCEPT;

	/**
	 * @brief Sets electrode impedance measurement mode.
	 *
	 * @details
	 * Prepares the device for electrode impedance measurement by injecting a
	 * small AC current (7 nA at a fixed frequency) through the bias electrodes
	 * to the measurement electrodes. The per-channel voltage response (Vpp)
	 * recorded during streaming can then be used to estimate electrode
	 * impedance using: Impedance = Vpp / 7 nA.
	 *
	 * Modes:
	 * - BA_IMPEDANCE_MEASUREMENT_MODE_OFF: No active impedance measurement.
	 * - BA_IMPEDANCE_MEASUREMENT_MODE_HZ_7_8: 7.8 Hz test wave.
	 * - BA_IMPEDANCE_MEASUREMENT_MODE_HZ_31_2: 31.2 Hz test wave.
	 * - BA_IMPEDANCE_MEASUREMENT_MODE_DR_DIV4: Test wave at sample_rate/4.
	 *
	 * Effect lifetime:
	 * - Takes effect on the next stream start and is reset when the stream
	 *   stops. Call this before every stream where impedance measurement is
	 *   desired.
	 *
	 * How to set values:
	 * - Choose the desired impedance mode (mode).
	 * - Call ba_eeg_manager_set_impedance_mode(instance, mode).
	 * - Apply settings with ba_eeg_manager_load_config(instance, callback,
	 * data) and wait for the callback, then start streaming.
	 *
	 * Requirements and notes:
	 * - Call before starting the stream (changes take effect on stream start).
	 * - The manager must be connected for the configuration to be pushed using
	 *   load_config.
	 * - At least one valid bias electrode should be configured when enabling
	 *   impedance measurement to ensure proper current injection.
	 *
	 * @param instance Handle of the EEG Manager instance for which to set the
	 * mode.
	 * @param mode Impedance measurement mode to set (see a list above).
	 */
	BA_CORE_DLL_EXPORT void ba_eeg_manager_set_impedance_mode(
		ba_eeg_manager* instance, ba_impedance_measurement_mode mode) NOEXCEPT;
	/**
	 * @brief Sets the data stream rate for the EEG device.
	 *
	 * @details
	 * Configures how many samples per second are produced during streaming.
	 * The selected value is applied on the next stream start and does not
	 * change the rate of an already active stream.
	 *
	 * How to set:
	 * - Choose a supported rate from ba_data_stream_rate (e.g., 250 Hz).
	 * - Call ba_eeg_manager_set_data_stream_rate(instance, rate).
	 * - Apply settings with ba_eeg_manager_load_config(instance, callback,
	 * data), wait for the callback to complete, then start streaming.
	 *
	 * How to check:
	 * - Call ba_eeg_manager_get_sample_frequency(instance).
	 *   - Before streaming: returns the configured rate that will be used on
	 * the next start.
	 *   - During streaming: returns the active device sample rate.
	 *
	 * Defaults:
	 * - If not explicitly configured before streaming, the default rate is 250
	 * Hz.
	 *
	 * Requirements and notes:
	 * - Call before starting the stream (changes take effect on stream start).
	 * - The manager must be connected for the configuration to be pushed using
	 * load_config.
	 * - If called while streaming, the new rate will take effect only after the
	 * next successful start_stream following load_config.
	 *
	 * Device-specific supported rates:
	 * - HALO: 250 Hz, 500 Hz
	 * - MINI: 250 Hz, 500 Hz
	 * - MIDI:   250 Hz
	 * - MAXI:   250 Hz
	 *
	 * Attempting to set a rate not supported by the connected device returns an
	 * error and leaves the previously configured rate unchanged.
	 *
	 * @param instance Handle of the EEG Manager instance to set the stream rate
	 * for.
	 * @param rate Desired data stream rate (see ba_data_stream_rate).
	 *
	 * @return ba_error
	 * - BA_ERROR_OK: rate accepted and stored; will apply on the next stream
	 * start.
	 * - BA_ERROR_UNSUPPORTED_DEVICE: a connected device does not support the
	 * requested rate.
	 * - BA_ERROR_INVALID_ARGUMENT: rate value is invalid or out of defined
	 * range.
	 * - BA_ERROR_CONNECTION: not connected when attempting to push
	 * configuration via load_config.
	 * - Other error codes may be returned if underlying operations fail.
	 */

	BA_CORE_DLL_EXPORT ba_error ba_eeg_manager_set_data_stream_rate(
		ba_eeg_manager* instance, ba_data_stream_rate rate) NOEXCEPT;
	/**
	 * @brief Retrieves a pointer to information about the connected EEG device.
	 *
	 * @details
	 * Returns a pointer to a structure describing the currently connected
	 * device. The pointer refers to memory owned by the manager; do not
	 * free or modify the returned data. The contents are updated internally
	 * when the device is initialized or queried.
	 *
	 * Usage and lifetime:
	 * - Valid only after a successful connection.
	 * - The returned pointer remains valid until the device is disconnected
	 *   or the manager is destroyed.
	 * - Treat the data as read-only.
	 *
	 * Requirements:
	 * - The manager must be connected.
	 *
	 * @param instance A pointer to the EEG manager instance.
	 * @return A read-only pointer to a ba_device_info structure describing the
	 *         connected device, or nullptr if no device is connected.
	 */
	BA_CORE_DLL_EXPORT const ba_device_info*
	ba_eeg_manager_get_device_info(const ba_eeg_manager* instance) NOEXCEPT;

	/**
	 * @brief Retrieves a pointer to information about the connected EEG device.
	 *
	 * @details
	 * Returns a pointer to a structure describing the currently connected
	 * device. The pointer refers to memory owned by the manager; do not
	 * free or modify the returned data. The contents are updated internally
	 * when the device is initialized or queried.
	 *
	 * Usage and lifetime:
	 * - Valid only after a successful connection.
	 * - The returned pointer remains valid until the device is disconnected
	 *   or the manager is destroyed.
	 * - Treat the data as read-only.
	 *
	 * Requirements:
	 * - The manager must be connected.
	 *
	 * @param instance A pointer to the EEG manager instance.
	 * @return A read-only pointer to a ba_device_info structure describing the
	 *         connected device, or nullptr if no device is connected.
	 */
	BA_CORE_DLL_EXPORT size_t ba_eeg_manager_get_channel_index(
		const ba_eeg_manager* instance, ba_eeg_channel ch) NOEXCEPT;

	/**
	 * @brief Retrieves the current sample frequency setting of the device.
	 *
	 * @details
	 * Returns the data stream rate that the manager/device will use:
	 * - Before streaming: the configured rate that will be applied on the next
	 *   stream start (as last set by ba_eeg_manager_set_data_stream_rate).
	 * - During streaming: the active device sample rate.
	 *
	 * Defaults:
	 * - If not explicitly configured, the default sample rate is 250 Hz.
	 *
	 * Usage notes:
	 * - Use this to verify the rate you set before starting the stream or to
	 *   check the active rate while streaming.
	 *
	 * @param instance A pointer to the EEG manager instance.
	 * @return The current or active sample frequency as a ba_data_stream_rate
	 * value.
	 */

	BA_CORE_DLL_EXPORT ba_data_stream_rate ba_eeg_manager_get_sample_frequency(
		const ba_eeg_manager* instance) NOEXCEPT;

	/**
	 * @brief Sets a callback invoked whenever a new data chunk is available.
	 *
	 * @details
	 * Registers a function that is called each time the manager assembles a
	 * complete data chunk during streaming. The callback may be executed on an
	 * internal reader/worker thread; keep it short and thread-safe to avoid
	 * blocking device communication. Pass NULL as a callback to disable.
	 *
	 * Chunk size:
	 * - Default chunk size is 25 samples.
	 * - To change it, call ba_core_config_set_chunk_size(size) before starting
	 *   streaming and while no managers are active (requires to be initialized
	 * core).
	 * - Valid range is 1–100 samples. Larger chunks reduce callback frequency
	 *   but increase latency; smaller chunks do the opposite.
	 *
	 * Usage notes:
	 * - Register the callback before starting the stream to avoid missing the
	 *   first chunks.
	 * - The provided data pointer is forwarded to the callback on each
	 *   invocation.
	 * - The callback will stop being invoked after the stream stops or the
	 *   callback is unregistered.
	 *
	 * Threading:
	 * - The thread on which the callback runs is not guaranteed. Protect any
	 *   shared state with synchronization primitives.
	 *
	 * @param instance Handle of the EEG Manager to attach the callback to.
	 * @param callback Function to call for each available chunk (or NULL to
	 *                 unregister).
	 * @param data User-defined pointer passed through to the callback.
	 */
	BA_CORE_DLL_EXPORT void ba_eeg_manager_set_callback_chunk(
		ba_eeg_manager* instance, ba_callback_chunk callback,
		void* data) NOEXCEPT;

	/**
	 * @brief Sets a callback invoked whenever the device reports a battery
	 * update.
	 *
	 * @details
	 * Registers a function called when new battery information is
	 * received from the device. The callback may run on an internal
	 * reader/worker thread; keep it short and thread-safe to avoid blocking
	 * device communication. Pass NULL as callback to disable.
	 *
	 * How it works:
	 * - the device event-drives Battery updates; there is no polling.
	 * - The manager caches the latest battery values. Inside your callback
	 *   (or afterward), call ba_eeg_manager_get_battery_info(instance) to read
	 *   the most recent cached data.
	 *
	 * Usage notes:
	 * - You can register the callback before or after connecting; updates will
	 *   only arrive while connected and when the device publishes them.
	 * - The provided data pointer is forwarded to the callback on each
	 *   invocation.
	 * - The callback stops when the device disconnects, streaming stops (if
	 *   applicable), or when unregistered.
	 *
	 * Threading:
	 * - The execution thread is not guaranteed. Protect shared state with
	 *   synchronization primitives.
	 *
	 * @param instance Handle of the EEG Manager to attach the callback to.
	 * @param callback Function to call on battery updates (or NULL to
	 * unregister).
	 * @param data User-defined pointer passed through to the callback.
	 */

	BA_CORE_DLL_EXPORT void ba_eeg_manager_set_callback_battery(
		ba_eeg_manager* instance, ba_callback_battery callback,
		void* data) NOEXCEPT;

	/**
	 * @brief Sets a callback invoked when the device disconnects.
	 *
	 * @details
	 * Registers a function to be called whenever the connection to the device
	 * is lost, whether due to an expected user-initiated disconnect or an
	 * unexpected drop (e.g., out of range, power off). The callback may run on
	 * an internal reader/worker thread; keep it short and thread-safe to avoid
	 * blocking device communication. Pass NULL as callback to disable.
	 *
	 * Usage notes:
	 * - You may register the callback before or after connecting.
	 * - The callback is invoked on both graceful and unexpected disconnects.
	 * - The provided data pointer is forwarded to the callback on each
	 *   invocation.
	 * - After the callback returns, the manager remains valid but is no longer
	 *   connected. Reconnect if further interaction is required.
	 *
	 * Threading:
	 * - The execution thread is not guaranteed. Protect shared state with
	 *   synchronization primitives.
	 *
	 * @param instance Handle of the EEG Manager to attach the callback to.
	 * @param callback Function to call on device disconnect (or NULL to
	 * unregister).
	 * @param data User-defined pointer passed through to the callback.
	 */

	BA_CORE_DLL_EXPORT void ba_eeg_manager_set_callback_disconnect(
		ba_eeg_manager* instance, ba_callback_disconnect callback,
		void* data) NOEXCEPT;

	/**
	 * @brief Adds an annotation at the current stream timestamp.
	 *
	 * @details
	 * Records the provided text together with the current sample timestamp in
	 * the manager's in-memory annotation list. You can later retrieve all
	 * accumulated annotations using ba_eeg_manager_get_annotations. All
	 * annotations are cleared on device disconnect.
	 *
	 * Calibration notes:
	 * - After starting the stream, wait for a short period to ensure annotation
	 * timestamps are properly calibrated.
	 * - Setting annotations immediately after stream start may result in
	 * inaccurate timestamps.
	 * - Use annotations to mark calibration events (e.g., start/end of
	 * calibration, electrode adjustment) during streaming.
	 * - This helps synchronize calibration steps with recorded EEG data for
	 * later analysis.
	 *
	 * Usage notes:
	 * - Call only while streaming; before stream start the current timestamp is
	 *   undefined and the operation may fail.
	 * - Keep annotation strings reasonably short to avoid unnecessary memory
	 *   usage.
	 *
	 * Requirements:
	 * - The manager must be connected and streaming.
	 *
	 * @param instance Handle of the EEG Manager to add an annotation to.
	 * @param annotation Null-terminated string to record as the annotation
	 * text.
	 * @return A ba_error indicating the outcome of the operation.
	 *
	 * Possible return values:
	 * @retval error::OK Annotation recorded successfully.
	 * @retval error::CONNECTION Not connected or stream not running.
	 * @retval error::ANNOTATION_UNAVAILABLE_CALIBRATING Annotation unavailable
	 * due to calibration in progress.
	 */

	BA_CORE_DLL_EXPORT ba_error ba_eeg_manager_annotate(
		ba_eeg_manager* instance, const char* annotation) NOEXCEPT;

	/**
	 * @brief Starts an over-the-air (OTA) update process for the EEG device.
	 *
	 * @details
	 * This function initiates the OTA update process, allowing the device's
	 * firmware to be updated. The operation is asynchronous, and the provided
	 * callback is invoked upon completion or failure of the update process.
	 *
	 * Usage notes:
	 * - Ensure the device is connected before calling this function.
	 * - The callback function should handle both success and failure scenarios.
	 * - The `data` parameter allows passing user-defined context to the
	 * callback.
	 *
	 * Requirements:
	 * - The manager must be connected to the device.
	 *
	 * @param instance A pointer to the EEG manager instance initiating the
	 * update.
	 * @param callback A function to be called when the update process
	 * completes. The callback should handle success and error cases.
	 * @param data A user-defined pointer passed to the callback for context.
	 * @return A `ba_error` indicating the outcome of the operation.
	 *
	 * Possible return values:
	 *
	 * - `BA_ERROR_CONNECTION`: Indicates a connection issue, such as the device
	 * not being connected.
	 * - `BA_ERROR_UPDATE_FILE_NOT_FOUND`: The update file required for the
	 * operation could not be located.
	 * - `BA_ERROR_UPDATE_FAILED_DEVICE_DISCONNECTED`: The update process failed
	 * because the device was disconnected.
	 * - `BA_ERROR_UPDATE_INITIATED_UNSUCCESSFULLY`: The update process was
	 * started but was not successful.
	 * - `BA_ERROR_OK`: Indicates that the operation completed successfully.
	 */
	BA_CORE_DLL_EXPORT ba_error ba_eeg_manager_start_update(
		ba_eeg_manager* instance, ba_callback_ota_update callback,
		void* data) NOEXCEPT;

	/**
	 * @brief Retrieves all annotations recorded during the current streaming
	 * session.
	 *
	 * @details
	 * This function provides access to the annotations added during the current
	 * streaming session. Each annotation includes a timestamp and the
	 * associated text. The annotations are cleared when the device disconnects.
	 *
	 * Usage notes:
	 * - Call this function only while the manager is connected.
	 * - The annotations pointer will be populated with an array of annotations,
	 *   and the annotations_size pointer will indicate the number of
	 * annotations.
	 * - The memory for the annotations array is managed by the EEG manager and
	 *   should not be freed by the caller.
	 *
	 * Requirements:
	 * - The manager must be connected and streaming.
	 *
	 * @param instance A pointer to the EEG manager instance.
	 * @param annotations A pointer to a ba_annotation array that will be
	 * populated with the recorded annotations.
	 * @param annotations_size A pointer to a size_t variable that will be set
	 * to the number of annotations.
	 */
	BA_CORE_DLL_EXPORT void ba_eeg_manager_get_annotations(
		const ba_eeg_manager* instance, ba_annotation** annotations,
		size_t* annotations_size) NOEXCEPT;

	/**
	 * @brief Clears all annotations recorded during the current streaming
	 * session.
	 *
	 * @details
	 * This function removes all annotations that were added during the current
	 * streaming session. It is useful for resetting the annotation list without
	 * disconnecting the device. Once cleared, the annotations cannot be
	 * retrieved.
	 *
	 * Usage notes:
	 * - Call this function only while the manager is connected.
	 * - This operation does not affect the streaming state or other
	 * configurations.
	 *
	 * Requirements:
	 * - The manager must be connected.
	 *
	 * @param instance A pointer to the EEG manager instance.
	 */
	BA_CORE_DLL_EXPORT void
	ba_eeg_manager_clear_annotations(ba_eeg_manager* instance) NOEXCEPT;

#ifdef __cplusplus
}
#endif //__cplusplus
