"""
Copyright (c) 2025 Andrew John Ward. All Rights Reserved.
PROPRIETARY AND CONFIDENTIAL - See LICENSE file for terms.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.database import get_db
from app.models import User
from app.schemas import (
    SpiralCreate,
    SpiralUpdate,
    SpiralResponse,
    SpiralExecuteRequest,
    ActionCreate,
    ActionUpdate,
    ActionResponse,
    ExecutionLogResponse
)
from app.utils.dependencies import get_current_user
from app.services.spiral_service import SpiralService
from app.services.execution_service import ExecutionService

router = APIRouter()


# Spiral endpoints
@router.get("", response_model=List[SpiralResponse])
async def list_spirals(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List all spirals for current user"""
    return SpiralService.get_user_spirals(current_user, db)


@router.post("", response_model=SpiralResponse, status_code=status.HTTP_201_CREATED)
async def create_spiral(
    spiral_data: SpiralCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new spiral"""
    return SpiralService.create_spiral(spiral_data, current_user, db)


@router.get("/{spiral_id}", response_model=SpiralResponse)
async def get_spiral(
    spiral_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific spiral"""
    return SpiralService.get_spiral(spiral_id, current_user, db)


@router.put("/{spiral_id}", response_model=SpiralResponse)
async def update_spiral(
    spiral_id: UUID,
    spiral_data: SpiralUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a spiral"""
    return SpiralService.update_spiral(spiral_id, spiral_data, current_user, db)


@router.delete("/{spiral_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_spiral(
    spiral_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a spiral"""
    SpiralService.delete_spiral(spiral_id, current_user, db)


@router.post("/{spiral_id}/toggle", response_model=SpiralResponse)
async def toggle_spiral(
    spiral_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Toggle spiral active status"""
    return SpiralService.toggle_spiral(spiral_id, current_user, db)


@router.post("/{spiral_id}/execute", response_model=ExecutionLogResponse)
async def execute_spiral(
    spiral_id: UUID,
    execute_data: SpiralExecuteRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Execute a spiral manually"""
    try:
        return await ExecutionService.execute_spiral(
            spiral_id,
            current_user,
            execute_data.input_data,
            db
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


# Action endpoints
@router.get("/{spiral_id}/actions", response_model=List[ActionResponse])
async def list_actions(
    spiral_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List all actions for a spiral"""
    spiral = SpiralService.get_spiral(spiral_id, current_user, db)
    return spiral.actions


@router.post("/{spiral_id}/actions", response_model=ActionResponse, status_code=status.HTTP_201_CREATED)
async def create_action(
    spiral_id: UUID,
    action_data: ActionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Add an action to a spiral"""
    return SpiralService.add_action(spiral_id, action_data, current_user, db)


@router.put("/actions/{action_id}", response_model=ActionResponse)
async def update_action(
    action_id: UUID,
    action_data: ActionUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update an action"""
    return SpiralService.update_action(action_id, action_data, current_user, db)


@router.delete("/actions/{action_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_action(
    action_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete an action"""
    SpiralService.delete_action(action_id, current_user, db)


# Execution log endpoints
@router.get("/{spiral_id}/logs", response_model=List[ExecutionLogResponse])
async def get_execution_logs(
    spiral_id: UUID,
    limit: int = 50,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get execution logs for a spiral"""
    return SpiralService.get_execution_logs(spiral_id, current_user, db, limit)