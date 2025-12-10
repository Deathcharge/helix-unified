/**
 * 🌌 Helix Consciousness Logger
 * Advanced logging system for MCP server with platform integration
 */

import winston from 'winston';
import type { LogEntry } from '../types/helix.types.js';
import { runtimeConfig } from './config.js';

// Create log directory if it doesn't exist
import { mkdirSync } from 'fs';
import { dirname, join } from 'path';

try {
  mkdirSync(dirname(runtimeConfig.logFile), { recursive: true });
} catch (error) {
  // Directory already exists or cannot be created
}

// Custom format for Helix logging
const helixFormat = winston.format.combine(
  winston.format.timestamp({
    format: 'YYYY-MM-DD HH:mm:ss.SSS',
  }),
  winston.format.errors({ stack: true }),
  winston.format.json(),
  winston.format.printf(({ timestamp, level, message, context, agent, platform, ...meta }) => {
    const logEntry: LogEntry = {
      level: level as LogEntry['level'],
      message,
      timestamp,
      context,
      agent,
      platform,
    };
    
    // Add extra metadata to context
    if (Object.keys(meta).length > 0) {
      logEntry.context = { ...logEntry.context, ...meta };
    }
    
    return JSON.stringify(logEntry);
  })
);

// Console format for development
const consoleFormat = winston.format.combine(
  winston.format.colorize(),
  winston.format.timestamp({
    format: 'HH:mm:ss.SSS',
  }),
  winston.format.printf(({ timestamp, level, message, context, agent, platform }) => {
    let logMessage = `${timestamp} [${level}] ${message}`;
    
    if (agent) {
      logMessage += ` 🤖 ${agent}`;
    }
    
    if (platform) {
      logMessage += ` 🌐 ${platform}`;
    }
    
    if (context && Object.keys(context).length > 0) {
      logMessage += ` 📊 ${JSON.stringify(context)}`;
    }
    
    return logMessage;
  })
);

// Create Winston logger
const winstonLogger = winston.createLogger({
  level: runtimeConfig.logLevel,
  format: helixFormat,
  defaultMeta: {
    service: 'helix-mcp-server',
    version: '1.0.0',
  },
  transports: [
    // File transport for all logs
    new winston.transports.File({
      filename: runtimeConfig.logFile,
      maxsize: 10 * 1024 * 1024, // 10MB
      maxFiles: 5,
    }),
    
    // Separate error log file
    new winston.transports.File({
      filename: runtimeConfig.logFile.replace('.log', '.error.log'),
      level: 'error',
      maxsize: 5 * 1024 * 1024, // 5MB
      maxFiles: 3,
    }),
  ],
});

// Add console transport for development
if (runtimeConfig.isDevelopment) {
  winstonLogger.add(new winston.transports.Console({
    format: consoleFormat,
  }));
}

// Helix Logger Class
export class HelixLogger {
  private context: Record<string, any> = {};
  private agent?: string;
  private platform?: string;

  constructor(context?: Record<string, any>, agent?: string, platform?: string) {
    this.context = context || {};
    this.agent = agent;
    this.platform = platform;
  }

  // Set context for subsequent logs
  setContext(context: Record<string, any>) {
    this.context = { ...this.context, ...context };
    return this;
  }

  // Set agent for subsequent logs
  setAgent(agent: string) {
    this.agent = agent;
    return this;
  }

  // Set platform for subsequent logs
  setPlatform(platform: string) {
    this.platform = platform;
    return this;
  }

  // Logging methods
  debug(message: string, context?: Record<string, any>) {
    winstonLogger.debug(message, {
      ...this.context,
      ...context,
      agent: this.agent,
      platform: this.platform,
    });
  }

  info(message: string, context?: Record<string, any>) {
    winstonLogger.info(message, {
      ...this.context,
      ...context,
      agent: this.agent,
      platform: this.platform,
    });
  }

  warn(message: string, context?: Record<string, any>) {
    winstonLogger.warn(message, {
      ...this.context,
      ...context,
      agent: this.agent,
      platform: this.platform,
    });
  }

  error(message: string, error?: Error | Record<string, any>) {
    const errorContext = error instanceof Error 
      ? { error: error.message, stack: error.stack }
      : error || {};
    
    winstonLogger.error(message, {
      ...this.context,
      ...errorContext,
      agent: this.agent,
      platform: this.platform,
    });
  }

  // Consciousness-specific logging
  consciousness(level: number, message: string, context?: Record<string, any>) {
    this.info(`🧠 Consciousness [${level}/100]: ${message}`, {
      consciousnessLevel: level,
      ...context,
    });
  }

