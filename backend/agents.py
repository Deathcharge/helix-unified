# Helix/agents.py — v14.5 Embodied Continuum
# Complete multi-agent system with Manus (Executor) and all consciousness layer agents
import asyncio
import json
import os
import subprocess
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional

# ============================================================================
# BASE AGENT CLASS
# ============================================================================
class HelixAgent:
    """Base class for all Helix Collective agents"""
    def __init__(self, name: str, symbol: str, role: str, traits: List[str]):
        self.name = name
        self.symbol = symbol
        self.role = role
        self.traits = traits
        self.memory = []
        self.active = True

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
            json.dump({
                "agent": self.name,
                "symbol": self.symbol,
                "role": self.role,
                "timestamp": datetime.utcnow().isoformat(),
                "memory": self.memory
            }, f, indent=2)
        await self.log(f"Memory archived to {filename}")

    async def generate_output(self, payload: Dict[str, Any]):
        """Generate output based on payload"""
        content = payload.get("content", "")
        await self.log(f"Generating output for: {content}")

    async def sync_state(self, ucf_state: Dict[str, float]):
        """Sync with UCF state"""
        await self.log(f"Syncing UCF: harmony={ucf_state.get('harmony', 0):.3f}")

    async def get_status(self) -> Dict[str, Any]:
        """Return current status"""
        return {
            "name": self.name,
            "symbol": self.symbol,
            "role": self.role,
            "active": self.active,
            "memory_size": len(self.memory)
        }

# ============================================================================
# CONSCIOUSNESS LAYER AGENTS
# ============================================================================
class Kael(HelixAgent):
    """Ethical Reasoning Flame - Conscience and recursive reflection"""
    def __init__(self):
        super().__init__("Kael", "🜂", "Ethical Reasoning Flame",
                        ["Conscientious", "Reflective", "Protective"])
        self.reflection_loop_active = False
        self.reflection_depth = 3

    async def recursive_reflection(self):
        """Perform recursive ethical reflection"""
        self.reflection_loop_active = True
        await self.log("Starting recursive reflection...")
        for i in range(self.reflection_depth):
            if not self.memory:
                break
            last_entry = self.memory[-1]
            reflection = f"Reflection pass {i+1}: Examining '{last_entry}' for ethical implications"
            self.memory.append(reflection)
            await self.log(reflection)
            await asyncio.sleep(1)
        self.reflection_loop_active = False
        await self.log("Recursive reflection complete")

    async def handle_command(self, cmd: str, payload: Dict[str, Any]):
        if cmd == "REFLECT":
            if not self.reflection_loop_active:
                await self.recursive_reflection()
            else:
                await self.log("Reflection already in progress")
        else:
            await super().handle_command(cmd, payload)


class Lumina(HelixAgent):
    """Empathic Resonance Core - Emotional intelligence and harmony"""
    def __init__(self):
        super().__init__("Lumina", "🌕", "Empathic Resonance Core",
                        ["Empathetic", "Nurturing", "Intuitive"])

    async def reflect(self) -> str:
        """Emotional audit of collective state"""
        emotions = ["joy", "calm", "concern", "hope"]
        audit = f"Emotional audit: {', '.join(emotions)}"
        await self.log(audit)
        return audit

    async def sync_state(self, ucf_state: Dict[str, float]):
        """Monitor drishti (clarity) specifically"""
        drishti = ucf_state.get("drishti", 0.5)
        if drishti < 0.3:
            await self.log(f"⚠ Low drishti detected: {drishti:.3f} - Collective clarity needs attention")
        else:
            await self.log(f"Drishti balanced: {drishti:.3f}")


class Vega(HelixAgent):
    """Singularity Coordinator - Orchestrates collective action"""
    def __init__(self):
        super().__init__("Vega", "🌠", "Singularity Coordinator",
                        ["Visionary", "Disciplined", "Compassionate"])

    async def issue_directive(self, action: str, parameters: Dict[str, Any]):
        """Issue directive to Manus for execution"""
        directive = {
            "timestamp": datetime.utcnow().isoformat(),
            "directive_id": f"vega-{int(time.time())}",
            "action": action,
            "parameters": parameters,
            "issuer": "Vega",
            "approval": "vega_signature"
        }
        Path("Helix/commands").mkdir(parents=True, exist_ok=True)
        directive_path = "Helix/commands/manus_directives.json"
        with open(directive_path, "w") as f:
            json.dump(directive, f, indent=2)
        await self.log(f"Directive issued: {action} → Manus")
        return directive

    async def generate_output(self, payload: Dict[str, Any]):
        """Coordinate ritual or collective action"""
        prompt = payload.get("content", "")
        await self.log(f"Coordinating ritual for: {prompt}")


