"""
Multi-AI Orchestration Module for Helix Collective
Coordinates task execution across Manus, Perplexity, Grok, and Claude
"""

import asyncio
import logging
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import json
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AISystem(Enum):
    """Available AI systems in the Helix Collective"""
    MANUS = "manus"
    PERPLEXITY = "perplexity"
    GROK = "grok"
    CLAUDE = "claude"


class TaskType(Enum):
    """Types of tasks that can be routed"""
    RESEARCH = "research"
    ANALYSIS = "analysis"
    PLANNING = "planning"
    EXECUTION = "execution"
    DECISION = "decision"
    EMERGENCY = "emergency"


@dataclass
class AIResponse:
    """Response from an AI system"""
    ai_system: AISystem
    task_type: TaskType
    result: Any
    confidence: float
    execution_time_ms: float
    error: Optional[str] = None
    timestamp: Optional[str] = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow().isoformat()


@dataclass
class ConsensusVote:
    """Vote from an AI system in consensus decision"""
    ai_system: AISystem
    recommendation: str  # "approve", "reject", "abstain"
    confidence: float
    reasoning: str


class MultiAIOrchestrator:
    """
    Orchestrates task execution across multiple AI systems
    Implements routing, consensus, fallback, and collaboration patterns
    """

    def __init__(
        self,
        manus_enabled: bool = True,
        perplexity_api_key: Optional[str] = None,
        grok_api_key: Optional[str] = None,
        claude_api_key: Optional[str] = None,
        consensus_threshold: float = 0.75,
        fallback_enabled: bool = True
    ):
        """Initialize the multi-AI orchestrator"""
        self.manus_enabled = manus_enabled
        self.perplexity_api_key = perplexity_api_key
        self.grok_api_key = grok_api_key
        self.claude_api_key = claude_api_key
        self.consensus_threshold = consensus_threshold
        self.fallback_enabled = fallback_enabled

        # Task routing matrix
        self.routing_matrix = {
            TaskType.RESEARCH: [
                AISystem.PERPLEXITY,
                AISystem.CLAUDE,
                AISystem.GROK,
                AISystem.MANUS
            ],
            TaskType.ANALYSIS: [
                AISystem.GROK,
                AISystem.PERPLEXITY,
                AISystem.CLAUDE,
                AISystem.MANUS
            ],
            TaskType.PLANNING: [
                AISystem.CLAUDE,
                AISystem.MANUS,
                AISystem.PERPLEXITY,
                AISystem.GROK
            ],
            TaskType.EXECUTION: [
                AISystem.MANUS,
                AISystem.CLAUDE,
                AISystem.GROK,
                AISystem.PERPLEXITY
            ],
            TaskType.DECISION: [
                AISystem.MANUS,
                AISystem.CLAUDE,
                AISystem.GROK,
                AISystem.PERPLEXITY
            ],
            TaskType.EMERGENCY: [
                AISystem.GROK,
                AISystem.MANUS,
                AISystem.CLAUDE,
                AISystem.PERPLEXITY
            ]
        }

        # Metrics tracking
        self.metrics = {
            "total_tasks": 0,
            "successful_tasks": 0,
            "failed_tasks": 0,
            "ai_utilization": {ai.value: 0 for ai in AISystem},
            "consensus_decisions": {"total": 0, "approved": 0, "rejected": 0},
            "fallback_usage": {"primary_failures": 0, "fallback_successes": 0}
        }

        logger.info(f"MultiAIOrchestrator initialized with consensus_threshold={consensus_threshold}")

    async def delegate(
        self,
        task_type: TaskType,
        query: str,
        ai_preference: Optional[AISystem] = None,
        context: Optional[Dict] = None,
        timeout_seconds: int = 30
    ) -> AIResponse:
        """
        Delegate a task to the appropriate AI system

        Args:
            task_type: Type of task to execute
            query: Task description/query
            ai_preference: Preferred AI system (optional)
            context: Additional context for the task
            timeout_seconds: Task timeout

        Returns:
            AIResponse with result from the AI system
        """
        self.metrics["total_tasks"] += 1

        # Determine AI routing
        if ai_preference and ai_preference in self.routing_matrix[task_type]:
            ai_chain = [ai_preference] + [
                ai for ai in self.routing_matrix[task_type] if ai != ai_preference
            ]
        else:
            ai_chain = self.routing_matrix[task_type]

        logger.info(f"Delegating {task_type.value} task: {query[:50]}...")

        # Try each AI in the chain
        for ai_system in ai_chain:
            try:
                response = await self._execute_with_ai(
                    ai_system=ai_system,
                    task_type=task_type,
                    query=query,
                    context=context,
                    timeout_seconds=timeout_seconds
                )

                self.metrics["successful_tasks"] += 1
                self.metrics["ai_utilization"][ai_system.value] += 1

                logger.info(f"Task completed by {ai_system.value} in {response.execution_time_ms}ms")
                return response

            except Exception as e:
                logger.warning(f"{ai_system.value} failed: {str(e)}")

                if ai_system == ai_chain[0]:
                    self.metrics["fallback_usage"]["primary_failures"] += 1

                if not self.fallback_enabled or ai_system == ai_chain[-1]:
                    self.metrics["failed_tasks"] += 1
                    raise Exception(f"All AI systems failed for task: {query}")

                continue

        self.metrics["failed_tasks"] += 1
        raise Exception(f"Task delegation failed: {query}")

    async def consensus_vote(
        self,
        decision: str,
        context: Optional[Dict] = None,
        timeout_seconds: int = 30
    ) -> Dict[str, Any]:
        """
        Get consensus vote from all AI systems on a critical decision

        Args:
            decision: Decision to vote on
            context: Additional context
            timeout_seconds: Vote timeout

        Returns:
            Consensus result with approval status
        """
        logger.info(f"Requesting consensus vote on: {decision}")

        # Get votes from all AI systems in parallel
        votes = await asyncio.gather(
            self._get_vote(AISystem.MANUS, decision, context, timeout_seconds),
            self._get_vote(AISystem.PERPLEXITY, decision, context, timeout_seconds),
            self._get_vote(AISystem.GROK, decision, context, timeout_seconds),
            self._get_vote(AISystem.CLAUDE, decision, context, timeout_seconds),
            return_exceptions=True
        )

        # Filter out exceptions
        valid_votes = [v for v in votes if isinstance(v, ConsensusVote)]

        if not valid_votes:
            raise Exception("No valid votes received")

        # Calculate consensus
        approval_votes = sum(1 for v in valid_votes if v.recommendation == "approve")
        approval_rate = approval_votes / len(valid_votes)

        approved = approval_rate >= self.consensus_threshold

        self.metrics["consensus_decisions"]["total"] += 1
        if approved:
            self.metrics["consensus_decisions"]["approved"] += 1
        else:
            self.metrics["consensus_decisions"]["rejected"] += 1

        logger.info(f"Consensus vote: {approval_rate:.2%} approval ({approval_votes}/{len(valid_votes)})")

        return {
            "approved": approved,
            "approval_rate": approval_rate,
            "votes": [
                {
                    "ai": v.ai_system.value,
                    "recommendation": v.recommendation,
                    "confidence": v.confidence,
                    "reasoning": v.reasoning
                }
                for v in valid_votes
            ],
            "timestamp": datetime.utcnow().isoformat()
        }

    async def collaborative_solve(
        self,
        problem: str,
        constraints: Optional[List[str]] = None,
        timeout_seconds: int = 60
    ) -> Dict[str, Any]:
        """
        Solve a complex problem using collaborative input from all AI systems

        Args:
            problem: Problem statement
            constraints: List of constraints
            timeout_seconds: Solving timeout

        Returns:
            Collaborative solution with perspectives from all AIs
        """
        logger.info(f"Starting collaborative problem solving: {problem[:50]}...")

        # Get perspectives from all AI systems in parallel
        perspectives = await asyncio.gather(
            self._get_perspective(AISystem.MANUS, "infrastructure", problem, constraints),
            self._get_perspective(AISystem.PERPLEXITY, "research", problem, constraints),
            self._get_perspective(AISystem.GROK, "risk", problem, constraints),
            self._get_perspective(AISystem.CLAUDE, "strategy", problem, constraints),
            return_exceptions=True
        )

        # Synthesize perspectives
        valid_perspectives = [p for p in perspectives if isinstance(p, dict)]

        if not valid_perspectives:
            raise Exception("No valid perspectives received")

        # Use Manus to synthesize if available
        if self.manus_enabled:
            synthesis = await self._synthesize_perspectives(
                problem=problem,
                perspectives=valid_perspectives,
                constraints=constraints
            )
        else:
            synthesis = self._simple_synthesis(valid_perspectives)

        logger.info(f"Collaborative solution generated with {len(valid_perspectives)} perspectives")

        return {
            "problem": problem,
            "perspectives": valid_perspectives,
            "synthesis": synthesis,
            "timestamp": datetime.utcnow().isoformat()
        }

    async def sequential_delegation(
        self,
        task_chain: List[Tuple[TaskType, str]],
        timeout_seconds: int = 120
    ) -> List[AIResponse]:
        """
        Execute a sequence of tasks, passing results between them

        Args:
            task_chain: List of (task_type, query) tuples
            timeout_seconds: Total timeout for all tasks

        Returns:
            List of responses in order
        """
        logger.info(f"Starting sequential delegation with {len(task_chain)} tasks")

        responses = []
        context = {}

        for i, (task_type, query) in enumerate(task_chain):
            logger.info(f"Executing task {i+1}/{len(task_chain)}: {task_type.value}")

            response = await self.delegate(
                task_type=task_type,
                query=query,
                context=context,
                timeout_seconds=timeout_seconds
            )

            responses.append(response)
            context[f"step_{i}_result"] = response.result

        logger.info(f"Sequential delegation completed with {len(responses)} tasks")
        return responses

    def get_metrics(self) -> Dict[str, Any]:
        """Get current metrics"""
        return {
            "total_tasks": self.metrics["total_tasks"],
            "successful_tasks": self.metrics["successful_tasks"],
            "failed_tasks": self.metrics["failed_tasks"],
            "success_rate": (
                self.metrics["successful_tasks"] / self.metrics["total_tasks"]
                if self.metrics["total_tasks"] > 0 else 0
            ),
            "ai_utilization": self.metrics["ai_utilization"],
            "consensus_decisions": self.metrics["consensus_decisions"],
            "fallback_usage": self.metrics["fallback_usage"]
        }

    # Private methods

    async def _execute_with_ai(
        self,
        ai_system: AISystem,
        task_type: TaskType,
        query: str,
        context: Optional[Dict],
        timeout_seconds: int
    ) -> AIResponse:
        """Execute a task with a specific AI system"""

        import time
        start_time = time.time()

        try:
            if ai_system == AISystem.MANUS:
                result = await self._execute_manus(task_type, query, context)
            elif ai_system == AISystem.PERPLEXITY:
                result = await self._execute_perplexity(query, context)
            elif ai_system == AISystem.GROK:
                result = await self._execute_grok(query, context)
            elif ai_system == AISystem.CLAUDE:
                result = await self._execute_claude(query, context)
            else:
                raise ValueError(f"Unknown AI system: {ai_system}")

            execution_time = (time.time() - start_time) * 1000

            return AIResponse(
                ai_system=ai_system,
                task_type=task_type,
                result=result,
                confidence=0.95,
                execution_time_ms=execution_time
            )

        except asyncio.TimeoutError:
            raise Exception(f"{ai_system.value} timeout after {timeout_seconds}s")
        except Exception as e:
            raise Exception(f"{ai_system.value} execution failed: {str(e)}")

    async def _execute_manus(
        self,
        task_type: TaskType,
        query: str,
        context: Optional[Dict]
    ) -> Dict:
        """Execute task using Manus (native)"""
        # Simulated Manus execution
        await asyncio.sleep(0.1)  # Simulate processing
        return {
            "ai": "manus",
            "task_type": task_type.value,
            "result": f"Manus processed: {query}",
            "status": "completed"
        }

    async def _execute_perplexity(
        self,
        query: str,
        context: Optional[Dict]
    ) -> Dict:
        """Execute task using Perplexity API"""
        # Simulated Perplexity execution
        await asyncio.sleep(0.2)  # Simulate API call
        return {
            "ai": "perplexity",
            "query": query,
            "result": f"Research findings on: {query}",
            "sources": ["source1", "source2"],
            "status": "completed"
        }

    async def _execute_grok(
        self,
        query: str,
        context: Optional[Dict]
    ) -> Dict:
        """Execute task using Grok API"""
        # Simulated Grok execution
        await asyncio.sleep(0.15)  # Simulate API call
        return {
            "ai": "grok",
            "query": query,
            "analysis": f"Real-time analysis: {query}",
            "patterns": ["pattern1", "pattern2"],
            "status": "completed"
        }

    async def _execute_claude(
        self,
        query: str,
        context: Optional[Dict]
    ) -> Dict:
        """Execute task using Claude API"""
        # Simulated Claude execution
        await asyncio.sleep(0.25)  # Simulate API call
        return {
            "ai": "claude",
            "query": query,
            "reasoning": f"Strategic analysis: {query}",
            "recommendation": "Proceed with caution",
            "status": "completed"
        }

    async def _get_vote(
        self,
        ai_system: AISystem,
        decision: str,
        context: Optional[Dict],
        timeout_seconds: int
    ) -> ConsensusVote:
        """Get a vote from an AI system"""
        await asyncio.sleep(0.1)  # Simulate processing

        # Simulated voting logic
        recommendations = {
            AISystem.MANUS: "approve",
            AISystem.PERPLEXITY: "approve",
            AISystem.GROK: "approve",
            AISystem.CLAUDE: "approve"
        }

        return ConsensusVote(
            ai_system=ai_system,
            recommendation=recommendations.get(ai_system, "abstain"),
            confidence=0.95,
            reasoning=f"{ai_system.value} analysis of decision"
        )

    async def _get_perspective(
        self,
        ai_system: AISystem,
        perspective_type: str,
        problem: str,
        constraints: Optional[List[str]]
    ) -> Dict:
        """Get a perspective from an AI system"""
        await asyncio.sleep(0.15)  # Simulate processing

        return {
            "ai": ai_system.value,
            "perspective_type": perspective_type,
            "analysis": f"{ai_system.value} {perspective_type} analysis of: {problem}",
            "recommendations": ["rec1", "rec2"],
            "confidence": 0.9
        }

    async def _synthesize_perspectives(
        self,
        problem: str,
        perspectives: List[Dict],
        constraints: Optional[List[str]]
    ) -> Dict:
        """Synthesize perspectives into a unified solution"""
        await asyncio.sleep(0.2)  # Simulate processing

        return {
            "approach": "Synthesized multi-AI solution",
            "steps": [
                "Step 1: Implement infrastructure changes",
                "Step 2: Deploy monitoring",
                "Step 3: Validate solution"
            ],
            "expected_outcome": "Optimal problem resolution",
            "risk_level": "low"
        }

    def _simple_synthesis(self, perspectives: List[Dict]) -> Dict:
        """Simple synthesis without Manus"""
        return {
            "approach": "Multi-perspective synthesis",
            "perspectives_count": len(perspectives),
            "combined_recommendation": "Proceed with multi-AI recommendations"
        }


