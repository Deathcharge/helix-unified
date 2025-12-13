"""
📊 Analytics Export API
Export usage data, metrics, and reports in various formats

VILLAIN ANALYTICS: TRACK YOUR EVIL EMPIRE 😈
"""

import csv
import io
import json
from datetime import datetime, timedelta
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Response
from pydantic import BaseModel
from sqlalchemy import func
from sqlalchemy.orm import Session

from ..database import (AgentRental, Team, TeamMember, UsageLog, User,
                        WebOSSession, get_db)

router = APIRouter()

# ============================================================================
# PYDANTIC MODELS
# ============================================================================

class UsageStatsResponse(BaseModel):
    total_api_calls: int
    total_agent_sessions: int
    total_web_os_sessions: int
    total_tokens_used: int
    date_range: dict
    breakdown_by_endpoint: dict
    breakdown_by_agent: dict

class ExportRequest(BaseModel):
    start_date: Optional[str] = None  # ISO format
    end_date: Optional[str] = None  # ISO format
    format: str = "csv"  # csv, json
    include_metadata: bool = True

# ============================================================================
# ANALYTICS ENDPOINTS
# ============================================================================

@router.get("/analytics/usage", response_model=UsageStatsResponse)
async def get_usage_stats(
    start_date: Optional[str] = Query(None, description="Start date (ISO format)"),
    end_date: Optional[str] = Query(None, description="End date (ISO format)"),
    team_id: Optional[str] = Query(None, description="Filter by team"),
    db: Session = Depends(get_db),
    user_id: str = "test-user-id"  # TODO: Get from JWT auth
):
    """
    📈 Get usage statistics for a user or team
    """
    # Parse dates
    if start_date:
        start = datetime.fromisoformat(start_date.replace("Z", "+00:00"))
    else:
        start = datetime.utcnow() - timedelta(days=30)

    if end_date:
        end = datetime.fromisoformat(end_date.replace("Z", "+00:00"))
    else:
        end = datetime.utcnow()

    # Build base query
    usage_query = db.query(UsageLog).filter(
        UsageLog.timestamp >= start,
        UsageLog.timestamp <= end
    )

    if team_id:
        # Get all team members
        members = db.query(TeamMember).filter(TeamMember.team_id == team_id).all()
        member_ids = [m.user_id for m in members]
        usage_query = usage_query.filter(UsageLog.user_id.in_(member_ids))
    else:
        usage_query = usage_query.filter(UsageLog.user_id == user_id)

    # Get total API calls
    total_api_calls = usage_query.count()

    # Get breakdown by endpoint
    endpoint_breakdown = {}
    endpoint_stats = usage_query.with_entities(
        UsageLog.endpoint,
        func.count(UsageLog.id).label("count")
    ).group_by(UsageLog.endpoint).all()

    for endpoint, count in endpoint_stats:
        endpoint_breakdown[endpoint or "unknown"] = count

    # Get agent sessions
    agent_query = db.query(AgentRental).filter(
        AgentRental.started_at >= start,
        AgentRental.started_at <= end
    )

    if team_id:
        agent_query = agent_query.filter(AgentRental.user_id.in_(member_ids))
    else:
        agent_query = agent_query.filter(AgentRental.user_id == user_id)

    total_agent_sessions = agent_query.count()
    total_tokens_used = db.query(func.sum(AgentRental.tokens_used)).filter(
        AgentRental.started_at >= start,
        AgentRental.started_at <= end,
        AgentRental.user_id == user_id if not team_id else AgentRental.user_id.in_(member_ids)
    ).scalar() or 0

    # Get breakdown by agent
    agent_breakdown = {}
    agent_stats = agent_query.with_entities(
        AgentRental.agent_id,
        func.count(AgentRental.id).label("count")
    ).group_by(AgentRental.agent_id).all()

    for agent_id, count in agent_stats:
        agent_breakdown[agent_id] = count

    # Get Web OS sessions
    webos_query = db.query(WebOSSession).filter(
        WebOSSession.started_at >= start,
        WebOSSession.started_at <= end
    )

    if team_id:
        webos_query = webos_query.filter(WebOSSession.user_id.in_(member_ids))
    else:
        webos_query = webos_query.filter(WebOSSession.user_id == user_id)

    total_web_os_sessions = webos_query.count()

    return UsageStatsResponse(
        total_api_calls=total_api_calls,
        total_agent_sessions=total_agent_sessions,
        total_web_os_sessions=total_web_os_sessions,
        total_tokens_used=int(total_tokens_used),
        date_range={
            "start": start.isoformat(),
            "end": end.isoformat()
        },
        breakdown_by_endpoint=endpoint_breakdown,
        breakdown_by_agent=agent_breakdown
    )

