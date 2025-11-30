"""
Helix Collective SaaS - Stripe Subscription Integration
========================================================

Handles:
- Subscription creation/cancellation
- Stripe webhook events
- Payment processing
- Tier upgrades/downgrades

Author: Claude (Manus Validator)
Date: 2025-11-30
"""

import stripe
import os
from typing import Dict, Any, Optional, List
from fastapi import HTTPException, Request
from pydantic import BaseModel
from datetime import datetime, timedelta
import hmac
import hashlib
from backend.saas_auth import Database

# ============================================================================
# CONFIGURATION
# ============================================================================

STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")
STRIPE_PUBLISHABLE_KEY = os.getenv("STRIPE_PUBLISHABLE_KEY")

stripe.api_key = STRIPE_SECRET_KEY

# Stripe Price IDs (create these in Stripe Dashboard)
STRIPE_PRICE_IDS = {
    "pro_monthly": os.getenv("STRIPE_PRICE_PRO_MONTHLY", "price_pro_monthly"),
    "pro_yearly": os.getenv("STRIPE_PRICE_PRO_YEARLY", "price_pro_yearly"),
    "workflow_monthly": os.getenv("STRIPE_PRICE_WORKFLOW_MONTHLY", "price_workflow_monthly"),
    "workflow_yearly": os.getenv("STRIPE_PRICE_WORKFLOW_YEARLY", "price_workflow_yearly"),
    "enterprise_monthly": os.getenv("STRIPE_PRICE_ENTERPRISE_MONTHLY", "price_enterprise_monthly"),
    "enterprise_yearly": os.getenv("STRIPE_PRICE_ENTERPRISE_YEARLY", "price_enterprise_yearly"),
}

# ============================================================================
# PYDANTIC MODELS
# ============================================================================

class CreateSubscriptionRequest(BaseModel):
    """Request to create subscription"""
    tier: str  # 'pro', 'workflow', 'enterprise'
    billing_cycle: str = "monthly"  # 'monthly' or 'yearly'
    payment_method_id: Optional[str] = None  # Stripe PaymentMethod ID

class SubscriptionResponse(BaseModel):
    """Subscription response"""
    subscription_id: str
    customer_id: str
    status: str
    tier: str
    current_period_end: datetime
    cancel_at_period_end: bool

class UpdateSubscriptionRequest(BaseModel):
    """Request to update subscription"""
    tier: Optional[str] = None
    billing_cycle: Optional[str] = None

class CheckoutSessionRequest(BaseModel):
    """Request to create Stripe Checkout session"""
    tier: str
    billing_cycle: str = "monthly"
    success_url: str
    cancel_url: str

# ============================================================================
# TIER TO PRICE MAPPING
# ============================================================================

def get_stripe_price_id(tier: str, billing_cycle: str) -> str:
    """
    Get Stripe Price ID for tier and billing cycle

    Args:
        tier: 'pro', 'workflow', 'enterprise'
        billing_cycle: 'monthly' or 'yearly'

    Returns:
        Stripe Price ID

    Raises:
        HTTPException if tier/cycle invalid
    """
    key = f"{tier}_{billing_cycle}"
    price_id = STRIPE_PRICE_IDS.get(key)

    if not price_id:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid tier '{tier}' or billing cycle '{billing_cycle}'"
        )

    return price_id

def get_tier_limits(tier: str) -> Dict[str, int]:
    """
    Get usage limits for tier

    Args:
        tier: 'free', 'pro', 'workflow', 'enterprise'

    Returns:
        Dict with requests_per_day, agents_allowed, prompts_allowed, workflows_allowed
    """
    limits = {
        "free": {
            "requests_per_day": 100,
            "agents_allowed": 3,
            "prompts_allowed": 10,
            "workflows_allowed": 0
        },
        "pro": {
            "requests_per_day": 10000,
            "agents_allowed": 14,
            "prompts_allowed": -1,  # Unlimited
            "workflows_allowed": 10
        },
        "workflow": {
            "requests_per_day": 20000,
            "agents_allowed": 14,
            "prompts_allowed": -1,
            "workflows_allowed": 100
        },
        "enterprise": {
            "requests_per_day": -1,  # Unlimited
            "agents_allowed": 14,
            "prompts_allowed": -1,
            "workflows_allowed": -1
        }
    }

    return limits.get(tier, limits["free"])

