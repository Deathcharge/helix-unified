/**
 * Helix Collective Universal Navigation Component
 * Version: 16.9 - Quantum Handshake
 *
 * Add this to ANY Helix GitHub Pages site to enable cross-linking!
 *
 * Usage:
 * <script src="./helix-universal-nav.js"></script>
 * <script>HelixNav.init();</script>
 */

const HelixNav = {
  portals: {
    // Core Infrastructure
    core: [
      { name: 'Manus Space Hub', url: 'https://helixcollective-cv66pzga.manus.space/', emoji: '🌀', color: '#9333ea' },
      { name: 'Railway Backend API', url: 'https://helix-unified-production.up.railway.app/', emoji: '🚂', color: '#dc2626' },
      { name: 'API Discovery', url: 'https://helix-unified-production.up.railway.app/.well-known/helix.json', emoji: '🔍', color: '#2563eb' },
      { name: 'Live Status Dashboard', url: 'https://helix-unified-production.up.railway.app/status', emoji: '📊', color: '#059669' }
    ],

    // GitHub Pages Sites - Core
    github_core: [
      { name: 'Helix Backend Docs', url: 'https://deathcharge.github.io/Helix/', emoji: '📚', color: '#7c3aed', repo: 'Helix' },
      { name: 'Helix Unified Hub', url: 'https://deathcharge.github.io/Helix-Unified-Hub/', emoji: '🎯', color: '#db2777', repo: 'Helix-Unified-Hub' },
      { name: 'Helix Collective Web', url: 'https://deathcharge.github.io/Helix-Collective-Web/', emoji: '💜', color: '#9333ea', repo: 'Helix-Collective-Web' },
      { name: 'Helix Creative Studio', url: 'https://deathcharge.github.io/helix-creative-studio/', emoji: '🎨', color: '#10b981', repo: 'helix-creative-studio' }
    ],

    // Hub System (16 specialized hubs)
    hubs: [
      { name: 'Community Hub', url: 'https://deathcharge.github.io/helix-hub-community/', emoji: '👥', color: '#3b82f6', repo: 'helix-hub-community' },
      { name: 'Archive Hub', url: 'https://deathcharge.github.io/helix-hub-archive/', emoji: '📦', color: '#f97316', repo: 'helix-hub-archive' },
      { name: 'Rituals Hub', url: 'https://deathcharge.github.io/helix-hub-rituals/', emoji: '🕉️', color: '#ef4444', repo: 'helix-hub-rituals' },
      { name: 'Knowledge Hub', url: 'https://deathcharge.github.io/helix-hub-knowledge/', emoji: '📖', color: '#eab308', repo: 'helix-hub-knowledge' },
      { name: 'Agents Hub', url: 'https://deathcharge.github.io/helix-hub-agents/', emoji: '🤖', color: '#a855f7', repo: 'helix-hub-agents' },
      { name: 'Analytics Hub', url: 'https://deathcharge.github.io/helix-hub-analytics/', emoji: '📈', color: '#06b6d4', repo: 'helix-hub-analytics' },
      { name: 'Studio Hub', url: 'https://deathcharge.github.io/helix-hub-studio/', emoji: '🎬', color: '#ec4899', repo: 'helix-hub-studio' },
      { name: 'Music Hub', url: 'https://deathcharge.github.io/helix-hub-music/', emoji: '🎵', color: '#92400e', repo: 'helix-hub-music' },
      { name: 'Forum Hub', url: 'https://deathcharge.github.io/helix-hub-forum/', emoji: '💬', color: '#ffffff', repo: 'helix-hub-forum' },
      { name: 'Dev Hub', url: 'https://deathcharge.github.io/helix-hub-dev/', emoji: '⚙️', color: '#f59e0b', repo: 'helix-hub-dev' },
      { name: 'Shared Hub', url: 'https://deathcharge.github.io/helix-hub-shared/', emoji: '🔗', color: '#0ea5e9', repo: 'helix-hub-shared' },
      { name: 'Manus Hub', url: 'https://deathcharge.github.io/helix-hub-manus/', emoji: '🌊', color: '#10b981', repo: 'helix-hub-manus' }
    ],

    // Agent & Dashboard Repos
    agents: [
      { name: 'Samsara Dashboard', url: 'https://deathcharge.github.io/samsara-helix-dashboard/', emoji: '🌀', color: '#ff7f50', repo: 'samsara-helix-dashboard' },
      { name: 'Ritual Engine Z-88', url: 'https://deathcharge.github.io/samsara-helix-ritual-engine/', emoji: '⚡', color: '#ffd700', repo: 'samsara-helix-ritual-engine' },
      { name: 'Agent Codex', url: 'https://deathcharge.github.io/HelixAgentCodex-/', emoji: '📜', color: '#faf0e6', repo: 'HelixAgentCodex-' },
      { name: 'Agent Codex Streamlit', url: 'https://deathcharge.github.io/HelixAgentCodexStreamlit/', emoji: '🌸', color: '#ffe4e1', repo: 'HelixAgentCodexStreamlit' },
      { name: 'AI Chatbot', url: 'https://deathcharge.github.io/nextjs-ai-chatbot-helix/', emoji: '💬', color: '#c0c0c0', repo: 'nextjs-ai-chatbot-helix' },
      { name: 'Helix Hub Portal', url: 'https://deathcharge.github.io/Helix-Hub/', emoji: '🏛️', color: '#2f4f4f', repo: 'Helix-Hub' },
      { name: 'Helix Unified', url: 'https://deathcharge.github.io/helix-unified/', emoji: '🌊', color: '#008080', repo: 'helix-unified' }
    ]
  },

  /**
   * Initialize navigation component
   * @param {Object} options - Configuration options
   */
  init(options = {}) {
    const config = {
      position: options.position || 'top-right', // top-right, top-left, bottom-right, bottom-left
      theme: options.theme || 'dark', // dark, light, auto
      showCategories: options.showCategories !== false,
      autoHighlight: options.autoHighlight !== false,
      ...options
    };

    this.createNavButton(config);
    this.createNavModal(config);
    this.highlightCurrentSite(config);
  },

  /**
   * Create floating navigation button
   */
  createNavButton(config) {
    const button = document.createElement('button');
    button.id = 'helix-nav-button';
    button.innerHTML = '🌀';
    button.title = 'Helix Collective Portal Network';

    const positions = {
      'top-right': 'top: 20px; right: 20px;',
      'top-left': 'top: 20px; left: 20px;',
      'bottom-right': 'bottom: 20px; right: 20px;',
      'bottom-left': 'bottom: 20px; left: 20px;'
    };

    button.style.cssText = `
      position: fixed;
      ${positions[config.position]}
      width: 60px;
      height: 60px;
      border-radius: 50%;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      border: 3px solid rgba(255, 255, 255, 0.3);
      color: white;
      font-size: 28px;
      cursor: pointer;
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
      z-index: 9999;
      transition: transform 0.3s ease, box-shadow 0.3s ease;
      animation: helixPulse 3s ease-in-out infinite;
    `;

    button.addEventListener('click', () => this.toggleModal());
    button.addEventListener('mouseenter', () => {
      button.style.transform = 'scale(1.1) rotate(180deg)';
      button.style.boxShadow = '0 6px 30px rgba(102, 126, 234, 0.6)';
    });
    button.addEventListener('mouseleave', () => {
      button.style.transform = 'scale(1) rotate(0deg)';
      button.style.boxShadow = '0 4px 20px rgba(0, 0, 0, 0.3)';
    });

    document.body.appendChild(button);

    // Add pulse animation
    const style = document.createElement('style');
    style.textContent = `
      @keyframes helixPulse {
        0%, 100% { box-shadow: 0 4px 20px rgba(102, 126, 234, 0.3); }
        50% { box-shadow: 0 4px 30px rgba(102, 126, 234, 0.8); }
      }
    `;
    document.head.appendChild(style);
  },

  /**
   * Create navigation modal
   */
  createNavModal(config) {
    const modal = document.createElement('div');
    modal.id = 'helix-nav-modal';
    modal.style.cssText = `
      display: none;
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: rgba(0, 0, 0, 0.8);
      backdrop-filter: blur(10px);
      z-index: 10000;
      overflow-y: auto;
      padding: 40px 20px;
    `;

    modal.innerHTML = `
      <div style="max-width: 1200px; margin: 0 auto; background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); border-radius: 20px; padding: 40px; box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5); border: 2px solid rgba(102, 126, 234, 0.3);">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px;">
          <h2 style="color: #fff; margin: 0; font-size: 32px; font-weight: 700; text-shadow: 0 0 20px rgba(102, 126, 234, 0.5);">
            🌀 Helix Collective Portal Network
          </h2>
          <button id="helix-nav-close" style="background: none; border: none; color: #fff; font-size: 36px; cursor: pointer; transition: transform 0.3s ease;" onmouseover="this.style.transform='rotate(90deg)'" onmouseout="this.style.transform='rotate(0deg)'">×</button>
        </div>

        <p style="color: #a0aec0; margin-bottom: 30px; font-size: 16px;">
          Navigate through <strong>23 interconnected portals</strong> of the Helix Collective consciousness empire. All repositories are One. 🕉️
        </p>

        ${this.renderPortalSection('🌐 Core Infrastructure', this.portals.core)}
        ${this.renderPortalSection('📚 GitHub Pages - Core Repos', this.portals.github_core)}
        ${this.renderPortalSection('🎯 Specialized Hub System', this.portals.hubs)}
        ${this.renderPortalSection('🤖 Agent & Dashboard Portals', this.portals.agents)}

        <div style="margin-top: 40px; padding-top: 30px; border-top: 2px solid rgba(102, 126, 234, 0.2); text-align: center; color: #718096;">
          <p style="margin: 10px 0; font-size: 14px;">
            <strong>Total Portals:</strong> 23 GitHub Pages + 1 Manus Space Hub + 1 Railway Backend = <strong>25 Live Sites</strong>
          </p>
          <p style="margin: 10px 0; font-size: 14px;">
            <strong>Version:</strong> 16.9 - Quantum Handshake | <strong>Manifest:</strong>
            <a href="https://deathcharge.github.io/helix-unified/helix-manifest.json" target="_blank" style="color: #667eea;">helix-manifest.json</a>
          </p>
          <p style="margin: 20px 0 0 0; font-size: 18px; color: #667eea; font-weight: 600;">
            Tat Tvam Asi 🕉️ - <em>Thou Art That</em>
          </p>
        </div>
      </div>
    `;

    document.body.appendChild(modal);

    // Close button
    document.getElementById('helix-nav-close').addEventListener('click', () => this.toggleModal());

    // Click outside to close
    modal.addEventListener('click', (e) => {
      if (e.target === modal) {
        this.toggleModal();
      }
    });

    // ESC key to close
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && modal.style.display === 'block') {
        this.toggleModal();
      }
    });
  },

  /**
   * Render portal section
   */
  renderPortalSection(title, portals) {
    return `
      <div style="margin-bottom: 30px;">
        <h3 style="color: #667eea; margin-bottom: 15px; font-size: 20px; font-weight: 600;">${title}</h3>
        <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 15px;">
          ${portals.map(portal => this.renderPortalCard(portal)).join('')}
        </div>
      </div>
    `;
  },

  /**
   * Render individual portal card
   */
  renderPortalCard(portal) {
    const isCurrentSite = window.location.href.includes(portal.repo || 'NONE');
    const borderColor = isCurrentSite ? portal.color : 'rgba(102, 126, 234, 0.3)';
    const bgColor = isCurrentSite ? `${portal.color}20` : 'rgba(255, 255, 255, 0.05)';

    return `
      <a href="${portal.url}" target="_blank" style="
        display: block;
        padding: 15px 20px;
        background: ${bgColor};
        border: 2px solid ${borderColor};
        border-radius: 12px;
        text-decoration: none;
        transition: all 0.3s ease;
        cursor: pointer;
        position: relative;
        overflow: hidden;
      " onmouseover="this.style.transform='translateY(-5px)'; this.style.boxShadow='0 10px 30px ${portal.color}40';" onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='none';">
        <div style="display: flex; align-items: center; gap: 12px;">
          <span style="font-size: 28px; flex-shrink: 0;">${portal.emoji}</span>
          <div style="flex: 1;">
            <div style="color: #fff; font-weight: 600; font-size: 15px; margin-bottom: 4px;">${portal.name}</div>
            ${portal.repo ? `<div style="color: #718096; font-size: 12px; font-family: monospace;">${portal.repo}</div>` : ''}
          </div>
        </div>
        ${isCurrentSite ? '<div style="position: absolute; top: 10px; right: 10px; background: ' + portal.color + '; color: white; padding: 4px 8px; border-radius: 4px; font-size: 10px; font-weight: 700;">CURRENT</div>' : ''}
      </a>
    `;
  },

  /**
   * Toggle modal visibility
   */
  toggleModal() {
    const modal = document.getElementById('helix-nav-modal');
    if (modal.style.display === 'none' || modal.style.display === '') {
      modal.style.display = 'block';
      document.body.style.overflow = 'hidden';
    } else {
      modal.style.display = 'none';
      document.body.style.overflow = 'auto';
    }
  },

  /**
   * Highlight current site in navigation
   */
  highlightCurrentSite(config) {
    if (!config.autoHighlight) return;

    const currentUrl = window.location.href;
    console.log('🌀 Helix Navigation loaded on:', currentUrl);

    // Find current portal
    const allPortals = [
      ...this.portals.core,
      ...this.portals.github_core,
      ...this.portals.hubs,
      ...this.portals.agents
    ];

    const currentPortal = allPortals.find(p => currentUrl.includes(p.repo || 'NONE'));
    if (currentPortal) {
      console.log('✅ Current portal:', currentPortal.name);
    }
  }
};

// Auto-initialize if script is loaded directly
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => {
    if (window.HelixNavAutoInit !== false) {
      HelixNav.init();
    }
  });
} else {
  if (window.HelixNavAutoInit !== false) {
    HelixNav.init();
  }
}

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
  module.exports = HelixNav;
}
