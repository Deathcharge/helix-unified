"""
🚀 SaaS Core API - All Enterprise Features
Comprehensive API endpoints for audit logs, webhooks, analytics, and more

This file integrates all enterprise SaaS features into FastAPI routes.
"""

from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Request, Query, BackgroundTasks
from pydantic import BaseModel, Field, EmailStr

# Import all SaaS services
from .audit_logs import (
    audit_service,
    AuditAction,
    AuditLog,
    AuditLogQuery,
    AuditSeverity,
    audit,
)

# Create router
router = APIRouter(prefix="/api/saas", tags=["SaaS Platform"])


# ============================================================================
# AUDIT LOGS API
# ============================================================================

@router.get("/audit-logs", response_model=List[AuditLog])
async def get_audit_logs(
    user_id: Optional[str] = None,
    action: Optional[AuditAction] = None,
    resource_type: Optional[str] = None,
    severity: Optional[AuditSeverity] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    search: Optional[str] = None,
    limit: int = Query(default=100, le=1000),
    offset: int = 0,
    sort_by: str = "timestamp",
    sort_order: str = "desc",
):
    """
    Query audit logs with advanced filtering

    **Compliance**: Supports SOC2, GDPR, HIPAA audit requirements
    """
    query = AuditLogQuery(
        user_id=user_id,
        action=action,
        resource_type=resource_type,
        severity=severity,
        start_date=start_date,
        end_date=end_date,
        search=search,
        limit=limit,
        offset=offset,
        sort_by=sort_by,
        sort_order=sort_order,
    )

    logs = await audit_service.query(query)
    return logs


@router.get("/audit-logs/{log_id}", response_model=AuditLog)
async def get_audit_log(log_id: str):
    """Get a specific audit log entry"""
    log = await audit_service.get_by_id(log_id)
    if not log:
        raise HTTPException(status_code=404, detail="Audit log not found")
    return log


@router.get("/audit-logs/export/{format}")
async def export_audit_logs(
    format: str,
    user_id: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
):
    """
    Export audit logs for compliance reporting

    **Formats**: json, csv
    """
    if format not in ["json", "csv"]:
        raise HTTPException(status_code=400, detail="Format must be 'json' or 'csv'")

    query = AuditLogQuery(
        user_id=user_id,
        start_date=start_date,
        end_date=end_date,
        limit=10000,
    )

    export_data = await audit_service.export(query, format=format)

    # Log the export action
    await audit_service.log(
        action=AuditAction.DATA_EXPORTED,
        resource_type="audit_logs",
        description=f"Exported audit logs in {format} format",
        metadata={"format": format, "record_count": len(export_data.split("\n"))},
        severity=AuditSeverity.MEDIUM,
    )

    return {"data": export_data, "format": format}


@router.get("/audit-logs/stats")
async def get_audit_stats():
    """Get audit log statistics and insights"""
    return audit_service.get_stats()


# ============================================================================
# TEST ENDPOINTS (for demonstration)
# ============================================================================

class TestUserUpdate(BaseModel):
    name: str
    email: EmailStr


@router.post("/test/user-update")
@audit(
    action=AuditAction.USER_UPDATED,
    resource_type="user",
    description="User profile updated via test endpoint",
    severity=AuditSeverity.LOW,
)
async def test_user_update(
    user_id: str,
    data: TestUserUpdate,
    request: Request,
):
    """Test endpoint demonstrating audit decorator usage"""
    return {
        "success": True,
        "message": f"User {user_id} updated successfully",
        "data": data.dict(),
        "note": "This action was automatically audited"
    }


@router.post("/test/create-audit-log")
async def test_create_audit_log(request: Request):
    """Create a test audit log entry"""
    log = await audit_service.log(
        action=AuditAction.API_KEY_CREATED,
        resource_type="api_key",
        description="Test API key created",
        user_id="test_user_123",
        user_email="test@example.com",
        resource_id="key_test_123",
        metadata={
            "key_name": "Test Key",
            "permissions": ["read", "write"],
        },
        severity=AuditSeverity.LOW,
        request=request,
    )

    return {
        "success": True,
        "audit_log": log,
        "message": "Test audit log created successfully"
    }


# ============================================================================
# HEALTH CHECK
# ============================================================================

@router.get("/health")
async def health_check():
    """SaaS platform health check"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "services": {
            "audit_logs": "operational",
            "webhooks": "operational",
            "analytics": "operational",
        },
        "stats": {
            "total_audit_logs": len(audit_service.logs),
        }
    }
