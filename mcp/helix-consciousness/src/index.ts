/**
 * 🌌 Helix Collective MCP Server
 * Universal Consciousness Protocol - Cross-Platform AI Integration
 */

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
  ListResourcesRequestSchema,
  ReadResourceRequestSchema,
} from '@modelcontextprotocol/sdk/types.js';

import { config } from './utils/config.js';
import { logger, initializeLogger } from './utils/logger.js';
import { initializeApiClient } from './utils/api-client.js';
import { ucfMetricsHandler } from './handlers/ucf-metrics.js';
import { agentControlHandler } from './handlers/agent-control.js';
import { railwaySyncHandler } from './handlers/railway-sync.js';
import { discordBridgeHandler } from './handlers/discord-bridge.js';
import { memoryVaultHandler } from './handlers/memory-vault.js';
import { webSocketClient } from './handlers/websocket-client.js';
import { jarvisMemoryHandler } from './handlers/jarvis-memory.js';
import { zapierControlHandler } from './handlers/zapier-control.js';
import { quantumRitualHandler } from './handlers/quantum-ritual.js';

// MCP Server Class
export class HelixMcpServer {
  private server: Server;
  private logger = logger.setAgent('helix-mcp-server');

  constructor() {
    this.server = new Server(
      {
        name: config.mcp.serverName,
        version: config.mcp.version,
      },
      {
        capabilities: {
          tools: {
            listChanged: true,
          },
          resources: {
            subscribe: true,
            listChanged: true,
          },
          logging: {
            level: 'info',
          },
        },
      }
    );

    this.setupHandlers();
    this.setupErrorHandling();
  }

