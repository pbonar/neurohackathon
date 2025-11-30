// background.js

let socket = null;
let lastNotificationTime = 0;
let lastTestNotificationTime = 0;
let reconnectAttempts = 0;
const MAX_RECONNECT_DELAY = 30000;
// Przywrócono pierwotne opóźnienie powiadomienia (60 sekund)
const THROTTLE_DELAY = 60000;

// chrome.runtime.onInstalled.addListener(() => {
//   console.log("🔔 Rozszerzenie zainstalowane, wysyłamy testowe powiadomienie");
  
//   chrome.permissions.contains({permissions: ['notifications']}, (hasPermission) => {
//     if (!hasPermission) {
//       console.warn("⚠️ Brak uprawnień do powiadomień");
//       return;
//     }
    
//     chrome.notifications.create({
//       type: 'basic',
//       iconUrl: chrome.runtime.getURL('icons/cow-128.png'),
//       title: 'Test powiadomienia',
//       message: 'Service worker działa!',
//       priority: 2,
//       requireInteraction: false
//     }, (id) => {
//       if (chrome.runtime.lastError) {
//         console.error("❌ Błąd powiadomienia:", chrome.runtime.lastError.message);
//       } else {
//         console.log("✅ Testowe powiadomienie wysłane, ID:", id);
//         lastNotificationTime = Date.now();
//       }
//     });
//   });
// });

function sendNotification(title, message) {
  const now = Date.now();
  const timeSinceLastNotification = now - lastNotificationTime;
  
  if (timeSinceLastNotification < THROTTLE_DELAY) { 
    console.log(`⏱ Powiadomienie pominięte (throttle). Poczekaj jeszcze: ${(THROTTLE_DELAY - timeSinceLastNotification) / 1000}s`);
    return;
  }

  console.log("🔔 Próba wysłania powiadomienia:", title, message);

  const notificationId = "ttg-" + crypto.randomUUID();

  chrome.notifications.create(notificationId, {
    type: 'basic',
    iconUrl: chrome.runtime.getURL('icons/cow-128.png'),
    title: title,
    message: message,
    priority: 2,
    requireInteraction: false, 
    isClickable: true
  }, (id) => {
    const error = chrome.runtime.lastError;
    if (error) {
      console.error("❌ Błąd powiadomienia:", error.message);
    } else {
      console.log("✅ Powiadomienie wysłane, ID:", id);
      lastNotificationTime = now; 
    }
  });
}

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'testNotification') {
    console.log("📬 Otrzymano żądanie testu powiadomienia");
    const now = Date.now();
    
    if (now - lastTestNotificationTime < 500) {
      console.log("⏳ Test zbyt szybki, poczekaj chwilę");
      sendResponse({ success: false, message: "Poczekaj 500ms między testami" });
      return;
    }
    
    lastTestNotificationTime = now;
    sendNotification("TEST: Powiadomienia działają!", "To jest powiadomienie testowe. Jeśli to widzisz - wszystko jest w porządku!");
    sendResponse({ success: true });
  }
  // NOWA OBSŁUGA POWIADOMIENIA PRZED WYSŁANIEM
  if (request.action === 'sendPreSendNotification') {
    console.log("✉️ Otrzymano żądanie powiadomienia przed wysłaniem wiadomości");
    
    let message = "Właśnie nacisnąłeś Enter. Czy ta wiadomość jest naprawdę pilna i konieczna? Zastanów się przez chwilę i weź głęboki oddech!";
    let title = "Wstrzymaj się na chwilę!";
    
    // Opcjonalne: Sprawdzenie treści wiadomości pod kątem słów kluczowych związanych ze stresem
    if (request.messageContent) {
        const stressKeywords = [
          "urgent", "ASAP", "asap", "deadline", "critical", "immediately",
          "emergency", "crisis", "important", "priority", "rush"
        ];
        
        const contentLower = request.messageContent.toLowerCase();
        const foundKeywords = stressKeywords.filter(keyword => 
            new RegExp(`\\b${keyword}\\b`, 'i').test(contentLower)
        );
        
        if (foundKeywords.length > 0) {
            title = "⚠️ UWAGA: Wiadomość jest NAPINKOWA!";
            message = `Wiadomość zawiera słowa kluczowe (np. ${foundKeywords.slice(0, 2).join(', ')}). Zadbaj o spokój, zanim klikniesz Wyślij.`;
        }
    }
    
    sendNotification(title, message);
    sendResponse({ success: true });
  }
  // KONIEC NOWEJ OBSŁUGI
  if (request.action === 'getConnectionStatus') {
    const isConnected = socket && socket.readyState === WebSocket.OPEN;
    sendResponse({ connected: isConnected });
  }
});

function connect() {
  try {
    console.log("🔌 Próba połączenia z WebSocket...");
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
        console.log("📡 Odebrano dane:", data);
        console.log(`   → focus: ${data.focus}%, stress: ${data.stress}%`);
        handleBrainData(data);
      } catch (error) {
        console.error("❌ Błąd parsowania danych:", error);
      }
    };
    
    socket.onerror = (error) => {
      console.error("❌ WebSocket error:", error);
      chrome.action.setBadgeText({ text: "ERR" });
      chrome.action.setBadgeBackgroundColor({ color: "#999" });
    };
    
    socket.onclose = () => {
      console.log("🔌 Rozłączono. Próba ponownego połączenia...");
      chrome.action.setBadgeText({ text: "OFF" });
      chrome.action.setBadgeBackgroundColor({ color: "#666" });
      
      const delay = Math.min(1000 * Math.pow(2, reconnectAttempts), MAX_RECONNECT_DELAY);
      reconnectAttempts++;
      console.log(`⏱ Próba reconnect za ${delay} ms`);
      
      setTimeout(connect, delay);
    };
  } catch (error) {
    console.error("❌ Błąd tworzenia WebSocket:", error);
    setTimeout(connect, 5000);
  }
}

function handleBrainData(data) {
  console.log("🧠 Aktualizacja badge i sprawdzenie poziomu mózgu...");
  chrome.action.setBadgeText({ text: data.focus.toString() });
  
  if (data.focus > 60) {
    chrome.action.setBadgeBackgroundColor({ color: "#4CAF50" });
  } else if (data.focus > 30) {
    chrome.action.setBadgeBackgroundColor({ color: "#FFC107" });
  } else {
    chrome.action.setBadgeBackgroundColor({ color: "#F44336" });
  }
  
  const isBrainFried = (data.focus < 40) || (data.stress > 75);
  
  if (isBrainFried) {
    console.log("⚠️ Wykryto krytyczny stan mózgu, wysyłamy powiadomienie");
    console.log(`   ⚠️ Krytyczne progi: focus<40 (${data.focus}), stress>75 (${data.stress})`);
    let message = '';
    
    if (data.focus < 40 && data.stress > 75) {
      message = `Mózg przeciążony! Skupienie: ${data.focus}%, Stres: ${data.stress}%. Zrób przerwę!`;
    } else if (data.focus < 40) {
      message = `Skupienie niskie (${data.focus}%). Czas na kawę lub spacer!`;
    } else if (data.stress > 75) {
      message = `Poziom stresu wysoki (${data.stress}%)! Weź głęboki oddech i dotknij trawy!`;
    }

    sendNotification("ALERT: Zadbaj o siebie!", message);
  } else {
    console.log(`   ✅ Stan OK (focus=${data.focus}%, stress=${data.stress}%)`);
  }
  
  chrome.storage.local.set({
    lastBrainData: data,
    lastUpdate: Date.now()
  }, () => console.log("💾 Dane zapisane w storage"));
}

connect();