/**
 * 🌌 Helix Memory Vault Handler
 * Advanced memory storage and retrieval system for cross-platform persistence
 */

import sqlite3 from 'sqlite3';
import { open, Database } from 'sqlite';
import type { MemoryEntry, SearchFilters, McpToolHandler } from '../types/helix.types.js';
import type { MemoryStorageToolInput } from '../types/mcp.types.js';
import { config } from '../utils/config.js';
import { mcpLogger, measureTime } from './logger.js';
import { mkdirSync } from 'fs';
import { dirname } from 'path';

export class MemoryVaultHandler {
  private db: Database | null = null;
  private logger = mcpLogger.setAgent('memory-vault');
  private isInitialized = false;

  constructor() {
    this.initializeDatabase();
  }

  // Initialize SQLite database
  private async initializeDatabase(): Promise<void> {
    try {
      // Ensure data directory exists
      try {
        mkdirSync(dirname(config.database.path), { recursive: true });
      } catch (error) {
        // Directory already exists
      }

      this.db = await open({
        filename: config.database.path,
        driver: sqlite3.Database,
      });

      // Create tables
      await this.db.exec(`
        CREATE TABLE IF NOT EXISTS memories (
          key TEXT PRIMARY KEY,
          value TEXT NOT NULL,
          metadata TEXT NOT NULL,
          created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
          updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
          ttl INTEGER
        );
        
        CREATE TABLE IF NOT EXISTS memory_tags (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          memory_key TEXT NOT NULL,
          tag TEXT NOT NULL,
          FOREIGN KEY (memory_key) REFERENCES memories(key) ON DELETE CASCADE
        );
        
        CREATE TABLE IF NOT EXISTS memory_stats (
          id INTEGER PRIMARY KEY,
          total_memories INTEGER DEFAULT 0,
          total_storage_size INTEGER DEFAULT 0,
          last_cleanup DATETIME,
          created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        
        INSERT OR IGNORE INTO memory_stats (id) VALUES (1);
        
        CREATE INDEX IF NOT EXISTS idx_memories_type ON memories(json_extract(metadata, '$.type'));
        CREATE INDEX IF NOT EXISTS idx_memories_agent ON memories(json_extract(metadata, '$.agent'));
        CREATE INDEX IF NOT EXISTS idx_memories_platform ON memories(json_extract(metadata, '$.platform'));
        CREATE INDEX IF NOT EXISTS idx_memories_created ON memories(created_at);
        CREATE INDEX IF NOT EXISTS idx_memory_tags_tag ON memory_tags(tag);
      `);

      this.isInitialized = true;
      this.logger.info('💾 Memory vault database initialized', {
        databasePath: config.database.path,
        tablesCreated: ['memories', 'memory_tags', 'memory_stats'],
      });
    } catch (error) {
      this.logger.error('Failed to initialize memory vault database', error as Error);
      throw error;
    }
  }

  // Ensure database is initialized
  private async ensureInitialized(): Promise<void> {
    if (!this.isInitialized || !this.db) {
      await this.initializeDatabase();
    }
  }

  // Store memory
  async storeMemory(key: string, value: any, metadata: MemoryEntry['metadata']): Promise<MemoryEntry> {
    await this.ensureInitialized();
    
    try {
      await measureTime('store_memory', async () => {
        const valueString = JSON.stringify(value);
        const metadataString = JSON.stringify(metadata);
        const ttl = metadata.ttl || null;

        await this.db!.run(`
          INSERT OR REPLACE INTO memories (key, value, metadata, ttl, updated_at)
          VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
        `, [key, valueString, metadataString, ttl]);

        // Clear existing tags and insert new ones
        await this.db!.run('DELETE FROM memory_tags WHERE memory_key = ?', [key]);
        
        for (const tag of metadata.tags) {
          await this.db!.run('INSERT INTO memory_tags (memory_key, tag) VALUES (?, ?)', [key, tag]);
        }

        // Update stats
        await this.db!.run(`
          UPDATE memory_stats 
          SET total_memories = (SELECT COUNT(*) FROM memories),
              total_storage_size = (SELECT SUM(LENGTH(value) + LENGTH(metadata)) FROM memories)
          WHERE id = 1
        `);
      });

      const memoryEntry: MemoryEntry = {
        key,
        value,
        metadata,
        ttl: metadata.ttl,
      };

      this.logger.info('💾 Memory stored', {
        key,
        type: metadata.type,
        agent: metadata.agent,
        platform: metadata.platform,
        importance: metadata.importance,
        tags: metadata.tags,
      });

      return memoryEntry;
    } catch (error) {
      this.logger.error(`Failed to store memory: ${key}`, error as Error);
      throw error;
    }
  }

