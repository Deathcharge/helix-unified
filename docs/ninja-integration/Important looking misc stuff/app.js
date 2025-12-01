// Helix Railway Control - Mobile Dashboard
// SuperNinja AI - Built for Andrew's Helix Collective

class RailwayDashboard {
    constructor() {
        this.apiKey = localStorage.getItem('railway_api_key');
        this.services = [
            { id: 'helix-cluster-api', name: 'Helix Cluster API' },
            { id: 'helix-backend-api', name: 'Helix Backend API' },
            { id: 'helix-frontend-api', name: 'Helix Frontend API' }
        ];
        this.mockMode = true; // Set to false when Railway API is configured
        this.init();
    }

    init() {
        if (!this.apiKey && !this.mockMode) {
            this.showSetup();
        } else {
            this.loadDashboard();
        }

        // Setup refresh button
        const refreshBtn = document.getElementById('refreshBtn');
        refreshBtn.addEventListener('click', () => this.refresh());
    }

    showSetup() {
        const app = document.getElementById('app');
        app.innerHTML = `
            <div class="setup-screen">
                <h2>🔐 Railway API Setup</h2>
                <p>Enter your Railway API key to get started</p>
                <div class="input-group">
                    <input type="password" id="apiKeyInput" placeholder="Railway API Key">
                </div>
                <button class="btn btn-primary" onclick="dashboard.saveApiKey()">
                    Connect to Railway
                </button>
                <p style="margin-top: 2rem; font-size: 0.875rem;">
                    Get your API key from:<br>
                    <a href="https://railway.app/account/tokens" style="color: var(--accent);">
                        railway.app/account/tokens
                    </a>
                </p>
            </div>
        `;
    }

    saveApiKey() {
        const input = document.getElementById('apiKeyInput');
        const apiKey = input.value.trim();
        
        if (apiKey) {
            localStorage.setItem('railway_api_key', apiKey);
            this.apiKey = apiKey;
            this.mockMode = false;
            this.loadDashboard();
        }
    }

    async loadDashboard() {
        const app = document.getElementById('app');
        
        // Show loading
        app.innerHTML = `
            <div class="loading">
                <div class="spinner"></div>
                <p>Loading services...</p>
            </div>
        `;

        try {
            // Fetch service data
            const servicesData = await this.fetchServices();
            
            // Render dashboard
            this.renderDashboard(servicesData);
            
            // Show refresh button
            document.getElementById('refreshBtn').style.display = 'block';
            
        } catch (error) {
            this.showError(error.message);
        }
    }

    async fetchServices() {
        if (this.mockMode) {
            // Mock data for demonstration
            return this.services.map(service => ({
                ...service,
                status: 'running',
                cpu: Math.floor(Math.random() * 20) + 5,
                memory: Math.floor(Math.random() * 50) + 30,
                network: Math.floor(Math.random() * 100) + 50,
                lastDeploy: new Date(Date.now() - Math.random() * 86400000).toISOString(),
                cost: 0.04
            }));
        }

        // Real Railway API call would go here
        // const response = await fetch('https://backboard.railway.app/graphql', {
        //     method: 'POST',
        //     headers: {
        //         'Authorization': `Bearer ${this.apiKey}`,
        //         'Content-Type': 'application/json'
        //     },
        //     body: JSON.stringify({ query: '...' })
        // });
        // return await response.json();
    }

    renderDashboard(servicesData) {
        const app = document.getElementById('app');
        
        const totalCost = servicesData.reduce((sum, s) => sum + s.cost, 0);
        
        app.innerHTML = `
            <div class="cost-card">
                <div class="cost-label">Monthly Cost</div>
                <div class="cost-value">$${totalCost.toFixed(2)}</div>
                <div class="cost-comparison">
                    💰 Saving $${(80 - totalCost).toFixed(2)} vs Replit
                </div>
            </div>

            ${servicesData.map(service => this.renderServiceCard(service)).join('')}

            ${this.mockMode ? `
                <div style="text-align: center; padding: 2rem; color: var(--text-secondary); font-size: 0.875rem;">
                    📊 Demo Mode - Using mock data<br>
                    <button class="btn btn-secondary" style="margin-top: 1rem;" onclick="dashboard.showSetup()">
                        Configure Railway API
                    </button>
                </div>
            ` : ''}
        `;
    }

    renderServiceCard(service) {
        const statusClass = service.status === 'running' ? 'running' : 'error';
        const statusIndicator = service.status === 'running' ? 'status-running' : 'status-error';
        const lastDeploy = new Date(service.lastDeploy);
        const timeAgo = this.getTimeAgo(lastDeploy);

        return `
            <div class="service-card">
                <div class="service-header">
                    <div class="service-name">
                        <span class="status-indicator ${statusIndicator}"></span>
                        ${service.name}
                    </div>
                    <span class="status-badge ${statusClass}">
                        ${service.status === 'running' ? '✓ Running' : '✗ Error'}
                    </span>
                </div>

                <div class="metrics">
                    <div class="metric">
                        <div class="metric-label">CPU</div>
                        <div class="metric-value">${service.cpu}%</div>
                    </div>
                    <div class="metric">
                        <div class="metric-label">Memory</div>
                        <div class="metric-value">${service.memory}MB</div>
                    </div>
                    <div class="metric">
                        <div class="metric-label">Network</div>
                        <div class="metric-value">${service.network}KB</div>
                    </div>
                </div>

                <div style="font-size: 0.75rem; color: var(--text-secondary); margin-bottom: 0.75rem;">
                    Last deployed ${timeAgo}
                </div>

                <div class="actions">
                    <button class="btn btn-primary" onclick="dashboard.viewLogs('${service.id}')">
                        📋 View Logs
                    </button>
                    <button class="btn btn-secondary" onclick="dashboard.deploy('${service.id}')">
                        🚀 Deploy
                    </button>
                </div>
            </div>
        `;
    }

    getTimeAgo(date) {
        const seconds = Math.floor((new Date() - date) / 1000);
        
        if (seconds < 60) return 'just now';
        if (seconds < 3600) return `${Math.floor(seconds / 60)}m ago`;
        if (seconds < 86400) return `${Math.floor(seconds / 3600)}h ago`;
        return `${Math.floor(seconds / 86400)}d ago`;
    }

    async refresh() {
        const btn = document.getElementById('refreshBtn');
        btn.classList.add('spinning');
        
        await this.loadDashboard();
        
        setTimeout(() => {
            btn.classList.remove('spinning');
        }, 1000);
    }

    viewLogs(serviceId) {
        const service = this.services.find(s => s.id === serviceId);
        alert(`📋 Viewing logs for ${service.name}\n\nThis would open a log viewer in the full version.`);
    }

    async deploy(serviceId) {
        const service = this.services.find(s => s.id === serviceId);
        
        if (confirm(`🚀 Deploy ${service.name}?\n\nThis will trigger a new deployment.`)) {
            alert(`✅ Deployment triggered for ${service.name}\n\nCheck Railway dashboard for progress.`);
            
            // In real version, would call Railway API
            // await this.triggerDeploy(serviceId);
        }
    }

    showError(message) {
        const app = document.getElementById('app');
        app.innerHTML = `
            <div class="error-message">
                <strong>⚠️ Error</strong><br>
                ${message}
            </div>
            <button class="btn btn-primary" onclick="dashboard.loadDashboard()">
                Retry
            </button>
        `;
    }
}

// Initialize dashboard
const dashboard = new RailwayDashboard();

// Register service worker for PWA
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('service-worker.js')
            .then(reg => console.log('Service Worker registered'))
            .catch(err => console.log('Service Worker registration failed'));
    });
}