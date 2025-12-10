# 🏗️ Helix Collective SaaS - Infrastructure & DevOps Guide

**Last Updated:** November 29, 2024
**Status:** Production-Ready Architecture
**Target:** Scalable from 100 to 100,000+ users

---

## 📋 Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Railway Deployment](#railway-deployment)
3. [Database Setup](#database-setup)
4. [Caching Strategy](#caching-strategy)
5. [Security & Compliance](#security--compliance)
6. [Monitoring & Observability](#monitoring--observability)
7. [Scaling Strategy](#scaling-strategy)
8. [Disaster Recovery](#disaster-recovery)
9. [Cost Optimization](#cost-optimization)
10. [CI/CD Pipeline](#cicd-pipeline)

---

## 🏛️ Architecture Overview

### High-Level System Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                         USERS                                 │
│  (Web Dashboard, API Clients, Mobile Apps, Integrations)     │
└───────────────────────┬──────────────────────────────────────┘
                        │
                        ▼
┌──────────────────────────────────────────────────────────────┐
│                    CLOUDFLARE CDN                             │
│  - DDoS Protection                                            │
│  - Rate Limiting (Layer 7)                                    │
│  - SSL/TLS Termination                                        │
│  - Caching (Static Assets)                                    │
└───────────────────────┬──────────────────────────────────────┘
                        │
                        ▼
┌──────────────────────────────────────────────────────────────┐
│                 RAILWAY - API GATEWAY                         │
│  - FastAPI Application (Python 3.11+)                         │
│  - JWT Authentication                                         │
│  - Request Validation                                         │
│  - Rate Limiting (Per-user tier)                              │
└───────┬───────────────┬────────────────┬─────────────────────┘
        │               │                │
        ▼               ▼                ▼
┌───────────────┐ ┌─────────────┐ ┌────────────────────┐
│ Router        │ │ Agent       │ │ Memory Service     │
│ Service       │ │ Service     │ │                    │
│               │ │             │ │ - Conversations    │
│ - LLM Routing │ │ - Task Queue│ │ - Prompts          │
│ - Load Balance│ │ - Execution │ │ - Vector Search    │
│ - Optimization│ │ - Streaming │ │                    │
└───────┬───────┘ └──────┬──────┘ └────────┬───────────┘
        │                │                 │
        ▼                ▼                 ▼
┌──────────────────────────────────────────────────────────────┐
│                    DATA LAYER                                 │
│                                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │ PostgreSQL   │  │ Redis        │  │ Vector DB    │       │
│  │              │  │              │  │ (Pinecone)   │       │
│  │ - Users      │  │ - Sessions   │  │              │       │
│  │ - Usage      │  │ - Rate Limits│  │ - Embeddings │       │
│  │ - Prompts    │  │ - Cache      │  │ - Semantic   │       │
│  │ - Convos     │  │ - Queues     │  │   Search     │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
└──────────────────────────────────────────────────────────────┘
        │                │                 │
        ▼                ▼                 ▼
┌──────────────────────────────────────────────────────────────┐
│                  EXTERNAL SERVICES                            │
│                                                               │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐    │
│  │Anthropic │  │ OpenAI   │  │   xAI    │  │Perplexity│    │
│  │(Claude)  │  │  (GPT)   │  │  (Grok)  │  │  (Llama) │    │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘    │
│                                                               │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                   │
│  │  Stripe  │  │  SendGrid│  │  Sentry  │                   │
│  │(Payments)│  │  (Email) │  │ (Errors) │                   │
│  └──────────┘  └──────────┘  └──────────┘                   │
└──────────────────────────────────────────────────────────────┘
```

### Service Breakdown

**1. API Gateway (FastAPI)**
- Single entry point for all requests
- Authentication & authorization
- Request validation & sanitization
- Rate limiting enforcement
- Metrics collection

**2. Router Service**
- Multi-LLM request routing
- Load balancing across providers
- Cost optimization logic
- Fallback & retry mechanisms

**3. Agent Service**
- Agent task queue (Celery/Redis)
- Agent execution runtime
- Response streaming (WebSockets)
- Result caching

**4. Memory Service**
- Conversation storage & retrieval
- Prompt library CRUD
- Vector embeddings (semantic search)
- Context retrieval for LLM calls

**5. Analytics Service**
- Usage tracking & aggregation
- Cost calculation
- Dashboard metrics
- Billing data preparation

---

## 🚂 Railway Deployment

### Railway Services Configuration

**Service 1: API Gateway**
```yaml
# railway.api.toml
[build]
builder = "NIXPACKS"
buildCommand = "pip install -r requirements.txt"

[deploy]
startCommand = "uvicorn backend.app:app --host 0.0.0.0 --port $PORT"
healthcheckPath = "/health"
healthcheckTimeout = 60
restartPolicyType = "ON_FAILURE"
restartPolicyMaxRetries = 3

[env]
PYTHON_VERSION = "3.11"
PORT = "8000"
WORKERS = "4"
```

**Service 2: Agent Worker**
```yaml
# railway.worker.toml
[build]
builder = "NIXPACKS"

[deploy]
startCommand = "celery -A backend.agents.worker worker --loglevel=info --concurrency=4"
restartPolicyType = "ON_FAILURE"
```

**Service 3: PostgreSQL**
```yaml
# Managed by Railway
# Automatic backups, scaling, monitoring
# Version: 15+
```

**Service 4: Redis**
```yaml
# Managed by Railway
# Version: 7+
# Max memory: 1GB (scale as needed)
```

### Environment Variables

**Required:**
```bash
# Database
DATABASE_URL=postgresql://user:pass@host:5432/helix
REDIS_URL=redis://default:pass@host:6379

# API Keys
ANTHROPIC_API_KEY=sk-ant-xxx
OPENAI_API_KEY=sk-xxx
XAI_API_KEY=xai-xxx
PERPLEXITY_API_KEY=pplx-xxx

# Authentication
JWT_SECRET_KEY=<generate-random-256-bit-key>
API_KEY_ENCRYPTION_KEY=<generate-random-256-bit-key>

# Payments
STRIPE_SECRET_KEY=sk_live_xxx
STRIPE_WEBHOOK_SECRET=whsec_xxx

# External Services
SENTRY_DSN=https://xxx@sentry.io/xxx
SENDGRID_API_KEY=SG.xxx
```

**Optional:**
```bash
# Vector Database
PINECONE_API_KEY=xxx
PINECONE_ENVIRONMENT=us-west1-gcp

# Feature Flags
ENABLE_AGENT_MARKETPLACE=true
ENABLE_CONVERSATION_MEMORY=true
ENABLE_COST_OPTIMIZATION=true

# Scaling
MAX_CONNECTIONS_PER_USER=10
CELERY_WORKER_CONCURRENCY=4
REDIS_MAX_CONNECTIONS=50

# Monitoring
POSTHOG_API_KEY=phc_xxx
DATADOG_API_KEY=xxx
```

### Deployment Commands

**Initial Setup:**
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Initialize project
railway init

# Link to existing project
railway link

# Add PostgreSQL
railway add --database postgresql

# Add Redis
railway add --database redis

# Deploy
railway up
```

**Continuous Deployment:**
```bash
# Railway auto-deploys on git push to main
git push origin main

# Manual deploy
railway up

# Deploy specific service
railway up --service api-gateway
```

---

## 🗄️ Database Setup

### PostgreSQL Schema

**Users Table:**
```sql
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  tier VARCHAR(20) DEFAULT 'free', -- free, pro, team, enterprise
  status VARCHAR(20) DEFAULT 'active', -- active, suspended, deleted
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_tier ON users(tier);
```

**API Keys Table:**
```sql
CREATE TABLE api_keys (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  key_hash VARCHAR(255) UNIQUE NOT NULL, -- SHA-256 hash
  key_prefix VARCHAR(20) NOT NULL, -- For display: "hx_user_1234"
  name VARCHAR(255),
  scopes TEXT[], -- ['chat', 'agents', 'prompts']
  rate_limit_override INTEGER, -- NULL = use tier default
  expires_at TIMESTAMP,
  last_used_at TIMESTAMP,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_api_keys_user_id ON api_keys(user_id);
CREATE INDEX idx_api_keys_key_hash ON api_keys(key_hash);
```

**Usage Table (Partitioned by month):**
```sql
CREATE TABLE usage (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id),
  api_key_id UUID REFERENCES api_keys(id),
  endpoint VARCHAR(100) NOT NULL, -- '/v1/chat', '/v1/agents/kael'
  model VARCHAR(50) NOT NULL, -- 'claude-3-haiku', 'gpt-4-turbo'
  provider VARCHAR(50) NOT NULL, -- 'anthropic', 'openai'
  prompt_tokens INTEGER NOT NULL,
  completion_tokens INTEGER NOT NULL,
  total_tokens INTEGER NOT NULL,
  cost_usd DECIMAL(10, 6) NOT NULL,
  latency_ms INTEGER,
  status VARCHAR(20), -- 'success', 'error', 'rate_limited'
  created_at TIMESTAMP DEFAULT NOW()
) PARTITION BY RANGE (created_at);

-- Create monthly partitions
CREATE TABLE usage_2024_11 PARTITION OF usage
  FOR VALUES FROM ('2024-11-01') TO ('2024-12-01');

CREATE TABLE usage_2024_12 PARTITION OF usage
  FOR VALUES FROM ('2024-12-01') TO ('2025-01-01');

CREATE INDEX idx_usage_user_id ON usage(user_id);
CREATE INDEX idx_usage_created_at ON usage(created_at);
```

**Prompts Table:**
```sql
CREATE TABLE prompts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  name VARCHAR(255) NOT NULL,
  template TEXT NOT NULL,
  tags TEXT[],
  version INTEGER DEFAULT 1,
  is_public BOOLEAN DEFAULT FALSE,
  model_preference VARCHAR(50),
  default_parameters JSONB, -- {"temperature": 0.7, "max_tokens": 1000}
  execution_count INTEGER DEFAULT 0,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_prompts_user_id ON prompts(user_id);
CREATE INDEX idx_prompts_tags ON prompts USING GIN(tags);
CREATE INDEX idx_prompts_is_public ON prompts(is_public);
```

**Conversations Table:**
```sql
CREATE TABLE conversations (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  title VARCHAR(255),
  messages JSONB NOT NULL DEFAULT '[]',
  metadata JSONB,
  message_count INTEGER DEFAULT 0,
  last_message_at TIMESTAMP,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_conversations_user_id ON conversations(user_id);
CREATE INDEX idx_conversations_last_message_at ON conversations(last_message_at DESC);
```

**Subscriptions Table:**
```sql
CREATE TABLE subscriptions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  stripe_subscription_id VARCHAR(255) UNIQUE,
  stripe_customer_id VARCHAR(255),
  tier VARCHAR(20) NOT NULL,
  status VARCHAR(20) NOT NULL, -- active, canceled, past_due
  current_period_start TIMESTAMP,
  current_period_end TIMESTAMP,
  cancel_at_period_end BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_subscriptions_user_id ON subscriptions(user_id);
CREATE INDEX idx_subscriptions_stripe_id ON subscriptions(stripe_subscription_id);
```

### Database Migrations

**Using Alembic:**
```bash
# Initialize Alembic
alembic init alembic

# Create migration
alembic revision --autogenerate -m "Initial schema"

# Run migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

**Migration Script Example:**
```python
# alembic/versions/001_initial_schema.py
def upgrade():
    op.create_table(
        'users',
        sa.Column('id', postgresql.UUID(), nullable=False),
        sa.Column('email', sa.String(255), nullable=False),
        # ... rest of schema
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_users_email', 'users', ['email'])

def downgrade():
    op.drop_index('idx_users_email')
    op.drop_table('users')
```

---

## 🚀 Caching Strategy

### Redis Cache Layers

**Layer 1: User Session Cache**
```python
# TTL: 24 hours
# Key format: session:{user_id}
{
  "user_id": "uuid",
  "tier": "pro",
  "daily_requests": 245,
  "rate_limit_remaining": 755
}
```

**Layer 2: Response Cache**
```python
# TTL: 1 hour
# Key format: response:{hash(messages)}
{
  "model": "claude-3-haiku",
  "response": "...",
  "tokens": 450,
  "cost": 0.00135
}
```

**Layer 3: Rate Limit Buckets**
```python
# TTL: 60 seconds
# Key format: ratelimit:{user_id}:{minute}
# Value: request count (integer)
```

**Layer 4: Agent Results Cache**
```python
# TTL: 7 days
# Key format: agent:{agent_name}:{hash(input)}
{
  "result": {...},
  "execution_time_ms": 15000,
  "cost": 0.002
}
```

### Cache Invalidation

**Strategies:**
1. **TTL-based:** Automatic expiry (default)
2. **Event-based:** Invalidate on data change
3. **LRU eviction:** When memory limit reached

**Implementation:**
```python
from redis import Redis
import hashlib
import json

class CacheService:
    def __init__(self, redis_url: str):
        self.redis = Redis.from_url(redis_url)

    def get_cached_response(self, messages: list) -> dict | None:
        cache_key = self._hash_messages(messages)
        cached = self.redis.get(f"response:{cache_key}")
        return json.loads(cached) if cached else None

    def cache_response(self, messages: list, response: dict, ttl: int = 3600):
        cache_key = self._hash_messages(messages)
        self.redis.setex(
            f"response:{cache_key}",
            ttl,
            json.dumps(response)
        )

    def _hash_messages(self, messages: list) -> str:
        content = json.dumps(messages, sort_keys=True)
        return hashlib.sha256(content.encode()).hexdigest()
```

---

## 🔒 Security & Compliance

### Authentication & Authorization

**API Key Generation:**
```python
import secrets
import hashlib

def generate_api_key(user_id: str) -> tuple[str, str]:
    # Generate random key
    random_bytes = secrets.token_bytes(32)
    key = f"hx_user_{random_bytes.hex()}"

    # Hash for storage
    key_hash = hashlib.sha256(key.encode()).hexdigest()

    # Prefix for display
    key_prefix = key[:12] + "..."

    return key, key_hash, key_prefix

# Store only hash in database
# Return plain key to user ONCE
```

**JWT Tokens:**
```python
from jose import jwt
from datetime import datetime, timedelta

def create_access_token(user_id: str, tier: str) -> str:
    payload = {
        "sub": user_id,
        "tier": tier,
        "exp": datetime.utcnow() + timedelta(hours=24)
    }
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm="HS256")

def verify_token(token: str) -> dict:
    return jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
```

### Data Encryption

**At Rest:**
- PostgreSQL: Encrypted volumes (Railway default)
- API keys: AES-256 encrypted before storage
- PII data: Column-level encryption

**In Transit:**
- TLS 1.3 for all connections
- Certificate pinning for mobile apps
- VPC peering for internal services

**Implementation:**
```python
from cryptography.fernet import Fernet

class EncryptionService:
    def __init__(self, key: str):
        self.cipher = Fernet(key.encode())

    def encrypt(self, data: str) -> str:
        return self.cipher.encrypt(data.encode()).decode()

    def decrypt(self, encrypted: str) -> str:
        return self.cipher.decrypt(encrypted.encode()).decode()
```

### Compliance

**GDPR (EU Users):**
- [ ] Data export endpoint (`GET /v1/users/me/export`)
- [ ] Data deletion endpoint (`DELETE /v1/users/me`)
- [ ] Cookie consent banner
- [ ] Privacy policy + ToS
- [ ] Data processing agreement (DPA)

**SOC 2 Type II (Enterprise):**
- [ ] Security audit (annual)
- [ ] Penetration testing (quarterly)
- [ ] Access logs retention (2 years)
- [ ] Incident response plan
- [ ] Business continuity plan

**PCI DSS (Credit Cards):**
- ✅ Use Stripe (PCI-compliant processor)
- ✅ Never store card numbers
- ✅ Tokenize payment methods

---

## 📊 Monitoring & Observability

### Metrics Collection

**Application Metrics (Prometheus):**
```python
from prometheus_client import Counter, Histogram, Gauge

# Request metrics
request_count = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

request_latency = Histogram(
    'http_request_duration_seconds',
    'HTTP request latency',
    ['endpoint']
)

# Business metrics
api_calls_by_model = Counter(
    'api_calls_total',
    'Total API calls',
    ['model', 'provider', 'tier']
)

active_users = Gauge(
    'active_users_total',
    'Number of active users',
    ['tier']
)
```

**Error Tracking (Sentry):**
```python
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration

sentry_sdk.init(
    dsn=SENTRY_DSN,
    environment="production",
    integrations=[FastApiIntegration()],
    traces_sample_rate=0.1,  # 10% of transactions
    profiles_sample_rate=0.1
)
```

### Logging

**Structured Logging:**
```python
import structlog

logger = structlog.get_logger()

logger.info(
    "llm_request",
    user_id=user_id,
    model="claude-3-haiku",
    tokens=450,
    cost_usd=0.00135,
    latency_ms=1234
)
```

**Log Aggregation (Railway Logs + External):**
- Railway built-in logs (7-day retention)
- Ship to Datadog/Logtail for long-term storage
- Set up alerts for errors, high latency, etc.

### Dashboards

**System Health Dashboard:**
- Request rate (req/min)
- Error rate (%)
- P95 latency (ms)
- CPU/Memory usage (%)
- Database connections
- Redis memory usage

**Business Dashboard:**
- Active users (daily/monthly)
- API calls by tier
- Revenue (MRR, ARR)
- Churn rate
- Conversion rate (free → pro)

---

## 🚀 Scaling Strategy

### Horizontal Scaling

**API Gateway:**
```yaml
# Railway auto-scaling
replicas: 2-10
cpu_threshold: 70%
memory_threshold: 80%
```

**Database Read Replicas:**
```sql
-- Use read replicas for analytics queries
-- Write to primary, read from replicas
```

**Caching:**
```
Redis Cluster (3 nodes)
  ├── Master (writes)
  ├── Replica 1 (reads)
  └── Replica 2 (reads)
```

### Vertical Scaling

**Database:**
- Start: 1GB RAM, 1 CPU
- 1k users: 4GB RAM, 2 CPU
- 10k users: 16GB RAM, 4 CPU
- 100k users: 64GB RAM, 8 CPU

**Redis:**
- Start: 1GB RAM
- 10k users: 4GB RAM
- 100k users: 16GB RAM

### Performance Optimization

**Database Query Optimization:**
```sql
-- Add compound indexes for common queries
CREATE INDEX idx_usage_user_date ON usage(user_id, created_at DESC);

-- Analyze slow queries
SELECT * FROM pg_stat_statements
ORDER BY total_time DESC
LIMIT 10;
```

**Connection Pooling:**
```python
from sqlalchemy.pool import QueuePool

engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=20,
    max_overflow=40,
    pool_timeout=30,
    pool_recycle=1800
)
```

---

## 🔄 Disaster Recovery

### Backup Strategy

**PostgreSQL:**
- Automated daily backups (Railway)
- Point-in-time recovery (PITR)
- Retention: 30 days
- Test restore monthly

**Redis:**
- RDB snapshots (every 6 hours)
- AOF persistence (every second)
- Backup to S3 daily

**Application Data:**
- Database exports (weekly)
- Configuration backups (on change)
- Encryption key backups (offline storage)

### Incident Response

**Runbook for Common Issues:**

**Issue 1: Database Connection Pool Exhausted**
```bash
# Check active connections
SELECT count(*) FROM pg_stat_activity;

# Kill idle connections
SELECT pg_terminate_backend(pid)
FROM pg_stat_activity
WHERE state = 'idle'
AND state_change < NOW() - INTERVAL '5 minutes';

# Increase pool size (emergency)
railway variables set MAX_DB_CONNECTIONS=50
```

**Issue 2: Redis Out of Memory**
```bash
# Check memory usage
redis-cli INFO memory

# Clear cache (emergency)
redis-cli FLUSHDB

# Increase memory limit
railway up --service redis --memory 4GB
```

**Issue 3: LLM Provider Outage**
```python
# Automatic failover implemented in router service
# Check provider status
curl https://api.helixcollective.io/v1/providers/status
```

---

## 💰 Cost Optimization

### Infrastructure Costs (Projected)

**Railway Hosting:**
- API Gateway: $20/month (2GB RAM, 1 CPU)
- Worker Service: $20/month
- PostgreSQL: $10/month (1GB)
- Redis: $10/month (1GB)
- **Total:** ~$60/month (startup)

**Scaling Costs:**
- 1k users: ~$150/month
- 10k users: ~$500/month
- 100k users: ~$2,000/month

**External Services:**
- Stripe: 2.9% + $0.30 per transaction
- Sentry: $26/month (Team plan)
- Pinecone: $70/month (Starter plan)
- SendGrid: $15/month (100k emails)

**LLM API Costs:**
- Variable: ~35% of user revenue
- Example: $1,000 user spend → $350 LLM cost

### Cost Monitoring

**Set up billing alerts:**
```bash
# Railway usage alert
railway alerts create --threshold $100 --period monthly

# AWS budget alert (if using S3, etc.)
aws budgets create-budget --budget-name helix-monthly --budget-limit 200
```

---

## 🔧 CI/CD Pipeline

### GitHub Actions Workflow

```yaml
# .github/workflows/deploy.yml
name: Deploy to Railway

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: pytest tests/
      - run: mypy backend/

  deploy:
    needs: test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: railway/deploy@v1
        with:
          railway_token: ${{ secrets.RAILWAY_TOKEN }}
          service: api-gateway
```

### Pre-Deployment Checklist

**Before Each Deploy:**
- [ ] All tests passing
- [ ] No critical Sentry errors
- [ ] Database migrations ready
- [ ] Feature flags configured
- [ ] Rollback plan documented

**Post-Deployment:**
- [ ] Smoke tests passed
- [ ] Monitor error rate (< 1%)
- [ ] Check latency (< 500ms p95)
- [ ] Verify new features work
- [ ] Announce in changelog

---

## 📚 Additional Resources

**Documentation:**
- [Railway Docs](https://docs.railway.app)
- [FastAPI Best Practices](https://fastapi.tiangolo.com/deployment/)
- [PostgreSQL Performance](https://wiki.postgresql.org/wiki/Performance_Optimization)
- [Redis Best Practices](https://redis.io/docs/manual/patterns/)

**Tools:**
- [Railway CLI](https://docs.railway.app/develop/cli)
- [Alembic Migrations](https://alembic.sqlalchemy.org/)
- [Prometheus](https://prometheus.io/)
- [Grafana Dashboards](https://grafana.com/)

---

**Infrastructure is ready. Time to build! 🚀**
