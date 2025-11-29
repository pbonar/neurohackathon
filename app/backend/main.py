import time
from brainaccess.utils import acquisition
from brainaccess.core.eeg_manager import EEGManager

# Import modułów
from processor import EEGProcessor
from transmitter import DataTransmitter

# --- KONFIGURACJA ---
SFREQ = 250
WINDOW_SIZE = SFREQ * 1  # 1 sekunda (skrócone dla szybszej reakcji)
DEVICE_NAME = "BA MINI 050"
ELECTRODES = {0: "Fp1", 1: "Fp2"}

def main():
    # 1. Inicjalizacja modułów
    processor = EEGProcessor(sfreq=SFREQ)
    transmitter = DataTransmitter(port=8765)
    eeg = acquisition.EEG()

    # Uruchom serwer WebSocket w tle
    transmitter.start_server()

    print(f"Łączenie z {DEVICE_NAME}...")
    
    with EEGManager() as mgr:
        # 2. Setup urządzenia
        eeg.setup(mgr, device_name=DEVICE_NAME, cap=ELECTRODES, sfreq=SFREQ)
        eeg.start_acquisition()
        print("Akwizycja rozpoczęta. Czekam na bufor...")
        time.sleep(2)

        try:
            while True:
                # 3. Pobranie danych
                eeg.get_mne()
                if not hasattr(eeg.data, 'mne_raw') or eeg.data.mne_raw is None:
                    continue
                    
                data = eeg.data.mne_raw.get_data() # (n_channels, n_samples)

                # Sprawdzenie czy mamy wystarczająco próbek
                if data.shape[1] < WINDOW_SIZE:
                    time.sleep(0.1)
                    continue

                # Wycięcie ostatniego okna
                window = data[:, -WINDOW_SIZE:]

                # 4. Przetwarzanie (Logika)
                result = processor.process_window(window)

                # 5. Logowanie w konsoli
                bar = "|" * int(result['focus_percent'] / 5)
                print(f"Stan: {result['state']:<15} | Focus: {result['focus_percent']:5.1f}% [{bar:<20}]")

                # 6. Wysyłka na frontend (Komunikacja)
                transmitter.send_data(result)

                # Krótka pauza, by nie zarżnąć CPU (i dać czas na akwizycję nowych próbek)
                # Zmieniono z 3s na 0.5s dla płynności
                time.sleep(0.5)

        except KeyboardInterrupt:
            print("\nZatrzymywanie...")
        finally:
            eeg.stop_acquisition()
            eeg.close()
            mgr.disconnect()
            print("Rozłączono.")

if __name__ == "__main__":
    main()