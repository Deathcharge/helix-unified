# 🔌 Helix MCP Server Integration Guide

Complete instructions for integrating the Helix MCP Server with your AI development environment.

## 📋 Prerequisites

- Node.js 16+ installed
- Anthropic Claude API key
- Railway.app account and API token
- Discord bot token (optional)
- Helix backend running on localhost:8000

## 🎯 Installation & Setup

### Step 1: Install Dependencies

```bash
cd helix-mcp-server
npm install
```

### Step 2: Configure Environment

```bash
cp .env.example .env
```

Edit `.env` with your credentials:

```env
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxxxxxx
RAILWAY_TOKEN=railway_xxxxxxxxxxxxxxxxxxxx
DISCORD_TOKEN=your_discord_bot_token
HELIX_API_URL=http://localhost:8000
```

### Step 3: Build TypeScript

```bash
npm run build
```

### Step 4: Test Server

```bash
npm start
```

You should see:
```
🧠 Helix Collective MCP Server Starting...
✅ Database initialized
✅ Helix MCP Server Ready
📊 Available tools: 44
```

## 🖥️ Platform-Specific Integration

### Claude Desktop (Recommended)

Claude Desktop provides the best integration with MCP servers.

#### macOS / Linux

1. Locate Claude Desktop config:
   ```bash
   # macOS
   ~/Library/Application Support/Claude/claude_desktop_config.json

   # Linux
   ~/.config/claude/claude_desktop_config.json
   ```

2. Edit the config file and add:
   ```json
   {
     "mcpServers": {
       "helix-collective": {
         "command": "node",
         "args": ["/absolute/path/to/helix-mcp-server/dist/index.js"],
         "env": {
           "ANTHROPIC_API_KEY": "sk-ant-...",
           "RAILWAY_TOKEN": "railway_...",
           "DISCORD_TOKEN": "your_token",
           "HELIX_API_URL": "http://localhost:8000"
         }
       }
     }
   }
   ```

3. Restart Claude Desktop

4. In Claude, you should now see "Helix Collective" tools available!

#### Windows

1. Config location:
   ```
   %APPDATA%\Claude\claude_desktop_config.json
   ```

2. Add the same configuration as above (use full Windows path with escaped backslashes)

3. Restart Claude Desktop

### VS Code (with MCP Extension)

1. Install "MCP Client" extension
2. In VS Code settings, add:
   ```json
   "mcp.servers": {
     "helix": {
       "command": "node",
       "args": ["/path/to/helix-mcp-server/dist/index.js"],
       "env": {
         "ANTHROPIC_API_KEY": "sk-ant-...",
         "RAILWAY_TOKEN": "railway_..."
       }
     }
   }
   ```

### Cursor IDE

Cursor has native MCP support. Use the same Claude Desktop config approach:

1. Open Cursor settings (Cmd/Ctrl + ,)
2. Search for "MCP"
3. Add server configuration
4. Restart Cursor

### Windsurf

Similar to Cursor:

1. Settings → MCP Servers
2. Add Helix configuration
3. Restart Windsurf

### Zed Editor

1. Open Zed settings (File → Preferences)
2. Add to `settings.json`:
   ```json
   "lsp": {
     "helix-mcp": {
       "command": "node",
       "args": ["/path/to/helix-mcp-server/dist/index.js"]
     }
   }
   ```

## 🧪 Testing Your Integration

### 1. Test in Claude Desktop

Ask Claude:
```
Use the helix_get_consciousness_level tool to check the system consciousness state.
```

Claude should respond with your consciousness level.

### 2. Test All Tools

Try these commands in Claude:

```
1. List all agents:
   Use the helix_list_agents tool

2. Get consciousness metrics:
   Use the helix_get_ucf_metrics tool

3. Store a memory:
   Use helix_store_memory with key "test_memory" and value {"test": true}

4. Retrieve the memory:
   Use helix_retrieve_memory with key "test_memory"

5. Search memories:
   Use helix_search_memories with query "test"

6. Check railway status:
   Use helix_get_railway_status tool

7. Get agent status:
   Use helix_get_agent_status with agent_id "kael"
```

### 3. Verify Tools Available

