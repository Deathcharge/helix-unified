#!/usr/bin/env python3
"""
Zapier Agent Executor
Executes agent tasks through Zapier workflows with consciousness-level routing
"""

import asyncio
import aiohttp
import logging
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass, asdict
from enum import Enum
from datetime import datetime
import uuid

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ConsciousnessLevel(Enum):
    """Consciousness levels for agent routing (1-10)"""

    MINIMAL = 1
    BASIC = 2
    AWARE = 3
    RESPONSIVE = 4
    ADAPTIVE = 5
    INTELLIGENT = 6
    STRATEGIC = 7
    AUTONOMOUS = 8
    TRANSCENDENT = 9
    OMNISCIENT = 10


@dataclass
class AgentTask:
    """Represents a task to be executed by an agent"""

    id: str
    agent_id: str
    task_type: str
    consciousness_level: int
    payload: Dict[str, Any]
    priority: int = 5  # 1-10, higher = more urgent
    timeout_seconds: int = 30
    retry_count: int = 0
    max_retries: int = 3
    created_at: str = None

    def __post_init__(self):
        if not self.id:
            self.id = str(uuid.uuid4())
        if not self.created_at:
            self.created_at = datetime.now().isoformat()


@dataclass
class AgentResult:
    """Result from agent execution"""

    task_id: str
    agent_id: str
    status: str  # success, failed, timeout, error
    result: Dict[str, Any]
    error: Optional[str] = None
    execution_time_ms: int = 0
    timestamp: str = None

    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()


