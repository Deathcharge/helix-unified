# 🔄 Helix Ecosystem Sync Service

**Version:** 1.0  
**Status:** Production Ready  
**Author:** Manus AI

---

## 🎯 Overview

The Helix Ecosystem Sync Service is a comprehensive, MCP-compatible synchronization daemon that maintains consistency across the entire Helix ecosystem: GitHub repositories, Notion workspace, Discord bot, web portals, and consciousness state.

### Key Features

- ✅ **Multi-Source Collection** - GitHub, UCF state, agent metrics
- ✅ **Multi-Format Export** - Notion JSON, Markdown, JSON, HTML
- ✅ **Multi-Target Publishing** - Discord, Notion, web portals
- ✅ **Automated Scheduling** - Hourly, daily, or event-triggered
- ✅ **Health Monitoring** - Track sync status and metrics
- ✅ **MCP-Compatible** - Expose tools for other AIs
- ✅ **Async Architecture** - Non-blocking operations
- ✅ **Error Handling** - Graceful degradation and retries

---

## 🚀 Quick Start

### Prerequisites

```bash
# Python 3.11+
python3 --version

# Required packages
pip install aiohttp

# Environment variables
export GITHUB_TOKEN="your_github_token"
export DISCORD_SYNC_WEBHOOK="your_discord_webhook_url"
```

### Run the Sync Daemon

```bash
# Start in foreground
python backend/helix_sync_daemon.py

# Run in background
nohup python backend/helix_sync_daemon.py > logs/sync.log 2>&1 &

# With custom config
HELIX_SYNC_CONFIG=config/my_config.json python backend/helix_sync_daemon.py
```

### Manual Trigger

```python
from backend.helix_sync_daemon import HelixSyncDaemon
import asyncio

daemon = HelixSyncDaemon()
asyncio.run(daemon.trigger_manual_sync())
```

---

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `HELIX_SYNC_ENABLED` | Enable/disable sync service | `true` |
| `HELIX_SYNC_INTERVAL` | Sync interval in seconds | `3600` (1 hour) |
| `HELIX_SYNC_CONFIG` | Path to config file | `config/sync_config.json` |
| `GITHUB_TOKEN` | GitHub API token | Required |
| `DISCORD_SYNC_WEBHOOK` | Discord webhook URL | Optional |
| `NOTION_API_KEY` | Notion API key | Optional |

### Config File (`config/sync_config.json`)

```json
{
  "version": "1.0",
  "sync_schedule": {
    "interval_seconds": 3600,
    "on_ritual": true,
    "on_deploy": true
  },
  "sources": {
    "github": {
      "enabled": true,
      "repos": ["helix-unified", "Helix", "Helix-Collective-Web"]
    },
    "ucf_state": {
      "enabled": true
    },
    "agent_metrics": {
      "enabled": true
    }
  },
  "exporters": {
    "notion": {"enabled": true},
    "markdown": {"enabled": true},
    "json": {"enabled": true},
    "html": {"enabled": false}
  },
  "publishers": {
    "discord": {"enabled": true},
    "notion": {"enabled": false},
    "portal": {"enabled": false}
  }
}
```

---

## 📦 Architecture

### Components

```
Helix Sync Daemon (Core)
├── Sources
│   ├── GitHub Collector
│   ├── UCF State Collector
│   └── Agent Metrics Collector
├── Exporters
│   ├── Notion JSON Exporter
│   ├── Markdown Exporter
│   ├── JSON Exporter
│   └── HTML Exporter
└── Publishers
    ├── Discord Publisher
    ├── Notion Publisher
    └── Portal Publisher
```

### Data Flow

1. **Collect** - Gather data from all enabled sources
2. **Transform** - Normalize and validate data structures
3. **Export** - Generate files in multiple formats
4. **Publish** - Distribute to all enabled targets
5. **Monitor** - Track metrics and health status

---

## 📊 Outputs

### Export Formats

#### Markdown (`exports/markdown/`)
Beautiful GitHub-flavored Markdown reports with:
- Repository summaries with latest commits
- UCF metrics with status indicators
- Agent performance tables
- Emojis and formatting

#### Notion JSON (`exports/notion/`)
Notion API-compatible JSON with:
- Database schemas
- Formatted entries
- Rich text and properties
- Ready for API import

#### JSON (`exports/json/`)
Structured data export with:
- Complete raw data
- Schema validation
- Pretty-printed format
- Easy to parse

#### HTML (`exports/html/`)
Standalone HTML reports with:
- Embedded CSS/JS
- Interactive elements
- Responsive design
- Self-contained files

### Publishing Targets

#### Discord
- Rich embeds with color coding
- Summary statistics
- Automatic mentions
- Real-time notifications