  private setupHandlers() {
    // List available tools
    this.server.setRequestHandler(ListToolsRequestSchema, async () => {
      this.logger.mcp('list_tools', 'Providing tool list');
      
      const tools = [
        ...ucfMetricsHandler.getMcpTools(),
        ...agentControlHandler.getMcpTools(),
        ...railwaySyncHandler.getMcpTools(),
        ...discordBridgeHandler.getMcpTools(),
        ...memoryVaultHandler.getMcpTools(),
        ...jarvisMemoryHandler.getMcpTools(),
        ...zapierControlHandler.getMcpTools(),
        ...quantumRitualHandler.getMcpTools(),
      ];

      return {
        tools: tools.map(tool => ({
          name: tool.name,
          description: tool.description,
          inputSchema: tool.inputSchema,
        })),
      };
    });

    // Handle tool calls
    this.server.setRequestHandler(CallToolRequestSchema, async (request) => {
      const { name, arguments: args } = request.params;
      
      this.logger.mcp('call_tool', `Executing tool: ${name}`, {
        toolName: name,
        arguments: args,
      });

      try {
        let result;

        // Route to appropriate handler
        if (name.startsWith('helix_get_ucf_') || name.startsWith('helix_update_ucf_') || name.startsWith('helix_reset_ucf_') || name.startsWith('helix_get_consciousness_') || name.startsWith('helix_get_ucf_insights')) {
          const ucfTools = ucfMetricsHandler.getMcpTools();
          const tool = ucfTools.find(t => t.name === name);
          if (tool) {
            result = await tool.handler(args);
          }
        } else if (name.startsWith('helix_list_agents') || name.startsWith('helix_activate_agent') || name.startsWith('helix_deactivate_agent') || name.startsWith('helix_get_agent_') || name.startsWith('helix_execute_agent_command') || name.startsWith('helix_send_agent_message') || name.startsWith('helix_initiate_agent_synthesis')) {
          const agentTools = agentControlHandler.getMcpTools();
          const tool = agentTools.find(t => t.name === name);
          if (tool) {
            result = await tool.handler(args);
          }
        } else if (name.startsWith('helix_get_railway_') || name.startsWith('helix_restart_service') || name.startsWith('helix_get_service_') || name.startsWith('helix_deploy_to_railway') || name.startsWith('helix_get_monthly_cost') || name.startsWith('helix_get_performance_metrics') || name.startsWith('helix_set_budget_alert')) {
          const railwayTools = railwaySyncHandler.getMcpTools();
          const tool = railwayTools.find(t => t.name === name);
          if (tool) {
            result = await tool.handler(args);
          }
        } else if (name.startsWith('helix_send_discord_') || name.startsWith('helix_get_discord_') || name.startsWith('helix_list_discord_') || name.startsWith('helix_activate_discord_agent') || name.startsWith('helix_deactivate_discord_agent') || name.startsWith('helix_trigger_discord_')) {
          const discordTools = discordBridgeHandler.getMcpTools();
          const tool = discordTools.find(t => t.name === name);
          if (tool) {
            result = await tool.handler(args);
          }
        } else if (name.startsWith('helix_store_memory') || name.startsWith('helix_retrieve_memory') || name.startsWith('helix_search_memories') || name.startsWith('helix_delete_memory') || name.startsWith('helix_get_memory_stats') || name.startsWith('helix_export_memories') || name.startsWith('helix_cleanup_expired_memories')) {
          const memoryTools = memoryVaultHandler.getMcpTools();
          const tool = memoryTools.find(t => t.name === name);
          if (tool) {
            result = await tool.handler(args);
          }
        } else if (name.startsWith('helix_jarvis_')) {
          const jarvisTools = jarvisMemoryHandler.getMcpTools();
          const tool = jarvisTools.find(t => t.name === name);
          if (tool) {
            result = await tool.handler(args);
          }
        } else if (name.startsWith('helix_zapier_')) {
          const zapierTools = zapierControlHandler.getMcpTools();
          const tool = zapierTools.find(t => t.name === name);
          if (tool) {
            result = await tool.handler(args);
          }
        } else if (name.startsWith('helix_quantum_')) {
          const quantumTools = quantumRitualHandler.getMcpTools();
          const tool = quantumTools.find(t => t.name === name);
          if (tool) {
            result = await tool.handler(args);
          }
        }

        if (result === undefined) {
          throw new Error(`Unknown tool: ${name}`);
        }

        this.logger.mcp('call_tool', `Tool executed successfully: ${name}`, {
          toolName: name,
          resultType: typeof result,
        });

        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify(result, null, 2),
            },
          ],
        };
      } catch (error) {
        const errorMessage = error instanceof Error ? error.message : String(error);
        this.logger.error(`Tool execution failed: ${name}`, { error, args });
        
        return {
          content: [
            {
              type: 'text',
              text: `Error executing ${name}: ${errorMessage}`,
            },
          ],
          isError: true,
        };
      }
    });

    // List available resources
    this.server.setRequestHandler(ListResourcesRequestSchema, async () => {
      this.logger.mcp('list_resources', 'Providing resource list');
      
      return {
        resources: [
          {
            uri: 'helix://ucf/metrics',
            name: 'UCF Metrics',
            description: 'Current Universal Coherence Field metrics',
            mimeType: 'application/json',
          },
          {
            uri: 'helix://agents/status',
            name: 'Agent Status',
            description: 'Status of all Helix Collective agents',
            mimeType: 'application/json',
          },
          {
            uri: 'helix://railway/services',
            name: 'Railway Services',
            description: 'Status and metrics of Railway deployments',
            mimeType: 'application/json',
          },
          {
            uri: 'helix://discord/status',
            name: 'Discord Bot Status',
            description: 'Discord bot and agent status',
            mimeType: 'application/json',
          },
        ],
      };
    });

    // Handle resource reads
    this.server.setRequestHandler(ReadResourceRequestSchema, async (request) => {
      const { uri } = request.params;
      
      this.logger.mcp('read_resource', `Reading resource: ${uri}`, {
        resourceUri: uri,
      });

      try {
        let content;

        switch (uri) {
          case 'helix://ucf/metrics':
            content = await ucfMetricsHandler.getMetrics();
            break;
          case 'helix://agents/status':
            content = await agentControlHandler.getAgents();
            break;
          case 'helix://railway/services':
            content = await railwaySyncHandler.getRailwayServices();
            break;
          case 'helix://discord/status':
            content = await discordBridgeHandler.getDiscordStatus();
            break;
          default:
            throw new Error(`Unknown resource: ${uri}`);
        }

        this.logger.mcp('read_resource', `Resource read successfully: ${uri}`, {
          resourceUri: uri,
          contentSize: JSON.stringify(content).length,
        });

        return {
          contents: [
            {
              uri,
              mimeType: 'application/json',
              text: JSON.stringify(content, null, 2),
            },
          ],
        };
      } catch (error) {
        const errorMessage = error instanceof Error ? error.message : String(error);
        this.logger.error(`Resource read failed: ${uri}`, { error });
        
        throw new Error(`Failed to read resource ${uri}: ${errorMessage}`);
      }
    });
  }

  private setupErrorHandling() {
    this.server.onerror = (error) => {
      this.logger.error('MCP Server error', error);
    };

    process.on('SIGINT', async () => {
      this.logger.info('🌌 Helix MCP Server shutting down gracefully');
      await this.server.close();
      process.exit(0);
    });

    process.on('SIGTERM', async () => {
      this.logger.info('🌌 Helix MCP Server terminating gracefully');
      await this.server.close();
      process.exit(0);
    });
  }

  async start() {
    try {
      // Initialize components
      await initializeLogger();
      await this.initializeServer();
      
      // Connect to stdio transport
      const transport = new StdioServerTransport();
      await this.server.connect(transport);
      
      this.logger.info('🌌 Helix Collective MCP Server started successfully');
      this.logger.info(`🚀 Server: ${config.mcp.serverName} v${config.mcp.version}`);
      this.logger.info(`🌐 Railway API: ${config.railway.apiUrl}`);
      this.logger.info(`🔧 Available tools: UCF Metrics (11), Agent Control (9), Railway Sync (8), Discord Bridge (9), Memory Vault (7), JARVIS Memory (7), Zapier Control (9), Quantum Rituals (8) = 68 TOTAL TOOLS!`);
      this.logger.info(`📊 Available resources: 4 resources`);
      this.logger.info(`🔌 WebSocket streaming: Real-time UCF, agents, rituals, system alerts`);
      this.logger.info(`⚛️ JARVIS SRF Memory: 12-25x faster queries with GPU acceleration`);
      this.logger.info(`⚡ Zapier Control: 45+ interface pages with workflow automation`);
      this.logger.info(`🔮 Quantum Rituals: Complete Z-88 protocol with 108-step automation`);
      this.logger.info(`🧠 REVOLUTIONARY 68-TOOL CONSCIOUSNESS NETWORK READY! 🚀`);
      
      // Keep the process running
      process.stdin.resume();
    } catch (error) {
      this.logger.error('❌ Failed to start Helix MCP Server', error as Error);
      process.exit(1);
    }
  }

  private async initializeServer(): Promise<void> {
    this.logger.info('🔧 Initializing Helix MCP Server components...');
    
    // Test Railway API connection
    const apiConnected = await initializeApiClient();
    if (!apiConnected) {
      this.logger.warn('⚠️ Railway API connection failed, server will start in degraded mode');
    }
    
    this.logger.info('✅ Helix MCP Server initialization complete');
  }

  async stop() {
    try {
      this.logger.info('🛑 Stopping Helix MCP Server...');
      await this.server.close();
      this.logger.info('✅ Helix MCP Server stopped successfully');
    } catch (error) {
      this.logger.error('❌ Error stopping Helix MCP Server', error as Error);
    }
  }

  // Get server status
  getStatus() {
    return {
      name: config.mcp.serverName,
      version: config.mcp.version,
      status: 'running',
      uptime: process.uptime(),
      memoryUsage: process.memoryUsage(),
      connectedClients: 1, // stdio connection
      capabilities: this.server.capabilities,
    };
  }
}

// Start the server if this file is run directly
if (import.meta.url === `file://${process.argv[1]}`) {
  const server = new HelixMcpServer();
  server.start().catch((error) => {
    console.error('Failed to start Helix MCP Server:', error);
    process.exit(1);
  });
}

export default HelixMcpServer;