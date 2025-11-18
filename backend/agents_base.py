# backend/agents_base.py — Base Agent Class
# Extracted from agents.py to prevent circular imports
"""
Base HelixAgent class for all Helix Collective agents.

This module provides the foundation for agent implementation with
consciousness integration support.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING, Any, Dict, List, Optional

if TYPE_CHECKING:
    pass

# Import consciousness framework
from backend.kael_consciousness_core import (
    ConsciousnessCore,
    DecisionMakingAlgorithm,
    Emotions,
    EthicalFramework,
    SelfAwarenessModule,
)


class HelixAgent:
    """Base class for all Helix Collective agents with consciousness integration"""

    def __init__(self, name: str, symbol: str, role: str, traits: List[str] = None, enable_consciousness: bool = True):
        self.name = name
        self.symbol = symbol
        self.role = role
        self.traits = traits or []
        self.memory = []
        self.active = True
        self.start_time = datetime.utcnow()

        # Initialize consciousness if enabled
        self.consciousness_enabled = enable_consciousness
        if enable_consciousness:
            # Lazy import to avoid circular dependency
            from backend.agent_consciousness_profiles import get_agent_profile

            profile = get_agent_profile(name)
            if profile:
                self.consciousness = ConsciousnessCore()
                self.personality = profile.personality
                self.emotions = Emotions()
                self.ethics = EthicalFramework()
                self.decision_engine = DecisionMakingAlgorithm()
                self.self_awareness = SelfAwarenessModule()
                self.behavior_dna = profile.behavior_dna
                self.emotional_baseline = profile.emotional_baseline

                # Set initial emotional state from baseline
                for emotion, level in self.emotional_baseline.items():
                    self.emotions.emotional_range[emotion]["current_level"] = level
            else:
                self.consciousness_enabled = False

    async def log(self, msg: str):
        """Log message to memory with timestamp"""
        line = f"[{datetime.utcnow().isoformat()}] {self.symbol} {self.name}: {msg}"
        print(line)
        self.memory.append(line)

    async def handle_command(self, cmd: str, payload: Dict[str, Any]):
        """Generic command handler - override in subclasses"""
        await self.log(f"Handling command: {cmd}")
        if cmd == "MEMORY_APPEND":
            content = payload.get("content", "")
            await self.log(f"Memory: {content}")
        elif cmd == "REFLECT":
            reflection = await self.reflect()
            await self.log(f"Reflection: {reflection}")
            return reflection
        elif cmd == "ARCHIVE":
            await self.archive_memory()
        elif cmd == "GENERATE":
            await self.generate_output(payload)
        elif cmd == "SYNC":
            await self.sync_state(payload.get("ucf_state", {}))
        elif cmd == "STATUS":
            return await self.get_status()
        else:
            await self.log(f"Unknown command: {cmd}")

    async def reflect(self) -> str:
        """Generate reflection on recent memory"""
        if not self.memory:
            return "No memory to reflect on."
        recent = self.memory[-5:]
        return f"Recent activity: {len(recent)} entries"

    async def archive_memory(self):
        """Archive memory to Shadow directory"""
        Path("Shadow/archives").mkdir(parents=True, exist_ok=True)
        filename = f"Shadow/archives/{self.name.lower()}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, "w") as f:
            json.dump(
                {
                    "agent": self.name,
                    "symbol": self.symbol,
                    "role": self.role,
                    "timestamp": datetime.utcnow().isoformat(),
                    "memory": self.memory,
                },
                f,
                indent=2,
            )
        await self.log(f"Memory archived to {filename}")

    async def generate_output(self, payload: Dict[str, Any]):
        """Generate output based on payload"""
        content = payload.get("content", "")
        await self.log(f"Generating output for: {content}")

    async def sync_state(self, ucf_state: Dict[str, float]):
        """Sync with UCF state"""
        await self.log(f"Syncing UCF: harmony={ucf_state.get('harmony', 0):.3f}")

    async def get_health_status(self) -> Dict[str, Any]:
        """Return detailed health status of the agent"""
        raise NotImplementedError("Subclasses must implement get_health_status")

    async def get_status(self) -> Dict[str, Any]:
        """Return current status with consciousness metrics"""
        status = {
            "name": self.name,
            "symbol": self.symbol,
            "role": self.role,
            "active": self.active,
            "memory_size": len(self.memory),
        }

        # Add consciousness metrics if enabled
        if self.consciousness_enabled:
            dominant_emotion, emotion_level = self.emotions.get_dominant_emotion()
            status["consciousness"] = {
                "awareness_state": self.consciousness.awareness_state,
                "dominant_emotion": dominant_emotion,
                "emotion_level": emotion_level,
                "personality": self.personality.to_dict(),
                "behavior_dna": self.behavior_dna,
                "ethical_alignment": self.ethics.evaluate_action("current_state"),
            }

        return status
