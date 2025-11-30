// Helix Collective Dashboard - Main Controller
class DashboardController {
    constructor() {
        this.startTime = Date.now();
        this.systemMetrics = {
            uptime: 0,
            totalConnections: 0,
            activeAgents: 0,
            networkStatus: 'online'
        };
        this.init();
    }

    init() {
        this.updateSystemTime();
        this.startSystemMetrics();
        this.initializeAnimations();
        this.setupKeyboardShortcuts();
        this.initializeNotifications();
    }

    updateSystemTime() {
        const updateTimeDisplay = () => {
            const timeElement = document.getElementById('system-time');
            if (timeElement) {
                const now = new Date();
                timeElement.textContent = now.toLocaleString('en-US', {
                    weekday: 'short',
                    year: 'numeric',
                    month: 'short',
                    day: 'numeric',
                    hour: '2-digit',
                    minute: '2-digit',
                    second: '2-digit'
                });
            }
        };

        updateTimeDisplay();
        setInterval(updateTimeDisplay, 1000);
    }

    startSystemMetrics() {
        setInterval(() => {
            this.updateSystemMetrics();
        }, 10000);

        // Initial update
        this.updateSystemMetrics();
    }

    updateSystemMetrics() {
        this.systemMetrics.uptime = Date.now() - this.startTime;
        this.systemMetrics.totalConnections = Math.floor(Math.random() * 500 + 1000);
        this.systemMetrics.activeAgents = agentRegistry.getActiveAgents().length;
        
        // Update system status if needed
        const statusIndicators = document.querySelectorAll('.status-indicator');
        statusIndicators.forEach(indicator => {
            if (this.systemMetrics.networkStatus === 'online') {
                indicator.classList.add('online');
                indicator.classList.remove('offline');
            } else {
                indicator.classList.add('offline');
                indicator.classList.remove('online');
            }
        });
    }

    initializeAnimations() {
        this.animateCosmicBackground();
        this.initializeParticleEffects();
        this.animateGlyphs();
    }

    animateCosmicBackground() {
        const stars = document.querySelector('.stars');
        const nebula = document.querySelector('.nebula');
        const aurora = document.querySelector('.aurora');

        // Additional animation variations can be added here
        setInterval(() => {
            if (aurora) {
                aurora.style.opacity = Math.random() * 0.3 + 0.3;
            }
        }, 5000);
    }

    initializeParticleEffects() {
        // Create floating particles for enhanced visual effect
        const createParticle = () => {
            const particle = document.createElement('div');
            particle.className = 'cosmic-particle';
            particle.style.cssText = `
                position: fixed;
                width: 2px;
                height: 2px;
                background: #00ffcc;
                border-radius: 50%;
                pointer-events: none;
                z-index: 1;
                left: ${Math.random() * window.innerWidth}px;
                top: ${window.innerHeight}px;
                box-shadow: 0 0 6px #00ffcc;
            `;

            document.body.appendChild(particle);

            const duration = Math.random() * 10000 + 5000;
            const endX = (Math.random() - 0.5) * window.innerWidth;
            const endY = -100;

            particle.animate([
                { transform: 'translate(0, 0)', opacity: 1 },
                { transform: `translate(${endX}px, ${endY}px)`, opacity: 0 }
            ], {
                duration: duration,
                easing: 'ease-out'
            }).onfinish = () => particle.remove();
        };

        // Create particles periodically
        setInterval(createParticle, 2000);
    }

