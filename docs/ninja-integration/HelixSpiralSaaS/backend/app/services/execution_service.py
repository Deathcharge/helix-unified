"""
Copyright (c) 2025 Andrew John Ward. All Rights Reserved.
PROPRIETARY AND CONFIDENTIAL - See LICENSE file for terms.
"""

from sqlalchemy.orm import Session
from typing import Dict, Any, Optional
from uuid import UUID
from datetime import datetime
import httpx
import logging

from app.models import Spiral, Action, ExecutionLog, User, Subscription
from app.services.email_service import email_service

logger = logging.getLogger(__name__)


class ExecutionService:
    """Service for executing spirals and actions"""
    
    @staticmethod
    async def execute_spiral(
        spiral_id: UUID,
        user: User,
        input_data: Dict[str, Any],
        db: Session
    ) -> ExecutionLog:
        """Execute a spiral with its actions"""
        
        # Get spiral
        spiral = db.query(Spiral).filter(
            Spiral.id == spiral_id,
            Spiral.user_id == user.id
        ).first()
        
        if not spiral:
            raise ValueError("Spiral not found")
        
        if not spiral.is_active:
            raise ValueError("Spiral is not active")
        
        # Check execution limits
        subscription = db.query(Subscription).filter(
            Subscription.user_id == user.id
        ).first()
        
        if subscription:
            limit = subscription.execution_limit
            if limit != -1:  # -1 means unlimited
                # Count executions this month
                from sqlalchemy import func, extract
                current_month_count = db.query(func.count(ExecutionLog.id)).filter(
                    ExecutionLog.spiral_id.in_(
                        db.query(Spiral.id).filter(Spiral.user_id == user.id)
                    ),
                    extract('month', ExecutionLog.started_at) == datetime.utcnow().month,
                    extract('year', ExecutionLog.started_at) == datetime.utcnow().year
                ).scalar()
                
                if current_month_count >= limit:
                    raise ValueError(f"Execution limit reached ({limit}). Please upgrade your plan.")
        
        # Create execution log
        execution_log = ExecutionLog(
            spiral_id=spiral.id,
            status="running",
            input_data=input_data
        )
        db.add(execution_log)
        db.commit()
        db.refresh(execution_log)
        
        try:
            # Execute actions in order
            context = {"input": input_data}
            
            for action in sorted(spiral.actions, key=lambda a: a.order_index):
                result = await ExecutionService._execute_action(action, context)
                context[f"action_{action.order_index}"] = result
            
            # Mark as successful
            execution_log.status = "success"
            execution_log.completed_at = datetime.utcnow()
            execution_log.output_data = context
            
            # Update spiral stats
            spiral.last_run_at = datetime.utcnow()
            spiral.run_count += 1
            
        except Exception as e:
            # Mark as failed
            execution_log.status = "failed"
            execution_log.completed_at = datetime.utcnow()
            execution_log.error_message = str(e)
            
            logger.error(f"Spiral execution failed: {str(e)}")
            
            # Send failure notification
            log_url = f"{settings.FRONTEND_URL}/spirals/{spiral.id}/logs/{execution_log.id}"
            email_service.send_execution_failure_alert(
                user.email,
                spiral.name,
                str(e),
                log_url
            )
        
        db.commit()
        db.refresh(execution_log)
        
        return execution_log
    
    @staticmethod
    async def _execute_action(action: Action, context: Dict[str, Any]) -> Any:
        """Execute a single action"""
        
        action_type = action.action_type
        config = action.config
        
        if action_type == "http_request":
            return await ExecutionService._execute_http_request(config, context)
        
        elif action_type == "email":
            return await ExecutionService._execute_email(config, context)
        
        elif action_type == "transform":
            return await ExecutionService._execute_transform(config, context)
        
        elif action_type == "ai_call":
            return await ExecutionService._execute_ai_call(config, context)
        
        elif action_type == "delay":
            return await ExecutionService._execute_delay(config)
        
        else:
            raise ValueError(f"Unknown action type: {action_type}")
    
    @staticmethod
    async def _execute_http_request(config: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute HTTP request action"""
        
        method = config.get("method", "GET").upper()
        url = config.get("url")
        headers = config.get("headers", {})
        body = config.get("body")
        
        # Replace variables in URL and body
        url = ExecutionService._replace_variables(url, context)
        if body:
            body = ExecutionService._replace_variables(body, context)
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            if method == "GET":
                response = await client.get(url, headers=headers)
            elif method == "POST":
                response = await client.post(url, headers=headers, json=body)
            elif method == "PUT":
                response = await client.put(url, headers=headers, json=body)
            elif method == "DELETE":
                response = await client.delete(url, headers=headers)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            response.raise_for_status()
            
            return {
                "status_code": response.status_code,
                "body": response.json() if response.headers.get("content-type", "").startswith("application/json") else response.text,
                "headers": dict(response.headers)
            }
    
    @staticmethod
    async def _execute_email(config: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute email action"""
        
        to_email = config.get("to")
        subject = config.get("subject")
        body = config.get("body")
        
        # Replace variables
        to_email = ExecutionService._replace_variables(to_email, context)
        subject = ExecutionService._replace_variables(subject, context)
        body = ExecutionService._replace_variables(body, context)
        
        success = email_service.send_email(to_email, subject, body)
        
        return {
            "success": success,
            "to": to_email,
            "subject": subject
        }
    
    @staticmethod
    async def _execute_transform(config: Dict[str, Any], context: Dict[str, Any]) -> Any:
        """Execute data transformation action"""
        
        operation = config.get("operation")
        
        if operation == "extract":
            # Extract specific fields from context
            source = config.get("source")
            fields = config.get("fields", [])
            data = context.get(source, {})
            return {field: data.get(field) for field in fields}
        
        elif operation == "filter":
            # Filter array based on condition
            source = config.get("source")
            condition = config.get("condition")
            data = context.get(source, [])
            # Simple filtering (can be enhanced)
            return [item for item in data if eval(condition, {"item": item})]
        
        elif operation == "map":
            # Transform each item in array
            source = config.get("source")
            mapping = config.get("mapping")
            data = context.get(source, [])
            return [ExecutionService._apply_mapping(item, mapping) for item in data]
        
        else:
            raise ValueError(f"Unknown transform operation: {operation}")
    
    @staticmethod
    async def _execute_ai_call(config: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute AI call action"""
        from anthropic import Anthropic
        from app.config import settings
        
        client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)
        
        prompt = config.get("prompt")
        model = config.get("model", "claude-3-sonnet-20240229")
        max_tokens = config.get("max_tokens", 1024)
        
        # Replace variables in prompt
        prompt = ExecutionService._replace_variables(prompt, context)
        
        message = client.messages.create(
            model=model,
            max_tokens=max_tokens,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return {
            "response": message.content[0].text,
            "model": model,
            "usage": {
                "input_tokens": message.usage.input_tokens,
                "output_tokens": message.usage.output_tokens
            }
        }
    
    @staticmethod
    async def _execute_delay(config: Dict[str, Any]) -> Dict[str, Any]:
        """Execute delay action"""
        import asyncio
        
        seconds = config.get("seconds", 1)
        await asyncio.sleep(seconds)
        
        return {"delayed": seconds}
    
    @staticmethod
    def _replace_variables(text: str, context: Dict[str, Any]) -> str:
        """Replace {{variable}} placeholders with context values"""
        import re
        
        if not isinstance(text, str):
            return text
        
        def replacer(match):
            var_name = match.group(1)
            # Support nested access like {{input.name}}
            parts = var_name.split(".")
            value = context
            for part in parts:
                if isinstance(value, dict):
                    value = value.get(part)
                else:
                    return match.group(0)  # Return original if not found
            return str(value) if value is not None else match.group(0)
        
        return re.sub(r'\{\{([^}]+)\}\}', replacer, text)
    
    @staticmethod
    def _apply_mapping(item: Any, mapping: Dict[str, str]) -> Dict[str, Any]:
        """Apply field mapping to an item"""
        result = {}
        for new_key, old_key in mapping.items():
            if isinstance(item, dict):
                result[new_key] = item.get(old_key)
            else:
                result[new_key] = getattr(item, old_key, None)
        return result


# Import settings at the end to avoid circular import
from app.config import settings