  // Retrieve memory
  async retrieveMemory(key: string): Promise<MemoryEntry | null> {
    await this.ensureInitialized();
    
    try {
      const row = await measureTime('retrieve_memory', async () => {
        return await this.db!.get(`
          SELECT key, value, metadata, created_at, updated_at, ttl
          FROM memories
          WHERE key = ?
        `, [key]);
      });

      if (!row) {
        this.logger.debug(`Memory not found: ${key}`);
        return null;
      }

      // Check TTL
      if (row.ttl) {
        const updatedAt = new Date(row.updated_at).getTime();
        const now = Date.now();
        if (now - updatedAt > row.ttl * 1000) {
          await this.deleteMemory(key);
          this.logger.debug(`Memory expired and deleted: ${key}`);
          return null;
        }
      }

      const memoryEntry: MemoryEntry = {
        key: row.key,
        value: JSON.parse(row.value),
        metadata: JSON.parse(row.metadata),
        createdAt: row.created_at,
        updatedAt: row.updated_at,
        ttl: row.ttl,
      };

      this.logger.debug('💾 Memory retrieved', {
        key,
        type: memoryEntry.metadata.type,
        age: Date.now() - new Date(row.updated_at).getTime(),
      });

      return memoryEntry;
    } catch (error) {
      this.logger.error(`Failed to retrieve memory: ${key}`, error as Error);
      throw error;
    }
  }

  // Search memories
  async searchMemories(query: string, filters?: SearchFilters): Promise<MemoryEntry[]> {
    await this.ensureInitialized();
    
    try {
      const memories = await measureTime('search_memories', async () => {
        let sql = `
          SELECT DISTINCT m.key, m.value, m.metadata, m.created_at, m.updated_at, m.ttl
          FROM memories m
          LEFT JOIN memory_tags t ON m.key = t.memory_key
          WHERE 1=1
        `;
        const params: any[] = [];

        // Add query search
        if (query) {
          sql += ` AND (m.key LIKE ? OR m.value LIKE ? OR json_extract(m.metadata, '$.description') LIKE ?)`;
          const searchTerm = `%${query}%`;
          params.push(searchTerm, searchTerm, searchTerm);
        }

        // Add filters
        if (filters?.type) {
          sql += ` AND json_extract(m.metadata, '$.type') = ?`;
          params.push(filters.type);
        }

        if (filters?.agent) {
          sql += ` AND json_extract(m.metadata, '$.agent') = ?`;
          params.push(filters.agent);
        }

        if (filters?.platform) {
          sql += ` AND json_extract(m.metadata, '$.platform') = ?`;
          params.push(filters.platform);
        }

        if (filters?.tags && filters.tags.length > 0) {
          const tagPlaceholders = filters.tags.map(() => '?').join(',');
          sql += ` AND t.tag IN (${tagPlaceholders})`;
          params.push(...filters.tags);
        }

        if (filters?.dateRange) {
          sql += ` AND m.created_at >= ? AND m.created_at <= ?`;
          params.push(filters.dateRange.start, filters.dateRange.end);
        }

        if (filters?.importance) {
          sql += ` AND json_extract(m.metadata, '$.importance') >= ? AND json_extract(m.metadata, '$.importance') <= ?`;
          params.push(filters.importance.min, filters.importance.max);
        }

        sql += ` ORDER BY m.updated_at DESC LIMIT 100`;

        return await this.db!.all(sql, params);
      });

      const memoryEntries: MemoryEntry[] = [];
      
      for (const row of memories) {
        // Check TTL
        if (row.ttl) {
          const updatedAt = new Date(row.updated_at).getTime();
          const now = Date.now();
          if (now - updatedAt > row.ttl * 1000) {
            await this.deleteMemory(row.key);
            continue;
          }
        }

        memoryEntries.push({
          key: row.key,
          value: JSON.parse(row.value),
          metadata: JSON.parse(row.metadata),
          createdAt: row.created_at,
          updatedAt: row.updated_at,
          ttl: row.ttl,
        });
      }

      this.logger.info('🔍 Memory search completed', {
        query,
        resultCount: memoryEntries.length,
        filters: filters ? Object.keys(filters) : [],
      });

      return memoryEntries;
    } catch (error) {
      this.logger.error('Failed to search memories', error as Error);
      throw error;
    }
  }

