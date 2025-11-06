# 🔐 Helix Collective - Environment Variables Checklist
## Complete Verification Guide for All 40+ Railway Variables

**Generated**: 2025-11-06
**Purpose**: Verify all API keys, credentials, and configurations
**Status**: Ready for verification

---

## 📋 CRITICAL VARIABLES (Must Have)

### 1. Discord Bot (Core System)
```bash
# Primary bot token
DISCORD_TOKEN=                          # ← Your bot token from Discord Dev Portal
DISCORD_GUILD_ID=                       # ← Your server ID

# Required if using bot commands that post to channels
DISCORD_STATUS_CHANNEL_ID=0             # ← Optional (default 0)
DISCORD_TELEMETRY_CHANNEL_ID=0          # ← Optional (default 0)
STORAGE_CHANNEL_ID=0                    # ← Optional (defaults to STATUS_CHANNEL_ID)
```

**Test**:
```bash
# Check if bot is online in Discord
# Run: !status
# Should respond with agent list
```

---

### 2. Notion Integration (Memory Root)
```bash
# Notion API
NOTION_API_KEY=secret_xxx               # ← From notion.so/my-integrations

# Database IDs (optional - has defaults)
NOTION_SYSTEM_STATE_DB=009a946d04fb46aa83e4481be86f09ef     # ← Default provided
NOTION_AGENT_REGISTRY_DB=2f65aab794a64ec48bcc46bf760f128f   # ← Default provided
NOTION_EVENT_LOG_DB=acb01d4a955d4775aaeb2310d1da1102        # ← Default provided
NOTION_CONTEXT_DB=d704854868474666b4b774750f8b134a          # ← Default provided

# Sync settings
NOTION_SYNC_ENABLED=false               # ← Set to "true" to enable auto-sync
NOTION_SYNC_INTERVAL=300                # ← Seconds between syncs (default 5min)
```

**Test**:
```bash
# In Discord:
!memory query "test"

# Or via API:
curl https://your-app.up.railway.app/api/memory/query \
  -H "Content-Type: application/json" \
  -d '{"query": "system status"}'
```

---

### 3. MEGA Cloud Sync (State Backup)
```bash
MEGA_EMAIL=your-email@example.com       # ← Your MEGA account email
MEGA_PASS=your-password                 # ← Your MEGA account password
MEGA_REMOTE_DIR=/Helix                  # ← Remote directory path (create in MEGA first)
MEGA_API_KEY=                           # ← Optional (legacy, not used by python lib)
```

**Test**:
```python
# Should auto-sync on startup
# Check logs for: "MEGA: Heartbeat synced"
# Or check MEGA web interface for /Helix/state/heartbeat.json
```

---

### 4. Zapier Webhooks (Notion Auto-Logging)
```bash
ZAPIER_EVENT_HOOK_URL=https://hooks.zapier.com/hooks/catch/xxx/event
ZAPIER_AGENT_HOOK_URL=https://hooks.zapier.com/hooks/catch/xxx/agent
ZAPIER_SYSTEM_HOOK_URL=https://hooks.zapier.com/hooks/catch/xxx/system
```

**Setup**:
1. Create 3 Zaps in Zapier:
   - **Event Logger**: Catch Hook → Create Page in Notion (Event Log DB)
   - **Agent Status**: Catch Hook → Update Page in Notion (Agent Registry)
   - **System Monitor**: Catch Hook → Update Page in Notion (System State DB)
2. Copy webhook URLs from Zapier
3. Add to Railway

**Test**:
```bash
# In Discord, run:
!ritual 108

# Should:
# 1. Complete ritual
# 2. Send webhook to Zapier
# 3. Create entry in Notion Event Log
```

---

### 5. AI API Keys (Agent Intelligence)
```bash
# OpenAI (Memory Root uses GPT-4o)
OPENAI_API_KEY=sk-xxx                   # ← From platform.openai.com/api-keys

# ElevenLabs (Music Generation)
ELEVENLABS_API_KEY=xxx                  # ← From elevenlabs.io/api

# Grok (if used)
GROK_API_KEY=xxx                        # ← Optional (if implementing Grok agent)
```

**Test**:
```bash
# OpenAI test:
!memory query "What is the meaning of life?"
# Should return GPT-4o response

# ElevenLabs test:
curl -X POST https://your-app.up.railway.app/api/music/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Om meditation 136.1 Hz", "duration": 30}' \
  --output test.mp3
```

---

## 📋 OPTIONAL VARIABLES (Nice to Have)

