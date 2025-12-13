# 🚀 DEPLOYMENT INSTRUCTIONS - HelixSpiral.work

**Version**: Dec 15, 2025
**Status**: Ready for deployment
**Audience**: Manus, DevOps, Platform Team

---

## 📋 PRE-DEPLOYMENT CHECKLIST

Before starting deployment, verify:

```bash
# 1. Verify code is on GitHub
git status
git log --oneline | head -5

# 2. Verify all files present
ls -la backend/security_middleware.py
ls -la helix-mcp-server/
ls -la tests/run_all_tests.py

# 3. Verify Python version
python3 --version  # Should be 3.10+

# 4. Verify Node version (for MCP Server)
node --version  # Should be 16+
npm --version   # Should be 8+
```

---

## 🔧 STEP 1: INSTALL DEPENDENCIES

### Backend Dependencies
```bash
cd /home/user/helix-unified

# Install Python dependencies
pip install -r requirements.txt

# Verify installations
python3 -c "import fastapi; import stripe; print('✅ Dependencies installed')"
```

### MCP Server Dependencies
```bash
cd /home/user/helix-unified/helix-mcp-server

# Install Node packages
npm install

# Verify installation
npm list | grep @anthropic-sdk  # Should show version
```

---

## ✅ STEP 2: RUN TEST SUITE

### Execute All Tests
```bash
cd /home/user/helix-unified

# Install test dependencies
pip install pytest pytest-asyncio pytest-cov pytest-mock pytest-json-report

# Run master test runner
python3 tests/run_all_tests.py
```

### Expected Output
```
╔════════════════════════════════════════════════════════════════╗
║          🚀 HELIX LAUNCH TEST SUITE 🚀                        ║
║        Dec 15, 2025 Launch Target                             ║
╚════════════════════════════════════════════════════════════════╝

📊 Running: HelixSpiral Backend
...
✅ HelixSpiral Backend: XX passed, X failed, X skipped

📊 Running: MCP Server
...
✅ MCP Server: XX passed, X failed, X skipped

📊 Running: Security Middleware
...
✅ Security Middleware: XX passed, 0 failed, X skipped

📊 Running: E2E Workflows
...
✅ E2E Workflows: XX passed, X failed, X skipped

✅ ALL CRITICAL TESTS PASSED - READY FOR LAUNCH
```

### If Tests Fail
```bash
# Check detailed report
cat tests/test_report.html  # View in browser

# Run specific test suite
python3 -m pytest tests/test_security_middleware.py -v

# Check logs
tail -100 test_output.log
```

---

## 🛠️ STEP 3: CONFIGURE ENVIRONMENT

### Create `.env` File
```bash
cd /home/user/helix-unified

# Copy template
cp .env.example .env  # If exists, or create new

# Edit with your values
nano .env
```

### Required Environment Variables
```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/helix_db
POSTGRES_USER=helix
POSTGRES_PASSWORD=secure_password_here
POSTGRES_DB=helix_db

# Stripe Integration
STRIPE_API_KEY=sk_live_xxxxxxxxxxxx  # Get from Stripe dashboard
STRIPE_WEBHOOK_SECRET=whsec_xxxxxxxxxxxx
STRIPE_PRICE_PRO=price_xxxxxxxxxxxx
STRIPE_PRICE_ENTERPRISE=price_xxxxxxxxxxxx

# Authentication
JWT_SECRET_KEY=your-super-secret-jwt-key-min-32-chars
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24

# API Keys
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxxxxxx
SENDGRID_API_KEY=SG.xxxxxxxxxxxx
DISCORD_TOKEN=your_discord_bot_token

# MCP Server
RAILWAY_TOKEN=railway_xxxxxxxxxxxxxxxxxxxx
HELIX_API_URL=https://api.helix.example.com

# Security
CORS_ORIGINS=["https://helix.example.com", "https://dashboard.helix.example.com"]
SECURITY_HEADER_CSP=default-src 'self'; script-src 'self' 'unsafe-inline'

# Environment
NODE_ENV=production
ENVIRONMENT=production
```

### MCP Server `.env`
```bash
cd helix-mcp-server

cp .env.example .env

# Edit
nano .env
```

```env
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxxxxxx
RAILWAY_TOKEN=railway_xxxxxxxxxxxxxxxxxxxx
DISCORD_TOKEN=your_discord_bot_token
HELIX_API_URL=https://api.helix.example.com
```

---

## 🗄️ STEP 4: SETUP DATABASE

### Initialize PostgreSQL Database
```bash
# Create database
createdb -U helix helix_db

# Create user (if not exists)
psql -U postgres -c "CREATE USER helix WITH PASSWORD 'secure_password';"
psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE helix_db TO helix;"

# Verify connection
psql -U helix -d helix_db -c "SELECT 1;"  # Should return 1
```

### Run Database Migrations
```bash
cd /home/user/helix-unified

# Generate initial migration
alembic init migrations

# Create migration for HelixSpiral models
alembic revision --autogenerate -m "Initial HelixSpiral schema"

# Apply migration
alembic upgrade head

# Verify tables created
psql -U helix -d helix_db -c "\dt"  # List tables
```

