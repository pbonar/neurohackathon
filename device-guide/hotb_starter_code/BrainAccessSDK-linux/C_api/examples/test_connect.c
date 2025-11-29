// This is the main file for a Bluetooth EEG system application, connection
// example. It includes necessary headers, defines sleep functions, and
// initializes variables.

#include "bacore.h"      // Include the core library
#include "eeg_manager.h" // Include the EEG manager library
#include <stdio.h>       // Include a standard I/O library for printing
#include <string.h>      // Include string manipulation functions

#ifdef _WIN32
#include <windows.h> // Windows-specific sleep function
#define sleep_ms(x) Sleep(x)
#else
#include <unistd.h>                    // POSIX (Linux/Unix) sleep function
#define sleep_ms(x) usleep((x) * 1000) // usleep takes microseconds
#endif

#define DEVICE_NAME "BA MINI 018"
ba_eeg_manager* manager1;

// Callback function for handling disconnection events.
// This function is called when the connection to the device is lost.
// It prints a message indicating the disconnection event.
// Callback function for handling disconnection events.
// This function is called when the connection to the device is lost.
// It prints a message indicating the disconnection event.
void disconnect_callback(void* data)
{
	printf("Disconnected\n");
}

// Main function to run the Bluetooth EEG system application
int main()
{
	ba_core_init();                    // Initialize the core library
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

	const ba_battery_info info = ba_eeg_manager_get_battery_info(manager1); // Get the battery information of the connected device
	printf(
		"battery level: %d | is charger connected: %d | is charging: %d \n", info.level, info.is_charger_connected,
		info.is_charging); // Print battery information

	ba_eeg_manager_disconnect(manager1); // Disconnect from the EEG device
	ba_core_close();                     // Close the core library
	printf("Core closed.\n");            // Print a message indicating the core has been
										 // closed

	return status; // Return the status code
}
