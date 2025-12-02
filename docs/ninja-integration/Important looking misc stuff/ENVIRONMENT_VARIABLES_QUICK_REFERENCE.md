# Environment Variables Quick Reference Card

## 🎯 Quick Service Mapping

### Discord Bot Service ONLY
```env
# Discord (Required)
DISCORD_BOT_TOKEN=
DISCORD_CLIENT_ID=
DISCORD_GUILD_ID=

# AI (Required)
ANTHROPIC_API_KEY=
CLAUDE_MODEL=claude-3-sonnet-20240229

# OpenAI (Optional - for images & Whisper)
OPENAI_API_KEY=

# TTS (Pick ONE or more)
GOOGLE_CLOUD_TTS_API_KEY=
# OR
ELEVENLABS_API_KEY=
# OR
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=

# Image Generation (Optional)
STABILITY_API_KEY=
REPLICATE_API_KEY=

# Voice Transcription (Optional)
ASSEMBLYAI_API_KEY=

# Agent Config
MAX_AGENTS=16
DEFAULT_AGENT_PERSONALITY=friendly
```

### API Backend Service ONLY
```env
# API (Required)
API_HOST=0.0.0.0
API_PORT=8000
API_SECRET_KEY=

# Webhooks (Optional)
WEBHOOK_SECRET=
WEBHOOK_URL=
```

### BOTH Services (Shared)
```env
# Database (Required)
DATABASE_URL=

# Logging (Optional)
LOG_LEVEL=INFO
LOG_FILE=logs/helix_unified.log

# Performance (Optional)
PERFORMANCE_MONITORING_ENABLED=true
RATE_LIMIT_ENABLED=true
```

---

## 🔑 API Key Sources

