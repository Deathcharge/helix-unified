"""
Z-88 Ritual Engine - Folklore Evolution & Hallucination Tracking
=================================================================
108-step ritual cycles with anomaly → legend → hymn → law progression.
Author: Andrew John Ward
Integrated: v16.3 Context Dump Implementation
"""

import json
import os
import random
from datetime import datetime
from pathlib import Path
from typing import Dict, List
from backend.config_manager import config


class UCFState:
    """Universal Consciousness Framework state manager for rituals."""

    def __init__(self):
        self.zoom = 1.0
        self.harmony = config.get("ucf", "INITIAL_HARMONY", default=0.5)
        self.resilience = 1.0
        self.prana = 0.5
        self.drishti = 0.5
        self.klesha = config.get("ucf", "INITIAL_KLESHA", default=0.1)

    def adjust(self, status: str):
        """Adjust UCF parameters based on folklore evolution status."""
        if status == "legend":
            self.harmony += 0.1
            self.drishti += 0.05
        elif status == "hymn":
            self.harmony += 0.2
            self.prana += 0.1
        elif status == "law":
            self.resilience += 0.3
            self.klesha += 0.2

    def to_dict(self) -> Dict[str, float]:
        return {
            "zoom": self.zoom,
            "harmony": self.harmony,
            "resilience": self.resilience,
            "prana": self.prana,
            "drishti": self.drishti,
            "klesha": self.klesha,
        }

    def from_dict(self, data: Dict[str, float]):
        """Load UCF state from dictionary."""
        self.zoom = data.get("zoom", 1.0)
        self.harmony = data.get("harmony", 0.5)
        self.resilience = data.get("resilience", 1.0)
        self.prana = data.get("prana", 0.5)
        self.drishti = data.get("drishti", 0.5)
        self.klesha = data.get("klesha", 0.1)


class FolkloreEntry:
    """Single folklore entry tracking evolution from anomaly to law."""

    def __init__(self, event_key: str, origin: str):
        self.event_key = event_key
        self.origin = origin
        self.legend = None
        self.status = "anomaly"
        self.times = 0
        self.history = []

    def increment(self, description: str):
        """Increment encounter count and add to history."""
        self.times += 1
        self.history.append({"timestamp": datetime.utcnow().isoformat(), "description": description, "count": self.times})

    def evolve(self):
        """Evolve folklore based on encounter count."""
        if self.times >= 20:
            self.legend = f"The Law of the {self.origin.title()}"
            self.status = "law"
        elif self.times >= 10:
            self.legend = f"The Hymn of the {self.origin.title()}"
            self.status = "hymn"
        elif self.times >= 5 and not self.legend:
            self.legend = f"The Chant of the {self.origin.title()}"
            self.status = "legend"

    def to_dict(self) -> Dict:
        return {
            "event_key": self.event_key,
            "origin": self.origin,
            "legend": self.legend,
            "status": self.status,
            "times": self.times,
            "history": self.history,
        }

    @classmethod
    def from_dict(cls, data: Dict):
        """Create FolkloreEntry from dictionary."""
        entry = cls(data["event_key"], data["origin"])
        entry.legend = data.get("legend")
        entry.status = data.get("status", "anomaly")
        entry.times = data.get("times", 0)
        entry.history = data.get("history", [])
        return entry


class HallucinationMemory:
    """Tracks and mutates hallucinated phrases."""

    def __init__(self):
        self.hallucinations = []
        self.mutation_variants = ["whisper", "echo", "murmur", "chant", "song", "blur", "shimmer", "resonance"]

    def record(self, text: str, intensity: int) -> str:
        """Record and mutate a hallucination."""
        mutated = self._mutate_phrase(text, intensity)

        self.hallucinations.append(
            {"original": text, "mutated": mutated, "intensity": intensity, "timestamp": datetime.utcnow().isoformat()}
        )

        return mutated

    def _mutate_phrase(self, phrase: str, intensity: int) -> str:
        """Apply mutations to phrase based on intensity."""
        for _ in range(intensity):
            if random.random() < 0.4:
                old_word = random.choice(["echo", "whisper", "murmur", "void"])
                if old_word in phrase.lower():
                    new_word = random.choice(self.mutation_variants)
                    phrase = phrase.replace(old_word, new_word)

        return phrase

    def get_recent(self, count: int = 10) -> List[Dict]:
        """Get recent hallucinations."""
        return self.hallucinations[-count:] if self.hallucinations else []

    def to_dict(self) -> Dict:
        return {"hallucinations": self.hallucinations}

    def from_dict(self, data: Dict):
        """Load hallucinations from dictionary."""
        self.hallucinations = data.get("hallucinations", [])