# ============================================================================
# CUSTOMER MANAGEMENT
# ============================================================================

async def get_or_create_stripe_customer(user_id: str, email: str) -> str:
    """
    Get existing Stripe customer or create new one

    Args:
        user_id: User UUID
        email: User email

    Returns:
        Stripe Customer ID
    """
    # Check if user already has Stripe customer ID
    customer_id = await Database.fetchval(
        "SELECT stripe_customer_id FROM users WHERE id = $1",
        user_id
    )

    if customer_id:
        return customer_id

    # Create new Stripe customer
    try:
        customer = stripe.Customer.create(
            email=email,
            metadata={"user_id": user_id}
        )

        # Store customer ID
        await Database.execute(
            "UPDATE users SET stripe_customer_id = $1 WHERE id = $2",
            customer.id,
            user_id
        )

        return customer.id

    except stripe.error.StripeError as e:
        raise HTTPException(status_code=500, detail=f"Stripe error: {str(e)}")

# ============================================================================
# SUBSCRIPTION MANAGEMENT
# ============================================================================

async def create_subscription(
    user_id: str,
    email: str,
    tier: str,
    billing_cycle: str = "monthly",
    payment_method_id: Optional[str] = None
) -> SubscriptionResponse:
    """
    Create Stripe subscription for user

    Args:
        user_id: User UUID
        email: User email
        tier: 'pro', 'workflow', 'enterprise'
        billing_cycle: 'monthly' or 'yearly'
        payment_method_id: Stripe PaymentMethod ID (optional, needed for direct subscription)

    Returns:
        Subscription response

    Raises:
        HTTPException on error
    """
    # Validate tier
    if tier not in ["pro", "workflow", "enterprise"]:
        raise HTTPException(status_code=400, detail="Invalid tier. Must be 'pro', 'workflow', or 'enterprise'")

    # Get or create Stripe customer
    customer_id = await get_or_create_stripe_customer(user_id, email)

    # Get price ID
    price_id = get_stripe_price_id(tier, billing_cycle)

    try:
        # Create subscription
        subscription = stripe.Subscription.create(
            customer=customer_id,
            items=[{"price": price_id}],
            payment_behavior="default_incomplete" if not payment_method_id else "allow_incomplete",
            default_payment_method=payment_method_id,
            expand=["latest_invoice.payment_intent"],
            metadata={
                "user_id": user_id,
                "tier": tier
            }
        )

        # Update user in database
        limits = get_tier_limits(tier)
        await Database.execute(
            """
            UPDATE users
            SET tier = $1,
                stripe_subscription_id = $2,
                subscription_status = $3,
                requests_per_day = $4,
                agents_allowed = $5,
                prompts_allowed = $6,
                trial_ends_at = $7
            WHERE id = $8
            """,
            tier,
            subscription.id,
            subscription.status,
            limits["requests_per_day"],
            limits["agents_allowed"],
            limits["prompts_allowed"],
            datetime.fromtimestamp(subscription.current_period_end) if subscription.current_period_end else None,
            user_id
        )

        return SubscriptionResponse(
            subscription_id=subscription.id,
            customer_id=customer_id,
            status=subscription.status,
            tier=tier,
            current_period_end=datetime.fromtimestamp(subscription.current_period_end),
            cancel_at_period_end=subscription.cancel_at_period_end
        )

    except stripe.error.StripeError as e:
        raise HTTPException(status_code=500, detail=f"Stripe error: {str(e)}")

