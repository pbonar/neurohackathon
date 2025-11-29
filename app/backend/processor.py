import numpy as np
from scipy.signal import welch, iirnotch, lfilter, butter

class EEGProcessor:
    def __init__(self, sfreq=250):
        self.sfreq = sfreq
        # Stan kalibracji
        self.max_focus = 0
        self.min_focus = 100
        
    def _filter_data(self, data):
        """Notch 50Hz i bandpass 1-40Hz"""
        # Notch
        b_notch, a_notch = iirnotch(50.0, 30.0, self.sfreq)
        data = lfilter(b_notch, a_notch, data)
        # Bandpass
        nyq = self.sfreq * 0.5
        b_band, a_band = butter(4, [1/nyq, 40/nyq], btype='band')
        data = lfilter(b_band, a_band, data)
        return data

    def _calculate_spectral_features(self, window_data):
        # Filtracja kanał po kanale
        filtered = np.array([self._filter_data(ch) for ch in window_data])
        # Uśrednianie kanałów (np. Fp1 i Fp2)
        avg_data = np.mean(filtered, axis=0)

        freqs, psd = welch(avg_data, self.sfreq, nperseg=self.sfreq)
        
        # Wyciąganie pasm
        alpha = np.mean(psd[(freqs >= 8) & (freqs <= 12)])
        beta = np.mean(psd[(freqs >= 13) & (freqs <= 30)])
        high_beta = np.mean(psd[(freqs >= 20) & (freqs <= 30)])
        
        return alpha, beta, high_beta

    def _normalize_focus(self, focus_raw):
        """Dynamiczna kalibracja min/max"""
        # Wstępne skalowanie z twojego kodu
        val = np.clip(focus_raw * 200, 0, 100)

        # Inicjalizacja przy pierwszym odczycie
        if self.max_focus == 0: 
            self.max_focus = val

        self.min_focus = min(self.min_focus, val)

        # Dynamiczne podnoszenie sufitu (adaptacja)
        if val <= self.max_focus + self.min_focus * 0.03:
            self.max_focus = max(self.max_focus, val)

        # Obliczenie procentu
        denominator = self.max_focus - self.min_focus
        if denominator == 0: 
            return 0.0
            
        focus_percent = min((val - self.min_focus) / denominator * 100, 100)
        return max(0, focus_percent) # Zabezpieczenie przed ujemnymi
    
    # def _normalize_stress(self, stress_raw):
    #     stress_percent
    #     return stress_percent

    def process_window(self, window_data):
        """Główna funkcja przetwarzająca okno danych"""
        alpha, beta, high_beta = self._calculate_spectral_features(window_data)
        
        # Ochrona przed dzieleniem przez zero
        if alpha <= 0: alpha = 0.0001 

        focus_ratio_raw = beta / alpha
        
        # Obliczenia końcowe
        focus_percent = self._normalize_focus(focus_ratio_raw)
        is_stressed = beta > 40 # Próg eksperymentalny
        
        state = "neutralnie"
        if focus_percent < 33: state = "nie skupione"
        elif focus_percent > 66: state = "skupione"
        stress_percent = 50 #zhardkodowane !!!! 

        print(f"focus_percent: {round(focus_percent, 2)}, stress_percent: {round(stress_percent, 2)}")

        return {
            "focus_percent": round(focus_percent, 2),
            "stress_percent": round(stress_percent, 2)
        }