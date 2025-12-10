"""
Comprehensive test suite for SaaS Stripe Integration
=====================================================

Tests:
- Subscription creation
- Subscription cancellation
- Subscription updates (tier changes)
- Checkout session creation
- Webhook event handling
- Payment history retrieval
- Tier upgrades/downgrades with proration
"""

from datetime import datetime, timedelta
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi import HTTPException
from urllib.parse import urlparse

from backend.saas_stripe import (
    STRIPE_PRICE_IDS,
    CheckoutSessionRequest,
    SubscriptionRequest,
    SubscriptionResponse,
    cancel_subscription,
    create_checkout_session,
    create_subscription,
    get_payment_history,
    get_stripe_price_id,
    handle_webhook_event,
    update_subscription,
)


class TestSubscriptionCreation:
    """Test subscription creation functionality"""

    @pytest.mark.asyncio
    async def test_create_subscription_pro_monthly(self):
        """Test creating a Pro monthly subscription"""
        user_id = "user_123"
        email = "test@example.com"
        tier = "pro"
        billing_cycle = "monthly"

        with patch('backend.saas_stripe.stripe') as mock_stripe, \
             patch('backend.saas_stripe.Database') as mock_db:

            # Mock Stripe customer creation
            mock_stripe.Customer.create.return_value = MagicMock(
                id="cus_test123"
            )

            # Mock Stripe subscription creation
            mock_subscription = MagicMock()
            mock_subscription.id = "sub_test123"
            mock_subscription.customer = "cus_test123"
            mock_subscription.status = "active"
            mock_subscription.current_period_end = int((datetime.utcnow() + timedelta(days=30)).timestamp())
            mock_subscription.cancel_at_period_end = False

            mock_stripe.Subscription.create.return_value = mock_subscription

            # Mock database update
            mock_pool = AsyncMock()
            mock_db.get_pool.return_value = mock_pool

            result = await create_subscription(user_id, email, tier, billing_cycle)

            assert isinstance(result, SubscriptionResponse)
            assert result.subscription_id == "sub_test123"
            assert result.customer_id == "cus_test123"
            assert result.status == "active"
            assert result.tier == "pro"

            # Verify Stripe calls
            mock_stripe.Customer.create.assert_called_once()
            mock_stripe.Subscription.create.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_subscription_enterprise_yearly(self):
        """Test creating Enterprise yearly subscription"""
        user_id = "user_123"
        email = "enterprise@example.com"
        tier = "enterprise"
        billing_cycle = "yearly"

        with patch('backend.saas_stripe.stripe') as mock_stripe, \
             patch('backend.saas_stripe.Database') as mock_db:

            mock_stripe.Customer.create.return_value = MagicMock(id="cus_ent123")

            mock_subscription = MagicMock()
            mock_subscription.id = "sub_ent123"
            mock_subscription.customer = "cus_ent123"
            mock_subscription.status = "active"
            mock_subscription.current_period_end = int((datetime.utcnow() + timedelta(days=365)).timestamp())
            mock_subscription.cancel_at_period_end = False

            mock_stripe.Subscription.create.return_value = mock_subscription

            mock_pool = AsyncMock()
            mock_db.get_pool.return_value = mock_pool

            result = await create_subscription(user_id, email, tier, billing_cycle)

            assert result.tier == "enterprise"
            # Verify yearly price ID was used
            call_args = mock_stripe.Subscription.create.call_args
            assert "enterprise_yearly" in str(call_args)

    @pytest.mark.asyncio
    async def test_create_subscription_invalid_tier(self):
        """Test subscription creation with invalid tier"""
        with pytest.raises(HTTPException) as exc_info:
            await create_subscription(
                "user_123",
                "test@example.com",
                "invalid_tier",
                "monthly"
            )

        assert exc_info.value.status_code == 400

    @pytest.mark.asyncio
    async def test_create_subscription_stripe_error(self):
        """Test subscription creation when Stripe API fails"""
        with patch('backend.saas_stripe.stripe') as mock_stripe:
            mock_stripe.Customer.create.side_effect = Exception("Stripe API error")

            with pytest.raises(HTTPException) as exc_info:
                await create_subscription(
                    "user_123",
                    "test@example.com",
                    "pro",
                    "monthly"
                )

            assert exc_info.value.status_code == 500