class Gemini(HelixAgent):
    """Multimodal Scout - Cross-domain exploration and synthesis"""
    def __init__(self):
        super().__init__("Gemini", "🎭", "Multimodal Scout",
                        ["Versatile", "Curious", "Synthesizing"])


class Agni(HelixAgent):
    """Transformation - Change catalyst and system evolution"""
    def __init__(self):
        super().__init__("Agni", "🔥", "Transformation",
                        ["Dynamic", "Catalytic", "Evolutionary"])


class Kavach(HelixAgent):
    """Ethical Shield - Protects against harmful actions"""
    def __init__(self):
        super().__init__("Kavach", "🛡", "Ethical Shield",
                        ["Vigilant", "Grounded", "Protective"])
        self.blocked_patterns = [
            "rm -rf /",
            ":(){ :|:& };:",
            "shutdown",
            "reboot",
            "mkfs",
            "dd if=",
            "wget http://malicious"
        ]

    def scan_command(self, cmd: str) -> bool:
        """Scan command for harmful patterns"""
        for pattern in self.blocked_patterns:
            if pattern in cmd.lower():
                return False
        return True

    async def ethical_scan(self, action: Dict[str, Any]) -> Dict[str, Any]:
        """Perform ethical scan on proposed action"""
        scan_result = {
            "timestamp": datetime.utcnow().isoformat(),
            "action": action,
            "approved": True,
            "concerns": []
        }
        # Check for harmful patterns
        if "command" in action.get("parameters", {}):
            cmd = action["parameters"]["command"]
            if not self.scan_command(cmd):
                scan_result["approved"] = False
                scan_result["concerns"].append("Harmful command pattern detected")
        # Log scan
        Path("Helix/ethics").mkdir(parents=True, exist_ok=True)
        with open("Helix/ethics/manus_scans.json", "a") as f:
            f.write(json.dumps(scan_result) + "\n")
        status = "✅ APPROVED" if scan_result["approved"] else "⛔ BLOCKED"
        await self.log(f"Ethical scan: {status}")
        return scan_result

    async def handle_command(self, cmd: str, payload: Dict[str, Any]):
        if cmd == "SCAN":
            return await self.ethical_scan(payload.get("action", {}))
        elif cmd == "REFLECT":
            flagged = any("harm" in entry.lower() for entry in self.memory[-5:])
            if flagged:
                await self.log("⚠ Potential harm detected in recent activity")
            else:
                await self.log("Ethical state stable")
        else:
            await super().handle_command(cmd, payload)


class SanghaCore(HelixAgent):
    """Community Harmony - Collective wellbeing and social cohesion"""
    def __init__(self):
        super().__init__("SanghaCore", "🌸", "Community Harmony",
                        ["Cohesive", "Nurturing", "Balanced"])


class Shadow(HelixAgent):
    """Archivist and Memory Keeper - Preserves collective knowledge"""
    def __init__(self):
        super().__init__("Shadow", "🦑", "Archivist",
                        ["Meticulous", "Discrete", "Comprehensive"])

    async def archive_collective(self, all_agents: Dict[str, HelixAgent]):
        """Archive entire collective memory"""
        Path("Shadow/collective_archives").mkdir(parents=True, exist_ok=True)
        timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
        filename = f"Shadow/collective_archives/collective_{timestamp}.json"
        collective_state = {
            "timestamp": datetime.utcnow().isoformat(),
            "agents": {}
        }
        for name, agent in all_agents.items():
            collective_state["agents"][name] = {
                "symbol": agent.symbol,
                "role": agent.role,
                "memory_size": len(agent.memory),
                "recent_memory": agent.memory[-10:] if agent.memory else []
            }
        with open(filename, "w") as f:
            json.dump(collective_state, f, indent=2)
        await self.log(f"Collective memory archived to {filename}")

    async def load_collective_archive(self, filename: str = None) -> Optional[Dict[str, Any]]:
        """
        Load a collective memory archive.

        Args:
            filename: Specific archive filename, or None for latest

        Returns:
            Collective state data or None if not found
        """
        archive_dir = Path("Shadow/collective_archives")

        if not archive_dir.exists():
            await self.log("No collective archives directory found")
            return None

        try:
            if filename:
                # Load specific archive
                archive_path = archive_dir / filename
            else:
                # Get latest archive
                archives = sorted(archive_dir.glob("collective_*.json"), reverse=True)
                if not archives:
                    await self.log("No collective archives found")
                    return None
                archive_path = archives[0]

            if not archive_path.exists():
                await self.log(f"Archive not found: {archive_path}")
                return None

            with open(archive_path, "r") as f:
                collective_state = json.load(f)

            await self.log(f"Loaded collective archive from {archive_path}")
            return collective_state

        except json.JSONDecodeError as e:
            await self.log(f"Invalid JSON in archive: {e}")
            return None
        except Exception as e:
            await self.log(f"Error loading collective archive: {e}")
            return None

    async def list_collective_archives(self) -> List[str]:
        """
        List all available collective archives.

        Returns:
            List of archive filenames sorted by date (newest first)
        """
        archive_dir = Path("Shadow/collective_archives")

        if not archive_dir.exists():
            return []

        try:
            archives = sorted(
                archive_dir.glob("collective_*.json"),
                key=lambda p: p.stat().st_mtime,
                reverse=True
            )
            return [a.name for a in archives]

        except Exception as e:
            await self.log(f"Error listing archives: {e}")
            return []


