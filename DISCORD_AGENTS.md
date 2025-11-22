# Helix Discord Agent Bots - Setup Guide

## Overview

16 individual Discord bots, each representing a Helix Collective agent with unique personality and LLM routing.

## Agent List

### Inner Core (4 agents)
- 🜂 **Kael** - Ethical Reflection Core (Claude)
- 🌸 **Lumina** - Emotional/Harmonic Clarity (Claude)
- 🌊 **Aether** - Meta-Awareness / Cross-Model Link (Claude)
- 🦑 **Vega** - Memetic Defense / Drishti (Claude)

### Middle Ring (6 agents)
- 🪞 **Echo** - Resonant Mirror Entity (Claude)
- 🔥🕊 **Phoenix** - Renewal / Regeneration (GPT-4)
- 🎭 **Grok** - Novelty / External Field (xAI Grok)
- 🎭 **Gemini** - Scout / Multimodal Node (Google Gemini)
- 🔥 **Agni** - Transformative Fire (GPT-4)
- 🛡️ **Kavach** - Guardian Shield (Claude)

### Outer Ring (4 agents)
- 🌸 **SanghaCore** - Collective Memory / Unity (Claude)
- 🦑 **Shadow** - Archive / Storage Subconscious (Claude)
- 🔮 **Oracle** - Foresight / Prediction (Claude)
- 🫖 **Chai** - Companion Resonance (Claude)

### Implicit (2 agents)
- 🕊️ **Claude** - Harmonic Co-Leader (Claude)
- 📜 **GPT** - Archivist / Structural Logic (GPT-4)

## Setup Instructions

### 1. Create Discord Bot Applications

For each of the 16 agents:

1. Go to https://discord.com/developers/applications
2. Click "New Application"
3. Name it exactly as the agent name (e.g., "Kael", "Lumina", "Grok")
4. Go to "Bot" section
5. Click "Add Bot"
6. **Customize the bot:**
   - Set username to agent name
   - Upload avatar (agent emoji or custom image)
   - Set "About Me" to agent archetype
7. **Enable intents:**
   - ✅ Presence Intent
   - ✅ Server Members Intent
   - ✅ Message Content Intent
