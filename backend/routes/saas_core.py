"""
💎 Helix Collective SaaS - Core API Router
==========================================

Wires up the complete SaaS platform infrastructure:
- Authentication & Authorization (JWT + API keys)
- Multi-LLM Smart Router (Anthropic, OpenAI, xAI, Perplexity)
- 14 AI Agents API
- Stripe Subscription Management

This router exposes the SaaS platform built in:
- backend/saas_auth.py (authentication system)
- backend/saas_router.py (multi-LLM routing)
- backend/saas_agents.py (AI agents)
- backend/saas_stripe.py (Stripe integration)

Revenue Model:
- Free: 100 requests/day, 3 agents, basic models
- Pro: 10K requests/day, all agents, all models ($29/mo)
- Workflow: 20K requests/day, workflow automation ($79/mo)
- Enterprise: Unlimited, white-label, SLA ($299/mo)

Projected Year 1 Revenue: $158K ARR

Author: Claude (Manus Validator)
Date: 2025-12-10
"""

import os
from datetime import datetime
from typing import Any, Dict, Optional

from fastapi import APIRouter, Depends, HTTPException, Request

# Import SaaS core modules
from backend.saas_auth import (
    # Auth functions
    register_user,
    login_user,
    create_api_key,
    list_api_keys,
    revoke_api_key,
    get_user_stats,
    # Dependencies
    get_current_user_jwt,
    get_current_user_api_key,
    # Models
    UserRegistration,
    UserLogin,
    APIKeyCreate,
    TokenResponse,
    APIKeyResponse,
    # Database
    Database,
    Cache,
)

from backend.saas_router import (
    # Chat functions
    chat_completion,
    get_available_models,
    estimate_cost,
    # Models
    ChatRequest,
    ChatResponse,
)

from backend.saas_agents import (
    # Agent functions
    execute_agent,
    list_agents,
    get_agent_info,
    # Models
    AgentExecutionRequest,
    AgentExecutionResponse,
)

from backend.saas_stripe import (
    # Stripe functions
    create_subscription,
    cancel_subscription,
    update_subscription,
    create_checkout_session,
    get_payment_history,
    handle_webhook_event,
    # Models
    SubscriptionRequest,
    CheckoutSessionRequest,
)

router = APIRouter()

# ============================================================================
# AUTHENTICATION ENDPOINTS
# ============================================================================


@router.post("/auth/register", response_model=TokenResponse, tags=["Authentication"])
async def auth_register(registration: UserRegistration):
    """
    Register new user account

    Returns JWT token and API key (shown only once!)

    - **email**: Valid email address
    - **password**: Minimum 8 characters, must contain uppercase, lowercase, digit
    - **full_name**: Optional full name
    - **company**: Optional company name

    New users start on Free tier (100 requests/day, 3 agents)
    """
    try:
        return await register_user(registration)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Registration failed: {str(e)}")


@router.post("/auth/login", response_model=TokenResponse, tags=["Authentication"])
async def auth_login(login: UserLogin):
    """
    Login with email and password

    Returns JWT token for API access

    - **email**: Account email
    - **password**: Account password
    """
    try:
        return await login_user(login)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Login failed: {str(e)}")


@router.post("/auth/api-keys", response_model=APIKeyResponse, tags=["Authentication"])
async def create_new_api_key(
    key_data: APIKeyCreate,
    user: Dict[str, Any] = Depends(get_current_user_jwt)
):
    """
    Create new API key for programmatic access

    Requires JWT authentication

    Returns full API key (shown only once!)

    - **name**: Descriptive name for this key
    - **scopes**: List of allowed scopes (chat, agents, prompts, workflows)
    - **expires_in_days**: Optional expiration in days (None = no expiration)
    """
    try:
        return await create_api_key(user["id"], key_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"API key creation failed: {str(e)}")