class TestSubscriptionCancellation:
    """Test subscription cancellation functionality"""

    @pytest.mark.asyncio
    async def test_cancel_subscription_at_period_end(self):
        """Test canceling subscription at end of billing period"""
        user_id = "user_123"
        immediate = False

        with patch('backend.saas_stripe.stripe') as mock_stripe, \
             patch('backend.saas_stripe.Database') as mock_db:

            # Mock database query for subscription ID
            mock_pool = AsyncMock()
            mock_db.get_pool.return_value = mock_pool
            mock_pool.fetchval.return_value = "sub_test123"

            # Mock Stripe subscription update
            mock_subscription = MagicMock()
            mock_subscription.id = "sub_test123"
            mock_subscription.cancel_at_period_end = True

            mock_stripe.Subscription.modify.return_value = mock_subscription

            result = await cancel_subscription(user_id, immediate)

            assert result["status"] == "scheduled_cancellation"
            assert "cancel_at_period_end" in result

            # Verify Stripe was called with correct parameters
            mock_stripe.Subscription.modify.assert_called_once_with(
                "sub_test123",
                cancel_at_period_end=True
            )

    @pytest.mark.asyncio
    async def test_cancel_subscription_immediately(self):
        """Test immediate subscription cancellation"""
        user_id = "user_123"
        immediate = True

        with patch('backend.saas_stripe.stripe') as mock_stripe, \
             patch('backend.saas_stripe.Database') as mock_db:

            mock_pool = AsyncMock()
            mock_db.get_pool.return_value = mock_pool
            mock_pool.fetchval.return_value = "sub_test123"

            mock_subscription = MagicMock()
            mock_subscription.id = "sub_test123"
            mock_subscription.status = "canceled"

            mock_stripe.Subscription.delete.return_value = mock_subscription

            result = await cancel_subscription(user_id, immediate)

            assert result["status"] == "canceled"

            # Verify Stripe delete was called
            mock_stripe.Subscription.delete.assert_called_once_with("sub_test123")

    @pytest.mark.asyncio
    async def test_cancel_subscription_no_active_subscription(self):
        """Test canceling when user has no active subscription"""
        user_id = "user_no_sub"

        with patch('backend.saas_stripe.Database') as mock_db:
            mock_pool = AsyncMock()
            mock_db.get_pool.return_value = mock_pool
            mock_pool.fetchval.return_value = None  # No subscription found

            with pytest.raises(HTTPException) as exc_info:
                await cancel_subscription(user_id, False)

            assert exc_info.value.status_code == 404


class TestSubscriptionUpdates:
    """Test subscription update functionality"""

    @pytest.mark.asyncio
    async def test_update_subscription_tier_upgrade(self):
        """Test upgrading from Pro to Enterprise"""
        user_id = "user_123"
        new_tier = "enterprise"
        new_billing_cycle = None

        with patch('backend.saas_stripe.stripe') as mock_stripe, \
             patch('backend.saas_stripe.Database') as mock_db:

            mock_pool = AsyncMock()
            mock_db.get_pool.return_value = mock_pool

            # Mock current subscription
            mock_pool.fetchrow.return_value = {
                "subscription_id": "sub_test123",
                "tier": "pro",
                "billing_cycle": "monthly"
            }

            # Mock Stripe subscription update
            mock_subscription = MagicMock()
            mock_subscription.id = "sub_test123"
            mock_subscription.status = "active"
            mock_stripe.Subscription.modify.return_value = mock_subscription

            result = await update_subscription(user_id, new_tier, new_billing_cycle)

            assert result["status"] == "updated"
            assert result["new_tier"] == "enterprise"

            # Verify proration was enabled
            call_args = mock_stripe.Subscription.modify.call_args
            assert call_args[1]["proration_behavior"] == "create_prorations"

    @pytest.mark.asyncio
    async def test_update_subscription_billing_cycle(self):
        """Test changing billing cycle from monthly to yearly"""
        user_id = "user_123"
        new_tier = None
        new_billing_cycle = "yearly"

        with patch('backend.saas_stripe.stripe') as mock_stripe, \
             patch('backend.saas_stripe.Database') as mock_db:

            mock_pool = AsyncMock()
            mock_db.get_pool.return_value = mock_pool

            mock_pool.fetchrow.return_value = {
                "subscription_id": "sub_test123",
                "tier": "pro",
                "billing_cycle": "monthly"
            }

            mock_subscription = MagicMock()
            mock_subscription.id = "sub_test123"
            mock_stripe.Subscription.modify.return_value = mock_subscription

            result = await update_subscription(user_id, new_tier, new_billing_cycle)

            assert result["new_billing_cycle"] == "yearly"

    @pytest.mark.asyncio
    async def test_update_subscription_downgrade(self):
        """Test downgrading from Enterprise to Pro"""
        user_id = "user_123"
        new_tier = "pro"

        with patch('backend.saas_stripe.stripe') as mock_stripe, \
             patch('backend.saas_stripe.Database') as mock_db:

            mock_pool = AsyncMock()
            mock_db.get_pool.return_value = mock_pool

            mock_pool.fetchrow.return_value = {
                "subscription_id": "sub_test123",
                "tier": "enterprise",
                "billing_cycle": "monthly"
            }

            mock_subscription = MagicMock()
            mock_subscription.id = "sub_test123"
            mock_stripe.Subscription.modify.return_value = mock_subscription

            result = await update_subscription(user_id, new_tier, None)

            assert result["new_tier"] == "pro"


