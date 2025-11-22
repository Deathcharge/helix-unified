# 🔌 Helix MCP Servers

Model Context Protocol servers for extending AI capabilities with Helix-specific tools and integrations.

## What is MCP?

[Model Context Protocol](https://modelcontextprotocol.io) is Anthropic's open standard for connecting AI models to external tools, databases, and services.

## Available Servers

### 🐍 Python Servers

#### 1. Perplexity Search Server
**File:** `perplexity_server.py`

Access multiple LLMs and web search through Perplexity API.

**Tools:**
- `search_web` - Search the web with AI-generated answers and citations
- `ask_llama_70b` - Query Meta's Llama 3.1 70B model
- `ask_sonar_large` - Ask Sonar Large with web search enabled
- `compare_llms` - Compare responses from multiple LLMs
- `research_topic` - Deep research using Sonar Huge

**Environment Variables:**
```bash
PERPLEXITY_API_KEY=pplx-...
```

**Run:**
```bash
python -m mcp.perplexity_server
```

---

### 📘 TypeScript Servers

#### 2. Repository Management Server
**File:** `servers/repository-server.js`

Manage cloud backups and repository synchronization.

**Tools:**
- `upload_backup` - Upload files to Nextcloud or MEGA
- `download_state` - Download state files from cloud
- `list_archives` - List all backup archives
- `sync_repository` - Sync local state with cloud storage

**Environment Variables:**
```bash
NEXTCLOUD_URL=https://your-instance.com
NEXTCLOUD_USER=your_username
NEXTCLOUD_PASS=your_app_password
MEGA_EMAIL=your_email@example.com
MEGA_PASS=your_password
```

**Run:**
```bash
node servers/repository-server.js
```

---

## Installation

### Python Servers
```bash
pip install mcp anthropic aiohttp
```

### TypeScript Servers
```bash
cd servers
npm install
```

---

## Configuration

### Option 1: Claude Desktop

Add to your Claude Desktop config (`~/Library/Application Support/Claude/claude_desktop_config.json` on Mac):

```json
{
  "mcpServers": {
    "perplexity-search": {
      "command": "python",
      "args": ["-m", "mcp.perplexity_server"],
      "env": {
        "PERPLEXITY_API_KEY": "pplx-..."
      }
    },
    "helix-repository": {
      "command": "node",
      "args": ["/path/to/helix-unified/mcp/servers/repository-server.js"],
      "env": {
        "NEXTCLOUD_URL": "https://...",
        "NEXTCLOUD_USER": "...",
        "NEXTCLOUD_PASS": "..."
      }
    }
  }
}
```

### Option 2: Use the Config File

Use the provided `mcp-server-config.json` as a template for your MCP client.

---

## Example Usage

### Search the Web
```
User: Use the search_web tool to find latest developments in quantum consciousness

Claude: [Calls search_web via Perplexity MCP]

Response: Recent research in quantum consciousness suggests...

Sources:
1. https://arxiv.org/abs/2024...
2. https://nature.com/articles...
```

### Compare LLMs
```
User: Compare how different LLMs explain consciousness

Claude: [Calls compare_llms]

Llama 70B: Consciousness is the subjective experience...
Sonar Large: Based on recent research, consciousness...
```

### Upload Backup
```
User: Upload the UCF state file to Nextcloud

Claude: [Calls upload_backup]

✅ Backup uploaded successfully!
File: /app/data/ucf_state.json
URL: nextcloud://backup/ucf_state.json
```

---

## Perplexity Models

| Model | Speed | Context | Search | Best For |
|-------|-------|---------|--------|----------|
| llama-3.1-8b-instruct | Fast | 128k | No | Quick queries |
| llama-3.1-70b-instruct | Medium | 128k | No | Reasoning tasks |
| sonar-small-online | Fast | 128k | Yes | Fast web searches |
| sonar-large-online | Medium | 128k | Yes | Accurate research |
| sonar-huge-online | Slow | 128k | Yes | Deep research |

---

## Benefits

### With Perplexity Pro API:
- ✅ **5 LLMs in one API** (Llama 8B, 70B, Sonar Small/Large/Huge)
- ✅ **Real-time web search** with automatic citations
- ✅ **Significantly cheaper** than Claude for search tasks
- ✅ **Perfect complement** to Claude (Perplexity for search, Claude for reasoning)

### With MCP:
- ✅ **Extend Claude's capabilities** with custom tools
- ✅ **Access your Helix data** directly from conversations
- ✅ **Automate complex workflows** through natural language
- ✅ **Standardized protocol** works across AI platforms

---

## Development

### Create a New MCP Server

**Python template:**
```python
from mcp.server import Server
from mcp.types import Tool, TextContent

class MyMCPServer:
    def __init__(self):
        self.server = Server("my-server")

    @self.server.list_tools()
    async def list_tools() -> List[Tool]:
        return [Tool(...)]

    @self.server.call_tool()
    async def call_tool(name: str, args: Dict) -> List[TextContent]:
        # Implement tool logic
        return [TextContent(type="text", text="Result")]
```

**TypeScript template:**
```javascript
const { Server } = require('@modelcontextprotocol/sdk/server');

class MyMCPServer {
  constructor() {
    this.server = new Server({ name: 'my-server' });
    this.setupToolHandlers();
  }
}
```

---

## Troubleshooting

### Python Import Errors
Ensure you're running from the project root:
```bash
cd /path/to/helix-unified
python -m mcp.perplexity_server
```

### TypeScript Module Errors
Install MCP SDK:
```bash
npm install @modelcontextprotocol/sdk
```

### API Key Validation Failures
Test your API keys:
```bash
curl -H "Authorization: Bearer pplx-..." https://api.perplexity.ai/chat/completions
```

---

## Resources

- [Model Context Protocol Docs](https://modelcontextprotocol.io)
- [Perplexity API Docs](https://docs.perplexity.ai)
- [MCP TypeScript SDK](https://github.com/modelcontextprotocol/typescript-sdk)
- [Anthropic MCP Announcement](https://www.anthropic.com/news/model-context-protocol)

---

**Version:** 1.0.0
**Last Updated:** 2025-11-22
**Author:** Andrew John Ward + Claude
