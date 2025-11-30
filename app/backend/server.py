import asyncio
import websockets
import json
import time
import numpy as np

# --- IMPORT NOWEJ KLASY Z LOGIKĄ ---
# Upewnij się, że plik processor.py jest w tym samym folderze!
from processor import EEGProcessor

# --- KONFIGURACJA ---
PORT = 8765
DEVICE_NAME = "BA MINI 047"
SFREQ = 250
WINDOW_SIZE = SFREQ * 5
ELECTRODES = {0: "Fp1", 1: "Fp2"}

# --- IMPORT BIBLIOTEK BRAINACCESS (BEZPIECZNY) ---
BRAINACCESS_AVAILABLE = False
try:
    from brainaccess.utils import acquisition
    from brainaccess.core.eeg_manager import EEGManager
    BRAINACCESS_AVAILABLE = True
except ImportError:
    print("[!] Nie znaleziono bibliotek BrainAccess. Dostępna tylko symulacja.")

# --- OBSŁUGA SYMULACJI (GDY BRAK OPASKI) ---
async def stream_simulation(websocket):
    print("Klient połączony (TRYB SYMULACJI)")
    try:
        while True:
            # Generujemy losowe dane, żeby frontend miał co pokazać
            f_sim = np.random.randint(30, 80)
            s_sim = np.random.randint(10, 50)
            
            result = {
                "focus": f_sim,
                "stress": s_sim,
                "alert": 0,
                "mode": "simulation"
            }
            
            await websocket.send(json.dumps(result))
            print(f"Symulacja: Focus {f_sim}% | Stress {s_sim}%")
            await asyncio.sleep(1)
            
    except websockets.exceptions.ConnectionClosed:
        print("Klient symulacji rozłączony")

# --- OBSŁUGA PRAWDZIWEGO EEG ---
async def stream_real_eeg(websocket, eeg):
    print("Klient połączony (TRYB REAL EEG)")
    
    # Tworzymy instancję procesora (osobną dla każdej sesji)
    processor = EEGProcessor()
    
    try:
        while True:
            # 1. Pobranie danych z biblioteki BrainAccess
            eeg.get_mne()
            
            # Czekamy, aż dane będą dostępne w obiekcie MNE
            if not hasattr(eeg.data, 'mne_raw') or eeg.data.mne_raw is None:
                await asyncio.sleep(0.1)
                continue

            mne_raw = eeg.data.mne_raw
            data, times = mne_raw.get_data(return_times=True)

            # 2. Sprawdzenie czy mamy wystarczająco dużo danych do okna
            if data.shape[1] < WINDOW_SIZE:
                # Czekamy na zapełnienie bufora
                await asyncio.sleep(0.5)
                continue

            # 3. Wycięcie ostatniego okna czasowego (np. ostatnich 2 sekund)
            window = data[:, -WINDOW_SIZE:]

            # 4. OBLICZENIA (Teraz robi to processor.py)
            # Funkcja zwróci None, jeśli wykryto artefakty (ruch)
            metrics = processor.process_window(window)

            if metrics:
                # 5. Przygotowanie danych do wysłania
                result = {
                    "focus": metrics["focus"],
                    "stress": metrics["stress"],
                    "alert": metrics["alert"],
                    "mode": "real"
                }

                await websocket.send(json.dumps(result))
                
                # Logowanie dla Twojej informacji
                print(f"REAL -> F: {metrics['focus']:05.2f}% | S: {metrics['stress']:05.2f}% | (Raw: {metrics['raw_focus']:.3f})")
            else:
                print("[!] Ignorowanie okna (artefakty/ruch)")

            # Częstotliwość wysyłania danych do klienta (np. co 0.5s lub 1s)
            await asyncio.sleep(0.5)

    except websockets.exceptions.ConnectionClosed:
        print("Klient rozłączony (EEG)")
    except Exception as e:
        print(f"Błąd w pętli EEG: {e}")
        import traceback
        traceback.print_exc()

# --- GŁÓWNA FUNKCJA ---
async def main():
    print("--- START SERWERA MÓZGU ---")
    
    use_simulation = True
    eeg_instance = None
    manager = None

    # 1. Próba połączenia ze sprzętem
    if BRAINACCESS_AVAILABLE:
        try:
            print(f"Szukanie urządzenia...")
            manager = EEGManager()
            eeg_instance = acquisition.EEG()
            
            # Otwieramy managera
            manager.__enter__() 
            
            # Setup urządzenia (dostosuj parametry cap i device_name jeśli trzeba)
            eeg_instance.setup(manager, device_name=DEVICE_NAME, cap=ELECTRODES, sfreq=SFREQ)
            eeg_instance.start_acquisition()
            
            print(f"SUKCES: Połączono z urządzeniem.")
            print("Buforowanie wstępne danych (3s)...")
            time.sleep(3) # Czekamy na zebranie pierwszych próbek
            use_simulation = False
            
        except Exception as e:
            print(f"[!] Nie udało się połączyć z opaską: {e}")
            print("[i] Przechodzę w tryb SYMULACJI.")
            if manager:
                manager.__exit__(None, None, None)
            use_simulation = True
    else:
        print("[i] Brak bibliotek - tryb SYMULACJI wymuszony.")

    # 2. Uruchomienie serwera WebSocket
    print(f"\n>> Serwer WebSocket nasłuchuje na ws://localhost:{PORT}")
    print(f">> Tryb pracy: {'SYMULACJA (dane losowe)' if use_simulation else 'REAL TIME EEG'}")

    try:
        if use_simulation:
            # Uruchom handler symulacji
            async with websockets.serve(stream_simulation, "localhost", PORT):
                await asyncio.get_running_loop().create_future() # Czekaj w nieskończoność
        else:
            # Uruchom handler EEG (przekazujemy instancję eeg przez lambda)
            # Lambda pozwala przekazać argument 'eeg_instance' do funkcji, która normalnie przyjmuje tylko 'ws'
            async with websockets.serve(lambda ws: stream_real_eeg(ws, eeg_instance), "localhost", PORT):
                await asyncio.get_running_loop().create_future()
    
    finally:
        # Sprzątanie po zamknięciu (CTRL+C)
        if not use_simulation and manager:
            print("Zamykanie połączenia z EEG...")
            try:
                eeg_instance.stop_acquisition()
                eeg_instance.close()
                manager.__exit__(None, None, None)
            except:
                pass
            print("EEG zamknięte.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nZatrzymano serwer.")