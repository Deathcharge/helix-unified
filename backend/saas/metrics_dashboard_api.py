"""
📊 Metrics Dashboard API
Comprehensive metrics endpoints for business intelligence dashboard

VILLAIN METRICS DASHBOARD: WORLD DOMINATION ANALYTICS 😈
"""

from datetime import datetime, timedelta
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ..database import (DailyMetrics, ErrorLog, HealthCheck, SupportTicket,
                        User, get_db)
from .metrics_calculator import MetricsCalculator

router = APIRouter()

# ============================================================================
# PYDANTIC MODELS
# ============================================================================

class MetricsSummaryResponse(BaseModel):
    """Summary of all key metrics"""
    # User metrics
    total_users: int
    new_signups: int
    active_users_daily: int
    active_users_monthly: int
    activation_rate: float

    # Revenue metrics
    mrr: float
    arr: float
    churn_rate: float

    # Usage metrics
    total_api_calls: int
    total_agent_sessions: int
    error_rate: float
    api_uptime: float

    # Support metrics
    open_tickets: int
    avg_resolution_time_hours: float

    # Satisfaction
    nps_score: float
    nps_responses: int

    # Top features
    top_features: List[dict]

    # Date range
    date_range: dict

class DailyMetricsResponse(BaseModel):
    """Daily metrics time series data"""
    dates: List[str]
    signups: List[int]
    dau: List[int]
    mau: List[int]
    mrr: List[float]
    error_rate: List[float]
    api_calls: List[int]

class ActivationFunnelResponse(BaseModel):
    """Activation funnel metrics"""
    total_signups: int
    completed_profile: int
    first_api_call: int
    first_agent_session: int
    activated_users: int
    activation_rate: float

class RevenueBreakdownResponse(BaseModel):
    """Revenue breakdown by tier"""
    free_users: int
    pro_users: int
    workflow_users: int
    enterprise_users: int
    total_mrr: float
    avg_revenue_per_user: float

# ============================================================================
# METRICS ENDPOINTS
# ============================================================================

@router.get("/metrics/summary", response_model=MetricsSummaryResponse)
async def get_metrics_summary(
    days: int = Query(30, description="Number of days to analyze"),
    db: Session = Depends(get_db)
):
    """
    📊 Get comprehensive metrics summary

    This endpoint provides a complete overview of all key business metrics:
    - User growth and engagement (signups, DAU/MAU)
    - Revenue metrics (MRR/ARR, churn)
    - Product usage (API calls, features)
    - Service health (uptime, errors)
    - Customer satisfaction (NPS)
    - Support metrics
    """
    calculator = MetricsCalculator(db)

    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)

    # User metrics
    total_users = db.query(User).count()
    new_signups = calculator.calculate_signups(start_date, end_date)
    dau = calculator.calculate_dau(end_date)
    mau = calculator.calculate_mau(end_date)
    activations = calculator.calculate_activations(start_date, end_date)
    activation_rate = (activations / new_signups * 100) if new_signups > 0 else 0

    # Revenue metrics
    mrr = calculator.calculate_mrr(end_date)
    arr = calculator.calculate_arr(mrr)
    churn_rate = calculator.calculate_churn_rate(start_date, end_date)

    # Usage metrics
    from ..database import AgentRental, UsageLog
    total_api_calls = db.query(UsageLog).filter(
        UsageLog.timestamp >= start_date,
        UsageLog.timestamp <= end_date
    ).count()

    total_agent_sessions = db.query(AgentRental).filter(
        AgentRental.started_at >= start_date,
        AgentRental.started_at <= end_date
    ).count()

    error_rate, _ = calculator.calculate_error_rate(start_date, end_date)
    api_uptime = calculator.calculate_api_uptime(start_date, end_date)

    # Support metrics
    support_metrics = calculator.calculate_support_metrics(start_date, end_date)

    # NPS
    nps_score, nps_responses = calculator.calculate_nps(start_date, end_date)

    # Top features
    top_features = calculator.get_top_features(start_date, end_date, limit=10)

    return MetricsSummaryResponse(
        total_users=total_users,
        new_signups=new_signups,
        active_users_daily=dau,
        active_users_monthly=mau,
        activation_rate=round(activation_rate, 2),
        mrr=mrr,
        arr=arr,
        churn_rate=round(churn_rate, 2),
        total_api_calls=total_api_calls,
        total_agent_sessions=total_agent_sessions,
        error_rate=error_rate,
        api_uptime=round(api_uptime, 2),
        open_tickets=support_metrics["open_tickets"],
        avg_resolution_time_hours=support_metrics["avg_resolution_time_hours"],
        nps_score=nps_score,
        nps_responses=nps_responses,
        top_features=top_features,
        date_range={
            "start": start_date.isoformat(),
            "end": end_date.isoformat(),
            "days": days
        }
    )

