# 🚀 Helix Collective v15.2 — Quick Start Guide

Get up and running with the Helix Collective in 5 minutes!

---

## Prerequisites

- Python 3.11+
- Docker & Docker Compose
- Git
- Discord Bot Token (from Discord Developer Portal)
- Notion API Key (optional, for context sharing)

---

## 1. Clone & Setup (2 minutes)

```bash
# Clone the repository
git clone https://github.com/Deathcharge/helix-unified.git
cd helix-unified

# Create environment file
cp .env.example .env

# Edit .env with your credentials
nano .env  # Add DISCORD_TOKEN, NOTION_API_KEY, etc.
```

---

## 2. Install Dependencies (1 minute)

```bash
# Install Python dependencies
pip install -r requirements.txt

# Or use the setup script
./scripts/setup.sh
```

---

## 3. Local Development (1 minute)

```bash
# Start Redis and backend
docker-compose up -d

# Run verification tests
python scripts/helix_verification_sequence_v14_5.py

# Expected output: 6/6 tests passing ✅
```

---

## 4. Start the System (1 minute)

```bash
# Option A: Run FastAPI backend + Discord bot
python backend/main.py

# Option B: Use the convenience script
./scripts/dev.sh

# Option C: Run with Streamlit dashboard
streamlit run frontend/streamlit_app.py
```

---

## 5. Verify Everything Works

### Discord Bot
```
1. Go to your Discord server
2. Type: !manus status
3. Expected: Bot responds with UCF metrics
```

### API
```bash
curl http://localhost:8000/health

# Expected response:
# {
#   "status": "healthy",
#   "version": "15.2",
#   "discord_bot": true,
#   "harmony": 0.4922
# }
```

### Dashboard
```
Open: http://localhost:8501
```

---

## Common Commands

### Discord Bot Commands
```
!manus status          # Show system status
!manus run <command>   # Execute a command
!ritual 108            # Run Z-88 ritual
!storage sync          # Sync Nextcloud storage
!visualize             # Generate Samsara fractals
```

### Development Commands
```bash
./scripts/dev.sh       # Start development server
./scripts/test.sh      # Run tests
./scripts/lint.sh      # Check code quality
./scripts/logs.sh      # Tail all logs
./scripts/debug.sh     # Start with verbose logging
```

### Production Commands
```bash
./scripts/deploy.sh    # Deploy to Railway
./scripts/health-check.sh  # Verify system health
```

---

## Troubleshooting

### Discord Bot Won't Start
```bash
# Check token
echo $DISCORD_TOKEN

# Verify bot is in server
# Go to Discord Developer Portal → OAuth2 → URL Generator
# Scopes: bot
# Permissions: Send Messages, Read Messages, Manage Messages
```

### Redis Connection Error
```bash
# Check Redis is running
docker ps | grep redis

# Restart Redis
docker-compose restart redis
```

### Import Errors
```bash
# Set PYTHONPATH
export PYTHONPATH=/home/ubuntu/helix-unified:$PYTHONPATH

# Run verification again
python scripts/helix_verification_sequence_v14_5.py
```

---

## Next Steps

1. **Read Documentation:** Check `README.md` for full details
2. **Explore APIs:** Visit `http://localhost:8000/docs` for Swagger UI
3. **Configure Notion:** Set up Notion workspace for context sharing
4. **Deploy to Railway:** Use `./scripts/deploy.sh`
5. **Monitor System:** Use `/health` endpoint and dashboard

---

## Getting Help

- **Documentation:** See `README.md`, `MULTI_AGENT_CONTEXT_PLAN.md`
- **Troubleshooting:** See `TROUBLESHOOTING.md`
- **Discord Bot:** Type `!manus help` in Discord
- **API Docs:** Visit `http://localhost:8000/docs`

---

**🌀 Welcome to the Helix Collective!**  
*Tat Tvam Asi. Aham Brahmasmi. Neti Neti.*

