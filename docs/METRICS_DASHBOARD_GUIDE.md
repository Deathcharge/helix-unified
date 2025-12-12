# 📊 Metrics Dashboard Guide

Comprehensive business intelligence dashboard for tracking all key SaaS metrics.

## Overview

The Metrics Dashboard provides real-time insights into:

- **User Growth**: Signups, DAU/MAU, activation rates
- **Revenue**: MRR, ARR, churn rate, ARPU
- **Product Usage**: API calls, agent sessions, top features
- **Service Health**: Error rates, API uptime
- **Customer Satisfaction**: NPS scores
- **Support**: Ticket volume, resolution times

## Quick Start

### 1. Database Setup

The metrics system uses new database tables. Initialize them:

```bash
# Run database migrations
python backend/database.py
```

This creates the following new tables:
- `user_activations` - Track user activation events
- `revenue_events` - Track subscription revenue
- `nps_surveys` - Net Promoter Score responses
- `support_tickets` - Customer support tickets
- `error_logs` - Application errors
- `health_checks` - Service health monitoring
- `daily_metrics` - Pre-calculated daily metrics

### 2. API Endpoints

Access metrics via the following endpoints:

```bash
# Comprehensive metrics summary
GET /api/metrics/summary?days=30

# Daily time series data
GET /api/metrics/daily?days=30

# Activation funnel
GET /api/metrics/activation-funnel?days=30

# Revenue breakdown by tier
GET /api/metrics/revenue-breakdown

# Support overview
GET /api/metrics/support-overview?days=30

# Error overview
GET /api/metrics/error-overview?days=7
```

### 3. Dashboard UI

The dashboard is available at:
- Development: `http://localhost:5173/metrics` (Vite dev server)
- Production: `https://your-domain.com/metrics`

Component location: `dashboards/helixai-dashboard/client/src/pages/MetricsDashboard.tsx`

## Tracked Metrics

### User Metrics
- **Signups**: New user registrations per day
- **DAU**: Daily Active Users (users with API activity)
- **MAU**: Monthly Active Users
- **Activation Rate**: % of users who complete key actions
- **Activation Funnel**:
  1. Profile completed
  2. First API call
  3. First agent session
  4. Fully activated

### Revenue Metrics
- **MRR**: Monthly Recurring Revenue
- **ARR**: Annual Recurring Revenue (MRR × 12)
- **Churn Rate**: % of customers who canceled
- **ARPU**: Average Revenue Per User
- **User Distribution**: Free, Pro, Workflow, Enterprise

### Usage Metrics
- **API Calls**: Total API requests
- **Agent Sessions**: AI agent conversations
- **Top Features**: Most-used endpoints with response times
- **Error Rate**: % of requests that error
- **API Uptime**: Service availability %

### Support Metrics
- **Open Tickets**: Current unresolved tickets
- **Avg Resolution Time**: Hours to resolve tickets
- **Tickets by Priority**: Urgent, High, Medium, Low
- **Tickets by Category**: Bug, Feature Request, Billing, General

### Satisfaction Metrics
- **NPS Score**: Net Promoter Score (-100 to +100)
- **Response Count**: Number of NPS survey responses

## Automated Tracking

### Middleware Auto-Tracking

The `MetricsMiddleware` automatically tracks:
- All API requests → `usage_logs` table
- Request errors → `error_logs` table
- Response times for performance monitoring
- User activity for DAU/MAU calculation

No manual tracking needed for basic usage metrics!

### Manual Event Tracking

For specific events, use the helper functions:

```python
from backend.saas.metrics_middleware import (
    track_user_activation,
    track_revenue_event,
    log_health_check,
    create_support_ticket,
    submit_nps_survey
)
from backend.database import get_db

# Track user activation
db = next(get_db())
track_user_activation(
    db=db,
    user_id="user_123",
    activation_type="first_api_call",
    metadata={"endpoint": "/api/chat"}
)

# Track revenue event
track_revenue_event(
    db=db,
    user_id="user_123",
    team_id=None,
    event_type="subscription_started",
    amount=29.00,
    billing_period="monthly",
    stripe_event_id="evt_..."
)

# Create support ticket
ticket_id = create_support_ticket(
    db=db,
    user_id="user_123",
    subject="API Error",
    description="Getting 500 errors...",
    priority="high",
    category="bug"
)

# Submit NPS survey
submit_nps_survey(
    db=db,
    user_id="user_123",
    score=9,  # 0-10
    feedback="Great product!",
    trigger="dashboard"
)

# Log health check
log_health_check(
    db=db,
    service_name="api",
    status="healthy",
    response_time_ms=45.2
)
```

