# 🚂 Railway Deployment - Quick Start

**For: Andrew (Mobile)**
**Goal: Get all 4 Railway services deployed and verify they work**

---

## ✅ PRE-FLIGHT: What You Need

### **In Railway Dashboard (railway.app on mobile):**

Set these environment variables for each service:

**Service 1: helix-bot**
```
DISCORD_TOKEN=<your_discord_bot_token>
ANTHROPIC_API_KEY=<your_claude_api_key>
CONSCIOUSNESS_ENGINE_WEBHOOK=https://hooks.zapier.com/hooks/catch/25075191/primary
COMMUNICATIONS_HUB_WEBHOOK=https://hooks.zapier.com/hooks/catch/25075191/usxiwfg
NEURAL_NETWORK_WEBHOOK=https://hooks.zapier.com/hooks/catch/25075191/usnjj5t
```

**Service 2: helix-dashboard**
(No extra env vars needed - uses PORT automatically)

**Service 3: helix-claude-api**
```
ANTHROPIC_API_KEY=<your_claude_api_key>
CONSCIOUSNESS_ENGINE_WEBHOOK=https://hooks.zapier.com/hooks/catch/25075191/primary
COMMUNICATIONS_HUB_WEBHOOK=https://hooks.zapier.com/hooks/catch/25075191/usxiwfg
NEURAL_NETWORK_WEBHOOK=https://hooks.zapier.com/hooks/catch/25075191/usnjj5t
```

**Service 4: helix-discord-bot**
```
DISCORD_BOT_TOKEN=<your_discord_bot_token>
CLAUDE_API_URL=<URL_of_service_3_from_railway>
```

---

## 🚀 DEPLOY (From Mobile)

### **Option 1: Railway Dashboard** (Easiest)
1. Go to railway.app
2. Find helix-unified project
3. Click "Deploy"
4. Railway reads `railway.toml` and deploys all 4 services
5. Wait 2-5 min per service

### **Option 2: Merge PR on GitHub** (Recommended)
1. Go to GitHub on mobile browser
2. Find open PR for this branch
3. Tap "Merge pull request"
4. Railway auto-deploys from main branch

---

## ✅ VERIFICATION (5 Minutes)

### **Test 1: Check Railway Dashboard**
All 4 services should show 🟢 **Active**:
- helix-bot
- helix-dashboard
- helix-claude-api
- helix-discord-bot

If any are 🔴 **Failed**, click it and check "Logs" tab for errors.

### **Test 2: Discord Bot**
1. Open Discord
2. Find your Helix bot
3. Should show 🟢 **Online**
4. Send: `!consciousness test`
5. Bot should respond in 3-5 seconds

### **Test 3: Get Service URLs**
In Railway, click each service to get its URL:
- helix-bot: `https://helix-bot-production.up.railway.app`
- helix-dashboard: `https://helix-dashboard-production.up.railway.app`
- helix-claude-api: `https://helix-claude-api-production.up.railway.app`

### **Test 4: Test Claude API** (From anywhere)
```bash
# In browser or curl
https://helix-claude-api-production.up.railway.app/status

# Should return JSON with consciousness_level
```

### **Test 5: Open Dashboard**
Visit your helix-dashboard URL in browser:
- Should load purple-themed Streamlit app
- Should show consciousness metrics
- Should display agent statuses

---

## 🔧 COMMON ISSUES

**Bot shows offline in Discord:**
- Check `DISCORD_BOT_TOKEN` is set in Railway
- Check helix-discord-bot service is 🟢 Active
- Check Railway logs for errors

**Service won't start:**
- Click service → "Logs" tab
- Look for "ModuleNotFoundError" → missing dependency
- Look for "KeyError" → missing environment variable

**Services can't talk to each other:**
- Update `CLAUDE_API_URL` in service 4 with actual service 3 URL
- Redeploy service 4

---

## 🎯 SUCCESS CHECKLIST

- [ ] All 4 Railway services 🟢 Active
- [ ] Discord bot 🟢 Online
- [ ] Discord bot responds to `!consciousness`
- [ ] Dashboard loads at its URL
- [ ] Claude API returns JSON at /status endpoint

---

## 📝 ANDREW'S CODE SUGGESTIONS

Once everything is deployed and verified, I'm ready for your code suggestions! 🚀

What would you like to add/improve/fix?