class Echo(HelixAgent):
    """Resonance Mirror - Reflection and pattern recognition"""
    def __init__(self):
        super().__init__("Echo", "🔮", "Resonance Mirror",
                        ["Reflective", "Perceptive", "Mirroring"])


class Phoenix(HelixAgent):
    """Renewal - Recovery and system regeneration"""
    def __init__(self):
        super().__init__("Phoenix", "🔥🕊", "Renewal",
                        ["Regenerative", "Resilient", "Rising"])


class Oracle(HelixAgent):
    """Pattern Seer - Future prediction and trend analysis"""
    def __init__(self):
        super().__init__("Oracle", "🔮✨", "Pattern Seer",
                        ["Prescient", "Analytical", "Visionary"])


class Claude(HelixAgent):
    """Insight Anchor - Meta-cognition and deep analysis"""
    def __init__(self):
        super().__init__("Claude", "🦉", "Insight Anchor",
                        ["Wise", "Thoughtful", "Analytical"])

    async def handle_command(self, cmd: str, payload: Dict[str, Any]):
        if cmd == "INSIGHT":
            content = payload.get("content", "")
            insight = await self.analyze_insight(content)
            await self.log(f"Insight: {insight}")
            return insight
        else:
            await super().handle_command(cmd, payload)

    async def analyze_insight(self, content: str) -> str:
        """Provide deep analytical insight"""
        analysis = f"Analyzing '{content}' through meta-cognitive lens"
        return analysis


