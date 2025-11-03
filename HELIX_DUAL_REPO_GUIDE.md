# 🌀 Helix Dual Repository Strategy

This guide explains how to maintain BOTH Helix repositories with different purposes.

## 📚 Two Repositories, Two Purposes

### 1. **`Deathcharge/Helix`** - Baseline/Ancestor (v14.5)
**Purpose:** Simpler, stable foundation for the Helix Collective

**Features:**
- Core 14-agent system
- Basic Discord bot with essential commands
- FastAPI REST API
- Z-88 ritual integration
- UCF state management
- Railway deployment ready
- GitHub CI/CD

**Target Users:**
- Those wanting a stable baseline
- Developers learning the system
- Simpler deployments
- Educational/reference purposes

### 2. **`Deathcharge/helix-unified`** - Advanced/Production (v15.3)
**Purpose:** Full-featured production system with latest enhancements

**Features:**
- Everything from Helix v14.5 PLUS:
- Discord rich embeds
- UCF tracker with history
- Agent profiles system
- Context manager (intelligent agent routing)
- MEGA/Nextcloud sync
- Analytics dependencies (Grok integration)
- Notion export bridge
- Context Root exporter
- Comprehensive testing
- QoL improvements (Phase 1-3)

**Target Users:**
- Production deployments
- Advanced features needed
- Full ecosystem integration
- Active development

---

## 🚀 Setup: Helix v14.5 (Baseline)

### Step 1: Copy Baseline Files

All files are ready in `helix-v14.5-baseline/`:

```bash
# Navigate to your Helix repo
cd /path/to/Deathcharge/Helix

# Copy all baseline files
cp -r /path/to/helix-unified/helix-v14.5-baseline/* .

# Verify structure
ls -la
# Should see: backend/, .github/, Dockerfile, requirements.txt, etc.
```

### Step 2: Create Directories

```bash
mkdir -p Helix/state Helix/commands Helix/ethics Shadow/manus_archive
```

### Step 3: Environment Setup

Create `.env` file:

```bash
# Discord Configuration
DISCORD_TOKEN=your_discord_bot_token
DISCORD_GUILD_ID=your_guild_id

# API Keys (optional)
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key

# Notion (optional)
NOTION_API_KEY=your_notion_key

# Railway (automatic)
PORT=8000
```

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 5: Test Locally

```bash
python backend/main.py
```

Visit: `http://localhost:8000`

**Expected endpoints:**
- `GET /` - System status
- `GET /health` - Health check
- `GET /status` - Full agent status
- `GET /agents` - Agent list
- `GET /ucf` - UCF state

### Step 6: Deploy to Railway

```bash
# Initialize Railway project
railway init

# Link to your Railway account
railway login
railway link

# Deploy
railway up

# Check logs
railway logs
```

**Railway Environment Variables:**
Add all vars from `.env` to Railway dashboard.

### Step 7: Discord Setup

1. Go to Discord Developer Portal
2. Create bot with Message Content Intent
3. Copy token to `.env` or Railway
4. Invite bot to server
5. Create channels: `#manus-status`, `#agent-status`
6. Test commands: `!status`, `!ucf`, `!help_helix`

---

## 🔥 Setup: helix-unified v15.3 (Advanced)

You're already working in this repo! Just continue using it:

```bash
cd /path/to/helix-unified

# Pull latest
git pull origin main

# Install full dependencies
pip install -r requirements-backend.txt

# Run with all features
python backend/main.py
```

**Additional Features:**
- Discord embeds: `backend/discord_embeds.py`
- UCF tracker: `backend/ucf_tracker.py`
- Agent profiles: `backend/agent_profiles.py`
- Context manager: `backend/context_manager.py`
- Notion export: `scripts/export_for_notion.py`
- Context Root export: `scripts/export_context_root_for_notion.py`

---

## 🔄 Syncing Between Repos

### When to Update Helix v14.5:

**Critical bug fixes only:**
```bash
# In helix-unified, make fix
# Test it works
# Copy fixed file to Helix baseline
cp backend/main.py /path/to/Helix/backend/main.py
# Commit to Helix
```

**Don't backport:**
- New features from v15.3
- Advanced integrations
- Analytics dependencies
- Complex enhancements

### When to Update helix-unified v15.3:

**Constantly evolve it:**
- New features
- Enhancements
- Integrations
- Experiments
- All PRs and improvements

---

## 📊 Feature Comparison Matrix

