// extension/background.js
let socket = null;
let lastNotificationTime = 0;
let reconnectAttempts = 0;
const MAX_RECONNECT_DELAY = 30000;

function connect() {
  try {
    socket = new WebSocket('ws://localhost:8765');
    
    socket.onopen = () => {
      console.log("✅ Połączono z serwerem Brain Monitor");
      reconnectAttempts = 0;
      chrome.action.setBadgeText({ text: "ON" });
      chrome.action.setBadgeBackgroundColor({ color: "#4CAF50" });
    };
    
    socket.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        handleBrainData(data);
      } catch (error) {
        console.error("Błąd parsowania danych:", error);
      }
    };
    
    socket.onerror = (error) => {
      console.error("❌ WebSocket error:", error);
      chrome.action.setBadgeText({ text: "ERR" });
      chrome.action.setBadgeBackgroundColor({ color: "#999" });
    };
    
    socket.onclose = () => {
      console.log("🔌 Rozłączono. Ponowne łączenie...");
      chrome.action.setBadgeText({ text: "OFF" });
      chrome.action.setBadgeBackgroundColor({ color: "#666" });
      
      // Exponential backoff dla reconnect
      const delay = Math.min(1000 * Math.pow(2, reconnectAttempts), MAX_RECONNECT_DELAY);
      reconnectAttempts++;
      
      setTimeout(connect, delay);
    };
  } catch (error) {
    console.error("Błąd tworzenia WebSocket:", error);
    setTimeout(connect, 5000);
  }
}

function handleBrainData(data) {
  chrome.action.setBadgeText({ text: data.focus.toString() });
  
  if (data.focus > 60) {
    chrome.action.setBadgeBackgroundColor({ color: "#4CAF50" }); // Green
  } else if (data.focus > 30) {
    chrome.action.setBadgeBackgroundColor({ color: "#FFC107" }); // Yellow
  } else {
    chrome.action.setBadgeBackgroundColor({ color: "#F44336" }); // Red
  }
  
  const isBrainFried = (data.focus < 20) || (data.stress > 85);
  
  if (isBrainFried) {
    sendNotification(data);
  }
  
  chrome.storage.local.set({
    lastBrainData: data,
    lastUpdate: Date.now()
  });
}

function sendNotification(data) {
  const now = Date.now();
  
  if (now - lastNotificationTime < 60000) {
    return;
  }
  
  let message = '';
  if (data.focus < 20 && data.stress > 85) {
    message = '🧠 Mózg przeciążony! Skupienie: ' + data.focus + '%, Stres: ' + data.stress + '%. Zrób przerwę!';
  } else if (data.focus < 20) {
    message = '😴 Skupienie krytycznie niskie (' + data.focus + '%). Czas na kawę lub spacer!';
  } else if (data.stress > 85) {
    message = '😰 Poziom stresu krytyczny (' + data.stress + '%)! Weź głęboki oddech i dotknij trawy!';
  }
  
  chrome.notifications.create({
    type: 'basic',
    iconUrl: 'icons/cow-128.png',
    title: '🛑 ALERT: Zadbaj o siebie!',
    message: message,
    priority: 2,
    requireInteraction: true
  });
  
  lastNotificationTime = now;
}

connect();

chrome.action.onClicked.addListener(() => {
  chrome.action.openPopup();
});