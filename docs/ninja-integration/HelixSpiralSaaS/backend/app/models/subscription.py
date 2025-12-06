"""
Copyright (c) 2025 Andrew John Ward. All Rights Reserved.
PROPRIETARY AND CONFIDENTIAL - See LICENSE file for terms.
"""

import uuid
from datetime import datetime

from app.database import Base
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship


class Subscription(Base):
    __tablename__ = "subscriptions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    stripe_customer_id = Column(String(255), unique=True)
    stripe_subscription_id = Column(String(255), unique=True)
    plan_type = Column(String(50), default="free")  # free, pro, enterprise
    status = Column(String(50), default="active")  # active, canceled, past_due, trialing
    current_period_start = Column(DateTime)
    current_period_end = Column(DateTime)
    cancel_at_period_end = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="subscription")
    
    def __repr__(self):
        return f"<Subscription {self.plan_type} - {self.status}>"
    
    @property
    def is_active(self):
        """Check if subscription is active"""
        return self.status in ["active", "trialing"]
    
    @property
    def execution_limit(self):
        """Get execution limit based on plan"""
        limits = {
            "free": 100,
            "pro": 10000,
            "enterprise": -1  # unlimited
        }
        return limits.get(self.plan_type, 100)
    
    @property
    def spiral_limit(self):
        """Get spiral limit based on plan"""
        limits = {
            "free": 5,
            "pro": -1,  # unlimited
            "enterprise": -1  # unlimited
        }
        return limits.get(self.plan_type, 5)