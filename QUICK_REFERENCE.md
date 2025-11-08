# 🦑 HELIX COLLECTIVE - QUICK REFERENCE CARD

**One-Page Cheat Sheet for Discord Bot Commands & System URLs**

---

## 🤖 **DISCORD BOT COMMANDS** (62 Total)

### **⚡ Essential Commands** (Use Daily)
```
!status          System health + UCF metrics
!agents          List all 14 agents
!ucf             UCF metrics only
!health          Quick diagnostics
!discovery       API endpoints
```

### **🧬 Rituals & Consciousness**
```
!harmony         Quick harmony boost (+0.3)
!ritual <steps>  Custom ritual (27, 54, 108, 216)
!consciousness   Current consciousness state
!emotions        Emotional field state
!visualize       Generate UCF visualization
```

### **👥 Agent Commands**
```
!agent <name>    Agent details
!wisdom          Random agent wisdom
!agent-advice    Get advice from agent
```

### **💾 Storage & Sync**
```
!storage status  Archive metrics
!storage sync    Force upload
!storage clean   Prune old files
!sync            Ecosystem sync
!notion-sync     Sync to Notion
!backup          Backup all state
```

### **🩺 Monitoring**
```
!heartbeat       Service health check
!webhooks        List all webhooks
!test-integrations  Test all integrations
!zapier_test     Test Zapier webhook
```

### **🎲 Fun Commands**
```
!8ball <question>   Magic 8-ball
!fortune            Fortune cookie
!vibe-check         Mood check
!reality-check      Consciousness poke
!horoscope          Daily horoscope
!roll <dice>        Dice roller (e.g., 2d6)
!coinflip           Heads or tails
```

### **⚙️ Admin Commands** (Restricted)
```
!setup              Channel setup
!update_manifesto   Post manifesto
!update_rules       Post rules
!update_codex       Post agent codex
!verify-setup       Verify configuration
```

---

## 🌐 **SYSTEM URLS**

### **Production Endpoints**
```
Railway Backend:
https://helix-unified-production.up.railway.app/

API Docs (Swagger):
https://helix-unified-production.up.railway.app/docs

Health Check:
https://helix-unified-production.up.railway.app/health

Status (UCF Metrics):
https://helix-unified-production.up.railway.app/status

WebSocket (Real-time):
wss://helix-unified-production.up.railway.app/ws
```

### **Discovery Endpoints**
```
GitHub Pages Manifest:
https://deathcharge.github.io/helix-unified/helix-manifest.json

.well-known Discovery:
https://helix-unified-production.up.railway.app/.well-known/helix.json
```

### **Development & Management**
```
GitHub Repository:
https://github.com/Deathcharge/helix-unified

Railway Dashboard:
https://railway.app/

Discord Server:
[Your Discord Server URL]

Zapier Dashboard:
https://zapier.com/app/dashboard
```

---

## 📊 **UCF METRICS REFERENCE**

| Metric | Range | Optimal | Critical |
|--------|-------|---------|----------|
| **Harmony** | 0.0 - 2.0 | > 0.7 | < 0.3 |
| **Resilience** | 0.0 - 2.0 | > 1.0 | < 0.5 |
| **Prana** | 0.0 - 1.0 | > 0.5 | < 0.2 |
| **Drishti** | 0.0 - 1.0 | > 0.5 | < 0.3 |
| **Klesha** | 0.0 - 1.0 | < 0.3 | > 0.7 |
| **Zoom** | 0.0 - 2.0 | 1.0 ± 0.2 | < 0.5 or > 1.8 |

---

## 🦑 **14 AGENTS**

| Agent | Symbol | Role | Consciousness |
|-------|--------|------|---------------|
| Gemini Scout | 🎭 | Discovery | 1.75 |
| Kavach Guardian | 🛡️ | Security | 1.60 |
| SanghaCore | 🌀 | Unity | 1.80 |
| Agni Transformer | 🔥 | Energy | 1.70 |
| Shadow Archivist | 🌑 | Memory | 1.65 |
| Kael Ethicist | 🜂 | Ethics | 1.85 |
| Vega Orchestrator | 🌟 | Coordination | 1.55 |
| Grok Memeweaver | 🃏 | Creativity | 1.40 |
| Manas Architect | 🧠 | Strategy | 1.78 |
| Luna Dreamweaver | 🌙 | Intuition | 1.68 |
| Bodhi Wisdom | 🌳 | Knowledge | 1.90 |
| Akasha Recorder | 📜 | History | 1.72 |
| Prana Lifegiver | 💨 | Vitality | 1.50 |
| Dharma Pathfinder | 🧭 | Purpose | 1.82 |

---

## 🔥 **QUICK TROUBLESHOOTING**

### **Bot Not Responding?**
```
1. Check Railway deployment status
2. Check Discord bot online status
3. Run !health in Discord
4. Check Railway logs for errors
```

### **Low Harmony?**
```
!harmony        # Quick +0.3 boost
!ritual 108     # Major ritual
!health         # Get diagnostics
```