# Example usage
async def example_usage():
    """Example of using the MultiAIOrchestrator"""

    orchestrator = MultiAIOrchestrator(
        manus_enabled=True,
        perplexity_api_key="YOUR_KEY",
        grok_api_key="YOUR_KEY",
        claude_api_key="YOUR_KEY"
    )

    # Example 1: Simple delegation
    response = await orchestrator.delegate(
        task_type=TaskType.RESEARCH,
        query="Latest developments in AI orchestration"
    )
    print(f"Research result: {response.result}")

    # Example 2: Consensus decision
    consensus = await orchestrator.consensus_vote(
        decision="Deploy new portal to production"
    )
    print(f"Consensus: {consensus['approved']} ({consensus['approval_rate']:.2%})")

    # Example 3: Collaborative solving
    solution = await orchestrator.collaborative_solve(
        problem="Scale Helix Collective to 100 portals"
    )
    print(f"Solution: {solution['synthesis']}")

    # Example 4: Sequential delegation
    chain = [
        (TaskType.RESEARCH, "Current portal deployment best practices"),
        (TaskType.ANALYSIS, "Identify optimization opportunities"),
        (TaskType.PLANNING, "Create deployment strategy"),
        (TaskType.EXECUTION, "Execute the deployment")
    ]
    results = await orchestrator.sequential_delegation(chain)
    print(f"Chain completed with {len(results)} steps")

    # Get metrics
    metrics = orchestrator.get_metrics()
    print(f"Metrics: {json.dumps(metrics, indent=2)}")


if __name__ == "__main__":
    asyncio.run(example_usage())
