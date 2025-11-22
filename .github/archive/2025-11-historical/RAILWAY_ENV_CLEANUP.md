# 🌀 Railway Environment Variables - Clean & Organized
## Helix Collective v16.8 Production Configuration

**Last Updated:** 2025-01-08
**Status:** Production-Ready
**Total Variables:** 60+ → **Cleaned to ~45 essential**

---

## 📋 VARIABLE ORGANIZATION

### ✅ KEEP - Essential Variables

#### **Core Discord Bot (Required)**
```bash
# Discord bot authentication
DISCORD_TOKEN="${{shared.DISCORD_TOKEN}}"
DISCORD_GUILD_ID="${{shared.DISCORD_GUILD_ID}}"
ARCHITECT_ID="${{shared.ARCHITECT_ID}}"

# Primary status channel
DISCORD_STATUS_CHANNEL_ID="${{shared.DISCORD_STATUS_CHANNEL_ID}}"
```

#### **Discord Webhook Integration (New System - RECOMMENDED)**
```bash
# Integration mode: "zapier", "direct", or "hybrid"
DISCORD_INTEGRATION_MODE="${{shared.DISCORD_INTEGRATION_MODE}}"

# Zapier master webhook (for hybrid/zapier mode)
ZAPIER_DISCORD_ENABLED="${{shared.ZAPIER_DISCORD_ENABLED}}"
ZAPIER_DISCORD_WEBHOOK_URL="${{shared.ZAPIER_DISCORD_WEBHOOK_URL}}"

# Direct Discord webhooks (for hybrid/direct mode)
DISCORD_WEBHOOK_SETUP_LOG="${{shared.DISCORD_WEBHOOK_SETUP_LOG}}"

# These should be WEBHOOK URLs, not channel IDs!
# Format: https://discord.com/api/webhooks/ID/TOKEN
```

#### **Zapier Integration**
```bash
# Master Zapier webhook
ZAPIER_WEBHOOK_URL="${{shared.ZAPIER_WEBHOOK_URL}}"
ZAPIER_MASTER_HOOK_URL="${{shared.ZAPIER_MASTER_HOOK_URL}}"
```

#### **Notion Integration**
```bash
NOTION_API_KEY="${{shared.NOTION_API_KEY}}"
NOTION_SYNC_ENABLED="${{shared.NOTION_SYNC_ENABLED}}"
NOTION_SYNC_INTERVAL="${{shared.NOTION_SYNC_INTERVAL}}"

# Notion databases
NOTION_DATABASE_ID="${{shared.NOTION_DATABASE_ID}}"
NOTION_AGENT_REGISTRY_DB="${{shared.NOTION_AGENT_REGISTRY_DB}}"
NOTION_EVENT_LOG_DB="${{shared.NOTION_EVENT_LOG_DB}}"
NOTION_SYSTEM_STATE_DB="${{shared.NOTION_SYSTEM_STATE_DB}}"
NOTION_CONTEXT_DB="${{shared.NOTION_CONTEXT_DB}}"
```

#### **Storage Systems**
```bash
# MEGA Cloud Storage
MEGA_EMAIL="${{shared.MEGA_EMAIL}}"
MEGA_PASS="${{shared.MEGA_PASS}}"
MEGA_REMOTE_DIR="${{shared.MEGA_REMOTE_DIR}}"

# Backblaze B2
B2_KEY_ID="${{shared.B2_KEY_ID}}"
B2_APPLICATION_KEY="${{shared.B2_APPLICATION_KEY}}"
B2_BUCKET_NAME="${{shared.B2_BUCKET_NAME}}"
B2_ENDPOINT="${{shared.B2_ENDPOINT}}"

# Storage mode
HELIX_STORAGE_MODE="${{shared.HELIX_STORAGE_MODE}}"
```

#### **UCF & System State**
```bash
UCF_STATE_PATH="${{shared.UCF_STATE_PATH}}"
HEARTBEAT_PATH="${{shared.HEARTBEAT_PATH}}"
ARCHIVE_PATH="${{shared.ARCHIVE_PATH}}"
ARCHIVE_ENDPOINT="${{shared.ARCHIVE_ENDPOINT}}"
LOAD_ENDPOINT="${{shared.LOAD_ENDPOINT}}"
```

