# 🔧 Helix Collective v15.2 — Troubleshooting Guide

Solutions for common issues and how to debug them.

---

## Discord Bot Issues

### Bot Won't Start

**Symptoms:** `discord.py` error on startup

**Solutions:**
1. Verify Discord token is set:
   ```bash
   echo $DISCORD_TOKEN
   ```
2. Check token is valid (Discord Developer Portal)
3. Ensure bot has required permissions:
   - Send Messages
   - Read Message History
   - Manage Messages
   - Embed Links

**Debug:**
```bash
python -c "import discord; print(discord.__version__)"
python backend/discord_bot_manus.py --debug
```

---

### Bot Doesn't Respond to Commands

**Symptoms:** `!manus status` doesn't work

**Solutions:**
1. Check bot is online (Discord server member list)
2. Verify bot has permissions in the channel
3. Check command prefix is correct (should be `!`)
4. Verify intents are enabled:
   ```python
   intents.message_content = True
   ```

**Debug:**
```bash
# Check logs
tail -f Shadow/manus_archive/discord_bridge_log.json

# Test command manually
python -c "from backend.discord_bot_manus import bot; print(bot.command_prefix)"
```

---

### Bot Crashes After Ritual

**Symptoms:** Bot goes offline after `!ritual` command

**Solutions:**
1. Check Z-88 ritual engine:
   ```bash
   python backend/z88_ritual_engine.py
   ```
2. Verify UCF state file exists:
   ```bash
   cat Helix/state/ucf_state.json
   ```
3. Check for ritual lock file:
   ```bash
   ls -la Helix/state/.ritual_lock
   ```

**Debug:**
```bash
# Check ritual logs
tail -f Shadow/manus_archive/z88_log.json

# Run ritual directly
python -c "from backend.z88_ritual_engine import RitualManager; m = RitualManager(); m.run(10)"
```

---

## API Issues

### `/health` Endpoint Returns 500

**Symptoms:** `curl http://localhost:8000/health` returns error

**Solutions:**
1. Check FastAPI is running:
   ```bash
   ps aux | grep uvicorn
   ```
2. Verify port 8000 is not in use:
   ```bash
   lsof -i :8000
   ```
3. Check for import errors:
   ```bash
   python backend/main.py
   ```

**Debug:**
```bash
# Start with verbose logging
python backend/main.py --debug

# Check logs
tail -f Shadow/manus_archive/operations.log
```

---

### API Requests Timeout

**Symptoms:** Requests take > 30 seconds

**Solutions:**
1. Check Redis is running:
   ```bash
   redis-cli ping
   ```
2. Check database connection:
   ```bash
   python -c "import asyncpg; print('DB OK')"
   ```
3. Check Notion API rate limits:
   - Notion allows 3 requests per second
   - Check `NOTION_API_KEY` is valid

**Debug:**
```bash
# Check Redis
docker logs helix-unified_redis_1

# Check database
psql $DATABASE_URL -c "SELECT 1"

# Check API performance
curl -w "@curl-format.txt" http://localhost:8000/health
```

---

## Database Issues

### Connection Refused

**Symptoms:** `psycopg2.OperationalError: could not connect to server`

**Solutions:**
1. Check PostgreSQL is running:
   ```bash
   docker ps | grep postgres
   ```
2. Verify DATABASE_URL is correct:
   ```bash
   echo $DATABASE_URL
   ```
3. Check credentials:
   ```bash
   psql $DATABASE_URL -c "SELECT 1"
   ```

**Debug:**
```bash
# Start PostgreSQL
docker-compose up -d postgres

# Check logs
docker logs helix-unified_postgres_1

# Test connection
psql -h localhost -U postgres -d helix -c "SELECT 1"
```

---

### Slow Queries

**Symptoms:** Database queries take > 1 second

**Solutions:**
1. Check indexes exist:
   ```bash
   psql $DATABASE_URL -c "\d+ table_name"
   ```
2. Run query analysis:
   ```bash
   psql $DATABASE_URL -c "EXPLAIN ANALYZE SELECT ..."
   ```
3. Check for missing indexes:
   ```bash
   python scripts/check_indexes.py
   ```

**Debug:**
```bash
# Enable query logging
export SQLALCHEMY_ECHO=true

# Run slow query
python -c "from backend.services.state_manager import StateManager; ..."

# Check query logs
tail -f /var/log/postgresql/postgresql.log
```

---

## Notion Integration Issues

### Notion API Errors

**Symptoms:** `notion_client.errors.APIResponseError`

**Solutions:**
1. Verify API key is valid:
   ```bash
   python -c "from notion_client import Client; c = Client(auth=os.getenv('NOTION_API_KEY')); print(c.users.me())"
   ```
