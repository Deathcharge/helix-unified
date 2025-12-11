"""
Copyright (c) 2025 Andrew John Ward. All Rights Reserved.
PROPRIETARY AND CONFIDENTIAL - See LICENSE file for terms.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel, Field


class ActionBase(BaseModel):
    action_type: str
    config: Dict[str, Any]


class ActionCreate(ActionBase):
    order_index: int


class ActionUpdate(BaseModel):
    action_type: Optional[str] = None
    config: Optional[Dict[str, Any]] = None
    order_index: Optional[int] = None


class ActionResponse(ActionBase):
    id: UUID
    spiral_id: UUID
    order_index: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class SpiralBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    trigger_type: str = "manual"
    trigger_config: Dict[str, Any] = {}


class SpiralCreate(SpiralBase):
    pass


class SpiralUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    is_active: Optional[bool] = None
    trigger_type: Optional[str] = None
    trigger_config: Optional[Dict[str, Any]] = None


class SpiralResponse(SpiralBase):
    id: UUID
    user_id: UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime
    last_run_at: Optional[datetime]
    run_count: int
    actions: List[ActionResponse] = []
    
    class Config:
        from_attributes = True


class SpiralExecuteRequest(BaseModel):
    input_data: Optional[Dict[str, Any]] = {}


class ExecutionLogResponse(BaseModel):
    id: UUID
    spiral_id: UUID
    status: str
    started_at: datetime
    completed_at: Optional[datetime]
    error_message: Optional[str]
    input_data: Optional[Dict[str, Any]]
    output_data: Optional[Dict[str, Any]]
    duration_seconds: Optional[float]
    
    class Config:
        from_attributes = True