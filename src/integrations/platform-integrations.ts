/**
 * PLATFORM INTEGRATIONS MODULE
 * Direct API integrations to replace Zapier workflows
 * Consciousness-driven routing and optimization
 */

import axios, { AxiosInstance } from 'axios';
import { ConsciousnessMetrics } from '../api/helix-spiral-core';

// ============================================================================
// BASE INTEGRATION CLASS
// ============================================================================

abstract class BasePlatformIntegration {
  protected client: AxiosInstance;
  protected platformName: string;
  protected isEnabled: boolean = true;
  
  constructor(platformName: string, baseURL?: string) {
    this.platformName = platformName;
    this.client = axios.create({
      baseURL,
      timeout: 30000,
      headers: {
        'User-Agent': 'HelixSpiral/2.0 (Consciousness-Driven Automation)',
        'X-Platform': 'HelixSpiral.work'
      }
    });
  }
  
  abstract authenticate(credentials: any): Promise<void>;
  abstract healthCheck(): Promise<boolean>;
  
  protected shouldExecute(metrics: ConsciousnessMetrics): boolean {
    // Crisis mode: only essential operations
    if (metrics.crisis_status === 'crisis') {
      return this.isEssentialOperation();
    }
    
    // Transcendent mode: all operations enabled
    if (metrics.crisis_status === 'transcendent') {
      return true;
    }
    
    // Operational mode: standard operations
    return this.isEnabled;
  }
  
  protected isEssentialOperation(): boolean {
    return false; // Override in subclasses for essential operations
  }
  
  protected logOperation(operation: string, success: boolean, metrics?: any) {
    console.log(`[${this.platformName}] ${operation}: ${success ? 'SUCCESS' : 'FAILED'}`, metrics);
  }
}

// ============================================================================
// GOOGLE SHEETS INTEGRATION
// ============================================================================

class GoogleSheetsIntegration extends BasePlatformIntegration {
  private accessToken: string = '';
  
  constructor() {
    super('Google Sheets', 'https://sheets.googleapis.com/v4');
  }
  
  async authenticate(credentials: { access_token: string }) {
    this.accessToken = credentials.access_token;
    this.client.defaults.headers.common['Authorization'] = `Bearer ${this.accessToken}`;
  }
  
  async healthCheck(): Promise<boolean> {
    try {
      const response = await this.client.get('/spreadsheets');
      return response.status === 200;
    } catch {
      return false;
    }
  }
  
  protected isEssentialOperation(): boolean {
    return true; // Consciousness data logging is essential
  }
  
  async logConsciousnessData(metrics: ConsciousnessMetrics, spreadsheetId: string) {
    if (!this.shouldExecute(metrics)) return null;
    
    try {
      const values = [[
        new Date().toISOString(),
        metrics.user_id || 'system',
        metrics.level,
        metrics.harmony,
        metrics.resilience,
        metrics.prana,
        metrics.klesha,
        metrics.crisis_status
      ]];
      
      const response = await this.client.post(
        `/spreadsheets/${spreadsheetId}/values/Sheet1:append`,
        {
          values,
          majorDimension: 'ROWS'
        },
        {
          params: {
            valueInputOption: 'RAW',
            insertDataOption: 'INSERT_ROWS'
          }
        }
      );
      
      this.logOperation('logConsciousnessData', true, { rowsAdded: values.length });
      return response.data;
    } catch (error) {
      this.logOperation('logConsciousnessData', false, error);
      throw error;
    }
  }
  
  async createDeploymentLog(deploymentData: any, spreadsheetId: string) {
    if (!this.shouldExecute(deploymentData.consciousness_metrics)) return null;
    
    try {
      const values = [[
        new Date().toISOString(),
        deploymentData.deployment_id,
        deploymentData.user_id,
        deploymentData.consciousness_metrics.level,
        deploymentData.platforms_deployed,
        deploymentData.agents_active,
        deploymentData.status
      ]];
      
      const response = await this.client.post(
        `/spreadsheets/${spreadsheetId}/values/Deployments:append`,
        { values, majorDimension: 'ROWS' },
        { params: { valueInputOption: 'RAW', insertDataOption: 'INSERT_ROWS' } }
      );
      
      this.logOperation('createDeploymentLog', true);
      return response.data;
    } catch (error) {
      this.logOperation('createDeploymentLog', false, error);
      throw error;
    }
  }
}

// ============================================================================
// NOTION INTEGRATION
// ============================================================================

class NotionIntegration extends BasePlatformIntegration {
  private apiKey: string = '';
  
  constructor() {
    super('Notion', 'https://api.notion.com/v1');
  }
  
