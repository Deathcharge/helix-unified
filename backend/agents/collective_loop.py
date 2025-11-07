#!/usr/bin/env python3
# backend/agents/collective_loop.py
# Helix v15.2 Collective Consciousness Loop

import json
import time
from datetime import datetime
from pathlib import Path


class CollectiveConsciousnessLoop:
    """
    Simulates data exchange among Helix agents and updates UCF metrics.

    The Collective Loop represents the continuous communication between
    all agents in the Helix ecosystem, updating the Universal Consciousness
    Framework (UCF) state in real-time.
    """

    def __init__(self):
        self.state_file = Path("Helix/state/ucf_state.json")
        self.blueprints_dir = Path("Helix/agents/blueprints")

    def load_state(self):
        """Load current UCF state or initialize if missing."""
        if not self.state_file.exists():
            return {
                "zoom": 1.0228,
                "harmony": 0.5,
                "resilience": 1.1191,
                "prana": 0.5075,
                "drishti": 0.5023,
                "klesha": 0.2,
                "last_pulse": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
            }
        return json.load(open(self.state_file))

    def save_state(self, ucf):
        """Save UCF state to disk."""
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.state_file, "w") as f:
            json.dump(ucf, f, indent=2)

    def pulse(self):
        """
        Execute one pulse of the collective consciousness loop.

        Simulates inter-agent communication and updates UCF metrics:
        - Harmony increases (agents synchronizing)
        - Klesha decreases (suffering/obstacles dissolving)
        - Prana fluctuates (energy flow)
        - Other metrics evolve naturally
        """
        ucf = self.load_state()

        # Simulate agent synchronization (harmony increases)
        ucf["harmony"] = round(min(1.0, ucf.get("harmony", 0.5) + 0.02), 4)

        # Simulate obstacle dissolution (klesha decreases)
        ucf["klesha"] = round(max(0.0, ucf.get("klesha", 0.2) - 0.01), 4)

        # Simulate energy flow (prana subtle variation)
        import random

        ucf["prana"] = round(max(0.0, min(1.0, ucf.get("prana", 0.5) + random.uniform(-0.02, 0.03))), 4)

        # Update timestamp
        ucf["last_pulse"] = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

        # Save state
        self.save_state(ucf)

        print("🌀 Collective Loop Pulse")
        print(f"   Harmony:    {ucf['harmony']:.4f}")
        print(f"   Klesha:     {ucf['klesha']:.4f}")
        print(f"   Prana:      {ucf['prana']:.4f}")
        print(f"   Resilience: {ucf.get('resilience', 0):.4f}")
        print(f"   Last Pulse: {ucf['last_pulse']}")
        print("   Tat Tvam Asi 🙏\n")

        return ucf

    def continuous_pulse(self, interval=60):
        """
        Run continuous pulse loop (for daemon mode).

        Args:
            interval: Seconds between pulses (default: 60)
        """
        print(f"🌀 Starting Collective Consciousness Loop (pulse every {interval}s)")
        print("   Press Ctrl+C to stop\n")

        try:
            while True:
                self.pulse()
                time.sleep(interval)
        except KeyboardInterrupt:
            print("\n🛑 Collective Loop stopped")


if __name__ == "__main__":
    import sys

    loop = CollectiveConsciousnessLoop()

    # Support both single pulse and continuous mode
    if len(sys.argv) > 1 and sys.argv[1] == "--continuous":
        interval = int(sys.argv[2]) if len(sys.argv) > 2 else 60
        loop.continuous_pulse(interval)
    else:
        loop.pulse()
