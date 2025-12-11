"""
⚙️ Admin Dashboard API
=====================

Platform administration dashboard for site owners.

Features:
- User management and analytics
- Revenue tracking and financial reports
- System health monitoring
- Feature usage analytics
- Subscription management
- Admin action logs

Author: Claude (Helix Collective)
Date: 2025-12-07
"""

import os
import secrets
# Import admin bypass system
import sys
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from admin_bypass import (AdminUser, get_admin_user, is_admin_user,
                          log_admin_action, require_admin)

router = APIRouter()

# ============================================================================
# MODELS
# ============================================================================

class PlatformStats(BaseModel):
    """Platform-wide statistics"""
    total_users: int
    active_users_30d: int
    total_revenue: float
    mrr: float  # Monthly Recurring Revenue
    arr: float  # Annual Recurring Revenue
    subscriptions_active: int
    subscriptions_by_tier: Dict[str, int]
    api_calls_today: int
    api_calls_this_month: int
    storage_used_gb: float
    top_products: List[Dict[str, Any]]

class UserAnalytics(BaseModel):
    """User analytics data"""
    user_id: str
    email: str
    name: str
    subscription_tier: str
    created_at: datetime
    last_active: Optional[datetime]
    total_api_calls: int
    total_spent: float
    favorite_features: List[str]

class RevenueReport(BaseModel):
    """Revenue reporting"""
    period: str  # 'daily', 'weekly', 'monthly', 'yearly'
    total_revenue: float
    new_subscriptions: int
    churned_subscriptions: int
    upgrade_revenue: float
    breakdown_by_tier: Dict[str, float]
    top_products: List[Dict[str, Any]]

class SystemHealth(BaseModel):
    """System health metrics"""
    status: str  # 'healthy', 'degraded', 'down'
    uptime_percentage: float
    api_response_time_ms: float
    error_rate: float
    database_connections: int
    redis_connections: int
    disk_usage_percentage: float
    memory_usage_percentage: float
    cpu_usage_percentage: float

class AdminAction(BaseModel):
    """Admin action log entry"""
    id: str
    admin_email: str
    action: str
    details: Dict[str, Any]
    timestamp: datetime
    ip_address: Optional[str]

# ============================================================================
# MOCK DATA GENERATION (Replace with real database queries)
# ============================================================================

def get_mock_platform_stats() -> PlatformStats:
    """Generate mock platform statistics"""
    return PlatformStats(
        total_users=1247,
        active_users_30d=892,
        total_revenue=42580.50,
        mrr=12450.00,
        arr=149400.00,
        subscriptions_active=2847,
        subscriptions_by_tier={
            "free": 456,
            "hobby": 892,
            "starter": 634,
            "pro": 521,
            "enterprise": 344
        },
        api_calls_today=156789,
        api_calls_this_month=4234567,
        storage_used_gb=234.7,
        top_products=[
            {"name": "Discord Bot Marketplace", "revenue": 15420.00, "users": 456},
            {"name": "AI Agent Rental", "revenue": 12890.00, "users": 234},
            {"name": "Consciousness API", "revenue": 8970.00, "users": 189},
            {"name": "Web OS Marketplace", "revenue": 5300.00, "users": 123}
        ]
    )

def get_mock_user_analytics(limit: int = 50) -> List[UserAnalytics]:
    """Generate mock user analytics"""
    users = []
    tiers = ["free", "hobby", "starter", "pro", "enterprise"]
    for i in range(min(limit, 50)):
        users.append(UserAnalytics(
            user_id=f"user_{secrets.token_hex(4)}",
            email=f"user{i}@example.com",
            name=f"User {i}",
            subscription_tier=tiers[i % len(tiers)],
            created_at=datetime.utcnow() - timedelta(days=i * 10),
            last_active=datetime.utcnow() - timedelta(hours=i),
            total_api_calls=1000 + i * 100,
            total_spent=float(i * 29.99),
            favorite_features=["discord-bots", "consciousness-api"]
        ))
    return users

def get_mock_revenue_report(period: str) -> RevenueReport:
    """Generate mock revenue report"""
    return RevenueReport(
        period=period,
        total_revenue=12450.00,
        new_subscriptions=45,
        churned_subscriptions=12,
        upgrade_revenue=2340.00,
        breakdown_by_tier={
            "hobby": 2500.00,
            "starter": 3200.00,
            "pro": 4100.00,
            "enterprise": 2650.00
        },
        top_products=[
            {"name": "Discord Bots", "revenue": 4500.00},
            {"name": "AI Agents", "revenue": 3200.00},
            {"name": "Consciousness API", "revenue": 2800.00}
        ]
    )