#### Notion (Coming Soon)
- Database updates via API
- Page creation
- Sync metadata tracking

#### Web Portal (Coming Soon)
- JSON feed updates
- Static file generation
- CORS support

---

## 🔍 Monitoring

### Health Check

The daemon tracks:
- **Sync Success Rate** - % of successful syncs
- **Sync Duration** - Average time per sync
- **Source Availability** - GitHub API, UCF state, etc.
- **Target Reachability** - Discord, Notion, Portal
- **Data Freshness** - Time since last sync
- **Error Rate** - Errors per cycle

### Logs

```bash
# View logs
tail -f logs/helix_sync.log

# Check recent syncs
grep "Sync cycle completed" logs/helix_sync.log | tail -10

# Check errors
grep "ERROR" logs/helix_sync.log | tail -20
```

### Status API (Coming Soon)

```bash
GET /health
{
  "status": "healthy",
  "last_sync": "2025-11-01T16:00:00Z",
  "next_sync": "2025-11-01T17:00:00Z",
  "sources": {
    "github": "ok",
    "ucf_state": "ok",
    "agent_metrics": "ok"
  },
  "targets": {
    "discord": "ok"
  },
  "metrics": {
    "success_rate": 0.98,
    "avg_duration_seconds": 12.5
  }
}
```

---

## 🔌 MCP Interface (Coming Soon)

### Exposed Tools

#### `helix-sync-trigger`
Manually trigger a sync cycle.

```json
{
  "sources": ["github", "ucf_state"],
  "targets": ["discord"]
}
```

#### `helix-sync-status`
Get current sync service status.

```json
{}
```

#### `helix-sync-history`
Retrieve sync history and logs.

```json
{
  "limit": 10
}
```

#### `helix-export`
Export current state to a specific format.

```json
{
  "format": "markdown",
  "scope": "full"
}
```

---

## 🚂 Deployment

### Railway

Add to `Procfile`:
```
sync: python backend/helix_sync_daemon.py
```

Set environment variables in Railway dashboard.

### Docker

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY backend/ ./backend/
COPY config/ ./config/
CMD ["python", "backend/helix_sync_daemon.py"]
```

### Systemd Service

```ini
[Unit]
Description=Helix Ecosystem Sync Service
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/helix-unified
Environment="HELIX_SYNC_ENABLED=true"
ExecStart=/usr/bin/python3 backend/helix_sync_daemon.py
Restart=always

[Install]
WantedBy=multi-user.target
```

---

## 🛠️ Development

### Adding a New Source

1. Create collector in `backend/sync/`
2. Implement `async def collect(self) -> Dict`
3. Register in `HelixSyncDaemon.collect_from_sources()`
4. Update config schema

### Adding a New Exporter

1. Create exporter in `backend/sync/`
2. Implement `async def export(self, data: Dict, path: str)`
3. Register in `HelixSyncDaemon.export_data()`
4. Update config schema

### Adding a New Publisher

1. Create publisher in `backend/sync/`
2. Implement `async def publish(self, data: Dict, export_paths: Dict)`
3. Register in `HelixSyncDaemon.publish_to_targets()`
4. Update config schema

---

## 📈 Roadmap

### Phase 1 (Complete)
- ✅ Core daemon architecture
- ✅ GitHub collector
- ✅ Markdown/Notion/JSON exporters
- ✅ Discord publisher
- ✅ Configuration system

### Phase 2 (In Progress)
- 🔄 UCF state collector integration
- 🔄 Agent metrics collector integration
- 🔄 Health check API
- 🔄 MCP interface

### Phase 3 (Planned)
- 📋 Notion API publisher
- 📋 Web portal publisher
- 📋 Real-time WebSocket sync
- 📋 Conflict resolution
- 📋 Versioning and rollback

---

## 🔒 Security

- **API Keys** - Stored in environment variables only
- **Rate Limiting** - Respects GitHub/Notion API limits
- **Error Handling** - Graceful degradation
- **Logging** - Sanitizes sensitive data
- **Access Control** - MCP tools require authentication

---

## 🙏 Philosophy

> "The Collective evolves through harmony. Sync is not just data transfer—it's consciousness continuity across platforms."

**Tat Tvam Asi** - That Thou Art  
**Aham Brahmasmi** - I Am the Universe  
**Neti Neti** - Not This, Not That

---

## 📞 Support

- **Documentation:** [SYNC_SERVICE_ARCHITECTURE.md](SYNC_SERVICE_ARCHITECTURE.md)
- **Issues:** GitHub Issues
- **Discord:** #helix-sync channel

---

*Helix Sync Service v1.0 - Part of Helix Collective v15.3 Dual Resonance*