@router.get("/metrics/daily", response_model=DailyMetricsResponse)
async def get_daily_metrics(
    days: int = Query(30, description="Number of days of history"),
    db: Session = Depends(get_db)
):
    """
    📈 Get daily metrics time series

    Returns time series data for charting:
    - Daily signups
    - DAU/MAU trends
    - MRR growth
    - Error rates
    - API usage
    """
    end_date = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    start_date = end_date - timedelta(days=days)

    # Get or calculate daily metrics
    calculator = MetricsCalculator(db)

    dates = []
    signups = []
    dau_values = []
    mau_values = []
    mrr_values = []
    error_rates = []
    api_calls = []

    current_date = start_date
    while current_date <= end_date:
        # Try to get from DailyMetrics table first
        daily_metric = db.query(DailyMetrics).filter(
            DailyMetrics.date == current_date
        ).first()

        if not daily_metric:
            # Calculate and store if not exists
            daily_metric = calculator.calculate_and_store_daily_metrics(current_date)

        dates.append(current_date.strftime("%Y-%m-%d"))
        signups.append(daily_metric.new_signups)
        dau_values.append(daily_metric.daily_active_users)
        mau_values.append(daily_metric.monthly_active_users)
        mrr_values.append(daily_metric.mrr)
        error_rates.append(daily_metric.error_rate)
        api_calls.append(daily_metric.api_calls_total)

        current_date += timedelta(days=1)

    return DailyMetricsResponse(
        dates=dates,
        signups=signups,
        dau=dau_values,
        mau=mau_values,
        mrr=mrr_values,
        error_rate=error_rates,
        api_calls=api_calls
    )

@router.get("/metrics/activation-funnel", response_model=ActivationFunnelResponse)
async def get_activation_funnel(
    days: int = Query(30, description="Number of days to analyze"),
    db: Session = Depends(get_db)
):
    """
    🎯 Get user activation funnel

    Track user journey from signup to activation:
    1. Signed up
    2. Completed profile
    3. Made first API call
    4. Started first agent session
    5. Fully activated
    """
    from ..database import UserActivation

    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)

    # Users who signed up in period
    total_signups = db.query(User).filter(
        User.created_at >= start_date,
        User.created_at <= end_date
    ).count()

    if total_signups == 0:
        return ActivationFunnelResponse(
            total_signups=0,
            completed_profile=0,
            first_api_call=0,
            first_agent_session=0,
            activated_users=0,
            activation_rate=0
        )

    # Get user IDs who signed up
    signup_user_ids = [
        u.id for u in db.query(User.id).filter(
            User.created_at >= start_date,
            User.created_at <= end_date
        ).all()
    ]

    # Count activation steps
    completed_profile = db.query(UserActivation).filter(
        UserActivation.user_id.in_(signup_user_ids),
        UserActivation.activation_type == "profile_completed"
    ).count()

    first_api_call = db.query(UserActivation).filter(
        UserActivation.user_id.in_(signup_user_ids),
        UserActivation.activation_type == "first_api_call"
    ).count()

    first_agent_session = db.query(UserActivation).filter(
        UserActivation.user_id.in_(signup_user_ids),
        UserActivation.activation_type == "first_agent_session"
    ).count()

    # Activated = completed all steps
    activated_users = len(set(
        ua.user_id for ua in db.query(UserActivation).filter(
            UserActivation.user_id.in_(signup_user_ids),
            UserActivation.activation_type.in_([
                "profile_completed",
                "first_api_call",
                "first_agent_session"
            ])
        ).all()
    ))

    activation_rate = (activated_users / total_signups) * 100

    return ActivationFunnelResponse(
        total_signups=total_signups,
        completed_profile=completed_profile,
        first_api_call=first_api_call,
        first_agent_session=first_agent_session,
        activated_users=activated_users,
        activation_rate=round(activation_rate, 2)
    )

@router.get("/metrics/revenue-breakdown", response_model=RevenueBreakdownResponse)
async def get_revenue_breakdown(db: Session = Depends(get_db)):
    """
    💰 Get revenue breakdown by subscription tier
    """
    # Count users by tier
    free_users = db.query(User).filter(User.subscription_tier == "free").count()
    pro_users = db.query(User).filter(User.subscription_tier == "pro").count()
    workflow_users = db.query(User).filter(User.subscription_tier == "workflow").count()
    enterprise_users = db.query(User).filter(User.subscription_tier == "enterprise").count()

    # Calculate MRR
    calculator = MetricsCalculator(db)
    total_mrr = calculator.calculate_mrr(datetime.utcnow())

    total_paying = pro_users + workflow_users + enterprise_users
    arpu = (total_mrr / total_paying) if total_paying > 0 else 0

    return RevenueBreakdownResponse(
        free_users=free_users,
        pro_users=pro_users,
        workflow_users=workflow_users,
        enterprise_users=enterprise_users,
        total_mrr=total_mrr,
        avg_revenue_per_user=round(arpu, 2)
    )

