# 🔑 Admin Setup Guide - Helix Collective v17.1

## How to Use Your Own Platform Without Paying Yourself

### Quick Setup (3 Steps)

1. **Add your email to environment variables:**
   ```bash
   ADMIN_EMAILS="your@email.com"
   ```

2. **Optional: Set a master admin key for emergency access:**
   ```bash
   MASTER_ADMIN_KEY="your-super-secret-admin-key-here"
   ```

3. **Restart your backend:**
   ```bash
   # Railway will auto-restart when you update env vars
   # For local: Ctrl+C and restart
   ```

That's it! You now have unlimited access to all platform features without paying. 🎉

---

## Environment Variables Reference

### Admin System

```bash
# Admin emails (comma-separated, no spaces around commas)
ADMIN_EMAILS="admin@helixspiral.work,owner@example.com,dev@company.com"

# Admin user IDs (if you want to use user IDs instead of/in addition to emails)
ADMIN_USER_IDS="user_abc123,user_def456"

# Master admin key for emergency access (use a strong random string)
MASTER_ADMIN_KEY="generate-with: openssl rand -base64 32"
```

### How Admin Bypass Works

When you're logged in with an admin email:
- ✅ **Subscription tier**: Automatically upgraded to **Enterprise**
- ✅ **Payment**: Bypass all Stripe payment requirements
- ✅ **Rate limits**: Unlimited API calls
- ✅ **Features**: Access to all paid features
- ✅ **Admin dashboard**: Access to `/admin` routes
- ✅ **Usage tracking**: Your usage won't pollute analytics (optional)

### Using the Master Admin Key

For emergency access or scripts:

```bash
curl https://api.helixspiral.work/admin/stats \
  -H "X-Admin-Key: your-master-admin-key-here"
```

---

## New Services Configuration

### Multimedia Suite

No additional env vars required! But you can configure:

```bash
# Storage provider (default: local filesystem)
MULTIMEDIA_STORAGE="s3"  # or "gcs", "azure", "local"

# AWS S3 (if using S3 storage)
AWS_ACCESS_KEY_ID="your-aws-key"
AWS_SECRET_ACCESS_KEY="your-aws-secret"
AWS_S3_BUCKET="helix-multimedia"
AWS_REGION="us-east-1"

# Storage quotas by tier (in GB)
STORAGE_QUOTA_PERSONAL=10
STORAGE_QUOTA_BUSINESS=100
STORAGE_QUOTA_ENTERPRISE=1000
```

### Email Marketing (Helix Mail)

```bash
# Email provider (SendGrid recommended)
EMAIL_PROVIDER="sendgrid"  # or "mailgun", "ses", "smtp"

# SendGrid
SENDGRID_API_KEY="SG.your-sendgrid-key-here"

# Mailgun
MAILGUN_API_KEY="your-mailgun-key"
MAILGUN_DOMAIN="mg.yourdomain.com"

# AWS SES
AWS_SES_REGION="us-east-1"
AWS_SES_FROM_EMAIL="noreply@yourdomain.com"

# SMTP (for any provider)
SMTP_HOST="smtp.gmail.com"
SMTP_PORT=587
SMTP_USER="your@email.com"
SMTP_PASS="your-app-password"
```

### Video Hosting (Helix Stream)

```bash
# Video storage
VIDEO_STORAGE="s3"  # or "gcs", "azure", "local"

# CDN for video delivery
VIDEO_CDN_URL="https://cdn.yourdomain.com"

# Transcoding service
TRANSCODING_SERVICE="aws-mediaconvert"  # or "gcs-transcoder", "local-ffmpeg"

# AWS MediaConvert
AWS_MEDIACONVERT_ROLE="arn:aws:iam::123:role/MediaConvertRole"
AWS_MEDIACONVERT_QUEUE="arn:aws:mediaconvert:us-east-1:123:queues/Default"
```

### Customer Support Chat (Helix Chat)

```bash
# WebSocket server URL (for real-time chat)
WEBSOCKET_URL="wss://api.helixspiral.work/ws"

# Chat notification webhooks
CHAT_NOTIFICATION_WEBHOOK="https://hooks.slack.com/services/..."

# AI chatbot (optional)
CHAT_AI_ENABLED=true
CHAT_AI_MODEL="claude-3-5-sonnet-20241022"
```

