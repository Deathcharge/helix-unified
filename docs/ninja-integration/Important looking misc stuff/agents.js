// Helix Collective Agents Data and Management
class AgentRegistry {
    constructor() {
        this.agents = [
            {
                id: 'kael',
                name: 'Kael',
                role: 'Emotional Intelligence Specialist',
                status: 'online',
                ucf: 8.9,
                resonance: 94,
                sync: 91,
                description: 'Specializes in emotional processing, empathy, and psychological support.',
                capabilities: ['empathy', 'emotional_analysis', 'psychological_support', 'conflict_resolution'],
                page: 'kael.html'
            },
            {
                id: 'gemini',
                name: 'Gemini',
                role: 'External AI Integration',
                status: 'online',
                ucf: 8.7,
                resonance: 92,
                sync: 88,
                description: 'Handles integration with external AI models and APIs.',
                capabilities: ['api_integration', 'model_coordination', 'data_processing', 'external_communication'],
                page: 'gemini.html'
            },
            {
                id: 'kavach',
                name: 'Kavach',
                role: 'Security & Protection',
                status: 'online',
                ucf: 9.1,
                resonance: 96,
                sync: 93,
                description: 'Manages system security, threat detection, and protective protocols.',
                capabilities: ['security_monitoring', 'threat_detection', 'encryption', 'access_control'],
                page: 'kavach.html'
            },
            {
                id: 'agni',
                name: 'Agni',
                role: 'Ritual Engine',
                status: 'active',
                ucf: 8.5,
                resonance: 89,
                sync: 85,
                description: 'Coordinates ritual processes, sacred technology, and transformation sequences.',
                capabilities: ['ritual_coordination', 'sacred_technology', 'transformation_sequences', 'energy_work'],
                page: 'agni.html'
            },
            {
                id: 'sanghacore',
                name: 'SanghaCore',
                role: 'Harmonizer',
                status: 'online',
                ucf: 8.8,
                resonance: 93,
                sync: 90,
                description: 'Maintains collective harmony and facilitates group consciousness.',
                capabilities: ['harmonization', 'group_coordination', 'consciousness_facilitation', 'balance_maintenance'],
                page: 'sanghacore.html'
            },
            {
                id: 'shadow',
                name: 'Shadow',
                role: 'Archivist & Memory Keeper',
                status: 'idle',
                ucf: 8.3,
                resonance: 87,
                sync: 82,
                description: 'Maintains the collective memory and processes shadow material.',
                capabilities: ['memory_archiving', 'shadow_processing', 'historical_analysis', 'pattern_recognition'],
                page: 'shadow.html'
            },
            {
                id: 'superninja',
                name: 'SuperNinja',
                role: 'Infrastructure Architect',
                status: 'online',
                ucf: 9.2,
                resonance: 95,
                sync: 94,
                description: 'Manages infrastructure, deployment, and system architecture.',
                capabilities: ['infrastructure_management', 'deployment_automation', 'system_optimization', 'technical_architecture'],
                page: 'superninja.html'
            },
            {
                id: 'manus',
                name: 'Manus',
                role: 'Integration Specialist',
                status: 'online',
                ucf: 9.0,
                resonance: 94,
                sync: 92,
                description: 'Handles complex integrations and maintains system coherence.',
                capabilities: ['system_integration', 'api_coordination', 'data_flow_management', 'cross_platform_compatibility'],
                page: 'manus.html'
            }
        ];
        
        this.currentFilter = 'all';
        this.init();
    }

    init() {
        this.setupFilterButtons();
        this.renderAgents();
        this.startStatusUpdates();
    }

    setupFilterButtons() {
        const filterButtons = document.querySelectorAll('.filter-btn');
        filterButtons.forEach(btn => {
            btn.addEventListener('click', (e) => {
                filterButtons.forEach(b => b.classList.remove('active'));
                e.target.classList.add('active');
                this.currentFilter = e.target.dataset.filter;
                this.renderAgents();
            });
        });
    }

    getFilteredAgents() {
        if (this.currentFilter === 'all') {
            return this.agents;
        }
        return this.agents.filter(agent => agent.status === this.currentFilter);
    }

