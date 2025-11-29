// This is the main file for a Bluetooth EEG system application, connection
// example. It includes necessary headers, defines sleep functions, and
// initializes variables.

#include "bacore.h"      // Include the core library
#include "eeg_manager.h" // Include the EEG manager library
#include <stdio.h>       // Include standard I/O library for printing
#include <string.h>      // Include string manipulation functions

#ifdef _WIN32
#include <windows.h> // Windows-specific sleep function
#define sleep_ms(x) Sleep(x)
#else
#include <unistd.h>                    // POSIX (Linux/Unix) sleep function
#define sleep_ms(x) usleep((x) * 1000) // usleep takes microseconds
#endif

#define DEVICE_NAME    "BA MINI 018"
#define DEVICE_CHANNEL 4
#define RUNTIME        5
ba_eeg_manager* manager1;

/**
 * @brief Callback function to handle EEG data chunks.
 *
 * This function processes the EEG data received in chunks. It extracts the
 * sample number and channel data, and prints the data for each sample.
 *
 * @param data Pointer to the array of data pointers for each channel.
 * @param size Number of samples in the data chunk.
 * @param user_data User-defined data (not used in this function).
 */
static void chunk_callback(const void* const* data, size_t size, void* user_data)
{
	// Get the data for the sample number and channels
	const size_t* eeg_data_sample_number = (const size_t*)data[ba_eeg_manager_get_channel_index(manager1, BA_EEG_CHANNEL_ID_SAMPLE_NUMBER)];

	for (size_t i = 0; i < size; ++i)
	{
		// Process the data directly without storing it in a structure
		printf("[%zu]", eeg_data_sample_number[i]);
		for (int j = 0; j < DEVICE_CHANNEL; ++j)
		{
			const double* eeg_data_channel = (const double*)data[ba_eeg_manager_get_channel_index(manager1, BA_EEG_CHANNEL_ID_ELECTRODE_MEASUREMENT + j)];
			printf(" %f", eeg_data_channel[i]);
		}
		printf("\n");
	}
}

/**
 * @brief Callback function to handle disconnection events.
 *
 * This function is called when the EEG device is disconnected. It prints a
 * message indicating that the device has been disconnected.
 *
 * @param data User-defined data (not used in this function).
 */
void disconnect_callback(void* data)
{
	printf("Disconnected\n");
}

// Main function to run the Bluetooth EEG system application
int main()
{
	ba_core_init();                    // Initialize the core  library
	ba_ble_device* device_list = NULL; // Pointer to the list of Bluetooth devices
	size_t device_list_size = 0;       // Size of the device list
	ba_init_error status_core = ba_core_scan(&device_list,
											 &device_list_size); // Scan for available Bluetooth devices

	printf("Scan returned with status: %d | device count: %zu\n", status_core,
		   device_list_size); // Print scan status and device count
	printf("Printing device list: \n");
	for (size_t i = 0; i < device_list_size; ++i)
	{
		printf("device %zu name: %s MAC: %s \n", i, device_list[i].name,
			   device_list[i].mac_address); // Print each device's name and MAC address
	}

	manager1 = ba_eeg_manager_new();                            // Create a new EEG manager instance
	ba_callback_disconnect disconnect_cb = disconnect_callback; // Define the disconnect callback function
	ba_eeg_manager_set_callback_disconnect(manager1, disconnect_cb,
										   NULL); // Set the disconnect callback for the EEG manager
	uint8_t status = BA_ERROR_OK;                 // Initialize the status variable

	status = ba_eeg_manager_connect(manager1, DEVICE_NAME, NULL, NULL); // Connect to the EEG device
	if (status != BA_ERROR_OK)
	{
		printf("Failed to connect with error: %d\n",
			   status); // Print an error message if connection fails
	}

	printf("Connected\n"); // Print a message indicating successful connection

	// Enable and set the gain for all electrode channels
	for (int i = 0; i < DEVICE_CHANNEL; ++i)
	{
		// Enable electrode contact channel
		ba_eeg_manager_set_channel_enabled(manager1, BA_EEG_CHANNEL_ID_ELECTRODE_CONTACT + i, true);
		// Enable electrode measurement channel
		ba_eeg_manager_set_channel_enabled(manager1, BA_EEG_CHANNEL_ID_ELECTRODE_MEASUREMENT + i, true);
		// Set gain for electrode measurement channel
		ba_eeg_manager_set_channel_gain(manager1, BA_EEG_CHANNEL_ID_ELECTRODE_MEASUREMENT + i, BA_GAIN_MODE_X8);
	}

	// Enable sample number channel
	ba_eeg_manager_set_channel_enabled(manager1, BA_EEG_CHANNEL_ID_SAMPLE_NUMBER, true);
	// Enable streaming channel
	ba_eeg_manager_set_channel_enabled(manager1, BA_EEG_CHANNEL_ID_STREAMING, true);

	// Load the configuration
	ba_eeg_manager_load_config(manager1, NULL, NULL);

	// Define the callback function for handling EEG data chunks
	ba_callback_chunk my_callback = chunk_callback;

	// Set the callback function for handling EEG data chunks
	ba_eeg_manager_set_callback_chunk(manager1, my_callback, manager1);

	// Start the EEG data streaming

	printf("start stream returned %d\n", ba_eeg_manager_start_stream(manager1, NULL, NULL));

	printf("stream_start\n");

	// Stop the EEG data streaming after 5 seconds
	for (size_t i = 0; i < RUNTIME; i++)
	{
		printf("sec: %d started\n", i);
		sleep_ms(1000 * 1);
	}
	ba_eeg_manager_stop_stream(manager1, NULL, NULL);
	printf("stream_stop\n");

	ba_eeg_manager_disconnect(manager1); // Disconnect from the EEG device
	ba_core_close();                     // Close the core  library
	printf("Core closed.\n");            // Print a message indicating the core has been
										 // closed

	return status; // Return the status code
}
