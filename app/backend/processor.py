import numpy as np
from scipy.signal import welch, iirnotch, lfilter, butter

SFREQ = 250
ARTIFACT_THRESHOLD = 15000 
SMOOTHING_FACTOR = 0.3       # 0.0 - brak wygładzania, 0.9 - bardzo wolne zmiany

class EEGProcessor:
    def __init__(self):
        # Stan kalibracji (dynamiczne min/max)
        self.min_focus = None
        self.max_focus = None
        self.min_stress = None
        self.max_stress = None

        # Ostatnie poprawne wartości (do wygładzania)
        self.last_focus_raw = 0
        self.last_stress_raw = 0
        
    def _filter_data(self, data, fs=SFREQ):
        """Notch 50Hz i bandpass 1-40Hz"""
        # Notch (wycięcie sieci elektrycznej)
        b_notch, a_notch = iirnotch(50.0, 30.0, fs)
        data = lfilter(b_notch, a_notch, data)
        
        # Bandpass (zakres fal mózgowych)
        nyq = fs * 0.5
        b_band, a_band = butter(4, [1/nyq, 40/nyq], btype='band')
        data = lfilter(b_band, a_band, data)
        return data

    def _check_artifacts(self, window_data):
        """Zwraca True jeśli wykryto zbyt silny sygnał (ruch)"""
        # Sprawdzamy amplitudę peak-to-peak
        peak_amp = np.max(window_data) - np.min(window_data)
        # BrainAccess zwraca dane w Voltach, więc 100uV to 0.0001
        # Jeśli dane są już w uV, dostosuj ARTIFACT_THRESHOLD
        print(f"DEBUG AMP: {peak_amp:.6f} (Próg: {ARTIFACT_THRESHOLD})")

        if peak_amp > ARTIFACT_THRESHOLD: 
            return True
        return False

    def _normalize(self, value, min_val, max_val):
        """Dynamiczna normalizacja do 0-100%"""
        if min_val is None or max_val is None:
            return value, value, value # Inicjalizacja
            
        # Aktualizacja min/max z powolnym "zapominaniem" (decay)
        # Aby max nie utknął na zawsze na wysokim poziomie
        max_val = max(max_val, value) - (max_val * 0.001) 
        min_val = min(min_val, value) + (min_val * 0.001)
        
        # Obliczenie procentu
        denom = (max_val - min_val) if (max_val - min_val) != 0 else 1
        percent = (value - min_val) / denom * 100
        
        return np.clip(percent, 0, 100), min_val, max_val

    def process_window(self, window_data):
        """Główna funkcja przetwarzająca okno danych"""
        
        # 1. Detekcja artefaktów (zanim zaczniemy liczyć FFT)
        # Jeśli którykolwiek kanał ma artefakt, odrzucamy całe okno
        # Zakładamy input shape: (n_channels, n_samples)
        for channel in window_data:
            if self._check_artifacts(channel):
                print("[!] Wykryto ruch - okno odrzucone")
                return None # Zwracamy None, żeby serwer wiedział, że nie ma nowych danych

        # 2. Filtracja i uśrednienie kanałów
        filtered = np.array([self._filter_data(ch) for ch in window_data])
        avg_data = np.mean(filtered, axis=0)

        # 3. Analiza widmowa (Welch)
        freqs, psd = welch(avg_data, SFREQ)
        
        # Wyciągnięcie pasm
        alpha = np.mean(psd[(freqs >= 8) & (freqs <= 12)])
        beta  = np.mean(psd[(freqs >= 13) & (freqs <= 30)])
        high_beta = np.mean(psd[(freqs >= 20) & (freqs <= 30)])
        
        # Zabezpieczenie przed dzieleniem przez zero
        if alpha == 0: alpha = 1e-10

        # 4. Obliczenie surowych wskaźników
        current_focus = beta / alpha
        current_stress = high_beta / alpha

        # 5. Wygładzanie (Exponential Moving Average)
        # Nowa wartość to X% nowej i (100-X)% starej
        self.last_focus_raw = (current_focus * (1 - SMOOTHING_FACTOR)) + (self.last_focus_raw * SMOOTHING_FACTOR)
        self.last_stress_raw = (current_stress * (1 - SMOOTHING_FACTOR)) + (self.last_stress_raw * SMOOTHING_FACTOR)

        # 6. Normalizacja
        focus_pct, self.min_focus, self.max_focus = self._normalize(
            self.last_focus_raw, self.min_focus, self.max_focus
        )
        
        stress_pct, self.min_stress, self.max_stress = self._normalize(
            self.last_stress_raw, self.min_stress, self.max_stress
        )

        return {
            "focus": round(float(focus_pct), 2),
            "stress": round(float(stress_pct), 2),
            "raw_focus": float(self.last_focus_raw), # Opcjonalnie do debugowania
            "alert": 1 if focus_pct < 30 else 0      # Przykładowy alert
        }