@router.get("/analytics/export/usage")
async def export_usage_data(
    format: str = Query("csv", description="Export format: csv or json"),
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    team_id: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    user_id: str = "test-user-id"  # TODO: Get from JWT auth
):
    """
    📥 Export usage data in CSV or JSON format
    """
    # Parse dates
    if start_date:
        start = datetime.fromisoformat(start_date.replace("Z", "+00:00"))
    else:
        start = datetime.utcnow() - timedelta(days=30)

    if end_date:
        end = datetime.fromisoformat(end_date.replace("Z", "+00:00"))
    else:
        end = datetime.utcnow()

    # Build query
    query = db.query(UsageLog).filter(
        UsageLog.timestamp >= start,
        UsageLog.timestamp <= end
    )

    if team_id:
        members = db.query(TeamMember).filter(TeamMember.team_id == team_id).all()
        member_ids = [m.user_id for m in members]
        query = query.filter(UsageLog.user_id.in_(member_ids))
    else:
        query = query.filter(UsageLog.user_id == user_id)

    # Get data
    usage_logs = query.order_by(UsageLog.timestamp.desc()).limit(10000).all()

    if format == "csv":
        # Create CSV
        output = io.StringIO()
        writer = csv.writer(output)

        # Write header
        writer.writerow([
            "timestamp",
            "user_id",
            "endpoint",
            "method",
            "status_code",
            "response_time_ms"
        ])

        # Write rows
        for log in usage_logs:
            writer.writerow([
                log.timestamp.isoformat(),
                log.user_id,
                log.endpoint,
                log.method,
                log.status_code,
                log.response_time_ms
            ])

        csv_content = output.getvalue()
        output.close()

        return Response(
            content=csv_content,
            media_type="text/csv",
            headers={
                "Content-Disposition": f"attachment; filename=usage_export_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.csv"
            }
        )

    elif format == "json":
        # Create JSON
        data = []
        for log in usage_logs:
            data.append({
                "timestamp": log.timestamp.isoformat(),
                "user_id": log.user_id,
                "endpoint": log.endpoint,
                "method": log.method,
                "status_code": log.status_code,
                "response_time_ms": log.response_time_ms,
                "metadata": log.request_metadata
            })

        return Response(
            content=json.dumps(data, indent=2),
            media_type="application/json",
            headers={
                "Content-Disposition": f"attachment; filename=usage_export_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
            }
        )

    else:
        raise HTTPException(status_code=400, detail="Invalid format. Use 'csv' or 'json'")

