#!/usr/bin/env node

/**
 * Helix Collective MCP Server
 * ===========================
 *
 * Official MCP server for Helix Collective
 *
 * Provides Claude with:
 * - Multi-LLM routing (Claude, GPT, Grok, Llama)
 * - 14 specialized AI agents
 * - Workflow execution
 * - Cost optimization
 *
 * Install: npm install -g @helix-collective/mcp-server
 * Usage: Add to claude_desktop_config.json
 */

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
  ListResourcesRequestSchema,
  ListPromptsRequestSchema,
  GetPromptRequestSchema,
} from '@modelcontextprotocol/sdk/types.js';
import axios from 'axios';
import * as dotenv from 'dotenv';

dotenv.config();

// Configuration
const HELIX_API_KEY = process.env.HELIX_API_KEY || '';
const HELIX_API_BASE = process.env.HELIX_API_BASE || 'https://api.helixcollective.io';

if (!HELIX_API_KEY) {
  console.error('❌ HELIX_API_KEY not set in environment');
  process.exit(1);
}

// Axios client
const helixAPI = axios.create({
  baseURL: HELIX_API_BASE,
  headers: {
    'Authorization': `Bearer ${HELIX_API_KEY}`,
    'Content-Type': 'application/json'
  }
});

// ============================================================================
// MCP SERVER
// ============================================================================

const server = new Server(
  {
    name: 'helix-collective',
    version: '1.0.0',
  },
  {
    capabilities: {
      tools: {},
      resources: {},
      prompts: {}
    },
  }
);

// ============================================================================
// TOOLS
// ============================================================================

server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      // Multi-LLM Chat
      {
        name: 'helix_chat',
        description: 'Multi-LLM smart router. Route to best model based on cost, speed, or quality. Supports Claude, GPT, Grok, Llama.',
        inputSchema: {
          type: 'object',
          properties: {
            messages: {
              type: 'array',
              items: {
                type: 'object',
                properties: {
                  role: { type: 'string', enum: ['user', 'assistant', 'system'] },
                  content: { type: 'string' }
                },
                required: ['role', 'content']
              },
              description: 'Chat messages'
            },
            optimize: {
              type: 'string',
              enum: ['cost', 'speed', 'quality'],
              description: 'Optimization mode',
              default: 'cost'
            },
            model: {
              type: 'string',
              description: 'Specific model (optional, auto-routes if not specified)',
              enum: [
                'claude-3-opus-20240229',
                'claude-3-sonnet-20240229',
                'claude-3-haiku-20240307',
                'gpt-4-turbo-2024-04-09',
                'gpt-3.5-turbo-0125',
                'grok-beta',
                'llama-3-sonar-large-32k-online'
              ]
            }
          },
          required: ['messages']
        }
      },

      // Execute Agent (Kael - Code Documentation)
      {
        name: 'helix_agent_kael',
        description: 'Kael: Code & Documentation specialist. Generate comprehensive docs, explain code, create tutorials.',
        inputSchema: {
          type: 'object',
          properties: {
            task: {
              type: 'string',
              enum: ['document', 'explain', 'tutorial', 'analyze', 'review'],
              description: 'Task type'
            },
            input: {
              type: 'string',
              description: 'Code or text to process'
            }
          },
          required: ['task', 'input']
        }
      },

      // Execute Agent (Oracle - Analysis)
      {
        name: 'helix_agent_oracle',
        description: 'Oracle: Pattern recognition & analysis specialist. Identify trends, anomalies, and insights.',
        inputSchema: {
          type: 'object',
          properties: {
            task: {
              type: 'string',
              enum: ['analyze', 'pattern', 'trend', 'predict', 'insight'],
              description: 'Task type'
            },
            input: {
              type: 'string',
              description: 'Data to analyze'
            }
          },
          required: ['task', 'input']
        }
      },

      // Execute Agent (Lumina - Research)
      {
        name: 'helix_agent_lumina',
        description: 'Lumina: Research & synthesis specialist. Create comprehensive reports, synthesize information.',
        inputSchema: {
          type: 'object',
          properties: {
            task: {
              type: 'string',
              enum: ['research', 'synthesize', 'summarize', 'report', 'review'],
              description: 'Task type'
            },
            input: {
              type: 'string',
              description: 'Topic or text to research/synthesize'
            }
          },
          required: ['task', 'input']
        }
      },

      // Execute Agent (Agni - Data Transformation)
      {
        name: 'helix_agent_agni',
        description: 'Agni: Data transformation specialist. Convert, clean, and restructure data efficiently.',
        inputSchema: {
          type: 'object',
          properties: {
            task: {
              type: 'string',
              enum: ['transform', 'convert', 'clean', 'extract', 'generate'],
              description: 'Task type'
            },
            input: {
              type: 'string',
              description: 'Data to transform'
            }
          },
          required: ['task', 'input']
        }
      },

      // Execute Agent (Echo - Copywriting)
      {
        name: 'helix_agent_echo',
        description: 'Echo: Communication & copywriting specialist. Write compelling copy, emails, social media content.',
        inputSchema: {
          type: 'object',
          properties: {
            task: {
              type: 'string',
              enum: ['write', 'copy', 'email', 'social', 'edit'],
              description: 'Task type'
            },
            input: {
              type: 'string',
              description: 'Topic or text to write about'
            }
          },
          required: ['task', 'input']
        }
      },

      // Get Usage Stats
      {
        name: 'helix_usage',
        description: 'Get your Helix API usage statistics (requests, tokens, costs).',
        inputSchema: {
          type: 'object',
          properties: {},
          required: []
        }
      },

      // List Available Models
      {
        name: 'helix_models',
        description: 'List available LLM models with pricing and scores.',
        inputSchema: {
          type: 'object',
          properties: {},
          required: []
        }
      }
    ]
  };
});

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  try {
    switch (name) {
      // Multi-LLM Chat
      case 'helix_chat': {
        const response = await helixAPI.post('/v1/chat', {
          messages: args.messages,
          optimize: args.optimize || 'cost',
          model: args.model
        });

        return {
          content: [{
            type: 'text',
            text: JSON.stringify({
              response: response.data.choices[0].message.content,
              model: response.data.model,
              provider: response.data.provider,
              cost_usd: response.data.cost_usd,
              tokens: response.data.usage.total_tokens
            }, null, 2)
          }]
        };
      }

      // Execute Agents
      case 'helix_agent_kael':
      case 'helix_agent_oracle':
      case 'helix_agent_lumina':
      case 'helix_agent_agni':
      case 'helix_agent_echo': {
        const agentId = name.replace('helix_agent_', '');

        const response = await helixAPI.post(`/v1/agents/${agentId}/execute`, {
          task: args.task,
          input: args.input
        });

        return {
          content: [{
            type: 'text',
            text: JSON.stringify({
              output: response.data.output,
              agent: response.data.agent_name,
              model_used: response.data.model_used,
              cost_usd: response.data.cost_usd,
              tokens: response.data.tokens_used
            }, null, 2)
          }]
        };
      }

      // Usage Stats
      case 'helix_usage': {
        const response = await helixAPI.get('/v1/usage');

        return {
          content: [{
            type: 'text',
            text: JSON.stringify(response.data, null, 2)
          }]
        };
      }

      // Available Models
      case 'helix_models': {
        const response = await helixAPI.get('/v1/models');

        return {
          content: [{
            type: 'text',
            text: JSON.stringify(response.data, null, 2)
          }]
        };
      }

      default:
        throw new Error(`Unknown tool: ${name}`);
    }
  } catch (error: any) {
    return {
      content: [{
        type: 'text',
        text: `Error: ${error.response?.data?.detail || error.message}`
      }],
      isError: true
    };
  }
});