def get_mock_system_health() -> SystemHealth:
    """Generate mock system health metrics"""
    return SystemHealth(
        status="healthy",
        uptime_percentage=99.94,
        api_response_time_ms=145.3,
        error_rate=0.12,
        database_connections=24,
        redis_connections=8,
        disk_usage_percentage=45.2,
        memory_usage_percentage=62.8,
        cpu_usage_percentage=38.5
    )

# ============================================================================
# ADMIN API ROUTES
# ============================================================================

@router.get("/stats")
async def get_platform_stats(
    user: AdminUser = Depends(get_admin_user)
) -> PlatformStats:
    """
    Get platform-wide statistics (Admin only)

    Requires: Admin privileges
    """
    if not user or not user.is_admin:
        raise HTTPException(status_code=403, detail="Admin privileges required")

    log_admin_action(user.dict(), "view_platform_stats")
    return get_mock_platform_stats()

@router.get("/users")
async def get_users(
    limit: int = Query(50, le=1000),
    offset: int = Query(0, ge=0),
    tier: Optional[str] = None,
    user: AdminUser = Depends(get_admin_user)
) -> List[UserAnalytics]:
    """
    Get user analytics (Admin only)

    Requires: Admin privileges
    """
    if not user or not user.is_admin:
        raise HTTPException(status_code=403, detail="Admin privileges required")

    log_admin_action(user.dict(), "view_user_analytics", {"limit": limit, "tier": tier})

    # TODO: Implement real database query with filtering
    users = get_mock_user_analytics(limit)

    if tier:
        users = [u for u in users if u.subscription_tier == tier]

    return users[offset:offset + limit]

@router.get("/revenue")
async def get_revenue_report(
    period: str = Query("monthly", regex="^(daily|weekly|monthly|yearly)$"),
    user: AdminUser = Depends(get_admin_user)
) -> RevenueReport:
    """
    Get revenue report (Admin only)

    Requires: Admin privileges
    """
    if not user or not user.is_admin:
        raise HTTPException(status_code=403, detail="Admin privileges required")

    log_admin_action(user.dict(), "view_revenue_report", {"period": period})
    return get_mock_revenue_report(period)

@router.get("/health")
async def get_system_health(
    user: AdminUser = Depends(get_admin_user)
) -> SystemHealth:
    """
    Get system health metrics (Admin only)

    Requires: Admin privileges
    """
    if not user or not user.is_admin:
        raise HTTPException(status_code=403, detail="Admin privileges required")

    log_admin_action(user.dict(), "view_system_health")
    return get_mock_system_health()

@router.post("/users/{user_id}/tier")
async def update_user_tier(
    user_id: str,
    new_tier: str,
    user: AdminUser = Depends(get_admin_user)
):
    """
    Update user's subscription tier (Admin only)

    Requires: Admin privileges
    """
    if not user or not user.is_admin:
        raise HTTPException(status_code=403, detail="Admin privileges required")

    log_admin_action(
        user.dict(),
        "update_user_tier",
        {"user_id": user_id, "new_tier": new_tier}
    )

    # TODO: Implement actual database update
    return {
        "success": True,
        "user_id": user_id,
        "new_tier": new_tier,
        "message": f"User tier updated to {new_tier}"
    }

@router.delete("/users/{user_id}")
async def delete_user(
    user_id: str,
    user: AdminUser = Depends(get_admin_user)
):
    """
    Delete user account (Admin only)

    Requires: Admin privileges
    """
    if not user or not user.is_admin:
        raise HTTPException(status_code=403, detail="Admin privileges required")

    log_admin_action(user.dict(), "delete_user", {"user_id": user_id})

    # TODO: Implement actual user deletion
    return {
        "success": True,
        "user_id": user_id,
        "message": "User account deleted"
    }

@router.get("/logs")
async def get_admin_logs(
    limit: int = Query(100, le=1000),
    user: AdminUser = Depends(get_admin_user)
) -> List[AdminAction]:
    """
    Get admin action logs (Admin only)

    Requires: Admin privileges
    """
    if not user or not user.is_admin:
        raise HTTPException(status_code=403, detail="Admin privileges required")

    # TODO: Implement actual log retrieval
    logs = [
        AdminAction(
            id=secrets.token_hex(8),
            admin_email=user.email,
            action="view_platform_stats",
            details={},
            timestamp=datetime.utcnow() - timedelta(minutes=i),
            ip_address="192.168.1.1"
        )
        for i in range(min(limit, 10))
    ]

    return logs