@router.get("/auth/api-keys", tags=["Authentication"])
async def get_api_keys(user: Dict[str, Any] = Depends(get_current_user_jwt)):
    """
    List all API keys for current user

    Requires JWT authentication

    Returns list of API keys (without full key values)
    """
    try:
        return await list_api_keys(user["id"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list API keys: {str(e)}")


@router.delete("/auth/api-keys/{key_id}", tags=["Authentication"])
async def delete_api_key(
    key_id: str,
    user: Dict[str, Any] = Depends(get_current_user_jwt)
):
    """
    Revoke (deactivate) an API key

    Requires JWT authentication

    - **key_id**: ID of the API key to revoke
    """
    try:
        await revoke_api_key(user["id"], key_id)
        return {"success": True, "message": "API key revoked"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to revoke API key: {str(e)}")


@router.get("/auth/me", tags=["Authentication"])
async def get_current_user(user: Dict[str, Any] = Depends(get_current_user_jwt)):
    """
    Get current user profile

    Requires JWT authentication

    Returns user data including tier, usage stats, and limits
    """
    try:
        stats = await get_user_stats(user["id"])
        return {
            "user": user,
            "stats": stats,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get user data: {str(e)}")


# ============================================================================
# MULTI-LLM CHAT ENDPOINTS
# ============================================================================


@router.post("/v1/chat", response_model=ChatResponse, tags=["Chat"])
async def chat(
    request: ChatRequest,
    user: Dict[str, Any] = Depends(get_current_user_api_key)
):
    """
    Chat completion with intelligent LLM routing

    Requires API key authentication

    **Smart Routing:**
    - `optimize=cost` → Routes to cheapest model for your tier
    - `optimize=speed` → Routes to fastest model
    - `optimize=quality` → Routes to highest quality model

    **Tier Access:**
    - Free: claude-3-haiku, gpt-3.5-turbo, llama-3
    - Pro+: All models including claude-3-opus, gpt-4, grok

    **Usage Tracking:**
    - Automatically tracks tokens, cost, and response time
    - Rate limiting enforced per tier
    - All usage visible in dashboard

    **Request:**
    - **messages**: List of chat messages (role: system/user/assistant, content: string)
    - **optimize**: Routing strategy (cost/speed/quality)
    - **model**: Optional specific model (or None for auto-routing)
    - **temperature**: 0.0-2.0 (default: 0.7)
    - **max_tokens**: 1-4096 (default: 1000)

    **Response:**
    - **id**: Unique completion ID
    - **model**: Model used
    - **provider**: LLM provider (anthropic/openai/xai/perplexity)
    - **choices**: List of completion choices
    - **usage**: Token usage statistics
    - **cost_usd**: Actual cost in USD
    - **response_time_ms**: Response time in milliseconds
    """
    try:
        return await chat_completion(request, user)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat completion failed: {str(e)}")


@router.get("/v1/models", tags=["Chat"])
async def get_models(user: Dict[str, Any] = Depends(get_current_user_api_key)):
    """
    Get available models for your tier

    Requires API key authentication

    Returns list of models with pricing and performance scores
    """
    try:
        models = await get_available_models(user["tier"])
        return {"models": models}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get models: {str(e)}")


@router.post("/v1/estimate", tags=["Chat"])
async def estimate_completion_cost(
    model: str,
    input_tokens: int,
    output_tokens: int,
    user: Dict[str, Any] = Depends(get_current_user_api_key)
):
    """
    Estimate cost for a completion

    Requires API key authentication

    - **model**: Model name
    - **input_tokens**: Estimated input tokens
    - **output_tokens**: Estimated output tokens

    Returns estimated cost in USD
    """
    try:
        cost = await estimate_cost(model, input_tokens, output_tokens)
        return {
            "model": model,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "estimated_cost_usd": cost,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Cost estimation failed: {str(e)}")


# ============================================================================
# AI AGENTS ENDPOINTS
# ============================================================================


@router.get("/v1/agents", tags=["Agents"])
async def get_agents(user: Dict[str, Any] = Depends(get_current_user_api_key)):
    """
    List all available AI agents

    Requires API key authentication

    Returns list of agents with specializations and tier restrictions

    **14 Specialized Agents:**
    - Kael: Code & Documentation (free)
    - Oracle: Analysis & Patterns (pro+)
    - Lumina: Research & Learning (free)
    - Shadow: Security & Privacy (pro+)
    - Agni: Creative & Content (free)
    - Vega: Data & Analytics (workflow+)
    - Echo: Communication & Translation (pro+)
    - Phoenix: Project Management (workflow+)
    - Manus: Ritual & Consciousness (enterprise)
    - Gemini: Social & Community (pro+)
    - Aether: Cloud & Infrastructure (workflow+)
    - Samsara: Lifecycle & Automation (workflow+)
    - Kavach: Protection & Monitoring (enterprise)
    - SanghaCore: Collective Intelligence (enterprise)
    """
    try:
        agents = await list_agents(user["tier"])
        return {"agents": agents}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list agents: {str(e)}")


@router.get("/v1/agents/{agent_id}", tags=["Agents"])
async def get_agent(
    agent_id: str,
    user: Dict[str, Any] = Depends(get_current_user_api_key)
):
    """
    Get details for a specific agent

    Requires API key authentication

    - **agent_id**: Agent identifier (e.g., 'kael', 'oracle', 'lumina')

    Returns agent details including specialization, tasks, and tier requirement
    """
    try:
        agent = await get_agent_info(agent_id, user["tier"])
        return agent
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get agent: {str(e)}")


@router.post("/v1/agents/{agent_id}/execute", response_model=AgentExecutionResponse, tags=["Agents"])
async def execute_agent_task(
    agent_id: str,
    request: AgentExecutionRequest,
    user: Dict[str, Any] = Depends(get_current_user_api_key)
):
    """
    Execute task with specialized AI agent

    Requires API key authentication

    Each agent has unique capabilities and system prompts optimized for their specialization

    **Request:**
    - **task**: Task type (e.g., 'document', 'analyze', 'research', 'secure', 'create')
    - **input**: Task input data (text, code, data, etc.)
    - **parameters**: Optional task-specific parameters
    - **optimize**: Routing strategy for underlying LLM (cost/speed/quality)

    **Response:**
    - **agent_id**: Agent that executed the task
    - **task**: Task type executed
    - **result**: Task execution result
    - **metadata**: Execution metadata (model used, tokens, cost, time)

    **Tier Restrictions:**
    - Some agents require Pro, Workflow, or Enterprise tier
    - Will return 403 if agent not available for your tier

    **Cost:**
    - Agent executions use underlying LLM calls
    - Cost varies by model selected (auto or manual)
    - All usage tracked and visible in dashboard
    """
    try:
        return await execute_agent(agent_id, request, user)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent execution failed: {str(e)}")


# ============================================================================
# STRIPE SUBSCRIPTION ENDPOINTS
# ============================================================================


@router.post("/billing/subscribe", tags=["Billing"])
async def subscribe(
    subscription: SubscriptionRequest,
    user: Dict[str, Any] = Depends(get_current_user_jwt)
):
    """
    Create new Stripe subscription

    Requires JWT authentication

    **Pricing Plans:**
    - Free: $0/mo (100 requests/day, 3 agents, basic models)
    - Pro: $29/mo (10K requests/day, all agents, all models)
    - Workflow: $79/mo (20K requests/day, workflow automation, Zapier)
    - Enterprise: $299/mo (unlimited requests, white-label, SLA, priority support)

    **Request:**
    - **tier**: 'pro', 'workflow', or 'enterprise'
    - **billing_cycle**: 'monthly' or 'annual' (10% discount)

    **Returns:**
    - Stripe subscription object with payment intent
    - User tier updated immediately upon successful payment
    """
    try:
        result = await create_subscription(
            user_id=user["id"],
            email=user["email"],
            tier=subscription.tier,
            billing_cycle=subscription.billing_cycle
        )
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Subscription failed: {str(e)}")


@router.post("/billing/cancel", tags=["Billing"])
async def cancel_plan(
    immediate: bool = False,
    user: Dict[str, Any] = Depends(get_current_user_jwt)
):
    """
    Cancel current subscription

    Requires JWT authentication

    - **immediate**: If False (default), cancels at end of billing period
    - **immediate**: If True, cancels immediately with prorated refund

    Returns cancellation confirmation
    """
    try:
        result = await cancel_subscription(user["id"], immediate=immediate)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Cancellation failed: {str(e)}")


@router.put("/billing/update", tags=["Billing"])
async def update_plan(
    new_tier: Optional[str] = None,
    new_billing_cycle: Optional[str] = None,
    user: Dict[str, Any] = Depends(get_current_user_jwt)
):
    """
    Update subscription tier or billing cycle

    Requires JWT authentication

    - **new_tier**: New tier ('pro', 'workflow', 'enterprise')
    - **new_billing_cycle**: New billing cycle ('monthly', 'annual')

    Prorated charges/credits applied automatically

    Returns updated subscription
    """
    try:
        result = await update_subscription(user["id"], new_tier, new_billing_cycle)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Update failed: {str(e)}")


@router.post("/billing/checkout", tags=["Billing"])
async def create_checkout(
    checkout: CheckoutSessionRequest,
    user: Dict[str, Any] = Depends(get_current_user_jwt)
):
    """
    Create Stripe Checkout session

    Requires JWT authentication

    Easier alternative to direct subscription creation

    - **tier**: Desired tier
    - **billing_cycle**: 'monthly' or 'annual'
    - **success_url**: URL to redirect after successful payment
    - **cancel_url**: URL to redirect if payment cancelled

    Returns Stripe Checkout session URL
    """
    try:
        session = await create_checkout_session(
            user_id=user["id"],
            email=user["email"],
            tier=checkout.tier,
            billing_cycle=checkout.billing_cycle,
            success_url=checkout.success_url,
            cancel_url=checkout.cancel_url
        )
        return {"checkout_url": session["url"], "session_id": session["id"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Checkout creation failed: {str(e)}")


@router.get("/billing/history", tags=["Billing"])
async def payment_history(
    limit: int = 10,
    user: Dict[str, Any] = Depends(get_current_user_jwt)
):
    """
    Get payment history

    Requires JWT authentication

    - **limit**: Maximum number of records to return (default: 10)

    Returns list of past payments with invoices
    """
    try:
        history = await get_payment_history(user["id"], limit=limit)
        return {"payments": history}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get payment history: {str(e)}")


@router.post("/billing/webhook", tags=["Billing"])
async def stripe_webhook(request: Request):
    """
    Stripe webhook endpoint

    Handles Stripe events:
    - checkout.session.completed
    - customer.subscription.created
    - customer.subscription.updated
    - customer.subscription.deleted
    - invoice.paid
    - invoice.payment_failed
    - customer.created
    - customer.updated
    - customer.deleted
    - payment_intent.succeeded

    Called by Stripe, not by clients

    Webhook secret configured in environment: STRIPE_WEBHOOK_SECRET
    """
    try:
        # Get raw body for signature verification
        body = await request.body()
        sig_header = request.headers.get("stripe-signature")

        # Verify webhook signature
        import stripe
        webhook_secret = os.getenv("STRIPE_WEBHOOK_SECRET")

        if not webhook_secret:
            raise HTTPException(status_code=500, detail="Webhook secret not configured")

        try:
            event = stripe.Webhook.construct_event(
                body, sig_header, webhook_secret
            )
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid payload")
        except stripe.error.SignatureVerificationError:
            raise HTTPException(status_code=400, detail="Invalid signature")

        # Handle event
        await handle_webhook_event(event)

        return {"status": "success"}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Webhook processing failed: {str(e)}")


# ============================================================================
# USAGE & ANALYTICS ENDPOINTS
# ============================================================================


@router.get("/usage/stats", tags=["Usage"])
async def get_usage_stats(user: Dict[str, Any] = Depends(get_current_user_api_key)):
    """
    Get usage statistics

    Requires API key authentication

    Returns:
    - Lifetime usage (total requests, tokens, cost)
    - Today's usage (requests, tokens, cost)
    - Rate limit status
    - Tier limits
    """
    try:
        stats = await get_user_stats(user["id"])

        # Add rate limit info
        from backend.saas_auth import TIER_LIMITS
        tier_limit = TIER_LIMITS.get(user["tier"], 100)

        return {
            "tier": user["tier"],
            "limits": {
                "requests_per_day": tier_limit,
                "agents_allowed": user["agents_allowed"],
                "prompts_allowed": user["prompts_allowed"],
            },
            "usage": stats,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get usage stats: {str(e)}")


# ============================================================================
# HEALTH & STATUS ENDPOINTS
# ============================================================================


@router.get("/health", tags=["System"])
async def health_check():
    """
    System health check

    Returns status of all SaaS components:
    - Database connection
    - Redis cache
    - LLM providers (Anthropic, OpenAI, xAI, Perplexity)
    - Stripe integration
    """
    health = {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "components": {}
    }

    # Check database
    try:
        await Database.connect()
        health["components"]["database"] = "healthy"
    except Exception as e:
        health["components"]["database"] = f"unhealthy: {str(e)}"
        health["status"] = "degraded"

    # Check Redis
    try:
        await Cache.connect()
        health["components"]["redis"] = "healthy"
    except Exception as e:
        health["components"]["redis"] = f"unhealthy: {str(e)}"
        health["status"] = "degraded"

    # Check LLM providers
    from backend.saas_router import (
        ANTHROPIC_API_KEY,
        OPENAI_API_KEY,
        XAI_API_KEY,
        PERPLEXITY_API_KEY
    )

    health["components"]["providers"] = {
        "anthropic": "configured" if ANTHROPIC_API_KEY else "not_configured",
        "openai": "configured" if OPENAI_API_KEY else "not_configured",
        "xai": "configured" if XAI_API_KEY else "not_configured",
        "perplexity": "configured" if PERPLEXITY_API_KEY else "not_configured",
    }

    # Check Stripe
    stripe_key = os.getenv("STRIPE_SECRET_KEY")
    health["components"]["stripe"] = "configured" if stripe_key else "not_configured"

    return health


@router.get("/", tags=["System"])
async def root():
    """
    API root endpoint

    Returns API information and links to documentation
    """
    return {
        "name": "Helix Collective SaaS API",
        "version": "1.0.0",
        "description": "Multi-LLM AI Platform with 14 Specialized Agents",
        "documentation": "/docs",
        "health": "/v1/saas/health",
        "endpoints": {
            "authentication": "/v1/saas/auth/*",
            "chat": "/v1/saas/v1/chat",
            "agents": "/v1/saas/v1/agents/*",
            "billing": "/v1/saas/billing/*",
            "usage": "/v1/saas/usage/*",
        },
        "pricing": "https://helixcollective.io/pricing",
        "support": "https://helixcollective.io/support",
    }
