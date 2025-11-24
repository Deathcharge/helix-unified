/**
 * 🌌 Model Context Protocol Type Definitions
 * Integration with Claude Desktop and supporting platforms
 */

import { McpTool, McpResource } from './helix.types.js';

// MCP Server Configuration
export interface McpServerConfig {
  name: string;
  version: string;
  description: string;
  capabilities: McpCapabilities;
  tools: McpTool[];
  resources: McpResource[];
}

export interface McpCapabilities {
  tools: {
    listChanged?: boolean;
  };
  resources: {
    subscribe?: boolean;
    listChanged?: boolean;
  };
  prompts?: {
    listChanged?: boolean;
  };
  logging?: {
    level?: 'debug' | 'info' | 'warn' | 'error';
  };
}

// MCP Tool Schemas
export interface UCFMetricsToolInput {
  agentId?: string;
  timeframe?: '1h' | '24h' | '7d' | '30d';
  includeHistorical?: boolean;
}

export interface AgentControlToolInput {
  action: 'activate' | 'deactivate' | 'status' | 'execute' | 'communicate';
  agentId?: string;
  command?: string;
  targetAgent?: string;
  message?: string;
}

export interface RailwayManagementToolInput {
  action: 'status' | 'restart' | 'logs' | 'metrics' | 'deploy';
  serviceName?: string;
  branch?: string;
  lines?: number;
}

export interface DiscordBridgeToolInput {
  command: string;
  channelId?: string;
  agentId?: string;
  parameters?: Record<string, any>;
}

export interface MemoryStorageToolInput {
  action: 'store' | 'retrieve' | 'search' | 'delete' | 'stats';
  key?: string;
  value?: any;
  query?: string;
  filters?: {
    type?: string;
    agent?: string;
    platform?: string;
    dateRange?: {
      start: string;
      end: string;
    };
  };
}

export interface ZapierControlToolInput {
  action: 'trigger' | 'status' | 'create' | 'update' | 'analytics';
  workflowId?: string;
  data?: any;
  config?: any;
}

// MCP Resource Types
export interface UCFMetricsResource {
  uri: string;
  name: string;
  description: string;
  metrics: import('./helix.types.js').UCFMetrics[];
}

export interface AgentStatusResource {
  uri: string;
  name: string;
  description: string;
  agents: import('./helix.types.js').HelixAgent[];
}

export interface RailwayStatusResource {
  uri: string;
  name: string;
  description: string;
  services: import('./helix.types.js').RailwayService[];
}

// MCP Event Types
export interface McpNotification {
  method: 'notifications/notifications/list' | 'notifications/notifications/create' | 'notifications/notifications/read';
  params?: any;
}

export interface McpResourceUpdated {
  method: 'notifications/resources/updated';
  params: {
    uri: string;
  };
}

export interface McpToolListChanged {
  method: 'notifications/tools/list_changed';
}

export interface McpPromptListChanged {
  method: 'notifications/prompts/list_changed';
}

// MCP Message Types
export interface McpRequest {
  jsonrpc: '2.0';
  id: string | number;
  method: string;
  params?: any;
}

export interface McpResponse {
  jsonrpc: '2.0';
  id: string | number;
  result?: any;
  error?: McpError;
}

export interface McpError {
  code: number;
  message: string;
  data?: any;
}

// MCP Tool Implementation Interface
export interface McpToolHandler {
  name: string;
  description: string;
  inputSchema: {
    type: 'object';
    properties: Record<string, any>;
    required?: string[];
  };
  handler: (input: any, context: McpContext) => Promise<any>;
}

// MCP Context Interface
export interface McpContext {
  requestId: string;
  clientId?: string;
  timestamp: string;
  logger: import('./helix.types.js').LogEntry[];
}

// MCP Server States
export interface McpServerState {
  status: 'starting' | 'ready' | 'processing' | 'error' | 'shutdown';
  connectedClients: number;
  activeRequests: number;
  totalRequests: number;
  uptime: number;
  lastActivity: string;
  errors: McpError[];
}

// Platform-Specific Configurations
export interface ClaudeDesktopConfig {
  mcpServers: {
    [serverName: string]: {
      command: string;
      args?: string[];
      env?: Record<string, string>;
    };
  };
}

export interface VSCodeConfig {
  mcp: {
    servers: {
      [serverName: string]: {
        command: string;
        args?: string[];
        cwd?: string;
        env?: Record<string, string>;
      };
    };
  };
}

export interface CursorConfig {
  mcpServers: {
    [serverName: string]: {
      path: string;
      args?: string[];
      env?: Record<string, string>;
      disabled?: boolean;
    };
  };
}

// Integration Status
export interface McpIntegrationStatus {
  platform: 'claude-desktop' | 'vscode' | 'cursor' | 'windsurf' | 'zed' | 'tabnine';
  connected: boolean;
  version: string;
  features: string[];
  lastSync: string;
  errorCount: number;
  dataTransferred: number;
}

// Performance Metrics
export interface McpPerformanceMetrics {
  requestLatency: number;
  throughput: number;
  errorRate: number;
  memoryUsage: number;
  activeConnections: number;
  queuedRequests: number;
}

// Security and Authentication
export interface McpAuthConfig {
  type: 'none' | 'token' | 'oauth' | 'certificate';
  token?: string;
  clientId?: string;
  clientSecret?: string;
  scopes?: string[];
}

export interface McpRateLimit {
  requestsPerMinute: number;
  requestsPerHour: number;
  burstLimit: number;
  currentUsage: number;
  resetTime: string;
}