""" EEG measurement example

Example how to get measurements and
save to fif format
using acquisition class from brainaccess.utils

Change Bluetooth device name
"""

import matplotlib.pyplot as plt
import matplotlib
import time

from brainaccess.utils import acquisition
from brainaccess.core.eeg_manager import EEGManager

matplotlib.use("TKAgg", force=True)

eeg = acquisition.EEG()

# define electrode locations depending on your device
halo: dict = {
    0: "Fp1",
    1: "Fp2",
    2: "O1",
    3: "O2",
}

cap: dict = {
 0: "F3",
 1: "F4",
 2: "C3",
 3: "C4",
 4: "P3",
 5: "P4",
 6: "O1",
 7: "O2",
}

# define device name
device_name = "BA MINI 047"

# start EEG acquisition setup
with EEGManager() as mgr:
    eeg.setup(mgr, device_name=device_name, cap=cap, sfreq=250)

    # Start acquiring data
    eeg.start_acquisition()
    print("Acquisition started")
    time.sleep(3)

    start_time = time.time()
    annotation = 1
    while time.time() - start_time < 5:
        time.sleep(1)
        # send annotation to the device
        print(f"Sending annotation {annotation} to the device")
        eeg.annotate(str(annotation))
        annotation += 1

    print("Preparing to plot data")
    time.sleep(2)

    # get all eeg data and stop acquisition
    eeg.get_mne()
    eeg.stop_acquisition()
    mgr.disconnect()

# Access MNE Raw object
mne_raw = eeg.data.mne_raw
print(f"MNE Raw object: {mne_raw}")

# Access data as NumPy arrays
data, times = mne_raw.get_data(return_times=True)
print(f"Data shape: {data.shape}")

# save EEG data to MNE fif format
eeg.data.save(f'./data/{time.strftime("%Y%m%d_%H%M")}-raw.fif')
# Close brainaccess library
eeg.close()
# conversion to microvolts
mne_raw.apply_function(lambda x: x*10**-6)
# Show recorded data
mne_raw.filter(1, 40).plot(scalings="auto", verbose=False)
plt.show()