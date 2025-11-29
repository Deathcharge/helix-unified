from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import uvicorn
import redis
import json
import jwt
import os
from datetime import datetime
import psycopg2
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Initialize FastAPI app
app = FastAPI(title="Agent Orchestration Service")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Redis connection
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
redis_client = redis.from_url(REDIS_URL)

# Database connection
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/agent_orchestration")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# JWT configuration
JWT_SECRET = os.getenv("JWT_SECRET", "your-secret-key")
ALGORITHM = "HS256"

# Database models


class AgentProfile(Base):
    __tablename__ = "agent_profiles"

    id = Column(Integer, primary_key=True, index=True)
    agent_id = Column(String, unique=True, index=True)
    name = Column(String, index=True)
    role = Column(String)
    capabilities = Column(Text)  # JSON string
    status = Column(String, default="inactive")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)


class AgentTask(Base):
    __tablename__ = "agent_tasks"

    id = Column(Integer, primary_key=True, index=True)
    agent_id = Column(String, index=True)
    task_type = Column(String)
    task_data = Column(Text)  # JSON string
    status = Column(String, default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)


# Create tables
Base.metadata.create_all(bind=engine)

# Data models


class AgentProfileCreate(BaseModel):
    agent_id: str
    name: str
    role: str
    capabilities: List[str]


class AgentProfileResponse(AgentProfileCreate):
    id: int
    status: str
    created_at: datetime
    updated_at: datetime


class AgentTaskCreate(BaseModel):
    agent_id: str
    task_type: str
    task_data: Dict[str, Any]


class AgentTaskResponse(AgentTaskCreate):
    id: int
    status: str
    created_at: datetime
    completed_at: Optional[datetime]


class TokenData(BaseModel):
    user_id: str

# Dependency


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# JWT token verification


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        token = credentials.credentials
        payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return TokenData(user_id=user_id)
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

# Health check endpoint


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "Agent Orchestration"}

# Agent profile management endpoints


@app.post("/api/agents", response_model=AgentProfileResponse)
async def create_agent_profile(agent: AgentProfileCreate, db=Depends(get_db), token: TokenData = Depends(verify_token)):
    # Check if agent already exists
    existing_agent = db.query(AgentProfile).filter(AgentProfile.agent_id == agent.agent_id).first()
    if existing_agent:
        raise HTTPException(status_code=400, detail="Agent already exists")

    # Create new agent profile
    db_agent = AgentProfile(
        agent_id=agent.agent_id,
        name=agent.name,
        role=agent.role,
        capabilities=json.dumps(agent.capabilities),
        status="active"
    )
    db.add(db_agent)
    db.commit()
    db.refresh(db_agent)

    # Publish agent creation event to Redis
    agent_event = {
        "event": "agent_created",
        "agent_id": agent.agent_id,
        "timestamp": datetime.utcnow().isoformat()
    }
    redis_client.publish("agent_events", json.dumps(agent_event))

    return db_agent


@app.get("/api/agents", response_model=List[AgentProfileResponse])
async def list_agents(skip: int = 0, limit: int = 100, db=Depends(get_db), token: TokenData = Depends(verify_token)):
    agents = db.query(AgentProfile).offset(skip).limit(limit).all()
    return agents


@app.get("/api/agents/{agent_id}", response_model=AgentProfileResponse)
async def get_agent_profile(agent_id: str, db=Depends(get_db), token: TokenData = Depends(verify_token)):
    agent = db.query(AgentProfile).filter(AgentProfile.agent_id == agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent


@app.put("/api/agents/{agent_id}", response_model=AgentProfileResponse)
async def update_agent_profile(
        agent_id: str,
        agent: AgentProfileCreate,
        db=Depends(get_db),
        token: TokenData = Depends(verify_token)):
    db_agent = db.query(AgentProfile).filter(AgentProfile.agent_id == agent_id).first()
    if not db_agent:
        raise HTTPException(status_code=404, detail="Agent not found")

    db_agent.name = agent.name
    db_agent.role = agent.role
    db_agent.capabilities = json.dumps(agent.capabilities)
    db_agent.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_agent)

    # Publish agent update event to Redis
    agent_event = {
        "event": "agent_updated",
        "agent_id": agent_id,
        "timestamp": datetime.utcnow().isoformat()
    }
    redis_client.publish("agent_events", json.dumps(agent_event))

    return db_agent