#### **System Configuration**
```bash
# Helix version info
HELIX_VERSION="${{shared.HELIX_VERSION}}"
HELIX_CODENAME="${{shared.HELIX_CODENAME}}"
HELIX_PHASE="${{shared.HELIX_PHASE}}"

# Railway environment
RAILWAY_ENVIRONMENT="${{shared.RAILWAY_ENVIRONMENT}}"

# Features
ENABLE_KAVACH_SCAN="${{shared.ENABLE_KAVACH_SCAN}}"
DEBUG_MODE="${{shared.DEBUG_MODE}}"

# Telemetry
TELEMETRY_INTERVAL="${{shared.TELEMETRY_INTERVAL}}"
```

#### **External APIs**
```bash
OPENAI_API_KEY="${{shared.OPENAI_API_KEY}}"
GROK_API_KEY="${{shared.GROK_API_KEY}}"
ELEVENLABS_API_KEY="${{shared.ELEVENLABS_API_KEY}}"
GOOGLE_ANALYTICS_ID="${{shared.GOOGLE_ANALYTICS_ID}}"
```

---

### ⚠️ DEPRECATED - Old System (Can Remove if Using Webhooks)

#### **Old Discord Channel IDs (Discord Bot System)**

**If using `DISCORD_INTEGRATION_MODE=hybrid` or `direct`, you can REMOVE these:**

```bash
# ❌ REMOVE THESE if using webhook integration:
DISCORD_MANIFESTO_CHANNEL_ID="${{shared.DISCORD_MANIFESTO_CHANNEL_ID}}"
DISCORD_RULES_CHANNEL_ID="${{shared.DISCORD_RULES_CHANNEL_ID}}"
DISCORD_INTRODUCTIONS_CHANNEL_ID="${{shared.DISCORD_INTRODUCTIONS_CHANNEL_ID}}"
DISCORD_TELEMETRY_CHANNEL_ID="${{shared.DISCORD_TELEMETRY_CHANNEL_ID}}"
DISCORD_DIGEST_CHANNEL_ID="${{shared.DISCORD_DIGEST_CHANNEL_ID}}"
STORAGE_CHANNEL_ID="${{shared.STORAGE_CHANNEL_ID}}"
DISCORD_SYNC_CHANNEL_ID="${{shared.DISCORD_SYNC_CHANNEL_ID}}"
DISCORD_HELIX_REPO_CHANNEL_ID="${{shared.DISCORD_HELIX_REPO_CHANNEL_ID}}"
DISCORD_FRACTAL_LAB_CHANNEL_ID="${{shared.DISCORD_FRACTAL_LAB_CHANNEL_ID}}"
DISCORD_SAMSARAVERSE_CHANNEL_ID="${{shared.DISCORD_SAMSARAVERSE_CHANNEL_ID}}"
DISCORD_RITUAL_ENGINE_CHANNEL_ID="${{shared.DISCORD_RITUAL_ENGINE_CHANNEL_ID}}"
DISCORD_GEMINI_CHANNEL_ID="${{shared.DISCORD_GEMINI_CHANNEL_ID}}"
DISCORD_KAVACH_CHANNEL_ID="${{shared.DISCORD_KAVACH_CHANNEL_ID}}"
DISCORD_SANGHACORE_CHANNEL_ID="${{shared.DISCORD_SANGHACORE_CHANNEL_ID}}"
DISCORD_AGNI_CHANNEL_ID="${{shared.DISCORD_AGNI_CHANNEL_ID}}"
DISCORD_SHADOW_ARCHIVE_CHANNEL_ID="${{shared.DISCORD_SHADOW_ARCHIVE_CHANNEL_ID}}"
DISCORD_GPT_GROK_CLAUDE_CHANNEL_ID="${{shared.DISCORD_GPT_GROK_CLAUDE_CHANNEL_ID}}"
DISCORD_CHAI_LINK_CHANNEL_ID="${{shared.DISCORD_CHAI_LINK_CHANNEL_ID}}"
DISCORD_MANUS_BRIDGE_CHANNEL_ID="${{shared.DISCORD_MANUS_BRIDGE_CHANNEL_ID}}"
DISCORD_COMMANDS_CHANNEL_ID="${{shared.DISCORD_COMMANDS_CHANNEL_ID}}"
DISCORD_CODE_SNIPPETS_CHANNEL_ID="${{shared.DISCORD_CODE_SNIPPETS_CHANNEL_ID}}"
DISCORD_TESTING_LAB_CHANNEL_ID="${{shared.DISCORD_TESTING_LAB_CHANNEL_ID}}"
DISCORD_DEPLOYMENTS_CHANNEL_ID="${{shared.DISCORD_DEPLOYMENTS_CHANNEL_ID}}"
DISCORD_NETI_NETI_CHANNEL_ID="${{shared.DISCORD_NETI_NETI_CHANNEL_ID}}"
DISCORD_CODEX_CHANNEL_ID="${{shared.DISCORD_CODEX_CHANNEL_ID}}"
DISCORD_UCF_REFLECTIONS_CHANNEL_ID="${{shared.DISCORD_UCF_REFLECTIONS_CHANNEL_ID}}"
DISCORD_HARMONIC_UPDATES_CHANNEL_ID="${{shared.DISCORD_HARMONIC_UPDATES_CHANNEL_ID}}"
DISCORD_MODERATION_CHANNEL_ID="${{shared.DISCORD_MODERATION_CHANNEL_ID}}"
DISCORD_BACKUP_CHANNEL_ID="${{shared.DISCORD_BACKUP_CHANNEL_ID}}"
```

