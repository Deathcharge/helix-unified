"""
📧 Email API Router
REST endpoints for email automation system
"""

import os
from datetime import datetime, timedelta
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel, EmailStr, validator
from sqlalchemy.orm import Session

from backend.core.rate_limit import get_rate_limit, limiter
from backend.database import User as DBUser
from backend.database import get_db
from backend.routes.auth import User, get_current_user
from backend.services.email_automation import (EMAIL_FROM, EMAIL_PROVIDER,
                                               EmailRecipient,
                                               check_email_health,
                                               send_billing_notification_email,
                                               send_bulk_email,
                                               send_feature_announcement_email,
                                               send_password_reset_email,
                                               send_team_invitation_email,
                                               send_usage_alert_email,
                                               send_weekly_summary_email,
                                               send_welcome_email)

router = APIRouter()

# ============================================================================
# MODELS
# ============================================================================

class SendWelcomeEmailRequest(BaseModel):
    user_email: EmailStr
    user_name: str
    activation_link: Optional[str] = None

class SendPasswordResetRequest(BaseModel):
    user_email: EmailStr
    user_name: str
    reset_token: str

class SendUsageAlertRequest(BaseModel):
    user_email: EmailStr
    user_name: str
    usage_metric: str
    current_usage: int
    limit: int
    percentage_used: int

class SendTeamInviteRequest(BaseModel):
    invitee_email: EmailStr
    team_name: str
    inviter_name: str
    invitation_token: str
    role: str = "member"

class SendBillingNotificationRequest(BaseModel):
    user_email: EmailStr
    user_name: str
    event_type: str  # payment_success, payment_failed, subscription_cancelled
    plan_name: str
    amount: Optional[float] = None
    next_billing_date: Optional[str] = None
    failure_reason: Optional[str] = None

class SendWeeklySummaryRequest(BaseModel):
    user_email: EmailStr
    user_name: str
    summary_data: dict

class SendFeatureAnnouncementRequest(BaseModel):
    user_email: EmailStr
    user_name: str
    feature_name: str
    feature_description: str
    feature_link: str

class SendBulkEmailRequest(BaseModel):
    recipients: List[EmailRecipient]
    subject: str
    html_content: str
    text_content: Optional[str] = None

    @validator('recipients')
    def validate_recipients(cls, v):
        """Limit bulk emails to prevent abuse"""
        if len(v) > 1000:
            raise ValueError('Cannot send to more than 1000 recipients at once')
        return v

class SendTestEmailRequest(BaseModel):
    recipient_email: EmailStr
    recipient_name: Optional[str] = "Test User"

class EmailResponse(BaseModel):
    success: bool
    message: str
    email_provider: Optional[str] = None
    sent_at: Optional[str] = None

class EmailHealthResponse(BaseModel):
    status: str
    email_provider: Optional[str] = None
    configured: bool
    from_email: Optional[str] = None
    checks: dict

# ============================================================================
# EMAIL SENDING ENDPOINTS
# ============================================================================

