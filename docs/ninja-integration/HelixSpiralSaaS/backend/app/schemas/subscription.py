"""
Copyright (c) 2025 Andrew John Ward. All Rights Reserved.
PROPRIETARY AND CONFIDENTIAL - See LICENSE file for terms.
"""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class SubscriptionBase(BaseModel):
    plan_type: str
    status: str


class SubscriptionResponse(SubscriptionBase):
    id: UUID
    user_id: UUID
    stripe_customer_id: Optional[str]
    stripe_subscription_id: Optional[str]
    current_period_start: Optional[datetime]
    current_period_end: Optional[datetime]
    cancel_at_period_end: bool
    created_at: datetime
    execution_limit: int
    spiral_limit: int
    
    class Config:
        from_attributes = True


class CheckoutSessionCreate(BaseModel):
    plan_type: str  # pro or enterprise
    success_url: str
    cancel_url: str


class CheckoutSessionResponse(BaseModel):
    session_id: str
    url: str


class PortalSessionResponse(BaseModel):
    url: str