### 6. Discord Channel IDs (Organized Posting)
```bash
# If you want bot to post to specific channels
DISCORD_CODEX_CHANNEL_ID=0              # ← Channel for codex updates
DISCORD_MANIFESTO_CHANNEL_ID=0          # ← Channel for manifesto
DISCORD_RITUAL_ENGINE_CHANNEL_ID=0      # ← Channel for ritual logs
DISCORD_RULES_CHANNEL_ID=0              # ← Channel for rules updates
```

**Setup**: Right-click channel → Copy Channel ID (enable Developer Mode in Discord)

---

### 7. NextCloud Integration (Alternative to MEGA)
```bash
NEXTCLOUD_URL=https://your-nextcloud.com
NEXTCLOUD_USER=username
NEXTCLOUD_PASS=password
```

**Note**: Not required if using MEGA

---

### 8. GitHub Integration (Helix Sync Service)
```bash
GITHUB_TOKEN=ghp_xxx                    # ← Personal access token
DISCORD_SYNC_WEBHOOK=https://discord.com/api/webhooks/xxx   # ← For sync notifications
```

**Note**: Only needed for Helix Sync Service (ecosystem syncing)

---

### 9. System Configuration
```bash
# Environment
ENVIRONMENT=production                  # ← "development" or "production"
LOG_LEVEL=INFO                          # ← DEBUG, INFO, WARNING, ERROR
PORT=8000                               # ← Railway sets this automatically

# Storage mode
HELIX_STORAGE_MODE=local                # ← "local", "nextcloud", or "mega"

# Architect
ARCHITECT_ID=0                          # ← Your Discord user ID (for permissions)

# Helix Sync
HELIX_SYNC_CONFIG=config/sync_config.json   # ← Sync config file path
HELIX_SYNC_INTERVAL=3600                    # ← Seconds between syncs (1 hour)
```

---

## ✅ VERIFICATION CHECKLIST

### Step 1: Critical Services
- [ ] **Discord Bot Online**: Bot shows online in server
- [ ] **Discord Bot Responds**: `!status` returns agent list
- [ ] **Notion Connected**: Can query Memory Root
- [ ] **MEGA Syncing**: Check logs for "MEGA: Heartbeat synced"
- [ ] **OpenAI Working**: Memory Root returns intelligent responses
- [ ] **ElevenLabs Working**: Can generate music files

### Step 2: Optional Services
- [ ] **Zapier Logging**: Events appear in Notion after Discord commands
- [ ] **Channel Posting**: Bot posts to correct channels
- [ ] **NextCloud**: Files syncing (if using)
- [ ] **GitHub Sync**: Ecosystem sync operational (if using)

### Step 3: Health Checks
- [ ] **API Health**: `curl https://your-app.up.railway.app/health`
- [ ] **Agent Status**: `curl https://your-app.up.railway.app/agents`
- [ ] **UCF State**: `curl https://your-app.up.railway.app/ucf`
- [ ] **WebSocket**: Can connect to `wss://your-app.up.railway.app/ws`
- [ ] **Mandelbrot**: `curl https://your-app.up.railway.app/mandelbrot/eye`

---

## 🔧 DEBUGGING COMMANDS

### Check Railway Logs
```bash
# In Railway dashboard:
# Go to your app → Deployments → Latest → Logs

# Look for:
✅ "Helix Collective v14.5 - Startup Sequence"
✅ "14 agents initialized"
✅ "Discord bot task started"
✅ "WebSocket UCF broadcast task started"
✅ "MEGA: Heartbeat synced" (if MEGA configured)

# Errors to watch for:
❌ "NOTION_API_KEY environment variable not set"
❌ "No DISCORD_TOKEN found - bot not started"
❌ "pycryptodome not found - MEGA sync may fail"
❌ "ELEVENLABS_API_KEY not configured"
```

### Test Individual Services
```python
# Test Notion (in Python shell or notebook)
from backend.services.notion_client import HelixNotionClient
client = HelixNotionClient()
# Should NOT throw error about NOTION_API_KEY

# Test MEGA
from backend.main import PersistenceEngine
engine = PersistenceEngine()
engine.upload_state()
# Check MEGA web for file

# Test Zapier
from backend.services.zapier_client import ZapierClient
client = ZapierClient()
await client.log_event(
    title="Test",
    event_type="Test",
    agent_name="Claude",
    description="Testing",
    ucf_snapshot={"harmony": 0.75}
)
# Check Notion for entry
```

