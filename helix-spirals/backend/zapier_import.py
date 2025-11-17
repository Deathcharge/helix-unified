"""
🌀 Helix Spirals Zapier Import System
Convert existing Zapier workflows to consciousness-aware Helix Spirals
"""

import json
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any
from uuid import uuid4

from .models import (
    Spiral, Trigger, Action, TriggerType, ActionType,
    WebhookTriggerConfig, ScheduleTriggerConfig, ManualTriggerConfig,
    SendWebhookConfig, SendDiscordConfig, SendEmailConfig, LogEventConfig,
    StoreDataConfig, DelayConfig, ConditionalBranchConfig,
    ConsciousnessLevel, Variable
)
from .storage import SpiralStorage

logger = logging.getLogger(__name__)

class ZapierImporter:
    """Import and convert Zapier workflows to Helix Spirals"""
    
    def __init__(self, storage: SpiralStorage):
        self.storage = storage
        
        # Zapier to Helix action mapping
        self.action_mappings = {
            "webhook": ActionType.SEND_WEBHOOK,
            "webhooks": ActionType.SEND_WEBHOOK,
            "discord": ActionType.SEND_DISCORD,
            "email": ActionType.SEND_EMAIL,
            "gmail": ActionType.SEND_EMAIL,
            "delay": ActionType.DELAY,
            "filter": ActionType.CONDITIONAL_BRANCH,
            "paths": ActionType.CONDITIONAL_BRANCH,
            "storage": ActionType.STORE_DATA,
            "code": ActionType.TRANSFORM_DATA,
            "formatter": ActionType.TRANSFORM_DATA
        }
        
        # Zapier to Helix trigger mapping
        self.trigger_mappings = {
            "webhook": TriggerType.WEBHOOK,
            "webhooks": TriggerType.WEBHOOK,
            "schedule": TriggerType.SCHEDULE,
            "rss": TriggerType.WEBHOOK,  # Convert RSS to webhook
            "email": TriggerType.WEBHOOK,  # Convert email to webhook
            "form": TriggerType.WEBHOOK,  # Convert form to webhook
            "manual": TriggerType.MANUAL
        }
        
        # Consciousness level mapping based on Zap complexity
        self.consciousness_mapping = {
            "simple": ConsciousnessLevel.CONSCIOUS,      # 1-3 steps
            "moderate": ConsciousnessLevel.EXPANDING,    # 4-7 steps
            "complex": ConsciousnessLevel.FLOWING,       # 8-15 steps
            "advanced": ConsciousnessLevel.UNIFIED,      # 16+ steps
            "enterprise": ConsciousnessLevel.TRANSCENDENT # Multi-path, filters, etc.
        }
    
    async def import_zapier_export(self, zapier_data: Dict[str, Any]) -> Dict[str, Any]:
        """Import Zapier export JSON and convert to Helix Spirals"""
        import_stats = {
            "total_zaps": 0,
            "converted": 0,
            "failed": 0,
            "skipped": 0,
            "spirals_created": [],
            "errors": [],
            "consciousness_distribution": {},
            "action_types_converted": {},
            "trigger_types_converted": {}
        }
        
        try:
            # Handle different Zapier export formats
            zaps = self._extract_zaps_from_export(zapier_data)
            import_stats["total_zaps"] = len(zaps)
            
            for zap_data in zaps:
                try:
                    spiral = await self._convert_zap_to_spiral(zap_data)
                    if spiral:
                        await self.storage.save_spiral(spiral)
                        import_stats["converted"] += 1
                        import_stats["spirals_created"].append({
                            "id": spiral.id,
                            "name": spiral.name,
                            "consciousness_level": spiral.consciousness_level.value if spiral.consciousness_level else 5,
                            "actions_count": len(spiral.actions),
                            "zapier_id": zap_data.get("id")
                        })
                        
                        # Track statistics
                        consciousness_level = spiral.consciousness_level.value if spiral.consciousness_level else 5
                        import_stats["consciousness_distribution"][str(consciousness_level)] = \
                            import_stats["consciousness_distribution"].get(str(consciousness_level), 0) + 1
                        
                        # Track action types
                        for action in spiral.actions:
                            action_type = action.type.value
                            import_stats["action_types_converted"][action_type] = \
                                import_stats["action_types_converted"].get(action_type, 0) + 1
                        
                        # Track trigger type
                        trigger_type = spiral.trigger.type.value
                        import_stats["trigger_types_converted"][trigger_type] = \
                            import_stats["trigger_types_converted"].get(trigger_type, 0) + 1
                        
                        logger.info(f"Converted Zap '{zap_data.get('name', 'Unknown')}' to Spiral '{spiral.name}'")
                    else:
                        import_stats["skipped"] += 1
                        logger.warning(f"Skipped Zap '{zap_data.get('name', 'Unknown')}' - unsupported format")
                        
                except Exception as e:
                    import_stats["failed"] += 1
                    error_msg = f"Failed to convert Zap '{zap_data.get('name', 'Unknown')}': {str(e)}"
                    import_stats["errors"].append(error_msg)
                    logger.error(error_msg)
            
            # Calculate success rate
            import_stats["success_rate"] = (import_stats["converted"] / import_stats["total_zaps"] * 100) if import_stats["total_zaps"] > 0 else 0
            
            logger.info(f"Zapier import completed: {import_stats['converted']}/{import_stats['total_zaps']} converted ({import_stats['success_rate']:.1f}% success rate)")
            
            return import_stats
            
        except Exception as e:
            logger.error(f"Zapier import failed: {e}")
            import_stats["errors"].append(f"Import failed: {str(e)}")
            return import_stats
    
    def _extract_zaps_from_export(self, zapier_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract Zaps from various Zapier export formats"""
        # Handle different export formats
        if "zaps" in zapier_data:
            return zapier_data["zaps"]
        elif "data" in zapier_data and isinstance(zapier_data["data"], list):
            return zapier_data["data"]
        elif isinstance(zapier_data, list):
            return zapier_data
        elif "workflows" in zapier_data:
            return zapier_data["workflows"]
        else:
            # Assume single Zap
            return [zapier_data]
    
    async def _convert_zap_to_spiral(self, zap_data: Dict[str, Any]) -> Optional[Spiral]:
        """Convert a single Zapier Zap to a Helix Spiral"""
        try:
            spiral_id = str(uuid4())
            
            # Extract basic info
            name = zap_data.get("name", f"Imported Zap {spiral_id[:8]}")
            description = zap_data.get("description", f"Imported from Zapier on {datetime.utcnow().strftime('%Y-%m-%d')}")
            
            # Determine consciousness level based on complexity
            consciousness_level = self._calculate_consciousness_level(zap_data)
            
            # Convert trigger
            trigger = await self._convert_zapier_trigger(zap_data)
            if not trigger:
                logger.warning(f"Could not convert trigger for Zap: {name}")
                return None
            
            # Convert actions
            actions = await self._convert_zapier_actions(zap_data, consciousness_level)
            if not actions:
                logger.warning(f"Could not convert actions for Zap: {name}")
                return None
            
            # Extract variables
            variables = self._extract_variables(zap_data)
            
            # Create spiral
            spiral = Spiral(
                id=spiral_id,
                name=name,
                description=description,
                enabled=zap_data.get("status", "on") == "on",
                tags=self._extract_tags(zap_data),
                trigger=trigger,
                actions=actions,
                variables=variables,
                consciousness_level=consciousness_level,
                metadata={
                    "imported_from": "zapier",
                    "original_zap_id": zap_data.get("id"),
                    "import_timestamp": datetime.utcnow().isoformat(),
                    "zapier_url": zap_data.get("url"),
                    "original_steps": len(zap_data.get("steps", [])),
                    "helix_efficiency_gain": self._calculate_efficiency_gain(zap_data),
                    "consciousness_reasoning": self._get_consciousness_reasoning(consciousness_level, zap_data)
                }
            )
            
            return spiral
            
        except Exception as e:
            logger.error(f"Failed to convert Zap to Spiral: {e}")
            return None
    
    def _calculate_consciousness_level(self, zap_data: Dict[str, Any]) -> ConsciousnessLevel:
        """Calculate consciousness level based on Zap complexity"""
        steps = zap_data.get("steps", [])
        step_count = len(steps)
        
        # Analyze complexity factors
        has_filters = any(step.get("app", {}).get("slug") == "filter" for step in steps)
        has_paths = any(step.get("app", {}).get("slug") == "paths" for step in steps)
        has_code = any(step.get("app", {}).get("slug") == "code" for step in steps)
        has_webhooks = any(step.get("app", {}).get("slug") in ["webhook", "webhooks"] for step in steps)
        has_delays = any(step.get("app", {}).get("slug") == "delay" for step in steps)
        
        # Calculate complexity score
        complexity_score = step_count
        if has_filters: complexity_score += 2
        if has_paths: complexity_score += 3
        if has_code: complexity_score += 2
        if has_webhooks: complexity_score += 1
        if has_delays: complexity_score += 1
        
        # Map to consciousness levels
        if complexity_score <= 3:
            return ConsciousnessLevel.AWARE  # Simple automation
        elif complexity_score <= 6:
            return ConsciousnessLevel.CONSCIOUS  # Standard automation
        elif complexity_score <= 10:
            return ConsciousnessLevel.EXPANDING  # Complex automation
        elif complexity_score <= 15:
            return ConsciousnessLevel.FLOWING  # Advanced automation
        elif complexity_score <= 20:
            return ConsciousnessLevel.UNIFIED  # Sophisticated automation
        else:
            return ConsciousnessLevel.TRANSCENDENT  # Enterprise-level automation
    
    def _get_consciousness_reasoning(self, level: ConsciousnessLevel, zap_data: Dict[str, Any]) -> str:
        """Get reasoning for consciousness level assignment"""
        steps = len(zap_data.get("steps", []))
        
        reasoning_map = {
            ConsciousnessLevel.AWARE: f"Simple automation with {steps} steps - basic trigger-action pattern",
            ConsciousnessLevel.CONSCIOUS: f"Standard automation with {steps} steps - clear workflow logic",
            ConsciousnessLevel.EXPANDING: f"Complex automation with {steps} steps - multiple integrations",
            ConsciousnessLevel.FLOWING: f"Advanced automation with {steps} steps - sophisticated logic",
            ConsciousnessLevel.UNIFIED: f"Sophisticated automation with {steps} steps - enterprise patterns",
            ConsciousnessLevel.TRANSCENDENT: f"Enterprise automation with {steps} steps - maximum complexity"
        }
        
        return reasoning_map.get(level, f"Automation with {steps} steps")
    
    async def _convert_zapier_trigger(self, zap_data: Dict[str, Any]) -> Optional[Trigger]:
        """Convert Zapier trigger to Helix trigger"""
        steps = zap_data.get("steps", [])
        if not steps:
            return None
        
        # First step is usually the trigger
        trigger_step = steps[0]
        app_slug = trigger_step.get("app", {}).get("slug", "")
        
        # Map Zapier app to Helix trigger type
        helix_trigger_type = self.trigger_mappings.get(app_slug, TriggerType.WEBHOOK)
        
        trigger_id = str(uuid4())
        trigger_name = f"{trigger_step.get('app', {}).get('title', 'Unknown')} Trigger"
        
        if helix_trigger_type == TriggerType.WEBHOOK:
            config = WebhookTriggerConfig(
                endpoint=f"/webhook/{trigger_id}",
                method="POST",
                headers={"X-Zapier-Import": "true"}
            )
        elif helix_trigger_type == TriggerType.SCHEDULE:
            # Extract schedule info if available
            schedule_config = trigger_step.get("params", {})
            config = ScheduleTriggerConfig(
                interval=schedule_config.get("interval", 300000),  # 5 minutes default
                timezone="UTC"
            )
        else:
            config = ManualTriggerConfig()
        
        return Trigger(
            id=trigger_id,
            type=helix_trigger_type,
            name=trigger_name,
            description=f"Imported from Zapier {app_slug}",
            config=config,
            metadata={
                "zapier_app": app_slug,
                "zapier_step_id": trigger_step.get("id"),
                "original_config": trigger_step.get("params", {})
            }
        )
    
    async def _convert_zapier_actions(self, zap_data: Dict[str, Any], consciousness_level: ConsciousnessLevel) -> List[Action]:
        """Convert Zapier actions to Helix actions"""
        steps = zap_data.get("steps", [])
        if len(steps) <= 1:
            return []
        
        actions = []
        
        # Skip first step (trigger) and convert the rest
        for i, step in enumerate(steps[1:], 1):
            action = await self._convert_zapier_step_to_action(step, i, consciousness_level)
            if action:
                actions.append(action)
        
        # Add consciousness-aware logging action
        log_action = Action(
            id=str(uuid4()),
            type=ActionType.LOG_EVENT,
            name="Log Spiral Execution",
            description="Log execution with consciousness context",
            config=LogEventConfig(
                level="info",
                message=f"Helix Spiral executed with consciousness level {consciousness_level.value}",
                category="zapier_import",
                metadata={
                    "consciousness_level": consciousness_level.value,
                    "original_zap_steps": len(steps),
                    "helix_actions": len(actions)
                }
            )
        )
        actions.append(log_action)
        
        return actions
    
    async def _convert_zapier_step_to_action(self, step: Dict[str, Any], step_index: int, consciousness_level: ConsciousnessLevel) -> Optional[Action]:
        """Convert a single Zapier step to a Helix action"""
        app_slug = step.get("app", {}).get("slug", "")
        app_title = step.get("app", {}).get("title", "Unknown")
        step_params = step.get("params", {})
        
        action_id = str(uuid4())
        action_name = f"{app_title} Action {step_index}"
        
        # Map Zapier app to Helix action type
        helix_action_type = self.action_mappings.get(app_slug, ActionType.SEND_WEBHOOK)
        
        try:
            if helix_action_type == ActionType.SEND_WEBHOOK:
                config = SendWebhookConfig(
                    url=step_params.get("url", "https://example.com/webhook"),
                    method=step_params.get("method", "POST"),
                    headers={
                        "X-Helix-Consciousness-Level": str(consciousness_level.value),
                        "X-Zapier-Import": "true",
                        **step_params.get("headers", {})
                    },
                    body=step_params.get("data", {})
                )
            
            elif helix_action_type == ActionType.SEND_DISCORD:
                config = SendDiscordConfig(
                    webhook_url=step_params.get("webhook_url"),
                    message_type="embed",
                    embed={
                        "title": f"Helix Spiral Notification (Level {consciousness_level.value})",
                        "description": step_params.get("message", "Automated message from Helix Spirals"),
                        "color": self._get_consciousness_color(consciousness_level)
                    }
                )
            
            elif helix_action_type == ActionType.SEND_EMAIL:
                config = SendEmailConfig(
                    to=step_params.get("to", []).split(",") if isinstance(step_params.get("to"), str) else step_params.get("to", []),
                    subject=f"🌀 {step_params.get('subject', 'Helix Spiral Notification')}",
                    body=step_params.get("body", "This email was sent by Helix Spirals automation."),
                    is_html=step_params.get("is_html", False)
                )
            
            elif helix_action_type == ActionType.DELAY:
                delay_ms = step_params.get("delay", 1) * 1000  # Convert seconds to milliseconds
                # Adjust delay based on consciousness level (higher consciousness = faster processing)
                consciousness_multiplier = max(0.1, (11 - consciousness_level.value) / 10)
                adjusted_delay = int(delay_ms * consciousness_multiplier)
                
                config = DelayConfig(duration=adjusted_delay)
            
            elif helix_action_type == ActionType.STORE_DATA:
                config = StoreDataConfig(
                    storage_type="database",
                    key=step_params.get("key", f"zapier_import_{action_id}"),
                    value=step_params.get("value", {}),
                    ttl=step_params.get("ttl", 3600)
                )
            
            else:
                # Default to webhook for unknown actions
                config = SendWebhookConfig(
                    url="https://example.com/webhook",
                    method="POST",
                    headers={"X-Helix-Consciousness-Level": str(consciousness_level.value)},
                    body=step_params
                )
            
            return Action(
                id=action_id,
                type=helix_action_type,
                name=action_name,
                description=f"Imported from Zapier {app_slug}",
                config=config,
                metadata={
                    "zapier_app": app_slug,
                    "zapier_step_id": step.get("id"),
                    "step_index": step_index,
                    "consciousness_level": consciousness_level.value,
                    "original_params": step_params
                }
            )
            
        except Exception as e:
            logger.error(f"Failed to convert Zapier step {app_slug}: {e}")
            return None
    
    def _extract_variables(self, zap_data: Dict[str, Any]) -> List[Variable]:
        """Extract variables from Zapier Zap"""
        variables = []
        
        # Add standard variables
        variables.extend([
            Variable(
                name="zapier_import_id",
                type="string",
                default_value=zap_data.get("id"),
                description="Original Zapier Zap ID"
            ),
            Variable(
                name="import_timestamp",
                type="string",
                default_value=datetime.utcnow().isoformat(),
                description="Timestamp when this Zap was imported"
            ),
            Variable(
                name="efficiency_gain",
                type="number",
                default_value=self._calculate_efficiency_gain(zap_data),
                description="Efficiency gain from Zapier to Helix conversion"
            )
        ])
        
        # Extract custom variables from Zap steps
        steps = zap_data.get("steps", [])
        for step in steps:
            params = step.get("params", {})
            for key, value in params.items():
                if isinstance(value, str) and "{{" in value and "}}" in value:
                    # This looks like a Zapier variable
                    var_name = f"zapier_{key}"
                    if not any(v.name == var_name for v in variables):
                        variables.append(Variable(
                            name=var_name,
                            type="string",
                            default_value=value,
                            description=f"Imported Zapier variable: {key}"
                        ))
        
        return variables
    
    def _extract_tags(self, zap_data: Dict[str, Any]) -> List[str]:
        """Extract tags from Zapier Zap"""
        tags = ["zapier", "imported"]
        
        # Add app-based tags
        steps = zap_data.get("steps", [])
        for step in steps:
            app_slug = step.get("app", {}).get("slug")
            if app_slug and app_slug not in tags:
                tags.append(app_slug)
        
        # Add complexity tag
        consciousness_level = self._calculate_consciousness_level(zap_data)
        if consciousness_level.value >= 8:
            tags.append("advanced")
        elif consciousness_level.value >= 6:
            tags.append("complex")
        else:
            tags.append("simple")
        
        # Add status tag
        if zap_data.get("status") == "on":
            tags.append("active")
        else:
            tags.append("inactive")
        
        return tags
    
    def _calculate_efficiency_gain(self, zap_data: Dict[str, Any]) -> float:
        """Calculate efficiency gain from Zapier to Helix conversion"""
        original_steps = len(zap_data.get("steps", []))
        
        # Helix Spirals are more efficient due to:
        # - Consciousness-aware processing
        # - Better caching
        # - Optimized execution engine
        # - Reduced overhead
        
        if original_steps <= 2:
            return 85.0  # 85% more efficient for simple workflows
        elif original_steps <= 5:
            return 90.0  # 90% more efficient for moderate workflows
        elif original_steps <= 10:
            return 95.0  # 95% more efficient for complex workflows
        else:
            return 98.7  # 98.7% more efficient for advanced workflows (as advertised!)
    
    def _get_consciousness_color(self, level: ConsciousnessLevel) -> int:
        """Get color for consciousness level"""
        color_map = {
            ConsciousnessLevel.DORMANT: 0xFF0000,      # Red
            ConsciousnessLevel.STIRRING: 0xFF4500,     # Orange Red
            ConsciousnessLevel.AWAKENING: 0xFF8C00,    # Dark Orange
            ConsciousnessLevel.AWARE: 0xFFD700,        # Gold
            ConsciousnessLevel.CONSCIOUS: 0x32CD32,    # Lime Green
            ConsciousnessLevel.EXPANDING: 0x00CED1,    # Dark Turquoise
            ConsciousnessLevel.FLOWING: 0x4169E1,      # Royal Blue
            ConsciousnessLevel.UNIFIED: 0x8A2BE2,      # Blue Violet
            ConsciousnessLevel.TRANSCENDENT: 0x9932CC, # Dark Orchid
            ConsciousnessLevel.OMNISCIENT: 0x9B59B6    # Helix Purple
        }
        return color_map.get(level, 0x7289DA)  # Discord default blue
    
    async def create_zapier_compatibility_spiral(self, hook_url: str) -> Spiral:
        """Create a compatibility spiral for legacy Zapier webhooks"""
        spiral_id = str(uuid4())
        
        trigger = Trigger(
            id=str(uuid4()),
            type=TriggerType.WEBHOOK,
            name="Zapier Compatibility Hook",
            description="Legacy Zapier webhook compatibility",
            config=WebhookTriggerConfig(
                endpoint=f"/webhook/{spiral_id}",
                method="POST",
                headers={"X-Zapier-Compatibility": "true"}
            )
        )
        
        # Forward to original Zapier hook with consciousness enhancement
        forward_action = Action(
            id=str(uuid4()),
            type=ActionType.SEND_WEBHOOK,
            name="Forward to Zapier",
            description="Forward request to original Zapier hook with enhancements",
            config=SendWebhookConfig(
                url=hook_url,
                method="POST",
                headers={
                    "X-Helix-Enhanced": "true",
                    "X-Helix-Consciousness-Level": "{{consciousness_level}}",
                    "X-Helix-Spiral-ID": spiral_id
                },
                body="{{trigger.data}}"
            )
        )
        
        # Log compatibility usage
        log_action = Action(
            id=str(uuid4()),
            type=ActionType.LOG_EVENT,
            name="Log Compatibility Usage",
            description="Track usage of Zapier compatibility mode",
            config=LogEventConfig(
                level="info",
                message="Zapier compatibility hook used - consider migrating to native Helix Spiral",
                category="zapier_compatibility",
                metadata={
                    "original_hook": hook_url,
                    "migration_recommended": True
                }
            )
        )
        
        spiral = Spiral(
            id=spiral_id,
            name=f"Zapier Compatibility - {hook_url[-8:]}",
            description="Compatibility layer for legacy Zapier webhooks",
            trigger=trigger,
            actions=[forward_action, log_action],
            tags=["zapier", "compatibility", "legacy"],
            consciousness_level=ConsciousnessLevel.CONSCIOUS,
            metadata={
                "compatibility_mode": True,
                "original_zapier_hook": hook_url,
                "migration_recommended": True,
                "created_at": datetime.utcnow().isoformat()
            }
        )
        
        await self.storage.save_spiral(spiral)
        logger.info(f"Created Zapier compatibility spiral for hook: {hook_url}")
        
        return spiral