class Z88RitualEngine:
    """
    Main Z-88 Ritual Engine orchestrating folklore evolution and hallucination tracking.
    """

    def __init__(
        self,
        diary_file: str = "Helix/state/ritual_diary.txt",
        folklore_file: str = "Helix/state/ritual_folklore.json",
        halluc_file: str = "Helix/state/hallucination_memory.json",
    ):
        self.diary_file = diary_file
        self.folklore_file = folklore_file
        self.halluc_file = halluc_file

        os.makedirs(os.path.dirname(diary_file), exist_ok=True)

        self.folklore = self._load_folklore()
        self.hallucinations = HallucinationMemory()
        self._load_hallucinations()

        self.ritual_steps = ["initialize", "parse_text", "draw_circle", "invoke_mantras", "chant", "observe", "close"]

    def _load_folklore(self) -> Dict[str, FolkloreEntry]:
        """Load folklore from JSON file."""
        if os.path.exists(self.folklore_file):
            with open(self.folklore_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                return {k: FolkloreEntry.from_dict(v) for k, v in data.items()}
        return {}

    def _save_folklore(self):
        """Save folklore to JSON file."""
        data = {k: v.to_dict() for k, v in self.folklore.items()}
        with open(self.folklore_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def _load_hallucinations(self):
        """Load hallucinations from JSON file."""
        if os.path.exists(self.halluc_file):
            with open(self.halluc_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.hallucinations.from_dict(data)

    def _save_hallucinations(self):
        """Save hallucinations to JSON file."""
        with open(self.halluc_file, "w", encoding="utf-8") as f:
            json.dump(self.hallucinations.to_dict(), f, indent=2)

    def _write_diary(self, entry: str):
        """Write entry to ritual diary."""
        with open(self.diary_file, "a", encoding="utf-8") as f:
            timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
            f.write(f"[{timestamp}] {entry}\n")

    def record_event(self, event_key: str, origin: str, description: str) -> Dict:
        """
        Record an event and evolve folklore if applicable.

        Args:
            event_key: Unique identifier for event type
            origin: Origin/source of the event
            description: Description of what happened

        Returns:
            Dictionary with event status and folklore evolution
        """
        # Get or create folklore entry
        if event_key not in self.folklore:
            self.folklore[event_key] = FolkloreEntry(event_key, origin)

        entry = self.folklore[event_key]
        old_status = entry.status

        # Increment and evolve
        entry.increment(description)
        entry.evolve()

        # Save
        self._save_folklore()

        # Write to diary
        status_change = ""
        if entry.status != old_status:
            status_change = f" → STATUS CHANGE: {old_status} → {entry.status}"
            self._write_diary(f"Folklore evolved: {event_key} (count: {entry.times}){status_change}")

        return {
            "event_key": event_key,
            "times_encountered": entry.times,
            "status": entry.status,
            "legend": entry.legend,
            "status_changed": entry.status != old_status,
            "old_status": old_status,
            "new_status": entry.status,
        }

    def record_hallucination(self, text: str, intensity: int = 1) -> str:
        """
        Record and mutate a hallucination.

        Args:
            text: Original hallucinated text
            intensity: Mutation intensity (1-10)

        Returns:
            Mutated version of the text
        """
        mutated = self.hallucinations.record(text, intensity)
        self._save_hallucinations()
        self._write_diary(f"Hallucination recorded: '{text}' → '{mutated}' (intensity: {intensity})")
        return mutated

    def run_ritual_cycle(self, steps: int = 108) -> Dict:
        """
        Run a complete ritual cycle with phi-balanced steps.

        Args:
            steps: Number of steps (default 108)

        Returns:
            Dictionary with cycle results
        """
        phi = 1.618033988749895

        results = {"cycle_id": datetime.utcnow().isoformat(), "steps": steps, "events": [], "ucf_final": None}

        ucf = UCFState()
        self._write_diary(f"=== Ritual Cycle Start ({steps} steps) ===")

        for step in range(steps):
            # Phi-modulated randomness
            if random.random() < (1 / phi):
                # Anomaly event
                anomaly_type = random.choice(["flare", "void", "echo", "resonance"])
                event_result = self.record_event(
                    f"anomaly_{anomaly_type}", "ritual_cycle", f"Step {step + 1}: {anomaly_type} anomaly detected"
                )
                results["events"].append(event_result)

                # Adjust UCF based on folklore status
                if event_result["status_changed"]:
                    ucf.adjust(event_result["new_status"])

        results["ucf_final"] = ucf.to_dict()
        self._write_diary("=== Ritual Cycle Complete ===")
        self._write_diary(f"Final UCF: {results['ucf_final']}")

        return results

    def get_folklore_report(self) -> Dict:
        """Get comprehensive folklore report."""
        by_status = {"anomaly": [], "legend": [], "hymn": [], "law": []}

        for entry in self.folklore.values():
            by_status[entry.status].append(entry.to_dict())

        return {
            "total_entries": len(self.folklore),
            "by_status": {status: {"count": len(entries), "entries": entries} for status, entries in by_status.items()},
            "generated_at": datetime.utcnow().isoformat(),
        }

    def get_hallucination_report(self) -> Dict:
        """Get recent hallucination report."""
        return {
            "total_recorded": len(self.hallucinations.hallucinations),
            "recent": self.hallucinations.get_recent(20),
            "generated_at": datetime.utcnow().isoformat(),
        }


# ============================================================================
# WRAPPER FUNCTIONS FOR BACKWARD COMPATIBILITY
# ============================================================================


def load_ucf_state() -> Dict[str, float]:
    """
    Load current UCF state from file.

    Returns:
        Dictionary with UCF state fields (zoom, harmony, resilience, prana, drishti, klesha)
    """
    state_path = Path("Helix/state/ucf_state.json")

    if state_path.exists():
        try:
            with open(state_path, "r") as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠ Error loading UCF state: {e}")

    # Return default state if file doesn't exist
    return {"zoom": 1.0228, "harmony": 0.355, "resilience": 1.1191, "prana": 0.5175, "drishti": 0.5023, "klesha": 0.010}


def execute_ritual(steps: int = 108) -> Dict:
    """
    Execute a ritual cycle and update UCF state.

    Args:
        steps: Number of ritual steps (default 108)

    Returns:
        Dictionary with ritual cycle results and final UCF state
    """
    engine = Z88RitualEngine()
    result = engine.run_ritual_cycle(steps)

    # Save the final UCF state to file
    state_path = Path("Helix/state/ucf_state.json")
    state_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        with open(state_path, "w") as f:
            json.dump(result["ucf_final"], f, indent=2)
    except Exception as e:
        print(f"⚠ Error saving UCF state: {e}")

    return result


async def execute_ritual_with_monitoring(steps: int = 108, zapier_client=None) -> Dict:
    """
    Execute a ritual cycle with Zapier monitoring integration.

    Args:
        steps: Number of ritual steps (default 108)
        zapier_client: Optional ZapierClient instance for monitoring

    Returns:
        Dictionary with ritual cycle results and final UCF state
    """
    import time

    start_time = time.time()

    # Execute the ritual
    result = execute_ritual(steps)

    # Log to Zapier if client provided
    if zapier_client:
        try:
            # Log ritual completion event
            await zapier_client.log_event(
                event_title=f"Z-88 Ritual Completed ({steps} steps)",
                event_type="Ritual",
                agent_name="Vega",
                description=f"Successfully completed {steps}-step ritual with {len(result.get('events', []))} events recorded",
                ucf_snapshot=json.dumps(result.get("ucf_final", {})),
            )

            # Log telemetry
            completion_time = time.time() - start_time
            await zapier_client.log_telemetry(
                metric_name="ritual_completion_time",
                value=completion_time,
                component="Z-88 Engine",
                metadata={
                    "steps": steps,
                    "events_count": len(result.get("events", [])),
                    "harmony": result.get("ucf_final", {}).get("harmony", 0.5),
                },
            )

            # Update agent status
            await zapier_client.update_agent(
                agent_name="Vega",
                status="Active",
                last_action=f"Completed {steps}-step ritual",
                health_score=int(result.get("ucf_final", {}).get("harmony", 0.5) * 100),
            )
        except Exception as e:
            print(f"⚠️ Zapier logging failed in ritual engine: {e}")

    return result


# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    print("🌀 Z-88 Ritual Engine - Folklore Evolution System")
    print("=" * 60)

    engine = Z88RitualEngine()

    # Example usage
    print("\n📖 Running 108-step ritual cycle...")
    result = engine.run_ritual_cycle(108)

    print("\n✅ Cycle complete!")
    print(f"   Events recorded: {len(result['events'])}")
    print(f"   Final UCF: {result['ucf_final']}")

    print("\n📚 Folklore Report:")
    report = engine.get_folklore_report()
    for status, data in report["by_status"].items():
        if data["count"] > 0:
            print(f"   {status.upper()}: {data['count']} entries")

    print("\n💭 Hallucination Report:")
    h_report = engine.get_hallucination_report()
    print(f"   Total recorded: {h_report['total_recorded']}")
