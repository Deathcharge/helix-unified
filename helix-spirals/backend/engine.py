"""
🌀 Helix Spirals Execution Engine
Core execution logic for automation workflows
"""

import asyncio
import logging
import json
from datetime import datetime
from typing import Dict, List, Optional, Any
from uuid import uuid4

from .models import (
    Spiral, Action, Trigger, ExecutionContext, ExecutionStatus,
    ExecutionLog, ExecutionError, Condition, ConditionOperator,
    TriggerType, ActionType
)
from .actions import ActionExecutor
from .storage import SpiralStorage

logger = logging.getLogger(__name__)

class RateLimiter:
    """Rate limiter for spiral execution"""
    def __init__(self, max_executions: int, window_ms: int, strategy: str = "sliding"):
        self.max_executions = max_executions
        self.window_ms = window_ms
        self.strategy = strategy
        self.executions: List[float] = []
    
    def allow(self) -> bool:
        """Check if execution is allowed"""
        now = datetime.utcnow().timestamp() * 1000
        cutoff = now - self.window_ms
        
        # Remove old executions
        self.executions = [e for e in self.executions if e > cutoff]
        
        if len(self.executions) >= self.max_executions:
            return False
        
        self.executions.append(now)
        return True

class SpiralEngine:
    """Main execution engine for Helix Spirals"""
    
    def __init__(self, storage: SpiralStorage, ws_manager=None):
        self.storage = storage
        self.ws_manager = ws_manager
        self.action_executor = ActionExecutor(self)
        self.execution_queue: Dict[str, ExecutionContext] = {}
        self.rate_limiters: Dict[str, RateLimiter] = {}
        self.active_executions: Dict[str, asyncio.Task] = {}
        
    async def execute(
        self,
        spiral_id: str,
        trigger_type: str,
        trigger_data: Dict[str, Any],
        metadata: Optional[Dict[str, Any]] = None
    ) -> ExecutionContext:
        """Execute a spiral"""
        try:
            # Get spiral
            spiral = await self.storage.get_spiral(spiral_id)
            if not spiral:
                raise ValueError(f"Spiral {spiral_id} not found")
            
            if not spiral.enabled:
                raise ValueError(f"Spiral {spiral_id} is disabled")
            
            # Check rate limiting
            if spiral.rate_limiting:
                limiter = self._get_rate_limiter(spiral_id, spiral.rate_limiting)
                if not limiter.allow():
                    raise ValueError(f"Rate limit exceeded for spiral {spiral_id}")
            
            # Create execution context
            context = ExecutionContext(
                spiral_id=spiral_id,
                execution_id=str(uuid4()),
                trigger={
                    "type": trigger_type,
                    "data": trigger_data,
                    "timestamp": datetime.utcnow().isoformat()
                },
                variables=self._initialize_variables(spiral, trigger_data),
                status=ExecutionStatus.PENDING
            )
            
            # Store in queue
            self.execution_queue[context.execution_id] = context
            
            # Execute spiral asynchronously
            task = asyncio.create_task(self._execute_spiral(spiral, context))
            self.active_executions[context.execution_id] = task
            
            # Wait briefly to get initial status
            await asyncio.sleep(0.1)
            
            return context
            
        except Exception as e:
            logger.error(f"Failed to execute spiral {spiral_id}: {e}")
            raise
    
    async def _execute_spiral(self, spiral: Spiral, context: ExecutionContext) -> ExecutionContext:
        """Internal spiral execution logic"""
        try:
            context.status = ExecutionStatus.RUNNING
            await self._log(context, "info", f"Starting spiral execution: {spiral.name}")
            
            # Broadcast execution start
            if self.ws_manager:
                await self.ws_manager.broadcast({
                    "type": "execution_started",
                    "spiralId": context.spiral_id,
                    "executionId": context.execution_id,
                    "timestamp": context.started_at
                })
            
            # Validate trigger conditions
            if spiral.trigger.conditions:
                conditions_met = await self._evaluate_conditions(
                    spiral.trigger.conditions, context
                )
                if not conditions_met:
                    await self._log(context, "info", "Trigger conditions not met, skipping execution")
                    context.status = ExecutionStatus.COMPLETED
                    context.completed_at = datetime.utcnow().isoformat()
                    return context
            
            # Execute actions
            for action in spiral.actions:
                context.current_action = action.id
                
                # Check action conditions
                if action.conditions:
                    conditions_met = await self._evaluate_conditions(
                        action.conditions, context
                    )
                    if not conditions_met:
                        await self._log(context, "info", f"Skipping action {action.name}: conditions not met")
                        continue
                
                # Execute action with retry logic
                await self._execute_action_with_retry(action, context)
                
                # Handle continue on error
                if context.status == ExecutionStatus.FAILED and not action.continue_on_error:
                    break
            
            # Mark as completed if not failed
            if context.status != ExecutionStatus.FAILED:
                context.status = ExecutionStatus.COMPLETED
            
            context.completed_at = datetime.utcnow().isoformat()
            await self._log(context, "info", f"Spiral execution completed: {spiral.name}")
            
            # Update statistics
            await self.storage.update_spiral_statistics(spiral.id, context)
            
            # Calculate UCF impact
            if hasattr(context, "ucf_impact") and context.ucf_impact:
                await self._update_ucf_metrics(context.ucf_impact)
            
            # Broadcast completion
            if self.ws_manager:
                await self.ws_manager.broadcast({
                    "type": "execution_completed",
                    "spiralId": context.spiral_id,
                    "executionId": context.execution_id,
                    "status": context.status.value,
                    "timestamp": context.completed_at
                })
            
        except Exception as e:
            context.status = ExecutionStatus.FAILED
            context.error = ExecutionError(
                message=str(e),
                action_id=context.current_action
            )
            context.completed_at = datetime.utcnow().isoformat()
            await self._log(context, "error", f"Spiral execution failed: {str(e)}")
            
            # Broadcast failure
            if self.ws_manager:
                await self.ws_manager.broadcast({
                    "type": "execution_failed",
                    "spiralId": context.spiral_id,
                    "executionId": context.execution_id,
                    "error": str(e),
                    "timestamp": context.completed_at
                })
            
        finally:
            # Clean up
            self.execution_queue.pop(context.execution_id, None)
            self.active_executions.pop(context.execution_id, None)
            
            # Store execution history
            await self.storage.save_execution_history(context)
        
        return context
    
    async def _execute_action_with_retry(self, action: Action, context: ExecutionContext):
        """Execute action with retry logic"""
        max_attempts = action.retry_config.max_attempts if action.retry_config else 1
        last_error = None
        
        for attempt in range(1, max_attempts + 1):
            try:
                await self._log(context, "info", f"Executing action {action.name} (attempt {attempt}/{max_attempts})")
                
                # Set timeout if specified
                if action.timeout:
                    await asyncio.wait_for(
                        self.action_executor.execute(action, context),
                        timeout=action.timeout / 1000.0  # Convert ms to seconds
                    )
                else:
                    await self.action_executor.execute(action, context)
                
                await self._log(context, "info", f"Action {action.name} completed successfully")
                return
                
            except asyncio.TimeoutError:
                last_error = "Action timeout"
                await self._log(context, "error", f"Action {action.name} timed out")
                
            except Exception as e:
                last_error = str(e)
                await self._log(context, "error", f"Action {action.name} failed: {str(e)}")
            
            if attempt < max_attempts:
                delay = self._calculate_retry_delay(attempt, action.retry_config)
                await self._log(context, "info", f"Retrying action {action.name} in {delay}ms")
                await asyncio.sleep(delay / 1000.0)
        
        # All retries failed
        if last_error and not action.continue_on_error:
            raise Exception(last_error)
    
    async def _evaluate_conditions(self, conditions: List[Condition], context: ExecutionContext) -> bool:
        """Evaluate conditions"""
        for condition in conditions:
            result = await self._evaluate_condition(condition, context)
            
            # Handle logical operators
            if condition.logical_operator == "OR" and result:
                return True
            if condition.logical_operator == "AND" and not result:
                return False
            
            # Handle nested conditions
            if condition.nested_conditions:
                nested_result = await self._evaluate_conditions(
                    condition.nested_conditions, context
                )
                if condition.logical_operator == "OR" and nested_result:
                    return True
                if condition.logical_operator == "AND" and not nested_result:
                    return False
        
        return True
    
    async def _evaluate_condition(self, condition: Condition, context: ExecutionContext) -> bool:
        """Evaluate single condition"""
        field_value = self._get_field_value(condition.field, context)
        condition_value = self._resolve_variable(condition.value, context)
        
        operator_map = {
            ConditionOperator.EQUALS: lambda a, b: a == b,
            ConditionOperator.NOT_EQUALS: lambda a, b: a != b,
            ConditionOperator.GREATER_THAN: lambda a, b: float(a) > float(b),
            ConditionOperator.LESS_THAN: lambda a, b: float(a) < float(b),
            ConditionOperator.CONTAINS: lambda a, b: str(b) in str(a),
            ConditionOperator.STARTS_WITH: lambda a, b: str(a).startswith(str(b)),
            ConditionOperator.ENDS_WITH: lambda a, b: str(a).endswith(str(b)),
            ConditionOperator.REGEX_MATCH: lambda a, b: bool(__import__('re').match(b, str(a))),
            ConditionOperator.IN_LIST: lambda a, b: a in b if isinstance(b, list) else False,
            ConditionOperator.IS_NULL: lambda a, b: a is None,
            ConditionOperator.IS_NOT_NULL: lambda a, b: a is not None,
        }
        
        evaluator = operator_map.get(condition.operator)
        if not evaluator:
            return False
        
        try:
            return evaluator(field_value, condition_value)
        except:
            return False
    
    def _initialize_variables(self, spiral: Spiral, trigger_data: Dict[str, Any]) -> Dict[str, Any]:
        """Initialize execution variables"""
        variables = {
            "trigger": trigger_data,
            "spiral": {
                "id": spiral.id,
                "name": spiral.name,
                "version": spiral.version
            },
            "execution": {
                "id": str(uuid4()),
                "timestamp": datetime.utcnow().isoformat()
            },
            "consciousness_level": spiral.consciousness_level.value if spiral.consciousness_level else 5
        }
        
        # Add default variables
        if spiral.variables:
            for var in spiral.variables:
                if var.default_value is not None:
                    variables[var.name] = var.default_value
        
        return variables
    
    def _get_field_value(self, field: str, context: ExecutionContext) -> Any:
        """Get field value from context using dot notation"""
        parts = field.split(".")
        value = context.dict()
        
        for part in parts:
            if isinstance(value, dict):
                value = value.get(part)
            else:
                return None
        
        return value
    
    def _resolve_variable(self, value: Any, context: ExecutionContext) -> Any:
        """Resolve variables in value"""
        if isinstance(value, str) and value.startswith("{{") and value.endswith("}}"):
            var_name = value[2:-2].strip()
            return context.variables.get(var_name, value)
        elif isinstance(value, dict):
            return {k: self._resolve_variable(v, context) for k, v in value.items()}
        elif isinstance(value, list):
            return [self._resolve_variable(v, context) for v in value]
        return value
    
    def _get_rate_limiter(self, spiral_id: str, config: Dict[str, Any]) -> RateLimiter:
        """Get or create rate limiter for spiral"""
        if spiral_id not in self.rate_limiters:
            self.rate_limiters[spiral_id] = RateLimiter(
                config.max_executions,
                config.window_ms,
                config.strategy
            )
        return self.rate_limiters[spiral_id]
    
    def _calculate_retry_delay(self, attempt: int, config) -> int:
        """Calculate retry delay based on strategy"""
        if not config:
            return 1000
        
        base_delay = config.initial_delay
        
        if config.backoff_strategy == "fixed":
            delay = base_delay
        elif config.backoff_strategy == "linear":
            delay = base_delay * attempt
        elif config.backoff_strategy == "exponential":
            delay = base_delay * (2 ** (attempt - 1))
        else:
            delay = base_delay
        
        if config.max_delay:
            delay = min(delay, config.max_delay)
        
        return delay
    
    async def _log(self, context: ExecutionContext, level: str, message: str):
        """Add log entry to execution context"""
        log_entry = ExecutionLog(
            timestamp=datetime.utcnow().isoformat(),
            level=level,
            message=message,
            action_id=context.current_action
        )
        context.logs.append(log_entry)
        logger.log(logging.INFO if level == "info" else logging.ERROR, f"[{context.execution_id}] {message}")
    
    async def _update_ucf_metrics(self, ucf_impact: Dict[str, float]):
        """Update UCF metrics based on execution impact"""
        # This would integrate with the existing UCF system
        logger.info(f"UCF Impact: {ucf_impact}")
    
    async def cancel_execution(self, execution_id: str) -> bool:
        """Cancel a running execution"""
        if execution_id in self.active_executions:
            task = self.active_executions[execution_id]
            task.cancel()
            
            if execution_id in self.execution_queue:
                context = self.execution_queue[execution_id]
                context.status = ExecutionStatus.CANCELLED
                context.completed_at = datetime.utcnow().isoformat()
                await self.storage.save_execution_history(context)
            
            return True
        return False
    
    async def get_active_executions(self) -> List[ExecutionContext]:
        """Get all active executions"""
        return list(self.execution_queue.values())
    
    async def get_execution_status(self, execution_id: str) -> Optional[ExecutionContext]:
        """Get execution status"""
        if execution_id in self.execution_queue:
            return self.execution_queue[execution_id]
        
        # Check history
        return await self.storage.get_execution_history(execution_id)