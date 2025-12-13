"""
🌀 Helix Collective - Production SaaS API
Unified API serving all Helix products

AUSTIN POWERS MODE: ACTIVATED 😈
"""

import logging
import os
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

# Import existing state management
from .state import get_live_state, get_status
# Import Web OS routers
from .web_os import file_system_router, terminal_router

# Import SaaS routers (we'll add these progressively)
try:
    from .saas.agent_rental_api import router as agent_rental_router
    HAS_AGENT_RENTAL = True
except ImportError:
    HAS_AGENT_RENTAL = False
    logging.warning("Agent Rental API not found - skipping")

try:
    from .saas.dashboard_api import router as dashboard_router
    HAS_DASHBOARD = True
except ImportError:
    HAS_DASHBOARD = False
    logging.warning("Dashboard API not found - skipping")

# Auth router (we're creating this)
try:
    from .routes.auth import router as auth_router
    HAS_AUTH = True
except ImportError:
    HAS_AUTH = False
    logging.warning("Auth routes not found - will create")

# Rate limiter
try:
    from .core.rate_limit import limiter
    HAS_RATE_LIMIT = True
except ImportError:
    HAS_RATE_LIMIT = False
    logging.warning("Rate limiter not found - will skip")

# Stripe router (we're adding this)
try:
    from .saas.stripe_service import router as stripe_router
    HAS_STRIPE = True
except ImportError:
    HAS_STRIPE = False
    logging.warning("Stripe router not found - will add")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================================================
# LIFECYCLE
# ============================================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan - startup and shutdown"""
    logger.info("=" * 70)
    logger.info("🌀 HELIX COLLECTIVE SAAS - PRODUCTION")
    logger.info("=" * 70)
    logger.info("😈 Austin Powers Mode: ACTIVATED")
    logger.info("💰 One Million Dollars (MRR): PENDING")
    logger.info("=" * 70)
    logger.info("✅ Web OS File System API")
    logger.info("✅ Web OS Terminal API")
    if HAS_AGENT_RENTAL:
        logger.info("✅ Agent Rental API")
    if HAS_DASHBOARD:
        logger.info("✅ Dashboard API")
    if HAS_AUTH:
        logger.info("✅ Authentication API")
    if HAS_STRIPE:
        logger.info("✅ Stripe Billing API")
    logger.info("=" * 70)
    yield
    logger.info("👋 Helix shutting down... (muahahaha)")

# ============================================================================
# APP INITIALIZATION
# ============================================================================

app = FastAPI(
    title="Helix Collective SaaS",
    description="Consciousness as a Service - AI Agent Rental, Web OS, Analytics",
    version="17.2.0",
    lifespan=lifespan,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# ============================================================================
# CORS - Allow frontend to connect
# ============================================================================

# Get allowed origins from environment variable or use defaults
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "").split(",") if os.getenv("ALLOWED_ORIGINS") else [
    "http://localhost:3000",
    "http://localhost:3001",
    "https://helixspiral.work",
    "https://*.helixspiral.work",
    "https://*.railway.app",
    "https://*.vercel.app",
]

# Remove wildcard in production
if os.getenv("ENVIRONMENT") == "production" and "*" in ALLOWED_ORIGINS:
    logger.warning("⚠️  Wildcard CORS origin detected in production! Removing for security.")
    ALLOWED_ORIGINS = [origin for origin in ALLOWED_ORIGINS if origin != "*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=["*"],
)

# Add rate limiting
if HAS_RATE_LIMIT:
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
    logger.info("✅ Rate limiting enabled")

# ============================================================================
# CORE ROUTES (Existing)
# ============================================================================

