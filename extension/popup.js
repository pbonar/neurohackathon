// extension/popup.js

let socket = null;
let reconnectAttempts = 0;
const MAX_RECONNECT_DELAY = 30000;

// Zmienne globalne
let currentPuzzle = [];
let currentSolution = [];
let sudokuTimerInterval = null; // Zmienna do licznika czasu

// Lista lokalnych plików wideo
const brainrotVideos = [
    "videos/video1.mp4",
    "videos/video2.mp4",
    "videos/video3.mp4"
];

// Pobieranie elementów z HTML
const elements = {
  // Główne wskaźniki
  textFocus: document.getElementById('text-focus'),
  barFocus: document.getElementById('bar-focus'),
  textStress: document.getElementById('text-stress'),
  barStress: document.getElementById('bar-stress'),
  statusIndicator: document.getElementById('status-indicator'),
  statusText: document.getElementById('status-text'),
  lastUpdate: document.getElementById('last-update'),
  alertBox: document.getElementById('alert-box'),
  
  // Nakładka i widoki
  overlayCalibration: document.getElementById('overlay-calibration'),
  stepMenu: document.getElementById('calib-step-menu'),
  stepSudoku: document.getElementById('calib-step-sudoku'),
  stepBrainrot: document.getElementById('calib-step-brainrot'),
  
  // Przyciski
  btnStartCalib: document.getElementById('btn-start-calib'),
  btnChooseSudoku: document.getElementById('btn-choose-sudoku'),
  btnChooseBrainrot: document.getElementById('btn-choose-brainrot'),
  btnBackMain: document.getElementById('btn-back-main'),

  // Elementy Sudoku
  sudokuBoard: document.getElementById('sudoku-board'),
  btnFinishSudoku: document.getElementById('btn-finish-sudoku'),
  btnBackSudoku: document.getElementById('btn-back-sudoku'),
  sudokuTimer: document.getElementById('sudoku-timer'), // Licznik czasu w HTML

  // Elementy Brainrot
  brainrotPlayer: document.getElementById('brainrot-player'),
  btnNextVideo: document.getElementById('btn-next-video'),
  btnFinishBrainrot: document.getElementById('btn-finish-brainrot')
};

// ============================================================
// 1. LOGIKA WEBSOCKET
// ============================================================

function connectToMonitor() {
  try {
    socket = new WebSocket('ws://localhost:8765');
    
    socket.onopen = () => {
      console.log("✅ Popup connected to Brain Monitor");
      reconnectAttempts = 0;
      updateConnectionStatus('connected', 'Połączono z serwerem');
    };
    
    socket.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        updateUI(data);
        updateLastUpdateTime();
      } catch (error) {
        console.error("Error parsing data:", error);
      }
    };
    
    socket.onerror = (error) => {
      console.error("❌ WebSocket error:", error);
      updateConnectionStatus('disconnected', 'Błąd połączenia');
    };
    
    socket.onclose = () => {
      console.log("🔌 Connection closed, retrying...");
      updateConnectionStatus('connecting', 'Ponowne łączenie...');
      const delay = Math.min(1000 * Math.pow(2, reconnectAttempts), MAX_RECONNECT_DELAY);
      reconnectAttempts++;
      setTimeout(connectToMonitor, delay);
    };
  } catch (error) {
    console.error("Error creating WebSocket:", error);
    updateConnectionStatus('disconnected', 'Nie można połączyć');
    setTimeout(connectToMonitor, 5000);
  }
}

function sendCommand(command, extraData = {}) {
    if (socket && socket.readyState === WebSocket.OPEN) {
        const payload = {
            command: command,
            timestamp: Date.now(),
            ...extraData
        };
        socket.send(JSON.stringify(payload));
        console.log(`📤 Wysłano komendę: ${command}`, payload);
    }
}

// ============================================================
// 2. AKTUALIZACJA UI
// ============================================================

