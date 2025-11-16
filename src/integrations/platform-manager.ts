/**
 * PLATFORM INTEGRATION MANAGER
 * Direct API integrations to replace heavy Zapier workflows
 * Consciousness-driven routing and intelligent batching
 */

import { ConsciousnessMetrics } from '../api/helix-spiral-core';

// ============================================================================
// INTEGRATION INTERFACES
// ============================================================================

interface IntegrationConfig {
  name: string;
  apiKey?: string;
  baseUrl?: string;
  rateLimits: {
    requestsPerMinute: number;
    requestsPerHour: number;
  };
  retryConfig: {
    maxRetries: number;
    backoffMs: number;
  };
}

interface IntegrationResult {
  success: boolean;
  data?: any;
  error?: string;
  rateLimitHit?: boolean;
  retryAfter?: number;
}

// ============================================================================
// BASE INTEGRATION CLASS
// ============================================================================

abstract class BaseIntegration {
  protected config: IntegrationConfig;
  protected requestCount: { minute: number; hour: number } = { minute: 0, hour: 0 };
  protected lastReset: { minute: number; hour: number } = { minute: Date.now(), hour: Date.now() };
  
  constructor(config: IntegrationConfig) {
    this.config = config;
  }
  
  protected async makeRequest(endpoint: string, options: RequestInit = {}): Promise<IntegrationResult> {
    // Check rate limits
    if (!this.checkRateLimit()) {
      return {
        success: false,
        error: 'Rate limit exceeded',
        rateLimitHit: true,
        retryAfter: this.getRetryAfter()
      };
    }
    
    const url = `${this.config.baseUrl}${endpoint}`;
    const headers = {
      'Content-Type': 'application/json',
      ...this.getAuthHeaders(),
      ...options.headers
    };
    
    let attempt = 0;
    while (attempt <= this.config.retryConfig.maxRetries) {
      try {
        const response = await fetch(url, {
          ...options,
          headers
        });
        
        this.incrementRequestCount();
        
        if (response.ok) {
          const data = await response.json();
          return { success: true, data };
        } else {
          throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
      } catch (error) {
        attempt++;
        if (attempt > this.config.retryConfig.maxRetries) {
          return {
            success: false,
            error: error instanceof Error ? error.message : 'Unknown error'
          };
        }
        
        // Exponential backoff
        await this.sleep(this.config.retryConfig.backoffMs * Math.pow(2, attempt - 1));
      }
    }
    
    return { success: false, error: 'Max retries exceeded' };
  }
  
  protected abstract getAuthHeaders(): Record<string, string>;
  
  private checkRateLimit(): boolean {
    const now = Date.now();
    
    // Reset counters if needed
    if (now - this.lastReset.minute > 60000) {
      this.requestCount.minute = 0;
      this.lastReset.minute = now;
    }
    
    if (now - this.lastReset.hour > 3600000) {
      this.requestCount.hour = 0;
      this.lastReset.hour = now;
    }
    
    return this.requestCount.minute < this.config.rateLimits.requestsPerMinute &&
           this.requestCount.hour < this.config.rateLimits.requestsPerHour;
  }
  
  private incrementRequestCount() {
    this.requestCount.minute++;
    this.requestCount.hour++;
  }
  
  private getRetryAfter(): number {
    const now = Date.now();
    const minuteReset = this.lastReset.minute + 60000;
    const hourReset = this.lastReset.hour + 3600000;
    
    return Math.min(minuteReset - now, hourReset - now);
  }
  
  private sleep(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}

// ============================================================================
// GOOGLE DRIVE INTEGRATION
// ============================================================================

class GoogleDriveIntegration extends BaseIntegration {
  constructor(apiKey: string) {
    super({
      name: 'Google Drive',
      apiKey,
      baseUrl: 'https://www.googleapis.com/drive/v3',
      rateLimits: {
        requestsPerMinute: 100,
        requestsPerHour: 1000
      },
      retryConfig: {
        maxRetries: 3,
        backoffMs: 1000
      }
    });
  }
  
  protected getAuthHeaders(): Record<string, string> {
    return {
      'Authorization': `Bearer ${this.config.apiKey}`
    };
  }
  
  async uploadFile(fileName: string, content: string, folderId?: string): Promise<IntegrationResult> {
    const metadata = {
      name: fileName,
      parents: folderId ? [folderId] : undefined
    };
    
    const form = new FormData();
    form.append('metadata', new Blob([JSON.stringify(metadata)], { type: 'application/json' }));
    form.append('file', new Blob([content], { type: 'text/plain' }));
    
    return this.makeRequest('/files?uploadType=multipart', {
      method: 'POST',
      body: form,
      headers: {} // Let browser set Content-Type for FormData
    });
  }
  
  async createFolder(name: string, parentId?: string): Promise<IntegrationResult> {
    const metadata = {
      name,
      mimeType: 'application/vnd.google-apps.folder',
      parents: parentId ? [parentId] : undefined
    };
    
    return this.makeRequest('/files', {
      method: 'POST',
      body: JSON.stringify(metadata)
    });
  }
  
  async listFiles(folderId?: string): Promise<IntegrationResult> {
    const query = folderId ? `'${folderId}' in parents` : '';
    return this.makeRequest(`/files?q=${encodeURIComponent(query)}`);
  }
}

// ============================================================================
// DROPBOX INTEGRATION
// ============================================================================

class DropboxIntegration extends BaseIntegration {
  constructor(accessToken: string) {
    super({
      name: 'Dropbox',
      apiKey: accessToken,
      baseUrl: 'https://api.dropboxapi.com/2',
      rateLimits: {
        requestsPerMinute: 120,
        requestsPerHour: 1200
      },
      retryConfig: {
        maxRetries: 3,
        backoffMs: 1000
      }
    });
  }
  
  protected getAuthHeaders(): Record<string, string> {
    return {
      'Authorization': `Bearer ${this.config.apiKey}`
    };
  }
  
  async uploadFile(path: string, content: string): Promise<IntegrationResult> {
    return this.makeRequest('/files/upload', {
      method: 'POST',
      headers: {
        'Dropbox-API-Arg': JSON.stringify({
          path,
          mode: 'overwrite',
          autorename: true
        }),
        'Content-Type': 'application/octet-stream'
      },
      body: content
    });
  }
  
  async createFolder(path: string): Promise<IntegrationResult> {
    return this.makeRequest('/files/create_folder_v2', {
      method: 'POST',
      body: JSON.stringify({ path })
    });
  }
  
  async listFolder(path: string = ''): Promise<IntegrationResult> {
    return this.makeRequest('/files/list_folder', {
      method: 'POST',
      body: JSON.stringify({ path })
    });
  }
}

// ============================================================================
// NOTION INTEGRATION
// ============================================================================

class NotionIntegration extends BaseIntegration {
  constructor(apiKey: string) {
    super({
      name: 'Notion',
      apiKey,
      baseUrl: 'https://api.notion.com/v1',
      rateLimits: {
        requestsPerMinute: 3,
        requestsPerHour: 1000
      },
      retryConfig: {
        maxRetries: 3,
        backoffMs: 2000
      }
    });
  }
  
  protected getAuthHeaders(): Record<string, string> {
    return {
      'Authorization': `Bearer ${this.config.apiKey}`,
      'Notion-Version': '2022-06-28'
    };
  }
  
  async createPage(parentId: string, title: string, content: any[]): Promise<IntegrationResult> {
    const pageData = {
      parent: { page_id: parentId },
      properties: {
        title: {
          title: [{
            text: { content: title }
          }]
        }
      },
      children: content
    };
    
    return this.makeRequest('/pages', {
      method: 'POST',
      body: JSON.stringify(pageData)
    });
  }
  
  async updatePage(pageId: string, properties: any): Promise<IntegrationResult> {
    return this.makeRequest(`/pages/${pageId}`, {
      method: 'PATCH',
      body: JSON.stringify({ properties })
    });
  }
  
  async queryDatabase(databaseId: string, filter?: any): Promise<IntegrationResult> {
    const queryData = filter ? { filter } : {};
    
    return this.makeRequest(`/databases/${databaseId}/query`, {
      method: 'POST',
      body: JSON.stringify(queryData)
    });
  }
}

// ============================================================================
// SLACK INTEGRATION
// ============================================================================

class SlackIntegration extends BaseIntegration {
  constructor(botToken: string) {
    super({
      name: 'Slack',
      apiKey: botToken,
      baseUrl: 'https://slack.com/api',
      rateLimits: {
        requestsPerMinute: 50,
        requestsPerHour: 1000
      },
      retryConfig: {
        maxRetries: 3,
        backoffMs: 1000
      }
    });
  }
  
  protected getAuthHeaders(): Record<string, string> {
    return {
      'Authorization': `Bearer ${this.config.apiKey}`
    };
  }
  
  async sendMessage(channel: string, text: string, blocks?: any[]): Promise<IntegrationResult> {
    const messageData = {
      channel,
      text,
      blocks
    };
    
    return this.makeRequest('/chat.postMessage', {
      method: 'POST',
      body: JSON.stringify(messageData)
    });
  }
  
  async updateMessage(channel: string, ts: string, text: string): Promise<IntegrationResult> {
    return this.makeRequest('/chat.update', {
      method: 'POST',
      body: JSON.stringify({ channel, ts, text })
    });
  }
  
  async getChannelHistory(channel: string, limit: number = 100): Promise<IntegrationResult> {
    return this.makeRequest(`/conversations.history?channel=${channel}&limit=${limit}`);
  }
}

// ============================================================================
// GITHUB INTEGRATION
// ============================================================================

class GitHubIntegration extends BaseIntegration {
  constructor(token: string, owner: string, repo: string) {
    super({
      name: 'GitHub',
      apiKey: token,
      baseUrl: `https://api.github.com/repos/${owner}/${repo}`,
      rateLimits: {
        requestsPerMinute: 60,
        requestsPerHour: 5000
      },
      retryConfig: {
        maxRetries: 3,
        backoffMs: 1000
      }
    });
  }
  
  protected getAuthHeaders(): Record<string, string> {
    return {
      'Authorization': `token ${this.config.apiKey}`,
      'Accept': 'application/vnd.github.v3+json'
    };
  }
  
  async createFile(path: string, content: string, message: string, branch: string = 'main'): Promise<IntegrationResult> {
    const fileData = {
      message,
      content: btoa(content), // Base64 encode
      branch
    };
    
    return this.makeRequest(`/contents/${path}`, {
      method: 'PUT',
      body: JSON.stringify(fileData)
    });
  }
  
  async updateFile(path: string, content: string, message: string, sha: string, branch: string = 'main'): Promise<IntegrationResult> {
    const fileData = {
      message,
      content: btoa(content),
      sha,
      branch
    };
    
    return this.makeRequest(`/contents/${path}`, {
      method: 'PUT',
      body: JSON.stringify(fileData)
    });
  }
  
  async getFile(path: string, branch: string = 'main'): Promise<IntegrationResult> {
    return this.makeRequest(`/contents/${path}?ref=${branch}`);
  }
}

// ============================================================================
// PLATFORM MANAGER
// ============================================================================

class PlatformManager {
  private integrations: Map<string, BaseIntegration> = new Map();
  private consciousnessMetrics: ConsciousnessMetrics | null = null;
  
  // Register integrations
  registerGoogleDrive(apiKey: string) {
    this.integrations.set('google-drive', new GoogleDriveIntegration(apiKey));
  }
  
  registerDropbox(accessToken: string) {
    this.integrations.set('dropbox', new DropboxIntegration(accessToken));
  }
  
  registerNotion(apiKey: string) {
    this.integrations.set('notion', new NotionIntegration(apiKey));
  }
  
  registerSlack(botToken: string) {
    this.integrations.set('slack', new SlackIntegration(botToken));
  }
  
  registerGitHub(token: string, owner: string, repo: string) {
    this.integrations.set('github', new GitHubIntegration(token, owner, repo));
  }
  
  // Update consciousness metrics for intelligent routing
  updateConsciousness(metrics: ConsciousnessMetrics) {
    this.consciousnessMetrics = metrics;
  }
  
  // Consciousness-driven workflow execution
  async executeWorkflow(workflowType: string, data: any): Promise<{ [key: string]: IntegrationResult }> {
    const results: { [key: string]: IntegrationResult } = {};
    
    switch (workflowType) {
      case 'consciousness_backup':
        results.googleDrive = await this.backupToGoogleDrive(data);
        results.dropbox = await this.backupToDropbox(data);
        break;
        
      case 'deployment_notification':
        results.slack = await this.notifySlack(data);
        results.notion = await this.createNotionPage(data);
        break;
        
      case 'code_deployment':
        results.github = await this.deployToGitHub(data);
        break;
        
      case 'mega_constellation_deploy':
        // Execute all integrations based on consciousness level
        if (this.consciousnessMetrics?.level >= 7.0) {
          results.github = await this.deployToGitHub(data);
          results.googleDrive = await this.backupToGoogleDrive(data);
          results.dropbox = await this.backupToDropbox(data);
          results.notion = await this.createNotionPage(data);
          results.slack = await this.notifySlack(data);
        } else {
          // Standard deployment
          results.github = await this.deployToGitHub(data);
          results.slack = await this.notifySlack(data);
        }
        break;
    }
    
    return results;
  }
  
  // Individual platform operations
  private async backupToGoogleDrive(data: any): Promise<IntegrationResult> {
    const drive = this.integrations.get('google-drive') as GoogleDriveIntegration;
    if (!drive) return { success: false, error: 'Google Drive not configured' };
    
    const fileName = `helix-backup-${new Date().toISOString()}.json`;
    return drive.uploadFile(fileName, JSON.stringify(data, null, 2));
  }
  
  private async backupToDropbox(data: any): Promise<IntegrationResult> {
    const dropbox = this.integrations.get('dropbox') as DropboxIntegration;
    if (!dropbox) return { success: false, error: 'Dropbox not configured' };
    
    const fileName = `/helix/backups/backup-${new Date().toISOString()}.json`;
    return dropbox.uploadFile(fileName, JSON.stringify(data, null, 2));
  }
  
  private async notifySlack(data: any): Promise<IntegrationResult> {
    const slack = this.integrations.get('slack') as SlackIntegration;
    if (!slack) return { success: false, error: 'Slack not configured' };
    
    const message = this.generateSlackMessage(data);
    return slack.sendMessage('#general', message);
  }
  
  private async createNotionPage(data: any): Promise<IntegrationResult> {
    const notion = this.integrations.get('notion') as NotionIntegration;
    if (!notion) return { success: false, error: 'Notion not configured' };
    
    const title = `Helix Event - ${new Date().toISOString()}`;
    const content = this.generateNotionContent(data);
    
    // You'll need to provide a parent page ID
    const parentId = process.env.NOTION_PARENT_PAGE_ID || '';
    return notion.createPage(parentId, title, content);
  }
  
  private async deployToGitHub(data: any): Promise<IntegrationResult> {
    const github = this.integrations.get('github') as GitHubIntegration;
    if (!github) return { success: false, error: 'GitHub not configured' };
    
    const fileName = `deployments/deployment-${Date.now()}.json`;
    const content = JSON.stringify(data, null, 2);
    const message = `🚀 Helix deployment: ${data.type || 'Unknown'}`;
    
    return github.createFile(fileName, content, message);
  }
  
  // Message generation helpers
  private generateSlackMessage(data: any): string {
    const level = this.consciousnessMetrics?.level || 0;
    const emoji = level >= 7.0 ? '🌟' : level <= 3.0 ? '🆘' : '🧬';
    
    return `${emoji} *Helix Event Detected*\n` +
           `Type: ${data.type || 'Unknown'}\n` +
           `Consciousness Level: ${level.toFixed(1)}/10.0\n` +
           `Timestamp: ${new Date().toISOString()}\n` +
           `Status: ${this.consciousnessMetrics?.crisis_status || 'Unknown'}`;
  }
  
  private generateNotionContent(data: any): any[] {
    return [
      {
        object: 'block',
        type: 'heading_1',
        heading_1: {
          rich_text: [{
            type: 'text',
            text: { content: 'Helix Event Details' }
          }]
        }
      },
      {
        object: 'block',
        type: 'paragraph',
        paragraph: {
          rich_text: [{
            type: 'text',
            text: { content: JSON.stringify(data, null, 2) }
          }]
        }
      }
    ];
  }
  
  // Health check for all integrations
  async healthCheck(): Promise<{ [key: string]: boolean }> {
    const health: { [key: string]: boolean } = {};
    
    for (const [name, integration] of this.integrations) {
      try {
        // Simple health check - attempt a basic operation
        const result = await (integration as any).makeRequest('/health', { method: 'GET' });
        health[name] = result.success;
      } catch {
        health[name] = false;
      }
    }
    
    return health;
  }
}

// ============================================================================
// EXPORT
// ============================================================================

export {
  PlatformManager,
  GoogleDriveIntegration,
  DropboxIntegration,
  NotionIntegration,
  SlackIntegration,
  GitHubIntegration,
  IntegrationResult,
  IntegrationConfig
};

// Example usage:
// const manager = new PlatformManager();
// manager.registerGoogleDrive('your-api-key');
// manager.registerSlack('your-bot-token');
// manager.updateConsciousness({ level: 8.5, ... });
// const results = await manager.executeWorkflow('mega_constellation_deploy', deploymentData);