# 🔐 Security Quick Start Guide

**Last Updated:** December 7, 2025  
**For:** Helix-Unified v17.2+

This guide helps you quickly implement the new security features in your development workflow.

---

## 🚀 Quick Setup (5 minutes)

### 1. Generate JWT Secret

```bash
# Generate a secure 32-character secret
openssl rand -hex 32
```

Copy the output and add to your `.env` file:

```bash
JWT_SECRET=<paste_generated_secret_here>
```

### 2. Install Dependencies

```bash
# Backend
pip install passlib[bcrypt] pyjwt slowapi

# Frontend
cd frontend && npm install axios
```

### 3. Set CORS Origins

Add to `.env`:

```bash
ALLOWED_ORIGINS=http://localhost:3000,https://yourdomain.com
ENVIRONMENT=development  # or 'production'
```

---

## 🔑 Using the New Auth System

### Backend: Password Hashing

```python
from backend.core.security import hash_password, verify_password

# Hash a password
hashed = hash_password("user_password_123")

# Verify a password
is_valid = verify_password("user_password_123", hashed)
```

### Backend: JWT Tokens

```python
from backend.core.security import create_access_token, decode_access_token

# Create token
token = create_access_token({
    "sub": user.id,
    "email": user.email,
    "name": user.name,
    "tier": "pro"
})

# Decode token
payload = decode_access_token(token)
if payload:
    user_id = payload["sub"]
```

### Backend: Rate Limiting

```python
from fastapi import Request
from backend.core.rate_limit import limiter, get_rate_limit

@router.post("/api/expensive-operation")
@limiter.limit(get_rate_limit("api_expensive"))  # 10/minute
async def expensive_operation(request: Request):
    # Your code here
    pass
```

### Backend: Error Handling

```python
from backend.core.errors import (
    InvalidCredentialsError,
    NotFoundError,
    RateLimitError,
)

# Raise custom errors
if not user:
    raise NotFoundError("User", user_id)

if not verify_password(password, user.password_hash):
    raise InvalidCredentialsError()
```

---

## 🌐 Frontend: Using Axios

### Import the Configured Instance

```typescript
import api, { apiHelpers } from '@/lib/axios'

// All requests automatically include auth token
const response = await api.get('/api/agents')
```

### Helper Functions

```typescript
// Login
const { access_token, user } = await apiHelpers.login(email, password)

// Signup
const { access_token, user } = await apiHelpers.signup(email, password, name)

// Get current user
const user = await apiHelpers.getCurrentUser()

// Logout
await apiHelpers.logout()

// Demo login
const { access_token, user } = await apiHelpers.demoLogin()
```

### Manual API Calls

```typescript
import api from '@/lib/axios'

// GET request
const agents = await api.get('/api/agents')

// POST request
const rental = await api.post('/api/agents/rental', {
  agent_id: 'kael',
  duration_hours: 24
})

// Error handling
try {
  await api.post('/api/protected-route')
} catch (error) {
  if (error.response?.status === 401) {
    // User will be automatically redirected to login
  }
}
```

---

## 🛡️ Frontend: Error Boundaries

### Wrap Components

```tsx
import { ErrorBoundary } from '@/components/ui/ErrorBoundary'

export default function MyPage() {
  return (
    <ErrorBoundary>
      <MyComponent />
    </ErrorBoundary>
  )
}
```

### Custom Fallback

```tsx
<ErrorBoundary fallback={<div>Custom error message</div>}>
  <MyComponent />
</ErrorBoundary>
```

---

## 🧪 Testing

### Run Frontend Tests

```bash
cd frontend

# Run once
npm test

# Watch mode
npm run test:watch

# With coverage
npm run test:coverage
```

### Run Backend Tests

```bash
# All tests
pytest

# With coverage
pytest --cov=backend --cov-report=html

# Specific test file
pytest tests/test_auth.py
```

---

## 🔒 Security Checklist

Before deploying to production:

- [ ] JWT_SECRET is set and at least 32 characters
- [ ] ALLOWED_ORIGINS does not include `*`
- [ ] ENVIRONMENT is set to `production`
- [ ] All passwords are hashed with bcrypt
- [ ] Rate limiting is enabled on all endpoints
- [ ] HTTPS is enforced
- [ ] Error messages don't leak sensitive info
- [ ] Secrets are not in version control
- [ ] Database connection pooling is configured
- [ ] Error boundaries are in place

---

## 📊 Rate Limit Tiers

| Endpoint Type | Limit | Use Case |
|--------------|-------|----------|
| `auth_login` | 5/minute | Login attempts |
| `auth_signup` | 3/minute | Account creation |
| `auth_password_reset` | 3/hour | Password reset |
| `api_general` | 100/minute | Standard API calls |
| `api_expensive` | 10/minute | AI operations, rendering |
| `webhook` | 1000/hour | Trusted webhooks |

### Custom Rate Limits

```python
from backend.core.rate_limit import limiter

@router.post("/custom-endpoint")
@limiter.limit("20/minute")  # Custom limit
async def custom_endpoint(request: Request):
    pass
```

---

## 🐛 Common Issues

### Issue: "JWT_SECRET environment variable is required"

**Solution:** Add JWT_SECRET to your `.env` file:
```bash
openssl rand -hex 32  # Generate secret
echo "JWT_SECRET=<generated_secret>" >> .env
```

### Issue: "CORS error in browser"

**Solution:** Add your frontend URL to ALLOWED_ORIGINS:
```bash
ALLOWED_ORIGINS=http://localhost:3000,https://yourdomain.com
```

### Issue: "Rate limit exceeded"

**Solution:** Wait for the retry period or adjust limits in `backend/core/rate_limit.py`

### Issue: "401 Unauthorized"

**Solution:** Check that:
1. Token is stored in localStorage as `helix_token`
2. Token hasn't expired (7 days default)
3. JWT_SECRET matches between token creation and verification

---

## 📚 Additional Resources

- [Comprehensive Audit Report](./COMPREHENSIVE_CODEBASE_AUDIT_2025.md) - Full security analysis
- [Implementation Plan](./IMPROVEMENT_IMPLEMENTATION_PLAN.md) - Detailed roadmap
- [Improvements Completed](./IMPROVEMENTS_COMPLETED_DEC_2025.md) - What's been done

---

## 🆘 Getting Help

1. **Check the logs:**
   ```bash
   # Backend logs
   tail -f logs/helix.log
   
   # Frontend console
   # Open browser DevTools → Console
   ```

2. **Run tests:**
   ```bash
   npm test  # Frontend
   pytest    # Backend
   ```

3. **Review examples:**
   - `backend/routes/auth.py` - Auth implementation
   - `frontend/lib/axios.ts` - API client
   - `frontend/__tests__/` - Test examples

---

**Quick Links:**
- 🔐 [Security Module](./backend/core/security.py)
- ⏱️ [Rate Limiting](./backend/core/rate_limit.py)
- ❌ [Error Handling](./backend/core/errors.py)
- 🌐 [Axios Config](./frontend/lib/axios.ts)
- 🛡️ [Error Boundary](./frontend/components/ui/ErrorBoundary.tsx)

---

*Stay secure! 🔒*
