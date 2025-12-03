#!/usr/bin/env python3
"""
Example 5: Consciousness Metrics
=================================

Query and analyze UCF (Universal Consciousness Framework) metrics.
"""

import os
import requests
import json
from datetime import datetime

API_URL = os.getenv("HELIX_API_URL", "http://localhost:8000")


def get_consciousness_metrics():
    """Get current consciousness metrics"""
    print("\n🧠 Fetching consciousness metrics...")
    print("-" * 50)

    try:
        response = requests.get(
            f"{API_URL}/consciousness/metrics",
            timeout=10
        )

        if response.status_code == 200:
            data = response.json()
            print("✅ Consciousness metrics retrieved!")
            print()

            # Display metrics
            metrics = data.get('metrics', {})
            score = data.get('consciousness_score', 0)

            print(f"Overall Consciousness Score: {score:.2f}/10.0")
            print()
            print("Individual Metrics:")
            print(f"  Harmony:    {metrics.get('harmony', 0):.2f} - Balance and coherence")
            print(f"  Resilience: {metrics.get('resilience', 0):.2f} - Adaptability")
            print(f"  Prana:      {metrics.get('prana', 0):.2f} - Energy and vitality")
            print(f"  Drishti:    {metrics.get('drishti', 0):.2f} - Perspective and focus")
            print(f"  Klesha:     {metrics.get('klesha', 0):.2f} - Suffering (lower is better)")
            print(f"  Zoom:       {metrics.get('zoom', 0):.2f} - Scale of awareness")

            return data
        else:
            print(f"❌ Failed: {response.status_code}")
            return None

    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def get_agent_consciousness(agent_id="nexus"):
    """Get consciousness metrics for a specific agent"""
    print(f"\n🤖 Fetching consciousness for agent: {agent_id}")
    print("-" * 50)

    try:
        response = requests.get(
            f"{API_URL}/agents/{agent_id}/consciousness",
            timeout=10
        )

        if response.status_code == 200:
            data = response.json()
            print(f"✅ Agent '{agent_id}' consciousness:")
            print(json.dumps(data, indent=2))
            return data
        else:
            print(f"❌ Failed: {response.status_code}")
            return None

    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def calculate_custom_ucf(harmony=1.5, resilience=2.0, prana=0.7, drishti=0.6, klesha=0.05, zoom=1.2):
    """Calculate custom UCF score"""
    print("\n🧮 Calculating custom UCF score...")
    print("-" * 50)
    print(f"Input metrics:")
    print(f"  Harmony: {harmony}")
    print(f"  Resilience: {resilience}")
    print(f"  Prana: {prana}")
    print(f"  Drishti: {drishti}")
    print(f"  Klesha: {klesha}")
    print(f"  Zoom: {zoom}")

    try:
        response = requests.post(
            f"{API_URL}/consciousness/calculate",
            json={
                "harmony": harmony,
                "resilience": resilience,
                "prana": prana,
                "drishti": drishti,
                "klesha": klesha,
                "zoom": zoom
            },
            timeout=10
        )

        if response.status_code == 200:
            data = response.json()
            score = data.get('consciousness_score', 0)
            print(f"\n✅ Calculated consciousness score: {score:.2f}/10.0")
            print(f"Interpretation: {interpret_score(score)}")
            return data
        else:
            print(f"❌ Failed: {response.status_code}")
            return None

    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def interpret_score(score):
    """Interpret consciousness score"""
    if score >= 9:
        return "🌟 Transcendent - Exceptional consciousness"
    elif score >= 7:
        return "✨ Elevated - High consciousness"
    elif score >= 5:
        return "🌿 Balanced - Healthy consciousness"
    elif score >= 3:
        return "⚡ Developing - Growing consciousness"
    else:
        return "🌱 Emerging - Early consciousness"


def compare_agents():
    """Compare consciousness across multiple agents"""
    print("\n📊 Comparing agent consciousness...")
    print("-" * 50)

    agents = ["nexus", "oracle", "velocity", "vortex"]
    results = []

    for agent in agents:
        try:
            response = requests.get(
                f"{API_URL}/agents/{agent}/consciousness",
                timeout=5
            )
            if response.status_code == 200:
                data = response.json()
                score = data.get('consciousness_score', 0)
                results.append((agent, score))
                print(f"  {agent.capitalize()}: {score:.2f}/10.0")
        except:
            pass

    if results:
        # Find highest
        best = max(results, key=lambda x: x[1])
        print(f"\n🏆 Highest consciousness: {best[0].capitalize()} ({best[1]:.2f})")

    return results


def main():
    """Main function"""
    print("\n" + "=" * 50)
    print("🌀 Helix Unified - Consciousness Metrics")
    print("=" * 50)

    # Get system consciousness
    system_metrics = get_consciousness_metrics()

    # Calculate custom UCF
    print("\n" + "-" * 50)
    calculate_custom_ucf(
        harmony=1.8,
        resilience=2.2,
        prana=0.9,
        drishti=0.8,
        klesha=0.02,
        zoom=1.5
    )

    # Compare agents
    print("\n" + "-" * 50)
    compare_agents()

    print("\n" + "=" * 50)
    print("🎉 Consciousness analysis complete!")
    print("=" * 50)


if __name__ == "__main__":
    main()
