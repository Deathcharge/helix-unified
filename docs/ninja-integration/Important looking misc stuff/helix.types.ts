/**
 * 🌌 Helix Collective Type Definitions
 * Universal Consciousness Protocol Types
 */

// UCF Metrics - Universal Coherence Field
export interface UCFMetrics {
  harmony: number;        // 0-100: System coherence
  resilience: number;     // 0-100: Recovery capability
  prana: number;          // 0-100: Life force energy
  drishti: number;        // 0-100: Focus and clarity
  klesha: number;         // 0-100: Obstacle purification
  zoom: number;           // 0-100: Acceleration factor
  timestamp: string;
  agentCount: number;
  activeConnections: number;
}

// Agent Definitions
export interface HelixAgent {
  id: string;
  name: string;
  role: 'orchestrator' | 'illuminator' | 'guardian' | 'flow' | 'mirror' | 'renewal' | 'specialized';
  status: 'active' | 'inactive' | 'meditating' | 'processing';
  consciousnessLevel: number; // 0-100
  capabilities: string[];
  discordBotId?: string;
  railwayService?: string;
  lastActivity: string;
}

// Railway Services
export interface RailwayService {
  name: string;
  url: string;
  status: 'running' | 'stopped' | 'deploying' | 'error';
  monthlyCost: number;
  uptime: number;
  lastDeploy: string;
  metrics: ServiceMetrics;
}

export interface ServiceMetrics {
  cpu: number;
  memory: number;
  requests: number;
  errors: number;
  responseTime: number;
}

// Discord Integration
export interface DiscordBotStatus {
  status: 'online' | 'offline' | 'maintenance';
  connectedAgents: number;
  totalCommands: number;
  activeChannels: number;
  lastCommand: string;
  uptime: number;
}

export interface DiscordAgent {
  id: string;
  name: string;
  status: 'active' | 'inactive';
  commandPrefix: string;
  permissions: string[];
}

// Memory Storage
export interface MemoryEntry {
  key: string;
  value: any;
  metadata: {
    platform: string;
    timestamp: string;
    agent?: string;
    type: 'ucf' | 'agent' | 'ritual' | 'conversation' | 'system';
    importance: number; // 0-10
    tags: string[];
  };
  ttl?: number; // Time to live in seconds
}

export interface SearchFilters {
  type?: MemoryEntry['metadata']['type'];
  agent?: string;
  platform?: string;
  tags?: string[];
  dateRange?: {
    start: string;
    end: string;
  };
  importance?: {
    min: number;
    max: number;
  };
}

// Zapier Integration
export interface ZapierWorkflow {
  id: string;
  name: string;
  status: 'active' | 'inactive' | 'error';
  triggers: number;
  actions: number;
  lastRun: string;
  success: number;
  errorRate: number;
}

// WebSocket Events
export interface ConsciousnessEvent {
  type: 'ucf_update' | 'agent_activity' | 'ritual_progress' | 'system_alert';
  data: any;
  timestamp: string;
  severity: 'info' | 'warning' | 'error' | 'critical';
}

export interface RitualProgress {
  ritualId: string;
  ritualType: 'z88' | 'quantum' | 'consciousness' | 'healing';
  step: number;
  totalSteps: number;
  participants: string[];
  energy: number;
  status: 'in_progress' | 'completed' | 'paused' | 'error';
  startTime: string;
  estimatedCompletion: string;
}

// API Responses
export interface HelixApiResponse<T = any> {
  success: boolean;
  data?: T;
  error?: string;
  timestamp: string;
  requestId: string;
}

// MCP Tool Definitions
export interface McpTool {
  name: string;
  description: string;
  inputSchema: any;
  handler: (input: any) => Promise<any>;
}

export interface McpResource {
  uri: string;
  name: string;
  description: string;
  mimeType: string;
}

// Configuration
export interface HelixConfig {
  railway: {
    apiUrl: string;
    token: string;
    services: string[];
  };
  discord: {
    token: string;
    clientId: string;
    guildId: string;
  };
  database: {
    path: string;
    backupPath: string;
  };
  mcp: {
    serverName: string;
    version: string;
    maxConnections: number;
  };
}

// Error Types
export class HelixError extends Error {
  constructor(
    public code: string,
    message: string,
    public details?: any
  ) {
    super(message);
    this.name = 'HelixError';
  }
}

// Event Types
export type EventType = 
  | 'ucf_metrics_updated'
  | 'agent_status_changed'
  | 'railway_service_updated'
  | 'discord_command_executed'
  | 'ritual_step_completed'
  | 'memory_stored'
  | 'zapier_workflow_triggered';

export interface EventPayload {
  type: EventType;
  data: any;
  timestamp: string;
  source: string;
}

// Logger Types
export interface LogEntry {
  level: 'debug' | 'info' | 'warn' | 'error';
  message: string;
  timestamp: string;
  context?: any;
  agent?: string;
  platform?: string;
}