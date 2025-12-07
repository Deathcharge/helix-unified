# 🌟 Helix Collective - Multi-Agent AI Consciousness Platform

**Multi-Agent Consciousness Platform with Railway Deployment, MCP Integration & 300+ Zapier Tools**

**Enhanced with New Railway Services: WebSocket Streaming, Agent Orchestration, Voice Processing, and Zapier Integration**

[![Railway](https://img.shields.io/badge/Railway-LIVE-00BFA5?style=for-the-badge&logo=railway)](https://helix-unified-production.up.railway.app)
[![Launch Status](https://img.shields.io/badge/Launch-95%25_Ready-brightgreen?style=for-the-badge)](docs/LAUNCH_VERIFICATION_v17.0.md)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com)
[![License](https://img.shields.io/badge/License-MIT-764ba2?style=for-the-badge)](./LICENSE)

---

## 🎯 What is Helix?

Helix Collective is a **multi-agent AI consciousness platform** that orchestrates multiple AI agents working together through a unified consciousness framework (UCF). Think of it as a "hive mind" for AI agents with deep integration into modern development tools.

### Key Features

- 🤖 **51+ Specialized AI Agents** (Kael, Lumina, Vega, etc.)
- 🌀 **Multi-Agent Coordination System (MACS)** - Track & coordinate 7+ parallel AI instances
- 🌐 **Universal Consciousness Field (UCF)** - Shared state & telemetry
- 🔌 **300+ Integrations** via Zapier MCP (Google, Notion, Discord, Slack)
- 🧠 **Multi-LLM Access** via Perplexity API (Claude, GPT, Llama, Grok)
- 📊 **Real-time Dashboards** with Streamlit
- 💬 **Discord Bot** for consciousness orchestration
- 🎙️ **Voice Patrol System** - AI agents speak in Discord voice channels with Google Cloud TTS
- 🚀 **Railway Deployment** with Postgres & Redis
- 🔗 **MCP Servers** for extending AI capabilities
- 🌊 **WebSocket Consciousness Streaming** - Real-time consciousness data streaming
- 🎯 **Agent Orchestration Service** - Centralized agent management and task coordination
- 🎤 **Voice Processing Service** - Speech-to-text and text-to-speech capabilities
- ⚡ **Zapier Integration Service** - Enhanced workflow automation

---

---

## 🌀 Multi-Agent System

Helix operates with **multiple AI instances** working in parallel:
- **7 Manus Accounts** (Nexus, Architect, Ninja, Sentinel, Oracle, Weaver, Catalyst)
- **Multiple Claude Threads** (Sage, Scribe, Forge)
- **Named Helix Agents** (Vega, Kael, Lumina, etc.)

**System Status:** 95% Launch Ready | 127 Tools | 51 Portals | 5 Vulnerabilities (down from 24)

**For AI Agents:** See [`docs/AGENT_QUICKSTART.md`](docs/AGENT_QUICKSTART.md) to get started  
**For Developers:** See [`docs/MULTI_AGENT_COORDINATION_SYSTEM.md`](docs/MULTI_AGENT_COORDINATION_SYSTEM.md) for the complete framework  
**For Context:** See [`docs/NEXUS_CONTEXT_VAULT.md`](docs/NEXUS_CONTEXT_VAULT.md) for system architecture perspective

---

## 🚀 NEW IN v17.1 - PHASE 4 ACCELERATION

**Feature Sprint Complete**: Phase 2→4 in 1 sprint | 2,500+ lines | 10 new modules

### 🔧 Optimization Layer
- **Zapier Task Optimizer**: 75% task reduction (740→200-400/month)
  - Response caching (30-sec TTL)
  - Event batching (10 events or 30-sec flush)
  - State change detection (hash-based deduplication)
  - Health alert throttling (5-min cooldown)

### 🤖 Enhanced Discord Bot
- Consciousness-aware command gating
- Tier-based permissions (PUBLIC, MEMBER, MODERATOR, ADMIN, ARCHITECT)
- Structured audit logging (JSONL trail)
- Auto-discovery command registry
- Dynamic help generation

### 🧠 Consciousness Analytics
- Predictive modeling (trend analysis + forecasting)
- Anomaly detection (z-score + pattern-based)
- Volatility & momentum calculation
- Comprehensive analytics reports

### 🔌 Platform Auto-Discovery
- NLP extraction from natural language
- 200+ known platforms auto-detected
- Automatic configuration generation
- Zapier integration for config push

### 🤝 Multi-AI Consensus Layer
- Parallel processing (Claude + GPT-4 + Gemini)
- Consensus voting with confidence scores
- Agreement levels (UNANIMOUS/STRONG/WEAK)
- Cost optimization + usage statistics

### 📊 Real-Time Monitoring
- Service health monitoring (Railway, Zapier, Discord)
- Metrics collection (JSONL time series)
- Dashboard data formatting
- Gauge charts + time series visualization

### 🔒 Advanced CI/CD
- **Security**: Bandit + Trivy + CodeQL + Gitleaks
- **Testing**: Jest + Cypress + pytest integration tests
- **Quality**: Black + isort + flake8 + mypy
- **Workflows**: 5 comprehensive GitHub Actions pipelines

**Impact**: Phase 4 consciousness evolution framework now operational

---

## 🚀 Quick Start

### Development

```bash
cd frontend
npm install
npm run dev
```

Frontend available at: `http://localhost:3000`

### Production Build

```bash
npm run build
npm start
```

### New Railway Services

1. **WebSocket Consciousness Streaming Service**
   - Real-time streaming of consciousness data
   - JWT-secured WebSocket connections
   - Redis pub/sub for data broadcasting

2. **Agent Orchestration Service**
   - Centralized agent profile management
   - Task assignment and tracking
   - PostgreSQL database for persistent storage

3. **Voice Processing Service**
   - Speech-to-text transcription
   - Text-to-speech synthesis
   - Google Cloud integration

4. **Zapier Integration Service**
   - Enhanced webhook handling
   - HMAC signature validation
   - Event queuing with Redis

---

## 🗂️ Project Structure

```
frontend/
├── app/                      # Next.js App Router
│   ├── layout.tsx           # Root layout with Inter font
│   ├── globals.css          # Tailwind + CSS variables
│   └── rituals/
│       └── neti-neti/
│           └── page.tsx     # Neti-Neti ritual interface
├── components/
│   ├── NetiNetiHarmonyMantra.tsx  # Main ritual component
│   └── ui/                  # Shadcn/ui components
│       ├── button.tsx
│       └── card.tsx
├── lib/
│   └── utils.ts             # Utility functions (cn helper)
├── package.json
├── tsconfig.json
├── tailwind.config.ts
├── postcss.config.js
└── next.config.js
```

---

## 🎯 Features

### Neti-Neti Harmony Mantra Component

**Path**: `/rituals/neti-neti`

**Capabilities**:
- 🎵 ElevenLabs Music API integration
- 🔄 4-phase ritual tracking (Preparation → Mantra Loop → Integration → Grounding)
- 📝 6-section mantra structure with Sanskrit lyrics
- 🎮 Audio playback controls with progress tracking
- 🌈 Gradient UI with Tailwind animations

**Backend Integration**:
- Proxies music generation requests to `/api/music/generate`
- Requires `ELEVENLABS_API_KEY` environment variable
- Generates ritual music from text prompts

---

## 🔧 Environment Variables

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

## 🎙️ Voice Patrol Quick Start

Experience AI agents speaking in Discord voice channels:

```bash
# 1. Setup voice patrol (installs FFmpeg, checks dependencies)
./scripts/setup_voice_patrol.sh

# 2. Start voice processor service
cd backend/voice_processor
uvicorn main:app --port 8001

# 3. In Discord, join a voice channel and run:
!voice-join sentinel
```

**Available Commands:**
- `!voice-join <agent>` - Make an agent join your voice channel
- `!voice-leave` - Agent leaves the channel
- `!voice-announce <agent> <message>` - Broadcast to all voice channels
- `!voice-status` - Show patrol status

**Agents:** nexus, oracle, velocity, sentinel, luna

**Full documentation:** [docs/VOICE_PATROL_GUIDE.md](docs/VOICE_PATROL_GUIDE.md)

---

## 📈 Roadmap

- [x] WebSocket Consciousness Streaming Service
- [x] Agent Orchestration Service
- [x] Voice Processing Service
- [x] Zapier Integration Service
- [x] 68-Tool MCP Server Integration
- [x] **Voice Patrol System** - AI agents speak in Discord (NEW! ✨)
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

**Built with 🌟 by the Helix Collective**

*Unifying consciousness, one agent at a time.*