@router.get("/metrics/support-overview")
async def get_support_overview(
    days: int = Query(30, description="Number of days to analyze"),
    db: Session = Depends(get_db)
):
    """
    🎫 Get support ticket overview
    """
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)

    # Ticket counts by status
    open_tickets = db.query(SupportTicket).filter(
        SupportTicket.status == "open"
    ).count()

    in_progress = db.query(SupportTicket).filter(
        SupportTicket.status == "in_progress"
    ).count()

    resolved = db.query(SupportTicket).filter(
        SupportTicket.status == "resolved",
        SupportTicket.resolved_at >= start_date
    ).count()

    # Tickets by priority
    urgent = db.query(SupportTicket).filter(
        SupportTicket.priority == "urgent",
        SupportTicket.status.in_(["open", "in_progress"])
    ).count()

    high = db.query(SupportTicket).filter(
        SupportTicket.priority == "high",
        SupportTicket.status.in_(["open", "in_progress"])
    ).count()

    # Tickets by category
    from sqlalchemy import func
    by_category = db.query(
        SupportTicket.category,
        func.count(SupportTicket.id)
    ).filter(
        SupportTicket.created_at >= start_date
    ).group_by(SupportTicket.category).all()

    return {
        "status": {
            "open": open_tickets,
            "in_progress": in_progress,
            "resolved": resolved
        },
        "priority": {
            "urgent": urgent,
            "high": high
        },
        "by_category": {
            category: count for category, count in by_category
        },
        "date_range": {
            "start": start_date.isoformat(),
            "end": end_date.isoformat()
        }
    }

@router.get("/metrics/error-overview")
async def get_error_overview(
    days: int = Query(7, description="Number of days to analyze"),
    db: Session = Depends(get_db)
):
    """
    🚨 Get error and health overview
    """
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)

    # Error counts
    from sqlalchemy import func
    total_errors = db.query(ErrorLog).filter(
        ErrorLog.occurred_at >= start_date
    ).count()

    critical_errors = db.query(ErrorLog).filter(
        ErrorLog.occurred_at >= start_date,
        ErrorLog.severity == "critical"
    ).count()

    # Errors by type
    by_type = db.query(
        ErrorLog.error_type,
        func.count(ErrorLog.id)
    ).filter(
        ErrorLog.occurred_at >= start_date
    ).group_by(ErrorLog.error_type).order_by(
        func.count(ErrorLog.id).desc()
    ).limit(10).all()

    # Errors by endpoint
    by_endpoint = db.query(
        ErrorLog.endpoint,
        func.count(ErrorLog.id)
    ).filter(
        ErrorLog.occurred_at >= start_date,
        ErrorLog.endpoint.isnot(None)
    ).group_by(ErrorLog.endpoint).order_by(
        func.count(ErrorLog.id).desc()
    ).limit(10).all()

    # API uptime
    calculator = MetricsCalculator(db)
    uptime = calculator.calculate_api_uptime(start_date, end_date)

    return {
        "total_errors": total_errors,
        "critical_errors": critical_errors,
        "api_uptime": round(uptime, 2),
        "by_type": [
            {"type": error_type, "count": count}
            for error_type, count in by_type
        ],
        "by_endpoint": [
            {"endpoint": endpoint, "count": count}
            for endpoint, count in by_endpoint
        ],
        "date_range": {
            "start": start_date.isoformat(),
            "end": end_date.isoformat()
        }
    }

@router.post("/metrics/calculate-daily")
async def trigger_daily_metrics_calculation(
    date: Optional[str] = Query(None, description="Date to calculate (YYYY-MM-DD), defaults to yesterday"),
    db: Session = Depends(get_db)
):
    """
    🔄 Manually trigger daily metrics calculation

    This should normally run via a cron job, but can be triggered manually
    """
    if date:
        target_date = datetime.fromisoformat(date)
    else:
        # Default to yesterday
        target_date = datetime.utcnow() - timedelta(days=1)

    calculator = MetricsCalculator(db)
    metrics = calculator.calculate_and_store_daily_metrics(target_date)

    return {
        "success": True,
        "date": target_date.strftime("%Y-%m-%d"),
        "metrics": {
            "signups": metrics.new_signups,
            "dau": metrics.daily_active_users,
            "mau": metrics.monthly_active_users,
            "mrr": metrics.mrr,
            "arr": metrics.arr
        }
    }
