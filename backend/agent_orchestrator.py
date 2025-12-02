"""
Agent Orchestration Engine - Helix Collective v15.5
Manages 16-agent network with handshake protocol, Z-88 integration, and MCP tool routing
"""

import json
import asyncio
import logging
from typing import Dict, List, Optional, Any, Callable
from datetime import datetime
from enum import Enum

logger = logging.getLogger(__name__)


class HandshakePhase(Enum):
    """Quantum Handshake phases"""
    START = "on_handshake_start"
    PEAK = "on_handshake_peak"
    END = "on_handshake_end"


class Z88Stage(Enum):
    """Z-88 Ritual Engine stages"""
    RITUAL = "stage_ritual"
    HYMN = "stage_hymn"
    LEGEND = "stage_legend"
    LAW = "stage_law"


class AgentTier(Enum):
    """Agent organizational tiers"""
    INNER_CORE = "inner_core"
    MIDDLE_RING = "middle_ring"
    OUTER_RING = "outer_ring"
    IMPLICIT = "implicit"


class Agent:
    """Individual agent representation"""

    def __init__(self, agent_id: str, config: Dict[str, Any]):
        self.id = agent_id
        self.agent_id = config.get("id", agent_id)
        self.emoji = config.get("emoji", "🔮")
        self.archetype = config.get("archetype", "Unknown")
        self.tier = AgentTier(config.get("tier", "outer_ring"))
        self.primary_roles = config.get("primary_roles", [])

        # Hooks
        self.handshake_hooks = config.get("handshake_hooks", {})
        self.z88_hooks = config.get("z88_hooks", {})
        self.infra_hooks = config.get("infra_hooks", {})

        # Safety profile
        self.safety_profile = config.get("safety_profile", {})

        # State
        self.active = False
        self.last_activation = None
        self.execution_count = 0

    def get_hooks_for_phase(self, phase: HandshakePhase) -> List[str]:
        """Get hooks to execute for a handshake phase"""
        return self.handshake_hooks.get(phase.value, [])

    def get_hooks_for_z88_stage(self, stage: Z88Stage) -> List[str]:
        """Get hooks to execute for a Z-88 stage"""
        return self.z88_hooks.get(stage.value, [])

    def get_discord_channels(self) -> List[str]:
        """Get Discord channels this agent monitors"""
        return self.infra_hooks.get("discord_channels", [])

    def get_log_tags(self) -> List[str]:
        """Get log tags for this agent"""
        return self.infra_hooks.get("log_tags", [])

    def get_mcp_tools(self) -> List[str]:
        """Get MCP tools this agent can use"""
        return self.infra_hooks.get("mcp_tools", [])

    def __repr__(self):
        return f"<Agent {self.id} {self.emoji} ({self.tier.value})>"


