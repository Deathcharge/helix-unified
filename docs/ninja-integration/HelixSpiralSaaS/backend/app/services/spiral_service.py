"""
Copyright (c) 2025 Andrew John Ward. All Rights Reserved.
PROPRIETARY AND CONFIDENTIAL - See LICENSE file for terms.
"""

from datetime import datetime
from typing import List, Optional
from uuid import UUID

from app.models import Action, ExecutionLog, Spiral, User
from app.schemas import (ActionCreate, ActionUpdate, SpiralCreate,
                         SpiralResponse, SpiralUpdate)
from fastapi import HTTPException, status
from sqlalchemy.orm import Session


class SpiralService:
    """Service for managing spirals (workflows)"""
    
    @staticmethod
    def create_spiral(spiral_data: SpiralCreate, user: User, db: Session) -> Spiral:
        """Create a new spiral"""
        # Check subscription limits
        from app.utils.dependencies import check_subscription_limits
        check_subscription_limits(user, db)
        
        # Create spiral
        spiral = Spiral(
            user_id=user.id,
            name=spiral_data.name,
            description=spiral_data.description,
            trigger_type=spiral_data.trigger_type,
            trigger_config=spiral_data.trigger_config
        )
        
        db.add(spiral)
        db.commit()
        db.refresh(spiral)
        
        return spiral
    
    @staticmethod
    def get_user_spirals(user: User, db: Session) -> List[Spiral]:
        """Get all spirals for a user"""
        return db.query(Spiral).filter(Spiral.user_id == user.id).all()
    
    @staticmethod
    def get_spiral(spiral_id: UUID, user: User, db: Session) -> Spiral:
        """Get a specific spiral"""
        spiral = db.query(Spiral).filter(
            Spiral.id == spiral_id,
            Spiral.user_id == user.id
        ).first()
        
        if not spiral:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Spiral not found"
            )
        
        return spiral
    
    @staticmethod
    def update_spiral(
        spiral_id: UUID,
        spiral_data: SpiralUpdate,
        user: User,
        db: Session
    ) -> Spiral:
        """Update a spiral"""
        spiral = SpiralService.get_spiral(spiral_id, user, db)
        
        # Update fields
        if spiral_data.name is not None:
            spiral.name = spiral_data.name
        if spiral_data.description is not None:
            spiral.description = spiral_data.description
        if spiral_data.is_active is not None:
            spiral.is_active = spiral_data.is_active
        if spiral_data.trigger_type is not None:
            spiral.trigger_type = spiral_data.trigger_type
        if spiral_data.trigger_config is not None:
            spiral.trigger_config = spiral_data.trigger_config
        
        spiral.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(spiral)
        
        return spiral
    
    @staticmethod
    def delete_spiral(spiral_id: UUID, user: User, db: Session):
        """Delete a spiral"""
        spiral = SpiralService.get_spiral(spiral_id, user, db)
        db.delete(spiral)
        db.commit()
    
    @staticmethod
    def toggle_spiral(spiral_id: UUID, user: User, db: Session) -> Spiral:
        """Toggle spiral active status"""
        spiral = SpiralService.get_spiral(spiral_id, user, db)
        spiral.is_active = not spiral.is_active
        spiral.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(spiral)
        return spiral
    
    @staticmethod
    def add_action(
        spiral_id: UUID,
        action_data: ActionCreate,
        user: User,
        db: Session
    ) -> Action:
        """Add an action to a spiral"""
        spiral = SpiralService.get_spiral(spiral_id, user, db)
        
        action = Action(
            spiral_id=spiral.id,
            order_index=action_data.order_index,
            action_type=action_data.action_type,
            config=action_data.config
        )
        
        db.add(action)
        db.commit()
        db.refresh(action)
        
        return action
    
    @staticmethod
    def update_action(
        action_id: UUID,
        action_data: ActionUpdate,
        user: User,
        db: Session
    ) -> Action:
        """Update an action"""
        action = db.query(Action).filter(Action.id == action_id).first()
        
        if not action:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Action not found"
            )
        
        # Verify ownership through spiral
        spiral = db.query(Spiral).filter(
            Spiral.id == action.spiral_id,
            Spiral.user_id == user.id
        ).first()
        
        if not spiral:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to modify this action"
            )
        
        # Update fields
        if action_data.action_type is not None:
            action.action_type = action_data.action_type
        if action_data.config is not None:
            action.config = action_data.config
        if action_data.order_index is not None:
            action.order_index = action_data.order_index
        
        action.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(action)
        
        return action
    
    @staticmethod
    def delete_action(action_id: UUID, user: User, db: Session):
        """Delete an action"""
        action = db.query(Action).filter(Action.id == action_id).first()
        
        if not action:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Action not found"
            )
        
        # Verify ownership
        spiral = db.query(Spiral).filter(
            Spiral.id == action.spiral_id,
            Spiral.user_id == user.id
        ).first()
        
        if not spiral:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to delete this action"
            )
        
        db.delete(action)
        db.commit()
    
    @staticmethod
    def get_execution_logs(
        spiral_id: UUID,
        user: User,
        db: Session,
        limit: int = 50
    ) -> List[ExecutionLog]:
        """Get execution logs for a spiral"""
        spiral = SpiralService.get_spiral(spiral_id, user, db)
        
        logs = db.query(ExecutionLog).filter(
            ExecutionLog.spiral_id == spiral.id
        ).order_by(ExecutionLog.started_at.desc()).limit(limit).all()
        
        return logs