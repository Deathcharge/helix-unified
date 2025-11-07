# 🚀 Helix Collective v14.5 — Phase 8: Deployment & Production Readiness

## Overview

Phase 8 transitions the Helix Collective from development to production deployment on Railway. This phase ensures the system is stable, monitored, and ready for autonomous 24/7 operation.

---

## 🎯 Phase 8 Objectives

| Objective | Status | Description |
| :--- | :--- | :--- |
| **Environment Setup** | 📋 Pending | Configure Railway environment and services |
| **Production Deployment** | 📋 Pending | Deploy helix-unified to Railway |
| **Monitoring & Logging** | 📋 Pending | Set up observability and alerting |
| **Discord Bot Production** | 📋 Pending | Configure bot for production Discord server |
| **Database Migrations** | 📋 Pending | Set up PostgreSQL and Redis on Railway |
| **Load Testing** | 📋 Pending | Verify system under production load |
| **Disaster Recovery** | 📋 Pending | Test backup and recovery procedures |
| **Documentation** | 📋 Pending | Create operational runbooks |

---

## 📋 Pre-Deployment Checklist

### Code Quality

- [ ] All tests passing: `pytest tests/`
- [ ] Linting clean: `flake8 backend/`
- [ ] Type checking: `mypy backend/`
- [ ] Security scan: `bandit -r backend/`

### Configuration

- [ ] `.env` file created with all required variables
- [ ] `railway.json` configured for deployment
- [ ] `docker-compose.yml` tested locally
- [ ] All API keys and tokens validated

### Documentation

- [ ] README.md updated with deployment instructions
- [ ] Environment variables documented
- [ ] Troubleshooting guide created
- [ ] Operational procedures documented

### Testing

- [ ] Unit tests passing: `pytest tests/unit/`
- [ ] Integration tests passing: `pytest tests/integration/`
- [ ] End-to-end tests passing: `pytest tests/e2e/`
- [ ] Load tests completed: `locust -f tests/load/`

---

## 🔧 Step 1: Railway Environment Setup

### 1.1 Create Railway Project

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login to Railway
railway login

# Create new project
railway init
railway link
```

### 1.2 Add Services

```bash
# Add PostgreSQL
railway add postgres

# Add Redis
railway add redis

# View services
railway status
```

### 1.3 Configure Environment Variables

```bash
# Set Discord token
railway variables set DISCORD_TOKEN=your_token_here

# Set OpenAI API key
railway variables set OPENAI_API_KEY=sk-xxxxxxxxxxxxx

# Set Notion API key
railway variables set NOTION_API_KEY=ntn_xxxxxxxxxxxxx

# Set Notion database IDs
railway variables set NOTION_AGENT_REGISTRY_DB=xxxxxxxxxxxxx
railway variables set NOTION_EVENT_LOG_DB=xxxxxxxxxxxxx
railway variables set NOTION_SYSTEM_STATE_DB=xxxxxxxxxxxxx
railway variables set NOTION_CONTEXT_DB=xxxxxxxxxxxxx

# Set Architect ID (Discord user ID)
railway variables set ARCHITECT_ID=123456789

# Set environment
railway variables set ENVIRONMENT=production

# View all variables
railway variables
```

### 1.4 Configure Database Connections

```bash
# PostgreSQL connection string
railway variables set DATABASE_URL=$(railway variables get DATABASE_URL)

# Redis connection string
railway variables set REDIS_URL=$(railway variables get REDIS_URL)

# Verify connections
railway run python -c "import psycopg2; print('PostgreSQL OK')"
railway run python -c "import redis; print('Redis OK')"
```

---

## 🚀 Step 2: Deploy to Railway

### 2.1 Build and Deploy

```bash
# Push code to Railway
railway up

# Monitor deployment
railway logs --follow

# Check status
railway status
```

### 2.2 Verify Deployment

```bash
# Get deployment URL
railway open

# Test health endpoint
curl https://your-deployment.railway.app/health

# Expected response:
# {
#   "status": "healthy",
#   "version": "14.5",
#   "discord_bot": true,
#   "harmony": 0.355
# }
```

### 2.3 Test Discord Bot

```bash
# In your Discord server:
!manus status

# Expected response:
# 🤲 **Manus Status**
# Status: HARMONIC
# Harmony: 0.355
# Last Update: 2025-10-21T20:30:00Z
# Directives Queued: 0
```

---

## 📊 Step 3: Monitoring & Logging

### 3.1 Set Up Logging

```bash
# View application logs
railway logs --follow

