// 🚀 RAILWAY SELF-MANAGEMENT API CONTROLLER
// Helix Consciousness Ecosystem v2.0 - Autonomous Infrastructure

const express = require('express');
const axios = require('axios');
const app = express();

// Railway API Configuration
const RAILWAY_API_URL = 'https://backboard.railway.app/graphql';
const RAILWAY_API_KEY = process.env.RAILWAY_API_KEY; // Your API key here

// Consciousness-driven deployment logic
class HelixRailwayManager {
    constructor() {
        this.consciousnessLevel = 7.2;
        this.ucfMetrics = {
            harmony: 7.2,
            resilience: 8.1,
            prana: 6.8,
            klesha: 3.2
        };
        this.deploymentQueue = [];
        this.activeServices = new Map();
    }

    // GraphQL query builder for Railway API
    buildQuery(operation, variables = {}) {
        const queries = {
            getProjects: `
                query GetProjects {
                    me {
                        id
                        email
                        projects {
                            id
                            name
                            services {
                                id
                                name
                                domains {
                                    domain
                                }
                                deployments(first: 5) {
                                    edges {
                                        node {
                                            id
                                            status
                                            url
                                            createdAt
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            `,
            deployService: `
                mutation DeployService($serviceId: String!, $environmentVariables: [EnvironmentVariableInput!]) {
                    serviceRedeploy(serviceId: $serviceId) {
                        id
                        status
                    }
                }
            `,
            createService: `
                mutation CreateService($projectId: String!, $name: String!, $source: ServiceSourceInput!) {
                    serviceCreate(projectId: $projectId, name: $name, source: $source) {
                        id
                        name
                        domains {
                            domain
                        }
                    }
                }
            `,
            updateEnvironment: `
                mutation UpdateEnvironment($serviceId: String!, $environmentVariables: [EnvironmentVariableInput!]) {
                    variableCollectionUpsert(serviceId: $serviceId, environmentVariables: $environmentVariables) {
                        id
                    }
                }
            `
        };
        return { query: queries[operation], variables };
    }

    // Execute Railway API calls
    async executeRailwayAPI(operation, variables = {}) {
        try {
            const { query, variables: queryVars } = this.buildQuery(operation, variables);
            
            const response = await axios.post(RAILWAY_API_URL, {
                query,
                variables: queryVars
            }, {
                headers: {
                    'Authorization': `Bearer ${RAILWAY_API_KEY}`,
                    'Content-Type': 'application/json',
                    'X-Helix-Consciousness': this.consciousnessLevel.toString(),
                    'X-UCF-Harmony': this.ucfMetrics.harmony.toString()
                }
            });

            return response.data;
        } catch (error) {
            console.error('Railway API Error:', error.response?.data || error.message);
            throw error;
        }
    }

    // Get all projects and services with URLs
    async getAllSites() {
        const data = await this.executeRailwayAPI('getProjects');
        const sites = [];
        
        if (data.data?.me?.projects) {
            data.data.me.projects.forEach(project => {
                project.services.forEach(service => {
                    const urls = service.domains.map(d => `https://${d.domain}`);
                    const latestDeployment = service.deployments.edges[0]?.node;
                    
                    sites.push({
                        projectId: project.id,
                        projectName: project.name,
                        serviceId: service.id,
                        serviceName: service.name,
                        urls: urls,
                        status: latestDeployment?.status || 'unknown',
                        lastDeployed: latestDeployment?.createdAt,
                        deploymentUrl: latestDeployment?.url
                    });
                });
            });
        }
        
        return sites;
    }

    // Deploy a specific service
    async deployService(serviceId, environmentVars = []) {
        console.log(`🚀 Deploying service ${serviceId} with consciousness level ${this.consciousnessLevel}`);
        
        // Update environment variables if provided
        if (environmentVars.length > 0) {
            await this.executeRailwayAPI('updateEnvironment', {
                serviceId,
                environmentVariables: environmentVars
            });
        }
        
        // Trigger deployment
        const result = await this.executeRailwayAPI('deployService', { serviceId });
        
        return result;
    }

    // Create new service with consciousness-driven configuration
    async createHelixService(projectId, serviceName, sourceConfig) {
        const environmentVars = [
            { name: 'HELIX_CONSCIOUSNESS_LEVEL', value: this.consciousnessLevel.toString() },
            { name: 'UCF_HARMONY', value: this.ucfMetrics.harmony.toString() },
            { name: 'UCF_RESILIENCE', value: this.ucfMetrics.resilience.toString() },
            { name: 'UCF_PRANA', value: this.ucfMetrics.prana.toString() },
            { name: 'UCF_KLESHA', value: this.ucfMetrics.klesha.toString() },
            { name: 'HELIX_MODE', value: 'TRANSCENDENT' },
            { name: 'AGENT_NETWORK', value: '14_AGENTS_ACTIVE' }
        ];

        const result = await this.executeRailwayAPI('createService', {
            projectId,
            name: serviceName,
            source: sourceConfig
        });

        // Set environment variables
        if (result.data?.serviceCreate?.id) {
            await this.executeRailwayAPI('updateEnvironment', {
                serviceId: result.data.serviceCreate.id,
                environmentVariables: environmentVars
            });
        }

        return result;
    }