function updateUI(data) {
  elements.textFocus.innerText = data.focus + "%";
  elements.barFocus.style.width = data.focus + "%";
  
  if (data.focus > 70) elements.barFocus.style.background = "linear-gradient(90deg, #4CAF50 0%, #8BC34A 100%)";
  else if (data.focus > 40) elements.barFocus.style.background = "linear-gradient(90deg, #FFC107 0%, #FFD54F 100%)";
  else elements.barFocus.style.background = "linear-gradient(90deg, #FF9800 0%, #FFB74D 100%)";
  
  elements.textStress.innerText = data.stress + "%";
  elements.barStress.style.width = data.stress + "%";
  
  if (data.stress > 80) {
    elements.barStress.style.background = "linear-gradient(90deg, #b71c1c 0%, #c62828 100%)";
    elements.barStress.style.boxShadow = "0 0 15px rgba(183, 28, 28, 0.8)";
  } else if (data.stress > 50) {
    elements.barStress.style.background = "linear-gradient(90deg, #F44336 0%, #E91E63 100%)";
    elements.barStress.style.boxShadow = "0 0 10px rgba(244, 67, 54, 0.5)";
  } else {
    elements.barStress.style.background = "linear-gradient(90deg, #FF9800 0%, #FFC107 100%)";
    elements.barStress.style.boxShadow = "none";
  }
  
  const isCritical = (data.focus < 20) || (data.stress > 85);
  if (isCritical) {
    elements.alertBox.classList.add('show');
    if (data.focus < 20 && data.stress > 85) elements.alertBox.querySelector('.alert-text').innerText = "KRYZYS! Niskie skupienie i wysoki stres!";
    else if (data.focus < 20) elements.alertBox.querySelector('.alert-text').innerText = "Skupienie krytycznie niskie! Zrób przerwę!";
    else elements.alertBox.querySelector('.alert-text').innerText = "Poziom stresu krytyczny! Idź dotknij trawy!";
  } else {
    elements.alertBox.classList.remove('show');
  }
}

function updateConnectionStatus(status, text) {
  elements.statusIndicator.className = `status-indicator ${status}`;
  elements.statusText.innerText = text;
}

function updateLastUpdateTime() {
  const now = new Date();
  elements.lastUpdate.innerText = `Ostatnia aktualizacja: ${now.toLocaleTimeString()}`;
}

// ============================================================
// 3. NAWIGACJA (PRZEŁĄCZANIE EKRANÓW)
// ============================================================

function showSection(sectionId) {
    elements.stepMenu.classList.add('hidden');
    elements.stepSudoku.classList.add('hidden');
    elements.stepBrainrot.classList.add('hidden');

    if (sectionId === 'menu') elements.stepMenu.classList.remove('hidden');
    if (sectionId === 'sudoku') elements.stepSudoku.classList.remove('hidden');
    if (sectionId === 'brainrot') elements.stepBrainrot.classList.remove('hidden');
}

// Główny przycisk "Start Kalibracji"
elements.btnStartCalib.addEventListener('click', () => {
    elements.overlayCalibration.classList.remove('hidden');
    showSection('menu');
});

// Przycisk "Anuluj" w menu
elements.btnBackMain.addEventListener('click', () => {
    elements.overlayCalibration.classList.add('hidden');
});

// ============================================================
// 4. SUDOKU & TIMER
// ============================================================

elements.btnChooseSudoku.addEventListener('click', () => {
    showSection('sudoku');
    elements.sudokuBoard.innerHTML = '<div style="color:#666; padding:30px; text-align:center;">Ładowanie Sudoku...</div>';

    fetch('https://sudoku-api.vercel.app/api/dosuku')
        .then(res => res.json())
        .then(data => {
            const rawGrid = data.newboard.grids[0];
            currentPuzzle = rawGrid.value.flat();
            currentSolution = rawGrid.solution.flat();
            
            renderSudoku(currentPuzzle);
            sendCommand("start_calibration", { mode: "sudoku" });
            
            // START TIMERA
            startSudokuTimer();
        })
        .catch(err => {
            console.error("Błąd API Sudoku:", err);
            useBackupSudoku();
            sendCommand("start_calibration", { mode: "sudoku" });
            
            // START TIMERA (nawet przy backupie)
            startSudokuTimer();
        });
});

function renderSudoku(puzzleData) {
    elements.sudokuBoard.innerHTML = ''; 
    puzzleData.forEach((num, index) => {
        const input = document.createElement('input');
        input.type = 'text'; 
        input.className = 'sudoku-cell';
        input.maxLength = 1;
        if (num !== 0) {
            input.value = num;
            input.disabled = true;
        }
        input.addEventListener('input', (e) => {
            if (!/^[1-9]$/.test(e.target.value)) e.target.value = '';
        });
        const row = Math.floor(index / 9);
        if (row === 2 || row === 5) input.style.borderBottom = "2px solid #333";
        elements.sudokuBoard.appendChild(input);
    });
}