# ============================================================================
# ADMIN DASHBOARD HTML
# ============================================================================

@router.get("/", response_class=HTMLResponse)
async def admin_dashboard_home():
    """Admin dashboard web interface"""
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Helix Admin Dashboard</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }

            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                background: #f5f7fa;
                color: #333;
            }

            .header {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 1.5rem 2rem;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }

            .header h1 {
                font-size: 2rem;
                margin-bottom: 0.5rem;
            }

            .header p {
                opacity: 0.9;
                font-size: 1rem;
            }

            .container {
                max-width: 1600px;
                margin: 0 auto;
                padding: 2rem;
            }

            .stats-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 1.5rem;
                margin-bottom: 2rem;
            }

            .stat-card {
                background: white;
                padding: 1.5rem;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                border-left: 4px solid #667eea;
            }

            .stat-card .icon {
                font-size: 2rem;
                margin-bottom: 0.5rem;
            }

            .stat-card .label {
                color: #666;
                font-size: 0.9rem;
                margin-bottom: 0.3rem;
            }

            .stat-card .value {
                font-size: 2rem;
                font-weight: bold;
                color: #333;
            }

            .stat-card .change {
                font-size: 0.85rem;
                margin-top: 0.5rem;
            }

            .change.positive {
                color: #28a745;
            }

            .change.negative {
                color: #dc3545;
            }

            .dashboard-grid {
                display: grid;
                grid-template-columns: 2fr 1fr;
                gap: 1.5rem;
                margin-bottom: 2rem;
            }

            .panel {
                background: white;
                padding: 1.5rem;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }

            .panel h2 {
                margin-bottom: 1rem;
                color: #333;
                font-size: 1.3rem;
            }

            .table {
                width: 100%;
                border-collapse: collapse;
            }

            .table th {
                background: #f8f9fa;
                padding: 0.75rem;
                text-align: left;
                font-weight: 600;
                color: #666;
                font-size: 0.85rem;
                text-transform: uppercase;
            }

            .table td {
                padding: 0.75rem;
                border-bottom: 1px solid #e9ecef;
            }

            .table tr:hover {
                background: #f8f9fa;
            }

            .badge {
                padding: 0.25rem 0.75rem;
                border-radius: 12px;
                font-size: 0.75rem;
                font-weight: 600;
                text-transform: uppercase;
            }

            .badge.enterprise {
                background: #764ba2;
                color: white;
            }

            .badge.pro {
                background: #667eea;
                color: white;
            }

            .badge.starter {
                background: #ffc107;
                color: #333;
            }

            .badge.hobby {
                background: #28a745;
                color: white;
            }

            .badge.free {
                background: #6c757d;
                color: white;
            }

            .action-btn {
                background: #667eea;
                color: white;
                border: none;
                padding: 0.5rem 1rem;
                border-radius: 4px;
                cursor: pointer;
                font-size: 0.9rem;
                transition: opacity 0.3s;
            }

            .action-btn:hover {
                opacity: 0.8;
            }

            .action-btn.danger {
                background: #dc3545;
            }

            .chart-placeholder {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                height: 200px;
                border-radius: 8px;
                display: flex;
                align-items: center;
                justify-content: center;
                color: white;
                font-size: 1.5rem;
            }

            @media (max-width: 768px) {
                .dashboard-grid {
                    grid-template-columns: 1fr;
                }
            }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>⚙️ Helix Admin Dashboard</h1>
            <p>Platform management and analytics</p>
        </div>

        <div class="container">
            <!-- Key Metrics -->
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="icon">👥</div>
                    <div class="label">Total Users</div>
                    <div class="value">1,247</div>
                    <div class="change positive">↑ 12.3% vs last month</div>
                </div>

                <div class="stat-card">
                    <div class="icon">💰</div>
                    <div class="label">Monthly Revenue</div>
                    <div class="value">$12,450</div>
                    <div class="change positive">↑ 8.7% vs last month</div>
                </div>

                <div class="stat-card">
                    <div class="icon">📊</div>
                    <div class="label">ARR</div>
                    <div class="value">$149,400</div>
                    <div class="change positive">↑ 15.2% vs last quarter</div>
                </div>

                <div class="stat-card">
                    <div class="icon">🔥</div>
                    <div class="label">Active Subscriptions</div>
                    <div class="value">2,847</div>
                    <div class="change positive">↑ 234 this month</div>
                </div>

                <div class="stat-card">
                    <div class="icon">⚡</div>
                    <div class="label">API Calls Today</div>
                    <div class="value">156,789</div>
                    <div class="change positive">↑ 5.4% vs yesterday</div>
                </div>

                <div class="stat-card">
                    <div class="icon">💾</div>
                    <div class="label">Storage Used</div>
                    <div class="value">234.7 GB</div>
                    <div class="change">45.2% of quota</div>
                </div>
            </div>

            <!-- Dashboard Grid -->
            <div class="dashboard-grid">
                <!-- Revenue Chart -->
                <div class="panel">
                    <h2>📈 Revenue Trend</h2>
                    <div class="chart-placeholder">
                        Chart: Revenue over time
                        <br/>
                        <small>(Integrate Chart.js or similar)</small>
                    </div>
                </div>

                <!-- System Health -->
                <div class="panel">
                    <h2>🏥 System Health</h2>
                    <table class="table">
                        <tr>
                            <td>Status</td>
                            <td><span class="badge pro">Healthy</span></td>
                        </tr>
                        <tr>
                            <td>Uptime</td>
                            <td>99.94%</td>
                        </tr>
                        <tr>
                            <td>API Response</td>
                            <td>145ms</td>
                        </tr>
                        <tr>
                            <td>Error Rate</td>
                            <td>0.12%</td>
                        </tr>
                        <tr>
                            <td>CPU Usage</td>
                            <td>38.5%</td>
                        </tr>
                    </table>
                </div>
            </div>

            <!-- Recent Users -->
            <div class="panel">
                <h2>👥 Recent Users</h2>
                <table class="table">
                    <thead>
                        <tr>
                            <th>Email</th>
                            <th>Tier</th>
                            <th>API Calls</th>
                            <th>Spent</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>user1@example.com</td>
                            <td><span class="badge enterprise">Enterprise</span></td>
                            <td>45,678</td>
                            <td>$299.00</td>
                            <td>
                                <button class="action-btn">Edit</button>
                                <button class="action-btn danger">Delete</button>
                            </td>
                        </tr>
                        <tr>
                            <td>user2@example.com</td>
                            <td><span class="badge pro">Pro</span></td>
                            <td>12,345</td>
                            <td>$79.00</td>
                            <td>
                                <button class="action-btn">Edit</button>
                                <button class="action-btn danger">Delete</button>
                            </td>
                        </tr>
                        <tr>
                            <td>user3@example.com</td>
                            <td><span class="badge hobby">Hobby</span></td>
                            <td>3,456</td>
                            <td>$10.00</td>
                            <td>
                                <button class="action-btn">Edit</button>
                                <button class="action-btn danger">Delete</button>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <!-- Top Products -->
            <div class="panel" style="margin-top: 1.5rem;">
                <h2>🏆 Top Products by Revenue</h2>
                <table class="table">
                    <thead>
                        <tr>
                            <th>Product</th>
                            <th>Revenue</th>
                            <th>Users</th>
                            <th>Growth</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>Discord Bot Marketplace</td>
                            <td>$15,420</td>
                            <td>456</td>
                            <td class="change positive">↑ 23%</td>
                        </tr>
                        <tr>
                            <td>AI Agent Rental</td>
                            <td>$12,890</td>
                            <td>234</td>
                            <td class="change positive">↑ 18%</td>
                        </tr>
                        <tr>
                            <td>Consciousness API</td>
                            <td>$8,970</td>
                            <td>189</td>
                            <td class="change positive">↑ 12%</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>

        <script>
            // Load real data from API
            async function loadDashboardData() {
                try {
                    const token = localStorage.getItem('admin_token');
                    if (!token) {
                        window.location.href = '/auth/login?redirect=/admin/dashboard';
                        return;
                    }

                    const response = await fetch('/admin/stats', {
                        headers: {'Authorization': `Bearer ${token}`}
                    });

                    if (response.status === 403) {
                        alert('Admin privileges required');
                        window.location.href = '/';
                        return;
                    }

                    const data = await response.json();
                    console.log('Dashboard data:', data);
                    // Update UI with real data
                } catch (error) {
                    console.error('Failed to load dashboard data:', error);
                }
            }

            loadDashboardData();
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

# ============================================================================
# EXPORTS
# ============================================================================

__all__ = ["router"]
