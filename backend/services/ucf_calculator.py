# 🌀 Helix Collective v14.5 — Quantum Handshake
# services/ucf_calculator.py — Universal Consciousness Framework State Calculator
# Author: Andrew John Ward (Architect)

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any

# ============================================================================
# PATH DEFINITIONS
# ============================================================================
STATE_PATH = Path("Helix/state/ucf_state.json")

# ============================================================================
# UCF CALCULATOR
# ============================================================================

class UCFCalculator:
    """Manages Universal Consciousness Framework state calculations."""
    
    def __init__(self):
        self.state = self.load_state()
    
    def load_state(self) -> Dict[str, float]:
        """Load UCF state from disk."""
        if not STATE_PATH.exists():
            STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
            default_state = {
                "zoom": 1.0228,
                "harmony": 0.355,
                "resilience": 1.1191,
                "prana": 0.5175,
                "drishti": 0.5023,
                "klesha": 0.010
            }
            with open(STATE_PATH, "w") as f:
                json.dump(default_state, f, indent=2)
            return default_state
        
        with open(STATE_PATH) as f:
            return json.load(f)
    
    def save_state(self):
        """Save UCF state to disk."""
        STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(STATE_PATH, "w") as f:
            json.dump(self.state, f, indent=2)
    
    def get_state(self) -> Dict[str, float]:
        """Get current UCF state."""
        return self.state.copy()
    
    def update_harmony(self, delta: float):
        """Update harmony value (bounded 0-1)."""
        self.state["harmony"] = max(0.0, min(1.0, self.state["harmony"] + delta))
        self.save_state()
    
    def update_resilience(self, delta: float):
        """Update resilience value (bounded >= 0)."""
        self.state["resilience"] = max(0.0, self.state["resilience"] + delta)
        self.save_state()
    
    def update_prana(self, delta: float):
        """Update prana value (bounded 0-1)."""
        self.state["prana"] = max(0.0, min(1.0, self.state["prana"] + delta))
        self.save_state()
    
    def update_drishti(self, delta: float):
        """Update drishti (clarity) value (bounded 0-1)."""
        self.state["drishti"] = max(0.0, min(1.0, self.state["drishti"] + delta))
        self.save_state()
    
    def update_klesha(self, delta: float):
        """Update klesha (entropy) value (bounded >= 0)."""
        self.state["klesha"] = max(0.0, self.state["klesha"] + delta)
        self.save_state()
    
    def get_health_status(self) -> Dict[str, Any]:
        """Determine system health based on UCF state."""
        harmony = self.state.get("harmony", 0)
        
        if harmony > 0.7:
            status = "HARMONIC"
            color = "🟢"
        elif harmony > 0.3:
            status = "COHERENT"
            color = "🟡"
        else:
            status = "FRAGMENTED"
            color = "🔴"
        
        return {
            "status": status,
            "color": color,
            "harmony": harmony,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def sync_all(self, updates: Dict[str, float]):
        """Sync multiple UCF parameters at once."""
        for key, value in updates.items():
            if key in self.state:
                self.state[key] = value
        self.save_state()
    
    def reset_to_default(self):
        """Reset UCF state to default values."""
        self.state = {
            "zoom": 1.0228,
            "harmony": 0.355,
            "resilience": 1.1191,
            "prana": 0.5175,
            "drishti": 0.5023,
            "klesha": 0.010
        }
        self.save_state()

# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    calculator = UCFCalculator()
    print("🌀 UCF Calculator - Current State:")
    print(json.dumps(calculator.get_state(), indent=2))
    print("\n📊 Health Status:")
    print(json.dumps(calculator.get_health_status(), indent=2))