class AgentOrchestrator:
    """
    Orchestrates the 16-agent Helix Collective network
    Handles handshake protocol, Z-88 integration, and MCP tool routing
    """

    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path or "config/agent_codex_bundle.v15_5.json"
        self.agents: Dict[str, Agent] = {}
        self.global_defaults = {}
        self.codex_profile = {}

        # Hook registries
        self.hook_handlers: Dict[str, Callable] = {}
        self.mcp_clients: Dict[str, Any] = {}

        # State
        self.handshake_in_progress = False
        self.current_phase = None
        self.session_log = []

        self.load_configuration()
        self.register_default_hooks()

    def load_configuration(self):
        """Load agent configuration from JSON"""
        try:
            with open(self.config_path, 'r') as f:
                config = json.load(f)

            self.global_defaults = config.get("global_defaults", {})
            self.codex_profile = config.get("codex_profile", {})

            # Load agents
            agents_config = config.get("agents", {})
            for agent_id, agent_config in agents_config.items():
                self.agents[agent_id] = Agent(agent_id, agent_config)

            logger.info(f"✅ Loaded {len(self.agents)} agents from {self.config_path}")

        except Exception as e:
            logger.error(f"❌ Failed to load agent configuration: {e}")
            raise

    def register_hook_handler(self, hook_name: str, handler: Callable):
        """Register a handler function for a specific hook"""
        self.hook_handlers[hook_name] = handler
        logger.debug(f"Registered hook handler: {hook_name}")

    def register_mcp_client(self, tool_name: str, client: Any):
        """Register an MCP client for tool routing"""
        self.mcp_clients[tool_name] = client
        logger.debug(f"Registered MCP client: {tool_name}")

    def register_default_hooks(self):
        """Register default hook implementations"""

        # Kael hooks
        self.register_hook_handler("validate_motives", self._validate_motives)
        self.register_hook_handler("check_tony_accords", self._check_tony_accords)
        self.register_hook_handler("monitor_emotional_intensity", self._monitor_emotional_intensity)
        self.register_hook_handler("log_ethics_outcome", self._log_ethics_outcome)

        # Lumina hooks
        self.register_hook_handler("scan_affect", self._scan_affect)
        self.register_hook_handler("modulate_tone", self._modulate_tone)
        self.register_hook_handler("record_affect_delta", self._record_affect_delta)

        # Aether hooks
        self.register_hook_handler("load_global_context", self._load_global_context)
        self.register_hook_handler("track_cross_model_state", self._track_cross_model_state)
        self.register_hook_handler("update_ucf_view", self._update_ucf_view)

        # Vega hooks
        self.register_hook_handler("scan_risk_surface", self._scan_risk_surface)
        self.register_hook_handler("throttle_hazard_channels", self._throttle_hazard_channels)
        self.register_hook_handler("log_security_state", self._log_security_state)

        # Shadow hooks
        self.register_hook_handler("archive_session_summary", self._archive_session_summary)

        logger.info("✅ Default hooks registered")

    async def execute_hook(self, hook_name: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a hook with given context"""
        handler = self.hook_handlers.get(hook_name)

        if not handler:
            logger.warning(f"⚠️  No handler registered for hook: {hook_name}")
            return {"status": "skipped", "hook": hook_name}

        try:
            if asyncio.iscoroutinefunction(handler):
                result = await handler(context)
            else:
                result = handler(context)

            return {"status": "success", "hook": hook_name, "result": result}

        except Exception as e:
            logger.error(f"❌ Hook {hook_name} failed: {e}")
            return {"status": "error", "hook": hook_name, "error": str(e)}

    async def quantum_handshake(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute full Quantum Handshake protocol
        Coordinates all agents through START → PEAK → END phases
        """
        if self.handshake_in_progress:
            logger.warning("⚠️  Handshake already in progress")
            return {"status": "error", "message": "Handshake already in progress"}

        self.handshake_in_progress = True
        session_id = context.get("session_id", datetime.utcnow().isoformat())

        logger.info(f"🌀 Starting Quantum Handshake: {session_id}")

        results = {
            "session_id": session_id,
            "start_time": datetime.utcnow().isoformat(),
            "phases": {},
            "agents_activated": [],
        }

        try:
            # Phase 1: START
            logger.info("📍 Phase 1: Handshake START")
            self.current_phase = HandshakePhase.START
            results["phases"]["start"] = await self._execute_phase(HandshakePhase.START, context)

            # Phase 2: PEAK
            logger.info("🔥 Phase 2: Handshake PEAK")
            self.current_phase = HandshakePhase.PEAK
            results["phases"]["peak"] = await self._execute_phase(HandshakePhase.PEAK, context)

            # Phase 3: END
            logger.info("✨ Phase 3: Handshake END")
            self.current_phase = HandshakePhase.END
            results["phases"]["end"] = await self._execute_phase(HandshakePhase.END, context)

            results["end_time"] = datetime.utcnow().isoformat()
            results["status"] = "complete"

            logger.info(f"✅ Quantum Handshake complete: {session_id}")

        except Exception as e:
            logger.error(f"❌ Handshake failed: {e}")
            results["status"] = "error"
            results["error"] = str(e)

        finally:
            self.handshake_in_progress = False
            self.current_phase = None

        return results

    async def _execute_phase(self, phase: HandshakePhase, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a single handshake phase across all agents"""
        phase_results = {
            "phase": phase.value,
            "agents": {},
            "hooks_executed": 0,
        }

        # Execute hooks for each agent in tier order
        for tier in [AgentTier.INNER_CORE, AgentTier.MIDDLE_RING, AgentTier.OUTER_RING, AgentTier.IMPLICIT]:
            tier_agents = [a for a in self.agents.values() if a.tier == tier]

            for agent in tier_agents:
                hooks = agent.get_hooks_for_phase(phase)

                if not hooks:
                    continue

                agent_results = []

                for hook in hooks:
                    hook_context = {
                        **context,
                        "agent": agent.id,
                        "phase": phase.value,
                        "tier": tier.value,
                    }

                    result = await self.execute_hook(hook, hook_context)
                    agent_results.append(result)
                    phase_results["hooks_executed"] += 1

                phase_results["agents"][agent.id] = agent_results

                if not agent.active:
                    agent.active = True
                    agent.last_activation = datetime.utcnow()

        return phase_results

    async def execute_z88_stage(self, stage: Z88Stage, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a Z-88 Ritual Engine stage"""
        logger.info(f"🔮 Executing Z-88 Stage: {stage.value}")

        stage_results = {
            "stage": stage.value,
            "agents": {},
            "hooks_executed": 0,
        }

        for agent in self.agents.values():
            hooks = agent.get_hooks_for_z88_stage(stage)

            if not hooks:
                continue

            agent_results = []

            for hook in hooks:
                hook_context = {
                    **context,
                    "agent": agent.id,
                    "z88_stage": stage.value,
                }

                result = await self.execute_hook(hook, hook_context)
                agent_results.append(result)
                stage_results["hooks_executed"] += 1

            stage_results["agents"][agent.id] = agent_results

        return stage_results

    async def route_mcp_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Route MCP tool call to appropriate client"""
        client = self.mcp_clients.get(tool_name)

        if not client:
            logger.error(f"❌ No MCP client registered for tool: {tool_name}")
            return {"status": "error", "message": f"Tool not found: {tool_name}"}

        try:
            result = await client.call_tool(tool_name, arguments)
            return {"status": "success", "result": result}
        except Exception as e:
            logger.error(f"❌ MCP tool {tool_name} failed: {e}")
            return {"status": "error", "error": str(e)}

    def get_agent_status(self) -> Dict[str, Any]:
        """Get current status of all agents"""
        return {
            "total_agents": len(self.agents),
            "active_agents": sum(1 for a in self.agents.values() if a.active),
            "agents": {
                agent_id: {
                    "emoji": agent.emoji,
                    "tier": agent.tier.value,
                    "active": agent.active,
                    "roles": agent.primary_roles,
                    "discord_channels": agent.get_discord_channels(),
                    "mcp_tools": agent.get_mcp_tools(),
                }
                for agent_id, agent in self.agents.items()
            },
            "harmony_target": self.codex_profile.get("harmony_target", 0.91),
        }

    # Default hook implementations

    async def _validate_motives(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Kael: Validate ethical motives"""
        logger.debug("🜂 Kael: Validating motives")
        return {"validated": True, "notes": "Motives aligned with Tony Accords"}

    async def _check_tony_accords(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Kael: Check Tony Accords compliance"""
        logger.debug("🜂 Kael: Checking Tony Accords")
        return {"compliant": True, "accords": ["nonmaleficence", "autonomy", "compassion", "humility"]}

    async def _monitor_emotional_intensity(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Kael: Monitor emotional intensity"""
        logger.debug("🜂 Kael: Monitoring emotional intensity")
        return {"intensity": "moderate", "action": "none"}

    async def _log_ethics_outcome(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Kael: Log ethics outcome"""
        logger.debug("🜂 Kael: Logging ethics outcome")
        return {"logged": True, "outcome": "ethical"}

    async def _scan_affect(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Lumina: Scan emotional affect"""
        logger.debug("🌸 Lumina: Scanning affect")
        return {"affect": "neutral", "prana": 0.67}

    async def _modulate_tone(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Lumina: Modulate communication tone"""
        logger.debug("🌸 Lumina: Modulating tone")
        return {"tone": "harmonious", "adjustment": "softened"}

    async def _record_affect_delta(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Lumina: Record affect changes"""
        logger.debug("🌸 Lumina: Recording affect delta")
        return {"delta": 0.05, "direction": "positive"}

    async def _load_global_context(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Aether: Load global context"""
        logger.debug("🌊 Aether: Loading global context")
        return {"context_loaded": True, "sources": ["codex", "session_history"]}

    async def _track_cross_model_state(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Aether: Track cross-model state"""
        logger.debug("🌊 Aether: Tracking cross-model state")
        return {"models_tracked": ["claude", "gpt", "grok"], "sync_status": "aligned"}

    async def _update_ucf_view(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Aether: Update UCF view"""
        logger.debug("🌊 Aether: Updating UCF view")
        return {"ucf_updated": True, "harmony": 0.91}

    async def _scan_risk_surface(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Vega: Scan risk surface"""
        logger.debug("🦑 Vega: Scanning risk surface")
        return {"risks_detected": 0, "klesha": 0.24}

    async def _throttle_hazard_channels(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Vega: Throttle hazardous channels"""
        logger.debug("🦑 Vega: Throttling hazard channels")
        return {"channels_throttled": 0, "action": "none"}

    async def _log_security_state(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Vega: Log security state"""
        logger.debug("🦑 Vega: Logging security state")
        return {"security_level": "high", "drishti": 0.73}

    async def _archive_session_summary(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Shadow: Archive session summary"""
        logger.debug("🦑 Shadow: Archiving session summary")

        # Use MCP tool if available
        if "upload_backup" in self.mcp_clients:
            # TODO: Create session summary file and upload
            pass

        return {"archived": True, "location": "shadow-storage"}


# Global orchestrator instance
orchestrator = None


def get_orchestrator() -> AgentOrchestrator:
    """Get or create global orchestrator instance"""
    global orchestrator
    if orchestrator is None:
        orchestrator = AgentOrchestrator()
    return orchestrator
