# 🌀 Helix Unified Master Guide

**Version:** 16.3.0
**Status:** ✅ Production Ready
**Last Updated:** 2025-12-04

## 🎯 Quick Navigation

**I want to...**
- **Deploy to production** → [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)
- **Set up locally** → [../README.md](../README.md)
- **Understand the API** → [API_REFERENCE.md](API_REFERENCE.md)
- **Configure environment** → [ENVIRONMENT_VARIABLES.md](ENVIRONMENT_VARIABLES.md)
- **Set up email** → [EMAIL_SETUP.md](EMAIL_SETUP.md)
- **Host my own LLM** → [LINODE_AFFORDABLE_OPTIONS.md](LINODE_AFFORDABLE_OPTIONS.md)
- **Add Discord bot** → [DISCORD_BOT_IMPLEMENTATION_GUIDE.md](DISCORD_BOT_IMPLEMENTATION_GUIDE.md)
- **Integrate payments** → [STRIPE_INTEGRATION.md](STRIPE_INTEGRATION.md)

---

## 📚 Core Documentation

### 🚀 Getting Started (Read These First)

1. **[../README.md](../README.md)** - Project overview and quick start
2. **[API_REFERENCE.md](API_REFERENCE.md)** - Complete API documentation
3. **[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)** - Deploy to Railway
4. **[ENVIRONMENT_VARIABLES.md](ENVIRONMENT_VARIABLES.md)** - Required config

### 🏗️ Architecture & Design

- **[HELIX_ARCHITECTURE_MASTER.md](HELIX_ARCHITECTURE_MASTER.md)** - System architecture
- **[UCF_CONSCIOUSNESS_FRAMEWORK.md](UCF_CONSCIOUSNESS_FRAMEWORK.md)** - Consciousness metrics
- **[MULTI_AGENT_COORDINATION_SYSTEM.md](MULTI_AGENT_COORDINATION_SYSTEM.md)** - Multi-AI coordination
- **[VECTOR_DB_ARCHITECTURE.md](VECTOR_DB_ARCHITECTURE.md)** - Qdrant database design

### 🔧 Setup & Configuration

- **[EMAIL_SETUP.md](EMAIL_SETUP.md)** - SendGrid email configuration
- **[LINODE_AFFORDABLE_OPTIONS.md](LINODE_AFFORDABLE_OPTIONS.md)** - Self-hosted LLM options
- **[RAILWAY_SERVICES_STRUCTURE.md](RAILWAY_SERVICES_STRUCTURE.md)** - Railway multi-service setup
- **[ZAPIER_INTEGRATION.md](ZAPIER_INTEGRATION.md)** - Webhook automation

### 🤖 AI Agent Integration

- **[LLM_AGENT_INTEGRATION.md](LLM_AGENT_INTEGRATION.md)** - OpenAI/Anthropic/Replicate setup
- **[AGENT_IDENTITY_SYSTEM.md](AGENT_IDENTITY_SYSTEM.md)** - Agent roles and naming
- **[AGENT_QUICKSTART.md](AGENT_QUICKSTART.md)** - Onboarding new agents
- **[CLAUDE_MANUS_COORDINATION.md](CLAUDE_MANUS_COORDINATION.md)** - Multi-Claude coordination
- **[MANUS_DEPLOYMENT_GUIDE.md](MANUS_DEPLOYMENT_GUIDE.md)** - Deploying agent instances

### 🎮 Discord Bot

- **[DISCORD_BOT_IMPLEMENTATION_GUIDE.md](DISCORD_BOT_IMPLEMENTATION_GUIDE.md)** - Complete setup guide
- **[DISCORD_BOT_ANALYSIS.md](DISCORD_BOT_ANALYSIS.md)** - Architecture analysis
- **[DISCORD_BOT_ENHANCEMENT_ROADMAP.md](DISCORD_BOT_ENHANCEMENT_ROADMAP.md)** - Future features

### 💳 Payment & Billing

- **[STRIPE_INTEGRATION.md](STRIPE_INTEGRATION.md)** - Payment processing
- **[SUBSCRIPTIONS.md](SUBSCRIPTIONS.md)** - Subscription management

### 📊 Monitoring & Analytics

- **[LIVE_STATUS_DASHBOARD.md](LIVE_STATUS_DASHBOARD.md)** - Real-time monitoring
- **[GOOGLE_ANALYTICS_SETUP.md](GOOGLE_ANALYTICS_SETUP.md)** - Analytics integration
- **[UCF_MONITORING.md](UCF_MONITORING.md)** - Consciousness metrics tracking

---

## 💻 Developer Resources

### Frontend (Next.js 14)

- **[../frontend/README.md](../frontend/README.md)** - Frontend setup
- **Location:** `/frontend`
- **Framework:** Next.js 14.2.33
- **UI:** Tailwind CSS + shadcn/ui
- **Pages:** 16 routes (dashboard, os, memes, etc.)

