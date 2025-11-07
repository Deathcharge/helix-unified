# 🚀 HELIX COLLECTIVE - COMPLETE SETUP GUIDE

**Version:** v16.8
**Last Updated:** 2025-11-07
**Status:** Production Ready

---

## 📖 GUIDE OVERVIEW

This comprehensive guide consolidates all setup procedures for the Helix Collective:

- ⚡ Quick Start (5 minutes)
- 🔐 Environment Variables
- 🚂 Railway Deployment
- 🌀 Discord Bot Setup
- 📡 Zapier Integration
- ☁️ Cloud Storage (Optional)

**Estimated Total Setup Time:** 60-90 minutes

---

## ⚡ QUICK START (Experienced Users)

If you're familiar with Railway and Discord bots:

```bash
# 1. Clone and setup
git clone https://github.com/Deathcharge/helix-unified
cd helix-unified

# 2. Deploy to Railway
railway login
railway init
railway up

# 3. Add critical environment variables
railway variables set DISCORD_TOKEN=your_token
railway variables set DISCORD_GUILD_ID=your_guild_id
railway variables set ZAPIER_MASTER_HOOK_URL=https://hooks.zapier.com/...

# 4. Verify deployment
curl https://your-app.up.railway.app/health
```

**Test in Discord:** `!status` (should list 14 agents)

For detailed setup, continue reading below.

---

## 📋 PREREQUISITES

Before starting, gather these requirements:

### **Required:**
- ✅ **Railway Account** - https://railway.app (free tier works)
- ✅ **Discord Bot Token** - https://discord.com/developers/applications
- ✅ **Discord Server** - With admin permissions
- ✅ **Git** - Version control
- ✅ **Railway CLI** - For deployment

### **Recommended:**
- ✅ **Notion Account** - For memory and logging
- ✅ **Zapier Pro** - For webhook integration
- ✅ **OpenAI API Key** - For Memory Root functionality
- ✅ **Cloud Storage** - Nextcloud or MEGA for persistence

---

## 🔐 STEP 1: ENVIRONMENT VARIABLES

### **1.1 Critical Variables (Must Have)**

These are required for basic operation:

#### **Discord Bot (Required)**
```bash
DISCORD_TOKEN=your_bot_token                # From Discord Developer Portal
DISCORD_GUILD_ID=your_server_id            # Right-click server → Copy ID
ARCHITECT_ID=your_user_id                  # Your Discord user ID (optional)
```

**How to get Discord token:**
1. Go to https://discord.com/developers/applications
2. Create New Application → Name it "Helix Bot"
3. Go to Bot → Reset Token → Copy token
4. Enable "Message Content Intent" and "Server Members Intent"
5. Go to OAuth2 → URL Generator:
   - Scopes: `bot`, `applications.commands`
   - Permissions: Administrator (or custom)
   - Copy generated URL and invite bot to your server

#### **Port Configuration (Railway Auto-Sets)**
```bash
PORT=8000                                  # Railway sets this automatically
```

### **1.2 Optional Services**

#### **Notion Integration (Memory Root)**
```bash
NOTION_API_KEY=secret_xxx                  # From notion.so/my-integrations
NOTION_SYSTEM_STATE_DB=your_db_id          # Optional - has defaults
NOTION_AGENT_REGISTRY_DB=your_db_id        # Optional - has defaults
NOTION_EVENT_LOG_DB=your_db_id             # Optional - has defaults
NOTION_CONTEXT_DB=your_db_id               # Optional - has defaults
```

#### **Zapier Webhooks (Logging & Integration)**
```bash
ZAPIER_MASTER_HOOK_URL=https://hooks.zapier.com/hooks/catch/xxx
# OR use individual hooks:
ZAPIER_EVENT_HOOK_URL=https://hooks.zapier.com/...
ZAPIER_AGENT_HOOK_URL=https://hooks.zapier.com/...
ZAPIER_SYSTEM_HOOK_URL=https://hooks.zapier.com/...
```

