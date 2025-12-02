"""
Helix Collective SaaS - Multi-LLM Smart Router
==============================================

Intelligent routing to optimal LLM based on:
- Cost optimization
- Speed optimization
- Quality optimization
- User tier restrictions

Author: Claude (Manus Validator)
Date: 2025-11-30
"""

import anthropic
import openai
from typing import List, Dict, Any, Optional, Literal
from pydantic import BaseModel, Field
from fastapi import HTTPException
import time
import os
from backend.security_middleware import SafeErrorResponse

# Import existing orchestrator if available
try:
    HAS_ORCHESTRATOR = True
except ImportError:
    HAS_ORCHESTRATOR = False

# Import auth system
from backend.saas_auth import track_usage

# ============================================================================
# CONFIGURATION
# ============================================================================

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
XAI_API_KEY = os.getenv("XAI_API_KEY")  # Grok
PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")

# Initialize clients
anthropic_client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY) if ANTHROPIC_API_KEY else None
openai_client = openai.OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None

# ============================================================================
# PYDANTIC MODELS
# ============================================================================


class Message(BaseModel):
    """Chat message"""

    role: Literal["system", "user", "assistant"]
    content: str


class ChatRequest(BaseModel):
    """Chat completion request"""

    messages: List[Message]
    optimize: Literal["cost", "speed", "quality"] = "cost"
    model: Optional[str] = None  # Specific model or None for auto-route
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: int = Field(default=1000, ge=1, le=4096)
    stream: bool = False


class ChatResponse(BaseModel):
    """Chat completion response"""

    id: str
    model: str
    provider: str
    choices: List[Dict[str, Any]]
    usage: Dict[str, int]
    cost_usd: float
    response_time_ms: int
    optimize_mode: str


# ============================================================================
# MODEL ROUTING LOGIC
# ============================================================================


# Model costs (per 1M tokens) - Updated 2024
MODEL_PRICING = {
    # Anthropic
    "claude-3-opus-20240229": {"input": 15.00, "output": 75.00},
    "claude-3-sonnet-20240229": {"input": 3.00, "output": 15.00},
    "claude-3-haiku-20240307": {"input": 0.25, "output": 1.25},
    # OpenAI
    "gpt-4-turbo-2024-04-09": {"input": 10.00, "output": 30.00},
    "gpt-4-1106-preview": {"input": 10.00, "output": 30.00},
    "gpt-3.5-turbo-0125": {"input": 0.50, "output": 1.50},
    # xAI (Grok)
    "grok-beta": {"input": 2.00, "output": 10.00},
    # Perplexity
    "llama-3-sonar-large-32k-online": {"input": 1.00, "output": 5.00},
}

# Model performance scores (0-100, higher = better)
MODEL_SCORES = {
    # Cost score (lower = cheaper)
    "cost": {
        "llama-3-sonar-large-32k-online": 95,
        "claude-3-haiku-20240307": 90,
        "gpt-3.5-turbo-0125": 85,
        "grok-beta": 75,
        "claude-3-sonnet-20240229": 50,
        "gpt-4-1106-preview": 35,
        "gpt-4-turbo-2024-04-09": 35,
        "claude-3-opus-20240229": 20,
    },
    # Speed score (higher = faster)
    "speed": {
        "gpt-3.5-turbo-0125": 95,
        "claude-3-haiku-20240307": 90,
        "llama-3-sonar-large-32k-online": 85,
        "grok-beta": 80,
        "gpt-4-turbo-2024-04-09": 75,
        "claude-3-sonnet-20240229": 70,
        "gpt-4-1106-preview": 70,
        "claude-3-opus-20240229": 60,
    },
    # Quality score (higher = better)
    "quality": {
        "claude-3-opus-20240229": 95,
        "gpt-4-turbo-2024-04-09": 90,
        "gpt-4-1106-preview": 88,
        "claude-3-sonnet-20240229": 85,
        "grok-beta": 80,
        "llama-3-sonar-large-32k-online": 78,
        "claude-3-haiku-20240307": 75,
        "gpt-3.5-turbo-0125": 70,
    },
}

# Tier restrictions
TIER_MODELS = {
    "free": ["claude-3-haiku-20240307", "gpt-3.5-turbo-0125", "llama-3-sonar-large-32k-online"],
    "pro": [
        "claude-3-haiku-20240307",
        "claude-3-sonnet-20240229",
        "claude-3-opus-20240229",
        "gpt-3.5-turbo-0125",
        "gpt-4-1106-preview",
        "gpt-4-turbo-2024-04-09",
        "grok-beta",
        "llama-3-sonar-large-32k-online",
    ],
    "workflow": None,  # All models
    "enterprise": None,  # All models
}


