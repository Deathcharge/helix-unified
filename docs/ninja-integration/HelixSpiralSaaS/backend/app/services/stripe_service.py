"""
Copyright (c) 2025 Andrew John Ward. All Rights Reserved.
PROPRIETARY AND CONFIDENTIAL - See LICENSE file for terms.
"""

import stripe
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime

from app.config import settings
from app.models import User, Subscription
from app.schemas import CheckoutSessionCreate, CheckoutSessionResponse, PortalSessionResponse

# Initialize Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY


class StripeService:
    """Stripe payment and subscription service"""
    
    @staticmethod
    def create_checkout_session(
        user: User,
        checkout_data: CheckoutSessionCreate,
        db: Session
    ) -> CheckoutSessionResponse:
        """Create Stripe checkout session for subscription"""
        
        # Get or create Stripe customer
        subscription = db.query(Subscription).filter(Subscription.user_id == user.id).first()
        
        if subscription and subscription.stripe_customer_id:
            customer_id = subscription.stripe_customer_id
        else:
            # Create new Stripe customer
            customer = stripe.Customer.create(
                email=user.email,
                metadata={"user_id": str(user.id)}
            )
            customer_id = customer.id
            
            # Update subscription with customer ID
            if subscription:
                subscription.stripe_customer_id = customer_id
                db.commit()
        
        # Get price ID based on plan
        price_id = (
            settings.STRIPE_PRICE_ID_PRO
            if checkout_data.plan_type == "pro"
            else settings.STRIPE_PRICE_ID_ENTERPRISE
        )
        
        # Create checkout session
        try:
            checkout_session = stripe.checkout.Session.create(
                customer=customer_id,
                payment_method_types=["card"],
                line_items=[{
                    "price": price_id,
                    "quantity": 1,
                }],
                mode="subscription",
                success_url=checkout_data.success_url,
                cancel_url=checkout_data.cancel_url,
                metadata={
                    "user_id": str(user.id),
                    "plan_type": checkout_data.plan_type
                }
            )
            
            return CheckoutSessionResponse(
                session_id=checkout_session.id,
                url=checkout_session.url
            )
        except stripe.error.StripeError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Stripe error: {str(e)}"
            )
    
    @staticmethod
    def create_portal_session(user: User, return_url: str, db: Session) -> PortalSessionResponse:
        """Create Stripe customer portal session"""
        
        subscription = db.query(Subscription).filter(Subscription.user_id == user.id).first()
        
        if not subscription or not subscription.stripe_customer_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No Stripe customer found"
            )
        
        try:
            portal_session = stripe.billing_portal.Session.create(
                customer=subscription.stripe_customer_id,
                return_url=return_url
            )
            
            return PortalSessionResponse(url=portal_session.url)
        except stripe.error.StripeError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Stripe error: {str(e)}"
            )
    
    @staticmethod
    def handle_webhook_event(event: dict, db: Session):
        """Handle Stripe webhook events"""
        
        event_type = event["type"]
        data = event["data"]["object"]
        
        if event_type == "checkout.session.completed":
            # Payment successful, activate subscription
            StripeService._handle_checkout_completed(data, db)
        
        elif event_type == "customer.subscription.updated":
            # Subscription updated
            StripeService._handle_subscription_updated(data, db)
        
        elif event_type == "customer.subscription.deleted":
            # Subscription canceled
            StripeService._handle_subscription_deleted(data, db)
        
        elif event_type == "invoice.payment_failed":
            # Payment failed
            StripeService._handle_payment_failed(data, db)
    
    @staticmethod
    def _handle_checkout_completed(session: dict, db: Session):
        """Handle successful checkout"""
        user_id = session["metadata"]["user_id"]
        plan_type = session["metadata"]["plan_type"]
        
        subscription = db.query(Subscription).filter(Subscription.user_id == user_id).first()
        if subscription:
            subscription.stripe_subscription_id = session["subscription"]
            subscription.plan_type = plan_type
            subscription.status = "active"
            db.commit()
    
    @staticmethod
    def _handle_subscription_updated(stripe_subscription: dict, db: Session):
        """Handle subscription update"""
        subscription = db.query(Subscription).filter(
            Subscription.stripe_subscription_id == stripe_subscription["id"]
        ).first()
        
        if subscription:
            subscription.status = stripe_subscription["status"]
            subscription.current_period_start = datetime.fromtimestamp(
                stripe_subscription["current_period_start"]
            )
            subscription.current_period_end = datetime.fromtimestamp(
                stripe_subscription["current_period_end"]
            )
            subscription.cancel_at_period_end = stripe_subscription["cancel_at_period_end"]
            db.commit()
    
    @staticmethod
    def _handle_subscription_deleted(stripe_subscription: dict, db: Session):
        """Handle subscription cancellation"""
        subscription = db.query(Subscription).filter(
            Subscription.stripe_subscription_id == stripe_subscription["id"]
        ).first()
        
        if subscription:
            subscription.status = "canceled"
            subscription.plan_type = "free"
            db.commit()
    
    @staticmethod
    def _handle_payment_failed(invoice: dict, db: Session):
        """Handle failed payment"""
        subscription = db.query(Subscription).filter(
            Subscription.stripe_subscription_id == invoice["subscription"]
        ).first()
        
        if subscription:
            subscription.status = "past_due"
            db.commit()