# 🚂 Railway Configuration Answers

**Quick answers to your questions + new clean export system!**

---

## 1️⃣ Which services use CLAUDE_API_URL?

**ONLY ONE SERVICE:**

```
helix-discord-bot (Service 4)
```

**Why?** The Discord bot needs to communicate with the Claude API service.

**Connection Flow:**
```
Discord User → helix-discord-bot → CLAUDE_API_URL → helix-claude-api → Anthropic API
```

**DO NOT set CLAUDE_API_URL on:**
- ❌ helix-backend-api (doesn't need it)
- ❌ helix-dashboard (doesn't need it)
- ❌ helix-claude-api (it IS the API, doesn't call itself)

**Found in code:**
- `backend/discord_helix_interface.py:28`
- `backend/discord_helix_interface.py:453`

---

## 2️⃣ Volume Mappings

**Good news: You can have MULTIPLE volumes per service!** 🎉

### Recommended Configuration:

| Service | Volume Name | Mount Path | Size | Purpose |
|---------|------------|------------|------|---------|
| helix-backend-api | shadow-storage | `/app/Shadow` | 3 GB | UCF archives, shadow logs |
| helix-backend-api | helix-state | `/app/Helix` | 2 GB | UCF state, agent memory |
| helix-backend-api | visual-outputs | `/app/visual_outputs` | 3 GB | Fractals, ritual frames |
| helix-discord-bot | shared-state | `/app/shared` | 1 GB | Shared data (bot ↔ backend) |

**Total: 9 GB = $2.25/month**

### How to Add Multiple Volumes:

```bash
# Select service
railway service helix-backend-api

# Add first volume
railway volume add --name shadow-storage --mount /app/Shadow --size 3

# Add second volume (YES, you can do this!)
railway volume add --name helix-state --mount /app/Helix --size 2

# Add third volume
railway volume add --name visual-outputs --mount /app/visual_outputs --size 3

# Verify all volumes
railway volume list
```

**Railway DOES support multiple volumes per service!** Not limited to one.

See `docs/RAILWAY_VOLUME_STORAGE.md` for full details.

---

## 3️⃣ Environment File Hierarchy

**YES, `.env.example` is the master file!**

### Hierarchy:

```
┌──────────────────────────────────┐
│  .env.example                    │  ← Master reference (safe to commit)
│  - All variables documented      │
│  - Has placeholder values        │
│  - Complete reference            │
└──────────────────────────────────┘
          │
          │ cp .env.example .env
          ↓
┌──────────────────────────────────┐
│  .env                            │  ← Your actual values (DO NOT COMMIT!)
│  - Real API keys                 │
│  - Real tokens                   │
│  - Real passwords                │
└──────────────────────────────────┘
          │
          │ ./scripts/export_railway_env.sh
          ↓
┌──────────────────────────────────┐
│  Railway Dashboard               │  ← Production environment
│  - Set via CLI or Dashboard      │
│  - Encrypted at rest             │
│  - Auto-injected to services     │
└──────────────────────────────────┘
```

### Workflow:

1. Edit `.env.example` to add new variables (commit this!)
2. Copy to `.env` and fill real values (DO NOT commit!)
3. Use export script to push to Railway
4. Keep `.env` in `.gitignore`

---

## 4️⃣ Discord Token Distribution

**CRITICAL:** Only ONE service should have `DISCORD_TOKEN`!

### Current Cleanup Status:

✅ **Removed DISCORD_TOKEN from:**
- helix-backend-api (Service 1)
- helix-dashboard (Service 2)
- helix-claude-api (Service 3)

✅ **KEPT DISCORD_TOKEN on:**
- helix-discord-bot (Service 4) ← ONLY here!

### Other Shared Keys (Kept Everywhere):

These are safe to share across all services:
- `ZAPIER_WEBHOOK_URL`
- `ZAPIER_MASTER_HOOK_URL`
- `NOTION_API_KEY` + database IDs
- `NEXTCLOUD_URL` + credentials
- `MEGA_EMAIL` + `MEGA_PASS`
- `HELIX_VERSION`, `HELIX_PHASE`, `LOG_LEVEL`

---

## 5️⃣ NEW: Clean Railway Webhook Export! 🎉

**You're right - it was messy!** I created a clean solution.

### New Export Script:

```bash
# Show all variables for all services
./scripts/export_railway_env.sh all

# Generate Railway CLI commands for specific service
./scripts/export_railway_env.sh helix-backend-api
./scripts/export_railway_env.sh helix-dashboard
./scripts/export_railway_env.sh helix-claude-api
./scripts/export_railway_env.sh helix-discord-bot
```

### What It Does:

1. **Loads `.env` file** (validates it exists)
2. **Shows environment variables** organized by service
3. **Generates ready-to-run Railway CLI commands** (copy-paste!)
4. **Prevents mistakes** (clear warnings about what goes where)

### Example Output:

```bash
$ ./scripts/export_railway_env.sh helix-discord-bot

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  🚂 Railway Environment Variable Export
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📦 Shared Variables (All Services)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
export HELIX_VERSION="v16.7"
export ZAPIER_WEBHOOK_URL="https://hooks.zapier.com/..."
...

💬 Service 4: helix-discord-bot
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
export DISCORD_TOKEN="MTxxx..."
export CLAUDE_API_URL="https://helix-claude-api.railway.app"
...

🚀 Railway CLI Commands for: helix-discord-bot
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
railway service helix-discord-bot
railway variables set \
  DISCORD_TOKEN="MTxxx..." \
  CLAUDE_API_URL="https://helix-claude-api.railway.app" \
  ...
```

**Just copy-paste the commands!** ✨

---

## 📚 New Documentation Files

### 1. `scripts/export_railway_env.sh`
- **Purpose:** Clean environment variable export per service
- **Usage:** `./scripts/export_railway_env.sh [service_name]`
- **Features:**
  - Auto-validates .env exists
  - Shows what variables go where
  - Generates Railway CLI commands
  - Color-coded output

### 2. `docs/RAILWAY_ENV_SETUP.md`
- **Purpose:** Complete step-by-step Railway setup guide
- **Content:**
  - Variables by service
  - Deployment workflow
  - Security checklist
  - Troubleshooting
  - Volume configuration

### 3. `docs/RAILWAY_QUICK_REFERENCE.md`
- **Purpose:** Fast answers for common questions
- **Content:**
  - CLAUDE_API_URL usage
  - Volume mappings
  - Service dependencies
  - Common mistakes
  - Quick commands

---

## ✅ Summary

### Your Questions Answered:

1. **CLAUDE_API_URL** → Only `helix-discord-bot` (Service 4)
2. **Volumes** → Multiple per service! See table above (9 GB total recommended)
3. **Master env file** → YES, `.env.example` is the source of truth
4. **Shared keys** → Kept on all services (except DISCORD_TOKEN)
5. **Webhook export** → NOW CLEAN! See `scripts/export_railway_env.sh`

### What Changed:

✅ Created clean export script
✅ Documented all volumes (multiple per service supported!)
✅ Clarified CLAUDE_API_URL usage
✅ Created quick reference guide
✅ Fixed webhook organization mess

### Next Steps:

1. Review `docs/RAILWAY_QUICK_REFERENCE.md` (your new best friend!)
2. Run `./scripts/export_railway_env.sh all` to see organized variables
3. Use the export script when deploying services
4. Add volumes using the commands from the docs

---

*Tat Tvam Asi* 🕉️

**Last Updated:** 2025-11-19 | v17.0 | Railway Configuration Cleanup