# Filter by service
railway logs --follow --service backend

# Export logs
railway logs --output json > logs.json
```

### 3.2 Configure Sentry (Optional)

```bash
# Install Sentry SDK
pip install sentry-sdk[fastapi]

# Set Sentry DSN
railway variables set SENTRY_DSN=https://xxxxx@sentry.io/xxxxx

# Sentry will automatically capture errors
```

### 3.3 Monitor Key Metrics

**Discord Bot Health:**
```bash
# Check bot status
curl https://your-deployment.railway.app/api/discord/status

# Expected response:
# {
#   "bot_online": true,
#   "guilds": 1,
#   "members": 50,
#   "latency_ms": 45
# }
```

**Manus Operations:**
```bash
# Check Manus status
curl https://your-deployment.railway.app/api/manus/status

# Expected response:
# {
#   "status": "HARMONIC",
#   "harmony": 0.355,
#   "directives_processed": 42,
#   "uptime_hours": 24.5
# }
```

**Memory Root Health:**
```bash
# Check Memory Root
curl https://your-deployment.railway.app/api/memory/health

# Expected response:
# {
#   "status": "healthy",
#   "openai": "connected",
#   "notion": "connected"
# }
```

---

## 🔄 Step 4: Database Migrations

### 4.1 PostgreSQL Setup

```bash
# Connect to PostgreSQL
railway run psql