async def cancel_subscription(user_id: str, immediate: bool = False) -> Dict[str, Any]:
    """
    Cancel user's subscription

    Args:
        user_id: User UUID
        immediate: If True, cancel immediately. If False, cancel at period end.

    Returns:
        Cancellation details

    Raises:
        HTTPException if no active subscription
    """
    # Get subscription ID
    subscription_id = await Database.fetchval(
        "SELECT stripe_subscription_id FROM users WHERE id = $1",
        user_id
    )

    if not subscription_id:
        raise HTTPException(status_code=404, detail="No active subscription found")

    try:
        if immediate:
            # Cancel immediately
            subscription = stripe.Subscription.delete(subscription_id)

            # Downgrade to free tier immediately
            free_limits = get_tier_limits("free")
            await Database.execute(
                """
                UPDATE users
                SET tier = 'free',
                    subscription_status = 'canceled',
                    stripe_subscription_id = NULL,
                    requests_per_day = $1,
                    agents_allowed = $2,
                    prompts_allowed = $3
                WHERE id = $4
                """,
                free_limits["requests_per_day"],
                free_limits["agents_allowed"],
                free_limits["prompts_allowed"],
                user_id
            )

            return {
                "status": "canceled",
                "canceled_at": datetime.utcnow(),
                "tier": "free",
                "message": "Subscription canceled immediately. Downgraded to free tier."
            }
        else:
            # Cancel at period end
            subscription = stripe.Subscription.modify(
                subscription_id,
                cancel_at_period_end=True
            )

            await Database.execute(
                "UPDATE users SET subscription_status = 'canceling' WHERE id = $1",
                user_id
            )

            return {
                "status": "canceling",
                "cancel_at": datetime.fromtimestamp(subscription.current_period_end),
                "message": f"Subscription will be canceled on {datetime.fromtimestamp(subscription.current_period_end).strftime('%Y-%m-%d')}"
            }

    except stripe.error.StripeError as e:
        raise HTTPException(status_code=500, detail=f"Stripe error: {str(e)}")

async def update_subscription(
    user_id: str,
    new_tier: Optional[str] = None,
    new_billing_cycle: Optional[str] = None
) -> SubscriptionResponse:
    """
    Update subscription tier or billing cycle

    Args:
        user_id: User UUID
        new_tier: New tier ('pro', 'workflow', 'enterprise') or None
        new_billing_cycle: New billing cycle ('monthly', 'yearly') or None

    Returns:
        Updated subscription

    Raises:
        HTTPException on error
    """
    # Get current subscription
    row = await Database.fetchrow(
        "SELECT stripe_subscription_id, tier FROM users WHERE id = $1",
        user_id
    )

    if not row or not row["stripe_subscription_id"]:
        raise HTTPException(status_code=404, detail="No active subscription found")

    subscription_id = row["stripe_subscription_id"]
    current_tier = row["tier"]

    try:
        # Get current subscription from Stripe
        subscription = stripe.Subscription.retrieve(subscription_id)

        # Determine new price
        tier_to_use = new_tier if new_tier else current_tier

        # Get current billing cycle from Stripe price
        current_price = subscription["items"]["data"][0]["price"]
        current_billing_cycle = "yearly" if current_price["recurring"]["interval"] == "year" else "monthly"
        billing_cycle_to_use = new_billing_cycle if new_billing_cycle else current_billing_cycle

        new_price_id = get_stripe_price_id(tier_to_use, billing_cycle_to_use)

        # Update subscription
        updated_subscription = stripe.Subscription.modify(
            subscription_id,
            items=[{
                "id": subscription["items"]["data"][0].id,
                "price": new_price_id,
            }],
            proration_behavior="always_invoice",  # Prorate the difference
            metadata={"tier": tier_to_use}
        )

        # Update database
        limits = get_tier_limits(tier_to_use)
        await Database.execute(
            """
            UPDATE users
            SET tier = $1,
                subscription_status = $2,
                requests_per_day = $3,
                agents_allowed = $4,
                prompts_allowed = $5
            WHERE id = $6
            """,
            tier_to_use,
            updated_subscription.status,
            limits["requests_per_day"],
            limits["agents_allowed"],
            limits["prompts_allowed"],
            user_id
        )

        return SubscriptionResponse(
            subscription_id=updated_subscription.id,
            customer_id=updated_subscription.customer,
            status=updated_subscription.status,
            tier=tier_to_use,
            current_period_end=datetime.fromtimestamp(updated_subscription.current_period_end),
            cancel_at_period_end=updated_subscription.cancel_at_period_end
        )

    except stripe.error.StripeError as e:
        raise HTTPException(status_code=500, detail=f"Stripe error: {str(e)}")

# ============================================================================
# STRIPE CHECKOUT
# ============================================================================