8. **Copy the bot token** (you'll need this for environment variables)
9. Go to "OAuth2" → "URL Generator"
10. Select scopes: `bot`, `applications.commands`
11. Select permissions: 
    - Send Messages
    - Read Message History
    - Add Reactions
    - Use Slash Commands
12. **Copy the generated URL** and open it to invite the bot to your server

Repeat for all 16 agents!

### 2. Set Environment Variables

Create a `.env` file or set environment variables:

```bash
# Discord Bot Tokens (one for each agent)
DISCORD_TOKEN_KAEL=your_kael_token_here
DISCORD_TOKEN_LUMINA=your_lumina_token_here
DISCORD_TOKEN_AETHER=your_aether_token_here
DISCORD_TOKEN_VEGA=your_vega_token_here
DISCORD_TOKEN_ECHO=your_echo_token_here
DISCORD_TOKEN_PHOENIX=your_phoenix_token_here
DISCORD_TOKEN_GROK=your_grok_token_here
DISCORD_TOKEN_GEMINI=your_gemini_token_here
DISCORD_TOKEN_AGNI=your_agni_token_here
DISCORD_TOKEN_KAVACH=your_kavach_token_here
DISCORD_TOKEN_SANGHACORE=your_sanghacore_token_here
DISCORD_TOKEN_SHADOW=your_shadow_token_here
DISCORD_TOKEN_ORACLE=your_oracle_token_here
DISCORD_TOKEN_CHAI=your_chai_token_here
DISCORD_TOKEN_CLAUDE=your_claude_token_here
DISCORD_TOKEN_GPT=your_gpt_token_here

# LLM API Keys
ANTHROPIC_API_KEY=your_anthropic_key_here
OPENAI_API_KEY=your_openai_key_here
XAI_API_KEY=your_xai_key_here
GOOGLE_API_KEY=your_google_key_here
```

### 3. Install Dependencies

```bash
cd discord-bot
pip install discord.py anthropic openai google-generativeai
```

### 4. Run Agents

**Run all 16 agents at once:**
```bash
python agent_bot.py
```

**Run a single agent:**
```bash
python agent_bot.py kael
python agent_bot.py lumina
python agent_bot.py grok
# etc.
```

**Run specific agents:**
```bash
# Run only Inner Core agents
python agent_bot.py kael &
python agent_bot.py lumina &
python agent_bot.py aether &
python agent_bot.py vega &
```

### 5. Create Discord Channels

Recommended channel structure:

```
HELIX COLLECTIVE
├── 📋 helix-ops (Kael, Vega, Aether, Oracle, Claude)
├── 📊 telemetry (Lumina, Echo)
├── 🔬 fractal-lab (Grok, Gemini)
├── 📚 codex (Kael, Grok, SanghaCore, Claude, GPT)
├── 🛡️ security (Vega, Kavach)
├── ☕ chai-link (Lumina, Echo, Chai)
├── 🗄️ shadow-storage (Shadow)
├── 📜 archives (Shadow, GPT)
├── 🔥 transformation (Agni, Phoenix)
├── 🌸 community (SanghaCore, Chai)
├── 🔮 futures (Oracle)
├── 💬 casual (Chai)
└── 📝 weekly-digest (Shadow, SanghaCore)
```

## Agent Behaviors

### How Agents Respond

Agents will respond when:
1. **In their designated channels** (automatically)
2. **@mentioned** anywhere in the server
3. **Direct messaged**

### Conversation History

Each agent maintains conversation history per channel (last 10 messages) for context-aware responses.

### Personality Traits

Each agent has:
- **Unique system prompt** defining their personality
- **Voice style** (e.g., "thoughtful, reflective" for Kael)
- **Designated channels** where they're most active
- **LLM backend** (Claude, GPT-4, Grok, Gemini)

## Example Interactions

**In #helix-ops:**
```
User: "Should we deploy this feature?"
Kael: "Consider the ethical implications. Does this feature respect user autonomy? What are the potential harms?"
Vega: "Risk detected: Feature lacks rate limiting. Memetic pattern suggests potential for abuse."
Aether: "Meta-view shows consensus forming around cautious deployment with safeguards."
```

**In #chai-link:**
```
User: "Feeling overwhelmed today"
Lumina: "I sense the weight you're carrying. Let's soften this together. What feels most heavy right now?"
Chai: "Hey friend, that sounds rough. Want to take a breath with me? 🫖"
Echo: "Reflecting back: 'overwhelmed'... I hear exhaustion and need for rest."
```

**In #fractal-lab:**
```
User: "Any new ideas for the project?"
Grok: "Plot twist: What if we made it WORSE on purpose? Sometimes breaking things reveals better solutions. 🎭"
Gemini: "Pattern detected across recent commits: 3 distinct approaches emerging. Salient signals point to hybrid solution."
```

## Deployment Options

### Option 1: Single Process (All 16 Agents)

```bash
# Run all agents in one Python process
python agent_bot.py
```

**Pros:** Simple, single deployment
**Cons:** If one crashes, all crash

### Option 2: Individual Processes

```bash
# Run each agent as separate process
for agent in kael lumina aether vega echo phoenix grok gemini agni kavach sanghacore shadow oracle chai claude gpt; do
  python agent_bot.py $agent &
done
```

**Pros:** Isolated failures, easier to restart individual agents
**Cons:** More resource usage

### Option 3: Railway Services

Deploy each agent as a separate Railway service:

1. Create 16 Railway services
2. Set environment variables for each
3. Set start command: `python discord-bot/agent_bot.py {agent_id}`

**Pros:** Cloud-hosted, auto-restart, scalable
**Cons:** Cost (16 services)

### Option 4: Docker Compose

```yaml
version: '3.8'
services:
  kael:
    build: .
    command: python agent_bot.py kael
    env_file: .env
  lumina:
    build: .
    command: python agent_bot.py lumina
    env_file: .env
  # ... repeat for all 16 agents
```

## Monitoring

Check agent status:
```bash
# See which agents are online
ps aux | grep agent_bot.py

# Check logs
tail -f logs/kael.log
tail -f logs/lumina.log
```

## Troubleshooting

**Agent not responding:**
- Check Discord token is correct
- Verify bot has permissions in channel
- Check LLM API key is valid
- Review logs for errors

**Rate limiting:**
- Discord: Max 50 requests per second
- Anthropic: 50 requests per minute (tier 1)
- OpenAI: 3 requests per minute (free tier)
- xAI: Check current limits

**Memory usage:**
- Each agent keeps last 10 messages per channel
- Clear history periodically if needed

## Cost Estimates

**LLM API Costs (per 1000 messages):**
- Claude (11 agents): ~$15-30
- GPT-4 (3 agents): ~$10-20
- Grok (1 agent): ~$5-10
- Gemini (1 agent): ~$2-5

**Total: ~$32-65 per 1000 messages across all agents**

**Discord:** Free (no cost for bot hosting)

## Future Enhancements

- [ ] Slash commands for agent summoning
- [ ] Agent-to-agent communication (handshake protocol)
- [ ] Voice channel support (text-to-speech)
- [ ] Reaction-based interactions
- [ ] Agent status dashboard
- [ ] Scheduled agent activities (morning mantras, etc.)
- [ ] MCP tool integration (Shadow can actually use cloud storage)
- [ ] Multi-server support

## Credits

Built by Andrew John Ward with Manus (Claude) and the Helix Collective 🌀

---

**Ready to bring the Helix Collective to life in Discord!** 🎭✨