def route_to_best_model(optimize: str, tier: str, specific_model: Optional[str] = None) -> tuple[str, str]:
    """
    Route to best model based on optimization mode and tier

    Args:
        optimize: 'cost', 'speed', or 'quality'
        tier: User tier ('free', 'pro', 'workflow', 'enterprise')
        specific_model: Specific model requested (or None for auto-route)

    Returns:
        (provider, model) tuple

    Raises:
        HTTPException if specific_model not allowed for tier
    """
    # If specific model requested, validate tier access
    if specific_model:
        allowed_models = TIER_MODELS.get(tier)
        if allowed_models is not None and specific_model not in allowed_models:
            raise HTTPException(
                status_code=403,
                detail=f"Model '{specific_model}' requires Pro tier or higher. Upgrade at https://helixcollective.io/pricing",
            )

        # Determine provider from model name
        if "claude" in specific_model:
            return "anthropic", specific_model
        elif "gpt" in specific_model:
            return "openai", specific_model
        elif "grok" in specific_model:
            return "xai", specific_model
        elif "llama" in specific_model:
            return "perplexity", specific_model
        else:
            raise HTTPException(status_code=400, detail=f"Unknown model: {specific_model}")

    # Auto-routing based on optimize mode
    scores = MODEL_SCORES.get(optimize, MODEL_SCORES["cost"])
    allowed_models = TIER_MODELS.get(tier)

    # Filter by tier
    if allowed_models is not None:
        available_scores = {k: v for k, v in scores.items() if k in allowed_models}
    else:
        available_scores = scores

    if not available_scores:
        raise HTTPException(status_code=500, detail="No models available for your tier")

    # Get best model by score
    best_model = max(available_scores, key=available_scores.get)

    # Determine provider
    if "claude" in best_model:
        provider = "anthropic"
    elif "gpt" in best_model:
        provider = "openai"
    elif "grok" in best_model:
        provider = "xai"
    elif "llama" in best_model:
        provider = "perplexity"
    else:
        provider = "unknown"

    return provider, best_model


# ============================================================================
# LLM PROVIDER CALLS
# ============================================================================


async def call_anthropic(model: str, messages: List[Message], temperature: float, max_tokens: int) -> Dict[str, Any]:
    """Call Anthropic Claude API"""
    if not anthropic_client:
        raise HTTPException(status_code=500, detail="Anthropic API key not configured")

    # Convert messages to Anthropic format
    system_message = None
    formatted_messages = []

    for msg in messages:
        if msg.role == "system":
            system_message = msg.content
        else:
            formatted_messages.append({"role": msg.role, "content": msg.content})

    # API call
    try:
        response = anthropic_client.messages.create(
            model=model, max_tokens=max_tokens, temperature=temperature, system=system_message, messages=formatted_messages
        )

        return {
            "content": response.content[0].text,
            "usage": {
                "input_tokens": response.usage.input_tokens,
                "output_tokens": response.usage.output_tokens,
                "total_tokens": response.usage.input_tokens + response.usage.output_tokens,
            },
            "finish_reason": response.stop_reason,
        }

    except Exception as e:
        status_code, error_response = SafeErrorResponse.sanitize_error(e, "anthropic_api_error")
        raise HTTPException(status_code=status_code, detail=error_response)


async def call_openai(model: str, messages: List[Message], temperature: float, max_tokens: int) -> Dict[str, Any]:
    """Call OpenAI GPT API"""
    if not openai_client:
        raise HTTPException(status_code=500, detail="OpenAI API key not configured")

    # Convert messages to OpenAI format
    formatted_messages = [{"role": msg.role, "content": msg.content} for msg in messages]

    # API call
    try:
        response = openai_client.chat.completions.create(
            model=model, messages=formatted_messages, temperature=temperature, max_tokens=max_tokens
        )

        return {
            "content": response.choices[0].message.content,
            "usage": {
                "input_tokens": response.usage.prompt_tokens,
                "output_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens,
            },
            "finish_reason": response.choices[0].finish_reason,
        }

    except Exception as e:
        status_code, error_response = SafeErrorResponse.sanitize_error(e, "openai_api_error")
        raise HTTPException(status_code=status_code, detail=error_response)


async def call_xai(model: str, messages: List[Message], temperature: float, max_tokens: int) -> Dict[str, Any]:
    """Call xAI Grok API (OpenAI-compatible)"""
    if not XAI_API_KEY:
        raise HTTPException(status_code=500, detail="xAI API key not configured")

    # xAI uses OpenAI-compatible API
    xai_client = openai.OpenAI(api_key=XAI_API_KEY, base_url="https://api.x.ai/v1")

    formatted_messages = [{"role": msg.role, "content": msg.content} for msg in messages]

    try:
        response = xai_client.chat.completions.create(
            model=model, messages=formatted_messages, temperature=temperature, max_tokens=max_tokens
        )

        return {
            "content": response.choices[0].message.content,
            "usage": {
                "input_tokens": response.usage.prompt_tokens,
                "output_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens,
            },
            "finish_reason": response.choices[0].finish_reason,
        }

    except Exception as e:
        status_code, error_response = SafeErrorResponse.sanitize_error(e, "xai_api_error")
        raise HTTPException(status_code=status_code, detail=error_response)