@router.get("/analytics/export/agent-sessions")
async def export_agent_sessions(
    format: str = Query("csv", description="Export format: csv or json"),
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    team_id: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    user_id: str = "test-user-id"  # TODO: Get from JWT auth
):
    """
    📥 Export agent session data
    """
    # Parse dates
    if start_date:
        start = datetime.fromisoformat(start_date.replace("Z", "+00:00"))
    else:
        start = datetime.utcnow() - timedelta(days=30)

    if end_date:
        end = datetime.fromisoformat(end_date.replace("Z", "+00:00"))
    else:
        end = datetime.utcnow()

    # Build query
    query = db.query(AgentRental).filter(
        AgentRental.started_at >= start,
        AgentRental.started_at <= end
    )

    if team_id:
        members = db.query(TeamMember).filter(TeamMember.team_id == team_id).all()
        member_ids = [m.user_id for m in members]
        query = query.filter(AgentRental.user_id.in_(member_ids))
    else:
        query = query.filter(AgentRental.user_id == user_id)

    # Get data
    sessions = query.order_by(AgentRental.started_at.desc()).limit(10000).all()

    if format == "csv":
        # Create CSV
        output = io.StringIO()
        writer = csv.writer(output)

        # Write header
        writer.writerow([
            "session_id",
            "user_id",
            "agent_id",
            "started_at",
            "ended_at",
            "messages_count",
            "tokens_used",
            "cost_credits",
            "status"
        ])

        # Write rows
        for session in sessions:
            writer.writerow([
                session.id,
                session.user_id,
                session.agent_id,
                session.started_at.isoformat(),
                session.ended_at.isoformat() if session.ended_at else "",
                session.messages_count,
                session.tokens_used,
                session.cost_credits,
                session.status
            ])

        csv_content = output.getvalue()
        output.close()

        return Response(
            content=csv_content,
            media_type="text/csv",
            headers={
                "Content-Disposition": f"attachment; filename=agent_sessions_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.csv"
            }
        )

    elif format == "json":
        # Create JSON
        data = []
        for session in sessions:
            data.append({
                "session_id": session.id,
                "user_id": session.user_id,
                "agent_id": session.agent_id,
                "started_at": session.started_at.isoformat(),
                "ended_at": session.ended_at.isoformat() if session.ended_at else None,
                "messages_count": session.messages_count,
                "tokens_used": session.tokens_used,
                "cost_credits": session.cost_credits,
                "status": session.status
            })

        return Response(
            content=json.dumps(data, indent=2),
            media_type="application/json",
            headers={
                "Content-Disposition": f"attachment; filename=agent_sessions_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
            }
        )

    else:
        raise HTTPException(status_code=400, detail="Invalid format. Use 'csv' or 'json'")

@router.get("/analytics/billing-summary")
async def get_billing_summary(
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    team_id: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    user_id: str = "test-user-id"  # TODO: Get from JWT auth
):
    """
    💰 Get billing summary with cost breakdown
    """
    # Parse dates
    if start_date:
        start = datetime.fromisoformat(start_date.replace("Z", "+00:00"))
    else:
        start = datetime.utcnow() - timedelta(days=30)

    if end_date:
        end = datetime.fromisoformat(end_date.replace("Z", "+00:00"))
    else:
        end = datetime.utcnow()

    # Get user/team info
    if team_id:
        team = db.query(Team).filter(Team.id == team_id).first()
        if not team:
            raise HTTPException(status_code=404, detail="Team not found")

        subscription_tier = team.subscription_tier
        subscription_status = team.subscription_status

        # Get all team members for usage calculation
        members = db.query(TeamMember).filter(TeamMember.team_id == team_id).all()
        member_ids = [m.user_id for m in members]
    else:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        subscription_tier = user.subscription_tier
        subscription_status = user.subscription_status
        member_ids = [user_id]

    # Get agent rental costs
    agent_costs = db.query(func.sum(AgentRental.cost_credits)).filter(
        AgentRental.started_at >= start,
        AgentRental.started_at <= end,
        AgentRental.user_id.in_(member_ids)
    ).scalar() or 0

    # Get API call count
    api_calls = db.query(func.count(UsageLog.id)).filter(
        UsageLog.timestamp >= start,
        UsageLog.timestamp <= end,
        UsageLog.user_id.in_(member_ids)
    ).scalar() or 0

    # Calculate estimated costs (simplified)
    base_cost = {
        "free": 0,
        "pro": 29,
        "workflow": 79,
        "enterprise": 299
    }.get(subscription_tier, 0)

    # Agent usage cost (if over included amount)
    agent_overage_cost = max(0, (agent_costs - 1000) * 0.01)  # $0.01 per credit over 1000

    total_cost = base_cost + agent_overage_cost

    return {
        "subscription_tier": subscription_tier,
        "subscription_status": subscription_status,
        "billing_period": {
            "start": start.isoformat(),
            "end": end.isoformat()
        },
        "costs": {
            "base_subscription": base_cost,
            "agent_usage": agent_overage_cost,
            "total": total_cost
        },
        "usage": {
            "api_calls": api_calls,
            "agent_credits_used": int(agent_costs),
            "team_members": len(member_ids) if team_id else 1
        }
    }