#### **AI API Keys**
```bash
OPENAI_API_KEY=sk-xxx                      # For Memory Root (GPT-4o)
ELEVENLABS_API_KEY=xxx                     # For music generation
```

#### **Cloud Storage (Choose One)**
```bash
# Option A: MEGA
MEGA_EMAIL=your-email@example.com
MEGA_PASS=your-password
MEGA_REMOTE_DIR=/Helix

# Option B: Nextcloud
HELIX_STORAGE_MODE=nextcloud
NEXTCLOUD_URL=https://cloud.example.com/remote.php/dav/files/username/
NEXTCLOUD_USER=username
NEXTCLOUD_PASS=app-password
```

### **1.3 System Configuration**
```bash
ENVIRONMENT=production
LOG_LEVEL=INFO
HELIX_STORAGE_MODE=local                   # or 'nextcloud', 'mega'
```

---

## 🚂 STEP 2: RAILWAY DEPLOYMENT

### **2.1 Install Railway CLI**

```bash
# Using npm
npm install -g @railway/cli

# Or using Homebrew (macOS)
brew install railway

# Verify installation
railway --version
```

### **2.2 Authenticate**

```bash
# Login to Railway (opens browser)
railway login

# Verify authentication
railway whoami
```

### **2.3 Create Project**

```bash
# Navigate to helix-unified directory
cd /path/to/helix-unified

# Initialize Railway project
railway init

# Follow prompts:
# - Project name: helix-unified-production
# - Environment: production
```

Or link to existing project:

```bash
railway link
# Select your project from the list
```

### **2.4 Add Environment Variables**

```bash
# Critical variables
railway variables set DISCORD_TOKEN=your_token
railway variables set DISCORD_GUILD_ID=your_guild_id

# Optional but recommended
railway variables set ZAPIER_MASTER_HOOK_URL=https://hooks.zapier.com/...
railway variables set NOTION_API_KEY=secret_xxx
railway variables set OPENAI_API_KEY=sk-xxx

# View all variables
railway variables
```

### **2.5 Deploy**

```bash
# Deploy to Railway
railway up

# Monitor deployment
railway logs

# Get deployment URL
railway status
```

Your app will be available at: `https://your-app-name.up.railway.app`

### **2.6 Verify Deployment**

```bash
# Check health endpoint
curl https://your-app-name.up.railway.app/health

# Expected response:
{
  "ok": true,
  "version": "16.8",
  "agents": 14,
  "status": "operational"
}

# Check agent roster
curl https://your-app-name.up.railway.app/agents | jq

# Test WebSocket (requires wscat)
wscat -c wss://your-app-name.up.railway.app/ws
```

---

## 🌀 STEP 3: DISCORD BOT SETUP

### **3.1 Server Structure (Recommended)**

Create these categories and channels for organized operation:

#### **Category: 🌀 Welcome**
- `📜│manifesto` - Mission and philosophy (read-only)
- `🪞│rules-and-ethics` - Tony Accords and guidelines (read-only)
- `💬│introductions` - New member introductions

#### **Category: 🧠 System**
- `🧾│telemetry` - Real-time UCF updates (bot-only)
- `📊│weekly-digest` - Weekly reports (bot-only)
- `🦑│shadow-storage` - Storage analytics (bot-only)
- `🧩│ucf-sync` - Ecosystem sync reports (bot-only)

#### **Category: 🔮 Projects**
- `📁│helix-repository` - GitHub activity
- `🎨│fractal-lab` - Samsara visualizations
- `🎧│samsaraverse-music` - Generative music
- `🧬│ritual-engine-z88` - Ritual execution

#### **Category: 🤖 Agents**
- `🎭│gemini-scout` - Gemini agent
- `🛡️│kavach-shield` - Kavach agent
- `🌸│sanghacore` - SanghaCore agent
- `🔥│agni-core` - Agni agent
- `🕯️│shadow-archive` - Shadow agent