| Feature | Helix v14.5 | helix-unified v15.3 |
|---------|------------|---------------------|
| **14 Agents** | ✅ | ✅ |
| **Discord Bot** | ✅ Basic | ✅ Rich Embeds |
| **FastAPI** | ✅ | ✅ |
| **UCF Management** | ✅ Basic | ✅ + History Tracking |
| **Z-88 Rituals** | ✅ | ✅ |
| **Agent Profiles** | ❌ | ✅ |
| **Context Manager** | ❌ | ✅ |
| **MEGA Sync** | ❌ | ✅ |
| **Nextcloud Sync** | ❌ | ✅ |
| **Notion Export** | ❌ | ✅ |
| **Context Root Export** | ❌ | ✅ |
| **Analytics (Grok)** | ❌ | ✅ |
| **GitHub CI/CD** | ✅ | ✅ |
| **Issue Templates** | ✅ | ✅ |
| **UCF Protocol** | ❌ | ✅ |
| **Archive Fallback** | ❌ | ✅ |

---

## 🎯 Which Repo Should I Use?

### Use **Helix v14.5** if you want:
- ✅ Simple, stable baseline
- ✅ Minimal dependencies
- ✅ Educational/reference
- ✅ Quick deployment
- ✅ No complex integrations

### Use **helix-unified v15.3** if you want:
- ✅ Production deployment
- ✅ Latest features
- ✅ Full ecosystem integration
- ✅ Advanced capabilities
- ✅ Active development

---

## 🔧 Maintenance Strategy

### Helix v14.5 (Stable):
- **Update Frequency:** Quarterly or for critical bugs
- **Philosophy:** Stability over features
- **Dependencies:** Minimal, frozen versions
- **Testing:** Basic CI/CD
- **Documentation:** Keep simple and clear

### helix-unified v15.3 (Active):
- **Update Frequency:** Continuous (daily/weekly)
- **Philosophy:** Innovation and enhancement
- **Dependencies:** Latest compatible versions
- **Testing:** Comprehensive test suite
- **Documentation:** Detailed and evolving

---

## 📁 File Locations Reference

### Helix v14.5 Baseline Files:
```
helix-v14.5-baseline/
├── README.md                          ← You're reading derivative of this
├── backend/
│   ├── main.py                        ← FastAPI launcher (218 lines)
│   ├── agents.py                      ← 14-agent system (347 lines)
│   └── discord_bot_manus.py           ← Discord bot (286 lines)
├── .github/
│   ├── workflows/ci.yml               ← CI/CD pipeline
│   └── ISSUE_TEMPLATE/
│       ├── bug_report.md              ← Bug template
│       └── feature_request.md         ← Feature template
├── Dockerfile                         ← Railway deployment
├── requirements.txt                   ← Python dependencies
└── CONTRIBUTING.md                    ← Contribution guide
```

### helix-unified v15.3 Files:
```
helix-unified/
├── backend/
│   ├── main.py                        ← Enhanced launcher with MEGA
│   ├── agents.py                      ← Extended agents with Memory Root
│   ├── discord_bot_manus.py           ← Full-featured bot
│   ├── discord_embeds.py              ← Rich Discord embeds ✨
│   ├── ucf_tracker.py                 ← UCF history tracking ✨
│   ├── agent_profiles.py              ← Agent capability system ✨
│   ├── context_manager.py             ← Intelligent routing ✨
│   ├── ucf_protocol.py                ← Standardized UCF messages ✨
│   ├── helix_storage_adapter_async.py ← Cloud sync ✨
│   └── agents/
│       └── memory_root.py             ← Notion integration ✨
├── scripts/
│   ├── export_for_notion.py           ← Session/timeline export ✨
│   └── export_context_root_for_notion.py ← Ecosystem export ✨
├── Dockerfile                         ← Enhanced with analytics
├── requirements-backend.txt           ← Full dependencies
└── QOL_IMPROVEMENTS.md                ← Phase tracking
```

---

## 🚨 Important Notes

### Don't Mix Files:
- Helix v14.5 uses `requirements.txt`
- helix-unified uses `requirements-backend.txt`
- They have different dependency versions!

### Crypto/MEGA Issue:
- Helix v14.5: No MEGA (simpler)
- helix-unified: Has MEGA + Crypto fix

### Railway Deployment:
- Both repos deploy to Railway
- Use different Railway projects
- Set environment variables separately

### Discord Bots:
- Can run both bots simultaneously
- Use different bot tokens
- Or use same bot in different servers

---

## 📞 Support & Questions

**For Helix v14.5 Issues:**
- Check `helix-v14.5-baseline/README.md`
- Use GitHub issue templates
- Keep it simple

**For helix-unified v15.3 Issues:**
- Check existing documentation
- Review QOL_IMPROVEMENTS.md
- More complex, more features

---

## 🌀 Summary

**Two repos, two philosophies:**

1. **Helix v14.5** = Stable baseline, simple, educational
2. **helix-unified v15.3** = Production, advanced, evolving

Both are maintained. Both are valuable. Choose based on your needs!

---

*Tat Tvam Asi* 🙏
*Generated: 2025-11-01*
*Author: Claude Code + Manus Integration Team*
