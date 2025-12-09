# Railway Deployment Guide v17.1 - Helix-Unified Backend

**Version:** v17.1 (Updated for SaaS Platform)  
**Last Updated:** December 8, 2025  
**Author:** Weaver #2 (Manus Collective)  
**Previous Version:** See `RAILWAY_DEPLOYMENT_GUIDE.md` for microservices architecture

---

## What's New in v17.1

This guide covers deploying the **monolithic v17.1 backend** with:

- ✅ Admin System with bypass authentication
- ✅ SaaS Marketplace ($1.57M ARR potential)
- ✅ Multimedia Suite (image generation, voice transcription, LLM)
- ✅ 8 new SaaS services (Analytics, Email, Chat, Video, Booking, Monitoring, CDP, Forms)
- ✅ 60+ API endpoints
- ✅ Production-grade security (bcrypt, rate limiting, CORS)

**For microservices deployment**, see `RAILWAY_DEPLOYMENT_GUIDE.md`.

---

## Quick Start (5 Minutes)

### Prerequisites
- Railway account
- GitHub access to helix-unified
- Admin email
- PostgreSQL database (Railway provides)

### Deployment Steps

1. **Create Railway Project**
   ```bash
   # Via Railway Dashboard
   New Project → Deploy from GitHub → helix-unified
   ```

2. **Add PostgreSQL**
   ```bash
   + New → Database → PostgreSQL
   ```

3. **Set Critical Variables**
   ```bash
   DATABASE_URL=${{Postgres.DATABASE_URL}}
   JWT_SECRET=<64-char-random-string>
   ADMIN_EMAILS=ward.andrew32@gmail.com,andrew@helix-collective.ai
   ```

4. **Deploy**
   ```bash
   Railway auto-deploys on variable save
   ```

5. **Verify**
   ```bash
   curl https://your-app.up.railway.app/health
   ```

---

## Part 1: Environment Variables

### Critical (Required)

```bash
# Database
DATABASE_URL=${{Postgres.DATABASE_URL}}

# Security
JWT_SECRET=<generate-with: openssl rand -hex 32>
ADMIN_EMAILS=ward.andrew32@gmail.com,andrew@helix-collective.ai

# Discord Bot
DISCORD_BOT_TOKEN=<from-discord-dev-portal>
DISCORD_GUILD_ID=<your-server-id>

# OpenAI (for LLM features)
OPENAI_API_KEY=<from-platform.openai.com>
OPENAI_API_URL=https://api.openai.com/v1
```

### SaaS Features (Optional)

```bash
# Stripe Payments
STRIPE_SECRET_KEY=<from-dashboard.stripe.com>
STRIPE_WEBHOOK_SECRET=<from-stripe-webhooks>
STRIPE_PRICE_IDS={"starter":"price_xxx","pro":"price_xxx","enterprise":"price_xxx"}

# Notion Integration
NOTION_API_KEY=<from-notion-integrations>
NOTION_DATABASE_IDS={"deployment_log":"<id>","agent_registry":"<id>"}

# Email Service (for SaaS email marketing)
SENDGRID_API_KEY=<from-sendgrid>
MAILGUN_API_KEY=<from-mailgun>

# Video Hosting (for SaaS video service)
CLOUDFLARE_STREAM_API_KEY=<from-cloudflare>
CLOUDFLARE_ACCOUNT_ID=<your-account-id>
```

### Performance & Monitoring

```bash
# Application
ENVIRONMENT=production
LOG_LEVEL=INFO
CORS_ORIGINS=https://samsarahelix.manus.space,https://helixdashboard.manus.space

# Rate Limiting
RATE_LIMIT_ENABLED=true
RATE_LIMIT_PER_MINUTE=60

# Monitoring
SENTRY_DSN=<optional-for-error-tracking>
```

---

## Part 2: Build Configuration

### Auto-Detected Settings

Railway should detect:
```bash
Build Command: pip install -r requirements.txt
Start Command: python -m uvicorn backend.main:app --host 0.0.0.0 --port $PORT
Root Directory: /
```

### Manual Override (if needed)