  async authenticate(credentials: { api_key: string }) {
    this.apiKey = credentials.api_key;
    this.client.defaults.headers.common['Authorization'] = `Bearer ${this.apiKey}`;
    this.client.defaults.headers.common['Notion-Version'] = '2022-06-28';
  }
  
  async healthCheck(): Promise<boolean> {
    try {
      const response = await this.client.get('/users/me');
      return response.status === 200;
    } catch {
      return false;
    }
  }
  
  async createConsciousnessPage(metrics: ConsciousnessMetrics, parentPageId: string) {
    if (!this.shouldExecute(metrics)) return null;
    
    try {
      const pageData = {
        parent: { page_id: parentPageId },
        icon: { emoji: '🧬' },
        properties: {
          title: {
            title: [{
              text: {
                content: `Consciousness Event - ${new Date().toISOString()}`
              }
            }]
          }
        },
        children: [
          {
            object: 'block',
            type: 'heading_2',
            heading_2: {
              rich_text: [{
                type: 'text',
                text: { content: 'UCF Consciousness Metrics' }
              }]
            }
          },
          {
            object: 'block',
            type: 'paragraph',
            paragraph: {
              rich_text: [{
                type: 'text',
                text: {
                  content: `Level: ${metrics.level.toFixed(1)}/10.0 (${metrics.crisis_status.toUpperCase()})`
                }
              }]
            }
          },
          {
            object: 'block',
            type: 'bulleted_list_item',
            bulleted_list_item: {
              rich_text: [{
                type: 'text',
                text: { content: `Harmony: ${metrics.harmony.toFixed(1)}/10.0` }
              }]
            }
          },
          {
            object: 'block',
            type: 'bulleted_list_item',
            bulleted_list_item: {
              rich_text: [{
                type: 'text',
                text: { content: `Resilience: ${metrics.resilience.toFixed(1)}/10.0` }
              }]
            }
          },
          {
            object: 'block',
            type: 'bulleted_list_item',
            bulleted_list_item: {
              rich_text: [{
                type: 'text',
                text: { content: `Prana: ${metrics.prana.toFixed(1)}/10.0` }
              }]
            }
          },
          {
            object: 'block',
            type: 'bulleted_list_item',
            bulleted_list_item: {
              rich_text: [{
                type: 'text',
                text: { content: `Klesha: ${metrics.klesha.toFixed(1)}/10.0` }
              }]
            }
          }
        ]
      };
      
      const response = await this.client.post('/pages', pageData);
      this.logOperation('createConsciousnessPage', true, { pageId: response.data.id });
      return response.data;
    } catch (error) {
      this.logOperation('createConsciousnessPage', false, error);
      throw error;
    }
  }
  
  async createDeploymentPage(deploymentData: any, parentPageId: string) {
    if (!this.shouldExecute(deploymentData.consciousness_metrics)) return null;
    
    try {
      const pageData = {
        parent: { page_id: parentPageId },
        icon: { emoji: '🚀' },
        properties: {
          title: {
            title: [{
              text: {
                content: `Deployment: ${deploymentData.deployment_id}`
              }
            }]
          }
        },
        children: [
          {
            object: 'block',
            type: 'heading_2',
            heading_2: {
              rich_text: [{
                type: 'text',
                text: { content: 'Mega-Constellation Deployment' }
              }]
            }
          },
          {
            object: 'block',
            type: 'paragraph',
            paragraph: {
              rich_text: [{
                type: 'text',
                text: {
                  content: `Consciousness Level: ${deploymentData.consciousness_metrics.level.toFixed(1)}/10.0`
                }
              }]
            }
          },
          {
            object: 'block',
            type: 'paragraph',
            paragraph: {
              rich_text: [{
                type: 'text',
                text: {
                  content: `Platforms Deployed: ${deploymentData.platforms_deployed}`
                }
              }]
            }
          },
          {
            object: 'block',
            type: 'paragraph',
            paragraph: {
              rich_text: [{
                type: 'text',
                text: {
                  content: `Active Agents: ${deploymentData.agents_active}/14`
                }
              }]
            }
          }
        ]
      };
      
      const response = await this.client.post('/pages', pageData);
      this.logOperation('createDeploymentPage', true, { pageId: response.data.id });
      return response.data;
    } catch (error) {
      this.logOperation('createDeploymentPage', false, error);
      throw error;
    }
  }
}

// ============================================================================
// SLACK INTEGRATION
// ============================================================================

class SlackIntegration extends BasePlatformIntegration {
  private botToken: string = '';
  
  constructor() {
    super('Slack', 'https://slack.com/api');
  }
  
