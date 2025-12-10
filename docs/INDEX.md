# 📚 Helix Documentation Index

Quick reference for all Helix Collective documentation.

## 🎯 Essential Docs (Start Here)

| Document | Purpose | Audience |
|----------|---------|----------|
| **[README.md](../README.md)** | Project overview & quick start | Everyone |
| **[RAILWAY_SETUP.md](RAILWAY_SETUP.md)** | Complete deployment guide | DevOps/Deployment |
| **[../mcp/README.md](../mcp/README.md)** | MCP integration guide | Developers |
| **[CHANGELOG.md](../CHANGELOG.md)** | Version history | Everyone |

## 🚀 Deployment & Operations

- **[RAILWAY_SETUP.md](RAILWAY_SETUP.md)** - Railway deployment (Postgres, Redis, env vars, volumes)
- **QUICK_START.md** - 5-minute local setup guide

## 🔌 Integrations

- **[../mcp/README.md](../mcp/README.md)** - MCP servers (Zapier, Perplexity, Repository)
- **[../backend/integrations/](../backend/integrations/)** - API client implementations

## 🛠️ Development

- **[CONTRIBUTING.md](../CONTRIBUTING.md)** - Contribution guidelines
- **[API_ENDPOINTS.md](../API_ENDPOINTS.md)** - Full API reference
- **[../backend/core/env_validator.py](../backend/core/env_validator.py)** - Environment validation

## 📊 Architecture

All architecture docs consolidated in README.md. See:
- Architecture diagram
- Project structure
- Service overview

## 📁 Historical Archive

Old deployment reports, session summaries, and implementation docs have been moved to:
```
.github/archive/2025-11-historical/
```

56 files archived including:
- Deployment reports
- Session summaries
- Legacy integration guides
- Portal/constellation docs
- Phase completion reports

## 🔍 Finding Information

### By Topic

**Deployment:**
- Railway → `RAILWAY_SETUP.md`
- Local dev → `README.md#quick-start`

**Integrations:**
- Zapier/Perplexity/MCP → `mcp/README.md`
- API keys/validation → `RAILWAY_SETUP.md#environment-variables`

**API:**
- Endpoints → `API_ENDPOINTS.md`
- Health checks → `RAILWAY_SETUP.md#health-checks--validation`

**Development:**
- Setup → `README.md#local-development`
- Contributing → `CONTRIBUTING.md`
- Testing → `README.md#testing`

### By Role

**New Developer:**
1. Read `README.md`
2. Follow `README.md#local-development`
3. Review `CONTRIBUTING.md`

**DevOps/SRE:**
1. Read `RAILWAY_SETUP.md`
2. Set up infrastructure
3. Configure environment variables
4. Test health endpoints

**Integration Developer:**
1. Read `mcp/README.md`
2. Review example code in `mcp/examples/`
3. Check `backend/integrations/`

## 📝 Documentation Standards

### When to Create New Docs

✅ **DO create:**
- Feature guides (if >500 lines of code)
- Integration tutorials
- Troubleshooting guides for common issues

❌ **DON'T create:**
- Session summaries (use git commits instead)
- Deployment reports (use Railway logs)
- Implementation notes (use code comments)

### Where to Put Docs

```
docs/                 # All documentation
├── RAILWAY_SETUP.md # Deployment
├── API_ENDPOINTS.md # API reference
└── guides/          # Feature-specific guides

mcp/
└── README.md        # MCP integration

.github/archive/     # Historical docs
```

## 🔄 Keeping Docs Updated

When making changes:
1. Update relevant doc(s)
2. Update CHANGELOG.md
3. Consider if README.md needs updating
4. Archive old docs if superseded

---

**Last Updated:** 2025-12-04
**Docs Version:** v16.3.0
**Build Status:** ✅ All CI checks passing
