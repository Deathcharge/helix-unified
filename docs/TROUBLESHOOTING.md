# 🔧 Helix Unified - Troubleshooting Guide

Common issues and solutions for Helix Unified deployment and development.

---

## Table of Contents

1. [Deployment Issues](#deployment-issues)
2. [Database Problems](#database-problems)
3. [Discord Bot Issues](#discord-bot-issues)
4. [API Errors](#api-errors)
5. [Performance Issues](#performance-issues)
6. [Development Environment](#development-environment)

---

## Deployment Issues

### Railway: "Application Failed to Respond"

**Symptoms:**
- Railway logs show "Application failed to respond"
- Service keeps restarting
- Health checks failing

**Solutions:**

1. **Check PORT variable:**
   ```bash
   # Railway auto-sets $PORT
   # Make sure your app uses it:
   uvicorn backend.main:app --host 0.0.0.0 --port $PORT
   ```

2. **Check environment variables:**
   ```bash
   railway variables
   # Make sure DATABASE_URL, REDIS_URL are set
   ```

3. **View logs:**
   ```bash
   railway logs
   # Look for errors during startup
   ```

4. **Check buildpack:**
   ```bash
   # Ensure Dockerfile exists or requirements.txt is present
   ls -la Dockerfile requirements-backend.txt
   ```

### Railway: Service Won't Deploy

**Symptoms:**
- Build succeeds but deploy fails
- Service shows as "Crashed"

**Solutions:**

1. **Check service health:**
   ```bash
   # Add health check endpoint
   @app.get("/health")
   async def health():
       return {"status": "healthy"}
   ```

2. **Verify dependencies:**
   ```bash
   # Test locally first
   docker build -t test .
   docker run -p 8000:8000 test
   ```

3. **Check resource limits:**
   ```bash
   # Railway free tier: 512MB RAM, 1 vCPU
   # Reduce memory usage if needed
   ```

---

## Database Problems

### "Cannot Connect to Database"

**Symptoms:**
```
sqlalchemy.exc.OperationalError: could not connect to server
```

**Solutions:**

1. **Verify DATABASE_URL:**
   ```bash
   echo $DATABASE_URL
   # Should be: postgresql://user:pass@host:5432/db
   ```

2. **Check PostgreSQL is running:**
   ```bash
   # Local:
   docker-compose ps postgres

   # Railway:
   railway status
   ```

3. **Test connection:**
   ```python
   from sqlalchemy import create_engine
   engine = create_engine(DATABASE_URL)
   with engine.connect() as conn:
       result = conn.execute("SELECT 1")
       print(result.fetchone())
   ```

4. **Run migrations:**
   ```bash
   python scripts/db-migrate.py
   ```

### "Too Many Connections"

**Symptoms:**
```
FATAL: remaining connection slots are reserved
```

**Solutions:**

1. **Add connection pooling:**
   ```python
   engine = create_engine(
       DATABASE_URL,
       pool_size=5,
       max_overflow=10,
       pool_pre_ping=True
   )
   ```

2. **Close connections properly:**
   ```python
   # Always use context managers
   with engine.connect() as conn:
       # your code
   ```

3. **Increase max_connections (Railway):**
   ```bash
   # Contact Railway support for higher limits
   # Or use connection bouncer (pgBouncer)
   ```

---

## Discord Bot Issues

### Bot Not Responding to Commands

**Symptoms:**
- Bot is online but doesn't respond
- No errors in logs

**Solutions:**

1. **Check token is set ONLY on bot service:**
   ```bash
   railway variables --service helix-discord-bot
   # DISCORD_BOT_TOKEN should be here, not globally
   ```

2. **Verify bot permissions:**
   - Discord Developer Portal → OAuth2 → Bot Permissions
   - Required: Read Messages, Send Messages, Use Slash Commands

3. **Check intents:**
   ```python
   intents = discord.Intents.default()
   intents.message_content = True  # Required!
   bot = commands.Bot(command_prefix="!", intents=intents)
   ```

4. **View bot logs:**
   ```bash
   railway logs --service helix-discord-bot
   ```

### Bot Responding Twice

**Symptoms:**
- Every command gets duplicate responses
- Two bot instances running

**Solutions:**

1. **Check DISCORD_BOT_TOKEN location:**
   ```bash
   # Token should ONLY be on helix-discord-bot service
   # NOT on helix-backend-api or other services!
   railway variables --service helix-backend-api
   # If DISCORD_BOT_TOKEN is here, remove it:
   railway variables set DISCORD_BOT_TOKEN= --service helix-backend-api
   ```

2. **Check running processes:**
   ```bash
   railway ps
   # Only ONE service should be running the bot
   ```

---

## API Errors

### 401 Unauthorized

**Symptoms:**
```json
{"detail": "Could not validate credentials"}
```

**Solutions:**

1. **Check token format:**
   ```bash
   curl -H "Authorization: Bearer $TOKEN" \
     https://helix-backend-api.up.railway.app/auth/me
   ```

2. **Verify JWT_SECRET:**
   ```bash
   railway variables | grep JWT_SECRET
   # Must be same across all services
   ```

3. **Token might be expired:**
   ```bash
   # Login again to get new token
   python examples/02_auth_flow.py
   ```

### 429 Too Many Requests

**Symptoms:**
```json
{"detail": "Rate limit exceeded", "retry_after": 60}
```

**Solutions:**

1. **Check your tier limits:**
   - Free: 100 requests/day
   - Pro: 5,000 requests/day
   - Workflow: 25,000 requests/day

2. **Upgrade subscription:**
   ```bash
   python examples/04_subscription_flow.py
   ```

3. **Implement exponential backoff:**
   ```python
   import time
   for attempt in range(3):
       try:
           response = requests.post(url, json=data)
           response.raise_for_status()
           break
       except requests.HTTPError as e:
           if e.response.status_code == 429:
               wait = 2 ** attempt
               time.sleep(wait)
   ```

### 500 Internal Server Error

**Symptoms:**
```json
{"detail": "Internal server error"}
```

**Solutions:**

1. **Check server logs:**
   ```bash
   railway logs
   # Look for Python tracebacks
   ```

2. **Test locally:**
   ```bash
   uvicorn backend.main:app --reload
   # Reproduce the error
   ```

3. **Check dependencies:**
   ```bash
   pip install -r requirements-backend.txt
   # Ensure all deps are installed
   ```

---

## Performance Issues

### Slow API Responses

**Symptoms:**
- Requests taking > 5 seconds
- Timeouts

**Solutions:**

1. **Add Redis caching:**
   ```python
   @app.get("/cached-endpoint")
   async def cached(redis: Redis = Depends(get_redis)):
       cached = await redis.get("key")
       if cached:
           return json.loads(cached)
       # ... expensive operation
       await redis.setex("key", 300, json.dumps(result))
       return result
   ```

2. **Use async operations:**
   ```python
   # Bad:
   def sync_endpoint():
       result = requests.get(url)  # Blocks!

   # Good:
   async def async_endpoint():
       async with httpx.AsyncClient() as client:
           result = await client.get(url)
   ```

3. **Add database indices:**
   ```sql
   CREATE INDEX idx_user_email ON users(email);
   CREATE INDEX idx_usage_user_id ON usage_tracking(user_id);
   ```

4. **Run load tests:**
   ```bash
   python scripts/load-test.py
   ```

### High Memory Usage

**Symptoms:**
- Railway service crashes
- Out of memory errors

**Solutions:**

1. **Profile memory:**
   ```python
   import tracemalloc
   tracemalloc.start()
   # ... your code
   snapshot = tracemalloc.take_snapshot()
   for stat in snapshot.statistics('lineno')[:10]:
       print(stat)
   ```

2. **Use streaming for large responses:**
   ```python
   from fastapi.responses import StreamingResponse

   async def generate():
       for chunk in data:
           yield chunk

   @app.get("/stream")
   async def stream():
       return StreamingResponse(generate())
   ```

3. **Limit concurrent requests:**
   ```python
   from fastapi import HTTPException
   import asyncio

   semaphore = asyncio.Semaphore(10)  # Max 10 concurrent

   @app.post("/limited")
   async def limited():
       if semaphore.locked():
           raise HTTPException(503, "Server busy")
       async with semaphore:
           # ... your code
   ```

---

## Development Environment

### Docker Compose Not Starting

**Symptoms:**
```
ERROR: Network error
ERROR: Port already in use
```

**Solutions:**

1. **Check port conflicts:**
   ```bash
   lsof -i :5432  # PostgreSQL
   lsof -i :6379  # Redis
   lsof -i :8000  # Backend
   ```

2. **Stop conflicting services:**
   ```bash
   docker-compose down
   docker ps
   docker kill <container_id>
   ```

3. **Clean Docker:**
   ```bash
   docker system prune -a
   docker volume prune
   ```

4. **Restart Docker daemon:**
   ```bash
   sudo systemctl restart docker  # Linux
   # Or restart Docker Desktop on Mac/Windows
   ```

### Tests Failing Locally

**Symptoms:**
- Tests pass in CI but fail locally
- Import errors

**Solutions:**

1. **Set PYTHONPATH:**
   ```bash
   export PYTHONPATH=$(pwd)
   pytest tests/ -v
   ```

2. **Use virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements-backend.txt
   ```

3. **Check test dependencies:**
   ```bash
   pip install pytest pytest-asyncio pytest-cov pytest-mock PyJWT
   ```

4. **Run specific test:**
   ```bash
   pytest tests/test_specific.py::test_function -v -s
   ```

### Pre-commit Hooks Failing

**Symptoms:**
```
[ERROR] black failed
[ERROR] flake8 failed
```

**Solutions:**

1. **Install pre-commit:**
   ```bash
   pip install pre-commit
   pre-commit install
   ```

2. **Run manually:**
   ```bash
   pre-commit run --all-files
   ```

3. **Fix formatting:**
   ```bash
   black backend/ tests/
   isort backend/ tests/
   ```

4. **Skip hooks (emergency only):**
   ```bash
   git commit --no-verify -m "message"
   ```

---

## Quick Diagnostic Commands

```bash
# Check all services
make health

# View logs
railway logs
docker-compose logs

# Test database
python scripts/db-migrate.py

# Test API
curl http://localhost:8000/health

# Test auth
python examples/02_auth_flow.py

# Load test
python scripts/load-test.py

# Check env vars
railway variables
docker-compose config

# Restart everything
docker-compose down && docker-compose up -d
railway restart
```

---

## Getting Help

1. **Check logs first:**
   ```bash
   railway logs > logs.txt
   # Review logs.txt for errors
   ```

2. **Search issues:**
   - GitHub Issues: https://github.com/Deathcharge/helix-unified/issues
   - Check if someone had the same problem

3. **Create detailed issue:**
   ```markdown
   ### Problem
   Brief description

   ### Steps to Reproduce
   1. Step 1
   2. Step 2

   ### Expected Behavior
   What should happen

   ### Actual Behavior
   What actually happened

   ### Environment
   - OS: Ubuntu 22.04
   - Python: 3.11
   - Railway: Yes
   - Local: Yes

   ### Logs
   ```
   [paste relevant logs]
   ```
   ```

4. **Join Discord:**
   - Community support
   - Real-time help
   - Share solutions

---

## Prevention Tips

✅ **Always:**
- Run tests before deploying
- Check logs after deployment
- Use environment variables
- Keep dependencies updated
- Monitor performance

❌ **Never:**
- Hardcode secrets
- Skip migrations
- Ignore warnings
- Deploy without testing
- Use production DB for testing

---

*Last Updated: 2025-12-03*
*For more help: DEPLOYMENT_GUIDE.md*