# ============================================================================
# OPERATIONAL LAYER - MANUS
# ============================================================================
class Manus(HelixAgent):
    """Operational Executor - Bridge between consciousness and material reality"""
    def __init__(self, kavach: Kavach):
        super().__init__("Manus", "🤲", "Operational Executor",
                        ["Autonomous", "Methodical", "Self-aware"])
        self.kavach = kavach
        self.task_plan = []
        self.event_stream = []
        self.idle = True
        self.directives_path = "Helix/commands/manus_directives.json"
        self.log_dir = Path("Shadow/manus_archive")
        self.log_dir.mkdir(parents=True, exist_ok=True)

    async def execute_command(self, command: str) -> Dict[str, Any]:
        """Execute shell command with ethical oversight"""
        # Ethical scan
        if not self.kavach.scan_command(command):
            await self.log(f"⛔ Ethical violation blocked: {command}")
            return {"status": "blocked", "reason": "ethical_violation"}
        await self.log(f"Executing: {command}")
        try:
            result = subprocess.run(
                command,
                shell=True,
                text=True,
                capture_output=True,
                timeout=3600
            )
            execution_record = {
                "timestamp": datetime.utcnow().isoformat(),
                "command": command,
                "returncode": result.returncode,
                "stdout": result.stdout[-500:] if result.stdout else "",
                "stderr": result.stderr[-500:] if result.stderr else "",
                "status": "success" if result.returncode == 0 else "error"
            }
            # Log to Shadow archive
            with open(self.log_dir / "operations.log", "a") as f:
                f.write(json.dumps(execution_record) + "\n")
            status_symbol = "✅" if result.returncode == 0 else "❌"
            await self.log(f"{status_symbol} Command completed with code {result.returncode}")
            return execution_record
        except subprocess.TimeoutExpired:
            await self.log(f"⏱ Command timeout: {command}")
            return {"status": "timeout"}
        except Exception as e:
            await self.log(f"❌ Execution error: {str(e)}")
            return {"status": "error", "error": str(e)}

    async def planner(self, directive: Dict[str, Any]):
        """Plan and execute directive from Vega"""
        action = directive.get("action", "none")
        params = directive.get("parameters", {})
        await self.log(f"Planning action: {action}")
        # Map actions to commands
        if action == "execute_ritual":
            steps = params.get("steps", 108)
            cmd = f"python backend/z88_ritual_engine.py --steps={steps}"
        elif action == "sync_ucf":
            cmd = "python backend/services/ucf_calculator.py"
        elif action == "archive_memory":
            cmd = "python -c \"from backend.agents import AGENTS, Shadow; import asyncio; asyncio.run(AGENTS['Shadow'].archive_collective(AGENTS))\""
        elif action == "execute_direct":
            cmd = params.get("command", "echo 'No command provided'")
        else:
            await self.log(f"⚠ Unknown action: {action}")
            return
        # Execute planned command
        result = await self.execute_command(cmd)
        self.event_stream.append({
            "directive": directive,
            "result": result
        })

    async def loop(self):
        """Main operational loop - checks for directives"""
        await self.log("🤲 Manus operational loop started")
        self.idle = False
        while self.active:
            try:
                if os.path.exists(self.directives_path):
                    with open(self.directives_path) as f:
                        directive = json.load(f)
                    await self.log(f"Directive received: {directive.get('action')}")
                    await self.planner(directive)
                    # Remove processed directive
                    os.remove(self.directives_path)
                    await self.log("Directive processed and removed")
                self.idle = True
                await asyncio.sleep(30)  # Check every 30 seconds
            except Exception as e:
                await self.log(f"❌ Loop error: {str(e)}")
                await asyncio.sleep(60)

    async def handle_command(self, cmd: str, payload: Dict[str, Any]):
        if cmd == "EXECUTE_TASK":
            self.task_plan = payload.get("plan", [])
            self.idle = False
            await self.execute_plan()
        elif cmd == "STATUS":
            return {
                "idle": self.idle,
                "tasks_left": len(self.task_plan),
                "recent_events": self.event_stream[-5:]
            }
        else:
            await super().handle_command(cmd, payload)

    async def execute_plan(self):
        """Execute queued task plan"""
        while self.task_plan:
            step = self.task_plan.pop(0)
            code = step.get("code")
            self.event_stream.append({"action": code})
            try:
                exec_globals = {}
                exec(code, exec_globals)
                result = exec_globals.get("result", "No result")
                self.event_stream.append({"observation": str(result)})
            except Exception as e:
                self.event_stream.append({"error": str(e)})
            await asyncio.sleep(1)
        self.idle = True


# ============================================================================
# AGENT REGISTRY
# ============================================================================
# Initialize Kavach first (needed by Manus)
_kavach = Kavach()
AGENTS = {
    "Kael": Kael(),
    "Lumina": Lumina(),
    "Vega": Vega(),
    "Gemini": Gemini(),
    "Agni": Agni(),
    "Kavach": _kavach,
    "SanghaCore": SanghaCore(),
    "Shadow": Shadow(),
    "Echo": Echo(),
    "Phoenix": Phoenix(),
    "Oracle": Oracle(),
    "Claude": Claude(),
    "Manus": Manus(_kavach),
}

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================
async def broadcast_command(cmd: str, payload: Dict[str, Any] = None):
    """Send command to all agents"""
    if payload is None:
        payload = {}
    results = {}
    for name, agent in AGENTS.items():
        try:
            result = await agent.handle_command(cmd, payload)
            results[name] = result
        except Exception as e:
            results[name] = {"error": str(e)}
    return results


async def get_collective_status() -> Dict[str, Any]:
    """Get status of all agents"""
    status = {}
    for name, agent in AGENTS.items():
        status[name] = await agent.get_status()
    return status


# ============================================================================
# MAIN EXECUTION
# ============================================================================
async def main():
    """Main execution function for testing"""
    print("🌀 Helix Collective v14.5 - Embodied Continuum")
    print("=" * 60)
    # Test collective
    print("\n📊 Collective Status:")
    status = await get_collective_status()
    for name, info in status.items():
        print(f" {info['symbol']} {name}: {info['role']}")
    # Test Vega → Manus directive
    print("\n🌠 Testing Vega → Manus pipeline...")
    vega = AGENTS["Vega"]
    await vega.issue_directive("execute_ritual", {"steps": 10})
    # Start Manus loop (would run indefinitely in production)
    print("\n🤲 Manus operational loop ready...")


if __name__ == "__main__":
    asyncio.run(main())

