import hashlib
import hmac
import json
import os
from datetime import datetime
from typing import Any, Dict, List, Optional

import jwt
import redis
import uvicorn
from fastapi import Depends, FastAPI, Header, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel

# Initialize FastAPI app
app = FastAPI(title="Zapier Integration Service")

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

# Zapier configuration
ZAPIER_SECRET = os.getenv("ZAPIER_SECRET", "your-zapier-secret")

# Data models


class WebhookEvent(BaseModel):
    event_type: str
    payload: Dict[str, Any]
    source: str
    timestamp: datetime


class WebhookResponse(BaseModel):
    status: str
    message: str
    event_id: Optional[str]


class TokenData(BaseModel):
    user_id: str


class ZapierTriggerRequest(BaseModel):
    trigger: str
    data: Dict[str, Any]


class ZapierActionRequest(BaseModel):
    action: str
    parameters: Dict[str, Any]

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

# Zapier webhook signature verification


def verify_zapier_signature(payload: bytes, signature: str, secret: str) -> bool:
    expected_signature = hmac.new(
        secret.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected_signature, signature)

# Health check endpoint


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "Zapier Integration"}

# Webhook endpoint for receiving events from Zapier


@app.post("/webhook/zapier", response_model=WebhookResponse)
async def zapier_webhook(
    request: Request,
    x_zapier_signature: str = Header(None),
    x_zapier_event: str = Header(None)
):
    # Get raw body for signature verification
    body = await request.body()

    # Verify Zapier signature if provided
    if x_zapier_signature and ZAPIER_SECRET:
        if not verify_zapier_signature(body, x_zapier_signature, ZAPIER_SECRET):
            raise HTTPException(status_code=401, detail="Invalid signature")

    try:
        # Parse JSON payload
        payload = await request.json()

        # Create webhook event
        event = WebhookEvent(
            event_type=x_zapier_event or "zapier_webhook",
            payload=payload,
            source="zapier",
            timestamp=datetime.utcnow()
        )

        # Generate event ID (MD5 for non-security ID generation)
        event_id = hashlib.md5(f"{event.event_type}{event.timestamp}".encode(), usedforsecurity=False).hexdigest()

        # Store event in Redis queue
        event_data = {
            "event_id": event_id,
            "event_type": event.event_type,
            "payload": event.payload,
            "source": event.source,
            "timestamp": event.timestamp.isoformat()
        }

        redis_client.lpush("zapier_events_queue", json.dumps(event_data))
        redis_client.publish("zapier_events", json.dumps(event_data))

        return WebhookResponse(
            status="success",
            message="Webhook received and queued",
            event_id=event_id
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid payload: {str(e)}")

# Endpoint to send data to Zapier (trigger a Zap)


@app.post("/api/trigger", response_model=WebhookResponse)
async def trigger_zapier_event(
    trigger_request: ZapierTriggerRequest,
    token: TokenData = Depends(verify_token)
):
    try:
        # Create event data
        event_data = {
            "trigger": trigger_request.trigger,
            "data": trigger_request.data,
            "timestamp": datetime.utcnow().isoformat()
        }

        # Store in Redis for Zapier to consume
        redis_client.lpush("zapier_triggers_queue", json.dumps(event_data))
        redis_client.publish("zapier_triggers", json.dumps(event_data))

        # Generate event ID (MD5 for non-security ID generation)
        event_id = hashlib.md5(f"{trigger_request.trigger}{datetime.utcnow()}".encode(), usedforsecurity=False).hexdigest()

        return WebhookResponse(
            status="success",
            message="Trigger event sent to Zapier",
            event_id=event_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to trigger Zapier event: {str(e)}")

# Endpoint to execute a Zapier action


@app.post("/api/action", response_model=WebhookResponse)
async def execute_zapier_action(
    action_request: ZapierActionRequest,
    token: TokenData = Depends(verify_token)
):
    try:
        # Create action data
        action_data = {
            "action": action_request.action,
            "parameters": action_request.parameters,
            "timestamp": datetime.utcnow().isoformat()
        }

        # Store in Redis for Zapier to consume
        redis_client.lpush("zapier_actions_queue", json.dumps(action_data))
        redis_client.publish("zapier_actions", json.dumps(action_data))

        # Generate event ID (MD5 for non-security ID generation)
        event_id = hashlib.md5(f"{action_request.action}{datetime.utcnow()}".encode(), usedforsecurity=False).hexdigest()

        return WebhookResponse(
            status="success",
            message="Action sent to Zapier",
            event_id=event_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to execute Zapier action: {str(e)}")

# Endpoint to get webhook events


@app.get("/api/events", response_model=List[Dict[str, Any]])
async def get_webhook_events(limit: int = 10, token: TokenData = Depends(verify_token)):
    events = []
    for event_json in redis_client.lrange("zapier_events_queue", 0, limit - 1):
        events.append(json.loads(event_json))
    return events

# Endpoint to get triggers


@app.get("/api/triggers", response_model=List[Dict[str, Any]])
async def get_zapier_triggers(limit: int = 10, token: TokenData = Depends(verify_token)):
    triggers = []
    for trigger_json in redis_client.lrange("zapier_triggers_queue", 0, limit - 1):
        triggers.append(json.loads(trigger_json))
    return triggers

# Endpoint to get actions


@app.get("/api/actions", response_model=List[Dict[str, Any]])
async def get_zapier_actions(limit: int = 10, token: TokenData = Depends(verify_token)):
    actions = []
    for action_json in redis_client.lrange("zapier_actions_queue", 0, limit - 1):
        actions.append(json.loads(action_json))
    return actions

# Endpoint to get webhook status


@app.get("/api/webhooks/status")
async def get_webhooks_status(token: TokenData = Depends(verify_token)):
    # Get queue lengths
    events_count = redis_client.llen("zapier_events_queue")
    triggers_count = redis_client.llen("zapier_triggers_queue")
    actions_count = redis_client.llen("zapier_actions_queue")

    return {
        "webhookCount": events_count,
        "triggerCount": triggers_count,
        "actionCount": actions_count,
        "status": "operational"
    }

# Endpoint to get service information


@app.get("/api/info")
async def get_service_info():
    return {
        "name": "Zapier Integration Service",
        "version": "1.0.0",
        "description": "Handles integration with Zapier for workflow automation"
    }

# Test endpoint for Zapier integration


@app.get("/api/test")
async def test_zapier_integration(token: TokenData = Depends(verify_token)):
    return {
        "status": "Zapier integration service is running",
        "timestamp": datetime.utcnow().isoformat()
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)  # nosec B104