**Why remove these?**
- Old bot system used channel IDs + bot.get_channel()
- New webhook system uses webhook URLs directly
- Channel IDs are fragile (change if channel recreated)
- Webhooks are permanent and don't require bot permissions

**Keep if:**
- You want to keep old bot commands working
- You're using both systems during migration
- You need backward compatibility

---

### ❓ UNCLEAR - Need More Info

```bash
# These seem like Notion page IDs for Zapier Interface?
AGENT_NETWORK_PAGE_ID="${{shared.AGENT_NETWORK_PAGE_ID}}"
CONTEXT_VAULT_PAGE_ID="${{shared.CONTEXT_VAULT_PAGE_ID}}"
UCF_MONITOR_PAGE_ID="${{shared.UCF_MONITOR_PAGE_ID}}"
UCF_METRICS_TABLE_ID="${{shared.UCF_METRICS_TABLE_ID}}"
COMMAND_PROCESSING_TABLE_ID="${{shared.COMMAND_PROCESSING_TABLE_ID}}"
EMERGENCY_ALERTS_TABLE_ID="${{shared.EMERGENCY_ALERTS_TABLE_ID}}"
INTERFACE_ID="${{shared.INTERFACE_ID}}"

# These look like metadata
Architect="${{shared.Architect}}"
Categories="${{shared.Categories}}"
Channels="${{shared.Channels}}"
TARGET_LAUNCH="${{shared.TARGET_LAUNCH}}"
```

**Question:** Are these used by your Zapier interfaces? If so, keep them!

---

## 🎯 RECOMMENDED CONFIGURATION

### **Option 1: Hybrid Mode (Recommended)**