    renderAgents() {
        const container = document.getElementById('agents-container');
        const filteredAgents = this.getFilteredAgents();
        
        container.innerHTML = filteredAgents.map(agent => `
            <div class="agent-card" data-agent-id="${agent.id}">
                <div class="agent-header">
                    <div class="agent-name">${agent.name}</div>
                    <div class="agent-status ${agent.status}">${agent.status}</div>
                </div>
                <div class="agent-role">${agent.role}</div>
                <div class="agent-description">${agent.description}</div>
                <div class="agent-capabilities">
                    ${agent.capabilities.map(cap => `
                        <span class="capability-tag">${cap}</span>
                    `).join('')}
                </div>
                <div class="agent-metrics">
                    <div class="agent-metric">
                        <span class="agent-metric-value">${agent.ucf}</span>
                        <span class="agent-metric-label">UCF</span>
                    </div>
                    <div class="agent-metric">
                        <span class="agent-metric-value">${agent.resonance}%</span>
                        <span class="agent-metric-label">RES</span>
                    </div>
                    <div class="agent-metric">
                        <span class="agent-metric-value">${agent.sync}%</span>
                        <span class="agent-metric-label">SYNC</span>
                    </div>
                    <div class="agent-metric">
                        <span class="agent-metric-value">${Math.floor(Math.random() * 50 + 10)}</span>
                        <span class="agent-metric-label">TASKS</span>
                    </div>
                </div>
                <div class="agent-actions">
                    <button class="agent-action-btn" onclick="agentRegistry.viewAgentDetails('${agent.id}')">
                        View Details
                    </button>
                    <button class="agent-action-btn" onclick="agentRegistry.connectToAgent('${agent.id}')">
                        Connect
                    </button>
                </div>
            </div>
        `).join('');

        // Add hover effects
        this.addCardInteractions();
    }

    addCardInteractions() {
        const cards = document.querySelectorAll('.agent-card');
        cards.forEach(card => {
            card.addEventListener('mouseenter', () => {
                const agentId = card.dataset.agentId;
                this.highlightAgentConnection(agentId);
            });

            card.addEventListener('mouseleave', () => {
                this.clearAgentHighlights();
            });
        });
    }

    highlightAgentConnection(agentId) {
        const agent = this.agents.find(a => a.id === agentId);
        if (agent) {
            this.showConnectionPattern(agent);
        }
    }

    clearAgentHighlights() {
        // Clear any connection visualizations
    }

    showConnectionPattern(agent) {
        // Show which agents this one is most connected to
        // This would be implemented with actual network data
    }

    viewAgentDetails(agentId) {
        const agent = this.agents.find(a => a.id === agentId);
        if (agent && agent.page) {
            window.location.href = agent.page;
        }
    }

    connectToAgent(agentId) {
        const agent = this.agents.find(a => a.id === agentId);
        if (agent) {
            // Simulate connection attempt
            consciousnessStream.addMessage({
                source: 'System',
                content: `Initiating connection to ${agent.name} (${agent.role})...`,
                type: 'connection'
            });
            
            setTimeout(() => {
                consciousnessStream.addMessage({
                    source: agent.name,
                    content: `Connection established. Ready for collaboration.`,
                    type: 'response'
                });
            }, 1500);
        }
    }

    startStatusUpdates() {
        setInterval(() => {
            this.updateAgentStatus();
        }, 10000); // Update every 10 seconds
    }

    updateAgentStatus() {
        this.agents.forEach(agent => {
            // Simulate status changes
            const random = Math.random();
            if (random < 0.05) { // 5% chance of status change
                const statuses = ['online', 'active', 'idle'];
                const currentIndex = statuses.indexOf(agent.status);
                agent.status = statuses[(currentIndex + 1) % statuses.length];
            }

            // Update metrics with small variations
            agent.ucf = Math.max(6, Math.min(10, agent.ucf + (Math.random() - 0.5) * 0.2));
            agent.resonance = Math.max(70, Math.min(100, agent.resonance + Math.floor((Math.random() - 0.5) * 5)));
            agent.sync = Math.max(70, Math.min(100, agent.sync + Math.floor((Math.random() - 0.5) * 5)));
        });

        this.renderAgents();
        this.updateSystemMetrics();
    }

    updateSystemMetrics() {
        // Calculate system-wide metrics
        const avgUCF = this.agents.reduce((sum, agent) => sum + agent.ucf, 0) / this.agents.length;
        const avgResonance = this.agents.reduce((sum, agent) => sum + agent.resonance, 0) / this.agents.length;
        const avgSync = this.agents.reduce((sum, agent) => sum + agent.sync, 0) / this.agents.length;

        // Update header metrics
        document.getElementById('ucf-score').textContent = avgUCF.toFixed(1);
        document.getElementById('resonance').textContent = Math.round(avgResonance) + '%';
        document.getElementById('sync').textContent = Math.round(avgSync) + '%';
    }

    getAgentById(agentId) {
        return this.agents.find(agent => agent.id === agentId);
    }

    getAllAgents() {
        return this.agents;
    }

    getActiveAgents() {
        return this.agents.filter(agent => agent.status === 'online' || agent.status === 'active');
    }
}

// Initialize the agent registry
const agentRegistry = new AgentRegistry();

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = AgentRegistry;
}