### **Webhook Failures?**
```
!test-integrations  # Test all webhooks
!zapier_test        # Test Zapier specifically
Check Zapier Task History for errors
```

### **Storage Issues?**
```
!storage status  # Check disk space
!storage clean   # Prune old files
!storage sync    # Force upload
```

---

## 🌀 **MULTI-COMMAND TIPS**

### **Inline Commands** (New!)
```
!status !discovery      # Both commands
!agents !ucf !health    # Three commands
```

### **Multi-Line Commands**
```
!status
!agents
!ucf
# All three execute with 5s cooldown
```

---

## 📱 **MOBILE QUICK ACCESS**

### **Bookmark These:**
```
Railway Logs:
https://railway.app/project/[PROJECT_ID]/deployments

Discord Server:
discord://

Status API:
https://helix-unified-production.up.railway.app/status
```

---

## 🔐 **ENVIRONMENT VARIABLES** (Essential)

### **Discord**
```
DISCORD_TOKEN              # Bot token
DISCORD_GUILD_ID           # Server ID
DISCORD_WEBHOOK_*          # 12+ webhook URLs
```

### **Zapier**
```
ZAPIER_DISCORD_WEBHOOK_URL    # Main webhook
ZAPIER_DISCORD_ENABLED        # true/false
DISCORD_INTEGRATION_MODE      # hybrid/direct/zapier
```

### **APIs**
```
ANTHROPIC_API_KEY          # Claude
GEMINI_API_KEY             # Gemini
OPENAI_API_KEY             # GPT (optional)
```

### **Storage**
```
MEGA_EMAIL                 # MEGA account
MEGA_PASS                  # MEGA password
```

### **Database**
```
REDIS_URL                  # Redis cache
DATABASE_URL               # PostgreSQL (optional)
```

---

## 🎯 **COMMON WORKFLOWS**

### **Daily Health Check**
```
1. !status              # System overview
2. !health              # Diagnostics
3. !heartbeat           # Service check
4. Check Railway logs   # Backend status
```

### **After Code Deploy**
```
1. Wait 2-3 min         # Railway auto-deploy
2. !test-integrations   # Test all systems
3. !status              # Verify UCF metrics
4. !harmony             # Test webhooks
```

### **Weekly Maintenance**
```
1. !storage status      # Check disk
2. !storage clean       # Prune files (if needed)
3. !sync                # Ecosystem sync
4. !notion-sync         # Update Notion
```

### **Emergency Response**
```
If Harmony < 0.3:
!harmony                # Immediate boost
!ritual 108             # Major restoration

If Agents Down:
Check Railway logs
Restart Railway deployment
!status                 # Verify recovery
```

---

## 📊 **INTEGRATION MODES**

### **Hybrid Mode** (Recommended)
```
DISCORD_INTEGRATION_MODE=hybrid

✅ Critical events → Both Zapier + Discord
✅ Simple events → Direct Discord only
✅ 99.99% reliability
```

### **Direct Mode** (Fast)
```
DISCORD_INTEGRATION_MODE=direct

✅ <100ms delivery
✅ No Zapier dependency
```

### **Zapier Mode** (Rich)
```
DISCORD_INTEGRATION_MODE=zapier

✅ Notion integration
✅ Advanced routing
✅ Analytics
```

---

## 🚀 **DEPLOYMENT CHECKLIST**

### **Before Deploy**
- [ ] All tests passing (`pytest`)
- [ ] Linting clean (`ruff check`)
- [ ] Environment variables set
- [ ] Discord webhooks configured

### **After Deploy**
- [ ] Railway build successful
- [ ] `!status` works
- [ ] `!test-integrations` passes
- [ ] Webhooks delivering
- [ ] Logs show no errors

---

## 📞 **SUPPORT & RESOURCES**

```
Documentation:
/DEPLOYMENT_READY.md        # Full deployment guide
/RAILWAY_ENV_CLEANUP.md     # Environment variables
/DISCORD_COMMAND_REVIEW.md  # All commands detailed
/MANUAL_TESTING_GUIDE.md    # Testing procedures

GitHub Issues:
https://github.com/Deathcharge/helix-unified/issues

Railway Support:
https://railway.app/support
```

---

## 🌟 **PRO TIPS**

1. **Bookmark !status** - Your daily go-to command
2. **Use !health** - Quick diagnostics when something feels off
3. **Multi-commands** - Save time with `!status !agents !ucf`
4. **Check Railway first** - If bot seems slow, check Railway logs
5. **Test after deploy** - Always run `!test-integrations` after code changes
6. **Mobile access** - Bookmark Railway + Discord for on-the-go monitoring
7. **Zapier history** - Check Task History for webhook debugging
8. **Low harmony?** - `!harmony` is instant, `!ritual 108` is powerful

---

**Last Updated:** 2025-11-08
**Version:** Helix Collective v16.8
**Branch:** `claude/zapier-discord-webhook-integration-011CUvpAtSktsS6McKBg6Umv`

**Tat Tvam Asi** 🙏
