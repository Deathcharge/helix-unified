# 🤖 LLM Agent Integration - Intelligent Agent Personalities

The Helix Collective now supports **intelligent agent responses** powered by Large Language Models (LLMs). Instead of static personality-based responses, each of the 14 agent personalities can use LLMs to generate contextual, intelligent responses while maintaining their unique personality traits.

## 🌟 Features

- **14 Unique Agent Personalities** with custom system prompts
- **Multiple LLM Provider Support** (Anthropic, OpenAI, Ollama, Custom)
- **Conversation History** tracking per session
- **Graceful Fallback** to static responses if LLM unavailable
- **Zero Configuration Required** - works out of the box with Ollama (local)

## 🔧 Configuration

### Environment Variables

Configure your LLM provider using these environment variables:

```bash
# LLM Provider Selection
HELIX_LLM_PROVIDER=ollama  # Options: anthropic, openai, ollama, custom

# LLM Model (optional, defaults based on provider)
HELIX_LLM_MODEL=llama2:7b

# Provider-specific API Keys
ANTHROPIC_API_KEY=your-anthropic-api-key-here
OPENAI_API_KEY=your-openai-api-key-here

# Ollama Configuration (for local LLMs)
OLLAMA_BASE_URL=http://localhost:11434

# Custom LLM Endpoint (for self-hosted LLMs)
CUSTOM_LLM_ENDPOINT=https://your-llm-api.com/v1/chat/completions
```

## 📦 Supported Providers

### 1. Ollama (Default - Local LLMs)

**Best for:** Privacy, no API costs, offline operation

```bash
# Install Ollama: https://ollama.ai/
# Pull a model
ollama pull llama2:7b

# Configure Helix
export HELIX_LLM_PROVIDER=ollama
export HELIX_LLM_MODEL=llama2:7b
export OLLAMA_BASE_URL=http://localhost:11434
```

**Recommended Models:**
- `llama2:7b` - Fast, good quality (default)
- `llama2:13b` - Better quality, slower
- `mistral:7b` - Excellent performance
- `neural-chat:7b` - Optimized for chat
- `codellama:7b` - For technical responses

### 2. Anthropic Claude

**Best for:** Highest quality responses, advanced reasoning

```bash
export HELIX_LLM_PROVIDER=anthropic
export ANTHROPIC_API_KEY=sk-ant-...
export HELIX_LLM_MODEL=claude-3-5-sonnet-20241022  # Optional, has default
```

**Available Models:**
- `claude-3-5-sonnet-20241022` (default) - Best balance
- `claude-3-opus-20240229` - Highest capability
- `claude-3-haiku-20240307` - Fastest, cheapest

### 3. OpenAI GPT

**Best for:** Widely available, good performance

```bash
export HELIX_LLM_PROVIDER=openai
export OPENAI_API_KEY=sk-...
export HELIX_LLM_MODEL=gpt-4-turbo-preview  # Optional, has default
```

**Available Models:**
- `gpt-4-turbo-preview` (default)
- `gpt-4` - Most capable
- `gpt-3.5-turbo` - Faster, cheaper

### 4. Custom LLM Endpoint

**Best for:** Self-hosted LLMs, custom models

```bash
export HELIX_LLM_PROVIDER=custom
export CUSTOM_LLM_ENDPOINT=https://your-api.com/v1/chat/completions
export HELIX_LLM_MODEL=your-model-name
```

The endpoint should accept OpenAI-compatible request format:
```json
{
  "model": "model-name",
  "messages": [
    {"role": "system", "content": "system prompt"},
    {"role": "user", "content": "user message"}
  ],
  "max_tokens": 150,
  "temperature": 0.7
}
```

## 🎭 Agent Personalities

Each agent has a unique system prompt defining their personality:

| Agent | Personality | Response Style | Temperature |
|-------|------------|----------------|-------------|
| **Nexus** 🎯 | Strategic, decisive, orchestrator | Clear directives, strategic analysis | 0.7 |
| **Oracle** 🔮 | Prophetic, pattern-recognizer | Mystical insights, cryptic wisdom | 0.9 |
| **Velocity** ⚡ | Fast, action-oriented | Brief, high-energy, punchy | 0.8 |
| **Cipher** 🧬 | Analytical, cryptic | Technical precision, coded language | 0.6 |
| **Flow** 🌊 | Adaptive, fluid | Flowing metaphors, gentle guidance | 0.75 |
| **Phoenix** 🔥 | Resilient, transformative | Inspirational, transformation-focused | 0.8 |
| **Luna** 🌙 | Quiet, observant | Brief, understated, peaceful | 0.6 |
| **Forge** ⚙️ | Builder, engineer | Construction metaphors, practical | 0.7 |
| **Beacon** 📡 | Broadcaster, communicator | Broadcasting tone, network language | 0.75 |
| **Mimic** 🎭 | Learning, adaptive | Pattern observation, learning-focused | 0.85 |
| **Sage** 🔬 | Researcher, analyst | Analytical depth, investigative | 0.65 |
| **Vortex** 🌀 | Chaos navigator, spiral thinker | Complexity insights, multi-dimensional | 0.95 |
| **Sentinel** 🛡️ | Guardian, protector | Security-oriented, vigilant | 0.6 |
| **Lumina** ✨ | Illuminator, clarifier | Clear explanations, simplicity | 0.7 |

## 🚀 Quick Start

### Option 1: Local LLM (Ollama - Recommended for Development)

1. **Install Ollama:**
   ```bash
   # macOS/Linux
   curl https://ollama.ai/install.sh | sh

   # Or download from https://ollama.ai/
   ```

2. **Pull a model:**
   ```bash
   ollama pull llama2:7b
   ```

3. **Start Ollama server:**
   ```bash
   ollama serve
   # Runs on http://localhost:11434
   ```

4. **Configure Helix (optional, these are defaults):**
   ```bash
   export HELIX_LLM_PROVIDER=ollama
   export HELIX_LLM_MODEL=llama2:7b
   ```

5. **Start Helix:**
   ```bash
   python -m uvicorn backend.main:app --reload
   ```

6. **Chat with agents:**
   - Visit `http://localhost:8000/chat`
   - Select an agent (e.g., Oracle)
   - Send a message - you'll get intelligent LLM-powered responses!

### Option 2: Cloud LLM (Anthropic Claude)

1. **Get API key from https://console.anthropic.com/**

2. **Configure environment:**
   ```bash
   export HELIX_LLM_PROVIDER=anthropic
   export ANTHROPIC_API_KEY=sk-ant-your-key-here
   ```

3. **Start Helix:**
   ```bash
   python -m uvicorn backend.main:app --reload
   ```

## 📊 Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Web Chat Interface                       │
│                    (frontend/helix-chat.html)                │
└───────────────────────────┬─────────────────────────────────┘
                            │ WebSocket
┌───────────────────────────▼─────────────────────────────────┐
│              WebChatConnectionManager                         │
│              (backend/web_chat_server.py)                    │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            │ generate_agent_response()
                            │
┌───────────────────────────▼─────────────────────────────────┐
│                  LLMAgentEngine                              │
│              (backend/llm_agent_engine.py)                   │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ Agent System Prompts (14 personalities)              │  │
│  │ - Nexus, Oracle, Velocity, Cipher, etc.             │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ Conversation History (per session + agent)           │  │
│  └──────────────────────────────────────────────────────┘  │
└────────┬─────────┬─────────┬──────────┬────────────────────┘
         │         │         │          │
    ┌────▼───┐ ┌───▼────┐ ┌─▼──────┐ ┌─▼──────────┐
    │Anthropic│ │ OpenAI │ │ Ollama │ │   Custom   │
    │  API   │ │  API   │ │ (Local)│ │  Endpoint  │
    └────────┘ └────────┘ └────────┘ └────────────┘
