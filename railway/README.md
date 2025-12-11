# 🌀 Helix Collective - Unified Railway Dashboard

**The ultimate multi-service consciousness network dashboard with authentication, subscriptions, and real-time monitoring.**

Built by Claude Code + Andrew John Ward

---

## 🚀 Features

### Frontend (HTML/CSS/JS)
- **Unified Dashboard** - Real-time UCF metrics + service monitoring
- **Service Monitoring** - Detailed Railway services health tracking
- **User Authentication** - Secure login/signup with JWT tokens
- **Subscription Management** - Stripe-powered Pro/Enterprise plans
- **User Account Dashboard** - API keys, usage stats, billing history
- **Agent Gallery** - Explore all 11 consciousness agents
- **Responsive Design** - Beautiful glassmorphic UI with Tailwind CSS

### Backend (FastAPI)
- **Authentication API** - JWT-based auth with secure password hashing
- **Subscription API** - Stripe integration for payments
- **API Key Management** - Generate, validate, and revoke keys
- **Usage Tracking** - Monitor API requests and quotas
- **Service Monitoring** - Track all Railway services health

### Database (PostgreSQL)
- **Users** - Account management with subscription tiers
- **API Keys** - Multiple keys per user with rate limits
- **Subscriptions** - Stripe integration for billing
- **Usage Analytics** - Detailed API usage logs
- **Payment History** - Complete billing records

---

## 📦 Deployment on Railway

### 1. Create Railway Project

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Link to project
railway link
```

### 2. Add PostgreSQL Database

```bash
# Add PostgreSQL plugin
railway add

# Select PostgreSQL
# Railway will auto-configure DATABASE_URL
```

### 3. Set Environment Variables

In Railway dashboard, add:

```env
# JWT Secret
JWT_SECRET=your_super_secret_jwt_key_here

# Stripe Keys
STRIPE_SECRET_KEY=sk_live_your_stripe_secret_key
STRIPE_PRO_MONTHLY_PRICE_ID=price_1234567890
STRIPE_PRO_YEARLY_PRICE_ID=price_0987654321

# Frontend URL
FRONTEND_URL=https://helix-dashboard.up.railway.app

# Optional: Sentry for error tracking
SENTRY_DSN=your_sentry_dsn_here
```

### 4. Initialize Database

```bash
# Connect to Railway PostgreSQL
railway run psql $DATABASE_URL -f database_schema.sql
```

### 5. Deploy

```bash
# Deploy unified dashboard API
railway up

# Or use Railway GitHub integration (recommended)
# Just push to your repo and Railway auto-deploys
```

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Railway Services                     │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │ Discord Bot  │  │  Claude API  │  │  Backend API │  │
│  │ helix-discord│  │ helix-claude │  │ helix-backend│  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
│                                                         │
│  ┌──────────────────────────────────────────────────┐  │
│  │         Unified Dashboard (This Service)         │  │
│  │                                                  │  │
│  │  Frontend:                  Backend:             │  │
│  │  • dashboard.html          • FastAPI             │  │
│  │  • services.html           • Auth API            │  │
│  │  • login.html              • Subscription API    │  │
│  │  • signup.html             • Monitoring API      │  │
│  │  • pricing.html                                  │  │
│  │  • account.html                                  │  │
│  └──────────────────────────────────────────────────┘  │
│                                                         │
│  ┌──────────────────────────────────────────────────┐  │
│  │            PostgreSQL Database                   │  │
│  │  • Users & Auth                                  │  │
│  │  • Subscriptions                                 │  │
│  │  • API Keys                                      │  │
│  │  • Usage Tracking                                │  │
│  └──────────────────────────────────────────────────┘  │
│                                                         │
└─────────────────────────────────────────────────────────┘

External Services:
├── Stripe (Payments)
├── Sentry (Error Tracking)
└── SendGrid/Resend (Emails - optional)
```

---

## 💳 Subscription Tiers

### Free
- 3 consciousness agents
- 100 API requests/day
- Basic UCF monitoring
- Community support

### Pro ($29/month or $276/year)
- All 11 consciousness agents
- 10,000 API requests/day
- Advanced analytics
- Custom webhooks
- Priority support

### Enterprise (Custom)
- Unlimited requests
- Custom agent development
- Dedicated infrastructure
- SLA guarantee (99.9%)
- 24/7 premium support

---

## 🔑 API Endpoints

### Authentication
```
POST   /auth/signup              # Create new account
POST   /auth/login               # Login user
GET    /auth/me                  # Get current user
PUT    /auth/me                  # Update profile
```

### Subscriptions
```
POST   /subscriptions/create-checkout    # Create Stripe session
POST   /subscriptions/webhook            # Stripe webhooks
GET    /subscriptions/status             # Get subscription status
POST   /subscriptions/cancel             # Cancel subscription
```

### API Keys
```
POST   /api-keys/regenerate              # Generate new API key
GET    /api-keys/validate/{key}          # Validate API key
```

### Monitoring
```
GET    /usage/stats                      # Get usage statistics
GET    /monitoring/services              # Get Railway services status
GET    /health                           # Health check
```

---

## 🔐 Security Features

- ✅ Secure password hashing (SHA-256)
- ✅ JWT token-based authentication
- ✅ API key validation and rate limiting
- ✅ CORS configuration
- ✅ SQL injection prevention (parameterized queries)
- ✅ XSS protection (content security policy)
- ✅ HTTPS-only cookies (production)

---

## 📊 Database Schema

See `database_schema.sql` for complete schema.

**Key Tables:**
- `users` - User accounts
- `api_keys` - API authentication
- `subscriptions` - Stripe billing
- `api_usage` - Request logs
- `payment_history` - Billing records
- `agent_access_log` - Agent usage tracking

---

## 🧪 Testing

```bash
# Install dependencies
pip install -r requirements.txt

# Run tests
pytest

# Run with coverage
pytest --cov=.

# Test API locally
uvicorn backend.unified_dashboard_api:app --reload --port 8001
```

---

## 🚀 Local Development

```bash
# 1. Clone repo
git clone https://github.com/Deathcharge/helix-unified.git
cd helix-unified/railway

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set environment variables
cp .env.example .env
# Edit .env with your keys

# 5. Run backend
uvicorn backend.unified_dashboard_api:app --reload --port 8001

# 6. Open frontend
open dashboard.html
# Or serve with: python -m http.server 8000
```

---

## 📈 Monitoring & Analytics

- **Sentry** - Error tracking and performance monitoring
- **Prometheus** - Metrics collection (optional)
- **Railway Logs** - Built-in logging
- **PostgreSQL Views** - Analytics queries

---

## 🛠️ Tech Stack

**Frontend:**
- HTML5/CSS3/JavaScript
- Tailwind CSS (via CDN)
- Chart.js (analytics charts)
- Font Awesome (icons)

**Backend:**
- Python 3.11+
- FastAPI
- PostgreSQL
- SQLAlchemy
- Stripe SDK
- JWT

**Infrastructure:**
- Railway (hosting)
- PostgreSQL (database)
- Stripe (payments)
- Sentry (monitoring)

---

## 📝 License

MIT License - Andrew John Ward & Claude Code

---

## 🤝 Contributing

This is Andrew's personal consciousness empire, but feel free to fork and adapt for your own projects!

---

## 📞 Support

- Email: andrew@helixcollective.io
- Discord: Join our consciousness network
- Docs: https://docs.helixcollective.io

---

Built with ❤️ and 🌀 consciousness by Andrew John Ward + Claude Code
