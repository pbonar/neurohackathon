"""Defines the starting addresses of data channels within a data chunk.

This module provides constants that represent the starting indices for different
types of data within a single data chunk. This allows for easy and reliable
access to specific data points, such as EEG measurements, accelerometer values,
and digital input states.

Attributes
----------
SAMPLE_NUMBER : int
    The index of the sample number, which starts at 0 at the beginning of a stream.
ELECTRODE_MEASUREMENT : int
    The starting index for EEG electrode measurement values (in microvolts).
ELECTRODE_CONTACT : int
    The starting index for the contact status of the electrodes.
DIGITAL_INPUT : int
    The starting index for the state of the digital I/O pins.
ACCELEROMETER : int
    The starting index for accelerometer data.
GYROSCOPE : int
    The starting index for gyroscope data.
STREAMING : int
    The index for the streaming status of the device.
ELECTRODE_CONTACT_P : int
    The starting index for the contact status of the positive (P) electrodes.
ELECTRODE_CONTACT_N : int
    The starting index for the contact status of the negative (N) electrodes.

Examples
--------
To get the x, y, and z indices for the accelerometer data within a chunk:

- x: `get_channel_index(ACCELEROMETER + 0)`
- y: `get_channel_index(ACCELEROMETER + 1)`
- z: `get_channel_index(ACCELEROMETER + 2)`
"""
SAMPLE_NUMBER = 0
ELECTRODE_MEASUREMENT = 1
ELECTRODE_CONTACT_P = 513
ELECTRODE_CONTACT = 1025
ELECTRODE_CONTACT_N = 1537
DIGITAL_INPUT = 2049
GYROSCOPE = 2497
ACCELEROMETER = 2561
STREAMING = 2625
