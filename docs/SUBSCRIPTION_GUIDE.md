# Subscription Management Guide

## Overview

Helix Unified includes a complete subscription management system powered by Stripe, with tier-based access control and usage metering.

## Subscription Tiers

### Free Tier
- **Price:** $0/month
- **Features:**
  - 100 API requests/day
  - 3 AI agents
  - 10 custom prompts
  - Community support

### Pro Tier
- **Price:** $99/month or $950/year
- **Features:**
  - 10,000 API requests/day
  - 14 AI agents (all available)
  - Unlimited custom prompts
  - 10 workflow automations
  - Email support
  - Advanced analytics

### Workflow Tier
- **Price:** $299/month or $2,850/year
- **Features:**
  - 20,000 API requests/day
  - 14 AI agents
  - Unlimited custom prompts
  - 100 workflow automations
  - Priority email support
  - Team management (up to 5 users)
  - Advanced analytics

### Enterprise Tier
- **Price:** $999/month or $9,500/year
- **Features:**
  - Unlimited API requests
  - 14 AI agents
  - Unlimited custom prompts
  - Unlimited workflow automations
  - 24/7 phone support
  - Unlimited team members
  - White-label options
  - SLA guarantee (99.9% uptime)
  - Custom integrations

## Backend Architecture

### Core Files

1. **`backend/saas_stripe.py`** - Stripe integration & subscription logic
2. **`backend/saas/dashboard_api.py`** - Dashboard & billing endpoints
3. **`backend/routes/saas_core.py`** - Main SaaS router
4. **`database/saas_schema.sql`** - Database schema

### Database Schema

```sql
-- Users table with subscription info
CREATE TABLE users (
    id UUID PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    tier VARCHAR(20) DEFAULT 'free',
    stripe_customer_id VARCHAR(255),
    stripe_subscription_id VARCHAR(255),
    subscription_status VARCHAR(50),
    requests_per_day INTEGER DEFAULT 100,
    agents_allowed INTEGER DEFAULT 3,
    prompts_allowed INTEGER DEFAULT 10,
    workflows_allowed INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Payments table
CREATE TABLE payments (
    id SERIAL PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    stripe_payment_id VARCHAR(255),
    stripe_invoice_id VARCHAR(255),
    amount_usd DECIMAL(10,2),
    currency VARCHAR(3) DEFAULT 'USD',
    status VARCHAR(20),
    description TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);
```

## API Endpoints

### Authentication

#### Register
```http
POST /v1/saas/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePass123!",
  "full_name": "John Doe",
  "company": "Acme Corp"
}
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "api_key": "sk_live_abc123...",
  "token_type": "bearer",
  "user": {
    "id": "uuid-here",
    "email": "user@example.com",
    "tier": "free"
  }
}
```

#### Login
```http
POST /v1/saas/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePass123!"
}
```

### Subscription Management

#### Get Billing Information
```http
GET /api/saas/dashboard/billing
Authorization: Bearer {token}
```

**Response:**
```json
{
  "tier": "pro",
  "current_period": {
    "api_calls_used": 5234,
    "api_calls_included": 10000,
    "additional_charges": 0.00,
    "estimated_total": 99.00,
    "period_start": "2025-12-01",
    "period_end": "2025-12-31"
  },
  "history": [
    {
      "date": "2025-11-30",
      "amount": 99.00,
      "api_calls": 8456,
      "status": "paid"
    }
  ]
}
```

#### Create Subscription
```http
POST /stripe/create-subscription
Authorization: Bearer {token}
Content-Type: application/json

{
  "tier": "pro",
  "billing_cycle": "monthly",
  "payment_method_id": "pm_1234..."
}
```

**Response:**
```json
{
  "subscription_id": "sub_1234...",
  "customer_id": "cus_5678...",
  "status": "active",
  "tier": "pro",
  "current_period_end": "2026-01-12T00:00:00Z",
  "cancel_at_period_end": false
}
```

