// extension/content.js
console.log("🌿 Touch the Grass content script running on", window.location.href);

const STRESS_KEYWORDS = [
  "urgent", "ASAP", "asap", "deadline", "critical", "immediately",
  "emergency", "crisis", "important", "priority", "rush"
];

// -----------------------------------------------
// 🧠 ZMIENNA GLOBALNA PRZECHOWUJĄCA STRES Z BACKENDU
// -----------------------------------------------
let currentStressLevel = 0; // Domyślnie niski stres
const ALERT_THRESHOLD = 70; // 70% jako próg ostrzegania

// -----------------------------------------------
// FUNKCJE POMOCNICZE
// -----------------------------------------------

function isMessageInput(element) {
  const tagName = element.tagName;
  const type = element.type;
  const role = element.getAttribute('role'); 

  if (tagName === 'TEXTAREA') return true;
  if (tagName === 'INPUT' && (type === 'text' || type === 'search' || type === 'email' || type === 'url')) return true;
  
  const isExplicitlyEditable = element.getAttribute('contenteditable') === 'true';
  
  if ((isExplicitlyEditable || role === 'textbox') && element.tagName !== 'BUTTON' && element.tagName !== 'A') {
      return true;
  }
  
  return false;
}

// -----------------------------------------------
// 🚨 GŁÓWNA LOGIKA: OSTRZEGANIE O STRESIE (FOCUSIN)
// -----------------------------------------------

document.addEventListener('focusin', (event) => {
    let currentElement = event.target;
    let messageInput = null;
    
    // 1. Znajdź pole wiadomości (przechodząc w górę DOM)
    for (let i = 0; i < 10; i++) { 
        if (!currentElement) break;
        if (isMessageInput(currentElement)) {
            messageInput = currentElement;
            break;
        }
        currentElement = currentElement.parentElement;
    }
    
    if (messageInput) {
        
        console.log(`🧠 DEBUG: Fokus na pole. Aktualny poziom stresu (z backendu): ${currentStressLevel}%`);

        if (currentStressLevel >= ALERT_THRESHOLD) {
            // 2. WYŚWIETLENIE OSTRZEŻENIA
            // Używamy alertu do testów, ale powiadomienie powinno być bardziej subtelne
            alert(`🚨 WYSOKI STRES (${currentStressLevel}%)! Pomyśl dwa razy przed wysłaniem tej wiadomości.`);
        }
    }
});


// -----------------------------------------------
// 🛰️ NASŁUCHIWANIE NA DANE O STRESIE Z BACKENDU
// -----------------------------------------------

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    // 1. Logika aktualizacji poziomu stresu (zakładamy, że akcja to 'updateStress')
    if (request.action === 'updateStress' && request.data) {
        
        const receivedStress = request.data.stress;

        if (typeof receivedStress === 'number') {
            currentStressLevel = receivedStress;
            console.log(`✅ Zaktualizowano poziom stresu z backendu: ${currentStressLevel}%`);
        }
    }
    
    // 2. Logika dla innych akcji (np. zapytań o słowa kluczowe)
    if (request.action === 'getStressKeywordCount') {
        const bodyText = document.body.innerText.toLowerCase();
        let count = 0;
        STRESS_KEYWORDS.forEach(keyword => {
            const regex = new RegExp(`\\b${keyword}\\b`, 'gi');
            const matches = bodyText.match(regex);
            if (matches) count += matches.length;
        });
        sendResponse({ count });
    }
});


// -----------------------------------------------
// 🎨 LOGIKA PODŚWIETLANIA SŁÓW KLUCZOWYCH
// -----------------------------------------------
let highlightTimeout;
function scheduleHighlight() {
  clearTimeout(highlightTimeout);
  highlightTimeout = setTimeout(highlightKeywords, 500);
}

function highlightKeywords() {
  const excludedDomains = ['youtube.com', 'netflix.com', 'twitch.tv'];
  if (excludedDomains.some(domain => window.location.hostname.includes(domain))) {
    return;
  }

  const walker = document.createTreeWalker(
    document.body,
    NodeFilter.SHOW_TEXT,
    {
      acceptNode: function(node) {
        if (node.parentElement.tagName === 'SCRIPT' ||
            node.parentElement.tagName === 'STYLE' ||
            node.parentElement.classList.contains('ttg-highlight')) {
          return NodeFilter.FILTER_REJECT;
        }
        return NodeFilter.FILTER_ACCEPT;
      }
    },
    false
  );

  const nodesToProcess = [];
  let node;

  while (node = walker.nextNode()) {
    STRESS_KEYWORDS.forEach(keyword => {
      const regex = new RegExp(`\\b${keyword}\\b`, 'i');
      if (regex.test(node.nodeValue)) {
        nodesToProcess.push({ node, keyword });
      }
    });
  }

  nodesToProcess.forEach(({ node, keyword }) => {
    try {
      const regex = new RegExp(`\\b(${keyword})\\b`, 'gi');
      const text = node.nodeValue;
      
      if (!regex.test(text)) return;
      
      const parent = node.parentNode;
      const fragment = document.createDocumentFragment();
      
      let lastIndex = 0;
      text.replace(regex, (match, p1, offset) => {
        if (offset > lastIndex) {
          fragment.appendChild(
            document.createTextNode(text.substring(lastIndex, offset))
          );
        }
        
        const highlight = document.createElement('span');
        highlight.className = 'ttg-highlight';
        highlight.style.cssText = `
          background: linear-gradient(120deg, #ffd93d 0%, #ffeb3b 100%);
          padding: 2px 4px;
          border-radius: 3px;
          font-weight: 500;
          box-shadow: 0 1px 3px rgba(255, 193, 7, 0.3);
          transition: all 0.2s ease;
        `;
        highlight.textContent = match;
        
        highlight.addEventListener('mouseenter', function() {
          this.style.backgroundColor = '#ffc107';
          this.style.transform = 'scale(1.05)';
        });
        highlight.addEventListener('mouseleave', function() {
          this.style.backgroundColor = '';
          this.style.transform = '';
        });
        
        fragment.appendChild(highlight);
        
        lastIndex = offset + match.length;
        return match;
      });
      
      if (lastIndex < text.length) {
        fragment.appendChild(
          document.createTextNode(text.substring(lastIndex))
        );
      }
      
      parent.replaceChild(fragment, node);
    } catch (error) {
      console.error("Error highlighting keyword:", error);
    }
  });
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', highlightKeywords);
} else {
  highlightKeywords();
}

const observer = new MutationObserver(scheduleHighlight);
observer.observe(document.body, {
  childList: true,
  subtree: true,
  characterData: false
});

console.log("🌿 Touch the Grass: Monitoring " + STRESS_KEYWORDS.length + " stress keywords");