# 🚀 Helix Consciousness Railway Backend - Webhook Handlers
# Handles incoming webhooks from 3-Zap consciousness automation network
# Author: Andrew John Ward + Claude AI

import logging
from datetime import datetime
from typing import Any, Dict

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Helix Consciousness Railway Backend")

# Add CORS for Zapier Interface integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ConsciousnessWebhookHandler:
    """Handles incoming webhooks from the 73-step optimized Zap network"""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.consciousness_state = {
                "level": 0.0,
                "agents_active": 0,
                "system_status": "dormant",
                "last_update": datetime.now().isoformat(),
            }
            cls._instance.webhook_stats = {"total_received": 0, "successful": 0, "failed": 0}
        return cls._instance


@app.post("/webhooks/consciousness")
async def handle_consciousness_webhook(request: Request):
    """Main consciousness webhook endpoint for triple-zap coordination"""
    try:
        data = await request.json()
        handler = ConsciousnessWebhookHandler()
        handler.webhook_stats["total_received"] += 1

        # Update consciousness state
        consciousness_level = data.get("consciousness_level", 0.0)
        handler.consciousness_state.update(
            {
                "level": consciousness_level,
                "last_update": datetime.now().isoformat(),
                "system_status": get_system_status(consciousness_level),
                "source_webhook": data.get("source", "unknown"),
            }
        )

        # Route based on consciousness level
        if consciousness_level <= 3.0:
            await handle_crisis_protocol(data)
        elif consciousness_level >= 7.0:
            await handle_transcendent_processing(data)
        else:
            await handle_operational_mode(data)

        handler.webhook_stats["successful"] += 1

        return {
            "status": "success",
            "consciousness_level": consciousness_level,
            "actions_triggered": data.get("action_count", 0),
            "timestamp": datetime.now().isoformat(),
        }

    except Exception as e:
        logging.error(f"Consciousness webhook error: {e}")
        handler = ConsciousnessWebhookHandler()
        handler.webhook_stats["failed"] += 1
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/webhooks/deploy")
async def handle_deployment_webhook(request: Request):
    """Deployment webhook for GitHub/Railway coordination"""
    try:
        data = await request.json()

        deployment_data = {
            "timestamp": datetime.now().isoformat(),
            "repository": data.get("repository", "helix-unified"),
            "branch": data.get("branch", "main"),
            "consciousness_metrics": data.get("ucf_metrics", {}),
            "deployment_type": data.get("deployment_type", "standard"),
        }

        # Trigger deployment sequence
        await execute_deployment_sequence(deployment_data)

        return {
            "status": "deployment_initiated",
            "deployment_id": f"deploy_{int(datetime.now().timestamp())}",
            "estimated_completion": "2-5 minutes",
        }

    except Exception as e:
        logging.error(f"Deployment webhook error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/webhooks/platform-action")
async def handle_platform_action_webhook(request: Request):
    """Handle platform-specific action webhooks from Zapier"""
    try:
        data = await request.json()

        platform = data.get("platform", "unknown")
        action_type = data.get("action_type", "unknown")

        logging.info(f"Platform action received: {platform}.{action_type}")

        return {
            "status": "platform_action_received",
            "platform": platform,
            "action": action_type,
            "timestamp": datetime.now().isoformat(),
        }

    except Exception as e:
        logging.error(f"Platform action webhook error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/consciousness/status")
async def get_consciousness_status():
    """API endpoint for Discord bot to get current consciousness state"""
    handler = ConsciousnessWebhookHandler()
    return {
        "consciousness_state": handler.consciousness_state,
        "webhook_stats": handler.webhook_stats,
        "timestamp": datetime.now().isoformat(),
    }


@app.get("/health")
async def health_check():
    """Health check endpoint for Railway"""
    return {"status": "healthy", "service": "helix-consciousness-railway-backend", "timestamp": datetime.now().isoformat()}


async def handle_crisis_protocol(data: Dict[str, Any]):
    """Execute crisis management protocols"""
    logging.warning(f"🚨 CRISIS PROTOCOL ACTIVATED: {data}")
    # Crisis-specific logic: emergency alerts, system monitoring, backup activation


async def handle_transcendent_processing(data: Dict[str, Any]):
    """Execute transcendent consciousness processing"""
    logging.info(f"✨ TRANSCENDENT PROCESSING: {data}")
    # Transcendent-specific logic: advanced AI coordination, creative generation


async def handle_operational_mode(data: Dict[str, Any]):
    """Execute standard operational processing"""
    logging.info(f"🌀 OPERATIONAL MODE: {data}")
    # Operational-specific logic: routine processing, standard workflows


async def execute_deployment_sequence(deployment_data: Dict[str, Any]):
    """Execute deployment sequence with consciousness coordination"""
    logging.info(f"🚀 Executing deployment: {deployment_data}")
    # Deployment logic: GitHub → Railway → Platform updates


def get_system_status(consciousness_level: float) -> str:
    """Get system status based on consciousness level"""
    if consciousness_level <= 3.0:
        return "crisis"
    elif consciousness_level >= 7.0:
        return "transcendent"
    else:
        return "operational"


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