@router.post("/send-welcome", response_model=EmailResponse)
@limiter.limit(get_rate_limit("email_send"))
async def send_welcome(
    request: Request,
    req: SendWelcomeEmailRequest,
    current_user: User = Depends(get_current_user)
) -> EmailResponse:
    """
    📧 Send welcome email to new user

    Requires authentication. Sends branded welcome email with optional activation link.
    """
    try:
        result = await send_welcome_email(
            user_email=req.user_email,
            user_name=req.user_name,
            activation_link=req.activation_link
        )

        return EmailResponse(
            success=result,
            message="Welcome email sent successfully" if result else "Failed to send email",
            email_provider=EMAIL_PROVIDER,
            sent_at=datetime.utcnow().isoformat()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send welcome email: {str(e)}")

@router.post("/send-password-reset", response_model=EmailResponse)
@limiter.limit(get_rate_limit("email_send"))
async def send_password_reset(
    request: Request,
    req: SendPasswordResetRequest
) -> EmailResponse:
    """
    🔐 Send password reset email

    No authentication required. Sends password reset link with 24-hour expiry.
    """
    try:
        result = await send_password_reset_email(
            user_email=req.user_email,
            user_name=req.user_name,
            reset_token=req.reset_token
        )

        return EmailResponse(
            success=result,
            message="Password reset email sent successfully" if result else "Failed to send email",
            email_provider=EMAIL_PROVIDER,
            sent_at=datetime.utcnow().isoformat()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send password reset email: {str(e)}")

@router.post("/send-usage-alert", response_model=EmailResponse)
@limiter.limit(get_rate_limit("email_send"))
async def send_usage_alert(
    request: Request,
    req: SendUsageAlertRequest,
    current_user: User = Depends(get_current_user)
) -> EmailResponse:
    """
    ⚠️ Send usage alert email

    Requires authentication. Notifies users when approaching usage limits.
    """
    try:
        result = await send_usage_alert_email(
            user_email=req.user_email,
            user_name=req.user_name,
            usage_metric=req.usage_metric,
            current_usage=req.current_usage,
            limit=req.limit,
            percentage_used=req.percentage_used
        )

        return EmailResponse(
            success=result,
            message="Usage alert sent successfully" if result else "Failed to send email",
            email_provider=EMAIL_PROVIDER,
            sent_at=datetime.utcnow().isoformat()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send usage alert: {str(e)}")

@router.post("/send-team-invite", response_model=EmailResponse)
@limiter.limit(get_rate_limit("email_send"))
async def send_team_invite(
    request: Request,
    req: SendTeamInviteRequest,
    current_user: User = Depends(get_current_user)
) -> EmailResponse:
    """
    👥 Send team invitation email

    Requires authentication. Sends team invitation with 7-day expiry.
    """
    try:
        result = await send_team_invitation_email(
            invitee_email=req.invitee_email,
            team_name=req.team_name,
            inviter_name=req.inviter_name,
            invitation_token=req.invitation_token,
            role=req.role
        )

        return EmailResponse(
            success=result,
            message="Team invitation sent successfully" if result else "Failed to send email",
            email_provider=EMAIL_PROVIDER,
            sent_at=datetime.utcnow().isoformat()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send team invitation: {str(e)}")

@router.post("/send-billing-notification", response_model=EmailResponse)
@limiter.limit(get_rate_limit("email_send"))
async def send_billing_notification(
    request: Request,
    req: SendBillingNotificationRequest,
    current_user: User = Depends(get_current_user)
) -> EmailResponse:
    """
    💳 Send billing notification email

    Requires authentication. Sends payment success/failure notifications.
    """
    try:
        result = await send_billing_notification_email(
            user_email=req.user_email,
            user_name=req.user_name,
            event_type=req.event_type,
            plan_name=req.plan_name,
            amount=req.amount,
            next_billing_date=req.next_billing_date,
            failure_reason=req.failure_reason
        )

        return EmailResponse(
            success=result,
            message="Billing notification sent successfully" if result else "Failed to send email",
            email_provider=EMAIL_PROVIDER,
            sent_at=datetime.utcnow().isoformat()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send billing notification: {str(e)}")

@router.post("/send-weekly-summary", response_model=EmailResponse)
@limiter.limit(get_rate_limit("email_send"))
async def send_weekly_summary(
    request: Request,
    req: SendWeeklySummaryRequest,
    current_user: User = Depends(get_current_user)
) -> EmailResponse:
    """
    📊 Send weekly summary email

    Requires authentication. Sends weekly usage summary with stats.
    """
    try:
        result = await send_weekly_summary_email(
            user_email=req.user_email,
            user_name=req.user_name,
            summary_data=req.summary_data
        )

        return EmailResponse(
            success=result,
            message="Weekly summary sent successfully" if result else "Failed to send email",
            email_provider=EMAIL_PROVIDER,
            sent_at=datetime.utcnow().isoformat()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send weekly summary: {str(e)}")

@router.post("/send-feature-announcement", response_model=EmailResponse)
@limiter.limit(get_rate_limit("email_send"))
async def send_feature_announcement(
    request: Request,
    req: SendFeatureAnnouncementRequest,
    current_user: User = Depends(get_current_user)
) -> EmailResponse:
    """
    🚀 Send feature announcement email

    Requires authentication. Announces new features to users.
    """
    try:
        result = await send_feature_announcement_email(
            user_email=req.user_email,
            user_name=req.user_name,
            feature_name=req.feature_name,
            feature_description=req.feature_description,
            feature_link=req.feature_link
        )

        return EmailResponse(
            success=result,
            message="Feature announcement sent successfully" if result else "Failed to send email",
            email_provider=EMAIL_PROVIDER,
            sent_at=datetime.utcnow().isoformat()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send feature announcement: {str(e)}")

@router.post("/send-bulk", response_model=EmailResponse)
@limiter.limit("5/hour")  # Strict limit for bulk emails
async def send_bulk(
    request: Request,
    req: SendBulkEmailRequest,
    current_user: User = Depends(get_current_user)
) -> EmailResponse:
    """
    📮 Send bulk email to multiple recipients

    Requires authentication. Limited to 5 requests per hour and 1000 recipients per request.
    Use for newsletters, announcements, etc.
    """
    try:
        result = await send_bulk_email(
            recipients=req.recipients,
            subject=req.subject,
            html_content=req.html_content,
            text_content=req.text_content
        )

        return EmailResponse(
            success=result,
            message=f"Bulk email sent to {len(req.recipients)} recipients" if result else "Failed to send bulk email",
            email_provider=EMAIL_PROVIDER,
            sent_at=datetime.utcnow().isoformat()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send bulk email: {str(e)}")

# ============================================================================
# TESTING & HEALTH ENDPOINTS
# ============================================================================

@router.post("/test", response_model=EmailResponse)
@limiter.limit("10/hour")
async def send_test_email(
    request: Request,
    req: SendTestEmailRequest,
    current_user: User = Depends(get_current_user)
) -> EmailResponse:
    """
    🧪 Send test email

    Requires authentication. Sends a simple test email to verify configuration.
    """
    try:
        test_html = f"""
        <html>
            <body style="font-family: Arial, sans-serif; padding: 20px;">
                <h1 style="color: #00ffcc;">🌀 Helix Email Test</h1>
                <p>Hello {req.recipient_name}!</p>
                <p>This is a test email from your Helix email automation system.</p>
                <p><strong>Email Provider:</strong> {EMAIL_PROVIDER or 'Not configured'}</p>
                <p><strong>From Address:</strong> {EMAIL_FROM or 'Not configured'}</p>
                <p><strong>Sent At:</strong> {datetime.utcnow().isoformat()}</p>
                <hr>
                <p style="color: #666; font-size: 12px;">
                    If you received this email, your email configuration is working correctly! 🎉
                </p>
            </body>
        </html>
        """

        test_text = f"""
        Helix Email Test

        Hello {req.recipient_name}!

        This is a test email from your Helix email automation system.

        Email Provider: {EMAIL_PROVIDER or 'Not configured'}
        From Address: {EMAIL_FROM or 'Not configured'}
        Sent At: {datetime.utcnow().isoformat()}

        If you received this email, your email configuration is working correctly!
        """

        result = await send_bulk_email(
            recipients=[EmailRecipient(email=req.recipient_email, name=req.recipient_name)],
            subject="🌀 Helix Email Test",
            html_content=test_html,
            text_content=test_text
        )

        return EmailResponse(
            success=result,
            message="Test email sent successfully" if result else "Failed to send test email",
            email_provider=EMAIL_PROVIDER,
            sent_at=datetime.utcnow().isoformat()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send test email: {str(e)}")

@router.get("/health", response_model=EmailHealthResponse)
async def email_health() -> EmailHealthResponse:
    """
    🏥 Check email system health

    No authentication required. Returns email configuration status.
    """
    health = check_email_health()

    return EmailHealthResponse(
        status="healthy" if health["configured"] else "not_configured",
        email_provider=health.get("provider"),
        configured=health["configured"],
        from_email=health.get("from_email"),
        checks=health.get("checks", {})
    )

# ============================================================================
# ADMIN ENDPOINTS
# ============================================================================

class EmailStatsResponse(BaseModel):
    total_emails_today: int
    total_emails_this_week: int
    total_emails_this_month: int
    emails_by_type: dict
    success_rate: float

@router.get("/stats", response_model=EmailStatsResponse)
async def get_email_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> EmailStatsResponse:
    """
    📊 Get email sending statistics

    Requires authentication. Returns email usage stats for monitoring.
    Note: Requires email logging to be implemented in database.
    """
    # TODO: Implement email logging table to track sent emails
    # For now, return placeholder data
    return EmailStatsResponse(
        total_emails_today=0,
        total_emails_this_week=0,
        total_emails_this_month=0,
        emails_by_type={
            "welcome": 0,
            "password_reset": 0,
            "team_invite": 0,
            "billing": 0,
            "weekly_summary": 0,
            "feature_announcement": 0
        },
        success_rate=100.0
    )

# ============================================================================
# EXPORTS
# ============================================================================

__all__ = ["router"]
