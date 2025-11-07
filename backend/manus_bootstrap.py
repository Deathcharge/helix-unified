# 🌀 Helix Collective v14.5 — Quantum Handshake
# backend/manus_bootstrap.py — Manus Bootstrap FastAPI Application
# Author: Andrew John Ward (Architect)

import json
import os
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Optional

import aiohttp
from fastapi import Depends, FastAPI, HTTPException
from services.zapier_client import ZapierClient, validate_zapier_config

# ============================================================================
# GLOBAL STATE
# ============================================================================

_http_session: Optional[aiohttp.ClientSession] = None
_zapier_client: Optional[ZapierClient] = None

# ============================================================================
# LIFESPAN MANAGEMENT
# ============================================================================


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    FastAPI lifespan context manager for startup and shutdown.

    Startup:
    - Create aiohttp.ClientSession for connection pooling
    - Initialize ZapierClient with shared session
    - Validate Zapier webhook configuration
    - Log startup event

    Shutdown:
    - Close aiohttp session gracefully
    - Log shutdown event
    """
    global _http_session, _zapier_client

    # ====================================================================
    # STARTUP
    # ====================================================================
    print("\n" + "=" * 70)
    print("🤲 MANUS BOOTSTRAP — STARTUP")
    print("=" * 70)

    # Create HTTP session
    print("\n📡 Creating aiohttp session...")
    _http_session = aiohttp.ClientSession()
    print("   ✅ Session created")

    # Initialize Zapier client
    print("\n🔗 Initializing Zapier client...")
    _zapier_client = ZapierClient(_http_session)

    # Validate Zapier configuration
    config = validate_zapier_config()
    print(f"   Event Hook:  {'✅' if config['event_hook'] else '⚠'}")
    print(f"   Agent Hook:  {'✅' if config['agent_hook'] else '⚠'}")
    print(f"   System Hook: {'✅' if config['system_hook'] else '⚠'}")

    if not config["all_configured"]:
        print("\n   ⚠️  WARNING: Not all Zapier webhooks configured!")
        print("      Set environment variables:")
        print("      - ZAPIER_EVENT_HOOK_URL")
        print("      - ZAPIER_AGENT_HOOK_URL")
        print("      - ZAPIER_SYSTEM_HOOK_URL")
    else:
        print("\n   ✅ All Zapier webhooks configured")

    # Log startup event
    print("\n📝 Logging startup event...")
    try:
        await _zapier_client.log_event(
            title="Manus Bootstrap Started",
            event_type="Status",
            agent_name="Manus",
            description="Manus bootstrap application started on Railway",
            ucf_snapshot={
                "harmony": 0.355,
                "prana": 0.7,
                "drishti": 0.8,
                "klesha": 0.2,
                "timestamp": datetime.utcnow().isoformat(),
            },
        )
        print("   ✅ Startup event logged")
    except Exception as e:
        print(f"   ⚠️  Failed to log startup: {e}")

    # Update Manus status
    print("\n📊 Updating Manus status...")
    try:
        await _zapier_client.update_agent(
            agent_name="Manus", status="Active", last_action="Bootstrap startup", health_score=100
        )
        print("   ✅ Status updated")
    except Exception as e:
        print(f"   ⚠️  Failed to update status: {e}")

    # Update system component
    print("\n🔧 Updating system state...")
    try:
        await _zapier_client.upsert_system_component(
            component="Manus Bootstrap", status="Active", harmony=0.355, error_log="", verified=True
        )
        print("   ✅ System state updated")
    except Exception as e:
        print(f"   ⚠️  Failed to update system state: {e}")

    print("\n" + "=" * 70)
    print("✅ MANUS BOOTSTRAP READY")
    print("=" * 70 + "\n")

    yield  # Application runs here

    # ====================================================================
    # SHUTDOWN
    # ====================================================================
    print("\n" + "=" * 70)
    print("🛑 MANUS BOOTSTRAP — SHUTDOWN")
    print("=" * 70)

    # Log shutdown event
    print("\n📝 Logging shutdown event...")
    try:
        if _zapier_client:
            await _zapier_client.log_event(
                title="Manus Bootstrap Shutdown",
                event_type="Status",
                agent_name="Manus",
                description="Manus bootstrap application shutting down",
                ucf_snapshot={"harmony": 0.355, "timestamp": datetime.utcnow().isoformat()},
            )
            print("   ✅ Shutdown event logged")
    except Exception as e:
        print(f"   ⚠️  Failed to log shutdown: {e}")

    # Close HTTP session
    print("\n📡 Closing aiohttp session...")
    if _http_session and not _http_session.closed:
        await _http_session.close()
        print("   ✅ Session closed")

    print("\n" + "=" * 70)
    print("✅ MANUS BOOTSTRAP SHUTDOWN COMPLETE")
    print("=" * 70 + "\n")


# ============================================================================
# FASTAPI APPLICATION
# ============================================================================

app = FastAPI(
    title="Helix Collective v14.5 — Manus Bootstrap",
    description="Manus operational executor with Zapier integration",
    version="14.5",
    lifespan=lifespan,
)

# ============================================================================
# DEPENDENCY INJECTION
# ============================================================================


def get_zapier() -> ZapierClient:
    """Dependency injection for Zapier client."""
    if _zapier_client is None:
        raise HTTPException(status_code=503, detail="Zapier client not initialized")
    return _zapier_client


def get_http_session() -> aiohttp.ClientSession:
    """Dependency injection for HTTP session."""
    if _http_session is None or _http_session.closed:
        raise HTTPException(status_code=503, detail="HTTP session not available")
    return _http_session


# ============================================================================
# HEALTH CHECK ENDPOINTS
# ============================================================================


@app.get("/health")
async def health_check() -> dict:
    """
    Health check endpoint for Railway monitoring.

    Returns:
    - status: Overall health status
    - version: Application version
    - timestamp: Current timestamp
    - zapier: Zapier configuration status
    - session: HTTP session status
    """
    config = validate_zapier_config()

    return {
        "status": "healthy",
        "version": "14.5",
        "codename": "Quantum Handshake",
        "timestamp": datetime.utcnow().isoformat(),
        "zapier": {
            "configured": config["all_configured"],
            "event_hook": config["event_hook"],
            "agent_hook": config["agent_hook"],
            "system_hook": config["system_hook"],
        },
        "session": {
            "open": _http_session is not None and not _http_session.closed,
        },
    }


@app.get("/api/status")
async def api_status(zap: ZapierClient = Depends(get_zapier)) -> dict:
    """
    Detailed API status endpoint.

    Returns:
    - manus_status: Manus operational status
    - zapier_status: Zapier integration status
    - uptime: Application uptime
    """
    return {
        "manus_status": "operational",
        "zapier_status": "connected",
        "uptime": "calculating...",
        "timestamp": datetime.utcnow().isoformat(),
    }


# ============================================================================
# ZAPIER TEST ENDPOINTS
# ============================================================================


@app.post("/test/zapier")
async def test_zapier(zap: ZapierClient = Depends(get_zapier)) -> dict:
    """
    Test all three Zapier webhooks.

    Sends test payloads to:
    1. Event Log webhook
    2. Agent Registry webhook
    3. System State webhook

    Returns:
    - status: Overall test status
    - results: Individual webhook test results
    """
    results = {
        "event_log": False,
        "agent_registry": False,
        "system_state": False,
    }

    # Test Event Log webhook
    try:
        await zap.log_event(
            title="Zapier Test Event",
            event_type="Status",
            agent_name="Manus",
            description="Testing Zapier integration from Manus Bootstrap",
            ucf_snapshot={
                "harmony": 0.355,
                "prana": 0.7,
                "drishti": 0.8,
                "klesha": 0.2,
            },
        )
        results["event_log"] = True
    except Exception as e:
        print(f"❌ Event Log test failed: {e}")

    # Test Agent Registry webhook
    try:
        await zap.update_agent(
            agent_name="Manus", status="Active", last_action="Testing Zapier integration", health_score=100
        )
        results["agent_registry"] = True
    except Exception as e:
        print(f"❌ Agent Registry test failed: {e}")

    # Test System State webhook
    try:
        await zap.upsert_system_component(
            component="Manus Bootstrap", status="Active", harmony=0.355, error_log="", verified=True
        )
        results["system_state"] = True
    except Exception as e:
        print(f"❌ System State test failed: {e}")

    # Determine overall status
    all_passed = all(results.values())

    return {
        "status": "all_passed" if all_passed else "partial_failure",
        "results": results,
        "timestamp": datetime.utcnow().isoformat(),
    }


@app.post("/test/zapier/event")
async def test_event_webhook(zap: ZapierClient = Depends(get_zapier)) -> dict:
    """Test Event Log webhook only."""
    try:
        await zap.log_event(
            title="Event Log Webhook Test",
            event_type="Status",
            agent_name="Manus",
            description="Testing Event Log webhook",
            ucf_snapshot={"harmony": 0.355},
        )
        return {"status": "success", "webhook": "event_log"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/test/zapier/agent")
async def test_agent_webhook(zap: ZapierClient = Depends(get_zapier)) -> dict:
    """Test Agent Registry webhook only."""
    try:
        await zap.update_agent(
            agent_name="Manus", status="Active", last_action="Testing Agent Registry webhook", health_score=100
        )
        return {"status": "success", "webhook": "agent_registry"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/test/zapier/system")
async def test_system_webhook(zap: ZapierClient = Depends(get_zapier)) -> dict:
    """Test System State webhook only."""
    try:
        await zap.upsert_system_component(
            component="Manus Bootstrap", status="Active", harmony=0.355, error_log="", verified=True
        )
        return {"status": "success", "webhook": "system_state"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# MANUS OPERATION ENDPOINTS
# ============================================================================


@app.get("/api/manus/status")
async def manus_status(zap: ZapierClient = Depends(get_zapier)) -> dict:
    """Get Manus operational status."""
    return {
        "agent": "Manus",
        "status": "HARMONIC",
        "harmony": 0.355,
        "directives_processed": 0,
        "uptime_seconds": 0,
        "timestamp": datetime.utcnow().isoformat(),
    }


@app.post("/api/manus/directive")
async def process_directive(directive: dict, zap: ZapierClient = Depends(get_zapier)) -> dict:
    """
    Process a directive and log to Notion via Zapier.

    Expected directive format:
    {
        "command": "execute_ritual",
        "params": {...}
    }
    """
    try:
        # Log directive processing
        await zap.log_event(
            title=f"Directive: {directive.get('command', 'unknown')}",
            event_type="Command",
            agent_name="Manus",
            description=f"Processing directive: {json.dumps(directive)}",
            ucf_snapshot={"harmony": 0.355},
        )

        # Update Manus status
        await zap.update_agent(
            agent_name="Manus",
            status="Active",
            last_action=f"Processing {directive.get('command', 'unknown')}",
            health_score=95,
        )

        return {"status": "success", "directive": directive, "timestamp": datetime.utcnow().isoformat()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# CONFIGURATION ENDPOINTS
# ============================================================================


@app.get("/api/config/zapier")
async def get_zapier_config() -> dict:
    """Get Zapier configuration status."""
    config = validate_zapier_config()
    return {
        "configured": config["all_configured"],
        "webhooks": {
            "event_log": config["event_hook"],
            "agent_registry": config["agent_hook"],
            "system_state": config["system_hook"],
        },
    }


@app.get("/api/config/environment")
async def get_environment_config() -> dict:
    """Get environment configuration (safe values only)."""
    return {
        "environment": os.getenv("ENVIRONMENT", "development"),
        "version": "14.5",
        "codename": "Quantum Handshake",
        "zapier_configured": validate_zapier_config()["all_configured"],
    }


# ============================================================================
# ROOT ENDPOINT
# ============================================================================


@app.get("/")
async def root() -> dict:
    """Root endpoint with basic information."""
    return {
        "name": "Helix Collective v14.5",
        "codename": "Quantum Handshake",
        "agent": "Manus",
        "role": "Operational Executor",
        "status": "operational",
        "endpoints": {
            "health": "/health",
            "status": "/api/status",
            "manus_status": "/api/manus/status",
            "zapier_config": "/api/config/zapier",
            "test_zapier": "/test/zapier",
            "docs": "/docs",
            "redoc": "/redoc",
        },
    }


# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    import uvicorn

    # Run with: uvicorn backend.manus_bootstrap:app --reload
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", "8000")), log_level="info")