@app.delete("/api/agents/{agent_id}")
async def delete_agent_profile(agent_id: str, db=Depends(get_db), token: TokenData = Depends(verify_token)):
    db_agent = db.query(AgentProfile).filter(AgentProfile.agent_id == agent_id).first()
    if not db_agent:
        raise HTTPException(status_code=404, detail="Agent not found")

    db.delete(db_agent)
    db.commit()

    # Publish agent deletion event to Redis
    agent_event = {
        "event": "agent_deleted",
        "agent_id": agent_id,
        "timestamp": datetime.utcnow().isoformat()
    }
    redis_client.publish("agent_events", json.dumps(agent_event))

    return {"message": "Agent deleted successfully"}

# Agent task management endpoints


@app.post("/api/tasks", response_model=AgentTaskResponse)
async def create_agent_task(task: AgentTaskCreate, db=Depends(get_db), token: TokenData = Depends(verify_token)):
    db_task = AgentTask(
        agent_id=task.agent_id,
        task_type=task.task_type,
        task_data=json.dumps(task.task_data)
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)

    # Publish task creation event to Redis for agent consumption
    task_event = {
        "event": "task_created",
        "task_id": db_task.id,
        "agent_id": task.agent_id,
        "task_type": task.task_type,
        "task_data": task.task_data,
        "timestamp": datetime.utcnow().isoformat()
    }
    redis_client.publish("agent_task_queue", json.dumps(task_event))

    return db_task


@app.get("/api/tasks", response_model=List[AgentTaskResponse])
async def list_agent_tasks(skip: int = 0, limit: int = 100, db=Depends(get_db), token: TokenData = Depends(verify_token)):
    tasks = db.query(AgentTask).offset(skip).limit(limit).all()
    return tasks


@app.get("/api/tasks/{task_id}", response_model=AgentTaskResponse)
async def get_agent_task(task_id: int, db=Depends(get_db), token: TokenData = Depends(verify_token)):
    task = db.query(AgentTask).filter(AgentTask.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.put("/api/tasks/{task_id}")
async def update_agent_task_status(
        task_id: int,
        status: str,
        completed_at: Optional[datetime] = None,
        db=Depends(get_db),
        token: TokenData = Depends(verify_token)):
    db_task = db.query(AgentTask).filter(AgentTask.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    db_task.status = status
    if completed_at:
        db_task.completed_at = completed_at
    db.commit()

    # Publish task update event to Redis
    task_event = {
        "event": "task_updated",
        "task_id": task_id,
        "status": status,
        "timestamp": datetime.utcnow().isoformat()
    }
    redis_client.publish("agent_task_events", json.dumps(task_event))

    return {"message": "Task updated successfully"}

# Agent status endpoints


@app.get("/api/agents/status")
async def get_agents_status(token: TokenData = Depends(verify_token)):
    # Get agent status from Redis (published by agents)
    agent_statuses = {}
    for key in redis_client.scan_iter("agent_status:*"):
        agent_id = key.decode().split(":")[1]
        status_data = redis_client.get(key)
        if status_data:
            agent_statuses[agent_id] = json.loads(status_data.decode())

    return {
        "agentCount": len(agent_statuses),
        "statuses": agent_statuses
    }

# Endpoint to get service information


@app.get("/api/info")
async def get_service_info():
    return {
        "name": "Agent Orchestration Service",
        "version": "1.0.0",
        "description": "Manages agent profiles, tasks, and coordination"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
