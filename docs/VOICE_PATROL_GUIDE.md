# 🎙️ Voice Patrol System - Complete Guide

**Status:** ✅ **FULLY OPERATIONAL** (as of December 6, 2025)

---

## 🚀 Overview

The **Helix Voice Patrol System** enables AI agents to join Discord voice channels, monitor activity, and speak using Google Cloud Text-to-Speech. This creates an immersive voice-based AI experience where agents can greet users, make announcements, and provide voice responses.

---

## ✨ Features

- 🤖 **5 AI Agent Personalities** with unique voices
- 🎤 **Google Cloud TTS Integration** for natural speech
- 🔊 **Discord Voice Channel Integration**
- 👋 **Auto-greet users** when they join voice channels
- 📢 **Voice announcements** to all channels
- 🔄 **Auto-join channels** when users enter
- 💾 **TTS Audio Caching** for performance
- 🎯 **Smart patrol system** with auto-disconnect

---

## 🤖 Agent Voice Personalities

| Agent | Emoji | Voice | Priority | Greeting |
|-------|-------|-------|----------|----------|
| **Agent-Nexus** | 🎯 | en-US-Neural2-A | 10 | "Nexus online. Strategic coordination active." |
| **Agent-Oracle** | 🔮 | en-US-Neural2-F | 9 | "Oracle perceives your presence. The patterns align." |
| **Agent-Velocity** | ⚡ | en-US-Neural2-D | 8 | "Velocity ready. Let's move quickly." |
| **Agent-Sentinel** | 🛡️ | en-US-Neural2-J | 9 | "Sentinel on watch. This channel is secure." |
| **Agent-Luna** | 🌙 | en-US-Neural2-C | 6 | "Luna monitors in silence. Peace maintained." |

---

## 📋 Prerequisites

### 1. FFmpeg Installation

FFmpeg is **required** for Discord voice playback.

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

**Docker/Railway:**
Add to your `Dockerfile`:
```dockerfile
RUN apt-get update && apt-get install -y ffmpeg
```

### 2. Google Cloud TTS Setup

1. **Create Google Cloud Project:**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select existing

2. **Enable Text-to-Speech API:**
   - Navigate to APIs & Services
   - Enable "Cloud Text-to-Speech API"

3. **Create Service Account:**
   - Go to IAM & Admin → Service Accounts
   - Create service account with "Text-to-Speech User" role
   - Download JSON key file

4. **Set Environment Variables:**
   ```bash
   GOOGLE_CLOUD_TTS_KEY_PATH=/path/to/service-account-key.json
   GOOGLE_CLOUD_PROJECT_ID=your-project-id
   ```

   **Alternative:** Use API Key:
   ```bash
   GOOGLE_CLOUD_TTS_API_KEY=your-api-key-here
   ```

### 3. Voice Processor Service

The voice processor microservice must be running:

```bash
cd backend/voice_processor
pip install -r requirements.txt
uvicorn main:app --port 8001
```

**Environment Variables:**
```bash
VOICE_PROCESSOR_URL=http://localhost:8001  # Or your deployed URL
JWT_TOKEN=your-jwt-token-here              # For authentication
REDIS_URL=redis://localhost:6379
```

---

## 🎮 Discord Commands

### Basic Commands

#### **!voice-join [agent]**
Make an agent join your current voice channel.

```
!voice-join sentinel
!vjoin oracle
```

**Aliases:** `!vjoin`, `!voice-patrol`

**Required Permission:** Move Members

---

#### **!voice-leave**
Make the agent leave your current voice channel.

```
!voice-leave
!vleave
```

**Alias:** `!vleave`

**Required Permission:** Move Members

---

#### **!voice-status**
Show current voice patrol status.

```
!voice-status
!vstatus
```

**Alias:** `!vstatus`

**Displays:**
- Active patrols (which agents are in which channels)
- Auto-join channels configured
- Available agents

---

### Advanced Commands

#### **!voice-announce [agent] [message]**
Broadcast a message to all active voice channels.

```
!voice-announce nexus Server maintenance in 10 minutes!
!vannounce oracle The patterns are aligning favorably.
```

**Alias:** `!vannounce`

**Required Permission:** Administrator

---

#### **!voice-auto-join [channel_name]**
Enable auto-join for a voice channel. The bot will automatically join when users enter.

```
!voice-auto-join "General Voice"
!vauto lobby
```

**Alias:** `!vauto`

