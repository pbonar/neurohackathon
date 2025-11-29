// extension/content.js
console.log("🌿 Touch the Grass content script running on", window.location.href);

const STRESS_KEYWORDS = [
  "urgent", "ASAP", "asap", "deadline", "critical", "immediately",
  "emergency", "crisis", "important", "priority", "rush"
];

// Debounce function to avoid excessive highlighting
let highlightTimeout;
function scheduleHighlight() {
  clearTimeout(highlightTimeout);
  highlightTimeout = setTimeout(highlightKeywords, 500);
}

function highlightKeywords() {
  // Don't highlight on certain sites where it might break things
  const excludedDomains = ['youtube.com', 'netflix.com', 'twitch.tv'];
  if (excludedDomains.some(domain => window.location.hostname.includes(domain))) {
    return;
  }

  const walker = document.createTreeWalker(
    document.body,
    NodeFilter.SHOW_TEXT,
    {
      acceptNode: function(node) {
        // Skip script, style, and already highlighted elements
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
        // Add text before match
        if (offset > lastIndex) {
          fragment.appendChild(
            document.createTextNode(text.substring(lastIndex, offset))
          );
        }
        
        // Add highlighted match
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
        
        // Add hover effect
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
      
      // Add remaining text
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

// Run highlighting on page load
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', highlightKeywords);
} else {
  highlightKeywords();
}

// Watch for dynamic content changes (e.g., Gmail, Slack)
const observer = new MutationObserver(scheduleHighlight);
observer.observe(document.body, {
  childList: true,
  subtree: true,
  characterData: false
});

// Listen for messages from popup
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
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

console.log("🌿 Touch the Grass: Monitoring " + STRESS_KEYWORDS.length + " stress keywords");