async def create_checkout_session(
    user_id: str,
    email: str,
    tier: str,
    billing_cycle: str,
    success_url: str,
    cancel_url: str
) -> Dict[str, str]:
    """
    Create Stripe Checkout session for subscription

    Args:
        user_id: User UUID
        email: User email
        tier: 'pro', 'workflow', 'enterprise'
        billing_cycle: 'monthly' or 'yearly'
        success_url: URL to redirect after successful payment
        cancel_url: URL to redirect if user cancels

    Returns:
        Dict with checkout_url and session_id
    """
    # Get or create customer
    customer_id = await get_or_create_stripe_customer(user_id, email)

    # Get price ID
    price_id = get_stripe_price_id(tier, billing_cycle)

    try:
        # Create checkout session
        session = stripe.checkout.Session.create(
            customer=customer_id,
            payment_method_types=["card"],
            line_items=[{
                "price": price_id,
                "quantity": 1,
            }],
            mode="subscription",
            success_url=success_url + "?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=cancel_url,
            metadata={
                "user_id": user_id,
                "tier": tier
            },
            subscription_data={
                "metadata": {
                    "user_id": user_id,
                    "tier": tier
                }
            }
        )

        return {
            "checkout_url": session.url,
            "session_id": session.id
        }

    except stripe.error.StripeError as e:
        raise HTTPException(status_code=500, detail=f"Stripe error: {str(e)}")

# ============================================================================
# WEBHOOK HANDLING
# ============================================================================

def verify_webhook_signature(payload: bytes, signature: str) -> bool:
    """
    Verify Stripe webhook signature

    Args:
        payload: Raw request body
        signature: Stripe-Signature header value

    Returns:
        True if valid, False otherwise
    """
    if not STRIPE_WEBHOOK_SECRET:
        return False

    try:
        stripe.Webhook.construct_event(
            payload,
            signature,
            STRIPE_WEBHOOK_SECRET
        )
        return True
    except Exception:
        return False

async def handle_webhook_event(event: Dict[str, Any]):
    """
    Handle Stripe webhook events

    Args:
        event: Stripe event object

    Supported events:
    - customer.subscription.created
    - customer.subscription.updated
    - customer.subscription.deleted
    - invoice.payment_succeeded
    - invoice.payment_failed
    """
    event_type = event["type"]
    data = event["data"]["object"]

    # Subscription created
    if event_type == "customer.subscription.created":
        await handle_subscription_created(data)

    # Subscription updated
    elif event_type == "customer.subscription.updated":
        await handle_subscription_updated(data)

    # Subscription deleted (canceled)
    elif event_type == "customer.subscription.deleted":
        await handle_subscription_deleted(data)

    # Payment succeeded
    elif event_type == "invoice.payment_succeeded":
        await handle_payment_succeeded(data)

    # Payment failed
    elif event_type == "invoice.payment_failed":
        await handle_payment_failed(data)

async def handle_subscription_created(subscription: Dict[str, Any]):
    """Handle subscription.created event"""
    user_id = subscription["metadata"].get("user_id")
    tier = subscription["metadata"].get("tier", "pro")

    if not user_id:
        return

    limits = get_tier_limits(tier)

    await Database.execute(
        """
        UPDATE users
        SET tier = $1,
            stripe_subscription_id = $2,
            subscription_status = $3,
            requests_per_day = $4,
            agents_allowed = $5,
            prompts_allowed = $6
        WHERE id = $7
        """,
        tier,
        subscription["id"],
        subscription["status"],
        limits["requests_per_day"],
        limits["agents_allowed"],
        limits["prompts_allowed"],
        user_id
    )

async def handle_subscription_updated(subscription: Dict[str, Any]):
    """Handle subscription.updated event"""
    user_id = subscription["metadata"].get("user_id")

    if not user_id:
        # Try to find user by subscription ID
        user_id = await Database.fetchval(
            "SELECT id FROM users WHERE stripe_subscription_id = $1",
            subscription["id"]
        )

    if not user_id:
        return

    tier = subscription["metadata"].get("tier", "pro")
    limits = get_tier_limits(tier)

    await Database.execute(
        """
        UPDATE users
        SET tier = $1,
            subscription_status = $2,
            requests_per_day = $3,
            agents_allowed = $4,
            prompts_allowed = $5
        WHERE id = $6
        """,
        tier,
        subscription["status"],
        limits["requests_per_day"],
        limits["agents_allowed"],
        limits["prompts_allowed"],
        user_id
    )

