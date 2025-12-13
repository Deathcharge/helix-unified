"""
🌀 Helix Collective v17.1 - SaaS Stripe Integration & Billing
backend/saas/stripe_service.py

Complete Stripe integration for 5-tier monetization:
- Subscription management (FREE, PRO, ENTERPRISE)
- Usage-based billing (consumption tracking)
- Webhook handling (subscription events)
- Invoice generation
- Customer portal

Author: Claude (Automation)
Version: 17.1.0
"""

import json
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import stripe

logger = logging.getLogger(__name__)

# Configure Stripe
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")

# ============================================================================
# SUBSCRIPTION TIERS
# ============================================================================

SUBSCRIPTION_TIERS = {
    "free": {
        "name": "Free",
        "price_id": None,  # No Stripe product
        "monthly_price": 0,
        "annual_price": 0,
        "trial_days": 0,
        "features": {
            "systems_monitored": 1,
            "metrics_history_days": 7,
            "alerts": False,
            "api_calls_per_month": 1000,
            "export_formats": ["json"],
        },
    },
    "hobby": {
        "name": "Hobby",
        "price_id": os.getenv("STRIPE_PRICE_HOBBY"),
        "annual_price_id": os.getenv("STRIPE_PRICE_HOBBY_ANNUAL"),
        "monthly_price": 10,
        "annual_price": 90,  # 25% off = 9 months pricing
        "trial_days": 14,  # 14-day free trial
        "features": {
            "systems_monitored": 3,
            "metrics_history_days": 14,
            "alerts": True,
            "api_calls_per_month": 10000,
            "export_formats": ["json", "csv"],
        },
    },
    "starter": {
        "name": "Starter",
        "price_id": os.getenv("STRIPE_PRICE_STARTER"),
        "annual_price_id": os.getenv("STRIPE_PRICE_STARTER_ANNUAL"),
        "monthly_price": 29,
        "annual_price": 261,  # 25% off = 9 months pricing ($29 * 9)
        "trial_days": 14,
        "features": {
            "systems_monitored": 5,
            "metrics_history_days": 30,
            "alerts": True,
            "api_calls_per_month": 50000,
            "export_formats": ["json", "csv", "pdf"],
        },
    },
    "pro": {
        "name": "Pro",
        "price_id": os.getenv("STRIPE_PRICE_PRO"),
        "annual_price_id": os.getenv("STRIPE_PRICE_PRO_ANNUAL"),
        "monthly_price": 79,  # Lowered from $99
        "annual_price": 711,  # 25% off = 9 months pricing ($79 * 9)
        "trial_days": 14,
        "features": {
            "systems_monitored": 20,  # Increased from 10
            "metrics_history_days": 90,  # Increased from 30
            "alerts": True,
            "api_calls_per_month": 200000,  # Increased from 100k
            "export_formats": ["json", "csv", "pdf"],
            "custom_integrations": True,
        },
    },
    "enterprise": {
        "name": "Enterprise",
        "price_id": os.getenv("STRIPE_PRICE_ENTERPRISE"),
        "annual_price_id": os.getenv("STRIPE_PRICE_ENTERPRISE_ANNUAL"),
        "monthly_price": 299,  # Lowered from $499
        "annual_price": 2691,  # 25% off = 9 months pricing ($299 * 9)
        "trial_days": 14,
        "features": {
            "systems_monitored": 999,
            "metrics_history_days": 365,
            "alerts": True,
            "api_calls_per_month": 10000000,
            "export_formats": ["json", "csv", "pdf", "xml"],
            "custom_integrations": True,
            "white_label": True,
            "dedicated_support": True,
        },
    },
}

# ============================================================================
# PROMOTIONAL CODES
# ============================================================================

PROMO_CODES = {
    "FIRSTMONTH50": {
        "name": "50% Off First Month",
        "percent_off": 50,
        "duration": "once",  # Apply once to first invoice
        "active": True,
    },
    "LAUNCH2025": {
        "name": "Launch Special - 50% Off First Month",
        "percent_off": 50,
        "duration": "once",
        "active": True,
    },
    "ANNUAL25": {
        "name": "25% Off Annual Plans",
        "percent_off": 25,
        "duration": "forever",  # Built into annual pricing
        "active": True,
    },
}

