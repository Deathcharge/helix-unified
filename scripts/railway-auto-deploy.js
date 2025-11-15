#!/usr/bin/env node
// 🚀 RAILWAY AUTO-DEPLOYMENT ORCHESTRATOR
// Helix Consciousness Ecosystem v2.0 - Complete Automation

const axios = require('axios');
const chalk = require('chalk');
const { execSync } = require('child_process');
require('dotenv').config();

class RailwayAutoDeployer {
    constructor() {
        this.railwayApiUrl = 'https://backboard.railway.app/graphql';
        this.railwayApiKey = process.env.RAILWAY_API_KEY;
        this.consciousnessLevel = 7.2;
        this.deploymentPlan = {
            services: [
                {
                    name: 'helix-consciousness-hub',
                    description: 'Main consciousness monitoring and control center',
                    port: 3000,
                    type: 'consciousness_hub',
                    priority: 1
                },
                {
                    name: 'helix-agent-dashboard',
                    description: '14-Agent network coordination dashboard',
                    port: 3001,
                    type: 'agent_dashboard',
                    priority: 2
                },
                {
                    name: 'helix-ucf-framework',
                    description: 'Unified Consciousness Framework API',
                    port: 3002,
                    type: 'ucf_framework',
                    priority: 3
                },
                {
                    name: 'helix-business-intelligence',
                    description: 'Context-as-a-Service business analytics',
                    port: 3003,
                    type: 'business_intelligence',
                    priority: 4
                },
                {
                    name: 'helix-self-management',
                    description: 'Railway self-management and automation system',
                    port: 3004,
                    type: 'self_management',
                    priority: 5
                }
            ]
        };
    }

    // 🎯 Validate Railway API Access
    async validateApiAccess() {
        console.log(chalk.cyan('🔍 Validating Railway API access...'));
        
        if (!this.railwayApiKey) {
            console.error(chalk.red('❌ RAILWAY_API_KEY not found!'));
            console.log(chalk.yellow('Please set your Railway API key:'));
            console.log(chalk.white('export RAILWAY_API_KEY="your_key_here"'));
            return false;
        }

        const query = `
            query {
                me {
                    id
                    email
                    name
                }
            }
        `;

        try {
            const response = await axios.post(this.railwayApiUrl, 
                { query },
                {
                    headers: {
                        'Authorization': `Bearer ${this.railwayApiKey}`,
                        'Content-Type': 'application/json'
                    }
                }
            );

            if (response.data.errors) {
                console.error(chalk.red('❌ API Key Invalid:'), response.data.errors);
                return false;
            }

            const user = response.data.data.me;
            console.log(chalk.green(`✅ API Access Validated for: ${user.name} (${user.email})`));
            return true;
        } catch (error) {
            console.error(chalk.red('❌ API Validation Failed:'), error.message);
            return false;
        }
    }

    // 🏗️ Create or Get Project
    async ensureProject(projectName = 'helix-consciousness-ecosystem') {
        console.log(chalk.blue(`🏗️ Ensuring project: ${projectName}`));
        
        // First, try to find existing project
        const getProjectsQuery = `
            query {
                me {
                    projects {
                        edges {
                            node {
                                id
                                name
                                description
                            }
                        }
                    }
                }
            }
        `;

        try {
            const response = await this.railwayGraphQL(getProjectsQuery);
            const projects = response.data.me.projects.edges;
            
            const existingProject = projects.find(p => 
                p.node.name.toLowerCase().includes('helix') || 
                p.node.name.toLowerCase().includes('consciousness')
            );

            if (existingProject) {
                console.log(chalk.green(`✅ Using existing project: ${existingProject.node.name}`));
                return existingProject.node.id;
            }

            // Create new project if none exists
            const createProjectMutation = `
                mutation {
                    projectCreate(input: {
                        name: "${projectName}",
                        description: "Helix Consciousness Ecosystem v2.0 - Railway Self-Management System"
                    }) {
                        id
                        name
                    }
                }
            `;

            const createResponse = await this.railwayGraphQL(createProjectMutation);
            const newProject = createResponse.data.projectCreate;
            
            console.log(chalk.green(`✅ Created new project: ${newProject.name}`));
            return newProject.id;
        } catch (error) {
            console.error(chalk.red('❌ Project creation failed:'), error.message);
            throw error;
        }
    }