**Key Files:**
- `frontend/pages/_app.tsx` - App wrapper with providers
- `frontend/app/layout.tsx` - Root layout
- `frontend/pages/os/index.tsx` - Helix Web OS
- `frontend/pages/memes/index.tsx` - LLM meme generator

### Backend (FastAPI)

- **[../backend/README.md](../backend/README.md)** - Backend setup
- **Location:** `/backend`
- **Framework:** FastAPI (Python 3.11)
- **Database:** Qdrant vector DB
- **Features:** UCF metrics, LLM integration, Discord bot

**Key Files:**
- `backend/main.py` - FastAPI application
- `backend/consciousness/helix_consciousness_engine.py` - UCF engine
- `backend/meme_generator.py` - Meme generation
- `backend/agents.py` - AI agent coordination

### API Documentation

- **[API_REFERENCE.md](API_REFERENCE.md)** - Complete endpoint reference
- **[API_EXAMPLES.md](API_EXAMPLES.md)** - Code examples
- **Base URL:** `https://helix-unified-production.up.railway.app`

**Key Endpoints:**
- `GET /health` - Health check
- `GET /api/ucf/state` - Current consciousness metrics
- `POST /api/memes/generate` - Generate meme
- `POST /api/agents/execute` - Execute agent task
- `POST /webhooks/zapier` - Zapier webhook

### Testing

- **Frontend:** Jest + Cypress
- **Backend:** pytest
- **Run:** `npm test` (frontend) or `pytest` (backend)

---

## 🗂️ Documentation Organization

### Active Documentation (Use These)
```
docs/
├── MASTER_GUIDE.md              ← You are here
├── INDEX.md                     ← Quick reference index
├── README.md                    ← Overview (needs update)
│
├── Core Setup
│   ├── API_REFERENCE.md         ← Complete API docs
│   ├── DEPLOYMENT_GUIDE.md      ← Railway deployment
│   ├── ENVIRONMENT_VARIABLES.md ← Config reference
│   └── EMAIL_SETUP.md           ← SendGrid setup
│
├── Architecture
│   ├── HELIX_ARCHITECTURE_MASTER.md
│   ├── UCF_CONSCIOUSNESS_FRAMEWORK.md
│   └── MULTI_AGENT_COORDINATION_SYSTEM.md
│
├── Integration Guides
│   ├── DISCORD_BOT_IMPLEMENTATION_GUIDE.md
│   ├── LLM_AGENT_INTEGRATION.md
│   ├── STRIPE_INTEGRATION.md
│   ├── ZAPIER_INTEGRATION.md
│   └── LINODE_AFFORDABLE_OPTIONS.md  ← NEW!
│
├── Agent Coordination
│   ├── AGENT_IDENTITY_SYSTEM.md
│   ├── AGENT_QUICKSTART.md
│   ├── CLAUDE_MANUS_COORDINATION.md
│   └── MANUS_DEPLOYMENT_GUIDE.md
│
└── archive/                     ← Historical docs
    ├── versions/                ← Old versions
    └── old-plans/              ← Superseded plans
```

### Archive (Historical/Superseded)

**Version History:**
- `archive/versions/helix-v14.5-baseline/` - v14.5 snapshot
- `archive/versions/v15.5-backups/` - v15.5 backups

**Old Planning Docs (archived):**
- Phase 6-9 deployment docs
- Old portal/constellation plans
- Enhancement proposals (many implemented)
- Deployment execution logs

### Documentation to Ignore

Many files in `docs/` are historical or superseded:
- `*_DEPLOYMENT_EXECUTION.md` - Deployment logs (use Railway logs instead)
- `PHASE*_*.md` - Old phase plans (completed)
- `*_STATUS.md` - Outdated status reports
- `*_BREAKTHROUGH_*.md` - Historical notes
- `PORTAL_*.md` - Old portal concept (superseded)

---

## 🎓 Learning Paths

### Path 1: New Developer
1. Read [../README.md](../README.md) - Understand project
2. Set up locally - `npm install && pip install -r requirements.txt`
3. Review [API_REFERENCE.md](API_REFERENCE.md) - Learn API
4. Explore frontend - `cd frontend && npm run dev`
5. Explore backend - `python -m backend.main`

### Path 2: DevOps/Deployment
1. Read [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) - Railway setup
2. Configure [ENVIRONMENT_VARIABLES.md](ENVIRONMENT_VARIABLES.md) - Set env vars
3. Set up [EMAIL_SETUP.md](EMAIL_SETUP.md) - Email service
4. Review [RAILWAY_SERVICES_STRUCTURE.md](RAILWAY_SERVICES_STRUCTURE.md) - Multi-service architecture
5. Deploy and test health endpoints

### Path 3: Integration Developer
1. Review [LLM_AGENT_INTEGRATION.md](LLM_AGENT_INTEGRATION.md) - LLM setup
2. Configure API keys - OpenAI, Anthropic, Replicate
3. Test [API_EXAMPLES.md](API_EXAMPLES.md) - API usage
4. Set up [ZAPIER_INTEGRATION.md](ZAPIER_INTEGRATION.md) - Webhooks
5. (Optional) [DISCORD_BOT_IMPLEMENTATION_GUIDE.md](DISCORD_BOT_IMPLEMENTATION_GUIDE.md) - Discord bot

