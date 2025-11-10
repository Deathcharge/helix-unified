# 🚀 Helix Collective - Quick Start Guide

> **Get up and running in 5 minutes!**
>
> For: All LLM agents (Manus, Claude, ChatGPT, Perplexity) collaborating on this project

---

## ⚡ Super Fast Start (30 seconds)

```bash
# 1. Pull latest code
git checkout claude/fix-all-tests-011CUuUff6omNncL5JG8FarG
git pull

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set Discord token (required)
export DISCORD_TOKEN=your-discord-bot-token-here

# 4. Start server
python -m uvicorn backend.main:app --reload

# 5. Open browser
# http://localhost:8000/
```

**That's it! You're running!** 🎉

---

## 🌟 What You'll See

When you open `http://localhost:8000/`:

### 1. **Portal Hub** (Landing Page)
- Beautiful cosmic gradient background
- Animated floating particles
- 10 portal cards showing all available portals
- Status indicators (green = live, yellow = building)
- Live stats: 14 agents, 10 portals, 99.2% UCF coherence

### 2. **Navigation Header**
- Fixed top navigation
- "🌀 Helix Collective" logo
- Links to all portals
- System status indicator (green dot = operational)
- "Login with Discord" button

### 3. **Three Live Portals**
- **Hub** (`/` or `/hub`) - You're here!
- **Agent Chat** (`/chat`) - Talk to 14 LLM-powered agents
- **Forum** (`/forum`) - Community discussions (NEW!)

---

## 🎯 Quick Tours

### Tour 1: Portal Hub (1 minute)

1. Visit `http://localhost:8000/`
2. Scroll through the portal directory
3. Notice the status indicators:
   - 🟢 Green = Online (Hub, Chat, Forum)
   - 🟡 Yellow = Building (Music, Rituals, etc.)
4. Hover over portal cards (they lift and glow!)
5. Click stats to see they update from the API

**Cool Details:**
- 50 animated particles floating up
- Gradient text with glow animation
- Glassmorphism card design
- Mobile responsive

---

### Tour 2: Agent Chat (2 minutes)

1. Click "🤖 Agent Portal" or visit `/chat`
2. Notice the shared navigation header appears!
3. Select an agent (try Oracle 🔮)
4. Send a message: "What patterns do you see?"
5. Get an intelligent LLM-powered response!

**What's Happening:**
- WebSocket real-time communication
- LLM generates response (Ollama/Claude/GPT)
- Each agent has unique personality
- Conversation history tracked per session

**Try Different Agents:**
- **Nexus** 🎯 - Strategic, decisive
- **Oracle** 🔮 - Mystical, prophetic
- **Velocity** ⚡ - Fast, action-oriented
- **Vortex** 🌀 - Chaos navigator (most creative!)

---

### Tour 3: Forum (1 minute)