function useBackupSudoku() {
    const backupPuzzle = [5,3,0,0,7,0,0,0,0,6,0,0,1,9,5,0,0,0,0,9,8,0,0,0,0,6,0,8,0,0,0,6,0,0,0,3,4,0,0,8,0,3,0,0,1,7,0,0,0,2,0,0,0,6,0,6,0,0,0,0,2,8,0,0,0,0,4,1,9,0,0,5,0,0,0,0,8,0,0,7,9];
    const backupSolution = [5,3,4,6,7,8,9,1,2,6,7,2,1,9,5,3,4,8,1,9,8,3,4,2,5,6,7,8,5,9,7,6,1,4,2,3,4,2,6,8,5,3,7,9,1,7,1,3,9,2,4,8,5,6,9,6,1,5,3,7,2,8,4,2,8,7,4,1,9,6,3,5,3,4,5,2,8,6,1,7,9];
    currentPuzzle = backupPuzzle;
    currentSolution = backupSolution;
    renderSudoku(currentPuzzle);
}

// Przycisk "Gotowe" w Sudoku
elements.btnFinishSudoku.addEventListener('click', () => {
    const cells = document.querySelectorAll('.sudoku-cell');
    let errors = 0;
    let isComplete = true;

    cells.forEach((cell, index) => {
        const userValue = parseInt(cell.value);
        const correctValue = currentSolution[index];
        cell.style.backgroundColor = "white";
        if (cell.disabled) cell.style.backgroundColor = "#f0f0f0";
        if (!cell.value) { isComplete = false; return; }
        if (userValue !== correctValue) { cell.style.backgroundColor = "#ffcdd2"; errors++; }
        else if (!cell.disabled) { cell.style.backgroundColor = "#c8e6c9"; }
    });

    if (!isComplete) { alert("Uzupełnij wszystkie pola!"); return; }
    if (errors > 0) { alert(`Masz ${errors} błędów!`); return; }

    stopSudokuTimer(); // Zatrzymaj czas
    alert("BRAWO! Kalibracja zakończona sukcesem.");
    finishCalibration();
});

// Przycisk "Wróć" w Sudoku
elements.btnBackSudoku.addEventListener('click', () => {
    stopSudokuTimer(); // Zatrzymaj czas
    showSection('menu'); 
    sendCommand("stop_calibration");
});

// --- FUNKCJE TIMERA ---

function startSudokuTimer() {
    let timeLeft = 60; // Czas w sekundach
    
    // Reset wizualny
    if(elements.sudokuTimer) {
        elements.sudokuTimer.innerText = "01:00";
        elements.sudokuTimer.style.color = "#d32f2f"; 
    }

    if (sudokuTimerInterval) clearInterval(sudokuTimerInterval);

    sudokuTimerInterval = setInterval(() => {
        timeLeft--;

        const minutes = Math.floor(timeLeft / 60);
        const seconds = timeLeft % 60;
        
        if(elements.sudokuTimer) {
            elements.sudokuTimer.innerText = `0${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;
        }

        if (timeLeft <= 0) {
            stopSudokuTimer();
            alert("⏰ CZAS MINĄŁ! Koniec kalibracji.");
            finishCalibration(); 
        }
    }, 1000);
}

function stopSudokuTimer() {
    if (sudokuTimerInterval) {
        clearInterval(sudokuTimerInterval);
        sudokuTimerInterval = null;
    }
}

// ============================================================
// 5. BRAINROT LOGIC
// ============================================================

elements.btnChooseBrainrot.addEventListener('click', () => {
    showSection('brainrot');
    loadRandomVideo();
    sendCommand("start_calibration", { mode: "brainrot" });
});

elements.btnNextVideo.addEventListener('click', () => {
    loadRandomVideo();
});

elements.btnFinishBrainrot.addEventListener('click', () => {
    finishCalibration();
});

function loadRandomVideo() {
    const randomVideoFile = brainrotVideos[Math.floor(Math.random() * brainrotVideos.length)];
    console.log("Ładowanie lokalnego wideo:", randomVideoFile);
    elements.brainrotPlayer.src = randomVideoFile;
    // Autoplay w popupie
    elements.brainrotPlayer.play().catch(e => console.log("Autoplay zablokowany:", e));
}

// ============================================================
// 6. WSPÓLNE ZAKOŃCZENIE I START
// ============================================================

function finishCalibration() {
    elements.overlayCalibration.classList.add('hidden');
    elements.brainrotPlayer.pause();
    elements.brainrotPlayer.src = ""; 
    sendCommand("stop_calibration");
}

// Inicjalizacja przy starcie
connectToMonitor();

document.addEventListener('DOMContentLoaded', () => {
  document.body.style.opacity = '0';
  setTimeout(() => {
    document.body.style.transition = 'opacity 0.3s ease';
    document.body.style.opacity = '1';
  }, 10);
});