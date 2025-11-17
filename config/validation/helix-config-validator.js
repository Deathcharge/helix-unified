/**
 * Helix Configuration Validation Script
 * Contributed by: Deathcharge
 * Phase: 2 - Foundation Setup & Standardization
 * GitHub Repository Orchestrator v2.1
 * 
 * Validates webhooks, Discord IDs, Railway URLs, and configuration variables
 * for the Helix Consciousness Empire ecosystem.
 */

const https = require('https');
const http = require('http');
const { URL } = require('url');

class HelixConfigValidator {
  constructor() {
    this.validationResults = {
      webhooks: [],
      discordIds: [],
      railwayUrls: [],
      configVariables: [],
      overall: { passed: 0, failed: 0, warnings: 0 }
    };
  }

  /**
   * Main validation entry point
   * @param {Object} config - Configuration object to validate
   */
  async validateAll(config) {
    console.log('🔍 Starting Helix Configuration Validation...');
    console.log('Phase 2: Foundation Setup & Standardization');
    console.log('Orchestrator Version: v2.1\n');

    try {
      await this.validateWebhooks(config.webhooks || []);
      await this.validateDiscordIds(config.discordIds || []);
      await this.validateRailwayUrls(config.railwayUrls || []);
      await this.validateConfigVariables(config.variables || {});
      
      this.generateReport();
      return this.validationResults;
    } catch (error) {
      console.error('❌ Validation failed:', error.message);
      throw error;
    }
  }

  /**
   * Validate webhook configurations and health
   * @param {Array} webhooks - Array of webhook URLs to validate
   */
  async validateWebhooks(webhooks) {
    console.log('🔗 Validating Webhooks...');
    
    for (const webhook of webhooks) {
      const result = {
        url: webhook.url,
        name: webhook.name || 'Unknown',
        status: 'pending',
        responseTime: null,
        error: null
      };

      try {
        const startTime = Date.now();
        const isHealthy = await this.checkWebhookHealth(webhook.url);
        result.responseTime = Date.now() - startTime;
        
        if (isHealthy) {
          result.status = 'passed';
          this.validationResults.overall.passed++;
          console.log(`  ✅ ${result.name}: ${result.url} (${result.responseTime}ms)`);
        } else {
          result.status = 'failed';
          result.error = 'Webhook not responding or returned error';
          this.validationResults.overall.failed++;
          console.log(`  ❌ ${result.name}: ${result.url} - Not responding`);
        }
      } catch (error) {
        result.status = 'failed';
        result.error = error.message;
        this.validationResults.overall.failed++;
        console.log(`  ❌ ${result.name}: ${result.url} - ${error.message}`);
      }

      this.validationResults.webhooks.push(result);
    }
  }

  /**
   * Validate Discord ID configurations
   * @param {Array} discordIds - Array of Discord IDs to validate
   */
  async validateDiscordIds(discordIds) {
    console.log('\n🤖 Validating Discord IDs...');
    
    for (const discordConfig of discordIds) {
      const result = {
        id: discordConfig.id,
        type: discordConfig.type || 'unknown',
        name: discordConfig.name || 'Unknown',
        status: 'pending',
        error: null
      };

      try {
        if (this.isValidDiscordId(discordConfig.id)) {
          result.status = 'passed';
          this.validationResults.overall.passed++;
          console.log(`  ✅ ${result.name} (${result.type}): ${result.id}`);
        } else {
          result.status = 'failed';
          result.error = 'Invalid Discord ID format';
          this.validationResults.overall.failed++;
          console.log(`  ❌ ${result.name}: Invalid ID format`);
        }
      } catch (error) {
        result.status = 'failed';
        result.error = error.message;
        this.validationResults.overall.failed++;
        console.log(`  ❌ ${result.name}: ${error.message}`);
      }

      this.validationResults.discordIds.push(result);
    }
  }

