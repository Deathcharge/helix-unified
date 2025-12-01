"""
Copyright (c) 2025 Andrew John Ward. All Rights Reserved.
PROPRIETARY AND CONFIDENTIAL - See LICENSE file for terms.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Dict, Any

from app.database import get_db
from app.models import User
from app.utils.dependencies import get_current_user
from app.config import settings

router = APIRouter()


class GenerateSpiralRequest(BaseModel):
    description: str


class GenerateSpiralResponse(BaseModel):
    spiral_config: Dict[str, Any]
    explanation: str


class SuggestActionsRequest(BaseModel):
    spiral_description: str
    existing_actions: List[Dict[str, Any]] = []


class SuggestActionsResponse(BaseModel):
    suggestions: List[Dict[str, Any]]


class DebugSpiralRequest(BaseModel):
    spiral_id: str
    error_message: str


class DebugSpiralResponse(BaseModel):
    diagnosis: str
    suggestions: List[str]


@router.post("/generate-spiral", response_model=GenerateSpiralResponse)
async def generate_spiral(
    request: GenerateSpiralRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Generate a spiral configuration from natural language description"""
    from anthropic import Anthropic
    
    client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)
    
    prompt = f"""You are an AI assistant that helps users create automation workflows (called "spirals").

User wants to create a spiral with this description:
"{request.description}"

Generate a JSON configuration for this spiral including:
1. A clear name for the spiral
2. A description
3. The trigger type (webhook, schedule, manual, or event)
4. Trigger configuration (if applicable)
5. A list of actions with their types and configurations

Available action types:
- http_request: Make HTTP requests (GET, POST, PUT, DELETE)
- email: Send emails
- transform: Transform data (extract, filter, map)
- ai_call: Call AI models for processing
- delay: Add delays between actions

Respond with a JSON object containing:
{{
  "name": "Spiral name",
  "description": "What this spiral does",
  "trigger_type": "manual|webhook|schedule|event",
  "trigger_config": {{}},
  "actions": [
    {{
      "order_index": 0,
      "action_type": "http_request",
      "config": {{
        "method": "GET",
        "url": "https://api.example.com/data",
        "headers": {{}},
        "body": null
      }}
    }}
  ]
}}

Also provide a brief explanation of how the spiral works."""

    try:
        message = client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=2048,
            messages=[{"role": "user", "content": prompt}]
        )
        
        response_text = message.content[0].text
        
        # Extract JSON from response
        import json
        import re
        
        # Try to find JSON in the response
        json_match = re.search(r'\{[\s\S]*\}', response_text)
        if json_match:
            spiral_config = json.loads(json_match.group())
        else:
            raise ValueError("Could not extract JSON from AI response")
        
        # Extract explanation (text before or after JSON)
        explanation = response_text.replace(json_match.group(), "").strip()
        if not explanation:
            explanation = "Spiral configuration generated successfully."
        
        return GenerateSpiralResponse(
            spiral_config=spiral_config,
            explanation=explanation
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate spiral: {str(e)}"
        )


@router.post("/suggest-actions", response_model=SuggestActionsResponse)
async def suggest_actions(
    request: SuggestActionsRequest,
    current_user: User = Depends(get_current_user)
):
    """Get AI-powered action suggestions for a spiral"""
    from anthropic import Anthropic
    
    client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)
    
    prompt = f"""You are an AI assistant helping users build automation workflows.

Spiral description: "{request.spiral_description}"

Existing actions: {request.existing_actions}

Suggest 3-5 additional actions that would enhance this spiral. For each suggestion, provide:
1. action_type (http_request, email, transform, ai_call, delay)
2. A brief description of what it does
3. Why it would be useful
4. Sample configuration

Respond with a JSON array of suggestions."""

    try:
        message = client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )
        
        response_text = message.content[0].text
        
        # Extract JSON array
        import json
        import re
        
        json_match = re.search(r'\[[\s\S]*\]', response_text)
        if json_match:
            suggestions = json.loads(json_match.group())
        else:
            suggestions = []
        
        return SuggestActionsResponse(suggestions=suggestions)
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate suggestions: {str(e)}"
        )


@router.post("/debug", response_model=DebugSpiralResponse)
async def debug_spiral(
    request: DebugSpiralRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get AI-powered debugging help for a failed spiral"""
    from anthropic import Anthropic
    from app.models import Spiral, ExecutionLog
    from uuid import UUID
    
    client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)
    
    # Get spiral details
    spiral = db.query(Spiral).filter(
        Spiral.id == UUID(request.spiral_id),
        Spiral.user_id == current_user.id
    ).first()
    
    if not spiral:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Spiral not found"
        )
    
    # Get recent execution logs
    recent_logs = db.query(ExecutionLog).filter(
        ExecutionLog.spiral_id == spiral.id,
        ExecutionLog.status == "failed"
    ).order_by(ExecutionLog.started_at.desc()).limit(3).all()
    
    prompt = f"""You are an AI debugging assistant for automation workflows.

Spiral name: {spiral.name}
Trigger type: {spiral.trigger_type}
Actions: {len(spiral.actions)}

Error message: "{request.error_message}"

Recent failed executions: {len(recent_logs)}

Analyze this error and provide:
1. A diagnosis of what went wrong
2. 3-5 specific suggestions to fix the issue
3. Best practices to prevent similar errors

Be specific and actionable."""

    try:
        message = client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )
        
        response_text = message.content[0].text
        
        # Parse response into diagnosis and suggestions
        lines = response_text.split('\n')
        diagnosis = lines[0] if lines else "Unable to diagnose"
        suggestions = [line.strip('- ').strip() for line in lines[1:] if line.strip().startswith('-')]
        
        if not suggestions:
            suggestions = ["Check your action configurations", "Verify API endpoints", "Review input data format"]
        
        return DebugSpiralResponse(
            diagnosis=diagnosis,
            suggestions=suggestions
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to debug spiral: {str(e)}"
        )