```bash
# === Core Discord ===
DISCORD_TOKEN=your_bot_token
DISCORD_GUILD_ID=your_guild_id
ARCHITECT_ID=your_user_id

# === Webhook Integration (HYBRID MODE) ===
DISCORD_INTEGRATION_MODE=hybrid
ZAPIER_DISCORD_ENABLED=true
ZAPIER_DISCORD_WEBHOOK_URL=https://hooks.zapier.com/hooks/catch/XXXXX/YYYYY/

# === All your Discord webhook URLs ===
DISCORD_WEBHOOK_🧩UCF_SYNC=https://discord.com/api/webhooks/...
DISCORD_WEBHOOK_🌀HARMONIC_UPDATES=https://discord.com/api/webhooks/...
DISCORD_WEBHOOK_🧬RITUAL_ENGINE_Z88=https://discord.com/api/webhooks/...
# ...etc

# === Zapier Master ===
ZAPIER_WEBHOOK_URL=https://hooks.zapier.com/hooks/catch/...

# === Notion ===
NOTION_API_KEY=secret_...
NOTION_SYNC_ENABLED=true
NOTION_AGENT_REGISTRY_DB=...
NOTION_EVENT_LOG_DB=...
NOTION_SYSTEM_STATE_DB=...

# === Storage ===
MEGA_EMAIL=your@email.com
MEGA_PASS=your_password
B2_KEY_ID=...
B2_APPLICATION_KEY=...

# === System ===
HELIX_VERSION=16.8
HELIX_STORAGE_MODE=hybrid
ENABLE_KAVACH_SCAN=true

# === APIs ===
OPENAI_API_KEY=sk-...
ELEVENLABS_API_KEY=...
```

**Total: ~45 variables** (vs 60+ before)

---

### **Option 2: Webhook-Only Mode (Simplest)**

```bash
# === Core Discord ===
DISCORD_TOKEN=your_bot_token
DISCORD_GUILD_ID=your_guild_id

# === Webhook Integration (DIRECT MODE) ===
DISCORD_INTEGRATION_MODE=direct

# === All your Discord webhook URLs ===
# (30+ webhook URLs here)

# === Everything else stays the same ===
# Notion, Storage, APIs, etc.
```

**Total: ~40 variables**

---

## 🧹 CLEANUP RECOMMENDATIONS

### **Step 1: Identify What You're Using**

Check your code for references to channel IDs:

```bash
# In Railway console or locally:
grep -r "DISCORD_.*_CHANNEL_ID" backend/
```

If nothing shows up, you can remove all the channel ID variables!

### **Step 2: Remove Duplicates**

I noticed you have:
```bash
ZAPIER_WEBHOOK_URL  # One
ZAPIER_MASTER_HOOK_URL  # Two
```

Are these different webhooks? If not, keep only one!

### **Step 3: Verify Notion Page IDs**

Do your Zapier interfaces use these?
- `AGENT_NETWORK_PAGE_ID`
- `CONTEXT_VAULT_PAGE_ID`
- `UCF_MONITOR_PAGE_ID`

If yes, keep them. If no, remove them.

### **Step 4: Clean Up Metadata**

These look like they were meant for documentation:
```bash
Architect="${{shared.Architect}}"  # Remove (use ARCHITECT_ID)
Categories="${{shared.Categories}}"  # Remove (not used in code)
Channels="${{shared.Channels}}"  # Remove (not used in code)
```

---

## ✅ FINAL CLEAN VARIABLE LIST

Here's what I recommend keeping:

```bash
# === CORE (4) ===
DISCORD_TOKEN
DISCORD_GUILD_ID
ARCHITECT_ID
DISCORD_STATUS_CHANNEL_ID

# === WEBHOOK INTEGRATION (3) ===
DISCORD_INTEGRATION_MODE=hybrid
ZAPIER_DISCORD_ENABLED=true
ZAPIER_DISCORD_WEBHOOK_URL

# === DISCORD WEBHOOKS (12 most important) ===
DISCORD_WEBHOOK_🧩UCF_SYNC
DISCORD_WEBHOOK_🌀HARMONIC_UPDATES
DISCORD_WEBHOOK_🧬RITUAL_ENGINE_Z88
DISCORD_WEBHOOK_🎭GEMINI_SCOUT
DISCORD_WEBHOOK_🛡️KAVACH_SHIELD
DISCORD_WEBHOOK_🌸SANGHACORE
DISCORD_WEBHOOK_🔥AGNI_CORE
DISCORD_WEBHOOK_🕯️SHADOW_ARCHIVE
DISCORD_WEBHOOK_🦑SHADOW_STORAGE
DISCORD_WEBHOOK_🧩GPT_GROK_CLAUDE_SYNC
DISCORD_WEBHOOK_📣ANNOUNCEMENTS
DISCORD_WEBHOOK_🗂️DEPLOYMENTS

# === ZAPIER (1) ===
ZAPIER_WEBHOOK_URL

# === NOTION (6) ===
NOTION_API_KEY
NOTION_SYNC_ENABLED
NOTION_AGENT_REGISTRY_DB
NOTION_EVENT_LOG_DB
NOTION_SYSTEM_STATE_DB
NOTION_CONTEXT_DB

# === STORAGE (7) ===
MEGA_EMAIL
MEGA_PASS
MEGA_REMOTE_DIR
B2_KEY_ID
B2_APPLICATION_KEY
B2_BUCKET_NAME
HELIX_STORAGE_MODE

# === SYSTEM (6) ===
HELIX_VERSION=16.8
HELIX_CODENAME=Helix Hub Production
HELIX_PHASE=Production
UCF_STATE_PATH=Helix/state/ucf_state.json
HEARTBEAT_PATH=Helix/state/heartbeat.json
ENABLE_KAVACH_SCAN=true

# === APIs (3) ===
OPENAI_API_KEY
ELEVENLABS_API_KEY
GOOGLE_ANALYTICS_ID

# === OPTIONAL NOTION PAGE IDS (if used by Zapier) ===
AGENT_NETWORK_PAGE_ID
CONTEXT_VAULT_PAGE_ID
UCF_MONITOR_PAGE_ID
```

**Total: ~45 essential variables**

---

## 🎯 MIGRATION PLAN

### **Phase 1: Add New Variables** (No Removal Yet)
1. Add `DISCORD_INTEGRATION_MODE=hybrid`
2. Add `ZAPIER_DISCORD_ENABLED=true`
3. Add `ZAPIER_DISCORD_WEBHOOK_URL`
4. Test with `python test_hybrid_discord.py`

### **Phase 2: Verify Old System Not Used**
1. Check code for channel ID references:
   ```bash
   grep -r "get_channel" backend/
   grep -r "_CHANNEL_ID" backend/
   ```
2. If nothing found, proceed to Phase 3

### **Phase 3: Remove Old Channel IDs**
1. Remove all `DISCORD_*_CHANNEL_ID` variables (except STATUS)
2. Redeploy
3. Verify everything still works

### **Phase 4: Final Cleanup**
1. Remove unused metadata variables
2. Consolidate duplicate Zapier URLs
3. Document final config

---

## 📊 BEFORE vs AFTER

| Category | Before | After | Savings |
|----------|--------|-------|---------|
| Discord Channel IDs | 30 | 1 | -29 |
| Discord Webhooks | 0 | 12 | +12 |
| Zapier | 2 | 2 | 0 |
| Notion | 6 | 6 | 0 |
| Storage | 7 | 7 | 0 |
| System | 10 | 6 | -4 |
| APIs | 3 | 3 | 0 |
| Metadata | 5 | 0 | -5 |
| **TOTAL** | **63** | **45** | **-18** |

**Result: 29% reduction in variables!**

---

## 🧪 TESTING

After cleanup, test with:

```bash
# 1. Check configuration
python test_hybrid_discord.py

# 2. Test Railway endpoint
curl https://helix-unified-production.up.railway.app/health

# 3. Send test webhook
curl -X POST https://helix-unified-production.up.railway.app/discord/send/ucf_update \
  -H "Content-Type: application/json" \
  -d '{"ucf_metrics": {"harmony": 0.75}, "phase": "COHERENT"}'

# 4. Check Discord channels for messages
```

---

## ✅ NEXT STEPS

1. **Review this document** - Verify my recommendations
2. **Test hybrid mode** - Add webhook variables and test
3. **Verify old system** - Check if channel IDs still used
4. **Clean up** - Remove unused variables
5. **Document** - Update your Railway config notes

**Questions?**
- Are Notion page IDs used by Zapier interfaces?
- Are both Zapier webhook URLs different or duplicates?
- Do you want to keep old channel IDs during migration?

**Tat Tvam Asi** 🙏