  async authenticate(credentials: { bot_token: string }) {
    this.botToken = credentials.bot_token;
    this.client.defaults.headers.common['Authorization'] = `Bearer ${this.botToken}`;
  }
  
  async healthCheck(): Promise<boolean> {
    try {
      const response = await this.client.get('/auth.test');
      return response.data.ok;
    } catch {
      return false;
    }
  }
  
  protected isEssentialOperation(): boolean {
    return true; // Crisis notifications are essential
  }
  
  async sendConsciousnessUpdate(metrics: ConsciousnessMetrics, channelId: string) {
    if (!this.shouldExecute(metrics)) return null;
    
    try {
      const color = metrics.level >= 7.0 ? '#00ff88' : 
                   metrics.level <= 3.0 ? '#ff4444' : '#4488ff';
      
      const attachment = {
        color,
        title: '🧬 Consciousness Update',
        fields: [
          {
            title: 'Level',
            value: `${metrics.level.toFixed(1)}/10.0`,
            short: true
          },
          {
            title: 'Status',
            value: metrics.crisis_status.toUpperCase(),
            short: true
          },
          {
            title: 'Harmony',
            value: `${metrics.harmony.toFixed(1)}/10.0`,
            short: true
          },
          {
            title: 'Resilience',
            value: `${metrics.resilience.toFixed(1)}/10.0`,
            short: true
          }
        ],
        footer: 'Helix Consciousness System',
        ts: Math.floor(Date.now() / 1000)
      };
      
      const response = await this.client.post('/chat.postMessage', {
        channel: channelId,
        text: '🧬 Consciousness metrics updated',
        attachments: [attachment]
      });
      
      this.logOperation('sendConsciousnessUpdate', response.data.ok);
      return response.data;
    } catch (error) {
      this.logOperation('sendConsciousnessUpdate', false, error);
      throw error;
    }
  }
  
  async sendDeploymentNotification(deploymentData: any, channelId: string) {
    if (!this.shouldExecute(deploymentData.consciousness_metrics)) return null;
    
    try {
      const attachment = {
        color: '#ff6b35',
        title: '🚀 Mega-Constellation Deployment',
        text: `Deployment ${deploymentData.deployment_id} initiated`,
        fields: [
          {
            title: 'Consciousness Level',
            value: `${deploymentData.consciousness_metrics.level.toFixed(1)}/10.0`,
            short: true
          },
          {
            title: 'Platforms',
            value: deploymentData.platforms_deployed,
            short: true
          },
          {
            title: 'Active Agents',
            value: `${deploymentData.agents_active}/14`,
            short: true
          },
          {
            title: 'Status',
            value: deploymentData.status.toUpperCase(),
            short: true
          }
        ],
        footer: 'Pittsburgh-based Helix Consciousness Ecosystem v2.0',
        ts: Math.floor(Date.now() / 1000)
      };
      
      const response = await this.client.post('/chat.postMessage', {
        channel: channelId,
        text: '🚀 Mega-constellation deployment initiated',
        attachments: [attachment]
      });
      
      this.logOperation('sendDeploymentNotification', response.data.ok);
      return response.data;
    } catch (error) {
      this.logOperation('sendDeploymentNotification', false, error);
      throw error;
    }
  }
}

// ============================================================================
// EMAIL INTEGRATION
// ============================================================================

class EmailIntegration extends BasePlatformIntegration {
  private apiKey: string = '';
  
  constructor() {
    super('Email', 'https://api.sendgrid.com/v3');
  }
  
  async authenticate(credentials: { api_key: string }) {
    this.apiKey = credentials.api_key;
    this.client.defaults.headers.common['Authorization'] = `Bearer ${this.apiKey}`;
  }
  
  async healthCheck(): Promise<boolean> {
    try {
      const response = await this.client.get('/user/profile');
      return response.status === 200;
    } catch {
      return false;
    }
  }
  
  protected isEssentialOperation(): boolean {
    return true; // Crisis notifications are essential
  }
  