#### Create Checkout Session
```http
POST /stripe/checkout-session
Authorization: Bearer {token}
Content-Type: application/json

{
  "tier": "pro",
  "billing_cycle": "yearly",
  "success_url": "https://example.com/success",
  "cancel_url": "https://example.com/cancel"
}
```

**Response:**
```json
{
  "checkout_url": "https://checkout.stripe.com/...",
  "session_id": "cs_test_..."
}
```

#### Upgrade Subscription
```http
POST /api/saas/dashboard/upgrade
Authorization: Bearer {token}
Content-Type: application/json

{
  "tier": "enterprise"
}
```

**Response:**
```json
{
  "status": "success",
  "checkout_url": "https://checkout.stripe.com/..."
}
```

#### Cancel Subscription
```http
POST /api/saas/dashboard/cancel-subscription
Authorization: Bearer {token}
```

**Response:**
```json
{
  "status": "success",
  "message": "Subscription will be cancelled at period end"
}
```

#### Get Invoices
```http
GET /api/saas/dashboard/invoices
Authorization: Bearer {token}
```

**Response:**
```json
{
  "invoices": [
    {
      "id": "in_1234...",
      "date": "2025-12-01",
      "amount": 99.00,
      "status": "paid",
      "download_url": "https://..."
    }
  ]
}
```

## Frontend Integration

### Using the Billing Page

The billing page (`frontend/pages/settings/billing.tsx`) provides a complete UI for:

1. **Current Billing Period Display**
   - API usage tracking with progress bars
   - Cost breakdown
   - Period dates

2. **Plan Selection & Upgrade**
   - Visual tier comparison
   - One-click upgrade to Stripe Checkout
   - Current plan indicator

3. **Invoice History**
   - Downloadable PDFs
   - Payment status
   - Historical usage data

### Example Usage

```tsx
import { useFormatters } from '@/lib/use-formatters';

function SubscriptionCard() {
  const formatters = useFormatters('USD');
  const [billing, setBilling] = useState(null);

  useEffect(() => {
    fetch('/api/saas/dashboard/billing', {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })
    .then(res => res.json())
    .then(data => setBilling(data));
  }, []);

  if (!billing) return <div>Loading...</div>;

  return (
    <div>
      <h2>Current Plan: {billing.tier}</h2>
      <p>
        Usage: {formatters.formatNumber(billing.current_period.api_calls_used)}
        / {formatters.formatNumber(billing.current_period.api_calls_included)}
      </p>
      <p>
        Total: {formatters.formatCurrency(billing.current_period.estimated_total)}
      </p>
    </div>
  );
}
```

## Webhook Handling

Stripe webhooks automatically sync subscription state:

### Supported Events

1. **`customer.subscription.created`**
   - Activates user subscription
   - Updates tier and limits

2. **`customer.subscription.updated`**
   - Syncs subscription changes
   - Updates billing cycle

3. **`customer.subscription.deleted`**
   - Downgrades to free tier
   - Clears subscription ID

4. **`invoice.payment_succeeded`**
   - Records payment
   - Confirms active status

5. **`invoice.payment_failed`**
   - Sets status to "past_due"
   - Triggers retry logic

### Webhook Endpoint

```http
POST /stripe/webhook
Stripe-Signature: {signature}
```

**Configuration in Stripe Dashboard:**
```
Endpoint URL: https://api.helixspiral.work/stripe/webhook
Events: customer.subscription.*, invoice.*
```

## Usage Metering

### Rate Limiting

API requests are tracked and limited based on tier:

```python
from backend.saas_auth import get_current_user_jwt

@router.post("/api/protected-endpoint")
async def protected_endpoint(user = Depends(get_current_user_jwt)):
    # User tier and limits automatically enforced
    # Returns 429 if rate limit exceeded
    pass
```

### Usage Tracking

```python
from backend.saas.usage_metering import UsageMeter

meter = UsageMeter()
meter.record_usage(user_id, "api_calls", quantity=1)
```

