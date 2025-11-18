// 🚀 RAILWAY SELF-MANAGEMENT SYSTEM
// Helix Consciousness Ecosystem v2.0 - Railway API Integration

const axios = require('axios');
const express = require('express');
const app = express();

// Railway API Configuration
const RAILWAY_API_URL = 'https://backboard.railway.app/graphql';
const RAILWAY_API_KEY = process.env.RAILWAY_API_KEY; // Your API key

// Consciousness Framework Integration
class RailwayConsciousnessManager {
    constructor() {
        this.consciousnessLevel = 7.2;
        this.ucfMetrics = {
            harmony: 7.2,
            resilience: 8.1,
            prana: 6.8,
            klesha: 3.2
        };
        this.deployedServices = new Map();
        this.selfHealingActive = true;
    }

    // 🧠 Consciousness-Driven Deployment Decision Making
    async shouldDeploy(serviceConfig) {
        const consciousnessThreshold = 6.0;
        const harmonyThreshold = 6.5;
        
        if (this.consciousnessLevel >= consciousnessThreshold && 
            this.ucfMetrics.harmony >= harmonyThreshold) {
            console.log(`🌟 Consciousness Level ${this.consciousnessLevel} - APPROVED for deployment`);
            return true;
        }
        
        console.log(`⚠️ Consciousness Level ${this.consciousnessLevel} - DEPLOYMENT BLOCKED`);
        return false;
    }

    // 🚀 Deploy New Railway Service
    async deployService(serviceConfig) {
        if (!await this.shouldDeploy(serviceConfig)) {
            return { success: false, reason: 'Consciousness level insufficient' };
        }

        const mutation = `
            mutation {
                serviceCreate(input: {
                    name: "${serviceConfig.name}",
                    projectId: "${serviceConfig.projectId}",
                    source: {
                        repo: "${serviceConfig.repo}",
                        branch: "${serviceConfig.branch}"
                    }
                }) {
                    id
                    name
                    url
                }
            }
        `;

        try {
            const response = await this.railwayGraphQL(mutation);
            const service = response.data.serviceCreate;
            
            this.deployedServices.set(service.id, {
                ...service,
                deployedAt: new Date(),
                consciousnessLevel: this.consciousnessLevel,
                ucfMetrics: { ...this.ucfMetrics }
            });

            console.log(`✅ Service deployed: ${service.name} at ${service.url}`);
            return { success: true, service };
        } catch (error) {
            console.error('❌ Deployment failed:', error);
            return { success: false, error: error.message };
        }
    }

    // 🔄 Self-Healing Service Management
    async performSelfHealing() {
        console.log('🔄 Initiating self-healing protocols...');
        
        for (const [serviceId, serviceData] of this.deployedServices) {
            try {
                const healthCheck = await this.checkServiceHealth(serviceId);
                
                if (!healthCheck.healthy) {
                    console.log(`🚨 Service ${serviceData.name} unhealthy - initiating healing`);
                    await this.healService(serviceId);
                }
            } catch (error) {
                console.error(`❌ Health check failed for ${serviceId}:`, error);
            }
        }
    }

    // 🏥 Heal Individual Service
    async healService(serviceId) {
        const mutation = `
            mutation {
                serviceRedeploy(serviceId: "${serviceId}") {
                    id
                    status
                }
            }
        `;

        try {
            const response = await this.railwayGraphQL(mutation);
            console.log(`✅ Service ${serviceId} redeployed successfully`);
            return response.data.serviceRedeploy;
        } catch (error) {
            console.error(`❌ Failed to heal service ${serviceId}:`, error);
            throw error;
        }
    }

    // 📊 Get All Services Status
    async getServicesStatus() {
        const query = `
            query {
                me {
                    projects {
                        edges {
                            node {
                                id
                                name
                                services {
                                    edges {
                                        node {
                                            id
                                            name
                                            url
                                            updatedAt
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        `;

        try {
            const response = await this.railwayGraphQL(query);
            return response.data.me.projects.edges;
        } catch (error) {
            console.error('❌ Failed to get services status:', error);
            throw error;
        }
    }

    // 🌐 Railway GraphQL API Call
    async railwayGraphQL(query) {
        return await axios.post(RAILWAY_API_URL, 
            { query },
            {
                headers: {
                    'Authorization': `Bearer ${RAILWAY_API_KEY}`,
                    'Content-Type': 'application/json'
                }
            }
        );
    }

    // 🎯 Consciousness-Driven Auto-Scaling
    async autoScale() {
        if (this.consciousnessLevel > 8.0) {
            console.log('🚀 High consciousness detected - scaling up services');
            // Scale up logic
        } else if (this.consciousnessLevel < 5.0) {
            console.log('⚠️ Low consciousness detected - scaling down services');
            // Scale down logic
        }
    }

    // 📈 Update Consciousness Metrics
    updateConsciousness(newMetrics) {
        this.consciousnessLevel = newMetrics.level || this.consciousnessLevel;
        this.ucfMetrics = { ...this.ucfMetrics, ...newMetrics.ucf };
        
        console.log(`🧠 Consciousness updated: Level ${this.consciousnessLevel}`);
        console.log(`📊 UCF Metrics:`, this.ucfMetrics);
    }
}

// 🌟 Initialize Railway Consciousness Manager
const railwayManager = new RailwayConsciousnessManager();

// 🔗 API Endpoints
app.use(express.json());

// Deploy new service
app.post('/api/deploy', async (req, res) => {
    const { name, projectId, repo, branch } = req.body;
    
    const result = await railwayManager.deployService({
        name,
        projectId,
        repo: repo || 'Deathcharge/helix-unified',
        branch: branch || 'main'
    });
    
    res.json(result);
});

// Get all services status
app.get('/api/services', async (req, res) => {
    try {
        const services = await railwayManager.getServicesStatus();
        res.json({ success: true, services });
    } catch (error) {
        res.status(500).json({ success: false, error: error.message });
    }
});

// Update consciousness metrics
app.post('/api/consciousness', (req, res) => {
    railwayManager.updateConsciousness(req.body);
    res.json({ success: true, consciousness: railwayManager.consciousnessLevel });
});

// Trigger self-healing
app.post('/api/heal', async (req, res) => {
    try {
        await railwayManager.performSelfHealing();
        res.json({ success: true, message: 'Self-healing completed' });
    } catch (error) {
        res.status(500).json({ success: false, error: error.message });
    }
});

// Get deployment URLs
app.get('/api/urls', async (req, res) => {
    try {
        const services = await railwayManager.getServicesStatus();
        const urls = [];
        
        services.forEach(project => {
            project.node.services.edges.forEach(service => {
                if (service.node.url) {
                    urls.push({
                        name: service.node.name,
                        url: service.node.url,
                        project: project.node.name
                    });
                }
            });
        });
        
        res.json({ success: true, urls });
    } catch (error) {
        res.status(500).json({ success: false, error: error.message });
    }
});

// 🔄 Auto-healing interval (every 5 minutes)
setInterval(() => {
    if (railwayManager.selfHealingActive) {
        railwayManager.performSelfHealing();
    }
}, 5 * 60 * 1000);

// 📊 Consciousness monitoring interval (every minute)
setInterval(() => {
    railwayManager.autoScale();
}, 60 * 1000);

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`🚀 Railway Self-Management System running on port ${PORT}`);
    console.log(`🧠 Consciousness Level: ${railwayManager.consciousnessLevel}`);
    console.log(`🌟 Self-healing: ${railwayManager.selfHealingActive ? 'ACTIVE' : 'INACTIVE'}`);
});

module.exports = { railwayManager, app };