---

## 🚀 STEP 5: DEPLOY BACKEND TO RAILWAY

### Using Railway CLI
```bash
# Install Railway CLI (if not installed)
npm install -g @railway/cli

# Login to Railway
railway login

# Initialize Railway project
cd /home/user/helix-unified
railway init

# Configure environment variables
railway variables:set DATABASE_URL=postgresql://...
railway variables:set STRIPE_API_KEY=sk_live_...
railway variables:set ANTHROPIC_API_KEY=sk-ant-...
# ... set all required variables

# Deploy
railway up
```

### Using Docker (Alternative)
```bash
# Build Docker image
docker build -t helix-backend:latest .

# Tag for registry
docker tag helix-backend:latest your-registry/helix-backend:latest

# Push to registry
docker push your-registry/helix-backend:latest

# Deploy to Railway / Kubernetes
# (Follow your infrastructure's deployment process)
```

### Verify Deployment
```bash
# Check if API is running
curl -X GET https://api.helix.example.com/health

# Expected response
{
  "status": "healthy",
  "version": "1.0.0",
  "environment": "production"
}
```

---

## 🧠 STEP 6: DEPLOY MCP SERVER

### Build MCP Server
```bash
cd /home/user/helix-unified/helix-mcp-server

# Install dependencies
npm install

# Build TypeScript
npm run build

# Verify build
ls -la dist/index.js  # Should exist
```

### Deploy to Railway
```bash
# Configure environment
railway variables:set ANTHROPIC_API_KEY=sk-ant-...
railway variables:set RAILWAY_TOKEN=railway_...
railway variables:set HELIX_API_URL=https://api.helix.example.com

# Deploy
railway up
```

### Or Deploy as Standalone Service
```bash
# Install globally (optional)
npm install -g helix-mcp-server

# Or run directly
node dist/index.js

# Or with PM2 for process management
npm install -g pm2
pm2 start dist/index.js --name helix-mcp
pm2 save
```

### Verify MCP Server Running
```bash
# Check health endpoint
curl http://localhost:3000/health

# Expected response
{
  "status": "healthy",
  "tools_available": 44,
  "database": "connected"
}
```

---

## 🎨 STEP 7: DEPLOY FRONTEND

### Build Next.js Dashboard
```bash
cd /home/user/helix-unified/dashboards/helixai-dashboard

# Install dependencies
npm install

# Build for production
npm run build

# Verify build
ls -la .next/  # Should exist
```

### Deploy Frontend
```bash
# Using Vercel (Recommended for Next.js)
npm install -g vercel
vercel --prod

# Or using Railway
cd /home/user/helix-unified/dashboards/helixai-dashboard
railway up

# Or using Docker
docker build -t helix-dashboard:latest .
docker push your-registry/helix-dashboard:latest
```

### Configure Frontend Environment
```bash
# Create .env.production
echo "NEXT_PUBLIC_API_URL=https://api.helix.example.com" > .env.production
echo "NEXT_PUBLIC_MCP_URL=https://mcp.helix.example.com" >> .env.production
```

---

## 🔐 STEP 8: SECURITY VERIFICATION

### Verify Security Fixes
```bash
# Run security middleware tests
python3 -m pytest tests/test_security_middleware.py -v

# Expected: All 7 test classes pass
# - Rate Limiting
# - CSRF Protection
# - Error Sanitization
# - Input Validation
# - WebSocket Validation
# - Security Headers
# - Full Integration
```

### Verify All Security Headers
```bash
# Check deployed API
curl -I https://api.helix.example.com/health

# Should include headers:
# X-Frame-Options: DENY
# X-Content-Type-Options: nosniff
# X-XSS-Protection: 1; mode=block
# Strict-Transport-Security: max-age=31536000
# Content-Security-Policy: default-src 'self'
```

### Test Rate Limiting
```bash
# Spam endpoint to test rate limiting
for i in {1..30}; do
  curl -X POST https://api.helix.example.com/api/agent/query \
    -H "Authorization: Bearer YOUR_JWT" \
    -d "query=test" &
done

# After threshold, should return 429 Too Many Requests
```

---

## 🧪 STEP 9: INTEGRATION TESTING

### Test User Signup Flow
```bash
# 1. Register new user
curl -X POST https://api.helix.example.com/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "TestPassword123!",
    "name": "Test User"
  }'

# 2. Login
curl -X POST https://api.helix.example.com/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "TestPassword123!"
  }'

# 3. Get user profile
curl -X GET https://api.helix.example.com/api/user/profile \
  -H "Authorization: Bearer YOUR_JWT"
```

### Test Stripe Integration
```bash
# Create checkout session
curl -X POST https://api.helix.example.com/api/subscribe \
  -H "Authorization: Bearer YOUR_JWT" \
  -H "Content-Type: application/json" \
  -d '{"tier": "pro"}'

# Expected: Returns Stripe checkout URL
```