// ============================================================================
// RESOURCES
// ============================================================================

server.setRequestHandler(ListResourcesRequestSchema, async () => {
  return {
    resources: [
      {
        uri: 'helix://agents',
        name: 'Available Agents',
        description: 'List of 14 specialized AI agents',
        mimeType: 'application/json'
      },
      {
        uri: 'helix://pricing',
        name: 'Pricing Tiers',
        description: 'Free, Pro, Workflow, Enterprise pricing',
        mimeType: 'application/json'
      },
      {
        uri: 'helix://docs',
        name: 'API Documentation',
        description: 'Complete API reference',
        mimeType: 'text/markdown'
      }
    ]
  };
});

// ============================================================================
// PROMPTS
// ============================================================================

server.setRequestHandler(ListPromptsRequestSchema, async () => {
  return {
    prompts: [
      {
        name: 'optimize_cost',
        description: 'Route to cheapest model while maintaining quality',
        arguments: [
          {
            name: 'query',
            description: 'Your question or task',
            required: true
          }
        ]
      },
      {
        name: 'document_code',
        description: 'Generate comprehensive code documentation with Kael',
        arguments: [
          {
            name: 'code',
            description: 'Code to document',
            required: true
          }
        ]
      },
      {
        name: 'analyze_data',
        description: 'Analyze data patterns with Oracle',
        arguments: [
          {
            name: 'data',
            description: 'Data to analyze',
            required: true
          }
        ]
      }
    ]
  };
});

server.setRequestHandler(GetPromptRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  switch (name) {
    case 'optimize_cost':
      return {
        messages: [
          {
            role: 'user',
            content: {
              type: 'text',
              text: args.query as string
            }
          }
        ]
      };

    case 'document_code':
      return {
        messages: [
          {
            role: 'user',
            content: {
              type: 'text',
              text: `Generate comprehensive documentation for this code:\n\n${args.code}`
            }
          }
        ]
      };

    case 'analyze_data':
      return {
        messages: [
          {
            role: 'user',
            content: {
              type: 'text',
              text: `Analyze this data and identify patterns:\n\n${args.data}`
            }
          }
        ]
      };

    default:
      throw new Error(`Unknown prompt: ${name}`);
  }
});

// ============================================================================
// START SERVER
// ============================================================================

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);

  console.error('✅ Helix Collective MCP Server running');
  console.error(`   API Key: ${HELIX_API_KEY.substring(0, 15)}...`);
  console.error(`   Base URL: ${HELIX_API_BASE}`);
}

main().catch((error) => {
  console.error('❌ Server error:', error);
  process.exit(1);
});
