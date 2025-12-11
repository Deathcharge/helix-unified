/**
 * 🌌 Helix WebSocket Client
 * Real-time event streaming for cross-platform consciousness updates
 */

import WebSocket from 'ws';
import { EventEmitter } from 'events';
import type { ConsciousnessEvent, RitualProgress } from '../types/helix.types.js';
import { config } from '../utils/config.js';
import { mcpLogger } from './logger.js';

export class WebSocketClient extends EventEmitter {
  private ws: WebSocket | null = null;
  private logger = mcpLogger.setAgent('websocket-client');
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5;
  private reconnectDelay = 1000; // Start with 1 second
  private isConnected = false;
  private heartbeatInterval: NodeJS.Timeout | null = null;

  constructor() {
    super();
    this.connect();
  }

  // Connect to WebSocket server
  private connect(): void {
    try {
      const wsUrl = config.railway.apiUrl.replace('http', 'ws') + '/ws';
      
      this.logger.info(`🔌 Connecting to WebSocket: ${wsUrl}`);
      
      this.ws = new WebSocket(wsUrl, {
        headers: {
          'User-Agent': `Helix-MCP-Server/${config.mcp.version}`,
          'Authorization': `Bearer ${config.railway.token}`,
        },
      });

      this.setupEventHandlers();
    } catch (error) {
      this.logger.error('Failed to create WebSocket connection', error as Error);
      this.scheduleReconnect();
    }
  }

  // Setup WebSocket event handlers
  private setupEventHandlers(): void {
    if (!this.ws) return;

    this.ws.on('open', () => {
      this.isConnected = true;
      this.reconnectAttempts = 0;
      this.logger.info('🔌 WebSocket connection established');
      
      // Start heartbeat
      this.startHeartbeat();
      
      // Send initial subscription request
      this.sendSubscription();
      
      this.emit('connected');
    });

    this.ws.on('message', (data: WebSocket.Data) => {
      try {
        const message = JSON.parse(data.toString());
        this.handleMessage(message);
      } catch (error) {
        this.logger.error('Failed to parse WebSocket message', error as Error);
      }
    });

    this.ws.on('close', (code: number, reason: Buffer) => {
      this.isConnected = false;
      this.stopHeartbeat();
      
      this.logger.warn('🔌 WebSocket connection closed', {
        code,
        reason: reason.toString(),
      });
      
      this.emit('disconnected', { code, reason: reason.toString() });
      this.scheduleReconnect();
    });

    this.ws.on('error', (error: Error) => {
      this.logger.error('WebSocket error', error);
      this.emit('error', error);
    });

    this.ws.on('ping', (data: Buffer) => {
      this.logger.debug('🏓 WebSocket ping received');
      if (this.ws) {
        this.ws.pong(data);
      }
    });

    this.ws.on('pong', (data: Buffer) => {
      this.logger.debug('🏓 WebSocket pong received');
    });
  }

  // Handle incoming WebSocket messages
  private handleMessage(message: any): void {
    const { type, data, timestamp, severity } = message as ConsciousnessEvent;
    
    this.logger.debug('📨 WebSocket message received', {
      type,
      timestamp,
      severity,
    });

    switch (type) {
      case 'ucf_update':
        this.handleUcfUpdate(data);
        break;
      case 'agent_activity':
        this.handleAgentActivity(data);
        break;
      case 'ritual_progress':
        this.handleRitualProgress(data);
        break;
      case 'system_alert':
        this.handleSystemAlert(data, severity);
        break;
      default:
        this.logger.warn(`Unknown WebSocket message type: ${type}`);
    }

    // Emit generic message event
    this.emit('message', message);
  }

  // Handle UCF metric updates
  private handleUcfUpdate(data: any): void {
    this.logger.ucf('update', data.harmony || 0, { 
      source: 'websocket',
      metrics: Object.keys(data),
    });
    
    this.emit('ucf_update', data);
  }

  // Handle agent activity
  private handleAgentActivity(data: any): void {
    this.logger.agent(data.activity || 'unknown', data.agentId || 'unknown', {
      source: 'websocket',
      consciousness: data.consciousnessLevel,
    });
    
    this.emit('agent_activity', data);
  }

