# Mobile Deployment Guide - Discord Enhancements

**For mobile-only users deploying to Railway**

---

## ✅ What's Been Pushed to GitHub

All Discord enhancements are now in the `helix-unified` repository:

1. **Scheduled Content System** (`discord-bot/scheduled_content.py`)
   - Weekly/bi-weekly/daily agent updates
   - LLM-powered content generation
   - Personality-driven templates

2. **Server Setup Script** (`discord-bot/server_setup.py`)
   - Creates voice channels for all categories
   - Adds voice-transcripts channel
   - Verifies server structure

3. **Updated Agent Bot** (`discord-bot/agent_bot.py`)
   - Integrated scheduler bot support
   - Fixed channel routing

4. **Documentation** (`discord-bot/DISCORD_ENHANCEMENTS.md`)
   - Complete setup instructions
   - Schedule reference
   - Troubleshooting guide

5. **Railway Config** (`discord-bot/Procfile.scheduler`)
   - Deployment configuration for scheduler bot

---

## 🚀 Railway Deployment Steps (Mobile)

### Step 1: Create Scheduler Bot Discord Account

**On mobile browser:**

1. Go to https://discord.com/developers/applications
2. Click "New Application"
3. Name: "Helix Scheduler"
4. Go to "Bot" tab → "Add Bot"
5. Enable these intents:
   - ✅ Presence Intent
   - ✅ Server Members Intent
   - ✅ Message Content Intent
6. Click "Reset Token" → Copy token (save it!)
7. Go to "OAuth2" → "URL Generator"
8. Select scopes:
   - ✅ bot
9. Select permissions:
   - ✅ Administrator (or manually select needed permissions)
10. Copy generated URL
11. Open URL in new tab → Add bot to your Discord server

### Step 2: Deploy Scheduler Bot on Railway

**In Railway app/website:**

1. Open your Railway project
2. Click "New Service"
3. Select "GitHub Repo"
4. Choose `Deathcharge/helix-unified`
5. Service name: "discord-scheduler"
6. Click "Settings" tab
7. Set **Build Command**:
   ```
   cd discord-bot && pip install -r requirements.txt
   ```
8. Set **Start Command**:
   ```
   cd discord-bot && python agent_bot.py scheduler
   ```
9. Click "Variables" tab
10. Add these environment variables:
    - `DISCORD_TOKEN_SCHEDULER` = (paste bot token from Step 1)
    - `ANTHROPIC_API_KEY` = (your Claude API key)
    - `OPENAI_API_KEY` = (your OpenAI key - optional)

11. Click "Deploy"

### Step 3: Set Up Discord Server Channels

**Option A: Manual (Recommended for mobile)**

In your Discord server, create these voice channels:

**🌀 WELCOME category:**
- Voice: "Welcome Lounge"

**🧠 SYSTEM category:**
- Voice: "System Monitor"
- Text: "voice-transcripts"

**🔮 PROJECTS category:**
- Voice: "Project Discussion"

**🎭 AGENTS category:**
- Voice: "Agent Coordination"

**🌐 CROSS-MODEL SYNC category:**
- Voice: "Model Sync Room"

**🔧 DEVELOPMENT category:**
- Voice: "Dev Workshop"

**🕉️ RITUAL & LORE category:**
- Voice: "Ritual Chamber"

**🔒 ADMIN category:**
- Voice: "Admin Office"

**Option B: Automated (Requires desktop/SSH)**

If you have access to a computer:
```bash
cd /home/ubuntu/helix-repos/helix-unified/discord-bot
python server_setup.py
```

### Step 4: Verify Deployment

**Check Railway logs:**
1. Open Railway app
2. Go to "discord-scheduler" service
3. Click "Deployments" → Latest deployment
4. Check logs for:
   ```
   Scheduler bot ready: Helix Scheduler#1234
   ```

**Check Discord:**
1. Verify scheduler bot is online in your server
2. Wait for next scheduled time (or adjust schedules)
3. Check channels for automated posts

---

## 📅 Content Schedule (UTC Times)

| Channel | When | Time |
|---------|------|------|
| telemetry | Every Sunday | 12:00 AM |
| weekly-digest | Every Sunday | 12:00 AM |
| shadow-storage | Every day | 5:00 AM |
| ucf-sync | Every Sunday | 12:00 AM |
| gemini-scout | Every other Tuesday | 12:00 PM |
| kavach-shield | Every other Wednesday | 12:00 PM |
| sanghacore | Every other Thursday | 12:00 PM |
| agni-core | Every other Friday | 12:00 PM |
| neti-neti-mantra | Every Monday | 6:00 AM |
| codex-archives | Every Sunday | 12:00 AM |
| ucf-reflections | Every Sunday | 1:00 AM |
| harmonic-updates | Every Sunday | 2:00 AM |

---

## 🔧 Troubleshooting

### Scheduler bot offline
- Check Railway logs for errors
- Verify `DISCORD_TOKEN_SCHEDULER` is correct
- Ensure bot is invited to server

### No automated posts
- Check system time (must be UTC)
- Verify channels exist with exact names
- Check Railway logs for generation errors
- Ensure `ANTHROPIC_API_KEY` is set

### Voice channels missing
- Manually create them (see Step 3)
- Ensure bot has "Manage Channels" permission

### Content generation fails
- Check API keys are valid
- Review Railway logs for specific errors
- System will fall back to template content

---

## 🎯 Next Steps

After deployment:

1. **Monitor first scheduled post** (next Sunday midnight UTC)
2. **Check voice-transcripts** when agents listen to voice
3. **Customize schedules** if needed (edit `scheduled_content.py`)
4. **Add more content templates** for new channels

---

## 📊 Railway Services Overview

You should now have these services running:

1. **backend** - Agent orchestration API
2. **dashboard** - Web dashboard (if deployed)
3. **claude-api** - Claude API proxy (if deployed)
4. **discord-bot** - Main Discord bot service
5. **discord-scheduler** - NEW: Scheduled content bot

All services should show "Active" status.

---

## 💡 Tips for Mobile Management

- Use Railway mobile app for quick log checks
- Use Discord mobile app to verify bot status
- Bookmark Railway dashboard for quick access
- Set up Railway notifications for deployment failures
- Keep bot tokens in secure notes app

---

## 🆘 Need Help?

If something isn't working:

1. Check Railway logs first
2. Verify all environment variables are set
3. Ensure bot has proper Discord permissions
4. Review `DISCORD_ENHANCEMENTS.md` for detailed troubleshooting

---

**Built with 🙏 by the Helix Collective**  
*Tat Tvam Asi • Aham Brahmasmi • Neti Neti*