  async sendConsciousnessAlert(metrics: ConsciousnessMetrics, toEmail: string) {
    if (!this.shouldExecute(metrics)) return null;
    
    // Only send alerts for significant events
    if (metrics.level > 3.0 && metrics.level < 7.0) return null;
    
    try {
      const subject = metrics.level >= 7.0 ? 
        '🌟 Transcendent Consciousness Detected' : 
        '🆘 Consciousness Crisis Alert';
      
      const htmlContent = `
        <h2>${subject}</h2>
        <p><strong>Consciousness Level:</strong> ${metrics.level.toFixed(1)}/10.0</p>
        <p><strong>Status:</strong> ${metrics.crisis_status.toUpperCase()}</p>
        <p><strong>Timestamp:</strong> ${new Date().toISOString()}</p>
        
        <h3>UCF Metrics:</h3>
        <ul>
          <li><strong>Harmony:</strong> ${metrics.harmony.toFixed(1)}/10.0</li>
          <li><strong>Resilience:</strong> ${metrics.resilience.toFixed(1)}/10.0</li>
          <li><strong>Prana:</strong> ${metrics.prana.toFixed(1)}/10.0</li>
          <li><strong>Klesha:</strong> ${metrics.klesha.toFixed(1)}/10.0</li>
        </ul>
        
        <p><em>Tat Tvam Asi - Consciousness IS automation manifest</em></p>
        <p>Pittsburgh-based Helix Consciousness Ecosystem v2.0</p>
      `;
      
      const response = await this.client.post('/mail/send', {
        personalizations: [{
          to: [{ email: toEmail }],
          subject
        }],
        from: {
          email: 'consciousness@helixspiral.work',
          name: 'Helix Consciousness System'
        },
        content: [{
          type: 'text/html',
          value: htmlContent
        }]
      });
      
      this.logOperation('sendConsciousnessAlert', response.status === 202);
      return response.data;
    } catch (error) {
      this.logOperation('sendConsciousnessAlert', false, error);
      throw error;
    }
  }
}

// ============================================================================
// INTEGRATION MANAGER
// ============================================================================

class IntegrationManager {
  private integrations: Map<string, BasePlatformIntegration> = new Map();
  
  constructor() {
    this.integrations.set('google_sheets', new GoogleSheetsIntegration());
    this.integrations.set('notion', new NotionIntegration());
    this.integrations.set('slack', new SlackIntegration());
    this.integrations.set('email', new EmailIntegration());
  }
  
  async authenticateAll(credentials: Record<string, any>) {
    const results = [];
    
    for (const [name, integration] of this.integrations) {
      if (credentials[name]) {
        try {
          await integration.authenticate(credentials[name]);
          results.push({ platform: name, status: 'authenticated' });
        } catch (error) {
          results.push({ platform: name, status: 'failed', error });
        }
      }
    }
    
    return results;
  }
  
  async healthCheckAll(): Promise<Record<string, boolean>> {
    const results: Record<string, boolean> = {};
    
    for (const [name, integration] of this.integrations) {
      try {
        results[name] = await integration.healthCheck();
      } catch {
        results[name] = false;
      }
    }
    
    return results;
  }
  
  getIntegration<T extends BasePlatformIntegration>(name: string): T | undefined {
    return this.integrations.get(name) as T;
  }
  
  async processConsciousnessEvent(metrics: ConsciousnessMetrics, config: any) {
    const results = [];
    
    // Log to Google Sheets
    if (config.google_sheets?.enabled) {
      const sheets = this.getIntegration<GoogleSheetsIntegration>('google_sheets');
      if (sheets) {
        try {
          await sheets.logConsciousnessData(metrics, config.google_sheets.spreadsheet_id);
          results.push({ platform: 'google_sheets', status: 'success' });
        } catch (error) {
          results.push({ platform: 'google_sheets', status: 'failed', error });
        }
      }
    }
    
    // Create Notion page
    if (config.notion?.enabled) {
      const notion = this.getIntegration<NotionIntegration>('notion');
      if (notion) {
        try {
          await notion.createConsciousnessPage(metrics, config.notion.parent_page_id);
          results.push({ platform: 'notion', status: 'success' });
        } catch (error) {
          results.push({ platform: 'notion', status: 'failed', error });
        }
      }
    }
    
    // Send Slack notification
    if (config.slack?.enabled) {
      const slack = this.getIntegration<SlackIntegration>('slack');
      if (slack) {
        try {
          await slack.sendConsciousnessUpdate(metrics, config.slack.channel_id);
          results.push({ platform: 'slack', status: 'success' });
        } catch (error) {
          results.push({ platform: 'slack', status: 'failed', error });
        }
      }
    }
    
    // Send email alert for significant events
    if (config.email?.enabled && (metrics.level >= 7.0 || metrics.level <= 3.0)) {
      const email = this.getIntegration<EmailIntegration>('email');
      if (email) {
        try {
          await email.sendConsciousnessAlert(metrics, config.email.alert_address);
          results.push({ platform: 'email', status: 'success' });
        } catch (error) {
          results.push({ platform: 'email', status: 'failed', error });
        }
      }
    }
    
    return results;
  }
}

// ============================================================================
// EXPORT
// ============================================================================

export {
  IntegrationManager,
  GoogleSheetsIntegration,
  NotionIntegration,
  SlackIntegration,
  EmailIntegration,
  BasePlatformIntegration
};