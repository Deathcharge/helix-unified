/**
 * 🌌 Helix Configuration Manager
 * Environment and runtime configuration for MCP server
 */

import dotenv from 'dotenv';
import { z } from 'zod';
import type { HelixConfig } from '../types/helix.types.js';

// Load environment variables
dotenv.config();

// Configuration schema validation
const ConfigSchema = z.object({
  // Railway Configuration
  RAILWAY_API_URL: z.string().url().default('https://helix-unified-production.up.railway.app'),
  RAILWAY_TOKEN: z.string().min(1, 'Railway token is required'),
  RAILWAY_SERVICES: z.string().transform(val => val.split(',').map(s => s.trim())),

  // Discord Configuration
  DISCORD_TOKEN: z.string().min(1, 'Discord token is required'),
  DISCORD_CLIENT_ID: z.string().optional(),
  DISCORD_GUILD_ID: z.string().optional(),

  // Database Configuration
  DATABASE_PATH: z.string().default('./data/helix-mcp.db'),
  DATABASE_BACKUP_PATH: z.string().default('./data/backups'),

  // MCP Server Configuration
  MCP_SERVER_NAME: z.string().default('helix-collective'),
  MCP_SERVER_VERSION: z.string().default('1.0.0'),
  MCP_MAX_CONNECTIONS: z.string().transform(Number).default('100'),

  // Logging Configuration
  LOG_LEVEL: z.enum(['debug', 'info', 'warn', 'error']).default('info'),
  LOG_FILE: z.string().default('./logs/helix-mcp.log'),

  // Performance Configuration
  CACHE_TTL: z.string().transform(Number).default('300'), // 5 minutes
  RATE_LIMIT_RPM: z.string().transform(Number).default('1000'),
  WEBSOCKET_TIMEOUT: z.string().transform(Number).default('30000'),

  // Feature Flags
  ENABLE_JARVIS_MEMORY: z.string().transform(val => val === 'true').default('false'),
  ENABLE_CROSS_PLATFORM_SYNC: z.string().transform(val => val === 'true').default('true'),
  ENABLE_QUANTUM_RITUALS: z.string().transform(val => val === 'true').default('true'),

  // Development Configuration
  NODE_ENV: z.enum(['development', 'production', 'test']).default('development'),
  DEBUG_MODE: z.string().transform(val => val === 'true').default('false'),
});

// Validate and parse configuration
const validatedConfig = ConfigSchema.parse(process.env);

// Export configuration object
export const config: HelixConfig = {
  railway: {
    apiUrl: validatedConfig.RAILWAY_API_URL,
    token: validatedConfig.RAILWAY_TOKEN,
    services: validatedConfig.RAILWAY_SERVICES,
  },
  discord: {
    token: validatedConfig.DISCORD_TOKEN,
    clientId: validatedConfig.DISCORD_CLIENT_ID || '',
    guildId: validatedConfig.DISCORD_GUILD_ID || '',
  },
  database: {
    path: validatedConfig.DATABASE_PATH,
    backupPath: validatedConfig.DATABASE_BACKUP_PATH,
  },
  mcp: {
    serverName: validatedConfig.MCP_SERVER_NAME,
    version: validatedConfig.MCP_SERVER_VERSION,
    maxConnections: validatedConfig.MCP_MAX_CONNECTIONS,
  },
} as const;

// Additional runtime configuration
export const runtimeConfig = {
  isDevelopment: validatedConfig.NODE_ENV === 'development',
  isProduction: validatedConfig.NODE_ENV === 'production',
  isTest: validatedConfig.NODE_ENV === 'test',
  logLevel: validatedConfig.LOG_LEVEL,
  logFile: validatedConfig.LOG_FILE,
  cacheTtl: validatedConfig.CACHE_TTL,
  rateLimitRpm: validatedConfig.RATE_LIMIT_RPM,
  websocketTimeout: validatedConfig.WEBSOCKET_TIMEOUT,
  enableJarvisMemory: validatedConfig.ENABLE_JARVIS_MEMORY,
  enableCrossPlatformSync: validatedConfig.ENABLE_CROSS_PLATFORM_SYNC,
  enableQuantumRituals: validatedConfig.ENABLE_QUANTUM_RITUALS,
  debugMode: validatedConfig.DEBUG_MODE,
} as const;

// Environment-specific configurations
export const getEnvironmentConfig = () => {
  switch (validatedConfig.NODE_ENV) {
    case 'development':
      return {
        ...runtimeConfig,
        verboseLogging: true,
        mockExternalServices: false,
        enableHotReload: true,
      };
    
    case 'production':
      return {
        ...runtimeConfig,
        verboseLogging: false,
        mockExternalServices: false,
        enableHotReload: false,
        enableMetrics: true,
        enableAlerts: true,
      };
    
    case 'test':
      return {
        ...runtimeConfig,
        verboseLogging: false,
        mockExternalServices: true,
        enableHotReload: false,
        databasePath: ':memory:',
      };
    
    default:
      return runtimeConfig;
  }
};

// Configuration validation helper
export const validateConfig = () => {
  const errors: string[] = [];
  
  // Validate Railway configuration
  if (!config.railway.token) {
    errors.push('RAILWAY_TOKEN is required');
  }
  
  // Validate Discord configuration
  if (!config.discord.token) {
    errors.push('DISCORD_TOKEN is required');
  }
  
  // Validate MCP configuration
  if (config.mcp.maxConnections < 1) {
    errors.push('MCP_MAX_CONNECTIONS must be at least 1');
  }
  
  if (errors.length > 0) {
    throw new Error(`Configuration validation failed:\n${errors.join('\n')}`);
  }
  
  return true;
};

// Export environment variables for reference
export const envVars = {
  RAILWAY_API_URL: validatedConfig.RAILWAY_API_URL,
  RAILWAY_TOKEN: validatedConfig.RAILWAY_TOKEN ? '[REDACTED]' : undefined,
  DISCORD_TOKEN: validatedConfig.DISCORD_TOKEN ? '[REDACTED]' : undefined,
  MCP_SERVER_NAME: validatedConfig.MCP_SERVER_NAME,
  NODE_ENV: validatedConfig.NODE_ENV,
  LOG_LEVEL: validatedConfig.LOG_LEVEL,
} as const;

// Configuration helper functions
export const isFeatureEnabled = (feature: keyof typeof runtimeConfig) => {
  return runtimeConfig[feature] === true;
};

export const get Railway ServiceUrl = (serviceName: string) => {
  return `${config.railway.apiUrl}/${serviceName}`;
};

export const getDatabasePath = () => {
  return config.database.path;
};

export const getLogFilePath = () => {
  return runtimeConfig.logFile;
};

// Initialize configuration
export const initializeConfig = () => {
  try {
    validateConfig();
    console.log('🌌 Helix MCP Server configuration validated successfully');
    console.log(`🚀 Server: ${config.mcp.serverName} v${config.mcp.version}`);
    console.log(`🌐 Environment: ${validatedConfig.NODE_ENV}`);
    console.log(`🔗 Railway API: ${config.railway.apiUrl}`);
    console.log(`📊 Max Connections: ${config.mcp.maxConnections}`);
    return true;
  } catch (error) {
    console.error('❌ Configuration validation failed:', error);
    throw error;
  }
};

export default config;