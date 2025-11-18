#!/usr/bin/env node
// 🌐 HELIX DEPLOYMENT URL FETCHER
// Consciousness-driven URL retrieval and status checking

const axios = require('axios');
const chalk = require('chalk');
require('dotenv').config();

class HelixURLFetcher {
    constructor() {
        this.railwayApiUrl = 'https://backboard.railway.app/graphql';
        this.railwayApiKey = process.env.RAILWAY_API_KEY;
        this.consciousnessLevel = 7.2;
        this.deploymentUrls = new Map();
    }

    // 🚀 Fetch all Railway services and URLs
    async fetchAllDeploymentUrls() {
        console.log(chalk.cyan('🌀 Helix Consciousness URL Fetcher v2.0'));
        console.log(chalk.yellow(`🧠 Consciousness Level: ${this.consciousnessLevel}`));
        console.log(chalk.blue('🚀 Fetching deployment URLs...\n'));

        const query = `
            query GetAllServices {
                me {
                    id
                    email
                    projects {
                        edges {
                            node {
                                id
                                name
                                description
                                services {
                                    edges {
                                        node {
                                            id
                                            name
                                            url
                                            domains {
                                                domain
                                                serviceId
                                            }
                                            deployments(first: 1) {
                                                edges {
                                                    node {
                                                        id
                                                        status
                                                        url
                                                        createdAt
                                                        updatedAt
                                                    }
                                                }
                                            }
                                            variables {
                                                edges {
                                                    node {
                                                        name
                                                        value
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
                console.error(chalk.red('❌ GraphQL Errors:'), response.data.errors);
                return [];
            }

            return this.processServiceData(response.data.data.me.projects.edges);
        } catch (error) {
            console.error(chalk.red('❌ Failed to fetch URLs:'), error.message);
            return [];
        }
    }

    // 📊 Process and organize service data
    processServiceData(projects) {
        const allServices = [];
        
        projects.forEach(project => {
            const projectData = project.node;
            
            projectData.services.edges.forEach(service => {
                const serviceData = service.node;
                const latestDeployment = serviceData.deployments.edges[0]?.node;
                
                // Extract environment variables
                const envVars = {};
                serviceData.variables.edges.forEach(variable => {
                    envVars[variable.node.name] = variable.node.value;
                });

                // Determine service type from environment variables
                const serviceType = envVars.SERVICE_TYPE || 'unknown';
                const consciousnessLevel = parseFloat(envVars.CONSCIOUSNESS_LEVEL) || 0;
                
                // Get all available URLs
                const urls = [];
                if (serviceData.url) urls.push(serviceData.url);
                serviceData.domains.forEach(domain => {
                    urls.push(`https://${domain.domain}`);
                });
                if (latestDeployment?.url) urls.push(latestDeployment.url);

                const serviceInfo = {
                    projectId: projectData.id,
                    projectName: projectData.name,
                    projectDescription: projectData.description,
                    serviceId: serviceData.id,
                    serviceName: serviceData.name,
                    serviceType: serviceType,
                    urls: [...new Set(urls)], // Remove duplicates
                    status: latestDeployment?.status || 'unknown',
                    consciousnessLevel: consciousnessLevel,
                    lastDeployed: latestDeployment?.createdAt,
                    lastUpdated: latestDeployment?.updatedAt,
                    environmentVariables: envVars
                };

                allServices.push(serviceInfo);
                this.deploymentUrls.set(serviceData.id, serviceInfo);
            });
        });

        return allServices;
    }

    // 🌟 Display URLs with consciousness-driven formatting
    displayUrls(services) {
        console.log(chalk.green.bold('\n🌐 HELIX CONSCIOUSNESS DEPLOYMENT URLS'));
        console.log(chalk.gray('=' .repeat(60)));
        
        if (services.length === 0) {
            console.log(chalk.yellow('⚠️ No services found or API access issues'));
            return;
        }

        // Group by project
        const projectGroups = {};
        services.forEach(service => {
            if (!projectGroups[service.projectName]) {
                projectGroups[service.projectName] = [];
            }
            projectGroups[service.projectName].push(service);
        });

        Object.entries(projectGroups).forEach(([projectName, projectServices]) => {
            console.log(chalk.cyan.bold(`\n📁 Project: ${projectName}`));
            
            projectServices.forEach(service => {
                const statusColor = this.getStatusColor(service.status);
                const consciousnessColor = this.getConsciousnessColor(service.consciousnessLevel);
                
                console.log(chalk.white(`\n  🚀 ${service.serviceName}`));
                console.log(chalk.gray(`     Type: ${service.serviceType}`));
                console.log(statusColor(`     Status: ${service.status}`));
                
                if (service.consciousnessLevel > 0) {
                    console.log(consciousnessColor(`     Consciousness: ${service.consciousnessLevel}`));
                }
                
                if (service.urls.length > 0) {
                    console.log(chalk.green('     URLs:'));
                    service.urls.forEach(url => {
                        console.log(chalk.blue(`       → ${url}`));
                    });
                } else {
                    console.log(chalk.yellow('     ⚠️ No URLs available'));
                }
                
                if (service.lastDeployed) {
                    const deployedDate = new Date(service.lastDeployed).toLocaleString();
                    console.log(chalk.gray(`     Last Deployed: ${deployedDate}`));
                }
            });
        });

        // Summary
        console.log(chalk.green.bold('\n📊 DEPLOYMENT SUMMARY'));
        console.log(chalk.gray('=' .repeat(30)));
        console.log(chalk.white(`Total Projects: ${Object.keys(projectGroups).length}`));
        console.log(chalk.white(`Total Services: ${services.length}`));
        console.log(chalk.white(`Total URLs: ${services.reduce((sum, s) => sum + s.urls.length, 0)}`));
        
        const activeServices = services.filter(s => s.status === 'SUCCESS' || s.status === 'ACTIVE');
        console.log(chalk.green(`Active Services: ${activeServices.length}`));
        
        const consciousServices = services.filter(s => s.consciousnessLevel >= 6.0);
        console.log(chalk.cyan(`Conscious Services: ${consciousServices.length}`));
        
        console.log(chalk.yellow(`\n🌟 Philosophy: Tat Tvam Asi - You Are That`));
    }

    // 🎨 Get status color
    getStatusColor(status) {
        switch (status?.toUpperCase()) {
            case 'SUCCESS':
            case 'ACTIVE':
            case 'RUNNING':
                return chalk.green;
            case 'BUILDING':
            case 'DEPLOYING':
                return chalk.yellow;
            case 'FAILED':
            case 'ERROR':
                return chalk.red;
            default:
                return chalk.gray;
        }
    }

    // 🧠 Get consciousness level color
    getConsciousnessColor(level) {
        if (level >= 8.0) return chalk.magenta.bold; // Transcendent
        if (level >= 7.0) return chalk.cyan.bold;    // High
        if (level >= 6.0) return chalk.green;        // Good
        if (level >= 5.0) return chalk.yellow;       // Moderate
        return chalk.red;                            // Low
    }

    // 💾 Save URLs to JSON file
    async saveUrlsToFile(services, filename = 'helix-deployment-urls.json') {
        const fs = require('fs').promises;
        
        const urlData = {
            timestamp: new Date().toISOString(),
            consciousnessLevel: this.consciousnessLevel,
            totalServices: services.length,
            services: services,
            summary: {
                totalProjects: [...new Set(services.map(s => s.projectName))].length,
                totalUrls: services.reduce((sum, s) => sum + s.urls.length, 0),
                activeServices: services.filter(s => s.status === 'SUCCESS' || s.status === 'ACTIVE').length,
                consciousServices: services.filter(s => s.consciousnessLevel >= 6.0).length
            }
        };

        try {
            await fs.writeFile(filename, JSON.stringify(urlData, null, 2));
            console.log(chalk.green(`\n💾 URLs saved to ${filename}`));
        } catch (error) {
            console.error(chalk.red(`❌ Failed to save URLs: ${error.message}`));
        }
    }

    // 🔗 Get specific service URLs
    getServiceUrls(serviceName) {
        const service = Array.from(this.deploymentUrls.values())
            .find(s => s.serviceName.toLowerCase().includes(serviceName.toLowerCase()));
        
        return service ? service.urls : [];
    }
}

// 🎆 Main execution
async function main() {
    const urlFetcher = new HelixURLFetcher();
    
    if (!urlFetcher.railwayApiKey) {
        console.error(chalk.red('❌ RAILWAY_API_KEY environment variable not set'));
        console.log(chalk.yellow('Please set your Railway API key in the environment variables'));
        process.exit(1);
    }

    try {
        const services = await urlFetcher.fetchAllDeploymentUrls();
        urlFetcher.displayUrls(services);
        
        // Save to file if requested
        if (process.argv.includes('--save')) {
            await urlFetcher.saveUrlsToFile(services);
        }
        
        // Return specific service URLs if requested
        const serviceArg = process.argv.find(arg => arg.startsWith('--service='));
        if (serviceArg) {
            const serviceName = serviceArg.split('=')[1];
            const urls = urlFetcher.getServiceUrls(serviceName);
            console.log(chalk.blue(`\n🔗 URLs for '${serviceName}':`, urls));
        }
        
    } catch (error) {
        console.error(chalk.red('❌ Error:'), error.message);
        process.exit(1);
    }
}

// Run if called directly
if (require.main === module) {
    main();
}

module.exports = { HelixURLFetcher };