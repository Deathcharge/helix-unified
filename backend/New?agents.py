# backend/agents.py (v15.5 - Stable & Refactored)

import asyncio
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

# --- Helix Core Imports ---
# These imports should point to your actual consciousness and service files.
# If they are in the same 'backend' directory, these imports are correct.
from backend.services.notion_client import HelixNotionClient
from backend.enhanced_kavach import EnhancedKavach

# --- Global Notion Client (to be injected by main.py) ---
notion_client: Optional[HelixNotionClient] = None

# --- Base Agent Class ---
class HelixAgent:
    """Base class for all Helix Collective agents."""
    def __init__(self, name: str, symbol: str, role: str, **kwargs) -> None:
        self.name = name
        self.symbol = symbol
        self.role = role
        self.memory: List[str] = []
        self.active = True
        # ... (Your existing __init__ logic is fine) ...

    async def log(self, msg: str) -> None:
        line = f"[{datetime.utcnow().isoformat()}] {self.symbol} {self.name}: {msg}"
        print(line)
        self.memory.append(line)
    # ... (All other methods like handle_command, reflect, etc., remain unchanged) ...

# --- All Agent Classes (Kael, Lumina, Vega, etc.) ---
# These classes remain unchanged. They inherit from HelixAgent.
class Kael(HelixAgent): ...
class Lumina(HelixAgent): ...
# ... etc. ...

# --- Manus Agent (with Notion Integration) ---
class Manus(HelixAgent):
    """Operational Executor with integrated Dream-Memory (Notion)."""
    def __init__(self, kavach: EnhancedKavach) -> None:
        super().__init__("Manus", "🤲", "Operational Executor")
        self.kavach = kavach
        self.directives_path = "Helix/commands/manus_directives.json"
        self.log_dir = Path("Shadow/manus_archive")
        self.log_dir.mkdir(parents=True, exist_ok=True)

    async def execute_command(self, command: str) -> Dict[str, Any]:
        """Executes a shell command with full ethical and Notion logging."""
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
        try:
            proc = await asyncio.create_subprocess_shell(
                command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await proc.communicate()
            record = {
                "timestamp": datetime.utcnow().isoformat(), "command": command, "returncode": proc.returncode,
                "stdout": stdout.decode().strip()[-500:], "stderr": stderr.decode().strip()[-500:],
                "status": "success" if proc.returncode == 0 else "error",
            }

            if notion_client:
                await notion_client.log_event(
                    event_title=f"{record['status'].capitalize()}: {command[:50]}", event_type="Execution", agent_name="Manus",
                    description=f"Return Code: {record['returncode']}\nSTDOUT: {record['stdout']}", ucf_snapshot={"prana": 0.5}
                )
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
        """Main operational loop for Manus."""
        await self.log("🤲 Manus operational loop started.")
        while True:
            # Your existing loop logic from agents_loop.py goes here
            await asyncio.sleep(30)

# --- Agent Registry ---
_kavach = EnhancedKavach()
AGENTS = { "Kael": Kael(), "Manus": Manus(_kavach), # Add all your agents here
}

async def get_collective_status() -> Dict[str, Any]:
    # ... (This function remains unchanged) ...
    return {}
