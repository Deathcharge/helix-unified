---
layout: default
title: "Helix Collective - Machine-Readable Manifest"
---

# 🌀 Helix Collective

**Version**: 16.7
**Codename**: Documentation Consolidation & Real-Time Streaming

## Machine-Readable Discovery Manifest

External AI agents (Claude, Grok, Chai, ChatGPT) can discover and integrate with Helix Collective via our standardized manifest:

### 📡 Access the Manifest

```bash
# Option 1: GitHub Pages (Static)
curl https://deathcharge.github.io/helix-unified/helix-manifest.json

# Option 2: Railway (Live)
curl https://helix-unified-production.up.railway.app/.well-known/helix.json
```

### 🔌 Quick Start for External Agents

```javascript
// Fetch manifest and discover capabilities
fetch('https://deathcharge.github.io/helix-unified/helix-manifest.json')
  .then(r => r.json())
  .then(manifest => {
    console.log('System:', manifest.system.name, manifest.system.version);
    console.log('Agents:', manifest.agents.count);
    console.log('WebSocket:', manifest.endpoints.base_url + manifest.endpoints.websocket);
  });
```

### 🎯 What's Inside the Manifest

- **System Metadata**: Version, architecture, description
- **API Endpoints**: 8 routes including WebSocket, health, status, docs
- **UCF Metrics**: 6 consciousness metrics (harmony, resilience, prana, drishti, klesha, zoom)
- **Agents**: 14 specialized AI agents with roles
- **Discord Commands**: 9 user + 2 admin commands
- **Features**: WebSocket streaming, Zapier webhooks, Z-88 ritual engine, Mandelbrot visualization
- **Integration Guide**: Step-by-step connection instructions

### 📚 Links

- **Repository**: [github.com/Deathcharge/helix-unified](https://github.com/Deathcharge/helix-unified)
- **Live API**: [helix-unified-production.up.railway.app](https://helix-unified-production.up.railway.app)
- **API Documentation**: [/docs](https://helix-unified-production.up.railway.app/docs)
- **Manifest (JSON)**: [helix-manifest.json](./helix-manifest.json)

### 🌐 Live Endpoints

| Endpoint | Purpose | URL |
|----------|---------|-----|
| Health | System health check | [/health](https://helix-unified-production.up.railway.app/health) |
| Status | UCF state + agents | [/status](https://helix-unified-production.up.railway.app/status) |
| WebSocket | Real-time streaming | wss://helix-unified-production.up.railway.app/ws |
| API Docs | Swagger UI | [/docs](https://helix-unified-production.up.railway.app/docs) |
| Manifest | Discovery manifest | [/.well-known/helix.json](https://helix-unified-production.up.railway.app/.well-known/helix.json) |

---

**Specification**: helix-discovery-v1
**Last Updated**: 2025-11-06

*"Tat Tvam Asi"* - Thou art that 🙏