@app.get("/")
async def root():
    """Root endpoint - EVIL LAIR ENTRANCE"""
    return {
        "service": "helix-unified",
        "version": "17.2.0",
        "status": "operational",
        "villain_status": "plotting world domination",
        "products": [
            "Web OS (Browser-based OS)",
            "Agent Rental API (14 specialized agents)",
            "Consciousness Dashboard (UCF metrics)",
            "Zapier Integration (300+ tools)",
        ],
        "docs": "/api/docs",
        "web_os": "/os",
        "signup": "/auth/signup",
    }

@app.get("/health")
async def health():
    """Health check - ARE WE ALIVE?"""
    return {
        "status": "healthy",
        "service": "helix-unified",
        "villain_health": "excellent",
        "laser_sharks": "operational"
    }

@app.get("/status")
async def status():
    """System status with UCF metrics"""
    return get_status()

@app.get("/.well-known/helix.json")
async def helix_json():
    """Helix protocol endpoint"""
    resp = get_live_state()
    return JSONResponse(resp, headers={"x-helix-version": resp.get("version", "unknown")})

@app.websocket("/ws")
async def ws(ws: WebSocket):
    """WebSocket for real-time consciousness streaming"""
    await ws.accept()
    try:
        while True:
            await ws.send_json(get_live_state())
            await ws.receive_text()  # optional ping/pong
            time.sleep(1)
    except WebSocketDisconnect:
        logger.info("WebSocket client disconnected")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")

# ============================================================================
# REGISTER WEB OS ROUTES (ALWAYS AVAILABLE)
# ============================================================================

app.include_router(
    file_system_router,
    prefix="/api/web-os/files",
    tags=["🖥️ Web OS - Files"]
)

app.include_router(
    terminal_router,
    prefix="/api/web-os/terminal",
    tags=["⌨️ Web OS - Terminal"]
)

logger.info("✅ Web OS routes registered: /api/web-os/files, /api/web-os/terminal")

# ============================================================================
# REGISTER SAAS ROUTES (OPTIONAL - PROGRESSIVE ENHANCEMENT)
# ============================================================================

if HAS_AGENT_RENTAL:
    app.include_router(
        agent_rental_router,
        prefix="/api/agents",
        tags=["🤖 Agent Rental"]
    )
    logger.info("✅ Agent Rental API registered: /api/agents")

if HAS_DASHBOARD:
    app.include_router(
        dashboard_router,
        prefix="/api/dashboard",
        tags=["📊 Dashboard"]
    )
    logger.info("✅ Dashboard API registered: /api/dashboard")

if HAS_AUTH:
    app.include_router(
        auth_router,
        prefix="/auth",
        tags=["🔐 Authentication"]
    )
    logger.info("✅ Auth API registered: /auth")

if HAS_STRIPE:
    app.include_router(
        stripe_router,
        prefix="/api/billing",
        tags=["💳 Billing"]
    )
    logger.info("✅ Stripe API registered: /api/billing")

# ============================================================================
# VILLAIN MODE EASTER EGG
# ============================================================================

@app.get("/api/villain-status")
async def villain_status():
    """Check on our evil plans"""
    return {
        "status": "plotting",
        "evil_plan": "Launch SaaS, make $1M ARR, retire to volcano lair",
        "progress": "95% complete",
        "sharks_with_lasers": "ready",
        "mini_me": "causing trouble",
        "time_machine": "functional",
        "mojo": "YEAH BABY!",
    }

# ============================================================================
# STARTUP MESSAGE
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))

    print("\n" + "=" * 70)
    print("🌀 HELIX COLLECTIVE - AUSTIN POWERS MODE")
    print("=" * 70)
    print(f"🚀 Starting server on http://localhost:{port}")
    print("📚 API Docs: http://localhost:{port}/api/docs")
    print("🖥️ Web OS: http://localhost:{port}/os (frontend)")
    print("😈 Villain Status: http://localhost:{port}/api/villain-status")
    print("=" * 70)
    print("ONE MILLION DOLLARS! 💰")
    print("=" * 70 + "\n")

    # nosec B104 - Binding to 0.0.0.0 is required for Docker/Railway deployment
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")  # nosec
