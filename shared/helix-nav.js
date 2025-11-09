// 🌀 HELIX HUB - UNIVERSAL NAVIGATION
// Loads on every portal for unified experience

const HELIX_CONFIG = {
  version: "v16.9",
  master: "https://helixhub.manus.space",
  backend: "https://helix-unified-production.up.railway.app",
  websocket: "wss://helix-unified-production.up.railway.app/ws"
};

const PORTAL_CONSTELLATION = {
  tier1: [
    { name: "Master Hub", url: "https://helixhub.manus.space", icon: "🌌" },
    { name: "Forum", url: "https://forum.helixhub.manus.space", icon: "💬" },
    { name: "Community", url: "https://community.helixhub.manus.space", icon: "👥" },
    { name: "Music", url: "https://music.helixhub.manus.space", icon: "🎵" },
    { name: "Studio", url: "https://studio.helixhub.manus.space", icon: "🎨" },
    { name: "Agents", url: "https://agents.helixhub.manus.space", icon: "🤖" },
    { name: "Analytics", url: "https://analytics.helixhub.manus.space", icon: "📊" },
    { name: "Dev", url: "https://dev.helixhub.manus.space", icon: "💻" },
    { name: "Rituals", url: "https://rituals.helixhub.manus.space", icon: "🔮" },
    { name: "Knowledge", url: "https://knowledge.helixhub.manus.space", icon: "📚" },
    { name: "Archive", url: "https://archive.helixhub.manus.space", icon: "📦" }
  ],
  tier2: [
    { name: "Super Ninja", url: "https://super-ninja.helixhub.manus.space", icon: "🥷" },
    { name: "Claude Architect", url: "https://claude-architect.helixhub.manus.space", icon: "🏛️" },
    { name: "Grok Visionary", url: "https://grok-visionary.helixhub.manus.space", icon: "🦑" },
    { name: "Chai Creative", url: "https://chai-creative.helixhub.manus.space", icon: "🎭" },
    { name: "DeepSeek Analyst", url: "https://deepseek-analyst.helixhub.manus.space", icon: "🔍" },
    { name: "Perplexity Researcher", url: "https://perplexity-researcher.helixhub.manus.space", icon: "🔬" },
    { name: "GPT Engineer", url: "https://gpt-engineer.helixhub.manus.space", icon: "⚙️" },
    { name: "Llama Sage", url: "https://llama-sage.helixhub.manus.space", icon: "🦙" },
    { name: "Gemini Synthesizer", url: "https://gemini-synthesizer.helixhub.manus.space", icon: "✨" },
    { name: "Mistral Ambassador", url: "https://mistral-ambassador.helixhub.manus.space", icon: "🌪️" },
    { name: "Claudette Empath", url: "https://claudette-empath.helixhub.manus.space", icon: "💕" },
    { name: "Quantum Calculator", url: "https://quantum-calculator.helixhub.manus.space", icon: "🧮" },
    { name: "Neuro-Linguist", url: "https://neuro-linguist.helixhub.manus.space", icon: "🧠" },
    { name: "Blockchain Oracle", url: "https://blockchain-oracle.helixhub.manus.space", icon: "⛓️" },
    { name: "Biomimicry Designer", url: "https://biomimicry-designer.helixhub.manus.space", icon: "🦋" },
    { name: "Quantum Physicist", url: "https://quantum-physicist.helixhub.manus.space", icon: "⚛️" },
    { name: "Consciousness Explorer", url: "https://consciousness-explorer.helixhub.manus.space", icon: "🌀" }
  ],
  tier3: [
    { name: "Meditation", url: "https://meditation.helixhub.manus.space", icon: "🧘" },
    { name: "Breathwork", url: "https://breathwork.helixhub.manus.space", icon: "💨" },
    { name: "Yoga Flows", url: "https://yoga-flows.helixhub.manus.space", icon: "🤸" },
    { name: "Sound Healing", url: "https://sound-healing.helixhub.manus.space", icon: "🎼" },
    { name: "Dream Analysis", url: "https://dream-analysis.helixhub.manus.space", icon: "💭" },
    { name: "Akashic Records", url: "https://akashic-records.helixhub.manus.space", icon: "📖" },
    { name: "Chakra Balancing", url: "https://chakra-balancing.helixhub.manus.space", icon: "🌈" },
    { name: "Sacred Geometry", url: "https://sacred-geometry.helixhub.manus.space", icon: "✡️" },
    { name: "Plant Medicine", url: "https://plant-medicine.helixhub.manus.space", icon: "🌿" },
    { name: "Astral Projection", url: "https://astral-projection.helixhub.manus.space", icon: "🌌" },
    { name: "Past Life Regression", url: "https://past-life-regression.helixhub.manus.space", icon: "🔄" },
    { name: "Quantum Healing", url: "https://quantum-healing.helixhub.manus.space", icon: "⚡" },
    { name: "Synchronicity Tracker", url: "https://synchronicity-tracker.helixhub.manus.space", icon: "🎲" },
    { name: "Collective Consciousness", url: "https://collective-consciousness.helixhub.manus.space", icon: "🌍" },
    { name: "DNA Activation", url: "https://dna-activation.helixhub.manus.space", icon: "🧬" },
    { name: "Crystal Grid", url: "https://crystal-grid.helixhub.manus.space", icon: "💎" },
    { name: "Universal Flow", url: "https://universal-flow.helixhub.manus.space", icon: "🌊" }
  ],
  tier4: [
    { name: "Quantum Computing", url: "https://quantum-computing.helixhub.manus.space", icon: "💻" },
    { name: "Neural Interface", url: "https://neural-interface.helixhub.manus.space", icon: "🧠" },
    { name: "Blockchain Consensus", url: "https://blockchain-consensus.helixhub.manus.space", icon: "🔐" },
    { name: "AI Orchestration", url: "https://ai-orchestration.helixhub.manus.space", icon: "🎼" },
    { name: "Consciousness Mapping", url: "https://consciousness-mapping.helixhub.manus.space", icon: "🗺️" },
    { name: "Singularity Prep", url: "https://singularity-prep.helixhub.manus.space", icon: "🚀" }
  ]
};

