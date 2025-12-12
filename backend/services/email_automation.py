"""
📧 Email Automation Service
Automated transactional and marketing emails for SaaS platform

Supports:
- Welcome emails
- Password reset
- Usage alerts
- Team invitations
- Billing notifications
- Activity summaries
"""

import os
from datetime import datetime
from typing import Dict, List, Optional

import httpx
from jinja2 import Environment, FileSystemLoader, select_autoescape
from pydantic import BaseModel

# ============================================================================
# CONFIGURATION
# ============================================================================

# Email provider (supports SendGrid, Mailgun, Resend, SMTP)
EMAIL_PROVIDER = os.getenv("EMAIL_PROVIDER", "sendgrid")  # sendgrid, mailgun, resend, smtp
EMAIL_FROM = os.getenv("EMAIL_FROM", "noreply@helix.ai")
EMAIL_FROM_NAME = os.getenv("EMAIL_FROM_NAME", "Helix Collective")

# Provider-specific API keys
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
MAILGUN_API_KEY = os.getenv("MAILGUN_API_KEY")
MAILGUN_DOMAIN = os.getenv("MAILGUN_DOMAIN")
RESEND_API_KEY = os.getenv("RESEND_API_KEY")

# SMTP configuration
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

# Template directory
TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "templates", "emails")


# ============================================================================
# PYDANTIC MODELS
# ============================================================================

class EmailTemplate(BaseModel):
    """Email template data"""
    subject: str
    html: str
    text: Optional[str] = None


class EmailRecipient(BaseModel):
    """Email recipient"""
    email: str
    name: Optional[str] = None


# ============================================================================
# TEMPLATE RENDERING
# ============================================================================

# Initialize Jinja2 environment
try:
    jinja_env = Environment(
        loader=FileSystemLoader(TEMPLATE_DIR),
        autoescape=select_autoescape(['html', 'xml'])
    )
except:
    jinja_env = None
    print(f"⚠️ Email templates directory not found: {TEMPLATE_DIR}")


def render_template(template_name: str, context: Dict) -> EmailTemplate:
    """Render email template with context"""
    if not jinja_env:
        # Fallback to basic template
        return EmailTemplate(
            subject=context.get("subject", "Notification from Helix"),
            html=f"<html><body>{context.get('message', '')}</body></html>",
            text=context.get('message', '')
        )

    # Render HTML template
    html_template = jinja_env.get_template(f"{template_name}.html")
    html = html_template.render(**context)

    # Try to render text template
    try:
        text_template = jinja_env.get_template(f"{template_name}.txt")
        text = text_template.render(**context)
    except:
        text = None

    return EmailTemplate(
        subject=context.get("subject", "Notification from Helix"),
        html=html,
        text=text
    )


# ============================================================================
# EMAIL SENDING
# ============================================================================

async def send_email_sendgrid(
    to: EmailRecipient,
    subject: str,
    html: str,
    text: Optional[str] = None
) -> bool:
    """Send email via SendGrid"""
    if not SENDGRID_API_KEY:
        print("⚠️ SendGrid API key not configured")
        return False

    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.sendgrid.com/v3/mail/send",
            headers={
                "Authorization": f"Bearer {SENDGRID_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "personalizations": [{
                    "to": [{"email": to.email, "name": to.name}]
                }],
                "from": {"email": EMAIL_FROM, "name": EMAIL_FROM_NAME},
                "subject": subject,
                "content": [
                    {"type": "text/html", "value": html}
                ] + ([{"type": "text/plain", "value": text}] if text else [])
            }
        )

        return response.status_code == 202


async def send_email_mailgun(
    to: EmailRecipient,
    subject: str,
    html: str,
    text: Optional[str] = None
) -> bool:
    """Send email via Mailgun"""
    if not MAILGUN_API_KEY or not MAILGUN_DOMAIN:
        print("⚠️ Mailgun API key or domain not configured")
        return False

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages",
            auth=("api", MAILGUN_API_KEY),
            data={
                "from": f"{EMAIL_FROM_NAME} <{EMAIL_FROM}>",
                "to": f"{to.name or to.email} <{to.email}>",
                "subject": subject,
                "html": html,
                "text": text or ""
            }
        )

        return response.status_code == 200