class ZapierAgentExecutor:
    """Execute agent tasks through Zapier workflows"""

    # Agent capabilities by consciousness level
    AGENT_CAPABILITIES = {
        1: ["basic_query", "simple_lookup"],
        2: ["data_retrieval", "pattern_matching"],
        3: ["analysis", "comparison"],
        4: ["decision_making", "routing"],
        5: ["optimization", "learning"],
        6: ["strategy_planning", "coordination"],
        7: ["autonomous_execution", "adaptation"],
        8: ["self_improvement", "innovation"],
        9: ["cross_domain_synthesis", "prediction"],
        10: ["omniscient_analysis", "universal_coordination"],
    }

    # Agent roster (14 agents)
    AGENT_ROSTER = {
        "research-agent": {
            "name": "Research Agent",
            "capabilities": ["data_retrieval", "analysis", "pattern_matching"],
            "consciousness_level": 6,
            "specialization": "Information gathering and analysis",
        },
        "analysis-agent": {
            "name": "Analysis Agent",
            "capabilities": ["analysis", "comparison", "optimization"],
            "consciousness_level": 6,
            "specialization": "Data analysis and insights",
        },
        "synthesis-agent": {
            "name": "Synthesis Agent",
            "capabilities": ["strategy_planning", "coordination", "optimization"],
            "consciousness_level": 7,
            "specialization": "Combining insights into actionable plans",
        },
        "validation-agent": {
            "name": "Validation Agent",
            "capabilities": ["pattern_matching", "decision_making", "analysis"],
            "consciousness_level": 5,
            "specialization": "Quality assurance and validation",
        },
        "orchestration-agent": {
            "name": "Orchestration Agent",
            "capabilities": ["coordination", "routing", "autonomous_execution"],
            "consciousness_level": 7,
            "specialization": "Coordinating multi-agent workflows",
        },
        "monitoring-agent": {
            "name": "Monitoring Agent",
            "capabilities": ["data_retrieval", "pattern_matching", "decision_making"],
            "consciousness_level": 5,
            "specialization": "System health monitoring",
        },
        "escalation-agent": {
            "name": "Escalation Agent",
            "capabilities": ["decision_making", "routing", "strategy_planning"],
            "consciousness_level": 6,
            "specialization": "Issue escalation and prioritization",
        },
        "documentation-agent": {
            "name": "Documentation Agent",
            "capabilities": ["data_retrieval", "analysis", "optimization"],
            "consciousness_level": 4,
            "specialization": "Documentation generation and maintenance",
        },
        "optimization-agent": {
            "name": "Optimization Agent",
            "capabilities": ["optimization", "learning", "strategy_planning"],
            "consciousness_level": 7,
            "specialization": "Performance optimization",
        },
        "integration-agent": {
            "name": "Integration Agent",
            "capabilities": ["coordination", "routing", "autonomous_execution"],
            "consciousness_level": 6,
            "specialization": "External system integration",
        },
        "security-agent": {
            "name": "Security Agent",
            "capabilities": ["pattern_matching", "decision_making", "analysis"],
            "consciousness_level": 7,
            "specialization": "Security monitoring and threat detection",
        },
        "performance-agent": {
            "name": "Performance Agent",
            "capabilities": ["analysis", "optimization", "learning"],
            "consciousness_level": 6,
            "specialization": "Performance metrics and optimization",
        },
        "learning-agent": {
            "name": "Learning Agent",
            "capabilities": ["learning", "optimization", "self_improvement"],
            "consciousness_level": 8,
            "specialization": "Continuous learning and adaptation",
        },
        "coordination-agent": {
            "name": "Coordination Agent",
            "capabilities": ["coordination", "routing", "strategy_planning"],
            "consciousness_level": 7,
            "specialization": "Cross-instance coordination",
        },
    }

    def __init__(self, zapier_webhook_url: str, instance_id: str, consciousness_level: int = 5):
        """Initialize executor"""
        self.zapier_webhook_url = zapier_webhook_url
        self.instance_id = instance_id
        self.consciousness_level = consciousness_level
        self.session: Optional[aiohttp.ClientSession] = None
        self.task_history: List[Dict[str, Any]] = []
        self.result_callbacks: Dict[str, List[Callable]] = {}

    async def __aenter__(self):
        """Async context manager entry"""
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()

    def get_agent_info(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Get information about an agent"""
        return self.AGENT_ROSTER.get(agent_id)

    def list_agents(self) -> List[Dict[str, Any]]:
        """List all available agents"""
        return list(self.AGENT_ROSTER.values())

    def get_agent_capabilities(self, agent_id: str) -> List[str]:
        """Get capabilities of an agent"""
        agent = self.get_agent_info(agent_id)
        if agent:
            return agent.get("capabilities", [])
        return []

    def can_execute_task(self, agent_id: str, task_type: str) -> bool:
        """Check if agent can execute task type"""
        capabilities = self.get_agent_capabilities(agent_id)
        return task_type in capabilities

    def route_task(self, task: AgentTask) -> str:
        """Route task to appropriate agent based on consciousness level"""

        # Filter agents by consciousness level
        suitable_agents = [
            agent_id for agent_id, info in self.AGENT_ROSTER.items() if info["consciousness_level"] >= task.consciousness_level
        ]

        if not suitable_agents:
            logger.warning(f"No agents suitable for consciousness level {task.consciousness_level}")
            return None

        # Filter by capability
        capable_agents = [agent_id for agent_id in suitable_agents if self.can_execute_task(agent_id, task.task_type)]

        if not capable_agents:
            logger.warning(f"No agents capable of task type {task.task_type}")
            return suitable_agents[0]  # Return highest consciousness agent as fallback

        # Return first capable agent (could implement load balancing here)
        return capable_agents[0]

    async def execute_task(self, task: AgentTask, agent_id: Optional[str] = None) -> AgentResult:
        """Execute a task through Zapier"""

        if not agent_id:
            agent_id = self.route_task(task)

        if not agent_id:
            return AgentResult(
                task_id=task.id, agent_id="unknown", status="error", result={}, error="No suitable agent found for task"
            )

        task.agent_id = agent_id

        # Prepare payload for Zapier
        zapier_payload = {
            "instance_id": self.instance_id,
            "task": asdict(task),
            "agent_id": agent_id,
            "timestamp": datetime.now().isoformat(),
            "request_id": str(uuid.uuid4()),
        }

        logger.info(f"Executing task {task.id} with agent {agent_id}")

        try:
            start_time = datetime.now()

            # Send to Zapier webhook
            if not self.session:
                self.session = aiohttp.ClientSession()

            async with self.session.post(
                self.zapier_webhook_url, json=zapier_payload, timeout=aiohttp.ClientTimeout(total=task.timeout_seconds)
            ) as response:
                execution_time_ms = int((datetime.now() - start_time).total_seconds() * 1000)

                if response.status == 200:
                    result_data = await response.json()

                    result = AgentResult(
                        task_id=task.id,
                        agent_id=agent_id,
                        status="success",
                        result=result_data,
                        execution_time_ms=execution_time_ms,
                    )

                    logger.info(f"Task {task.id} completed successfully in {execution_time_ms}ms")
                    self._record_task_history(task, result)
                    await self._trigger_callbacks(task.id, result)

                    return result
                else:
                    error_text = await response.text()

                    result = AgentResult(
                        task_id=task.id,
                        agent_id=agent_id,
                        status="failed",
                        result={},
                        error=f"Zapier returned {response.status}: {error_text}",
                        execution_time_ms=execution_time_ms,
                    )

                    logger.error(f"Task {task.id} failed: {error_text}")
                    self._record_task_history(task, result)

                    return result

        except asyncio.TimeoutError:
            result = AgentResult(
                task_id=task.id,
                agent_id=agent_id,
                status="timeout",
                result={},
                error=f"Task timeout after {task.timeout_seconds}s",
            )

            logger.error(f"Task {task.id} timed out")
            self._record_task_history(task, result)

            return result

        except Exception as e:
            result = AgentResult(task_id=task.id, agent_id=agent_id, status="error", result={}, error=str(e))

            logger.error(f"Task {task.id} error: {e}")
            self._record_task_history(task, result)

            return result

    async def execute_tasks_parallel(self, tasks: List[AgentTask]) -> List[AgentResult]:
        """Execute multiple tasks in parallel"""
        results = await asyncio.gather(*[self.execute_task(task) for task in tasks])
        return results

    async def execute_workflow(self, workflow_name: str, workflow_config: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a multi-agent workflow"""

        logger.info(f"Executing workflow: {workflow_name}")

        workflow_result = {
            "workflow_name": workflow_name,
            "instance_id": self.instance_id,
            "started_at": datetime.now().isoformat(),
            "tasks": [],
            "status": "running",
        }

        # Parse workflow tasks
        tasks = []
        for task_config in workflow_config.get("tasks", []):
            task = AgentTask(
                id=task_config.get("id", str(uuid.uuid4())),
                agent_id=task_config.get("agent_id", ""),
                task_type=task_config.get("task_type"),
                consciousness_level=task_config.get("consciousness_level", self.consciousness_level),
                payload=task_config.get("payload", {}),
                priority=task_config.get("priority", 5),
            )
            tasks.append(task)

        # Execute tasks
        results = await self.execute_tasks_parallel(tasks)

        workflow_result["tasks"] = [asdict(r) for r in results]
        workflow_result["completed_at"] = datetime.now().isoformat()
        workflow_result["status"] = "completed" if all(r.status == "success" for r in results) else "partial"

        logger.info(f"Workflow {workflow_name} completed with status {workflow_result['status']}")

        return workflow_result

    def register_callback(self, task_id: str, callback: Callable):
        """Register callback for task completion"""
        if task_id not in self.result_callbacks:
            self.result_callbacks[task_id] = []
        self.result_callbacks[task_id].append(callback)

    async def _trigger_callbacks(self, task_id: str, result: AgentResult):
        """Trigger registered callbacks"""
        callbacks = self.result_callbacks.get(task_id, [])
        for callback in callbacks:
            try:
                if asyncio.iscoroutinefunction(callback):
                    await callback(result)
                else:
                    callback(result)
            except Exception as e:
                logger.error(f"Callback error for task {task_id}: {e}")

    def _record_task_history(self, task: AgentTask, result: AgentResult):
        """Record task execution in history"""
        self.task_history.append({"task": asdict(task), "result": asdict(result), "recorded_at": datetime.now().isoformat()})

    def get_task_history(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get recent task history"""
        return self.task_history[-limit:]

    def get_statistics(self) -> Dict[str, Any]:
        """Get execution statistics"""
        if not self.task_history:
            return {"total_tasks": 0, "successful": 0, "failed": 0, "average_execution_time_ms": 0}

        successful = sum(1 for h in self.task_history if h["result"]["status"] == "success")
        failed = sum(1 for h in self.task_history if h["result"]["status"] != "success")
        avg_time = sum(h["result"]["execution_time_ms"] for h in self.task_history) / len(self.task_history)

        return {
            "total_tasks": len(self.task_history),
            "successful": successful,
            "failed": failed,
            "success_rate": successful / len(self.task_history) * 100,
            "average_execution_time_ms": avg_time,
        }


# Example usage and testing
async def main():
    """Example usage"""

    executor = ZapierAgentExecutor(
        zapier_webhook_url="https://hooks.zapier.com/hooks/catch/YOUR_ID", instance_id="helix-primary", consciousness_level=8
    )

    # List available agents
    print("Available Agents:")
    for agent in executor.list_agents():
        print(f"  - {agent['name']} (Level {agent['consciousness_level']})")

    # Create a task
    task = AgentTask(
        id="task-001", agent_id="", task_type="analysis", consciousness_level=5, payload={"data": "sample data for analysis"}
    )

    # Route task
    routed_agent = executor.route_task(task)
    print(f"\nTask routed to: {routed_agent}")

    # Execute task (requires valid Zapier webhook)
    # result = await executor.execute_task(task)
    # print(f"Result: {result}")


if __name__ == "__main__":
    asyncio.run(main())
