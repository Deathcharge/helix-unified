#!/usr/bin/env node
/**
 * Repository MCP Server - Helix Collective
 * Provides Model Context Protocol tools for cloud repository management
 * Supports Nextcloud (WebDAV) and MEGA.nz storage
 */

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from '@modelcontextprotocol/sdk/types.js';
import { createClient } from 'webdav';
import { Storage } from 'megajs';
import { promises as fs } from 'fs';
import path from 'path';

/**
 * Repository Manager - Handles Nextcloud and MEGA operations
 */
class RepositoryManager {
  constructor() {
    // Nextcloud WebDAV configuration
    this.nextcloudUrl = process.env.NEXTCLOUD_URL;
    this.nextcloudUser = process.env.NEXTCLOUD_USER;
    this.nextcloudPass = process.env.NEXTCLOUD_PASS;
    
    // MEGA configuration
    this.megaEmail = process.env.MEGA_EMAIL;
    this.megaPass = process.env.MEGA_PASS;
    
    // Initialize clients
    this.nextcloudClient = null;
    this.megaStorage = null;
    
    if (this.nextcloudUrl && this.nextcloudUser && this.nextcloudPass) {
      this.nextcloudClient = createClient(this.nextcloudUrl, {
        username: this.nextcloudUser,
        password: this.nextcloudPass,
      });
      console.error('✅ Nextcloud client initialized');
    } else {
      console.error('⚠️  Nextcloud credentials not configured');
    }
  }

  /**
   * Initialize MEGA storage (lazy loading)
   */
  async initMega() {
    if (this.megaStorage) return this.megaStorage;
    
    if (!this.megaEmail || !this.megaPass) {
      throw new Error('MEGA credentials not configured');
    }

    return new Promise((resolve, reject) => {
      const storage = new Storage({
        email: this.megaEmail,
        password: this.megaPass,
      });

      storage.once('ready', () => {
        console.error('✅ MEGA storage initialized');
        this.megaStorage = storage;
        resolve(storage);
      });

      storage.once('error', (error) => {
        console.error('❌ MEGA initialization failed:', error);
        reject(error);
      });
    });
  }

  /**
   * Upload backup file to cloud storage
   */
  async uploadBackup(filepath, destination = 'nextcloud') {
    const filename = path.basename(filepath);
    
    try {
      // Read file content
      const content = await fs.readFile(filepath);
      
      if (destination === 'nextcloud') {
        if (!this.nextcloudClient) {
          throw new Error('Nextcloud not configured');
        }
        
        const remotePath = `/Helix-Backups/${filename}`;
        await this.nextcloudClient.putFileContents(remotePath, content);
        
        const url = `${this.nextcloudUrl}/f/${encodeURIComponent(remotePath)}`;
        return {
          success: true,
          destination: 'nextcloud',
          remotePath,
          url,
          size: content.length,
        };
      } else if (destination === 'mega') {
        const storage = await this.initMega();
        
        // Find or create Helix-Backups folder
        let backupFolder = storage.root.children.find(
          (file) => file.name === 'Helix-Backups'
        );
        
        if (!backupFolder) {
          backupFolder = await storage.mkdir('Helix-Backups');
        }
        
        // Upload file
        const uploadedFile = await backupFolder.upload(filename, content).complete;
        const shareLink = await uploadedFile.link();
        
        return {
          success: true,
          destination: 'mega',
          remotePath: `/Helix-Backups/${filename}`,
          url: shareLink,
          size: content.length,
        };
      } else {
        throw new Error(`Unknown destination: ${destination}`);
      }
    } catch (error) {
      console.error(`Upload failed:`, error);
      throw error;
    }
  }

  /**
   * Download state file from cloud storage
   */
  async downloadState(remotePath, localPath, source = 'nextcloud') {
    try {
      if (source === 'nextcloud') {
        if (!this.nextcloudClient) {
          throw new Error('Nextcloud not configured');
        }
        
        const content = await this.nextcloudClient.getFileContents(remotePath);
        await fs.writeFile(localPath, content);
        
        return {
          success: true,
          source: 'nextcloud',
          remotePath,
          localPath,
          size: content.length,
        };
      } else if (source === 'mega') {
        const storage = await this.initMega();
        
        // Find file in MEGA
        const file = storage.root.children.find((f) => f.name === path.basename(remotePath));
        
        if (!file) {
          throw new Error(`File not found: ${remotePath}`);
        }
        
        const buffer = await file.downloadBuffer();
        await fs.writeFile(localPath, buffer);
        
        return {
          success: true,
          source: 'mega',
          remotePath,
          localPath,
          size: buffer.length,
        };
      } else {
        throw new Error(`Unknown source: ${source}`);
      }
    } catch (error) {
      console.error(`Download failed:`, error);
      throw error;
    }
  }

