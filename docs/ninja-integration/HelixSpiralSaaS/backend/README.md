# HelixSpiral.work Backend API

**Copyright (c) 2025 Andrew John Ward. All Rights Reserved.**

Enterprise-grade FastAPI backend for HelixSpiral - A Zapier alternative with AI-powered automation.

---

## 🚀 Features

- ✅ **User Authentication** - JWT-based auth with refresh tokens
- ✅ **Stripe Integration** - Subscription management (Free, Pro, Enterprise)
- ✅ **Spiral Management** - Create and manage automation workflows
- ✅ **Action System** - HTTP requests, emails, data transforms, AI calls
- ✅ **Execution Engine** - Run spirals with full logging
- ✅ **AI Assistant** - Natural language spiral generation
- ✅ **Email Notifications** - SendGrid integration
- ✅ **PostgreSQL Database** - Production-ready data storage
- ✅ **API Documentation** - Auto-generated OpenAPI docs

---

## 📋 Prerequisites

- Python 3.11+
- PostgreSQL 14+
- Stripe account
- SendGrid account
- Anthropic API key

---

## 🛠️ Local Development Setup

### 1. Clone and Install

```bash
cd helixspiral-saas/backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment

Copy `.env.example` to `.env` and fill in your values:

```bash
cp .env.example .env
```

Required variables:
- `DATABASE_URL` - PostgreSQL connection string
- `SECRET_KEY` - JWT secret (generate with `openssl rand -hex 32`)
- `STRIPE_SECRET_KEY` - Stripe API key
- `STRIPE_WEBHOOK_SECRET` - Stripe webhook secret
- `SENDGRID_API_KEY` - SendGrid API key
- `ANTHROPIC_API_KEY` - Anthropic Claude API key

### 3. Initialize Database

```bash
# Create tables
python -c "from app.database import Base, engine; Base.metadata.create_all(bind=engine)"

# Or use Alembic for migrations
alembic upgrade head
```

### 4. Run Development Server

```bash
uvicorn app.main:app --reload --port 8000
```

API will be available at:
- **API**: http://localhost:8000
- **Docs**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc

---

## 🚢 Railway Deployment

### 1. Create Railway Project

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Initialize project
railway init
```

### 2. Add PostgreSQL Database

In Railway dashboard:
1. Click "New" → "Database" → "PostgreSQL"
2. Railway will auto-generate `DATABASE_URL`

### 3. Configure Environment Variables

Add these in Railway dashboard:

```bash
# JWT
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Stripe
STRIPE_SECRET_KEY=sk_live_your_key
STRIPE_PUBLISHABLE_KEY=pk_live_your_key
STRIPE_WEBHOOK_SECRET=whsec_your_secret
STRIPE_PRICE_ID_PRO=price_pro_id
STRIPE_PRICE_ID_ENTERPRISE=price_enterprise_id

# SendGrid
SENDGRID_API_KEY=SG.your_key
FROM_EMAIL=noreply@helixspiral.work
FROM_NAME=HelixSpiral

# AI
ANTHROPIC_API_KEY=sk-ant-your_key

# App
APP_NAME=HelixSpiral
APP_URL=https://api.helixspiral.work
FRONTEND_URL=https://helixspiral.work
ENVIRONMENT=production

# CORS
CORS_ORIGINS=https://helixspiral.work

# Rate Limiting
RATE_LIMIT_PER_MINUTE=60
```

### 4. Deploy

```bash
railway up
```

Or connect GitHub repo for automatic deployments.

### 5. Set Up Stripe Webhooks

1. Go to Stripe Dashboard → Developers → Webhooks
2. Add endpoint: `https://your-api-url.railway.app/api/subscriptions/webhook`
3. Select events:
   - `checkout.session.completed`
   - `customer.subscription.updated`
   - `customer.subscription.deleted`
   - `invoice.payment_failed`
4. Copy webhook secret to `STRIPE_WEBHOOK_SECRET`

---

## 📚 API Documentation

### Authentication

**Register:**
```bash
POST /api/auth/register
{
  "email": "user@example.com",
  "password": "securepassword",
  "full_name": "John Doe"
}
```

**Login:**
```bash
POST /api/auth/login
{
  "email": "user@example.com",
  "password": "securepassword"
}
```

**Response:**
```json
{
  "access_token": "eyJ...",
  "refresh_token": "eyJ...",
  "token_type": "bearer"
}
```

### Spirals

**Create Spiral:**
```bash
POST /api/spirals
Authorization: Bearer {access_token}
{
  "name": "Daily Weather Email",
  "description": "Send weather forecast every morning",
  "trigger_type": "schedule",
  "trigger_config": {
    "cron": "0 9 * * *"
  }
}
```

**Add Action:**
```bash
POST /api/spirals/{spiral_id}/actions
Authorization: Bearer {access_token}
{
  "order_index": 0,
  "action_type": "http_request",
  "config": {
    "method": "GET",
    "url": "https://api.weather.com/forecast",
    "headers": {}
  }
}
```

**Execute Spiral:**
```bash
POST /api/spirals/{spiral_id}/execute
Authorization: Bearer {access_token}
{
  "input_data": {
    "location": "New York"
  }
}
```

### AI Assistant

**Generate Spiral from Description:**
```bash
POST /api/ai/generate-spiral
Authorization: Bearer {access_token}
{
  "description": "Send me an email every day at 9am with the weather forecast"
}
```

---

## 🧪 Testing

```bash
# Run tests
pytest

# With coverage
pytest --cov=app tests/

# Specific test file
pytest tests/test_auth.py
```

---

## 📊 Database Schema

### Users
- id (UUID)
- email (unique)
- password_hash
- full_name
- created_at, updated_at
- email_verified, is_active

### Subscriptions
- id (UUID)
- user_id (FK)
- stripe_customer_id, stripe_subscription_id
- plan_type (free, pro, enterprise)
- status (active, canceled, past_due)
- current_period_start, current_period_end

### Spirals
- id (UUID)
- user_id (FK)
- name, description
- is_active
- trigger_type, trigger_config
- last_run_at, run_count

### Actions
- id (UUID)
- spiral_id (FK)
- order_index
- action_type, config

### ExecutionLogs
- id (UUID)
- spiral_id (FK)
- status (success, failed, running)
- started_at, completed_at
- error_message
- input_data, output_data

---

## 🔒 Security

- ✅ JWT authentication with refresh tokens
- ✅ Password hashing with bcrypt
- ✅ CORS configuration
- ✅ Rate limiting
- ✅ SQL injection prevention (SQLAlchemy)
- ✅ XSS protection
- ✅ Stripe webhook signature verification

---

## 📈 Monitoring

### Health Check
```bash
GET /api/health
```

### Logs
```bash
# Railway logs
railway logs

# Or in Railway dashboard
```

---

## 🐛 Troubleshooting

### Database Connection Issues
```bash
# Test connection
python -c "from app.database import engine; engine.connect()"
```

### Stripe Webhook Issues
```bash
# Test webhook locally with Stripe CLI
stripe listen --forward-to localhost:8000/api/subscriptions/webhook
```

### Email Not Sending
- Verify SendGrid API key
- Check sender email is verified in SendGrid
- Review SendGrid activity logs

---

## 📝 License

Copyright (c) 2025 Andrew John Ward. All Rights Reserved.
PROPRIETARY AND CONFIDENTIAL - See LICENSE file for terms.

---

## 🤝 Support

For issues or questions:
- Email: andrew@deathcharge.dev
- Documentation: https://helixspiral.work/docs

---

**Built with ❤️ by Andrew John Ward**