In **Settings → Deploy**:
```bash
Build Command: pip install -r requirements.txt && python -m backend.database init
Start Command: uvicorn backend.main:app --host 0.0.0.0 --port $PORT --workers 2
```

---

## Part 3: Database Setup

### Option A: Railway PostgreSQL (Recommended)

1. Add PostgreSQL plugin
2. Use `${{Postgres.DATABASE_URL}}`
3. Migrations run automatically on first start

### Option B: External Database

```bash
DATABASE_URL=postgresql://user:pass@host:5432/dbname
```

### Run Migrations Manually

```bash
# Via Railway CLI
railway run python -c "from backend.database import init_db; init_db()"

# Or add to build command
pip install -r requirements.txt && python -m backend.database init
```

---

## Part 4: Verify Deployment

### Health Check

```bash
curl https://your-app.up.railway.app/health
```

Expected response:
```json
{
  "status": "healthy",
  "version": "17.1",
  "database": "connected",
  "admin_system": "active",
  "saas_marketplace": "enabled",
  "timestamp": "2025-12-08T12:00:00Z"
}
```

### Test Admin Login

```bash
curl -X POST https://your-app.up.railway.app/api/admin/login \
  -H "Content-Type: application/json" \
  -d '{"email":"ward.andrew32@gmail.com","password":"your-password"}'
```

### Test SaaS Endpoints

```bash
# Generate API key
curl -X POST https://your-app.up.railway.app/api/keys/generate \
  -H "Authorization: Bearer <jwt-token>" \
  -H "Content-Type: application/json" \
  -d '{"name":"Test Key","scopes":["read","write"]}'

# Check multimedia suite
curl https://your-app.up.railway.app/api/multimedia/status \
  -H "Authorization: Bearer <jwt-token>"
```

---

## Part 5: Connect Frontend

### Update Samsara Showcase

In your Manus Space environment:
```bash
VITE_HELIX_API_URL=https://your-app.up.railway.app
```

### Update Other Portals

Update all 12 Manus Spaces with new backend URL:
```bash
# helixdashboard.manus.space
# samsarahelix.manus.space
# helixcollective.manus.space
# etc.
```

### Test Connection

1. Open samsara-showcase
2. Check Collective Agent Dashboard
3. Verify MCP Integration Panel loads
4. Check browser console for errors

---

## Part 6: Configure Stripe (Optional)

### Create Products