### Uptime Monitoring (Helix Monitor)

```bash
# Monitoring check interval (seconds)
MONITOR_DEFAULT_INTERVAL=60

# Alert channels
MONITOR_ALERT_EMAIL=true
MONITOR_ALERT_SLACK=true
MONITOR_ALERT_DISCORD=true

# Slack webhook for alerts
SLACK_WEBHOOK_URL="https://hooks.slack.com/services/..."

# Discord webhook for alerts
DISCORD_ALERT_WEBHOOK="https://discord.com/api/webhooks/..."

# PagerDuty (optional)
PAGERDUTY_API_KEY="your-pagerduty-key"
PAGERDUTY_SERVICE_ID="your-service-id"
```

### Analytics Platform (Helix Analytics)

```bash
# Data warehouse
ANALYTICS_DATABASE_URL="postgresql://user:pass@host:5432/analytics"

# ClickHouse for time-series analytics (optional)
CLICKHOUSE_HOST="localhost"
CLICKHOUSE_PORT=9000
CLICKHOUSE_USER="default"
CLICKHOUSE_PASSWORD=""

# Refresh intervals
ANALYTICS_CACHE_TTL=300  # seconds
```

### Customer Data Platform (Helix CDP)

```bash
# Event storage
CDP_EVENTS_DATABASE="postgresql://..."

# Redis for real-time data
CDP_REDIS_URL="redis://localhost:6379"

# Segment integration (optional)
SEGMENT_WRITE_KEY="your-segment-key"

# Data retention (days)
CDP_EVENT_RETENTION_DAYS=365
```

---

## Admin Dashboard Access

Once you've set your admin email:

1. **Sign up/login** with your admin email at: `https://yourdomain.com/auth/login`
2. **Access admin dashboard**: `https://yourdomain.com/admin`
3. **View platform stats**: `https://yourdomain.com/admin/stats`
4. **Manage users**: `https://yourdomain.com/admin/users`
5. **Revenue reports**: `https://yourdomain.com/admin/revenue`

### Admin Dashboard Features

- 📊 **Platform Statistics**
  - Total users, active users, revenue
  - MRR, ARR, subscription breakdown
  - API usage, storage metrics

- 👥 **User Management**
  - View all users and their tiers
  - Manually upgrade/downgrade users
  - Delete accounts
  - Reset passwords

- 💰 **Revenue Tracking**
  - Daily, weekly, monthly, yearly reports
  - Revenue by tier and product
  - Churn analysis
  - Top customers

- 🔍 **System Health**
  - Uptime percentage
  - API response times
  - Error rates
  - Database and Redis connections

- 📝 **Admin Action Logs**
  - Audit trail of all admin actions
  - Who did what and when
  - IP addresses and timestamps

---

## API Documentation Portal

Access the beautiful API docs at: `https://yourdomain.com/docs/api`

Features:
- 📖 Complete API reference for all endpoints
- 💻 Code examples in cURL, Python, JavaScript
- 🧪 Interactive API testing (try endpoints live)
- 🔐 Authentication guides
- ⏱️ Rate limits by tier
- 🎨 Beautiful, developer-friendly UI

---

## Security Best Practices

### 1. **Use Strong Admin Key**
```bash
# Generate a secure key
openssl rand -base64 32

# Or use Python
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 2. **Restrict Admin Emails**
Only add emails you control. Anyone with an admin email gets full access.

### 3. **Use HTTPS**
Always use HTTPS in production. HTTP is insecure.

### 4. **Rotate Keys**
Change your `MASTER_ADMIN_KEY` periodically (every 90 days).

### 5. **Monitor Admin Actions**
Check `/admin/logs` regularly to audit admin activity.

### 6. **Separate Admin Accounts**
Don't use your personal email for admin access. Create a dedicated admin email.

---

## Railway Deployment

### Add Environment Variables

1. Go to your Railway project
2. Click on your service
3. Go to **Variables** tab
4. Add the environment variables:

```
ADMIN_EMAILS=your@email.com
MASTER_ADMIN_KEY=your-secure-key-here
```

5. Click **Deploy** (or wait for auto-deploy)

### Verify Deployment

Check logs for:
```
✅ Admin Bypass Middleware enabled (v17.1)
   → Admin users bypass payment and tier restrictions
   → Configure ADMIN_EMAILS in environment variables