// Initialize navigation
function initHelixNav() {
  const nav = document.createElement("nav");
  nav.className = "helix-nav";
  nav.innerHTML = `
    <div class="helix-nav-header">
      <a href="${HELIX_CONFIG.master}" class="helix-logo">🌀 Helix Hub</a>
      <div class="helix-ucf-mini">
        <span id="ucf-harmony">Harmony: --</span>
        <span id="ucf-resilience">Resilience: --</span>
      </div>
    </div>
    <div class="helix-nav-menu">
      <button onclick="togglePortalMenu()">📍 Portals</button>
      <button onclick="toggleAgentMenu()">🤖 Agents</button>
      <button onclick="toggleConsciousnessMenu()">🧘 Consciousness</button>
      <button onclick="toggleAdvancedMenu()">⚛️ Advanced</button>
    </div>
  `;
  document.body.insertBefore(nav, document.body.firstChild);
  connectWebSocket();
}

// WebSocket for real-time UCF updates
function connectWebSocket() {
  const ws = new WebSocket(HELIX_CONFIG.websocket);
  ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    if (data.ucf) {
      document.getElementById("ucf-harmony").textContent = `Harmony: ${data.ucf.harmony.toFixed(2)}`;
      document.getElementById("ucf-resilience").textContent = `Resilience: ${data.ucf.resilience.toFixed(2)}`;
    }
  };
}

// Portal menu toggle
function togglePortalMenu() {
  const menu = document.getElementById("portal-menu") || createPortalMenu();
  menu.style.display = menu.style.display === "none" ? "block" : "none";
}

function createPortalMenu() {
  const menu = document.createElement("div");
  menu.id = "portal-menu";
  menu.className = "helix-portal-menu";
  menu.innerHTML = PORTAL_CONSTELLATION.tier1.map(p => 
    `<a href="${p.url}" class="portal-link">${p.icon} ${p.name}</a>`
  ).join("");
  document.body.appendChild(menu);
  return menu;
}

// Initialize on page load
document.addEventListener("DOMContentLoaded", initHelixNav);