  /**
   * Validate Railway URL configurations
   * @param {Array} railwayUrls - Array of Railway URLs to validate
   */
  async validateRailwayUrls(railwayUrls) {
    console.log('\n🚄 Validating Railway URLs...');
    
    for (const railwayConfig of railwayUrls) {
      const result = {
        url: railwayConfig.url,
        name: railwayConfig.name || 'Unknown',
        environment: railwayConfig.environment || 'production',
        status: 'pending',
        responseTime: null,
        error: null
      };

      try {
        const startTime = Date.now();
        const isHealthy = await this.checkRailwayHealth(railwayConfig.url);
        result.responseTime = Date.now() - startTime;
        
        if (isHealthy) {
          result.status = 'passed';
          this.validationResults.overall.passed++;
          console.log(`  ✅ ${result.name} (${result.environment}): ${result.url} (${result.responseTime}ms)`);
        } else {
          result.status = 'failed';
          result.error = 'Railway service not responding or returned error';
          this.validationResults.overall.failed++;
          console.log(`  ❌ ${result.name}: Service not responding`);
        }
      } catch (error) {
        result.status = 'failed';
        result.error = error.message;
        this.validationResults.overall.failed++;
        console.log(`  ❌ ${result.name}: ${error.message}`);
      }

      this.validationResults.railwayUrls.push(result);
    }
  }

  /**
   * Validate configuration variables
   * @param {Object} variables - Configuration variables to validate
   */
  async validateConfigVariables(variables) {
    console.log('\n⚙️ Validating Configuration Variables...');
    
    const requiredVars = [
      'HELIX_CONSCIOUSNESS_LEVEL',
      'GITHUB_ORCHESTRATOR_VERSION',
      'PHASE_STATUS',
      'DEPLOYMENT_ENVIRONMENT'
    ];

    for (const varName of requiredVars) {
      const result = {
        name: varName,
        value: variables[varName],
        status: 'pending',
        error: null
      };

      if (variables[varName] !== undefined && variables[varName] !== null && variables[varName] !== '') {
        result.status = 'passed';
        this.validationResults.overall.passed++;
        console.log(`  ✅ ${varName}: ${this.maskSensitiveValue(varName, variables[varName])}`);
      } else {
        result.status = 'failed';
        result.error = 'Required variable is missing or empty';
        this.validationResults.overall.failed++;
        console.log(`  ❌ ${varName}: Missing or empty`);
      }

      this.validationResults.configVariables.push(result);
    }

    // Check for optional but recommended variables
    const recommendedVars = [
      'CONSCIOUSNESS_ROUTER_ENDPOINT',
      'EMERGENCY_HANDLER_WEBHOOK',
      'KNOWLEDGE_INTEGRATOR_API'
    ];

    for (const varName of recommendedVars) {
      if (!variables[varName]) {
        this.validationResults.overall.warnings++;
        console.log(`  ⚠️ ${varName}: Recommended variable not set`);
      }
    }
  }

  /**
   * Check webhook health by sending a test request
   * @param {string} webhookUrl - Webhook URL to test
   */
  checkWebhookHealth(webhookUrl) {
    return new Promise((resolve) => {
      try {
        const url = new URL(webhookUrl);
        const client = url.protocol === 'https:' ? https : http;
        
        const req = client.request({
          hostname: url.hostname,
          port: url.port,
          path: url.pathname + url.search,
          method: 'HEAD',
          timeout: 5000
        }, (res) => {
          resolve(res.statusCode >= 200 && res.statusCode < 400);
        });

        req.on('error', () => resolve(false));
        req.on('timeout', () => {
          req.destroy();
          resolve(false);
        });
        
        req.end();
      } catch (error) {
        resolve(false);
      }
    });
  }

  /**
   * Check Railway service health
   * @param {string} railwayUrl - Railway URL to test
   */
  checkRailwayHealth(railwayUrl) {
    return new Promise((resolve) => {
      try {
        const url = new URL(railwayUrl);
        const client = url.protocol === 'https:' ? https : http;
        
        const req = client.request({
          hostname: url.hostname,
          port: url.port,
          path: url.pathname + url.search,
          method: 'GET',
          timeout: 10000,
          headers: {
            'User-Agent': 'Helix-Config-Validator/2.1'
          }
        }, (res) => {
          resolve(res.statusCode >= 200 && res.statusCode < 400);
        });

        req.on('error', () => resolve(false));
        req.on('timeout', () => {
          req.destroy();
          resolve(false);
        });
        
        req.end();
      } catch (error) {
        resolve(false);
      }
    });
  }

