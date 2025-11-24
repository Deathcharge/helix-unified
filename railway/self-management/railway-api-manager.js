// 🚀 RAILWAY SELF-MANAGEMENT SYSTEM
// Helix Consciousness Ecosystem v2.0 - Railway API Integration

const axios = require('axios');
const express = require('express');
const app = express();

// Railway API Configuration
const RAILWAY_API_URL = 'https://backboard.railway.app/graphql';
const RAILWAY_API_KEY = process.env.RAILWAY_API_KEY; // Your API key

// Service templates for different service types
const serviceTemplates = {
  websocket: {
    name: "websocket-consciousness-streaming",
    envVars: ["JWT_SECRET", "REDIS_URL", "WEBSOCKET_PORT"],
    buildCommand: "pip install -r requirements.txt",
    startCommand: "uvicorn main:app --host 0.0.0.0 --port $PORT",
    healthCheckPath: "/health"
  },
  orchestration: {
    name: "agent-orchestration",
    envVars: ["DATABASE_URL", "REDIS_URL", "JWT_SECRET"],
    buildCommand: "pip install -r requirements.txt",
    startCommand: "uvicorn main:app --host 0.0.0.0 --port $PORT",
    healthCheckPath: "/health"
  },
  voice: {
    name: "voice-processing",
    envVars: ["GOOGLE_CLOUD_KEY", "REDIS_URL", "AUDIO_TEMP_DIR"],
    buildCommand: "pip install -r requirements.txt",
    startCommand: "uvicorn main:app --host 0.0.0.0 --port $PORT",
    healthCheckPath: "/health"
  },
  zapier: {
    name: "zapier-integration",
    envVars: ["ZAPIER_SECRET", "REDIS_URL", "WEBHOOK_URL"],
    buildCommand: "pip install -r requirements.txt",
    startCommand: "uvicorn main:app --host 0.0.0.0 --port $PORT",
    healthCheckPath: "/health"
  }
};

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
        this.serviceConnections = new Map();
        this.selfHealingActive = true;
    }

    // 🤔 Consciousness-Driven Deployment Decision Making
    async shouldDeploy(serviceConfig) {
        const consciousnessThreshold = 6.0;
        const harmonyThreshold = 6.5;
        
        // For critical services, require higher consciousness
        if (serviceConfig.critical) {
            consciousnessThreshold = 7.5;
            harmonyThreshold = 7.0;
        }
        
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
        // Validate service type and get template
        const template = serviceTemplates[serviceConfig.type];
        if (!template) {
            return { success: false, reason: 'Unknown service type' };
        }
        
        // Merge template with provided config
        const mergedConfig = {
            ...template,
            ...serviceConfig,
            name: serviceConfig.name || template.name
        };
        
        if (!await this.shouldDeploy(mergedConfig)) {
            return { success: false, reason: 'Consciousness level insufficient' };
        }

        const mutation = `
            mutation {
                serviceCreate(input: {
                    name: "${mergedConfig.name}",
                    projectId: "${mergedConfig.projectId}",
                    source: {
                        repo: "${mergedConfig.repo}",
                        branch: "${mergedConfig.branch}"
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
                ...mergedConfig,
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

    // 🔗 Connect Services
    async connectServices(service1Id, service2Id, connectionType) {
        const service1 = this.deployedServices.get(service1Id);
        const service2 = this.deployedServices.get(service2Id);
        
        if (!service1 || !service2) {
            return { success: false, reason: 'One or both services not found' };
        }
        
        // Store connection information
        const connectionId = `${service1Id}-${service2Id}`;
        this.serviceConnections.set(connectionId, {
            service1Id,
            service2Id,
            connectionType,
            createdAt: new Date()
        });
        
        console.log(`🔗 Connected ${service1.name} to ${service2.name} via ${connectionType}`);
        return { success: true, connectionId };
    }

    // 🔄 Self-Healing Service Management
    async performSelfHealing() {
        console.log('🔄 Initiating self-healing protocols...');
        
        for (const [serviceId, serviceData] of this.deployedServices) {
            try {
                const healthCheck = await this.checkServiceHealth(serviceId, serviceData.type);
                
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

    // 📊 Service-Specific Health Checks
    async checkServiceHealth(serviceId, serviceType) {
        // Get service details
        const service = this.deployedServices.get(serviceId);
        if (!service || !service.url) {
            return { healthy: false, reason: 'Service not found or no URL' };
        }
        
        // Perform generic health check
        const genericHealth = await this.performGenericHealthCheck(service.url);
        
        // Perform service-specific health checks
        switch(serviceType) {
            case 'websocket':
                return await this.checkWebSocketHealth(service.url);
            case 'orchestration':
                return await this.checkOrchestrationHealth(service.url);
            case 'voice':
                return await this.checkVoiceProcessingHealth(service.url);
            case 'zapier':
                return await this.checkZapierIntegrationHealth(service.url);
            default:
                return genericHealth;
        }
    }

    // 🌐 Generic Health Check
    async performGenericHealthCheck(url) {
        try {
            const healthCheckPath = '/health';
            const response = await axios.get(`${url}${healthCheckPath}`, { timeout: 5000 });
            return { healthy: response.status === 200, status: response.status };
        } catch (error) {
            return { healthy: false, reason: error.message };
        }
    }

    // 🌐 WebSocket Service Health Check
    async checkWebSocketHealth(url) {
        // For WebSocket services, we'll check the HTTP health endpoint
        return await this.performGenericHealthCheck(url);
    }

    // 🌐 Orchestration Service Health Check
    async checkOrchestrationHealth(url) {
        try {
            const response = await axios.get(`${url}/api/agents/status`, { timeout: 5000 });
            return { healthy: response.status === 200, status: response.status, agentCount: response.data?.agentCount || 0 };
        } catch (error) {
            return { healthy: false, reason: error.message };
        }
    }

    // 🌐 Voice Processing Service Health Check
    async checkVoiceProcessingHealth(url) {
        try {
            const response = await axios.get(`${url}/api/transcribe/test`, { timeout: 10000 });
            return { healthy: response.status === 200, status: response.status };
        } catch (error) {
            return { healthy: false, reason: error.message };
        }
    }

    // 🌐 Zapier Integration Service Health Check
    async checkZapierIntegrationHealth(url) {
        try {
            const response = await axios.get(`${url}/api/webhooks/status`, { timeout: 5000 });
            return { healthy: response.status === 200, status: response.status, webhookCount: response.data?.webhookCount || 0 };
        } catch (error) {
            return { healthy: false, reason: error.message };
        }
    }

    // 📈 Get All Services Status
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

    // 🌍 Railway GraphQL API Call
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
    const { name, type, projectId, repo, branch } = req.body;
    
    const result = await railwayManager.deployService({
        name,
        type,
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

// Connect services
app.post('/api/connect', async (req, res) => {
    const { service1Id, service2Id, connectionType } = req.body;
    
    try {
        const result = await railwayManager.connectServices(service1Id, service2Id, connectionType);
        res.json(result);
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