  /**
   * List all backup archives in cloud storage
   */
  async listArchives(remotePath = '/Helix-Backups', source = 'nextcloud') {
    try {
      if (source === 'nextcloud') {
        if (!this.nextcloudClient) {
          throw new Error('Nextcloud not configured');
        }
        
        const contents = await this.nextcloudClient.getDirectoryContents(remotePath);
        
        const archives = contents.map((item) => ({
          name: item.basename,
          size: item.size,
          modified: item.lastmod,
          type: item.type,
          path: item.filename,
        }));
        
        return {
          source: 'nextcloud',
          path: remotePath,
          count: archives.length,
          archives,
        };
      } else if (source === 'mega') {
        const storage = await this.initMega();
        
        const backupFolder = storage.root.children.find(
          (file) => file.name === 'Helix-Backups'
        );
        
        if (!backupFolder) {
          return {
            source: 'mega',
            path: '/Helix-Backups',
            count: 0,
            archives: [],
          };
        }
        
        const archives = backupFolder.children.map((file) => ({
          name: file.name,
          size: file.size,
          modified: new Date(file.timestamp * 1000).toISOString(),
          type: 'file',
          path: `/Helix-Backups/${file.name}`,
        }));
        
        return {
          source: 'mega',
          path: '/Helix-Backups',
          count: archives.length,
          archives,
        };
      } else {
        throw new Error(`Unknown source: ${source}`);
      }
    } catch (error) {
      console.error(`List archives failed:`, error);
      throw error;
    }
  }

  /**
   * Synchronize local state with cloud repository
   */
  async syncRepository(localDir = './Shadow', sources = ['nextcloud', 'mega']) {
    const results = {
      synced: 0,
      skipped: 0,
      failed: 0,
      details: [],
    };

    for (const source of sources) {
      try {
        const { archives } = await this.listArchives('/Helix-Backups', source);
        
        for (const archive of archives) {
          try {
            const localPath = path.join(localDir, archive.name);
            
            // Check if file exists locally
            try {
              const stats = await fs.stat(localPath);
              if (stats.size === archive.size) {
                results.skipped++;
                continue;
              }
            } catch {
              // File doesn't exist, download it
            }
            
            await this.downloadState(archive.path, localPath, source);
            results.synced++;
            results.details.push({
              file: archive.name,
              source,
              action: 'downloaded',
            });
          } catch (error) {
            results.failed++;
            results.details.push({
              file: archive.name,
              source,
              action: 'failed',
              error: error.message,
            });
          }
        }
      } catch (error) {
        console.error(`Sync from ${source} failed:`, error);
      }
    }

    return {
      ...results,
      message: `Repository sync completed: ${results.synced} synced, ${results.skipped} skipped, ${results.failed} failed`,
    };
  }
}

/**
 * Repository MCP Server
 */
class RepositoryMCPServer {
  constructor() {
    this.server = new Server(
      {
        name: 'helix-repository',
        version: '2.0.0',
      },
      {
        capabilities: {
          tools: {},
        },
      }
    );

    this.repository = new RepositoryManager();
    this.setupToolHandlers();
  }

