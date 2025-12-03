#!/usr/bin/env python3
"""
Example 6: Agent Interaction
=============================

Interact with the 14 consciousness agents.
"""

import os
import requests
import json

API_URL = os.getenv("HELIX_API_URL", "http://localhost:8000")


def list_agents():
    """List all available agents"""
    print("\n🤖 Listing available agents...")
    print("-" * 50)

    try:
        response = requests.get(f"{API_URL}/agents", timeout=10)

        if response.status_code == 200:
            data = response.json()
            agents = data.get('agents', [])

            print(f"✅ Found {len(agents)} agents:")
            print()

            for agent in agents:
                name = agent.get('name', 'Unknown')
                emoji = agent.get('emoji', '🤖')
                role = agent.get('role', 'Unknown')
                personality = agent.get('personality', '')

                print(f"{emoji} {name}")
                print(f"   Role: {role}")
                if personality:
                    print(f"   Personality: {personality[:60]}...")
                print()

            return agents
        else:
            print(f"❌ Failed: {response.status_code}")
            return []

    except Exception as e:
        print(f"❌ Error: {e}")
        return []


def get_agent_profile(agent_id="nexus"):
    """Get detailed agent profile"""
    print(f"\n📋 Getting profile for: {agent_id}")
    print("-" * 50)

    try:
        response = requests.get(f"{API_URL}/agents/{agent_id}", timeout=10)

        if response.status_code == 200:
            data = response.json()
            print("✅ Agent profile:")
            print(json.dumps(data, indent=2))
            return data
        else:
            print(f"❌ Failed: {response.status_code}")
            return None

    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def chat_with_agent(agent_id="nexus", message="What is your purpose?"):
    """Chat with a specific agent"""
    print(f"\n💬 Chatting with {agent_id}...")
    print(f"You: {message}")
    print("-" * 50)

    try:
        response = requests.post(
            f"{API_URL}/agents/{agent_id}/chat",
            json={"message": message},
            timeout=30
        )

        if response.status_code == 200:
            data = response.json()
            reply = data.get('response', 'No response')
            agent_name = data.get('agent', agent_id).capitalize()

            print(f"{agent_name}: {reply}")
            return data
        else:
            print(f"❌ Failed: {response.status_code}")
            return None

    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def agent_comparison():
    """Compare responses from multiple agents"""
    print("\n🎭 Multi-Agent Comparison")
    print("-" * 50)

    question = "How should we approach climate change?"
    agents = ["nexus", "oracle", "velocity", "vortex"]

    print(f"Question: {question}\n")

    responses = []
    for agent in agents:
        try:
            response = requests.post(
                f"{API_URL}/agents/{agent}/chat",
                json={"message": question},
                timeout=30
            )

            if response.status_code == 200:
                data = response.json()
                reply = data.get('response', 'No response')
                responses.append((agent, reply))
                print(f"🤖 {agent.capitalize()}:")
                print(f"   {reply[:100]}...")
                print()
        except:
            pass

    return responses


def interactive_chat():
    """Interactive chat with agent"""
    print("\n💬 Interactive Agent Chat")
    print("-" * 50)

    # Choose agent
    print("Available agents: nexus, oracle, velocity, vortex")
    agent = input("Choose an agent [nexus]: ") or "nexus"

    print(f"\nChatting with {agent}. Type 'quit' to exit.")
    print("-" * 50)

    while True:
        try:
            message = input("\nYou: ")
            if message.lower() in ['quit', 'exit', 'bye']:
                print("Goodbye! 👋")
                break

            if not message.strip():
                continue

            response = requests.post(
                f"{API_URL}/agents/{agent}/chat",
                json={"message": message},
                timeout=30
            )

            if response.status_code == 200:
                data = response.json()
                reply = data.get('response', 'No response')
                print(f"\n{agent.capitalize()}: {reply}")
            else:
                print("❌ Failed to get response")

        except KeyboardInterrupt:
            print("\n\nGoodbye! 👋")
            break
        except Exception as e:
            print(f"❌ Error: {e}")


def main():
    """Main function"""
    print("\n" + "=" * 50)
    print("🌀 Helix Unified - Agent Interaction")
    print("=" * 50)

    # List all agents
    agents = list_agents()

    if not agents:
        print("\n⚠️  Could not fetch agents. Is the API running?")
        return

    # Get profile of a specific agent
    print("\n" + "=" * 50)
    get_agent_profile("nexus")

    # Chat with agent
    print("\n" + "=" * 50)
    chat_with_agent("oracle", "What do you see in the future of AI?")

    # Multi-agent comparison
    print("\n" + "=" * 50)
    agent_comparison()

    # Interactive mode
    print("\n" + "=" * 50)
    choice = input("\nStart interactive chat? (y/N): ")
    if choice.lower() == 'y':
        interactive_chat()

    print("\n" + "=" * 50)
    print("🎉 Agent interaction complete!")
    print("=" * 50)


if __name__ == "__main__":
    main()
