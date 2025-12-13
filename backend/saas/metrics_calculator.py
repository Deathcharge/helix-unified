"""
📊 Metrics Calculation Utilities
Calculate DAU/MAU, MRR/ARR, Churn Rate, NPS, and other key metrics

VILLAIN METRICS: MEASURING WORLD DOMINATION 😈
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple

from sqlalchemy import and_, func, or_
from sqlalchemy.orm import Session

from ..database import (
    DailyMetrics, ErrorLog, HealthCheck, NPSSurvey, RevenueEvent,
    SupportTicket, User, UserActivation, UsageLog
)


class MetricsCalculator:
    """Calculate and aggregate key business metrics"""

    def __init__(self, db: Session):
        self.db = db

    # ========================================================================
    # USER METRICS
    # ========================================================================

    def calculate_signups(self, start_date: datetime, end_date: datetime) -> int:
        """Calculate new user signups in date range"""
        return self.db.query(func.count(User.id)).filter(
            User.created_at >= start_date,
            User.created_at <= end_date
        ).scalar() or 0

    def calculate_activations(self, start_date: datetime, end_date: datetime) -> int:
        """Calculate user activations (completed key action)"""
        # Count users who completed their first activation
        return self.db.query(func.count(func.distinct(UserActivation.user_id))).filter(
            UserActivation.completed_at >= start_date,
            UserActivation.completed_at <= end_date
        ).scalar() or 0

    def calculate_dau(self, date: datetime) -> int:
        """Calculate Daily Active Users"""
        start_of_day = date.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = start_of_day + timedelta(days=1)

        # Users who made API calls or logged in on this day
        active_users = self.db.query(func.count(func.distinct(UsageLog.user_id))).filter(
            UsageLog.timestamp >= start_of_day,
            UsageLog.timestamp < end_of_day
        ).scalar() or 0

        return active_users

    def calculate_mau(self, date: datetime) -> int:
        """Calculate Monthly Active Users"""
        start_of_month = date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        if date.month == 12:
            end_of_month = start_of_month.replace(year=date.year + 1, month=1)
        else:
            end_of_month = start_of_month.replace(month=date.month + 1)

        # Users who made API calls in this month
        active_users = self.db.query(func.count(func.distinct(UsageLog.user_id))).filter(
            UsageLog.timestamp >= start_of_month,
            UsageLog.timestamp < end_of_month
        ).scalar() or 0

        return active_users

    # ========================================================================
    # REVENUE METRICS
    # ========================================================================

    def calculate_mrr(self, date: datetime) -> float:
        """Calculate Monthly Recurring Revenue"""
        # Get all active subscriptions as of this date
        active_subscriptions = self.db.query(User).filter(
            User.subscription_status == "active",
            User.created_at <= date,
            or_(
                User.subscription_end_date.is_(None),
                User.subscription_end_date > date
            )
        ).all()

        # Calculate MRR based on subscription tier
        tier_pricing = {
            "free": 0,
            "pro": 29,
            "workflow": 79,
            "enterprise": 299
        }

        mrr = sum(tier_pricing.get(user.subscription_tier, 0) for user in active_subscriptions)

        # Add team subscriptions
        from ..database import Team
        team_subscriptions = self.db.query(Team).filter(
            Team.subscription_status == "active",
            Team.created_at <= date,
            or_(
                Team.subscription_end_date.is_(None),
                Team.subscription_end_date > date
            )
        ).all()

        team_tier_pricing = {
            "free": 0,
            "pro": 49,
            "workflow": 149,
            "enterprise": 499
        }

        mrr += sum(team_tier_pricing.get(team.subscription_tier, 0) for team in team_subscriptions)

        return float(mrr)

    def calculate_arr(self, mrr: float) -> float:
        """Calculate Annual Recurring Revenue from MRR"""
        return mrr * 12

    def calculate_churn_rate(self, start_date: datetime, end_date: datetime) -> float:
        """Calculate churn rate (percentage of customers who canceled)"""
        # Customers at start of period
        customers_start = self.db.query(func.count(User.id)).filter(
            User.subscription_status == "active",
            User.created_at < start_date
        ).scalar() or 0

        if customers_start == 0:
            return 0.0

        # Customers who churned during period
        churned = self.db.query(func.count(User.id)).filter(
            User.subscription_status.in_(["canceled", "inactive"]),
            User.subscription_end_date >= start_date,
            User.subscription_end_date < end_date
        ).scalar() or 0

        return (churned / customers_start) * 100

    # ========================================================================
    # NPS METRICS
    # ========================================================================

    def calculate_nps(self, start_date: datetime, end_date: datetime) -> Tuple[float, int]:
        """
        Calculate Net Promoter Score
        Returns: (nps_score, response_count)

        NPS = % Promoters (9-10) - % Detractors (0-6)
        """
        surveys = self.db.query(NPSSurvey).filter(
            NPSSurvey.created_at >= start_date,
            NPSSurvey.created_at <= end_date
        ).all()

        if not surveys:
            return (0.0, 0)

        total = len(surveys)
        promoters = len([s for s in surveys if s.score >= 9])
        detractors = len([s for s in surveys if s.score <= 6])

        nps = ((promoters - detractors) / total) * 100

        return (round(nps, 1), total)

    # ========================================================================
    # USAGE METRICS
    # ========================================================================

    def calculate_error_rate(self, start_date: datetime, end_date: datetime) -> Tuple[float, int]:
        """
        Calculate error rate
        Returns: (error_rate_percentage, total_errors)
        """
        total_requests = self.db.query(func.count(UsageLog.id)).filter(
            UsageLog.timestamp >= start_date,
            UsageLog.timestamp <= end_date
        ).scalar() or 0

        if total_requests == 0:
            return (0.0, 0)

        error_requests = self.db.query(func.count(UsageLog.id)).filter(
            UsageLog.timestamp >= start_date,
            UsageLog.timestamp <= end_date,
            UsageLog.status_code >= 400
        ).scalar() or 0

        # Also count logged errors
        logged_errors = self.db.query(func.count(ErrorLog.id)).filter(
            ErrorLog.occurred_at >= start_date,
            ErrorLog.occurred_at <= end_date
        ).scalar() or 0

        total_errors = error_requests + logged_errors
        error_rate = (error_requests / total_requests) * 100

        return (round(error_rate, 2), total_errors)

    def calculate_api_uptime(self, start_date: datetime, end_date: datetime) -> float:
        """Calculate API uptime percentage"""
        health_checks = self.db.query(HealthCheck).filter(
            HealthCheck.checked_at >= start_date,
            HealthCheck.checked_at <= end_date,
            HealthCheck.service_name == "api"
        ).all()

        if not health_checks:
            return 100.0

        healthy = len([h for h in health_checks if h.status == "healthy"])
        total = len(health_checks)

        return (healthy / total) * 100

    # ========================================================================
    # SUPPORT METRICS
    # ========================================================================

    def calculate_support_metrics(
        self, start_date: datetime, end_date: datetime
    ) -> Dict[str, any]:
        """Calculate support ticket metrics"""
        # New tickets
        new_tickets = self.db.query(func.count(SupportTicket.id)).filter(
            SupportTicket.created_at >= start_date,
            SupportTicket.created_at <= end_date
        ).scalar() or 0

        # Resolved tickets
        resolved_tickets = self.db.query(func.count(SupportTicket.id)).filter(
            SupportTicket.resolved_at >= start_date,
            SupportTicket.resolved_at <= end_date
        ).scalar() or 0

        # Average resolution time
        resolved = self.db.query(SupportTicket).filter(
            SupportTicket.resolved_at >= start_date,
            SupportTicket.resolved_at <= end_date,
            SupportTicket.resolved_at.isnot(None)
        ).all()

        avg_resolution_hours = 0
        if resolved:
            total_hours = sum([
                (ticket.resolved_at - ticket.created_at).total_seconds() / 3600
                for ticket in resolved
            ])
            avg_resolution_hours = total_hours / len(resolved)

        # Open tickets
        open_tickets = self.db.query(func.count(SupportTicket.id)).filter(
            SupportTicket.status.in_(["open", "in_progress"])
        ).scalar() or 0

        return {
            "new_tickets": new_tickets,
            "resolved_tickets": resolved_tickets,
            "open_tickets": open_tickets,
            "avg_resolution_time_hours": round(avg_resolution_hours, 2)
        }

    # ========================================================================
    # FEATURE USAGE
    # ========================================================================

    def get_top_features(
        self, start_date: datetime, end_date: datetime, limit: int = 10
    ) -> List[Dict[str, any]]:
        """Get top features/endpoints by usage"""
        feature_usage = self.db.query(
            UsageLog.endpoint,
            func.count(UsageLog.id).label("usage_count"),
            func.avg(UsageLog.response_time_ms).label("avg_response_time")
        ).filter(
            UsageLog.timestamp >= start_date,
            UsageLog.timestamp <= end_date
        ).group_by(
            UsageLog.endpoint
        ).order_by(
            func.count(UsageLog.id).desc()
        ).limit(limit).all()

        return [
            {
                "feature": endpoint or "unknown",
                "usage_count": count,
                "avg_response_time_ms": round(avg_time, 2) if avg_time else 0
            }
            for endpoint, count, avg_time in feature_usage
        ]

    # ========================================================================
    # DAILY METRICS AGGREGATION
    # ========================================================================

    def calculate_and_store_daily_metrics(self, date: datetime) -> DailyMetrics:
        """Calculate all metrics for a day and store in DailyMetrics table"""
        start_of_day = date.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = start_of_day + timedelta(days=1)

        # Check if already exists
        existing = self.db.query(DailyMetrics).filter(
            DailyMetrics.date == start_of_day
        ).first()

        # Calculate all metrics
        signups = self.calculate_signups(start_of_day, end_of_day)
        dau = self.calculate_dau(date)
        mau = self.calculate_mau(date)
        activations = self.calculate_activations(start_of_day, end_of_day)

        mrr = self.calculate_mrr(date)
        arr = self.calculate_arr(mrr)

        nps_score, nps_responses = self.calculate_nps(start_of_day, end_of_day)
        error_rate, error_count = self.calculate_error_rate(start_of_day, end_of_day)
        support_metrics = self.calculate_support_metrics(start_of_day, end_of_day)

        # API calls and agent sessions
        api_calls = self.db.query(func.count(UsageLog.id)).filter(
            UsageLog.timestamp >= start_of_day,
            UsageLog.timestamp < end_of_day
        ).scalar() or 0

        from ..database import AgentRental
        agent_sessions = self.db.query(func.count(AgentRental.id)).filter(
            AgentRental.started_at >= start_of_day,
            AgentRental.started_at < end_of_day
        ).scalar() or 0

        if existing:
            # Update existing
            existing.new_signups = signups
            existing.daily_active_users = dau
            existing.monthly_active_users = mau
            existing.activations_count = activations
            existing.mrr = mrr
            existing.arr = arr
            existing.api_calls_total = api_calls
            existing.agent_sessions_total = agent_sessions
            existing.error_count = error_count
            existing.error_rate = error_rate
            existing.new_tickets = support_metrics["new_tickets"]
            existing.resolved_tickets = support_metrics["resolved_tickets"]
            existing.avg_resolution_time_hours = support_metrics["avg_resolution_time_hours"]
            existing.nps_score = nps_score
            existing.nps_responses = nps_responses
            existing.calculated_at = datetime.utcnow()
            self.db.commit()
            self.db.refresh(existing)
            return existing
        else:
            # Create new
            metrics = DailyMetrics(
                date=start_of_day,
                new_signups=signups,
                daily_active_users=dau,
                monthly_active_users=mau,
                activations_count=activations,
                mrr=mrr,
                arr=arr,
                api_calls_total=api_calls,
                agent_sessions_total=agent_sessions,
                error_count=error_count,
                error_rate=error_rate,
                new_tickets=support_metrics["new_tickets"],
                resolved_tickets=support_metrics["resolved_tickets"],
                avg_resolution_time_hours=support_metrics["avg_resolution_time_hours"],
                nps_score=nps_score,
                nps_responses=nps_responses
            )
            self.db.add(metrics)
            self.db.commit()
            self.db.refresh(metrics)
            return metrics
