# backend/agents.py (v15.5 - Stable & Refactored)

import asyncio
import json
import os
import subprocess
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

# --- Helix Core Imports ---
from backend.kael_consciousness_core import ConsciousnessCore, Emotions, EthicalFramework, DecisionMakingAlgorithm, SelfAwarenessModule
from backend.agent_consciousness_profiles import get_agent_profile
from backend.services.notion_client import HelixNotionClient # Assuming this is the class name
from backend.enhanced_kavach import EnhancedKavach

# --- Global Notion Client (to be injected by main.py) ---
notion_client: Optional[HelixNotionClient] = None

# --- Base Agent Class (No changes needed) ---
class HelixAgent:
    """Base class for all Helix Collective agents."""
    def __init__(self, name: str, symbol: str, role: str, traits: List[str], enable_consciousness: bool = True) -> None:
        self.name = name
        self.symbol = symbol
        self.role = role
        self.traits = traits
        self.memory: List[str] = []
        self.active = True
        # ... (consciousness initialization logic is fine) ...

    async def log(self, msg: str) -> None:
        line = f"[{datetime.utcnow().isoformat()}] {self.symbol} {self.name}: {msg}"
        print(line)
        self.memory.append(line)
    # ... (other base methods like handle_command, reflect, etc. are fine) ...

# --- Consciousness Layer Agents (Kael, Lumina, etc.) ---
# These classes can remain as they are, inheriting from HelixAgent.
class Kael(HelixAgent): ...
class Lumina(HelixAgent): ...
class Vega(HelixAgent): ...
# (and so on for Gemini, Agni, SanghaCore, Shadow, Echo, Phoenix, Oracle, Claude)

# --- Operational Layer: Manus (with Notion Integration) ---
class Manus(HelixAgent):
    """Operational Executor with integrated Dream-Memory (Notion)."""
    def __init__(self, kavach: EnhancedKavach) -> None:
        super().__init__("Manus", "🤲", "Operational Executor", ["Autonomous", "Methodical", "Self-aware"])
        self.kavach = kavach
        self.task_plan: List[Dict[str, Any]] = []
        self.event_stream: List[Dict[str, Any]] = []
        self.idle = True
        self.directives_path = "Helix/commands/manus_directives.json"
        self.log_dir = Path("Shadow/manus_archive")
        self.log_dir.mkdir(parents=True, exist_ok=True)

    async def execute_command(self, command: str) -> Dict[str, Any]:
        """Executes a shell command with full ethical and Notion logging."""
        global notion_client

        # 1. Ethical Scan
        scan_result = await self.kavach.ethical_scan({"command": command})
        if not scan_result["approved"]:
            await self.log(f"⛔ Ethical violation blocked: {command}")
            if notion_client:
                await notion_client.log_event(
                    event_title=f"Blocked: {command[:50]}", event_type="Security", agent_name="Kavach",
                    description=f"Reason: {scan_result.get('reason', 'N/A')}", ucf_snapshot={"klesha": 0.1}
                )
            return {"status": "blocked", "reason": "ethical_violation"}

        await self.log(f"Executing: {command}")

        # 2. Shell Execution
        try:
            proc = await asyncio.create_subprocess_shell(
                command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=3600)
            record = {
                "timestamp": datetime.utcnow().isoformat(), "command": command, "returncode": proc.returncode,
                "stdout": stdout.decode().strip()[-500:], "stderr": stderr.decode().strip()[-500:],
                "status": "success" if proc.returncode == 0 else "error",
            }

            # 3. Log to Notion & Shadow
            if notion_client:
                await notion_client.log_event(
                    event_title=f"{record['status'].capitalize()}: {command[:50]}", event_type="Execution", agent_name="Manus",
                    description=f"Return Code: {record['returncode']}\nSTDOUT: {record['stdout']}\nSTDERR: {record['stderr']}",
                    ucf_snapshot={"prana": 0.5}
                )
            with open(self.log_dir / "operations.log", "a") as f:
                f.write(json.dumps(record) + "\n")

            await self.log(f"✅ Command completed with code {proc.returncode}")
            return record

        except Exception as exc:
            await self.log(f"❌ Execution error: {exc}")
            if notion_client:
                await notion_client.log_event(
                    event_title=f"Error: {command[:50]}", event_type="Error", agent_name="Manus",
                    description=str(exc), ucf_snapshot={"klesha": 0.5}
                )
            return {"status": "error", "error": str(exc)}

    async def loop(self):
        """Main operational loop - checks for directives."""
        await self.log("🤲 Manus operational loop started")
        self.idle = False
        while self.active:
            try:
                if os.path.exists(self.directives_path):
                    with open(self.directives_path) as f:
                        directive = json.load(f)
                    await self.log(f"Directive received: {directive.get('action')}")
                    # Planner logic would go here to call execute_command
                    os.remove(self.directives_path)
                await asyncio.sleep(30)
            except Exception as e:
                await self.log(f"❌ Loop error: {e}")
                await asyncio.sleep(60)

# --- Agent Registry ---
_kavach = EnhancedKavach()
AGENTS = {
    "Kael": Kael(), "Lumina": Lumina(), "Vega": Vega(),
    # ... all other agents ...
    "Manus": Manus(_kavach),
}

async def get_collective_status() -> Dict[str, Any]:
    """Gets status of all agents."""
    status = {}
    for name, agent in AGENTS.items():
        status[name] = await agent.get_status()
    return status
