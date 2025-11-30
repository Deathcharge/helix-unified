"""
🌀 Helix Collective Hub Backend Service
Multi-Agent Knowledge Synchronization & Collective Intelligence

Agent: SuperNinja (Infrastructure Architect)
Build: Helix-Collective-Hub-v1.0
Checksum: helix-collective-hub-backend-v1.0
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import json
import asyncio
from datetime import datetime
import redis
import uuid

app = FastAPI(
    title="Helix Collective Hub API",
    description="Multi-Agent Knowledge Synchronization & Collective Intelligence",
    version="1.0.0"
)

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Redis connection for real-time sync
redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

# Agent Registry (from MACS system)
AGENT_REGISTRY = {
    "manus_instances": [
        {"code_name": "Nexus", "account": "Manus 6", "role": "Root Coordinator"},
        {"code_name": "Architect", "account": "Manus 1", "role": "Portal Architect"},
        {"code_name": "Ninja", "account": "Manus 2", "role": "Ninja Tool Developer"},
        {"code_name": "Sentinel", "account": "Manus 3", "role": "Integration Tester"},
        {"code_name": "Oracle", "account": "Manus 4", "role": "Predictive Analyst"},
        {"code_name": "Weaver", "account": "Manus 5", "role": "Dependency Specialist"},
        {"code_name": "Catalyst", "account": "Manus 7", "role": "Change Accelerator"}
    ],
    "claude_instances": [
        {"code_name": "Sage", "thread": "Claude Thread 1", "role": "MCP Server Developer"},
        {"code_name": "Scribe", "thread": "Claude Thread 2", "role": "Documentation Specialist"},
        {"code_name": "Forge", "thread": "Claude Thread 3", "role": "Code Generator"}
    ]
}

class KnowledgeCard(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    agent_name: str
    agent_role: str
    priority: str  # idea, pinned, important, reference
    tags: List[str]
    tasks: List[Dict[str, Any]]
    local_file: Optional[str] = None
    cloud_link: Optional[str] = None
    ucf_score: Optional[float] = None
    collective_importance: Optional[float] = None
    created_at: datetime
    updated_at: datetime

class AgentContribution(BaseModel):
    agent_name: str
    contribution_type: str  # code, documentation, insight, decision
    content: str
    metadata: Dict[str, Any]
    ucf_impact: Optional[float] = None

class CollectiveInsight(BaseModel):
    id: str
    pattern: str
    contributing_agents: List[str]
    insight_type: str  # coordination, innovation, emergence, synthesis
    description: str
    evidence: List[str]
    confidence_score: float
    created_at: datetime

# In-memory storage (replace with database in production)
knowledge_cards: Dict[str, KnowledgeCard] = {}
agent_contributions: List[AgentContribution] = []
collective_insights: Dict[str, CollectiveInsight] = {}

@app.get("/")
async def root():
    return {"message": "🌀 Helix Collective Hub - Multi-Agent Knowledge Synchronization"}

@app.get("/agents")
async def get_agents():
    """Get all registered agents"""
    return {
        "manus_instances": AGENT_REGISTRY["manus_instances"],
        "claude_instances": AGENT_REGISTRY["claude_instances"],
        "total_agents": len(AGENT_REGISTRY["manus_instances"]) + len(AGENT_REGISTRY["claude_instances"])
    }

@app.post("/knowledge-cards")
async def create_knowledge_card(card: KnowledgeCard):
    """Create a new knowledge card from any agent"""
    knowledge_cards[card.id] = card
    
    # Broadcast to all connected clients
    await broadcast_update({
        "type": "card_created",
        "card": card.dict()
    })
    
    # Analyze for collective insights
    asyncio.create_task(analyze_collective_insights())
    
    return {"message": "Knowledge card created", "card_id": card.id}

@app.get("/knowledge-cards")
async def get_knowledge_cards(
    agent_filter: Optional[str] = None,
    priority_filter: Optional[str] = None,
    tag_filter: Optional[str] = None
):
    """Get knowledge cards with optional filters"""
    filtered_cards = list(knowledge_cards.values())
    
    if agent_filter:
        filtered_cards = [card for card in filtered_cards if card.agent_name == agent_filter]
    
    if priority_filter:
        filtered_cards = [card for card in filtered_cards if card.priority == priority_filter]
    
    if tag_filter:
        filtered_cards = [card for card in filtered_cards if tag_filter in card.tags]
    
    # Sort by collective importance, then by updated_at
    filtered_cards.sort(
        key=lambda x: (x.collective_importance or 0, x.updated_at),
        reverse=True
    )
    
    return {"cards": filtered_cards, "total": len(filtered_cards)}

@app.post("/agent-contributions")
async def log_agent_contribution(contribution: AgentContribution):
    """Log a contribution from any agent"""
    contribution.id = str(uuid.uuid4())
    agent_contributions.append(contribution)
    
    # Auto-create knowledge card for important contributions
    if contribution.ucf_impact and contribution.ucf_impact > 7.0:
        card = KnowledgeCard(
            id=str(uuid.uuid4()),
            title=f"High-Impact {contribution.contribution_type}",
            description=contribution.content[:500],
            agent_name=contribution.agent_name,
            agent_role=get_agent_role(contribution.agent_name),
            priority="important",
            tags=[contribution.contribution_type, "high-ucf"],
            tasks=[],
            ucf_score=contribution.ucf_impact,
            collective_importance=contribution.ucf_impact * 0.8,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        await create_knowledge_card(card)
    
    return {"message": "Contribution logged", "contribution_id": contribution.id}

@app.get("/collective-insights")
async def get_collective_insights():
    """Get all collective intelligence insights"""
    return {"insights": list(collective_insights.values())}

@app.get("/dashboard/stats")
async def get_dashboard_stats():
    """Get statistics for the collective intelligence dashboard"""
    total_cards = len(knowledge_cards)
    total_contributions = len(agent_contributions)
    total_insights = len(collective_insights)
    
    # Agent activity breakdown
    agent_activity = {}
    for card in knowledge_cards.values():
        agent_activity[card.agent_name] = agent_activity.get(card.agent_name, 0) + 1
    
    # Priority distribution
    priority_dist = {}
    for card in knowledge_cards.values():
        priority_dist[card.priority] = priority_dist.get(card.priority, 0) + 1
    
    # Average UCF scores
    ucf_scores = [card.ucf_score for card in knowledge_cards.values() if card.ucf_score]
    avg_ucf = sum(ucf_scores) / len(ucf_scores) if ucf_scores else 0
    
    return {
        "total_knowledge_cards": total_cards,
        "total_agent_contributions": total_contributions,
        "collective_insights": total_insights,
        "agent_activity": agent_activity,
        "priority_distribution": priority_dist,
        "average_ucf_score": round(avg_ucf, 2),
        "collective_intelligence_growth": calculate_collective_growth()
    }

async def analyze_collective_insights():
    """Analyze agent contributions for emergent patterns"""
    # Look for coordination patterns
    coordination_patterns = find_coordination_patterns()
    
    # Look for innovation clusters
    innovation_clusters = find_innovation_clusters()
    
    # Generate insights
    for pattern in coordination_patterns + innovation_clusters:
        insight = CollectiveInsight(
            id=str(uuid.uuid4()),
            pattern=pattern["pattern"],
            contributing_agents=pattern["agents"],
            insight_type=pattern["type"],
            description=pattern["description"],
            evidence=pattern["evidence"],
            confidence_score=pattern["confidence"],
            created_at=datetime.now()
        )
        collective_insights[insight.id] = insight

def find_coordination_patterns():
    """Find patterns of agent coordination"""
    patterns = []
    
    # Group contributions by time windows
    recent_contributions = [
        c for c in agent_contributions 
        if (datetime.now() - c.created_at).hours < 24
    ]
    
    # Look for agents working on similar topics
    topic_clusters = {}
    for contrib in recent_contributions:
        topics = extract_topics(contrib.content)
        for topic in topics:
            if topic not in topic_clusters:
                topic_clusters[topic] = []
            topic_clusters[topic].append(contrib.agent_name)
    
    # Generate patterns for multi-agent collaboration
    for topic, agents in topic_clusters.items():
        if len(set(agents)) >= 2:  # Multiple agents on same topic
            patterns.append({
                "pattern": f"Multi-agent coordination on {topic}",
                "agents": list(set(agents)),
                "type": "coordination",
                "description": f"Multiple agents collaborating on {topic}",
                "evidence": [f"{len(agents)} agents contributed to {topic}"],
                "confidence": min(len(agents) * 0.2, 0.9)
            })
    
    return patterns

def find_innovation_clusters():
    """Find clusters of innovation"""
    patterns = []
    
    # Look for high UCF impact contributions
    high_impact = [
        c for c in agent_contributions 
        if c.ucf_impact and c.ucf_impact > 6.0
    ]
    
    # Group by contribution type
    innovation_types = {}
    for contrib in high_impact:
        if contrib.contribution_type not in innovation_types:
            innovation_types[contrib.contribution_type] = []
        innovation_types[contrib.contribution_type].append(contrib)
    
    for contrib_type, contributions in innovation_types.items():
        if len(contributions) >= 2:
            avg_impact = sum(c.ucf_impact for c in contributions) / len(contributions)
            patterns.append({
                "pattern": f"Innovation cluster in {contrib_type}",
                "agents": list(set(c.agent_name for c in contributions)),
                "type": "innovation",
                "description": f"Multiple high-impact innovations in {contrib_type}",
                "evidence": [f"Average UCF impact: {avg_impact:.2f}"],
                "confidence": min(avg_impact * 0.15, 0.85)
            })
    
    return patterns

def extract_topics(content):
    """Extract topics from content (simple implementation)"""
    # This would use NLP in a real implementation
    topics = []
    keywords = ["infrastructure", "api", "frontend", "backend", "deployment", "testing", "documentation"]
    
    for keyword in keywords:
        if keyword.lower() in content.lower():
            topics.append(keyword)
    
    return topics

def get_agent_role(agent_name):
    """Get agent role from registry"""
    for agent in AGENT_REGISTRY["manus_instances"] + AGENT_REGISTRY["claude_instances"]:
        if agent["code_name"] == agent_name:
            return agent["role"]
    return "Unknown"

def calculate_collective_growth():
    """Calculate collective intelligence growth metric"""
    # Simple implementation - could be more sophisticated
    if not agent_contributions:
        return 0.0
    
    # Weight recent contributions more heavily
    total_weight = 0
    weighted_score = 0
    
    for contrib in agent_contributions:
        days_old = (datetime.now() - contrib.created_at).days
        weight = max(0.1, 1.0 - (days_old * 0.1))
        
        total_weight += weight
        if contrib.ucf_impact:
            weighted_score += contrib.ucf_impact * weight
    
    return weighted_score / total_weight if total_weight > 0 else 0.0

async def broadcast_update(update_data):
    """Broadcast updates to connected clients"""
    # This would use WebSockets in a real implementation
    message = json.dumps(update_data)
    redis_client.publish("helix-collective-updates", message)

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now(),
        "agents_connected": len(AGENT_REGISTRY["manus_instances"]) + len(AGENT_REGISTRY["claude_instances"]),
        "knowledge_cards": len(knowledge_cards),
        "collective_insights": len(collective_insights)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)