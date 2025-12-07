"""
Copyright (c) 2025 Andrew John Ward. All Rights Reserved.
PROPRIETARY AND CONFIDENTIAL - See LICENSE file for terms.
"""

import uuid
from datetime import datetime

from app.database import Base
from sqlalchemy import (Boolean, Column, DateTime, ForeignKey, Integer, String,
                        Text)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship


class Spiral(Base):
    __tablename__ = "spirals"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    is_active = Column(Boolean, default=True)
    trigger_type = Column(String(50), default="manual")  # webhook, schedule, manual, event
    trigger_config = Column(JSONB, default={})
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_run_at = Column(DateTime)
    run_count = Column(Integer, default=0)
    
    # Relationships
    user = relationship("User", back_populates="spirals")
    actions = relationship("Action", back_populates="spiral", cascade="all, delete-orphan", order_by="Action.order_index")
    execution_logs = relationship("ExecutionLog", back_populates="spiral", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Spiral {self.name}>"


class Action(Base):
    __tablename__ = "actions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    spiral_id = Column(UUID(as_uuid=True), ForeignKey("spirals.id"), nullable=False)
    order_index = Column(Integer, nullable=False)
    action_type = Column(String(50), nullable=False)  # http_request, database, email, ai_call, transform
    config = Column(JSONB, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    spiral = relationship("Spiral", back_populates="actions")
    
    def __repr__(self):
        return f"<Action {self.action_type} - Order {self.order_index}>"


class ExecutionLog(Base):
    __tablename__ = "execution_logs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    spiral_id = Column(UUID(as_uuid=True), ForeignKey("spirals.id"), nullable=False)
    status = Column(String(50), default="running")  # success, failed, running
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)
    error_message = Column(Text)
    input_data = Column(JSONB)
    output_data = Column(JSONB)
    
    # Relationships
    spiral = relationship("Spiral", back_populates="execution_logs")
    
    def __repr__(self):
        return f"<ExecutionLog {self.status}>"
    
    @property
    def duration_seconds(self):
        """Calculate execution duration in seconds"""
        if self.completed_at and self.started_at:
            return (self.completed_at - self.started_at).total_seconds()
        return None