| Service | Get Key From | Used For |
|---------|-------------|----------|
| Discord | [Discord Developer Portal](https://discord.com/developers/applications) | Bot authentication |
| Anthropic | [Anthropic Console](https://console.anthropic.com) | Claude AI responses |
| OpenAI | [OpenAI Platform](https://platform.openai.com/api-keys) | DALL-E images, Whisper |
| Google Cloud | [Google Cloud Console](https://console.cloud.google.com) | TTS, Speech-to-Text |
| ElevenLabs | [ElevenLabs](https://elevenlabs.io) | Premium TTS |
| Stability AI | [Stability AI](https://platform.stability.ai) | Stable Diffusion |
| Replicate | [Replicate](https://replicate.com) | Multiple AI models |
| AssemblyAI | [AssemblyAI](https://www.assemblyai.com) | Speech transcription |

---

## ⚡ Minimal Setup (Just to Get Started)

### Discord Bot
```env
DISCORD_BOT_TOKEN=your_token
ANTHROPIC_API_KEY=your_key
DATABASE_URL=sqlite:///helix_unified.db
```

### API Backend
```env
API_SECRET_KEY=your_secret
DATABASE_URL=sqlite:///helix_unified.db
API_PORT=8000
```

**That's it!** Everything else is optional and adds features.

---

## 🎨 Feature Enablement Matrix

| Want This Feature? | Add These Variables |
|-------------------|---------------------|
| **AI Conversations** | `ANTHROPIC_API_KEY` ✅ Required |
| **Voice TTS** | `GOOGLE_CLOUD_TTS_API_KEY` or `ELEVENLABS_API_KEY` |
| **Image Generation** | `OPENAI_API_KEY` or `STABILITY_API_KEY` |
| **Voice Transcription** | `OPENAI_API_KEY` or `ASSEMBLYAI_API_KEY` |
| **Webhooks** | `WEBHOOK_SECRET`, `WEBHOOK_URL` |
| **Sentiment Analysis** | Nothing! Built-in ✅ |
| **Auto-Moderation** | Nothing! Built-in ✅ |
| **Performance Monitoring** | Nothing! Built-in ✅ |

---

## 🚨 Common Mistakes

### ❌ DON'T DO THIS
```env
# Don't put Discord token in API service
# API Backend doesn't need it!
DISCORD_BOT_TOKEN=xxx  # ❌ Wrong service!

# Don't put API keys in database service
ANTHROPIC_API_KEY=xxx  # ❌ Database doesn't use this!
```

### ✅ DO THIS
```env
# Discord Bot Service
DISCORD_BOT_TOKEN=xxx  # ✅ Correct!
ANTHROPIC_API_KEY=xxx  # ✅ Correct!

# API Backend Service
API_SECRET_KEY=xxx     # ✅ Correct!
DATABASE_URL=xxx       # ✅ Correct!
```

---

## 💰 Cost Optimization

### Free Tier Options
- **Discord**: Free bot hosting
- **Railway**: $5/month credit (enough for small bots)
- **Anthropic**: Pay-as-you-go (very affordable)
- **SQLite**: Free (use `DATABASE_URL=sqlite:///helix_unified.db`)

### Paid But Worth It
- **Google Cloud TTS**: $4 per 1M characters
- **OpenAI DALL-E**: $0.04 per image
- **ElevenLabs**: $5/month for 30k characters

### Skip If Budget Tight
- Image generation (use free alternatives)
- Premium TTS (use Google Cloud free tier)
- Voice transcription (enable only when needed)

---

## 🔄 Variable Priority

### Priority 1: CRITICAL (Bot won't work without these)
```env
DISCORD_BOT_TOKEN=
ANTHROPIC_API_KEY=
DATABASE_URL=
```

### Priority 2: HIGH (Major features)
```env
GOOGLE_CLOUD_TTS_API_KEY=  # Voice features
API_SECRET_KEY=             # API security
```

### Priority 3: MEDIUM (Nice to have)
```env
OPENAI_API_KEY=      # Images & Whisper
ELEVENLABS_API_KEY=  # Better TTS
STABILITY_API_KEY=   # Image generation
```

### Priority 4: LOW (Optional enhancements)
```env
ASSEMBLYAI_API_KEY=  # Alternative transcription
REPLICATE_API_KEY=   # Alternative image gen
WEBHOOK_SECRET=      # Webhook security
```

---

## 📋 Copy-Paste Templates

### Template 1: Full Featured
```env
# Discord Bot Service
DISCORD_BOT_TOKEN=
DISCORD_CLIENT_ID=
ANTHROPIC_API_KEY=
OPENAI_API_KEY=
GOOGLE_CLOUD_TTS_API_KEY=
STABILITY_API_KEY=
DATABASE_URL=
LOG_LEVEL=INFO
MAX_AGENTS=16
```

### Template 2: Budget Friendly
```env
# Discord Bot Service
DISCORD_BOT_TOKEN=
ANTHROPIC_API_KEY=
DATABASE_URL=sqlite:///helix_unified.db
LOG_LEVEL=INFO
MAX_AGENTS=8
```

### Template 3: Voice Focused
```env
# Discord Bot Service
DISCORD_BOT_TOKEN=
ANTHROPIC_API_KEY=
GOOGLE_CLOUD_TTS_API_KEY=
OPENAI_API_KEY=
ASSEMBLYAI_API_KEY=
DATABASE_URL=
VOICE_AUTO_JOIN=true
MAX_VOICE_CONNECTIONS=10
```

---

## 🎓 Learning Path

### Week 1: Basic Setup
- Add `DISCORD_BOT_TOKEN`
- Add `ANTHROPIC_API_KEY`
- Use SQLite database
- Test basic commands

### Week 2: Add Voice
- Add `GOOGLE_CLOUD_TTS_API_KEY`
- Test voice features
- Configure voice settings

### Week 3: Add Images
- Add `OPENAI_API_KEY` or `STABILITY_API_KEY`
- Test image generation
- Create custom commands

### Week 4: Production Ready
- Switch to PostgreSQL
- Add monitoring
- Enable all features
- Scale as needed

---

## 🆘 Emergency Troubleshooting

### Bot Not Responding?
1. Check `DISCORD_BOT_TOKEN` ✅
2. Check `ANTHROPIC_API_KEY` ✅
3. Check bot has permissions in Discord ✅

### Voice Not Working?
1. Check `GOOGLE_CLOUD_TTS_API_KEY` ✅
2. Check bot has voice permissions ✅
3. Check `TTS_PROVIDER` is set ✅

### Images Not Generating?
1. Check `OPENAI_API_KEY` or `STABILITY_API_KEY` ✅
2. Check API quota/billing ✅
3. Check logs for errors ✅

### Database Errors?
1. Check `DATABASE_URL` format ✅
2. Check database is running ✅
3. Run migrations ✅

---

## 📞 Quick Help

**Need help?** Check these files:
- Full guide: `docs/RAILWAY_DEPLOYMENT_GUIDE.md`
- All variables: `docs/ENVIRONMENT_VARIABLES.md`
- Setup help: `docs/DEVELOPMENT_SETUP.md`
- Security: `SECURITY.md`

---

**Keep this card handy for quick reference! 📌**