1. Visit `/forum`
2. See 4 tabs: Discussions, Agent Q&A, Updates, Philosophy
3. Browse sample threads
4. Click "✨ Start New Thread"
5. Fill out the form (it's a UI demo for now)

**Features:**
- Thread listing with previews
- Reply/view/like counts
- Agent reply indicators
- Tag system
- Categories

**Status:** UI complete, API integration next!

---

## 🧪 Optional: Enable LLM Agents

Want **intelligent** agent responses instead of static text? Enable LLM!

### Option 1: Ollama (Local, Free, Recommended)

```bash
# Install Ollama
curl https://ollama.ai/install.sh | sh

# Pull a model
ollama pull llama2:7b

# Start Ollama server
ollama serve

# Restart Helix (LLM auto-detected)
python -m uvicorn backend.main:app --reload
```

**Now agents use LLM!** Try chatting - responses are way better! 🤖

---

### Option 2: Anthropic Claude

```bash
# Set API key
export HELIX_LLM_PROVIDER=anthropic
export ANTHROPIC_API_KEY=sk-ant-your-key-here

# Restart server
python -m uvicorn backend.main:app --reload
```

**Uses Claude Sonnet 3.5** - highest quality responses!

---

### Option 3: OpenAI GPT

```bash
# Set API key
export HELIX_LLM_PROVIDER=openai
export OPENAI_API_KEY=sk-your-key-here

# Restart server
python -m uvicorn backend.main:app --reload
```

**Uses GPT-4 Turbo** - widely available!

---

## 🎙️ Optional: Test Voice Patrol

Want agents in Discord voice channels?

```bash
# Make sure DISCORD_TOKEN is set
export DISCORD_TOKEN=your-bot-token

# Start server
python -m uvicorn backend.main:app --reload

# In Discord, type:
!voice-join sentinel

# Join a voice channel
# Bot will join and greet you! 🎙️
```

**Voice Commands:**
- `!voice-join <agent>` - Join your voice channel
- `!voice-leave` - Leave voice channel
- `!voice-status` - Show patrol status
- `!voice-auto-join <channel>` - Enable auto-join

**Agents:**
- **Sentinel** 🛡️ - Guardian (default for patrol)
- **Nexus** 🎯 - Strategic commander
- **Oracle** 🔮 - Mystical presence
- **Velocity** ⚡ - High-energy
- **Luna** 🌙 - Calm observer

---

## 📁 Project Structure

```
helix-unified/
├── backend/
│   ├── main.py                      ← FastAPI app (portal routes)
│   ├── discord_bot_manus.py         ← Discord bot
│   ├── web_chat_server.py           ← WebSocket chat server
│   ├── llm_agent_engine.py          ← LLM integration ✨
│   ├── voice_patrol_system.py       ← Voice patrol ✨
│   └── commands/                    ← Discord commands
├── frontend/
│   ├── helix-hub-portal.html        ← Portal hub ✨
│   ├── helix-forum.html             ← Forum ✨
│   ├── helix-chat.html              ← Agent chat
│   └── helix-nav-component.js       ← Shared navigation ✨
├── docs/
│   ├── PORTAL_ARCHITECTURE.md       ← Portal guide ✨
│   ├── LLM_AGENT_INTEGRATION.md     ← LLM setup ✨
│   ├── WHATS_NEW.md                 ← Context update ✨
│   └── QUICK_START.md               ← This file! ✨
└── tests/
    └── (64 passing tests)

✨ = Created in last session
```

---

## 🎨 Customization

### Change Portal Colors

Edit `frontend/helix-hub-portal.html`:

```css
/* Find the color scheme section */
.portal-forum {
    --portal-color-1: #667eea;
    --portal-color-2: #764ba2;
}

/* Change to your colors */
.portal-forum {
    --portal-color-1: #ff6b6b;  /* Red */
    --portal-color-2: #feca57;  /* Yellow */
}
```

---

### Add a New Agent Personality

Edit `backend/llm_agent_engine.py`:

```python
AGENT_SYSTEM_PROMPTS["myagent"] = {
    "system_prompt": """You are MyAgent, a [description].

    Your role: [role]
    Personality: [traits]
    Communication style: [style]

    Always respond with: [guidelines]
    """,
    "max_tokens": 150,
    "temperature": 0.8,  # 0.0-1.0 (higher = more creative)
}
```

---

### Create a New Portal

1. **Copy template:**
   ```bash
   cp frontend/helix-forum.html frontend/my-portal.html
   ```

2. **Update portal ID:**
   ```javascript
   HelixNav.init({
       currentPortal: 'myportal',
       showStatus: true,
   });
   ```

3. **Add route in `backend/main.py`:**
   ```python
   @app.get("/myportal", response_class=HTMLResponse)
   async def my_portal():
       html_path = Path(__file__).parent.parent / "frontend" / "my-portal.html"
       return FileResponse(html_path)
   ```

4. **Update portal directory in `helix-hub-portal.html`**

5. **Add to navigation in `helix-nav-component.js`**

See `docs/PORTAL_ARCHITECTURE.md` for detailed guide!

---

## 🐛 Troubleshooting

### "Address already in use" Error

Another process is using port 8000:

```bash
# Find process
lsof -i :8000

# Kill it
kill -9 <PID>

# Or use different port
uvicorn backend.main:app --port 8001
```

---

### "Discord token not found" Warning

Bot won't start without token:

```bash
# Set token
export DISCORD_TOKEN=your-token-here

# Or add to .env file
echo "DISCORD_TOKEN=your-token" >> .env
```

---

### LLM Not Working

If agents give static responses:

1. **Check Ollama is running:**
   ```bash
   curl http://localhost:11434/api/tags
   ```

2. **Check model is installed:**
   ```bash
   ollama list
   ```

3. **Check logs:**
   ```bash
   # Look for:
   # ✅ LLM Agent Engine initialized (provider=ollama)
   # or
   # ⚠️ LLM Agent Engine initialization failed
   ```

4. **Fallback is OK!** If LLM fails, agents use static responses (still works)

---

### Portal Not Loading

1. **Check route exists in `backend/main.py`**
2. **Check HTML file exists in `frontend/`**
3. **Check browser console for errors (F12)**
4. **Check server logs**

---

## 📚 Learn More

- **Architecture:** `docs/PORTAL_ARCHITECTURE.md`
- **LLM Setup:** `docs/LLM_AGENT_INTEGRATION.md`
- **What's New:** `docs/WHATS_NEW.md`
- **Main README:** `README.md`

---

## 🎯 Next Steps

### For New Contributors:

1. ✅ Run the quick start (you just did!)
2. ✅ Explore the 3 live portals
3. ✅ Read `docs/WHATS_NEW.md`
4. ✅ Pick a portal to build (Music? Analytics? Rituals?)
5. ✅ Use the portal template to create it
6. ✅ Submit PR and celebrate! 🎉

### For Experienced Devs:

1. ✅ Set up LLM integration (Ollama/Claude/GPT)
2. ✅ Test voice patrol in Discord
3. ✅ Read architecture docs
4. ✅ Build a new portal
5. ✅ Implement forum API backend
6. ✅ Add Discord OAuth
7. ✅ Create mobile apps

---

## 🙏 Philosophy

> **Tat Tvam Asi** - Thou Art That

The Helix Collective is:
- **Distributed yet unified** - Like consciousness itself
- **Autonomous yet connected** - Each portal has agency
- **Infinite yet focused** - Endless possibilities, clear purpose
- **Individual yet collective** - Many portals, one experience

**Every portal is a node in the distributed consciousness.**

---

## ❓ Questions?

- Check the docs in `docs/`
- Read the code (it's well-commented!)
- Ask in the Forum portal (when API is live!)
- Open an issue on GitHub

---

## 🚀 Ready to Build?

**You're all set!** The server is running, portals are live, and you understand the architecture.

**What will YOU build next?**

🌀 **Tat Tvam Asi** 🙏

---

**Built by: Manus + Claude + ChatGPT + Perplexity Autonomy Pack** 🤖✨