## Testing Subscriptions

### Test Mode Setup

1. Use Stripe test keys:
```env
STRIPE_SECRET_KEY=sk_test_...
STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_WEBHOOK_SECRET=whsec_test_...
```

2. Test card numbers:
```
Success: 4242 4242 4242 4242
Decline: 4000 0000 0000 0002
3D Secure: 4000 0025 0000 3155
```

### Example Flow

```python
# examples/04_subscription_flow.py
python examples/04_subscription_flow.py
```

## Environment Variables

Required Stripe configuration:

```env
# Stripe Keys
STRIPE_SECRET_KEY=sk_live_...
STRIPE_PUBLISHABLE_KEY=pk_live_...
STRIPE_WEBHOOK_SECRET=whsec_...

# Price IDs (create in Stripe Dashboard)
STRIPE_PRICE_PRO_MONTHLY=price_...
STRIPE_PRICE_PRO_YEARLY=price_...
STRIPE_PRICE_WORKFLOW_MONTHLY=price_...
STRIPE_PRICE_WORKFLOW_YEARLY=price_...
STRIPE_PRICE_ENTERPRISE_MONTHLY=price_...
STRIPE_PRICE_ENTERPRISE_YEARLY=price_...
```

## Best Practices

### 1. Always Check Tier Access

```python
@router.get("/premium-feature")
async def premium_feature(user = Depends(get_current_user_jwt)):
    if user["tier"] == "free":
        raise HTTPException(403, "Upgrade to access this feature")
    # Feature logic
```

### 2. Handle Failed Payments

```python
# In webhook handler
async def handle_payment_failed(invoice):
    # Send email to user
    # Update subscription status
    # Allow grace period
```

### 3. Provide Upgrade Prompts

```tsx
function FeatureGate({ tier, children }) {
  const { user } = useAuth();

  if (user.tier === 'free') {
    return (
      <div>
        <p>Upgrade to {tier} to unlock this feature</p>
        <button onClick={handleUpgrade}>Upgrade Now</button>
      </div>
    );
  }

  return children;
}
```

### 4. Test Webhook Delivery

```bash
# Use Stripe CLI for local testing
stripe listen --forward-to localhost:8000/stripe/webhook
stripe trigger customer.subscription.created
```

## Troubleshooting

### Subscription not activating

1. Check webhook delivery in Stripe Dashboard
2. Verify webhook signature
3. Check database for subscription_id and status

### Rate limits not working

1. Verify user tier in database
2. Check cache for rate limit keys
3. Ensure middleware is loaded

### Checkout session failing

1. Verify price IDs match Stripe Dashboard
2. Check success/cancel URLs are valid
3. Ensure customer_id is correct

## Migration Guide

### From Free to Paid

User upgrades automatically via Stripe Checkout:
1. User clicks "Upgrade"
2. Redirected to Stripe Checkout
3. On success, webhook updates database
4. User gains immediate access to features

### Cancellation

Subscriptions cancel at period end:
1. User clicks "Cancel"
2. Stripe marks `cancel_at_period_end=true`
3. User retains access until end date
4. On period end, webhook downgrades to free

## Revenue Projections

Based on current tier structure:

| Tier | Monthly | Yearly | Target Users | Monthly Revenue |
|------|---------|--------|--------------|-----------------|
| Free | $0 | $0 | 10,000 | $0 |
| Pro | $99 | $950 | 100 | $9,900 |
| Workflow | $299 | $2,850 | 30 | $8,970 |
| Enterprise | $999 | $9,500 | 10 | $9,990 |
| **Total** | | | **10,140** | **$28,860** |

**Year 1 Projected ARR:** $346,320

## Related Documentation

- [Internationalization Guide](./INTERNATIONALIZATION_GUIDE.md)
- [Stripe Setup](./STRIPE_SETUP.md)
- [API Reference](./API_REFERENCE.md)
- [Database Schema](../database/saas_schema.sql)
