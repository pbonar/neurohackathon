import time
import numpy as np
from scipy.signal import welch, iirnotch, lfilter, butter
from brainaccess.utils import acquisition
from brainaccess.core.eeg_manager import EEGManager
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# --- KONFIGURACJA ---
SFREQ = 250
WINDOW_SIZE = SFREQ * 5  # 5 sekund
DEVICE_NAME = "BA MINI 050"

# Elektrody
electrodes_mini = {0: "Fp1", 1: "Fp2"}

# --- FILTRY ---
def filter_data(data, fs=SFREQ):
    b_notch, a_notch = iirnotch(50.0, 30.0, fs)
    data = lfilter(b_notch, a_notch, data)
    nyq = fs * 0.5
    b_band, a_band = butter(4, [1/nyq, 40/nyq], btype='band')
    data = lfilter(b_band, a_band, data)
    return data

# --- ANALIZA PASM ---
def get_band_power(data, fs, low_f, high_f):
    freqs, psd = welch(data, fs, nperseg=fs)
    idx_min = np.argmax(freqs >= low_f)
    idx_max = np.argmax(freqs >= high_f)
    return float(np.mean(psd[idx_min:idx_max]))

def calculate_metrics(window_data):
    filtered = np.array([filter_data(ch) for ch in window_data])
    avg_data = np.mean(filtered, axis=0)

    theta = get_band_power(avg_data, SFREQ, 4, 8)
    alpha = get_band_power(avg_data, SFREQ, 8, 12)
    beta  = get_band_power(avg_data, SFREQ, 13, 30)

    return theta, alpha, beta

# --- DYNAMICZNY WYKRES ---
def live_plot(eeg):
    fig, ax = plt.subplots()
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 50)
    ax.set_xlabel("Czas (aktualizacje)")
    ax.set_ylabel("Moc (PSD)")
    ax.set_title("Moc fal EEG: Theta / Alpha / Beta")

    x_data = []
    theta_data = []
    alpha_data = []
    beta_data = []

    line_theta, = ax.plot([], [], label='Theta', color='blue')
    line_alpha, = ax.plot([], [], label='Alpha', color='green')
    line_beta, = ax.plot([], [], label='Beta', color='red')
    ax.legend()

    counter = 0

    def update(frame):
        nonlocal counter
        eeg.get_mne()
        mne_raw = eeg.data.mne_raw
        data, times = mne_raw.get_data(return_times=True)

        if data.shape[1] < WINDOW_SIZE:
            return line_theta, line_alpha, line_beta

        window = data[:, -WINDOW_SIZE:]
        theta, alpha, beta = calculate_metrics(window)

        x_data.append(counter)
        theta_data.append(theta)
        alpha_data.append(alpha)
        beta_data.append(beta)
        counter += 1

        # ograniczamy do ostatnich 100 punktów
        x_plot = x_data[-100:]
        theta_plot = theta_data[-100:]
        alpha_plot = alpha_data[-100:]
        beta_plot = beta_data[-100:]

        line_theta.set_data(x_plot, theta_plot)
        line_alpha.set_data(x_plot, alpha_plot)
        line_beta.set_data(x_plot, beta_plot)

        ax.set_xlim(max(0, counter-100), counter)
        return line_theta, line_alpha, line_beta

    ani = FuncAnimation(fig, update, interval=1000)
    plt.show()

# --- GŁÓWNY PROGRAM ---
def main():
    eeg = acquisition.EEG()

    print(f"Łączenie z {DEVICE_NAME}...")
    with EEGManager() as mgr:
        eeg.setup(mgr, device_name=DEVICE_NAME, cap=electrodes_mini, sfreq=SFREQ)
        eeg.start_acquisition()
        print("Akwizycja rozpoczęta. Buforowanie 2 sekundy...")
        time.sleep(2)

        try:
            live_plot(eeg)  # uruchamiamy dynamiczny wykres
        except KeyboardInterrupt:
            print("Zatrzymywanie...")
        finally:
            eeg.stop_acquisition()
            eeg.close()
            mgr.disconnect()
            print("Rozłączono.")

if __name__ == "__main__":
    main()
