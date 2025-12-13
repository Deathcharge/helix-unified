"""
📊 Metrics Collection Middleware
Automatically track usage, errors, and health metrics

VILLAIN METRICS: AUTO-TRACKING EVERYTHING 😈
"""

import time
import traceback
import uuid
from datetime import datetime
from typing import Callable

from fastapi import Request, Response
from sqlalchemy.orm import Session
from starlette.middleware.base import BaseHTTPMiddleware

from ..database import (ErrorLog, HealthCheck, SessionLocal, UsageLog,
                        UserActivation)


class MetricsMiddleware(BaseHTTPMiddleware):
    """
    Middleware to automatically collect metrics for all API requests

    Tracks:
    - Request/response metrics (timing, status codes)
    - Errors and exceptions
    - User activity for DAU/MAU calculation
    """

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Start timing
        start_time = time.time()

        # Track request
        user_id = None
        try:
            # Try to get user ID from request (you may need to adjust based on your auth)
            if hasattr(request.state, 'user_id'):
                user_id = request.state.user_id
            elif 'Authorization' in request.headers:
                # Extract from JWT or API key
                user_id = self._extract_user_id(request)
        except:
            pass

        # Process request
        response = None
        error_occurred = False

        try:
            response = await call_next(request)
        except Exception as e:
            error_occurred = True
            # Log the error
            self._log_error(
                user_id=user_id,
                error=e,
                endpoint=str(request.url.path),
                method=request.method,
                request_data={
                    "query_params": dict(request.query_params),
                    "path_params": dict(request.path_params) if hasattr(request, 'path_params') else {}
                }
            )
            raise
        finally:
            # Calculate response time
            response_time_ms = (time.time() - start_time) * 1000

            # Log usage
            if response:
                self._log_usage(
                    user_id=user_id,
                    endpoint=str(request.url.path),
                    method=request.method,
                    status_code=response.status_code,
                    response_time_ms=response_time_ms
                )

        return response

    def _extract_user_id(self, request: Request) -> str:
        """Extract user ID from request (implement based on your auth system)"""
        # This is a placeholder - implement based on your authentication
        # Example: decode JWT token or API key
        return None

    def _log_usage(
        self,
        user_id: str,
        endpoint: str,
        method: str,
        status_code: int,
        response_time_ms: float
    ):
        """Log API usage to database"""
        try:
            db = SessionLocal()
            try:
                usage_log = UsageLog(
                    user_id=user_id or "anonymous",
                    endpoint=endpoint,
                    method=method,
                    status_code=status_code,
                    response_time_ms=response_time_ms,
                    request_metadata={}
                )
                db.add(usage_log)
                db.commit()
            finally:
                db.close()
        except Exception as e:
            # Don't let logging errors break the request
            print(f"Failed to log usage: {e}")

    def _log_error(
        self,
        user_id: str,
        error: Exception,
        endpoint: str,
        method: str,
        request_data: dict
    ):
        """Log errors to database"""
        try:
            db = SessionLocal()
            try:
                error_log = ErrorLog(
                    user_id=user_id,
                    error_type=type(error).__name__,
                    error_message=str(error),
                    stack_trace=traceback.format_exc(),
                    endpoint=endpoint,
                    method=method,
                    request_data=request_data,
                    severity="error"
                )
                db.add(error_log)
                db.commit()
            finally:
                db.close()
        except Exception as e:
            print(f"Failed to log error: {e}")


# ============================================================================
# METRICS TRACKING HELPERS
# ============================================================================

def track_user_activation(
    db: Session,
    user_id: str,
    activation_type: str,
    metadata: dict = None
):
    """
    Track a user activation event

    Activation types:
    - profile_completed
    - first_api_call
    - first_agent_session
    - payment_added
    """
    try:
        # Check if already tracked
        existing = db.query(UserActivation).filter(
            UserActivation.user_id == user_id,
            UserActivation.activation_type == activation_type
        ).first()

        if not existing:
            activation = UserActivation(
                id=str(uuid.uuid4()),
                user_id=user_id,
                activation_type=activation_type,
                metadata=metadata or {}
            )
            db.add(activation)
            db.commit()
    except Exception as e:
        print(f"Failed to track activation: {e}")
        db.rollback()


def track_revenue_event(
    db: Session,
    user_id: str,
    team_id: str,
    event_type: str,
    amount: float,
    billing_period: str = "monthly",
    stripe_event_id: str = None,
    metadata: dict = None
):
    """
    Track a revenue event

    Event types:
    - subscription_started
    - subscription_renewed
    - subscription_upgraded
    - subscription_downgraded
    - subscription_canceled
    """
    from ..database import RevenueEvent

    try:
        event = RevenueEvent(
            id=str(uuid.uuid4()),
            user_id=user_id,
            team_id=team_id,
            event_type=event_type,
            amount=amount,
            billing_period=billing_period,
            stripe_event_id=stripe_event_id,
            metadata=metadata or {}
        )
        db.add(event)
        db.commit()
    except Exception as e:
        print(f"Failed to track revenue event: {e}")
        db.rollback()


def log_health_check(
    db: Session,
    service_name: str,
    status: str,
    response_time_ms: float = None,
    metadata: dict = None
):
    """
    Log a health check result

    Statuses: healthy, degraded, down
    """
    try:
        health_check = HealthCheck(
            service_name=service_name,
            status=status,
            response_time_ms=response_time_ms,
            metadata=metadata or {}
        )
        db.add(health_check)
        db.commit()
    except Exception as e:
        print(f"Failed to log health check: {e}")
        db.rollback()


def create_support_ticket(
    db: Session,
    user_id: str,
    subject: str,
    description: str,
    priority: str = "medium",
    category: str = "general"
) -> str:
    """
    Create a support ticket

    Returns: ticket_id
    """
    from ..database import SupportTicket

    ticket_id = str(uuid.uuid4())

    try:
        ticket = SupportTicket(
            id=ticket_id,
            user_id=user_id,
            subject=subject,
            description=description,
            priority=priority,
            category=category,
            status="open"
        )
        db.add(ticket)
        db.commit()
        return ticket_id
    except Exception as e:
        print(f"Failed to create support ticket: {e}")
        db.rollback()
        raise


def submit_nps_survey(
    db: Session,
    user_id: str,
    score: int,
    feedback: str = None,
    trigger: str = "dashboard"
):
    """
    Submit an NPS survey response

    Score: 0-10
    """
    from ..database import NPSSurvey

    try:
        if not 0 <= score <= 10:
            raise ValueError("NPS score must be between 0 and 10")

        survey = NPSSurvey(
            id=str(uuid.uuid4()),
            user_id=user_id,
            score=score,
            feedback=feedback,
            survey_trigger=trigger
        )
        db.add(survey)
        db.commit()
    except Exception as e:
        print(f"Failed to submit NPS survey: {e}")
        db.rollback()
        raise
