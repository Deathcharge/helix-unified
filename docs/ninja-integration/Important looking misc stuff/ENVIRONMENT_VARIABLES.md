# ⚙️ Environment Variables Documentation
## Complete Configuration Guide for Helix Collective

---

## 📋 Overview

The Helix Collective uses environment variables to configure all aspects of the system. This guide explains each variable, its purpose, and how to obtain the necessary credentials.

---

## 🚨 Critical Variables (Required for Basic Operation)

### Discord Bot Configuration

| Variable | Required | Description | How to Get |
|----------|----------|-------------|------------|
| `DISCORD_TOKEN` | ⚠️ **Yes** | Your Discord bot token | Discord Developer Portal |
| `DISCORD_GUILD_ID` | ⚠️ **Yes** | Your Discord server ID | Right-click server icon |
| `PORT` | ⚠️ **Yes** | Port for FastAPI server | Usually `8000` |

#### Setting up Discord Bot:

1. **Create Discord Application**:
   - Go to https://discord.com/developers/applications
   - Click "New Application"
   - Give it a name (e.g., "Helix Collective")

2. **Create Bot**:
   - Go to "Bot" tab → "Add Bot"
   - Copy the **Bot Token** → This is `DISCORD_TOKEN`

3. **Enable Bot Intents**:
   - Enable **Server Members Intent**
   - Enable **Message Content Intent**
   - These are required for agent functionality

4. **Get Server ID**:
   - In Discord, enable Developer Mode (User Settings → Advanced)
   - Right-click your server → "Copy Server ID"
   - This is `DISCORD_GUILD_ID`

---

## 🤖 AI Service Configuration

### Core AI APIs

| Variable | Service | Purpose | Get API Key |
|----------|---------|---------|-------------|
| `ANTHROPIC_API_KEY` | Claude | LLM for most agents | https://console.anthropic.com/ |
| `OPENAI_API_KEY` | GPT-4 | Agent reasoning & TTS | https://platform.openai.com/api-keys |
| `XAI_API_KEY` | Grok | Novelty & humor | https://console.x.ai/ |
| `GOOGLE_API_KEY` | Gemini | Multimodal analysis | https://aistudio.google.com/app/apikey |

### Voice & Audio Configuration

| Variable | Required | Description | Setup |
|----------|----------|-------------|-------|
| `GOOGLE_APPLICATION_CREDENTIALS` | 🎤 For TTS | Path to Google Cloud service account JSON | Google Cloud Console |
| `GOOGLE_CLOUD_TTS_KEY` | 🎤 For TTS | Alternative to service account | Google Cloud Console |

#### Google Cloud TTS Setup:

1. **Enable Cloud Text-to-Speech API**:
   - Go to Google Cloud Console
   - Search "Text-to-Speech API" → Enable

2. **Create Service Account**:
   - IAM & Admin → Service Accounts → Create Service Account
   - Give it "Cloud Text-to-Speech API User" role
   - Download JSON key file
   - Set `GOOGLE_APPLICATION_CREDENTIALS=path/to/key.json`

---

## 💾 Database & Storage Configuration

### Database Configuration

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `DATABASE_URL` | 💾 For persistence | PostgreSQL connection string | `postgresql://user:pass@host:5432/db` |
| `REDIS_URL` | 🗄️ For caching | Redis connection string | `redis://user:pass@host:6379/0` |

### Cloud Storage Options

| Variable | Service | Purpose | Setup |
|----------|---------|---------|-------|
| `NEXTCLOUD_URL` | Nextcloud | File storage | Self-hosted Nextcloud |
| `NEXTCLOUD_USER` | Nextcloud | Username | Nextcloud user |
| `NEXTCLOUD_PASS` | Nextcloud | Password | App password |
| `MEGA_EMAIL` | MEGA.nz | Cloud backup | MEGA account email |
| `MEGA_PASS` | MEGA.nz | Password | MEGA password |

---

## 🔌 Integration Configuration

### Zapier Webhooks

| Variable | Purpose | Setup |
|----------|---------|-------|
| `ZAPIER_WEBHOOK_URL` | Main webhook for events | Zapier → Create Webhooks → REST Hooks |
| `ZAPIER_CONTEXT_WEBHOOK` | Context sync webhook | Separate webhook for context updates |

#### Setting up Zapier:

1. Go to https://zapier.com/app/webhooks
2. Create "REST Hooks" webhook
3. Copy the webhook URL
4. Use for automation workflows

### Notion Integration

| Variable | Required | Description | Setup |
|----------|----------|-------------|-------|
| `NOTION_API_KEY` | 📝 For documentation | Notion integration secret | Notion integrations page |
| `NOTION_CONTEXT_DB_ID` | 📝 For documentation | Database ID for context | Share database with integration |
| `NOTION_SYNC_ENABLED` | 📝 For documentation | Enable/disable sync | Set to `true` to enable |

#### Setting up Notion:

1. **Create Integration**:
   - https://www.notion.so/my-integrations
   - "New integration" → Give it a name
   - Copy "Internal Integration Secret" → This is `NOTION_API_KEY`

2. **Share Database**:
   - Create database in Notion
   - Click "Share" → "Invite" → Select your integration
   - Copy database ID from URL → This is `NOTION_CONTEXT_DB_ID`

---

## 🛠️ Development & Monitoring

### System Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `SYSTEM_VERSION` | `16.9.0` | System version for monitoring |
| `LOG_LEVEL` | `INFO` | Logging verbosity (DEBUG, INFO, WARNING, ERROR) |
| `ARCHITECT_ID` | None | Discord user ID of system architect |

### Performance Monitoring