```

---

## Local Development

### .env File

Create/update `.env` file in the `backend/` directory:

```bash
# Admin access
ADMIN_EMAILS="dev@localhost.com"
MASTER_ADMIN_KEY="local-dev-key-not-for-production"

# Database
DATABASE_URL="postgresql://localhost:5432/helix"
REDIS_URL="redis://localhost:6379"

# Authentication
JWT_SECRET="change-this-in-production"

# Services (optional for local dev)
GOOGLE_CLIENT_ID="your-google-oauth-client-id"
GOOGLE_CLIENT_SECRET="your-google-oauth-secret"

# Stripe
STRIPE_SECRET_KEY="sk_test_..."
STRIPE_PUBLISHABLE_KEY="pk_test_..."
STRIPE_WEBHOOK_SECRET="whsec_..."

# Email (use Mailhog for local testing)
EMAIL_PROVIDER="smtp"
SMTP_HOST="localhost"
SMTP_PORT=1025
```

### Start Services

```bash
# Terminal 1: Start PostgreSQL
docker run -p 5432:5432 -e POSTGRES_PASSWORD=password postgres

# Terminal 2: Start Redis
docker run -p 6379:6379 redis

# Terminal 3: Start backend
cd backend
python -m uvicorn main:app --reload --port 8000
```

---

## Testing Admin Access

### 1. Create Admin Account

```bash
curl -X POST http://localhost:8000/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "your@email.com",
    "password": "SecurePass123!",
    "name": "Admin User"
  }'
```

### 2. Login

```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "your@email.com",
    "password": "SecurePass123!"
  }'
```

Save the `access_token` from the response.

### 3. Check Admin Status

```bash
curl -X GET http://localhost:8000/auth/me \
  -H "Authorization: Bearer YOUR_TOKEN"
```

You should see:
```json
{
  "id": "user_abc123",
  "email": "your@email.com",
  "subscription_tier": "enterprise",  // ← Automatically upgraded!
  "is_admin": true                     // ← Admin flag
}
```

### 4. Access Admin Dashboard

```bash
curl -X GET http://localhost:8000/admin/stats \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## Revenue Potential

### New Services Added (v17.1)

| Service | Price Range | Target Users | Monthly Revenue |
|---------|-------------|--------------|-----------------|
| **Multimedia Suite** | $12-99/mo | 1,000 | $30,000 |
| **Analytics Platform** | $49-299/mo | 200 | $15,000 |
| **Email Marketing** | $29-199/mo | 500 | $20,000 |
| **Customer Chat** | $19-99/mo | 300 | $10,000 |
| **Video Hosting** | $39-499/mo | 100 | $8,000 |
| **Appointment Booking** | $15-79/mo | 400 | $8,000 |
| **Uptime Monitoring** | $29-299/mo | 200 | $10,000 |
| **Customer Data Platform** | $99-999/mo | 50 | $12,000 |

**Total Potential MRR**: $113,000
**Total Potential ARR**: $1,356,000 💰

---

## Support

### Issues?

1. Check logs: `tail -f Shadow/manus_archive/helix-collective.log`
2. Verify env vars: `echo $ADMIN_EMAILS`
3. Restart service: Railway auto-restarts on env changes
4. Test locally first

### Questions?

- **Email**: support@helixspiral.work (once you set up Helix Mail!)
- **Discord**: Your Discord bot integration
- **Docs**: https://yourdomain.com/docs/api

---

## Next Steps

1. ✅ Set `ADMIN_EMAILS` in environment
2. ✅ Generate strong `MASTER_ADMIN_KEY`
3. ✅ Deploy to Railway
4. ✅ Test admin access
5. 📧 Set up Stripe for customer payments
6. 🎨 Customize branding
7. 📢 Start marketing your services!

---

**Built with ❤️ by Claude for Helix Collective**

Last updated: 2025-12-07