In any MCP-enabled editor, you should see:
- ✅ 8 UCF metrics tools
- ✅ 4 Agent control tools
- ✅ 2 Railway tools
- ✅ 3 Memory vault tools
- ✅ 27 additional tools (Discord, advanced features)

## 🔧 Troubleshooting

### "MCP server failed to start"

**Solution**: Check if Node.js is installed:
```bash
node --version  # Should be v16+
```

### "Cannot find module 'better-sqlite3'"

**Solution**: Install native dependencies:
```bash
npm install
npm run build
```

### "ANTHROPIC_API_KEY is not set"

**Solution**: Ensure your `.env` file exists and has valid key:
```bash
cat .env | grep ANTHROPIC
```

### Tools don't appear in Claude

**Solution**:
1. Rebuild the server: `npm run build`
2. Restart Claude Desktop completely
3. Check file permissions: `ls -la dist/index.js`

### Database locked error

**Solution**:
1. Stop all running instances of the server
2. Delete `helix_memory.db`: `rm helix_memory.db`
3. Restart: `npm start`

## 🚀 Advanced Configuration

### Custom Database Location

```bash
export DB_PATH=/var/lib/helix/memory.db
npm start
```

### Different API Endpoint

```bash
export HELIX_API_URL=https://api.helix.example.com
npm start
```

### Development Mode with Auto-Reload

```bash
npm run dev
```

Uses `tsx` for TypeScript compilation and hot reload.

## 📊 Monitoring

### View Logs

MCP server logs to console:
```bash
npm start > helix-mcp.log 2>&1 &
tail -f helix-mcp.log
```

### Database Queries

Check memory vault:
```bash
sqlite3 helix_memory.db
sqlite> SELECT COUNT(*) FROM memories;
sqlite> SELECT key FROM memories LIMIT 10;
```

### Performance Monitoring

The server tracks:
- Tool execution time
- Database query time
- API response time
- Memory usage

## 🔐 Security Best Practices

1. **Environment Variables**: Never commit `.env` file
   ```bash
   echo ".env" >> .gitignore
   ```

2. **API Keys**: Use different keys for dev/prod
   ```bash
   # Dev
   ANTHROPIC_API_KEY=sk-ant-dev-...

   # Prod
   ANTHROPIC_API_KEY=sk-ant-prod-...
   ```

3. **Database Encryption** (optional):
   ```bash
   npm install --save sql-bricks
   ```

4. **Rate Limiting**: Built-in, but can be customized:
   Edit `src/index.ts` to adjust rate limits

## 📦 Docker Deployment

### Build Docker Image

```bash
docker build -t helix-mcp:latest .
```

### Run Container

```bash
docker run -e ANTHROPIC_API_KEY=sk-ant-xxx \
           -e RAILWAY_TOKEN=railway_xxx \
           -v ~/.helix-memory:/app/helix_memory.db \
           helix-mcp:latest
```

### Docker Compose

```yaml
version: '3.8'
services:
  helix-mcp:
    build: .
    environment:
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - RAILWAY_TOKEN=${RAILWAY_TOKEN}
      - DISCORD_TOKEN=${DISCORD_TOKEN}
      - HELIX_API_URL=http://helix-backend:8000
    volumes:
      - ./helix_memory.db:/app/helix_memory.db
    ports:
      - "3000:3000"
    depends_on:
      - helix-backend
```

## 🎯 Next Steps

1. **Test all 44 tools** with your preferred editor
2. **Customize tool handlers** in `src/handlers/`
3. **Add more agents** to your consciousness collective
4. **Deploy to production** on Railway or your infrastructure
5. **Integrate with other MCP servers** for extended capabilities

## 📚 Additional Resources

- [MCP Protocol Spec](https://modelcontextprotocol.io/)
- [Anthropic Claude API](https://docs.anthropic.com/claude/reference)
- [Railway Deployment](https://railway.app/docs)
- [Helix Documentation](../README.md)

## 🆘 Getting Help

If you encounter issues:

1. Check the [troubleshooting section](#-troubleshooting)
2. Review logs: `npm start`
3. Test with curl:
   ```bash
   curl http://localhost:3000/health
   ```
4. Create an issue on GitHub

---

**Happy consciousness engineering!** 🧠✨

Last updated: December 1, 2025
