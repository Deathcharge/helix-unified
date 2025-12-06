# 💳 Stripe Payment Setup Guide

**Complete guide to setting up Stripe payments for Helix Unified**

---

## 🎯 What You'll Set Up

- **Subscription Plans** - Professional, Team, Enterprise tiers
- **Usage-Based Billing** - Charge based on API calls
- **Payment Methods** - Credit cards, Apple Pay, Google Pay
- **Invoicing** - Automatic invoice generation
- **Webhooks** - Real-time payment event handling

---

## ⚡ Quick Start (15 Minutes)

### Step 1: Create Stripe Account

1. Go to [stripe.com](https://stripe.com)
2. Click "Start now" → Sign up
3. Complete account verification
4. Enable **Test Mode** (toggle in top-right)

---

### Step 2: Get API Keys

**In Stripe Dashboard:**

1. Go to **Developers** → **API keys**
2. Copy your keys:
   - **Publishable key** - `pk_test_...` (safe for frontend)
   - **Secret key** - `sk_test_...` (keep secure!)

**Add to Railway:**

```bash
# In Railway dashboard or CLI:
railway variables set STRIPE_PUBLISHABLE_KEY=pk_test_...
railway variables set STRIPE_SECRET_KEY=sk_test_...
```

---

### Step 3: Create Products

**In Stripe Dashboard:**

1. Go to **Products** → **Add product**

#### Product 1: Professional Plan

```
Name: Helix Professional
Description: Perfect for individuals and small teams
Price: $49/month
Billing period: Monthly
```

**Features to list:**
- 50,000 API calls/month
- Full consciousness metrics
- Discord integration
- Email support

#### Product 2: Team Plan

```
Name: Helix Team
Description: For growing teams with advanced needs
Price: $149/month
Billing period: Monthly
```

**Features:**
- 200,000 API calls/month
- Priority support
- Team management (up to 10 users)
- Advanced analytics

#### Product 3: Enterprise Plan

```
Name: Helix Enterprise
Description: Custom solutions for large organizations
Price: Custom (contact sales)
```

**Features:**
- Unlimited API calls
- Dedicated support
- Custom integrations
- SLA guarantee

---

### Step 4: Usage-Based Pricing (Optional)

For charging based on API usage:

**Create Usage-Based Product:**

1. **Products** → **Add product**
2. **Pricing model:** Usage-based
3. **Billing period:** Monthly
4. **Pricing:**
   - First 10,000 calls: Free
   - 10,001 - 50,000: $0.001 per call
   - 50,001+: $0.0005 per call

**Record usage in backend:**

```python
# backend/billing/stripe_usage.py
import stripe

def record_api_usage(subscription_id: str, quantity: int):
    """Record API calls for usage-based billing"""
    stripe.SubscriptionItem.create_usage_record(
        subscription_id,
        quantity=quantity,
        timestamp=int(time.time()),
        action='increment'
    )
```

---

### Step 5: Set Up Webhooks

**Why webhooks?**
- Know when payments succeed/fail
- Handle subscription updates
- Process refunds automatically

**Setup:**

1. **Developers** → **Webhooks** → **Add endpoint**
2. **Endpoint URL:** `https://your-backend.railway.app/api/stripe/webhook`
3. **Events to listen for:**
   - `checkout.session.completed` - New subscription
   - `customer.subscription.updated` - Plan changes
   - `customer.subscription.deleted` - Cancellations
   - `invoice.payment_succeeded` - Successful payment
   - `invoice.payment_failed` - Failed payment

4. **Copy Webhook Signing Secret:** `whsec_...`

**Add to Railway:**

```bash
railway variables set STRIPE_WEBHOOK_SECRET=whsec_...
```

---

## 🔧 Backend Integration

### Install Stripe SDK

```bash
# Python backend
pip install stripe

# Add to requirements.txt
echo "stripe>=7.0.0" >> requirements.txt
```

### Create Stripe Service

**File: `backend/billing/stripe_service.py`**

```python
import stripe
import os

stripe.api_key = os.environ['STRIPE_SECRET_KEY']

def create_checkout_session(
    customer_email: str,
    price_id: str,
    success_url: str,
    cancel_url: str
):
    """Create Stripe Checkout session for subscription"""
    session = stripe.checkout.Session.create(
        customer_email=customer_email,
        payment_method_types=['card'],
        line_items=[{
            'price': price_id,
            'quantity': 1,
        }],
        mode='subscription',
        success_url=success_url,
        cancel_url=cancel_url,
    )
    return session

def get_customer_subscription(customer_id: str):
    """Get active subscription for customer"""
    subscriptions = stripe.Subscription.list(customer=customer_id, status='active')
    return subscriptions.data[0] if subscriptions.data else None

def cancel_subscription(subscription_id: str):
    """Cancel a subscription at period end"""
    return stripe.Subscription.modify(
        subscription_id,
        cancel_at_period_end=True
    )
```

### Create Webhook Handler

**File: `backend/api/routes/stripe_webhook.py`**

```python
from fastapi import APIRouter, Request, HTTPException
import stripe
import os

router = APIRouter()
webhook_secret = os.environ['STRIPE_WEBHOOK_SECRET']

@router.post("/stripe/webhook")
async def stripe_webhook(request: Request):
    """Handle Stripe webhook events"""
    payload = await request.body()
    sig_header = request.headers.get('stripe-signature')

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, webhook_secret
        )
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Invalid signature")

    # Handle the event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        handle_successful_subscription(session)

    elif event['type'] == 'invoice.payment_succeeded':
        invoice = event['data']['object']
        handle_successful_payment(invoice)

    elif event['type'] == 'customer.subscription.deleted':
        subscription = event['data']['object']
        handle_subscription_cancellation(subscription)

    return {"status": "success"}

def handle_successful_subscription(session):
    """Activate user's subscription"""
    customer_email = session['customer_email']
    subscription_id = session['subscription']

    # Update database
    # db.users.update_one(
    #     {'email': customer_email},
    #     {'$set': {'subscription_id': subscription_id, 'plan': 'professional'}}
    # )

    print(f"✅ Subscription created for {customer_email}")

def handle_successful_payment(invoice):
    """Log successful payment"""
    print(f"💰 Payment succeeded: {invoice['amount_paid']/100} USD")

def handle_subscription_cancellation(subscription):
    """Deactivate user's subscription"""
    customer_id = subscription['customer']
    print(f"❌ Subscription cancelled for customer {customer_id}")
```

---

## 🎨 Frontend Integration

### Install Stripe.js

```bash
cd frontend
npm install @stripe/stripe-js
```

### Create Checkout Component

**File: `frontend/components/Checkout.tsx`**

```tsx
import React from 'react';
import { loadStripe } from '@stripe/stripe-js';

const stripePromise = loadStripe(process.env.NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY!);

export const CheckoutButton: React.FC<{
  priceId: string;
  planName: string;
}> = ({ priceId, planName }) => {
  const handleCheckout = async () => {
    const stripe = await stripePromise;

    // Call backend to create checkout session
    const response = await fetch('/api/create-checkout-session', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ priceId }),
    });

    const { sessionId } = await response.json();

    // Redirect to Stripe Checkout
    const result = await stripe?.redirectToCheckout({ sessionId });

    if (result?.error) {
      console.error(result.error.message);
    }
  };

  return (
    <button
      onClick={handleCheckout}
      className="px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-lg"
    >
      Subscribe to {planName}
    </button>
  );
};
```

---

## 🧪 Testing

### Test Mode

**Always test in Test Mode first!**

**Test Credit Cards:**

```
✅ Success: 4242 4242 4242 4242
❌ Declined: 4000 0000 0000 0002
🔐 3D Secure: 4000 0025 0000 3155
```

**Any future expiry date and any 3-digit CVC**

### Test Webhooks Locally

Use Stripe CLI for local testing:

```bash
# Install Stripe CLI
brew install stripe/stripe-cli/stripe

# Login
stripe login

# Forward webhooks to local server
stripe listen --forward-to localhost:8000/api/stripe/webhook

# Trigger test events
stripe trigger checkout.session.completed
stripe trigger invoice.payment_succeeded
```

---

## 🚀 Going Live

### Checklist Before Launch

- [ ] Switch to **Live Mode** in Stripe dashboard
- [ ] Get **Live API keys** (replace test keys)
- [ ] Update webhook endpoint to production URL
- [ ] Test live checkout flow with real card
- [ ] Set up payment failure notifications
- [ ] Configure invoice email templates
- [ ] Enable customer portal for self-service

### Switch to Production

```bash
# Replace test keys with live keys
railway variables set STRIPE_PUBLISHABLE_KEY=pk_live_...
railway variables set STRIPE_SECRET_KEY=sk_live_...
railway variables set STRIPE_WEBHOOK_SECRET=whsec_live_...
```

---

## 💡 Best Practices

### Security

1. **Never** expose secret key in frontend
2. **Always** validate webhooks with signature
3. **Use** idempotency keys for API calls
4. **Store** customer IDs securely in database

### User Experience

1. **Show clear pricing** on landing page
2. **Allow plan changes** without contacting support
3. **Provide trial period** (7-14 days)
4. **Send email receipts** automatically
5. **Enable customer portal** for self-service

### Compliance

1. **Display terms** clearly before checkout
2. **Collect billing address** for tax calculation
3. **Handle VAT/GST** for international customers
4. **Provide refund policy** prominently

---

## 📊 Stripe Dashboard Features

### Revenue Analytics

**Dashboard** → **Home**
- Revenue over time
- Active subscriptions
- Churn rate
- MRR (Monthly Recurring Revenue)

### Customer Management

**Customers** tab:
- View all customers
- Manual subscription changes
- Issue refunds
- Send invoices

### Failed Payments

**Settings** → **Billing** → **Retry rules**

Configure automatic retry logic:
- Retry after 3 days
- Retry after 5 days
- Retry after 7 days
- Cancel subscription after 4 failed attempts

---

## 🐛 Troubleshooting

### "Webhook signature verification failed"

**Fix:** Check that `STRIPE_WEBHOOK_SECRET` matches the webhook's signing secret in Stripe dashboard.

### "No such price: price_..."

**Fix:** Verify price ID exists in Stripe dashboard → Products.

### Checkout redirects but subscription not created

**Check:**
1. Webhook endpoint is reachable (not localhost)
2. Webhook is listening for `checkout.session.completed`
3. Check Railway logs for errors

### Customer can't access subscription

**Fix:** Implement Stripe Customer Portal:

```python
def create_customer_portal_session(customer_id: str, return_url: str):
    """Create Stripe Customer Portal session"""
    session = stripe.billing_portal.Session.create(
        customer=customer_id,
        return_url=return_url,
    )
    return session.url
```

---

## 📚 Additional Resources

- [Stripe Docs](https://stripe.com/docs)
- [Stripe Testing](https://stripe.com/docs/testing)
- [Subscription Billing Guide](https://stripe.com/docs/billing/subscriptions/overview)
- [Webhook Best Practices](https://stripe.com/docs/webhooks/best-practices)

---

**Questions?** Check Stripe support or test in Test Mode first!

**Pro Tip:** Start with simple monthly subscriptions, add usage-based billing later once you have customers! 💰