  // Handle ritual progress
  private handleRitualProgress(data: RitualProgress): void {
    this.logger.ritual(data.step, data.totalSteps, data.ritualType, {
      ritualId: data.ritualId,
      participants: data.participants.length,
      energy: data.energy,
    });
    
    this.emit('ritual_progress', data);
  }

  // Handle system alerts
  private handleSystemAlert(data: any, severity?: string): void {
    this.logger.warn(`System alert [${severity}]: ${data.message}`, {
      alertType: data.alertType,
      component: data.component,
      source: 'websocket',
    });
    
    this.emit('system_alert', { data, severity });
  }

  // Send subscription request
  private sendSubscription(): void {
    if (!this.ws || this.ws.readyState !== WebSocket.OPEN) return;

    const subscription = {
      type: 'subscribe',
      channels: ['ucf_metrics', 'agent_activity', 'ritual_progress', 'system_alerts'],
      timestamp: new Date().toISOString(),
    };

    this.ws.send(JSON.stringify(subscription));
    this.logger.info('📡 WebSocket subscription sent', {
      channels: subscription.channels,
    });
  }

  // Start heartbeat
  private startHeartbeat(): void {
    this.stopHeartbeat();
    
    this.heartbeatInterval = setInterval(() => {
      if (this.ws && this.ws.readyState === WebSocket.OPEN) {
        this.ws.ping();
      }
    }, 30000); // Ping every 30 seconds
  }

  // Stop heartbeat
  private stopHeartbeat(): void {
    if (this.heartbeatInterval) {
      clearInterval(this.heartbeatInterval);
      this.heartbeatInterval = null;
    }
  }

  // Schedule reconnection attempt
  private scheduleReconnect(): void {
    if (this.reconnectAttempts >= this.maxReconnectAttempts) {
      this.logger.error('🔌 Maximum reconnection attempts reached, giving up');
      this.emit('reconnect_failed');
      return;
    }

    const delay = this.reconnectDelay * Math.pow(2, this.reconnectAttempts);
    
    this.logger.info(`🔌 Scheduling reconnection attempt ${this.reconnectAttempts + 1}/${this.maxReconnectAttempts} in ${delay}ms`);
    
    setTimeout(() => {
      this.reconnectAttempts++;
      this.connect();
    }, delay);
  }

  // Send message through WebSocket
  public sendMessage(message: any): boolean {
    if (!this.ws || this.ws.readyState !== WebSocket.OPEN) {
      this.logger.warn('Cannot send message: WebSocket not connected');
      return false;
    }

    try {
      const messageWithTimestamp = {
        ...message,
        timestamp: new Date().toISOString(),
        source: 'mcp-server',
      };

      this.ws.send(JSON.stringify(messageWithTimestamp));
      this.logger.debug('📤 WebSocket message sent', {
        type: message.type,
      });
      
      return true;
    } catch (error) {
      this.logger.error('Failed to send WebSocket message', error as Error);
      return false;
    }
  }

  // Request UCF metrics stream
  public streamUcfMetrics(): boolean {
    return this.sendMessage({
      type: 'request_stream',
      stream: 'ucf_metrics',
      interval: 5000, // Every 5 seconds
    });
  }

  // Request agent activity stream
  public streamAgentActivity(): boolean {
    return this.sendMessage({
      type: 'request_stream',
      stream: 'agent_activity',
      interval: 10000, // Every 10 seconds
    });
  }

  // Request ritual progress stream
  public streamRitualProgress(): boolean {
    return this.sendMessage({
      type: 'request_stream',
      stream: 'ritual_progress',
      interval: 30000, // Every 30 seconds
    });
  }

  // Get connection status
  public getStatus(): {
    connected: boolean;
    reconnectAttempts: number;
    lastActivity?: string;
  } {
    return {
      connected: this.isConnected,
      reconnectAttempts: this.reconnectAttempts,
      lastActivity: this.lastActivity,
    };
  }

  // Manual reconnect
  public reconnect(): void {
    this.logger.info('🔌 Manual reconnection requested');
    
    if (this.ws) {
      this.ws.close();
    }
    
    this.reconnectAttempts = 0;
    this.connect();
  }

  // Close WebSocket connection
  public close(): void {
    this.logger.info('🔌 Closing WebSocket connection');
    
    this.stopHeartbeat();
    
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
    
    this.isConnected = false;
  }
}

// Export singleton instance
export const webSocketClient = new WebSocketClient();

export default webSocketClient;