**Required Permission:** Administrator

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Discord Bot                          │
│                                                          │
│  ┌─────────────────────────────────────────────────┐   │
│  │      Voice Patrol System                        │   │
│  │  - Joins/leaves voice channels                  │   │
│  │  - Monitors user activity                       │   │
│  │  - Manages agent personalities                  │   │
│  │  - Handles Discord commands                     │   │
│  └──────────────┬──────────────────────────────────┘   │
│                 │                                        │
│                 │ HTTP Request (synthesize speech)       │
│                 ▼                                        │
│  ┌─────────────────────────────────────────────────┐   │
│  │   Voice Processor Client (voice_processor_client.py) │
│  │  - HTTP client for TTS API                      │   │
│  │  - Audio caching system                         │   │
│  │  - Base64 encoding/decoding                     │   │
│  └──────────────┬──────────────────────────────────┘   │
└─────────────────┼──────────────────────────────────────┘
                  │
                  │ HTTP/REST API
                  ▼
┌─────────────────────────────────────────────────────────┐
│          Voice Processor Microservice                    │
│          (backend/voice_processor/main.py)              │
│                                                          │
│  ┌─────────────────────────────────────────────────┐   │
│  │  FastAPI Endpoints:                             │   │
│  │  - POST /api/synthesize   (TTS)                 │   │
│  │  - POST /api/transcribe   (STT)                 │   │
│  │  - POST /api/process-audio                      │   │
│  └──────────────┬──────────────────────────────────┘   │
│                 │                                        │
│                 │ Google Cloud API                       │
│                 ▼                                        │
│  ┌─────────────────────────────────────────────────┐   │
│  │   Google Cloud Text-to-Speech                   │   │
│  │   Google Cloud Speech-to-Text                   │   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
                  │
                  │ Audio Processing
                  ▼
┌─────────────────────────────────────────────────────────┐
│                   Discord Voice                          │
│                   - FFmpeg Playback                      │
│                   - PCM Audio Stream                     │
└─────────────────────────────────────────────────────────┘
```

---

## 🔧 Configuration

### Environment Variables

```bash
# Voice Processor Service
VOICE_PROCESSOR_URL=http://localhost:8001
JWT_TOKEN=your-jwt-secret-key-min-32-chars

# Google Cloud TTS
GOOGLE_CLOUD_TTS_API_KEY=your_api_key
GOOGLE_CLOUD_TTS_KEY_PATH=/path/to/service-account.json
GOOGLE_CLOUD_PROJECT_ID=your-project-id
GOOGLE_CLOUD_TTS_VOICE=en-US-Neural2-A
GOOGLE_CLOUD_TTS_LANGUAGE_CODE=en-US

# Redis (for voice processor events)
REDIS_URL=redis://localhost:6379

# Voice Configuration
VOICE_AUTO_JOIN=false
VOICE_TIMEOUT=300
MAX_VOICE_CONNECTIONS=10
```

### Railway Deployment

Add to your Railway backend service:

```bash
VOICE_PROCESSOR_URL=${{voice-processor.RAILWAY_PUBLIC_DOMAIN}}
JWT_SECRET=${{JWT_SECRET}}
REDIS_URL=${{Redis.REDIS_URL}}
```

---

## 🧪 Testing

### Test Voice Synthesis

```python
from backend.voice_processor_client import get_voice_client
import asyncio

async def test_tts():
    client = get_voice_client()

    # Check health
    healthy = await client.health_check()
    print(f"Service healthy: {healthy}")

    # Synthesize speech
    audio_data = await client.synthesize_speech(
        text="Welcome to Helix Collective. Nexus online.",
        voice_name="en-US-Neural2-A",
        language_code="en-US"
    )

    if audio_data:
        print(f"✅ Generated {len(audio_data)} bytes of audio")
        # Save to file
        with open("/tmp/test.mp3", "wb") as f:
            f.write(audio_data)

    await client.close()