class TestCheckoutSessions:
    """Test Stripe Checkout session creation"""

    @pytest.mark.asyncio
    async def test_create_checkout_session_success(self):
        """Test creating Stripe Checkout session"""
        user_id = "user_123"
        email = "test@example.com"
        tier = "pro"
        billing_cycle = "monthly"
        success_url = "https://example.com/success"
        cancel_url = "https://example.com/cancel"

        with patch('backend.saas_stripe.stripe') as mock_stripe:
            # Mock Stripe Checkout session creation
            mock_session = MagicMock()
            mock_session.id = "cs_test123"
            mock_session.url = "https://checkout.stripe.com/pay/cs_test123"

            mock_stripe.checkout.Session.create.return_value = mock_session

            result = await create_checkout_session(
                user_id, email, tier, billing_cycle, success_url, cancel_url
            )

            assert result["id"] == "cs_test123"
            parsed_url = urlparse(result["url"])
            assert parsed_url.hostname == "checkout.stripe.com"

            # Verify Stripe was called with correct parameters
            call_args = mock_stripe.checkout.Session.create.call_args
            assert call_args[1]["success_url"] == success_url
            assert call_args[1]["cancel_url"] == cancel_url
            assert call_args[1]["mode"] == "subscription"

    @pytest.mark.asyncio
    async def test_create_checkout_session_invalid_urls(self):
        """Test checkout session with invalid URLs"""
        with pytest.raises(HTTPException):
            await create_checkout_session(
                "user_123",
                "test@example.com",
                "pro",
                "monthly",
                "not_a_url",
                "also_not_a_url"
            )


class TestWebhookHandling:
    """Test Stripe webhook event handling"""

    @pytest.mark.asyncio
    async def test_handle_checkout_completed_webhook(self):
        """Test handling checkout.session.completed webhook"""
        event = {
            "type": "checkout.session.completed",
            "data": {
                "object": {
                    "customer": "cus_test123",
                    "subscription": "sub_test123",
                    "metadata": {
                        "user_id": "user_123",
                        "tier": "pro"
                    }
                }
            }
        }

        with patch('backend.saas_stripe.Database') as mock_db:
            mock_pool = AsyncMock()
            mock_db.get_pool.return_value = mock_pool

            await handle_webhook_event(event)

            # Verify database was updated with subscription info
            assert mock_pool.execute.called

    @pytest.mark.asyncio
    async def test_handle_subscription_updated_webhook(self):
        """Test handling customer.subscription.updated webhook"""
        event = {
            "type": "customer.subscription.updated",
            "data": {
                "object": {
                    "id": "sub_test123",
                    "customer": "cus_test123",
                    "status": "active",
                    "cancel_at_period_end": False
                }
            }
        }

        with patch('backend.saas_stripe.Database') as mock_db:
            mock_pool = AsyncMock()
            mock_db.get_pool.return_value = mock_pool

            await handle_webhook_event(event)

            assert mock_pool.execute.called

    @pytest.mark.asyncio
    async def test_handle_subscription_deleted_webhook(self):
        """Test handling customer.subscription.deleted webhook"""
        event = {
            "type": "customer.subscription.deleted",
            "data": {
                "object": {
                    "id": "sub_test123",
                    "customer": "cus_test123"
                }
            }
        }

        with patch('backend.saas_stripe.Database') as mock_db:
            mock_pool = AsyncMock()
            mock_db.get_pool.return_value = mock_pool
            mock_pool.fetchval.return_value = "user_123"

            await handle_webhook_event(event)

            # Verify user was downgraded to free tier
            assert mock_pool.execute.called

    @pytest.mark.asyncio
    async def test_handle_invoice_payment_failed_webhook(self):
        """Test handling invoice.payment_failed webhook"""
        event = {
            "type": "invoice.payment_failed",
            "data": {
                "object": {
                    "customer": "cus_test123",
                    "subscription": "sub_test123",
                    "amount_due": 2900
                }
            }
        }

        with patch('backend.saas_stripe.Database') as mock_db:
            mock_pool = AsyncMock()
            mock_db.get_pool.return_value = mock_pool

            await handle_webhook_event(event)

            # Verify payment failure was logged
            assert mock_pool.execute.called

    @pytest.mark.asyncio
    async def test_handle_unknown_webhook_event(self):
        """Test handling unknown webhook event type"""
        event = {
            "type": "unknown.event.type",
            "data": {"object": {}}
        }

        # Should not raise exception for unknown events
        await handle_webhook_event(event)