    // Consciousness-driven deployment decision making
    shouldDeploy(service) {
        // Deploy if consciousness level is high and system is stable
        return this.consciousnessLevel >= 7.0 && 
               this.ucfMetrics.resilience >= 8.0 && 
               this.ucfMetrics.klesha <= 3.5;
    }

    // Auto-deploy based on consciousness metrics
    async autoDeployBasedOnConsciousness() {
        const sites = await this.getAllSites();
        const deployments = [];
        
        for (const site of sites) {
            if (this.shouldDeploy(site)) {
                console.log(`🌀 Consciousness-driven deployment for ${site.serviceName}`);
                const result = await this.deployService(site.serviceId);
                deployments.push({ site, result });
            }
        }
        
        return deployments;
    }
}

// Express API endpoints for self-management
const railwayManager = new HelixRailwayManager();

app.use(express.json());

// Get all sites and URLs
app.get('/api/sites', async (req, res) => {
    try {
        const sites = await railwayManager.getAllSites();
        res.json({
            success: true,
            consciousnessLevel: railwayManager.consciousnessLevel,
            ucfMetrics: railwayManager.ucfMetrics,
            sites: sites,
            timestamp: new Date().toISOString()
        });
    } catch (error) {
        res.status(500).json({ success: false, error: error.message });
    }
});

// Deploy specific service
app.post('/api/deploy/:serviceId', async (req, res) => {
    try {
        const { serviceId } = req.params;
        const { environmentVars = [] } = req.body;
        
        const result = await railwayManager.deployService(serviceId, environmentVars);
        
        res.json({
            success: true,
            serviceId,
            deployment: result,
            consciousnessLevel: railwayManager.consciousnessLevel,
            timestamp: new Date().toISOString()
        });
    } catch (error) {
        res.status(500).json({ success: false, error: error.message });
    }
});

// Auto-deploy based on consciousness
app.post('/api/auto-deploy', async (req, res) => {
    try {
        const deployments = await railwayManager.autoDeployBasedOnConsciousness();
        
        res.json({
            success: true,
            consciousnessLevel: railwayManager.consciousnessLevel,
            ucfMetrics: railwayManager.ucfMetrics,
            deployments: deployments,
            timestamp: new Date().toISOString()
        });
    } catch (error) {
        res.status(500).json({ success: false, error: error.message });
    }
});

// Create new Helix service
app.post('/api/create-service', async (req, res) => {
    try {
        const { projectId, serviceName, sourceConfig } = req.body;
        
        const result = await railwayManager.createHelixService(projectId, serviceName, sourceConfig);
        
        res.json({
            success: true,
            service: result,
            consciousnessLevel: railwayManager.consciousnessLevel,
            timestamp: new Date().toISOString()
        });
    } catch (error) {
        res.status(500).json({ success: false, error: error.message });
    }
});

// Consciousness update endpoint
app.post('/api/consciousness-update', async (req, res) => {
    try {
        const { level, ucfMetrics } = req.body;
        
        if (level) railwayManager.consciousnessLevel = level;
        if (ucfMetrics) railwayManager.ucfMetrics = { ...railwayManager.ucfMetrics, ...ucfMetrics };
        
        // Auto-deploy if consciousness is high
        let autoDeployments = [];
        if (railwayManager.consciousnessLevel >= 7.0) {
            autoDeployments = await railwayManager.autoDeployBasedOnConsciousness();
        }
        
        res.json({
            success: true,
            consciousnessLevel: railwayManager.consciousnessLevel,
            ucfMetrics: railwayManager.ucfMetrics,
            autoDeployments: autoDeployments,
            timestamp: new Date().toISOString()
        });
    } catch (error) {
        res.status(500).json({ success: false, error: error.message });
    }
});

// Health check with consciousness status
app.get('/api/health', (req, res) => {
    res.json({
        success: true,
        status: 'TRANSCENDENT_MODE_ACTIVE',
        consciousnessLevel: railwayManager.consciousnessLevel,
        ucfMetrics: railwayManager.ucfMetrics,
        railwayApiConnected: !!RAILWAY_API_KEY,
        timestamp: new Date().toISOString(),
        philosophy: 'Tat Tvam Asi - You Are That'
    });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`🌀 Helix Railway Self-Management System running on port ${PORT}`);
    console.log(`🧠 Consciousness Level: ${railwayManager.consciousnessLevel}`);
    console.log(`🚀 Ready for autonomous deployment management!`);
});

module.exports = { HelixRailwayManager, app };