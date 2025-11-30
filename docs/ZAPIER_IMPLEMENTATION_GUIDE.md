# Zapier Workflow Implementation Guide

**Version:** 1.0  
**Last Updated:** November 18, 2025  
**Status:** Production Ready

---

## Table of Contents

1. [Quick Start](#quick-start)
2. [Workflow Templates](#workflow-templates)
3. [Implementation Steps](#implementation-steps)
4. [Configuration](#configuration)
5. [Testing](#testing)
6. [Monitoring](#monitoring)
7. [Troubleshooting](#troubleshooting)

---

## Quick Start

### 1. Choose a Workflow Template

We provide 8 production-ready templates in `templates/zapier-workflows/`:

| Template | Use Case | Complexity |
|----------|----------|-----------|
| 01-simple-agent-execution | Single agent task | ⭐ |
| 02-consciousness-routing | Route by consciousness level | ⭐⭐ |
| 03-sequential-chain | Multi-step sequential workflow | ⭐⭐ |
| 04-parallel-execution | Parallel agent execution | ⭐⭐ |
| 05-error-handling | Retry with exponential backoff | ⭐⭐ |
| 06-incident-response | Incident detection & resolution | ⭐⭐⭐ |
| 07-cross-instance-coordination | Multi-instance coordination | ⭐⭐⭐ |
| 08-multi-agent-orchestration | 14-agent full orchestration | ⭐⭐⭐⭐ |

### 2. Create Zapier Workflow

1. Log in to [Zapier](https://zapier.com)
2. Click "Create Zap"
3. Choose "Webhooks by Zapier" as trigger
4. Click "Catch Raw Hook"
5. Copy the webhook URL

### 3. Import Template

```bash
# Copy template to your Zapier workflow
cat templates/zapier-workflows/01-simple-agent-execution.json
```

### 4. Configure Credentials

Set these environment variables in Zapier:

```
API_TOKEN=sk_live_your_token_here
API_BASE_URL=https://api.helix-primary.manus.space
INSTANCE_ID=helix-primary
```

### 5. Test Workflow

```bash
curl -X POST https://hooks.zapier.com/hooks/catch/YOUR_ID/simple-agent-task \
  -H "Content-Type: application/json" \
  -d '{
    "agent_id": "research-agent",
    "task_type": "data_retrieval",
    "consciousness_level": 5,
    "payload": {"query": "test data"},
    "callback_url": "https://your-callback-url.com"
  }'
```

---

## Workflow Templates

### Template 1: Simple Agent Execution

**File:** `01-simple-agent-execution.json`

**Flow:**
```
Webhook → Execute Agent → Store Result → Send Response
```

**Best For:**
- Single agent tasks
- Quick integrations
- Testing agent connectivity

**Example Request:**
```json
{
  "agent_id": "research-agent",
  "task_type": "data_retrieval",
  "consciousness_level": 5,
  "payload": {"query": "find recent metrics"},
  "callback_url": "https://your-app.com/webhook"
}
```

### Template 2: Consciousness-Level Routing

**File:** `02-consciousness-routing.json`

**Flow:**
```
Webhook → Check Consciousness Level → Route to Agent → Execute
```

**Best For:**
- Dynamic agent selection
- Complexity-based routing
- Adaptive workflows

**Example Request:**
```json
{
  "consciousness_level": 7,
  "task_type": "strategy_planning",
  "payload": {"goal": "optimize performance"},
  "callback_url": "https://your-app.com/webhook"
}
```

### Template 3: Sequential Chain

**File:** `03-sequential-chain.json`

**Flow:**
```
Research → Analysis → Synthesis → Validation → Result
```

**Best For:**
- Multi-stage data processing
- Complex analysis pipelines
- Quality assurance workflows

**Example Request:**
```json
{
  "input_data": {"raw_data": "..."},
  "callback_url": "https://your-app.com/webhook"
}
```

### Template 4: Parallel Execution

**File:** `04-parallel-execution.json`

**Flow:**
```
Research ─┐
Analysis  ├→ Aggregate → Result
Validation┘
```

**Best For:**
- Independent analyses
- Performance optimization
- Multi-perspective evaluation

**Example Request:**
```json
{
  "payload": {"data": "..."},
  "callback_url": "https://your-app.com/webhook"
}
```

### Template 5: Error Handling & Retry

**File:** `05-error-handling.json`

**Flow:**
```
Execute → Check Success → Retry (up to 3x) → Final Result
```

**Best For:**
- Unreliable connections
- Transient failures
- Production workflows

**Retry Strategy:**
- Exponential backoff: 2s, 4s, 8s
- Max 3 retries
- Graceful failure handling

**Example Request:**
```json
{
  "agent_id": "research-agent",
  "task_type": "data_retrieval",
  "consciousness_level": 5,
  "payload": {"query": "..."},
  "callback_url": "https://your-app.com/webhook",
  "error_callback_url": "https://your-app.com/error"
}
```

### Template 6: Incident Response

**File:** `06-incident-response.json`

**Flow:**
```
Detect → Analyze → Escalate → Remediate → Verify → Report
```

**Best For:**
- Automated incident response
- System monitoring
- Emergency procedures

**Severity Levels:**
- Critical: Auto-remediation enabled
- High: Manual review required
- Medium: Logged for review

**Example Request:**
```json
{
  "incident_id": "INC-001",
  "metrics": {
    "cpu": 95,
    "memory": 88,
    "error_rate": 12.5
  },
  "callback_url": "https://your-app.com/webhook"
}
```

### Template 7: Cross-Instance Coordination

**File:** `07-cross-instance-coordination.json`

**Flow:**
```
Sync State → Plan Workflow → Execute Distributed → Aggregate → Report
```

**Best For:**
- Multi-instance coordination
- Distributed workflows
- Ecosystem-wide operations

**Example Request:**
```json
{
  "instances": [
    "helix-primary",
    "helix-workflows",
    "helix-agents"
  ],
  "goal": "sync metrics across ecosystem",
  "callback_url": "https://your-app.com/webhook"
}
```

### Template 8: Multi-Agent Orchestration

**File:** `08-multi-agent-orchestration.json`

**Flow:**
```
Phase 1: Research (Research + Learning)
Phase 2: Analysis (Analysis + Performance)
Phase 3: Synthesis (Synthesis + Optimization)
Phase 4: Validation (Validation + Security)
Phase 5: Execution (Orchestration + Integration)
Phase 6: Documentation
```

**Best For:**
- Complex multi-agent workflows
- Full ecosystem orchestration
- Advanced analysis pipelines

**Example Request:**
```json
{
  "goal": "comprehensive system analysis",
  "consciousness_level": 8,
  "input_data": {"system_state": "..."},
  "callback_url": "https://your-app.com/webhook"
}
```

---

## Implementation Steps

### Step 1: Set Up Zapier Account

1. Create Zapier account at https://zapier.com
2. Create new Zap
3. Select "Webhooks by Zapier" as trigger
4. Copy webhook URL

### Step 2: Configure API Credentials

In Zapier workflow settings:

```
API_TOKEN = sk_live_your_token_here
API_BASE_URL = https://api.helix-primary.manus.space
INSTANCE_ID = helix-primary
```

### Step 3: Add Workflow Steps

For each step in the template:

1. Click "+" to add action
2. Search for action type (HTTP, Formatter, etc.)
3. Configure with template parameters
4. Map previous step outputs to inputs

### Step 4: Configure Webhooks

For callback URLs:

```
https://your-app.com/api/webhooks/zapier
```

### Step 5: Enable Error Handling

For each HTTP step:

1. Click "Options"
2. Enable "Catch Errors"
3. Configure error path

### Step 6: Test Workflow

```bash
# Send test request
curl -X POST https://hooks.zapier.com/hooks/catch/YOUR_ID \
  -H "Content-Type: application/json" \
  -d @test-payload.json
```

---

## Configuration

### Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `API_TOKEN` | Bearer token for API auth | `sk_live_...` |
| `API_BASE_URL` | Instance API base URL | `https://api.helix-primary.manus.space` |
| `INSTANCE_ID` | Instance identifier | `helix-primary` |
| `WEBHOOK_URL` | Zapier webhook URL | `https://hooks.zapier.com/...` |

### Consciousness Levels

| Level | Name | Capabilities | Timeout |
|-------|------|-------------|---------|
| 1-2 | Minimal | Basic queries | 5s |
| 3-4 | Basic | Data processing | 15s |
| 5-6 | Intelligent | Analysis & routing | 30s |
| 7-8 | Autonomous | Strategy & execution | 60s |
| 9-10 | Transcendent | Advanced synthesis | 180s |

### Retry Configuration

```json
{
  "max_retries": 3,
  "backoff_strategy": "exponential",
  "initial_delay_seconds": 2,
  "max_delay_seconds": 8
}
```

---

## Testing

### Unit Testing

Test individual steps:

```bash
# Test agent execution
curl -X POST https://api.helix-primary.manus.space/api/agents/execute \
  -H "Authorization: Bearer $API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "agent_id": "research-agent",
    "task_type": "data_retrieval",
    "consciousness_level": 5,
    "payload": {"test": true}
  }'
```

### Integration Testing

Test full workflow:

```bash
# Send to Zapier webhook
curl -X POST $ZAPIER_WEBHOOK_URL \
  -H "Content-Type: application/json" \
  -d @test-payload.json
```

### Load Testing

Test with multiple concurrent requests:

```bash
# Using Apache Bench
ab -n 100 -c 10 -p test-payload.json \
  -T application/json \
  $ZAPIER_WEBHOOK_URL
```

---

## Monitoring

### Zapier Dashboard

1. Log in to Zapier
2. View "Zap History"
3. Check execution status
4. Review error logs

### Metrics to Track

- **Execution Time:** Average, P95, P99
- **Success Rate:** % of successful executions
- **Error Rate:** % of failed executions
- **Agent Utilization:** Tasks per agent
- **Queue Depth:** Pending tasks

### Logging

All executions are logged to:

```
/var/log/helix/zapier-executions.log
```

Format:
```
[TIMESTAMP] [WORKFLOW_ID] [STATUS] [AGENT_ID] [DURATION_MS]
```

---

## Troubleshooting

### Webhook Not Triggering

**Problem:** Zapier workflow not executing

**Solutions:**
1. Verify webhook URL is correct
2. Check Zapier account is active
3. Test with curl:
   ```bash
   curl -X POST $WEBHOOK_URL -d '{"test": true}'
   ```
4. Check Zapier logs for errors

### Agent Not Found

**Problem:** "Agent not found" error

**Solutions:**
1. Verify agent ID spelling
2. Check agent roster: `GET /api/agents`
3. Verify agent is online
4. Check consciousness level requirement

### Timeout Errors

**Problem:** Workflow times out

**Solutions:**
1. Reduce consciousness level
2. Use parallel execution instead of sequential
3. Optimize agent payload size
4. Check API response times

### Authentication Failures

**Problem:** "Unauthorized" or "Invalid token" error

**Solutions:**
1. Verify API token is correct
2. Check token hasn't expired
3. Verify token has required permissions
4. Generate new token if needed

### High Latency

**Problem:** Slow workflow execution

**Solutions:**
1. Use parallel execution for independent tasks
2. Cache frequently accessed data
3. Optimize database queries
4. Consider consciousness level reduction
5. Check network connectivity

---

## Best Practices

### 1. Error Handling

Always implement retry logic:

```json
{
  "max_retries": 3,
  "exponential_backoff": true,
  "error_callbacks": true
}
```

### 2. Monitoring

Log all executions:

```json
{
  "logging_enabled": true,
  "log_level": "info",
  "metrics_tracking": true
}
```

### 3. Security

- Never hardcode API tokens
- Use environment variables
- Rotate tokens regularly
- Enable HTTPS for all URLs

### 4. Performance

- Use parallel execution when possible
- Implement caching
- Optimize payload sizes
- Monitor execution times

### 5. Testing

- Test each workflow before production
- Use staging environment first
- Monitor error rates
- Set up alerts

---

## Support

For issues or questions:

1. Check [Troubleshooting](#troubleshooting) section
2. Review workflow logs
3. Test with curl
4. Check Zapier documentation
5. Contact support team

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | Nov 18, 2025 | Initial release with 8 templates |