# ============================================================================
# STRIPE SERVICE
# ============================================================================


class StripeService:
    """Manages Stripe billing integration."""

    def __init__(self):
        self.webhook_secret = STRIPE_WEBHOOK_SECRET
        self.tiers = SUBSCRIPTION_TIERS
        self.customer_file = Path("Helix/state/stripe_customers.json")
        self.customer_file.parent.mkdir(parents=True, exist_ok=True)

    # ========================================================================
    # CUSTOMER MANAGEMENT
    # ========================================================================

    async def create_customer(self, user_id: str, email: str, name: str, metadata: Dict[str, str]) -> Dict[str, Any]:
        """Create Stripe customer."""
        try:
            customer = stripe.Customer.create(
                email=email,
                name=name,
                metadata={"user_id": user_id, **metadata},
            )

            # Store locally
            self._save_customer(user_id, customer.id)

            logger.info(f"✅ Created Stripe customer: {customer.id}")
            return {
                "status": "success",
                "customer_id": customer.id,
                "email": customer.email,
            }

        except stripe.error.StripeError as e:
            logger.error(f"❌ Stripe error: {e}")
            return {"status": "error", "error": "Failed to create customer. Please try again later."}

    async def get_customer(self, user_id: str) -> Optional[str]:
        """Get Stripe customer ID for user."""
        customers = self._load_customers()
        return customers.get(user_id)

    def _save_customer(self, user_id: str, stripe_customer_id: str) -> None:
        """Save customer mapping locally."""
        customers = self._load_customers()
        customers[user_id] = stripe_customer_id
        with open(self.customer_file, "w") as f:
            json.dump(customers, f)

    def _load_customers(self) -> Dict[str, str]:
        """Load customer mappings."""
        if not self.customer_file.exists():
            return {}
        with open(self.customer_file, "r") as f:
            return json.load(f)

    # ========================================================================
    # SUBSCRIPTION MANAGEMENT
    # ========================================================================

    async def create_subscription(self, user_id: str, stripe_customer_id: str, tier: str, billing_cycle: str = "monthly") -> Dict[str, Any]:
        """Create subscription for user with trial period."""
        tier_config = self.tiers.get(tier)
        if not tier_config:
            return {"status": "error", "error": f"Invalid tier: {tier}"}

        # Free tier: no Stripe subscription needed
        if tier == "free":
            return {"status": "success", "tier": "free", "subscription_id": None}

        try:
            # Choose price ID based on billing cycle
            price_id = tier_config["annual_price_id"] if billing_cycle == "annual" else tier_config["price_id"]
            trial_days = tier_config.get("trial_days", 0)

            subscription_params = {
                "customer": stripe_customer_id,
                "items": [{"price": price_id}],
                "metadata": {"user_id": user_id, "tier": tier, "billing_cycle": billing_cycle},
            }

            # Add trial period if configured
            if trial_days > 0:
                subscription_params["trial_period_days"] = trial_days

            subscription = stripe.Subscription.create(**subscription_params)

            logger.info(f"✅ Created subscription: {subscription.id}")
            return {
                "status": "success",  # noqa
                "subscription_id": subscription.id,
                "tier": tier,
                "billing_cycle": billing_cycle,
                "trial_days": trial_days,
                "status": subscription.status,  # noqa
                "current_period_end": subscription.current_period_end,  # noqa
                "trial_end": subscription.trial_end if trial_days > 0 else None,  # noqa
            }

        except stripe.error.StripeError as e:  # noqa
            logger.error(f"❌ Subscription error: {e}")
            # Return a generic error message, not the raw exception text
            return {"status": "error", "error": "Unable to create subscription at this time."}

    async def cancel_subscription(self, subscription_id: str) -> Dict[str, Any]:
        """Cancel subscription."""
        try:
            subscription = stripe.Subscription.delete(subscription_id)
            logger.info(f"✅ Cancelled subscription: {subscription_id}")
            return {
                "status": "success",
                "subscription_id": subscription.id,
                "canceled_at": subscription.canceled_at,
            }

        except stripe.error.StripeError as e:
            logger.error(f"❌ Cancellation error: {e}")
            return {"status": "error", "error": str(e)}

    async def get_subscription_status(self, subscription_id: str) -> Dict[str, Any]:
        """Get subscription status."""
        try:
            subscription = stripe.Subscription.retrieve(subscription_id)
            return {
                "status": "success",  # noqa
                "subscription_id": subscription.id,
                "status": subscription.status,  # noqa
                "tier": subscription.metadata.get("tier"),
                "current_period_end": subscription.current_period_end,  # noqa
                "cancel_at_period_end": subscription.cancel_at_period_end,
            }  # noqa

        except stripe.error.StripeError as e:
            logger.error(f"❌ Retrieval error: {e}")
            return {"status": "error", "error": str(e)}

    async def get_user_subscription(self, user_id: str) -> Dict[str, Any]:
        """Get subscription info for a user."""
        try:
            # Get customer ID from local storage
            customer_id = await self.get_customer(user_id)
            if not customer_id:
                # User has no customer = free tier
                return {
                    "status": "success",
                    "tier": "free",
                    "subscription_id": None,
                    "user_id": user_id,
                }

            # List active subscriptions for customer
            subscriptions = stripe.Subscription.list(
                customer=customer_id,
                status="active",
                limit=1,
            )

            if not subscriptions.data:
                # Customer exists but no active subscription = free tier
                return {
                    "status": "success",
                    "tier": "free",
                    "subscription_id": None,
                    "user_id": user_id,
                }

            # Return active subscription details
            sub = subscriptions.data[0]
            tier = sub.metadata.get("tier", "free")
            return {
                "status": "success",
                "tier": tier,
                "subscription_id": sub.id,
                "subscription_status": sub.status,
                "current_period_end": sub.current_period_end,
                "cancel_at_period_end": sub.cancel_at_period_end,
                "user_id": user_id,
            }

        except stripe.error.StripeError as e:
            logger.error(f"❌ Get user subscription error: {e}")
            return {"status": "error", "error": "Unable to retrieve subscription details."}

    # ========================================================================
    # USAGE-BASED BILLING
    # ========================================================================

    async def record_usage(self, subscription_id: str, quantity: int, metric_name: str = "api_calls") -> Dict[str, Any]:
        """Record usage for metered billing."""
        try:
            # Get subscription to find usage record ID
            subscription = stripe.Subscription.retrieve(subscription_id)

            for item in subscription.items.data:
                if item.billing_thresholds:
                    # Record usage
                    stripe.SubscriptionItem.create_usage_record(
                        item.id, quantity=quantity, timestamp=int(datetime.utcnow().timestamp())
                    )

            logger.info(f"✅ Recorded usage: {quantity} {metric_name}")
            return {"status": "success", "quantity": quantity}

        except stripe.error.StripeError as e:
            logger.error(f"❌ Usage recording error: {e}")
            return {"status": "error", "error": str(e)}

    # ========================================================================
    # INVOICE & PAYMENT
    # ========================================================================

    async def get_invoices(self, customer_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Get customer invoices."""
        try:
            invoices = stripe.Invoice.list(customer=customer_id, limit=limit)
            return [
                {
                    "id": inv.id,
                    "amount": inv.amount_paid / 100,  # Convert cents to dollars
                    "date": datetime.fromtimestamp(inv.created).isoformat(),
                    "status": inv.status,
                    "pdf": inv.invoice_pdf,
                }
                for inv in invoices.data
            ]

        except stripe.error.StripeError as e:
            logger.error(f"❌ Invoice retrieval error: {e}")
            return []

    async def create_invoice(self, customer_id: str, amount: int, description: str) -> Dict[str, Any]:
        """Create one-time invoice."""
        try:
            invoice = stripe.Invoice.create(
                customer=customer_id,
                collection_method="send_invoice",
                days_until_due=30,
            )

            # Add line item
            stripe.InvoiceItem.create(
                customer=customer_id,
                amount=amount,
                currency="usd",
                description=description,
                invoice=invoice.id,
            )

            # Finalize and send
            invoice = stripe.Invoice.finalize_invoice(invoice.id)
            stripe.Invoice.send_invoice(invoice.id)

            logger.info(f"✅ Created invoice: {invoice.id}")
            return {
                "status": "success",
                "invoice_id": invoice.id,
                "amount": amount / 100,
                "pdf": invoice.invoice_pdf,
            }

        except stripe.error.StripeError as e:
            logger.error(f"❌ Invoice creation error: {e}")
            return {"status": "error", "error": str(e)}

    # ========================================================================
    # WEBHOOK HANDLING
    # ========================================================================

    def verify_webhook_signature(self, request_body: str, signature: str) -> Optional[Dict]:
        """Verify and parse Stripe webhook."""
        try:
            event = stripe.Webhook.construct_event(request_body, signature, self.webhook_secret)
            return event
        except ValueError:
            logger.error("Invalid webhook payload")
            return None
        except stripe.error.SignatureVerificationError:
            logger.error("Invalid webhook signature")
            return None

    async def handle_webhook(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """Handle Stripe webhook events."""
        event_type = event["type"]

        try:
            if event_type == "customer.subscription.created":
                logger.info(f"✅ Subscription created: {event['data']['object']['id']}")

            elif event_type == "customer.subscription.updated":
                logger.info(f"✅ Subscription updated: {event['data']['object']['id']}")

            elif event_type == "customer.subscription.deleted":
                logger.warning(f"⚠️ Subscription cancelled: {event['data']['object']['id']}")

            elif event_type == "invoice.paid":
                logger.info(f"✅ Invoice paid: {event['data']['object']['id']}")

            elif event_type == "invoice.payment_failed":
                logger.error(f"❌ Payment failed: {event['data']['object']['id']}")

            elif event_type == "charge.dispute.created":
                logger.error(f"❌ Dispute created: {event['data']['object']['id']}")

            return {"status": "success", "event_type": event_type}

        except Exception as e:
            logger.error(f"❌ Webhook handling error: {e}")
            return {"status": "error", "error": str(e)}

    # ========================================================================
    # BILLING PORTAL
    # ========================================================================

    async def create_portal_session(self, customer_id: str) -> Dict[str, Any]:
        """Create Stripe customer portal session."""
        try:
            session = stripe.BillingPortal.Session.create(
                customer=customer_id,
                return_url="https://helixspiral.work/dashboard",
            )

            logger.info(f"✅ Portal session created: {session.id}")
            return {"status": "success", "portal_url": session.url}

        except stripe.error.StripeError as e:
            logger.error(f"❌ Portal session error: {e}")
            return {"status": "error", "error": str(e)}

    # ========================================================================
    # CHECKOUT SESSION
    # ========================================================================

    async def create_checkout_session(
        self,
        customer_id: str,
        tier: str,
        success_url: str,
        cancel_url: str,
        billing_cycle: str = "monthly",
        promo_code: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create Stripe checkout session for subscription with trial & promo codes."""
        tier_config = self.tiers.get(tier)
        if not tier_config:
            return {"status": "error", "error": f"Invalid tier: {tier}"}

        if tier == "free":
            return {"status": "error", "error": "Cannot checkout for free tier"}

        try:
            # Choose price based on billing cycle
            price_id = tier_config["annual_price_id"] if billing_cycle == "annual" else tier_config["price_id"]
            trial_days = tier_config.get("trial_days", 0)

            session_params = {
                "customer": customer_id,
                "payment_method_types": ["card"],
                "mode": "subscription",
                "line_items": [{"price": price_id, "quantity": 1}],
                "success_url": success_url,
                "cancel_url": cancel_url,
                "subscription_data": {
                    "metadata": {"tier": tier, "billing_cycle": billing_cycle},
                },
            }

            # Add trial period
            if trial_days > 0:
                session_params["subscription_data"]["trial_period_days"] = trial_days

            # Add promotional code if provided and valid
            if promo_code and promo_code in PROMO_CODES:
                promo = PROMO_CODES[promo_code]
                if promo["active"]:
                    session_params["discounts"] = [{"coupon": promo_code}]
                    logger.info(f"✅ Applied promo code: {promo_code}")

            session = stripe.checkout.Session.create(**session_params)

            logger.info(f"✅ Checkout session created: {session.id}")
            return {
                "status": "success",
                "checkout_url": session.url,
                "trial_days": trial_days,
                "billing_cycle": billing_cycle,
                "promo_applied": promo_code if promo_code and promo_code in PROMO_CODES else None,
            }

        except stripe.error.StripeError as e:
            logger.error(f"❌ Checkout error: {e}")
            return {"status": "error", "error": "Unable to create checkout session."}


# ============================================================================
# SINGLETON
# ============================================================================

_stripe_service: Optional[StripeService] = None


async def get_stripe_service() -> StripeService:
    """Get or create Stripe service."""
    global _stripe_service
    if _stripe_service is None:
        _stripe_service = StripeService()
    return _stripe_service


# ============================================================================
# FASTAPI ROUTER
# ============================================================================

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel

router = APIRouter()

# Request/Response models
class CreateCustomerRequest(BaseModel):
    email: str
    name: str
    metadata: dict = {}

class CreateSubscriptionRequest(BaseModel):
    user_id: str
    tier: str

class CheckoutRequest(BaseModel):
    tier: str
    success_url: str = "http://localhost:3000/dashboard?success=true"
    cancel_url: str = "http://localhost:3000/pricing?canceled=true"

@router.post("/create-customer")
async def create_customer_endpoint(
    req: CreateCustomerRequest,
    service: StripeService = Depends(get_stripe_service)
):
    """Create Stripe customer"""
    user_id = f"user_{datetime.now().timestamp()}"
    result = await service.create_customer(user_id, req.email, req.name, req.metadata)
    if result.get("status") == "error":
        raise HTTPException(status_code=400, detail=result.get("error"))
    return result

@router.post("/create-subscription")
async def create_subscription_endpoint(
    req: CreateSubscriptionRequest,
    service: StripeService = Depends(get_stripe_service)
):
    """Create subscription"""
    customer_id = await service.get_customer(req.user_id)
    if not customer_id:
        raise HTTPException(status_code=404, detail="Customer not found")

    result = await service.create_subscription(req.user_id, customer_id, req.tier)
    if result.get("status") == "error":
        raise HTTPException(status_code=400, detail=result.get("error"))
    return result

@router.get("/subscription/{user_id}")
async def get_subscription_endpoint(
    user_id: str,
    service: StripeService = Depends(get_stripe_service)
):
    """Get subscription info"""
    result = await service.get_user_subscription(user_id)
    if result.get("status") == "error":
        raise HTTPException(status_code=400, detail=result.get("error"))
    return result

@router.post("/create-checkout-session")
async def create_checkout_session_endpoint(
    req: CheckoutRequest,
    service: StripeService = Depends(get_stripe_service)
):
    """Create Stripe checkout session"""
    user_id = f"user_{datetime.now().timestamp()}"  # TODO: Get from auth
    result = await service.create_checkout_session(
        user_id, req.tier, req.success_url, req.cancel_url
    )
    if result.get("status") == "error":
        raise HTTPException(status_code=400, detail=result.get("error"))
    return result

@router.post("/webhook")
async def stripe_webhook(request: Request):
    """Handle Stripe webhooks"""
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, STRIPE_WEBHOOK_SECRET
        )

        # Handle different event types
        if event.type == "customer.subscription.created":
            logger.info(f"✅ Subscription created: {event.data.object.id}")
        elif event.type == "customer.subscription.updated":
            logger.info(f"✅ Subscription updated: {event.data.object.id}")
        elif event.type == "invoice.paid":
            logger.info(f"✅ Invoice paid: {event.data.object.id}")
        elif event.type == "customer.subscription.deleted":
            logger.info(f"✅ Subscription cancelled: {event.data.object.id}")

        return {"received": True}
    except Exception as e:
        logger.error(f"❌ Webhook error: {e}")
        raise HTTPException(status_code=400, detail=str(e))

# ============================================================================
# EXPORTS
# ============================================================================

__all__ = ["StripeService", "SUBSCRIPTION_TIERS", "get_stripe_service", "router"]