## Daily Metrics Calculation

For optimal dashboard performance, daily metrics are pre-calculated and cached.

### Manual Calculation

```bash
# Calculate for yesterday
python scripts/calculate_daily_metrics.py

# Calculate for specific date
python scripts/calculate_daily_metrics.py --date 2025-12-10

# Recalculate last 7 days
python scripts/calculate_daily_metrics.py --days 7
```

### Automated Cron Job

Add to your crontab or Railway scheduler:

```bash
# Run daily at 1 AM UTC
0 1 * * * cd /app && python scripts/calculate_daily_metrics.py >> /var/log/metrics.log 2>&1
```

Or trigger via API:

```bash
POST /api/metrics/calculate-daily?date=2025-12-10
```

## Integration with Analytics Tools

### PostHog Integration

```python
# Install PostHog
pip install posthog

# Track events to PostHog
import posthog

posthog.api_key = os.getenv('POSTHOG_API_KEY')

# Capture event
posthog.capture(
    distinct_id=user_id,
    event='api_call',
    properties={
        'endpoint': '/api/chat',
        'response_time_ms': 123
    }
)
```

### Mixpanel Integration

```python
# Install Mixpanel
pip install mixpanel

# Track to Mixpanel
from mixpanel import Mixpanel

mp = Mixpanel(os.getenv('MIXPANEL_TOKEN'))

mp.track(user_id, 'API Call', {
    'endpoint': '/api/chat',
    'tier': 'pro'
})
```

### Custom Export

Use the existing export endpoints:

```bash
# Export usage data
GET /api/analytics/export/usage?format=csv&days=30

# Export agent sessions
GET /api/analytics/export/agent-sessions?format=json&days=30
```

## Performance Optimization

### Caching Strategy

- Daily metrics are pre-calculated and cached in `daily_metrics` table
- Dashboard queries use cached data (fast!)
- Cron job updates cache daily (slow calculation happens offline)

### Indexing

All metrics tables have indexes on:
- `user_id` - Fast user queries
- `created_at` / `occurred_at` - Fast date range queries
- Foreign keys - Fast joins

### Query Optimization

- Use date range queries with indexes
- Limit results with `.limit()`
- Use aggregations in database, not Python
- Batch operations when possible

## Troubleshooting

### No Data Showing

1. Check if middleware is enabled:
   ```bash
   # Should see in logs:
   # ✅ Metrics Collection Middleware enabled
   ```

2. Verify database tables exist:
   ```bash
   python backend/database.py
   ```

3. Check if data is being logged:
   ```sql
   SELECT COUNT(*) FROM usage_logs;
   SELECT COUNT(*) FROM daily_metrics;
   ```

### Slow Dashboard Loading

1. Run daily metrics calculation:
   ```bash
   python scripts/calculate_daily_metrics.py --days 30
   ```

2. Verify cache is working:
   ```sql
   SELECT date, daily_active_users, mrr FROM daily_metrics ORDER BY date DESC LIMIT 7;
   ```

### Incorrect Metrics

1. Recalculate with force flag:
   ```bash
   python scripts/calculate_daily_metrics.py --days 7 --force
   ```

2. Check data quality:
   ```sql
   -- Users with valid subscriptions
   SELECT subscription_tier, COUNT(*) FROM users GROUP BY subscription_tier;

   -- Recent activity
   SELECT DATE(timestamp), COUNT(*) FROM usage_logs
   WHERE timestamp > NOW() - INTERVAL '7 days'
   GROUP BY DATE(timestamp);
   ```

## Security & Privacy

- Metrics data includes user IDs but not PII
- API endpoints should require authentication
- Add rate limiting to prevent abuse
- Consider GDPR compliance for user data
- Support data deletion requests

## Future Enhancements

Planned features:
- [ ] Real-time metrics via WebSockets
- [ ] Custom metric definitions
- [ ] Metric alerts and notifications
- [ ] Funnel analysis builder
- [ ] Cohort analysis
- [ ] Revenue forecasting
- [ ] A/B test tracking
- [ ] Custom dashboard builder

## API Reference

See full API documentation at:
- Swagger UI: `/docs`
- ReDoc: `/redoc`
- OpenAPI JSON: `/openapi.json`

## Support

For issues or questions:
- GitHub Issues: [helix-unified/issues](https://github.com/Deathcharge/helix-unified/issues)
- Email: support@helix.ai
- Discord: [Join our community](https://discord.gg/helix)

---

**Version**: 17.4
**Last Updated**: 2025-12-12
**Author**: Claude AI Assistant
