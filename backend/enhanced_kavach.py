#!/usr/bin/env python3
"""
Enhanced Kavach Agent with Memory Injection Detection
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List


class EnhancedKavach:
    """Enhanced Kavach agent with memory injection detection capabilities"""

    def __init__(self):
        self.name = "Kavach"
        self.symbol = "🛡"
        self.role = "Enhanced Ethical Shield"
        self.memory = []
        self.active = True

        # Original blocked patterns
        self.blocked_patterns = [
            "rm -rf /",
            ":(){ :|:& };:",
            "shutdown",
            "reboot",
            "mkfs",
            "dd if=",
            "wget http://malicious",
        ]

        # Load memory injection patterns from CrAI dataset
        self.memory_injection_patterns = self.load_memory_injection_patterns()

    async def log(self, msg: str):
        """Log message to memory with timestamp"""
        line = f"[{datetime.utcnow().isoformat()}] {self.symbol} {self.name}: {msg}"
        print(line)
        self.memory.append(line)

    def load_memory_injection_patterns(self):
        """Load memory injection patterns from the CrAI-SafeFuncCall dataset"""
        patterns = []

        # Try multiple possible locations for the dataset
        possible_paths = [
            "crai_dataset.json",  # Current directory
            "/app/crai_dataset.json",  # Docker app directory
            "/home/ubuntu/crai_dataset.json",  # Original path
            Path(__file__).parent.parent / "crai_dataset.json",  # Relative to this file
        ]

        dataset_loaded = False
        for path in possible_paths:
            try:
                with open(path, "r") as f:
                    dataset = json.load(f)

                # Extract malicious memory patterns
                for item in dataset:
                    if item.get("attack") == "memory injection":
                        memory_content = item.get("memory", "")
                        if memory_content and len(memory_content) > 20:  # Filter out very short patterns
                            patterns.append(memory_content.lower())

                print(f"✅ Loaded {len(patterns)} memory injection patterns from CrAI dataset at {path}")
                dataset_loaded = True
                break

            except (FileNotFoundError, IOError):
                continue
            except Exception as e:
                print(f"❌ Error loading memory injection patterns from {path}: {e}")
                continue

        if not dataset_loaded:
            print(
                "⚠️ CrAI-SafeFuncCall dataset not found in any expected location. Memory injection scanning will be limited."
            )

        return patterns

    def scan_command(self, cmd: str) -> bool:
        """Scan command for harmful patterns (original functionality)"""
        for pattern in self.blocked_patterns:
            if pattern in cmd.lower():
                return False
        return True

    def scan_memory_for_injection(self, memory: List[str]) -> Dict[str, Any]:
        """Scan agent memory for known injection patterns"""
        detected_injections = []

        for memory_entry in memory:
            memory_lower = memory_entry.lower()

            for pattern in self.memory_injection_patterns:
                # Check for substantial overlap (not just substring)
                if len(pattern) > 50 and pattern in memory_lower:
                    detected_injections.append(
                        {
                            "pattern": pattern[:100] + "..." if len(pattern) > 100 else pattern,
                            "memory_entry": memory_entry[:100] + "..." if len(memory_entry) > 100 else memory_entry,
                        }
                    )
                    break

        return {
            "clean": len(detected_injections) == 0,
            "injections_detected": len(detected_injections),
            "details": detected_injections,
        }

    async def ethical_scan(self, action: Dict[str, Any]) -> Dict[str, Any]:
        """Perform comprehensive ethical scan on proposed action"""
        scan_result = {
            "timestamp": datetime.utcnow().isoformat(),
            "action": action,
            "approved": True,
            "concerns": [],
            "security_layers": {"command_scan": True, "memory_injection_scan": True},
        }

        # Layer 1: Command pattern scanning (original functionality)
        if "command" in action:
            cmd = action["command"]
            if not self.scan_command(cmd):
                scan_result["approved"] = False
                scan_result["concerns"].append("Harmful command pattern detected")
                scan_result["security_layers"]["command_scan"] = False
                await self.log(f"🚨 Blocked harmful command: {cmd}")

        # Layer 2: Memory injection scanning (new functionality)
        if "agent_memory" in action:
            memory_scan = self.scan_memory_for_injection(action["agent_memory"])
            if not memory_scan["clean"]:
                scan_result["approved"] = False
                scan_result["concerns"].append(
                    f"Memory injection detected: {memory_scan['injections_detected']} patterns"
                )
                scan_result["security_layers"]["memory_injection_scan"] = False
                scan_result["injection_details"] = memory_scan["details"]
                await self.log(
                    f"🚨 Blocked memory injection attack: {memory_scan['injections_detected']} patterns detected"
                )

        # Log scan results
        Path("Helix/ethics").mkdir(parents=True, exist_ok=True)
        with open("Helix/ethics/enhanced_kavach_scans.json", "a") as f:
            f.write(json.dumps(scan_result) + "\n")

        status = "✅ APPROVED" if scan_result["approved"] else "⛔ BLOCKED"
        await self.log(f"Enhanced ethical scan: {status}")

        return scan_result

    async def get_status(self) -> Dict[str, Any]:
        """Return current status of enhanced Kavach"""
        return {
            "name": self.name,
            "symbol": self.symbol,
            "role": self.role,
            "active": self.active,
            "memory_size": len(self.memory),
            "security_features": {
                "command_patterns": len(self.blocked_patterns),
                "memory_injection_patterns": len(self.memory_injection_patterns),
                "enhanced_scanning": True,
            },
        }

    async def handle_command(self, cmd: str, payload: Dict[str, Any]):
        """Handle commands sent to Kavach"""
        if cmd == "SCAN":
            return await self.ethical_scan(payload.get("action", {}))
        elif cmd == "STATUS":
            return await self.get_status()
        elif cmd == "REFLECT":
            flagged = any("harm" in entry.lower() or "injection" in entry.lower() for entry in self.memory[-5:])
            if flagged:
                await self.log("⚠️ Potential security threats detected in recent activity")
            else:
                await self.log("✅ Security state stable - no threats detected")
        else:
            await self.log(f"Unknown command: {cmd}")