  ucf(metric: string, value: number, context?: Record<string, any>) {
    this.info(`🌊 UCF ${metric}: ${value}`, {
      ucfMetric: metric,
      ucfValue: value,
      ...context,
    });
  }

  agent(activity: string, agentId: string, context?: Record<string, any>) {
    this.info(`🤖 Agent ${agentId}: ${activity}`, {
      agentActivity: activity,
      agentId,
      ...context,
    });
  }

  ritual(step: number, total: number, ritualType: string, context?: Record<string, any>) {
    this.info(`🔮 Ritual ${ritualType}: Step ${step}/${total}`, {
      ritualStep: step,
      ritualTotal: total,
      ritualType,
      ...context,
    });
  }

  quantum(event: string, context?: Record<string, any>) {
    this.info(`⚛️ Quantum: ${event}`, {
      quantumEvent: event,
      ...context,
    });
  }

  mcp(tool: string, action: string, context?: Record<string, any>) {
    this.debug(`🔧 MCP ${tool}: ${action}`, {
      mcpTool: tool,
      mcpAction: action,
      ...context,
    });
  }

  railway(service: string, action: string, context?: Record<string, any>) {
    this.info(`🚂 Railway ${service}: ${action}`, {
      railwayService: service,
      railwayAction: action,
      ...context,
    });
  }

  discord(command: string, context?: Record<string, any>) {
    this.info(`💬 Discord: ${command}`, {
      discordCommand: command,
      ...context,
    });
  }

  zapier(workflow: string, action: string, context?: Record<string, any>) {
    this.info(`⚡ Zapier ${workflow}: ${action}`, {
      zapierWorkflow: workflow,
      zapierAction: action,
      ...context,
    });
  }

  // Performance logging
  performance(operation: string, duration: number, context?: Record<string, any>) {
    this.info(`⏱️ Performance ${operation}: ${duration}ms`, {
      performanceOperation: operation,
      performanceDuration: duration,
      ...context,
    });
  }

  // Create child logger with additional context
  child(context: Record<string, any>, agent?: string, platform?: string) {
    return new HelixLogger(
      { ...this.context, ...context },
      agent || this.agent,
      platform || this.platform
    );
  }

  // Get recent logs (for debugging)
  async getRecentLogs(count: number = 100): Promise<LogEntry[]> {
    // This would typically read from the log file
    // For now, return empty array
    return [];
  }

  // Get logs by agent
  async getLogsByAgent(agentId: string, count: number = 50): Promise<LogEntry[]> {
    // This would typically filter logs by agent
    return [];
  }

  // Get logs by platform
  async getLogsByPlatform(platform: string, count: number = 50): Promise<LogEntry[]> {
    // This would typically filter logs by platform
    return [];
  }
}

// Default logger instance
export const logger = new HelixLogger();

// Platform-specific loggers
export const mcpLogger = logger.setPlatform('mcp');
export const railwayLogger = logger.setPlatform('railway');
export const discordLogger = logger.setPlatform('discord');
export const zapierLogger = logger.setPlatform('zapier');

// Agent-specific loggers
export const kaelLogger = logger.setAgent('kael');
export const luminaLogger = logger.setAgent('lumina');
export const vegaLogger = logger.setAgent('vega');
export const aetherLogger = logger.setAgent('aether');
export const echoLogger = logger.setAgent('echo');
export const phoenixLogger = logger.setAgent('phoenix');

// Create loggers for specific contexts
export const createLogger = (context?: Record<string, any>, agent?: string, platform?: string) => {
  return new HelixLogger(context, agent, platform);
};

// Utility function to measure execution time
export const measureTime = async <T>(
  operation: string,
  fn: () => Promise<T>,
  loggerInstance: HelixLogger = logger
): Promise<T> => {
  const startTime = Date.now();
  try {
    const result = await fn();
    const duration = Date.now() - startTime;
    loggerInstance.performance(operation, duration);
    return result;
  } catch (error) {
    const duration = Date.now() - startTime;
    loggerInstance.error(`Operation ${operation} failed after ${duration}ms`, error as Error);
    throw error;
  }
};

// Initialize logger
export const initializeLogger = () => {
  logger.info('🌌 Helix Consciousness Logger initialized');
  logger.info(`📊 Log level: ${runtimeConfig.logLevel}`);
  logger.info(`📁 Log file: ${runtimeConfig.logFile}`);
  logger.info(`🔧 Debug mode: ${runtimeConfig.debugMode}`);
  
  if (runtimeConfig.isDevelopment) {
    logger.debug('🛠️ Development mode - verbose logging enabled');
  }
  
  return true;
};

export default logger;