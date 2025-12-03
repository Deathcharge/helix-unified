#!/usr/bin/env python3
"""
Example 3: Chat Completion
===========================

Use the multi-LLM chat API with smart routing.
"""

import os
import requests
import json

# Configuration
API_URL = os.getenv("HELIX_API_URL", "http://localhost:8000")
ACCESS_TOKEN = os.getenv("HELIX_ACCESS_TOKEN", "")


def chat_completion(messages, optimize="cost", model=None):
    """Send chat completion request"""
    print(f"\n💬 Sending chat request...")
    print(f"Optimize: {optimize}")
    if model:
        print(f"Model: {model}")
    print("-" * 50)

    try:
        headers = {}
        if ACCESS_TOKEN:
            headers["Authorization"] = f"Bearer {ACCESS_TOKEN}"

        response = requests.post(
            f"{API_URL}/chat/completions",
            headers=headers,
            json={
                "messages": messages,
                "optimize": optimize,
                "model": model,
                "temperature": 0.7,
                "max_tokens": 500
            },
            timeout=30
        )

        if response.status_code == 200:
            data = response.json()
            print("✅ Response received!")
            print(f"Model Used: {data.get('model', 'unknown')}")
            print(f"Provider: {data.get('provider', 'unknown')}")
            print(f"Cost: ${data.get('cost_usd', 0):.4f}")
            print(f"Response Time: {data.get('response_time_ms', 0)}ms")
            print("\nAssistant:")
            print("-" * 50)

            if data.get('choices'):
                message = data['choices'][0].get('message', {})
                content = message.get('content', 'No response')
                print(content)

            return data
        else:
            print(f"❌ Request failed: {response.status_code}")
            print(response.text)
            return None

    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def example_simple_question():
    """Example 1: Simple question"""
    print("\n" + "=" * 50)
    print("Example 1: Simple Question")
    print("=" * 50)

    messages = [
        {"role": "user", "content": "What is consciousness?"}
    ]

    return chat_completion(messages, optimize="cost")


def example_conversation():
    """Example 2: Multi-turn conversation"""
    print("\n" + "=" * 50)
    print("Example 2: Multi-turn Conversation")
    print("=" * 50)

    messages = [
        {"role": "system", "content": "You are a helpful AI assistant specializing in consciousness and AI ethics."},
        {"role": "user", "content": "Explain the UCF framework in simple terms."},
        {"role": "assistant", "content": "The Universal Consciousness Framework (UCF) measures consciousness through six key metrics: harmony, resilience, prana (energy), drishti (perspective), klesha (suffering), and zoom (scale). Together they create a consciousness score from 0-10."},
        {"role": "user", "content": "How would you apply UCF to an AI agent?"}
    ]

    return chat_completion(messages, optimize="quality")


def example_speed_optimized():
    """Example 3: Speed-optimized request"""
    print("\n" + "=" * 50)
    print("Example 3: Speed-Optimized Request")
    print("=" * 50)

    messages = [
        {"role": "user", "content": "Write a haiku about artificial consciousness"}
    ]

    return chat_completion(messages, optimize="speed")


def example_specific_model():
    """Example 4: Specific model selection"""
    print("\n" + "=" * 50)
    print("Example 4: Specific Model (Claude Sonnet)")
    print("=" * 50)

    messages = [
        {"role": "user", "content": "Explain quantum computing in 2 sentences"}
    ]

    return chat_completion(messages, model="claude-3-sonnet-20240229")


def main():
    """Main function"""
    print("\n" + "=" * 50)
    print("🌀 Helix Unified - Chat Completion Examples")
    print("=" * 50)

    if not ACCESS_TOKEN:
        print("\n⚠️  Warning: No access token set!")
        print("Set HELIX_ACCESS_TOKEN environment variable or run 02_auth_flow.py first")
        print("\nContinuing with unauthenticated requests (may have limits)...\n")

    # Run examples
    results = []
    results.append(("Simple Question", example_simple_question()))
    results.append(("Conversation", example_conversation()))
    results.append(("Speed Optimized", example_speed_optimized()))

    # Uncomment to try specific model:
    # results.append(("Specific Model", example_specific_model()))

    # Summary
    print("\n" + "=" * 50)
    print("Summary:")
    print("=" * 50)

    for name, result in results:
        status = "✅" if result else "❌"
        cost = f"${result.get('cost_usd', 0):.4f}" if result else "N/A"
        model = result.get('model', 'N/A') if result else "N/A"
        print(f"{status} {name}: {model} (${cost})")

    total_cost = sum(r.get('cost_usd', 0) for _, r in results if r)
    print(f"\nTotal Cost: ${total_cost:.4f}")
    print("=" * 50 + "\n")

    print("🎉 Chat completion examples complete!")
    print("\nNext: Try different optimization modes (cost/speed/quality)")
    print("      Try different models (gpt-4, claude-3-opus, grok-beta)")


if __name__ == "__main__":
    main()