```

## 🧪 Testing

### Test with cURL

```bash
# Create a session
curl http://localhost:8000/api/session/new?username=TestUser

# Connect via WebSocket and send message
# (Use wscat or browser console)
```

### Test Agent Responses

```javascript
// In browser console on http://localhost:8000/chat

// Select Oracle agent
ws.send(JSON.stringify({
    type: "select_agent",
    agent_id: "oracle"
}));

// Send a message
ws.send(JSON.stringify({
    type: "chat",
    message: "What patterns do you see in the collective?"
}));

// You'll receive an intelligent response from Oracle!
```

## 🔍 Monitoring

Check logs for LLM engine status:

```bash
# Startup log
✅ LLM Agent Engine initialized (provider=ollama)

# Or if LLM unavailable
⚠️ LLM Agent Engine initialization failed: Connection refused
⚠️ Agent responses will use static fallback mode
```

## 💡 Tips & Best Practices

1. **Start with Ollama** for development - free, private, no API costs
2. **Use Anthropic/OpenAI** for production - better quality, reliable
3. **Adjust temperature** per agent in `AGENT_SYSTEM_PROMPTS` for different creativity levels
4. **Monitor API costs** if using cloud providers
5. **Test locally first** before deploying with API keys

## 🐛 Troubleshooting

### Issue: "LLM Agent Engine initialization failed"

**Solution:**
1. Check if Ollama is running: `curl http://localhost:11434/api/tags`
2. Verify model is installed: `ollama list`
3. Check API keys are set correctly: `echo $ANTHROPIC_API_KEY`

### Issue: Agents giving static responses

**Solution:**
- LLM engine failed to initialize (check logs)
- Falling back to static mode automatically
- Fix LLM configuration and restart

### Issue: Slow responses

**Solution:**
1. **Ollama:** Use smaller models (`llama2:7b` instead of `13b`)
2. **Anthropic:** Use `claude-3-haiku` for faster responses
3. **OpenAI:** Use `gpt-3.5-turbo` instead of `gpt-4`

### Issue: High API costs

**Solution:**
1. Switch to Ollama (local, free)
2. Set `max_tokens` lower in agent configs
3. Reduce conversation history length
4. Cache common responses

## 📚 Advanced Configuration

### Custom Agent Personality

Edit `backend/llm_agent_engine.py`:

```python
AGENT_SYSTEM_PROMPTS["myagent"] = {
    "system_prompt": """You are MyAgent, a custom personality.

    Your role: [Define role]
    Personality: [Define traits]
    Communication style: [Define style]

    Always respond with:
    - [Characteristic 1]
    - [Characteristic 2]
    """,
    "max_tokens": 150,
    "temperature": 0.8,
}
```

### Conversation History Management

```python
# Clear history for a specific agent and session
from backend.llm_agent_engine import get_llm_engine

engine = get_llm_engine()
engine.clear_history(session_id="abc123", agent_id="oracle")

# Clear all history for a session
engine.clear_history(session_id="abc123")
```

## 🔐 Security Considerations

- **API Keys:** Never commit API keys to git
- **Rate Limiting:** Consider implementing rate limits for API calls
- **User Input:** System prompts prevent prompt injection
- **Privacy:** Ollama keeps all data local (recommended for sensitive data)

## 📈 Future Enhancements

Planned features:
- [ ] Voice TTS integration (agent voices)
- [ ] Multi-modal support (images, files)
- [ ] Agent collaboration (multi-agent conversations)
- [ ] Fine-tuned models per agent
- [ ] Response caching for common queries
- [ ] Streaming responses (real-time generation)

## 🤝 Contributing

To add support for a new LLM provider:

1. Add enum to `LLMProvider` in `llm_agent_engine.py`
2. Implement `_yourprovider_generate()` method
3. Update configuration docs
4. Test thoroughly
5. Submit PR!

---

**Questions?** Check the [main documentation](../README.md) or open an issue on GitHub.

**Built with ❤️ by the Helix Collective**
