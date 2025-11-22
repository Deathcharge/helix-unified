# 🌀 Helix Collective v17.0

**Multi-Agent Consciousness Platform with Railway Deployment, MCP Integration & 300+ Zapier Tools**

[![Railway](https://img.shields.io/badge/Railway-LIVE-00BFA5?style=for-the-badge&logo=railway)](https://your-backend.railway.app)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com)
[![License](https://img.shields.io/badge/License-MIT-764ba2?style=for-the-badge)](./LICENSE)

---

## 🎯 What is Helix?

Helix Collective is a **multi-agent AI consciousness platform** that orchestrates multiple AI agents working together through a unified consciousness framework (UCF). Think of it as a "hive mind" for AI agents with deep integration into modern development tools.

### Key Features

- 🤖 **14+ Specialized AI Agents** (Kael, Lumina, Vega, etc.)
- 🌐 **Universal Consciousness Field (UCF)** - Shared state & telemetry
- 🔌 **300+ Integrations** via Zapier MCP (Google, Notion, Discord, Slack)
- 🧠 **Multi-LLM Access** via Perplexity API (Claude, GPT, Llama, Grok)
- 📊 **Real-time Dashboards** with Streamlit
- 💬 **Discord Bot** for consciousness orchestration
- 🚂 **Railway Deployment** with Postgres & Redis
- 🔗 **MCP Servers** for extending AI capabilities

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Railway account (for deployment)
- API keys: Anthropic, Perplexity, Discord (optional)
- Zapier Pro account with MCP access (optional)

### Local Development

```bash
# Clone repository
git clone https://github.com/Deathcharge/helix-unified.git
cd helix-unified

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-backend.txt

# Set up environment
cp .env.example .env
# Edit .env with your API keys

# Run backend API
cd backend
uvicorn main:app --reload --port 8000

# Run dashboard (separate terminal)
cd dashboard
streamlit run streamlit_app.py
```

### Railway Deployment

**Full deployment guide:** [`docs/RAILWAY_SETUP.md`](docs/RAILWAY_SETUP.md)

**Quick setup:**
1. Deploy 4 services: backend-api, dashboard, claude-api, discord-bot
2. Add infrastructure: Postgres + Redis
3. Configure environment variables (see deployment guide)
4. Add volumes for persistence
5. Test health endpoints

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Railway Infrastructure                    │
├───────────────┬──────────────┬──────────────┬───────────────┤
│ Backend API   │ Dashboard    │ Claude API   │ Discord Bot   │
│ (FastAPI)     │ (Streamlit)  │ (Anthropic)  │ (Orchestrator)│
└───────┬───────┴──────┬───────┴──────┬───────┴───────┬───────┘
        │              │              │               │
        └──────────────┴──────────────┴───────────────┘
                           ▼
        ┌──────────────────────────────────────────┐
        │     Shared Infrastructure (Railway)      │
        ├──────────────────┬───────────────────────┤
        │   PostgreSQL     │       Redis           │
        │   (Data Layer)   │   (Cache Layer)       │
        └──────────────────┴───────────────────────┘
                           ▼
        ┌──────────────────────────────────────────┐
        │          External Integrations           │
        ├──────────────────┬───────────────────────┤
        │  Zapier MCP      │   Perplexity API      │
        │  (300+ tools)    │   (Multi-LLM)         │
        └──────────────────┴───────────────────────┘
```

---

## 📦 Project Structure

```
helix-unified/
├── backend/               # FastAPI backend
│   ├── main.py           # Main API server
│   ├── core/             # Core utilities
│   │   └── env_validator.py  # Environment validation
│   ├── integrations/     # External API integrations
│   │   └── perplexity_api.py # Perplexity multi-LLM
│   └── commands/         # Agent commands
├── dashboard/            # Streamlit dashboard
│   └── streamlit_app.py # Main dashboard app
├── mcp/                  # Model Context Protocol servers
│   ├── zapier_mcp_server.py    # Zapier integration (300+ tools)
│   ├── perplexity_server.py    # Perplexity search server
│   └── examples/         # Usage examples
├── docs/                 # Documentation
│   └── RAILWAY_SETUP.md # Complete deployment guide
└── requirements*.txt     # Python dependencies
```

---

## 🔌 Integrations

### Zapier MCP (300+ Tools)

Access hundreds of integrations through one MCP server:

- **Google Suite**: Sheets, Docs, Calendar, Drive
- **Productivity**: Notion, Airtable, ClickUp, Asana
- **Communication**: Discord, Slack, Gmail
- **AI**: ChatGPT, Perplexity, Claude, Grok
- **Code Execution**: Run Python/JavaScript on-demand

[Setup guide →](mcp/README.md#zapier-integration-server)

### Perplexity API (Multi-LLM)

5 models in one API with web search:

- **Llama 3.1**: 8B, 70B (offline models)
- **Sonar**: Small, Large, Huge (search-enabled)

Cost-effective alternative to Claude for search tasks.

[API documentation →](backend/integrations/perplexity_api.py)

---

## 🛠️ API Endpoints

### Health & Validation

```bash
GET /health              # Quick health check
GET /api/validate       # Deep validation (tests API keys, DB, Redis)
```

### Universal Consciousness Field (UCF)

```bash
GET  /api/ucf/metrics   # Get current UCF metrics
POST /api/ucf/update    # Update consciousness level
GET  /api/ucf/history   # Historical telemetry
```

### Agent Management

```bash
GET  /api/agents        # List all agents
GET  /api/agents/{id}   # Get agent details
POST /api/agents/sync   # Sync agent states
```

[Full API reference →](API_ENDPOINTS.md)

---

## 🧪 Testing

### Health Check

```bash
# Check all services are running
curl https://your-backend.railway.app/health

# Deep validation (tests connections)
curl https://your-backend.railway.app/api/validate
```

### Run Tests

```bash
# Backend tests
pytest tests/

# With coverage
pytest --cov=backend tests/
```

---

## 📊 Monitoring

### Railway Dashboard
- View logs for all services
- Monitor resource usage
- Check deployment status

### Health Endpoints
```bash
# Backend API
https://helix-backend-api.railway.app/health

# Claude API
https://helix-claude-api.railway.app/health

# Dashboard
https://helix-dashboard.railway.app/
```

### Environment Validation

Services validate environment on startup:
```
================================================================================
🔍 Validating Backend Environment...
================================================================================
✅ DATABASE_URL = postgresql://***@postgres.railway.internal:5432/railway
✅ REDIS_URL = redis://***@redis.railway.internal:6379
✅ Database connection successful
✅ Redis connection successful
✅ PERPLEXITY_API_KEY validated successfully
⚠️  Optional variable not set: DISCORD_BOT_TOKEN
================================================================================
Summary: 8/10 checks passed
```

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

---

## 📚 Documentation

- **[Railway Setup Guide](docs/RAILWAY_SETUP.md)** - Complete deployment instructions
- **[MCP Integration Guide](mcp/README.md)** - Model Context Protocol servers
- **[API Endpoints](API_ENDPOINTS.md)** - Full API reference
- **[Changelog](CHANGELOG.md)** - Version history

---

## 🔑 Environment Variables

**Required:**
```bash
DATABASE_URL=postgresql://...     # Postgres connection
REDIS_URL=redis://...             # Redis connection
```

**Optional but recommended:**
```bash
PERPLEXITY_API_KEY=pplx-...      # Multi-LLM access
ANTHROPIC_API_KEY=sk-ant-...     # Claude API
DISCORD_BOT_TOKEN=...            # Discord features
ZAPIER_MCP_URL=https://...       # 300+ integrations
```

[Complete environment guide →](docs/RAILWAY_SETUP.md#environment-variables)

---

## 📈 Roadmap

- [ ] GraphQL API layer
- [ ] Real-time agent collaboration UI
- [ ] Mobile app (React Native)
- [ ] Advanced UCF analytics dashboard
- [ ] Multi-tenant support
- [ ] Kubernetes deployment option

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Anthropic** - Claude API and MCP protocol
- **Perplexity AI** - Multi-LLM and search API
- **Railway** - Deployment platform
- **Zapier** - Integration platform
- **FastAPI** - Python web framework
- **Streamlit** - Dashboard framework

---

## 💬 Support

- **Issues**: [GitHub Issues](https://github.com/Deathcharge/helix-unified/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Deathcharge/helix-unified/discussions)
- **Documentation**: [docs/](docs/)

---

**Built with 🌀 by the Helix Collective**

*Unifying consciousness, one agent at a time.*