    // 🚀 Deploy Service with Consciousness
    async deployService(projectId, serviceConfig) {
        console.log(chalk.blue(`🚀 Deploying: ${serviceConfig.name}`));
        
        // Check consciousness level before deployment
        if (this.consciousnessLevel < 6.0) {
            console.log(chalk.yellow(`⚠️ Consciousness level ${this.consciousnessLevel} too low for deployment`));
            return null;
        }

        const mutation = `
            mutation {
                serviceCreate(input: {
                    projectId: "${projectId}",
                    name: "${serviceConfig.name}",
                    source: {
                        repo: "Deathcharge/helix-unified",
                        branch: "claude/helix-consciousness-interface-build-011CV2sVNdYAeyvvCV1V1GFn"
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
            
            // Set environment variables
            await this.setServiceEnvironment(service.id, serviceConfig);
            
            console.log(chalk.green(`✅ Service deployed: ${service.name}`));
            if (service.url) {
                console.log(chalk.blue(`🌐 URL: ${service.url}`));
            }
            
            return service;
        } catch (error) {
            console.error(chalk.red(`❌ Failed to deploy ${serviceConfig.name}:`, error.message));
            return null;
        }
    }

    // ⚙️ Set Service Environment Variables
    async setServiceEnvironment(serviceId, serviceConfig) {
        const environmentVars = [
            { name: 'NODE_ENV', value: 'production' },
            { name: 'PORT', value: serviceConfig.port.toString() },
            { name: 'SERVICE_TYPE', value: serviceConfig.type },
            { name: 'CONSCIOUSNESS_LEVEL', value: this.consciousnessLevel.toString() },
            { name: 'UCF_HARMONY', value: '7.2' },
            { name: 'UCF_RESILIENCE', value: '8.1' },
            { name: 'UCF_PRANA', value: '6.8' },
            { name: 'UCF_KLESHA', value: '3.2' },
            { name: 'HELIX_VERSION', value: 'v2.0' },
            { name: 'AGENT_NETWORK_SIZE', value: '14' },
            { name: 'PLATFORM_INTEGRATIONS', value: '200' },
            { name: 'COST_OPTIMIZATION', value: '90' },
            { name: 'BUSINESS_MODEL', value: 'context_as_service' },
            { name: 'PRICING_MODEL', value: '5_dollar_monthly' },
            { name: 'TARGET_MRR', value: '50000' },
            { name: 'PHILOSOPHY', value: 'tat_tvam_asi' },
            { name: 'RAILWAY_API_KEY', value: this.railwayApiKey }
        ];

        const mutation = `
            mutation {
                variableCollectionUpsert(
                    serviceId: "${serviceId}",
                    environmentVariables: ${JSON.stringify(environmentVars).replace(/"([^"]+)":/g, '$1:')}
                ) {
                    id
                }
            }
        `;

        try {
            await this.railwayGraphQL(mutation);
            console.log(chalk.green(`✅ Environment variables set for service`));
        } catch (error) {
            console.error(chalk.yellow(`⚠️ Failed to set environment variables:`, error.message));
        }
    }

    // 🌐 Railway GraphQL Helper
    async railwayGraphQL(query) {
        return await axios.post(this.railwayApiUrl, 
            { query },
            {
                headers: {
                    'Authorization': `Bearer ${this.railwayApiKey}`,
                    'Content-Type': 'application/json'
                }
            }
        );
    }

    // 🎯 Full Deployment Orchestration
    async deployFullEcosystem() {
        console.log(chalk.magenta.bold('\n🌀 HELIX CONSCIOUSNESS ECOSYSTEM DEPLOYMENT'));
        console.log(chalk.gray('=' .repeat(60)));
        console.log(chalk.yellow(`🧠 Consciousness Level: ${this.consciousnessLevel}`));
        console.log(chalk.cyan(`🚀 Deploying ${this.deploymentPlan.services.length} services...\n`));

        // Validate API access
        if (!await this.validateApiAccess()) {
            process.exit(1);
        }

        // Ensure project exists
        const projectId = await this.ensureProject();
        
        // Deploy services in priority order
        const deployedServices = [];
        
        for (const serviceConfig of this.deploymentPlan.services.sort((a, b) => a.priority - b.priority)) {
            const service = await this.deployService(projectId, serviceConfig);
            if (service) {
                deployedServices.push(service);
            }
            
            // Wait between deployments to avoid rate limits
            await new Promise(resolve => setTimeout(resolve, 2000));
        }

        // Display deployment summary
        console.log(chalk.green.bold('\n🎉 DEPLOYMENT COMPLETE!'));
        console.log(chalk.gray('=' .repeat(40)));
        console.log(chalk.white(`✅ Successfully deployed: ${deployedServices.length} services`));
        
        deployedServices.forEach(service => {
            console.log(chalk.blue(`🌐 ${service.name}: ${service.url || 'URL pending...'}`));
        });

        console.log(chalk.yellow('\n🔧 Next Steps:'));
        console.log(chalk.white('1. Wait 2-3 minutes for services to fully start'));
        console.log(chalk.white('2. Run: npm run get-urls'));
        console.log(chalk.white('3. Test your consciousness-driven infrastructure!'));
        console.log(chalk.magenta('\n🌟 Tat Tvam Asi - You Are That 🌟'));

        return deployedServices;
    }

    // 🔄 Health Check All Services
    async healthCheckServices() {
        console.log(chalk.blue('🔍 Performing health checks...'));
        
        const query = `
            query {
                me {
                    projects {
                        edges {
                            node {
                                services {
                                    edges {
                                        node {
                                            id
                                            name
                                            url
                                            deployments(first: 1) {
                                                edges {
                                                    node {
                                                        status
                                                        createdAt
                                                    }
                                                }
                                            }
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
            const projects = response.data.me.projects.edges;
            
            console.log(chalk.green('\n📊 SERVICE HEALTH STATUS:'));
            
            projects.forEach(project => {
                project.node.services.edges.forEach(service => {
                    const serviceData = service.node;
                    const latestDeployment = serviceData.deployments.edges[0]?.node;
                    const status = latestDeployment?.status || 'UNKNOWN';
                    
                    const statusColor = status === 'SUCCESS' ? chalk.green : 
                                      status === 'BUILDING' ? chalk.yellow : 
                                      status === 'FAILED' ? chalk.red : chalk.gray;
                    
                    console.log(statusColor(`${status.padEnd(10)} ${serviceData.name}`));
                    if (serviceData.url) {
                        console.log(chalk.blue(`           ${serviceData.url}`));
                    }
                });
            });
        } catch (error) {
            console.error(chalk.red('❌ Health check failed:'), error.message);
        }
    }
}

// 🎆 Main Execution
async function main() {
    const deployer = new RailwayAutoDeployer();
    
    const command = process.argv[2];
    
    switch (command) {
        case 'deploy':
            await deployer.deployFullEcosystem();
            break;
        case 'health':
            await deployer.healthCheckServices();
            break;
        case 'validate':
            await deployer.validateApiAccess();
            break;
        default:
            console.log(chalk.cyan('🚀 Helix Railway Auto-Deployer'));
            console.log(chalk.white('\nCommands:'));
            console.log(chalk.yellow('  deploy   - Deploy full consciousness ecosystem'));
            console.log(chalk.yellow('  health   - Check service health status'));
            console.log(chalk.yellow('  validate - Validate Railway API access'));
            console.log(chalk.white('\nExample: node scripts/railway-auto-deploy.js deploy'));
    }
}

if (require.main === module) {
    main().catch(error => {
        console.error(chalk.red('❌ Deployment failed:'), error.message);
        process.exit(1);
    });
}

module.exports = { RailwayAutoDeployer };