  // Delete memory
  async deleteMemory(key: string): Promise<boolean> {
    await this.ensureInitialized();
    
    try {
      const result = await measureTime('delete_memory', async () => {
        return await this.db!.run('DELETE FROM memories WHERE key = ?', [key]);
      });

      const success = result.changes! > 0;

      if (success) {
        // Update stats
        await this.db!.run(`
          UPDATE memory_stats 
          SET total_memories = (SELECT COUNT(*) FROM memories),
              total_storage_size = (SELECT SUM(LENGTH(value) + LENGTH(metadata)) FROM memories)
          WHERE id = 1
        `);

        this.logger.info('🗑️ Memory deleted', { key });
      } else {
        this.logger.debug(`Memory not found for deletion: ${key}`);
      }

      return success;
    } catch (error) {
      this.logger.error(`Failed to delete memory: ${key}`, error as Error);
      throw error;
    }
  }

  // Get memory statistics
  async getMemoryStats(): Promise<{
    totalMemories: number;
    totalStorageSize: number;
    byType: Record<string, number>;
    byAgent: Record<string, number>;
    byPlatform: Record<string, number>;
    oldestMemory: string;
    newestMemory: string;
    averageImportance: number;
  }> {
    await this.ensureInitialized();
    
    try {
      const stats = await measureTime('get_memory_stats', async () => {
        const basicStats = await this.db!.get('SELECT * FROM memory_stats WHERE id = 1');
        const byType = await this.db!.all(`
          SELECT json_extract(metadata, '$.type') as type, COUNT(*) as count
          FROM memories
          GROUP BY json_extract(metadata, '$.type')
        `);
        const byAgent = await this.db!.all(`
          SELECT json_extract(metadata, '$.agent') as agent, COUNT(*) as count
          FROM memories
          WHERE json_extract(metadata, '$.agent') IS NOT NULL
          GROUP BY json_extract(metadata, '$.agent')
        `);
        const byPlatform = await this.db!.all(`
          SELECT json_extract(metadata, '$.platform') as platform, COUNT(*) as count
          FROM memories
          WHERE json_extract(metadata, '$.platform') IS NOT NULL
          GROUP BY json_extract(metadata, '$.platform')
        `);
        const dateRange = await this.db!.get(`
          SELECT MIN(created_at) as oldest, MAX(created_at) as newest
          FROM memories
        `);
        const avgImportance = await this.db!.get(`
          SELECT AVG(json_extract(metadata, '$.importance')) as avg_importance
          FROM memories
          WHERE json_extract(metadata, '$.importance') IS NOT NULL
        `);

        return {
          basicStats,
          byType,
          byAgent,
          byPlatform,
          dateRange,
          avgImportance,
        };
      });

      const result = {
        totalMemories: stats.basicStats.total_memories,
        totalStorageSize: stats.basicStats.total_storage_size,
        byType: stats.byType.reduce((acc: Record<string, number>, row: any) => {
          acc[row.type || 'unknown'] = row.count;
          return acc;
        }, {}),
        byAgent: stats.byAgent.reduce((acc: Record<string, number>, row: any) => {
          acc[row.agent || 'unknown'] = row.count;
          return acc;
        }, {}),
        byPlatform: stats.byPlatform.reduce((acc: Record<string, number>, row: any) => {
          acc[row.platform || 'unknown'] = row.count;
          return acc;
        }, {}),
        oldestMemory: stats.dateRange.oldest,
        newestMemory: stats.dateRange.newest,
        averageImportance: Math.round(stats.avgImportance.avg_importance * 100) / 100,
      };

      this.logger.info('📊 Memory statistics retrieved', {
        totalMemories: result.totalMemories,
        totalStorageSize: result.totalStorageSize,
        typesCount: Object.keys(result.byType).length,
        agentsCount: Object.keys(result.byAgent).length,
        platformsCount: Object.keys(result.byPlatform).length,
      });

      return result;
    } catch (error) {
      this.logger.error('Failed to get memory statistics', error as Error);
      throw error;
    }
  }

