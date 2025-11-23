/**
 * 🌌 Helix Railway API Client
 * Secure communication with Railway backend services
 */

import axios, { AxiosInstance, AxiosResponse } from 'axios';
import type { 
  UCFMetrics, 
  HelixAgent, 
  RailwayService, 
  DiscordBotStatus,
  HelixApiResponse 
} from '../types/helix.types.js';
import { config } from './config.js';
import { railwayLogger, measureTime } from './logger.js';

// Railway API Client Class
export class RailwayApiClient {
  private client: AxiosInstance;
  private logger = railwayLogger;

  constructor() {
    this.client = axios.create({
      baseURL: config.railway.apiUrl,
      timeout: 30000,
      headers: {
        'Content-Type': 'application/json',
        'User-Agent': `Helix-MCP-Server/${config.mcp.version}`,
        'Authorization': `Bearer ${config.railway.token}`,
      },
    });

    // Request interceptor
    this.client.interceptors.request.use(
      (config) => {
        this.logger.debug(`🚂 Railway API Request: ${config.method?.toUpperCase()} ${config.url}`, {
          url: config.url,
          method: config.method,
          headers: config.headers,
        });
        return config;
      },
      (error) => {
        this.logger.error('Railway API request error', error);
        return Promise.reject(error);
      }
    );

    // Response interceptor
    this.client.interceptors.response.use(
      (response: AxiosResponse) => {
        this.logger.debug(`🚂 Railway API Response: ${response.status} ${response.config.url}`, {
          status: response.status,
          url: response.config.url,
          duration: response.headers['x-response-time'],
        });
        return response;
      },
      (error) => {
        this.logger.error('Railway API response error', {
          status: error.response?.status,
          url: error.config?.url,
          message: error.message,
        });
        return Promise.reject(error);
      }
    );
  }

  // Health check
  async healthCheck(): Promise<boolean> {
    try {
      const response = await measureTime(
        'health_check',
        () => this.client.get('/status')
      );
      
      return response.status === 200 && response.data?.status === 'healthy';
    } catch (error) {
      this.logger.error('Health check failed', error as Error);
      return false;
    }
  }

  // UCF Metrics Methods
  async getUcfMetrics(agentId?: string): Promise<UCFMetrics> {
    try {
      const response = await measureTime(
        'get_ucf_metrics',
        () => this.client.get<HelixApiResponse<UCFMetrics>>('/.well-known/helix.json', {
          params: agentId ? { agentId } : undefined,
        })
      );

      if (!response.data?.success || !response.data?.data) {
        throw new Error('Invalid response format');
      }

      return response.data.data;
    } catch (error) {
      this.logger.error('Failed to get UCF metrics', error as Error);
      throw error;
    }
  }

  async updateUcfMetrics(metrics: Partial<UCFMetrics>): Promise<UCFMetrics> {
    try {
      const response = await measureTime(
        'update_ucf_metrics',
        () => this.client.put<HelixApiResponse<UCFMetrics>>('/.well-known/helix.json', {
          metrics,
          timestamp: new Date().toISOString(),
        })
      );

      if (!response.data?.success || !response.data?.data) {
        throw new Error('Invalid response format');
      }

      return response.data.data;
    } catch (error) {
      this.logger.error('Failed to update UCF metrics', error as Error);
      throw error;
    }
  }

  // Agent Management Methods
  async getAgents(): Promise<HelixAgent[]> {
    try {
      const response = await measureTime(
        'get_agents',
        () => this.client.get<HelixApiResponse<HelixAgent[]>>('/api/agents')
      );

      if (!response.data?.success || !response.data?.data) {
        throw new Error('Invalid response format');
      }

      return response.data.data;
    } catch (error) {
      this.logger.error('Failed to get agents', error as Error);
      throw error;
    }
  }

  async getAgent(agentId: string): Promise<HelixAgent> {
    try {
      const response = await measureTime(
        'get_agent',
        () => this.client.get<HelixApiResponse<HelixAgent>>(`/api/agents/${agentId}`)
      );

      if (!response.data?.success || !response.data?.data) {
        throw new Error('Invalid response format');
      }

      return response.data.data;
    } catch (error) {
      this.logger.error(`Failed to get agent ${agentId}`, error as Error);
      throw error;
    }
  }

  async activateAgent(agentId: string): Promise<HelixAgent> {
    try {
      const response = await measureTime(
        'activate_agent',
        () => this.client.post<HelixApiResponse<HelixAgent>>(`/api/agents/${agentId}/activate`)
      );

      if (!response.data?.success || !response.data?.data) {
        throw new Error('Invalid response format');
      }

      this.logger.agent('Activated', agentId);
      return response.data.data;
    } catch (error) {
      this.logger.error(`Failed to activate agent ${agentId}`, error as Error);
      throw error;
    }
  }

  async deactivateAgent(agentId: string): Promise<HelixAgent> {
    try {
      const response = await measureTime(
        'deactivate_agent',
        () => this.client.post<HelixApiResponse<HelixAgent>>(`/api/agents/${agentId}/deactivate`)
      );

      if (!response.data?.success || !response.data?.data) {
        throw new Error('Invalid response format');
      }

      this.logger.agent('Deactivated', agentId);
      return response.data.data;
    } catch (error) {
      this.logger.error(`Failed to deactivate agent ${agentId}`, error as Error);
      throw error;
    }
  }

