#!/usr/bin/env python3
# 🌀 Helix Collective v14.5 — Quantum Handshake
# scripts/test_memory_root.py — Memory Root Integration Tests
# Author: Andrew John Ward (Architect)

import asyncio
import json
import os
import sys
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.agents.memory_root import get_memory_root
from backend.services.notion_client import get_notion_client

# ============================================================================
# TEST SUITE
# ============================================================================

class MemoryRootTestSuite:
    """Test suite for Memory Root integration."""
    
    def __init__(self):
        self.results = {
            "timestamp": datetime.utcnow().isoformat(),
            "tests": [],
            "passed": 0,
            "failed": 0
        }
    
    async def run_all_tests(self):
        """Run all tests."""
        print("=" * 70)
        print("🧠 MEMORY ROOT INTEGRATION TEST SUITE")
        print("=" * 70)
        
        # Test 1: Memory Root Initialization
        await self.test_memory_root_init()
        
        # Test 2: Notion Client Connectivity
        await self.test_notion_connectivity()
        
        # Test 3: Agent Retrieval
        await self.test_agent_retrieval()
        
        # Test 4: Event Query
        await self.test_event_query()
        
        # Test 5: Context Snapshot Retrieval
        await self.test_context_retrieval()
        
        # Test 6: Memory Synthesis (requires OpenAI)
        await self.test_memory_synthesis()
        
        # Test 7: Health Check
        await self.test_health_check()
        
        # Print results
        await self.print_results()
    
    async def test_memory_root_init(self):
        """Test 1: Memory Root Initialization."""
        print("\n[Test 1] Memory Root Initialization")
        try:
            memory_root = await get_memory_root()
            if memory_root:
                print("✅ Memory Root initialized successfully")
                self.results["tests"].append({
                    "name": "Memory Root Initialization",
                    "status": "PASS"
                })
                self.results["passed"] += 1
            else:
                print("❌ Memory Root initialization failed")
                self.results["tests"].append({
                    "name": "Memory Root Initialization",
                    "status": "FAIL",
                    "error": "Memory Root returned None"
                })
                self.results["failed"] += 1
        except Exception as e:
            print(f"❌ Error: {e}")
            self.results["tests"].append({
                "name": "Memory Root Initialization",
                "status": "FAIL",
                "error": str(e)
            })
            self.results["failed"] += 1
    
    async def test_notion_connectivity(self):
        """Test 2: Notion Client Connectivity."""
        print("\n[Test 2] Notion Client Connectivity")
        try:
            notion = await get_notion_client()
            if notion:
                health = await notion.health_check()
                if health:
                    print("✅ Notion connection healthy")
                    self.results["tests"].append({
                        "name": "Notion Connectivity",
                        "status": "PASS"
                    })
                    self.results["passed"] += 1
                else:
                    print("❌ Notion health check failed")
                    self.results["tests"].append({
                        "name": "Notion Connectivity",
                        "status": "FAIL",
                        "error": "Health check returned False"
                    })
                    self.results["failed"] += 1
            else:
                print("⚠ Notion client unavailable (expected if NOTION_API_KEY not set)")
                self.results["tests"].append({
                    "name": "Notion Connectivity",
                    "status": "SKIP",
                    "reason": "NOTION_API_KEY not set"
                })
        except Exception as e:
            print(f"❌ Error: {e}")
            self.results["tests"].append({
                "name": "Notion Connectivity",
                "status": "FAIL",
                "error": str(e)
            })
            self.results["failed"] += 1
    
    async def test_agent_retrieval(self):
        """Test 3: Agent Retrieval from Notion."""
        print("\n[Test 3] Agent Retrieval")
        try:
            memory_root = await get_memory_root()
            if not memory_root or not memory_root.notion_client:
                print("⚠ Skipping: Notion client unavailable")
                self.results["tests"].append({
                    "name": "Agent Retrieval",
                    "status": "SKIP",
                    "reason": "Notion client unavailable"
                })
                return
            
            agents = await memory_root.notion_client.get_all_agents()
            if agents and len(agents) > 0:
                print(f"✅ Retrieved {len(agents)} agents from Notion")
                print(f"   Sample: {agents[0]['name']} ({agents[0]['status']})")
                self.results["tests"].append({
                    "name": "Agent Retrieval",
                    "status": "PASS",
                    "agent_count": len(agents)
                })
                self.results["passed"] += 1
            else:
                print("❌ No agents retrieved")
                self.results["tests"].append({
                    "name": "Agent Retrieval",
                    "status": "FAIL",
                    "error": "No agents found"
                })
                self.results["failed"] += 1
        except Exception as e:
            print(f"❌ Error: {e}")
            self.results["tests"].append({
                "name": "Agent Retrieval",
                "status": "FAIL",
                "error": str(e)
            })
            self.results["failed"] += 1
    
    async def test_event_query(self):
        """Test 4: Event Query from Notion."""
        print("\n[Test 4] Event Query")
        try:
            memory_root = await get_memory_root()
            if not memory_root or not memory_root.notion_client:
                print("⚠ Skipping: Notion client unavailable")
                self.results["tests"].append({
                    "name": "Event Query",
                    "status": "SKIP",
                    "reason": "Notion client unavailable"
                })
                return
            
            # Try to query events for Manus
            events = await memory_root.notion_client.query_events_by_agent("Manus", limit=5)
            if events is not None:
                print(f"✅ Retrieved {len(events)} events for Manus")
                if events:
                    print(f"   Sample: {events[0]['title']}")
                self.results["tests"].append({
                    "name": "Event Query",
                    "status": "PASS",
                    "event_count": len(events)
                })
                self.results["passed"] += 1
            else:
                print("❌ Event query failed")
                self.results["tests"].append({
                    "name": "Event Query",
                    "status": "FAIL",
                    "error": "Query returned None"
                })
                self.results["failed"] += 1
        except Exception as e:
            print(f"❌ Error: {e}")
            self.results["tests"].append({
                "name": "Event Query",
                "status": "FAIL",
                "error": str(e)
            })
            self.results["failed"] += 1
    
    async def test_context_retrieval(self):
        """Test 5: Context Snapshot Retrieval."""
        print("\n[Test 5] Context Snapshot Retrieval")
        try:
            memory_root = await get_memory_root()
            if not memory_root or not memory_root.notion_client:
                print("⚠ Skipping: Notion client unavailable")
                self.results["tests"].append({
                    "name": "Context Retrieval",
                    "status": "SKIP",
                    "reason": "Notion client unavailable"
                })
                return
            
            # Try to retrieve a known session
            context = await memory_root.retrieve_session_context("claude-2025-10-21-helix-v14.5")
            if context:
                print(f"✅ Retrieved context for session: {context['session_id']}")
                print(f"   AI System: {context['ai_system']}")
                self.results["tests"].append({
                    "name": "Context Retrieval",
                    "status": "PASS",
                    "session_id": context['session_id']
                })
                self.results["passed"] += 1
            else:
                print("⚠ Session not found (expected if seeding not run)")
                self.results["tests"].append({
                    "name": "Context Retrieval",
                    "status": "SKIP",
                    "reason": "Session not found"
                })
        except Exception as e:
            print(f"❌ Error: {e}")
            self.results["tests"].append({
                "name": "Context Retrieval",
                "status": "FAIL",
                "error": str(e)
            })
            self.results["failed"] += 1
    
    async def test_memory_synthesis(self):
        """Test 6: Memory Synthesis with GPT4o."""
        print("\n[Test 6] Memory Synthesis")
        try:
            memory_root = await get_memory_root()
            if not memory_root:
                print("⚠ Skipping: Memory Root unavailable")
                self.results["tests"].append({
                    "name": "Memory Synthesis",
                    "status": "SKIP",
                    "reason": "Memory Root unavailable"
                })
                return
            
            if not memory_root.openai_client:
                print("⚠ Skipping: OpenAI client unavailable (set OPENAI_API_KEY)")
                self.results["tests"].append({
                    "name": "Memory Synthesis",
                    "status": "SKIP",
                    "reason": "OPENAI_API_KEY not set"
                })
                return
            
            # Try to synthesize a memory
            response = await memory_root.synthesize_memory("Notion integration")
            if response:
                print(f"✅ Memory synthesis successful")
                print(f"   Response length: {len(response)} characters")
                print(f"   Preview: {response[:100]}...")
                self.results["tests"].append({
                    "name": "Memory Synthesis",
                    "status": "PASS",
                    "response_length": len(response)
                })
                self.results["passed"] += 1
            else:
                print("⚠ Memory synthesis returned empty response")
                self.results["tests"].append({
                    "name": "Memory Synthesis",
                    "status": "SKIP",
                    "reason": "No matching context found"
                })
        except Exception as e:
            print(f"❌ Error: {e}")
            self.results["tests"].append({
                "name": "Memory Synthesis",
                "status": "FAIL",
                "error": str(e)
            })
            self.results["failed"] += 1
    
    async def test_health_check(self):
        """Test 7: Memory Root Health Check."""
        print("\n[Test 7] Health Check")
        try:
            memory_root = await get_memory_root()
            if not memory_root:
                print("❌ Memory Root unavailable")
                self.results["tests"].append({
                    "name": "Health Check",
                    "status": "FAIL",
                    "error": "Memory Root unavailable"
                })
                self.results["failed"] += 1
                return
            
            health = await memory_root.health_check()
            print(f"✅ Health check completed")
            print(f"   Status: {health['status']}")
            print(f"   OpenAI: {'✅' if health.get('openai_available') else '❌'}")
            print(f"   Notion: {'✅' if health.get('notion_available') else '❌'}")
            
            self.results["tests"].append({
                "name": "Health Check",
                "status": "PASS",
                "health": health['status']
            })
            self.results["passed"] += 1
        except Exception as e:
            print(f"❌ Error: {e}")
            self.results["tests"].append({
                "name": "Health Check",
                "status": "FAIL",
                "error": str(e)
            })
            self.results["failed"] += 1
    
    async def print_results(self):
        """Print test results summary."""
        print("\n" + "=" * 70)
        print("TEST RESULTS SUMMARY")
        print("=" * 70)
        
        total = self.results["passed"] + self.results["failed"]
        passed = self.results["passed"]
        failed = self.results["failed"]
        
        print(f"\n✅ PASSED: {passed}")
        print(f"❌ FAILED: {failed}")
        print(f"📊 TOTAL:  {total}")
        
        if total > 0:
            pass_rate = (passed / total) * 100
            print(f"📈 PASS RATE: {pass_rate:.1f}%")
        
        # Save results
        results_path = Path("Shadow/manus_archive/memory_root_test_results.json")
        results_path.parent.mkdir(parents=True, exist_ok=True)
        with open(results_path, "w") as f:
            json.dump(self.results, f, indent=2)
        
        print(f"\n✅ Results saved to {results_path}")
        
        print("\n" + "=" * 70)

# ============================================================================
# ENTRY POINT
# ============================================================================

async def main():
    """Run test suite."""
    suite = MemoryRootTestSuite()
    await suite.run_all_tests()

if __name__ == "__main__":
    asyncio.run(main())

