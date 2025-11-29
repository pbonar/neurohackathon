import numpy as np

from brainaccess.connect import processor


sampling_rate = 250
t = np.arange(0, 5, step=1.0 / (sampling_rate))
wave = 10 * np.sin(np.pi * 2 * 5 * t)
wave += 100 * np.sin(np.pi * 2 * 23 * t)
wave = wave.reshape(5, sampling_rate) + 2
wave2 = 10 * np.sin(np.pi * 2 * 5 * t).reshape(5, sampling_rate) + 2
data = np.stack([wave, wave2], axis=2)
data = np.moveaxis(data, 2, 0)


# Calculate mean of the data

mean = processor.mean(data[0, :, :])

# Filter data

data_filtered = processor.filter_bandpass(data, sampling_rate, 48, 52)

# Calculate fft

data_fft = processor.fft(data, sampling_rate)["mag"]
