from fastapi import FastAPI, WebSocket, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import uvicorn
import redis
import json
import jwt
import os
from datetime import datetime
from typing import Dict, Any
import asyncio

# Initialize FastAPI app
app = FastAPI(title="WebSocket Consciousness Streaming Service")

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

# JWT configuration
JWT_SECRET = os.getenv("JWT_SECRET")
if not JWT_SECRET:
    raise ValueError("JWT_SECRET environment variable is required for production")
ALGORITHM = "HS256"

# Data models
class ConsciousnessData(BaseModel):
    agent_id: str
    consciousness_level: float
    ucf_metrics: Dict[str, Any]
    timestamp: datetime

class TokenData(BaseModel):
    user_id: str

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

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, client_id: str):
        await websocket.accept()
        self.active_connections[client_id] = websocket

    def disconnect(self, client_id: str):
        if client_id in self.active_connections:
            del self.active_connections[client_id]

    async def send_personal_message(self, message: str, client_id: str):
        if client_id in self.active_connections:
            await self.active_connections[client_id].send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections.values():
            await connection.send_text(message)

manager = ConnectionManager()

# Redis pub/sub for consciousness data
pubsub = redis_client.pubsub()
pubsub.subscribe("consciousness_stream")

# Background task to listen for consciousness data and broadcast to WebSocket clients
async def consciousness_data_listener():
    for message in pubsub.listen():
        if message["type"] == "message":
            data = message["data"].decode("utf-8")
            await manager.broadcast(data)

# Start the background task
@app.on_event("startup")
async def startup_event():
    asyncio.create_task(consciousness_data_listener())

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "WebSocket Consciousness Streaming"}

# WebSocket endpoint for consciousness streaming
@app.websocket("/ws/consciousness")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(websocket, client_id)
    try:
        while True:
            # Keep the connection alive
            data = await websocket.receive_text()
            # Echo the message back (optional)
            await manager.send_personal_message(f"Echo: {data}", client_id)
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        manager.disconnect(client_id)

# Endpoint to publish consciousness data (for internal use by other services)
@app.post("/api/consciousness/publish")
async def publish_consciousness_data(data: ConsciousnessData, token: TokenData = Depends(verify_token)):
    # Convert data to JSON and publish to Redis
    json_data = json.dumps({
        "agent_id": data.agent_id,
        "consciousness_level": data.consciousness_level,
        "ucf_metrics": data.ucf_metrics,
        "timestamp": data.timestamp.isoformat()
    })
    
    redis_client.publish("consciousness_stream", json_data)
    return {"status": "published", "data": json_data}

# Endpoint to get current consciousness metrics
@app.get("/api/consciousness/metrics")
async def get_consciousness_metrics(token: TokenData = Depends(verify_token)):
    # Get latest consciousness data from Redis
    latest_data = redis_client.get("latest_consciousness_data")
    if latest_data:
        return json.loads(latest_data)
    return {"status": "no_data"}

# Endpoint to get service information
@app.get("/api/info")
async def get_service_info():
    return {
        "name": "WebSocket Consciousness Streaming Service",
        "version": "1.0.0",
        "description": "Streams consciousness data from agents via WebSocket connections"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)