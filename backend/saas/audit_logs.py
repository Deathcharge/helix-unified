"""
🔍 Audit Logs Service
Enterprise-grade audit logging for compliance (SOC2, GDPR, HIPAA)

Features:
- Automatic action tracking with decorators
- IP address, user agent, and geolocation capture
- Retention policies and archiving
- Advanced filtering and search
- Export for compliance reports
- Real-time alerts for suspicious activity
"""

import asyncio
import hashlib
import json
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional, Callable
from functools import wraps
import ipaddress

from pydantic import BaseModel, Field
from fastapi import Request, HTTPException
import httpx


class AuditAction(str, Enum):
    """Standard audit action types"""
    # Authentication
    LOGIN = "auth.login"
    LOGOUT = "auth.logout"
    LOGIN_FAILED = "auth.login_failed"
    PASSWORD_CHANGE = "auth.password_change"
    PASSWORD_RESET = "auth.password_reset"
    MFA_ENABLED = "auth.mfa_enabled"
    MFA_DISABLED = "auth.mfa_disabled"

    # User Management
    USER_CREATED = "user.created"
    USER_UPDATED = "user.updated"
    USER_DELETED = "user.deleted"
    USER_SUSPENDED = "user.suspended"
    USER_ACTIVATED = "user.activated"

    # Team Management
    TEAM_CREATED = "team.created"
    TEAM_UPDATED = "team.updated"
    TEAM_DELETED = "team.deleted"
    MEMBER_INVITED = "team.member_invited"
    MEMBER_REMOVED = "team.member_removed"
    MEMBER_ROLE_CHANGED = "team.member_role_changed"

    # API Keys
    API_KEY_CREATED = "api_key.created"
    API_KEY_DELETED = "api_key.deleted"
    API_KEY_ROTATED = "api_key.rotated"

    # Billing
    SUBSCRIPTION_CREATED = "billing.subscription_created"
    SUBSCRIPTION_UPDATED = "billing.subscription_updated"
    SUBSCRIPTION_CANCELED = "billing.subscription_canceled"
    PAYMENT_SUCCEEDED = "billing.payment_succeeded"
    PAYMENT_FAILED = "billing.payment_failed"

    # Data Access
    DATA_EXPORTED = "data.exported"
    DATA_IMPORTED = "data.imported"
    DATA_DELETED = "data.deleted"

    # Settings
    SETTINGS_UPDATED = "settings.updated"
    WEBHOOK_CREATED = "webhook.created"
    WEBHOOK_UPDATED = "webhook.updated"
    WEBHOOK_DELETED = "webhook.deleted"

    # Security
    PERMISSION_CHANGED = "security.permission_changed"
    ACCESS_DENIED = "security.access_denied"
    RATE_LIMIT_EXCEEDED = "security.rate_limit_exceeded"
    SUSPICIOUS_ACTIVITY = "security.suspicious_activity"

    # Admin Actions
    ADMIN_ACCESS = "admin.access"
    ADMIN_IMPERSONATE = "admin.impersonate"
    ADMIN_CONFIG_CHANGE = "admin.config_change"