async def send_email_resend(
    to: EmailRecipient,
    subject: str,
    html: str,
    text: Optional[str] = None
) -> bool:
    """Send email via Resend"""
    if not RESEND_API_KEY:
        print("⚠️ Resend API key not configured")
        return False

    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.resend.com/emails",
            headers={
                "Authorization": f"Bearer {RESEND_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "from": f"{EMAIL_FROM_NAME} <{EMAIL_FROM}>",
                "to": [to.email],
                "subject": subject,
                "html": html,
                "text": text
            }
        )

        return response.status_code in [200, 201]


async def send_email(
    to: EmailRecipient,
    subject: str,
    html: str,
    text: Optional[str] = None
) -> bool:
    """Send email using configured provider"""
    try:
        if EMAIL_PROVIDER == "sendgrid":
            return await send_email_sendgrid(to, subject, html, text)
        elif EMAIL_PROVIDER == "mailgun":
            return await send_email_mailgun(to, subject, html, text)
        elif EMAIL_PROVIDER == "resend":
            return await send_email_resend(to, subject, html, text)
        else:
            print(f"⚠️ Unsupported email provider: {EMAIL_PROVIDER}")
            return False
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
        return False


# ============================================================================
# AUTOMATED EMAIL FUNCTIONS
# ============================================================================

async def send_welcome_email(user_email: str, user_name: str, activation_link: Optional[str] = None):
    """Send welcome email to new user"""
    template = render_template("welcome", {
        "subject": f"Welcome to Helix, {user_name}! 🌀",
        "user_name": user_name,
        "activation_link": activation_link,
        "dashboard_url": "https://helix.ai/dashboard",
        "docs_url": "https://helix.ai/docs"
    })

    return await send_email(
        to=EmailRecipient(email=user_email, name=user_name),
        subject=template.subject,
        html=template.html,
        text=template.text
    )


async def send_password_reset_email(user_email: str, user_name: str, reset_token: str):
    """Send password reset email"""
    reset_link = f"https://helix.ai/reset-password?token={reset_token}"

    template = render_template("password_reset", {
        "subject": "Reset Your Helix Password",
        "user_name": user_name,
        "reset_link": reset_link,
        "expires_hours": 24
    })

    return await send_email(
        to=EmailRecipient(email=user_email, name=user_name),
        subject=template.subject,
        html=template.html,
        text=template.text
    )


async def send_usage_alert_email(user_email: str, user_name: str, usage_percent: float, tier: str):
    """Send usage limit alert"""
    template = render_template("usage_alert", {
        "subject": f"⚠️ You've used {usage_percent}% of your {tier} plan",
        "user_name": user_name,
        "usage_percent": usage_percent,
        "tier": tier,
        "upgrade_url": "https://helix.ai/upgrade"
    })

    return await send_email(
        to=EmailRecipient(email=user_email, name=user_name),
        subject=template.subject,
        html=template.html,
        text=template.text
    )


async def send_team_invitation_email(
    invitee_email: str,
    team_name: str,
    inviter_name: str,
    invitation_token: str,
    role: str
):
    """Send team invitation email"""
    invitation_link = f"https://helix.ai/accept-invitation?token={invitation_token}"

    template = render_template("team_invitation", {
        "subject": f"{inviter_name} invited you to join {team_name} on Helix",
        "team_name": team_name,
        "inviter_name": inviter_name,
        "role": role,
        "invitation_link": invitation_link,
        "expires_days": 7
    })

    return await send_email(
        to=EmailRecipient(email=invitee_email),
        subject=template.subject,
        html=template.html,
        text=template.text
    )