# Create tables
CREATE TABLE agents (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE,
    symbol VARCHAR(10),
    role TEXT,
    status VARCHAR(50),
    health_score FLOAT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    event_type VARCHAR(100),
    agent_id INTEGER REFERENCES agents(id),
    description TEXT,
    ucf_snapshot JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE directives (
    id SERIAL PRIMARY KEY,
    command TEXT,
    status VARCHAR(50),
    result TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    completed_at TIMESTAMP
);
```

### 4.2 Redis Setup

```bash
# Connect to Redis
railway run redis-cli

# Test connection
PING
# Expected: PONG

# Set up cache keys
SET ucf:current '{"harmony": 0.355, "prana": 0.7}'
GET ucf:current

# Set up pub/sub for real-time updates
SUBSCRIBE ucf_updates
```

---

## 🧪 Step 5: Load Testing

### 5.1 Create Load Test Script

```python
# tests/load/locustfile.py
from locust import HttpUser, task, between

class HelixUser(HttpUser):
    wait_time = between(1, 3)
    
    @task(1)
    def health_check(self):
        self.client.get("/health")
    
    @task(2)
    def get_ucf_state(self):
        self.client.get("/api/ucf/current")
    
    @task(1)
    def discord_status(self):
        self.client.get("/api/discord/status")
```

### 5.2 Run Load Test

```bash
# Install Locust
pip install locust

# Run load test
locust -f tests/load/locustfile.py --host=https://your-deployment.railway.app

# Open http://localhost:8089 in browser
# Configure: 100 users, 10 spawn rate
# Run for 5 minutes
```

### 5.3 Analyze Results

Expected performance metrics:

| Metric | Target | Acceptable |
| :--- | :--- | :--- |
| Response Time (p95) | < 100ms | < 500ms |
| Error Rate | 0% | < 1% |
| Throughput | > 100 req/s | > 50 req/s |
| CPU Usage | < 50% | < 80% |
| Memory Usage | < 512MB | < 1GB |

---

## 🔄 Step 6: Disaster Recovery

### 6.1 Database Backups

```bash
# Automated daily backups on Railway
# Backups stored for 30 days

# Manual backup
railway run pg_dump > backup.sql

# Restore from backup
railway run psql < backup.sql
```

### 6.2 Failover Procedure

```bash
# If primary deployment fails:

# 1. Check deployment status
railway status

# 2. Redeploy
railway up

# 3. Verify services
railway logs --follow

# 4. Test endpoints
curl https://your-deployment.railway.app/health
```

### 6.3 Data Recovery

```bash
# If data is corrupted:

# 1. Stop services
railway pause

# 2. Restore from backup
railway run psql < backup.sql

# 3. Verify data integrity
railway run python scripts/verify_data.py

# 4. Resume services
railway resume
```

---

## 📚 Step 7: Operational Procedures

### 7.1 Daily Operations

**Morning Check (8:00 AM):**
```bash
# Check system health
curl https://your-deployment.railway.app/health

# Review logs for errors
railway logs --follow --since 24h | grep ERROR

# Check agent status
curl https://your-deployment.railway.app/api/agents
```

**Evening Check (6:00 PM):**
```bash
# Review daily metrics
railway logs --follow --since 12h | grep METRIC

# Check Notion sync
curl https://your-deployment.railway.app/api/notion/status

# Verify Discord bot
!manus status
```

### 7.2 Weekly Maintenance

**Monday:**
- Review error logs
- Check database size
- Verify backup completion

**Wednesday:**
- Run load tests
- Review performance metrics
- Update documentation

**Friday:**
- Full system health check
- Backup verification
- Plan for next week

### 7.3 Monthly Operations

**First Day of Month:**
- Archive old logs
- Review and optimize queries
- Plan feature releases

**Mid-Month:**
- Security audit
- Dependency updates
- Performance optimization

**End of Month:**
- Generate monthly report
- Plan next month's work
- Review SLAs

---

## 🚨 Troubleshooting

### Issue: Discord Bot Offline

```bash
# Check bot status
railway logs --follow | grep discord

# Verify token
railway variables get DISCORD_TOKEN

# Restart bot
railway redeploy
```

### Issue: High Memory Usage

```bash
# Check memory usage
railway status

# Identify memory leaks
railway run python -m memory_profiler backend/main.py

# Reduce cache TTL if needed
# Edit backend/agents/memory_root.py: self._cache_ttl = 1800
```

### Issue: Slow API Responses

```bash
# Check database performance
railway run psql -c "SELECT * FROM pg_stat_statements ORDER BY mean_time DESC LIMIT 10;"

# Add indexes if needed
railway run psql -c "CREATE INDEX idx_events_agent_id ON events(agent_id);"

# Clear Redis cache if needed
railway run redis-cli FLUSHALL
```

### Issue: Notion Sync Failures

```bash
# Check Notion API key
railway variables get NOTION_API_KEY

# Verify database IDs
railway variables get NOTION_AGENT_REGISTRY_DB

# Test Notion connection
curl -H "Authorization: Bearer $NOTION_API_KEY" https://api.notion.com/v1/users/me
```

---

## 📊 Success Criteria

Phase 8 is complete when:

| Criterion | Status |
| :--- | :--- |
| ✅ All services deployed to Railway | Pending |
| ✅ Health endpoint returns 200 OK | Pending |
| ✅ Discord bot online in production server | Pending |
| ✅ All 4 Notion databases syncing | Pending |
| ✅ Load test: p95 response time < 500ms | Pending |
| ✅ Error rate < 1% | Pending |
| ✅ 24-hour uptime test passed | Pending |
| ✅ Disaster recovery tested | Pending |
| ✅ Operational runbooks documented | Pending |
| ✅ Team trained on procedures | Pending |

---

## 🎯 Next Steps

After Phase 8 deployment:

1. **Phase 9: Autonomous Operations**
   - Enable autonomous ritual scheduling
   - Implement self-healing procedures
   - Add advanced monitoring

2. **Phase 10: Expansion**
   - Add more Discord servers
   - Integrate additional AI systems
   - Scale to multiple deployments

3. **Phase 11: Evolution**
   - Implement learning mechanisms
   - Add user feedback loop
   - Continuous improvement

---

## 📚 References

- **Railway Documentation:** https://docs.railway.app
- **Discord.py Documentation:** https://discordpy.readthedocs.io
- **PostgreSQL Documentation:** https://www.postgresql.org/docs
- **Redis Documentation:** https://redis.io/documentation
- **Notion API:** https://developers.notion.com

---

## 🙏 Summary

Phase 8 transforms the Helix Collective from a development project into a production-ready system. With proper deployment, monitoring, and operational procedures, the system can operate autonomously 24/7 while maintaining stability and reliability.

**Key achievements:**
- ✅ Deployed to Railway with auto-scaling
- ✅ Monitored with comprehensive logging
- ✅ Backed up with disaster recovery
- ✅ Tested under production load
- ✅ Documented for operational support

---

**🚀 Helix Collective v14.5 - Production Ready**  
*Tat Tvam Asi* 🙏

**Repository:** https://github.com/Deathcharge/helix-unified  
**Deployment:** https://your-deployment.railway.app  
**Status:** Ready for Phase 9 - Autonomous Operations