async def call_perplexity(model: str, messages: List[Message], temperature: float, max_tokens: int) -> Dict[str, Any]:
    """Call Perplexity API (OpenAI-compatible)"""
    if not PERPLEXITY_API_KEY:
        raise HTTPException(status_code=500, detail="Perplexity API key not configured")

    # Perplexity uses OpenAI-compatible API
    perplexity_client = openai.OpenAI(api_key=PERPLEXITY_API_KEY, base_url="https://api.perplexity.ai")

    formatted_messages = [{"role": msg.role, "content": msg.content} for msg in messages]

    try:
        response = perplexity_client.chat.completions.create(
            model=model, messages=formatted_messages, temperature=temperature, max_tokens=max_tokens
        )

        return {
            "content": response.choices[0].message.content,
            "usage": {
                "input_tokens": response.usage.prompt_tokens,
                "output_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens,
            },
            "finish_reason": response.choices[0].finish_reason,
        }

    except Exception as e:
        status_code, error_response = SafeErrorResponse.sanitize_error(e, "perplexity_api_error")
        raise HTTPException(status_code=status_code, detail=error_response)


# ============================================================================
# COST CALCULATION
# ============================================================================


def calculate_cost(model: str, usage: Dict[str, int]) -> float:
    """
    Calculate cost in USD for a completion

    Args:
        model: Model name
        usage: Usage dict with input_tokens and output_tokens

    Returns:
        Cost in USD
    """
    pricing = MODEL_PRICING.get(model)
    if not pricing:
        return 0.0

    input_cost = (usage["input_tokens"] / 1_000_000) * pricing["input"]
    output_cost = (usage["output_tokens"] / 1_000_000) * pricing["output"]

    return round(input_cost + output_cost, 6)


# ============================================================================
# MAIN CHAT COMPLETION ENDPOINT
# ============================================================================


async def chat_completion(request: ChatRequest, user: Dict[str, Any]) -> ChatResponse:
    """
    Handle chat completion request with smart routing

    Args:
        request: Chat request
        user: User data from auth middleware

    Returns:
        Chat response with model output and metadata
    """
    start_time = time.time()

    # Route to best model
    provider, model = route_to_best_model(optimize=request.optimize, tier=user["tier"], specific_model=request.model)

    # Call appropriate provider
    if provider == "anthropic":
        result = await call_anthropic(
            model=model, messages=request.messages, temperature=request.temperature, max_tokens=request.max_tokens
        )
    elif provider == "openai":
        result = await call_openai(
            model=model, messages=request.messages, temperature=request.temperature, max_tokens=request.max_tokens
        )
    elif provider == "xai":
        result = await call_xai(
            model=model, messages=request.messages, temperature=request.temperature, max_tokens=request.max_tokens
        )
    elif provider == "perplexity":
        result = await call_perplexity(
            model=model, messages=request.messages, temperature=request.temperature, max_tokens=request.max_tokens
        )
    else:
        raise HTTPException(status_code=500, detail=f"Unknown provider: {provider}")

    # Calculate metrics
    response_time_ms = int((time.time() - start_time) * 1000)
    cost_usd = calculate_cost(model, result["usage"])

    # Track usage (fire and forget)
    await track_usage(
        user_id=user["id"],
        endpoint="/v1/chat",
        method="POST",
        provider=provider,
        model=model,
        tokens_input=result["usage"]["input_tokens"],
        tokens_output=result["usage"]["output_tokens"],
        cost_usd=cost_usd,
        response_time_ms=response_time_ms,
        status_code=200,
    )

    # Build response
    response_id = f"chatcmpl-{int(time.time())}"

    return ChatResponse(
        id=response_id,
        model=model,
        provider=provider,
        choices=[
            {
                "index": 0,
                "message": {"role": "assistant", "content": result["content"]},
                "finish_reason": result["finish_reason"],
            }
        ],
        usage=result["usage"],
        cost_usd=cost_usd,
        response_time_ms=response_time_ms,
        optimize_mode=request.optimize,
    )


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================


async def get_available_models(tier: str) -> List[Dict[str, Any]]:
    """
    Get list of available models for a tier

    Args:
        tier: User tier

    Returns:
        List of model info dicts
    """
    allowed_models = TIER_MODELS.get(tier)

    # If None (enterprise/workflow), all models available
    if allowed_models is None:
        allowed_models = list(MODEL_PRICING.keys())

    models = []
    for model in allowed_models:
        pricing = MODEL_PRICING.get(model)
        models.append(
            {
                "id": model,
                "provider": (
                    "anthropic"
                    if "claude" in model
                    else "openai" if "gpt" in model else "xai" if "grok" in model else "perplexity"
                ),
                "pricing": pricing,
                "scores": {
                    "cost": MODEL_SCORES["cost"].get(model, 50),
                    "speed": MODEL_SCORES["speed"].get(model, 50),
                    "quality": MODEL_SCORES["quality"].get(model, 50),
                },
            }
        )

    return models


async def estimate_cost(model: str, input_tokens: int, output_tokens: int) -> float:
    """
    Estimate cost for a completion

    Args:
        model: Model name
        input_tokens: Estimated input tokens
        output_tokens: Estimated output tokens

    Returns:
        Estimated cost in USD
    """
    return calculate_cost(model, {"input_tokens": input_tokens, "output_tokens": output_tokens})