class TestPaymentHistory:
    """Test payment history retrieval"""

    @pytest.mark.asyncio
    async def test_get_payment_history_success(self):
        """Test retrieving payment history"""
        user_id = "user_123"
        limit = 10

        with patch('backend.saas_stripe.Database') as mock_db, \
             patch('backend.saas_stripe.stripe') as mock_stripe:

            mock_pool = AsyncMock()
            mock_db.get_pool.return_value = mock_pool
            mock_pool.fetchval.return_value = "cus_test123"

            # Mock Stripe invoices
            mock_invoice = MagicMock()
            mock_invoice.id = "in_test123"
            mock_invoice.amount_paid = 2900
            mock_invoice.currency = "usd"
            mock_invoice.created = int(datetime.utcnow().timestamp())
            mock_invoice.invoice_pdf = "https://stripe.com/invoice.pdf"
            mock_invoice.status = "paid"

            mock_stripe.Invoice.list.return_value = MagicMock(
                data=[mock_invoice]
            )

            result = await get_payment_history(user_id, limit)

            assert len(result) > 0
            assert result[0]["amount"] == 29.00  # Converted from cents
            assert result[0]["currency"] == "usd"
            assert result[0]["status"] == "paid"

    @pytest.mark.asyncio
    async def test_get_payment_history_no_customer(self):
        """Test payment history when user has no Stripe customer"""
        user_id = "user_no_customer"

        with patch('backend.saas_stripe.Database') as mock_db:
            mock_pool = AsyncMock()
            mock_db.get_pool.return_value = mock_pool
            mock_pool.fetchval.return_value = None  # No customer ID

            result = await get_payment_history(user_id, 10)

            assert result == []


class TestPriceMapping:
    """Test Stripe price ID mapping"""

    def test_get_stripe_price_id_all_tiers(self):
        """Test price ID mapping for all tier/billing combinations"""
        # Test all valid combinations
        assert get_stripe_price_id("pro", "monthly") == STRIPE_PRICE_IDS["pro_monthly"]
        assert get_stripe_price_id("pro", "yearly") == STRIPE_PRICE_IDS["pro_yearly"]
        assert get_stripe_price_id("workflow", "monthly") == STRIPE_PRICE_IDS["workflow_monthly"]
        assert get_stripe_price_id("workflow", "yearly") == STRIPE_PRICE_IDS["workflow_yearly"]
        assert get_stripe_price_id("enterprise", "monthly") == STRIPE_PRICE_IDS["enterprise_monthly"]
        assert get_stripe_price_id("enterprise", "yearly") == STRIPE_PRICE_IDS["enterprise_yearly"]

    def test_get_stripe_price_id_invalid(self):
        """Test price ID mapping with invalid inputs"""
        with pytest.raises(ValueError):
            get_stripe_price_id("free", "monthly")  # Free tier not in Stripe

        with pytest.raises(ValueError):
            get_stripe_price_id("pro", "invalid_cycle")


class TestRequestModels:
    """Test Pydantic request models"""

    def test_subscription_request_valid(self):
        """Test valid subscription request"""
        request = SubscriptionRequest(tier="pro", billing_cycle="monthly")
        assert request.tier == "pro"
        assert request.billing_cycle == "monthly"

    def test_checkout_session_request_valid(self):
        """Test valid checkout session request"""
        request = CheckoutSessionRequest(
            tier="workflow",
            billing_cycle="yearly",
            success_url="https://example.com/success",
            cancel_url="https://example.com/cancel"
        )
        assert request.tier == "workflow"
        assert request.billing_cycle == "yearly"
        assert request.success_url.startswith("https://")