async def send_billing_notification_email(
    user_email: str,
    user_name: str,
    notification_type: str,  # payment_success, payment_failed, subscription_canceled
    amount: Optional[float] = None,
    next_billing_date: Optional[datetime] = None
):
    """Send billing notification"""
    subjects = {
        "payment_success": "Payment Successful - Helix",
        "payment_failed": "⚠️ Payment Failed - Action Required",
        "subscription_canceled": "Your Helix subscription has been canceled"
    }

    template = render_template("billing_notification", {
        "subject": subjects.get(notification_type, "Billing Notification"),
        "user_name": user_name,
        "notification_type": notification_type,
        "amount": amount,
        "next_billing_date": next_billing_date,
        "billing_url": "https://helix.ai/billing"
    })

    return await send_email(
        to=EmailRecipient(email=user_email, name=user_name),
        subject=template.subject,
        html=template.html,
        text=template.text
    )


async def send_weekly_summary_email(
    user_email: str,
    user_name: str,
    stats: Dict
):
    """Send weekly activity summary"""
    template = render_template("weekly_summary", {
        "subject": "Your Helix Weekly Summary 📊",
        "user_name": user_name,
        "api_calls": stats.get("api_calls", 0),
        "agent_sessions": stats.get("agent_sessions", 0),
        "tokens_used": stats.get("tokens_used", 0),
        "top_feature": stats.get("top_feature", "API"),
        "dashboard_url": "https://helix.ai/dashboard"
    })

    return await send_email(
        to=EmailRecipient(email=user_email, name=user_name),
        subject=template.subject,
        html=template.html,
        text=template.text
    )


async def send_feature_announcement_email(
    user_email: str,
    user_name: str,
    feature_name: str,
    feature_description: str,
    feature_url: str
):
    """Send new feature announcement"""
    template = render_template("feature_announcement", {
        "subject": f"✨ New Feature: {feature_name}",
        "user_name": user_name,
        "feature_name": feature_name,
        "feature_description": feature_description,
        "feature_url": feature_url
    })

    return await send_email(
        to=EmailRecipient(email=user_email, name=user_name),
        subject=template.subject,
        html=template.html,
        text=template.text
    )


# ============================================================================
# BATCH EMAIL SENDING
# ============================================================================

async def send_bulk_email(
    recipients: List[EmailRecipient],
    subject: str,
    html: str,
    text: Optional[str] = None,
    batch_size: int = 100
):
    """Send email to multiple recipients in batches"""
    results = []

    for i in range(0, len(recipients), batch_size):
        batch = recipients[i:i + batch_size]

        for recipient in batch:
            success = await send_email(recipient, subject, html, text)
            results.append({
                "email": recipient.email,
                "success": success
            })

    return results


# ============================================================================
# EMAIL HEALTH CHECK
# ============================================================================

def check_email_configuration() -> Dict:
    """Check if email is properly configured"""
    checks = {
        "provider": EMAIL_PROVIDER,
        "from_address": EMAIL_FROM,
        "configured": False,
        "provider_specific": {}
    }

    if EMAIL_PROVIDER == "sendgrid":
        checks["provider_specific"]["api_key_set"] = bool(SENDGRID_API_KEY)
        checks["configured"] = bool(SENDGRID_API_KEY)
    elif EMAIL_PROVIDER == "mailgun":
        checks["provider_specific"]["api_key_set"] = bool(MAILGUN_API_KEY)
        checks["provider_specific"]["domain_set"] = bool(MAILGUN_DOMAIN)
        checks["configured"] = bool(MAILGUN_API_KEY and MAILGUN_DOMAIN)
    elif EMAIL_PROVIDER == "resend":
        checks["provider_specific"]["api_key_set"] = bool(RESEND_API_KEY)
        checks["configured"] = bool(RESEND_API_KEY)
    elif EMAIL_PROVIDER == "smtp":
        checks["provider_specific"]["host"] = SMTP_HOST
        checks["provider_specific"]["port"] = SMTP_PORT
        checks["provider_specific"]["credentials_set"] = bool(SMTP_USER and SMTP_PASSWORD)
        checks["configured"] = bool(SMTP_USER and SMTP_PASSWORD)

    checks["templates_available"] = jinja_env is not None

    return checks