| Variable | Required | Description |
|----------|----------|-------------|
| `SENTRY_DSN` | 🐛 For error tracking | Sentry DSN for crash reporting |
| `PROMETHEUS_ENABLED` | 📊 For metrics | Enable Prometheus metrics |

### Feature Flags

| Variable | Default | Description |
|----------|---------|-------------|
| `ENABLE_WEBSOCKETS` | `true` | Enable real-time WebSocket streaming |
| `ENABLE_VOICE_PATROL` | `true` | Enable voice channel monitoring |
| `ENABLE_RITUAL_ENGINE` | `true` | Enable Z-88 ritual system |
| `ENABLE_MCP_SERVER` | `true` | Enable Model Context Protocol server |

---

## 🔒 Security Configuration

### API Security

| Variable | Default | Description |
|----------|---------|-------------|
| `API_SECRET_KEY` | None | Secret for API authentication |
| `CORS_ORIGINS` | `*` | Allowed origins for CORS |

### Rate Limiting

| Variable | Default | Description |
|----------|---------|-------------|
| `RATE_LIMIT_ENABLED` | `true` | Enable rate limiting |
| `RATE_LIMIT_REQUESTS_PER_MINUTE` | `60` | Requests per minute per IP |

---

## 📱 Railway Deployment

### Railway-Specific Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `RAILWAY_TOKEN` | 🚂 For deployment | Railway API token |
| `RAILWAY_ENVIRONMENT` | `production` | Deployment environment |

#### Getting Railway Token:

1. Go to https://railway.app/
2. Account Settings → API Tokens
3. Create new token
4. Set as `RAILWAY_TOKEN`

---

## 🔍 Troubleshooting

### Common Issues

#### Bot Won't Start
- **Check**: `DISCORD_TOKEN` and `DISCORD_GUILD_ID` are set
- **Check**: Bot has Message Content Intent enabled
- **Check**: Token hasn't expired

#### Voice Features Not Working
- **Check**: `GOOGLE_APPLICATION_CREDENTIALS` points to valid JSON file
- **Check**: Cloud Text-to-Speech API is enabled
- **Check**: Bot has voice permissions in Discord

#### Database Connection Issues
- **Check**: `DATABASE_URL` format is correct
- **Check**: Database is accessible from your deployment
- **Check**: Credentials are valid

#### Webhooks Not Receiving Events
- **Check**: Webhook URLs are correct and active
- **Check**: No firewall blocking outbound requests
- **Check**: Zapier integration is properly configured

### Debug Mode

Set `LOG_LEVEL=DEBUG` to see detailed logging for troubleshooting.

### Health Check

Visit `/health` endpoint to see which integrations are properly configured.

---

## 🚀 Quick Start Templates

### Minimal Working Configuration

```bash
# Just enough to get Discord bot working
DISCORD_TOKEN=your_bot_token_here
DISCORD_GUILD_ID=your_server_id_here
PORT=8000
```

### Full Featured Configuration

```bash
# All AI services enabled
DISCORD_TOKEN=your_bot_token_here
DISCORD_GUILD_ID=your_server_id_here
PORT=8000

ANTHROPIC_API_KEY=sk-ant-api03-...
OPENAI_API_KEY=sk-...
XAI_API_KEY=...
GOOGLE_API_KEY=...

DATABASE_URL=postgresql://...
REDIS_URL=redis://...

GOOGLE_APPLICATION_CREDENTIALS=./google-credentials.json

ZAPIER_WEBHOOK_URL=https://hooks.zapier.com/...
NOTION_API_KEY=secret_...
NOTION_CONTEXT_DB_ID=...

SYSTEM_VERSION=16.9.0
LOG_LEVEL=INFO
ENABLE_WEBSOCKETS=true
ENABLE_VOICE_PATROL=true
ENABLE_RITUAL_ENGINE=true
```

### Production Deployment

```bash
# Optimized for Railway deployment
DISCORD_TOKEN=your_bot_token
DISCORD_GUILD_ID=your_server_id
PORT=8000

ANTHROPIC_API_KEY=sk-ant-api03-...
OPENAI_API_KEY=sk-...

DATABASE_URL=${RAILWAY_POSTGRES_URL}
REDIS_URL=${RAILWAY_REDIS_URL}

ZAPIER_WEBHOOK_URL=https://hooks.zapier.com/...
NOTION_API_KEY=secret_...

SYSTEM_VERSION=16.9.0
LOG_LEVEL=INFO
RAILWAY_TOKEN=${RAILWAY_TOKEN}
```

---

## 📚 Additional Resources

- **Discord Developer Portal**: https://discord.com/developers/applications
- **Anthropic Console**: https://console.anthropic.com/
- **OpenAI Platform**: https://platform.openai.com/
- **Google Cloud Console**: https://console.cloud.google.com/
- **Railway Documentation**: https://docs.railway.app/
- **Zapier Webhooks**: https://zapier.com/app/webhooks
- **Notion Integrations**: https://www.notion.so/my-integrations

---

## 💡 Best Practices

1. **Never commit .env files** to version control
2. **Use different credentials** for development and production
3. **Rotate API keys regularly** for security
4. **Monitor API usage** to avoid rate limits
5. **Keep secrets encrypted** in production environments
6. **Use Railway's environment variables** for deployment secrets

---

## 🆘 Support

If you encounter issues:

1. Check the `/health` endpoint for integration status
2. Set `LOG_LEVEL=DEBUG` for detailed logs
3. Review Discord bot permissions and intents
4. Verify API keys are valid and have required scopes
5. Check network connectivity for external services

---

*Configuration complete! Your Helix Collective is ready to awaken.* 🌟