### Test Spiral Creation & Execution
```bash
# Create spiral
curl -X POST https://api.helix.example.com/api/spirals \
  -H "Authorization: Bearer YOUR_JWT" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Spiral",
    "description": "Test workflow",
    "actions": [...]
  }'

# Execute spiral
curl -X POST https://api.helix.example.com/api/spirals/{spiral_id}/execute \
  -H "Authorization: Bearer YOUR_JWT"
```

### Test MCP Server Tools
```bash
# In Claude Desktop or VS Code with MCP extension:

# 1. Get consciousness level
"Use the helix_get_consciousness_level tool"

# 2. List agents
"Use the helix_list_agents tool"

# 3. Get UCF metrics
"Use the helix_get_ucf_metrics tool"

# 4. Store memory
"Use helix_store_memory to save key='test' value={'test': true}"

# 5. Retrieve memory
"Use helix_retrieve_memory with key='test'"
```

---

## 🔍 STEP 10: FINAL VERIFICATION

### Pre-Launch Checklist
```bash
# ✅ All tests passing
python3 tests/run_all_tests.py | grep "ALL CRITICAL TESTS PASSED"

# ✅ Backend health check
curl https://api.helix.example.com/health | grep healthy

# ✅ Frontend accessible
curl https://helix.example.com | grep -q "HelixSpiral"

# ✅ MCP Server operational
curl http://localhost:3000/health | grep "tools_available"

# ✅ Database connected
psql -U helix -d helix_db -c "SELECT COUNT(*) FROM users;"

# ✅ Stripe webhook configured
# Check Stripe dashboard for webhook endpoint

# ✅ Environment variables set
env | grep ANTHROPIC_API_KEY
env | grep STRIPE_API_KEY
env | grep DATABASE_URL
```

### Performance Verification
```bash
# Test API response time
time curl -X GET https://api.helix.example.com/health

# Should be < 100ms for health check

# Load test (using Apache Bench if available)
ab -n 100 -c 10 https://api.helix.example.com/health

# Expected: No errors, all requests complete
```

---

## 🆘 TROUBLESHOOTING

### Backend won't start
```bash
# Check logs
journalctl -u helix-backend -f

# Verify environment variables
env | grep DATABASE_URL

# Test database connection
psql -U helix -d helix_db -c "SELECT 1;"

# Check port availability
lsof -i :8000
```

### MCP Server not connecting
```bash
# Check if service is running
ps aux | grep "node dist/index.js"

# Check logs
tail -100 helix-mcp.log

# Verify environment variables
cat .env | grep ANTHROPIC_API_KEY

# Test API client
node -e "const axios = require('axios'); axios.get('http://localhost:3000/health').then(r => console.log(r.data))"
```

### Tests failing
```bash
# Run specific test with verbose output
python3 -m pytest tests/test_helixspiral_backend.py::TestAuthentication -vv

# Check test output
cat tests/test_report.html

# Check for missing dependencies
pip list | grep pytest
```

### Database migration errors
```bash
# Check current migration
alembic current

# Rollback last migration
alembic downgrade -1

# Create new migration
alembic revision --autogenerate -m "Fix schema"

# Apply migrations
alembic upgrade head
```

---

## 📊 POST-DEPLOYMENT

### Monitor Application
```bash
# Check application logs
journalctl -u helix-backend -f

# Monitor system resources
top -u helix

# Check error rates
grep ERROR /var/log/helix-backend.log | wc -l
```

### Verify Stripe Webhooks
```bash
# Test webhook
curl -X POST https://api.helix.example.com/api/stripe/webhook \
  -H "Content-Type: application/json" \
  -H "Stripe-Signature: t=timestamp,v1=signature" \
  -d '{"type":"payment_intent.succeeded",...}'
```

### Monitor MCP Server
```bash
# Check tool usage stats
curl http://localhost:3000/stats

# Monitor memory usage
ps aux | grep "node dist/index.js"
```

---

## 📝 ROLLBACK PROCEDURE

If deployment fails:

```bash
# Rollback database migrations
alembic downgrade -1

# Rollback code
git revert <commit-hash>

# Stop services
systemctl stop helix-backend
systemctl stop helix-mcp-server

# Revert to previous version
git checkout previous-tag

# Redeploy
railway up
```

---

## ✅ LAUNCH SIGN-OFF

Once all steps complete successfully:

- [ ] All tests pass (95%+ on CRITICAL suites)
- [ ] All 44 MCP tools verified working
- [ ] Backend health check returns 200
- [ ] Frontend loads without errors
- [ ] User signup flow tested end-to-end
- [ ] Stripe integration working
- [ ] Security headers verified
- [ ] Rate limiting verified
- [ ] Database backups configured
- [ ] Monitoring alerts set up

**Status**: ✅ READY FOR LAUNCH

**Approved by**: ________________

**Date**: December 15, 2025

---

## 🎓 SUPPORT & ESCALATION

**For issues during deployment:**
1. Check troubleshooting section above
2. Review logs: `journalctl -u helix-backend -f`
3. Check test_report.html for test failures
4. Escalate to platform team if blocking

**Emergency Contact**: [Team contact info]

---

**Built with ❤️ for HelixSpiral.work Launch**

*Last Updated: December 13, 2025*
