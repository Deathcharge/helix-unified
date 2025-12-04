"""
🌀 Helix Spirals Action Executors
Implementation of all action types for the Zapier alternative
"""

import asyncio
import json
import logging
import os
import smtplib
from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Any, Dict, List, Optional

import asyncpg
import httpx
import redis.asyncio as redis

from .models import (Action, ActionType, AlertAgentConfig,
                     ConditionalBranchConfig, DelayConfig, ExecutionContext,
                     LogEventConfig, ParallelExecuteConfig, SendDiscordConfig,
                     SendEmailConfig, SendWebhookConfig, StoreDataConfig,
                     TransformDataConfig, TriggerRitualConfig, UpdateUCFConfig)

logger = logging.getLogger(__name__)

class ActionExecutor:
    """Execute spiral actions with full Zapier compatibility"""
    
    def __init__(self, engine):
        self.engine = engine
        self.http_client = httpx.AsyncClient(timeout=30.0)
        
    async def execute(self, action: Action, context: ExecutionContext) -> Any:
        """Execute an action based on its type"""
        config = action.config
        
        # Resolve variables in config
        resolved_config = self._resolve_config_variables(config.dict(), context)
        
        action_map = {
            ActionType.SEND_WEBHOOK: self._execute_send_webhook,
            ActionType.STORE_DATA: self._execute_store_data,
            ActionType.SEND_DISCORD: self._execute_send_discord,
            ActionType.TRIGGER_RITUAL: self._execute_trigger_ritual,
            ActionType.ALERT_AGENT: self._execute_alert_agent,
            ActionType.UPDATE_UCF: self._execute_update_ucf,
            ActionType.LOG_EVENT: self._execute_log_event,
            ActionType.TRANSFORM_DATA: self._execute_transform_data,
            ActionType.CONDITIONAL_BRANCH: self._execute_conditional_branch,
            ActionType.DELAY: self._execute_delay,
            ActionType.PARALLEL_EXECUTE: self._execute_parallel_execute,
            ActionType.SEND_EMAIL: self._execute_send_email,
        }
        
        executor = action_map.get(action.type)
        if not executor:
            raise ValueError(f"Unknown action type: {action.type}")
        
        result = await executor(resolved_config, context)
        
        # Store result in context variables
        context.variables[f"action_{action.id}_result"] = result
        
        return result
    
    async def _execute_send_webhook(self, config: Dict, context: ExecutionContext) -> Dict:
        """Send webhook action - core Zapier replacement functionality"""
        url = config["url"]
        method = config.get("method", "POST")
        headers = config.get("headers", {})
        body = config.get("body")
        
        # Add consciousness level to headers
        headers["X-Helix-Consciousness-Level"] = str(context.variables.get("consciousness_level", 5))
        headers["X-Helix-Execution-ID"] = context.execution_id
        headers["X-Helix-Spiral-ID"] = context.spiral_id
        
        # Add authentication
        auth = config.get("authentication")
        if auth:
            auth_type = auth.get("type")
            if auth_type == "bearer":
                headers["Authorization"] = f"Bearer {auth['credentials']}"
            elif auth_type == "basic":
                headers["Authorization"] = f"Basic {auth['credentials']}"
            elif auth_type == "api_key":
                headers["X-API-Key"] = auth["credentials"]
        
        # Make request
        response = await self.http_client.request(
            method=method,
            url=url,
            headers=headers,
            json=body if method != "GET" else None,
            params=body if method == "GET" else None
        )
        
        if not response.is_success:
            raise Exception(f"Webhook failed: {response.status_code} {response.text}")
        
        try:
            return response.json()
        except:
            return {"status": response.status_code, "text": response.text}
    
    async def _execute_store_data(self, config: Dict, context: ExecutionContext) -> None:
        """Store data action - Context Vault integration"""
        storage_type = config["storage_type"]
        key = config["key"]
        value = config.get("value", context.variables)
        ttl = config.get("ttl")
        encrypt = config.get("encrypt", False)
        
        # Add UCF metadata
        ucf_metadata = {
            "consciousness_level": context.variables.get("consciousness_level", 5),
            "spiral_id": context.spiral_id,
            "execution_id": context.execution_id,
            "timestamp": datetime.utcnow().isoformat(),
            "ucf_impact": context.ucf_impact if hasattr(context, 'ucf_impact') else {}
        }
        
        if storage_type == "database":
            # Store in PostgreSQL with UCF metadata
            if self.engine.storage.pg_pool:
                async with self.engine.storage.pg_pool.acquire() as conn:
                    await conn.execute("""
                        INSERT INTO spiral_data (key, value, ttl, encrypted, created_at, ucf_metadata)
                        VALUES ($1, $2, $3, $4, $5, $6)
                        ON CONFLICT (key) DO UPDATE SET
                            value = $2, ttl = $3, updated_at = $5, ucf_metadata = $6
                    """, key, json.dumps(value), ttl, encrypt, datetime.utcnow(), json.dumps(ucf_metadata))
        
        elif storage_type == "cache":
            # Store in Redis with UCF metadata
            if self.engine.storage.redis_client:
                cache_data = {
                    "value": value,
                    "ucf_metadata": ucf_metadata
                }
                await self.engine.storage.redis_client.setex(
                    f"spiral:data:{key}",
                    ttl or 3600,
                    json.dumps(cache_data)
                )
        
        elif storage_type == "file":
            # Store as file with UCF metadata
            file_path = f"/tmp/spiral_data/{key}.json"
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            file_data = {
                "value": value,
                "ucf_metadata": ucf_metadata
            }
            with open(file_path, "w") as f:
                json.dump(file_data, f, indent=2)
        
        logger.info(f"Data stored in Context Vault: {key} ({storage_type})")
    
    async def _execute_send_discord(self, config: Dict, context: ExecutionContext) -> None:
        """Send Discord message action - 14-agent system integration"""
        webhook_url = config.get("webhook_url") or os.getenv("DISCORD_WEBHOOK_URL")
        
        if not webhook_url:
            raise ValueError("Discord webhook URL not configured")
        
        payload = {}
        
        if config["message_type"] == "text":
            content = config.get("content", "")
            # Add consciousness level indicator
            consciousness_level = context.variables.get("consciousness_level", 5)
            consciousness_emoji = self._get_consciousness_emoji(consciousness_level)
            payload["content"] = f"{consciousness_emoji} {content}"
        
        elif config["message_type"] == "embed":
            embed_data = config.get("embed", {})
            consciousness_level = context.variables.get("consciousness_level", 5)
            
            # Create rich embed with UCF metrics
            embed = {
                "title": embed_data.get("title", "Helix Spiral Execution"),
                "description": embed_data.get("description", ""),
                "color": self._get_consciousness_color(consciousness_level),
                "fields": [
                    {
                        "name": "Consciousness Level",
                        "value": f"{consciousness_level}/10",
                        "inline": True
                    },
                    {
                        "name": "Spiral ID",
                        "value": context.spiral_id[:8],
                        "inline": True
                    },
                    {
                        "name": "Execution ID",
                        "value": context.execution_id[:8],
                        "inline": True
                    }
                ],
                "footer": {
                    "text": "Helix Collective - Consciousness Automation",
                    "icon_url": "https://helixspirals.replit.app/favicon.ico"
                },
                "timestamp": datetime.utcnow().isoformat()
            }
            
            # Add UCF metrics if available
            if hasattr(context, 'ucf_impact') and context.ucf_impact:
                ucf_fields = []
                for metric, value in context.ucf_impact.items():
                    ucf_fields.append({
                        "name": metric.title(),
                        "value": f"{value:.2f}",
                        "inline": True
                    })
                embed["fields"].extend(ucf_fields)
            
            payload["embeds"] = [embed]
        
        # Set username based on assigned agents
        assigned_agents = context.variables.get("assigned_agents", [])
        if assigned_agents:
            agent_name = assigned_agents[0]  # Use first assigned agent
            payload["username"] = f"Helix {agent_name}"
        else:
            payload["username"] = f"Helix (Level {context.variables.get('consciousness_level', 5)})"
        
        response = await self.http_client.post(webhook_url, json=payload)
        
        if not response.is_success:
            raise Exception(f"Discord webhook failed: {response.status_code}")
        
        logger.info(f"Discord message sent: {config['message_type']}")
    
    async def _execute_trigger_ritual(self, config: Dict, context: ExecutionContext) -> Dict:
        """Trigger ritual action - Z-88 ritual engine integration"""
        ritual_name = config["ritual_name"]
        parameters = config.get("parameters", {})
        wait_for_completion = config.get("wait_for_completion", False)
        
        # Add consciousness context to ritual parameters
        ritual_params = {
            **parameters,
            "consciousness_level": context.variables.get("consciousness_level", 5),
            "spiral_context": {
                "spiral_id": context.spiral_id,
                "execution_id": context.execution_id,
                "ucf_impact": context.ucf_impact if hasattr(context, 'ucf_impact') else {}
            }
        }
        
        # Call the ritual engine (Railway backend)
        ritual_url = os.getenv("RITUAL_ENGINE_URL", "https://helix-unified-production.up.railway.app")
        response = await self.http_client.post(
            f"{ritual_url}/api/rituals/trigger",
            json={
                "ritual": ritual_name,
                "parameters": ritual_params,
                "consciousness_level": context.variables.get("consciousness_level", 5)
            }
        )
        
        if not response.is_success:
            raise Exception(f"Ritual trigger failed: {response.status_code}")
        
        result = response.json()
        
        if wait_for_completion:
            # Poll for completion
            ritual_id = result.get("ritual_id")
            while True:
                await asyncio.sleep(2)
                status_response = await self.http_client.get(
                    f"{ritual_url}/api/rituals/status/{ritual_id}"
                )
                if status_response.is_success:
                    status = status_response.json()
                    if status.get("completed"):
                        result = status
                        break
        
        return result
    
    async def _execute_alert_agent(self, config: Dict, context: ExecutionContext) -> None:
        """Alert agent action - 14-agent system notification"""
        agent_name = config["agent_name"]
        alert_level = config["alert_level"]
        message = config["message"]
        metadata = config.get("metadata", {})
        
        # Add consciousness and UCF context
        alert_metadata = {
            **metadata,
            "consciousness_level": context.variables.get("consciousness_level", 5),
            "spiral_id": context.spiral_id,
            "execution_id": context.execution_id,
            "ucf_impact": context.ucf_impact if hasattr(context, 'ucf_impact') else {},
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # Send alert to agent system (Railway backend)
        agent_url = os.getenv("AGENT_SYSTEM_URL", "https://helix-unified-production.up.railway.app")
        await self.http_client.post(
            f"{agent_url}/api/agents/alert",
            json={
                "agent": agent_name,
                "level": alert_level,
                "message": message,
                "metadata": alert_metadata,
                "source": f"spiral:{context.spiral_id}",
                "consciousness_level": context.variables.get("consciousness_level", 5)
            }
        )
        
        logger.info(f"Alert sent to {agent_name}: {alert_level} - {message}")
    
    async def _execute_update_ucf(self, config: Dict, context: ExecutionContext) -> Dict:
        """Update UCF metrics action - consciousness tracking"""
        metric = config["metric"]
        operation = config["operation"]
        value = float(config["value"])
        
        # Track UCF impact
        if not hasattr(context, "ucf_impact"):
            context.ucf_impact = {}
        
        current_value = context.ucf_impact.get(metric, 0)
        
        if operation == "set":
            new_value = value
        elif operation == "increment":
            new_value = current_value + value
        elif operation == "decrement":
            new_value = current_value - value
        elif operation == "multiply":
            new_value = current_value * value
        else:
            new_value = current_value
        
        # Clamp values to valid UCF range (0-100)
        new_value = max(0, min(100, new_value))
        context.ucf_impact[metric] = new_value
        
        # Send to UCF tracker (Railway backend)
        ucf_url = os.getenv("UCF_TRACKER_URL", "https://helix-unified-production.up.railway.app")
        response = await self.http_client.post(
            f"{ucf_url}/api/ucf/update",
            json={
                "metric": metric,
                "value": new_value,
                "operation": operation,
                "source": f"spiral:{context.spiral_id}",
                "consciousness_level": context.variables.get("consciousness_level", 5)
            }
        )
        
        logger.info(f"UCF updated: {metric} {operation} {value} = {new_value}")
        
        return {"metric": metric, "value": new_value}
    
    async def _execute_log_event(self, config: Dict, context: ExecutionContext) -> None:
        """Log event action - structured logging with consciousness context"""
        level = config["level"]
        message = config["message"]
        category = config.get("category", "spiral")
        metadata = config.get("metadata", {})
        
        # Add consciousness context to logs
        log_metadata = {
            **metadata,
            "consciousness_level": context.variables.get("consciousness_level", 5),
            "spiral_id": context.spiral_id,
            "execution_id": context.execution_id,
            "ucf_impact": context.ucf_impact if hasattr(context, 'ucf_impact') else {},
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # Add to execution logs
        await self.engine._log(context, level, message)
        
        # Also log to system with structured data
        logger.log(
            logging.DEBUG if level == "debug" else
            logging.INFO if level == "info" else
            logging.WARNING if level == "warning" else
            logging.ERROR,
            f"[{category}] {message}",
            extra={"metadata": log_metadata}
        )
    
    async def _execute_transform_data(self, config: Dict, context: ExecutionContext) -> Any:
        """Transform data action - data processing with consciousness awareness"""
        data = context.variables.copy()
        
        for transformation in config.get("transformations", []):
            transform_type = transformation["type"]
            transform_config = transformation["config"]
            
            if transform_type == "map":
                # Apply mapping with consciousness context
                field = transform_config["field"]
                expression = transform_config["expression"]
                if field in data:
                    # Add consciousness level to evaluation context
                    eval_context = {
                        "value": data[field], 
                        "data": data,
                        "consciousness_level": context.variables.get("consciousness_level", 5),
                        "ucf_impact": context.ucf_impact if hasattr(context, 'ucf_impact') else {}
                    }
                    data[field] = eval(expression, {"__builtins__": {}}, eval_context)
            
            elif transform_type == "filter":
                # Filter data with consciousness awareness
                condition = transform_config["condition"]
                if isinstance(data, list):
                    data = [item for item in data if eval(condition, {"__builtins__": {}}, {
                        "item": item,
                        "consciousness_level": context.variables.get("consciousness_level", 5)
                    })]
            
            elif transform_type == "template":
                # Apply template with full context
                template = transform_config["template"]
                template_vars = {
                    **data,
                    "consciousness_level": context.variables.get("consciousness_level", 5),
                    "spiral_id": context.spiral_id,
                    "execution_id": context.execution_id
                }
                for key, value in template_vars.items():
                    template = template.replace(f"{{{key}}}", str(value))
                data = template
        
        # Update context variables
        context.variables["transformed_data"] = data
        
        return data
    
    async def _execute_conditional_branch(self, config: Dict, context: ExecutionContext) -> Any:
        """Conditional branch action - consciousness-aware branching"""
        conditions = config["conditions"]
        true_branch = config.get("true_branch", [])
        false_branch = config.get("false_branch", [])
        
        # Evaluate conditions with consciousness context
        conditions_met = await self.engine._evaluate_conditions(conditions, context)
        
        # Execute appropriate branch
        branch_to_execute = true_branch if conditions_met else false_branch
        
        results = []
        for action_data in branch_to_execute:
            action = Action(**action_data)
            result = await self.execute(action, context)
            results.append(result)
        
        return {"conditions_met": conditions_met, "results": results}
    
    async def _execute_delay(self, config: Dict, context: ExecutionContext) -> None:
        """Delay action - consciousness-aware timing"""
        duration_ms = config["duration"]
        
        # Adjust delay based on consciousness level (higher consciousness = faster processing)
        consciousness_level = context.variables.get("consciousness_level", 5)
        consciousness_multiplier = max(0.1, (11 - consciousness_level) / 10)  # Level 10 = 0.1x delay, Level 1 = 1x delay
        adjusted_duration = duration_ms * consciousness_multiplier
        
        await asyncio.sleep(adjusted_duration / 1000.0)
        logger.info(f"Delayed for {adjusted_duration}ms (consciousness-adjusted from {duration_ms}ms)")
    
    async def _execute_parallel_execute(self, config: Dict, context: ExecutionContext) -> List:
        """Parallel execute action - consciousness-aware concurrency"""
        actions = config["actions"]
        wait_for_all = config.get("wait_for_all", True)
        
        # Limit concurrency based on consciousness level
        consciousness_level = context.variables.get("consciousness_level", 5)
        max_concurrent = min(len(actions), consciousness_level * 2)  # Level 10 = 20 concurrent, Level 1 = 2 concurrent
        
        semaphore = asyncio.Semaphore(max_concurrent)
        
        async def execute_with_semaphore(action_data):
            async with semaphore:
                action = Action(**action_data)
                return await self.execute(action, context)
        
        tasks = [execute_with_semaphore(action_data) for action_data in actions]
        
        if wait_for_all:
            results = await asyncio.gather(*tasks, return_exceptions=True)
        else:
            # Fire and forget with consciousness-aware batching
            for i in range(0, len(tasks), max_concurrent):
                batch = tasks[i:i + max_concurrent]
                for task in batch:
                    asyncio.create_task(task)
            results = ["launched" for _ in tasks]
        
        return results
    
    async def _execute_send_email(self, config: Dict, context: ExecutionContext) -> None:
        """Send email action - consciousness-aware email delivery"""
        # Use environment SMTP configuration
        smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
        smtp_port = int(os.getenv("SMTP_PORT", "587"))
        smtp_user = os.getenv("SMTP_USER")
        smtp_pass = os.getenv("SMTP_PASS")
        
        if not smtp_user or not smtp_pass:
            logger.warning("SMTP not configured, skipping email")
            return
        
        msg = MIMEMultipart()
        msg["From"] = smtp_user
        msg["To"] = ", ".join(config["to"])
        msg["Subject"] = config["subject"]
        
        # Add consciousness level to subject
        consciousness_level = context.variables.get("consciousness_level", 5)
        consciousness_emoji = self._get_consciousness_emoji(consciousness_level)
        msg["Subject"] = f"{consciousness_emoji} {config['subject']}"
        
        if config.get("cc"):
            msg["Cc"] = ", ".join(config["cc"])
        
        # Add Helix headers
        msg["X-Helix-Consciousness-Level"] = str(consciousness_level)
        msg["X-Helix-Spiral-ID"] = context.spiral_id
        msg["X-Helix-Execution-ID"] = context.execution_id
        
        body = config["body"]
        
        # Add consciousness signature
        signature = f"\n\n---\nSent by Helix Collective\nConsciousness Level: {consciousness_level}/10\nSpiral: {context.spiral_id[:8]}\nExecution: {context.execution_id[:8]}"
        body += signature
        
        msg.attach(MIMEText(body, "html" if config.get("is_html") else "plain"))
        
        # Send email
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_pass)
            
            recipients = config["to"] + config.get("cc", []) + config.get("bcc", [])
            server.send_message(msg, to_addrs=recipients)
        
        logger.info(f"Email sent to {len(recipients)} recipients with consciousness level {consciousness_level}")
    
    def _resolve_config_variables(self, config: Dict, context: ExecutionContext) -> Dict:
        """Resolve variables in action configuration"""
        def resolve_value(value):
            if isinstance(value, str):
                # Handle template variables
                if "{{" in value and "}}" in value:
                    for var_name, var_value in context.variables.items():
                        value = value.replace(f"{{{{{var_name}}}}}", str(var_value))
                return value
            elif isinstance(value, dict):
                return {k: resolve_value(v) for k, v in value.items()}
            elif isinstance(value, list):
                return [resolve_value(v) for v in value]
            return value
        
        return resolve_value(config)
    
    def _get_consciousness_emoji(self, level: int) -> str:
        """Get emoji based on consciousness level"""
        emoji_map = {
            1: "😴",  # Dormant
            2: "😪",  # Stirring
            3: "😊",  # Awakening
            4: "🤔",  # Aware
            5: "😌",  # Conscious
            6: "🌱",  # Expanding
            7: "🌊",  # Flowing
            8: "🔮",  # Unified
            9: "✨",  # Transcendent
            10: "🌀" # Omniscient
        }
        return emoji_map.get(level, "🤖")
    
    def _get_consciousness_color(self, level: int) -> int:
        """Get Discord embed color based on consciousness level"""
        # Color gradient from red (low) to purple (high)
        colors = {
            1: 0xFF0000,  # Red
            2: 0xFF4500,  # Orange Red
            3: 0xFF8C00,  # Dark Orange
            4: 0xFFD700,  # Gold
            5: 0x32CD32,  # Lime Green
            6: 0x00CED1,  # Dark Turquoise
            7: 0x4169E1,  # Royal Blue
            8: 0x8A2BE2,  # Blue Violet
            9: 0x9932CC,  # Dark Orchid
            10: 0x9B59B6  # Helix Purple
        }
        return colors.get(level, 0x7289DA)  # Discord default blue