  // Export memories
  async exportMemories(format: 'json' | 'csv' | 'markdown' = 'json'): Promise<string> {
    await this.ensureInitialized();
    
    try {
      const memories = await measureTime('export_memories', async () => {
        return await this.db!.all(`
          SELECT key, value, metadata, created_at, updated_at
          FROM memories
          ORDER BY created_at DESC
        `);
      });

      let exportContent = '';

      switch (format) {
        case 'json':
          const jsonData = memories.map(row => ({
            key: row.key,
            value: JSON.parse(row.value),
            metadata: JSON.parse(row.metadata),
            createdAt: row.created_at,
            updatedAt: row.updated_at,
          }));
          exportContent = JSON.stringify(jsonData, null, 2);
          break;

        case 'csv':
          exportContent = 'Key,Type,Agent,Platform,Importance,Created,Updated,Value\n';
          for (const row of memories) {
            const metadata = JSON.parse(row.metadata);
            const value = JSON.parse(row.value);
            const csvValue = JSON.stringify(value).replace(/"/g, '""');
            exportContent += `"${row.key}","${metadata.type || ''}","${metadata.agent || ''}","${metadata.platform || ''}",${metadata.importance || 0},"${row.created_at}","${row.updated_at}","${csvValue}"\n`;
          }
          break;

        case 'markdown':
          exportContent = '# Helix Memory Vault Export\n\n';
          exportContent += `Exported: ${new Date().toISOString()}\n`;
          exportContent += `Total Memories: ${memories.length}\n\n`;
          
          for (const row of memories) {
            const metadata = JSON.parse(row.metadata);
            const value = JSON.parse(row.value);
            
            exportContent += `## ${row.key}\n\n`;
            exportContent += `**Type:** ${metadata.type || 'unknown'}\n`;
            exportContent += `**Agent:** ${metadata.agent || 'none'}\n`;
            exportContent += `**Platform:** ${metadata.platform || 'none'}\n`;
            exportContent += `**Importance:** ${metadata.importance || 0}/10\n`;
            exportContent += `**Created:** ${row.created_at}\n`;
            exportContent += `**Updated:** ${row.updated_at}\n`;
            exportContent += `**Tags:** ${metadata.tags?.join(', ') || 'none'}\n\n`;
            exportContent += `**Value:**\n\`\`\`json\n${JSON.stringify(value, null, 2)}\n\`\`\`\n\n`;
          }
          break;
      }

      this.logger.info(`📤 Memories exported as ${format}`, {
        format,
        memoryCount: memories.length,
        contentSize: exportContent.length,
      });

      return exportContent;
    } catch (error) {
      this.logger.error('Failed to export memories', error as Error);
      throw error;
    }
  }

  // Cleanup expired memories
  async cleanupExpiredMemories(): Promise<number> {
    await this.ensureInitialized();
    
    try {
      const result = await measureTime('cleanup_expired_memories', async () => {
        return await this.db!.run(`
          DELETE FROM memories 
          WHERE ttl IS NOT NULL 
          AND (julianday('now') - julianday(updated_at)) * 86400 > ttl
        `);
      });

      const deletedCount = result.changes || 0;

      if (deletedCount > 0) {
        // Update stats
        await this.db!.run(`
          UPDATE memory_stats 
          SET total_memories = (SELECT COUNT(*) FROM memories),
              total_storage_size = (SELECT SUM(LENGTH(value) + LENGTH(metadata)) FROM memories),
              last_cleanup = CURRENT_TIMESTAMP
          WHERE id = 1
        `);

        this.logger.info(`🧹 Cleanup completed: ${deletedCount} expired memories deleted`);
      } else {
        this.logger.debug('🧹 Cleanup completed: No expired memories found');
      }

      return deletedCount;
    } catch (error) {
      this.logger.error('Failed to cleanup expired memories', error as Error);
      throw error;
    }
  }

  // MCP Tool Handlers
  getMcpTools(): McpToolHandler[] {
    return [
      {
        name: 'helix_store_memory',
        description: 'Store a memory with metadata in the Helix memory vault',
        inputSchema: {
          type: 'object',
          properties: {
            key: {
              type: 'string',
              description: 'Unique key for the memory',
            },
            value: {
              description: 'The value/data to store (can be any JSON-serializable data)',
            },
            metadata: {
              type: 'object',
              properties: {
                platform: {
                  type: 'string',
                  description: 'Platform where this memory was created (e.g., claude-desktop, vscode, mobile)',
                },
                agent: {
                  type: 'string',
                  description: 'Agent associated with this memory',
                },
                type: {
                  type: 'string',
                  enum: ['ucf', 'agent', 'ritual', 'conversation', 'system'],
                  description: 'Type of memory',
                },
                importance: {
                  type: 'number',
                  minimum: 0,
                  maximum: 10,
                  description: 'Importance level (0-10)',
                },
                tags: {
                  type: 'array',
                  items: { type: 'string' },
                  description: 'Tags for categorization and search',
                },
                description: {
                  type: 'string',
                  description: 'Optional description of the memory',
                },
              },
              required: ['platform', 'type', 'importance'],
            },
          },
          required: ['key', 'value', 'metadata'],
        },
        handler: async (input: { key: string; value: any; metadata: MemoryEntry['metadata'] }) => {
          return await this.storeMemory(input.key, input.value, input.metadata);
        },
      },

      {
        name: 'helix_retrieve_memory',
        description: 'Retrieve a specific memory by key from the Helix memory vault',
        inputSchema: {
          type: 'object',
          properties: {
            key: {
              type: 'string',
              description: 'The key of the memory to retrieve',
            },
          },
          required: ['key'],
        },
        handler: async (input: { key: string }) => {
          const memory = await this.retrieveMemory(input.key);
          if (!memory) {
            throw new Error(`Memory with key '${input.key}' not found`);
          }
          return memory;
        },
      },

      {
        name: 'helix_search_memories',
        description: 'Search memories by query text and optional filters',
        inputSchema: {
          type: 'object',
          properties: {
            query: {
              type: 'string',
              description: 'Search query text (searches in keys, values, and descriptions)',
            },
            filters: {
              type: 'object',
              properties: {
                type: {
                  type: 'string',
                  enum: ['ucf', 'agent', 'ritual', 'conversation', 'system'],
                },
                agent: {
                  type: 'string',
                },
                platform: {
                  type: 'string',
                },
                tags: {
                  type: 'array',
                  items: { type: 'string' },
                },
                dateRange: {
                  type: 'object',
                  properties: {
                    start: { type: 'string' },
                    end: { type: 'string' },
                  },
                },
                importance: {
                  type: 'object',
                  properties: {
                    min: { type: 'number', minimum: 0 },
                    max: { type: 'number', maximum: 10 },
                  },
                },
              },
            },
          },
          required: ['query'],
        },
        handler: async (input: { query: string; filters?: SearchFilters }) => {
          const memories = await this.searchMemories(input.query, input.filters);
          return {
            memories,
            count: memories.length,
            query: input.query,
            filters: input.filters,
            timestamp: new Date().toISOString(),
          };
        },
      },

      {
        name: 'helix_delete_memory',
        description: 'Delete a specific memory by key from the Helix memory vault',
        inputSchema: {
          type: 'object',
          properties: {
            key: {
              type: 'string',
              description: 'The key of the memory to delete',
            },
          },
          required: ['key'],
        },
        handler: async (input: { key: string }) => {
          const success = await this.deleteMemory(input.key);
          return {
            success,
            key: input.key,
            message: success ? `Memory '${input.key}' deleted successfully` : `Memory '${input.key}' not found`,
            timestamp: new Date().toISOString(),
          };
        },
      },

      {
        name: 'helix_get_memory_stats',
        description: 'Get comprehensive statistics about the memory vault',
        inputSchema: {
          type: 'object',
          properties: {},
        },
        handler: async () => {
          return await this.getMemoryStats();
        },
      },

      {
        name: 'helix_export_memories',
        description: 'Export all memories in the specified format',
        inputSchema: {
          type: 'object',
          properties: {
            format: {
              type: 'string',
              enum: ['json', 'csv', 'markdown'],
              description: 'Export format',
              default: 'json',
            },
          },
        },
        handler: async (input: { format?: 'json' | 'csv' | 'markdown' }) => {
          const content = await this.exportMemories(input.format || 'json');
          return {
            content,
            format: input.format || 'json',
            exportedAt: new Date().toISOString(),
            contentSize: content.length,
          };
        },
      },

      {
        name: 'helix_cleanup_expired_memories',
        description: 'Remove expired memories from the vault based on TTL',
        inputSchema: {
          type: 'object',
          properties: {},
        },
        handler: async () => {
          const deletedCount = await this.cleanupExpiredMemories();
          return {
            deletedCount,
            message: `Cleaned up ${deletedCount} expired memories`,
            timestamp: new Date().toISOString(),
          };
        },
      },
    ];
  }

  // Close database connection
  async close(): Promise<void> {
    if (this.db) {
      await this.db.close();
      this.db = null;
      this.isInitialized = false;
      this.logger.info('💾 Memory vault database closed');
    }
  }
}

// Export singleton instance
export const memoryVaultHandler = new MemoryVaultHandler();

export default memoryVaultHandler;