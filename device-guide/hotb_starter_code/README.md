# BrainAccess EEG Device Connection Guide

This document provides step-by-step instructions on how to set up the environment and establish a connection with BrainAccess EEG devices (Halo/Cap) using Python.

## 1. Prerequisites

Before running the scripts, ensure you have the following:
* **Hardware:** BrainAccess Halo or Cap (charged).
* **Connector** USB Connector pluged into your computer.
* **Software:** Python 3.8 or newer.
* **Bluetooth:** A computer with Bluetooth 4.0+ (BLE) support.
* **Device status:** Ensure device's LED is blinking (it informs that device is ready to be connected).
 

## 2. Connection on Windows

Do not pair the device manually via Windows Settings. Let the Python script handle the connection.

If you have previously paired the device:

    Go to Settings > Bluetooth & devices.

    Find the device (e.g., BrainAccess).

    Click Remove device.

Ensure no other software (like BrainAccess Board) is currently connected to the device.

1. Create virtual environment for your project and activate it.

```bash
python -m venv .venv
.venv\Source\activate.bat
```

2. Install BrainAccess SDK via pip manager.
```bash
pip install brainaccess
```

3. Test connectivity by running `test.py` scirpt with appropriate `device_name` and `electrode_locations`.
```bash
python test.py
```

## 3. Connection on Linux

1. Create virtual environment for your project and activate it.

```bash
python3 -m venv venv
source venv/bin/activate
```

2. Install BrainAccess SDK via pip manager.

```bash
pip install brainaccess
```

OR directly from the source files

```bash
pip install ./BrainAccessSDK-linux/python_api
```

3. Test connectivity by running `test.py` scirpt with appropriate `device_name` and `electrode_locations`.

```bash
python3 test.py
```

## 4. How to find device's name?

**ATTENTION**:
If you have trouble finding our device name you can find the device name in the **BrainAccess Board** panel or use a helping script:

```bash 
python device_name_lookup.py
```

> there may be slight connectivity issues. Try rebooting the device after few failed attempts.


for signal processing we recommend [MNE](https://mne.tools/stable/index.html) library.