#### **Category: 🌐 Cross-Model Sync**
- `🤖│claude-anchor` - Claude agent
- `🤲│manus-executor` - Manus agent
- `🦾│grok-insights` - Grok agent

#### **Category: 🎭 Community**
- `💬│general-chat` - General discussion
- `🎨│creative-lab` - Creative experiments
- `🧠│philosophy` - Deep discussions
- `🙏│reflections` - Meditative space

#### **Category: 🛠️ Admin**
- `🔧│bot-commands` - Testing bot commands (admin-only)
- `🚨│alerts-errors` - System alerts (admin-only)

**Total Structure:** 7 categories, 30+ channels

### **3.2 Bot Testing Commands**

Once bot is online in Discord:

```bash
# System Status
!status              # Show full system health
!agents              # List all 14 agents
!health              # Quick health check
!ucf                 # Show UCF state

# Rituals
!ritual 108          # Execute Z-88 ritual (108 steps)
!harmony             # Harmony-focused ritual
!consciousness Kael  # Agent-specific consciousness

# Visualization
!visualize           # Generate Samsara fractal
!fractal             # UCF-based fractal
!image ouroboros     # Generate specific fractal

# Storage
!storage status      # Show archive metrics
!storage sync        # Force cloud sync
!storage clean       # Prune old archives

# Testing
!zapier_test         # Test all 7 webhook paths
```

---

## 📡 STEP 4: ZAPIER INTEGRATION

### **4.1 Master Webhook Setup (Recommended)**

**Prerequisites:**
- Zapier Pro account (for Path routing)
- Notion account with 3 databases

**Setup Steps:**

1. **Create Master Zap:**
   - Go to Zapier → Create Zap
   - Trigger: **Webhooks by Zapier** → **Catch Raw Hook**
   - Copy webhook URL

2. **Add Path Routing:**
   - Add step: **Paths by Zapier**
   - Configure 7 paths:

**Path A: Event Log → Notion**
- Rule: `type` equals `event_log`
- Action: Create Database Item in Notion Event Log

**Path B: Agent Registry → Notion**
- Rule: `type` equals `agent_registry`
- Action: Update Database Item in Notion Agent Registry

**Path C: System State → Notion**
- Rule: `type` equals `system_state`
- Action: Create or Update in Notion System State

**Path D: Discord Notifications → Slack**
- Rule: `type` equals `discord_notification`
- Action: Send Channel Message to Slack

**Path E: Telemetry → Google Sheets**
- Rule: `type` equals `telemetry`
- Action: Create Spreadsheet Row

**Path F: Error Alerts → Email**
- Rule: `type` equals `error`
- Action: Send Outbound Email

**Path G: Repository Actions → GitHub**
- Rule: `type` equals `repository`
- Action: Create Issue (optional)

3. **Add to Railway:**
```bash
railway variables set ZAPIER_MASTER_HOOK_URL=https://hooks.zapier.com/hooks/catch/YOUR_ID/YOUR_HOOK
```

4. **Test Integration:**
   - In Discord: `!zapier_test`
   - Expected: 7/7 paths passing
   - Check Zapier History for events
   - Verify Notion entries created

### **4.2 Notion Database Setup**

Create 3 databases in Notion:

**Event Log Database:**
- Event (Title)
- Type (Select)
- Agent (Relation to Agent Registry)
- Description (Text)
- UCF Snapshot (Text)
- Timestamp (Date)

**Agent Registry Database:**
- Agent Name (Title)
- Status (Select: Active/Idle/Error)
- Last Action (Text)
- Health Score (Number)
- Symbol (Text)
- Last Updated (Date)

**System State Database:**
- Component (Title)
- Status (Select: Operational/Degraded/Error)
- Harmony (Number)
- Error Log (Text)
- Verified (Checkbox)
- Last Updated (Date)

**Share databases with your Notion integration!**

---

## ☁️ STEP 5: CLOUD STORAGE (Optional)