async def handle_subscription_deleted(subscription: Dict[str, Any]):
    """Handle subscription.deleted event"""
    user_id = subscription["metadata"].get("user_id")

    if not user_id:
        user_id = await Database.fetchval(
            "SELECT id FROM users WHERE stripe_subscription_id = $1",
            subscription["id"]
        )

    if not user_id:
        return

    # Downgrade to free tier
    free_limits = get_tier_limits("free")

    await Database.execute(
        """
        UPDATE users
        SET tier = 'free',
            subscription_status = 'canceled',
            stripe_subscription_id = NULL,
            requests_per_day = $1,
            agents_allowed = $2,
            prompts_allowed = $3
        WHERE id = $4
        """,
        free_limits["requests_per_day"],
        free_limits["agents_allowed"],
        free_limits["prompts_allowed"],
        user_id
    )

async def handle_payment_succeeded(invoice: Dict[str, Any]):
    """Handle invoice.payment_succeeded event"""
    customer_id = invoice["customer"]
    amount = invoice["amount_paid"] / 100  # Convert cents to dollars

    # Find user
    user_id = await Database.fetchval(
        "SELECT id FROM users WHERE stripe_customer_id = $1",
        customer_id
    )

    if not user_id:
        return

    # Record payment
    await Database.execute(
        """
        INSERT INTO payments (
            user_id, stripe_payment_id, stripe_invoice_id,
            amount_usd, status, description
        ) VALUES ($1, $2, $3, $4, 'succeeded', $5)
        """,
        user_id,
        invoice.get("payment_intent"),
        invoice["id"],
        amount,
        f"Subscription payment - Invoice {invoice['number']}"
    )

    # Ensure subscription is active
    await Database.execute(
        "UPDATE users SET subscription_status = 'active' WHERE id = $1",
        user_id
    )

async def handle_payment_failed(invoice: Dict[str, Any]):
    """Handle invoice.payment_failed event"""
    customer_id = invoice["customer"]

    # Find user
    user_id = await Database.fetchval(
        "SELECT id FROM users WHERE stripe_customer_id = $1",
        customer_id
    )

    if not user_id:
        return

    # Update subscription status
    await Database.execute(
        "UPDATE users SET subscription_status = 'past_due' WHERE id = $1",
        user_id
    )

    # Record failed payment
    await Database.execute(
        """
        INSERT INTO payments (
            user_id, stripe_invoice_id, amount_usd, status, description
        ) VALUES ($1, $2, $3, 'failed', $4)
        """,
        user_id,
        invoice["id"],
        invoice["amount_due"] / 100,
        f"Payment failed - Invoice {invoice['number']}"
    )

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

async def get_subscription_info(user_id: str) -> Optional[Dict[str, Any]]:
    """
    Get user's subscription info from Stripe

    Args:
        user_id: User UUID

    Returns:
        Subscription info dict or None if no subscription
    """
    subscription_id = await Database.fetchval(
        "SELECT stripe_subscription_id FROM users WHERE id = $1",
        user_id
    )

    if not subscription_id:
        return None

    try:
        subscription = stripe.Subscription.retrieve(subscription_id)

        return {
            "id": subscription.id,
            "status": subscription.status,
            "current_period_start": datetime.fromtimestamp(subscription.current_period_start),
            "current_period_end": datetime.fromtimestamp(subscription.current_period_end),
            "cancel_at_period_end": subscription.cancel_at_period_end,
            "canceled_at": datetime.fromtimestamp(subscription.canceled_at) if subscription.canceled_at else None,
        }

    except stripe.error.StripeError:
        return None

async def get_payment_history(user_id: str, limit: int = 10) -> List[Dict[str, Any]]:
    """
    Get user's payment history

    Args:
        user_id: User UUID
        limit: Number of payments to return

    Returns:
        List of payment dicts
    """
    payments = await Database.fetch(
        """
        SELECT stripe_payment_id, stripe_invoice_id, amount_usd,
               currency, status, description, created_at
        FROM payments
        WHERE user_id = $1
        ORDER BY created_at DESC
        LIMIT $2
        """,
        user_id,
        limit
    )

    return [dict(payment) for payment in payments]