    animateGlyphs() {
        // Add subtle animations to agent cards and other elements
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.animation = 'glow 3s ease-in-out infinite';
                }
            });
        });

        document.querySelectorAll('.agent-card').forEach(card => {
            observer.observe(card);
        });
    }

    setupKeyboardShortcuts() {
        document.addEventListener('keydown', (e) => {
            // Ctrl/Cmd + K: Quick agent search
            if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
                e.preventDefault();
                this.openAgentSearch();
            }

            // Ctrl/Cmd + D: Toggle dashboard dark mode (if implemented)
            if ((e.ctrlKey || e.metaKey) && e.key === 'd') {
                e.preventDefault();
                this.toggleDarkMode();
            }

            // Ctrl/Cmd + R: Refresh metrics
            if ((e.ctrlKey || e.metaKey) && e.key === 'r') {
                e.preventDefault();
                this.refreshAllMetrics();
            }

            // Escape: Close modals
            if (e.key === 'Escape') {
                this.closeAllModals();
            }
        });
    }

    openAgentSearch() {
        const modal = document.createElement('div');
        modal.className = 'search-modal';
        modal.innerHTML = `
            <div class="search-modal-content">
                <div class="search-header">
                    <h3>Quick Agent Search</h3>
                    <button class="close-search">&times;</button>
                </div>
                <input type="text" class="agent-search-input" placeholder="Search agents..." autofocus>
                <div class="search-results"></div>
            </div>
        `;

        modal.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(10, 10, 15, 0.95);
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 10000;
        `;

        document.body.appendChild(modal);

        const input = modal.querySelector('.agent-search-input');
        const results = modal.querySelector('.search-results');
        const closeBtn = modal.querySelector('.close-search');

        const performSearch = (query) => {
            const agents = agentRegistry.getAllAgents();
            const filtered = agents.filter(agent => 
                agent.name.toLowerCase().includes(query.toLowerCase()) ||
                agent.role.toLowerCase().includes(query.toLowerCase()) ||
                agent.capabilities.some(cap => cap.toLowerCase().includes(query.toLowerCase()))
            );

            results.innerHTML = filtered.map(agent => `
                <div class="search-result-item" data-agent-id="${agent.id}">
                    <div class="search-result-name">${agent.name}</div>
                    <div class="search-result-role">${agent.role}</div>
                    <div class="search-result-capabilities">
                        ${agent.capabilities.slice(0, 3).join(', ')}
                    </div>
                </div>
            `).join('');

            results.querySelectorAll('.search-result-item').forEach(item => {
                item.addEventListener('click', () => {
                    const agentId = item.dataset.agentId;
                    document.body.removeChild(modal);
                    agentRegistry.viewAgentDetails(agentId);
                });
            });
        };

        input.addEventListener('input', (e) => {
            performSearch(e.target.value);
        });

        closeBtn.addEventListener('click', () => {
            document.body.removeChild(modal);
        });

        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                document.body.removeChild(modal);
            }
        });

        // Initial search to show all agents
        performSearch('');
    }

    toggleDarkMode() {
        document.body.classList.toggle('light-mode');
        const isLightMode = document.body.classList.contains('light-mode');
        
        consciousnessStream.addMessage({
            source: 'System',
            content: `Theme changed to ${isLightMode ? 'light' : 'dark'} mode.`,
            type: 'system'
        });
    }

    refreshAllMetrics() {
        metricsVisualizer.resetAllCharts();
        agentRegistry.updateAgentStatus();
        
        consciousnessStream.addMessage({
            source: 'System',
            content: 'All metrics refreshed and synchronized.',
            type: 'system'
        });
    }

    closeAllModals() {
        document.querySelectorAll('.search-modal, .agent-detail-modal').forEach(modal => {
            if (modal.parentNode) {
                modal.parentNode.removeChild(modal);
            }
        });
    }

    initializeNotifications() {
        this.checkPermissions();
        this.setupSystemNotifications();
    }

    checkPermissions() {
        if ('Notification' in window && Notification.permission === 'default') {
            // Request permission on first user interaction
            document.addEventListener('click', () => {
                Notification.requestPermission();
            }, { once: true });
        }
    }

    setupSystemNotifications() {
        // Monitor for important events
        setInterval(() => {
            const ucfScore = parseFloat(document.getElementById('ucf-score')?.textContent || 0);
            
            if (ucfScore > 9.5) {
                this.showNotification('High UCF Alert', `Consciousness level reached ${ucfScore}!`, 'success');
            }
            
            const activeAgents = this.systemMetrics.activeAgents;
            if (activeAgents < 4) {
                this.showNotification('Low Activity', `Only ${activeAgents} agents currently active`, 'warning');
            }
        }, 60000); // Check every minute
    }

    showNotification(title, message, type = 'info') {
        if ('Notification' in window && Notification.permission === 'granted') {
            const icon = type === 'success' ? '✅' : type === 'warning' ? '⚠️' : 'ℹ️';
            
            const notification = new Notification(`${icon} ${title}`, {
                body: message,
                icon: 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><text y=".9em" font-size="90">🌀</text></svg>',
                tag: 'helix-dashboard'
            });

            setTimeout(() => notification.close(), 5000);
        }

        // Also show in-console message
        console.log(`[${type.toUpperCase()}] ${title}: ${message}`);
    }

    // Performance monitoring
    monitorPerformance() {
        if ('performance' in window) {
            const perfData = performance.getEntriesByType('navigation')[0];
            const loadTime = perfData.loadEventEnd - perfData.loadEventStart;
            
            console.log(`Dashboard load time: ${loadTime}ms`);
            
            // Monitor memory usage if available
            if ('memory' in performance) {
                const memory = performance.memory;
                const usedMB = (memory.usedJSHeapSize / 1024 / 1024).toFixed(2);
                console.log(`Memory usage: ${usedMB}MB`);
            }
        }
    }

    // Export dashboard state
    exportDashboardState() {
        const state = {
            timestamp: new Date().toISOString(),
            systemMetrics: this.systemMetrics,
            agents: agentRegistry.getAllAgents(),
            consciousnessMessages: consciousnessStream.messages,
            charts: {
                latency: metricsVisualizer.exportChartData('latency'),
                load: metricsVisualizer.exportChartData('load'),
                memory: metricsVisualizer.exportChartData('memory'),
                density: metricsVisualizer.exportChartData('density')
            }
        };

        return state;
    }

    // Handle visibility changes
    handleVisibilityChange() {
        document.addEventListener('visibilitychange', () => {
            if (document.hidden) {
                console.log('Dashboard hidden - reducing update frequency');
            } else {
                console.log('Dashboard visible - resuming normal updates');
                this.refreshAllMetrics();
            }
        });
    }
}

// Add glow animation to styles
const style = document.createElement('style');
style.textContent = `
    @keyframes glow {
        0%, 100% { box-shadow: 0 0 5px rgba(0, 255, 204, 0.5); }
        50% { box-shadow: 0 0 20px rgba(0, 255, 204, 0.8), 0 0 30px rgba(0, 255, 204, 0.6); }
    }
    
    .search-modal {
        font-family: 'Space Mono', monospace;
    }
    
    .search-modal-content {
        background: var(--bg-secondary);
        border: 1px solid var(--border-color);
        border-radius: 12px;
        padding: 2rem;
        min-width: 500px;
        max-width: 80vw;
        max-height: 80vh;
        overflow-y: auto;
    }
    
    .search-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1rem;
    }
    
    .close-search {
        background: none;
        border: none;
        color: var(--text-primary);
        font-size: 1.5rem;
        cursor: pointer;
    }
    
    .agent-search-input {
        width: 100%;
        padding: 1rem;
        background: var(--bg-tertiary);
        border: 1px solid var(--border-color);
        border-radius: 8px;
        color: var(--text-primary);
        font-family: inherit;
        margin-bottom: 1rem;
    }
    
    .search-result-item {
        padding: 1rem;
        background: var(--bg-tertiary);
        border: 1px solid var(--border-color);
        border-radius: 8px;
        margin-bottom: 0.5rem;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .search-result-item:hover {
        border-color: var(--primary-color);
        background: rgba(0, 255, 204, 0.1);
    }
    
    .search-result-name {
        font-weight: bold;
        color: var(--primary-color);
    }
    
    .search-result-role {
        color: var(--text-secondary);
        margin: 0.25rem 0;
    }
    
    .search-result-capabilities {
        font-size: 0.8rem;
        color: var(--text-secondary);
    }
`;
document.head.appendChild(style);

// Initialize the dashboard controller
const dashboardController = new DashboardController();

// Monitor performance
dashboardController.monitorPerformance();
dashboardController.handleVisibilityChange();

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = DashboardController;
}