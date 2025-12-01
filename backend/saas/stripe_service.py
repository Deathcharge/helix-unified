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
from datetime import datetime, timedelta
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
        "features": {
            "systems_monitored": 1,
            "metrics_history_days": 7,
            "alerts": False,
            "api_calls_per_month": 1000,
            "export_formats": ["json"],
        },
    },
    "pro": {
        "name": "Pro",
        "price_id": os.getenv("STRIPE_PRICE_PRO"),  # Set in .env
        "monthly_price": 99,
        "features": {
            "systems_monitored": 10,
            "metrics_history_days": 30,
            "alerts": True,
            "api_calls_per_month": 100000,
            "export_formats": ["json", "csv", "pdf"],
        },
    },
    "enterprise": {
        "name": "Enterprise",
        "price_id": os.getenv("STRIPE_PRICE_ENTERPRISE"),
        "monthly_price": 499,
        "features": {
            "systems_monitored": 999,
            "metrics_history_days": 365,
            "alerts": True,
            "api_calls_per_month": 10000000,
            "export_formats": ["json", "csv", "pdf", "xml"],
        },
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

    async def create_customer(
        self, user_id: str, email: str, name: str, metadata: Dict[str, str]
    ) -> Dict[str, Any]:
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
            return {"status": "error", "error": str(e)}

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

    async def create_subscription(
        self, user_id: str, stripe_customer_id: str, tier: str
    ) -> Dict[str, Any]:
        """Create subscription for user."""
        tier_config = self.tiers.get(tier)
        if not tier_config:
            return {"status": "error", "error": f"Invalid tier: {tier}"}

        # Free tier: no Stripe subscription needed
        if tier == "free":
            return {"status": "success", "tier": "free", "subscription_id": None}

        try:
            subscription = stripe.Subscription.create(
                customer=stripe_customer_id,
                items=[{"price": tier_config["price_id"]}],
                metadata={"user_id": user_id, "tier": tier},
            )

            logger.info(f"✅ Created subscription: {subscription.id} ({tier})")
            return {
                "status": "success",
                "subscription_id": subscription.id,
                "tier": tier,
                "status": subscription.status,
                "current_period_end": subscription.current_period_end,
            }

        except stripe.error.StripeError as e:
            logger.error(f"❌ Subscription error: {e}")
            return {"status": "error", "error": str(e)}

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
                "status": "success",
                "subscription_id": subscription.id,
                "status": subscription.status,
                "tier": subscription.metadata.get("tier"),
                "current_period_end": subscription.current_period_end,
                "cancel_at_period_end": subscription.cancel_at_period_end,
            }

        except stripe.error.StripeError as e:
            logger.error(f"❌ Retrieval error: {e}")
            return {"status": "error", "error": str(e)}

    # ========================================================================
    # USAGE-BASED BILLING
    # ========================================================================

    async def record_usage(
        self, subscription_id: str, quantity: int, metric_name: str = "api_calls"
    ) -> Dict[str, Any]:
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

    async def create_invoice(
        self, customer_id: str, amount: int, description: str
    ) -> Dict[str, Any]:
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
            event = stripe.Webhook.construct_event(
                request_body, signature, self.webhook_secret
            )
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
        self, customer_id: str, tier: str, success_url: str, cancel_url: str
    ) -> Dict[str, Any]:
        """Create Stripe checkout session for subscription."""
        tier_config = self.tiers.get(tier)
        if not tier_config:
            return {"status": "error", "error": f"Invalid tier: {tier}"}

        if tier == "free":
            return {"status": "error", "error": "Cannot checkout for free tier"}

        try:
            session = stripe.checkout.Session.create(
                customer=customer_id,
                payment_method_types=["card"],
                mode="subscription",
                line_items=[
                    {
                        "price": tier_config["price_id"],
                        "quantity": 1,
                    }
                ],
                success_url=success_url,
                cancel_url=cancel_url,
            )

            logger.info(f"✅ Checkout session created: {session.id}")
            return {"status": "success", "checkout_url": session.url}

        except stripe.error.StripeError as e:
            logger.error(f"❌ Checkout error: {e}")
            return {"status": "error", "error": str(e)}


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
# EXPORTS
# ============================================================================

__all__ = ["StripeService", "SUBSCRIPTION_TIERS", "get_stripe_service"]