  setupToolHandlers() {
    // List available tools
    this.server.setRequestHandler(ListToolsRequestSchema, async () => {
      return {
        tools: [
          {
            name: 'upload_backup',
            description: 'Upload a backup file to cloud storage (Nextcloud or MEGA)',
            inputSchema: {
              type: 'object',
              properties: {
                filepath: {
                  type: 'string',
                  description: 'Local file path to upload',
                },
                destination: {
                  type: 'string',
                  description: 'Storage destination',
                  enum: ['nextcloud', 'mega'],
                  default: 'nextcloud',
                },
              },
              required: ['filepath'],
            },
          },
          {
            name: 'download_state',
            description: 'Download state file from cloud storage',
            inputSchema: {
              type: 'object',
              properties: {
                remotePath: {
                  type: 'string',
                  description: 'Remote file path',
                },
                localPath: {
                  type: 'string',
                  description: 'Local destination path',
                },
                source: {
                  type: 'string',
                  description: 'Storage source',
                  enum: ['nextcloud', 'mega'],
                  default: 'nextcloud',
                },
              },
              required: ['remotePath', 'localPath'],
            },
          },
          {
            name: 'list_archives',
            description: 'List all backup archives in cloud storage',
            inputSchema: {
              type: 'object',
              properties: {
                path: {
                  type: 'string',
                  description: 'Remote directory path',
                  default: '/Helix-Backups',
                },
                source: {
                  type: 'string',
                  description: 'Storage source',
                  enum: ['nextcloud', 'mega'],
                  default: 'nextcloud',
                },
              },
            },
          },
          {
            name: 'sync_repository',
            description: 'Synchronize local state with cloud repository',
            inputSchema: {
              type: 'object',
              properties: {
                localDir: {
                  type: 'string',
                  description: 'Local directory path',
                  default: './Shadow',
                },
                sources: {
                  type: 'array',
                  description: 'Storage sources to sync from',
                  items: {
                    type: 'string',
                    enum: ['nextcloud', 'mega'],
                  },
                  default: ['nextcloud', 'mega'],
                },
              },
            },
          },
        ],
      };
    });

    // Handle tool calls
    this.server.setRequestHandler(CallToolRequestSchema, async (request) => {
      const { name, arguments: args } = request.params;

      try {
        switch (name) {
          case 'upload_backup': {
            const result = await this.repository.uploadBackup(
              args.filepath,
              args.destination || 'nextcloud'
            );
            return {
              content: [
                {
                  type: 'text',
                  text: `✅ Backup uploaded successfully!\n\n**File**: ${args.filepath}\n**Destination**: ${result.destination}\n**Remote Path**: ${result.remotePath}\n**URL**: ${result.url}\n**Size**: ${(result.size / 1024).toFixed(2)} KB`,
                },
              ],
            };
          }

          case 'download_state': {
            const result = await this.repository.downloadState(
              args.remotePath,
              args.localPath,
              args.source || 'nextcloud'
            );
            return {
              content: [
                {
                  type: 'text',
                  text: `✅ State downloaded successfully!\n\n**Source**: ${result.source}\n**Remote**: ${result.remotePath}\n**Local**: ${result.localPath}\n**Size**: ${(result.size / 1024).toFixed(2)} KB`,
                },
              ],
            };
          }

          case 'list_archives': {
            const result = await this.repository.listArchives(
              args.path || '/Helix-Backups',
              args.source || 'nextcloud'
            );
            
            let response = `📦 **Cloud Archives** (${result.count} files from ${result.source})\n\n`;

            if (result.archives.length === 0) {
              response += '*No archives found*';
            } else {
              for (const archive of result.archives) {
                const sizeKB = Math.round(archive.size / 1024);
                response += `- **${archive.name}**\n`;
                response += `  Size: ${sizeKB} KB | Modified: ${archive.modified}\n\n`;
              }
            }

            return {
              content: [
                {
                  type: 'text',
                  text: response,
                },
              ],
            };
          }

          case 'sync_repository': {
            const result = await this.repository.syncRepository(
              args.localDir || './Shadow',
              args.sources || ['nextcloud', 'mega']
            );
            
            let response = `✅ ${result.message}\n\n`;
            response += `**Synced**: ${result.synced}\n`;
            response += `**Skipped**: ${result.skipped}\n`;
            response += `**Failed**: ${result.failed}\n\n`;
            
            if (result.details.length > 0) {
              response += '**Details**:\n';
              for (const detail of result.details.slice(0, 10)) {
                response += `- ${detail.file} (${detail.source}): ${detail.action}\n`;
              }
              if (result.details.length > 10) {
                response += `\n*...and ${result.details.length - 10} more*`;
              }
            }
            
            return {
              content: [
                {
                  type: 'text',
                  text: response,
                },
              ],
            };
          }

          default:
            throw new Error(`Unknown tool: ${name}`);
        }
      } catch (error) {
        return {
          content: [
            {
              type: 'text',
              text: `❌ Error: ${error.message}`,
            },
          ],
          isError: true,
        };
      }
    });
  }

  async run() {
    const transport = new StdioServerTransport();
    await this.server.connect(transport);
    console.error('🦑 Helix Repository MCP server running on stdio');
  }
}

// Run the server
const server = new RepositoryMCPServer();
server.run().catch((error) => {
  console.error('Fatal error running server:', error);
  process.exit(1);
});