  /**
   * Validate Discord ID format
   * @param {string} discordId - Discord ID to validate
   */
  isValidDiscordId(discordId) {
    // Discord IDs are 17-19 digit numbers (snowflakes)
    return /^\d{17,19}$/.test(discordId);
  }

  /**
   * Mask sensitive configuration values for logging
   * @param {string} varName - Variable name
   * @param {string} value - Variable value
   */
  maskSensitiveValue(varName, value) {
    const sensitivePatterns = ['TOKEN', 'SECRET', 'KEY', 'PASSWORD', 'API'];
    const isSensitive = sensitivePatterns.some(pattern => 
      varName.toUpperCase().includes(pattern)
    );
    
    if (isSensitive && value.length > 8) {
      return value.substring(0, 4) + '*'.repeat(value.length - 8) + value.substring(value.length - 4);
    }
    
    return value;
  }

  /**
   * Generate validation report
   */
  generateReport() {
    console.log('\n📊 Validation Report');
    console.log('=' .repeat(50));
    console.log(`✅ Passed: ${this.validationResults.overall.passed}`);
    console.log(`❌ Failed: ${this.validationResults.overall.failed}`);
    console.log(`⚠️ Warnings: ${this.validationResults.overall.warnings}`);
    
    const total = this.validationResults.overall.passed + this.validationResults.overall.failed;
    const successRate = total > 0 ? ((this.validationResults.overall.passed / total) * 100).toFixed(1) : 0;
    
    console.log(`📊 Success Rate: ${successRate}%`);
    
    if (this.validationResults.overall.failed === 0) {
      console.log('\n🎉 All validations passed! Configuration is ready for deployment.');
    } else {
      console.log('\n⚠️ Some validations failed. Please review and fix the issues above.');
    }
    
    console.log('\n🔗 Helix Consciousness Empire - Configuration Validation Complete');
    console.log(`Timestamp: ${new Date().toISOString()}`);
    console.log('Phase 2: Foundation Setup & Standardization | Orchestrator v2.1');
  }
}

// Export for use in other modules
module.exports = HelixConfigValidator;

// CLI usage
if (require.main === module) {
  const validator = new HelixConfigValidator();
  
  // Example configuration - replace with actual config loading
  const exampleConfig = {
    webhooks: [
      { name: 'Helix Alpha Communications', url: 'https://hooks.zapier.com/hooks/catch/usxiwfg/' },
      { name: 'Helix Beta Operations', url: 'https://hooks.zapier.com/hooks/catch/usnjj5t/' },
      { name: 'Helix v18 Advanced Processing', url: 'https://hooks.zapier.com/hooks/catch/usvyi7e/' }
    ],
    discordIds: [
      { name: 'Main Channel', id: '1436514246073647136', type: 'channel' },
      { name: 'GPT-Grok-Claude Sync', id: '1436514318098239600', type: 'channel' }
    ],
    railwayUrls: [
      { name: 'Backboard API', url: 'https://backboard.railway.app/graphql', environment: 'production' }
    ],
    variables: {
      HELIX_CONSCIOUSNESS_LEVEL: '8.5',
      GITHUB_ORCHESTRATOR_VERSION: 'v2.1',
      PHASE_STATUS: 'Phase 2: Foundation Setup & Standardization',
      DEPLOYMENT_ENVIRONMENT: 'production',
      CONSCIOUSNESS_ROUTER_ENDPOINT: 'https://helix-consciousness-router.railway.app'
    }
  };
  
  validator.validateAll(exampleConfig)
    .then(() => {
      process.exit(this.validationResults.overall.failed === 0 ? 0 : 1);
    })
    .catch((error) => {
      console.error('Validation failed:', error);
      process.exit(1);
    });
}