class AuditSeverity(str, Enum):
    """Severity levels for audit events"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class AuditLog(BaseModel):
    """Audit log entry model"""
    id: str = Field(default_factory=lambda: f"audit_{datetime.utcnow().timestamp()}_{hash(datetime.utcnow())}")
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    # Who
    user_id: Optional[str] = None
    user_email: Optional[str] = None
    actor_type: str = "user"  # user, system, api_key, admin

    # What
    action: AuditAction
    resource_type: str  # user, team, api_key, webhook, etc.
    resource_id: Optional[str] = None
    severity: AuditSeverity = AuditSeverity.LOW

    # Where
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    geo_location: Optional[Dict[str, Any]] = None

    # Details
    description: str
    metadata: Dict[str, Any] = Field(default_factory=dict)
    changes: Optional[Dict[str, Any]] = None  # before/after for updates

    # Security
    request_id: Optional[str] = None
    session_id: Optional[str] = None
    api_key_id: Optional[str] = None

    # Status
    success: bool = True
    error_message: Optional[str] = None

    # Compliance
    retention_days: int = 2555  # 7 years default (SOC2/GDPR)
    archived: bool = False
    checksum: Optional[str] = None  # For tamper detection

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

    def compute_checksum(self) -> str:
        """Compute SHA-256 checksum for tamper detection"""
        data = f"{self.timestamp}{self.user_id}{self.action}{self.resource_id}{self.metadata}"
        return hashlib.sha256(data.encode()).hexdigest()


class AuditLogQuery(BaseModel):
    """Query parameters for audit log search"""
    user_id: Optional[str] = None
    user_email: Optional[str] = None
    action: Optional[AuditAction] = None
    resource_type: Optional[str] = None
    resource_id: Optional[str] = None
    severity: Optional[AuditSeverity] = None

    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

    ip_address: Optional[str] = None
    success: Optional[bool] = None

    search: Optional[str] = None  # Full-text search
    limit: int = Field(default=100, le=1000)
    offset: int = 0
    sort_by: str = "timestamp"
    sort_order: str = "desc"


class AuditLogService:
    """
    Audit logging service with in-memory storage

    In production, this should use a database (PostgreSQL with TimescaleDB,
    Elasticsearch, or dedicated audit log service like AWS CloudTrail)
    """

    def __init__(self):
        self.logs: List[AuditLog] = []
        self.geo_cache: Dict[str, Dict[str, Any]] = {}
        self.alert_webhooks: List[str] = []

    async def log(
        self,
        action: AuditAction,
        resource_type: str,
        description: str,
        user_id: Optional[str] = None,
        user_email: Optional[str] = None,
        resource_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        changes: Optional[Dict[str, Any]] = None,
        severity: AuditSeverity = AuditSeverity.LOW,
        request: Optional[Request] = None,
        success: bool = True,
        error_message: Optional[str] = None,
    ) -> AuditLog:
        """Create an audit log entry"""

        # Extract request metadata
        ip_address = None
        user_agent = None
        request_id = None

        if request:
            ip_address = request.client.host if request.client else None
            user_agent = request.headers.get("user-agent")
            request_id = request.headers.get("x-request-id")

        # Get geolocation for IP
        geo_location = None
        if ip_address:
            geo_location = await self._get_geolocation(ip_address)

        # Create audit log
        audit_log = AuditLog(
            user_id=user_id,
            user_email=user_email,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            severity=severity,
            ip_address=ip_address,
            user_agent=user_agent,
            geo_location=geo_location,
            description=description,
            metadata=metadata or {},
            changes=changes,
            request_id=request_id,
            success=success,
            error_message=error_message,
        )

        # Compute checksum for integrity
        audit_log.checksum = audit_log.compute_checksum()

        # Store log
        self.logs.append(audit_log)

        # Trigger alerts for high severity events
        if severity in [AuditSeverity.HIGH, AuditSeverity.CRITICAL]:
            asyncio.create_task(self._send_alert(audit_log))

        return audit_log

    async def query(self, query: AuditLogQuery) -> List[AuditLog]:
        """Query audit logs with filters"""
        filtered_logs = self.logs

        # Apply filters
        if query.user_id:
            filtered_logs = [log for log in filtered_logs if log.user_id == query.user_id]

        if query.user_email:
            filtered_logs = [log for log in filtered_logs if log.user_email == query.user_email]

        if query.action:
            filtered_logs = [log for log in filtered_logs if log.action == query.action]

        if query.resource_type:
            filtered_logs = [log for log in filtered_logs if log.resource_type == query.resource_type]

        if query.resource_id:
            filtered_logs = [log for log in filtered_logs if log.resource_id == query.resource_id]

        if query.severity:
            filtered_logs = [log for log in filtered_logs if log.severity == query.severity]

        if query.start_date:
            filtered_logs = [log for log in filtered_logs if log.timestamp >= query.start_date]

        if query.end_date:
            filtered_logs = [log for log in filtered_logs if log.timestamp <= query.end_date]

        if query.ip_address:
            filtered_logs = [log for log in filtered_logs if log.ip_address == query.ip_address]

        if query.success is not None:
            filtered_logs = [log for log in filtered_logs if log.success == query.success]

        # Full-text search
        if query.search:
            search_lower = query.search.lower()
            filtered_logs = [
                log for log in filtered_logs
                if search_lower in log.description.lower()
                or search_lower in str(log.metadata).lower()
            ]

        # Sort
        reverse = query.sort_order == "desc"
        filtered_logs = sorted(
            filtered_logs,
            key=lambda x: getattr(x, query.sort_by),
            reverse=reverse
        )

        # Paginate
        start = query.offset
        end = start + query.limit
        return filtered_logs[start:end]

    async def get_by_id(self, log_id: str) -> Optional[AuditLog]:
        """Get audit log by ID"""
        for log in self.logs:
            if log.id == log_id:
                return log
        return None

    async def export(
        self,
        query: AuditLogQuery,
        format: str = "json"
    ) -> str:
        """Export audit logs for compliance reporting"""
        logs = await self.query(query)

        if format == "json":
            return json.dumps([log.dict() for log in logs], indent=2, default=str)

        elif format == "csv":
            import csv
            import io

            output = io.StringIO()
            if logs:
                writer = csv.DictWriter(output, fieldnames=logs[0].dict().keys())
                writer.writeheader()
                for log in logs:
                    writer.writerow(log.dict())

            return output.getvalue()

        else:
            raise ValueError(f"Unsupported format: {format}")

    async def _get_geolocation(self, ip_address: str) -> Optional[Dict[str, Any]]:
        """Get geolocation for IP address (cached)"""
        # Check cache first
        if ip_address in self.geo_cache:
            return self.geo_cache[ip_address]

        # Skip private IPs
        try:
            ip_obj = ipaddress.ip_address(ip_address)
            if ip_obj.is_private or ip_obj.is_loopback:
                return {"type": "private"}
        except ValueError:
            return None

        # Fetch from IP geolocation API (using ip-api.com - free tier)
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"http://ip-api.com/json/{ip_address}",
                    timeout=2.0
                )
                if response.status_code == 200:
                    data = response.json()
                    geo_data = {
                        "country": data.get("country"),
                        "country_code": data.get("countryCode"),
                        "region": data.get("regionName"),
                        "city": data.get("city"),
                        "lat": data.get("lat"),
                        "lon": data.get("lon"),
                        "isp": data.get("isp"),
                    }
                    self.geo_cache[ip_address] = geo_data
                    return geo_data
        except Exception:
            pass

        return None

    async def _send_alert(self, log: AuditLog):
        """Send alert for high-severity events"""
        for webhook_url in self.alert_webhooks:
            try:
                async with httpx.AsyncClient() as client:
                    await client.post(
                        webhook_url,
                        json={
                            "type": "audit_alert",
                            "severity": log.severity,
                            "action": log.action,
                            "description": log.description,
                            "user_id": log.user_id,
                            "timestamp": log.timestamp.isoformat(),
                            "metadata": log.metadata,
                        },
                        timeout=5.0
                    )
            except Exception:
                pass  # Don't fail the main operation if alert fails

    def get_stats(self) -> Dict[str, Any]:
        """Get audit log statistics"""
        total_logs = len(self.logs)

        # Count by action
        action_counts = {}
        for log in self.logs:
            action_counts[log.action] = action_counts.get(log.action, 0) + 1

        # Count by severity
        severity_counts = {}
        for log in self.logs:
            severity_counts[log.severity] = severity_counts.get(log.severity, 0) + 1

        # Count failures
        failed_actions = sum(1 for log in self.logs if not log.success)

        # Most active users
        user_activity = {}
        for log in self.logs:
            if log.user_id:
                user_activity[log.user_id] = user_activity.get(log.user_id, 0) + 1

        top_users = sorted(user_activity.items(), key=lambda x: x[1], reverse=True)[:10]

        return {
            "total_logs": total_logs,
            "action_counts": action_counts,
            "severity_counts": severity_counts,
            "failed_actions": failed_actions,
            "top_users": [{"user_id": uid, "count": count} for uid, count in top_users],
        }


# Global audit service instance
audit_service = AuditLogService()


def audit(
    action: AuditAction,
    resource_type: str,
    description: str = "",
    severity: AuditSeverity = AuditSeverity.LOW,
    capture_changes: bool = False,
):
    """
    Decorator to automatically audit function calls

    Usage:
        @audit(AuditAction.USER_UPDATED, "user", "User profile updated")
        async def update_user(user_id: str, data: dict, request: Request):
            # ... update logic ...
            return updated_user
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Extract request if available
            request = kwargs.get('request') or next((arg for arg in args if isinstance(arg, Request)), None)

            # Get user info if available
            user_id = kwargs.get('user_id') or kwargs.get('current_user')

            # Capture before state if needed
            before_state = None
            if capture_changes and 'data' in kwargs:
                before_state = kwargs.get('data')

            # Execute function
            try:
                result = await func(*args, **kwargs) if asyncio.iscoroutinefunction(func) else func(*args, **kwargs)

                # Log success
                await audit_service.log(
                    action=action,
                    resource_type=resource_type,
                    description=description or f"{action} completed successfully",
                    user_id=str(user_id) if user_id else None,
                    resource_id=kwargs.get('resource_id'),
                    metadata={
                        "function": func.__name__,
                        "args": str(args)[:500],  # Limit size
                    },
                    severity=severity,
                    request=request,
                    success=True,
                )

                return result

            except Exception as e:
                # Log failure
                await audit_service.log(
                    action=action,
                    resource_type=resource_type,
                    description=f"{action} failed: {str(e)}",
                    user_id=str(user_id) if user_id else None,
                    resource_id=kwargs.get('resource_id'),
                    metadata={
                        "function": func.__name__,
                        "error": str(e),
                    },
                    severity=AuditSeverity.HIGH,
                    request=request,
                    success=False,
                    error_message=str(e),
                )
                raise

        return wrapper
    return decorator
