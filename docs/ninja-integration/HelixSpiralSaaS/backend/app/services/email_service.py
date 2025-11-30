"""
Copyright (c) 2025 Andrew John Ward. All Rights Reserved.
PROPRIETARY AND CONFIDENTIAL - See LICENSE file for terms.
"""

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content
from typing import List, Optional
import logging

from app.config import settings

logger = logging.getLogger(__name__)


class EmailService:
    """Email service using SendGrid"""
    
    def __init__(self):
        self.client = SendGridAPIClient(settings.SENDGRID_API_KEY)
        self.from_email = Email(settings.FROM_EMAIL, settings.FROM_NAME)
    
    def send_email(
        self,
        to_email: str,
        subject: str,
        html_content: str,
        text_content: Optional[str] = None
    ) -> bool:
        """Send an email"""
        try:
            message = Mail(
                from_email=self.from_email,
                to_emails=To(to_email),
                subject=subject,
                html_content=Content("text/html", html_content)
            )
            
            if text_content:
                message.add_content(Content("text/plain", text_content))
            
            response = self.client.send(message)
            
            if response.status_code in [200, 201, 202]:
                logger.info(f"Email sent successfully to {to_email}")
                return True
            else:
                logger.error(f"Failed to send email: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"Error sending email: {str(e)}")
            return False
    
    def send_welcome_email(self, to_email: str, full_name: str) -> bool:
        """Send welcome email to new user"""
        subject = f"Welcome to {settings.APP_NAME}! 🌀"
        
        html_content = f"""
        <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                    <h1 style="color: #6366f1;">Welcome to HelixSpiral! 🌀</h1>
                    
                    <p>Hi {full_name or 'there'},</p>
                    
                    <p>Thank you for joining HelixSpiral! We're excited to have you on board.</p>
                    
                    <h2 style="color: #6366f1;">Getting Started</h2>
                    
                    <p>Here's what you can do with your free account:</p>
                    <ul>
                        <li>✅ Create up to 5 spirals (automated workflows)</li>
                        <li>✅ 100 spiral executions per month</li>
                        <li>✅ Basic triggers (webhook, manual)</li>
                        <li>✅ Standard actions (HTTP, email, transform)</li>
                    </ul>
                    
                    <h2 style="color: #6366f1;">Quick Links</h2>
                    <ul>
                        <li><a href="{settings.FRONTEND_URL}/dashboard">Go to Dashboard</a></li>
                        <li><a href="{settings.FRONTEND_URL}/docs">Read Documentation</a></li>
                        <li><a href="{settings.FRONTEND_URL}/pricing">Upgrade Your Plan</a></li>
                    </ul>
                    
                    <p>Need help? Reply to this email or visit our <a href="{settings.FRONTEND_URL}/support">support page</a>.</p>
                    
                    <p>Happy automating! 🚀</p>
                    
                    <p style="color: #666; font-size: 14px; margin-top: 40px;">
                        The HelixSpiral Team<br>
                        <a href="{settings.FRONTEND_URL}">{settings.FRONTEND_URL}</a>
                    </p>
                </div>
            </body>
        </html>
        """
        
        return self.send_email(to_email, subject, html_content)
    
    def send_subscription_confirmation(
        self,
        to_email: str,
        full_name: str,
        plan_type: str,
        next_billing_date: str
    ) -> bool:
        """Send subscription confirmation email"""
        subject = f"Subscription Confirmed - {plan_type.title()} Plan"
        
        html_content = f"""
        <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                    <h1 style="color: #6366f1;">Subscription Confirmed! 🎉</h1>
                    
                    <p>Hi {full_name or 'there'},</p>
                    
                    <p>Your subscription to the <strong>{plan_type.title()} Plan</strong> has been confirmed!</p>
                    
                    <h2 style="color: #6366f1;">Plan Details</h2>
                    <ul>
                        <li><strong>Plan:</strong> {plan_type.title()}</li>
                        <li><strong>Next Billing Date:</strong> {next_billing_date}</li>
                    </ul>
                    
                    <h2 style="color: #6366f1;">What's Included</h2>
                    {'<ul><li>✅ 10,000 executions/month</li><li>✅ Unlimited spirals</li><li>✅ All triggers and actions</li><li>✅ Priority support</li></ul>' if plan_type == 'pro' else '<ul><li>✅ Unlimited executions</li><li>✅ Unlimited spirals</li><li>✅ All features</li><li>✅ Dedicated support</li><li>✅ SLA guarantee</li></ul>'}
                    
                    <p><a href="{settings.FRONTEND_URL}/dashboard" style="background-color: #6366f1; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; display: inline-block; margin-top: 20px;">Go to Dashboard</a></p>
                    
                    <p style="color: #666; font-size: 14px; margin-top: 40px;">
                        You can manage your subscription anytime from your <a href="{settings.FRONTEND_URL}/settings/billing">billing settings</a>.
                    </p>
                </div>
            </body>
        </html>
        """
        
        return self.send_email(to_email, subject, html_content)
    
    def send_execution_failure_alert(
        self,
        to_email: str,
        spiral_name: str,
        error_message: str,
        log_url: str
    ) -> bool:
        """Send execution failure alert"""
        subject = f"⚠️ Spiral Execution Failed: {spiral_name}"
        
        html_content = f"""
        <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                    <h1 style="color: #ef4444;">Spiral Execution Failed ⚠️</h1>
                    
                    <p>Your spiral <strong>{spiral_name}</strong> failed to execute.</p>
                    
                    <h2 style="color: #ef4444;">Error Details</h2>
                    <div style="background-color: #fee; padding: 15px; border-left: 4px solid #ef4444; margin: 20px 0;">
                        <code>{error_message}</code>
                    </div>
                    
                    <p><a href="{log_url}" style="background-color: #6366f1; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; display: inline-block; margin-top: 20px;">View Execution Log</a></p>
                    
                    <h2 style="color: #6366f1;">Troubleshooting Tips</h2>
                    <ul>
                        <li>Check your action configurations</li>
                        <li>Verify API endpoints are accessible</li>
                        <li>Review input data format</li>
                        <li>Check authentication credentials</li>
                    </ul>
                    
                    <p style="color: #666; font-size: 14px; margin-top: 40px;">
                        Need help? <a href="{settings.FRONTEND_URL}/support">Contact support</a>
                    </p>
                </div>
            </body>
        </html>
        """
        
        return self.send_email(to_email, subject, html_content)
    
    def send_usage_limit_warning(
        self,
        to_email: str,
        full_name: str,
        current_usage: int,
        limit: int,
        reset_date: str
    ) -> bool:
        """Send usage limit warning"""
        percentage = (current_usage / limit) * 100
        subject = f"⚠️ Usage Limit Warning - {percentage:.0f}% Used"
        
        html_content = f"""
        <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                    <h1 style="color: #f59e0b;">Usage Limit Warning ⚠️</h1>
                    
                    <p>Hi {full_name or 'there'},</p>
                    
                    <p>You've used <strong>{current_usage} out of {limit}</strong> spiral executions this month ({percentage:.0f}%).</p>
                    
                    <div style="background-color: #fef3c7; padding: 15px; border-left: 4px solid #f59e0b; margin: 20px 0;">
                        <p style="margin: 0;"><strong>Your usage will reset on {reset_date}</strong></p>
                    </div>
                    
                    <h2 style="color: #6366f1;">Need More Executions?</h2>
                    <p>Upgrade your plan to get more executions and unlock additional features:</p>
                    <ul>
                        <li><strong>Pro Plan:</strong> 10,000 executions/month</li>
                        <li><strong>Enterprise Plan:</strong> Unlimited executions</li>
                    </ul>
                    
                    <p><a href="{settings.FRONTEND_URL}/pricing" style="background-color: #6366f1; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; display: inline-block; margin-top: 20px;">Upgrade Now</a></p>
                </div>
            </body>
        </html>
        """
        
        return self.send_email(to_email, subject, html_content)


# Create singleton instance
email_service = EmailService()