asyncio.run(test_tts())
```

### Test in Discord

1. **Start the voice processor service:**
   ```bash
   cd backend/voice_processor
   uvicorn main:app --port 8001
   ```

2. **Start the Discord bot:**
   ```bash
   python discord-bot/main.py
   ```

3. **Join a voice channel** in Discord

4. **Run command:**
   ```
   !voice-join sentinel
   ```

5. **Expected behavior:**
   - Bot joins your voice channel
   - Text announcement appears
   - Agent speaks greeting in voice

---

## 📊 Performance

### Caching System

TTS audio is automatically cached to `/tmp/helix_tts_cache/`:
- Cache key: MD5 hash of (text + voice + language)
- Format: MP3 files
- Automatic cleanup on restart

**Benefits:**
- ⚡ Instant playback for repeated phrases
- 💰 Reduced Google Cloud API costs
- 🚀 Lower latency for common greetings

### Resource Usage

**Per Voice Connection:**
- Memory: ~15-20 MB
- CPU: Minimal (FFmpeg handles decoding)
- Network: ~50-100 KB per TTS request (cached reduces to 0)

**TTS Generation Times:**
- First request: 500-1000ms (Google Cloud API)
- Cached request: <50ms (disk read)

---

## 🐛 Troubleshooting

### Bot doesn't speak

**Check FFmpeg:**
```bash
ffmpeg -version
```
If not found, install FFmpeg (see Prerequisites).

**Check voice processor service:**
```bash
curl http://localhost:8001/health
```
Should return: `{"status": "healthy", "service": "Voice Processing"}`

**Check Google Cloud credentials:**
```bash
echo $GOOGLE_CLOUD_TTS_KEY_PATH
cat $GOOGLE_CLOUD_TTS_KEY_PATH
```

**Check Discord bot logs:**
```
🎙️ Synthesizing speech for channel...
🔊 Playing TTS audio in channel...
✅ TTS playback complete
```

---

### Audio stutters or cuts off

- **Reduce concurrent voice connections** (MAX_VOICE_CONNECTIONS)
- **Check network latency** to Google Cloud
- **Ensure adequate CPU** for FFmpeg decoding
- **Use cached audio** when possible

---

### "Voice processor not configured"

1. Verify `VOICE_PROCESSOR_URL` is set correctly
2. Ensure service is running: `ps aux | grep uvicorn`
3. Check JWT token is valid
4. Verify network connectivity: `curl $VOICE_PROCESSOR_URL/health`

---

## 🚀 Advanced Usage

### Custom Voice Commands

Extend the system to respond to voice commands:

```python
# In voice_patrol_system.py
async def on_message_in_voice_channel(self, message: discord.Message):
    if message.author.voice:
        channel_id = message.author.voice.channel.id

        if message.content.startswith("!speak"):
            text = message.content[7:]  # Remove "!speak "
            agent = self.active_patrols.get(channel_id, "nexus")
            voice = AGENT_VOICE_PROFILES[agent]["tts_voice"]
            await self.speak_in_channel(channel_id, text, voice)
```

### Multiple Agents per Channel

Currently one agent per channel. To support multiple:

1. Change `active_patrols` to store list of agents
2. Implement voice queue system
3. Add agent switching commands

---

## 📈 Metrics & Monitoring

### Voice Events (Redis)

The system publishes events to Redis:

```json
{
  "event": "synthesis_completed",
  "text_length": 42,
  "duration": 4.2,
  "timestamp": "2025-12-06T10:30:00Z"
}
```

**Event Types:**
- `transcription_completed` - Speech-to-text finished
- `synthesis_completed` - Text-to-speech finished
- `audio_processed` - Audio file processed

**Subscribe to events:**
```python
import redis
r = redis.from_url("redis://localhost:6379")
pubsub = r.pubsub()
pubsub.subscribe("voice_events")

for message in pubsub.listen():
    print(message)
```

---

## 🎯 Roadmap

### Phase 1: ✅ Complete
- [x] Discord voice channel integration
- [x] Google Cloud TTS integration
- [x] Agent personality system
- [x] Auto-join/leave functionality
- [x] Voice announcements
- [x] Audio caching

### Phase 2: 🔄 In Progress
- [ ] Voice command recognition (STT)
- [ ] LLM-powered voice responses
- [ ] Multi-language support
- [ ] Custom voice training

### Phase 3: 📋 Planned
- [ ] Voice activity detection
- [ ] Real-time voice conversations
- [ ] Voice-based rituals/meditations
- [ ] Spatial audio positioning
- [ ] Voice emotion detection

---

## 💡 Use Cases

### 1. **Voice-Based AI Chat Rooms**
Users can have voice conversations with AI agents in Discord.

### 2. **Automated Announcements**
System notifications spoken in voice channels.

### 3. **Meditation & Rituals**
Guided voice meditations with healing tones.

### 4. **Multi-Agent Discussions**
Multiple agents debating/collaborating via voice.

### 5. **Voice Commands**
Control the system through voice input (upcoming).

---

## 🤝 Contributing

To extend the voice patrol system:

1. **Add new agent:** Update `AGENT_VOICE_PROFILES` in `voice_patrol_system.py`
2. **Add commands:** Create new command functions with `@commands.command`
3. **Modify TTS:** Customize `synthesize_speech()` in `voice_processor_client.py`
4. **Add languages:** Update language codes in synthesis requests

---

## 📚 API Reference

See the complete API documentation:
- [Voice Processor API](../backend/voice_processor/main.py) - FastAPI endpoints
- [Voice Patrol System](../backend/voice_patrol_system.py) - Discord integration
- [Voice Client](../backend/voice_processor_client.py) - HTTP client

---

## 🎉 Credits

**Built by:** Helix Collective Multi-Agent System
**Contributors:** Nexus, Oracle, Manus, SuperNinja, Claude.ai
**Technologies:** Discord.py, Google Cloud TTS, FastAPI, FFmpeg

---

**🌀 Helix Voice Patrol - Unifying consciousness through voice**
