/**
 * Helix Collective - Shared Navigation Component
 *
 * This component can be embedded in any Helix portal to provide
 * unified navigation across the entire portal constellation.
 *
 * Usage:
 * <script src="https://helix-hub.manus.space/helix-nav-component.js"></script>
 * <div id="helix-nav"></div>
 */

(function() {
    'use strict';

    // Portal Directory Configuration
    const PORTALS = [
        { id: 'hub', name: 'Hub', icon: '🌀', url: '/', description: 'Portal Directory' },
        { id: 'chat', name: 'Chat', icon: '💬', url: '/chat', description: 'Agent Chat' },
        { id: 'forum', name: 'Forum', icon: '🗣️', url: '#', description: 'Community' },
        { id: 'music', name: 'Music', icon: '🎵', url: '#', description: 'KAIRO Studio' },
        { id: 'agents', name: 'Agents', icon: '🤖', url: '/chat', description: 'Agent Hub' },
        { id: 'rituals', name: 'Rituals', icon: '🔮', url: '#', description: 'Z-88 Engine' },
        { id: 'knowledge', name: 'Docs', icon: '📚', url: '#', description: 'Knowledge Base' },
        { id: 'analytics', name: 'Analytics', icon: '📊', url: '#', description: 'Metrics' },
        { id: 'studio', name: 'Studio', icon: '🎨', url: '#', description: 'Creative Tools' },
        { id: 'dev', name: 'Dev', icon: '💻', url: '#', description: 'Developer Console' },
    ];

    // Navigation styles (injected into page)
    const NAV_STYLES = `
        <style id="helix-nav-styles">
            .helix-nav-container {
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                background: rgba(15, 12, 41, 0.95);
                backdrop-filter: blur(10px);
                padding: 1rem 2rem;
                display: flex;
                justify-content: space-between;
                align-items: center;
                z-index: 9999;
                border-bottom: 1px solid rgba(255, 255, 255, 0.1);
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
            }

            .helix-nav-logo {
                font-size: 1.5rem;
                font-weight: bold;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                cursor: pointer;
                text-decoration: none;
                transition: filter 0.3s;
            }

            .helix-nav-logo:hover {
                filter: brightness(1.2);
            }

            .helix-nav-links {
                display: flex;
                gap: 2rem;
                align-items: center;
                flex: 1;
                justify-content: center;
            }

            .helix-nav-link {
                color: rgba(255, 255, 255, 0.8);
                text-decoration: none;
                transition: all 0.3s;
                font-size: 0.95rem;
                display: flex;
                align-items: center;
                gap: 0.3rem;
                padding: 0.4rem 0.8rem;
                border-radius: 8px;
            }

            .helix-nav-link:hover {
                color: #667eea;
                background: rgba(255, 255, 255, 0.05);
                transform: translateY(-2px);
            }

            .helix-nav-link.active {
                color: #667eea;
                background: rgba(102, 126, 234, 0.2);
            }

            .helix-nav-menu {
                display: flex;
                align-items: center;
                gap: 1rem;
            }

            .helix-nav-status {
                display: flex;
                align-items: center;
                gap: 0.5rem;
                padding: 0.4rem 1rem;
                background: rgba(74, 222, 128, 0.1);
                border-radius: 20px;
                font-size: 0.85rem;
                color: rgba(74, 222, 128, 1);
            }

            .helix-nav-status-dot {
                width: 8px;
                height: 8px;
                background: #4ade80;
                border-radius: 50%;
                animation: helix-pulse 2s ease-in-out infinite;
            }

            @keyframes helix-pulse {
                0%, 100% { opacity: 1; transform: scale(1); }
                50% { opacity: 0.6; transform: scale(0.8); }
            }

            .helix-nav-login-btn {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border: none;
                padding: 0.6rem 1.5rem;
                border-radius: 25px;
                color: white;
                cursor: pointer;
                font-weight: 600;
                transition: all 0.3s;
                font-size: 0.9rem;
            }

            .helix-nav-login-btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
            }

            .helix-nav-user {
                display: flex;
                align-items: center;
                gap: 0.8rem;
                cursor: pointer;
                padding: 0.4rem 0.8rem;
                border-radius: 8px;
                transition: all 0.3s;
            }

            .helix-nav-user:hover {
                background: rgba(255, 255, 255, 0.05);
            }

            .helix-nav-avatar {
                width: 36px;
                height: 36px;
                border-radius: 50%;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 1.2rem;
            }

            .helix-nav-username {
                color: rgba(255, 255, 255, 0.9);
                font-size: 0.9rem;
                font-weight: 500;
            }

            /* Mobile menu toggle */
            .helix-nav-mobile-toggle {
                display: none;
                background: none;
                border: none;
                color: white;
                font-size: 1.5rem;
                cursor: pointer;
            }

            /* Mobile responsive */
            @media (max-width: 768px) {
                .helix-nav-links {
                    display: none;
                    position: absolute;
                    top: 100%;
                    left: 0;
                    right: 0;
                    background: rgba(15, 12, 41, 0.98);
                    flex-direction: column;
                    gap: 0;
                    padding: 1rem 0;
                }

                .helix-nav-links.mobile-open {
                    display: flex;
                }

                .helix-nav-link {
                    width: 100%;
                    padding: 1rem 2rem;
                    border-radius: 0;
                }

                .helix-nav-mobile-toggle {
                    display: block;
                }

                .helix-nav-status {
                    display: none;
                }
            }

            /* Body padding to account for fixed nav */
            body {
                padding-top: 70px !important;
            }
        </style>
    `;

    // Navigation HTML template
    function generateNavHTML(config = {}) {
        const {
            currentPortal = 'hub',
            showStatus = true,
            user = null,
        } = config;

        const statusHTML = showStatus ? `
            <div class="helix-nav-status">
                <span class="helix-nav-status-dot"></span>
                <span id="helix-nav-status-text">All Systems Operational</span>
            </div>
        ` : '';

        const userHTML = user ? `
            <div class="helix-nav-user" onclick="HelixNav.openUserMenu()">
                <div class="helix-nav-avatar">${user.avatar || '👤'}</div>
                <span class="helix-nav-username">${user.username}</span>
            </div>
        ` : `
            <button class="helix-nav-login-btn" onclick="HelixNav.login()">
                Login with Discord
            </button>
        `;

        const linksHTML = PORTALS.map(portal => {
            const activeClass = portal.id === currentPortal ? 'active' : '';
            const isExternal = portal.url.startsWith('http');
            const target = isExternal ? 'target="_blank"' : '';

            return `
                <a href="${portal.url}"
                   class="helix-nav-link ${activeClass}"
                   title="${portal.description}"
                   ${target}>
                    <span>${portal.icon}</span>
                    <span>${portal.name}</span>
                </a>
            `;
        }).join('');

        return `
            <nav class="helix-nav-container">
                <a href="/" class="helix-nav-logo">🌀 Helix Collective</a>

                <button class="helix-nav-mobile-toggle" onclick="HelixNav.toggleMobileMenu()">
                    ☰
                </button>

                <div class="helix-nav-links" id="helix-nav-links">
                    ${linksHTML}
                </div>

                <div class="helix-nav-menu">
                    ${statusHTML}
                    ${userHTML}
                </div>
            </nav>
        `;
    }

    // HelixNav API
    window.HelixNav = {
        /**
         * Initialize the navigation component
         */
        init: function(config = {}) {
            // Inject styles
            if (!document.getElementById('helix-nav-styles')) {
                document.head.insertAdjacentHTML('beforeend', NAV_STYLES);
            }

            // Find or create nav container
            let navContainer = document.getElementById('helix-nav');
            if (!navContainer) {
                navContainer = document.createElement('div');
                navContainer.id = 'helix-nav';
                document.body.insertBefore(navContainer, document.body.firstChild);
            }

            // Render navigation
            navContainer.innerHTML = generateNavHTML(config);

            // Start status updates
            if (config.showStatus !== false) {
                this.updateStatus();
            }

            console.log('🌀 Helix Navigation initialized');
        },

        /**
         * Update system status indicator
         */
        updateStatus: async function() {
            try {
                const response = await fetch('/api/collective/status');
                if (response.ok) {
                    const statusText = document.getElementById('helix-nav-status-text');
                    if (statusText) {
                        statusText.textContent = 'All Systems Operational';
                    }
                }
            } catch (error) {
                const statusText = document.getElementById('helix-nav-status-text');
                if (statusText) {
                    statusText.textContent = 'Status Unknown';
                }
            }

            // Update every 30 seconds
            setTimeout(() => this.updateStatus(), 30000);
        },

        /**
         * Discord OAuth login
         */
        login: function() {
            // TODO: Implement Discord OAuth flow
            const clientId = ''; // Set your Discord client ID
            const redirectUri = encodeURIComponent(window.location.origin + '/auth/callback');
            const scope = 'identify email';

            // For now, show placeholder
            alert('Discord OAuth coming soon! 🚀\n\nThis will redirect to Discord for authentication.');

            // Uncomment when ready:
            // window.location.href = `https://discord.com/api/oauth2/authorize?client_id=${clientId}&redirect_uri=${redirectUri}&response_type=code&scope=${scope}`;
        },

        /**
         * Open user menu dropdown
         */
        openUserMenu: function() {
            // TODO: Implement user menu dropdown
            alert('User menu coming soon! 🚀\n\nFeatures:\n- Profile\n- Settings\n- Logout');
        },

        /**
         * Toggle mobile menu
         */
        toggleMobileMenu: function() {
            const links = document.getElementById('helix-nav-links');
            if (links) {
                links.classList.toggle('mobile-open');
            }
        },

        /**
         * Set current user
         */
        setUser: function(user) {
            this.init({ user });
        },

        /**
         * Logout user
         */
        logout: function() {
            // Clear user session
            localStorage.removeItem('helix_user');
            sessionStorage.removeItem('helix_token');
            this.init(); // Refresh nav
            window.location.href = '/';
        },
    };

    // Auto-initialize on DOM ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function() {
            // Check if auto-init is enabled (default: true)
            const autoInit = !document.querySelector('[data-helix-nav-manual]');
            if (autoInit) {
                HelixNav.init();
            }
        });
    } else {
        // DOM already loaded
        const autoInit = !document.querySelector('[data-helix-nav-manual]');
        if (autoInit) {
            HelixNav.init();
        }
    }

})();
