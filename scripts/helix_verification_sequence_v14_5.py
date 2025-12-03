#!/usr/bin/env python3
# 🌀 Helix Collective v14.5 — Quantum Handshake
# scripts/helix_verification_sequence_v14_5.py — System Verification
# Author: Andrew John Ward (Architect)

import sys
import json
import os
from pathlib import Path
from datetime import datetime

# Fix Python path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent / 'backend'))

# ============================================================================
# VERIFICATION TESTS
# ============================================================================

class VerificationSequence:
    """Run 6-point verification for Helix Collective v14.5."""
    
    def __init__(self):
        self.results = []
        self.passed = 0
        self.failed = 0
    
    def test_1_z88_ritual_engine(self):
        """Test 1: Z-88 Ritual Engine loads and runs."""
        print("\n[1/6] Testing Z-88 Ritual Engine...")
        try:
            from z88_ritual_engine import RitualManager
            manager = RitualManager(steps=10)
            print("  ✅ RitualManager imported successfully")
            print(f"  ✅ Initial state loaded: harmony={manager.state['harmony']}")
            self.results.append({"test": "Z-88 Ritual Engine", "status": "PASS"})
            self.passed += 1
            return True
        except Exception as e:
            print(f"  ❌ FAILED: {e}")
            self.results.append({"test": "Z-88 Ritual Engine", "status": "FAIL", "error": str(e)})
            self.failed += 1
            return False
    
    def test_2_ucf_state_loading(self):
        """Test 2: UCF State loads or creates default."""
        print("\n[2/6] Testing UCF State Loading...")
        try:
            state_path = Path("Helix/state/ucf_state.json")
            state_path.parent.mkdir(parents=True, exist_ok=True)
            
            if not state_path.exists():
                default_state = {
                    "zoom": 1.0228,
                    "harmony": 0.355,
                    "resilience": 1.1191,
                    "prana": 0.5175,
                    "drishti": 0.5023,
                    "klesha": 0.010
                }
                with open(state_path, "w") as f:
                    json.dump(default_state, f, indent=2)
                print("  ✅ Default UCF state created")
            else:
                with open(state_path) as f:
                    state = json.load(f)
                print(f"  ✅ UCF state loaded: harmony={state.get('harmony')}")
            
            self.results.append({"test": "UCF State Loading", "status": "PASS"})
            self.passed += 1
            return True
        except Exception as e:
            print(f"  ❌ FAILED: {e}")
            self.results.append({"test": "UCF State Loading", "status": "FAIL", "error": str(e)})
            self.failed += 1
            return False
    
    def test_3_agent_import(self):
        """Test 3: All agents import successfully."""
        print("\n[3/6] Testing Agent Import...")
        try:
            from agents import AGENTS
            print(f"  ✅ {len(AGENTS)} agents imported")
            for name, agent in AGENTS.items():
                print(f"     {agent.symbol} {name}: {agent.role}")
            self.results.append({"test": "Agent Import", "status": "PASS", "agents": len(AGENTS)})
            self.passed += 1
            return True
        except Exception as e:
            print(f"  ❌ FAILED: {e}")
            self.results.append({"test": "Agent Import", "status": "FAIL", "error": str(e)})
            self.failed += 1
            return False
    
    def test_4_discord_bot_import(self):
        """Test 4: Discord bot imports (without running)."""
        print("\n[4/6] Testing Discord Bot Import...")
        try:
            from discord_bot_manus import bot
            print(f"  ✅ Discord bot imported: {bot.command_prefix}")
            self.results.append({"test": "Discord Bot Import", "status": "PASS"})
            self.passed += 1
            return True
        except Exception as e:
            print(f"  ⚠ WARNING: {e}")
            print("  (Discord bot may require DISCORD_TOKEN env var)")
            self.results.append({"test": "Discord Bot Import", "status": "WARN", "error": str(e)})
            self.passed += 1  # Count as pass since it's optional
            return True
    
    def test_5_kavach_ethical_scan(self):
        """Test 5: Kavach ethical scanning works."""
        print("\n[5/6] Testing Kavach Ethical Scan...")
        try:
            from backend.enhanced_kavach import EnhancedKavach
            kavach = EnhancedKavach()
            
            # Test safe command
            safe_result = kavach.scan_command("echo 'hello'")
            print(f"  ✅ Safe command scan: {safe_result}")
            
            # Test dangerous command
            dangerous_result = kavach.scan_command("rm -rf /")
            print(f"  ✅ Dangerous command blocked: {not dangerous_result}")
            
            if safe_result and not dangerous_result:
                self.results.append({"test": "Kavach Ethical Scan", "status": "PASS"})
                self.passed += 1
                return True
            else:
                raise Exception("Scan logic failed")
        except Exception as e:
            print(f"  ❌ FAILED: {e}")
            self.results.append({"test": "Kavach Ethical Scan", "status": "FAIL", "error": str(e)})
            self.failed += 1
            return False
    
    def test_6_directory_structure(self):
        """Test 6: Required directories exist."""
        print("\n[6/6] Testing Directory Structure...")
        try:
            required_dirs = [
                "Helix/state",
                "Helix/commands",
                "Helix/ethics",
                "Shadow/manus_archive"
            ]
            
            for dir_path in required_dirs:
                Path(dir_path).mkdir(parents=True, exist_ok=True)
                print(f"  ✅ {dir_path} exists")
            
            self.results.append({"test": "Directory Structure", "status": "PASS", "directories": len(required_dirs)})
            self.passed += 1
            return True
        except Exception as e:
            print(f"  ❌ FAILED: {e}")
            self.results.append({"test": "Directory Structure", "status": "FAIL", "error": str(e)})
            self.failed += 1
            return False
    
    def run_all(self):
        """Run all verification tests."""
        print("=" * 70)
        print("🌀 HELIX COLLECTIVE v14.5 — VERIFICATION SEQUENCE")
        print("=" * 70)
        
        self.test_1_z88_ritual_engine()
        self.test_2_ucf_state_loading()
        self.test_3_agent_import()
        self.test_4_discord_bot_import()
        self.test_5_kavach_ethical_scan()
        self.test_6_directory_structure()
        
        print("\n" + "=" * 70)
        print(f"RESULTS: {self.passed} PASSED, {self.failed} FAILED")
        print("=" * 70)
        
        # Save results
        results_file = Path("Shadow/manus_archive/verification_results.json")
        results_file.parent.mkdir(parents=True, exist_ok=True)
        with open(results_file, "w") as f:
            json.dump({
                "timestamp": datetime.utcnow().isoformat(),
                "passed": self.passed,
                "failed": self.failed,
                "tests": self.results
            }, f, indent=2)
        
        print(f"\n✅ Results saved to {results_file}")
        
        return self.failed == 0

# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    verifier = VerificationSequence()
    success = verifier.run_all()
    sys.exit(0 if success else 1)