  async executeAgentCommand(agentId: string, command: string, parameters?: Record<string, any>): Promise<any> {
    try {
      const response = await measureTime(
        'execute_agent_command',
        () => this.client.post<HelixApiResponse>(`/api/agents/${agentId}/execute`, {
          command,
          parameters,
          timestamp: new Date().toISOString(),
        })
      );

      if (!response.data?.success) {
        throw new Error('Command execution failed');
      }

      this.logger.agent(`Executed: ${command}`, agentId, { parameters });
      return response.data.data;
    } catch (error) {
      this.logger.error(`Failed to execute command on agent ${agentId}`, error as Error);
      throw error;
    }
  }

  // Railway Service Management
  async getRailwayServices(): Promise<RailwayService[]> {
    try {
      const response = await measureTime(
        'get_railway_services',
        () => this.client.get<HelixApiResponse<RailwayService[]>>('/api/railway/services')
      );

      if (!response.data?.success || !response.data?.data) {
        throw new Error('Invalid response format');
      }

      return response.data.data;
    } catch (error) {
      this.logger.error('Failed to get Railway services', error as Error);
      throw error;
    }
  }

  async getRailwayService(serviceName: string): Promise<RailwayService> {
    try {
      const response = await measureTime(
        'get_railway_service',
        () => this.client.get<HelixApiResponse<RailwayService>>(`/api/railway/services/${serviceName}`)
      );

      if (!response.data?.success || !response.data?.data) {
        throw new Error('Invalid response format');
      }

      return response.data.data;
    } catch (error) {
      this.logger.error(`Failed to get Railway service ${serviceName}`, error as Error);
      throw error;
    }
  }

  async restartRailwayService(serviceName: string): Promise<boolean> {
    try {
      const response = await measureTime(
        'restart_railway_service',
        () => this.client.post<HelixApiResponse>(`/api/railway/services/${serviceName}/restart`)
      );

      if (!response.data?.success) {
        throw new Error('Restart failed');
      }

      this.logger.railway(serviceName, 'Restarted');
      return true;
    } catch (error) {
      this.logger.error(`Failed to restart Railway service ${serviceName}`, error as Error);
      throw error;
    }
  }

  async getServiceLogs(serviceName: string, lines: number = 100): Promise<string[]> {
    try {
      const response = await measureTime(
        'get_service_logs',
        () => this.client.get<HelixApiResponse<string[]>>(`/api/railway/services/${serviceName}/logs`, {
          params: { lines },
        })
      );

      if (!response.data?.success || !response.data?.data) {
        throw new Error('Invalid response format');
      }

      return response.data.data;
    } catch (error) {
      this.logger.error(`Failed to get logs for Railway service ${serviceName}`, error as Error);
      throw error;
    }
  }

  // Discord Bot Methods
  async getDiscordStatus(): Promise<DiscordBotStatus> {
    try {
      const response = await measureTime(
        'get_discord_status',
        () => this.client.get<HelixApiResponse<DiscordBotStatus>>('/api/discord/status')
      );

      if (!response.data?.success || !response.data?.data) {
        throw new Error('Invalid response format');
      }

      return response.data.data;
    } catch (error) {
      this.logger.error('Failed to get Discord status', error as Error);
      throw error;
    }
  }

  async sendDiscordCommand(command: string, channelId?: string): Promise<any> {
    try {
      const response = await measureTime(
        'send_discord_command',
        () => this.client.post<HelixApiResponse>('/api/discord/command', {
          command,
          channelId,
          timestamp: new Date().toISOString(),
        })
      );

      if (!response.data?.success) {
        throw new Error('Command execution failed');
      }

      this.logger.discord(command);
      return response.data.data;
    } catch (error) {
      this.logger.error(`Failed to send Discord command: ${command}`, error as Error);
      throw error;
    }
  }

  // WebSocket Connection Info
  getWebSocketUrl(): string {
    const wsUrl = config.railway.apiUrl.replace('http', 'ws');
    return `${wsUrl}/ws`;
  }

  // Batch Operations
  async getSystemStatus(): Promise<{
    ucfMetrics: UCFMetrics;
    agents: HelixAgent[];
    railwayServices: RailwayService[];
    discordStatus: DiscordBotStatus;
  }> {
    try {
      const [ucfMetrics, agents, railwayServices, discordStatus] = await Promise.all([
        this.getUcfMetrics(),
        this.getAgents(),
        this.getRailwayServices(),
        this.getDiscordStatus(),
      ]);

      this.logger.info('🌊 Complete system status retrieved');
      
      return {
        ucfMetrics,
        agents,
        railwayServices,
        discordStatus,
      };
    } catch (error) {
      this.logger.error('Failed to get complete system status', error as Error);
      throw error;
    }
  }

  // Performance Metrics
  async getPerformanceMetrics(): Promise<{
    responseTime: number;
    uptime: number;
    requestCount: number;
    errorCount: number;
    memoryUsage: number;
  }> {
    try {
      const response = await measureTime(
        'get_performance_metrics',
        () => this.client.get<HelixApiResponse>('/api/metrics/performance')
      );

      if (!response.data?.success || !response.data?.data) {
        throw new Error('Invalid response format');
      }

      return response.data.data;
    } catch (error) {
      this.logger.error('Failed to get performance metrics', error as Error);
      throw error;
    }
  }
}

// Export singleton instance
export const railwayApi = new RailwayApiClient();

// Initialize API client
export const initializeApiClient = async (): Promise<boolean> => {
  try {
    const isHealthy = await railwayApi.healthCheck();
    if (isHealthy) {
      railwayLogger.info('🚂 Railway API client initialized and connected');
      return true;
    } else {
      railwayLogger.warn('🚂 Railway API client initialized but backend is unhealthy');
      return false;
    }
  } catch (error) {
    railwayLogger.error('❌ Failed to initialize Railway API client', error as Error);
    return false;
  }
};

export default railwayApi;