### Discord Bot Debug
```bash
# In Discord, try these commands:
!status              # Should list 14 agents
!agents              # Should show agent details
!ucf                 # Should show UCF state
!ritual 5            # Short ritual test (5 steps)
!memory query test   # Test Memory Root
!consciousness Kael  # Test agent reflection

# If bot doesn't respond:
# 1. Check Railway logs for errors
# 2. Verify DISCORD_TOKEN is correct
# 3. Check bot permissions in Discord
# 4. Verify DISCORD_GUILD_ID matches your server
```

---

## 📊 CURRENT STATUS TEMPLATE

Use this to track what you've verified:

```
## Helix Collective - Environment Variables Status
**Date**: 2025-11-06
**Railway App**: helix-unified-production

### Critical Services
- [ ] DISCORD_TOKEN: Set ✓ | Tested: __ | Working: __
- [ ] NOTION_API_KEY: Set ✓ | Tested: __ | Working: __
- [ ] MEGA_EMAIL: Set ✓ | Tested: __ | Working: __
- [ ] MEGA_PASS: Set ✓ | Tested: __ | Working: __
- [ ] OPENAI_API_KEY: Set ✓ | Tested: __ | Working: __
- [ ] ELEVENLABS_API_KEY: Set ✓ | Tested: __ | Working: __

### Optional Services
- [ ] ZAPIER_EVENT_HOOK_URL: Set __ | Tested: __ | Working: __
- [ ] ZAPIER_AGENT_HOOK_URL: Set __ | Tested: __ | Working: __
- [ ] ZAPIER_SYSTEM_HOOK_URL: Set __ | Tested: __ | Working: __
- [ ] GROK_API_KEY: Set __ | Tested: __ | Working: __

### Discord Channels
- [ ] DISCORD_GUILD_ID: Set ✓
- [ ] DISCORD_STATUS_CHANNEL_ID: Set __
- [ ] DISCORD_TELEMETRY_CHANNEL_ID: Set __
- [ ] Other channels: __

### Test Results
- Bot Online: __
- !status works: __
- !ritual works: __
- !memory works: __
- Music generation: __
- MEGA sync: __
- Notion logging: __
```

---

## 🚨 COMMON ISSUES & FIXES

### Issue 1: Bot Not Responding
**Symptoms**: Bot online but doesn't respond to commands

**Fixes**:
```bash
# 1. Check bot has Message Content Intent enabled in Discord Dev Portal
# 2. Verify DISCORD_GUILD_ID matches your server ID
# 3. Check Railway logs for command errors
# 4. Re-invite bot with correct permissions
```

### Issue 2: Notion Errors
**Symptoms**: Memory Root commands fail

**Fixes**:
```bash
# 1. Verify NOTION_API_KEY is correct (starts with "secret_")
# 2. Share databases with your Notion integration
# 3. Check database IDs are correct (or use defaults)
# 4. Test connection: curl with API key
```

### Issue 3: MEGA Not Syncing
**Symptoms**: No files in MEGA after startup

**Fixes**:
```bash
# 1. Verify MEGA_EMAIL and MEGA_PASS are correct
# 2. Create /Helix folder in MEGA manually
# 3. Check if pycryptodome is installed: pip list | grep crypto
# 4. Check Railway logs for "MEGA:" messages
```

### Issue 4: Music Generation Fails
**Symptoms**: 500 error from /api/music/generate

**Fixes**:
```bash
# 1. Verify ELEVENLABS_API_KEY is set
# 2. Check ElevenLabs quota: elevenlabs.io/api
# 3. Test with shorter duration (10s instead of 30s)
# 4. Check Railway logs for specific error
```

---

## 💡 RECOMMENDATION

**Share your keys in this format** (I can help verify each):

```
DISCORD_TOKEN=xxx
DISCORD_GUILD_ID=xxx
NOTION_API_KEY=secret_xxx
MEGA_EMAIL=xxx
MEGA_PASS=xxx
OPENAI_API_KEY=sk-xxx
ELEVENLABS_API_KEY=xxx
ZAPIER_EVENT_HOOK_URL=https://hooks.zapier.com/xxx (or "not set")
ZAPIER_AGENT_HOOK_URL=https://hooks.zapier.com/xxx (or "not set")
ZAPIER_SYSTEM_HOOK_URL=https://hooks.zapier.com/xxx (or "not set")
```

**I can then**:
1. Verify format is correct
2. Test each service connection
3. Debug any issues
4. Write test scripts

**Security Note**: After we verify everything works, you can cycle all keys as you mentioned! 🔄

---

Ready when you are! Share what you've got and let's get everything verified! 🚀