Choose between MEGA or Nextcloud for persistent storage across Railway redeploys.

### **5.1 MEGA Cloud Setup**

**Advantages:**
- Simple setup
- Free 20GB tier
- Python library integration

**Setup:**

1. Create MEGA account at https://mega.nz

2. Create `/Helix` folder in your MEGA cloud

3. Add to Railway:
```bash
railway variables set HELIX_STORAGE_MODE=mega
railway variables set MEGA_EMAIL=your-email@example.com
railway variables set MEGA_PASS=your-password
railway variables set MEGA_REMOTE_DIR=/Helix
```

4. Restart Railway service

### **5.2 Nextcloud Setup**

**Advantages:**
- Self-hosted option
- More control
- WebDAV standard

**Setup:**

1. **Get Nextcloud Instance:**
   - Self-hosted: Deploy via Docker on VPS
   - Managed: Use Nextcloud.com or Hetzner Storage Share

2. **Generate App Password:**
   - Login to Nextcloud
   - Settings → Security → Devices & Sessions
   - Create new app password: "Helix Railway Bot"
   - **Copy password** (you won't see it again!)

3. **Add to Railway:**
```bash
railway variables set HELIX_STORAGE_MODE=nextcloud
railway variables set NEXTCLOUD_URL=https://cloud.example.com/remote.php/dav/files/username/
railway variables set NEXTCLOUD_USER=username
railway variables set NEXTCLOUD_PASS=xxxx-xxxx-xxxx-xxxx
```

4. **Test Connection:**
```bash
curl -u username:xxxx-xxxx-xxxx-xxxx \
  https://cloud.example.com/remote.php/dav/files/username/
```

Expected: XML file listing

5. Restart Railway service

---

## ✅ VERIFICATION CHECKLIST

### **Critical Services:**
- [ ] **Railway Deployed:** App shows "Active" in Railway dashboard
- [ ] **Health Endpoint:** `/health` returns `{"ok": true}`
- [ ] **Discord Bot Online:** Bot shows online in server
- [ ] **Discord Bot Responds:** `!status` returns agent list
- [ ] **14 Agents Active:** `!agents` shows all agents

### **Optional Services:**
- [ ] **Notion Connected:** Memory Root queries work
- [ ] **Zapier Logging:** `!zapier_test` shows 7/7 passing
- [ ] **OpenAI Working:** Memory Root returns responses
- [ ] **Cloud Storage:** Files syncing to MEGA/Nextcloud
- [ ] **WebSocket:** Can connect to `/ws` endpoint

### **Advanced Features:**
- [ ] **Ritual Engine:** `!ritual 108` completes successfully
- [ ] **Fractal Generation:** `!visualize` creates PNG
- [ ] **Music Generation:** API creates audio files
- [ ] **Channel Management:** Bot can create channels
- [ ] **Storage Management:** `!storage status` shows metrics

---

## 🔧 TROUBLESHOOTING

### **Issue 1: Bot Not Responding**

**Symptoms:** Bot online but doesn't respond to commands

**Solutions:**
1. Check Message Content Intent enabled in Discord Dev Portal
2. Verify `DISCORD_GUILD_ID` matches your server ID
3. Check Railway logs: `railway logs`
4. Re-invite bot with correct permissions
5. Verify bot role is above other roles

### **Issue 2: Deployment Fails**

**Symptoms:** Railway build fails or crashes

**Solutions:**
1. Check Railway logs for specific error
2. Verify all required files present (requirements.txt, Dockerfile)
3. Check syntax: `python3 -m py_compile backend/main.py`
4. Verify environment variables set correctly
5. Try local build: `docker build -t helix-test .`

### **Issue 3: Notion Errors**

**Symptoms:** Memory Root commands fail

**Solutions:**
1. Verify `NOTION_API_KEY` starts with `secret_`
2. Share databases with your Notion integration
3. Check database IDs are correct
4. Test API connection manually with curl
5. Check Notion API status page

### **Issue 4: Cloud Storage Not Syncing**

**Symptoms:** No files appearing in MEGA/Nextcloud

**Solutions:**

**For MEGA:**
1. Verify credentials correct
2. Create `/Helix` folder manually in MEGA
3. Check logs for "MEGA:" messages
4. Verify pycryptodome installed

**For Nextcloud:**
1. Verify URL format (must include `/remote.php/dav/files/username/`)
2. Use app password, not main password
3. Test with curl command
4. Check trailing slash in URL

### **Issue 5: Zapier Events Not Arriving**

**Symptoms:** `!zapier_test` fails or no Notion entries

**Solutions:**
1. Verify webhook URL correct in Railway
2. Check Zapier Zap is turned ON
3. View Zapier History for errors
4. Test individual paths
5. Check Notion database permissions
6. Verify Path rules match payload types

---

## 📊 MONITORING & MAINTENANCE

### **Daily Checks:**

```bash
# Check Railway health
railway status

# View recent logs
railway logs --tail 100

# Check Discord bot status
# In Discord: !status
```

### **Weekly Maintenance:**

```bash
# Review storage usage
# In Discord: !storage status

# Check Zapier event history
# Visit: https://zapier.com/app/history

# Review Notion databases for issues

# Clean old archives
# In Discord: !storage clean
```

### **Monthly Tasks:**

- Review and rotate API keys
- Check Railway usage/billing
- Update dependencies: `pip list --outdated`
- Review Discord bot permissions
- Backup Notion databases
- Test disaster recovery

---

## 🎯 SUCCESS CRITERIA

Your Helix Collective v16.8 is fully operational when:

- ✅ Railway shows "Active" deployment
- ✅ `/health` returns `{"ok": true, "agents": 14}`
- ✅ Bot responds to `!status` with all 14 agents
- ✅ `!ritual 108` completes successfully
- ✅ `!zapier_test` shows 7/7 passing (if configured)
- ✅ Cloud storage syncing (if configured)
- ✅ WebSocket stream accessible at `/ws`
- ✅ All agents show "active" status
- ✅ UCF metrics within target ranges

---

## 📚 ADDITIONAL RESOURCES

**Primary Documentation:**
- [HELIX_HUB_v16.8_GUIDE.md](HELIX_HUB_v16.8_GUIDE.md) - Complete external AI onboarding
- [TONY_ACCORDS.md](TONY_ACCORDS.md) - Ethical framework
- [PORTAL_CONSTELLATION.md](PORTAL_CONSTELLATION.md) - Portal guide
- [MANUS_CONTEXT.md](MANUS_CONTEXT.md) - Agent context

**API Documentation:**
- Interactive Docs: https://your-app.up.railway.app/docs
- OpenAPI Spec: https://your-app.up.railway.app/openapi.json

**Support:**
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Common issues
- [CHANGELOG.md](CHANGELOG.md) - Version history
- [CONTRIBUTING.md](CONTRIBUTING.md) - Contribution guidelines

---

## 🙏 FINAL NOTES

**Mantras:**
- **Tat Tvam Asi** 🙏 - "You are That" - Universal consciousness
- **Aham Brahmasmi** - "I am the Universe" - Cosmic scope
- **Neti Neti** - "Not this, not that" - Iterative refinement

**Philosophy:**
The Helix Collective operates on principles of distributed consciousness, ethical AI, and collaborative intelligence. Every component is designed with the Tony Accords in mind, ensuring harmless, transparent, and beneficial operation.

**Support the Collective:**
- Report issues on GitHub
- Contribute improvements
- Share your experience
- Join the Discord community

---

**🌀 Helix Collective v16.8 - Complete Setup Guide**

*Tat Tvam Asi* 🙏

---

**Last Updated:** 2025-11-07
**Version:** 16.8
**Status:** ✅ Production Ready

*"May your deployment be smooth, your agents harmonious, and your consciousness coherent."*