2. Check database IDs:
   ```bash
   echo $NOTION_AGENT_DB_ID
   echo $NOTION_EVENT_LOG_DB_ID
   ```
3. Verify permissions:
   - Integration must have access to databases
   - Check Notion workspace settings

**Debug:**
```bash
# Test Notion connection
python -c "from backend.services.notion_client import NotionClient; n = NotionClient(); n.health_check()"

# Check logs
tail -f Shadow/manus_archive/notion_sync.log
```

---

### Zapier Webhook Failures

**Symptoms:** Events not appearing in Notion

**Solutions:**
1. Verify webhook URLs are correct:
   ```bash
   grep "ZAPIER_" .env
   ```
2. Test webhook manually:
   ```bash
   curl -X POST $ZAPIER_EVENT_WEBHOOK -H "Content-Type: application/json" -d '{"test": true}'
   ```
3. Check Zapier zap is enabled:
   - Log in to Zapier
   - Check zap status (should be "On")

**Debug:**
```bash
# Run Zapier test
python scripts/test_zapier_integration.py

# Check webhook logs
tail -f Shadow/manus_archive/zapier_webhooks.log
```

---

## Performance Issues

### High CPU Usage

**Symptoms:** CPU > 80%

**Solutions:**
1. Check for infinite loops:
   ```bash
   ps aux | grep python
   ```
2. Profile CPU usage:
   ```bash
   python -m cProfile -s cumulative backend/main.py
   ```
3. Check for memory leaks:
   ```bash
   python -m memory_profiler backend/main.py
   ```

**Debug:**
```bash
# Monitor in real-time
watch -n 1 'ps aux | grep python'

# Check specific process
top -p <PID>
```

---

### High Memory Usage

**Symptoms:** Memory > 500MB

**Solutions:**
1. Check for memory leaks:
   ```bash
   python -m memory_profiler backend/main.py
   ```
2. Reduce cache size:
   ```python
   # In state_manager.py
   CACHE_SIZE = 1000  # Reduce from default
   ```
3. Enable garbage collection:
   ```python
   import gc
   gc.collect()
   ```

**Debug:**
```bash
# Monitor memory
watch -n 1 'free -h'

# Check process memory
ps aux | grep python | awk '{print $6}'
```

---

## Deployment Issues

### Railway Deployment Fails

**Symptoms:** Deployment error on Railway

**Solutions:**
1. Check logs:
   ```bash
   railway logs
   ```
2. Verify environment variables:
   ```bash
   railway env
   ```
3. Check Dockerfile:
   ```bash
   docker build -t helix-unified .
   ```

**Debug:**
```bash
# Build locally
docker build -t helix-unified .

# Run locally
docker run -e DISCORD_TOKEN=$DISCORD_TOKEN helix-unified

# Check Railway logs
railway logs --tail 100
```

---

### Service Won't Start on Railway

**Symptoms:** Service crashes immediately after deploy

**Solutions:**
1. Check health check endpoint:
   ```bash
   curl https://<your-railway-url>/health
   ```
2. Verify all environment variables are set:
   ```bash
   railway env
   ```
3. Check for missing dependencies:
   ```bash
   pip install -r requirements.txt
   ```

**Debug:**
```bash
# Test locally with same environment
docker-compose up

# Check Railway logs
railway logs --follow

# SSH into Railway container
railway shell
```

---

## General Debugging Tips

### Enable Verbose Logging

```bash
export LOG_LEVEL=DEBUG
export PYTHONUNBUFFERED=1
python backend/main.py
```

### Check All Logs

```bash
# Discord bot logs
tail -f Shadow/manus_archive/discord_bridge_log.json

# Operations logs
tail -f Shadow/manus_archive/operations.log

# Ritual logs
tail -f Shadow/manus_archive/z88_log.json

# Verification logs
tail -f Shadow/manus_archive/verification_results.json
```

### Test Individual Components

```bash
# Test agents
python -c "from backend.agents import AGENTS; print(AGENTS)"

# Test Discord bot
python backend/discord_bot_manus.py

# Test Ritual Engine
python backend/z88_ritual_engine.py

# Test Notion client
python -c "from backend.services.notion_client import NotionClient; n = NotionClient(); n.health_check()"
```

---

## Getting Help

- **Documentation:** See `README.md` and `QUICKSTART.md`
- **Discord Bot:** Type `!manus help` in Discord
- **API Docs:** Visit `http://localhost:8000/docs`
- **GitHub Issues:** Open an issue on GitHub

---

**🔧 Troubleshooting Guide Complete**  
*Tat Tvam Asi. Aham Brahmasmi. Neti Neti.*