1. Go to [Stripe Dashboard](https://dashboard.stripe.com/products)
2. Create 3 products:
   - **Starter** - $29/month
   - **Pro** - $99/month
   - **Enterprise** - $299/month

### Get Price IDs

```bash
STRIPE_PRICE_IDS={
  "starter":"price_1ABC123...",
  "pro":"price_1DEF456...",
  "enterprise":"price_1GHI789..."
}
```

### Configure Webhook

1. Go to [Webhooks](https://dashboard.stripe.com/webhooks)
2. Add endpoint: `https://your-app.up.railway.app/api/stripe/webhook`
3. Select events:
   - `payment_intent.succeeded`
   - `customer.subscription.updated`
   - `invoice.payment_failed`
4. Copy webhook secret to `STRIPE_WEBHOOK_SECRET`

---

## Part 7: Monitoring

### Railway Dashboard

Monitor in **Metrics** tab:
- CPU usage
- Memory usage
- Request count
- Response times

### Application Logs

```bash
# Via Railway CLI
railway logs --tail 100

# Via Dashboard
Deployments → Active Deployment → Logs
```

### Health Monitoring

Set up external monitoring (optional):
```bash
# Zapier workflow (every 5 minutes)
GET https://your-app.up.railway.app/health

# Or use UptimeRobot, Pingdom, etc.
```

---

## Part 8: Scaling

### Vertical Scaling

In **Settings → Resources**:
```bash
Memory: 512MB → 2GB (recommended)
CPU: Shared → Dedicated (for high traffic)
```

### Horizontal Scaling

Enable auto-scaling:
```bash
Min Replicas: 2
Max Replicas: 5
```

Railway distributes load automatically.

---

## Part 9: Security Checklist

- [ ] `JWT_SECRET` is 64+ characters
- [ ] `ADMIN_EMAILS` restricted to authorized users
- [ ] `CORS_ORIGINS` whitelists specific domains only
- [ ] Rate limiting enabled (60 req/min)
- [ ] HTTPS enforced (Railway SSL)
- [ ] Environment variables not in Git
- [ ] Stripe webhook secret configured
- [ ] Database credentials auto-managed
- [ ] API keys bcrypt hashed
- [ ] Input validation on all endpoints

---

## Part 10: Troubleshooting

### Database Connection Failed

**Symptom:** `"database": "disconnected"`

**Fix:**
```bash
# Verify DATABASE_URL
railway variables

# Check PostgreSQL service
railway status

# Run migrations
railway run python -m backend.database init
```

### CORS Errors

**Symptom:** Frontend can't connect

**Fix:**
```bash
# Add frontend domain to CORS_ORIGINS
CORS_ORIGINS=https://samsarahelix.manus.space,https://helixdashboard.manus.space

# Redeploy
railway up
```

### Admin Login Fails

**Symptom:** 401 Unauthorized

**Fix:**
```bash
# Verify email in ADMIN_EMAILS
railway variables | grep ADMIN_EMAILS

# Check JWT_SECRET is set
railway variables | grep JWT_SECRET

# Create admin user manually
railway run python -c "from backend.admin import create_admin; create_admin('ward.andrew32@gmail.com')"
```

### High Memory Usage

**Symptom:** Service crashes, OOM errors

**Fix:**
```bash
# Increase memory in Settings → Resources
Memory: 512MB → 1GB → 2GB

# Reduce workers in start command
uvicorn backend.main:app --workers 1
```

---

## Part 11: Rollback

### Via Dashboard

1. Go to **Deployments**
2. Find last successful deployment
3. Click **"Redeploy"**

### Via CLI

```bash
railway rollback
```

### Via Git

```bash
git revert HEAD
git push origin main
```

---

## Success Criteria

✅ Deployment successful when:

- Health endpoint returns `"status": "healthy"`
- Admin login works
- Frontend connects successfully
- Database migrations completed
- No errors in logs
- CORS allows requests
- SSL certificate active
- API endpoints respond correctly

---

## Next Steps

1. **Test all endpoints** - Use Postman collection
2. **Configure Stripe** - Set up products and webhooks
3. **Enable monitoring** - Add Sentry, Zapier workflows
4. **Load testing** - Use Artillery or k6
5. **User onboarding** - Create first users, generate API keys
6. **Documentation** - Update API docs with production URLs

---

## Additional Resources

**Helix-Unified Docs:**
- `WHATS_NEW_v17.1.md` - Feature overview
- `ADMIN_SETUP.md` - Admin system setup
- `RAILWAY_SERVICES_SETUP.md` - Microservices architecture
- `AUDIT_SUMMARY.md` - Security status

**Railway Docs:**
- [Railway Documentation](https://docs.railway.app/)
- [Environment Variables](https://docs.railway.app/develop/variables)
- [Custom Domains](https://docs.railway.app/deploy/exposing-your-app)

**Support:**
- GitHub: [helix-unified/issues](https://github.com/Deathcharge/helix-unified/issues)
- Discord: Samsara Helix Collective
- Email: andrew@helix-collective.ai

---

## Deployment Checklist

### Pre-Deployment
- [ ] Railway account created
- [ ] GitHub repository access
- [ ] Environment variables collected
- [ ] Admin email configured

### Deployment
- [ ] Railway project created
- [ ] PostgreSQL provisioned
- [ ] Environment variables set
- [ ] Initial deployment successful

### Post-Deployment
- [ ] Health endpoint verified
- [ ] Admin login tested
- [ ] Frontend connected
- [ ] Stripe configured (if using)
- [ ] Monitoring enabled

### Launch
- [ ] Security checklist completed
- [ ] Performance tested
- [ ] Documentation updated
- [ ] Team notified

---

**Your Helix-Unified v17.1 backend is now live! 🚀**

**Tat Tvam Asi** 🌀

---

**Document Version:** 1.0  
**Last Updated:** December 8, 2025  
**Maintained By:** Weaver #2 (Manus Collective)
