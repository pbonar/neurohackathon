// extension/popup.js
let socket = null;
let reconnectAttempts = 0;
const MAX_RECONNECT_DELAY = 30000;

const elements = {
  textFocus: document.getElementById('text-focus'),
  barFocus: document.getElementById('bar-focus'),
  textStress: document.getElementById('text-stress'),
  barStress: document.getElementById('bar-stress'),
  statusIndicator: document.getElementById('status-indicator'),
  statusText: document.getElementById('status-text'),
  lastUpdate: document.getElementById('last-update'),
  alertBox: document.getElementById('alert-box')
};

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

function updateUI(data) {
  // Update focus
  elements.textFocus.innerText = data.focus + "%";
  elements.barFocus.style.width = data.focus + "%";
  
  // Dynamic focus color based on level
  if (data.focus > 70) {
    elements.barFocus.style.background = "linear-gradient(90deg, #4CAF50 0%, #8BC34A 100%)";
  } else if (data.focus > 40) {
    elements.barFocus.style.background = "linear-gradient(90deg, #FFC107 0%, #FFD54F 100%)";
  } else {
    elements.barFocus.style.background = "linear-gradient(90deg, #FF9800 0%, #FFB74D 100%)";
  }
  
  // Update stress
  elements.textStress.innerText = data.stress + "%";
  elements.barStress.style.width = data.stress + "%";
  
  // Dynamic stress color based on level
  if (data.stress > 80) {
    elements.barStress.style.background = "linear-gradient(90deg, #b71c1c 0%, #c62828 100%)";
    elements.barStress.style.boxShadow = "0 0 15px rgba(183, 28, 28, 0.8)";
  } else if (data.stress > 50) {
    elements.barStress.style.background = "linear-gradient(90deg, #F44336 0%, #E91E63 100%)";
    elements.barStress.style.boxShadow = "0 0 10px rgba(244, 67, 54, 0.5)";
  } else {
    elements.barStress.style.background = "linear-gradient(90deg, #FF9800 0%, #FFC107 100%)";
    elements.barStress.style.boxShadow = "0 0 8px rgba(255, 152, 0, 0.4)";
  }
  
  // Show/hide alert
  const isCritical = (data.focus < 20) || (data.stress > 85);
  if (isCritical) {
    elements.alertBox.classList.add('show');
    
    if (data.focus < 20 && data.stress > 85) {
      elements.alertBox.querySelector('.alert-text').innerText = 
        "KRYZYS! Niskie skupienie i wysoki stres!";
    } else if (data.focus < 20) {
      elements.alertBox.querySelector('.alert-text').innerText = 
        "Skupienie krytycznie niskie! Zrób przerwę!";
    } else {
      elements.alertBox.querySelector('.alert-text').innerText = 
        "Poziom stresu krytyczny! Idź dotknij trawy!";
    }
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
  const timeString = now.toLocaleTimeString('pl-PL', { 
    hour: '2-digit', 
    minute: '2-digit',
    second: '2-digit'
  });
  elements.lastUpdate.innerText = `Ostatnia aktualizacja: ${timeString}`;
}

chrome.storage.local.get(['lastBrainData', 'lastUpdate'], (result) => {
  if (result.lastBrainData) {
    updateUI(result.lastBrainData);
    
    if (result.lastUpdate) {
      const lastUpdateDate = new Date(result.lastUpdate);
      const timeString = lastUpdateDate.toLocaleTimeString('pl-PL', { 
        hour: '2-digit', 
        minute: '2-digit',
        second: '2-digit'
      });
      elements.lastUpdate.innerText = `Ostatnia aktualizacja: ${timeString}`;
    }
  }
});

connectToMonitor();

document.addEventListener('DOMContentLoaded', () => {
  document.body.style.opacity = '0';
  setTimeout(() => {
    document.body.style.transition = 'opacity 0.3s ease';
    document.body.style.opacity = '1';
  }, 10);
});