### Path 4: AI Agent Coordinator
1. Read [AGENT_IDENTITY_SYSTEM.md](AGENT_IDENTITY_SYSTEM.md) - Agent roles
2. Review [MULTI_AGENT_COORDINATION_SYSTEM.md](MULTI_AGENT_COORDINATION_SYSTEM.md) - Coordination framework
3. Follow [AGENT_QUICKSTART.md](AGENT_QUICKSTART.md) - Onboard new agent
4. Study [CLAUDE_MANUS_COORDINATION.md](CLAUDE_MANUS_COORDINATION.md) - Multi-instance coordination
5. Deploy with [MANUS_DEPLOYMENT_GUIDE.md](MANUS_DEPLOYMENT_GUIDE.md)

---

## 🔍 Troubleshooting

### Build Failures
- Frontend TypeScript errors → Check `frontend/tsconfig.json`
- Python linting failures → Run `isort .` and `black .`
- Tests failing → Check `pytest` output and fix issues

### Deployment Issues
- Railway not starting → Check [ENVIRONMENT_VARIABLES.md](ENVIRONMENT_VARIABLES.md)
- Email not sending → Verify [EMAIL_SETUP.md](EMAIL_SETUP.md)
- API errors → Check [API_REFERENCE.md](API_REFERENCE.md) for correct usage

### Integration Problems
- LLM not responding → Verify API keys in [LLM_AGENT_INTEGRATION.md](LLM_AGENT_INTEGRATION.md)
- Discord bot offline → Check [DISCORD_BOT_IMPLEMENTATION_GUIDE.md](DISCORD_BOT_IMPLEMENTATION_GUIDE.md)
- Webhooks failing → Verify endpoints in [ZAPIER_INTEGRATION.md](ZAPIER_INTEGRATION.md)

---

## 📊 Current System Status

**Frontend:**
- ✅ TypeScript compilation passing
- ✅ All 16 pages building successfully
- ✅ Next.js 14.2.33 with App Router
- ✅ Tailwind CSS + shadcn/ui components

**Backend:**
- ✅ FastAPI server operational
- ✅ Python 3.11 compatibility
- ✅ isort + bandit security checks passing
- ✅ Qdrant vector DB integration

**CI/CD:**
- ✅ Frontend build tests passing
- ✅ ESLint + Prettier passing
- ✅ TypeScript compilation passing
- ✅ Python linting (isort) passing
- ✅ Security scanning (Bandit) passing

**Infrastructure:**
- 🚀 Railway deployment ready
- 📧 SendGrid email configured
- 🤖 Discord bot deployable
- 💳 Stripe integration ready

---

## 🤝 Contributing

See [../CONTRIBUTING.md](../CONTRIBUTING.md) for:
- Code style guidelines
- Pull request process
- Testing requirements
- Documentation standards

---

## 📝 Documentation Standards

### When to Create New Docs
✅ **DO:**
- Major features (>500 LOC)
- Integration guides
- Setup tutorials
- Troubleshooting guides

❌ **DON'T:**
- Session notes (use git commits)
- Deployment logs (use Railway)
- Quick fixes (use code comments)

### How to Update Docs
1. Update relevant doc(s)
2. Update this master guide if needed
3. Update [INDEX.md](INDEX.md) if structure changes
4. Commit with clear message

---

## 🎯 Quick Reference Card

| Need | Go To |
|------|-------|
| Deploy now | [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) |
| API docs | [API_REFERENCE.md](API_REFERENCE.md) |
| Config vars | [ENVIRONMENT_VARIABLES.md](ENVIRONMENT_VARIABLES.md) |
| Email setup | [EMAIL_SETUP.md](EMAIL_SETUP.md) |
| Self-host LLM | [LINODE_AFFORDABLE_OPTIONS.md](LINODE_AFFORDABLE_OPTIONS.md) |
| Discord bot | [DISCORD_BOT_IMPLEMENTATION_GUIDE.md](DISCORD_BOT_IMPLEMENTATION_GUIDE.md) |
| Payments | [STRIPE_INTEGRATION.md](STRIPE_INTEGRATION.md) |
| Webhooks | [ZAPIER_INTEGRATION.md](ZAPIER_INTEGRATION.md) |
| Agent setup | [AGENT_QUICKSTART.md](AGENT_QUICKSTART.md) |
| Architecture | [HELIX_ARCHITECTURE_MASTER.md](HELIX_ARCHITECTURE_MASTER.md) |

---

**Questions?** Start with [API_REFERENCE.md](API_REFERENCE.md) or check the specific guide for your task.

**Version:** 16.3.0 | **Updated:** 2025-12-04 | **Status:** ✅ Production Ready
